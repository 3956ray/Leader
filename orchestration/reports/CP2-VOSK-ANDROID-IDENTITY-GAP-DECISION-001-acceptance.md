# Metadata scope decision acceptance

RESULT: ACCEPTED

Leader read the full formal decision and checked consistency with PRD, INDEX and LOG. Independently recomputed all four reported hashes and byte lengths:

- Decision: 13299 bytes, e4cb90e2184db26dd5021c4acae079384f585a89f7c616f5b2e25af1a85e4dab
- PRD: 75503 bytes, e17fd24fbd1d9b2ca57ee74bca305a1b88280d540f312642625cce0b9e743651
- INDEX: 13858 bytes, 3290952fe7e139e8b5c9809a785a651ded3c83e304242681497da6ff174204ee
- LOG: 54027 bytes, f8d894c3f9ad8c7d1d8a2edcf827af308573d71461fc45bcf4ce5a99ba710d1e

APPROVED only defines one official Central metadata batch: ten attempts, one fixed Android coordinate, at most one parent POM, 1 MiB per response, 5 MiB aggregate and 30 seconds each. Official source establishment is included to avoid circular prerequisites; validated-layout URL derivation is permitted, guessing is not. POM XML must not resolve external entities or execute builds. Artifact GET/HEAD/Range, model research and second versions are excluded. Success concerns metadata identity only, never AAR existence/content/security. Old insufficient result and budgets remain historical.

Decision addresses the precise scope blocker without changing privacy, CP1 recovery, 90 percent vocabulary or CP2/CP3/Alpha gates. Product repo independently clean at 92e50278. PM reports local links/metadata/log-prefix checks; full knowledge lint unavailable, no runtime tests appropriate. Formal knowledge files remain uncommitted; unrelated modifications are not attributed to this task.

Next task is PM-only public metadata research against the authoritative knowledge decision. Product documentation sync is deferred until before any subsequent developer work; no product development is authorized by this research dispatch.
