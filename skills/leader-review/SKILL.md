---
name: leader-review
description: 本项目换机后的单任务调度与证据审查规则。
---

先读AGENTS.md、handoff/START-HERE.md、project/state/current-task和正式来源。沿用用户授权，从真实代码与文件状态出发。
每次只派一个Checkpoint任务；写明目标、范围、不做、验收、证据与停止条件。修改以最小必要为原则。
读取必要内容，验证合适测试及实际截图/设备证据；通过项和未验证项分开，不以mock或聊天摘要替代实测。
主机、模拟器、真实服务、真机、家庭是不同证据层。无完整证据不得称整体完成。
使用leader_loop.py记录状态，不直接改账本。迁移先核验路径和新任务路由，不自动向旧ID派单。
