"""Leader independent read-only F identity/manifest verification; no candidate imports."""
import hashlib,json,os,stat,subprocess
from pathlib import Path
L=Path('/Users/orderly_ray/Leader');Q=Path('/Users/orderly_ray/Projects/think')
T=L/'orchestration/tasks/CP2-ASR-EXECUTION-RELEASE-FREEZE-V8-001.json'
HEAD='75a9349c2e54d18a46dacddad762e7e669e9fbc2'
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(v):return (json.dumps(v,sort_keys=True,ensure_ascii=True,allow_nan=False,separators=(',',':'))+'\n').encode('ascii')
def digest(v):return sha(canon(v))
def git(*a):return subprocess.check_output(['git','-C',str(Q),*a])
def g(*a):return git(*a).decode().strip()
dirs={}
def read(p):
 for parent in p.parents:
  if parent not in dirs:
   s=parent.lstat();assert stat.S_ISDIR(s.st_mode);dirs[parent]=(s.st_dev,s.st_ino,s.st_mode)
 s=p.lstat();assert stat.S_ISREG(s.st_mode) and s.st_nlink==1
 with p.open('rb') as f:
  z=os.fstat(f.fileno());assert (z.st_dev,z.st_ino)==(s.st_dev,s.st_ino);b=f.read();z=os.fstat(f.fileno())
 n=p.lstat()
 for x in (z,n):assert (x.st_dev,x.st_ino,x.st_mode,x.st_size,x.st_nlink,x.st_mtime_ns,x.st_ctime_ns)==(s.st_dev,s.st_ino,s.st_mode,len(b),1,s.st_mtime_ns,s.st_ctime_ns)
 return b
def load(p):return json.loads(read(p))
def record(p,label):
 b=read(p);return dict(path=label,bytes=len(b),sha256=sha(b),git_blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),mode='100644',type='blob')
raw=read(T);assert sha(raw)=='59fb9a077347ac20385b55ae7e237b776c1b2934e5eccee510dc0ceca718ccf1';t=json.loads(raw)
assert g('rev-parse','HEAD')==HEAD and g('rev-parse','HEAD^')==t['baseline_commit'] and not git('status','--porcelain=v1','--untracked-files=all')
out=t['output_directory'];names=['F.json','MANIFEST.json','REPORT.md','freeze.json'];newpaths=[out+'/'+n for n in names]
assert git('diff','--name-status','HEAD^','HEAD').decode().splitlines()==['A\t'+p for p in newpaths]
old=git('ls-tree','-r','-z','HEAD^');new=git('ls-tree','-r','-z','HEAD')
remaining=[r for r in new.split(b'\0') if r and r.split(b'\t',1)[1].decode() not in newpaths]
assert b'\0'.join(remaining)+b'\0'==old and len(remaining)==129523 and sha(old)=='f1d1f3adbead75a4a0e7ef9daeb2b4886edd143de209b6418c41f7b1f7b64198'
entries={}
for r in new.split(b'\0'):
 if r:
  d,p=r.split(b'\t',1);entries[p.decode()]=tuple(d.decode().split())
outputs=[]
for name,p in zip(names,newpaths):
 row=record(Q/p,name);assert entries[p]==(row['mode'],row['type'],row['git_blob']);outputs.append(row)
 if name.endswith('.json'):assert canon(load(Q/p))==read(Q/p)
assert [x['sha256'] for x in outputs]==['c6e59308eb1ae72ce3d42e1c5678656d0f9442a3baaf8e503867368c98a9bad4','a373d657558fd7a8982bf29b737f313420f593793c93d8d3f24504071777f4c4','f8bf98968875ceb93c1b8189cf06b246b1021664100f8663672c53b444c073c4','000d922060e830706c638b3304b79a71cb191fc61a05de24b0a2ebc31319e607']
C=t['accepted_C'];K=t['accepted_K'];F=dict(domain='think-manual-F-v8',version=8,C=C['bundle'],K=K['identities']['K'],policy=C['policy'],intake_schema=C['intake'])
assert canon(F)==read(Q/out/'F.json')
m=load(Q/out/'MANIFEST.json');fr=load(Q/out/'freeze.json')
paths=sorted(p for p in entries if p.startswith(C['root']+'/') or p.startswith(K['root']+'/'))
assert len(paths)==69505 and [r['path'] for r in m['files']]==paths
records=[]
for p in paths:
 r=record(Q/p,p);assert entries[p]==(r['mode'],r['type'],r['git_blob']);records.append(r)
