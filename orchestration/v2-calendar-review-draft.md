# Calendar import review draft — not dispatched

Source: approved emulator-first-full-engineering-addendum-2026-09-16.md, D1–D6. Bind the reviewed clean final Git baseline only when dispatched. Current sole task remains V2-OFFLINE-VOICE-002 until receipt/review and explicit parking; no calendar implementation is authorized by this draft. Voice entry quality and separate explicit voice controls remain unmet full-goal requirements. Approved emulator-first rules permit independent work after parking a blocked single task.

## Single goal / CP4

User-selected, read-only calendar import into local notes, preserving original content and traceable source identity. No source mutation or automatic reminders.

## Allowed work

- READ_CALENDAR only; user selects calendar and bounded date range before preview. Rejection/revocation/cancel leaves source and local notes unchanged.
- Preserve title, description, source calendar/event identity, original dates/time zones, recurrence and reminder metadata. Title-only events remain importable.
- One recurring master becomes one note; exceptions are separately visible/selectable. Unsupported recurrence/exception/reminder values remain preserved and explicitly unconverted.
- Preview new/imported/changed/unconverted/skipped counts, selection and editable local category. No automatic AI submission or reminder enablement.
- Source identity plus content fingerprint controls idempotence; repeated batch/relaunch creates no duplicates. Changed source never silently overwrites edited notes; skip or explicit new copy.
- Transactional batch, stale-preview recheck, migrations preserving existing notes and identity. Source-ID ambiguity after account reconstruction requires explicit handling.

## Evidence

Actual Android provider fixture isolated to synthetic calendar data: Chinese/title-only/all-day/time zones, recurrence/exceptions, source edit/deletion, similar titles, permission refusal/revocation, cancel/retry, local edits and relaunch. Verify source rows/metadata unchanged and local content/mapping/transaction rollback, not just counts or success UI. Test fixture may write its own source events; product must not request write-calendar permission.

## Exclusions and stop conditions

No account creation, source calendar edits, cloud sync, AI upload, recurrence-to-reminder conversion, voice changes or cross-feature backup implementation. Stop affected work for data loss, unauthorized sending or unknown dependencies. Xiaomi/provider/private-calendar evidence remains pending until the user’s final device phase. Deliver fixed commit/APK identity, D1–D6 mapping, tests, unresolved cases; stop after this single task.
