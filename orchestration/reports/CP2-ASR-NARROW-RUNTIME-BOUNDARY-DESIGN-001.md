# CP2-ASR-NARROW-RUNTIME-BOUNDARY-DESIGN-001 审查报告

- RESULT：`COMPLETE`
- DESIGN VERDICT：`design_feasible`（待返工后验收）
- Leader 结论：`REVISE`
- 提交：`8eea68384efcb61cbea40a423b755edf3175f22d`

## 已通过的范围

- 提交父项精确为 `1812669faa90bfc899ac0ab0b01f17b39145ea37`，只新增约定设计目录的 7 个普通文档/JSON/Mermaid 文件，产品工作区干净，`git show --check` 通过。
- 22 个固定证据文件的 SHA-256 经 Leader 从提交 `0ded8eb...22fbb` 逐项重算，全部与 `context.md` 一致；证据目录 tree `1bdd940c85554147b904b033c59095f849d22a46` 无漂移，Leader 报告和五份正式文档哈希也一致。
- 人类可读提案完整区分 Observed／Inferred／Proposed，给出 P0 最小能力、加载所有权、模型/音频信任边界、PCM 生命周期、完整 denylist、两个真实选项、六类权衡、before/after 图、回退和九层未来验证计划。
- `design_feasible` 被准确限定为“形成可供未来源码审查的设计合同”，没有宣称源码可闭合、制品可构建、运行时安全、音频隐私或 CP2/CP3 通过。
- JSON 可解析，证据 ID 均已登记，选项/图路径存在，六类权衡齐全；所有相对链接可解析，未发现绝对本机路径、symlink、hardlink 异常、实现目录、产品源码或第三方正文。

## 必须返工的两项

1. `hardening.json` 登记了 `E01`–`E09`，但两个选项的 `evidenceCoverage` 未逐项覆盖全部相关证据：选项 1 缺 `E03/E04/E06/E08/E09`，选项 2 缺 `E04/E06`。人类可读提案已有完整九项 coverage；结构化 JSON 必须与其一致，并对每个选项/证据明确使用 `addresses`、`mitigates`、`unaffected` 或 `unknown`。
2. `context.md` 声称输入集合 SHA-256 由七条身份记录排序得到，但没有列出精确记录字节、字段分隔、排序键与终止换行；固定 tree listing SHA-256 的规范也未说明。第三方证据 tree 与 22 份文件哈希本身已复核通过，但派生集合哈希仍不可由新 reviewer 确定性重算。

## 返工边界

只允许修改 `context.md` 和 `hardening.json`：补全结构化 coverage，并把输入集合哈希改成有完整规范、明确记录内容、排序和 LF 规则且能独立重算的值。不得改动设计结论、人类可读提案、图或任何现有产品文件，不得读取 corpus、新正文、源码或进行技术执行。
