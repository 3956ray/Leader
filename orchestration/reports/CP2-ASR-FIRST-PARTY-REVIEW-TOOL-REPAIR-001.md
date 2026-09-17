# 第一方离线审查工具：Leader 验收

任务：CP2-ASR-FIRST-PARTY-REVIEW-TOOL-REPAIR-001

结论：ACCEPTED。开发者 RESULT=COMPLETE；tool_ready_for_freeze 仅覆盖离线核心、schema 与合成证据候选。未进行正式冻结，不具备真实获取入口，不是源码可行或 CP2 通过。

提交：da9279a411d990e4c37191e22be680b2c4bfcb07；父项：5c882ec880022cfd053ed16dc15f1bb4d7e43e3b。

## 验收依据

- Leader 已逐项静态阅读 policy、parser、controller、adapter、storage、audit、verify、测试和自建 fixture。依赖为 Python 标准库；正文只作为数据解析，没有第三方代码执行或网络入口。
- F1–F9 与六类验收要求具备行为测试映射。非唯一 include、条件/宏/非法语法采取显式登记后停止；denylist 发现后无后续请求；缺少 P0/人工/可达性/fixed-point 证据无法产生可行结论。
- Leader 在独立目录 /private/tmp/think-leader-offline-v2-jsp__lbn 复制 11 个源码/fixture 文件，执行 python3 -B verify.py leader-a 和 leader-b：两次各 66 个测试、117 条测试及子场景记录全部通过，危险运行时事件为零。
- 两次规范化结果逐字节一致，SHA-256：9d86eccf2c898a772e9973f34faeec4b04cab5ccb258aaaba15ca04772fa4954；与开发者最终提交 run-a/run-b 也逐字节一致。
- Leader 用独立 json/hashlib 脚本（不导入工具）重算两次各 83 条账本的连续序号、前序与当前哈希、终态证据哈希，并检查调用身份能对应先前授权。denylist 与短写停止证据符合要求。
- 最终提交后重新比对 11 个独立复跑输入哈希，完全未变；无需重复执行相同测试。
- 最终核对新增 302 文件全部在 tools/asr_review_offline_v2/；清单内 301 个文件的大小、SHA-256、普通文件属性和 HEAD 内容全部一致，其余一项为清单本身。git show --check 通过，工作区干净。未新增第三方依赖或产品实现。
- 旧尝试五个第一方文件哈希全部未变；正式决定和 PRD 哈希未变。没有读取或枚举旧 corpus。

最终机器检查见 CP2-ASR-FIRST-PARTY-REVIEW-TOOL-REPAIR-001-final-verification.json。独立运行证据和源码身份已归档到 CP2-ASR-FIRST-PARTY-REVIEW-TOOL-REPAIR-001-leader-evidence/。

开发者报告：/Users/orderly_ray/Projects/think/tools/asr_review_offline_v2/REPORT.md，SHA-256 b3c008c85547c0adac0292412369f568ce08ec24682642b1983e9cfb84abc12c。文件清单 SHA-256 9168b74fff58840d1529015432f3bf5ed59a87fc5725b8b4a5ef8b4edcdd65c0。

## 限制与下一阶段

当前 adapter 和入口只接受 project-synthetic 输入；source_verdict 始终为 insufficient_evidence。真实 HTTP/API 传输、元数据身份导入和真实输入协议尚未实现或验收。不能把本次候选冻结包装为完整真实获取 release，不能在冻结任务中临时补代码。

完整 C++ 预处理、真实闭包/P0/许可证、真实网络资源限制、模型、真机、性能及动态音频隐私均未验证。永久磁盘不可写、不可捕获终止、同 UID 恶意并发不在已证明的终态保障中。

后续先升级产品经理明确“第一方真实获取组件与输入协议的离线开发”范围；开发阶段仍用完全自建合成响应、禁止实际网络。完整可执行工具通过独立验收后再单独冻结，最后另行映射既有精确授权并调度真实获取。本次不冻结不完整 release，也不请求重复用户授权。

旧源码准备尝试保持 BLOCKED；现有第三方 block/manual_review 不变，CP1 Deferred, not removed，CP2 未通过、CP3 未批准。
