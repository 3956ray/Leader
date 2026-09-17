# V2-CALENDAR-IMPORT-001 independent review

Verdict: ACCEPTED for CP4 emulator engineering scope. Xiaomi15/private-provider/family validation remains unverified. No full-App or whole-Checkpoint-family completion claim.

Final commit84f3691f97efaae6e9fdbb7c81405e6525770e38; implementation38d9c9ea47424ed26a43ffbeecf1797ed774debd; baselinec22345b1ef18335e11df15f4595879464a385f5b. Clean codex/v2-calendar-import. Attempt9b7b85da-ae29-4198-9f6e-a7e2df71784d, contract6428f6f45b8af2686011caa3813378ffbbe6ca56dd51e471da31eb1340b17223.

## Evidence and boundaries

- D1: Product READ_CALENDAR only, no source writes/INTERNET. User source/range selection precedes event access. Dedicated synthetic fixture is separate test APK/UID and may write only its own synthetic calendar. Actual cancellation, system denial/revocation source/local snapshots compared unchanged; manual text remains usable.
- D2: Chinese/multiline/title-only, all-day and separate end timezone, repeating master beginning before range, moved/cancelled exceptions preserved. Source payload/version and original readable text persisted separately. Final source-before/after JSON pairs independently equal, including controlled-edit baseline pair.
- D3: Actual Compose select/category/preview/confirm tests; no imported local reminders. Preview counters reflect new/same/changed/skipped and unconverted source recurrence/reminder metadata. Source snapshot viewer accessible from imported note.
- D4: Mapping uses source identity and SHA256 content versions; explicit changed-source copy protects old notes/drafts/mappings. Existing edits and trashed note restoration verified. Same batch/reopen idempotence, stale source/deletion/local changes, SQL failure rollback. Root found final-read cancellation race, developer added post-read cancellation+permission checks and deterministic rollback test; independently rerun.
- D5: Final128KiB-guard APK passed3actual Android calendar tests (20s,12.461s,8.363s).900000-byte synthetic description rejected without writes;90000-byte description imported/read after database reopen, exact original/body/mapping and repeated preview. Earlier cancellation-guard APK8existing regressions passed (including realAlarmManager and2backup tests); later change only calendar row-size guard, final host/build/lint and3calendar tests rerun. Manual force-stop/relaunch/permission evidence is earlier version; scope/version limits explicit, not a claim all tests ran on finalAPK.
- D6: Xiaomi15/source-provider differences and private source selection deferred per user. Family and natural reminder cycles not passed.

Root independently reran99host tests with --rerun-tasks:0failures/errors/skips,28s. Build/lint developer evidence passed,19warnings/0errors; calendar context warning retains applicationContext only.59evidence manifest entries verified.3archivedAPK hashes independently match result; final product325d96965a977bff7aaaf3a51f1f960b04bc5674a0154f2f6567cad39745fcd2, test5377d8ebeb49656ead0648df880a7caf2de9d07c2b6105de21290fcb4ee516e8. No new dependency, no voice/candidate runtime modification. Test helper failures are retained and excluded from success evidence.

## Explicit remaining limits

No atomic lock across Android source provider and local SQLite; last-read/commit source race documented. Account/calendar reconstruction/ID reuse cannot guarantee continuity, user acknowledgment required. Limits128KiB/event,4MiB/batch,300events,5000instances,366days and local10000rows/table/32MiB text; fail closed without truncation. Current backup excludes calendar provenance/mapping; laterCP8 compatibility required. Voice001/002 remain partial; controls,AI,relations,UI refinement and final device/family work remain.

Next: approvedE7 CP5 AI suggestions, one new contract from this clean baseline. No real provider credentials/consent inferred. Existing approved product plan authorizes this sequence; no repeat PM decision required.
