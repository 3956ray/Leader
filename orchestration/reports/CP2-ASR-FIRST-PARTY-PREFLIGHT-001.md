# 第一方准备审查

- RESULT：BLOCKED；准备结论：blocked。
- 任务：CP2-ASR-NARROW-SOURCE-BOUNDARY-FEASIBILITY-GATE-001；阶段：first_party_preflight_review_only。
- 审查完成；存在必须修改解析/控制语义的问题，已按原合同 stop_conditions 第 3、5 项停止续接，不修复、不重冻、不运行工具。
- 冻结完成状态：未证实。工具安全就绪：否，已确认阻断缺陷。两项判断独立；即使补足冻结证据，也不能消除下列代码问题。
- 本报告不判断第三方源码边界，不声称 CP2 或 CP3 通过。

## 范围与方法

完整逐行阅读现存 policy（154 行）、git_data_fetcher.py（116 行）、literal_include_parser.py（112 行）、source_boundary_controller.py（441 行）及 pre-body-empty-evidence.json（17 行）。行号来自 nl -ba，未截断。对照最终 current-task.json、此前已完整读取的两份精确授权归档，以及上一轮历史工具记录/核对报告。未导入、执行、测试任何被审工具；下列合成触发只用于文本推理，并非运行结果或上游事实。

合同引用均为 /Users/orderly_ray/Leader/orchestration/current-task.json 数组的一基序号：S=scope，A=acceptance，T=stop_conditions。授权归档为 /Users/orderly_ray/Leader/orchestration/reports/CP2-ASR-NARROW-SOURCE-BOUNDARY-FEASIBILITY-AUTHORIZATION-001.md 和同任务名的 orchestration/tasks/…json。

## 确定缺陷及条件性后果

### F1：内部、生成或未解析边会被直接当作外部边

证据：[policy:68](/private/tmp/think-cp2-asr-narrow-source-boundary-20260905.693AnW/policy/source-boundary-review-policy.json:68)、同文件 73 行；[parser:84](/private/tmp/think-cp2-asr-narrow-source-boundary-20260905.693AnW/trusted-tools/literal_include_parser.py:84)、100–106 行。合同 S6、A4、T1/T3。

任何角括号目标直接归 system_external，不查询固定 tree；任何归一化后不在 tree 的引号目标也直接归 system_external。若正文含仓库内部角括号头，或引号中的缺失/生成头，这些边不会触发 unresolved/generated 停止。相对路径只尝试一个位置，也没有证明该位置就是唯一解释。结果可漏记内部依赖并继续获取，fixed point 可失真。规则本身与合同存在差距，需改 policy/解析语义；固定上游是否含这些输入未验证。

### F2：字面量语法与 C/C++ 指令识别不足

证据：[parser:8](/private/tmp/think-cp2-asr-narrow-source-boundary-20260905.693AnW/trusted-tools/literal_include_parser.py:8)、9–10、65–76 行；[policy:66](/private/tmp/think-cp2-asr-narrow-source-boundary-20260905.693AnW/policy/source-boundary-review-policy.json:66)。合同 S6、A4、T3。

开/闭定界符未配对：合成行 `#include "x.h>` 会匹配，尽管合同要求非法字面量停止。只按物理行匹配且不处理注释/续行：`#/**/include "x.h"` 可被静默跳过，多行注释内以 #include 起始的行却可成为依赖。普通完整行的宏 include 会被拒绝，这是已有保护，但不能补足遗漏形式。条件编译指令也没有状态记录：条件内的 include 统一进入同一图，无法区分确定必需边与条件未知边；是否可接受保守超集从未明确证明，不能把该图当作真实必需闭包。需改解析语义。

### F3：发现允许目录内的 denylist 边后仍可能继续请求其他 seed

证据：[parser:102](/private/tmp/think-cp2-asr-narrow-source-boundary-20260905.693AnW/trusted-tools/literal_include_parser.py:102)–106；[controller:336](/private/tmp/think-cp2-asr-narrow-source-boundary-20260905.693AnW/trusted-tools/source_boundary_controller.py:336)–362、207–228；[policy:121](/private/tmp/think-cp2-asr-narrow-source-boundary-20260905.693AnW/policy/source-boundary-review-policy.json:121)。合同 T1/T5。

允许路径只标 internal，只有 forbidden_scope 分支附带 denylistMatches。控制器解析后只查 forbidden_edges 的 denylist；internal 目标入队，等目标出队才做路径 denylist。合成情形：某个非最后 seed 引用 tree 中存在的 `sherpa-onnx/csrc/wave-reader.h`，该路径命中 policy 的 `wav`，但 include 行不命中现有内容正则；程序会先继续处理剩余 seed，直到目标出队才停。虽会在该目标请求前拒绝它，仍违反“触达即停止任何后续获取”。需要控制/解析语义修改。

### F4：控制器可以在没有 P0 映射的情况下输出可行

