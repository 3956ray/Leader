# CP2-ASR-GATE-RUNTIME-SOURCE-001 验收报告

- TASK RESULT：`COMPLETE`
- TASK 结论：`ACCEPTED`
- ARTIFACT VERDICT：`block`
- 提交：`e00323b38d182fe82add0c26d7420a6d14dc7405`

## 验收证据

- 提交只新增源码归档的 `manual-review.md`、`scan-report.md` 和可解析 `scan-report.json`；没有应用、构建、依赖、权限或第三方制品进入 Git，产品仓库干净。
- 隔离归档位于 `/private/tmp/think-cp2-sherpa-source-f67rX7/`，Leader 独立复核大小 `11,614,988` bytes 和 SHA-256 `acf539e930283442c4237b7b23a06ebe3bff10cbc00694a4f09a3580e3c10e9e` 与报告/扫描目标一致。
- scanner 1.1.2 直接扫描压缩归档，JSON 记录 `block`、100/100、最高 critical、0 skipped_large、0 skipped_limit、0 unreadable；报告明确静态扫描盲区。
- Leader 从 JSON 独立复核两个高风险符号链接分别指向 `/Users/fangjun/.../main.go` 和 `/Users/fangjun/.../run.sh`，越出归档根。依据门禁策略，归档 path/link 边界风险足以判定 `block`。
- scanner 的 critical 敏感数据+网络组合由人工降解说明为 release CI 的 SSH 发布行为，没有虚构凭证外传；但仍明确禁止在工作站执行。
- 人工报告覆盖 CI/自动执行面、远程下载链、ONNX Runtime/native/JNI、Manifest/权限/网络、日志/文件/音频能力、许可证、来源和当前漏洞查询。
- 报告明确裁决仅适用于固定源码归档，不继承给尚未审查的 AAR 或模型。

## 后果与未验证

- 该源码归档不得解压、运行、构建、安装、导入或采用；隔离副本保留供核验。
- 官方 AAR、模型与词表均未下载或扫描；源码到 AAR 的对应关系、最终二进制行为和 CP2 真机门槛仍未验证。
- 接受的是“审查任务完成且 block 证据成立”，不是接受该第三方制品。
