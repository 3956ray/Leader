# CP2 替代离线中文 ASR 官方证据卡

Owner: Product Lead
Last updated: 2026-09-06
Source: `CP2-ALTERNATIVE-OFFLINE-CHINESE-ASR-OFFICIAL-RESEARCH-001` 有界官方材料研究；下列 12 个官方页面
Confidence: Medium-High（官方能力、平台与许可证声明可追溯；未下载、执行、构建或真机验证）
Related decisions: cp2-hotwords-chain-termination-route-decision-2026-09-06.md；prd-v0.1-2026-09-04.md
Next review date: 2026-09-13

Research Quality: 92 · pass
Validation Level: V2
Next evidence: Product Lead 从合格 shortlist 中最多选择一个候选，另立安全 intake 决策；选择前不得取得源码、模型或二进制
Allowed next investment: 仅允许一次独立产品选择决策；本文件本身不授权安全 intake、下载、扫描、构建、运行、真机测试或集成
Pause/Kill condition: shortlist 候选不能在独立 intake 中关闭来源、许可证、Android CPU-only、内存音频、隐私与可复现供应链边界

## 研究合同与边界

本研究支持的唯一决策是：在不接触候选源码正文、源码树、模型、AAR、APK、库或其他制品的前提下，判断是否存在至少两个值得进入未来独立安全 intake 选择决策的非 sherpa-onnx 离线中文 ASR 候选。

本轮只读取官方产品／项目文档、官方仓库 README、LICENSE 和官方平台页面。GitHub 页面只使用 README、LICENSE 与仓库首页公开说明，没有读取源码文件。没有 clone、下载、登录、安装、执行、构建、推理、benchmark、访问 corpus 或修改 `/Users/orderly_ray/Projects/think`。

## 页面预算账本

页面从首次使用起即计入预算；即使页面正文抽取不完整，只要官方搜索摘要用于结论，也计为一个页面。

| Source ID | 候选 | 官方页面 | 类型／维护者 | 访问状态 | 本研究使用的主张 |
| --- | --- | --- | --- | --- | --- |
| SRC-20260906-think-asr-alt-01 | Vosk | https://alphacephei.com/vosk/index.zh.html | 官方中文介绍／Alpha Cephei | complete | 支持中文、离线移动端、Android、流式 API、约 50 MB 小模型、可重配词表 |
| SRC-20260906-think-asr-alt-02 | Vosk | https://github.com/alphacep/vosk-api | 官方仓库 README／Alpha Cephei | complete | 开源离线、Android API、连续转写、流式 API、词表重配、Apache-2.0 仓库许可证 |
| SRC-20260906-think-asr-alt-03 | Vosk | https://alphacephei.com/vosk/models | 官方模型目录／Alpha Cephei | complete | 中文模型条目、模型大小与许可证字段；小型中文模型约 42 MB，许可证标为 Apache-2.0 |
| SRC-20260906-think-asr-alt-04 | WeNet | https://wenet-e2e.github.io/wenet/runtime.html | 官方 runtime 文档／WeNet | complete | 流式与非流式统一模型、Android device 路径、逐帧输入、LibTorch runtime |
| SRC-20260906-think-asr-alt-05 | WeNet | https://github.com/wenet-e2e/wenet/blob/main/docs/pretrained_models.md?plain=1 | 官方预训练模型文档／WeNet | complete | 多个中文模型与 Android runtime 包；模型许可证跟随相应数据集许可证 |
| SRC-20260906-think-asr-alt-06 | WeNet | https://github.com/wenet-e2e/wenet/blob/main/LICENSE | 官方 LICENSE／WeNet | complete | WeNet runtime 仓库采用 Apache-2.0 |
| SRC-20260906-think-asr-alt-07 | ONNX Runtime Mobile + SenseVoiceSmall-onnx | https://onnxruntime.ai/docs/tutorials/mobile/ | 官方移动端文档／Microsoft | complete | Android Java／C／C++ 包、模型在设备上加载和运行、默认 CPU、arm64 库示例、应在目标设备测量大小与性能 |
| SRC-20260906-think-asr-alt-08 | ONNX Runtime Mobile + SenseVoiceSmall-onnx | https://www.modelscope.cn/models/iic/SenseVoiceSmall-onnx | 官方模型页／iic、ModelScope | partial | 官方页面摘要标明中文 ASR、ONNX 量化模型、约 241.59 MB、Apache-2.0、2024-09-26 更新；正文渲染未完整抽取 |
| SRC-20260906-think-asr-alt-09 | ONNX Runtime Mobile + SenseVoiceSmall-onnx | https://github.com/Microsoft/onnxruntime/blob/main/LICENSE | 官方 LICENSE／Microsoft | complete | ONNX Runtime 采用 MIT License |
| SRC-20260906-think-asr-alt-10 | whisper.cpp | https://github.com/ggml-org/whisper.cpp | 官方仓库 README／ggml-org | complete | C／C++、CPU-only、Android、离线设备侧示例、量化、C API、MIT 仓库许可证 |
| SRC-20260906-think-asr-alt-11 | whisper.cpp | https://github.com/ggml-org/whisper.cpp/blob/master/examples/whisper.android/README.md?plain=1 | 官方 Android 示例 README／ggml-org | complete | Android 示例把模型和样本放入 app assets，并建议 tiny／base 模型 |
| SRC-20260906-think-asr-alt-12 | whisper.cpp | https://github.com/openai/whisper | 官方模型仓库 README／OpenAI | complete | 多语言模型、模型规格与相对资源需求、非英语能力、整文件按 30 秒窗口转写 |

