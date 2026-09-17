# CP2-ASR-NARROW-RUNTIME-BOUNDARY-DESIGN-DECISION-002 验收报告

- RESULT：`APPROVED`
- 结论：`ACCEPTED`
- 正式决定：`cp2-narrow-runtime-boundary-design-decision-2026-09-05.md`

## 验收结论

产品经理接受项目自有 handle 型 CPU-only／ASR-only 窄边界作为后续源码审查合同，并拒绝“宽 API＋caller 规则”作为产品架构终态。接受的 `design_feasible` 仍只表示能定义下一道可证伪门禁，不批准第三方源码、制品、适配器实现、构建输入、依赖、模型、集成、CP2 或 CP3。

下一项技术任务被限定为 `CP2-ASR-NARROW-SOURCE-BOUNDARY-FEASIBILITY-GATE-001`：在全新隔离目录，从固定 sherpa-onnx commit/tree 以正文前冻结的 9 个 seed、仅 `LICENSE` 与 `csrc` 普通 `.h/.cc`、确定性 literal include、96 文件/1 MiB 上限重新取得正文，只建立 P0 核心内部源码图并静态判断边界可行性。它需要 Product Lead 新授权，当前不得执行。

## Leader 独立复核

- 本次产品决策合同 SHA-256 为 `b1f1b45eb0d83f2a4673ae0a19e3c09606034b121ad9352989f17b11226b6717`；Leader R1 验收报告 SHA-256 为 `5981edfe0e6c295529d80e0b9b2f418284c6c46431e6441aa4615b9b118dd3f2`。
- 设计首版/返工提交、首版/最终目录 tree 分别重算为 `8eea683...f22d`、`a57f643...d2c`、`5e7de6b...b81f`、`31376c73...379d`；七个设计产物 SHA-256 和 28 项输入摘要 `c318c5a5...64d2` 均与决定引用一致。
- 新任务固定官方 commit `917bed95...a60e`、tree `fd2c4e97...bdc0`、9 个精确 seed、仅 `LICENSE`/`csrc` 普通文本 blob、96 文件/1,048,576 字节硬上限；禁止复用旧 corpus、101 项候选、部分快照、block/manual_review 制品。
- denylist、broad JNI/Kotlin、用户可控 provider/库/模型路径均为获取前停止/阻塞边界；system/external 只登记不获取，CMake、JNI/Kotlin、依赖、模型、音频和二进制不取得。
- 结论词汇被限制为 `source_boundary_feasible`、`source_boundary_blocked` 或 `insufficient_evidence`；任何结论都不是快照、实现、构建、制品、模型、CP2 或 CP3 批准。
- 正式决定、更新 PRD、产品知识库 INDEX/LOG SHA-256 分别为 `55b523da2d5a6b6518b726620f3ace47dbc054fd98cef8af44bc3d2bee9f3c0a`、`d9f1d3e1d539348deb2eff5093a73e6b92f39f9b18e520fe9f23f7fd62aaefd0`、`e3083774a0d604e591f69f726f2e07d32eeb24c411b19ec91fd90160d344f1c6`、`d4b1eae087ca17c0dbf2c1df9abe585bd563b3300e089727a848f950dda643d9`。
- 产品知识库原有大量历史修改/未跟踪文件保持原状；只验收本决定明确列出的决定、PRD、INDEX、LOG 更新，不归因或覆盖其他材料。

## 后果与未验证

- 当前 Product Lead 设计授权已经耗尽；新正文与源码级门禁必须使用正式决定中的精确授权句另行批准。
- `fixed_point=false`、两条内部缺失边、332 条 system/external 边及源码、依赖、构建、制品、模型、动态隐私和小米 15 门槛全部保持未验证。
- CP1 父亲人工门槛继续 `Deferred, not removed`；CP2 未通过，CP3 未批准。
