# 单文件热词消费端审查结果

RESULT：**PRODUCT_DECISION_REQUIRED**。本次获取和局部审查已完成，并在下层实现缺口处停止；制品仍为 **manual_review**，CP2 未通过。

只发出一次固定请求，取得 `online-recognizer.cc` 8,993 字节；Git blob 与 SHA-256 均匹配。没有重试、第二文件、重定向或元数据请求。本次授权已消费。

可见证据共 28 行／1,237 字节：

- `Register` 将 `hotwords-file` 注册到文件参数。
- `Validate` 对非空文件参数要求 `modified_beam_search`。可见另一分支在参数非空时调用 `FileExists`；若返回 false，会把路径值传给错误日志宏并返回 false。空值仅绕过这个局部调用，不能证明完整纯内存路径。
- `ToString` 包含该参数，说明存在配置诊断输出表面；未观察运行时日志或实际数据泄露。
- 构造函数将配置传给 `OnlineRecognizerImpl::Create(config)`。文件引用的 `online-recognizer-impl.h` 未读取；到此停止。

正文中没有精确 `hotwords_buf` token，但这不能证明下层不支持 buffer。`FileExists` 的实现、实际文件操作、完整选择逻辑及 App 可达性均未验证。

首次扫描因 `.cc` 后缀被归类为非文本，不能算源码检查通过；已保留该结果，用逐字节相同的私有 `.cpp` 副本补齐文本覆盖。文本扫描为 1 个文本、0 个跳过、0 个发现，只表示没有命中配置规则，不构成采用批准。

产品仓库仍为 `bd0bb57e`，工作区干净。原始响应、正文及扫描全文只在私有目录；未执行第三方代码、构建、模型加载或 App 修改。旧 run、冻结规则、隐私和 Checkpoint 边界保持。

下一步：产品经理基于派生证据决定路线；不得自动获取第二文件。
