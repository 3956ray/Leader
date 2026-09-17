# CP2-ASR-MINIMAL-SOURCE-SNAPSHOT-GATE-001 验收报告

- TASK RESULT：`BLOCKED`
- TASK 结论：`ACCEPTED`
- ARTIFACT VERDICT：`manual_review`
- 提交：`6952167795d1243534a93fa59a18372fb0d192e8`

## 验收结论

开发者正确执行了合同停止条件：固定 allowlist 后取得的首批 50 个正文文件暴露出 5 个清单外仓库内头文件，其中 `offline-tts-frontend.h` 跨入合同明确排除的 TTS 能力。合同禁止在正文获取后增补或重冻清单，因此任务不得继续，快照未完成，也不得作为后续构建输入。接受的是“有证据地停止”，不是接受该快照。

## Leader 独立复核

- 官方 Git commit 响应为 `917bed95c8e5c7c18aa4d69fea42e9ef8ef0a60e`，tree `fd2c4e97c9f7499b6ed91c7c2854b4211f61bdc0`；tree 响应 8,585 项且 `truncated=false`，其中 275 个 mode `120000` 未进入 allowlist。
- 隔离目录 `/private/tmp/think-cp2-minimal-source-g78VnT` 中原始冻结清单时间早于快照正文；原始清单与 Git 提交中的副本逐字节相同，SHA-256 为 `d6ca88c3bab331ea0034613d7412e74d4cb3c3ec2317f37d1bf35e0b52fc3097`。
- 冻结清单共 151 项、887,313 字节；路径排序且唯一，均为相对安全路径、Git blob、mode `100644`/`100755`，不可变 URL 与各自 Git blob SHA 一致。
- Leader 对实际 50 个文件重新计算大小、Git blob SHA-1 语义与 SHA-256，50/50 与 manifest 一致；实际集合等于 50 条已验证证明集合，是冻结清单的真子集。
- Leader 独立 lstat 得到 4 个目录、50 个普通文件、0 符号链接、0 硬链接异常、0 特殊文件，总计 258,363 字节。
- Leader 逐行复核 5 个遗漏 include：`cat.h`、`math.h`、`offline-tts-frontend.h`、`phrase-matcher.h`、`unbind.h`，均存在于已验证正文引用中；TTS 边界冲突成立。
- Leader 在新的临时输出目录重新运行 `scan-untrusted-code 1.1.2`；结构化和 Markdown 结果与提交副本逐字节一致：`sandbox_only`、40/100、2 个不可达 high、无 block signal。两项命中分别位于 CMake 告警帮助字符串和 logger 调试提示字符串，人工解释成立，但不解除闭包阻塞。
- 提交只新增指定安全审查目录的 6 个文档/JSON 文件；没有产品源码、第三方源码、二进制、模型或音频进入 Git，产品仓库最终工作区干净。

## 后果与未验证

- 当前部分快照 verdict=`manual_review`，不得构建、配置、安装、加载、测试、导入或集成。
- 101 个冻结文件未获取；JNI/Kotlin、完整依赖/许可证、arm64 CPU-only ASR-only 编译闭包、运行时与真机性质均未验证。
- 现有源码归档 `block`、AAR/Zipformer `manual_review`、Conformer `Deferred, not removed`、CP1 usability deferred 和 CP2 未通过状态不变。
- 继续需要新的产品路线决定：必须先解决上游共享源列表和 ASR/TTS 头文件耦合，再定义新的闭合发现/冻结协议；不得把本次清单静默修订后重跑。
