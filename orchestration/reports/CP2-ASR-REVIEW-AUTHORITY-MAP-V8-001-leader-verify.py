"""Independent Leader verification of fixed M delivery. No candidate or raw-source access."""
import hashlib,json,stat,subprocess
from pathlib import Path
L=Path('/Users/orderly_ray/Leader');Q=Path('/Users/orderly_ray/Projects/think');TMP=Path('/private/tmp/think-m-v8-5wnagmsa')
ID='CP2-ASR-REVIEW-AUTHORITY-MAP-V8-001';HEAD='6b83f40e75cbb501102207018658f6de15a79ff2'
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(v):return (json.dumps(v,ensure_ascii=True,allow_nan=False,sort_keys=True,separators=(',',':'))+'\n').encode('ascii')
def digest(v):return sha(canon(v))
def git(*a):return subprocess.check_output(['git','-C',str(Q),*a])
def g(*a):return git(*a).decode().strip()
def read(p):
 assert stat.S_ISREG(p.lstat().st_mode) and p.lstat().st_nlink==1
 assert all(stat.S_ISDIR(x.lstat().st_mode) for x in p.parents)
 return p.read_bytes()
def load(p):return json.loads(read(p))
def rec(p,label):
 b=read(p);return dict(path=label,bytes=len(b),sha256=sha(b),git_blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),mode='100644',type='blob')
tb=read(L/'orchestration/tasks'/(ID+'.json'));assert sha(tb)=='3c073c93647d1d02ae442dc244b6072f97f19618e9274d3fb8b52c6aff2defa2';t=json.loads(tb)
assert g('rev-parse','HEAD')==HEAD and g('rev-parse','HEAD^')==t['baseline_commit'] and not git('status','--porcelain=v1','--untracked-files=all')
d=t['output_directory'];out=Q/d;names=sorted(['M.json','PROVENANCE.json','VERIFICATION.json','MANIFEST.json','REPORT.md']);paths=[d+'/'+n for n in names]
assert sorted(x.name for x in out.iterdir())==names
assert git('diff','--name-status','HEAD^','HEAD').decode().splitlines()==['A\t'+p for p in paths]
old=git('ls-tree','-r','-z','HEAD^');new=git('ls-tree','-r','-z','HEAD');retained=[r for r in new.split(b'\0') if r and r.split(b'\t',1)[1].decode() not in paths]
assert b'\0'.join(retained)+b'\0'==old and len(retained)==129527 and sha(old)=='51cd9034f9420d473e24a606c8e75d3269cae02ff89ea943a0fef0f1244425e4'
files=[]
for name,p in zip(names,paths):
 r=rec(Q/p,name);assert g('ls-tree','HEAD','--',p)==f"100644 blob {r['git_blob']}\t{p}";assert git('cat-file','blob',r['git_blob'])==read(Q/p);files.append(r)
 if name.endswith('.json'):assert canon(load(Q/p))==read(Q/p)
assert [r['sha256'] for r in files]==['661615944e4d565dba2e9fd8ad4da759a4cff6dd5654c721360411da6d347ea0','b9a4ef2ec1d75fe532ee53bc7ee7b3569dfef326aae4821641b905720709373a','494dd1adb8bf8a1accd93c68defe11a68b363e9920b3bba7d25bfda6244a2a74','060727f04387a9b731b01d9baf4c417270bc4429912b5d018e24c167191f4655','3a3e349be0de1f3eee13d3c76441c261dbdcb9867a8864818f24be5bf78335e9']
assert len(t['pinned_references'])==27
for row in t['pinned_references']:
 b=read(Path(row['path']));assert len(b)==row['bytes'] and sha(b)==row['sha256']
