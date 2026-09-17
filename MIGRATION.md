# 换机恢复

迁移范围：当前健身房小程序的指挥者规则、PM研究/基线/来源、dev完整历史/源码/测试证据及项目级 Agent 设置。账号凭证、运行库、Codex本机聊天数据库、微信登录状态和其他项目未纳入本次上传。已有远端内容保留。

## 1. 检出三个仓库与独立产品工作树

安装 Git、Python 3、Node 24.18.0 和微信开发者工具，并登录自己的 GitHub、Codex 和微信账号。在自选的一个空工作目录中执行：

```sh
git clone https://github.com/3956ray/Leader.git
git clone https://github.com/3956ray/ProductManager.git
git clone https://github.com/3956ray/Developer.git
git -C Developer worktree add -b gym-miniapp ../gym-miniapp origin/gym-miniapp
```

得到同级 `Leader/`、`ProductManager/`、`Developer/`、`gym-miniapp/`。最后一个目录是 Developer 仓库的独立分支工作树；源项目11个原提交均保留，D2原提交仍是 `ada2d60b96ab712a01e9e0cae9d7ccbcc91cc0b7`。不要在 Developer/main 开发产品。

## 2. 恢复角色与路径

在新电脑建立三个任务，工作目录分别为 Leader、ProductManager、gym-miniapp。将下列指令作为新任务的首条消息：

- Leader：「你是健身房小程序指挥者。读取 AGENTS.md、MIGRATION.md、projects/gym-miniapp/HANDOFF.md。先恢复路径/角色，接续D2验收，未验收前不派D3。」
- PM：「你是健身房小程序PM。读取 AGENTS.md、GYM-HANDOFF.md 和 product-knowledge-base/ideas/gym-occupancy。正式基线已冻结，等待指挥者单任务；不要重新启动全量调研。」
- dev：「你是健身房小程序开发者。读取 AGENTS.md、GYM-HANDOFF.md。D2原交付ada2d60已完成，等待Leader验收；不自动开始D3。」

拿到三个新的任务ID后，在 Leader 中执行（尖括号替换成真实ID）：

```sh
python3 scripts/restore_gym.py --leader-thread <Leader-ID> --pm-thread <PM-ID> --dev-thread <dev-ID>
python3 scripts/restore_gym.py --apply --leader-thread <Leader-ID> --pm-thread <PM-ID> --dev-thread <dev-ID>
```

第一次只检查，第二次只更新当前三仓路径与角色路由，并运行 leader_check。不会改正式文档、历史证据、启动自动调度或修改网络校验。可用 `git diff` 查看新机路径变更。历史报告/基线索引里的旧绝对路径保留原文；原文hash不应通过批量替换破坏。

## 3. 恢复配置与验证

- PM：已有 `.codex/config.toml`、`.agents/skills/`、知识库 `agents/` 保留。
- dev：Developer/main 的三个 `.codex/agents/*.toml` 与 `.codex/config.toml.disabled` 保留停用状态。产品工作树自带项目规则与本次使用的两个 skills；如需启用额外角色，应按新电脑的可用模型和配置格式核对后设置。
- Leader：以项目规则和三任务路由调度，不依赖全局代理配置。保留用户要求的中文、最小修改、必要验证后停止等规则。
- 模型名是原配置快照，不代表新账号一定可用；供应商API密钥、代理、权限信任和登录需在新电脑重新配置。
- `gym-miniapp` 中执行 `node scripts/check.mjs`。产品代码未因迁移改变；D2独立业务回归仍由新Leader执行 `node --test test/*.test.mjs`，记录新的证据。
- 合成演示库按源码 README / `doc/demo-scenarios.md` 重新初始化；不恢复旧票据/会话/数据库。初始化命令会创建本机密钥，勿提交 `.runtime/`。
- 微信工具导入 `gym-miniapp`，使用用户已有测试号访问权限。默认客户端后端未配置，合法域名校验开启。

## 当前下一步

D2交付待Leader独立验收；D3尚未开始。详见 [HANDOFF](projects/gym-miniapp/HANDOFF.md)。创建测试号已完成，但临时跳过组合网络校验仍未授权。此次GitHub备份不构成发布小程序、连接真实数据库或关闭校验的授权。

## 完整性与历史

本次新增资料清单见 `migration/files.sha256.json`，记录角色工作树、相对路径、字节数、SHA256；原正式需求另有source hashes，历史测试另有各阶段manifest。旧UI截图与日志只证明当时已验收的层次。
源分支保留原Git历史；原manifest适用于它记录的提交，不将迁移新增的交接/规则文件冒充旧验收源码。GitHub仓库不自动恢复旧Codex任务的聊天或运行状态，使用这里的规则、正式文档和交接摘要继续。
