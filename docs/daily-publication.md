# 日报发布机制

只提交 `source`；Pages 由 Actions 直接部署产物，不再向 `master` 写入生成文件。保留 Hexo 和现有主题。

## 每日发布

生成日报 HTML（现有 `layout: page` front matter、当天日期、正文和来源），然后在已登录 GitHub CLI 的环境执行：

```sh
tools/daily/submit-daily.sh 2026-10-22 /path/to/2026-10-22.html
```

此命令只创建数据候选 commit，不移动任何分支；随后显式派发 `source` 上已有的 `deploy.yml`。不需要连接器执行 update_ref，不依赖 push 递归触发工作流，不新增长期 PAT 或 API 密钥。GitHub CLI 凭据需有仓库写入及 Actions dispatch 权限。

已有候选 commit（例如恢复未挂接日报）可直接派发：

```sh
gh workflow run deploy.yml --repo blastmann/blastmann.github.io --ref source \
  -f candidate_sha=65ae1e13d49333de80b0dc8fcf39b87ecc16eea6 \
  -f report_date=2026-10-21
```

原有定时调研任务仍负责调研和生成内容；它的发布步骤应调用上述命令。此仓库工作流不会自行生成或编造日报，也不依赖默认分支上的 cron。仅有 GitHub 连接器、无法派发工作流的运行环境不能直接调用此入口，需转到可执行该命令的任务环境。

## 权限和校验

- 仅 `source` ref 可运行；只有导入 job 有 `contents: write`。构建只读；部署 job 仅 `pages: write` / `id-token: write`，使用临时 `GITHUB_TOKEN`。
- 候选必须是单父提交，父提交属于当前 source 历史，改动仅限指定日期日报与聚合页。绝不 checkout 或运行候选中的代码，忽略候选聚合页并从实际文件重新生成。
- 拒绝路径越界、符号链接、主动脚本和覆盖已发布的不同内容。日期、大小、页面布局、章节和来源做基本检查。正文事实仍由调研任务负责。
- 已导入内容可安全重复提交；自动按日期倒序更新聚合页，保留已有摘要。只允许普通快进 push，遇到其他写入失败退出，可重试整个派发。全流程串行，不取消正在执行的发布。
- 同一工作流直接构建并部署，解决 GITHUB_TOKEN 提交不再触发后续工作流的问题。
- 生成 `browser-ai-daily/publication.json`，记录实际构建 source SHA、最新日期及日报/聚合页 SHA-256。部署后从公开 HTTPS 地址读取并逐字节核对；失败时整个 run 标红，不能仅凭 commit 或 dispatch 成功宣布发布。

## 查看结果与重试

```sh
gh run list --repo blastmann/blastmann.github.io --workflow deploy.yml --limit 5
gh run view RUN_ID --repo blastmann/blastmann.github.io
# 不带候选参数，仅重新构建部署当前 source
gh workflow run deploy.yml --repo blastmann/blastmann.github.io --ref source
```

线上回执：https://blastmann.github.io/browser-ai-daily/publication.json

失败证据保留在 Actions 日志；沿用 GitHub 原生工作流失败通知。未额外安装通知或定时服务。若需要改正文，按正常 source 编辑提交处理，候选导入接口有意不允许覆盖。

## 2026-10-21 故障证据

- 原 source HEAD：`840b95e78306255758881426537f3a66e77b7960`。
- 候选：`65ae1e13d49333de80b0dc8fcf39b87ecc16eea6`，父提交等于原 HEAD，差异只有当日日报及聚合页两文件。
- source 无分支保护；仓库 rulesets 为空。旧部署成功，本次候选没有工作流记录，因为创建 commit 不会触发 push。
- 原对话报告连接器写入安全检查拦截；其内部拒绝细节未在可读对话中保留，不能声称具体规则或 GitHub HTTP 错误码。
- 本次显式带 expected_sha、force=false 的 update_ref 成功，证明没有 GitHub 侧保护阻止快进；无强推，无删除历史。
- 旧方案 Pages 来源为 master，Actions 使用 GITHUB_TOKEN 向 master 发布，存在二次触发限制。现改为 artifact 直接部署；Pages build_type 改为 workflow，环境允许 source。此设置变更不写任何分支。

如果回退工作流，必须同时恢复 Pages 的 legacy/master 发布配置；旧 master 产物仍保留，但已经不作为新部署来源。
