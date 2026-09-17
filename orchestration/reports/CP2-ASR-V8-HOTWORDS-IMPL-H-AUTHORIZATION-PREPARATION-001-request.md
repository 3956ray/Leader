# 最后一个热词链文件：待批准请求

状态：**PENDING_USER_APPROVAL**。尚未读取或获取该正文；此请求不是授权。

只确认 `OnlineRecognizerImpl::Create(config)` 是否在此有定义，以及直接配置处理能否提供文件／内存热词选择线索。**如果只有声明、目标不存在或继续委派，立即停止，并永久结束这条热词逐文件补证链，不再追第三文件。**

| 固定字段 | 值 |
| --- | --- |
| 后续任务 | `CP2-ASR-V8-HOTWORDS-IMPL-H-SINGLE-BODY-REVIEW-001` |
| 仓库 | `k2-fsa/sherpa-onnx` |
| commit | `917bed95c8e5c7c18aa4d69fea42e9ef8ef0a60e` |
| tree | `fd2c4e97c9f7499b6ed91c7c2854b4211f61bdc0` |
| 唯一文件 | `sherpa-onnx/csrc/online-recognizer-impl.h` |
| Git blob | `9c2b4b71d22b6757e9faa87d5b42f9e586a08456` |
| Git 类型／模式 | `blob`／`100644` |
| 精确正文大小 | **2,286 字节** |
| 预期正文 SHA-256 | `ee879c7618a637a24e6011b9e426a49550ef8cc76d10235f61c5b751569608f6` |

最多 **1 次 GET、0 重试、0 重定向、0 元数据请求**。仅固定 Git blob 接口，无账号、凭据、代理或额外网络探测。成功、失败或超时均结束机会。正文必须精确等于 2,286 字节，硬上限 262,144；响应实体另限 16,384 字节。连接／读取采用 10 秒无活动超时。

人工只看目标 factory、直接配置处理、选择／I/O 线索及最小函数／类型上下文，整个审查累计最多 **64 个唯一行、4,096 字节**；不能导出整正文。目标只有声明或没有定义就停止，不转向其他方法寻找替代答案。需要更多上下文、第二文件或超过可见预算时同样停止。

身份来自已验收提交的两份第一方清单：snapshot manifest `/entries/69` 与 discovery manifest `/files/61`；双方的版本、blob、mode、大小一致。首快照记录该文件未取得，后一次已验收发现清单提供历史内容摘要；本次仅核对派生记录和提交原字节，没有打开历史正文或原始元数据。

原始响应、正文和扫描全文仅保存在全新私有目录。扫描仅覆盖同一新正文；原结果和覆盖缺口如实保留，0 指标不代表安全。没有 include／symbol／`.cc`／`FileExists`／具体识别器跟随，没有源码执行、构建、加载、集成、v9 或规则修改。

任何结果都回产品决策门。当前路线仍暂停，CP2 未通过；旧 run、音频隐私、三步路径和所有真机门槛不变。

完整合同：[pending JSON](/Users/orderly_ray/Leader/orchestration/reports/CP2-ASR-V8-HOTWORDS-IMPL-H-AUTHORIZATION-PREPARATION-001-request.json)；身份来源：[identity sources](/Users/orderly_ray/Leader/orchestration/reports/CP2-ASR-V8-HOTWORDS-IMPL-H-AUTHORIZATION-PREPARATION-001-identity-sources.json)。

## 待用户明确批准的完整授权句

> 我批准 `CP2-ASR-V8-HOTWORDS-IMPL-H-SINGLE-BODY-REVIEW-001`：只针对 repository `k2-fsa/sherpa-onnx`、upstream commit `917bed95c8e5c7c18aa4d69fea42e9ef8ef0a60e`、tree `fd2c4e97c9f7499b6ed91c7c2854b4211f61bdc0`、path `sherpa-onnx/csrc/online-recognizer-impl.h`、Git blob `9c2b4b71d22b6757e9faa87d5b42f9e586a08456`、mode `100644`、decoded size `2286`，允许 1 次 GET 和一次离线局部静态审查；人工可见范围最多 64 个唯一行／4,096 bytes，只判断 `OnlineRecognizerImpl::Create(config)` 是否定义、config 的直接处理、file/buffer selector、文件 I/O 线索与是否继续委派。不得请求 metadata、重试、重定向、跟随任何 include／symbol／`.cc`／`FileExists`／具体 recognizer 或第二正文，不得构建、执行、加载、测试、集成、联网扩展、修改 detector/schema/freeze/旧 run、建立 v9 或形成 clearance。任一身份不匹配、超过 262,144 bytes、目标未定义或继续委派时立即停止并回产品决策门；该结果是热词源码链最后一次正文补证，不授权第三文件。本授权不批准源码采用、CP2、CP3 或父亲 Alpha。

单独批准的依据：[正式产品决定](/Users/orderly_ray/Projects/think/doc/cp2-v8-hotwords-consumer-route-decision-2026-09-06.md)“准备任务验收”和“Product Lead 授权模板”。上一份消费端获取授权已结束；这份新文件请求须展示后另获明确批准。
