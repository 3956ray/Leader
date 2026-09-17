# 同一头文件的七处局部静态审查

RESULT：`active_paths_review_complete_for_product_decision`。当前停线保持。

5 个活动命中中，第 15 行是固定 include 文件名中的 decoder，局部没有运行时加载操作；其依赖实现仍未审查。其余 4 处涉及 OnlineRecognizerConfig 的 hotwords_file 字符串字段、构造参数及成员初始化：当前头文件确实允许传入并保存这一配置值。相邻 hotwords_buf 文档描述缓冲输入与文件输入的选择。这些是与路径边界有关的局部证据，不能仅当作无意义名称而放行；同时，它们不证明实际发生文件访问，也不证明未来业务接口会暴露该能力。

新增的两处 comment 分别描述 decoder 的尾部空白帧状态，以及热词缓冲输入替代文件输入；注释字节本身不执行操作。本次局部描述不构成 authority-map clearance，不能补写或解除旧 pending。

人工只查看目标行、相关注释、完整局部构造函数及最小 namespace/type 锚点；唯一读取的 retained 文件为本次 body-0002.json。七处完整 tuple、逐次可见行/byte/hash、具体局部数据流与未验证引用均在同名 JSON 和 read receipts 中。没有查看完整 header、其他正文或跨文件实现，没有网络请求、候选/扫描器/控制器运行或第三方执行。

按正式决定，已记录配置字段及传值这一最小政策相关证据，至此停止，建议保持当前 sherpa-onnx 获取/采用路线暂停并返回产品决策。是否值得继续取得别的实现证据必须另行决定；不进入 comment 映射、v9 或获取。

原 denylist_capability 和 4 对 2 的 complete-set rejection 保持；零成功 adjudication，源码仍 insufficient_evidence、fixed_point=false，CP2 未通过。许可、完整闭包、实际可达性、运行时和真机表现均未验证。
