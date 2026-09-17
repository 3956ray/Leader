# 健身房小程序独立调度边界

用户指定本任务负责小程序调研、PRD、Checkpoint、开发派发与验收。当前目录只保存本项目调度记录。上层 Android 项目的源码路径、角色路由、Checkpoint 和特定功能限制不适用于本小程序；不得修改上层 orchestration 或 thinkV2。

保留单任务串行、正式文档优先、证据验收和第三方安全门禁。会员入口已获用户确定；具体身份验证方案按本项目批准 PRD 实现。真实数据接入、公开发布不得凭模拟测试视为通过。

每次读取本目录 orchestration 三份配置，检查对应 PM/dev 状态及目标仓库，派单前运行 `python3 scripts/leader_check.py --root projects/gym-miniapp`。未知源码路径时不得向任何既有产品目录派发代码修改。

换机路径与角色先按仓库根 MIGRATION.md 恢复；检查命令从 Leader 根运行。原上层 Android 描述仅历史背景，本仓库现为专用指挥者。
