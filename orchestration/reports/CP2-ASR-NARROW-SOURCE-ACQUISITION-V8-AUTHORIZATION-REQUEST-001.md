# v8 一次有限源码获取：待用户明确批准

状态：等待批准。此请求不构成 A 或获取许可；开发者空闲，尚未建立 A/T/input/N。

工具 C、原证据补录 P、审查承诺 K、执行冻结 F 和最终映射 M 均已分别通过 Leader 独立验收。下一步拟执行 **CP2-ASR-NARROW-SOURCE-ACQUISITION-V8-001**，只进行一次有限静态源码获取与证据记录。

## 此次批准的具体范围

- 使用已经验收且不可修改的 v8，从全新空私有隔离目录开始；只从 api.github.com 的 Git Data blob 端点取得固定上游版本的允许文件，不恢复旧运行或复用旧 corpus。
- 固定仓库 k2-fsa/sherpa-onnx，commit `917bed95c8e5c7c18aa4d69fea42e9ef8ef0a60e`，tree `fd2c4e97c9f7499b6ed91c7c2854b4211f61bdc0`。
- 上限 **96 个文件、1,048,576 字节解码正文（1 MiB）**；仅 LICENSE 及 sherpa-onnx/csrc/ 下符合冻结路径和角色要求的普通 .h/.cc blob100644。9 个起始文件依次为：

1. `LICENSE`
2. `sherpa-onnx/csrc/online-recognizer.h`
3. `sherpa-onnx/csrc/online-recognizer.cc`
4. `sherpa-onnx/csrc/online-recognizer-impl.h`
5. `sherpa-onnx/csrc/online-recognizer-impl.cc`
6. `sherpa-onnx/csrc/online-stream.h`
7. `sherpa-onnx/csrc/online-stream.cc`
8. `sherpa-onnx/csrc/online-model-config.h`
9. `sherpa-onnx/csrc/version.h`

允许在这些文件内按冻结的静态 include 规则发现范围内的后继；每次请求前均必须通过身份、路径、角色、denylist、预算和持久化检查。遇到 active/uncertain deny、词法歧义、不支持的预处理形式、未知或冲突裁定、证据/文件安全/容量或网络失败等任一停止条件，即结束本次尝试。不得临场改工具、绕过、重试或续跑。

人工映射仅覆盖同一精确 body 中原两处 comment occurrence；由冻结 controller 对新取得的 body 重建完整身份后判断。不能扩展到相邻字段、API、实现、源码许可或能力不可达。原 pending、分析、ledger 和旧终态不改写；新裁定只能产生新 run 的追加证据。

设计合同仍为 commit `a57f643bac24edef5d6601b8a59baa77060f3d2c`、tree `31376c73f43caf3bbfd664d8316ffecdc589379d`、28 项输入集合 `c318c5a5f91d4af1d2759895ab9d5296c5784eaa214548b92f25fba4096764d2`。

## 精确冻结身份

| 绑定 | 精确身份 |
| --- | --- |
| 产品准备完成提交 | `6b83f40e75cbb501102207018658f6de15a79ff2` |
| C bundle SHA256 | `9bd39cec857137703c205b92b755eca200c58a2345d197a1ce853825cd1fe1bf` |
| F 冻结提交 | `75a9349c2e54d18a46dacddad762e7e669e9fbc2` |
| runtime F.json SHA256 | `c6e59308eb1ae72ce3d42e1c5678656d0f9442a3baaf8e503867368c98a9bad4` |
| M 映射提交 | `6b83f40e75cbb501102207018658f6de15a79ff2` |
| M.json SHA256 | `661615944e4d565dba2e9fd8ad4da759a4cff6dd5654c721360411da6d347ea0` |
| policy SHA256 | `abf2119febd5cadeb76943d0fce72606cba842b2fab5b24dd2e43ba040be62b0` |
| intake SHA256 | `1e7ba2c62a848fdfa0349cc8d30a8eaedb2d3dbd745a85dbdb584a57f27d1146` |
| K SHA256 | `8c90922477a24040e22a34800caeadbf6d9e4d8929097ac946c23a8560c6ecce` |
| F 独立验收 SHA256 | `4f35f0fd8efe2dff2950148cf9d8e72599fbb70e675db2147a1f35da3a6fb8e9` |
| M 独立验收 SHA256 | `afc74ff5c1e6023bbf5846203c688a6132c1229774717330e991b6e8f8a55c2d` |

M.F 绑定上表 runtime F 摘要，不使用 supporting freeze.json 摘要。规范范围及所有精确引用保存在同名请求 JSON（SHA256 `2114259dc42837e96d938c65bce2b165ee47836623408c4377ffb8d11d5a392b`）；该 JSON 也只是待批准请求。

## 输入例外与执行前检查

只允许在批准后重新核验既有两份固定身份输入：

- `/private/tmp/think-frozen-metadata-preflight-_6wsajyf/commit.json`，2336 bytes，SHA256 `e020549c1a78964acc8e400091ee54ba29f29ffd08e5b919a1bf06801dd68089`。
- 同目录 `tree.json`，2742250 bytes，SHA256 `7643e529ba6588e5dbe425acb624569218596a6316a1be9bc7d55bacd105ccd2`。

这两项是历史身份输入例外，不是旧源码复用。本轮仅从历史派生记录取得上述身份，未重新打开；批准后必须 no-follow、限量、普通单链接和精确摘要核验。缺失或改变即停止，不自动联网替换，不访问同目录其他材料。

冻结限制还包括 metadata 单项8MiB、单blob响应1500000 bytes、总raw16MiB、input65536 bytes、连接/读取超时各10秒、无凭证/proxy/redirect/retry，及固定证据容量。批准后先记录你的原文和本请求hash，才建立绑定 F/M/policy 的新 A；Leader 再从独立验收及授权 pins 构造受信输入映射并验收，最后单独下发一次 run_input 调用。输入不得任命自己的 Trust，执行前身份变化必须停止。

## 明确不批准

本次不允许第三方代码执行、构建、安装、依赖或模型获取/加载/推理、音频操作、产品集成、源码导出成可采用快照，也不批准 CP2 通过或 CP3/父亲 Alpha。第三方正文与完整扫描上下文留在私有目录，Git 只提交派生身份、预算、停止和验证报告。原始音频不落盘、不上传、不进日志；三步录入/找回及 CP1/Conformer Deferred, not removed 保持。

## 为何需要这次批准

最新正式决定 [原 token 证据补录决定](/Users/orderly_ray/Projects/think/doc/cp2-review-token-provenance-decision-2026-09-06.md) 的后续顺序要求：只有 F/M 完成后，才请求全新的 acquisition A；P/K/F/M 和以前的“继续开发”不构成这次真实获取授权，旧获取授权不可复用。现在 F/M 均已验收，请求已精确绑定，因此只需对本次具体范围做出决定。

若你回复“批准”，Leader 会把这条回复仅记录为本请求所述**一次**尝试的批准。若你缩小范围，以你的明确限制为准；未收到批准前不建立 A/T/input/N，不下发获取任务。
