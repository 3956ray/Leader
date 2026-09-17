# CP2-ASR-NARROW-RUNTIME-BOUNDARY-DESIGN-001-R1 验收报告

- RESULT：`COMPLETE`
- DESIGN VERDICT：`design_feasible`
- 结论：`ACCEPTED`
- 首版提交：`8eea68384efcb61cbea40a423b755edf3175f22d`
- 返工提交：`a57f643bac24edef5d6601b8a59baa77060f3d2c`
- 最终设计目录 tree：`31376c73f43caf3bbfd664d8316ffecdc589379d`

## 验收结论

接受的是一个可供后续独立源码审查使用的项目自有 CPU-only／ASR-only 窄边界设计合同。`design_feasible` 只表示现有已提交证据足以定义可审查、可证伪的合同；不表示 sherpa-onnx 源码能够闭合、构建可行、运行时或模型获准、音频隐私已动态证明、CP2 通过或 CP3 获准。

推荐选项是项目自有 handle 型窄适配边界。业务层只可看到固定运行时/已独立批准模型的 opaque handle、stream 生命周期、有界内存 PCM、decode、只读结果、版本与释放。固定加载由内部单一 owner 持有；文件/WAV、ADSP/QNN/RKNN、TTS、VAD、speaker/diarization、denoise、punctuation、audio tagging、WebSocket、PortAudio、下载/FetchContent、宽 JNI/C++ 和用户可控路径/provider 全部在边界外。

## Leader 独立复核

- 首版提交的父项为 `1812669faa90bfc899ac0ab0b01f17b39145ea37`，只新增约定目录的 7 个普通文件；返工提交父项为首版，只修改 `context.md` 与 `hardening.json`。两个提交均通过 `git show --check`，最终工作区干净。
- 固定发现证据提交 `0ded8eb...22fbb` 的目录 tree 为 `1bdd940c85554147b904b033c59095f849d22a46` 且到设计父提交无漂移。Leader 逐项重算 22 个固定证据文件、Leader 报告和五份正式产品文档 SHA-256，28 条 canonical record 全部匹配。
- Leader 按文档规定的 UTF-8、ASCII `|` 三字段、无符号字节序和每条 LF 规则从零重算输入集合摘要为 `c318c5a5f91d4af1d2759895ab9d5296c5784eaa214548b92f25fba4096764d2`，与 `context.md` 和 `hardening.json` 一致。
- `hardening.json` 可解析；两个选项各有且仅有 E01–E09 九条 coverage，无重复/缺失/未登记 ID，effect 与人类可读覆盖表一致；每个选项的安全、性能、内存、可靠性、可运维性和迁移权衡完整。
- Observed／Inferred／Proposed、P0 能力映射、加载所有权、模型/音频分离、成功/取消/错误/超时释放、完整 denylist、两个真实选项、before/after 图、回滚与九层未来验证计划均存在且边界一致。
- 所有相对链接存在；Mermaid 文件通过静态结构检查；未发现绝对本机路径、symlink、hardlink 异常、`implementation/`、产品源码、第三方正文、构建输入、依赖、模型、二进制或音频。

## 保留未知与下一门槛

- `fixed_point=false`、两条内部缺失边、332 条 system/external 边、源码闭包、外部依赖/许可证、ONNX Runtime、构建、制品、模型、源码—二进制 provenance、动态行为均未验证。
- 小米 15、双中文模型、准确率、30/90 秒延迟、内存、耗电、发热、20 次 90 秒稳定性、飞行模式与音频不落盘/不上网/不进日志均未验证。
- 下一步只能回到产品经理/Product Lead 决策门。任何源码级边界审查、新正文、最终快照、实现或构建都必须新的单项合同与授权。
