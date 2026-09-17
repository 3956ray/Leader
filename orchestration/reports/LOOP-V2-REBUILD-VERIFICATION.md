# Loop v2 rebuild verification

Overall: BOTH LIVE RECEIPTS VERIFIED; APP HEARTBEAT WAKEUP STILL UNVERIFIED

2026-09-07 update: the original developer recovery final became readable through read_thread. Its four binding fields and literal acknowledgment/COMPLETE/no-change flags match the contract. See probes/dev-receipt.json and dev-review.json. The earlier empty reads remain accurate historical observations; root cause and any causal relation to the user's new message are unknown. No work was resent. Late receipt recovery now has a guarded transition preserving the resolved blocker. All 23 tests pass. PM and developer live receipt gates pass; the following earlier blocked notes are history. App heartbeat remains paused until separately resumed, and no timed wakeup success is claimed.

## Implemented

- Atomic authoritative loop-ledger.json with serialized state transitions and append-only event history; current-task/state are generated views.
- Frozen contract and digest, unique attempt ID, executor routing, receipt turn binding.
- Separate send intent, confirmed delivery, observed acknowledgment, result receipt and review.
- Duplicate dispatch/task replacement/checkpoint jump prevention; missing results and uncertain delivery cannot be accepted.
- Hash-bound review evidence; failed checks/BLOCKED result cannot pass acceptance.
- Mirror drift detection and explicit recovery; old product task and all pre-migration state retained in the ledger.
- Product dispatch hold remains active. Existing PRD Checkpoints were not changed.

## Verification

22 unittest cases pass, including full synthetic loop and continuation, rejection/rework, stale routing, identity mismatch, missing acknowledgment, duplicate send, evidence alteration, failed acceptance, held product dispatch, state-view drift and CLI recovery after view damage.

PM live probe: PASS. Sent LOOP-V2-PM-PROBE-001, observed acknowledged/COMPLETE from original final message in turn 01a07751-7592-7dd2-88d3-de8df9f5c74b, matched task/attempt/hash/role, checked unchanged product Git worktree, accepted and automatically staged/sent developer probe without another user prompt. Evidence: orchestration/probes/pm-receipt.json and pm-review.json.

Compact wait_threads omitted boolean literal values in its rendering; read_thread original final preserved them. Protocol now requires original final text for structured receipts, never guesses missing fields.

Developer live probe: BLOCKED. Initial turn 01a07753-66a3-7c62-92c1-789cfcb8e5ff and one receipt-only follow-up 01a07755-7e51-7890-8899-40977912bd37 both reported completed with no error, no final message and empty original items. No ACK or COMPLETE inferred. This is not an observed permission denial and its cause is unknown. No more automatic retries. See dev-empty-result.md and dev-blocked.json.

Product repository independently remains clean at 92e50278, main ahead 58. No product, knowledge, dependency, artifact or checkpoint modifications were made by these probes.

## Remaining gates

- Obtain a readable developer acknowledgment/result and independently accept that probe.
- Real app heartbeat wakeup is not yet proven; automation remains PAUSED. Do not claim it works from configuration alone.
- Only after both probes pass, verify rebuild evidence and use release-hold. Reconcile the parked product scope decision and existing user authorization before subsequent product dispatch; no repeated authorization request unless its scope is genuinely insufficient.
- The engine records Leader-verified observations; it does not independently invoke application tools, make semantic product judgments or run as a background daemon. Leader must perform the wait/review/continue loop and the app must supply scheduled wakeups.
