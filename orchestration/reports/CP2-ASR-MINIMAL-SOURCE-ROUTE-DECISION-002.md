# CP2-ASR-MINIMAL-SOURCE-ROUTE-DECISION-002 验收报告

- RESULT：`REVISE`
- 结论：`ACCEPTED`

## 正式决定

- 保留“可复现最小源码快照 → arm64-v8a、CPU-only、ASR-only 运行时”的方向，但撤销“下一任务直接冻结最终 allowlist”的失败流程。
- 修订为两个互不继承裁决的阶段：阶段 A 只建立有界静态闭包发现材料；阶段 B 以后另行授权，在全新隔离目录重新获取并验证最终闭合快照。
- 阶段 A 必须在正文前冻结 seed、允许根/类型、确定性 include 规则，以及 256 文件、2,097,152 字节的硬上限；只有 `offline-tts-frontend.h` 可作接口级发现例外，不允许取得任何 TTS 实现或继续跟随 TTS 依赖。
- 发现材料不是最终快照或构建输入；CMake/源码/脚本不得执行，外部依赖/模型不得获取，产品源码不得修改，CP2 未通过且 CP3 未批准。
- Product Lead 对已结束任务的授权已经耗尽；任何新的逐文件正文获取必须对 `CP2-ASR-STATIC-CLOSURE-DISCOVERY-GATE-002` 重新明确授权。

## 独立核验证据

- 正式决定：`/Users/orderly_ray/Documents/Products Manager/product-knowledge-base/ideas/personal-thought-archive/cp2-minimal-source-route-revision-decision-2026-09-05.md`
- 决定 SHA-256：`1982303adbce8d47a1b5af7b4b3855a928f14e4e9209135523abeabeb7ae0ea4`
- 更新 PRD SHA-256：`4a6ac008ae460ab491a66758aa4113c15a274bd7e724ef906df7223f878aeec0`
- INDEX SHA-256：`ff90e9abf692478e017b555e5bd416a8d2129bae7af09805b1415cf36572dfd4`
- LOG SHA-256：`6641369138dc0ed5eaf34e765e35dfea98d4192f8b1531335c939a883cebb60e`
- 决定中引用的首次门禁六份证据与 Leader 验收报告哈希均由 Leader 重新计算并逐项一致。

## 未验证与工作区说明

- 有界发现能否在上限内收敛、TTS 接口能否解耦、JNI/Kotlin 与外部依赖边界均未验证。
- 产品知识库存在此前已有的大量未提交修改；本次正式决定、PRD、INDEX、LOG 通过路径与哈希验收，但未提交。
- 决定与 PRD 尚未同步到产品仓库；在同步验收和 Product Lead 新授权前不得下发发现任务。
