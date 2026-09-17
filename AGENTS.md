# 指挥者工作区

本仓库仅保存调度、产品决策、验收和迁移资料。先按用户当前项目选择入口，禁止混用项目状态或任务ID。

- 思（thinkV2）Android：`handoff/START-HERE.md`、`handoff/THINK-AGENTS.md`，调度目录为根目录`orchestration/`。
- 健身房微信小程序：`MIGRATION.md`、`projects/gym-miniapp/HANDOFF.md`、`projects/gym-miniapp/AGENTS.md`；调度目录为`projects/gym-miniapp/orchestration/`。

中文沟通；编码/审查优先使用`.agents/skills/karpathy-guidelines/SKILL.md`。一次一个明确Checkpoint，开发者运行中不重复派发。用户决定优先，正式产品文档为真源，聊天不代替证据。Leader默认不改产品源码，验收后才记ACCEPTED。
换机需重绑当前任务/路径，旧ID仅历史；默认不恢复自动调度。不得上传密钥、登录状态、真实私人数据或未获公开分发许可的资产。
派单前运行对应项目的leader_check；thinkV2迁移先运行`python3 scripts/handoff_check.py`，其成功不代表产品验收。
