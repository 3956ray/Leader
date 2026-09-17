# CP2-ASR-STATIC-CLOSURE-DISCOVERY-AUTHORIZATION-002 验收报告

- RESULT：`AUTHORIZED`
- 结论：`ACCEPTED`
- 日期：`2026-09-05`

## Product Lead 明确授权

> 我批准 `CP2-ASR-STATIC-CLOSURE-DISCOVERY-GATE-002`：仅允许针对 sherpa-onnx commit `917bed95c8e5c7c18aa4d69fea42e9ef8ef0a60e`、tree `fd2c4e97c9f7499b6ed91c7c2854b4211f61bdc0`，按任务合同在正文获取前冻结的 seed、允许根／类型、确定性 include 闭包规则及 256 文件／2,097,152 字节上限，从 GitHub Git Data blob API 获取逐文件正文，用于静态闭包发现；`offline-tts-frontend.h` 只可作接口级静态分析。此授权不允许使用现有 block 归档或 manual_review 快照，不允许执行、构建、配置 CMake、获取外部依赖或模型、修改产品源码、形成构建输入、集成、宣称 CP2 通过或进入 CP3。

## 适用边界

- 授权只适用于 `CP2-ASR-STATIC-CLOSURE-DISCOVERY-GATE-002`，固定 commit/tree、正文前冻结策略和 256 文件/2 MiB 上限不得改变。
- `offline-tts-frontend.h` 是唯一 TTS 接口级静态分析例外；不得跟随或取得任何 TTS 实现、eSpeak/Piper 或更多 TTS 文件。
- 只允许可信只读文本/结构解析、scanner、文件类型和链接检查及人工静态复核；发现 corpus 不是最终快照或构建输入。
- 不授权使用现有 block/manual_review 制品，不授权执行、构建、配置、依赖/模型获取、产品源码修改、集成、CP2 通过或 CP3。

## 调度结论

授权与正式修订决定的精确授权句一致，覆盖阶段 A 的执行前置条件且未扩大到阶段 B。Leader 可以下发唯一开发者任务；任务完成后必须停止等待验收，任何最终快照仍需另一次 Product Lead 授权。
