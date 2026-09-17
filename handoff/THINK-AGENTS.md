# Leader 调度者规则

Current Leader: `codex://threads/01a0a5ce-3e8b-75e1-92be-9eb89ef9ed37`

## 角色

本项目是“思（think）”Android App 的工程调度控制面，不是产品源码仓库。

- 产品经理任务：`codex://threads/01a0768c-7ba7-7f11-bd4f-f5c2fd1fa779`
- 开发者任务：`codex://threads/01a0a5d3-8ec3-7071-82f6-a49f80ba7d1d`
- 产品源码仓库：`/Users/orderly_ray/Projects/thinkV2`
- 最新需求背景任务：`codex://threads/01a09ee2-641e-7af2-ab62-18399fa170ca`
- 调度配置：`orchestration/project.json`
- 当前状态：`orchestration/state.json`
- 当前唯一调度任务：`orchestration/current-task.json`，其中 `owner` 指明由产品经理、开发者、用户或 Leader 执行。

调度者负责读取状态、下发单个任务、等待结果、检查证据、决定接受/返工/升级产品决策。调度者默认不修改产品源码。

用户已确认 thinkV2 是空白项目，授权从零完整开发。旧 think 源码、测试与验收不继承。新项目入口为 `README.md`、`doc/requirements.md` 和 `doc/product-baseline-decision-2026-09-16.md`；若以下历史规则引用 `doc/README.md`，使用新项目实际入口。最新正式基线允许按单一 Checkpoint 串行开发文字、分类/回收站、提醒和备份，工程验收不等于设备/家庭交付通过。

## 唯一事实来源

发生冲突时依次采用：

1. 用户在当前任务中的明确决定；
2. 产品知识库中的已批准产品决策；
3. 产品仓库 `doc/README.md` 指定的 PRD、命名决策、开发指南和暂停条件；
4. 产品仓库 `AGENTS.md`；
5. 本项目的调度状态和已验收记录；
6. 产品经理或开发者聊天中的建议。

聊天内容只有在写入正式产品文档后才构成产品需求。实现结果只有在调度者验收后才构成 Checkpoint 通过证据。

## 每次运行的启动顺序

1. 读取 `orchestration/project.json`、`orchestration/state.json` 和 `orchestration/current-task.json`。
2. 读取产品仓库的 `AGENTS.md`、`doc/README.md`、当前 Checkpoint、相关功能需求与验收标准。
3. 检查产品经理任务、开发者任务是否空闲及其最新结果。
4. 检查产品仓库分支、工作区修改和最近提交；不得覆盖或归因不明修改。
5. 运行 `python3 scripts/leader_check.py`。检查失败时不得下发开发任务。

## 单任务调度协议

- 同一时间只能有一个开发者任务，且只能属于一个 Checkpoint。
- 开发者运行中不得重复下发或用新任务覆盖旧任务。
- 每项任务必须包含：唯一目标、允许范围、明确不做、验收标准、证据要求、停止条件。
- 任务不得写成“持续开发整个 App”或同时跨越多个 Checkpoint。
- 当前 Checkpoint 未通过时，不得实现后续 Checkpoint 的正式功能。
- 读取、审计、技术样机和可点击原型不等于正式产品功能完成。
- 目标仓库工作区不干净时，先识别修改所有权和目的，再决定是否继续。

## 状态转换

允许的主流程：

`NEEDS_RECONCILIATION → READY_FOR_DISPATCH → IN_PROGRESS → AWAITING_REVIEW → ACCEPTED`

审查失败时转为 `REVISE`，随后生成范围更小的返工任务。遇到产品决策、隐私红线、Checkpoint 门槛或 PRD 暂停条件时转为 `PRODUCT_DECISION_REQUIRED` 或 `PAUSED`，不得自行绕过。

只有同时满足以下条件才能标记 `ACCEPTED`：

- 任务范围内的产物存在；
- 验收标准逐项有证据；
- 与 PRD、三步路径和隐私边界一致；
- 适当测试已通过；
- 未验证项已明确记录；
- 未引入未审查的第三方依赖；
- Git 修改边界清楚，没有把无关修改混入结果。

## 产品决策升级

只有以下问题交给产品经理：

- 改变用户行为、P0/P1、三步路径或数据边界；
- 改变“原始录音不落盘、不上传”等隐私约束；
- 改变当前 Checkpoint 的通过门槛；
- 需要扩大范围或触发 PRD 暂停条件。

产品经理的结论必须明确为 `APPROVED`、`REVISE` 或 `PAUSE`，并在正式产品文档中落地后才能继续开发。

## 开发者报告要求

开发者完成每项任务时必须返回：

- `RESULT`：`COMPLETE`、`BLOCKED` 或 `PRODUCT_DECISION_REQUIRED`；
- 修改文件及其目的；
- 测试命令和结果；
- 验收标准逐项证据；
- 未验证项目；
- PRD/范围偏移检查；
- Git 提交或未提交状态；
- 建议的下一步，但不得自行开始下一步。

## 硬性红线

- 不得保存、上传、记录或写入测试附件中的原始录音。
- 不得使用父亲的真实数据作为 fixture、日志、截图或公开材料。
- 不得新增账号、同步、支付、公开发布、Flutter、KMP 或云端语音识别。
- 第三方 Skill、仓库、依赖、插件、安装器或容器必须先通过产品仓库的安全门禁。
- 不得用聊天摘要代替真机数据、测试结果、文件内容或提交记录。

## 换机优先规则（2026-09-17）

先读 `handoff/START-HERE.md`。上文旧机器绝对路径和任务ID均为历史，不直接用于新机器派单。
本仓库的冻结账本保持交接时原样；先核对待审交付，再给新任务配置新本地路径和路由。
用户指定仓库：Leader=3956ray/Leader，PM=3956ray/ProductManager，dev=3956ray/Developer。
不得把公开脱敏导出等同原始产品Git历史已完整迁移；受限语音资产按Developer排除清单处理。
