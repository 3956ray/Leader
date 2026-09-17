# Receipt recovery

For LOOP-V2-DEV-PROBE-001, executor turn 01a07753-66a3-7c62-92c1-789cfcb8e5ff reported completed but wait_threads had no final message and read_thread returned items=[] with no receipt. No ACK, result or acceptance was inferred.

Leader sent one bounded follow-up requesting only receipt recovery for the same task/attempt, with no product work or repeated execution. The new observed recovery turn must be bound to the returned receipt. If it also lacks a valid receipt, block transport instead of retrying indefinitely.
