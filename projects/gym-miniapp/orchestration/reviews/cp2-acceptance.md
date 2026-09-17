# CP2 acceptance

Decision: ACCEPTED, engineering scope only.
Task: GYM-CP2-OBSERVATION-001
Accepted commit: 6729bb7f2579a559e44a920d5cf92347e3791564

## Verified evidence

Developer report, implementation notes, dependency review and manifest reviewed. Final clean Git worktree verified; manifest and Commander tested-source hashes match every listed file. No generated database/runtime/key files tracked. Frozen product baseline and technical contract unchanged. No new dependency or later-checkpoint domain implementation.

Developer final suite: 45/45 PASS. Commander independently verified full 43-test suite and the final affected native suite 7/7, with static check PASS; final source hashes match cp2-tested-files.json. Logs: cp2-leader-tests.log and cp2-leader-native-supplement.log. Independent scheduling probe also passed.

- B01 venue/O01: public no-login API, empty real venue details, manual source and consistent durable revision; two independent HTTP clients and authorized publication.
- O02: backend/native 899/900 boundaries, immutable original observation timestamp/TTL across reads, restart and cleanup.
- O03: unavailable/control states and no resurrection of historical observations.
- O04/I01: transactional CAS/event/audit/operation, rollback, actual competing processes, same-key replay, committed role-revocation barrier, frozen confirmation revision and uncertain result recovery.
- O05: single inflight refresh lifecycle, delayed callback invalidation, conservative server time plus monotonic elapsed time, offline historical state and clock failure closed. Native evidence is VM only.
- D01/C01 observation: service-process restart, startup historical cleanup, bounded 100-row batches, injected batch failure and durable cursor recovery, next-hour scheduling after batch execution time.

Both early review findings R1 scheduling drift and R2 independent clients/process evidence are closed by inspected code and tests.

## Explicit unverified layers

No WeChat compilation, actual AppID/official login, device compatibility or real venue validation. These remain NOT_RUN. Membership, account deletion, schedule and non-observation cleanup are not represented as completed. No deployment/upload/publication authorized by this acceptance.

Next authorized checkpoint: CP3 under its own single task contract.
