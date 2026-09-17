# Voice controls / CP2 — undispatched review draft

Source: approved emulator-first-full-engineering-addendum-2026-09-16.md, paragraph following V7. Current sole developer task remains offline dictation. This document grants no execution or later checkpoint acceptance.

## Goal

Explicit local command mode for new note, save current draft and cancel current voice input. The user must deliberately enter command mode; normal dictation text cannot invoke actions.

## Review boundaries

- Command recognition uses the admitted real local runtime, with audio only in bounded memory. No arbitrary commands, scripting, network calls or expanded navigation.
- Unknown/ambiguous recognitions perform no action. Do not use loose substring matching that turns quoted or negated phrases into commands.
- Saving requires nonempty current draft and explicit confirmation. Bind confirmation to note/session/revision so changed content requires a new decision.
- Cancel stops only the current input and preserves prior text and saved notes. Late callbacks cannot execute cancelled commands.
- New-note action must preserve an existing draft under normal persistence behavior; interruption/error never discards existing edits.
- Leaving command mode, backgrounding, permission loss and cancellation release audio resources and invalidate pending actions.
- Provide accessible visible mode state and action confirmation; dictation and command mode must be distinguishable on screen.

## Evidence

Tests and emulator flows cover ordinary dictation containing command words, quoted/negated/unknown phrases, explicit mode entry/exit, nonempty-save confirmation and rejection, edits while confirmation pending, cancellation and delayed recognition. Verify database content before/after, not only UI text. Include actual local-engine recognized commands, raw results and failures; mocked recognition only proves action routing. Microphone/OEM/father pronunciation and accidental activation remain later physical evidence.

Freeze baseline and contract only after commander closes the current single task. Dictation accuracy failure remains an explicit unresolved product requirement, even if command routing can progress independently under the approved partial-work rule.
