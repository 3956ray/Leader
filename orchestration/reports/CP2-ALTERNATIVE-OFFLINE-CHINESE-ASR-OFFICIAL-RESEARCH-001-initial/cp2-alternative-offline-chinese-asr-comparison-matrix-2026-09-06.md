# CP2 替代离线中文 ASR 比较矩阵

Owner: Product Lead
Last updated: 2026-09-06
Source: cp2-alternative-offline-chinese-asr-evidence-cards-2026-09-06.md；SRC-20260906-think-asr-alt-01–12
Confidence: Medium-High（官方材料比较；全部运行时、安全、隐私与真机结果未验证）
Related decisions: cp2-hotwords-chain-termination-route-decision-2026-09-06.md
Next review date: 2026-09-13

Research Quality: 92 · pass
Validation Level: V2
Next evidence: 独立产品决策最多选择一个合格候选进入未来安全 intake
Allowed next investment: 决策文档；不得自动取得候选源码、模型或二进制
Pause/Kill condition: 合格候选不足两个，或未来 intake 无法关闭可复现来源、许可证、内存音频与隐私边界

标记：`O` = 官方材料直接观察；`I` = 基于官方材料的有限推断；`U` = 未验证。每个单元格均引用 Evidence Card 中的 Source ID。

## 十二维比较

| # | 维度 | Vosk | WeNet | ONNX Runtime Mobile + SenseVoiceSmall-onnx | whisper.cpp |
| --- | --- | --- | --- | --- | --- |
| 1 | 本地／离线与强制上传 | **O**：官方明确离线移动端；核心路径无强制云端描述。`01,02` | **I**：Android device runtime 支持本地执行；是否所有组件均无上传未明。`04,05` | **O+I**：runtime 在设备加载／运行；与本地 ONNX 模型组合不要求原始音频云端，但完整 ASR 链未证。`07,08` | **O**：官方列出离线设备侧使用。`10` |
| 2 | 中文与流式／录后 | **O**：明确中文、流式／连续识别。`01,02` | **O**：多个中文模型，支持流式／非流式。`04,05` | **O/U**：明确中文 ASR 模型；所选页面主要支持离线文件转写，Android 流式形态未知。`08` | **O/U**：multilingual／非英语与整文件 30 秒窗口；页面未明确 Mandarin／Chinese。`12` |
| 3 | Android／arm64／CPU | **O/U**：Android API；arm64-v8a、CPU-only 包与最低系统未固定。`01,02` | **O/U**：Android device；具体 arm64 ABI、CPU-only 发行包未固定。`04,05` | **O**：Android Java／C／C++，默认 CPU，文档含 arm64 库示例；候选精确包未固定。`07` | **O/U**：Android 与 CPU-only；精确 ABI／发行包未固定。`10,11` |
| 4 | 内存 PCM／stream 与文件路径 | **O/U**：有 streaming API，但本轮页面未明确 Android PCM 参数与是否完全无文件路径。`01,02` | **O/U**：逐帧输入概念成立；真实 Android 内存音频接口未知。`04` | **I/U**：通用 runtime 消费内存 tensor；音频预处理到 tensor 的完整 Android 链未知，模型页示例偏 PCM 文件。`07,08` | **U**：Android 示例为 assets／文件导向；所选页面未证明内存 PCM 生产路径。`11` |
| 5 | 音频落盘／上传／日志／释放 | **O/U**：离线降低上传需要；sample、日志、缓存、buffer 释放均未审。`01,02` | **I/U**：设备 runtime 可减少上传；落盘、日志和释放未知。`04` | **I/U**：可设计纯本地；前后处理组件是否落盘／记录／释放未知。`07,08` | **O/U**：离线可减少上传；Android 示例使用文件，生产隐私控制未知。`10,11` |
| 6 | runtime／模型大小与最低设备 | **O/U**：官方小模型约 50 MB，中文小模型约 42 MB；runtime 内存和最低设备未知。`01,03` | **U**：文档提到量化模型，但本轮没有可比较的目标包大小和设备要求。`05` | **O/U**：模型页约 241.59 MB；runtime 文档尺寸仅为旧版示例，组合内存／最低设备未知。`07,08` | **O/U**：模型参数与约 1 GB VRAM 参考，Android 推荐 tiny／base；实际 ggml 文件、RAM 与 Xiaomi 15 CPU 结果未知。`11,12` |
| 7 | runtime／模型许可证与来源 | **O**：runtime Apache-2.0；官方中文模型条目标 Apache-2.0，来源可识别。`02,03` | **O/U**：runtime Apache-2.0；模型随数据集许可证，具体中文模型权利未闭合。`05,06` | **O**：runtime MIT；模型官方页 Apache-2.0，Microsoft 与 iic 来源可识别；仍需法律及制品复核。`08,09` | **O/U**：runtime 仓库 MIT；模型权重精确许可证／重分发边界未在所选材料中单独关闭。`10,12` |
| 8 | 维护者／版本／发布渠道 | **O/U**：Alpha Cephei 官方站与仓库可识别；本轮未固定 release/version。`01,02,03` | **O/U**：WeNet 官方组织与文档可识别；未固定 Android release。`04,05,06` | **O/U**：Microsoft runtime、iic ModelScope 模型可识别；模型页显示 2024-09-26 更新，精确组合版本未固定。`07,08,09` | **O/U**：ggml-org runtime、OpenAI 模型来源可识别；精确 release／权重版本未固定。`10,12` |
| 9 | 词表／热词／短语偏置／后纠错 | **O/U**：明确可快速重配词表；中文适用性、动态代价与准确率未验证。`01,02` | **U**：本轮所选页面没有关闭 Android 中文热词机制。`04,05` | **O/U**：模型页摘要存在 hotword 示例线索，但没有证明直接 Android 支持或纯本地完整机制。`08` | **U**：所选官方页面未建立满足本产品的词表／phrase bias 合同。`10,12` |
| 10 | 小米 15 飞行模式／30–90 秒／90 秒×20／隐私可测性 | **I**：Android 离线与较小模型使测试设计可行；无实测。`01,02,03` | **I**：可设计设备测试，但包、模型与内存边界未闭合；无实测。`04,05` | **I**：Android CPU runtime 可设计测试，但组合链复杂、模型较大；无实测。`07,08` | **I**：Android CPU-only 可设计测试；30 秒窗口与文件导向风险需先关闭；无实测。`10,11,12` |
| 11 | 可复现供应链／安全门禁 | **I**：官方 runtime、模型和许可证入口清晰，可另立精确制品 intake；当前没有固定版本／散列。`02,03` | **I/U**：官方组织清晰，但 LibTorch、Android 包与模型数据集许可证形成多层闭包。`04,05,06` | **I/U**：两条官方供应链可分别固定，但前后处理／解码可能引入第三闭包；当前无制品。`07,08,09` | **I/U**：runtime 与上游模型组织清晰；模型权利、Android 包与音频路径需先闭合。`10,11,12` |
| 12 | 接入复杂度与主要未知 | **I：低至中**。已有 Android API、流式与小模型；未知集中于 ABI、PCM、隐私与准确率。`01–03` | **I：高**。LibTorch、模型许可、JNI／ABI、体积和热词均未闭合。`04–06` | **I：高**。runtime 只是推理底座，需完整本地预处理／tokenizer／decoder／长音频链。`07–09` | **I：中至高**。已有 Android 示例，但中文官方证据、模型权利、内存 PCM 与长音频行为未闭合。`10–12` |

