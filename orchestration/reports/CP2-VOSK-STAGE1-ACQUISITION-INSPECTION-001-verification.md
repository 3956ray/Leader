# Stage1 independent verification

Verification: PASS for limited acquisition and outer inspection, pending receipt/acceptance transition.

Leader read the fixed stage1 helper without executing it, recomputed both artifact SHA-256 values and byte lengths, checked all eleven final evidence-manifest records, and independently parsed outer ZIP inventories and the previously selected text members using scripts/verify_vosk_stage1.py. That verification read no nested code, executed no target, made no network requests and extracted nothing.

| Object | Actual bytes | SHA-256 | Outer entries | Rechecked selected text |
| --- | ---: | --- | ---: | ---: |
| Vosk Android 0.3.75 AAR | 13472638 | ab2f8b91ac8051561aa325546b35fed9a68b36b8121bac5c6fb927525c4adfad | 13 | 156 bytes |
| vosk-model-small-cn-0.22 ZIP | 43898754 | 3af8b0e7e0f835ae9d414ce5df580237a3cfb08d586c9fbbb0f7ff29ad5b14ba | 20 | 559 bytes |

Retained HTTP headers and ledger record two direct 200 GET responses, no redirects/retries, total network body 57371392 bytes, acquisition/inspection 130.165 seconds. The helper enforces HTTPS with certificate checking and streamed response bounds, checks canonical paths/types/collisions and local/central headers before selecting text. No evidence of target execution or dependency fetching in that helper. This is static evidence about observed operations, not independent packet capture or proof that system isolation existed.

Actual compressed sizes, inventory declarations, selected text hashes and full-read CRCs match. Unread binary CRC/content explicitly remain Unknown. unpacked directory is empty. Worktree remained clean at 5c07c8a9. Declaration totals: runtime 39779164 bytes, model 68292271, comfortably within limits. The Leader reread 715 bytes of already-covered member text, additional review cost well within stage1 bounds and not included in developer's 715-byte execution tally.

No outer LICENSE/NOTICE exists in either inventory; the POM/catalog Apache-2.0 statements do not close redistribution obligations. Runtime contains classes.jar, Manifest and four named ABI directories with libvosk.so; filename is not verified ABI. Model configuration declares 16000Hz and README contains benchmark CER values, neither is target-device validation. JNA5.18.1/.module, nested code, native capabilities, complete license/provenance, privacy/PCM and all CP2 performance/user gates remain unverified. Local SHA is not independent publisher authentication; same-response MD5/SHA1 headers were preserved but are not signatures.

This evidence supports basic_inventory_complete only. adoption_gate remains blocked, CP2 not passed, no installation/build/loading/inference/integration/device permission. No universal scanner or 16-hour adapter was created. The small task-local helper and policy test claims are not certification of all failure paths; no retry/redirect occurred in this run.

Callback/original-final visibility is being reconciled separately; do not fake an ACK from the presence of files. One receipt-only follow-up was sent, with no repeat acquisition permitted.
