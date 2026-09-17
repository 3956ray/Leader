# v3 进行中复核：合规正文可生成无法读取的终态

状态：CONFIRMED，当前候选不得标记为可验收；这是当前开发任务内的证据恢复缺陷。

独立目录：/private/tmp/think-leader-acquisition-v3-wl77oio5

复现结果：leader-large-edge-result.json；事件与终态：evidence/leader-large-edge/。全部输入为 Leader 自建，真实网络事件与陷阱触发均为零。

构造：默认九个 seed 均为项目自建注释；第二个 seed 内容为 `#include "leaf.h"` 加换行重复 12,000 次，随后 `#if 0`、`#endif`；已知 leaf 是自建空注释。总正文仅 216,171 字节，低于 1 MiB。通过生产候选 run_input 和自建 FakeFactory 执行，没有真实网络。

结果：两次调用后正确以 edge_conditional 停止，记录 12,002 条边；terminal.json 大小 2,188,808 字节。但 inspect_run 调用 read_regular 的默认 2,000,000 字节上限，抛出 Rejected: unsafe_evidence_file。写入方允许的终态不能由已交付读取方恢复。相关事件快照也携带整个边列表，存在同样问题。

要求：在当前 v3 范围内修复写入/读取和证据预算的一致性，仍保持资源有界。可以选取有证明的记录预算或分段设计，但不得静默丢边、无界扩大读取、放宽原 96 文件/1 MiB 或改变源码获取范围。超过工具证据容量时必须在后续请求前停止，并留下可以独立重算/恢复的明确终态与最后检查点。新增本例及边界测试；重新完成受影响回归与最终确定性双跑。

现有 95 项基础测试在 Leader 独立首跑中通过，但未覆盖本缺陷。基础通过不替代该失败证据。
