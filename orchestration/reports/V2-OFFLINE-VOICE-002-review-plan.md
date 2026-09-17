# V2-OFFLINE-VOICE-002 review plan

Baseline23ede0961ff83e5637493d7eb5f6c5ecf6b84f59 is reviewed partial, not accepted CP2. ACK confirms contract and unchanged fixture identities. Candidate is a single Sherpa-ONNX + SenseVoice2024-07-17 int8 route, runtime version to pin before execution.

Review exact model/tokens/runtime dependencies, source/license/digests and arm64/16KB compatibility. Reject inherited old-project approval. Official Android examples establish a candidate lead, not project permission or successful integration. No upstream audio fixtures or cloud path.

For non-streaming adaptation, examine bounded sample/float/tensor lifetime, cancellation and native decoding return behavior,90-second input and release-to-complete-result timing. If segmenting, preserve speech across boundaries without dropped/repeated text; any new buffering or chunk policy needs tests. Silence must not become hallucinated formal notes. No auto-save, existing session/revision/cursor/manual ownership safeguards remain.

Freeze decoding settings before the original30-case accuracy run. Verify same fixture SHA, voice/rate and per-clip PCM identity; assess all66 proper-name occurrences and meaningful semantic preservation rather than anchors alone. No hotword answers or corrected-output substitution. Any regenerated PCM mismatch must be explained rather than silently called equivalent.

Quality failure ends that candidate experiment with exact partial evidence; quality success proceeds to10x30sec P95<=5sec,20x90sec plus UI/privacy/regression and exact final identities. Record model/package size, load time, memory, emulator limitations. Keep Xiaomi/family and full-feature backup obligations explicit. No second route or next checkpoint without commander dispatch.

Quality review: all30 outputs read; raw proper names61/66 exceed90%, but at least5 clips misidentify a named person, so strict usability cannot reach27/30. Long performance test stopped per contract. Exactly29 PCM hashes match001; CN14 differs (old166172 versus new83086 samples) despite reported same generator identity. Do not attribute cause without evidence;61/66 describes this run, not an entirely identical30-PCM comparison. Private embedding remains independently PAUSE. Await final assessment/commit/evidence archive.
