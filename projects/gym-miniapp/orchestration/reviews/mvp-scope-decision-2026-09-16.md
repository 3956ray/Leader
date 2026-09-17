# MVP 范围决定

Decision: APPROVED for PRD and bounded development after PRD acceptance
Owner: 小程序指挥者
Last updated: 2026-09-16
Authority: 用户授权指挥者推进调研、判断 MVP、编写 PRD/Checkpoint 并交 dev 开发
Evidence: research-source-snapshot.json；PM 最终研究与证据卡；PM validation.json；wechat-login-source-check.md

## 采纳

单店原生微信小程序，公共场馆页与我的两个入口；馆方人工观察忙闲、前台核验会员关系、今日/本周课表及维护端为 P0。服务端持久化、身份与权限、撤销、数据过期、失败反馈和测试隔离为完整交付的一部分。

明确采纳对原首页设想的调整：首版使用大状态词表示人工忙闲，不展示没有可靠来源的预计人数大数字。保持来源、观察时间和不可用表达。自动人数及门禁接入延后，不以随机数、累计进门数或课程容量替代。

暂缓预约、支付、开门、定位围栏、推送、器械实时占用、训练日志、AI及社交。核心业务不因未知门禁 API 而停止开发。

源码目标选定 /Users/orderly_ray/Projects/gym-miniapp；首次建项再次核对目录及所有权。PM 研究中 target_repo=null 为早期快照，由本决定更新。

## 验收判断

研究文件和产物存在；覆盖任务要求的四类问题，11张证据卡和21条候选验收条目区分事实、推断、参数假设及真实验证。Leader已阅读研究及证据，检查本地引用存在，独立读取微信官方code2Session正文。研究完成足以支持产品设计；RQ90不是实际用户效果证明。

PM 未执行全库标准 lint，原因是脚本缺失；局部元数据、引用、编号和差异检查通过并留下记录。此限制不阻塞本文范围决定，不能宣称全库验证通过。研究未提交Git，变更清单明确，不混入其他项目源码。

## 后续合同

将 prd-draft.md、checkpoints-draft.md 与 research-draft-review-2026-09-16.md 整理成知识库正式 PRD、完整验收矩阵和串行 Checkpoint。明确会话/角色授予撤销、重新绑定与删除、参数、清理语义、时区和异常行为。每个 Checkpoint 保持单一可验收结果。

本决定批准范围，尚未宣告 PRD 定稿或任一开发 Checkpoint 通过。PM 正式文档经 Leader 复核后才能下发首项开发。

## 未通过的外部门槛

真实 AppID、域名证书/部署、iOS和Android实测、馆方合作、真实会员核验和真实课表仍无完成证据。工程、开发工具、真机、试点分别记账。公开发布需独立授权。
