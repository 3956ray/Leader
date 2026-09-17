import json,hashlib,re
from pathlib import Path
work=Path('/private/tmp/think-leader-v8-el98lnwd');prod=Path('/Users/orderly_ray/Projects/think/tools/asr_review_acquisition_v8');out=Path('/Users/orderly_ray/Leader/orchestration/reports')
def canon(x):return (json.dumps(x,sort_keys=True,ensure_ascii=True,separators=(',',':'),allow_nan=False)+'\n').encode()
def sha(b):return hashlib.sha256(b).hexdigest()
def digest(x):return sha(canon(x))
a=work/'evidence/leader-a';b=work/'evidence/leader-b';raw=(a/'normalized.json').read_bytes();n=json.loads(raw)
assert sha(raw)=='e4967828a929e199fc913c352d08fb17e081d04a618280d9bbc285cd26487664'
assert n['tests_run']==174 and len(n['outcomes'])==1338 and n['all_passed'] and n['skipped']==0
assert not n['zero_network']['actual_network_events'] and not n['zero_network']['trapped_workload_calls'] and not n['runtime_capability_violations']
old=json.loads((prod.parent/'asr_review_acquisition_v7/evidence/run-r1-a/normalized.json').read_bytes())['outcomes'];oldids={x['test'] for x in old};assert len(old)==1210 and [x for x in n['outcomes'] if x['test'] in oldids]==old
v6=json.loads((prod.parent/'asr_review_acquisition_v6/evidence/run-r1-a/normalized.json').read_bytes())['outcomes'];v6ids={x['test'] for x in v6};assert len(v6)==961 and [x for x in n['outcomes'] if x['test'] in v6ids]==v6
T=dict(n['scenarios']);T.update({k:v['terminal'] for k,v in n['acquisition'].items()});T.update({'manual-'+k:v['terminal'] for k,v in n['manual'].items()});assert len(T)==456
cols={
 'ledger_collection_sha256':digest([{'scenario':k,'ledger_hash':T[k]['ledger_hash'],'ledger_count':T[k]['ledger_count']} for k in sorted(T)]),
 'terminal_collection_sha256':digest([{'scenario':k,'evidence_hash':T[k]['evidence_hash']} for k in sorted(T)]),
 'source_analysis_collection_sha256':digest([{'scenario':k,'reports':T[k]['source_analyses']} for k in sorted(T)]),
 'adjudication_collection_sha256':digest([{'scenario':k,'records':T[k].get('manual_capability_adjudications',[])} for k in sorted(T)]),
 'authority_collection_sha256':digest([{'scenario':k,'authority':T[k].get('manual_authority')} for k in sorted(T)])}
expected=json.loads((prod/'evidence/delivery.json').read_bytes())['collections'];assert cols==expected,(cols,expected)
files={str(p.relative_to(a)):sha(p.read_bytes()) for p in a.rglob('*.json') if p.name!='tests-log.json'};assert len(files)==11571
for other in [b,prod/'evidence/run-a',prod/'evidence/run-b']:
 assert files=={str(p.relative_to(other)):sha(p.read_bytes()) for p in other.rglob('*.json') if p.name!='tests-log.json'}
pending=[{'path':str(p.relative_to(a)),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in sorted(a.rglob('.pending-*'))]
assert pending==json.loads((prod/'evidence/delivery.json').read_bytes())['paired_nonjson_partial_writes']
for other in [b,prod/'evidence/run-a',prod/'evidence/run-b']:
 assert pending==[{'path':str(p.relative_to(other)),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in sorted(other.rglob('.pending-*'))]
 assert len([p for p in other.rglob('*') if p.is_file() and p.name!='tests-log.json'])==11574
counts={}
for run in [a,b]:
 count=0
 for name,terminal in T.items():
  actual=json.loads((run/name/'terminal.json').read_bytes());assert actual==terminal and digest({k:v for k,v in terminal.items() if k!='evidence_hash'})==terminal['evidence_hash'];previous='0'*64
  for i in range(1,terminal['ledger_count']+1):
   rb=(run/name/f'event-{i:04d}.json').read_bytes();v=json.loads(rb);assert rb==canon(v) and v['sequence']==i and v['previous']==previous;assert digest({k:x for k,x in v.items() if k!='hash'})==v['hash'];previous=v['hash'];count+=1
  assert previous==terminal['ledger_hash'] and terminal['source_verdict']=='insufficient_evidence'
 counts[run.name]=count
assert set(counts.values())=={7071}
recalc=json.loads((work/'leader-recalculation.json').read_bytes());assert recalc['result']=='PASS' and recalc['recomputed_ledger_records']==counts
r={'RESULT':'PASS','candidate':'1fe85740a185a63ca4f35df2abd22ae410f82fbb','independent_directory':str(work),'tests_per_run':174,'outcomes_per_run':1338,'old_v7_outcomes_exact_equal':1210,'old_v6_outcomes_exact_equal':961,'skipped':0,'normalized_sha256':sha(raw),'immutable_json_files_identical_per_run_across_4_runs':len(files),'scenarios':456,'pending_files_four_run_equal':pending,'ledger_records_independently_rehashed':counts,'collections':cols,'zero_network':n['zero_network'],'candidate_independent_recalculator':recalc,'seconds':{key:float(re.search(r'Ran 174 tests in ([0-9.]+)s',(work/(key+'.log')).read_text()).group(1)) for key in ['leader-a','leader-b']},'scope':'Two Leader runs in new first-party-only directory; no real source/review/transport; source verdict remains insufficient_evidence.'}
(out/'CP2-ASR-REVIEW-TIMESTAMP-REPRESENTATION-OFFLINE-001-runs.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print(json.dumps(r))
