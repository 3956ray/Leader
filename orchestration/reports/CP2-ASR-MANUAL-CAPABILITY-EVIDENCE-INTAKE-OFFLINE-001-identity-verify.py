import json,hashlib,stat,subprocess,ast
from pathlib import Path
repo=Path('/Users/orderly_ray/Projects/think'); root=repo/'tools/asr_review_acquisition_v7'; commit='534e416b989698589bfb511332b3b0af2de4f185'; parent='7557ed554025ab7a06ea5f76cc1429915bbbbe06'; pref='tools/asr_review_acquisition_v7/'
def git(*a):return subprocess.check_output(['git',*a],cwd=repo)
def sh(b):return hashlib.sha256(b).hexdigest()
def canon(x):return (json.dumps(x,sort_keys=True,ensure_ascii=True,separators=(',',':'),allow_nan=False)+'\n').encode()
assert git('rev-parse','HEAD').decode().strip()==commit
assert git('rev-parse','HEAD^').decode().strip()==parent
assert not git('status','--porcelain')
changed=git('diff','--name-status',parent,commit).decode().splitlines(); assert len(changed)==15938 and all(x.startswith('A\t'+pref) for x in changed)
tree={}
for row in git('ls-tree','-r','-z',commit,'--',pref).split(b'\0'):
 if not row:continue
 meta,p=row.decode().split('\t');mode,typ,blob=meta.split();assert mode=='100644' and typ=='blob';tree[p[len(pref):]]=(mode,blob)
m=json.loads((root/'evidence/file-manifest.json').read_bytes()); assert len(m['files'])==m['file_count']==15937
assert sh(canon(m['files']))==m['collection_sha256']=='cefef6be345e695cf16906f860b7ea76fbbd8277537365f794cd47b631c918ad'
assert {x['path'] for x in m['files']}==set(tree)-{'evidence/file-manifest.json'}
actual={}
for name,(mode,blob) in sorted(tree.items()):
 p=root/name; st=p.lstat(); assert stat.S_ISREG(st.st_mode) and st.st_nlink==1
 for d in p.parents:
  if d==repo:break
  assert not d.is_symlink()
 b=p.read_bytes(); assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==blob
 actual[name]={'path':name,'bytes':len(b),'sha256':sh(b),'git_blob':blob,'git_mode':mode,'file_type':'regular','nlink':1}
for x in m['files']:assert x==actual[x['path']],x['path']
prov=json.loads((root/'provenance.json').read_bytes()); sources=prov['sources']; assert len(sources)==23
for x in sources:
 b=git('show',prov['source_commit']+':tools/asr_review_acquisition_v6/'+x['path'])
 assert len(b)==x['bytes'] and sh(b)==x['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['source_git_blob']
 assert actual[x['path']]['sha256']==x['candidate_sha256']
 if x['path'].startswith('tests/'): assert b==(root/x['path']).read_bytes()
scan=json.loads((root/'evidence/scan-inputs.json').read_bytes()); assert len(scan['files'])==scan['count']==15929 and sh(canon(scan['files']))==scan['collection_sha256']
for x in scan['files']:assert x=={k:actual[x['path']][k] for k in ['path','bytes','sha256']}
raw=json.loads((root/'evidence/static-raw.json').read_bytes()); ctx=json.loads((root/'evidence/static-context.json').read_bytes()); assert sh((root/'evidence/static-raw.json').read_bytes())==ctx['raw_report_sha256']
assert raw['verdict']==ctx['raw_verdict']=='sandbox_only'; assert len(raw['findings'])==len(ctx['reviewed_findings'])==465
for a,b in zip(raw['findings'],ctx['reviewed_findings']):
 assert a==b['finding']; p=root/a['path']; rawb=p.read_bytes();line=rawb.decode().splitlines()[a['line']-1]
 assert sh(rawb)==b['file_sha256'] and sh(line.encode())==b['line_sha256']
modules=sorted([*root.glob('offline_review/*.py'),*root.glob('tests/*.py'),*[root/n for n in ['audit.py','verify.py','network_guard.py','recalculate.py','SCHEMA.md']]])
bundle=[{'path':p.relative_to(root).as_posix(),'sha256':sh(p.read_bytes())} for p in modules]
assert len(bundle)==25 and sh(canon(bundle))=='fd4c6bffd3597e2ca05ab5518f0a6f6ace008694f4b8655cf4115206d8f2af46'
r={'RESULT':'PASS','commit':commit,'parent':parent,'tree':git('rev-parse',commit+':tools/asr_review_acquisition_v7').decode().strip(),'files_verified':len(actual),'manifest_sha256':actual['evidence/file-manifest.json']['sha256'],'manifest_collection':m['collection_sha256'],'sources_verified':len(sources),'all_original_test_files_unchanged':True,'bundle_sha256':sh(canon(bundle)),'scan_inputs_verified':len(scan['files']),'raw_scan_verdict':raw['verdict'],'scan_finding_contexts_rehashed':465,'worktree_clean':True,'scope':'Identity, provenance and existing first-party scan evidence only; does not assert semantic acceptance or runtime pass.'}
p=Path('/Users/orderly_ray/Leader/orchestration/reports/CP2-ASR-MANUAL-CAPABILITY-EVIDENCE-INTAKE-OFFLINE-001-identity.json');p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print(json.dumps(r))
