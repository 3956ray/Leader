# CP3 independent acceptance plan

Status: prepared, not executed. Task GYM-CP3-MEMBERSHIP-001; accepted base 6729bb7f2579a559e44a920d5cf92347e3791564. Frozen acceptance matrix and technical contract remain authoritative.

## Pairing and verification

- Secure eight-digit codes preserve leading zeros. Five forced collisions roll back the complete creation, old request invalidation and count; do not swallow unrelated database failures.
- AES-GCM display copy binds environment/store/request/expiry; only active owner can decrypt. Terminal state clears ciphertext and lookup is unusable; no plaintext in operation results, logs, audit or cache.
- Exact 600-second expiry; fixed-window generation and error buckets sample time under lock. Same key does not recount; unknown code counts operator only, located requester errors count both, conflicts/server errors do not count. Limits persist across session and process restarts.
- Distinct Registry and Binding enforce both current-slot unique constraints. Inspect must return Registry revision even without a Binding, and distinguish requester binding from reference's current binding. Member reference normalization preserves case/leading zeros.
- Ordinary bind cannot restore revoked Registry. Explicit restore requires fresh pairing and front-desk confirmation; another account's occupied slot conflicts. Fixed/no-fixed/pending expiry modes and exact time boundaries must be distinct.

## Unbind and deletion

- Five-minute fresh authentication uses authAt, not last interaction. Confirm/cancel and CAS use the correct independently read account/binding/registry/pairing revisions.
- Client saves a securely random receipt before delete POST. Storage/random/hash failures prevent transmission. Lost response recovers through receipt capability; receipt never appears in URL or logs.
- Acceptance transaction marks deleting, revokes every session/role, closes bindings and invalidates pairings. Concurrent login cannot recreate until final cleanup; all domain writes deny deleting subjects.
- Actual durable jobs clean in bounded atomic batches, retry original job after injected failure/restart, retain identity lock, expose delayed after 24h, and only complete after verifying no remaining personal links.
- Final transaction removes identity mapping and account linkage; completed receipt becomes unknown at seven days. Re-login creates new userId with no inherited role or membership. Minimal revoked Registry survives and still requires explicit restore.
- Deletion removes account-associated pending-operation/member caches and scrubs actor links from existing observation/audit history while preserving public observation control/time.

## Evidence layers

Require native owner/operator paths plus persistent backend, actual competing processes and independent HTTP clients, rollback/expiry/rate/identity races, deletion recovery and previous CP0–CP2 regressions. Validate test assertions against requirements, final source hashes and clean scoped commit. VM tests do not establish WeChat compilation, official identity, real device or front-desk validation. No schedule implementation during CP3.
