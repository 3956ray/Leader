"""Read-only independent verification of this new run; no acquisition imports."""
import os, stat, pathlib, json, hashlib, base64, collections
ROOT=pathlib.Path('/private/tmp/think-acquisition-v8-driver-w125vAFT')
RUN=pathlib.Path('/private/tmp/think-acquisition-v8-quarantine-3_hb53be/source_v8_once')
def can(v): return (json.dumps(v,sort_keys=True,ensure_ascii=True,separators=(',',':'),allow_nan=False)+'\n').encode('ascii')
def sha(b): return hashlib.sha256(b).hexdigest()
def dig(v): return sha(can(v))
def dirfd(path):
 fd=os.open('/',os.O_RDONLY|os.O_DIRECTORY)
 for part in path.parts[1:]:
  child=os.open(part,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=fd);os.close(fd);fd=child
 return fd
fd=dirfd(RUN); assert stat.S_IMODE(os.fstat(fd).st_mode)==0o700
inventory=[]; rawfiles={}; objects={}
for name in sorted(os.listdir(fd)):
 f=os.open(name,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK,dir_fd=fd)
 try:
  s=os.fstat(f); assert stat.S_ISREG(s.st_mode) and s.st_nlink==1 and stat.S_IMODE(s.st_mode)==0o600 and s.st_size<=6*1048576+4096
  chunks=[];remain=s.st_size+1
  while remain:
   b=os.read(f,min(remain,65536))
   if not b: break
   chunks.append(b);remain-=len(b)
  b=b''.join(chunks);z=os.fstat(f)
  assert (s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns,s.st_ctime_ns)==(z.st_dev,z.st_ino,z.st_size,z.st_mtime_ns,z.st_ctime_ns) and len(b)==s.st_size
 finally: os.close(f)
 inventory.append(dict(path=name,bytes=len(b),sha256=sha(b),mode='0600',regular=True,nlink=1,nofollow=True,stable_fd=True))
 rawfiles[name]=b
 if not name.startswith('.pending-'):
  v=json.loads(b);assert can(v)==b;objects[name]=v
os.close(fd)
t=objects['terminal.json']; assert dig({k:v for k,v in t.items() if k!='evidence_hash'})==t['evidence_hash']
events=[objects['event-%04d.json'%i] for i in range(1,t['ledger_count']+1)]
assert len([n for n in objects if n.startswith('event-')])==len(events)
previous='0'*64
for i,e in enumerate(events,1):
 assert e['sequence']==i and e['previous']==previous and dig({k:v for k,v in e.items() if k!='hash'})==e['hash'];previous=e['hash']
assert previous==t['ledger_hash'] and events[-1]['event']=='terminal_checkpoint'
assert all(t[k]==v for k,v in events[-1]['state'].items())
byhash={e['hash']:e for e in events}
def archive(d):
 out=[]
 for x in d['parts']:
  assert sha(rawfiles[x['file']])==x['sha256'];o=objects[x['file']]
  b=base64.b64decode(o['content'],validate=True)
  assert o['encoding']=='base64' and len(b)==o['bytes']==x['bytes'] and len(b)<=48000 and sha(b)==o['sha256'];out.append(b)
 b=b''.join(out);assert len(b)==d['bytes'] and sha(b)==d['sha256']
 return b
metadata={}
for d in t.get('metadata_imports',[]):
 b=archive(d['archive']);assert d['verified'] and sha(b)==d['sha256'] and len(b)==d['bytes'];metadata[d['kind']]=json.loads(b)
