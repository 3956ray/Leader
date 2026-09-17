# CP2-ASR-GATE-MODEL-ZIPFORMER-001 验收报告

- TASK RESULT：`COMPLETE`
- TASK 结论：`ACCEPTED`
- ARTIFACT VERDICT：`manual_review`
- 提交：`cb6f4ba1e2ccd10cf5b0301c3b59a68f75f6837f`

## 验收证据

- 提交只新增 Zipformer 四文件集的 scanner Markdown/JSON 与人工报告；没有模型、应用、依赖或源码进入 Git，产品仓库干净。
- Leader 独立复核隔离目录四个文件：encoder `21,621,684` / `1c556e...87b1`，decoder `1,888,682` / `22f123...68bbf`，joiner `1,795,562` / `a7cf9d...36169`，tokens `48,697` / 本地 SHA-256 `8b294d...66ac`，均与报告及上游固定提交元数据一致。
- Scanner 在明确提高单文件上限后覆盖 4 files、0 skipped/unreadable，原始 verdict `low_indicators`；报告未将其等同安全批准。
- 可信标准库静态解析报告可复核：三份 ONNX protobuf 完整、无 external_data、实际节点只用标准 `ai.onnx`、无自定义节点/训练信息/函数/字符串张量，张量尺寸与 raw 长度一致。
- encoder/decoder/joiner 特征维度与 5,537 项模型词表静态匹配；tokens 0..5538 中最后两个为 disambiguation symbols。
- 人工报告正确识别两个关键阻塞：同固定仓库 FP32 encoder 存在上游 `PAIT-ONNX-200` 架构后门提示且 INT8 是量化输出，无法仅靠标准算子检查排除继承；官方示例使用 INT8 encoder + FP32 decoder + INT8 joiner，而非本四文件全 INT8 组合。
- 训练/导出 provenance、许可证随包材料和 WenetSpeech 再分发条件未闭合，因此 `manual_review` 与证据一致，不满足 `approved_with_controls`。

## 后果与未验证

- 该四文件集当前不得加载、推理、测试、打包或集成；需要模型安全 reviewer、上游说明/可复现来源和组合兼容性证明后重新裁决。
- Conformer 候选尚未获取；运行时 AAR 仍为 `manual_review`，源码归档为 `block`；CP2 未通过。
- 接受的是审查任务完成与裁决成立，不是接受该模型。
