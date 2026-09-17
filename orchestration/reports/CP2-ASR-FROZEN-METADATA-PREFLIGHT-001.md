# CP2 冻结元数据预检

RESULT: BLOCKED。预检按停止条件结束；冻结工具无法接受已固定的真实 tree 元数据，未开始任何源码正文请求。此结果不表示上游源码不可行，也不推翻既有合成测试结果。

## 身份与读取边界

产品 HEAD 为 e2d64f98aae52bd5e015962191a3bf2c121beeb2，工作区干净。已验收代码 e4cd300ca50be776b7077f1d7fae783642a696a7 和冻结文档均未修改。

仅从既有第一方身份报告定位并读取 `/private/tmp/think-cp2-minimal-source-g78VnT/commit.json` 与 `tree.json`，经目录链和文件 no-follow、普通单链接、有界读取检查，复制到全新私有目录 `/private/tmp/think-frozen-metadata-preflight-_6wsajyf/`。未枚举或读取旧 corpus、snapshot、候选正文。

| 输入 | 字节 | SHA-256 |
| --- | ---: | --- |
| commit.json | 2336 | e020549c1a78964acc8e400091ee54ba29f29ffd08e5b919a1bf06801dd68089 |
| tree.json | 2742250 | 7643e529ba6588e5dbe425acb624569218596a6316a1be9bc7d55bacd105ccd2 |

二者均与冻结 pin 完全一致。详细证据为同目录 `CP2-ASR-FROZEN-METADATA-PREFLIGHT-001-inputs.json`。

## 静态扫描

已按产品第三方门禁与 scan-untrusted-code skill 执行静态扫描，将单文件扫描上限明确设为冻结 metadata 上限 8 MiB，避免默认 2 MiB 跳过 tree。扫描两份文本，未跳过或无法读取文件；原始 verdict 为 manual_review，score 32，四项 medium，无 high/critical。原始报告保留于 `CP2-ASR-FROZEN-METADATA-PREFLIGHT-001-scan/`。

人工上下文复核：commit 第 32 行为签名验证 payload 中时间戳 1788238085；tree 第 13813、18907、57834 行为 Git SHA 中的数字子串。四项均是端口数字模式命中，不是网络地址或可执行动作。该复核仅支持固定身份 JSON 的静态解析，原始扫描 verdict 不改写，不形成运行时、源码或其他制品采用批准。

## 冻结解析结果

启用 NetworkGuard 后只调用已冻结的纯解析函数。canonical input 与 commit 解析通过，tree 在 `Rejected("tree_path_or_duplicate")` 停止。完整 tree 有 8585 条记录、零重复路径，其中 171 个名称不满足解析器的受限字符规则；首个为第 2525 项 `flutter-examples/hello_world/ios/Runner/Assets.xcassets/AppIcon.appiconset/Icon-App-1024x1024@1x.png`。171 项均不在允许获取的 LICENSE 或 csrc 普通 .h/.cc 范围内。

根因是第一方解析器将实际获取路径的受限字符规则施加于整个递归目录的惰性元数据名称。不能通过过滤条目、重写原始 JSON、换 pin 或原地修改冻结工具绕过。

NetworkGuard 记录实际网络事件与陷阱调用均为空；正文请求为零，未调用 run_input 或 transport。证据见 `CP2-ASR-FROZEN-METADATA-PREFLIGHT-001-parser.json` 与 `CP2-ASR-FROZEN-METADATA-PREFLIGHT-001-path-summary.json`。

## 验收与下一步

本预检的身份、扫描、可复现停止点、零正文请求及修改边界证据完整，接受其停止报告；工具与真实元数据兼容性未通过，真实获取不得下发。所有真实传输、源码闭包、构建、模型、实机与音频隐私动态检查仍未验证；CP2 未通过，CP3/Alpha 未批准。

升级产品经理裁定最小离线第一方修复范围：保留旧 release/freeze 不变，在独立候选中区分惰性元数据名称和实际正文获取授权，保持完整身份、重复/穿越防护与原有获取边界；自建合成回归后另行允许只读真实元数据兼容验证，再经独立验收与单独新冻结。既有精确正文授权与所有限额不变，不需要重复申请相同用户授权。
