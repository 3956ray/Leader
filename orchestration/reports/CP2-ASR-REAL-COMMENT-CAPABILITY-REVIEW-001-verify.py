import os,stat,json,hashlib
from pathlib import Path
O=Path('/Users/orderly_ray/Leader/orchestration/reports');r=json.loads((O/'CP2-ASR-REAL-COMMENT-REVIEW-AUTHORIZATION-001.json').read_text());b=r['binding'];sha=lambda x:hashlib.sha256(x).hexdigest()
assert sha((O/'CP2-ASR-REAL-COMMENT-REVIEW-AUTHORIZATION-001.json').read_bytes())=='c66a9fe77a77e15ca6dfa8f958f47ac1de4e1816de52779add3b9eee497163c7'
assert sha(Path('/Users/orderly_ray/Projects/think/doc/cp2-source-semantics-readiness-decision-2026-09-06.md').read_bytes())==r['formal_decision_sha256']
a=json.loads((O/'CP2-ASR-REAL-COMMENT-REVIEW-AUTHORIZATION-001-approved.json').read_text());assert a['user_response']=='批准' and a['binding']==b
path=Path(b['private_envelope']);fd=os.open('/',os.O_RDONLY|os.O_DIRECTORY);checked=[]
try:
 for part in path.parts[1:-1]:
  child=os.open(part,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=fd);os.close(fd);fd=child;s=os.fstat(fd);assert stat.S_ISDIR(s.st_mode)
  if part in ('think-asr-v5-acquisition-hqssnorn','run'):assert stat.S_IMODE(s.st_mode)==0o700
  checked.append({'component':part,'directory':True,'nofollow':True,'mode':oct(stat.S_IMODE(s.st_mode))})
 child=os.open(path.name,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK,dir_fd=fd)
 try:
  s=os.fstat(child);assert stat.S_ISREG(s.st_mode) and s.st_nlink==1 and stat.S_IMODE(s.st_mode)==0o600 and s.st_size==b['envelope_bytes']
  raw=os.read(child,b['envelope_bytes']+1);assert len(raw)==b['envelope_bytes'] and os.read(child,1)==b'';assert sha(raw)==b['envelope_sha256']
 finally:os.close(child)
finally:os.close(fd)
obj=json.loads(raw);body=obj['text'].encode('utf-8');assert b'\0' not in body and len(body)==b['body_bytes'] and sha(body)==b['body_sha256'];assert hashlib.sha1(b'blob '+str(len(body)).encode()+b'\0'+body).hexdigest()==b['git_blob_sha1'];assert obj['path']==b['source_path'] and obj['role']=='cpp_source_header' and obj['sha256']==b['body_sha256'] and obj['blob_sha']==b['git_blob_sha1'] and obj['bytes']==len(body)
plain=obj['text'].splitlines();physical=body.splitlines(keepends=True);assert len(plain)==len(physical)
targets=[]
for target in b['targets']:
 n=target['line'];line=plain[n-1];assert sha(line.encode())==target['line_sha256'];start=sum(len(x) for x in physical[:n-1]);segment=physical[n-1];hit=segment.lower().index(b'websocket');assert line.lstrip().startswith('//');assert segment.lower().count(b'websocket')==1
 targets.append({**target,'rule':'websocket','physical_line_sha256':sha(segment),'line_byte_start':start,'line_byte_end':start+len(segment),'token_byte_start':start+hit,'token_byte_end':start+hit+9,'line_starts_with_comment_marker':True,'ends_with_continuation':segment.rstrip(b'\r\n').endswith(b'\\')})
result={'RESULT':'PASS','binding':b,'directory_chain':checked,'private_files_read':1,'body_envelope_regular_singlelink_0600':True,'body_and_blob_hashes_verified':True,'line_count':len(plain),'targets':targets,'network_or_source_execution':False,'scope':'Byte identities and literal markers only; manual semantic adjudication is separate.'};(O/'CP2-ASR-REAL-COMMENT-CAPABILITY-REVIEW-001-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'RESULT':'PASS','targets':targets},indent=2));print('Authorized same-file context, lines1-82:')
for n,line in enumerate(plain[:82],1):print(f'{n}: {line}')
