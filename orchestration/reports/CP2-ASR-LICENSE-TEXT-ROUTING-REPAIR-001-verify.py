import hashlib,json,stat,subprocess,tempfile,shutil,re,ast
from pathlib import Path
P=Path('/Users/orderly_ray/Projects/think'); V=P/'tools/asr_review_acquisition_v5'; B=P/'tools/asr_review_acquisition_v4'
O=Path('/Users/orderly_ray/Leader/orchestration/reports')
def sha(b):return hashlib.sha256(b).hexdigest()
def canonical(o):return (json.dumps(o,sort_keys=True,ensure_ascii=True,separators=(',',':'),allow_nan=False)+'\n').encode('ascii')
def git(*args):return subprocess.check_output(['git','-C',str(P),*args]).decode().strip()
head='a60ced8861f4a9fd4716aa65866a90a861978989'
assert git('rev-parse','HEAD')==head
assert git('rev-parse','HEAD^')=='f347260f8afc24a22970cead9740c5b6792d0527'
assert git('status','--porcelain')==''
changes=git('diff-tree','--no-commit-id','--name-status','-r',head).splitlines()
assert len(changes)==1966 and all(x.startswith('A\ttools/asr_review_acquisition_v5/') for x in changes)
tree=git('rev-parse','HEAD:tools/asr_review_acquisition_v5');assert tree=='d5d66a3ef147b3fa587c8b77dd537b94c82fdf50'
blobs={}
for line in git('ls-tree','-r','HEAD:tools/asr_review_acquisition_v5').splitlines():
 meta,path=line.split('\t');mode,kind,blob=meta.split();assert mode=='100644' and kind=='blob';blobs[path]=blob
files={x.relative_to(V).as_posix():x for x in V.rglob('*') if x.is_file()}
assert set(files)==set(blobs)
for rel,p in files.items():
 s=p.lstat();raw=p.read_bytes();assert stat.S_ISREG(s.st_mode) and s.st_nlink==1
 assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==blobs[rel]
manifest=json.loads((V/'evidence/file-manifest.json').read_bytes());records=manifest['records']
assert len(records)==1965 and {r['path'] for r in records}==set(files)-{'evidence/file-manifest.json'}
assert sha(canonical(records))==manifest['records_sha256']=='8354cd10fe23a82edcf0d1d80cdad490aa088f3d27911a2858260001d84f20a9'
for r in records:
 p=files[r['path']];raw=p.read_bytes();assert (len(raw),sha(raw),oct(stat.S_IMODE(p.lstat().st_mode)))==(r['bytes'],r['sha256'],r['mode'])
prov=json.loads((V/'evidence/provenance.json').read_bytes())
for key,path in [('v2','tools/asr_offline_review_v2'),('v3','tools/asr_review_acquisition_v3'),('v4','tools/asr_review_acquisition_v4'),('v3_freeze','doc/security-reviews/asr-acquisition-v3-release-freeze/2026-09-06'),('v4_freeze','doc/security-reviews/asr-acquisition-v4-release-freeze/2026-09-06')]:
 # Resolve paths from the known tree object rather than assuming historical directory names.
 expected=prov['old_readonly_trees'][key]
 assert expected in git('ls-tree','-r','-t','HEAD') and expected in git('ls-tree','-r','-t','HEAD^')
baselines=json.loads((V/'evidence/baseline-files.json').read_bytes());assert len(baselines)==19
changed=[]
for r in baselines:
 old=(B/r['path']).read_bytes();new=(V/r['path']).read_bytes()
 assert sha(old)==r['v4_sha256'] and sha(new)==r['v5_sha256'] and (old==new)==r['byte_identical']
 if old!=new:changed.append(r['path'])
bundlepaths=sorted(list((V/'offline_review').glob('*.py'))+list((V/'tests').glob('*.py'))+[V/n for n in ['audit.py','verify.py','network_guard.py','recalculate.py','SCHEMA.md']])
bundle=[{'path':p.relative_to(V).as_posix(),'sha256':sha(p.read_bytes())} for p in bundlepaths]
assert len(bundle)==20 and sha(canonical(bundle))==prov['v5_bundle_sha256']=='1dd806b43fe95722150449e795337ee1e3a8e399ae53766e6aa041d5ca39dd3e'
assert sha(canonical(prov['policy']))==prov['v5_policy_sha256']
oldpolicy=dict(prov['policy']);roles=oldpolicy.pop('content_roles');oldpolicy['kind']='complete-acquisition-candidate-v3'
assert sha(canonical(oldpolicy))==prov['v4_policy_sha256']=='ee9d1ae7b4b17d2d895d3a6e0b62f73bfda7eb8a9cfae50e9d264f9ed23fc627'
assert sha(canonical(roles))==prov['role_contract_sha256']
scan=json.loads((V/'evidence/static-scan/scan-report.json').read_bytes());context=json.loads((V/'evidence/static-scan-context.json').read_bytes())
assert sha((V/'evidence/static-scan/scan-report.json').read_bytes())==context['scanner_report_sha256']=='f83ba6965c60fce950bf7c7881ed391b6aac72b8cb06c518f33f8955ca616aa5'
assert scan['verdict']=='sandbox_only' and scan['risk_score']==100 and scan['block_signals']==[]
assert len(scan['findings'])==len(context['findings'])==18
for f,c in zip(scan['findings'],context['findings']):
 assert all(f[k]==c[k] for k in ['path','line','rule_id','severity'])
 raw=(V/f['path']).read_bytes();assert sha(raw)==c['file_sha256'];txt=raw.decode()
 if c['assessment']=='hash_substring_false_positive':
  for m in re.finditer('8086',txt):
   assert re.fullmatch('[0-9a-f]{64}',re.search(r'[0-9a-f]*$',txt[:m.start()]).group()+re.match(r'[0-9a-f]*',txt[m.start():]).group())
 elif f['path'].endswith('.py'):
  line=f['line'];treeast=ast.parse(txt)
  assert any(isinstance(n,ast.Constant) and isinstance(n.value,str) and n.lineno<=line<=n.end_lineno for n in ast.walk(treeast))
 elif f['path'].endswith('.json'): json.loads(txt)
 else: assert f['path']=='README.md'
inputs=json.loads((V/'evidence/static-scan-input.json').read_bytes());assert len(inputs)==1959
for r in inputs:
 raw=(V/r['path']).read_bytes();assert sha(raw)==r['sha256'] and len(raw)==r['bytes']
root=Path(tempfile.mkdtemp(prefix='think-leader-v5-',dir='/private/tmp'))
for rel,p in files.items():
 if rel.startswith('evidence/'):continue
 target=root/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,target)
(root/'evidence').mkdir()
result={'result':'PASS','head':head,'parent':git('rev-parse','HEAD^'),'tree':tree,'files':len(files),'manifest_records':len(records),'manifest_sha256':sha((V/'evidence/file-manifest.json').read_bytes()),'records_sha256':manifest['records_sha256'],'baseline_records':len(baselines),'changed_baseline_paths':changed,'bundle_sha256':sha(canonical(bundle)),'bundle_records':bundle,'policy_sha256':prov['v5_policy_sha256'],'role_contract_sha256':prov['role_contract_sha256'],'scanner_original_verdict':scan['verdict'],'scanner_score':scan['risk_score'],'scanner_findings_checked':18,'scanner_snapshot_hashes_checked':1959,'independent_root':str(root)}
(O/'CP2-ASR-LICENSE-TEXT-ROUTING-REPAIR-001-verification.json').write_bytes(canonical(result))
print(json.dumps({k:v for k,v in result.items() if k!='bundle_records'},indent=2))
