# V2-BACKUP-RESTORE-001 acceptance

Decision: ACCEPTED for CP8 current-feature engineering at cc957d56e8f5337d6548ed2b0296712fc0cbdcba. Full app and physical/family acceptance remain incomplete.

- C1/C4: actual Downloads SAF exports with default and edited names; plaintext/cloud-provider guidance; cancel and synthetic ENOSPC through real picker verified. Failed attempts retained and excluded. Cleanup uncertainty is reported honestly.
- C2/C3/C5: strict bounded JSON, exact payload length/hash and full source-field equality independently checked; malformed input rejection and limits covered by reviewed tests.
- C6/C7/C8/C9: read-only previews, single-transaction merge, unchanged originals, new-ID note/draft/reminder mapping, disabled imported reminders, receipts and duplicate no-op verified in host and actual Android evidence.
- C10: independent 79 host tests passed, 63 tested inputs unchanged at final HEAD; final Android logs report 8 passed (one template test included). Real SQLite/SAF byte and snapshot verification passed. Lint 0 errors/14 warnings. No new dependencies. Clean Git workspace and diff check.
- Result SHA256 bbf83cf6d8694706aa3fd96c07616c2c6635b828f614cb79c57937c2db500d70; all 340 referenced file hash/size entries match.
- APK SHA256 d718a08ce4531368988cbc7ae4bcdf7fc5fae94eb471682ed165e80a355cb554.

Evidence: final-verification.json, final-independent-tests.json, export-bytes-review.json, restore-review.json and initial-review.md in this report directory; product doc/backup-verification.md and doc/evidence/backup. Final tests exclude the interrupted emulator run; later rerun passed. Test-provider corrections do not alter product permission behavior.

Unverified: Xiaomi 15, household use, natural reminder days, physical full disk, other OEM/cloud providers and human TalkBack. Later voice/calendar/AI/relations and their backup compatibility remain separate required stages.
