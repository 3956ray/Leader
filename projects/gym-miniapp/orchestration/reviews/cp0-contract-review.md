# CP0 契约审阅

Status: 修订等待中，非最终验收
Task: GYM-CP0-FOUNDATION-001
Date: 2026-09-16

已读取配置、数据库迁移、HTTP健康检查、测试源及技术契约。基础代码范围限于CP0，测试覆盖实际子进程重启、迁移回滚、作用域隔离和锁竞争。开发者日志7项通过，Leader独立复验待最终输入稳定后进行。

## 已发送开发者的必要修订

1. 会员绑定/恢复要求Registry版本，但现有pairing lookup只在用户已有当前关联时返回它。解绑或删除后新账号仍可能对应现有revoked Registry；必须有受operator权限保护的精确引用核对/版本读取路径，不能假设不存在。
2. 删除需要account revision，但GET session只列sessionRevision。必须提供本人accountRevision，并明确两个版本各自用于什么动作。
3. 逐动作核对所有expectedRevision都有合法可获取的前置读取路径。这里只补齐CP0技术契约，不提前实现后续业务。

Git已由父级Projects解析改为本项目独立仓库，当前未提交变更均属本次开发者建项。最终提交仍需核对文件清单与敏感数据排除。
