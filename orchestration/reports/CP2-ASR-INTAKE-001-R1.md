# CP2-ASR-INTAKE-001-R1 验收报告

- RESULT：`COMPLETE`
- 结论：`ACCEPTED`
- 提交：`e9c2e8fc3a9e0ef97470b7c42b364d5ddaa5d3ac`

## 验收证据

- 提交只修改 `doc/security-reviews/sherpa-onnx-cp2-intake/2026-09-05/intake.md`。
- 唯一实质改动是把后续门禁裁决限定为 `block`、`sandbox_only`、`manual_review`、`approved_with_controls`，并删除将 `approved` 作为独立裁决的表述。
- 全文检查不再发现 `approved`、`rejected` 或 `low_indicators` 被用作最终门禁枚举；`NOT_APPROVED` 仅表示当前尚未批准。
- 已核验版本、提交、URL、哈希、许可证、候选、兼容性和基准字段未改变。
- `git diff --check` 通过；提交后 `main...origin/main [ahead 15]`，工作区干净。

## 未验证

- 所有第三方制品仍未获取或扫描；本验收只通过身份清单，不构成任何制品采用或 CP2 通过。
