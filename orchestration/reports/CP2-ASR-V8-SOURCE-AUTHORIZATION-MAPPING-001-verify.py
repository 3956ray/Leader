"""Independent approved mapping reconstruction and guarded complete-bundle pure preflight."""
import os,sys,stat,json,hashlib,tempfile,subprocess,base64
from pathlib import Path
L=Path('/Users/orderly_ray/Leader');Q=Path('/Users/orderly_ray/Projects/think');R=L/'orchestration/reports';ID='CP2-ASR-V8-SOURCE-AUTHORIZATION-MAPPING-001';OUT=R/(ID+'-artifacts')
def sha(b):return hashlib.sha256(b).hexdigest()
def can(v):return (json.dumps(v,ensure_ascii=True,allow_nan=False,sort_keys=True,separators=(',',':'))+'\n').encode('ascii')
def h(v):return sha(can(v))
def read(p):
 s=p.lstat();assert stat.S_ISREG(s.st_mode) and s.st_nlink==1 and all(stat.S_ISDIR(q.lstat().st_mode) for q in p.parents);return p.read_bytes()
def load(p):return json.loads(read(p))
def ref(p):b=read(p);return dict(path=str(p),bytes=len(b),sha256=sha(b))
def git(*a):return subprocess.check_output(['git','-C',str(Q),*a])
rq=R/'CP2-ASR-NARROW-SOURCE-ACQUISITION-V8-AUTHORIZATION-REQUEST-001.json';ap=R/'CP2-ASR-NARROW-SOURCE-ACQUISITION-V8-AUTHORIZATION-001-approved.json';req=load(rq);approval=load(ap)
assert sha(read(rq))=='2114259dc42837e96d938c65bce2b165ee47836623408c4377ffb8d11d5a392b' and sha(read(ap))=='694c69bc465663cb2a8ba58e21c9757d131d6135956a92df00ed78f997979c81'
assert approval['RESULT']=='APPROVED' and approval['user_reply']=='\u6279\u51c6' and approval['request_json']==ref(rq)
assert git('rev-parse','HEAD').decode().strip()==req['baseline_commit'] and not git('status','--porcelain=v1','--untracked-files=all')
for row in req['references']:assert ref(Path(row['path']))==row
fa=load(R/'CP2-ASR-EXECUTION-RELEASE-FREEZE-V8-001-acceptance.json');ma=load(R/'CP2-ASR-REVIEW-AUTHORITY-MAP-V8-001-acceptance.json');ka=load(R/'CP2-ASR-REVIEW-MAP-COMMITMENT-V8-001-R1-acceptance.json');C=req['accepted_C']
fr=load(Q/fa['output_directory']/'freeze.json');fm=load(Q/fa['output_directory']/'MANIFEST.json');git_records={}
for r in git('ls-tree','-r','-z','HEAD').split(b'\0'):
 if r:
  desc,p=r.split(b'\t',1);git_records[p.decode()]=tuple(desc.decode().split())
for row in fm['files']:
 b=read(Q/row['path']);blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest();assert len(b)==row['bytes'] and sha(b)==row['sha256'] and blob==row['git_blob'] and git_records[row['path']]==('100644','blob',blob)
assert len(fm['files'])==69505 and h(fm['files'])==fa['product_input_collection_sha256']
for row in fm['external_references']:assert ref(Path(row['path']))==row
assert len(fm['external_references'])==33 and h(fm['external_references'])==fa['external_reference_collection_sha256']
for a in (fa,ma,ka):
 assert a['RESULT']=='ACCEPTED' and git('rev-parse','HEAD:'+a['output_directory']).decode().strip()==a['output_tree']
 for row in a['files']:
  b=read(Q/a['output_directory']/row['path']);assert sha(b)==row['sha256'] and len(b)==row['bytes']
