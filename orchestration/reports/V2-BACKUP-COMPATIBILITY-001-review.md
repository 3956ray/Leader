# V2-BACKUP-COMPATIBILITY-001 — ACCEPTED engineering

Final7eb5b4dafe891d10fe65a15c5f67b01c0d2ab3ae, clean codex/v2-backup-compatibility; baseline53fb5da83c841d565f8c2f627de4d81905a1abf6. Contract89c1bb14b1f3ef54516c2b1bed7f98a73e5c430bc71e4218c882bcae51845b2b, attempt85ebe7d3-3c42-4907-84c0-168c13c79c2a.

## Independent review
Reviewed strict v2 encoder/decoder and explicitv1 path, exact-field validation/limits/checksum, full snapshot/preview/merge and conflict maps, receipt semantics, transactional migration/restore, vocabulary ownership, AI reset hook and device/host assertions. Unknown version/meaningful fields fail closed. Source strings remain immutable, target IDs remap. Original records preserved, skipped dependencies remain skipped. Receipt means processed including explicit skipped rows, not complete restoration of every original row; UI and format disclose this.

Verified96archive manifest entries and all3APK hashes. Read raw logs confirming7CP8 +20existingAndroid tests. Independently reran all123host tests with --rerun-tasks:0failures/errors/skips, build success. No new dependency/permission; product Manifest binary identical to accepted baseline APK.

Actual SAF snapshot comparisons independently verified: export/cancel/ENOSPC leave DB unchanged; empty preview contains no rows; restored notes/drafts/categories/origins/calendar/AI/relations/vocabulary exactly match original; reminder configuration preserved but disabled and runtime scheduling cursor cleared; one exact exportID/hash receipt added. Restart/repeat/corrupt snapshots exactly equal restored snapshot. Validated actual exportedv2 payload length/hash and field counts:10notes,3drafts,1category,1reminder,1relation,2vocabulary,9calendar,2AI. Subsequent calendar action adds exactly1note+1source row, every prior row of all inspected tables remains unchanged.

Migration rollback/retry and new-process no-resurrection, category/edge collision maps, source-conflict copy and receipt-collision assertions reviewed. Five injected restore stages verify rows and relation-trigger SQL rollback together. Actual restore-button test checks stale preview rejection, AI disabled/consent cleared, vocabulary reloaded and credentials excluded. Legacyv1 fixture and frozen reader test reject newv2 on old reader and preserve new fields while reading old files.

## Version/evidence boundaries
ProductAPK1f246d3ded802097cab0250df0cd6e252335ff3d16b91148b25840e9be2cc4fc identical for all cited tests. Finaltest aa91a166914b0985ceb81b4ed16c148c5e4d71df7cfb925312b218491953edde covers7CP8+last2AI; earlier18regressions used3e0d722a8d74c6a5466072da81dce60e3095ae7a165cf12d09eb01643a1b334d. Inspected AI fixture diff: only narrows INSERT prefix to VALUES; assertions preserved. Failed prior runs retained, not counted as passing.

SAF used reused dedicated syntheticAVD and currentcp8-final files, not a pristine wholeAVD. ENOSPC is actual Android file-descriptor write failure from syntheticprovider, not full physical disk. Cleanup of partial failed export remains explicitly unknown; no successful-backup claim. reminder_runtime operational reconcile stamps excluded from backup equality; no user field excluded. Real AI provider, Xiaomi15 SAF, actualTalkBack, family/natural reminder experience remain unverified. Voice quality and separate voice controls remain pending. This accepts E9/CP8 engineering, not full-App completion.

Next: retained approved independent CP2 minimal voice commands before final phone/family phase; no new model candidate or reopening pausedSenseVoice.
