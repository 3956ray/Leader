import json,hashlib,stat,subprocess,re
from pathlib import Path
P=Path('/Users/orderly_ray/Projects/think');F=P/'doc/security-reviews/asr-acquisition-v5-release-freeze/2026-09-06';V=P/'tools/asr_review_acquisition_v5';O=Path('/Users/orderly_ray/Leader/orchestration/reports')
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(o):return (json.dumps(o,ensure_ascii=True,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode('ascii')
def git(*a):return subprocess.check_output(['git','-C',str(P),*a]).decode().strip()
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
head='b0193cf1e818f76a4e429c4d0aeeb81d29a16cbc';parent='a60ced8861f4a9fd4716aa65866a90a861978989';base=F.relative_to(P).as_posix()
assert git('rev-parse','HEAD')==head and git('rev-parse','HEAD^')==parent and git('status','--porcelain')==''
assert set(git('diff-tree','--no-commit-id','--name-status','-r',head).splitlines())=={'A\t'+base+'/'+n for n in ['MANIFEST.json','freeze.json','REPORT.md']}
assert git('rev-parse','HEAD:'+base)=='1c7f74e87bfb20c75d2a4b1b75445a0a92916d1c'
git('show','--check','--format=',head)
pins={'MANIFEST.json':('107b27e5d671973d3c4ca386e7acb311128ee33e6b2fba3175a3db93ff864356',567921),'freeze.json':('21aaee7a39eb0ee9668c0e10f3ad51ee6068356c9924b57597c122bbf521541e',40797),'REPORT.md':('edf3d4fd4c10c1f14907bbc992fb239f531e8add9258a7ec05223fcfe82f1e7e',10795)}
for name,(h,size) in pins.items():
 p=F/name;raw=p.read_bytes();s=p.lstat();assert stat.S_ISREG(s.st_mode) and s.st_nlink==1
 assert (sha(raw),len(raw))==(h,size) and blob(raw)==git('rev-parse','HEAD:'+base+'/'+name)
 if name.endswith('.json'):assert canon(json.loads(raw))==raw
f=json.loads((F/'freeze.json').read_bytes());m=json.loads((F/'MANIFEST.json').read_bytes());a=f['accepted_release'];records=m['artifact_files']
assert f['input_schema']==5 and f['commit_parent']==parent and m['accepted_commit']==parent==a['commit']
assert len(records)==m['file_count']==a['complete_artifact_file_count']==1966
assert sha(canon(records))==m['artifact_records_sha256']==a['complete_artifact_records_sha256']=='d47ef78b6c452533377fa97d97bb245f83597f5028154a47a589c6e9ee24b678'
assert a['manifest_document_sha256']==pins['MANIFEST.json'][0]
actual={p.relative_to(V).as_posix() for p in V.rglob('*') if p.is_file()};assert actual=={r['path'] for r in records};assert [r['path'] for r in records]==sorted(actual)
gitfiles={}
for l in git('ls-tree','-r','HEAD:tools/asr_review_acquisition_v5').splitlines():
 meta,path=l.split('\t');mode,kind,h=meta.split();assert (mode,kind)==('100644','blob');gitfiles[path]=h
assert set(gitfiles)==actual
for r in records:
 p=V/r['path'];raw=p.read_bytes();s=p.lstat();assert stat.S_ISREG(s.st_mode) and s.st_nlink==r['link_count']==1 and r['regular_file'] is True
 assert oct(stat.S_IMODE(s.st_mode))==r['filesystem_mode'] and r['git_mode']=='100644'
 assert len(raw)==r['bytes'] and sha(raw)==r['sha256'] and blob(raw)==r['git_blob_sha1']==gitfiles[r['path']]
orig=json.loads((V/'evidence/file-manifest.json').read_bytes());assert len(orig['records'])==1965
assert sha((V/'evidence/file-manifest.json').read_bytes())==a['original_manifest_sha256']==m['original_manifest_sha256']
assert sha(canon(orig['records']))==orig['records_sha256']==a['original_records_sha256']==m['original_records_sha256']
for r in orig['records']:
 raw=(V/r['path']).read_bytes();assert (sha(raw),len(raw))==(r['sha256'],r['bytes'])
bundlepaths=sorted(list((V/'offline_review').glob('*.py'))+list((V/'tests').glob('*.py'))+[V/n for n in ['audit.py','verify.py','network_guard.py','recalculate.py','SCHEMA.md']])
bundle=[{'path':p.relative_to(V).as_posix(),'sha256':sha(p.read_bytes())} for p in bundlepaths]
assert bundle==m['bundle_records'] and len(bundle)==20
assert sha(canon(bundle))==m['code_schema_test_bundle_sha256']==a['code_schema_test_bundle_sha256']=='1dd806b43fe95722150449e795337ee1e3a8e399ae53766e6aa041d5ca39dd3e'
prov=json.loads((V/'evidence/provenance.json').read_bytes());assert f['policy']==prov['policy']
assert sha(canon(f['policy']))==f['policy_sha256']==prov['v5_policy_sha256']
assert f['content_roles']==f['policy']['content_roles'] and sha(canon(f['content_roles']))==f['role_contract_sha256']==prov['role_contract_sha256']
old=dict(f['policy']);old.pop('content_roles');old['kind']='complete-acquisition-candidate-v3';assert sha(canon(old))==prov['v4_policy_sha256']
for t in f['verification_this_task']['readonly_trees']:
 assert git('rev-parse','HEAD:'+t['path'])==git('rev-parse','HEAD^:'+t['path'])==t['git_tree']
assert len(f['sources'])==42
refs={}
for k,r in f['sources'].items():
 p=Path(r['path']);assert p.is_absolute();assert not p.is_relative_to(Path('/private/tmp/think-asr-v4-acquisition-3sx4ux01'))
 raw=p.read_bytes();s=p.lstat();assert stat.S_ISREG(s.st_mode) and s.st_nlink==r['link_count']==1 and r['regular_file']
 assert (sha(raw),len(raw))==(r['sha256'],r['bytes']),k
 if 'git_blob_sha1' in r:
  assert r['pinned_at_commit']==parent and p==P/r['repository_path']
  assert blob(raw)==r['git_blob_sha1']==git('rev-parse',parent+':'+r['repository_path'])
 refs[k]=r['sha256']
ctx=Path(f['sources']['design_context']['path']).read_text();body=ctx.split('<!-- canonical-input-records-v1:start -->')[1].split('<!-- canonical-input-records-v1:end -->')[0].split('```text\n')[1].split('```')[0]
lines=body.splitlines();assert len(lines)==28 and all(len(l.split('|'))==3 for l in lines)
d=sha(('\n'.join(sorted(lines,key=lambda x:x.encode()))+'\n').encode());assert d==f['policy']['design']['sha256']
design_path='doc/security-reviews/sherpa-onnx-narrow-runtime-boundary-design/2026-09-05';assert git('rev-parse',f['policy']['design']['commit']+':'+design_path)==f['policy']['design']['tree']
assert refs['current_license_decision']=='27789c9bd35e6e452de70c21b637fc496d8ac17902cda075a98af81c7006aa75'
assert refs['leader_acceptance']=='d9b8ba069a105eec3b23d14bc97f8ea833aac83ec5831842c8461006f959b0c1'
assert not f['authority_mapping']['second_real_acquisition_authorized'] and not f['authority_mapping']['acquisition_executed']
assert f['first_party_scanner']['original_verdict']=='sandbox_only' and f['first_party_scanner']['findings']==18 and f['first_party_scanner']['risk_score']==100
assert f['conclusion_limits']['source_verdict']=='insufficient_evidence'
r={'result':'PASS','commit':head,'parent':parent,'freeze_directory_tree':git('rev-parse','HEAD:'+base),'documents':{k:{'sha256':v[0],'bytes':v[1]} for k,v in pins.items()},'verified_artifact_files':len(records),'artifact_records_sha256':m['artifact_records_sha256'],'bundle_file_count':len(bundle),'bundle_sha256':a['code_schema_test_bundle_sha256'],'policy_sha256':f['policy_sha256'],'role_contract_sha256':f['role_contract_sha256'],'direct_references_verified':refs,'design_records':28,'design_digest':d,'original_manifest_verified':True,'old_trees_unchanged':True,'clean_worktree':True,'source_reads':'first-party code/derived evidence only; no referenced historical raw bodies or real metadata opened','candidate_functions_or_tests_executed':False,'fresh_authorization_required':True,'pinned_dispatch_archive_must_remain_immutable':f['sources']['freeze_dispatch']}
(O/'CP2-ASR-LICENSE-TYPED-RELEASE-FREEZE-001-verification.json').write_bytes(canon(r));print(json.dumps({k:v for k,v in r.items() if k!='direct_references_verified'},indent=2))
