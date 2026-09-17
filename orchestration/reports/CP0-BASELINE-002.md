# CP0-BASELINE-002 验收报告

- RESULT：`COMPLETE`
- 结论：`ACCEPTED`
- 提交：`a35392335d183c9e567065ea389f85fc9d46a0c4`

## 证据

- Wrapper JAR SHA-256：`497c8c2a7e5031f6aa847f88104aa80a93532ec32ee17bdb8d1d2f67a194a9c7`，与 Gradle 9.5.0 官方值一致。
- `distributionUrl` 固定 `gradle-9.5.0-bin.zip`，`distributionSha256Sum` 为 `553c78f50dafcd54d65b9a444649057857469edf836431389695608536d6b746`。
- 安全复核记录固定官方来源、时间、替换前后哈希、文件大小和隔离扫描摘要。
- Wrapper 子项为 `approved_with_controls`，项目总门禁仍为 `manual_review`。
- 提交只包含 wrapper JAR 和安全复核文档，工作区干净；分支 `main...origin/main [ahead 6]`。

## 未验证

- 未执行 Wrapper、Gradle 构建或依赖解析。
- 依赖校验元数据、AndroidX 版本和永久 applicationId 仍待处理。

