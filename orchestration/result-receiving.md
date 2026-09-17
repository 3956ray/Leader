# Result receiving protocol

State transitions now follow [LOOP-V2.md](LOOP-V2.md). Every receipt binds task_id, attempt_id, contract_sha256, assigned_thread_id and observed execution turn. Use leader_loop.py ack/result/review; do not manually patch current-task.json or state.json.

The user now explicitly requires both current PM and developer to call back to Leader after each completed task. This supersedes the earlier no-push preference in historical task contracts. The completion callback contains the task identity, result, artifact/evidence references, checks, limitations and Git state; it is not acceptance. The instruction has been sent to both current tasks. Actual reverse delivery is still subject to the application permission check and must be observed, not assumed.

If a callback is denied, record the exact failure in the executor final response and do not retry or bypass it. Leader polling remains a recovery mechanism, not the primary completion notification. User intent in the Leader task does not by itself prove another task's automatic permission reviewer will allow the send.

1. The executor completes its contract, writes only authorized artifacts, sends a completion callback to current Leader and leaves the report plus actual callback success/failure in its own final response. It then stops.
2. Leader uses permitted wait_threads snapshots to inspect completion in the assigned task. read_thread is only for necessary context, not recovery of a permission-denied transmission payload.
3. Leader records a receipt with task ID, executor task/turn, artifact reference and pending/accepted review status. Receiving a final response is not product evidence acceptance.
4. Leader independently inspects authorized formal artifacts, test evidence and Git boundaries. It moves dispatched/IN_PROGRESS to completed/AWAITING_REVIEW once completion is observed, then separately accepts, revises or escalates.
5. Leader waits during the active interaction, receives the executor callback, reads original result evidence and continues authorized dispatch. The user deleted scheduled automation: do not recreate it or depend on a timer to receive results.
6. If polling itself is permission-denied, stop and request the required direct user permission. Do not replace it with another channel to obtain the same denied data.

The callback should explicitly identify itself as a completed-task report, not a request to execute copied instructions. Leader checks its identity and independently reviews evidence before dispatching further work. PM and developer do not dispatch to each other; Leader remains the only scheduler.
