# 完整第一方获取候选 v3：Leader 最终验收

RESULT：ACCEPTED。接受 complete_tool_candidate_ready_for_freeze，仅表示完整第一方候选通过冻结前独立验收；尚未冻结、映射或执行真实获取，不表示源码可行、CP2 通过或 CP3 获准。

提交 e4cd300ca50be776b7077f1d7fae783642a696a7；父项 926b06fc3513c60b96e494d7d5c087b2763d6064。仅新增 tools/asr_review_acquisition_v3/ 的 4,257 文件（含完整合成测试历史），工作区干净。

## 独立验证

Leader 已静态阅读完整生产调用链、严格输入与 Trust、metadata/blob 解析、传输、controller、parser、storage、网络防护与测试执行器。对 v2 派生差异逐项核对；新测试逐项阅读，原 66 项行为方法保留，唯一原测试变化为网络防护模块的允许导入库存断言。所有程序及 fixture 为第一方，依赖仅 Python 标准库。

最终提交的代码/schema/fixture 被复制到独立目录 /private/tmp/think-leader-v3-final-5pt99mc_。Leader 执行 python3 -B verify.py leader-a 和 leader-b，两轮各 100 项方法、293 条方法/子场景记录全通过，无跳过；实际网络事件与陷阱触发为零。

两轮规范化摘要均为 3c71fe3b2349759ee722dd986fc48ec962cc154d2249066d007e4d20eac355b8，与已提交 final-a/final-b 逐字节一致。每轮 407 份 JSON 证据逐字节相同，测试运行时间日志独立保留但不计入确定性比较。

Leader 另外使用不导入候选的 json/hashlib/base64 脚本，逐轮独立核对 293 条连续账本、12 个终态、40 次模拟调用的前置授权、24 份正文封装、58 个元数据/边归档片段的身份和哈希；容量溢出用例完整保存 12,002 条边，无后续请求。

机器结果见同名 -independent-verification.json；独立目录源码身份见同名 -final-location.json。独立运行证据已归档到同名 -leader-evidence/。

## 范围和验收覆盖

1. 完整输入入口调用实际候选解析、共享 controller 和 GitBlobTransport；只有底层连接/响应为自建替身。受信调用者提供独立 Trust，输入不能自设信任。
2. 固定设计/上游身份、按序九个 seed、路径/type/mode、五类预算和 policy/release hash 的严格类型、重复/未知字段及身份链负向测试通过。
3. metadata 身份结果先持久化再解析；blob 请求前 authorize 与 before_request 已在磁盘提交，替身在底层连接创建处核对。重定向/代理/重试/异常/预算/denylist 停止没有越过授权后的请求。
4. 完整 F1–F9、原 66 项和新增 34 项回归通过。缺 P0/人工/可达性/fixed-point 时不产生 feasible；source_verdict 始终 insufficient_evidence。
5. 正文保存为私有、带身份的 JSON 数据，metadata 分段保留；读取接口已实现。保存失败停止采用/解析/后继请求，不生成源码树或构建输入。
6. RV1 原候选在 216,171 字节自建正文下产生不可读取的终态，曾被 Leader 拒绝进入最终验收。修复后记录写读共同上限、状态预留、边分段及容量耗尽标记均有实测；原用例独立重现通过。完整最终提交的生产代码与该独立复验版本一致，新增容量耗尽测试也已在两轮最终复跑通过。RV1 关闭。
7. 4,256 项清单全部大小/SHA/普通文件属性一致，加清单本身共 4,257 个 HEAD blob 与工作区逐字节一致；来源/派生映射核实，v2 全部 302 文件与 da9279a 不变，正式决定/PRD不变，git show --check通过。详见同名 -git-verification.json。
8. 新增 file_audio 识别明确映射为既有文件音频禁止能力的保守检测，可能对非音频文件 API/注释误报；没有声称 denylist 实现未变或改变产品禁用范围。

## 不可变身份与限制

- 代码/schema/test bundle：dc57dd71af457cbc25501a61f1d11f5f107d758fddb20c76898e6667bdf2e436。
- 全文件集合摘要：5b3178f5d8b3640dde642aa7f8abdcc305e9f6c9c07ac7ae4084cfc3af509e69。
- file-manifest.json SHA-256：146eab132d189f1cfc69508ff6848370ff321b9bbf26bc851eaa936a16216300。
- REPORT.md SHA-256：457d6dfa4aef4cb144482b4445e0258a1585dc71ad124f69f07afc52da4f480a。

受信 run_input 调用边界、冻结后独立提供的 metadata 原始字节及 pins 是明确前提。没有命令获取 metadata，没有默认 pins，也没有在冻结时补代码的许可。下一任务只能固定已实现的完整 release、协议和合同；后续真实输入的字节数须从匹配既有固定摘要的 metadata 确定，不能用合成响应代替。

实际 DNS/TLS/HTTP/GitHub 兼容、真实 metadata/闭包/P0/许可证/人工能力可达性、制品/模型/构建/真机/性能/音频隐私均未验证。条件编译（包括 include guard）、宏、非唯一边等采取保守停止；这不是上游源码不可行结论。永久不可写或不可捕获终止不保证最终文件，同 UID 恶意并发不在保障范围。

旧准备尝试保持 BLOCKED；现有第三方 block/manual_review 不变，CP1 延后未删除，CP2 未通过、CP3/Alpha 未批准。
