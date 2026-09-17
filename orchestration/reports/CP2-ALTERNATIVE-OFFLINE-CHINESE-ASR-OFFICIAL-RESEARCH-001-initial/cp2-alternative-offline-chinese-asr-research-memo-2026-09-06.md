# 决策备忘录：CP2 替代离线中文 ASR 官方研究

Owner: Product Lead
Last updated: 2026-09-06
Source: cp2-alternative-offline-chinese-asr-evidence-cards-2026-09-06.md；cp2-alternative-offline-chinese-asr-comparison-matrix-2026-09-06.md；`CP2-ALTERNATIVE-OFFLINE-CHINESE-ASR-OFFICIAL-RESEARCH-001` 合同
Confidence: Medium-High（两个候选通过研究硬筛选；所有制品、安全、运行时与真机结论仍未知）
Related decisions: cp2-hotwords-chain-termination-route-decision-2026-09-06.md；cp2-runtime-security-route-decision-2026-09-05.md；prd-v0.1-2026-09-04.md
Next review date: 2026-09-13

Research Quality: 92 · pass
Validation Level: V2
Next evidence: 独立产品任务决定是否、以及只选择哪一个 shortlist 候选进入有界安全 intake
Allowed next investment: 一项产品选择决策；未获得新决定前不进行任何候选制品取得、源码读取、扫描、构建、运行或测试
Pause/Kill condition: Product Lead 不选择候选；或被选候选在 intake 第一阶段无法关闭许可证、来源、Android CPU-only 与纯内存音频边界

## RESULT

**COMPLETE — `research_sufficient_for_security_intake_decision`。**

在 12/18 个官方页面预算内完成 4 个非 sherpa-onnx 候选比较。Vosk 与 ONNX Runtime Mobile + SenseVoiceSmall-onnx 满足研究阶段硬筛选，可供未来独立产品决策最多选择一个进入安全 intake。WeNet 和 whisper.cpp 存在不得以推断补齐的许可证或中文证据缺口，不进入 shortlist。

本结论不是候选采用批准，也不是安全 intake 批准。没有候选源码、模型、AAR、APK、库或二进制被取得、保存、执行或审查；`/Users/orderly_ray/Projects/think` 未修改；CP2 未通过，CP3 与父亲 Alpha 未批准。

## 决策支持结论

### 推荐 1：Vosk

推荐把 Vosk 作为下一次产品选择决策的第一候选，原因是：

- 官方证据直接覆盖中文、Android、设备离线、流式／连续识别和可重配词表；
- 小型中文模型约 42 MB，产品侧安装与 Xiaomi 15 性能验证负担相对可控；
- runtime 与官方中文模型条目均有 Apache-2.0 标识，来源边界比其他候选简单；
- 与“按住说话、单段 90 秒、本地转文字、原始录音不上传”的 P0 路径最接近。

必须保留的反证与未知：本轮没有固定版本、散列、arm64-v8a 包、Android PCM API、日志／缓存／buffer 释放；没有验证普通话真实准确率、专名词表效果、30／90 秒耗时、90 秒 20 次稳定性、飞行模式、内存、发热或原始音频不落盘。

### 推荐 2：ONNX Runtime Mobile + SenseVoiceSmall-onnx

推荐把该组合列为第二候选，而不是直接可采用 SDK：

- ONNX Runtime 官方支持 Android Java／C／C++ 设备侧运行且默认有 CPU 路径；
- iic 官方模型页摘要标识中文 ASR、ONNX 量化模型、约 241.59 MB 和 Apache-2.0；runtime 为 MIT；
- 可以设计无原始音频云端上传的本地路线。

主要风险是它只提供“推理 runtime + 模型”的组合证据。音频预处理、特征提取、tokenizer、解码、标点、长音频切分和 Android 内存 PCM 接口可能依赖额外组件；任一组件要求云端、文件路径、不可识别来源或不兼容许可证，应在安全 intake 早停。模型官方页本轮只取得部分页面摘要，也必须在 intake 前重新固定官方元数据。

## 未进入 shortlist

- **WeNet**：官方资料证明中文、Android device、流式／非流式与 Apache-2.0 runtime，但模型文档把许可证指向相应数据集；在三页预算内没有关闭一个具体中文 Android 模型的许可证与重分发边界。Android ABI、CPU-only 包、内存 PCM、体积和热词也未知。
- **whisper.cpp**：官方资料证明 Android、CPU-only、离线和多语言，但本轮选定页面没有明确写出 Mandarin／Chinese，且没有把 runtime MIT 与模型权重许可证／重分发范围分别闭合。Android 示例还是 assets／文件导向，内存 PCM 与隐私边界未知。

