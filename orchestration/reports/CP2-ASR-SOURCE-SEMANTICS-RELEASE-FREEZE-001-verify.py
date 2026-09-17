import json,hashlib,stat,subprocess
from pathlib import Path
P=Path('/Users/orderly_ray/Projects/think');V=P/'tools/asr_review_acquisition_v6';D=P/'doc/security-reviews/asr-acquisition-v6-release-freeze/2026-09-06';O=Path('/Users/orderly_ray/Leader/orchestration/reports')
sha=lambda raw:hashlib.sha256(raw).hexdigest();C=lambda o:(json.dumps(o,sort_keys=True,ensure_ascii=True,separators=(',',':'),allow_nan=False)+'\n').encode('ascii');digest=lambda o:sha(C(o));git=lambda *a:subprocess.check_output(['git','-C',str(P),*a]).decode().strip();load=lambda p:json.loads(p.read_bytes())
head='d78577b8bac1108791e0c4ba3c7a0cd672958c94';base='f55fda2dea237120ce09639112767c9857dab8d5'
assert git('rev-parse','HEAD')==head and git('rev-parse','HEAD^')==base and not git('status','--porcelain');git('show','--check','--format=',head)
expected={'freeze.json':(54757,'09523de2726e1ac84d065bbf7284d20ae006fae2f561baa6ffbbb88bba0059b7'),'MANIFEST.json':(2952140,'a120ddf5e1a80d112454647ca0cee364c6aebdcb4ca112bbcbc624040cdb7914'),'REPORT.md':(25690,'5cee4af12a373d80ace966a6122b8ea8853b0e239bc5a8d7c63016c9662d482e')}
assert set(git('diff-tree','--no-commit-id','--name-status','-r',head).splitlines())=={'A\t'+str((D/n).relative_to(P)) for n in expected}
assert {p.name for p in D.iterdir()}==set(expected)
for name,(size,h) in expected.items():
 raw=(D/name).read_bytes();st=(D/name).lstat();assert stat.S_ISREG(st.st_mode) and st.st_nlink==1 and len(raw)==size and sha(raw)==h
 if name.endswith('.json'):assert C(json.loads(raw))==raw
f=load(D/'freeze.json');m=load(D/'MANIFEST.json');ids=load(V/'evidence/identities.json');accept=load(O/'CP2-ASR-SOURCE-SEMANTICS-OFFLINE-READINESS-001-R1-acceptance.json')
assert f['accepted_release']['commit']==f['commit_parent']==m['accepted_commit']==base
assert git('rev-parse','HEAD:tools/asr_review_acquisition_v6')==git('rev-parse','HEAD^:tools/asr_review_acquisition_v6')==m['release_tree']==f['accepted_release']['tree']=='05f0b591753a9d8c845656c2f8d6be2c8c725464'
assert git('rev-parse','HEAD:'+str(D.relative_to(P)))=='b674a029f2faefdd92367866236037a74b7ac053'
assert f['accepted_release']['manifest_sha256']==expected['MANIFEST.json'][1]
blobs={}
for line in git('ls-tree','-r',base+':tools/asr_review_acquisition_v6').splitlines():
 meta,path=line.split('\t');mode,kind,h=meta.split();assert kind=='blob';blobs[path]=(mode,h)
files={p.relative_to(V).as_posix():p for p in V.rglob('*') if p.is_file()};assert set(files)==set(blobs)=={r['path'] for r in m['artifact_files']}
assert len(files)==m['artifact_count']==f['accepted_release']['files']==10910
records=[]
for rel in sorted(files):
 p=files[rel];st=p.lstat();raw=p.read_bytes();assert stat.S_ISREG(st.st_mode) and st.st_nlink==1 and blobs[rel][0]=='100644';h=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest();assert h==blobs[rel][1]
 records.append({'path':rel,'bytes':len(raw),'sha256':sha(raw),'git_blob':h,'git_mode':'100644','file_type':'regular','nlink':1})
