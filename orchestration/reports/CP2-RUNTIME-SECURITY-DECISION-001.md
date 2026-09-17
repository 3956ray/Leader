# CP2-RUNTIME-SECURITY-DECISION-001 验收报告

- RESULT：`APPROVED`
- 结论：`ACCEPTED`

## 正式决定

- 只批准“可复现最小源码快照 → arm64-v8a、CPU-only、ASR-only 构建”的安全路线，不批准任何现有源码归档、AAR 或 Zipformer 制品。
- 路线批准不等于执行授权；Product Lead 必须另行明确授权“从不可变上游提交获取 allowlist 文件并创建新的最小源码快照，用于安全审查”后，Leader 才能下发快照任务。
- 快照只能逐文件从不可变来源建立、零符号链接、显式 allowlist，先取得独立 `approved_with_controls`；之后工具链、依赖、构建和新运行时产物仍各自独立门禁。
- Conformer 为 `Deferred, not removed`，运行时最小路线获准后、任何模型加载或两候选比较前必须恢复。
- CP2 仍未通过，所有真机、性能、稳定性、飞行模式和音频隐私门槛不变；CP3 与父亲 Alpha 未批准。

## 独立核验证据

- 正式决定：`/Users/orderly_ray/Documents/Products Manager/product-knowledge-base/ideas/personal-thought-archive/cp2-runtime-security-route-decision-2026-09-05.md`
- 决定 SHA-256：`2aec8cad71a6669e1fbaf26ab659cfd80baa02fb0d38c3367d1ced7c0b06c448`
- 产品 PRD SHA-256：`cc1a1ff792ab37c889e5861d2b09ff60fcd96423776be4746c83485cae678760`
- INDEX SHA-256：`8ea302466ad8f070df3960f8b4085a14f5d2d0b30bc9a9cd0f7934e52f62acb3`
- LOG SHA-256：`daefa2924219fb8948ebe2daa9fa5eeeece2c487281be996ae3693b7c08324de`
- Leader 已全文核对路线、当前三项裁决、授权句、下一单边界、Conformer 状态、暂停条件和禁止声明，内容一致。

## 未验证与工作区说明

- 最小源码快照尚未获 Product Lead 执行授权，也未建立或扫描。
- 产品知识库存在此前已有的大量未提交修改；本次指定决定/PRD/INDEX/LOG 通过路径与哈希验收，但未提交。