index={e['path']:e for e in metadata.get('tree',{}).get('tree',[])}
package=json.loads(archive(t['manual_package_archive'])) if 'manual_package_archive' in t else None
bodymap={};bodies=[]
for m in t['manifest']:
 assert sha(rawfiles[m['evidence_file']])==m['evidence_sha256'];o=objects[m['evidence_file']];b=o['text'].encode('utf8')
 assert all(o[k]==m[k] for k in ('path','blob_sha','sha256','bytes','role','authorization'))
 assert len(b)==m['bytes'] and sha(b)==m['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==m['blob_sha']
 assert index[m['path']]['sha']==m['blob_sha'] and index[m['path']]['size']==len(b)
 bodymap[m['path']]=b;bodies.append(m)
assert len(bodies)==t['body_files'] and sum(m['bytes'] for m in bodies)==t['body_bytes']
requests=[]
for i,c in enumerate(t['calls'],1):
 a=byhash[c['authorization']];q=byhash[c['checkpoint']];intent=a['state']['request_intent'];entry=index[c['path']]
 assert a['event']=='authorize' and q['event']=='before_request' and q['sequence']==a['sequence']+1
 assert q['previous']==a['hash'] and q['state']['last_authorization']['record_hash']==a['hash']
 assert intent['path']==c['path'] and intent['sha']==c['sha']==entry['sha'] and intent['expected_size']==entry['size']
 assert entry['type']=='blob' and entry['mode']=='100644'
 assert c['host']=='api.github.com' and c['endpoint']=='/repos/k2-fsa/sherpa-onnx/git/blobs/'+c['sha']
 assert intent['pre_files']<96 and intent['pre_bytes']+entry['size']<=1048576
 assert intent['role']==('license_text' if c['path']=='LICENSE' else 'cpp_source_header')
 requests.append(dict(number=i,**c,**{k:intent[k] for k in ('role','role_origin','expected_size','pre_files','pre_bytes')},authorize_sequence=a['sequence'],before_request_sequence=q['sequence'],before_raw_bytes=q['state']['raw_bytes'],retained=any(m['path']==c['path'] for m in bodies)))
assert len(set(c['authorization'] for c in t['calls']))==len(t['calls'])
assert len([e for e in events if e['event']=='before_request'])==len(requests)
analyses=[];reports={}
for a in t['source_analyses']:
 raw=archive(a['archive']);assert sha(raw)==a['report_sha256'];r=json.loads(raw);assert can(r)==raw
 b=bodymap[r['source']];assert base64.b64decode(r['body_base64'],validate=True)==b
 assert sha(b)==r['body_sha256'] and len(b)==r['bytes']
 for ln in r['lines']:
  for k in ('sha256','line_sha256'):
   if k in ln: assert sha(b[ln['start']:ln['end']])==ln[k]
 reports[r['source']]=r
 analyses.append(dict(source=r['source'],report_sha256=a['report_sha256'],decision=r['decision'],guard=r['guard'],capability_review_status=r['capability_review_status'],analysis_complete=r['analysis_complete'],persistence_complete=a['persistence_complete'],lexical_issues=r['lexical_issues'],directive_issues=r['directive_issues'],file_safety_issues=r['file_safety_issues'],edge_classifications=dict(collections.Counter(e['classification'] for e in r['edges'])),capabilities=[{k:e[k] for k in ('classification','rule','detector','line','start','end','evidence_sha256') if k in e} for e in r['capabilities']]))
adjudications=[]
for entry in t.get('manual_capability_adjudications',[]):
 o=objects[entry['file']];assert sha(rawfiles[entry['file']])==entry['sha256']
 if o['domain']=='think-manual-adjudication-v8':
  source=entry['source'];r=reports[source];b=bodymap[source]
  assert o['original_report_sha256']==dig(r) and o['occurrences']==package['representation']['occurrences']
  mentions=[e for e in r['capabilities'] if e['classification']=='comment_capability_mention'];assert len(mentions)==len(o['occurrences'])
  for e,row in zip(mentions,o['occurrences']):
   ident=row['identity'];ln=r['lines'][e['line']-1];physical=b[ln['start']:ln['end']];historic=physical[:-2] if physical.endswith(b'\r\n') else physical[:-1] if physical.endswith(b'\n') else physical
   assert sha(physical)==ident['physical_line_sha256'] and sha(historic)==ident['historical_line_sha256']
   assert (e['line'],ln['start'],ln['end'],e['start'],e['end'],e['rule'],e['detector'],b[e['start']:e['end']].decode())==(ident['line'],ident['line_start'],ident['line_end'],ident['token_start'],ident['token_end'],ident['rule'],ident['detector'],ident['raw_token'])
   assert dig(ident)==row['occurrence_id']
  for k,p in [('execution_release_freeze','F'),('authority_map','M'),('acquisition_authorization','A'),('historical_context','H'),('commitment','K')]: assert o[k]==dig(package[p])
  assert o['input_hash']==t['input_hash'] and o['trusted_pins']==dig(t['manual_authority']['T'])
  assert o['new_run_identity']==dig(dict(domain='think-manual-N-v8',version=8,F=dig(package['F']),M=dig(package['M']),T=dig(t['manual_authority']['T']),input_hash=t['input_hash']))
  m=next(m for m in bodies if m['path']==source);assert o['execution_envelope']['sha256']==m['evidence_sha256'] and o['execution_envelope']['file']==m['evidence_file']
 adjudications.append({k:v for k,v in o.items() if k!='occurrences'} | dict(file=entry['file'],file_sha256=entry['sha256'],occurrence_ids=[row['occurrence_id'] for row in o.get('occurrences',[])]))
summary=dict(verification='PASS',run_path=str(RUN),inventory=inventory,inventory_collection_sha256=dig(inventory),file_count=len(inventory),total_bytes=sum(x['bytes'] for x in inventory),file_groups=dict(collections.Counter('event' if n.startswith('event-') else 'body' if n.startswith('body-') else 'metadata' if n.startswith('metadata-') else 'source_analysis' if n.startswith('source-analysis-') else 'adjudication' if n.startswith('manual-adjudication-') else 'package' if n.startswith('manual-package-') else 'pending' if n.startswith('.pending-') else 'terminal' if n=='terminal.json' else 'other' for n in rawfiles)),requests=requests,bodies=bodies,source_analyses=analyses,adjudications=adjudications,terminal={k:v for k,v in t.items() if k not in ('edges','source_analyses','manifest','calls','manual_package_archive','metadata_imports')},event_summary=[dict(sequence=e['sequence'],event=e['event'],hash=e['hash'],previous=e['previous']) for e in events],raw_metadata_count=len(metadata),metadata_tree_records=len(index),pending_files=[n for n in rawfiles if n.startswith('.pending-')])
# This output is derived; no body text, base64 or original raw scanner context.
print(json.dumps(summary,sort_keys=True,separators=(',',':')))
