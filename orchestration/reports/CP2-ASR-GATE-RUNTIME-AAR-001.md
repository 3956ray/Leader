# CP2-ASR-GATE-RUNTIME-AAR-001 验收报告

- TASK RESULT：`COMPLETE`
- TASK 结论：`ACCEPTED`
- ARTIFACT VERDICT：`manual_review`
- 提交：`7ab7784542801e4c3d37d0c6e244b31039255351`

## 验收证据

- 提交只新增 AAR 的 scanner Markdown/JSON 与人工报告；没有 AAR、应用、Gradle、Manifest、依赖、权限或源码进入 Git，产品仓库干净。
- Leader 独立复核隔离 AAR 大小 `49,113,869` bytes、SHA-256 `c4ef49e309f24fcee5c106b8a279481aaecaabb078cd37b2cd6e9a62cc8a73c8`，与官方 GitHub asset digest、报告和扫描目标一致。
- Scanner 重跑时明确把单文件上限提高到 64 MiB，最终 20 candidates、17 binary、0 skipped/unreadable，原始 verdict `low_indicators`；报告没有将其等同批准。
- 隔离静态审计记录 26 个 AAR entries、4 个 ABI、16 个 ELF `.so`，无 traversal/symlink/encryption；Manifest 只有 minSdk 21、无权限/组件。
- Java/native 静态面未确认联网/上传链，但确认 native 动态加载、`popen`、日志、临时文件、WaveWriter/音频写盘和远超 ASR 的广泛公共能力。
- 关键来源缺口成立：固定 tag 的公开 Android workflow 在产出 AAR 前失败，而资产后来由维护者上传；没有 attestation/SBOM/可复现 hash，无法证明 source-to-binary 对应。
- AAR 不含 LICENSE/NOTICE/third-party inventory；ONNX Runtime 和其他 native 组件的来源与许可证组合未闭合。
- `manual_review` 与证据一致：没有充分 block 恶意链，但不满足 `approved_with_controls`；报告只适用于精确 AAR，不继承到模型或集成。

## 后果与未验证

- 该 AAR 当前不得安装、加载、构建、测试或集成，需上游 provenance/许可证/SBOM 或合格 native reviewer 解决报告问题后重新裁决。
- 模型、最终 App、真机性能、稳定性、飞行模式和音频隐私仍未验证；CP2 未通过。
- 接受的是审查任务与 `manual_review` 结论，不是接受该 AAR。
