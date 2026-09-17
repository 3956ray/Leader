import json,hashlib,stat,subprocess,ast,re,tempfile,shutil
from pathlib import Path
P=Path('/Users/orderly_ray/Projects/think');V=P/'tools/asr_review_acquisition_v6';B=P/'tools/asr_review_acquisition_v5';O=Path('/Users/orderly_ray/Leader/orchestration/reports')
sha=lambda b:hashlib.sha256(b).hexdigest();canon=lambda o:(json.dumps(o,ensure_ascii=True,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode('ascii');git=lambda *a:subprocess.check_output(['git','-C',str(P),*a]).decode().strip()
head='e6879d2f0da87b6f070314e98727ed22ef403d04';assert git('rev-parse','HEAD')==head and git('rev-parse','HEAD^')=='c84685fce9205886a6fbe41386acaaa5b7374a57' and not git('status','--porcelain')
changes=git('diff-tree','--no-commit-id','--name-status','-r',head).splitlines();assert len(changes)==6767 and all(l.startswith('A\ttools/asr_review_acquisition_v6/') for l in changes)
assert git('rev-parse','HEAD:tools/asr_review_acquisition_v6')=='8ff892477fa8d8d3e4e7d59fcc11f24262b5e830'
blobs={}
for l in git('ls-tree','-r','HEAD:tools/asr_review_acquisition_v6').splitlines():
 meta,path=l.split('\t');mode,kind,h=meta.split();assert (mode,kind)==('100644','blob');blobs[path]=h
files={p.relative_to(V).as_posix():p for p in V.rglob('*') if p.is_file()};assert set(files)==set(blobs)
for rel,p in files.items():
 s=p.lstat();raw=p.read_bytes();assert stat.S_ISREG(s.st_mode) and s.st_nlink==1;assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==blobs[rel]
m=json.loads((V/'evidence/file-manifest.json').read_bytes());assert len(m['files'])==m['count']==6766 and {r['path'] for r in m['files']}==set(files)-{'evidence/file-manifest.json'}
assert sha((V/'evidence/file-manifest.json').read_bytes())=='00e12352eb3d12031a1791fed487b202deabff88f9e53ac518b7d93777566bed';assert sha(canon(m['files']))==m['collection_sha256']=='654d54de1c9dd3559e6046442b49e973b891503e667d5804fc6b85b651d9bef0'
for r in m['files']:
 raw=files[r['path']].read_bytes();assert (sha(raw),len(raw))==(r['sha256'],r['bytes'])
prov=json.loads((V/'provenance.json').read_bytes());assert len(prov['copied_first_party_files'])==21
for r in prov['copied_first_party_files']:
 old=(B/r['path']).read_bytes();new=(V/r['path']).read_bytes();assert sha(old)==r['v5_sha256'] and sha(new)==r['v6_sha256'] and (old==new)==r['unchanged']
for path,tree in prov['unchanged_baseline_trees'].items():assert git('rev-parse','HEAD:'+path)==tree==git('rev-parse','HEAD^:'+path)
ids=json.loads((V/'evidence/identities.json').read_bytes());assert sha(canon(ids['policy']))==ids['policy_sha256'];old=dict(ids['policy']);old.pop('source_semantics');old['kind']='typed-acquisition-candidate-v5';assert sha(canon(old))==ids['unchanged_v5_policy_sha256']=='41b852bea2b247bf6b8f253bc57e3965dd835c10031000e52b438a09c3aa65db'
assert sha(canon(ids['policy']['source_semantics']))==ids['semantic_contract_sha256'];assert sha(canon(ids['policy']['content_roles']))==ids['role_contract_sha256']
paths=sorted(list((V/'offline_review').glob('*.py'))+list((V/'tests').glob('*.py'))+[V/n for n in ['audit.py','verify.py','network_guard.py','recalculate.py','SCHEMA.md']]);bundle=[{'path':p.relative_to(V).as_posix(),'sha256':sha(p.read_bytes())} for p in paths];assert sha(canon(bundle))==ids['bundle_sha256']=='e5fe9e51afe3d86bf7b4ef0196399a50fc98226fdac45aa21907fcf52dbf9677'
scan=json.loads((V/'evidence/static-scan/scan-report.json').read_bytes());c=json.loads((V/'evidence/static-scan/context.json').read_bytes());snapshot=json.loads((V/'evidence/static-scan/snapshot.json').read_bytes());assert sha((V/'evidence/static-scan/scan-report.json').read_bytes())==c['raw_report_sha256']=='f118c8af43fff85bc804c3f73b5a14316ee079e647a86c325e8c7b5c6e5f80b3'
assert scan['verdict']=='sandbox_only' and scan['risk_score']==100 and len(scan['findings'])==len(c['findings'])==104 and not scan['block_signals']
assert len(snapshot['files'])==snapshot['count']==6759 and sha(canon(snapshot['files']))==snapshot['collection_sha256']==c['snapshot_collection_sha256']
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
assert medium_count==142
supp=json.loads((V/'evidence/static-scan/supplemental-diff/scan-report.json').read_bytes());assert supp['verdict']=='low_indicators' and supp['risk_score']==0 and supp['findings']==[] and supp['stats']['text_files']==1
assert sha((V/'v5-to-v6.diff').read_bytes())==c['supplemental_diff']['bytes_sha256']
root=Path(tempfile.mkdtemp(prefix='think-leader-v6-',dir='/private/tmp'))
for rel,p in files.items():
 if rel.startswith('evidence/'):continue
 target=root/rel;target.parent.mkdir(exist_ok=True,parents=True);shutil.copyfile(p,target)
(root/'evidence').mkdir()
r={'RESULT':'PASS','head':head,'git_tree':'8ff892477fa8d8d3e4e7d59fcc11f24262b5e830','files_verified':6767,'manifest_records':6766,'bundle_records':bundle,'bundle_sha256':ids['bundle_sha256'],'policy_sha256':ids['policy_sha256'],'semantic_contract_sha256':ids['semantic_contract_sha256'],'old_trees_unchanged':True,'baseline_file_records_verified':21,'scanner_original_verdict':'sandbox_only','scanner_findings_checked':104,'medium_digest_matches_checked':142,'scan_snapshot_files_verified':6759,'independent_root':str(root)}
(O/'CP2-ASR-SOURCE-SEMANTICS-OFFLINE-READINESS-001-identity.json').write_bytes(canon(r));print(json.dumps({k:v for k,v in r.items() if k!='bundle_records'},indent=2))
