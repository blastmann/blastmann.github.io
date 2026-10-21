#!/usr/bin/env python3
"""Import one data-only candidate, rebuild the archive, and verify publication."""
import argparse
import datetime as dt
import hashlib
import html
import json
import os
from pathlib import Path
import re
import subprocess
import time
import urllib.request

ROOT = Path('source/browser-ai-daily')

def git(*args):
    return subprocess.check_output(['git', *args], text=True).strip()

def article_path(date):
    dt.date.fromisoformat(date)
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', date):
        raise ValueError('Expected ISO date')
    return ROOT / date[:4] / date[5:7] / (date + '.html')

def validate(text, date):
    if len(text.encode()) > 500_000:
        raise ValueError('Article exceeds 500 KB')
    header, body = text.split('\n---\n', 1)
    if not header.startswith('---\n') or not re.search(r'^layout: page$', header, re.M):
        raise ValueError('Article must use the existing page layout')
    if date not in header or '<h2>' not in body or 'https://' not in body:
        raise ValueError('Missing date, sections, or sources')
    if re.search(r'<\s*(script|iframe|object|embed|style|link|base)\b|\bon\w+\s*=|javascript\s*:', body, re.I):
        raise ValueError('Active content is not permitted in daily articles')
    return body

def archive():
    index = ROOT / 'index.html'
    text = index.read_text()
    start, tail = text.split('<ul>', 1)
    _, end = tail.split('</ul>', 1)
    # Preserve editorial descriptions for existing entries, but derive membership from files.
    entries = {m.group(1): m.group(0) for m in re.finditer(r'<li><strong>(\d{4}-\d{2}-\d{2})</strong>.*?</li>', text, re.S)}
    rows = []
    for path in sorted(ROOT.glob('*/*/????-??-??.html'), reverse=True):
        date = path.stem
        if path != article_path(date):
            raise ValueError(f'Misplaced article: {path}')
        row = entries.get(date)
        if row is None:
            body = validate(path.read_text(), date)
            heading = re.search(r'<h[23]>(.*?)</h[23]>', body, re.S)
            summary = html.escape(html.unescape(re.sub('<[^>]+>', '', heading.group(1))))
            row = f'<li><strong>{date}</strong> — {summary}。<br><a href="{date[:4]}/{date[5:7]}/{date}.html">阅读日报</a></li>'
        rows.append(row)
    index.write_text(start + '<ul>\n' + '\n'.join(rows) + '\n</ul>' + end)

def import_candidate(sha, date):
    if not re.fullmatch('[0-9a-f]{40}', sha):
        raise ValueError('Candidate must be a full commit SHA')
    path = article_path(date)
    subprocess.run(['git', 'fetch', '--no-tags', 'origin', sha], check=True)
    parents = git('show', '-s', '--format=%P', sha).split()
    if len(parents) != 1:
        raise ValueError('Candidate must have one parent')
    subprocess.run(['git', 'merge-base', '--is-ancestor', parents[0], 'HEAD'], check=True)
    changed = set(git('diff', '--name-only', parents[0], sha).splitlines())
    if (changed and str(path) not in changed) or not changed <= {str(path), str(ROOT / 'index.html')}:
        raise ValueError(f'Candidate changes paths outside this daily: {changed}')
    mode = git('ls-tree', sha, '--', str(path)).split()[0]
    if mode != '100644':
        raise ValueError('Article must be a regular file')
    content = subprocess.check_output(['git', 'show', f'{sha}:{path}'], text=True)
    validate(content, date)
    if path.exists() and path.read_text() != content:
        raise ValueError('Existing article differs; explicit editorial correction required')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    archive()
    subprocess.run(['git', 'add', '--', str(path), str(ROOT / 'index.html')], check=True)
    if subprocess.run(['git', 'diff', '--cached', '--quiet']).returncode == 0:
        print('Already imported; continuing with build and deployment')
        return
    subprocess.run(['git', '-c', 'user.name=github-actions[bot]', '-c', 'user.email=41898282+github-actions[bot]@users.noreply.github.com', 'commit', '-m', f'daily: publish {date}', '-m', f'Candidate: {sha}'], check=True)
    # A concurrent writer causes a clean failure; never overwrite it or force push.
    subprocess.run(['git', 'push', 'origin', 'HEAD:refs/heads/source'], check=True)

def receipt():
    latest = max(p.stem for p in ROOT.glob('*/*/????-??-??.html'))
    relative = str(article_path(latest).relative_to('source'))
    paths = ['browser-ai-daily/index.html', relative]
    hashes = {}
    for name in paths:
        data = (Path('public') / name).read_bytes()
        if latest.encode() not in data:
            raise ValueError(f'Generated page missing latest date: {name}')
        hashes[name] = hashlib.sha256(data).hexdigest()
    payload = {'source_sha': git('rev-parse', 'HEAD'), 'latest_date': latest, 'sha256': hashes}
    (Path('public/browser-ai-daily/publication.json')).write_text(json.dumps(payload, indent=2) + '\n')
    print(json.dumps(payload))

def verify(base, sha):
    base = base.rstrip('/')
    def fetch(path):
        request = urllib.request.Request(f'{base}/{path}?publication={sha}', headers={'Cache-Control': 'no-cache', 'User-Agent': 'daily-publication-verifier'})
        with urllib.request.urlopen(request, timeout=20) as response:
            return response.read()
    for attempt in range(18):
        try:
            data = json.loads(fetch('browser-ai-daily/publication.json'))
            if data['source_sha'] != sha:
                raise ValueError('Pages still serves a previous source revision')
            for path, expected in data['sha256'].items():
                if hashlib.sha256(fetch(path)).hexdigest() != expected:
                    raise ValueError(f'Online content does not match build: {path}')
            print(f'Verified public pages for {sha}: {data["latest_date"]}')
            return
        except Exception as error:
            print(f'Attempt {attempt + 1}: {error}', flush=True)
            if attempt == 17:
                raise
            time.sleep(10)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('operation', choices=['import', 'receipt', 'verify'])
    parser.add_argument('--sha', default=os.environ.get('CANDIDATE_SHA', ''))
    parser.add_argument('--date', default=os.environ.get('REPORT_DATE', ''))
    parser.add_argument('--url', default='https://blastmann.github.io')
    args = parser.parse_args()
    if args.operation == 'import':
        import_candidate(args.sha, args.date)
    elif args.operation == 'receipt':
        receipt()
    else:
        verify(args.url, args.sha)
