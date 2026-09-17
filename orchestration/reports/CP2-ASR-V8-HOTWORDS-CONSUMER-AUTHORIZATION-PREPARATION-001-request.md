# 单文件正文与局部静态审查：待批准请求

状态：**PENDING_USER_APPROVAL**。这份文件不是获取授权；尚未发起请求。

目标是确认热词配置是否从文件读取、能否只使用内存文本，以及实现是否仍委派给其他文件。若需要其他文件，本次立即停止，不会自动追加。

| 固定字段 | 值 |
| --- | --- |
| 后续任务 | `CP2-ASR-V8-HOTWORDS-CONSUMER-SINGLE-BODY-REVIEW-001` |
| 仓库 | `k2-fsa/sherpa-onnx` |
| commit | `917bed95c8e5c7c18aa4d69fea42e9ef8ef0a60e` |
| tree | `fd2c4e97c9f7499b6ed91c7c2854b4211f61bdc0` |
| 唯一文件 | `sherpa-onnx/csrc/online-recognizer.cc` |
| Git blob | `20d4646bb5c6ffbe714848cc497e1809113d5195` |
| Git 类型／模式 | `blob`／`100644` |
| 精确正文大小 | **8,993 字节** |
| 预期正文 SHA-256 | `c872eb5cdf4f4e25b133e79cfd156343782f61a344efba7b3aef4a6f3d1e1b79` |

只允许向固定 Git blob 接口发出 **1 次请求**。成功、失败或超时均结束本次机会；不重试、不续跑、不跟随重定向。正文须精确等于 8,993 字节，硬上限 262,144 字节；响应实体另限 65,536 字节。无需账号、代理或凭据，不请求 commit/tree 元数据。

人工只查看热词相关命中和最小函数／类型上下文；不导出整文件。原始响应、正文及必要扫描片段仅保存在全新私有目录。只交付派生身份、局部观察、缺口和核验结果。

身份不匹配、超限、文件保护或持久化失败，或出现其他禁止能力时立即停止。需要第二个文件、include、symbol 或依赖时，只记录缺口并返回产品决策。没有第三方执行、构建、模型加载、集成、新v9、规则修改或clearance；此前的run、硬停止和pending不变，CP2/CP3/Alpha仍未批准。

身份来自两份已验收提交的第一方清单：`69521677…` 的 snapshot manifest `/entries/74`，以及 `0ded8eb5…` 的 discovery manifest `/files/66`。二者均与当前提交原字节一致，mode、blob、大小及upstream commit/tree相互吻合。仅使用派生身份；未打开历史正文、raw metadata或scanner context，也未联网。既往制品仍为manual_review，历史任务验收不构成源码采用批准。

完整机器合同：[pending JSON](/Users/orderly_ray/Leader/orchestration/reports/CP2-ASR-V8-HOTWORDS-CONSUMER-AUTHORIZATION-PREPARATION-001-request.json)，来源核对：[identity verification](/Users/orderly_ray/Leader/orchestration/reports/CP2-ASR-V8-HOTWORDS-CONSUMER-AUTHORIZATION-PREPARATION-001-identity-verification.json)。

## 待用户明确批准的完整授权句

> 我批准 `CP2-ASR-V8-HOTWORDS-CONSUMER-SINGLE-BODY-REVIEW-001`：只针对 upstream commit `917bed95c8e5c7c18aa4d69fea42e9ef8ef0a60e`、tree `fd2c4e97c9f7499b6ed91c7c2854b4211f61bdc0`、path `sherpa-onnx/csrc/online-recognizer.cc`、Git blob `20d4646bb5c6ffbe714848cc497e1809113d5195`、mode `100644`、decoded size `8993`，允许一次正文获取和一次离线静态审查；只判断 `hotwords_file`／`hotwords_buf` 的直接消费、selector、空值行为与文件 I/O 线索。不得获取或跟随任何第二文件、include、symbol、依赖或 metadata，不得运行第三方内容、构建、加载、测试、集成、联网扩展、修改 detector/schema/freeze/旧 run 或形成 clearance；任一身份不匹配、超过 262,144 bytes、需要下一文件或出现其他禁止能力时立即停止并回产品决策门。本授权不批准 v9、源码采用、CP2、CP3 或父亲 Alpha。

需要单独批准的依据：[正式产品决定](/Users/orderly_ray/Projects/think/doc/cp2-v8-local-configuration-route-decision-2026-09-06.md)“Product Lead 新授权句”与“准备任务交付与验收”。旧获取授权已消费，不能覆盖这份新的正文请求。批准后才另行记录新授权与下发单文件任务。
