import json,hashlib,stat,ast,subprocess
from pathlib import Path
O=Path('/Users/orderly_ray/Leader/orchestration/reports'); V=Path('/Users/orderly_ray/Projects/think/tools/asr_review_acquisition_v5'); L=Path('/private/tmp/think-leader-v5-qnrj4yoo')
def canonical(o):return (json.dumps(o,sort_keys=True,ensure_ascii=True,separators=(',',':'),allow_nan=False)+'\n').encode('ascii')
def sha(raw):return hashlib.sha256(raw).hexdigest()
def digest(o):return sha(canonical(o))
v=json.loads((O/'CP2-ASR-LICENSE-TEXT-ROUTING-REPAIR-001-verification.json').read_bytes())
for r in v['bundle_records']:
 assert sha((V/r['path']).read_bytes())==r['sha256']==sha((L/r['path']).read_bytes())
roots=[L/'evidence/leader-a',L/'evidence/leader-b',V/'evidence/run-a',V/'evidence/run-b']
names={p.relative_to(roots[0]).as_posix() for p in roots[0].rglob('*.json') if p.name!='tests-log.json'}
assert len(names)==962
for root in roots:
 assert {p.relative_to(root).as_posix() for p in root.rglob('*.json') if p.name!='tests-log.json'}==names
 for rel in names:assert (root/rel).read_bytes()==(roots[0]/rel).read_bytes()
raw=(roots[0]/'normalized.json').read_bytes();n=json.loads(raw)
assert sha(raw)=='f2a0fb9c4854991a628ac386ebe0901dea430b9eedebf4d561d5322b2a95a097'
assert n['tests_run']==132 and len(n['outcomes'])==761 and all(r['status']=='PASS' for r in n['outcomes'])
assert n['all_passed'] and not n['static_audit']['errors'] and not n['runtime_capability_violations']
assert n['zero_network']['actual_network_events']==n['zero_network']['trapped_workload_calls']==[]
assert n['zero_network']['dns_http_socket_traps']==12
counts={}
for root in roots[:2]:
 count=0; scenarios=0
 for f in root.glob('*/terminal.json'):
  scenarios+=1;t=json.loads(f.read_bytes());assert t['source_verdict']=='insufficient_evidence'
  assert digest({k:v for k,v in t.items() if k!='evidence_hash'})==t['evidence_hash']
  previous='0'*64;auths={}
  for seq in range(1,t['ledger_count']+1):
   p=f.parent/f'event-{seq:04d}.json';b=p.read_bytes();r=json.loads(b)
   assert b==canonical(r) and r['sequence']==seq and r['previous']==previous
   previous=digest({k:v for k,v in r.items() if k!='hash'});assert previous==r['hash'];count+=1
   if r['event']=='authorize':auths[r['hash']]=r['state']['request_intent']
  assert previous==t['ledger_hash'] and r['event']=='terminal_checkpoint'
  if t['kind']=='typed-acquisition-candidate-v5':
   assert t['scanner_status']=='pending' and t['license_review_status']=='manual_review'
   assert t['role_contract_sha256']==v['role_contract_sha256']
   for m in t['manifest']:
    b=(f.parent/m['evidence_file']).read_bytes();assert sha(b)==m['evidence_sha256'];body=json.loads(b);text=body['text'].encode('utf-8')
    assert sha(text)==m['sha256'] and len(text)==m['bytes']
    assert hashlib.sha1(b'blob '+str(len(text)).encode()+b'\0'+text).hexdigest()==m['blob_sha']
    assert m['role']==body['role']==auths[m['authorization']]['role']
    assert (m['path']=='LICENSE')==(m['role']=='license_text')
   assert all(e['source']!='LICENSE' for e in t['edges'])
 assert count==720 and scenarios==25;counts[root.name]={'ledger_records':count,'scenarios':scenarios}
original=0;new=0
for p in (L/'tests').glob('test_*.py'):
 count=sum(isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name.startswith('test_') for n in ast.walk(ast.parse(p.read_text())))
 if p.name=='test_content_routing.py':new+=count
 else:original+=count
assert (original,new)==(112,20)
assert subprocess.check_output(['git','-C',str(V),'status','--porcelain'])==b''
r={'result':'PASS','independent_root':str(L),'tests_per_run':132,'inherited_tests':original,'new_tests':new,'test_subtest_outcomes_per_run':761,'all_passed_no_skips':True,'byte_identical_json_across_all_four_runs':962,'normalized_sha256':sha(raw),'independently_rehashed':counts,'candidate_bundle_unchanged':v['bundle_sha256'],'zero_network':n['zero_network'],'source_verdict':'insufficient_evidence','methods':['Reviewed candidate recalculate.py without imports, executed on independent pair','Leader separately authored hash/role/ledger and four-run identity verification'],'commands':['python3 -B verify.py leader-a','python3 -B verify.py leader-b','python3 -B recalculate.py leader-a leader-b']}
(O/'CP2-ASR-LICENSE-TEXT-ROUTING-REPAIR-001-runs.json').write_bytes(canonical(r));print(json.dumps(r,indent=2))
