# CP2 第一方审查工具：Leader 独立复核

日期：2026-09-05。关联任务：CP2-ASR-NARROW-SOURCE-BOUNDARY-FEASIBILITY-GATE-001。

## 结论

现存第一方策略、解析器和控制器不满足原合同，不能启动获取。准备阶段结论为 blocked；源码边界结论仍未验证，不能把工具缺陷写成 sherpa-onnx 源码本身不可行。必须修订策略/解析语义，命中当前合同的停止条件，转交产品经理决定最小离线返工范围。

## 独立确认的阻塞证据

证据根：`/private/tmp/think-cp2-asr-narrow-source-boundary-20260905.693AnW`。仅阅读第一方文本，未执行工具，未读取第三方正文或枚举 corpus。

1. `trusted-tools/literal_include_parser.py:84` 把全部尖括号 include 直接判为 system_external；`:100` 把固定 tree 中不存在的引号目标也判为 system_external。`policy/source-boundary-review-policy.json:68` 与 `:73` 明确采用了这些规则。因此缺失的内部头或用尖括号引用的仓库内头可能被漏掉，不能满足原合同“未解析/宏/歧义/漏记内部边必须显式登记并停止”的要求。
2. `literal_include_parser.py:102` 对允许目录内路径先赋 internal，仅对 forbidden_scope 分支生成 denylistMatches。`source_boundary_controller.py:336` 仅在 forbidden_scope 集合中检查 denylist；内部路径要到后续弹出队列时（`:223`）才做路径检查。因此已发现某些禁止依赖后仍可能继续请求其他 seed/排在前面的文件，不满足发现即停止。正文正则不能完整补上该路径检查，例如 path token 命中而词边界正则不命中的名称。
3. `source_boundary_controller.py:371` 至 `:379` 只依据队列和 include fixed point 生成 source_boundary_feasible，没有检查 P0 符号映射是否齐全、人工扫描裁决或完整 denylist 可达性。即使外部人工流程未来会检查，该自动输出本身也可能提前表达错误结论。

上述结论由完整第一方文本静态复核得出，不依赖运行第三方代码或假设实际上游内容。

## 处置建议

请产品经理按停止规则正式裁定：允许独立、可逆、仅第一方的离线工具返工和合成输入验证；保留旧尝试及哈希证据，不改旧冻结文件、不下载或复用第三方内容。将工具开发、首次正式冻结、源码获取三者边界写清，避免把每次尚未执行的工具修复混同为扩展第三方授权。工具通过 Leader 验收后，未来任何实际源码获取仍须符合固定身份、9 seed、96 文件/1 MiB 和原隐私/Checkpoint 边界。

用户本轮已明确要求 Leader 继续调度、开始开发；这支持必要的可逆工程工作，但不被解释为放宽隐私约束、批准任何现有制品或跳过 CP2/CP3 门槛。若正式规则确需更改，由产品经理落地决定后再派发实现。

## 验证边界

本轮产品仓库 main，HEAD `4c128821f22ff8b61939976789e3df70746c6a51`，工作区干净；leader_check 通过。尚未执行修复或测试，没有新增依赖、模型、音频、产品源码或提交。CP2 未通过，CP3 未批准。
