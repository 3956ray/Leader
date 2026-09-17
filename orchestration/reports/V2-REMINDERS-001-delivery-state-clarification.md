# Reminder delivery uncertainty clarification

Within the approved B6/B7 contract, the commander accepted the developer's conservative handling of a crash between database state and OS notification posting. This is implementation clarification, not a weaker completion criterion or a claim that reminders never fail.

- Distinguish a known missed occurrence, a successfully returned OS post call and an indeterminate crash window. None proves the user read the notification.
- An indeterminate occurrence must be visible as unconfirmed, not asserted definitely undelivered. Summary wording must express uncertainty; retain affected note/time/reason and a view/reset path.
- Do not automatically repost the same uncertain occurrence, avoiding duplicate alerts; future recurrence must continue. An explicit reset uses a new plan revision.
- Test both crash windows, cold-start versus late callback, and callbacks arriving after disable/edit/soft delete. No stale schedule resurrection or hidden loss of the entire plan.

The user separately confirmed emulator-only verification during development, followed by their own Xiaomi 15 validation after development is complete. This does not turn natural delivery or physical-device evidence into a passed item.
