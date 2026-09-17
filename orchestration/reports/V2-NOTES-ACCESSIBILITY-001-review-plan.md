# Note accessibility review plan — task sent, acceptance pending

Task288f5fe5-ba80-4381-be49-c7abf3c328c7 / contractbcc6df204fefd1d191a7be21cc097af4a59b43b1b967ffb6c8c6cc0c4678427f; baseline29482c49d17fc9c6470c0ea964419288b8931f67. Live developer turn01a0aa9a-462a-76e0-bdc1-eac005e98003 confirmed running. Await explicit ACK; no duplicate dispatch.

Evidence audit:
1. Enumerate actual home/search/editor/category-picker/category-management/trash/related-list and confirmations. Matrix identifies font1.0/1.5/2.0, light/dark, logicalwidth/rotation/IME state, expected action and actual result; no blanket pass from a single screen.
2. Inspect before/after PNGs at original resolution plus platform bounds/roles/actions. Scrollability is acceptable; offscreen essential actions must be reachable, not merely exist in Compose tree. Check2.0font narrow screen and keyboard visibly covering editor.
3. Stable-ID tests for same-title records remain independent of visualUUID. Helpful title/excerpt/context must distinguish records; avoid moving UUID clutter into spoken labels. No fake content.
4. Focus tests distinguish keyboard input focus, accessibility focus and actualTalkBack service. Dialog cancellation/confirmation returns to useful focus; menu/back/keyboard/rotation preserve draft and manual ownership. Do not install a service without its gate.
5. Durable DB before/after verifies ordinary note/category/trash/restore/relationship workflows and affected voice/AI entry semantics; no schema/data/consent/navigation-scope change.
6. Final immutable commit/APKs/test-source and screenshot mapping, raw meaningfultests, lint/build, known gaps. Prior screenshots and failures retained only diagnostically. No fullApp acceptance.

Remaining goal beyond task: generalASRquality threshold failure; realAIprovider missing; Xiaomi15 feature-specific tests, natural reminders and family use. UI task must not absorb or erase these items. Artifact/actual runtime evidence needed, not only chat summaries.

## Observed baseline screenshot
Independently viewed before/home-font2-narrow.png: heading and category-management label wrap across lines; feature controls fill visible viewport, no note list visible. Screenshot alone cannot establish list is unreachable; sent current-task feedback to verify actual populated list scroll/open at2.0font/narrowwidth and inspect fixedheader vs weightedLazyColumn height. Do not lower font or hide existing routes. Before environment fingerprint Android17 emulator37.1; installed-service dump does not itself prove usableTalkBack, keep actualservice test distinct.

## Developer probe update
Six matrix combinations0/6 formallypassed;1.0light narrow is full-flow probe. Developer reports exactID, IME, rotation/background and durable draft checks passed in probe, but actual save-button platform bound32dp despite visual56dp due scroll child overlapping/clipping fixed topbar. Product clipping/z-order fix in progress; verify final platform clickable bounds and actual action, not layout-size alone. Failure evidence retained.

Developer reports preinstalledTalkBack discovered, bounded realservice gesture test planned without download. Earlier service dump alone was insufficient; final evidence must identify active service and gesture/focus results separately fromUiAutomation. No Leader intervention/authorization blocker reported; current task continues, no scope change.

## Interim six-group logs and screenshot finding
All6matrix instrumentation logs currently reportOK(1test), not yet finalAPK acceptance. Viewed2.0light home-real-list and editor-ime: populated list reachable and meaningful same-title excerpts visible. EditorIME screenshot has primary SAVE rendered as two vertical characters and tall wrapped topbar. Requested bounded adaptive primary-action layout correction without font reduction/behavior changes, followed by affected font/orientation/IME and durable back/save recheck. Passing bounds/assertions alone do not settle actual readability. Await updatedfinal evidence.

## Developer response to rendered finding
SAVE receives sufficient width instead of weighted half allocation; visible return label shortened with retained draft-preservation accessibility label. Verify2.0narrow final screenshot and confirmation of unchangedback behavior. Six prior operation/DB runs passed, but some screenshot transition frames not final visual proof; wait for stable captures.

Separate focus problem: merged action semantics omit full keyboard-focus exposure in platformnode; developer fixing. ActualTalkBack greenfocus observed, firstswipe injection failed; no realservice navigation pass yet. Planned officialkeyboard route must be reported specifically as keyboard navigation, not proof of touchgesture success or audible speech quality. Retain failedgesture evidence. No task expansion.

## Bounded TalkBack attempt closed, explicit gap
Developer reports installedTalkBack17 binding/touchexploration/greenfocus present; injected swipes and officialkeyboard combinations did not reliably movefocus with and withoutUiAutomation. Hardware-event boundedprobe also failed to establish appnavigation. Restored priorservice settings, no continuedservice research. Do not infer productbug or service pass from inconclusive injection. ActualTalkBack navigation/dialogreadscreen focusreturn unverified, retains targetdevice gap.

