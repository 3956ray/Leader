# CP5 review plan — not acceptance

Contract GYM-CP5-INTEGRATION-001; accepted baseline e8c004e194b8a332c05c206927d3f196c67a33d9. Prior goal turn made progress: CP4 independently accepted and CP5 dispatched. Developer active turn confirmed 01a0a82c-fb5d-7f71-9d06-cfae47059745.

## Evidence to inspect on delivery

1. Match all 30 frozen AC identifiers exactly once in the report matrix. Inspect scenario-level evidence, not only aggregate test counts. W01 and T01/T02 remain later-stage evidence; do not manufacture CP5 passes for them.
2. Verify final code hashes and clean scoped commit; inspect integration changes against CP4 baseline, unchanged frozen document hashes and dependency boundary.
3. Inspect actual native lifecycle flows and cross-domain invariants: course/member writes cannot refresh observations; delayed operation results cannot regrant qualification; page/account transitions cannot expose stale personal data.
4. Verify actual startup/hourly cleanup and failed deletion recovery, durable jobs, bounded batches, retained current controls, identity lock and final cleanup ordering. Helper-only assertions are insufficient for integrated wiring.
5. Inspect official DevTools version, selected base library, AppID capability, import/compile output and actual native interaction evidence. Static checks/VM screenshots do not establish tool PASS. Check public/My/operator normal and failure states and distinguish simulator evidence from backend responses.
6. Run independent regression appropriate to final changes after source review. Reconcile every failed or blocked scenario with report; preserve evidence and distinguish platform prerequisites from engineering defects.

## Gate

CP5 ACCEPTED requires both engineering and tools PASS. No CP6 dispatch without that acceptance and its separate real platform/device prerequisites and authorization. No uploads, publication, real membership records or security-check bypass authorized here.

## Tool diagnostic checkpoint

Developer reports official tool Stable 2.02.2608070. Independently inspected cli-open-host.log: official CLI reports IDE service port disabled; no successful target import/compile evidence yet. First sandbox open EPERM and host service-port-disabled failures are distinct and retained. GUI currently involves another project; developer reports stopping unreliable import-dialog retries without modifying that project. AppID remains touristappid placeholder. Actual base library/native screenshots unverified. Tool layer provisionally BLOCKED, not CP5 acceptance.

Developer confirms no pending background process at this checkpoint and continues independent engineering integration/30AC matrix. Overall work is still progressing, so this is not an impasse of the active goal. Do not restart or duplicate CP5.

## Preliminary engineering review (working tree, not acceptance)

Read integrated-lifecycle.test.mjs and integration-tests.log: 23/23 pass in developer run. New shared cleanup-runners module is called by server/main and controlled-clock integration tests. Tests exercise all three schedulers, hourly failure/retry, revoked Registry survival, observation TTL unchanged by membership/schedule/deletion, and current withdrawal control preservation. These are controlled timer/service tests; retain separate actual child-process restart evidence in final matrix. Source remains mutable until developer final manifest/commit.

Read native regressions for delayed delete response preserving newer session/storage, hidden role response preventing navigation, and late login modal confirmation preventing platform login. Final independent test execution pending delivery.
