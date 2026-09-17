# V2-NOTES-ACCESSIBILITY-001 review

Verdict: accept scoped emulator UI engineering at 8a98e09d1276a17016a4e71f7f7385f6c57e402c. This does not accept actual TalkBack service navigation, CP3 as a whole, Xiaomi or family delivery.

## Evidence and scope
- Exact task/attempt/contract receipt registered. Developer turn completed and idle. Clean worktree observed at final commit; baseline29482c49. Product source diff limited to NotesScreen, LifecycleScreen, RelationsScreen and AccessibleButton. No repository/model/schema/permission/dependency changes.
- Read layout/semantics diff and retained same-ID callbacks, confirmation and enabled guards. Actual focus state is observed rather than fabricated. Header/scroll clipping and adaptive button sizing address recorded defects; related-note spoken labels use actual context instead of UUID.
- Independently reran host unit tests on final checkout:127 tests,0 failures/errors/skips; successful build. Evidence in independent-host.json.
- Verified all372 manifest files and four archived APK SHA256 values. Manifest hash030b683d49fe276dd52a66c55d8152b20b4a11231f76426a603fe7d1ff928189. Build and final test-build logs successful; lint0 errors18warnings remains disclosed.
- Six font/theme raw instrumentation logs report OK; result files contain66 button checks, minimum heights56dp and widths above56dp. Actual route tests include durable editing, rotation/back, same-title stableID, categories, relation and trash restore. Keyboard evidence checks real focus and dialog cancellation return separately.
- Leader directly inspected before/after and normalIME rendered evidence during review. Initially insufficient scroll screenshot was returned for correction. Corrected2.0/320dp screenshot shows appended end text and caret above keyboard: fieldbottom899,IMEtop983; actual touch selection287/287 then297/297 and exact persisted draft. ScrollBy automation is not physical keyboard/swipe proof.
- Read raw20 existing regression logs and2 realVosk UI logs. Final NotesUiTest also passed. Product APK44668032a613b6426b4f02eef02d4e76e294bedbdc657a3a5e3bfda6576ae1b3 shared across test cohorts; final test13305d5c61547b656235c0b382b9bfa2248f384972cd4b68bb03249e005a4f2f. Cohort ZIP comparisons differ only classes4.dex; report retains exact cohorts, not a claim all tests used final testAPK. Source changes to regression tests adapt scrolling/testtags; assertions retained. No claim of byte-reproducible builds.

## Unverified / remaining
Actual TalkBack service binding and greenfocus were observed, but bounded navigation failed; no actual service navigation/dialog speech-focus pass. Contract explicitly requires separate reporting of outcome and bounded attempt, so scoped acceptance does not waive this gap. Xiaomi15, family, natural reminders, generalASR quality and realAI provider remain incomplete; Voice002 stays parked partial with embeddingPAUSE. These prevent whole-app completion. No new checkpoint dispatched by this review.
