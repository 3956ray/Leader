"""Construct approved mapping; bounded two-metadata read and guarded pure validation only."""
import os,sys,stat,json,hashlib,subprocess,tempfile
from pathlib import Path
L=Path('/Users/orderly_ray/Leader');Q=Path('/Users/orderly_ray/Projects/think');R=L/'orchestration/reports'
ID='CP2-ASR-V8-SOURCE-AUTHORIZATION-MAPPING-001';OUT=R/(ID+'-artifacts')
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(v):return (json.dumps(v,sort_keys=True,ensure_ascii=True,allow_nan=False,separators=(',',':'))+'\n').encode('ascii')
def digest(v):return sha(canon(v))
def read(p):
 s=p.lstat();assert stat.S_ISREG(s.st_mode) and s.st_nlink==1 and all(stat.S_ISDIR(q.lstat().st_mode) for q in p.parents)
 return p.read_bytes()
def load(p):return json.loads(read(p))
def ref(p):b=read(p);return dict(path=str(p),bytes=len(b),sha256=sha(b))
def git(*a):return subprocess.check_output(['git','-C',str(Q),*a])
reqpath=R/'CP2-ASR-NARROW-SOURCE-ACQUISITION-V8-AUTHORIZATION-REQUEST-001.json';approvalpath=R/'CP2-ASR-NARROW-SOURCE-ACQUISITION-V8-AUTHORIZATION-001-approved.json'
assert sha(read(reqpath))=='2114259dc42837e96d938c65bce2b165ee47836623408c4377ffb8d11d5a392b'
assert sha(read(approvalpath))=='694c69bc465663cb2a8ba58e21c9757d131d6135956a92df00ed78f997979c81'
req=load(reqpath);approval=load(approvalpath);assert approval['RESULT']=='APPROVED' and approval['user_reply']=='\u6279\u51c6' and approval['attempts']==1
for row in req['references']+[approval['request'],approval['request_json']]:assert ref(Path(row['path']))==row
assert git('rev-parse','HEAD').decode().strip()==req['baseline_commit'] and not git('status','--porcelain=v1','--untracked-files=all')
fa=load(R/'CP2-ASR-EXECUTION-RELEASE-FREEZE-V8-001-acceptance.json');ma=load(R/'CP2-ASR-REVIEW-AUTHORITY-MAP-V8-001-acceptance.json');ka=load(R/'CP2-ASR-REVIEW-MAP-COMMITMENT-V8-001-R1-acceptance.json')
assert all(a['RESULT']=='ACCEPTED' for a in (fa,ma,ka))
freeze=load(Q/fa['output_directory']/'freeze.json');manifest=load(Q/fa['output_directory']/'MANIFEST.json')
assert len(manifest['files'])==69505 and digest(manifest['files'])==fa['product_input_collection_sha256']
tree={}
for line in git('ls-tree','-r','-z','HEAD').split(b'\0'):
 if line:
  desc,p=line.split(b'\t',1);tree[p.decode()]=tuple(desc.decode().split())
for row in manifest['files']:
 b=read(Q/row['path']);blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
 assert len(b)==row['bytes'] and sha(b)==row['sha256'] and blob==row['git_blob'] and tree[row['path']]==('100644','blob',blob)
for row in manifest['external_references']:assert ref(Path(row['path']))==row
assert len(manifest['external_references'])==33 and digest(manifest['external_references'])==fa['external_reference_collection_sha256']
for a in (fa,ma,ka):
 assert git('rev-parse','HEAD:'+a['output_directory']).decode().strip()==a['output_tree']
 for row in a['files']:
  b=read(Q/a['output_directory']/row['path']);assert len(b)==row['bytes'] and sha(b)==row['sha256']
C=req['accepted_C'];assert git('rev-parse','HEAD:'+C['root']).decode().strip()==C['tree']
bundle=freeze['candidate_bundle']['records'];assert len(bundle)==28 and digest(bundle)==C['bundle']
assert all(sha(read(Q/C['root']/row['path']))==row['sha256'] for row in bundle)
objects={name:load(Q/ka['output_directory']/(name+'.json')) for name in ('H','R','representation','K')}
objects['F']=load(Path(req['F']['file']['path']));objects['M']=load(Path(req['M']['file']['path']))
assert digest(objects['F'])==req['F']['file']['sha256']==fa['runtime_F_sha256'] and digest(objects['M'])==req['M']['file']['sha256']==ma['identities']['M']
policy=freeze['contracts']['policy']['canonical_object'];assert digest(policy)==req['scope']['policy_hash']==C['policy']
A=dict(domain='think-manual-A-v8',version=8,F=digest(objects['F']),M=digest(objects['M']),scope=digest(policy),authority=sha(read(approvalpath)))
T=dict(domain='think-manual-T-v8',version=8,C=C['bundle'],F=A['F'],M=A['M'],A=digest(A))
objects['A']=A;package=dict(domain='think-manual-package-v8',version=8,**objects)
metadata=req['metadata_identity_exception']['files'];raw_metadata=[];receipts=[]
for row in metadata:
 p=Path(row['path']);fd=os.open('/',os.O_RDONLY|os.O_DIRECTORY);ancestry=[]
 try:
  for part in p.parts[1:-1]:
   nxt=os.open(part,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=fd);os.close(fd);fd=nxt;s=os.fstat(fd);assert stat.S_ISDIR(s.st_mode);ancestry.append(dict(mode=oct(stat.S_IMODE(s.st_mode)),device=s.st_dev,inode=s.st_ino))
  filefd=os.open(p.name,os.O_RDONLY|os.O_NOFOLLOW,dir_fd=fd)
  try:
   before=os.fstat(filefd);assert stat.S_ISREG(before.st_mode) and before.st_nlink==1 and before.st_size==row['bytes']
   chunks=[];remaining=row['bytes']+1
   while remaining:
    b=os.read(filefd,min(65536,remaining))
    if not b:break
    chunks.append(b);remaining-=len(b)
   data=b''.join(chunks);after=os.fstat(filefd);pathstat=os.stat(p.name,dir_fd=fd,follow_symlinks=False)
   for s in (after,pathstat):assert (s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_nlink,s.st_mtime_ns,s.st_ctime_ns)==(before.st_dev,before.st_ino,before.st_mode,before.st_size,1,before.st_mtime_ns,before.st_ctime_ns)
   assert len(data)==row['bytes'] and sha(data)==row['sha256'];raw_metadata.append(data)
   receipts.append(dict(**row,regular=True,single_link=True,nofollow=True,stable_descriptor=True,mode=oct(stat.S_IMODE(before.st_mode)),private_parent_mode=ancestry[-1]['mode']))
  finally:os.close(filefd)
 finally:os.close(fd)
