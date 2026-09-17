# CP2-ASR-MINIMAL-SOURCE-AUTHORIZATION-001 验收报告

- RESULT：`AUTHORIZED`
- 结论：`ACCEPTED`
- 日期：`2026-09-05`

## Product Lead 明确授权

> 我明确授权 CP2-ASR-MINIMAL-SOURCE-SNAPSHOT-GATE-001：从 sherpa-onnx 不可变上游提交按显式 allowlist 逐文件获取内容，并在全新隔离目录创建无符号链接的最小源码快照，仅用于静态安全审查。此授权不包括构建、安装、加载模型、修改产品源码、集成或进入 CP3。

## 适用边界

- 授权对象仅为 `CP2-ASR-MINIMAL-SOURCE-SNAPSHOT-GATE-001`。
- 只允许从固定的 sherpa-onnx 上游提交按冻结的逐文件 allowlist 获取普通文件内容，在全新隔离目录形成零符号链接快照并进行静态安全审查。
- 不允许使用、解压、复制或修补此前 verdict=`block` 的源码归档来建立快照。
- 不授权构建、安装、模型下载或加载、产品源码修改、集成、运行第三方代码、真机测试或进入 CP3。
- 现有源码归档 `block`、AAR/Zipformer `manual_review`、Conformer `Deferred, not removed` 及 CP2 未通过状态保持不变。

## 调度结论

授权文字明确覆盖正式产品决定要求的执行前置条件，未扩大到后续阶段。Leader 可以下发唯一开发者任务 `CP2-ASR-MINIMAL-SOURCE-SNAPSHOT-GATE-001`；该任务的完成只产生快照静态门禁裁决，不等于批准构建或采用。
