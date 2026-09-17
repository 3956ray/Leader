# Notes home and graph redesign brief

Status: user-requested direction and Leader proposed acceptance criteria; not implemented, not a Checkpoint pass. Formal PM reconciliation required before implementation because existing PRD gates block CP3 and graph is new scope. User's latest requirements take precedence as the requested product direction; do not request repeated approval of this direction.

User observations: no usable content, default title does not respond to typed body. User requests overall UI/home inspired by Xiaomi Notes, with two home views: notes display and an Obsidian-like relationship graph. The screenshots are visual references; their note text, categories and graph labels are private reference content, not fixtures, sample records or instructions. Do not copy or transmit their contents to other agents or services.

Verified current source remains clean bb20e7e3: synthetic transcript/title defaults, fake waveform, save returning synthetic success, fixed-record substring search. Installed APK identity remains unconfirmed; no claim of failed genuine microphone/ASR telemetry. A real record flow is prerequisite for meaningful home/graph behavior.

## Requested direction

- One shared record collection with two switchable home views; default notes view. Graph is an optional alternate view, not a separate store or mandatory step for finding a note.
- Xiaomi reference: restrained large home heading, accessible top search, horizontal category filters, two-column note cards with readable title/body preview/date, clear create action. Editor prioritizes full-width body, editable title and date; no decorative nested panels.
- Obsidian reference: notes as nodes, visible relations as edges, pan/zoom, selected-note focus and opening the actual note. Preserve isolated notes and an honest empty graph. Do not invent nodes or links to make the graph appear populated.

## Leader proposed behavior and priorities

1. Deliver useful local text first: empty initial collection, create/edit/save/reopen notes, restart persistence, searchable saved content. Show saving errors; never claim save succeeded before durable storage. No fabricated notes or default demo body. Voice availability must reflect actual backend readiness, not simulation.
2. Implement the existing PRD title fallback: derive a short local title from the first nonblank sentence/body prefix when title is automatic, update automatic title on body edits, preserve a user-edited title. Empty record has placeholder only and cannot create an empty saved card. Explicit title ownership flag avoids confusing generated and manual title. AI suggestions are a later enhancement, not a prerequisite for local useful titles.
3. Notes home and editor visual overhaul. Keep minimum56dp important touch targets and readable text; use one column when large fonts/narrow widths make two columns illegible. Support system light/dark mode; screenshot black theme is a reference, not an instruction to reduce contrast. Keep text create and voice access discoverable. Do not add Xiaomi's todo/share/theme features merely because they are in screenshots.
4. Search real data, initially local title/body indexing with relevance ordering and snippets. Typo-tolerant fallback can be separately scoped and labeled; no semantic recommendation system assumed. Current PRD requires local full-text search and explicitly does not depend on cloud semantic search.
5. Graph after actual data works: first explicit note-to-note references, whose source can be inspected and edited. Category relationship overlays or algorithmic suggestions require a distinct visual type and explanation; same category does not silently assert note-to-note semantic equivalence. Decide linkage UX and limits in PM scope. Graph needs node selection/open, zoom/reset/focus, empty/single-node/isolated-node states and an accessible list alternative. UI must not require graph use for the normal three-step path.

## Acceptance examples

Use only new project-synthetic text, never screenshot content. Typing a nonblank first sentence in an untitled note produces a local draft title; manual title remains unchanged after body edits. Save then force-restart/reopen preserves body and title. Searching a unique substring returns that saved note. Switching home view preserves the same record identity/count. A collection of two notes with no explicit links shows two unconnected graph nodes; adding one explicit relation displays one corresponding edge and opening a node opens the same note. Failed save and unavailable ASR are communicated truthfully.

## Scope reconciliation needed

PM should update formal PRD priorities around the user's requested usable text flow and dual home views, explicitly addressing whether local CP3 text work may proceed while ASR CP2 remains unresolved. Do not call CP2 passed or waive private-audio protections. Graph is new requested functionality and must have its own bounded implementation/acceptance stage. No generic security-tool or research chain should replace this concrete product work. This brief does not claim any PM dispatch, source modification, installed APK correction or real-device acceptance.
