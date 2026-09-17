# CP0-BASELINE-003 验收报告

- RESULT：`COMPLETE`
- 结论：`ACCEPTED`
- 提交：`7dacd3676fa7efc8162c1ed1171389e96fc807cb`

## 证据

- 只升级已有 AndroidX/Test 依赖族，没有新增坐标、插件或仓库。
- 版本均为官方稳定版固定值，无动态、预览或快照版本。
- `gradle/verification-metadata.xml`：472 个组件、789 个工件和 789 个 SHA-256；文件哈希 `fa337c7ffca461fc17627db76326d6b8b59d0708c7902e8ccbd108bd4f8ae420`。
- strict 模式的 `clean test lint assembleDebug` 成功，52 个任务执行完成。
- 独立读取测试 XML：1 个测试、0 skipped、0 failures、0 errors。
- 独立读取 lint XML：0 error；Debug APK 哈希与审查记录一致：`f042ab1809257504291c4533e7a7110222d2530f35f12d28ceb2b903b8b9cfee`。
- 构建没有重新引入 Foojay、自动备份、未审查仓库或新依赖族。
- 提交后工作区干净；分支 `main...origin/main [ahead 7]`。

## 控制条件

- 当前固定依赖基线为 `approved_with_controls`；任何依赖、插件、仓库或哈希变化必须重新过门禁。
- 未运行真机或仪器测试；永久 applicationId 仍未决定。
- 本结果只放行可逆本地开发，不代表任何用户或真机 Checkpoint 已通过。

