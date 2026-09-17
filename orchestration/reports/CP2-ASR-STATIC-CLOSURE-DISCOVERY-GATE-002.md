# CP2-ASR-STATIC-CLOSURE-DISCOVERY-GATE-002 验收报告

- TASK RESULT：`BLOCKED`
- TASK 结论：`ACCEPTED`
- ARTIFACT VERDICT：`manual_review`
- 提交：`0ded8eb54e5d4d529759b46c62b9b5eb10722fbb`

## 验收结论

任务正确形成了有界、可追溯的静态发现证据，并在 Leader 收敛指令后停止；接受的是“按授权获取、诚实暴露边界缺陷并停止”，不是接受 discovery corpus、候选 allowlist 或 sherpa-onnx 构建输入。当前材料不得进入阶段 B。

阻塞不只来自未达到固定点：冻结排除规则没有覆盖 `wave`，导致 seed `sherpa-onnx/jni/jni.cc` 的确定性 include 合法取得 `wave-writer.h`，该头文件明确暴露按路径写 WAV 的 API；冻结 JNI/Kotlin/API 表面同时包含 `ADSP_LIBRARY_PATH` 修改、QNN/RKNN provider/config 与 native library load。现有材料不能证明 CPU-only、ASR-only、原始音频不落盘的最终边界。

## Leader 独立复核

- 官方 commit/tree 响应分别为固定 `917bed95...a60e` 与 `fd2c4e97...bdc0`；tree `truncated=false`、8,585 项、6,545 blobs、275 个 symlink mode，metadata SHA-256 与报告一致。
- `discovery-policy.json` SHA-256 为 `a5f9e9206a4b08c73c531c8c62b56dd2943ab5537fc8f8bf71bbef54642cf41b`；38 个 seed、允许根和 256/2 MiB 上限与 Leader 合同精确一致。文件时间证明 policy 早于 corpus 首个正文，冻结证据的合同哈希一致。
- Leader 独立复算 615 条 canonical JSON ledger 哈希链，序号/前序哈希/记录哈希全部连续；终端哈希 `ac5ac1fc6e3cf733108fac14cece50e5f3088dc3fa24efc99b217e96d843f397`，ledger SHA-256 `8b58b9ae18a46a7fb46c5141dbbaf183b43d1da7b4e597f32b9e77143b8ef4cf`。112 个 corpus 文件全部有事前 fetch authorization；仅 `offline-zipformer-ctc-model-config.h` 已授权但未取得。
- Leader 对 112 个文件重新计算实际大小、Git blob SHA-1 语义、内容 SHA-256、API response SHA/大小与 response SHA-256，全部与 manifest 一致；实际集合与 manifest 完全相等，总计 499,282 字节。
- Leader 独立 lstat 得到 6 个目录、112 个普通文件、0 symlink、0 hardlink 异常、0 特殊文件；全部正文可按 UTF-8 解码且无 NUL。
- Leader 在新临时输出目录复跑 `scan-untrusted-code 1.1.2`，JSON/Markdown 与提交副本逐字节一致：`sandbox_only`、40/100、2 个不可达 high、0 block signal、0 skipped/unreadable。两项分别是 CMake 帮助字符串和 logger 调试提示字符串，人工解释成立，但不解除架构/闭包阻塞。
- Leader 逐行确认：`jni.cc:12` include `wave-writer.h`；其头文件暴露 filename/path WAV 写入；`common.cc` 读取/修改并记录 `ADSP_LIBRARY_PATH`；Kotlin/JNI/Core 表面含 QNN/RKNN 配置、分支和 `System.loadLibrary`。报告所述边界缺陷成立。
- 三个任务内解析器均为提交中的 100644 证据文件；Leader 以 AST/静态关键词复核，未发现 subprocess、shell、eval/exec/importlib 或执行 corpus 的路径。网络获取器限制到 `api.github.com`，离线 finalizer 只读 corpus/响应并生成证据。
- 提交只新增指定安全审查目录的 22 个证据/解析器文件；没有 corpus 正文、tree/blob 响应、产品源码、第三方二进制、模型或音频进入 Git，产品仓库最终工作区干净。

## 固定点与停止说明

- 收敛时恢复进程正在等待 GitHub API 限流；Leader 明确要求停止新增正文，进程以 SIGINT/130 结束，停止后零新增正文。
- 当前 `fixed_point=false`，两条内部边未取得/处理；因此 101 项候选路径只是未冻结、未闭合的 evidence-only candidate，不能成为最终 allowlist。
- 即使补齐两条边，已确认的 WAV 写文件与 ADSP/QNN/RKNN 宽表面仍足以阻止当前 policy 产生符合目标的最终边界；继续不能在本任务内通过重冻、删文件或修改源码解决。

## 后果与未验证

- discovery corpus verdict=`manual_review`，不得作为最终快照、构建输入、依赖批准或产品集成输入。
- 阶段 B 未批准；CP2 未通过，CP3 未批准；源码归档 `block`、AAR/Zipformer/首次部分快照 `manual_review`、Conformer `Deferred, not removed` 保持不变。
- 下一步必须由产品经理/Product Lead 决定：是否先批准一个纯设计的 CPU-only/ASR-only 窄 API/适配边界，或暂停 sherpa-onnx 路线并重新选择运行时。不得在本任务内继续获取、重冻或修改产品源码。
