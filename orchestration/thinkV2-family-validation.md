# Family delivery validation (pending)

This document preserves the final user-facing validation requirements while engineering continues. No result below is complete merely because a unit or emulator test passes.

User device decision: use emulators during development; after development is complete, the user will validate on Xiaomi 15. Do not request or operate a physical device early. Retain natural reminder timing and physical/household validation as explicit final evidence gaps while continuing the full engineering roadmap.

## Before personal use

- Bind the intended APK hash and source commit to the specified physical Android device.
- Keep the father's original calendar and notes intact. Use synthetic data and a test backup copy for destructive/failure scenarios.
- Complete device notification permissions/channel and power-restriction checks without changing settings invisibly.
- Verify readable large-font screens, keyboard/back behavior and manual TalkBack navigation for the delivered flows.

## Household workflow

| Step | Observable evidence | Current state |
| --- | --- | --- |
| Create a new record | Father performs entry and confirms saved content; record assistance and friction | Not tested |
| Repeated reminder | Same note's schedule produces real events; notification opens exact record, dismissal does not cancel future repeats | Not tested |
| Retrieve a record | Father finds and opens intended content from home without family operating for him | Not tested |
| Backup/restore | A synthetic copy exports and restores with field-level equality; local records survive conflicts/failure | Not implemented/tested |
| Core usability | Father confirms usefulness, with any required help and blocking issues recorded | Not tested |

For daily/weekly recurrence, fixed-clock or compressed-time engineering tests remain labeled simulated. Natural repeat delivery and physical-device behavior require actual event evidence. The initial family observation can include one real reminder event, while repeated engineering delivery evidence remains separate.

If typing blocks the father's use, elevate real offline voice input as a required next implementation; do not declare the need satisfied by a text-only engineering build. Raw audio must not be persisted, uploaded or logged. Existing source privacy constraints remain.

## After initial success

Observe voluntary repeat recording/retrieval and assistance needed. One successful trial does not prove sustained use. This follow-up is not automatically scheduled by this document.

Full-app roadmap items (voice, calendar migration, optional AI suggestions and explicit note relations) remain tracked in the completion matrix. First household workflow validation does not automatically close the full development goal or authorize public release.