这两个候选的“不合格”只表示本轮官方证据未达到硬筛选，不等于技术上不支持中文、不可用或不安全。

## 个性词表状态

- Vosk：官方明确可重配词表，状态为 `officially claimed, product threshold unverified`。
- WeNet：本轮所选页面未关闭 Android 中文热词机制，状态为 `unknown`。
- ONNX Runtime Mobile + SenseVoiceSmall-onnx：官方模型页摘要存在 hotword 示例线索，但未证明直接 Android、纯本地和完整组合支持，状态为 `partial evidence, unverified`。
- whisper.cpp：本轮所选页面没有建立满足本产品的词表／phrase bias 合同，状态为 `unknown`。

产品级“个性词典／词表实现”继续为 `Deferred, not removed — implementation route unresolved`。CP2 的常用专名加入词典后正确率至少 90% 门槛没有删除；最终候选必须验证该能力，或由 Product Lead 另立正式决定修订门槛。

## 下一步建议与授权边界

未来可创建但本任务不自行开始的唯一产品任务建议：

`CP2-ALTERNATIVE-ASR-SECURITY-INTAKE-SELECTION-DECISION-001`

唯一目标：只基于本轮证据卡与比较矩阵，在 Vosk 和 ONNX Runtime Mobile + SenseVoiceSmall-onnx 中最多选择一个候选，定义一个独立、可停止、不可继承 sherpa-onnx 裁决的安全 intake 合同。

该产品选择任务本身不需要取得新正文或制品。只有当 Product Lead 正式选择候选并批准 intake 合同后，后续技术任务才可以按新合同取得精确限定的官方元数据／README／LICENSE 或制品；不得复用旧授权。

若 Product Lead 选择 Vosk，建议未来 intake 的第一停止点依次是：固定官方 runtime release 与 Android arm64-v8a 发行身份；固定一个官方中文小模型及许可证／散列；静态证明 Android 音频入口可由内存 PCM 驱动且不强制文件；随后才决定是否允许下载与安全扫描。

若 Product Lead 选择 ONNX Runtime 组合，建议第一停止点必须先形成完整组件表：runtime、模型、音频预处理、特征、tokenizer、decoder、标点与长音频切分。组件表任何一项来源／许可证／纯本地边界不明，即停止，不进入制品获取。

## 未验证项

- 所有候选的精确 release、commit、制品 URL、SHA-256、签名、SBOM、漏洞状态和依赖闭包；
- Android arm64-v8a／CPU-only 的真实可用包、JNI／Kotlin API 与最低系统；
- 麦克风 PCM 到识别结果是否可全程只驻留内存，是否存在 sample、临时文件、缓存、日志、崩溃报告或遥测；
- 中文准确率、标点、噪声、口音、专名、热词／词表与转写后纠错；
- Xiaomi 15 飞行模式、30／90 秒延迟、90 秒连续 20 次、RAM、耗电、温升与退出后的 buffer 释放；
- 模型和 runtime 的商业使用、再分发、notice 与第三方权利，仍需未来合格审查；
- 云端 AI 只接收转写文字的产品边界尚未因本研究获得任何新验证。

## 保持不变与禁止声明

- 三步录入、三步找回、微信式按住说话、单段 90 秒不变。
- 原始录音不落盘、不上传、不进日志；只允许把转写文字发送云端 AI 做标题和分类。
- CP1 父亲人工验证、Conformer 与个性词表实现均为 `Deferred, not removed`；适用门禁必须在 CP3 前恢复。
- 小米 15 仍是目标证据设备；本轮没有任何真机结果。
- 不扩大到账号、同步、支付、Flutter、KMP、云端语音识别或公开发布。
- sherpa-onnx 的 `block`／`manual_review` 制品和已终止热词链不因替代研究而恢复或继承。

禁止声称“Vosk 已安全／已批准”“SenseVoice 组合已可集成”“WeNet 或 whisper.cpp 不支持中文”“官方声称离线就证明不落盘”“许可证标识等于法律批准”“研究完成即 CP2 通过”或“可以开始父亲 Alpha”。

## Eval

- Evidence Quality: 92/100 · pass
- Validation Level: V2
- Decision: `research_sufficient_for_security_intake_decision`
- Allowed investment: 仅下一次产品选择决策；零自动技术执行
- Stop condition: 少于一个候选被正式选择，或被选候选无法在 intake 初期关闭来源、许可证、Android CPU-only、内存音频和隐私合同

