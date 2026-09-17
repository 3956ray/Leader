# CP8 review plan — development ongoing, not acceptance

Developer reports schema8 / backupv2,122host and3newAndroid tests passed; final legacy/SAF/regressions still underway. No independent verification yet.

Review重点:
- Vocabulary prefs migration inside SQLite transaction: preserve existing data, no completed marker on rollback; oldprefs retained but never reread after successful migration, no deleted-word resurrection. Same snapshot/merge atomicity and200pair bound.
- Calendar provenance copied immutably, note identity remapped; multiple explicit conflict copies source_key/fingerprint must not cause later source import overwrite, duplicates or incorrect localChanged decisions.
- AI accepted provenance mapped to copied records; no credentials/config/temp results exported; current runtime disabled and consent invalidated after successful restore.
- Receipt export/restore: same exportId/differenthash rejection; existing restored receipts must not incorrectly suppress incompletely recovered data after conflict/skip paths. Self receipt collisions and stale preview must fail safely.
- Relations endpoints, category collisions and reused-edge IDs mapped without losing data; skipped conflict semantics clear.
- Old actualv1 reader rejects v2, new reader accurately accepts v1 with disclosed missing fields; no permissive unknown fields.
- Actual Android SAF success/cancel/failure, full-field empty/conflict/repeat recovery and exact rollback; distinguish fixture/unit/real UI.

Only current boundedCP8 task active. Await final immutable commit/APK/manifest before independent tests/acceptance.

## Latest developer progress (unverified)
Reported final productAPK1f246d3ded802097cab0250df0cd6e252335ff3d16b91148b25840e9be2cc4fc;123host/build34s/lint0errors18warnings. SixCP8 device cases plus finalAPK actualSAF success/cancel/ENOSPC/empty preview zero-write/roundtrip/idempotence/corruption/restart reported passed. Actual calendar post-restore same8+changed1, explicit newcopy adds1 with existing records unchanged. Receipt skip/hash-conflict and vocabulary migration rollback/new-process no-resurrection rawJSON reported available. Category+relationID collision Android evidence and20regressions still running; no acceptance.

Environment: ThinkV2Backup reuses prior dedicated syntheticAVD with older syntheticDownloads; product pm-clear per isolatedcase; only currentcp8-final files manipulated. SAF initial drawer animation misclick diagnostic retained; distinguish retry logs from successful final path. Verify file/APK identity and source mapping at final review.

## Final-test fixture inspection
Independently read AiDeviceTest diff: sole change narrows startsWith("INSERT INTO ai_acceptances") to startsWith("INSERT INTO ai_acceptances VALUES"); existing delayed-accept assertions unchanged. This avoids trapping migration INSERT SELECT and retains acceptance-write latch. Actual final rerun still pending. Product reported locked1f246d3ded802097cab0250df0cd6e252335ff3d16b91148b25840e9be2cc4fc; finaltest aa91a166914b0985ceb81b4ed16c148c5e4d71df7cfb925312b218491953edde. SevenCP8 and last2AI tests running; prior18regressions reported pass. No Gradle launched during developer device work. Await cleancommit/manifest and exact version mapping.
