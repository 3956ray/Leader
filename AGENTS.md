# 指挥者工作区

本仓库只保存工程调度、决策、验收与迁移信息，不保存产品源码。
当前迁移项目：单店健身房微信小程序，入口 `projects/gym-miniapp/`。
优先读 `MIGRATION.md`、`projects/gym-miniapp/HANDOFF.md` 和该目录 `AGENTS.md`。
PM 真源在兄弟仓库 ProductManager；产品源码在 Developer 的 gym-miniapp 分支，独立工作树为兄弟目录 gym-miniapp。
不得把其他项目的路径、任务ID、产品限制或验收状态用于本项目。

## 执行规则

- 中文沟通；编码、审查、重构优先使用 `.agents/skills/karpathy-guidelines/SKILL.md`。
- 一次一个明确 Checkpoint 任务；开发者未完成时不重复派发。
- 用户决定优先；正式产品文档是需求真源，聊天报告不能替代验收证据。
- 指挥者默认不改产品源码。验收后才记 ACCEPTED，未验证层必须明确。
- 派发前读取项目三份 orchestration 配置，检查 PM/dev 是否空闲、源码分支与工作区，再运行 `python3 scripts/leader_check.py --root projects/gym-miniapp`。
- 换机后旧任务ID只作历史引用，重新绑定三个当前任务后才恢复派发；默认不启用自动调度。
- 不上传运行数据库、密钥、真实会员数据、登录状态；不把演示通过算作官方身份/真机/门店验收。
