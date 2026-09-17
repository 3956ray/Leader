from pathlib import Path
import os,stat,json,hashlib,base64,subprocess,ast,collections,re
R=Path('/Users/orderly_ray/Projects/think');D=R/'doc/security-reviews/sherpa-onnx-narrow-source-acquisition-v5/2026-09-06';P=Path('/private/tmp/think-asr-v5-acquisition-hqssnorn');V=R/'tools/asr_review_acquisition_v5';O=Path('/Users/orderly_ray/Leader/orchestration/reports')
sha=lambda b:hashlib.sha256(b).hexdigest();canon=lambda o:(json.dumps(o,ensure_ascii=True,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode('ascii');digest=lambda o:sha(canon(o));git=lambda *a:subprocess.check_output(['git','-C',str(R),*a]).decode().strip()
def read(p):
 p=Path(p);assert p.is_relative_to(P) and '..' not in p.parts
 fd=os.open('/',os.O_RDONLY|os.O_DIRECTORY)
 try:
  for part in p.parts[1:-1]:
   nxt=os.open(part,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=fd);os.close(fd);fd=nxt
  item=os.open(p.name,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK,dir_fd=fd)
  try:
   s=os.fstat(item);assert stat.S_ISREG(s.st_mode) and s.st_nlink==1 and s.st_size<=8388608
   parts=[];n=0
   while True:
    b=os.read(item,min(65536,s.st_size+1-n))
    if not b:break
    parts.append(b);n+=len(b);assert n<=s.st_size
   assert n==s.st_size;return b''.join(parts),s
  finally:os.close(item)
 finally:os.close(fd)
e=json.loads((D/'acquisition.json').read_bytes());inv=json.loads((D/'private-evidence-manifest.json').read_bytes());inspect=e['inspection']
assert len(inv['records'])==inv['files']==100 and digest(inv['records'])==inv['records_sha256']=='aad379247571ad3dd1f45e09411669b1c83e06372928d50a7ced17922c8f4ba3'
found=set()
for root,dirs,files in os.walk(P,followlinks=False):
 s=Path(root).lstat();assert stat.S_ISDIR(s.st_mode) and stat.S_IMODE(s.st_mode)==0o700
 for name in dirs:assert stat.S_ISDIR((Path(root)/name).lstat().st_mode)
 found.update((Path(root)/name).relative_to(P).as_posix() for name in files)
assert found=={r['path'] for r in inv['records']}
for r in inv['records']:
 raw,s=read(P/r['path']);assert sha(raw)==r['sha256'] and len(raw)==r['bytes'];assert format(stat.S_IMODE(s.st_mode),'04o')==r['mode']=='0600'
raw,_=read(P/'run/terminal.json');t=json.loads(raw);assert raw==canon(t) and sha(raw)==inspect['terminal_file_sha256'];assert digest({k:v for k,v in t.items() if k!='evidence_hash'})==t['evidence_hash']==inspect['terminal_evidence_hash']
records=[];previous='0'*64
for seq in range(1,t['ledger_count']+1):
 raw,_=read(P/'run'/f'event-{seq:04d}.json');r=json.loads(raw);assert raw==canon(r) and len(raw)<=2000000 and len(canon(r['state']))<=1000000
 assert r['sequence']==seq and r['previous']==previous;previous=digest({k:v for k,v in r.items() if k!='hash'});assert previous==r['hash'];records.append(r)
assert len(records)==22 and previous==t['ledger_hash']==inspect['ledger_hash'];assert records[-1]['event']=='terminal_checkpoint'
assert [{'event':r['event'],'hash':r['hash'],'sequence':r['sequence']} for r in records]==inspect['ledger_events']
auths=[r for r in records if r['event']=='authorize'];assert len(auths)==len(t['calls'])==len(t['manifest'])==2
assert sum(r['event']=='metadata_verified' for r in records[:10])==2
input_raw,_=read(P/'input.json');inp=json.loads(input_raw);assert input_raw==canon(inp) and len(input_raw)==2603 and sha(input_raw)==t['input_hash']=='a6ec55dd0ff07d4cceab430bdc09cca05d98dea5307fb139cb700da398d76b61'
f=json.loads((R/'doc/security-reviews/asr-acquisition-v5-release-freeze/2026-09-06/freeze.json').read_bytes());assert inp['schema']==5 and inp['policy']==f['policy'];assert t['policy_hash']==digest(inp['policy'])==f['policy_sha256'];assert t['release_hash']==f['accepted_release']['code_schema_test_bundle_sha256'];assert t['role_contract_sha256']==digest(f['content_roles'])
bodies=[]
for n,(call,auth,m,summary) in enumerate(zip(t['calls'],auths,t['manifest'],inspect['requests'])):
 checkpoint=records[auth['sequence']];intent=auth['state']['request_intent'];assert checkpoint['event']=='before_request' and checkpoint['state']['last_authorization']['record_hash']==auth['hash']
 assert call['authorization']==auth['hash']==m['authorization'] and call['checkpoint']==checkpoint['hash'];assert call['path']==m['path']==intent['path']==f['policy']['seeds'][n]
 assert call['host']=='api.github.com' and call['endpoint']=='/repos/k2-fsa/sherpa-onnx/git/blobs/'+call['sha'];assert call['sha']==m['blob_sha']==intent['sha']
 assert intent['role_origin']=='seed' and intent['role']==m['role']==f['content_roles']['seeds'][m['path']] and intent['role_contract_sha256']==t['role_contract_sha256']
 assert auth['state']['body_files']==n and auth['state']['body_bytes']==sum(len(b) for b in bodies)
 raw,_=read(P/'run'/m['evidence_file']);b=json.loads(raw);assert raw==canon(b) and sha(raw)==m['evidence_sha256'];body=b['text'].encode('utf-8');assert b'\0' not in body and len(body)==m['bytes'] and sha(body)==m['sha256'];assert hashlib.sha1(b'blob '+str(len(body)).encode()+b'\0'+body).hexdigest()==m['blob_sha']
 for k in ['path','blob_sha','sha256','bytes','authorization','role']:assert b[k]==m[k]
 assert summary['body']==m and summary['authorization_sequence']==auth['sequence'];bodies.append(body)
assert [len(b) for b in bodies]==[11358,7939];assert len(t['text_reviews'])==1 and t['text_reviews'][0]['path']=='LICENSE' and all(x['source']!='LICENSE' for x in t['edges'])
assert sum(r['event']=='text_review_pending' for r in records)==1
parts_count=0
for meta in t['metadata_imports']:
 values=[]
 for part in meta['archive']['parts']:
  raw,_=read(P/'run'/part['file']);assert sha(raw)==part['sha256'];o=json.loads(raw);v=base64.b64decode(o['content'],validate=True);assert len(v)==part['bytes']==o['bytes'] and len(v)<=48000 and sha(v)==o['sha256'];values.append(v);parts_count+=1
 raw=b''.join(values);original,_=read(P/'identity-inputs'/(meta['kind']+'.json'));assert raw==original and sha(raw)==meta['sha256']==meta['archive']['sha256'];assert len(raw)==meta['bytes']==meta['archive']['bytes'] and meta['verified'] and meta['archive']['complete']
 assert {'bytes':len(raw),'sha256':sha(raw)}==inp['metadata'][meta['kind']]
assert parts_count==59
tree=json.loads(read(P/'identity-inputs/tree.json')[0]);entries={x['path']:x for x in tree['tree']};assert len(entries)==len(tree['tree'])==8585 and tree['sha']==f['policy']['tree']
for call,m in zip(t['calls'],t['manifest']):
 ent=entries[call['path']];assert (ent['sha'],ent['size'],ent['mode'],ent['type'])==(call['sha'],m['bytes'],'100644','blob')
assert t['body_files']==2 and t['body_bytes']==19297 and t['blob_raw_bytes']==27161 and t['raw_bytes']==2771747==27161+sum(x['bytes'] for x in t['metadata_imports'])
assert t['stop_reason']=='denylist_capability' and not t['fixed_point'] and t['source_verdict']=='insufficient_evidence' and t['scanner_status']=='pending' and t['license_review_status']=='manual_review'
assert t['pending_seeds']==f['policy']['seeds'][2:] and not t['pending_internal'] and not t['persistence_errors'];assert len(t['edges'])==16 and dict(collections.Counter(x['classification'] for x in t['edges']))==inspect['edge_classification_counts']
lines=bodies[1].decode().splitlines();assert all(lines[i-1].lstrip().startswith('//') and 'websocket' in lines[i-1].lower() for i in [57,60])
for r in inspect['denylist_source_context']:assert sha(lines[r['line']-1].encode())==r['line_sha256']
assert [x for x in t['edges'] if x['classification'] in ('conditional','unsupported_directive')]==inspect['cpp_stop_directives']
assert lines[4].startswith('#ifndef ') and lines[5].startswith('#define ') and lines[241].startswith('#endif')
for key,path in [('preflight_sha256','preflight.json'),('pre_body_empty_proof_sha256','empty-output-before-body.json'),('attempt_marker_sha256','attempt-started.json'),('invocation_result_sha256','invocation-result.json')]:assert sha(read(P/path)[0])==e[key]
assert json.loads(read(P/'empty-output-before-body.json')[0])==e['pre_body_empty_proof'] and e['pre_body_empty_proof']['entries']==[]
assert json.loads(read(P/'preflight.json')[0])==e['preflight']
for path,h in e['preflight']['source_authorities'].items():assert sha(Path(path).read_bytes())==h
code=Path(e['driver']['path']).read_bytes();assert sha(code)==e['driver']['sha256'];a=ast.parse(code);calls=[x for x in ast.walk(a) if isinstance(x,ast.Call) and isinstance(x.func,ast.Name) and x.func.id=='run_input'];assert len(calls)==1 and len(calls[0].args)==5 and not calls[0].keywords
scans={}
for kind,s in inspect['scans'].items():
 raw,_=read(s['path']);assert sha(raw)==s['sha256'];scan=json.loads(raw);assert scan['verdict']==s['verdict'] and scan['risk_score']==s['risk_score'] and scan['stats']==s['stats'] and not scan['block_signals'];assert all(scan['stats'][k]==0 for k in ['skipped_large','skipped_limit','unreadable','binary_files'])
 assert len(scan['findings'])==len(s['findings'])
 for rawfinding,context in zip(scan['findings'],s['findings']):
  for k in ['rule_id','path','line','severity']:assert rawfinding[k]==context[k]
  text=read(P/'identity-inputs'/context['path'])[0].decode();line=text.splitlines()[context['line']-1];assert sha(line.encode())==context['source_line_sha256']
  if context['path']=='tree.json':assert re.search(r'[0-9a-f]{40}',line)
  else:assert 'payload' in line and '8085' in line
 scans[kind]={'verdict':scan['verdict'],'score':scan['risk_score'],'findings':len(scan['findings'])}
head='5dbfe9ad300a8750cf2f76588983a7069760f200';assert git('rev-parse','HEAD')==head and git('rev-parse','HEAD^')==e['baseline_commit'] and not git('status','--porcelain');git('show','--check','--format=',head)
expected={'REPORT.md':'e68fa66b5f4fcc2e3145212435b2fa18407ce100c8ad06cbb3b5e9b59e99102f','acquisition.json':'98a09576a41139917f123792d8928b42f35d83199272cad5f9ab289f9137be5f','private-evidence-manifest.json':'bc3d650e84a20be59c574a7d79d0c86cc515119cbbacdc0c4064259359abe6d5','MANIFEST.json':'7d25fbc4226dbde2301779f36c94a0f9017eaa53d14611064235a6f11ae31c82'}
assert set(git('diff-tree','--no-commit-id','--name-status','-r',head).splitlines())=={'A\t'+(D/name).relative_to(R).as_posix() for name in expected}
for name,h in expected.items():
 raw=(D/name).read_bytes();assert sha(raw)==h;assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==git('rev-parse','HEAD:'+(D/name).relative_to(R).as_posix())
fm=json.loads((R/'doc/security-reviews/asr-acquisition-v5-release-freeze/2026-09-06/MANIFEST.json').read_bytes())
for x in fm['artifact_files']:assert sha((V/x['path']).read_bytes())==x['sha256']
for x in f['verification_this_task']['readonly_trees']:assert git('rev-parse','HEAD:'+x['path'])==x['git_tree']
r={'RESULT':'PASS','commit':head,'private_files_verified':100,'ledger_records':22,'metadata_parts':59,'request_count':2,'body_bytes':19297,'blob_raw_bytes_recorded':27161,'total_raw_bytes_recorded':2771747,'license_text_routing_verified':True,'stop_reason':'denylist_capability','deny_rule':'websocket','deny_context':'line comments57/60, not reachable-capability proof','additional_independent_stops':'include guard5/242 and define6; frozen semantic expansion prohibited','internal_edges_unfetched':9,'remaining_seeds':7,'no_successor_authorization':True,'fixed_point':False,'source_verdict':'insufficient_evidence','scans':scans,'frozen_files_rehashed':1966,'git_boundary_clean':True,'driver_single_default_entry_call_verified_statically':True,'wire_limit':'No original blob API JSON/HTTP headers retained; body identity, metadata and ledger verified but network transcript/individual wire fields cannot be independently replayed.','third_party_execution':False,'old_corpus_or_body_read':False}
(O/'CP2-ASR-NARROW-SOURCE-ACQUISITION-V5-001-verification.json').write_bytes(canon(r));print(json.dumps(r,indent=2))