for key in ('accepted_C','accepted_K','accepted_F'):assert g('rev-parse','HEAD:'+t[key]['root'])==t[key]['tree']
fp=Q/t['accepted_F']['root']/'F.json';kp=Q/t['accepted_K']['root']/'K.json';F=load(fp);K=load(kp);C=t['accepted_C']
assert canon(F)==read(fp) and F==dict(domain='think-manual-F-v8',version=8,C=C['bundle'],K=t['accepted_K']['identities']['K'],policy=C['policy'],intake_schema=C['intake'])
assert digest(F)==t['accepted_F']['runtime_F_sha256'] and digest(K)==F['K'] and K['operational_authority'] is False
M=dict(domain='think-manual-M-v8',version=8,F=digest(F),K=digest(K),**{k:K[k] for k in ('H','R','representation','authority','entries','map_schema')})
assert len(M)==10 and read(out/'M.json')==canon(M)
assert len(M['entries'])==2 and M['entries'][0]['occurrence_id']!=M['entries'][1]['occurrence_id']
assert all(r['decision']=='comment_only_nonoperative_for_this_body' for r in M['entries'])
assert M['F']!=t['accepted_F']['supporting_freeze_sha256']
prov=load(out/'PROVENANCE.json');ver=load(out/'VERIFICATION.json');manifest=load(out/'MANIFEST.json')
assert prov['pinned_references']==ver['pinned_references']==t['pinned_references']
fa=load(Path(t['accepted_F']['acceptance']['path']));ka=load(Path(t['accepted_K']['acceptance']['path']))
assert fa['RESULT']==ka['RESULT']=='ACCEPTED' and fa['runtime_F_sha256']==M['F'] and ka['identities']==t['accepted_K']['identities']
assert prov['acceptances']==ver['acceptances'] and prov['P_record']==ka['P']==ver['P_record']
for row in prov['acceptances'].values():assert row in t['pinned_references'] and load(Path(row['path']))['RESULT']=='ACCEPTED'
def pointer(o,p):
 for s in p.split('/')[1:]:o=o[int(s)] if isinstance(o,list) else o[s]
 return o
def leaves(o,p=''):
 if isinstance(o,dict):return sum((leaves(v,p+'/'+k) for k,v in o.items()),[])
 if isinstance(o,list):return sum((leaves(v,p+'/'+str(i)) for i,v in enumerate(o)),[])
 return [p]
mapping=prov['field_mapping'];assert len(mapping)==13 and sorted(r['target'] for r in mapping)==sorted(leaves(M))
for row in mapping:
 target=row['target'];s=row['source'];value=pointer(M,target)
 if target in ('/domain','/version'):
  assert s==dict(kind='accepted schema constant',locator='domain/version',path=str(Q/C['root']/'offline_review/manual.py'))
  assert value==('think-manual-M-v8' if target=='/domain' else 8)
 elif target in ('/F','/K'):
  p=fp if target=='/F' else kp;assert s==dict(kind='exact byte digest',locator='whole canonical file bytes',path=str(p));assert value==sha(read(p))
 else:
  assert s==dict(kind='JSON pointer',locator=target,path=str(kp));assert canon(value)==canon(pointer(K,target))
 assert row['derivation']
assert all(v is False for v in prov['scope'].values())
assert manifest['files']==[r for r in files if r['path']!='MANIFEST.json'] and digest(manifest['files'])==manifest['collection_sha256']=='fa7f9d1461fefc9d86987a70f7d38fb712f4708530585d0bef3e8d4f6be237cd'
assert {r['path'] for r in ver['scripts']+[ver['independent_script']]}=={str(TMP/n) for n in ['produce.py','verify.py','finish.py']}
for row in ver['scripts']+[ver['independent_script'],ver['core_output'],ver['production_output']]:
 p=Path(row['path']);assert p.parent==TMP;b=read(p);assert len(b)==row['bytes'] and sha(b)==row['sha256']
assert sha(read(TMP/'verify.py'))=='42b779c4665ff6cf1048019f7b45646727f2088fe8afb8d8bfa368e618fab6fc'
assert ver['core_result']==load(TMP/'core-result.json') and ver['production_result']==load(TMP/'production.json')
assert not git('status','--porcelain=v1','--untracked-files=all') and g('rev-parse','HEAD')==HEAD
print(json.dumps(dict(RESULT='PASS',task_id=ID,commit=HEAD,parent=t['baseline_commit'],root_tree=g('rev-parse','HEAD^{tree}'),output_tree=g('rev-parse','HEAD:'+d),files=files,manifest_collection_sha256=manifest['collection_sha256'],worktree_clean=True,old_git_records=129527,old_git_records_sha256=sha(old),pinned_references=27,M_sha256=digest(M),F_sha256=digest(F),K_sha256=digest(K),P_sha256=ka['P']['sha256'],leaf_semantics_checked=13,complete_M_reconstructed=True,source_pointer_reads=0,candidate_imports=[],scope='Firstparty derived F/K mapping only; original review and token/time truth inherited from accepted K/P. No A/T/input/N or full package.'),sort_keys=True,indent=2))