证据：[controller:364](/private/tmp/think-cp2-asr-narrow-source-boundary-20260905.693AnW/trusted-tools/source_boundary_controller.py:364)–379；[policy:149](/private/tmp/think-cp2-asr-narrow-source-boundary-20260905.693AnW/policy/source-boundary-review-policy.json:149)。合同 A5/A7。

fixed_point 只依赖队列、missing_internal、parser_stops 与 outcome；整个控制器没有 P0 source map 输入或完整性条件，也没有逐项人工扫描裁决条件。只要这些队列检查通过就直接赋值 source_boundary_feasible，并写入报告/打印。后来人工审查不能追溯使这次提前输出满足合同。此项是可直接从控制流证明的结论门禁缺失，不代表本次曾输出该结论。

### F5：HTTP 重定向可以产生不对应 ledger 的额外正文请求

证据：[fetcher:17](/private/tmp/think-cp2-asr-narrow-source-boundary-20260905.693AnW/trusted-tools/git_data_fetcher.py:17)–24、27–32、46–54；[controller:245](/private/tmp/think-cp2-asr-narrow-source-boundary-20260905.693AnW/trusted-tools/source_boundary_controller.py:245)–264。合同 S3/S4、A2/A3、T5。

ledger 只授权初始 blob，重定向检查仅限制 HTTPS、主机和 `/git/` 前缀，未要求固定 `/blobs/{已授权SHA}`。若服务返回同仓库 `/git/blobs/另一个SHA` 的重定向，标准重定向处理将继续请求该正文；后置 SHA 校验只能在获取后发现不一致。不存在为该额外目标生成请求前授权的路径。是否实际发生重定向未知；允许该路径的实现缺陷确定。

### F6：网络响应无大小上限，校验发生在完整读入之后

证据：[fetcher:47](/private/tmp/think-cp2-asr-narrow-source-boundary-20260905.693AnW/trusted-tools/git_data_fetcher.py:47)–64；[controller:229](/private/tmp/think-cp2-asr-narrow-source-boundary-20260905.693AnW/trusted-tools/source_boundary_controller.py:229)–264。合同 S4/S5 与硬上限/身份失败停止要求。

请求前会按固定 tree.size 核对正文预算，但 response.read() 对原始 JSON 无界读取，再 decode/parse；API size 与 base64 解码后长度在此后才校验。若响应异常膨胀，先消耗无界内存，blob 路径还会在解码前保存整个原始响应。1 MiB 是授权解码正文上限，不应误称同样限制了 JSON/base64 开销；当前代码缺的是独立、合理的响应读取上限。未观察实际超限，不能把正常服务响应假定为资源边界保证。

### F7：带空白的 base64 内容会在身份正确时仍失败

证据：[fetcher:57](/private/tmp/think-cp2-asr-narrow-source-boundary-20260905.693AnW/trusted-tools/git_data_fetcher.py:57)–70；[controller:286](/private/tmp/think-cp2-asr-narrow-source-boundary-20260905.693AnW/trusted-tools/source_boundary_controller.py:286)–298。合同 S4、A3。

代码将 JSON content 原样交给 base64.b64decode(validate=True)，未处理换行空白。若接口的 content 字符串包含 LF 等非 base64 字母，严格校验会抛异常，即使去除格式换行后可还原正确 blob。后果是本可核验正文被记为获取/验证失败并停下；不会继续请求。严格解码失败条件可确定，当前固定接口响应是否采用这种格式未查看，也没有网络查证；因此不能宣称本次必然在首个 blob 失败。这是待解决的接口兼容准备风险，未运行实验。

### F8：异常中断未持久化完整的停止/闭包状态

证据：[controller:38](/private/tmp/think-cp2-asr-narrow-source-boundary-20260905.693AnW/trusted-tools/source_boundary_controller.py:38)–41、319–335、391–405、433–441；[fetcher:94](/private/tmp/think-cp2-asr-narrow-source-boundary-20260905.693AnW/trusted-tools/git_data_fetcher.py:94)–101。合同 evidence_required 第 2/3 项、A3/A4。

ledger 在请求前 fsync、manifest/request-results 分步持久化，是已有保护。但边/解析停止与 terminal 仅在循环结束写出；parse_source 异常或写最终报告失败会仅由外层打印 fatalControllerError，未保存结构化终态/队列/已解析边；KeyboardInterrupt 不在 Exception 捕获内。元数据哈希不符时也不持久化派生失败状态。故中断后能留下部分请求证据，却不能保证无需旧正文就可恢复闭包或确定停止位置。不能声称所有异常证据都丢失；硬终止本身也不可能保证最终报告。当前缺陷是已有可捕获失败缺少足够第一方检查点。

### F9：路径/链接保护不是完整的执行前不变量

