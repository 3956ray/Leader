# CP4 independent acceptance plan

Prepared, not executed. Task GYM-CP4-SCHEDULE-001; accepted baseline 22369e6320a64b96949acc31f195461134bba52d. Frozen matrix S01-S04, Z01 and relevant B01/M04/D01/I01/C01 govern.

- Public readers cannot see draft. Publication atomically validates both draft and publication revisions and replaces the full explicit 1–14-local-day coverage. Compare independent HTTP clients and competing publishers.
- Distinguish unpublished, explicit empty covered day, outside/ended coverage, and withdrawn. No fallback to an earlier snapshot, including after cleanup/restart. No schedule state implies real-time venue occupancy.
- Stable course IDs and per-course revisions survive rescheduling/cancellation; cancelled courses remain visibly marked but do not participate in current-course or overlap decisions. Touching intervals allowed, scheduled overlap rejected; cross-midnight/week queries use interval intersection.
- Explicit local date/time and UTC offset must round-trip through configured IANA zone. Reject nonexistent times, require explicit repeated-time choice, test non-UTC+8 and DST. Device timezone must not determine venue dates. Read current summary at exact start/end boundaries.
- Freeze operator confirmation/form snapshot across preview conversion, draft reads and publishing. Scope operation digest to target/body, query unknown writes with original key, read current snapshot after historical result. No optimistic publication or silent CAS overwrite.
- Native today/week/maintenance paths: normal/empty/error/offline/withdrawn; one actual inflight per resource through hide/show and delayed callbacks; failed response retains clearly historical revision and never inserts prior-week fixtures.
- Cleanup actual retired snapshot selection and retention boundary in store local time, bounded batches and persistent failure/restart recovery. Preserve draft/current publication/control; remove any new personal author links during account deletion.
- Verify unchanged observation TTL and membership eligibility, prior regression suite, no new unreviewed dependencies, exact final manifest and clean scoped commit. VM/native logic evidence does not prove WeChat rendering, devices or real venue data.
