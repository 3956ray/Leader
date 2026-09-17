# v5 下一次有限源码获取：待用户授权

状态：等待 Product Lead 明确批准；此文件不是已获授权记录。

v5 工具及独立冻结已由 Leader 验收。拟执行一个新任务 CP2-ASR-NARROW-SOURCE-ACQUISITION-V5-001：从全新空隔离目录，使用本冻结，对固定上游版本进行一次有界静态源码获取。上限仍为96个文件、1,048,576字节，原9个精确seed和所有停止条件不变。不会构建、运行或集成第三方代码；不会恢复旧run。遇到不支持的C++形式、越界、拒绝项或证据缺失即停止，不临场修复后续跑。

绑定的已验收冻结提交：b0193cf1e818f76a4e429c4d0aeeb81d29a16cbc。
冻结目录tree：1c7f74e87bfb20c75d2a4b1b75445a0a92916d1c。
freeze.json SHA256：21aaee7a39eb0ee9668c0e10f3ad51ee6068356c9924b57597c122bbf521541e。
MANIFEST.json SHA256：107b27e5d671973d3c4ca386e7acb311128ee33e6b2fba3175a3db93ff864356。
完整版本集合SHA256：d47ef78b6c452533377fa97d97bb245f83597f5028154a47a589c6e9ee24b678。

## 正式决定中的授权范围

我批准在 `CP2-ASR-LICENSE-TEXT-ROUTING-REPAIR-001` 通过 Leader 独立验收并形成不可修改的新冻结后，另开一次全新任务，以设计合同提交 `a57f643bac24edef5d6601b8a59baa77060f3d2c`、设计 tree `31376c73f43caf3bbfd664d8316ffecdc589379d`、28 项输入摘要 `c318c5a5f91d4af1d2759895ab9d5296c5784eaa214548b92f25fba4096764d2`，针对 sherpa-onnx commit `917bed95c8e5c7c18aa4d69fea42e9ef8ef0a60e`、tree `fd2c4e97c9f7499b6ed91c7c2854b4211f61bdc0`，按原 9 个精确 seed、仅限 `LICENSE` 与 `sherpa-onnx/csrc/` 普通 `.h`／`.cc` blob、96 文件／1,048,576 字节、既有 denylist、请求前授权与全部停止条件，从空的隔离目录执行一次有限静态正文获取。不得复用旧 corpus 或已停止 run，不得扩展解析语义、建立可采用快照、构建、执行、安装、加载、推理、集成、宣称 CP2 通过或进入 CP3。

## 为何需要本次确认

正式产品决定 doc/cp2-license-text-routing-decision-2026-09-06.md 明确：**“任何新冻结后的真实正文获取必须取得新的 Product Lead 明确授权。”** 前一次真实获取已终止。离线修复和冻结已全部完成验收，本次确认仅针对新的真实获取。

收到明确批准后，Leader 记录用户原文、复核新冻结和固定输入映射、通过调度检查，再单独下发上述新任务。此请求不意味着CP2通过，也不批准CP3或父亲Alpha。
