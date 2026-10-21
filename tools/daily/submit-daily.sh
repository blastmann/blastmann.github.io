#!/usr/bin/env bash
# Submit data as an unreferenced commit, then let the trusted source workflow import it.
set -euo pipefail
if [[ $# != 2 ]]; then
  echo 'Usage: tools/daily/submit-daily.sh YYYY-MM-DD /path/to/article.html' >&2
  exit 2
fi
report_date=$1
article_file=$2
repo=blastmann/blastmann.github.io
script_dir=$(cd -- "$(dirname -- "$0")" && pwd)
python3 - "$script_dir" "$report_date" "$article_file" <<'PY'
import sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
from daily import article_path, validate
article_path(sys.argv[2])
validate(Path(sys.argv[3]).read_text(), sys.argv[2])
PY
payload_dir=$(mktemp -d)
trap 'rm -rf "$payload_dir"' EXIT
base=$(gh api "repos/$repo/git/ref/heads/source" --jq '.object.sha')
base_tree=$(gh api "repos/$repo/git/commits/$base" --jq '.tree.sha')
python3 - "$article_file" > "$payload_dir/blob.json" <<'PY'
import json, sys
from pathlib import Path
print(json.dumps({'content': Path(sys.argv[1]).read_text(), 'encoding': 'utf-8'}))
PY
blob=$(gh api --method POST "repos/$repo/git/blobs" --input "$payload_dir/blob.json" --jq '.sha')
python3 - "$base_tree" "$blob" "$report_date" > "$payload_dir/tree.json" <<'PY'
import json, sys
base, blob, date = sys.argv[1:]
print(json.dumps({'base_tree': base, 'tree': [{'path': f'source/browser-ai-daily/{date[:4]}/{date[5:7]}/{date}.html', 'mode': '100644', 'type': 'blob', 'sha': blob}]}))
PY
tree=$(gh api --method POST "repos/$repo/git/trees" --input "$payload_dir/tree.json" --jq '.sha')
python3 - "$tree" "$base" "$report_date" > "$payload_dir/commit.json" <<'PY'
import json, sys
print(json.dumps({'tree': sys.argv[1], 'parents': [sys.argv[2]], 'message': f'daily candidate: {sys.argv[3]}'}))
PY
candidate=$(gh api --method POST "repos/$repo/git/commits" --input "$payload_dir/commit.json" --jq '.sha')
echo "Candidate: $candidate"
gh workflow run deploy.yml --repo "$repo" --ref source -f "candidate_sha=$candidate" -f "report_date=$report_date"
echo 'Submission accepted. Check Actions for import, deployment, and public verification; dispatch alone is not publication success.'
