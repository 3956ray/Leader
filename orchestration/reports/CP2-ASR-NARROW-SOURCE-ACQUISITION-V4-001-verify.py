from pathlib import Path
import json,os,stat,hashlib,base64,subprocess,sys
R=Path('/Users/orderly_ray/Projects/think');D=R/'doc/security-reviews/sherpa-onnx-narrow-source-acquisition-v4/2026-09-06';P=Path('/private/tmp/think-asr-v4-acquisition-3sx4ux01');sha=lambda b:hashlib.sha256(b).hexdigest();canon=lambda x:(json.dumps(x,sort_keys=True,ensure_ascii=True,separators=(',',':'),allow_nan=False)+'\n').encode('ascii');digest=lambda x:sha(canon(x));g=lambda *a:subprocess.check_output(['git','-C',str(R),*a])
def read(p):
 p=Path(p);assert p.is_relative_to(P)
 fd=os.open('/',os.O_RDONLY|os.O_DIRECTORY)
 try:
  for part in p.parts[1:-1]:
   new=os.open(part,os.O_RDONLY|os.O_NOFOLLOW|os.O_DIRECTORY,dir_fd=fd);os.close(fd);fd=new
  f=os.open(p.name,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK,dir_fd=fd)
  try:
   s=os.fstat(f);assert stat.S_ISREG(s.st_mode) and s.st_nlink==1 and s.st_size<=8388608
   chunks=[];n=0
   while True:
    c=os.read(f,min(65536,s.st_size+1-n))
    if not c:break
    chunks.append(c);n+=len(c);assert n<=s.st_size
   raw=b''.join(chunks);assert len(raw)==s.st_size
   return raw,s
  finally:os.close(f)
 finally:os.close(fd)
e=json.loads((D/'acquisition-evidence.json').read_bytes());inventory=e['private_artifact_inventory'];assert inventory['count']==len(inventory['records'])==88 and digest(inventory['records'])==inventory['records_sha256']=='57c2e1bed3b591c4c2ec4fafd63da4b6fe4f7a974d3d0b4331c48a9289022d1c'
for x in inventory['records']:
 raw,s=read(x['path']);assert len(raw)==x['bytes'] and sha(raw)==x['sha256'] and format(stat.S_IMODE(s.st_mode),'04o')==x['mode']
raw,_=read(P/'run/terminal.json');t=json.loads(raw);assert sha(raw)==e['terminal']['file_sha256'];assert digest({k:v for k,v in t.items() if k!='evidence_hash'})==t['evidence_hash'];assert len(raw)<=2000000
records=[];prev='0'*64
for n in range(1,t['ledger_count']+1):
 raw,_=read(P/'run'/f'event-{n:04d}.json');x=json.loads(raw);assert raw==canon(x);assert len(raw)<=2000000 and len(canon(x['state']))<=1000000;assert x['sequence']==n and x['previous']==prev;assert digest({k:v for k,v in x.items() if k!='hash'})==x['hash'];prev=x['hash'];records.append(x)
assert len(records)==16 and prev==t['ledger_hash']==e['ledger']['final_hash'];assert [x['event'] for x in records[-6:]]==['authorize','before_request','body_preserved','verified','parsed','terminal_checkpoint'];assert len(t['calls'])==len(t['manifest'])==1;assert sum(x['event']=='authorize' for x in records)==1
call=t['calls'][0];auth=records[10];checkpoint=records[11];assert call['authorization']==auth['hash'] and call['checkpoint']==checkpoint['hash'];assert checkpoint['state']['last_authorization']['record_hash']==auth['hash'];assert auth['state']['request_intent']==e['request_intent'];assert auth['state']['body_files']==auth['state']['body_bytes']==0
assert call['path']=='LICENSE' and call['sha']=='d645695673349e3947e8e5ae42332d0ac3164cd7' and call['host']=='api.github.com' and call['endpoint']=='/repos/k2-fsa/sherpa-onnx/git/blobs/'+call['sha'];assert t['calls']==e['requests']
item=t['manifest'][0];raw,_=read(P/'run'/item['evidence_file']);b=json.loads(raw);assert raw==canon(b) and sha(raw)==item['evidence_sha256'];body=b['text'].encode('utf-8');assert b'\0' not in body and len(body)==11358==item['bytes'];assert sha(body)==item['sha256'];assert hashlib.sha1(b'blob '+str(len(body)).encode()+b'\0'+body).hexdigest()==item['blob_sha']==call['sha']
for k in ['path','blob_sha','sha256','bytes','authorization']:assert b[k]==item[k]
parts_count=0
for meta in t['metadata_imports']:
 parts=[]
 for part in meta['archive']['parts']:
  raw,_=read(P/'run'/part['file']);assert sha(raw)==part['sha256'];o=json.loads(raw);v=base64.b64decode(o['content'],validate=True);assert len(v)==part['bytes']==o['bytes'] and len(v)<=48000 and sha(v)==o['sha256'];parts.append(v);parts_count+=1
 v=b''.join(parts);original,_=read(P/'identity'/(meta['kind']+'.json'));assert v==original and sha(v)==meta['sha256']==meta['archive']['sha256'];assert len(v)==meta['bytes']==meta['archive']['bytes'] and meta['verified'] and meta['archive']['complete']
