import json,hashlib,stat,subprocess,ast,tempfile,shutil
from pathlib import Path
repo=Path('/Users/orderly_ray/Projects/think'); root=repo/'tools/asr_review_acquisition_v7'; commit='443bbb5dc73e52dc11610ba766fdda23a0923b80'; parent='534e416b989698589bfb511332b3b0af2de4f185'; pref='tools/asr_review_acquisition_v7/'
def git(*a):return subprocess.check_output(['git',*a],cwd=repo)
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return (json.dumps(x,sort_keys=True,ensure_ascii=True,separators=(',',':'),allow_nan=False)+'\n').encode()
def tree(ref):
 out={}
 for row in git('ls-tree','-r','-z',ref,'--',pref).split(b'\0'):
  if row:
   meta,p=row.decode().split('\t');mode,typ,blob=meta.split();assert mode=='100644' and typ=='blob';out[p[len(pref):]]=(mode,blob)
 return out
assert git('rev-parse','HEAD').decode().strip()==commit and git('rev-parse','HEAD^').decode().strip()==parent and not git('status','--porcelain')
changed=git('diff','--name-status',parent,commit).decode().splitlines(); assert all(x.split('\t')[1].startswith(pref) and x[0] in ('A','M') for x in changed)
assert sum(x[0]=='M' for x in changed)==9 and sum(x[0]=='A' for x in changed)==25462
assert not git('diff','--check',parent,commit)
new,old=tree(commit),tree(parent);assert len(new)==41400
for n,meta in old.items():
 if n.startswith('evidence/'):assert new[n]==meta
m=json.loads((root/'evidence/r1/file-manifest.json').read_bytes());assert len(m['files'])==41399 and sha(canon(m['files']))==m['collection_sha256']=='878e2d4d7d007e700b4d75684ec0dcb19e359e11f1d148b048edd865c7caa847'
assert {x['path'] for x in m['files']}==set(new)-{'evidence/r1/file-manifest.json'}
actual={}
for name,(mode,blob) in sorted(new.items()):
 p=root/name; st=p.lstat();assert stat.S_ISREG(st.st_mode) and st.st_nlink==1
 for d in p.parents:
  if d==repo:break
  assert not d.is_symlink()
 b=p.read_bytes();assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==blob
 actual[name]={'path':name,'bytes':len(b),'sha256':sha(b),'git_blob':blob,'git_mode':mode,'file_type':'regular','nlink':1}
for x in m['files']:assert x==actual[x['path']],x['path']
scan=json.loads((root/'evidence/r1/scan-inputs.json').read_bytes());assert len(scan['files'])==25482 and sha(canon(scan['files']))==scan['collection_sha256']
for x in scan['files']:assert x=={k:actual[x['path']][k] for k in ['path','bytes','sha256']}
raw=json.loads((root/'evidence/r1/static-raw.json').read_bytes());ctx=json.loads((root/'evidence/r1/static-context.json').read_bytes());assert sha((root/'evidence/r1/static-raw.json').read_bytes())==ctx['raw_report_sha256'];assert raw['verdict']==ctx['raw_verdict']=='sandbox_only'
assert len(raw['findings'])==len(ctx['reviewed_findings'])==751
for a,b in zip(raw['findings'],ctx['reviewed_findings']):
 assert a==b['finding'];p=root/a['path'];v=p.read_bytes();line=v.decode().splitlines()[a['line']-1]
 assert sha(v)==b['file_sha256'] and sha(line.encode())==b['line_sha256']
modules=sorted([*root.glob('offline_review/*.py'),*root.glob('tests/*.py'),*[root/n for n in ['audit.py','verify.py','network_guard.py','recalculate.py','SCHEMA.md']]])
bundle=[{'path':p.relative_to(root).as_posix(),'sha256':sha(p.read_bytes())} for p in modules];assert len(bundle)==25 and sha(canon(bundle))=='198c24c66a3e82117828e9eacfa333b4dde8eb19949c7425b8a81b839399553e'
for f,h in [('doc/cp2-manual-capability-evidence-decision-2026-09-06.md','071febe2c7f3c896c48877b4ffd90e1bd3083571e9e6fad8524943e7d7023972'),('doc/prd-v0.1-2026-09-04.md','5c376c961c9ecafd21cb5492254a1c45c7adf422e2a890c1d1181a3871f386a6')]:assert sha((repo/f).read_bytes())==h
work=Path(tempfile.mkdtemp(prefix='think-leader-v7r1-',dir='/private/tmp'))
for name in new:
 if not name.startswith('evidence/'):
  dest=work/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(root/name,dest)
(work/'evidence').mkdir();assert all(sha((work/x['path']).read_bytes())==x['sha256'] for x in bundle)
report={'RESULT':'PASS','commit':commit,'parent':parent,'tree':git('rev-parse',commit+':tools/asr_review_acquisition_v7').decode().strip(),'files_verified':41400,'modified_files':[x.split('\t')[1] for x in changed if x[0]=='M'],'new_files':25462,'manifest_sha256':actual['evidence/r1/file-manifest.json']['sha256'],'collection_sha256':m['collection_sha256'],'old_evidence_unchanged':sum(x.startswith('evidence/') for x in old),'old_evidence_method':'opaque exact-byte Git blob verification; no old scanner context decoded','bundle_sha256':sha(canon(bundle)),'scan_inputs_verified':25482,'raw_scan_verdict':raw['verdict'],'scan_contexts_rehashed':751,'worktree_clean':True,'isolated_first_party_copy':str(work),'scope':'Identity, code-only copy, provenance boundary and new scan contexts; runtime and semantic verdict separate.'}
p=Path('/Users/orderly_ray/Leader/orchestration/reports/CP2-ASR-MANUAL-CAPABILITY-EVIDENCE-INTAKE-OFFLINE-001-R1-identity.json');p.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report))
