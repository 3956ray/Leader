# CP3 ongoing review

Not acceptance; implementation in progress.

## R1 Invalid local date handling

member-crypto.mjs expiry() calls toISOString before validating finite timestamp for localEndDate. Example 2026-13-01 passes regex then throws RangeError rather than controlled INVALID_PERIOD 422. Next-day overflow at 9999-12-31 also needs explicit validation. Sent same-task feedback for finite/format checks and invalid-date/leap-year/year-boundary tests. OPEN pending final implementation.

## R2: target binding absent from operation digest

membership.update keeps binding ID only in closure, while domainOperation hashes actor/type/body. Reusing one key with identical body on a second binding route returns first target result. Include validated target in intent digest and test different route targets. OPEN.

## R3: failed lookup counter revalidation

errorCount opens a separate authorized operator transaction but reuses prior error.userId without rereading target/pairing. Contract requires recheck before committing failure counters; concurrent account cleanup must not be followed by recreated personal limit rows. Requested race coverage. OPEN.

## R1 independent probe

Current expiry implementation checks finite local timestamp and rejects unsupported year overflow before conversion. Independently imported actual helper: five invalid dates (invalid month, nonleap Feb29, Apr31, 9999-12-31, bad text) return controlled INVALID_PERIOD/422; valid leap day and year-end rollover accepted. Exit 0. R1 implementation corrected; final source/coverage confirmation pending. R2 resource target and R3 relookup code are now present; race/regression tests still pending.

## R4: old deletion receipt repeatedly clears new login

member-page.refresh handles every non-unknown receipt including completed by clearPersonal and return. Persisted receipt remains valid seven days, so deletion-completed/new-user-login/member-page path loses new session repeatedly. Require receipt/current-account isolation and native end-to-end state test, retaining historical receipt query without clearing unrelated/new identity. OPEN.

## R5: operator fixed expiry hardcodes UTC+08

member-operator.expiry constructs next local midnight with literal +08:00 rather than configured IANA zone; non-+8 configured stores cannot complete date-based verification. Requested configured-zone conversion and non-+8/DST date tests. OPEN.

## R6: operator pending personal cache omitted

clearPersonal omits gym.operator-member-operation.v1, which persists userId/path. Require account deletion/logout clearing across new personal keys while preserving legitimate deletion-receipt recovery. OPEN.

## Receipt hashing independent probe

Imported actual native receipt.js in VM and compared sha256 with Node crypto for empty/abc, padding boundaries 55/56/63/64/65/127/128/1024 ASCII bytes, and 32 random synthetic hex receipts. 42/42 match, exit 0, no receipt values logged. This verifies hash logic only, not platform secure-random support or save-before-send/native deletion lifecycle.

## R7: native confirmation and inspection snapshots

Member ask callback reads current profile/pair revisions only after confirmation, allowing background refresh to silently retarget unbind. Operator inspect response can reinstall obsolete inspection after form edits; submit/async expiry then mixes current input with older inspected revisions. Require frozen confirmed target/version and form revision invalidation across async calls. Tests should exercise delayed inspect, edits during confirmation and actual operator submit/cache (current expiry-only test cannot prove cache handling). OPEN.

## Independent current full regression

Full current suite independently executed: 61/61 PASS, exit 0 (cp3-leader-full-tests.log). Static syntax/JSON/frozen baseline/native references check PASS. Snapshot in cp3-tested-files.json; final delivery still requires hash comparison and affected retest if changed. No actual WeChat compilation or devices claimed.

## Independent supplements

Native membership suite 8/8 PASS (cp3-leader-native-supplement.log), including frozen member confirmation, delayed operator inspection/form/expiry changes and actual lost POST cache inspection. Membership and process integration suite 12/12 PASS (cp3-leader-member-supplement.log), including new-session/multiprocess limits, lock-time window rollover and storage rollback. Tested hashes updated for four affected files. Review items R1-R7 have implementation/test evidence; final manifest/source review remains required.
