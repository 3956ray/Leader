# 既有源码授权映射

RESULT: MATCHED。Leader 接受此映射；不新增或扩大 Product Lead 授权。

授权依据为已归档的 `CP2-ASR-NARROW-SOURCE-BOUNDARY-FEASIBILITY-AUTHORIZATION-001.md`（SHA-256 4ab16012743be83aaf997cddf5c721c284cbf7b046664dc6c6b3de8ff6183a1a）及原任务 immutable contract（SHA-256 440b006933714153d392bbe5e3774a1e2c52dca44cf2a504e3553a5deccd5185）。后续正式完整工具范围决定、metadata 兼容决定明确允许完整候选独立验收/新冻结后由 Leader 映射相同范围，无需重复用户确认。

已接受 v4 提交 524c6484b1290cd2556ebf9a1031a4d00b273a86；新冻结提交 2f4760d0ff3ea78de929198fba88d3744353a321；freeze SHA a9961c8243a75e244517428f53fed87374cd190a5114d5f62193826337196305；bundle SHA 642d29885efb5df375564d0ebeec0875d4701e5dfc816934de329d3c2dda42d0。原尝试保持终止，旧冻结不变，本次使用新任务和新隔离输出。

## 逐项对应

| 原授权字段 | 本次固定值/边界 |
| --- | --- |
| 设计合同 | a57f643bac24edef5d6601b8a59baa77060f3d2c；tree 31376c73f43caf3bbfd664d8316ffecdc589379d；28 项摘要 c318c5a5f91d4af1d2759895ab9d5296c5784eaa214548b92f25fba4096764d2 |
| 上游 | k2-fsa/sherpa-onnx commit 917bed95c8e5c7c18aa4d69fea42e9ef8ef0a60e；tree fd2c4e97c9f7499b6ed91c7c2854b4211f61bdc0 |
| seed | freeze.fixed_scope.ordered_seeds，与原归档 9 项及顺序相等 |
| 正文路径/类型 | LICENSE 或 sherpa-onnx/csrc/ 普通 .h/.cc；blob/100644、严格原始 ASCII 路径；denylist 前置拒绝 |
| 预算 | 最多 96 文件、1,048,576 解码字节；全部独立 raw/响应/证据上限保持冻结值 |
| 来源 | 仅由固定 tree 的 blob SHA 生成 api.github.com Git Data blob endpoint；不接受任意 URL，无代理/跳转/重试；不添加 metadata 网络端点 |
| 授权时序 | 已冻结 run_input/controller 在每个 blob 请求之前持久化 authorize 与 before_request；外层不得预取或伪装 synthetic |
| 派生规则 | 原确定性 include/deny/停止规则完全不变；触发即停止本次请求链，禁止修补代码/清单、重冻或续跑 |
| 禁止 | 旧 corpus/快照/受限制品、禁止能力、外部依赖/模型/音频/二进制、执行第三方源码、构建/安装/推理/集成/CP3 |

两份身份 metadata 的原始 pin 未变，纯解析兼容已验收。下一项真实获取任务只可读取 `/private/tmp/think-frozen-metadata-preflight-_6wsajyf/commit.json` 和 `tree.json` 这两个精确身份输入；不得枚举同级内容或旧 corpus。经 no-follow/目录链/普通单链接/有界读取再验 2336/2742250 字节与两个固定 SHA，复制至新私有位置，以已冻结 Trust/input_document/canonical/parse_input 导入。此实际输入用途依据原源码身份合同及完整获取协议的后续派单，不把“纯解析通过”单独当成新的正文授权或通用制品批准。

每次执行重新派生并记录 canonical input；2037 字节与 baab9ddac779808ad8a1ac79e1c76937bc5875cba335148c7984aa54e41810a2 仅作相同输入交叉核对，不能代替验证。外层只连接既有接口，不引入新解析/网络/授权实现。全部真实输入、正文和追加式证据留在新隔离目录，以编号惰性 JSON 保存，不导出源码树/快照/构建输入或提交产品 Git。

下一唯一任务为 `CP2-ASR-NARROW-SOURCE-ACQUISITION-V4-001`：执行一次冻结的有界正文获取并交付可独立重算的停止/完成证据和静态扫描。停止后允许整理该次已有证据，不能继续获取；完整 P0/人工可达性/源码可行性判断作为后续独立审查，不由工具 sufficient/feasible 代替。现有工具 source_verdict 保持 insufficient_evidence。CP2 未通过。
