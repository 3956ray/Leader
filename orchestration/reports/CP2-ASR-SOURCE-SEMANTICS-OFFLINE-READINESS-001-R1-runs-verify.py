import json,hashlib,stat,ast,subprocess
from pathlib import Path
O=Path('/Users/orderly_ray/Leader/orchestration/reports'); V=Path('/Users/orderly_ray/Projects/think/tools/asr_review_acquisition_v6'); L=Path('/private/tmp/think-leader-v6r1-8r48_6ia')
def canonical(o):return (json.dumps(o,sort_keys=True,ensure_ascii=True,separators=(',',':'),allow_nan=False)+'\n').encode('ascii')
def sha(raw):return hashlib.sha256(raw).hexdigest()
def digest(o):return sha(canonical(o))
v=json.loads((O/'CP2-ASR-SOURCE-SEMANTICS-OFFLINE-READINESS-001-R1-identity.json').read_bytes())
for r in v['bundle_records']:
 assert sha((V/r['path']).read_bytes())==r['sha256']==sha((L/r['path']).read_bytes())
roots=[L/'evidence/leader-r1-a',L/'evidence/leader-r1-b',V/'evidence/run-r1-a',V/'evidence/run-r1-b']
names={p.relative_to(roots[0]).as_posix() for p in roots[0].rglob('*.json') if p.name!='tests-log.json'}
assert len(names)==5432
for root in roots:
 assert {p.relative_to(root).as_posix() for p in root.rglob('*.json') if p.name!='tests-log.json'}==names
 for rel in names:assert (root/rel).read_bytes()==(roots[0]/rel).read_bytes()
raw=(roots[0]/'normalized.json').read_bytes();n=json.loads(raw)
assert sha(raw)=='2b32965a3fd400d688abb9ba32027db481ff9c48c6db305b225587533bdfd1ea'
assert n['tests_run']==158 and len(n['outcomes'])==961 and all(r['status']=='PASS' for r in n['outcomes'])
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
  if t['kind']=='typed-acquisition-candidate-v6':
   assert t['scanner_status']=='pending' and t['license_review_status']=='manual_review'
   assert t['role_contract_sha256']=='1c8a95b48c034e830b2a0a545192c691af12127774152921e1df73c6ee670125'
   for m in t['manifest']:
    b=(f.parent/m['evidence_file']).read_bytes();assert sha(b)==m['evidence_sha256'];body=json.loads(b);text=body['text'].encode('utf-8')
    assert sha(text)==m['sha256'] and len(text)==m['bytes']
    assert hashlib.sha1(b'blob '+str(len(text)).encode()+b'\0'+text).hexdigest()==m['blob_sha']
    assert m['role']==body['role']==auths[m['authorization']]['role']
    assert (m['path']=='LICENSE')==(m['role']=='license_text')
   assert all(e['source']!='LICENSE' for e in t['edges'])
 assert count==3628 and scenarios==133;counts[root.name]={'ledger_records':count,'scenarios':scenarios}
original=132;new=26
delivery=json.loads((V/'evidence/delivery.json').read_bytes())
terminals={**n['scenarios'],**{name:case['terminal'] for name,case in n['acquisition'].items()}}
collections={}
for key,fields in [('ledger_collection_sha256',['ledger_count','ledger_hash']),('terminal_collection_sha256',['evidence_hash'])]:
 records=[{'scenario':name,**{field:t[field] for field in fields}} for name,t in sorted(terminals.items())]
 collections[key]=digest(records);assert collections[key]==delivery['collections'][key]
collections['source_analysis_collection_sha256']=digest([{'scenario':name,'reports':t['source_analyses']} for name,t in sorted(terminals.items())]);assert collections['source_analysis_collection_sha256']==delivery['collections']['source_analysis_collection_sha256']
for rel,h in delivery['evidence_sha256'].items():assert sha((V/rel).read_bytes())==h
assert subprocess.check_output(['git','-C',str(V),'status','--porcelain'])==b''
r={'result':'PASS','independent_root':str(L),'tests_per_run':158,'inherited_tests':original,'new_tests':new,'test_subtest_outcomes_per_run':961,'all_passed_no_skips':True,'byte_identical_json_across_all_four_runs':5432,'normalized_sha256':sha(raw),'independently_rehashed':counts,'collections':collections,'candidate_bundle_unchanged':v['bundle_sha256'],'zero_network':n['zero_network'],'source_verdict':'insufficient_evidence','methods':['Reviewed candidate recalculate.py without imports, executed on independent pair','Leader separately authored hash/role/ledger and four-run identity verification'],'commands':['python3 -B verify.py leader-r1-a','python3 -B verify.py leader-r1-b','python3 -B recalculate.py leader-r1-a leader-r1-b']}
(O/'CP2-ASR-SOURCE-SEMANTICS-OFFLINE-READINESS-001-R1-runs.json').write_bytes(canonical(r));print(json.dumps(r,indent=2))
