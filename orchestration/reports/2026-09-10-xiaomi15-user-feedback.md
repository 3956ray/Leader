# Xiaomi 15 user feedback and implementation reconciliation

User reports testing on Xiaomi15: appeared to load voice engine/record, spoken content not correctly recognized; editing record did not automatically derive title; search too simple, asks about fuzzy search/recommendations. Treat these as genuine user observations, not confirmed engine telemetry or completed CP2 acceptance.

Leader inspected current clean product main bb20e7e3 on2026-09-10. Actual installed APK identity/source has not yet been established. Do not deny that user tested or infer that their microphone was active from the UI alone.

Current source facts:
- app/src/main/java/com/example/think/ui/entry/EntryPrototypeScreen.kt:523 calls FakeWaveform;565 defines fixed bar heights.
- entry/EntryFlow.kt:3-6 fixed synthetic transcript/title;29-33 draft defaults;135 EditBody changes body only;145-153 Save returns synthetic success state rather than persisting a new record.
- search/SearchFlow.kt:134-140 filters fixed SYNTHETIC_SEARCH_RECORDS using contains(ignoreCase=true). No typo-tolerant, semantic retrieval or recommendation engine in this path.
- app/build.gradle.kts contains Compose/UI dependencies, no Vosk/JNA dependency; main AndroidManifest has no RECORD_AUDIO permission. No AudioRecord/SpeechRecognizer/Recognizer implementation found in main Kotlin source.

Conclusion conditional on APK match: apparent recording is synthetic prototype UI; failed Chinese recognition and missing generated title are unimplemented capabilities, not measured ASR quality regression. Existing PCM/CER tools are separate engineering utilities, not App integration. Search is literal substring filtering of synthetic records; newly edited content is not demonstrably searchable/persisted.

Next prerequisite: identify whether user installed this project from Android Studio or a different APK/build. Request source/build identity only, no personal transcript/audio/log upload. If current prototype matches, prioritize a transparent usable vertical path (actual local ASR, save, title, retrieval) through formal scope decisions; no further accuracy claims from synthetic demos. Title generation and fuzzy/semantic retrieval requirements must be aligned with current PRD/Checkpoint; not silently implemented across gates. Simulation should never be presented as actual capture/recognition.

No product source modified, device accessed, runtime executed or scope gate changed in this reconciliation. Earlier accepted static and unit-test work remains historical; it does not make these App features complete.