Remaining independent review: final save-horizontal layout and platformkeyboardfocus results; distinguish actual inputfocus/navigation from accessibility ACTION_FOCUS. Dialogfocusreturn acceptance needs direct evidence or explicitly partial outcome; don't waive scope solely because business-route tests pass. Overall CP3 acceptance undecided until final artifact.

## Independent keyboard failure inspection
Read keyboard-final/instrumentation.log plus two preceding attempts: RequestFocus missing/false initially, then request returns but 신규/NewNote node Focused=false, testfails before actualTab/dialogreturn. This is unresolved currenttest evidence, not solely aTalkBack injection gap. Sent bounded diagnosis suggestion: samewindow unwrappedMaterial3Button control, realFocusState/inputmode/Tab distinguish harness vs wrapper; preserve assertions, no fabricatedFocused semantics. Final acceptance requires genuine keyboard evidence or explicit unresolved scope, not reinterpretation of this failure.

## Focus diagnosis update from developer (await raw final evidence)
PriorTab skippednewbutton; helper now explicitly grants canFocus from enabled and exposes realonFocusChanged state, RequestFocus returns actualBoolean. Developer reports actualTab now focusesNewNote thenSearch, precedingassertions retained. Remaining platformroot.findFocus(INPUT) returns nonfocusedrootView; planned enumeration of realvirtual nodes must assert focused on correct app/control and retain originalroot result. This is acceptable evidence-method refinement only if actualTab and true nodefocused still asserted; no forcedsemanticfocused. Dialogclose return still pending. Avoid repeated control experiments once diagnosis is supported.

## Developer final-focus pass reported
RequestFocus actualtrue, NewNote focusedtrue; realTab then search Compose+platformEditText focusedtrue; discard-dialog cancel openerFocusedAfterDismiss=true, originalkeyboardfocus restored and body unchanged. Await rawJSON/log and finalsource identities for independent verification; no forcedfocused/deletedassertions claimed. Finaltopbar+focus version reruns6matrices with dedicatedtest systemanimations disabled for stable captures; originaltransitionframes archiveddiagnostic. Record animation setting/restoration as testenvironment, not new productbehavior. TalkBacknavigation gap unchanged.

## Rendered primary-action fix confirmed provisionally
Updated2.0-light/editor-ime PNG visually shows完整horizontal返回/保存. Gboard temporaryKeyboard font size updated panel obscures lowerbody; not itself aproductbug. Requested supplementalnormalIME screenshot after dismissing systemprompt, samefont/width and actualeditable scrolling. No fullmatrixrerun for onecapture. Bind latestshots to finalartifact before finalacceptance.

### Interim regression evidence inspection
- Current developer turn 01a0aa9a-462a-76e0-bdc1-eac005e98003 independently polled active/inProgress; no final result yet, HEAD remains29482c49. leader_check passed.
- Read every raw log referenced by regression-summary.json: 20 Android tests report OK. Separately inspected voice-regression/command.log (VoiceCommandEngineTest) and ordinary.log (VoiceUiTest): one passing test each. This confirms raw log outcomes only; final APK/commit binding and full acceptance remain pending.
- New uncommitted NotesImeTest and verification report present; normal-keyboard supplementary visual evidence still to inspect in final package. No acceptance or new dispatch.

### Normal IME supplemental evidence review
- Viewed normal-ime after-banner-dismiss and body-scrolled PNGs, read NotesImeTest and result. Normal Gboard is visible; save/back horizontal. body-scrolled displays automatic title/top status, not later body. swipeDown followed by hardcoded longChineseBodyScrolled=true does not prove long-body end reachable; performTextInput and exact SQLite prove persistence only.
- Sent bounded same-task feedback: show actual later/end body and visible caret above IME with visibility/position assertions plus durable edit. Fix minimally only if real product defect; otherwise correct probe direction and supplement only this case. Acceptance pending, no new checkpoint.

### Corrected normal IME evidence inspected
- Read updated NotesImeTest, raw OK(1) log and result JSON; viewed visible-end-after-edit PNG. At font2/320dp, field bottom899 < IME top983; screenshot shows final appended Chinese text and caret handle above normal keyboard, save/back visible. Actual touch selects text end287 before and297 after append; exact draft SQL asserted after back. Scroll uses actual Compose ScrollBy action, not physical swipe or keyboard typing; claim limited accordingly.
- Prior wrong-direction diagnostic remains excluded. This closes the identified missing visible-end example at tested configuration; final artifact/version binding remains pending. Developer reports final NotesUiTest binding and archival next, no confirmed product defect or Leader blocker.