预算汇总：Vosk 3；WeNet 3；ONNX Runtime Mobile + SenseVoiceSmall-onnx 3；whisper.cpp 3；跨候选公共页面 0；合计 **12/18**。本轮不再扩展页面。

## Evidence Card：Vosk

### E-VOSK-01｜中文、离线、Android 与流式路径

- Claim: Vosk 官方资料明确列出中文，支持离线移动设备和 Android，并提供流式／连续识别能力。
- Evidence: SRC-20260906-think-asr-alt-01；SRC-20260906-think-asr-alt-02。
- Evidence type: Observed。
- Source class: B（项目官方文档与官方仓库 README）。
- Limits: 官方页面没有在本轮证据内固定具体 Android release、arm64-v8a ABI、最低 Android 版本或 Xiaomi 15 性能。
- Product implication: 满足“中文 + Android + 本地离线 + 不强制上传原始音频”的硬筛选基础，适合优先进入未来安全 intake 选择决策。

### E-VOSK-02｜体积、许可证与来源

- Claim: 官方介绍把便携模型描述为约 50 MB；官方模型目录列出约 42 MB 的小型中文模型及 Apache-2.0，runtime 仓库同样标为 Apache-2.0。
- Evidence: SRC-20260906-think-asr-alt-01；SRC-20260906-think-asr-alt-02；SRC-20260906-think-asr-alt-03。
- Evidence type: Observed。
- Source class: B。
- Limits: 本轮没有取得模型文件、散列、发布签名、SBOM 或固定 release；许可证识别不替代法律审查。
- Product implication: 四个候选中，它对 P0 的体积和来源边界最清晰，但仍不能直接下载或采用。

### E-VOSK-03｜个性词表与剩余隐私缺口

- Claim: 官方资料明确说明词表可以快速重配。
- Evidence: SRC-20260906-think-asr-alt-01；SRC-20260906-think-asr-alt-02。
- Evidence type: Observed。
- Source class: B。
- Limits: 词表重配是否适用于选定中文模型、动态更新代价、专名准确率、内存 PCM API、原始音频是否可能被 sample／日志／缓存落盘、buffer 释放均未验证。
- Product implication: 个性词表能力状态优于其他候选，但 P0 的 90% 专名门槛仍须实测。

## Evidence Card：WeNet

### E-WENET-01｜中文、Android 与流式路径

- Claim: 官方 runtime 文档描述流式／非流式统一模型、Android device 路径和逐帧输入；官方模型文档列出多组中文 runtime 模型。
- Evidence: SRC-20260906-think-asr-alt-04；SRC-20260906-think-asr-alt-05。
- Evidence type: Observed。
- Source class: B。
- Limits: 本轮官方页面没有给出可固定的 Android arm64-v8a、CPU-only 包、最低系统、完整 Java／JNI API 或内存 PCM 接口合同。
- Product implication: 产品能力方向相关，但 Android 接入与验证成本明显高于 Vosk。

### E-WENET-02｜runtime 与模型许可证不闭合

- Claim: WeNet runtime 仓库采用 Apache-2.0；模型文档说明预训练模型许可证跟随相应数据集许可证。
- Evidence: SRC-20260906-think-asr-alt-05；SRC-20260906-think-asr-alt-06。
- Evidence type: Observed。
- Source class: B。
- Counterevidence: 在每候选三页预算内，没有关闭一个具体中文 Android runtime 模型的数据集许可证文本、模型权利边界和可重分发条件。
- Product implication: 不满足本轮“runtime 与模型许可证／来源均可识别”的硬筛选，不进入 shortlist。

### E-WENET-03｜工程边界未知

- Claim: 逐帧输入和设备 runtime 暗示可以设计本地流式处理。
- Evidence: SRC-20260906-think-asr-alt-04。
- Evidence type: Inferred。
- Limits: 是否强制文件路径、音频落盘／日志、buffer 释放、模型大小、内存占用、热词机制、目标设备性能与可复现依赖闭包均为 Unknown。
- Product implication: 若未来补齐模型许可证，仍需要单独的高成本预 intake；本轮不推荐。