证据：[controller:151](/private/tmp/think-cp2-asr-narrow-source-boundary-20260905.693AnW/trusted-tools/source_boundary_controller.py:151)–180、269–276；[fetcher:74](/private/tmp/think-cp2-asr-narrow-source-boundary-20260905.693AnW/trusted-tools/git_data_fetcher.py:74)–80；[controller:38](/private/tmp/think-cp2-asr-narrow-source-boundary-20260905.693AnW/trusted-tools/source_boundary_controller.py:38)。合同 S1/S5、A3。

corpus 在检查 islink 前就 listdir；若它被替换为符号链接，会先枚举目标。write_new_file 的 O_NOFOLLOW 只保护末级文件，metadata/derived 父目录没有逐级拒绝符号链接；ledger 的 open(...,'ab') 不采用排他/不跟随打开，且 FileIO.write 返回写入长度未检查，若短写发生会 fsync 后照常允许请求。body 最终 lstat 普通文件/单链接与路径 containment 检查有效，但不补足这些证据路径与写入完成保障。上轮所查目录和五文件没有链接异常；本项说明条件触发的代码缺口，不指控发生本地替换或短写。

## 未证明的准备条件

1. 固定常量、9 seed 与顺序：policy 7–30、54–63 与合同一致；controller 192–212 实现原 seed 顺序及 UTF-8 字节序后继队列。controller 127–140、229–242 在单个目标请求前检查允许根/类型/mode/tree size 和累计预算。所称 PASS 仅为文本对照。
2. 身份验证不完整闭合：controller 159–164/104–109 验证 tree 响应 SHA-256、tree SHA 和 truncated=false；但不消费 commit 响应或验证 commit→tree 绑定，不重算设计提交/tree/28 项摘要。fetcher.metadata_main 仅按调用者给定哈希验证。手工前置流程可以承担这些检查，因此不能仅因缺少自动化断言整个流程必然绕过；现存执行记录尚无完成证据，工具入口也不要求这些已验证凭据。
3. 哈希链：controller 44–87 的 canonical JSON、前哈希加 LF、SHA-256 与 policy 123–139 一致，245 行先追加授权才在 259 行发起初始请求。没有运行独立重算器；重定向、短写和异常边界分别见 F5/F9/F8。
4. blob 验证：fetcher 58–70 核对 API SHA/size/encoding、解码长度及 `blob {len}\0{content}` Git SHA-1；controller 265–268 计算 SHA-256、拒绝 NUL 并严格 UTF-8 解码，再写入和 lstat 检查。这些分支存在不等于已验证任何实际正文。SHA-256 是记录用摘要，没有独立期望值，不能宣传为额外的独立来源身份认证。
5. denylist 覆盖：policy 99–119 是有限词法正则，不能证明所有文件音频 I/O、动态路径或宽公共表面被覆盖；按行扫注释和字符串还可能把说明文字判作实际能力并停止。后续人工能力映射尚未进行，不能将“正则无发现”或“词命中”分别等同于安全或上游必需功能。F3 是无需覆盖推测也成立的即时停止缺陷。
6. 停止路径：已被分类识别的预算、类型、parserStops、forbidden_scope、内容 denylist 及捕获的 blob 异常均 break，没有显式 retry；这是有效保护。保护不能覆盖 F1/F2 未识别的停止条件或 F3 延迟识别。
7. 冻结证据：policy:5 的 frozenBeforeBody=true 是声明；pre-body-empty-evidence:4–16 是历史空目录记录。上轮五文件哈希与旧记录一致证明身份连续，已知 freeze manifest 未发现；没有独立完成记录证明三工具人工审查通过或被冻结为批准版本。controller 只验传入 policy 哈希，11–12 行先导入工具，没有绑定/验证三工具哈希。本轮没有创建或补签冻结文件。不可据此断言历史上完全没有冻结行为，也不可声称冻结完成。

## 验证、交付及下一步

- 已执行：在 /Users/orderly_ray/Leader 读取 cat orchestration/current-task.json，确认 first_party_preflight_review_only；在本次隔离根精确执行 nl -ba 对五个第一方文件全文逐行读取；未枚举任何目录。
- Git 核对：在 /Users/orderly_ray/Projects/think 执行 git rev-parse HEAD、git status --short --branch、git status --porcelain=v1 --untracked-files=all，成功；HEAD=4c128821f22ff8b61939976789e3df70746c6a51，main ahead 26，工作区干净。
- 未执行：被审工具、scanner、测试、网络或任何 corpus/API 正文访问；没有第三方实际触发结果、完整闭包、P0 映射、上游能力或模型/真机证据。合成例子均为静态控制流说明。
- 唯一新增文件：/private/tmp/think-cp2-first-party-preflight-20260905-01a071cf.md，用于 Leader 准备审查验收。原五文件、产品仓库及控制面均未修改；无 Git 提交/push。
- 建议：Leader 按必须变更策略/解析语义的停止条件验收 blocked，并决定正式后续路径；不能用“补齐冻结文件”使当前工具就绪，也不能自行修改后继续同一冻结尝试。原精确授权不因换人自动失效，但不覆盖绕过当前停止条件。此建议尚未执行；到此停止等待验收。