## 硬筛选

硬筛选要求五项都存在官方材料支持：中文／普通话；Android 调用路径；本地／离线核心识别；runtime 与模型许可证／来源可识别；核心能力不强制上传原始音频。未知不按通过处理。

| 候选 | 中文 | Android | 本地／离线 | runtime + 模型许可／来源 | 无强制原始音频云端 | 结果 |
| --- | --- | --- | --- | --- | --- | --- |
| Vosk | PASS | PASS | PASS | PASS | PASS | **QUALIFIED** |
| WeNet | PASS | PASS | PASS（device runtime） | **FAIL：具体中文模型许可证未闭合** | PASS（有限推断） | **NOT QUALIFIED** |
| ONNX Runtime Mobile + SenseVoiceSmall-onnx | PASS | PASS | PASS（组合路线） | PASS（模型页为 partial extraction，intake 须复核） | PASS（组合推断） | **QUALIFIED WITH CONDITIONS** |
| whisper.cpp | **FAIL：所选官方页未明确中文** | PASS | PASS | **FAIL：模型权重范围未单独闭合** | PASS | **NOT QUALIFIED** |

## 排序与含义

1. **Vosk：第一优先 future intake 候选。** 产品匹配最直接，证据页同时覆盖中文、Android、离线、流式、小模型、词表和 Apache-2.0。它仍未通过任何安全、源码、模型或真机门禁。
2. **ONNX Runtime Mobile + SenseVoiceSmall-onnx：第二优先、条件式 future intake 候选。** 中文模型、设备侧 Android CPU runtime 与双许可证可识别，但它是组合路线，前后处理和解码闭包可能在 intake 早期失败。
3. WeNet 与 whisper.cpp 只保留为研究记录，不进入本轮 shortlist。除非未来正式决定重新开放官方证据预算并关闭硬缺口，不得为它们启动制品 intake。

本排序只支持“是否足以召开下一次安全 intake 选择决策”。它不批准下载、源码、模型、二进制、实现、构建、运行、真机测试、CP2、CP3 或父亲 Alpha。

