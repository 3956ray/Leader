# V2-NOTES-LIFECYCLE-001 engineering acceptance

Decision: ACCEPTED for the bounded CP3 category/lifecycle implementation. Full-app, physical-device and family validation remain incomplete.

Accepted HEAD: `e363ea92615c8b0594388e9a9992e0782ab545aa`; baseline: `e2f6f4a2e91ec367dea034dff263368341212fe6`.

## Independent evidence

- Read production schema migration, category ID/provenance handling, reference updates, revision protection, soft delete/restore, ViewModel and new UI code.
- Reviewed the 11 new lifecycle tests and extended ViewModel/Android tests. They cover exact legacy fields and draft-only category migration, rollback of schema/version and rows, differing formal/draft categories, stale edits, preserving draft contents through trash and fallback to unclassified on restore.
- Independently reran `:app:testDebugUnitTest --offline --rerun-tasks` using the reviewed local toolchain. All 33 tests passed: 14 original repository/rule tests, 11 lifecycle tests, 7 ViewModel tests and 1 template test. Log: `/private/tmp/thinkv2-leader-lifecycle-tests.log`.
- Verified tested source/config digests match final submitted files, final HEAD and clean worktree, baseline diff check, and 89 file/report/APK digest entries. Adjacent verification JSON contains the recorded results.
- Read actual `OK (4 tests)` Android instrumentation log and tests, in-place S1 APK-to-S2 APK migration and force-stop/reopen evidence. These are synthetic emulator checks, not Xiaomi/family evidence.
- Viewed home, category management, soft-delete confirmation and recycle-bin screenshots. Key actions and recovery explanation are visible. Full manual TalkBack and other screen/API combinations remain unverified.

## Scope disposition

Stable categories, create/rename/reassign/delete-category semantics, non-destructive v1-to-v2 migration, recoverable note deletion and same-ID restore meet PM A5/A6 engineering criteria. No permanent note-delete API or automatic trash purge is present. Existing core persistence tests remain active, with fault injection adapted to the production UPDATE path rather than removed.

No runtime dependency, Gradle, manifest or private-backup boundary expansion is part of this task. The report records no real-device/private-data access. Host search timing is not a device guarantee, and complete category/trash lists are not an unlimited-scale claim.

Remaining: Xiaomi/physical-device checks, manual accessibility, father trial, broader Android/screens, prolonged background behavior and real device disk-full. Later reminder, backup, ASR, migration and other approved full-app requirements are not completed by this acceptance.

Next: V2-REMINDERS-001, one CP7 task implementing PM B1-B10 against this accepted lifecycle baseline.
