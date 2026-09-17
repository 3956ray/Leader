"""Independent standard-library F verifier; no producer/candidate import or execution.
--core verifies three outputs; --final verifies all four and their Git boundary.
"""
import os,sys,json,hashlib,stat,subprocess
from pathlib import Path
PROJECT=Path('/Users/orderly_ray/Projects/think');TEMP=Path(__file__).resolve().parent
TASK=Path('/Users/orderly_ray/Leader/orchestration/tasks/CP2-ASR-EXECUTION-RELEASE-FREEZE-V8-001.json')
network=[]
def guard(event,args):
 if event.startswith(('socket.','http.client.')) or event in ('os.system','os.fork','os.forkpty','os.posix_spawn','os.exec'):
  network.append(event);raise RuntimeError('network/process denied')
 if event=='subprocess.Popen':assert args[1][0]=='git' and args[1][1] in ('ls-tree','rev-parse','status','diff','diff-tree','ls-files')
sys.addaudithook(guard)
def canonical(value):return (json.dumps(value,ensure_ascii=True,sort_keys=True,allow_nan=False,separators=(',',':'))+'\n').encode('ascii')
def sha(data):return hashlib.sha256(data).hexdigest()
def digest(value):return sha(canonical(value))
def oid(data):return hashlib.sha1(b'blob '+str(len(data)).encode('ascii')+b'\0'+data).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=PROJECT)
checked_dirs={}
def checked_bytes(path):
 # lstat every distinct ancestor, then independently recheck the full set at end.
 parent=path.parent
 while True:
  if parent not in checked_dirs:
   info=parent.lstat();assert stat.S_ISDIR(info.st_mode) and not stat.S_ISLNK(info.st_mode);checked_dirs[parent]=(info.st_dev,info.st_ino,info.st_mode)
  if parent==parent.parent:break
  parent=parent.parent
 before=path.lstat();assert stat.S_ISREG(before.st_mode) and before.st_nlink==1
 with path.open('rb') as stream:
  descriptor=os.fstat(stream.fileno());assert (descriptor.st_dev,descriptor.st_ino)==(before.st_dev,before.st_ino)
  chunks=[]
  while True:
   block=stream.read(1024*1024)
   if not block:break
   chunks.append(block)
  after=os.fstat(stream.fileno())
 data=b''.join(chunks);now=path.lstat()
 for info in (after,now):assert (info.st_dev,info.st_ino,info.st_size,info.st_mode,info.st_nlink,info.st_mtime_ns,info.st_ctime_ns)==(before.st_dev,before.st_ino,before.st_size,before.st_mode,1,before.st_mtime_ns,before.st_ctime_ns)
 assert len(data)==before.st_size
 return data
def record(path,label=None):
 b=checked_bytes(path);assert not path.stat().st_mode&0o111
 return dict(path=label or path.name,bytes=len(b),sha256=sha(b),git_blob=oid(b),mode='100644',type='blob')
def document(path):
 b=checked_bytes(path);v=json.loads(b);assert canonical(v)==b;return v
raw=checked_bytes(TASK);assert len(raw)==19635 and sha(raw)=='59fb9a077347ac20385b55ae7e237b776c1b2934e5eccee510dc0ceca718ccf1';t=json.loads(raw)
C=t['accepted_C'];K=t['accepted_K'];out=PROJECT/t['output_directory'];final='--final' in sys.argv
names=['F.json','MANIFEST.json','freeze.json']+(['REPORT.md'] if final else [])
assert {p.name for p in out.iterdir()}==set(names)
manifest=document(out/'MANIFEST.json');freeze=document(out/'freeze.json');F=document(out/'F.json')
assert F==dict(domain='think-manual-F-v8',version=8,C=C['bundle'],K=K['identities']['K'],policy=C['policy'],intake_schema=C['intake']) and type(F['version']) is int
assert set(F)=={'domain','version','C','K','policy','intake_schema'}
base_raw=git('ls-tree','-r','-z',t['baseline_commit']);assert len(base_raw.split(b'\0'))-1==129523
base={}
for entry in base_raw.split(b'\0'):
 if entry:
  descriptor,path=entry.split(b'\t',1);mode,kind,blob=descriptor.decode().split();base[path.decode()]=(mode,kind,blob)
