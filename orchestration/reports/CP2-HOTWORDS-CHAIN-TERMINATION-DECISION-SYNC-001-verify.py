"""First-party read-only verification of the exact five-document sync."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
R = Path('/Users/orderly_ray/Projects/think')
O = Path('/Users/orderly_ray/Leader/orchestration')
TID = 'CP2-HOTWORDS-CHAIN-TERMINATION-DECISION-SYNC-001'
BASE = '0043d343d4cb30b9c212bcb111c618fb2ca1d6e9'
task = json.loads((O / 'tasks' / (TID + '.json')).read_bytes())
allowed = {'AGENTS.md', 'doc/README.md', 'doc/development-guide-v0.1-2026-09-04.md', 'doc/prd-v0.1-2026-09-04.md', 'doc/cp2-hotwords-chain-termination-route-decision-2026-09-06.md'}
def git(*args):
    return subprocess.check_output(['git', *args], cwd=R)
def tree(rev):
    return {row.split(b'\t', 1)[1].decode(): row.split(b'\t', 1)[0].decode() for row in git('ls-tree', '-r', '-z', rev).split(b'\0') if row}
def ref(path):
    b=path.read_bytes()
    return {'path':str(path),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
head = git('rev-parse', 'HEAD').decode().strip()
assert head != BASE and git('rev-parse', 'HEAD^').decode().strip() == BASE
assert not git('status', '--porcelain')
assert set(git('diff', '--name-only', BASE, head).decode().splitlines()) == allowed
before, after = tree(BASE), tree(head)
assert {k:v for k,v in before.items() if k not in allowed} == {k:v for k,v in after.items() if k not in allowed}
for source in task['formal_sources']:
    b=Path(source['path']).read_bytes()
    assert len(b)==source['bytes'] and hashlib.sha256(b).hexdigest()==source['sha256']
    assert (R/source['destination']).read_bytes()==b
links=[]
for name in ('AGENTS.md','doc/README.md','doc/development-guide-v0.1-2026-09-04.md'):
    p=R/name
    text=p.read_text(encoding='utf-8')
    for url in re.findall(r'\]\(([^)]+)\)',text):
        if '://' in url or url.startswith('#'):
            continue
        q=(p.parent/url.split('#')[0]).resolve()
        assert q.exists(),str(q)
        links.append(str(q))
    assert 'CP2-ALTERNATIVE-OFFLINE-CHINESE-ASR-OFFICIAL-RESEARCH-001' in text
    assert 'cp2-hotwords-chain-termination-route-decision-2026-09-06.md' in text
subprocess.run(['git','diff','--check',BASE,head],cwd=R,check=True)
report={'task_id':TID,'RESULT':'PASS','commit':head,'parent':BASE,'tree':git('rev-parse','HEAD^{tree}').decode().strip(),'old_leaf_records':len(before),'unchanged_outside_allowed':len({k:v for k,v in before.items() if k not in allowed}),'allowed_files':[dict(ref(R/n),git_record=after[n]) for n in sorted(allowed)],'formal_copies_exact':True,'navigation_links_checked':len(links),'clean':True,'code_or_old_evidence_changes':False}
out=O/'reports'/(TID+'-verification.json')
with out.open('x',encoding='utf-8') as f:
    json.dump(report,f,ensure_ascii=False,indent=2)
    f.write('\n')
print(json.dumps(report,ensure_ascii=False))
