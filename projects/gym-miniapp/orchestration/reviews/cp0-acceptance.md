# CP0 验收

Decision: ACCEPTED
Task: GYM-CP0-FOUNDATION-001
Commit: 0fdede77301c6c21d0e6fdd7cfe9865a937cb8d7
Date: 2026-09-16

## 逐项证据

- E01：独立Git根确认，38个文件只含本项目；工作区干净。原生两Tab骨架、启动/迁移命令、依赖来源与限制记录存在，无npm依赖或新增第三方下载。
- D01：Leader独立执行npm test，7/7通过，含实际HTTP健康、SIGTERM换PID重启、SIGKILL后相同磁盘探针、跨环境/门店隔离、缺配置/密钥失败关闭。最终提交代码与cp0-tested-files.json全部一致，无需重复相同测试。
- 迁移与事务：重复迁移不变、篡改拒绝、新DDL失败回滚、写事务回滚、多进程锁竞争及解锁后写入均有测试。
- 静态/基线：Leader执行npm run check通过；三份正式基线hash一致。只证明语法/JSON/文件引用，不证明微信编译。
- I01/F01/R01/R02/C01/C02/X01/Z01：已阅读逐动作接口、持久化结构、会话/限流/加密/删除/清理/时区设计，当前仅接受契约层；后续业务代码和测试尚未进行。
- 评审修订：operator精确memberRef核对可取得无Binding的revoked Registry版本；GET session包含accountRevision，逐动作版本来源含CLI角色inspect。修订不改变产品范围或提前开通业务。
- 文件边界：复核manifest各hash与文件一致，Git无.runtime/数据库/密钥，最终工作区干净；没有混入父级Projects或thinkV2。

Leader测试日志：cp0-leader-test.log；已测试源hash：cp0-tested-files.json；开发者证据：源码reports/cp0/。

## 限制与下一项

Node SQLite绑定稳定性及本机发行签名/全量CVE未全面验证，已固定版本并限定本地用途；后续部署前单独评审。本次没有真实数据、远程服务或新增依赖。AppID、微信工具编译、官方登录、真机、门店与发布均未验证。

准许下发唯一 CP1 身份与operator基础任务；不得提前实现忙闲、会员核验或课表业务。清理、删除等契约在对应CP实现后才可标业务通过。
