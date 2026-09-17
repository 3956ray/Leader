import json,hashlib,stat,subprocess,tempfile,shutil,ast
from pathlib import Path
repo=Path('/Users/orderly_ray/Projects/think');root=repo/'tools/asr_review_acquisition_v8';commit='1fe85740a185a63ca4f35df2abd22ae410f82fbb';parent='4e853863e1bf0a68fbf8061767803797947eeec2';pref='tools/asr_review_acquisition_v8/'
def git(*a):return subprocess.check_output(['git',*a],cwd=repo)
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return (json.dumps(x,sort_keys=True,ensure_ascii=True,separators=(',',':'),allow_nan=False)+'\n').encode()
assert git('rev-parse','HEAD').decode().strip()==commit and git('rev-parse','HEAD^').decode().strip()==parent and not git('status','--porcelain')
changes=git('diff','--name-status',parent,commit).decode().splitlines();assert len(changes)==69497 and all(x.startswith('A\t'+pref) for x in changes)
assert not git('diff','--check',parent,commit,'--','.',':!'+pref+'v7-to-v8.diff')
check=subprocess.run(['git','diff','--check',parent,commit],cwd=repo,capture_output=True,text=True);lines=check.stdout.splitlines();assert len(lines)==64 and all('trailing whitespace.' in x and pref+'v7-to-v8.diff:' in x for x in lines[::2]) and all(x=='+ ' for x in lines[1::2]),lines[:4]
tree={}
for row in git('ls-tree','-r','-z',commit,'--',pref).split(b'\0'):
 if row:
  meta,p=row.decode().split('\t');mode,typ,blob=meta.split();assert mode=='100644' and typ=='blob';tree[p[len(pref):]]=(mode,blob)
m=json.loads((root/'evidence/file-manifest.json').read_bytes());assert len(m['files'])==69496 and sha(canon(m['files']))==m['collection_sha256']=='209f2db082868de5060595009e14d111927452bd2aa86c9354115176b74aa352'
assert {x['path'] for x in m['files']}==set(tree)-{'evidence/file-manifest.json'}
actual={}
for name,(mode,blob) in sorted(tree.items()):
 p=root/name;st=p.lstat();assert stat.S_ISREG(st.st_mode) and st.st_nlink==1
 for d in p.parents:
  if d==repo:break
  assert not d.is_symlink()
 b=p.read_bytes();assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==blob
 actual[name]={'path':name,'bytes':len(b),'sha256':sha(b),'git_blob':blob,'git_mode':mode,'file_type':'regular','nlink':1}
for x in m['files']:assert x==actual[x['path']],x['path']
scan=json.loads((root/'evidence/scan-inputs.json').read_bytes());assert len(scan['files'])==69488 and sha(canon(scan['files']))==scan['collection_sha256']=='cc6626ea370fb81120b08c15cc2b95cb5466c619dee2907889329669a19a3a83'
for x in scan['files']:assert x=={k:actual[x['path']][k] for k in ['path','bytes','sha256']}
raw=json.loads((root/'evidence/static-raw.json').read_bytes());ctx=json.loads((root/'evidence/static-context.json').read_bytes());assert sha((root/'evidence/static-raw.json').read_bytes())=='2a508b79971c099452666055acc25c509956d4546a60d8bfe72980c23fa8fd6f';assert raw['verdict']==ctx['raw_verdict']=='sandbox_only';assert len(raw['findings'])==len(ctx['findings'])==2564
cache={}
for a,b in zip(raw['findings'],ctx['findings']):
 assert a==b['finding'];name=a['path'];assert actual[name]['sha256']==b['file_sha256']
 if name not in cache:cache[name]=(root/name).read_text().splitlines()
 assert sha(cache[name][a['line']-1].encode())==b['line_sha256']
modules=sorted([*root.glob('offline_review/*.py'),*root.glob('tests/*.py'),*[root/n for n in ['audit.py','verify.py','network_guard.py','recalculate.py','SCHEMA.md']]])
bundle=[{'path':p.relative_to(root).as_posix(),'sha256':sha(p.read_bytes())} for p in modules];assert len(bundle)==28 and sha(canon(bundle))=='9bd39cec857137703c205b92b755eca200c58a2345d197a1ce853825cd1fe1bf'
assert git('rev-parse',commit+':tools/asr_review_acquisition_v7').decode().strip()=='2797686abaf25028545e7a9d764b8a827e207560'
work=Path(tempfile.mkdtemp(prefix='think-leader-v8-',dir='/private/tmp'))
for name in tree:
 if not name.startswith('evidence/'):
  dest=work/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(root/name,dest)
(work/'evidence').mkdir();assert all(sha((work/x['path']).read_bytes())==x['sha256'] for x in bundle)
report={'RESULT':'PASS','commit':commit,'parent':parent,'tree':git('rev-parse',commit+':tools/asr_review_acquisition_v8').decode().strip(),'file_count':len(tree),'manifest_sha256':actual['evidence/file-manifest.json']['sha256'],'manifest_collection':m['collection_sha256'],'bundle_sha256':sha(canon(bundle)),'bundle_files':len(bundle),'scan_inputs_verified':len(scan['files']),'scan_contexts_rehashed':2564,'original_scan_verdict':raw['verdict'],'old_v7_tree_unchanged':True,'only_new_v8':True,'worktree_clean':True,'whitespace':'all non-diff files pass;32 standard unified-diff single-space context lines verified separately','isolated_first_party_copy':str(work)}
p=Path('/Users/orderly_ray/Leader/orchestration/reports/CP2-ASR-REVIEW-TIMESTAMP-REPRESENTATION-OFFLINE-001-identity.json');p.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