assert git('rev-parse','HEAD:'+C['root']).decode().strip()==C['tree']
F=load(Path(req['F']['file']['path']));M=load(Path(req['M']['file']['path']));policy=req['scope']['frozen_policy'];assert h(policy)==C['policy']
assert h(F)==fa['runtime_F_sha256']==req['F']['file']['sha256'] and h(M)==ma['identities']['M']==req['M']['file']['sha256']
A={'authority':sha(read(ap)),'scope':h(policy),'M':h(M),'F':h(F),'version':8,'domain':'think-manual-A-v8'}
T={'A':h(A),'F':h(F),'M':h(M),'C':C['bundle'],'domain':'think-manual-T-v8','version':8}
package={'domain':'think-manual-package-v8','version':8,'F':F,'M':M,'A':A}
for name in ('H','R','representation','K'):package[name]=load(Q/ka['output_directory']/(name+'.json'))
meta=req['metadata_identity_exception']['files'];input_doc={'schema':8,'policy':policy,'policy_hash':h(policy),'release_hash':C['bundle'],'metadata':{name:{k:r[k] for k in ('sha256','bytes')} for name,r in zip(('commit','tree'),meta)},'manual_review':{'bytes':len(can(package)),'sha256':h(package)}}
for name,v in [('A',A),('T',T),('manual-package',package),('input',input_doc)]:assert can(v)==read(OUT/(name+'.json'))
pins=load(OUT/'pins.json');assert pins==dict(candidate=C['bundle'],execution_freeze=h(F),authority_map=h(M),acquisition_authorization=h(A),release_hash=C['bundle'],commit_metadata_hash=meta[0]['sha256'],tree_metadata_hash=meta[1]['sha256'],approval=ref(ap),request=ref(rq),F_acceptance=ref(R/'CP2-ASR-EXECUTION-RELEASE-FREEZE-V8-001-acceptance.json'),M_acceptance=ref(R/'CP2-ASR-REVIEW-AUTHORITY-MAP-V8-001-acceptance.json'))
assert base64.b64decode(package['R']['content_base64'],validate=True) and sha(base64.b64decode(package['R']['content_base64'],validate=True))==M['R']
# Independent descriptor reader, exact two approved metadata files only.
rawmeta=[];receipts=[]
for row in meta:
 p=Path(row['path']);fd=os.open('/',os.O_RDONLY|os.O_DIRECTORY)
 try:
  for part in p.parts[1:-1]:
   n=os.open(part,os.O_RDONLY|os.O_NOFOLLOW|os.O_DIRECTORY,dir_fd=fd);os.close(fd);fd=n
  filefd=os.open(p.name,os.O_RDONLY|os.O_NOFOLLOW,dir_fd=fd)
  try:
   a=os.fstat(filefd);assert stat.S_ISREG(a.st_mode) and a.st_nlink==1 and a.st_size==row['bytes'];b=bytearray()
   while len(b)<=row['bytes']:
    block=os.read(filefd,min(32768,row['bytes']+1-len(b)))
    if not block:break
    b.extend(block)
   z=os.fstat(filefd);n=os.stat(p.name,dir_fd=fd,follow_symlinks=False)
   for s in (z,n):assert (s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns)==(a.st_dev,a.st_ino,a.st_mode,1,a.st_size,a.st_mtime_ns,a.st_ctime_ns)
   assert len(b)==row['bytes'] and sha(b)==row['sha256'];rawmeta.append(bytes(b));receipts.append(dict(**row,nofollow=True,regular_singlelink=True,stable_fd=True,mode=oct(stat.S_IMODE(a.st_mode))))
  finally:os.close(filefd)
 finally:os.close(fd)
for before,after in zip(load(OUT/'metadata-identities.json'),receipts):assert all(before[k]==after[k] for k in ('path','bytes','sha256','mode'))
temp=Path(tempfile.mkdtemp(prefix='think-v8-mapping-full-preflight-',dir='/private/tmp'));bundle=fr['candidate_bundle']['records'];assert len(bundle)==28 and h(bundle)==C['bundle']
for row in bundle:
 p=Path(row['path']);assert not p.is_absolute() and '..' not in p.parts;b=read(Q/C['root']/p);assert sha(b)==row['sha256'];dest=temp/p;dest.parent.mkdir(exist_ok=True);dest.write_bytes(b)
assert not git('status','--porcelain=v1','--untracked-files=all')
sys.path.insert(0,str(temp));from network_guard import NetworkGuard
with NetworkGuard() as ng:
 from offline_review.manual import ManualPins,validate_package
 from offline_review.protocol import Trust,input_document,parse_input,parse_commit,parse_tree,candidate_release_hash
 mp=ManualPins(pins['candidate'],pins['execution_freeze'],pins['authority_map'],pins['acquisition_authorization']);trust=Trust(pins['release_hash'],pins['commit_metadata_hash'],pins['tree_metadata_hash'],mp)
 assert mp.document()==T and candidate_release_hash()==C['bundle']
 expected=input_document(trust,len(rawmeta[0]),len(rawmeta[1]));expected['manual_review']={'bytes':len(can(package)),'sha256':h(package)};assert can(expected)==can(input_doc)
 assert validate_package(read(OUT/'manual-package.json'),mp,C['bundle'],C['policy'])==package
 assert parse_input(read(OUT/'input.json'),trust)==input_doc
 parsed_commit=parse_commit(rawmeta[0]);parsed_tree=parse_tree(rawmeta[1])
 evidence=ng.evidence();assert evidence['actual_network_events']==[] and evidence['trapped_workload_calls']==[]
assert not any(n in sys.modules for n in ('offline_review.acquisition','offline_review.controller','offline_review.transport'))
print(json.dumps(dict(RESULT='PASS',approved_record=ref(ap),request=ref(rq),product_head=req['baseline_commit'],frozen_inputs_rehashed=69505,frozen_external_references_rehashed=33,bundle_files=28,independent_objects_rebuilt=['A','T','manual-package','input','pins'],files=[ref(p) for p in sorted(OUT.glob('*.json'))],identities=dict(C=C['bundle'],F=h(F),M=h(M),A=h(A),T=h(T),package=h(package),input=h(input_doc),policy=C['policy']),metadata=receipts,tree_entries=len(parsed_tree),network=evidence,pure_validations=['candidate_release_hash','ManualPins.document','input_document','validate_package','parse_input','parse_commit','parse_tree'],copy_directory=str(temp),copied_bundle=bundle,imported_modules=sorted(n for n in sys.modules if n.startswith('offline_review')),rawbody_requests=0,new_run_created=False,limitations=['No run_input/controller/transport invocation.','Prior partial-eight-module harness failed running_release_hash before network/body; immutable A/T/input/package were not regenerated; complete28filecopy pure validation now passes.','No thirdpartybody/read/execution or originalenvelope; only exact two approvedmetadata identities, no rawcopies exported.']),sort_keys=True,indent=2))
