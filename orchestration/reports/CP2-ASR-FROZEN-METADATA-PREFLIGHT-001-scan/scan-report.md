# Untrusted Code Static Scan

- Target: `/private/tmp/think-frozen-metadata-preflight-_6wsajyf`
- Verdict: **manual_review**
- Risk score: **32/100**
- Highest severity: **medium**
- Verdict basis: contextual or medium-severity indicators require human review

A low finding count means only that configured rules found no high-risk indicator. It is not a safety guarantee.

## Summary

| Severity | Count |
|---|---:|
| critical | 0 |
| high | 0 |
| medium | 4 |
| low | 0 |
| info | 0 |

## Findings

| Severity | Confidence | Context | Reachable | Rule | Path | Line | Evidence | Rationale |
|---|---|---|---|---|---|---:|---|---|
| medium | Confirmed | source_code | no | IOC-DAAM-PORT-8085 | `commit.json` | 32 | "payload": "tree fd2c4e97c9f7499b6ed91c7c2854b4211f61bdc0\nparent 6fe2cdeb2df6b43817bc49c36e3a1263c25af096\nauthor Fangjun Kuang <csukuangfj@gmail.com> 1788238085 +0800\ncommitter GitHub <noreply@github.com> 1788238085 +0800\n\nRelease v1.1... | Observed external data-channel port; require contextual review. |
| medium | Confirmed | source_code | no | IOC-DAAM-PORT-8085 | `tree.json` | 13813 | "sha": "e0a2ac883917acb75e8085f3d3791cefe5c8c49f", | Observed external data-channel port; require contextual review. |
| medium | Confirmed | source_code | no | IOC-DAAM-PORT-8086 | `tree.json` | 18907 | "sha": "362edc3c87ed585a051f2c4faab9bf4da8c80863", | Observed external auxiliary-channel port; require contextual review. |
| medium | Confirmed | source_code | no | IOC-DAAM-PORT-8087 | `tree.json` | 57834 | "sha": "2d16a19e9e05dbc808742e57ac7ef7d7009a9dc2", | Observed external worker-channel port; require contextual review. |

## Context summary

```json
{
  "source_code": 4
}
```

## Score breakdown

```json
[
  {
    "rule_id": "IOC-DAAM-PORT-8085",
    "path": "commit.json",
    "severity": "medium",
    "source_kind": "source_code",
    "points": 8
  },
  {
    "rule_id": "IOC-DAAM-PORT-8085",
    "path": "tree.json",
    "severity": "medium",
    "source_kind": "source_code",
    "points": 8
  },
  {
    "rule_id": "IOC-DAAM-PORT-8086",
    "path": "tree.json",
    "severity": "medium",
    "source_kind": "source_code",
    "points": 8
  },
  {
    "rule_id": "IOC-DAAM-PORT-8087",
    "path": "tree.json",
    "severity": "medium",
    "source_kind": "source_code",
    "points": 8
  }
]
```

## Scan statistics

```json
{
  "candidates": 2,
  "text_files": 2,
  "binary_files": 0,
  "skipped_large": 0,
  "skipped_limit": 0,
  "unreadable": 0,
  "archives": 0
}
```

## Limitations

- Static inspection cannot prove that an artifact is safe.
- Runtime-fetched, encrypted, obfuscated, oversized, or generated payloads may not be visible.
- A network/upload capability does not prove successful data transfer.
- Repository reputation and dependency vulnerability lookups are outside the offline V1.1 scan.
- Binary metadata, code-signing, and package provenance checks are reserved for a later macOS/Python extension.
