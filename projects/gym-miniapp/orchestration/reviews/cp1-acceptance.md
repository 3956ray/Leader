# CP1 acceptance

Decision: ACCEPTED (engineering scope only).
Task: GYM-CP1-IDENTITY-001
Accepted commit: 7a9e76c0123ec3c80ab3aa9bde9886f1e8ad6880

## Evidence

- Product reports/cp1/developer-report.md and manifest.json reviewed; final worktree clean, all manifest and independently tested source hashes match. No runtime secrets/databases tracked. Frozen baseline unchanged.
- Developer final suite: 30/30 passed; static check passed.
- Commander independent full suite: 28/28 passed (cp1-leader-test.log). Final changes independently verified with 20/20 identity/native tests (cp1-leader-supplement.log), then static check. Other tested source hashes unchanged (cp1-tested-files.json).
- AC-L01 engineering: strict official adapter transport contract, isolated explicit test identity, replay/error rejection and secret handling.
- AC-F01: session expiry boundaries, nonrenewing polling, five-session limit, concurrent identity uniqueness, current logout and failure rollback.
- AC-M04 role foundation: server-side authority, audited CLI grant/revoke, foreign-store denial, real concurrent revoke/write ordering.
- AC-R01 login: persistent 120/min limit with multiprocess/restart evidence; time sampled inside transaction.
- AC-P01 foundation: explicit purpose/consent/refusal; public scaffold accessible. Related AC-I01: strict parsing and atomic idempotent logout/role changes verified.
- Review findings closed: lock timing, foreground stale auth, overlapping refresh, revoke ordering, and uncertain logout retries with same key.

## Limits

No actual official login, WeChat compilation, phone tests or real venue validation. These remain NOT_RUN, not acceptance of those later layers. Membership, observation, schedule and deletion are outside CP1. No added third-party dependency. Retention cleanup beyond logical expiry remains scheduled for later checkpoints.

Next: dispatch only CP2 manual observation workflow.