expected_paths=sorted([p for p in base if p.startswith(C['root']+'/') or p.startswith(K['root']+'/')],key=lambda p:p.encode('ascii'))
assert len(expected_paths)==69505
records=[]
for path in expected_paths:
 row=record(PROJECT/path,path);assert (row['mode'],row['type'],row['git_blob'])==base[path];records.append(row)
assert manifest['files']==records and manifest['file_count']==69505 and manifest['files_collection_sha256']==digest(records)
assert manifest['files_collection_domain']=='sha256-canonical-ascii-path-sorted-existing-product-input-records-v1'
assert manifest['external_references_collection_domain']=='sha256-canonical-ascii-absolute-path-sorted-pinned-reference-records-v1'
assert set(manifest)=={'domain','version','canonical','files','file_count','files_collection_domain','files_collection_sha256','external_references','external_reference_count','external_references_collection_domain','external_references_collection_sha256','exclusions'}
references=sorted(t['pinned_references']+[dict(path=str(TASK),bytes=len(raw),sha256=sha(raw))],key=lambda p:p['path'].encode('ascii'))
assert len(references)==len({r['path'] for r in references})==33
for ref in references:
 data=checked_bytes(Path(ref['path']));assert len(data)==ref['bytes'] and sha(data)==ref['sha256']
assert manifest['external_references']==references and manifest['external_reference_count']==33 and manifest['external_references_collection_sha256']==digest(references)
by_path={r['path']:r for r in records};cpaths=[p for p in expected_paths if p.startswith(C['root']+'/')];assert len(cpaths)==69497
for accepted in K['files']:assert by_path[K['root']+'/'+accepted['path']]==dict(accepted,path=K['root']+'/'+accepted['path'])
for candidate in (C,K):assert git('rev-parse',t['baseline_commit']+':'+candidate['root']).decode().strip()==candidate['tree']
manifest_path=C['root']+'/evidence/file-manifest.json';old_manifest=json.loads(checked_bytes(PROJECT/manifest_path));assert by_path[manifest_path]['sha256']==C['file_manifest_sha256']
old_expected=[]
for name in cpaths:
 if name==manifest_path:continue
 r=by_path[name];old_expected.append(dict(path=name[len(C['root'])+1:],bytes=r['bytes'],sha256=r['sha256'],git_blob=r['git_blob'],git_mode=r['mode'],file_type='regular',nlink=1))
assert old_manifest['files']==old_expected and old_manifest['file_count']==69496 and old_manifest['collection_sha256']==digest(old_expected)
ids_path=C['root']+'/evidence/identities.json';ids=json.loads(checked_bytes(PROJECT/ids_path));contracts=dict(policy=ids['policy'],intake=ids['intake_contract'],semantic=ids['policy']['source_semantics'],role=ids['policy']['content_roles'])
hashes={n:digest(v) for n,v in contracts.items()};assert hashes['intake']==C['intake']==ids['intake_contract_sha256'];assert hashes['policy']==C['policy']==ids['policy_sha256']
assert hashes['semantic']==ids['semantic_contract_sha256']=='2b048314969209f4db3a6a63f2b6646ceeb06d5b3794fa44e1dcd52c0b583c86'
assert hashes['role']==ids['role_contract_sha256']=='1c8a95b48c034e830b2a0a545192c691af12127774152921e1df73c6ee670125'
bundle=[]
for name in cpaths:
 rel=Path(name).relative_to(C['root'])
 if (len(rel.parts)==2 and rel.parts[0] in ('offline_review','tests') and rel.suffix=='.py') or str(rel) in ('audit.py','verify.py','network_guard.py','recalculate.py','SCHEMA.md'):
  bundle.append(dict(path=str(rel),sha256=by_path[name]['sha256']))
