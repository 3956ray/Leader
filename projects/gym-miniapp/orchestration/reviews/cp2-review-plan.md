# CP2 independent acceptance plan

Task: GYM-CP2-OBSERVATION-001. Status: prepared, not executed; no acceptance implied.

## Authoritative requirements

Frozen acceptance matrix AC-B01 venue, AC-O01–O05, AC-D01 observation, AC-I01 observation, AC-C01 observation; technical-contract sections 2, 3, 6 and 7. Contract baseline commit: 7a9e76c0123ec3c80ab3aa9bde9886f1e8ad6880.

## Evidence to inspect

1. Public endpoints and two independent readers: no login required, same committed revision/time/source; honest missing venue details, no numeric occupancy.
2. Backend transaction: role checked under write lock, CAS and operation body digest, event/head/audit/operation rollback together; no accepted write after committed revoke. Successful interactive writes renew session idle; public polls do not.
3. Time: commit timestamp sampled inside transaction, 60-second publication intent, 899/900-second boundaries. Malformed/future timestamps fail unavailable. No read/restart/cache/cleanup changes observedAt or validUntil.
4. Native lifecycle: one real inflight request per resource across hide/show; late callbacks cannot overwrite a newer state or restore trust. Response transit time cannot extend freshness. Foreground restoration obtains a new time baseline. Missing/broken monotonic clock and offline restart retain only explicitly historical information.
5. Maintenance failure: uncertain response retains original key/body/time; result query plus current-state read, never optimistic success or automatic new observation. Expired intent requires a new physical observation confirmation; CAS conflicts do not overwrite another operator.
6. Controls: never/unknown/paused/withdrawn remain distinct and unavailable; no scanning historical events to replace current control. Cached connection state is separate from observation age.
7. Cleanup: event retention at 30 days, bounded startup/hourly work, persisted progress/errors, restart recovery. Current head is self-contained and survives removal of its historical event. Verify actual scheduler wiring, not only cleanup helper tests.
8. Regressions: prior CP0/CP1 tests, frozen source hashes, isolated synthetic fixtures, no added unreviewed dependencies or later-CP implementation. Inspect changed source and test coverage before independent execution.

## Acceptance record requirements

Record exact final commit, clean/owned changes, tested source hashes, per-AC evidence and command exit codes. Tool compilation, official WeChat, devices and real venue remain separate unverified layers. Do not infer them from native JavaScript VM tests.
