# 完整获取工具冻结：Leader 验收

RESULT：ACCEPTED。冻结提交 e2d64f98aae52bd5e015962191a3bf2c121beeb2，父项 e4cd300ca50be776b7077f1d7fae783642a696a7。接受三文件冻结产物，未执行真实获取。

Leader 已读取 freeze.json 与 REPORT.md 全文，独立重算 MANIFEST 的 4,257 文件集合、全部文件 SHA-256/Git blob/普通单链接属性，核对真实 Git tree bdd78d6fc5d2837bc2749d441659886c07406321。冻结 policy 与 Leader 独立测试时的规范化输入逐字节一致，摘要 ee9d1ae7b4b17d2d895d3a6e0b62f73bfda7eb8a9cfae50e9d264f9ed23fc627。

冻结合同 SHA-256：b64dc4823d1ba38280497fd7b95c56c690caf0b9392d91cb58f0c0df95a4061f；MANIFEST SHA-256：5b81a88e471a93d830ef635379e83f2bc96ece8e03aa14ad75a1ae1980fa2bde；REPORT SHA-256：4d46de81ba12e481f6449bca06f62c118cba74ed168ff2d0dd50ac582ffaf4f8。

两个 JSON 无重复字段，规范化字节及跨文件摘要一致，无自引用。来源文件摘要、组件/schema 摘要、设计/上游身份、按序九个 seed、原正式 denylist、96 文件/1 MiB 与两个真实 metadata pin 全部和既有正式记录一致。代码 bundle、原集合、新完整集合、合同与未来具体输入的身份明确区分。

Git 只新增约定三个文档，所有工具目录未变，git show --check通过，工作区干净。最终机器证据见同名 -verification.json。

冻结文件中的 pending 是形成时的历史状态；本报告构成 Leader 对精确三文件的接受记录，不回写/重冻原合同。

真实 metadata 的来源可用性、字节与格式兼容仍是实际获取前的条件。接下来先只读检查两个已有固定哈希的元数据文件；它们只作上游身份输入，不采用旧源码/清单/快照。若不匹配或冻结解析器不接受，停止，不改代码或重冻。元数据通过后才可单独调度新正文获取。

本次冻结不批准源码采用、构建、模型、CP2/CP3/Alpha；工具源码结论仍为 insufficient_evidence。
