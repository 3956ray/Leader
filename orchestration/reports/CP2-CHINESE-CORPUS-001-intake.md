# Public Mandarin corpus intake

User instruction, 2026-09-09: 可以 你可以先去搜索公开的 中文数据家来进行测试 然后继续工作

Leader interprets this as selecting public Chinese speech data for engineering tests and continuing authorized preparation. It does not silently approve an unreviewed ASR native runtime or the separately proposed JNA binary. Public licensed source recordings need an explicit product-document distinction from private user microphone recordings; no private recording rule is relaxed.

Official pages directly read using the browser (Firecrawl previously returned 402):

- https://www.openslr.org/33/ AISHELL-1: Apache License v2.0 field, Mandarin, 400 speakers from different accent areas, quiet indoor high-fidelity recording downsampled to 16kHz, manual transcription accuracy stated above95%. Download data_aishell.tgz 15G includes speech/transcripts; resource_aishell.tgz 1.2M includes lexicon/speaker info. Description says free for academic use; do not silently turn that phrase into an academic-only restriction or disregard license text. Small separately hosted official test download not shown on this page.
- https://www.openslr.org/18/ THCHS-30: Tsinghua CSLT Chinese corpus, Apache License v2.0 field; data_thchs30.tgz6.4G speech/transcripts; test-noise.tgz1.9G standard0dB noise test; resource.tgz24M supplementary resources. Description says free to academic users. Original README linked at http://data.cslt.org/thchs30/README.html. Small clean-test-only artifact not shown here.

These are source-page statements, not downloaded-file verification. No audio downloaded, no benchmark executed. Read speech is not evidence of father accent accuracy; do not substitute for CP2 personal-name/real-device gates. Vosk model could have used public corpora: training overlap must be declared Unknown unless official evidence resolves it; benchmark is regression baseline, not guaranteed unseen generalization.

Recommended engineering evaluation: deterministic small official test split, fixed utterance IDs and hashes, untouched reference text plus explicit normalization, character error rate=(S+D+I)/N aggregated by characters, sample failures not hidden; 30/90-second stability measured separately, no fake ASR score presented as recognition. Acquisition scope should avoid multi-GB training downloads and unverified third-party repacks.
