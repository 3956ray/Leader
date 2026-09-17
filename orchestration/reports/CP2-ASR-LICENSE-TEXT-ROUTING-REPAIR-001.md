# Leader acceptance: v5 explicit LICENSE text routing

Disposition: ACCEPTED — license_text_routing_candidate_ready_for_freeze.

Accepted commit: a60ced8861f4a9fd4716aa65866a90a861978989; parent f347260f8afc24a22970cead9740c5b6792d0527; v5 tree d5d66a3ef147b3fa587c8b77dd537b94c82fdf50. Acceptance covers first-party offline repair only. CP2 has not passed; CP3/Alpha are not authorized.

## Scope and identities

Leader independently checked all 1966 new v5 Git blobs against actual bytes, regular single-link files, exact commit boundary and clean worktree. The original manifest has 1965 records, SHA256 628c49834480dfb03f33db20dfae927bc3d7e6eea4d7088924d521f2917edb2b, canonical record digest 8354cd10fe23a82edcf0d1d80cdad490aa088f3d27911a2858260001d84f20a9. Existing v2/v3/v4 and old freezes retain their recorded tree objects.

The 20-file code/schema/test bundle is 1dd806b43fe95722150449e795337ee1e3a8e399ae53766e6aa041d5ca39dd3e. Policy SHA256 is 41b852bea2b247bf6b8f253bc57e3965dd835c10031000e52b438a09c3aa65db; role-contract SHA256 is 1c8a95b48c034e830b2a0a545192c691af12127774152921e1df73c6ee670125. Input schema changes from 3 to 5; typed kind and content_roles are explicit. Removing content_roles and restoring the former kind reproduces old policy ee9d1ae7b4b17d2d895d3a6e0b62f73bfda7eb8a9cfae50e9d264f9ed23fc627 exactly. All other source identity, roots, type/mode, seeds, budgets, denylist, transport and privacy controls remain unchanged.

19 baseline file hashes and byte-identical claims verified. Only eight baseline components change: acquisition, controller, protocol, storage, audit, verify, recalculate and SCHEMA; new routing and content-routing tests complete the implementation. The C++ parser, generic policy, synthetic adapter, transport, network guard and inherited test/support/fixture bytes remain unchanged. Historical evidence is referenced rather than copied.

Developer disclosed a temporary sibling commit-console file outside the v5 write boundary, immediately removed and never staged. Leader confirms it is absent and final Git scope is exact; the transient write is a disclosed process deviation, not erased by final cleanliness. Next task explicitly directs temporary console output to system temporary storage. No unknown or unrelated product modifications were found.

## Criterion evidence

1. Exact LICENSE/license_text routes to inert preserved text, never C++ parse or graph expansion. Spy and prose regressions cover apostrophes, unmatched quotes, URL/Markdown/multilingual and include-like content. Existing conservative deny indicators remain stopping evidence outside the graph.
2. Explicit policy roles and internal-edge assignment are validated before authorization, rechecked at adapter receipt creation and bound through durable intent, body and terminal. Unknown/near/conflicting path-role combinations fail closed; an internal C++ edge to LICENSE stops before successor acquisition.
3. Body identity/preservation, UTF8/NUL, budgets, request controls and ledger safeguards pass unchanged baseline regressions. Typed terminal always retains scanner_status=pending, license_review_status=manual_review and source_verdict=insufficient_evidence, including fabricated synthetic review fields. No synthetic simulation grants adoption.
4. Existing supported C++ literal includes retain graph/order. Include guards, conditionals, macros/generated forms, unknown directives and continuations remain intentional contract stops, with no successor request. They are not evidence of upstream infeasibility.
5. Leader copied first-party code/self-authored fixtures only to /private/tmp/think-leader-v5-qnrj4yoo. Both independent runs passed 132 tests (112 unchanged inherited +20 new), 761 method/subtest outcomes, no skips; 25 scenarios and720 ledger records per run. NetworkGuard has12 traps, actual_network_events=[] and trapped_workload_calls=[]. Code bundle remained unchanged before/after.
6. Reviewed independent recalculate.py ran against leader-a/leader-b. A separately authored Leader verifier rehashed both ledger chains/terminals/body identities/role bindings and compared962 JSON files across all four developer/Leader runs, byte-identical except deliberately excluded human timing/command logs. Normalized SHA256 f2a0fb9c4854991a628ac386ebe0901dea430b9eedebf4d561d5322b2a95a097.

## Actual scanner interpretation

Original scanner verdict remains sandbox_only, score100,18 findings (9high/5medium/4low), no block signals. Raw JSON SHA256 f83ba6965c60fce950bf7c7881ed391b6aac72b8cb06c518f33f8955ca616aa5. Leader read all raw findings and reviewed their corresponding source contexts; file hashes match. Python line matches are AST string constants, JSON matches are inert log/test data, README matches are command documentation, and all8086 matches are inside64-character SHA256 strings. No finding identifies an active eval/child process call or that network endpoint. This supports these bounded first-party tests; it does not rewrite the raw scanner verdict or approve third-party source/license/runtime artifacts.

All1959 scan-input snapshot records rehashed unchanged. Original coverage1961 candidates/1960text,0large/limit/unreadable; redundant .patch was classified nontext but every underlying code/schema/test was scanned. Later reports/context/final manifest were not scanner inputs and are checked as evidence. Custom AST capability audit has zero errors; it is not a hostile-code sandbox.

## Limits and next action

No real LICENSE, API/metadata, corpus or other third-party body was read, and no live request, dependency, build, model, device or App integration was performed in this review. Runtime source scanning, manual license suitability, actual v5 metadata/transport/body behavior, C++ closure, feasibility and all device/ASR/privacy gates remain unverified. Historical v4 real metadata validation cannot be presented as a v5 rerun. Prior wire JSON/header replay limitations remain.

Latest formal decision SHA256 27789c9bd35e6e452de70c21b637fc496d8ac17902cda075a98af81c7006aa75 controls. Separate three-file v5 freeze is now eligible for dispatch. Existing v4 run is terminated; old source authorization/mapping is historical. After independently accepted new freeze, a fresh explicit Product Lead authorization and separate dispatch are required for any second real acquisition. Existing third-party block/manual_review decisions, CP1 deferred gate and all privacy/checkpoint boundaries persist.

## Reproduction evidence

- CP2-ASR-LICENSE-TEXT-ROUTING-REPAIR-001-verify.py: SHA256 d66329e22b20a83d2c979412176f770aa5d59bfa00f3a882bda5009603efdfea
- CP2-ASR-LICENSE-TEXT-ROUTING-REPAIR-001-verification.json: SHA256 55276c8410d97cb2f36f8bef7b68259d655ad2b4e796800281c447008b473f2d
- CP2-ASR-LICENSE-TEXT-ROUTING-REPAIR-001-runs-verify.py: SHA256 eeb181874bb1a6a7bb6f4274ba2854eb6c74432b403659b40ec0964f88e9bffc
- CP2-ASR-LICENSE-TEXT-ROUTING-REPAIR-001-runs.json: SHA256 d99054b677f0a8620d1d71c14ba1406f049786874e66859f6a3e8622be726421

Test commands in the independent copy: python3 -B verify.py leader-a; python3 -B verify.py leader-b; python3 -B recalculate.py leader-a leader-b. All exit0. The identity verifier creates a new isolated copy if rerun; it never accesses real third-party data.