assert len(bundle)==28 and digest(bundle)==C['bundle']==ids['bundle_sha256']
assert freeze['candidate_bundle']==dict(records=bundle,files=28,sha256=digest(bundle),domain='SHA256 canonical sorted candidate-relative path/sha256 collection, not Git tree')
assert freeze['contracts']=={name:dict(canonical_object=obj,sha256=hashes[name]) for name,obj in contracts.items()}
assert freeze['contracts_source']==by_path[ids_path]
assert freeze['C']==C and freeze['K']=={k:K[k] for k in ('commit','tree','root','identities')}
ka=json.loads(checked_bytes(Path(t['predecessor_acceptance'])));assert ka['RESULT']=='ACCEPTED' and ka['identities']==K['identities'] and ka['files']==K['files'] and ka['candidate_commit']==K['commit']
assert freeze['acceptances']==dict(C=ka['accepted_C_report'],K=K['acceptance'],P=ka['P_acceptance'],P_record=ka['P'])
for ref in freeze['acceptances'].values():assert ref in references
ca=json.loads(checked_bytes(Path(ka['accepted_C_report']['path'])));pa=json.loads(checked_bytes(Path(ka['P_acceptance']['path'])))
assert ca['RESULT']=='ACCEPTED' and ca['candidate_commit']==C['commit'] and ca['candidate_tree']==C['tree'] and ca['bundle_sha256']==C['bundle']
assert pa['RESULT']=='ACCEPTED' and pa['P']==ka['P'] and ka['P']['sha256']==K['identities']['P']
H=document(PROJECT/K['root']/'H.json');actualK=document(PROJECT/K['root']/'K.json');assert digest(H)==K['identities']['H'] and digest(actualK)==F['K'] and actualK['operational_authority'] is False
assert freeze['historical_H']['canonical_object']==H and freeze['historical_H']['canonical_sha256']==digest(H)
assert freeze['historical_H']['context_release_domain']=='Historical freeze.json exact-byte hash, unrelated to runtime execution F'
assert freeze['prepared_task']==dict(path=str(TASK),bytes=len(raw),sha256=sha(raw))
assert freeze['formal_sources']==[r for r in references if r['path'].startswith(str(PROJECT)+'/')]
def descriptor(name):
 b=checked_bytes(out/name);return dict(path=t['output_directory']+'/'+name,bytes=len(b),sha256=sha(b))
assert freeze['runtime_F']==dict(file=descriptor('F.json'),canonical_object=F,hash_domain='SHA256 canonical runtime F.json; future M.F must bind this digest')
assert freeze['manifest']==dict(file=descriptor('MANIFEST.json'),file_count=69505,files_collection_sha256=digest(records),external_reference_count=33,external_references_collection_sha256=digest(references))
assert freeze['original_C_file_manifest']['file']==by_path[manifest_path] and freeze['original_C_file_manifest']['records']==69496 and freeze['original_C_file_manifest']['collection_sha256']==digest(old_expected)
assert 'not treated as final passing evidence' in freeze['original_C_file_manifest']['archival_scope']
assert freeze['domain']=='think-v8-execution-release-support-record-v1' and freeze['version']==1 and freeze['task']==t['task_id'] and freeze['baseline_commit']==t['baseline_commit']
assert 'must never be used as M.F' in freeze['supporting_freeze_identity']
q=freeze['constraints'];p=contracts['policy']
assert q['upstream']=={k:p[k] for k in ('host','repository','commit','tree')} and q['design']==p['design']
assert q['seed_order']==p['seeds'] and len(q['seed_order'])==9 and q['ordered_seed_roles']==[dict(path=s,role=p['content_roles']['seeds'][s]) for s in p['seeds']]
assert {k:q['path_rules'][k] for k in ('repository_prefix','include_roots','type','mode')}=={k:p[k] for k in ('repository_prefix','include_roots','type','mode')}
assert q['limits']==p['limits']==dict(files=96,decoded=1048576,metadata_raw=8388608,blob_raw=1500000,total_raw=16777216) and q['input_bytes']==65536
assert q['transport']==dict(connect_timeout=10,read_timeout=10,credentials=False,proxy=False,redirect=False,retries=0,scope='constraints only, no transport execution or acquisition authorization')
assert q['evidence_limits']==p['evidence_limits'] and q['deny']==p['deny'] and q['priority']==p['source_semantics']['priority']
assert q['hard_stops']==['Identity/file safety, path/role/mode/type, budgets, persistence and capacity failures remain prior hard stops.','Active or uncertain deny, lexical ambiguity/traps and unsupported preprocessor/ineligible include outrank comment adjudication.','Unknown/conflicting/forbidden/unresolved/pending decisions fail closed; no global token/comment exception, wrapper bypass or implicit Trust.','Exact complete one-to-one occurrence matching only, two original comment decisions do not clear adjacent fields/API/implementation or capabilities.','Original pending/source analysis/ledger/terminal and terminated historical runs remain immutable; no old acquisition authority reuse.']
assert q['privacy']==['Normal recording and retrieval stay within three steps.','Original audio only in memory; no disk, upload, logs, test attachments or crash reports.']
assert q['checkpoint']==['CP1 and Conformer Deferred, not removed.','CP2 not passed; CP3 and father Alpha not approved.']
a=freeze['evidence_attribution'];assert a['C']['source']==ka['accepted_C_report'] and (a['C']['leader_runs'],a['C']['tests_per_run'],a['C']['outcomes_per_run'],a['C']['skips_per_run'])==(2,174,1338,0)
assert a['C']['raw_scan_verdict']=='sandbox_only' and a['C']['raw_scan_score']==100 and 'not third-party security PASS' in a['C']['qualification']
assert a['K']['source']==K['acceptance'] and a['K']['source_leaf_mappings']==121 and a['K']['original_R_and_P_full_reconstruction'] is True and a['K']['original_review_time_lossless'] is True
assert freeze['baseline_git']['records']==129523 and freeze['baseline_git']['ls_tree_r_z_sha256']==sha(base_raw)
assert freeze['effect']==dict(new_acquisition_authorized=False,pending_cleared=False,candidate_executed=False,network_executed=False,source_read=False,private_read=False,future_objects_created=False)
assert freeze['next']=='Leader independently accepts F first; then separate M, fresh hash-bound user acquisition A after F/M, then trusted T/N. No automatic continuation.'
for script in freeze['verification_scripts']:
 data=checked_bytes(Path(script['path']));assert len(data)==script['bytes'] and sha(data)==script['sha256']
