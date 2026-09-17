# CP2 ongoing review

Not acceptance; source is still changing.

## R1: hourly cleanup schedule drift

Observed fixed setInterval(HOUR) with next_run_at set to final batch time + HOUR. A nonzero or multibatch runtime can place the next fixed tick before next_run_at; batch then skips and the next opportunity is another hour later. Sent to developer on the existing CP2 task for correction and deterministic scheduling coverage. Status: OPEN pending final implementation/test evidence.

## R1 follow-up

Current implementation uses chained setTimeout scheduled from persisted next_run_at minus current time. Commander independently imported actual scheduler and verified with fake timers: a run advances time 250ms, sets due time, then incurs another 30ms; timeout is HOUR-30, fires at due time, and second run is scheduled correctly. PASS, exit 0. Scheduler-only check; database cleanup/failure tests and final source-hash verification remain pending. R1 status: implementation corrected, full delivery evidence pending.

## R2: independent client/process evidence

Early observations.test.mjs compares current()/venue() on one service instance. Final evidence must add two independent HTTP clients, service-process restart persistence, and competing operator observation CAS/revoke ordering through actual observation writes. Requested within existing CP2 task. Status: OPEN, final evidence pending.

## Independent regression and recovery

Commander full suite 43/43 PASS, exit 0 (cp2-leader-tests.log), static check PASS. Page changed during review; affected native suite independently rerun, exit 0 (cp2-leader-native-supplement.log). Source hashes recorded in cp2-tested-files.json; final delivery must match or changed files require review. Actual HTTP/process tests now cover R2; pending final manifest check. Developer turn ended with usage-limit failure before final report/commit. Fresh usage read permits ordinary usage; resumed same CP2 task, confirmed new active turn 01a0a7cf-111b-7f13-bb46-3201af321cbe. No new checkpoint dispatched.