assert records==m['files'] and digest(records)==m['files_collection_sha256']=='83c3d1b4458e773d4eb3a0dd038f22f4554d471a10ca6b55b82f676b3c8db3ba'
refs=sorted(t['pinned_references']+[dict(path=str(T),bytes=len(raw),sha256=sha(raw))],key=lambda r:r['path'])
assert len(refs)==33 and m['external_references']==refs
for r in refs:
 b=read(Path(r['path']));assert len(b)==r['bytes'] and sha(b)==r['sha256']
assert digest(refs)==m['external_references_collection_sha256']=='c001b9df2e3a1a0544d7e691497abbeaf9b2efc87dbe2bc2bea07be32a23a0d7'
for c in (C,K):assert g('rev-parse',HEAD+':'+c['root'])==c['tree']
by={r['path']:r for r in records};bundle=fr['candidate_bundle']['records']
expected_bundle=sorted([dict(path=p[len(C['root'])+1:],sha256=r['sha256']) for p,r in by.items() if p.startswith(C['root']+'/') and ((len(Path(p[len(C['root'])+1:]).parts)==2 and Path(p[len(C['root'])+1:]).parts[0] in ('offline_review','tests') and p.endswith('.py')) or p[len(C['root'])+1:] in ('audit.py','verify.py','network_guard.py','recalculate.py','SCHEMA.md'))],key=lambda r:r['path'])
assert bundle==expected_bundle and len(bundle)==28 and digest(bundle)==C['bundle']
ids=load(Q/C['root']/'evidence/identities.json');contracts=dict(policy=ids['policy'],intake=ids['intake_contract'],semantic=ids['policy']['source_semantics'],role=ids['policy']['content_roles'])
assert fr['contracts']=={k:dict(canonical_object=v,sha256=digest(v)) for k,v in contracts.items()}
assert digest(contracts['policy'])==F['policy'] and digest(contracts['intake'])==F['intake_schema']
assert fr['runtime_F']['canonical_object']==F and fr['runtime_F']['file']['sha256']==digest(F)
assert fr['manifest']['file']['sha256']==outputs[1]['sha256']
for r in fr['acceptances'].values():assert r in refs
assert fr['acceptances']['K']==K['acceptance'] and fr['acceptances']['P_record']['sha256']==K['identities']['P']
assert fr['C']==C and fr['K']=={k:K[k] for k in ('commit','tree','root','identities')}
oldmanifest=load(Q/C['root']/'evidence/file-manifest.json');oldrows=[]
for r in records:
 if r['path'].startswith(C['root']+'/') and r['path']!=C['root']+'/evidence/file-manifest.json':oldrows.append(dict(path=r['path'][len(C['root'])+1:],bytes=r['bytes'],sha256=r['sha256'],git_blob=r['git_blob'],git_mode=r['mode'],file_type='regular',nlink=1))
assert len(oldrows)==69496 and oldrows==oldmanifest['files'] and digest(oldrows)==oldmanifest['collection_sha256']
temp=Path('/private/tmp/think-f-v8-14aswdsm')
assert {r['path'] for r in fr['verification_scripts']}=={str(temp/'produce.py'),str(temp/'verify.py')}
for r in fr['verification_scripts']:
 b=read(Path(r['path']));assert sha(b)==r['sha256'] and len(b)==r['bytes']
assert sha(read(temp/'verify.py'))=='faaa33645961306784d5ed5bf083c62a4a5e2ff2bc03d20da8b92749d7925d00'
for p,identity in dirs.items():
 s=p.lstat();assert (s.st_dev,s.st_ino,s.st_mode)==identity
assert g('rev-parse','HEAD')==HEAD and not git('status','--porcelain=v1','--untracked-files=all')
result=dict(RESULT='PASS',commit=HEAD,parent=t['baseline_commit'],root_tree=g('rev-parse','HEAD^{tree}'),output_tree=g('rev-parse',HEAD+':'+out),files=outputs,worktree_clean=True,product_inputs=len(records),external_refs=len(refs),old_records=len(remaining),old_records_sha256=sha(old),files_collection_sha256=digest(records),external_collection_sha256=digest(refs),C_manifest_rows=len(oldrows),C_bundle_files=len(bundle),F_sha256=digest(F),supporting_freeze_sha256=outputs[3]['sha256'],contracts={k:digest(v) for k,v in contracts.items()},K=F['K'],P=K['identities']['P'],developer_verifier_preflight='Exact reviewed source and permitted derived/script path references verified before separate run',limitations=['All firstparty synthetic/source evidence hashed opaque, no private/original source pointer reads.','No candidate or prior verifier imports/execution; document acceptance only.'])
print(json.dumps(result,sort_keys=True,indent=2))