input_doc=dict(schema=8,policy=policy,policy_hash=digest(policy),release_hash=C['bundle'],metadata={name:{k:r[k] for k in ('bytes','sha256')} for name,r in zip(('commit','tree'),metadata)},manual_review=dict(bytes=len(canon(package)),sha256=digest(package)))
assert len(canon(input_doc))<=65536 and len(canon(package))<=262144
pins=dict(candidate=C['bundle'],execution_freeze=A['F'],authority_map=A['M'],acquisition_authorization=digest(A),release_hash=C['bundle'],commit_metadata_hash=metadata[0]['sha256'],tree_metadata_hash=metadata[1]['sha256'],approval=ref(approvalpath),request=ref(reqpath),F_acceptance=ref(R/'CP2-ASR-EXECUTION-RELEASE-FREEZE-V8-001-acceptance.json'),M_acceptance=ref(R/'CP2-ASR-REVIEW-AUTHORITY-MAP-V8-001-acceptance.json'))
OUT.mkdir(mode=0o700)
for name,obj in [('A',A),('T',T),('manual-package',package),('input',input_doc),('pins',pins),('metadata-identities',receipts)]:
 with (OUT/(name+'.json')).open('xb') as f:os.chmod(f.name,0o600);f.write(canon(obj))
# Exact previously reviewed pure modules copied into a new directory; no controller/transport imports.
moduletmp=Path(tempfile.mkdtemp(prefix='think-v8-approved-preflight-',dir='/private/tmp'))
module_records=load(Q/ka['output_directory']/'VERIFICATION.json')['module_identities']
assert len(module_records)==8
for row in module_records:
 b=read(Q/row['path']);assert len(b)==row['bytes'] and sha(b)==row['sha256'];dest=moduletmp/Path(row['path']).relative_to(C['root']);dest.parent.mkdir(exist_ok=True)
 dest.write_bytes(b)
assert not git('status','--porcelain=v1','--untracked-files=all')
sys.path.insert(0,str(moduletmp))
from network_guard import NetworkGuard
with NetworkGuard() as guard:
 from offline_review.manual import ManualPins,validate_package
 from offline_review.protocol import Trust,parse_input,parse_commit,parse_tree,input_document
 mp=ManualPins(C['bundle'],A['F'],A['M'],digest(A));trust=Trust(C['bundle'],metadata[0]['sha256'],metadata[1]['sha256'],mp)
 assert mp.document()==T
 rebuilt=input_document(trust,len(raw_metadata[0]),len(raw_metadata[1]));rebuilt['manual_review']=input_doc['manual_review'];assert rebuilt==input_doc
 assert validate_package(canon(package),mp,C['bundle'],digest(policy))==package
 assert parse_input(canon(input_doc),trust)==input_doc
 commit= parse_commit(raw_metadata[0]);tree_result=parse_tree(raw_metadata[1])
 guard_result=guard.evidence();assert guard_result['actual_network_events']==[] and guard_result['trapped_workload_calls']==[]
assert not any(n in sys.modules for n in ('offline_review.controller','offline_review.transport','offline_review.acquisition'))
result=dict(RESULT='PASS',approval=ref(approvalpath),request=ref(reqpath),product_head=req['baseline_commit'],frozen_inputs_rehashed=69505,external_references_rehashed=33,bundle_files=28,files=[ref(p) for p in sorted(OUT.glob('*.json'))],metadata=receipts,guard=guard_result,pure_validations=['ManualPins.document','input_document','validate_package','parse_input','parse_commit','parse_tree'],parsed_tree_count=len(tree_result),module_copy_directory=str(moduletmp),module_records=module_records,candidate_imports=sorted(n for n in sys.modules if n.startswith('offline_review')),network_requests=0,raw_body_reads=0,new_run_created=False,limits='Pure approved authority/input mapping; no run_input/controller/transport or original source/private envelope. Metadata bytes stay in memory; no raw copies exported.')
print(json.dumps(result,sort_keys=True,indent=2))