assert parts_count==59
raw,_=read(P/'identity/input.json');inp=json.loads(raw);assert raw==canon(inp) and len(raw)==2037 and sha(raw)==t['input_hash']=='baab9ddac779808ad8a1ac79e1c76937bc5875cba335148c7984aa54e41810a2';tree=json.loads(read(P/'identity/tree.json')[0]);entry=next(x for x in tree['tree'] if x['path']=='LICENSE');assert (entry['sha'],entry['mode'],entry['type'],entry['size'])==(call['sha'],'100644','blob',11358)
assert t['stop_reason']=='edge_unclosed_literal' and t['fixed_point'] is False and t['source_verdict']=='insufficient_evidence';assert len(t['pending_seeds'])==8 and not t['pending_internal'] and not t['persistence_errors'];assert t['body_files']==1 and t['body_bytes']==11358 and t['blob_raw_bytes']==15935 and t['raw_bytes']==2760521
assert e['before_call']['entries']==[];assert e['empty_root_proof']['entry_count']==0 and e['empty_root_proof']['empty_root_before_inputs']
scanrun=json.loads(read(P/'scan-run/scan-report.json')[0]);scanid=json.loads(read(P/'scan-identity/scan-report.json')[0]);assert scanrun['verdict']=='low_indicators' and not scanrun['findings'];old=json.loads(Path('/Users/orderly_ray/Leader/orchestration/reports/CP2-ASR-METADATA-PATH-COMPATIBILITY-REPAIR-001-scan/scan-report.json').read_bytes());assert scanid['findings']==old['findings'] and scanid['verdict']=='manual_review';assert all(x['stats'][k]==0 for x in [scanrun,scanid] for k in ['skipped_large','skipped_limit','unreadable'])
expected={'REPORT.md':'095b5b1c520fb9c2d5c5d5973289c2c46f03d2b7433462bc65cb311a770d0454','acquisition-evidence.json':'ecf5e19202e81ad7a47988eefa5479c2eb87e31622ef5b00c8d32dc5c7949a4b','scanner-review.json':'18ac7f2d36f4f28255d295be40cc4da5d65417dc26ba3fa559e5f448eb2bec41','MANIFEST.json':'9bd70eb815a473db8538cd2c0bebf6ea8db8ab855b4951cd71bfaa68df164cb2'}
assert g('rev-parse','HEAD').decode().strip()=='9aa40913c57cccd31105ac88385102f0a0758d63';assert g('rev-parse','HEAD^').decode().strip()=='2f4760d0ff3ea78de929198fba88d3744353a321';assert not g('status','--porcelain');assert set(g('diff-tree','--no-commit-id','--name-only','-r','HEAD').decode().splitlines())=={str((D/n).relative_to(R)) for n in expected}
for n,h in expected.items():assert sha((D/n).read_bytes())==h and (D/n).read_bytes()==g('show','HEAD:'+str((D/n).relative_to(R)))
f=json.loads((R/'doc/security-reviews/asr-acquisition-v4-release-freeze/2026-09-06/freeze.json').read_bytes());assert f['policy']==inp['policy'];m=json.loads((R/'doc/security-reviews/asr-acquisition-v4-release-freeze/2026-09-06/MANIFEST.json').read_bytes())
for x in m['artifact_files']:assert sha((R/x['path']).read_bytes())==x['sha256']
for p in ['tools/asr_review_offline_v2','tools/asr_review_acquisition_v3','tools/asr_review_acquisition_v4','doc/security-reviews/asr-acquisition-v3-release-freeze','doc/security-reviews/asr-acquisition-v4-release-freeze']:assert not g('diff','HEAD^','HEAD','--',p)
line=b['text'].splitlines()[182];assert "'" in line;print('LICENSE line 183 context:',line)
result={'RESULT':'PASS','private_files_rehashed':88,'ledger_records':16,'metadata_parts':59,'requests':1,'body_files':1,'decoded_bytes':11358,'blob_raw_bytes':15935,'total_raw_bytes':2760521,'stop_reason':t['stop_reason'],'fixed_point':False,'no_successor_authorization':True,'stop_line':183,'natural_language_apostrophe_confirmed':True,'frozen_file_hashes_verified':1024,'derived_commit':'9aa40913c57cccd31105ac88385102f0a0758d63','git_boundary_clean':True,'wire_evidence_limit':'Original blob API JSON/headers unavailable; no independent replay of wire fields. Body identity and ledger independently verified.','scanner_findings_unchanged':True,'source_verdict':'insufficient_evidence'}
Path('/Users/orderly_ray/Leader/orchestration/reports/CP2-ASR-NARROW-SOURCE-ACQUISITION-V4-001-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
