# V2-EXPLICIT-RELATIONS-001 — ACCEPTED engineering

Final53fb5da83c841d565f8c2f627de4d81905a1abf6 on codex/v2-explicit-relations, clean; baseline186204ee45b2f2664fd8073e53a63fe118e0df04. Contract981a5e0733148b37aee52d293ea3f2ae614b7c23f0c1f605560b14bed4fcb701; attempt3653a2dd-eb41-4831-9a4e-38734870da34.

## Review evidence
- R1/R4: reviewed repository constraints, normalized pair, manual source, active endpoint trigger, stable edge ID, transactional create/remove/migration, live note/draft join, hidden recycled endpoints. Independent tests cover symmetric links, duplicates, self/missing/trash, both-endpoint restore, stale edge removal, literal search and migration failure rollback preserving prior data.
- R2/R3: reviewed editor draft persistence and exact-ID navigation, confirmations, bounded50-row list, same-node accessibility action/identity. Optional graph absent as allowed; no fake entry.
- R5: independently verified all40 archive manifest entries and3 APK hashes; raw logs confirm3 final relation Android tests and13 earlier regression tests. Inspected Android test assertions and screenshot at1.5font. Checked actual1000notes/5000edges/source999 persisted dataset and exact ordered first/second page endpoints against DB; restart snapshots identical across all9 tables.
- Independent full host rerun:115tests,0failures/errors/skips; BUILD SUCCESSFUL, --rerun-tasks. Evidence in independent-host.json; no concurrent developer Gradle. Standard build/lint developer logs verified in manifest,0errors19warnings.
- Source scope and clean Git verified; no new dependency/permission. Current backup relation exclusion explicitly disclosed.

## Version and interpretation limits
13 Android regressions and force-stop snapshots used pre-message-regressions.apk02dec1fb03ad17d92e762989bb8f2625a4c22d2d7e41ccb7f60fc61edd6253d3. Final APKc777c739b8f1e78d642d440a61cad32a0e86c161fc638c1401a7e483f9aa1986 differs only in classes10.dex ZIP entry; DEX strings differ in relation failure message and compiler metadata, consistent with reported wording-only change. Final3 relation tests rerun; don't relabel earlier13 as finalAPK runs.

Reported SQL10sample upper-middle statistic1391us, max2939us; UI single285ms, neither cold-start nor UI P95. Large-font platform accessibility focus/click verified, actual TalkBack speech untested and keyboard input focus false. Full UUIDs occupy visible/list spoken identity; family-facing presentation remains in later UI refinement, without altering stable-ID storage/navigation.

This accepts E8/CP3 engineering only. Full CP8 relation/source backup, actual TalkBack/Xiaomi15/family, real AI provider and voice quality/controls remain unresolved. No full-App completion. Next approved E9 is full-feature backup compatibility.
