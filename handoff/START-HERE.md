# 换机交接入口 · 2026-09-17

## 1. 恢复三个工作区

使用自己的 GitHub 登录克隆 Leader、ProductManager、Developer。安装 Git、Python3；Android构建环境按Developer说明安装。不要把旧电脑的auth.json、Keychain、API密钥或全局Codex数据库放进Git。

在Codex分别打开三个仓库并建立Leader、PM、dev任务。Git仓库不会恢复旧任务运行态，旧codex://链接仅供追溯；新任务的实际ID需要重新登记。三个任务各自先读仓库AGENTS.md和交接入口。

## 2. 先核验，不自动开工

在Leader运行 `python3 scripts/handoff_check.py`。它验证文件校验清单、冻结合同、账本/视图一致和正式来源快照。它不证明产品功能通过。

当前唯一产品任务V2-REMINDERS-USABILITY-001停在review；用户换机要求优先，本机未派下一开发单。读取该单receipt、review-plan、independent-host和Developer交付：
- attempt `8da8a67a-0259-4df6-9ae1-924d7c3fad37`
- contract `f691b2393ed29bec186ea9d2ee7579807e629a6a78ba575873b18e29948377cf`
- baseline `8a98e09d1276a17016a4e71f7f7385f6c57e402c`
- final `88d38616c5a5947d4ca798d4039c6368fa465624`
- 产品APK `23753ee0a9ad763aabad807d3fb1b1055cc55baa883eb29e3771932e671965cc`
- 六组/7回归testAPK `78f194f5b7d4c867a194a1ed1f329e01f3b35f32aba601a175ff083746ab7fa6`
- 普通IME testAPK `776599dbb576ba0b743a73e11ebb8d212ba47e3c338716b466f679dadb92562e`

Leader已经独立校验414个manifest文件、归档APK、主机127测试0失败；普通键盘截图已目视核对。最后尚须将审查证据收齐、形成正式review结论再通过状态工具接受/返工，不能把本说明当accepted。开发者报告六组42按钮/36输入检查、7Android回归；自然周期和实际TalkBack未过。旧原始归档 `/private/tmp/thinkv2-V2-REMINDERS-USABILITY-001-8da8a67a/` 的远端保存位置见Developer迁移回执。

## 3. 路径与任务重新绑定

原始账本/合同/证据中的绝对路径和任务ID保留为历史，不批量替换，否则会破坏合同SHA和证据引用。`path-map.json`把正式来源映射到本仓库逐字节快照；PM仓库为后续正式决策维护位置。

在完成现有review之前，不修改被冻结的contract_body或assigned_thread_id。新Leader可以读取历史执行者交付做review，不需要旧dev重新运行。跨机review输入应使用新机实际文件路径及核对后的SHA（先用当前review工具校验），保留旧执行身份作来源。

结束当前任务后，为下一单创建新合同，使用新dev任务ID及新产品本地路径；同步project.json的新路由与leader_root/target_repo/canonical_sources以及approved_sequence来源路径，保留旧映射记录。新任务必须经stage → send-intent →实际发送→sent→ACK。不要手改旧账本历史或绕过校验。原leader_check依赖旧绝对来源路径，在重绑前失败是预期，不要伪造路径存在；新路径调整后检查通过才派新单。

## 4. Agent 关系与偏好

历史Leader `01a0a5ce-3e8b-75e1-92be-9eb89ef9ed37`；PM `01a0768c-7ba7-7f11-bd4f-f5c2fd1fa779`；dev `01a0a5d3-8ec3-7071-82f6-a49f80ba7d1d`；最新父亲需求背景 `01a09ee2-641e-7af2-ab62-18399fa170ca`。它们不是跨设备可用的保证。

Leader默认不改产品源码，仅派发一个可验收单项、审查真实代码/截图/测试、接受或返工。PM只有正式文档落地的APPROVED/REVISE/PAUSE构成产品决策；dev完成单项就停。用户不希望重复请求已有授权，禁止闲置时反复派准备/研究任务。

本机配置可读偏好为model=gpt-6-astra、reasoning=medium、provider=team_relay；仅供历史参考，不能保证新电脑模型或服务可用。提供商登录/地址与密钥应由用户在新电脑单独配置，未导出。旧全局配置含never/danger-full-access，但本会话实际受sandbox/auto_review管控；不自动迁移宽权限。新电脑按其安全策略运行。

技能：优先karpathy-guidelines（最小改动、明确假设、适当验证）；新机若未安装可先遵循AGENTS.md和`skills/leader-review/SKILL.md`的等价项目规则。原第三方skill包未重新发布；插件/连接器要重新授权。不复制全局插件缓存。无自动续跑/定时任务需要恢复。

## 5. 保留完整目标与真实缺口

thinkV2由空白独立开发；用户顺序为模拟器工程先行，完整开发后由用户用小米15，再家庭验证。旧think数据与验收不继承。

文字/分类/回收站/提醒/备份/日历/AI建议/显式关系/最小语音命令已有分项工程证据；这不等于完整App交付。通用ASR质量未达标：Vosk专名47/66、可用10/30；隔离SenseVoice61/66、23/30仍失败且私人嵌入许可PAUSE，不启动另一路无界模型研究。真实AI provider=false。实际TalkBack导航、自然每日/每周提醒、小米15与父亲家庭操作未验证。禁止降低门槛、虚构结果、上传录音/私人数据。

下一步先结束当前review，再依批准基线排一个独立任务；不要因换机将目标标完成，不抢先请求用户真机测试替代未完成工程。

## 6. 三仓发布回执（2026-09-17）

- Leader 已推送；初次迁移提交 `a25ed2575c9d0cd8dedb3c3f526987e4910f9634`。
- PM 已推送到 `codex/thinkv2-pm-migration-20260917`，提交 `d590c574a09726eaa640c2719674f206d50c5d4e`；克隆后需检出此分支。[PM恢复入口](https://github.com/3956ray/ProductManager/blob/codex/thinkv2-pm-migration-20260917/product-knowledge-base/ideas/think-v2/migration-handoff-2026-09-17.md)。
- Developer 已完成公开迁移：交接分支 `codex/migrate-thinkv2-20260917` = `9ecfe708b32a749a3980fa00ea47d3e507e75daa`；源码分支 `codex/thinkv2-public-history` = `6cfd50f5eb6e2a8e6df0968886c9bec9b7d1ba14`。Leader独立核对远端分支一致。[开发恢复入口](https://github.com/3956ray/Developer/blob/codex/migrate-thinkv2-20260917/handoff/thinkV2/NEW_COMPUTER.md)；[公开证据包 Release](https://github.com/3956ray/Developer/releases/tag/thinkv2-migration-20260917)，1,172,246,269 bytes。Developer已匿名完整下载校验 SHA256 `f286e9712e5badbaca062398f3ed7c6301fecbfdcec77e236ace04627bce8706`。原审批阻塞已由用户在dev任务直接批准解决。
- 离开旧电脑前手动安全转移 `/Users/orderly_ray/Projects/thinkV2-migration-private-20260917/complete-original-transfer.tar.gz`（1,849,004,421 bytes）。此包仅私下/离线转移，不上传公开仓库；开发者报告 SHA256 为 `e45bfc25e368b1f823fa2477d03c9c2ac6a899b4bf1cd773b22ff5ac01abd5c9`，新机须重新核对。它包含完整原始历史和验收存档；仅克隆远端三个仓库不足以恢复受限原始资源，公开证据还需下载Release附件。

发布状态见 `publication-status.json`。迁移不改变提醒任务 AWAITING_REVIEW，也不表示完整App验收通过。
