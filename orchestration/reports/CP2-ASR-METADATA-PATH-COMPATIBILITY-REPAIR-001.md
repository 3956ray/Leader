# metadata 兼容修复独立验收

RESULT: ACCEPTED。结论：metadata_compat_candidate_ready_for_freeze。

只接受第一方兼容候选及两份固定身份 JSON 的纯解析兼容性；不批准真实正文获取、源码采用、构建、模型或 CP2/CP3。

## 固定候选与代码审查

- 提交：524c6484b1290cd2556ebf9a1031a4d00b273a86；父项：55d3c3303a3884c88240c2f14d9b855fd51ae88e。
- 目录：tools/asr_review_acquisition_v4/；Git tree：4e0002cacaa429b282889161b705946ae30d9414。
- 18 文件代码/schema/测试 bundle SHA-256：642d29885efb5df375564d0ebeec0875d4701e5dfc816934de329d3c2dda42d0。
- 原 manifest SHA-256：c214f48326c45433949be979d3e971328bae7fd219612bee5fb149404b1bc799；1023 条记录集合 SHA-256：db462eb6ee6493433a6f963d561e8bea9469bc4b9783882c10ac8315724daae3。
- 完整目录包含 1024 文件；Leader 逐文件核对 HEAD blob、SHA、大小、普通单链接及清单中的 0600/0644 属性。提交只新增 v4，旧 v2/v3/freeze tree 不变，工作区干净，git show --check 通过。

完整阅读新增名称测试、protocol 和 runner 差异；对继承模块和原 100 项测试按 provenance 与已验收 v3 逐字节核对。生产差异仅为 valid_metadata_name、TreeIndex 和 tree 解析的名称校验/返回表示。获取授权、路径解析、transport、decode、ledger、预算、denylist 和策略字节未变；策略 SHA-256 仍为 ee9d1ae7b4b17d2d895d3a6e0b62f73bfda7eb8a9cfae50e9d264f9ed23fc627。

metadata 层保留原始 Unicode 字符串、完整属性、顺序/索引、raw bytes 与集合摘要。Cc/Cs、绝对/drive/backslash/空/点/双点 segment 与原值重复被拒绝；NFC/NFD、ZWJ、百分号样式等惰性数据不解码或合并。实际严格路径授权仍独立执行，metadata 名称不作为文件系统路径。TreeIndex 沿用可信进程内接口边界，不宣称抵御恶意调用者或同 UID 写者。

## 独立合成复跑

仅复制 22 份必要第一方代码、测试、说明与自建 fixture 到独立临时目录，未复制开发者历史 run。先完成静态审查和候选身份固定，再执行：

- python3 -B verify.py leader-a
- python3 -B verify.py leader-b
- python3 -B recalculate.py leader-a leader-b

两次各 112 方法、634 方法/子场景记录全部通过，无跳过；覆盖原 100 项/293 记录及新增 12 项/341 记录。规范化 SHA-256 均为 3ffa05250d75b3c320624be778446fb20c28c9cd4a2357ebfe2bb7e49bd9d10d，与开发者相同。独立 recalculator 不导入候选模块，重算每轮 364 条 ledger、13 终态及请求、原始合成 metadata/body/overflow archive；每轮 495 份 JSON 字节一致。NetworkGuard 的实际网络事件与陷阱调用均为空。

新增自建 171 名称测试同时证明无损保留、原 check_entry 拒绝，以及完整请求 path/SHA/替身 trace 不变；csrc/.h 外形的特殊字符依赖仍在授权前停止。恶意/重复名称无授权事件，NFC/NFD 保留独立身份。

证据：同名前缀 `-git.json`、`-leader-evidence/`。完整独立运行目录记录在 git 报告的 copy_root，主要日志/规范化结果/重算报告已另存 Leader。

## 固定真实 metadata 纯解析

合成验收通过且 bundle 固定后，仅从已批准的两个精确路径经目录链/no-follow/普通单链接/有界读取，复制至新私有临时目录。commit 为 2336 字节，SHA e020549c1a78964acc8e400091ee54ba29f29ffd08e5b919a1bf06801dd68089；tree 为 2742250 字节，SHA 7643e529ba6588e5dbe425acb624569218596a6316a1be9bc7d55bacd105ccd2，均符合原 pin。

静态扫描单文件上限明确为 8 MiB，无跳过/不可读。manual_review、score 32、四项 medium 与先前人工复核 findings 完全一致，仍为时间戳/Git SHA 的数字子串命中，无新增项或 block；原扫描 verdict 不改写。仅支持批准的固定 JSON 解析用途。

在 NetworkGuard 下，仅调用 input_document、parse_input、parse_commit、parse_tree。三种解析均 PASS：8585 条完整记录、0 重复、旧字符规则不接受的 171 个名称全部无损保留，实际获取范围内此类名称数量为 0。独立 JSON 对照确认 document/records/属性/顺序/索引/raw bytes 全部不变；完整有序集合 SHA-256 为 ef9119025fab7c3e5613061ca3d83a91294ebdebb70baa5ca19218c074e58453。

该候选下派生 canonical input 为 2037 字节，SHA-256 baab9ddac779808ad8a1ac79e1c76937bc5875cba335148c7984aa54e41810a2；它只是固定候选的验证数据身份，不是获取派单。实际网络和正文请求均为 0，未调用 controller/run_input/transport/blob decode，未创建 allowlist。证据见 `-real-metadata.json`、`-metadata-location.json`、`-scan/`。

本次两份临时 raw JSON 在验证后已删除；原批准只读输入未动。未向 fixture、工具、产品仓库、Git 或知识库复制真实 JSON，未枚举/读取相邻旧 corpus。

## 限制与下一步

Leader 检查脚本曾因假设所有证据文件为 0644、以及假设新文件有 source_commit 而停止；改为核对清单声明属性与新文件身份后检查通过，未修改候选、未发生候选测试失败或真实解析后补代码。

源码授权范围、固定身份、9 seed、96 文件/1 MiB、denylist、隐私和三步路径保持。真实网络/TLS/HTTP互通、源码闭包/P0/许可/人工可达性、构建/制品/模型/实机/性能/90秒稳定性/飞行模式/动态音频隐私仍未验证。旧 block/manual_review 不变；CP1/Conformer Deferred, not removed；CP2 未通过，CP3/Alpha 未批准。

下一唯一任务仅在新文档目录冻结已验收 v4 完整身份与双层名称规则，不改任何代码或旧冻结。Leader 独立接受新冻结后，才可另行映射既有精确正文授权。
