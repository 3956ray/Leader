# D2 clarifications

External-key explanation read/accepted at SHA8f0e5da5bb94eff0d0f6111f680b301a183d83892cc0da9705264462d44313e2. Stable source/external IDs survive updates/absence/cleanup; unknowable source key reuse is a documented limitation, explicit evidence escalates affected import. No heuristic/system expansion.

Leader approves narrow explicit replan exception to resolve P5.3/P5.5 conflict. Ordinary plan still reuses fresh candidate. Only unapplied candidate with changed local bound versions may be explicitly replaced; old batch, source revision/hash and current versions checked atomically, old batch invalidated, replacement requires fresh review. No draft/public/cursor mutation, no source version inflation. Concurrent applied result/highwater/hash rules preserved. PM formal addendum pending before implementation of exception; independent D2 work continues.

Formal explicit-replan addendum read and accepted, SHA256 dce434a06635ed83866fa3a701e1b2c90f1a869c22fd3e471ee5a93341fa77c3. Includes DM09-RP1–RP5 and preserves approved minimal boundaries. Added to current D2 inputs; no new task.
