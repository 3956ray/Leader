# Leader 指挥者仓库

换机后请按项目选择交接入口；本仓库不存产品源码或账号登录状态。

| 项目 | 恢复入口 | 调度状态 |
|---|---|---|
| 思（thinkV2）Android | [换机交接](handoff/START-HERE.md) | 根目录`orchestration/`；提醒UI交付88d3861待Leader最终验收 |
| 健身房微信小程序 | [换机步骤](MIGRATION.md)、[当前交接](projects/gym-miniapp/HANDOFF.md) | `projects/gym-miniapp/orchestration/` |

角色仓库：[Leader](https://github.com/3956ray/Leader)、[PM](https://github.com/3956ray/ProductManager)、[dev](https://github.com/3956ray/Developer)。

thinkV2保留原始冻结账本与正式来源快照；执行`python3 scripts/handoff_check.py`核验完整性。产品完整目标和缺口见[验收矩阵](orchestration/thinkV2-completion-matrix.md)。旧think证据不等于thinkV2通过，旧任务ID/本机路径需要重绑。

用户2026-09-17在获知公开内部账本、路径与任务元数据风险后明确批准推送；凭据、真实私人数据与受限模型资产仍不公开。原始受限开发备份须私下转移，详见Developer交接。
