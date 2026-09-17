# Backup review checkpoints

Active contract: V2-BACKUP-RESTORE-001 / CP8, attempt a7044d94-1422-4102-9994-0c6c80dcee68, baseline 1dde8ec7bd34caac991097c9f3962958cc753fab. This is an audit plan, not completion evidence.

## Existing-state round trip

- Exported snapshots must pass the application's own strict parser. Include formal notes, draft-only records, active/inactive drafts, category ownership and tombstones, trashed notes and their drafts, and reminder configuration.
- Compare empty-destination restoration field by field, explicitly accounting for imported reminders being disabled and runtime notification state not being a backup payload.
- A trashed note may retain a deleted category identity: represent this legitimate state without rejecting a self-generated backup or losing restoration semantics.

## Merge and preview

- Same formal body alone is insufficient to declare equality: inspect associated drafts, categories and reminder configurations.
- Map conflict copies and category identities consistently; preserve existing local records and their reminder plans.
- Verify preview performs no writes or OS scheduling, and becomes stale on relevant note/draft/category/trash/reminder changes.
- Repeated exportId/hash does not create more copies; same exportId with different bytes is rejected.

## Parse and failure boundaries

- Strict UTF-8, bounded file/payload/depth/counts, unique JSON keys/IDs and fields, numeric/time/rule validation, references and unknown versions/data fields.
- Corrupt/truncated/oversized input and injected partial SQL failure must leave the entire prior DB and OS schedules unchanged.
- Actual Android SAF write/read/cancel/error evidence; success follows completed writes. Plaintext/base64 and cloud-provider choices must be represented honestly.

No original audio or private father data in fixtures. Final acceptance requires code review, meaningful test evidence, exact artifact identity and documented physical/provider limitations.
