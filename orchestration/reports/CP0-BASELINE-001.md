# CP0-BASELINE-001 验收报告

- RESULT：`COMPLETE`
- 结论：`ACCEPTED`
- 提交：`c5dd1da4e6eda00140fd23c61a153106c0f2eb2c`

## 验收证据

- `android:allowBackup="false"`，旧版备份与新版云备份/设备迁移规则均排除全部应用数据域。
- Manifest、备份规则、数据提取规则和字符串 XML 均通过独立解析。
- Foojay 插件与自动 JDK 下载配置已移除；非文档运行时配置中没有 Foojay 引用。
- Java source/target 与 Kotlin JVM target 均为 17。
- 用户可见应用名为“思”，`versionName` 为 `0.1-alpha`，临时 applicationId 有明确注释且未伪装为冻结值。
- 安全复核只把已修正子项标记完成，总门禁仍为 `manual_review`。
- 提交后工作区干净；分支为 `main...origin/main [ahead 5]`。

## 未验证

- 按任务限制未运行 Gradle、构建、单元测试或真机测试。
- Wrapper、依赖校验、AndroidX 版本与永久 applicationId 仍待后续任务。

