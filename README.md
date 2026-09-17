# Leader · 思（thinkV2）工程指挥者

换电脑后从 **[交接入口](handoff/START-HERE.md)** 开始。此仓库保存调度规则、冻结合同、历史账本、审查记录和恢复指南，不是产品源码仓库。

| 角色 | 专用仓库 |
|---|---|
| 指挥者 | https://github.com/3956ray/Leader |
| 产品经理 | https://github.com/3956ray/ProductManager |
| 开发者 | https://github.com/3956ray/Developer |

当前产品提交：`88d38616c5a5947d4ca798d4039c6368fa465624`。当前单 `V2-REMINDERS-USABILITY-001` **AWAITING_REVIEW**，开发者已交付，Leader 独立127项主机测试通过，但尚未正式接受。上一单笔记UI `8a98e09` 已接受。

## 关键入口

- [AGENTS.md](AGENTS.md)：单任务、单Checkpoint、隐私与验收规则。
- [权威账本](orchestration/loop-ledger.json)、[当前任务](orchestration/current-task.json)、[状态](orchestration/state.json)。状态视图由工具生成，不能手改成通过。
- [完整需求与缺口](orchestration/thinkV2-completion-matrix.md)。历史旧think不等于thinkV2验收。
- [路径与正式来源快照](handoff/path-map.json)：保留原文SHA，适用于新机器离线核验。
- `scripts/leader_loop.py`：状态转换；`scripts/leader_check.py`：原路径环境的派单前检查。
- `scripts/handoff_check.py`：跨机器交接完整性检查，不派单、不自动接受结果。

此仓库公开。未包含账户令牌、API密钥、全局Codex聊天数据库、父亲真实数据、录音、其他独立项目或自动启动任务。
