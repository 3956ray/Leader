# 两处 websocket 注释的离线人工复核

RESULT：COMPLETE。两处精确命中均为 `comment_only_nonoperative_for_this_body`。

仅读取获批的 `online-recognizer.h` 正文（7,939 字节）及同文件必要上下文。第 57、60 行都是结果结构体中的普通行注释，说明相邻布尔字段被服务端使用；注释自身不执行网络操作。文件、Git blob、正文、两处行哈希和字节区间均已核验。

相邻字段仍是实际数据声明，注释所指的服务端用途不能被忽略。本结论不证明这些字段、依赖或运行时没有 WebSocket 能力，也不批准整个文件。没有读取任何被引用的实现文件。

冻结工具、旧运行与待审状态均未修改；规则没有全局豁免，新的获取尚未授权。工具目前没有接收这类人工裁定的接口，后续交产品经理决定是否批准一个精确绑定证据的离线方案，或暂停该路线。

完整逐项证据：[复核记录](/Users/orderly_ray/Leader/orchestration/reports/CP2-ASR-REAL-COMMENT-CAPABILITY-REVIEW-001.json)；SHA256 `0d8b34a06960a2c82a07effc376b60efe3c06aea1c968fb5a83b160c0d0519e6`。
