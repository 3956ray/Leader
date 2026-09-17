# CP2-ASR-RUNTIME-BOUNDARY-ROUTE-DECISION-003 验收报告

- RESULT：`APPROVED`
- 结论：`ACCEPTED`
- 选定路线：A，仅批准下一项纯设计任务的产品路线
- 正式决定：`cp2-runtime-boundary-route-decision-2026-09-05.md`

## 验收结论

产品经理选择先用已提交证据设计项目自有 CPU-only／ASR-only 窄 API／适配边界。该决定没有批准 discovery corpus、候选 allowlist、sherpa-onnx 制品、最终快照、构建、模型、产品集成、CP2 或 CP3，也没有授权直接执行下一设计任务。

路线 A 是一项低成本、可停止的设计判断，不继承任何既有制品裁决。若设计返回 `design_blocked`／`insufficient_evidence`，或 P0 只能依赖 WAV 文件 I/O、ADSP/QNN/RKNN、TTS、宽 JNI、自动下载或用户可控动态加载，sherpa-onnx 路线暂停并回到产品决策门；不得自动启动替代运行时研究。

## Leader 独立复核

- 本次产品决策合同 SHA-256 为 `ba885073ae2486b99954833ee131926faf4802bdcbe9b7d6fe9b94f652d314c5`；Leader 验收报告 SHA-256 为 `c413bcc7cd6b558463b0d88ffae31bbf5ce3cdb441c3cee0fd52b4159802545e`。
- `think` 提交 `0ded8eb54e5d4d529759b46c62b9b5eb10722fbb` 下证据目录 tree 为 `1bdd940c85554147b904b033c59095f849d22a46`。决定引用的七份发现证据 SHA-256 全部与仓库文件重算结果一致：`manual-review.md`、`security-verdict.json`、ledger、停止证据、停止后分析、候选 allowlist 和依赖/许可证复核。
- 正式决定、更新后 PRD、产品知识库根索引和日志 SHA-256 分别为 `36fabbf187f7d5aebfb760f550f1273d10908371fd390ee4937968a5b8c576f5`、`a8929112ce2024834f341f9e16bfcabc4fc774f1a331cdf4e73cdadfc7527905`、`12874c2c1051aa84e549ac554d07c87ea135171d69deeff49b9a4925327d66e4`、`36c0286402f607b3a4677cc02f572e064024d4c2535f2cb2ac1881824400bf09`。
- 决定准确区分了：`fixed_point=false` 来自 Leader 收敛停止，不能证明上游无法闭合；WAV 路径写入、ADSP 环境修改、QNN/RKNN 与宽 JNI/Kotlin 表面是独立成立的边界缺陷。
- 下一任务只允许使用固定提交中的已提交结构化证据、正式复核文件、Leader 报告与现行产品决定；明确禁止读取隔离 corpus、获取新正文、修改产品源码、形成实现/构建输入及任何动态技术执行。
- 产品知识库原有工作区包含大量历史修改和未跟踪材料；本任务只验收本决定及其明确列出的 PRD／INDEX／LOG 更新，不把其他材料归因于本任务，也不覆盖它们。

## 后果与未验证

- 下一设计任务 `CP2-ASR-NARROW-RUNTIME-BOUNDARY-DESIGN-001` 需要 Product Lead 使用精确授权句另行批准；在授权前不得执行。
- 当前 discovery 仍未达到固定点，外部依赖、许可证、源码—制品对应、arm64 CPU-only 构建、模型、中文效果、性能、稳定性、飞行模式、小米 15 和音频隐私动态证据均未验证。
- CP1 父亲人工门槛继续 `Deferred, not removed`；CP2 未通过，CP3 未批准。
