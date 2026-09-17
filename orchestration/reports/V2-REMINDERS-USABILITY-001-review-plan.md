# CP7 reminder usability review plan

Contract: f691b2393ed29bec186ea9d2ee7579807e629a6a78ba575873b18e29948377cf; attempt8da8a67a-0259-4df6-9ae1-924d7c3fad37; baseline8a98e09d1276a17016a4e71f7f7385f6c57e402c.

- Inspect actual six font/theme configurations and screenshots of list, form, validation errors and event history. Verify large-font fixed-header/error space does not make form or save unreachable; do not infer bugs from static layout alone.
- Verify actual selected/toggle state and labels; keyboard focus; essential button bounds; same-title plans open exact IDs. Actual TalkBack outcome separately documented, no blanket accessibility pass.
- Save/date/time/repeat/weekdays/enabled changes must reach actual database. Back/rotation behavior must match existing semantics; existing scheduling, notification privacy/revision/dedup and cancel behavior retained. Distinguish a dismissed keyboard from navigation.
- Tie every cohort to exact product/test APK and final commit. Inspect raw logs and database assertions, not only summary booleans; preserve failed probes and never count hardcoded success flags as proof.
- Review minimal source diff, no schema/dependency/permission change. Verify manifest hashes and relevant host/Android results. Accept scoped engineering only, retain natural daily/weekly, Xiaomi, family, TalkBack, ASR and real-provider gaps.

Initial observation: new developer turn01a0aaf0-7144-7051-8052-10fe18572986 is active/inProgress; ACK pending. Clean baseline worktree and leader_check passed. No duplicate dispatch.

Initial visual review: matrix/2.0-light/error-with-ime shows fixed header/error consuming most area above keyboard and caret handle overlapping keyboard toolbar. This is a constrained viewport observation, not yet proof of blocked operation. Sent same-task request to verify actual visible correction of date/time/weekdays through save and DB, minimally fix only if obstruction confirmed; preserve error content/font scale. Baseline screenshot probe is not full workflow success.

Interim scope review: developer confirms baseline snapshot probe is not correction-path acceptance; initial multi-root dump failure retained. Current changes move full error/header into scroll, enlarge switch row and fill18sp body. Read ReminderRepository diff: only noteLabel SELECT adds category/body for bounded matchingExcerpt. Searched all main reminder callers: consumed by ReminderModel labels and screen; no notification sender caller found. This read-only presentation query is within same-title disambiguation scope, not scheduling/schema change. Final correction-path DB assertions, switch state/bounds and actual matrix evidence still pending.

First post-change2.0-light run raw log fails at platform switch class assertion: expected android.widget.Switch, observed android.view.View. Viewed target-2 screenshot: enabled row and repeat controls render; visual switch does not establish accessible switch state. No pass claimed. Developer still active; next review must inspect actual node checkable/checked/actions and chosen semantics correction or supported mapping explanation, preserving state/operability assertions.

Normal IME supplemental inspection: viewed normal-ime/reminders-2.0-dark-normal-correct-time-ime.png (00:33), which shows ordinary keyboard without font-size banner, complete focused10:35 field/caret above IME. Read normal-ime/instrumentation.log: OK(1),31.383s. Earlier12:29 matrix image still had banner and was not accepted as ordinaryIME. Final supplemental testAPK binding remains pending in delivery.
