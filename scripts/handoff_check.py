#!/usr/bin/env python3
"""Read-only portable handoff integrity check; never dispatches or accepts work."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
def read(name):
    return json.loads((root / name).read_text(encoding='utf-8'))
def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

manifest = read('handoff/manifest.json')
errors = []
for entry in manifest['files']:
    p = root / entry['path']
    if not p.is_file() or digest(p) != entry['sha256']:
        errors.append('missing/changed: ' + entry['path'])
ledger = read('orchestration/loop-ledger.json')
task = read('orchestration/current-task.json')
state = read('orchestration/state.json')
if ledger['task'] != task or ledger['state'] != state:
    errors.append('ledger and views differ')
body_hash = hashlib.sha256(json.dumps(task['contract_body'], sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest()
if body_hash != task['contract_sha256']:
    errors.append('frozen contract hash differs')
for entry in read('handoff/path-map.json')['source_snapshots']:
    if digest(root / entry['portable_path']) != entry['sha256']:
        errors.append('canonical source differs: ' + entry['portable_path'])
for error in errors:
    print(error)
print('Handoff integrity:', 'FAILED' if errors else 'OK', '| task:', task['task_id'], '| phase:', task['phase'])
print('Historical paths/thread IDs require reconciliation. No dispatch or acceptance performed.')
raise SystemExit(bool(errors))