## Evidence Card：ONNX Runtime Mobile + SenseVoiceSmall-onnx

### E-ORTSENSE-01｜Android 设备侧 CPU runtime

- Claim: ONNX Runtime Mobile 官方文档支持在 Android 上通过 Java／C／C++ 将模型加载并运行于设备，所有目标默认支持 CPU；文档也展示 arm64 库尺寸示例。
- Evidence: SRC-20260906-think-asr-alt-07。
- Evidence type: Observed。
- Source class: B。
- Limits: arm64 尺寸是文档中的 ONNX Runtime 1.18／ResNet 示例，不是本候选当前 ASR 组合的精确体积、版本或性能。
- Product implication: 提供可识别的 Android 本地 CPU 推理底座，但不是开箱即用的 ASR SDK。

### E-ORTSENSE-02｜中文模型、体积与双许可证

- Claim: iic 官方 ModelScope 页面摘要把 SenseVoiceSmall-onnx 标为中文 ASR ONNX 量化模型，约 241.59 MB、Apache-2.0；ONNX Runtime 官方 LICENSE 为 MIT。
- Evidence: SRC-20260906-think-asr-alt-08；SRC-20260906-think-asr-alt-09。
- Evidence type: Observed（模型页为 partial extraction）。
- Source class: B。
- Limits: 模型页正文未完整抽取；未固定模型文件、散列、依赖、tokenizer、前后处理实现或精确 runtime release。
- Product implication: runtime 与模型来源／许可证可分别识别，满足研究阶段硬筛选，但 intake 首项应复核模型页及完整依赖边界。

### E-ORTSENSE-03｜组合路线的关键推断

- Claim: 由设备侧 ONNX runtime 与中文 ONNX 模型可以构成“不强制把原始音频发送云端”的候选路线。
- Evidence: SRC-20260906-think-asr-alt-07；SRC-20260906-think-asr-alt-08。
- Evidence type: Inferred。
- Counterevidence: 官方页面没有证明 Android 端完整的音频预处理、特征提取、tokenizer、解码、标点和长音频切分均可在本地且由同一许可证闭包实现；内存 PCM 输入也未证实。
- Product implication: 可列为第二候选，但属于高复杂度组合路线；任何一个缺失组件要求云端、文件落盘或来源不清，都应在 intake 早停。

## Evidence Card：whisper.cpp

### E-WHISPER-01｜Android、CPU-only 与离线路径

- Claim: whisper.cpp 官方 README 声明 C／C++、CPU-only、Android 支持和设备侧离线使用，并提供 C API 与量化路径。
- Evidence: SRC-20260906-think-asr-alt-10。
- Evidence type: Observed。
- Source class: B。
- Limits: 本轮没有固定 Android ABI 包、JNI 接口、runtime release、准确体积或最低系统。
- Product implication: 平台方向相关，但不足以单独满足全部硬筛选。

### E-WHISPER-02｜Android 示例与文件导向风险

- Claim: 官方 Android 示例把模型和音频样本放入 app assets，并建议使用 tiny／base 模型。
- Evidence: SRC-20260906-think-asr-alt-11。
- Evidence type: Observed。
- Source class: B。
- Counterevidence: 该示例是文件／assets 导向，本轮页面没有证明生产 API 可直接消费内存 PCM 并保证不落盘。
- Product implication: 与“按住说话后仅内存转写、原始录音不落盘”仍有待关闭的接口边界。

### E-WHISPER-03｜中文与模型权利证据不足

- Claim: OpenAI Whisper 官方 README 说明模型为 multilingual、支持非英语，并给出模型规格和整文件 30 秒窗口处理方式。
- Evidence: SRC-20260906-think-asr-alt-12。
- Evidence type: Observed。
- Counterevidence: 本轮选定官方页面没有明确写出 Mandarin／Chinese；也未在 runtime 许可证之外分别关闭模型权重的精确许可证／重分发范围。
- Product implication: 按“不以常识或模型知识补齐官方缺口”的合同，中文与模型许可证硬筛选失败，不进入 shortlist。

## Evidence Eval

- Decision Alignment: 15/15
- Source Quality: 18/20
- Citation Coverage: 18/20
- Fact/Inference/Unknown Separation: 15/15
- Counterevidence: 9/10
- Decision Value: 8/10
- Maintainability: 9/10
- Total: **92/100 · pass**

扣分原因：SenseVoiceSmall-onnx 官方页面只有部分抽取；没有在预算内固定候选版本、制品身份或目标设备结果；WeNet 和 whisper.cpp 的硬缺口被保留，未以推断补齐。