assert records==m['artifact_files'];assert digest(records)==m['artifact_collection_sha256']==f['accepted_release']['artifact_collection_sha256']=='e9d396749b7e397fc3b83dba793691d0be7d42dadd8060f5f1624b4758924608'
old=load(V/'evidence/file-manifest.json');assert len(old['files'])==m['original_manifest']['records']==10909
assert digest(old['files'])==old['collection_sha256']==m['original_manifest']['collection_sha256']
assert sha((V/m['original_manifest']['path']).read_bytes())==m['original_manifest']['sha256']=='9842eec0768da72eb736a635b5cf65739a6376e8556641595ffde841a4781569'
for r in old['files']:assert sha(files[r['path']].read_bytes())==r['sha256'] and files[r['path']].stat().st_size==r['bytes']
assert m['bundle_count']==len(m['bundle_records'])==22
assert m['bundle_records']==load(O/'CP2-ASR-SOURCE-SEMANTICS-OFFLINE-READINESS-001-R1-identity.json')['bundle_records']
assert digest(m['bundle_records'])==ids['bundle_sha256']==m['bundle_sha256']==f['accepted_release']['bundle_sha256']
assert f['policy']==ids['policy'] and f['source_semantics']==f['policy']['source_semantics'] and f['content_roles']==f['policy']['content_roles']
for obj,key in [('policy','policy_sha256'),('source_semantics','semantic_contract_sha256'),('content_roles','role_contract_sha256')]:assert digest(f[obj])==f[key]==ids[key]
assert f['input_schema']==6 and f['source_report_schema']==1 and f['kind']=='typed-acquisition-candidate-v6'
assert len(f['sources'])==48
for name,r in f['sources'].items():
 path=Path(r['path']);assert path.is_absolute() and path.name not in ('current-task.json','state.json');raw=path.read_bytes();st=path.lstat();assert stat.S_ISREG(st.st_mode) and st.st_nlink==r['nlink']==1 and r['file_type']=='regular';assert sha(raw)==r['sha256'] and len(raw)==r['bytes']
 if 'git_commit' in r:
  assert r['git_commit']==base and path==P/r['project_relative_path'];assert git('rev-parse',base+':'+r['project_relative_path'])==r['git_blob'];assert r['git_mode']=='100644';assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==r['git_blob']
assert f['sources']['leader_acceptance']['sha256']==f['leader_acceptance']['report_sha256']=='b06d977b376a8e1ed16efcb452e724333a79b14a471834c5b0a80de45c65678b'
assert f['sources']['stable_freeze_dispatch']['sha256']=='6c6bd4e48b2086853f0a09e782769fe3bcf0e7f72d29827e811b916b5e3c8de2'
assert f['leader_acceptance']['decision']=='ACCEPTED offline v6 R1 candidate' and accept['decision']=='ACCEPTED'
for key in ['verification','semantic_recomputation','acceptance_evidence']:assert f['leader_acceptance'][key]==accept[key]
for path,tree in load(V/'provenance.json')['unchanged_baseline_trees'].items():assert git('rev-parse','HEAD:'+path)==git('rev-parse','HEAD^:'+path)==tree
assert git('rev-parse','a57f643bac24edef5d6601b8a59baa77060f3d2c:doc/security-reviews/sherpa-onnx-narrow-runtime-boundary-design/2026-09-05')==f['fixed_scope']['design']['tree']=='31376c73f43caf3bbfd664d8316ffecdc589379d'
n=load(V/'evidence/run-r1-a/normalized.json');ts={**n['scenarios'],**{k:v['terminal'] for k,v in n['acquisition'].items()}};assert len(ts)==133
collections={}
for key,fields in [('ledger_collection_sha256',['ledger_hash','ledger_count']),('terminal_collection_sha256',['evidence_hash'])]:collections[key]=digest([{'scenario':name,**{k:t[k] for k in fields}} for name,t in sorted(ts.items())])
collections['source_analysis_collection_sha256']=digest([{'scenario':name,'reports':t['source_analyses']} for name,t in sorted(ts.items())]);assert collections==f['evidence_collections']==accept['verification']['collections']
assert f['first_party_scanner']['raw_verdict']=='sandbox_only' and f['first_party_scanner']['risk_score']==100 and f['first_party_scanner']['summary']=={'high':9,'medium':274,'low':4}
for key in ['new_acquisition_authorized','pending_override_implemented','real_capability_adjudication_authorized','network_or_workload_executed','input_or_Trust_created']:assert f['authority'][key] is False
r={'RESULT':'PASS','commit':head,'parent':base,'freeze_tree':'b674a029f2faefdd92367866236037a74b7ac053','candidate_tree':m['release_tree'],'new_files':{n:{'bytes':x[0],'sha256':x[1]} for n,x in expected.items()},'release_files':10910,'reference_files':48,'original_manifest_records':10909,'artifact_collection_sha256':m['artifact_collection_sha256'],'bundle_sha256':m['bundle_sha256'],'policy_sha256':f['policy_sha256'],'semantic_contract_sha256':f['semantic_contract_sha256'],'role_contract_sha256':f['role_contract_sha256'],'evidence_collections':collections,'noncyclic_domains_reviewed':True,'new_acquisition_authorized':False,'real_manual_review_authorized':False,'candidate_executed':False,'real_body_or_metadata_read':False,'git_clean':True}
(O/'CP2-ASR-SOURCE-SEMANTICS-RELEASE-FREEZE-001-verification.json').write_bytes(C(r));print(json.dumps(r,indent=2))
