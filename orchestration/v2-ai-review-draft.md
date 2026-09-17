# V2 AI suggestions review preparation — NOT DISPATCHED

Dependency: finish and independently review current V2-CALENDAR-IMPORT-001 before binding a new baseline/attempt/contract. This file is preparation only, not permission to start a second developer task.

Authority: approved emulator-first-full-engineering-addendum-2026-09-16.md E7 I1-I6. Single CP5 task; preserve local notes, reminders, calendar import, voice and current backup behavior. No voice candidate revival, relations implementation or backup format expansion. Credentials and actual provider consent are absent; do not infer configuration from other projects or read unrelated secrets.

## Implementation and acceptance

- Default disabled. User-editable endpoint/model/credential; clear/disable supported. Platform protected credential storage, no credential in logs/Git/backups. Visible provider and exact outgoing fields before consent; endpoint/provider change invalidates consent. Protocol and supported endpoint format documented, avoid imaginary universal compatibility.
- User selects current note, previews minimal text and needed candidate category names/local identifiers, explicitly requests suggestion. No whole database, unrelated imported calendar provenance/account fields, recycled content, raw audio or unrelated relations. Imported note body can contain source metadata: inspect the actual outgoing selection rather than assume every body is safe/minimal.
- Real asynchronous request adapter with bounded input/response, timeout/cancel, duplicate prevention; no silent vendor fallback. Independent title/category suggestions, editable and rejectable. Manual choices retained. RecordId/revision plus title/category ownership guards prevent stale response/application. New category is a proposal requiring explicit confirmation, never automatic creation.
- Parse only bounded title/category result; provider prose/instructions cannot trigger actions, execute code or replace body. Offline/429/5xx/invalid/empty response preserves existing data and manual features. Cancellation/disable invalidates late results; UI explains sent content cannot be recalled.
- Persist accepted suggestion provenance separately from final user choice as needed by I3 and later CP8. Explicit current backup limitations, migrations preserve prior data. Temporary unaccepted responses excluded from backup.
- Host and Android emulator tests use clearly labeled synthetic mock endpoints for failure/race/boundary cases, plus real UI configure/consent/preview/accept/reject/disable flows and outgoing-field assertions. Never claim mock as provider_verified. Build/lint/affected regression evidence and exact final commit/APK required.
- Actual provider proof only with user-configured endpoint and explicit testing consent, synthetic single-note request, sanitized response/field evidence. If unavailable, retain provider_verified=false and exact external gap; independent engineering may finish with partial real-service validation, not full-App completion.

## Review traps

Check redirects and endpoint changes do not leak credentials or forward text to an unconfirmed supplier; failures do not log URLs with embedded secrets or response bodies. Verify source/account metadata of imported notes is excluded unless explicitly selected as necessary current-note text. Check secret clearing and configuration disable across process restart. Cancellation must prevent apply even if underlying transport completes. Current-node switch, draft edits, manual title/category edits and category deletion during flight must invalidate affected proposals. No automatic tests against configured personal providers; no acquiring keys/accounts or payments.

## Delivery

Unique CP5 contract to be created only after CP4 result review. Report I1-I6 with host/emulator/provider/Xiaomi/family labels; provider_unverified is a tracked gap, not a deleted requirement. Next independent work is explicit relations after this task closes under approved sequencing.
