# CP4 ongoing review

Not acceptance.

## R1 Coverage ended versus never published

Public renderer maps existing expired/outside coverage to unpublished label. AC-S02 explicitly distinguishes coverage ended from never published and empty/withdrawn. Requested current coverage endAt boundary and today/week partial-coverage UI tests. Also requested immediate stale-current downgrade on foreground before asynchronous response, since clock trust resets. OPEN.

## Independent regression

Full current suite 83/83 PASS, exit 0 (cp4-leader-full-tests.log); static syntax/JSON/frozen baseline/native references check PASS. Source snapshot cp4-tested-files.json. R1 covered by native exact coverage-end, outside/partial selection and immediate foreground downgrade test; final source match pending. No WeChat compilation/device claims.

## R2 final integration teardown failure — REVISE

Final commit 582488dcbc37369b88312b36210e9a352d136d61, manifest matched and clean. Independent final supplement exit 1: 9/10, ENOTEMPTY in identity-support.mjs fixture after hook while schedule test service was still alive. Runner hung until Commander terminated only confirmed child localhost service PID 5560. Evidence cp4-leader-final-supplement.log. Fix teardown ordering: await owned service/process exits before DB close and fixture removal, including failed assertions/startup paths; do not hide failure with forced recursive deletion while writers live. Preserve original integration assertions. Reverify targeted test and final complete regression. CP4 not accepted; CP5 not dispatched.
