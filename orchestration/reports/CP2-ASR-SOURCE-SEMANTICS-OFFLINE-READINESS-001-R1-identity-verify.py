import json,hashlib,stat,subprocess,ast,re,tempfile,shutil
from pathlib import Path
P=Path('/Users/orderly_ray/Projects/think');V=P/'tools/asr_review_acquisition_v6';B=P/'tools/asr_review_acquisition_v5';O=Path('/Users/orderly_ray/Leader/orchestration/reports')
sha=lambda b:hashlib.sha256(b).hexdigest();canon=lambda o:(json.dumps(o,ensure_ascii=True,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode('ascii');git=lambda *a:subprocess.check_output(['git','-C',str(P),*a]).decode().strip()
head='f55fda2dea237120ce09639112767c9857dab8d5';assert git('rev-parse','HEAD')==head and git('rev-parse','HEAD^')=='e6879d2f0da87b6f070314e98727ed22ef403d04' and not git('status','--porcelain')
changes=git('diff-tree','--no-commit-id','--name-status','-r',head).splitlines();assert changes and all(l.split('\t')[1].startswith('tools/asr_review_acquisition_v6/') for l in changes)
assert git('rev-parse','HEAD:tools/asr_review_acquisition_v6')=='05f0b591753a9d8c845656c2f8d6be2c8c725464'
blobs={}
for l in git('ls-tree','-r','HEAD:tools/asr_review_acquisition_v6').splitlines():
 meta,path=l.split('\t');mode,kind,h=meta.split();assert (mode,kind)==('100644','blob');blobs[path]=h
files={p.relative_to(V).as_posix():p for p in V.rglob('*') if p.is_file()};assert set(files)==set(blobs)
for rel,p in files.items():
 s=p.lstat();raw=p.read_bytes();assert stat.S_ISREG(s.st_mode) and s.st_nlink==1;assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==blobs[rel]
m=json.loads((V/'evidence/file-manifest.json').read_bytes());assert len(m['files'])==m['count']==10909 and {r['path'] for r in m['files']}==set(files)-{'evidence/file-manifest.json'}
assert sha((V/'evidence/file-manifest.json').read_bytes())=='9842eec0768da72eb736a635b5cf65739a6376e8556641595ffde841a4781569';assert sha(canon(m['files']))==m['collection_sha256']=='b1d0bcffc328914f092297fd8e1a44bf81423e29299e5e57e1372562d4b38c18'
for r in m['files']:
 raw=files[r['path']].read_bytes();assert (sha(raw),len(raw))==(r['sha256'],r['bytes'])
prov=json.loads((V/'provenance.json').read_bytes());assert len(prov['copied_first_party_files'])==21
for r in prov['copied_first_party_files']:
 old=(B/r['path']).read_bytes();new=(V/r['path']).read_bytes();assert sha(old)==r['v5_sha256'] and sha(new)==r['v6_sha256'] and (old==new)==r['unchanged']
for path,tree in prov['unchanged_baseline_trees'].items():assert git('rev-parse','HEAD:'+path)==tree==git('rev-parse','HEAD^:'+path)
ids=json.loads((V/'evidence/identities.json').read_bytes());assert sha(canon(ids['policy']))==ids['policy_sha256'];old=dict(ids['policy']);old.pop('source_semantics');old['kind']='typed-acquisition-candidate-v5';assert sha(canon(old))==ids['unchanged_v5_policy_sha256']=='41b852bea2b247bf6b8f253bc57e3965dd835c10031000e52b438a09c3aa65db'
assert sha(canon(ids['policy']['source_semantics']))==ids['semantic_contract_sha256'];assert sha(canon(ids['policy']['content_roles']))==ids['role_contract_sha256']
paths=sorted(list((V/'offline_review').glob('*.py'))+list((V/'tests').glob('*.py'))+[V/n for n in ['audit.py','verify.py','network_guard.py','recalculate.py','SCHEMA.md']]);bundle=[{'path':p.relative_to(V).as_posix(),'sha256':sha(p.read_bytes())} for p in paths];assert sha(canon(bundle))==ids['bundle_sha256']=='99114c1ad1126e627723585251ed696063562de4b507d35c28b93a3b1ffb6160'
scan=json.loads((V/'evidence/static-scan/scan-report.json').read_bytes());c=json.loads((V/'evidence/static-scan/context.json').read_bytes());snapshot=json.loads((V/'evidence/static-scan/snapshot.json').read_bytes());assert sha((V/'evidence/static-scan/scan-report.json').read_bytes())==c['raw_report_sha256']=='0aedda9528a1145533ffd9b615a1481beb7257960c9bfd931dd6f38e6846f5c5'
assert scan['verdict']=='sandbox_only' and scan['risk_score']==100 and len(scan['findings'])==len(c['findings'])==287 and not scan['block_signals']
assert len(snapshot['files'])==snapshot['count']==10902 and sha(canon(snapshot['files']))==snapshot['collection_sha256']==c['snapshot_collection_sha256']
for r in snapshot['files']:
 raw=(V/r['path']).read_bytes();assert (sha(raw),len(raw))==(r['sha256'],r['bytes'])
def pointer(obj,path):
 for part in path.split('/')[1:]:
  part=part.replace('~1','/').replace('~0','~');obj=obj[int(part)] if isinstance(obj,list) else obj[part]
 return obj
medium_count=0
for index,(f,r) in enumerate(zip(scan['findings'],c['findings'])):
 assert index==r['finding_index'] and all(f[k]==r[k] for k in ['path','line','rule_id']) and f['severity']==r['raw_severity']
 raw=(V/r['path']).read_bytes();assert sha(raw)==r['file_sha256'];text=raw.decode()
 if r['raw_severity']=='medium':
  data=json.loads(raw)
  for match in r['matches']:
   value=pointer(data,match['json_pointer']);assert value==match['hash_value'] and re.fullmatch(r'(?:[0-9a-f]{40}|[0-9a-f]{64})',value) and match['substring'] in value;medium_count+=1
  for match in re.finditer(r['rule_id'].rsplit('-',1)[-1],text):
   token=re.search(r'[0-9a-f]*$',text[:match.start()]).group()+re.match(r'[0-9a-f]*',text[match.start():]).group();assert len(token) in [40,64]
 elif r['path'].endswith('.py'):
  assert any(isinstance(n,ast.Constant) and isinstance(n.value,str) and n.lineno<=r['line']<=n.end_lineno for n in ast.walk(ast.parse(text)))
 elif r['path'].endswith('.json'):
  d=json.loads(text)
  for match in r.get('matches',[]):assert pointer(d,match['json_pointer'])==match['value']
 else:assert r['path']=='README.md'
assert medium_count==366
supp=json.loads((V/'evidence/static-scan/supplemental-diffs/scan-report.json').read_bytes());assert supp['verdict']=='low_indicators' and supp['risk_score']==0 and supp['findings']==[] and supp['stats']['text_files']==2
for r in c['supplemental_diffs']['copies']:
 raw=(V/r['original_path']).read_bytes();assert sha(raw)==r['sha256'] and len(raw)==r['bytes']

rev=json.loads((V/'revision-provenance.json').read_bytes());assert rev['parent_commit']==git('rev-parse','HEAD^') and not rev['assertion_changes']
for record in rev['source_records']:
 oldraw=subprocess.check_output(['git','-C',str(P),'show','HEAD^:tools/asr_review_acquisition_v6/'+record['path']]);newraw=(V/record['path']).read_bytes()
 assert sha(oldraw)==record['parent_sha256'] and sha(newraw)==record['revised_sha256'] and (oldraw==newraw)==record['unchanged']
def methods(ref,directory):
 found={}
 for f in (P/directory/'tests').glob('test_*.py'):
  text=subprocess.check_output(['git','-C',str(P),'show',ref+':'+directory+'/tests/'+f.name]).decode()
  for cls in ast.parse(text).body:
   if isinstance(cls,ast.ClassDef):
    for m in cls.body:
     if isinstance(m,ast.FunctionDef) and m.name.startswith('test_'):found[f.stem+'.'+cls.name+'.'+m.name]=sha(ast.get_source_segment(text,m).encode())
 return found
oldmethods=methods('HEAD^','tools/asr_review_acquisition_v6');newmethods=methods('HEAD','tools/asr_review_acquisition_v6');v5methods=methods('HEAD','tools/asr_review_acquisition_v5')
assert len(oldmethods)==153 and len(newmethods)==158 and len(v5methods)==132 and set(v5methods)<=set(oldmethods)
assert len(rev['prior_methods'])==153 and {r['test'] for r in rev['prior_methods']}==set(oldmethods)
for record in rev['prior_methods']:assert oldmethods[record['test']]==newmethods[record['test']]==record['parent_source_sha256']==record['revised_source_sha256'] and record['unchanged']
assert set(rev['new_methods'])==set(newmethods)-set(oldmethods)
assert {n for n in v5methods if v5methods[n]!=newmethods[n]}=={'test_behavior.ParserBehavior.test_F2_mismatched_delimiters','test_content_routing.ContentRoutingTests.test_intentional_cpp_stops_without_successor_request'}
semantic=dict(ids['policy']['source_semantics'])
for key in ('revision','header_name_ambiguity','directive_extent'):semantic.pop(key)
assert sha(canon(semantic))==ids['parent_v6_semantic_sha256']=='4ba4322cafd11012dbf10a778ca402fce141ccf5891e21c2c938d31e615fb476'
parent_policy=dict(ids['policy']);parent_policy['source_semantics']=semantic
assert sha(canon(parent_policy))==ids['parent_v6_policy_sha256']=='b94a5a5e8118f6c510d5a7e6b3da124835a8697ac77dec166378bedeb6623bd5'
for name,expected in [('cp2-source-semantics-readiness-decision-2026-09-06.md','35498c5d8424add7eed68401f5a5094ce000b5ea6265e4bb292b814f91f7c283'),('prd-v0.1-2026-09-04.md','97ff4382c179482a02261b73b85e7e422d200c0dbf6654bac093cc56fc5d373f')]:assert sha((P/'doc'/name).read_bytes())==expected

root=Path(tempfile.mkdtemp(prefix='think-leader-v6r1-',dir='/private/tmp'))
for rel,p in files.items():
 if rel.startswith('evidence/'):continue
 target=root/rel;target.parent.mkdir(exist_ok=True,parents=True);shutil.copyfile(p,target)
(root/'evidence').mkdir()
r={'RESULT':'PASS','baseline132_retained':True,'prior153_methods_identical':True,'new_methods':5,'head':head,'git_tree':'05f0b591753a9d8c845656c2f8d6be2c8c725464','files_verified':10910,'manifest_records':10909,'bundle_records':bundle,'bundle_sha256':ids['bundle_sha256'],'policy_sha256':ids['policy_sha256'],'semantic_contract_sha256':ids['semantic_contract_sha256'],'old_trees_unchanged':True,'baseline_file_records_verified':21,'scanner_original_verdict':'sandbox_only','scanner_findings_checked':287,'medium_digest_matches_checked':366,'scan_snapshot_files_verified':10902,'independent_root':str(root)}
(O/'CP2-ASR-SOURCE-SEMANTICS-OFFLINE-READINESS-001-R1-identity.json').write_bytes(canon(r));print(json.dumps({k:v for k,v in r.items() if k!='bundle_records'},indent=2))