assert {r['path'] for r in freeze['verification_scripts']}=={str(TEMP/'produce.py'),str(Path(__file__).resolve())}
assert set(freeze)=={'domain','version','task','baseline_commit','runtime_F','supporting_freeze_identity','manifest','C','K','historical_H','acceptances','prepared_task','formal_sources','contracts','contracts_source','candidate_bundle','original_C_file_manifest','constraints','evidence_attribution','verification_scripts','baseline_git','effect','next'}
# All original Git records are invariant both before and after the new commit.
now_raw=git('ls-tree','-r','-z','HEAD');old_now=[]
for line in now_raw.split(b'\0'):
 if line and not line.split(b'\t',1)[1].decode().startswith(t['output_directory']+'/'):old_now.append(line)
assert b'\0'.join(old_now)+b'\0'==base_raw
head=git('rev-parse','HEAD').decode().strip()
if head!=t['baseline_commit']:
 assert git('rev-parse','HEAD^').decode().strip()==t['baseline_commit']
 assert sorted(git('diff-tree','--no-commit-id','--name-only','-r','HEAD').decode().splitlines())==sorted(t['output_directory']+'/'+n for n in names)
# Current uncommitted tracked modifications may only be these new output paths.
for changed in git('diff','--name-only',t['baseline_commit']).decode().splitlines():assert changed in [t['output_directory']+'/'+n for n in names]
if final:
 report=checked_bytes(out/'REPORT.md').decode('utf-8')
 for name in ('F.json','freeze.json','MANIFEST.json'):assert descriptor(name)['sha256'] in report
 assert sha(checked_bytes(Path(__file__).resolve())) in report
 for text in ('69505','33','129523','sandbox_only','M.F','CP2','174','1338','121'):assert text in report
for parent,old_info in checked_dirs.items():
 s=parent.lstat();assert (s.st_dev,s.st_ino,s.st_mode)==old_info
assert not network and not any(n.startswith('offline_review') for n in sys.modules)
result=dict(RESULT='PASS',phase='final' if final else 'core',files=[record(out/n) for n in sorted(names)],F_sha256=descriptor('F.json')['sha256'],supporting_freeze_sha256=descriptor('freeze.json')['sha256'],MANIFEST_sha256=descriptor('MANIFEST.json')['sha256'],product_input_count=len(records),external_reference_count=len(references),files_collection_sha256=digest(records),external_collection_sha256=digest(references),C_manifest_rows=69496,C_total_files=69497,K_files=8,bundle_count=28,bundle_sha256=digest(bundle),contracts=hashes,K=F['K'],P=K['identities']['P'],P_acceptance=K['identities']['P_acceptance'],old_records=129523,old_records_sha256=sha(base_raw),network_events=network,candidate_imports=[],real_source_or_private_reads=0,limits='Byte-hash and first-party derived-document validation only; no source/runtime/license/build/model/device/audio or checkpoint approval.')
print(json.dumps(result,sort_keys=True,separators=(',',':')))
