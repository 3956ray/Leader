# v4 新冻结独立验收

RESULT: ACCEPTED。接受提交 2f4760d0ff3ea78de929198fba88d3744353a321 的三份新冻结文档，父项 524c6484b1290cd2556ebf9a1031a4d00b273a86。冻结目录 tree b97e96fe5e413da2859d967e2aac9bfd0334fbf6。

Leader 已完整阅读 REPORT 和 freeze 全部字段，独立重算 canonical JSON、1024 项完整清单、原 1023 项清单、18 文件代码 bundle、policy 和文件/Git blob 身份；逐个核对普通单链接及 0600/0644 属性。27 份正式来源/外部派生证据的大小与 SHA 均匹配，真实解析记录与 Leader 原报告相等。

- freeze.json SHA-256：a9961c8243a75e244517428f53fed87374cd190a5114d5f62193826337196305。
- MANIFEST.json SHA-256：d11f799d37a9d5ada92071109cdbcc4d267e2eeb9bc6e1b034607b2bc2992fb7。
- REPORT.md SHA-256：61aac5e0165b49cbb09333443de0b29af9daa43451ebf982db5da257409e1a44。
- 完整 1024 记录集合 SHA-256：36ec2210a02d58b4c712c1d6f354c356188748f1a380b0b608a1ee4e9ae6970d。
- 18 文件 bundle SHA-256：642d29885efb5df375564d0ebeec0875d4701e5dfc816934de329d3c2dda42d0。

旧 v2/v3/v4/旧冻结四个范围的 Git tree 和提交差异均未变。三个新文件范围、父项和干净工作区符合合同。只调用已验收的 policy/bundle 纯身份函数，NetworkGuard 记录为空；未读真实 JSON、未运行获取或测试、未改代码。

policy、deny 检测、确定性处理规则与已验收旧策略相等；fixed_scope 原字段和原始 immutable contract 逐项相等。新增名称双层表示只修复已正式批准的惰性元数据兼容，不扩大实际路径授权。metadata_exception 不清除其他制品 verdict，也不单独构成正文授权。

freeze 中 pending 是文档形成时的历史状态；本外部验收记录接受其精确字节，不修改或补签原文。详细机器证据见同名 `-verification.json`。

下一步可由 Leader 单独将既有精确正文授权映射到此已接受 release 并派发有界任务。真实网络、源码闭包/P0/许可证/人工可达性、构建/模型/实机/动态音频隐私均尚未验证；CP2 未通过，CP3/Alpha 未批准。
