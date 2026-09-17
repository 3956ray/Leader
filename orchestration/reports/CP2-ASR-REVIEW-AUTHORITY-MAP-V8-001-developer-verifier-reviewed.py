"""Independent M reconstruction from fixed F/K, standard library only.
F MANIFEST is hash-only. No recursive input walk, candidate or producer imports.
"""
import json,hashlib,sys,stat,subprocess,re,os
from pathlib import Path
ROOT=Path('/Users/orderly_ray/Projects/think');D=Path(__file__).resolve().parent;TASK=Path('/Users/orderly_ray/Leader/orchestration/tasks/CP2-ASR-REVIEW-AUTHORITY-MAP-V8-001.json')
network=[]
def audit(event,args):
 if event.startswith(('socket.','http.client.')) or event in ('os.system','os.fork','os.forkpty','os.posix_spawn','os.exec'):
  network.append(event);raise RuntimeError('forbidden capability')
 if event=='subprocess.Popen':assert args[1][0]=='git' and args[1][1] in ('ls-tree','rev-parse','diff','diff-tree','status','ls-files')
sys.addaudithook(audit)
def canon(o):return (json.dumps(o,ensure_ascii=True,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode('ascii')
def sha(b):return hashlib.sha256(b).hexdigest()
def digest(o):return sha(canon(o))
def git(*a):return subprocess.check_output(['git',*a],cwd=ROOT)
def read(p):
 for q in p.parents:
  s=q.lstat();assert stat.S_ISDIR(s.st_mode) and not stat.S_ISLNK(s.st_mode)
 a=p.lstat();assert stat.S_ISREG(a.st_mode) and a.st_nlink==1
 with p.open('rb') as f:
  s=os.fstat(f.fileno());assert (a.st_dev,a.st_ino)==(s.st_dev,s.st_ino);b=f.read();z=os.fstat(f.fileno())
 assert (s.st_size,s.st_mode,s.st_nlink,s.st_mtime_ns,s.st_ctime_ns)==(z.st_size,z.st_mode,1,z.st_mtime_ns,z.st_ctime_ns) and len(b)==s.st_size
 return b
def record(p):
 b=read(p);assert not p.lstat().st_mode&0o111;return dict(path=p.name,bytes=len(b),sha256=sha(b),git_blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),mode='100644',type='blob')
b=read(TASK);assert len(b)==16582 and sha(b)=='3c073c93647d1d02ae442dc244b6072f97f19618e9274d3fb8b52c6aff2defa2';t=json.loads(b);task_id=dict(path=str(TASK),bytes=len(b),sha256=sha(b));out=ROOT/t['output_directory']
raw={}
for row in t['pinned_references']:
 b=read(Path(row['path']));assert len(b)==row['bytes'] and sha(b)==row['sha256'];raw[row['path']]=b
assert len(raw)==27
# Parse only necessary pinned derived objects, never F's 20 MB MANIFEST.
def obj(p):
 b=raw[str(p)];v=json.loads(b);assert canon(v)==b;return v
def external(p):return json.loads(raw[p])
C=t['accepted_C'];Kpin=t['accepted_K'];Fpin=t['accepted_F'];Fp=ROOT/Fpin['root']/'F.json';Kp=ROOT/Kpin['root']/'K.json';F=obj(Fp);K=obj(Kp)
assert F==dict(domain='think-manual-F-v8',version=8,C=C['bundle'],K=Kpin['identities']['K'],policy=C['policy'],intake_schema=C['intake']) and type(F['version']) is int
assert sha(raw[str(Fp)])==Fpin['runtime_F_sha256'] and sha(raw[str(Kp)])==Kpin['identities']['K']
assert set(K)=={'domain','version','C','H','R','representation','authority','entries','map_schema','operational_authority'}
assert K['domain']=='think-manual-K-v8' and type(K['version']) is int and K['version']==8 and K['operational_authority'] is False
assert K['C']==F['C'] and K['map_schema']==F['intake_schema']==C['intake']
for key,source in [('H','H'),('R','original_R'),('representation','representation')]:assert K[key]==Kpin['identities'][source]
rep=obj(ROOT/Kpin['root']/'representation.json');H=obj(ROOT/Kpin['root']/'H.json')
assert digest(rep)==K['representation'] and digest(H)==K['H'] and rep['original_report_sha256']==K['R'] and rep['authority']==K['authority']
assert digest(rep['reviewed_at'])==Kpin['identities']['timestamp']
assert sha(raw[str(ROOT/Kpin['root']/'R.json')])==Kpin['identities']['R_wrapper']
assert type(K['entries']) is list and len(K['entries'])==2 and K['entries']==[{key:r[key] for key in ('occurrence_id','decision')} for r in rep['occurrences']]
assert len({r['occurrence_id'] for r in K['entries']})==2
for row in K['entries']:
 assert set(row)=={'occurrence_id','decision'} and re.fullmatch('[0-9a-f]{64}',row['occurrence_id']) and row['decision']=='comment_only_nonoperative_for_this_body'
assert K['authority']=='df26a4884e47a63c3cdbd0e2afc118e4a4f70f4ef7db9a267d6307e01b4aa9c2'
M=dict(domain='think-manual-M-v8',version=8,F=sha(raw[str(Fp)]),K=sha(raw[str(Kp)]),H=K['H'],R=K['R'],representation=K['representation'],authority=K['authority'],entries=K['entries'],map_schema=K['map_schema'])
assert len(M)==10 and read(out/'M.json')==canon(M)
assert M['F']!=Fpin['supporting_freeze_sha256'] and M['F']!=H['context_release']
fa=external(Fpin['acceptance']['path']);ka=external(Kpin['acceptance']['path'])
assert fa['RESULT']==ka['RESULT']=='ACCEPTED' and fa['candidate_commit']==Fpin['commit'] and ka['candidate_commit']==Kpin['commit']
assert fa['runtime_F_sha256']==M['F'] and fa['supporting_freeze_sha256']==Fpin['supporting_freeze_sha256'] and fa['K']==ka['identities']==Kpin['identities']
assert fa['C']==C and fa['output_tree']==Fpin['tree'] and ka['output_tree']==Kpin['tree']
ca_pin=next(x for x in t['pinned_references'] if x['path'].endswith('CP2-ASR-REVIEW-TIMESTAMP-REPRESENTATION-OFFLINE-001-acceptance.json'));ca=external(ca_pin['path']);assert ca['RESULT']=='ACCEPTED' and ca['candidate_commit']==C['commit'] and ca['candidate_tree']==C['tree'] and ca['bundle_sha256']==C['bundle']
pa_pin=next(x for x in t['pinned_references'] if x['path'].endswith('CP2-ASR-REVIEW-TOKEN-PROVENANCE-COMPLETION-001-acceptance.json'));pa=external(pa_pin['path']);assert pa['RESULT']=='ACCEPTED' and pa['P']==ka['P'] and pa_pin==ka['P_acceptance']
assert pa['P']['sha256']==Kpin['identities']['P'] and pa['P'] in t['pinned_references']
ids=external(str(ROOT/C['root']/'evidence/identities.json'));assert digest(ids['policy'])==C['policy'] and digest(ids['intake_contract'])==C['intake']
# Compare Git metadata only for whole C/K/F; no fixture/scan/candidate bulk reads.
base=git('ls-tree','-r','-z',t['baseline_commit']);assert len(base.split(b'\0'))-1==129527
for pin in (C,Kpin,Fpin):assert git('rev-parse','HEAD:'+pin['root']).decode().strip()==pin['tree']
retained=[]
for entry in git('ls-tree','-r','-z','HEAD').split(b'\0'):
 if entry and not entry.split(b'\t',1)[1].decode().startswith(t['output_directory']+'/'):retained.append(entry)
assert b'\0'.join(retained)+b'\0'==base
prov=json.loads(read(out/'PROVENANCE.json'));assert canon(prov)==read(out/'PROVENANCE.json')
assert prov['task']==t['task_id'] and prov['baseline_commit']==t['baseline_commit'] and prov['prepared_task']==task_id and prov['pinned_references']==t['pinned_references']
assert prov['accepted_trees']=={n:t[n] for n in ('accepted_C','accepted_K','accepted_F')}
assert prov['acceptances']==dict(C=ca_pin,K=Kpin['acceptance'],F=Fpin['acceptance'],P=pa_pin) and prov['P_record']==pa['P']
assert prov['baseline_git']['records']==129527 and prov['baseline_git']['ls_tree_r_z_sha256']==sha(base)
expected_ids=dict(M=digest(M),runtime_F=M['F'],supporting_freeze=Fpin['supporting_freeze_sha256'],K=M['K'],H=M['H'],original_R=M['R'],R_wrapper=Kpin['identities']['R_wrapper'],representation=M['representation'],authority=M['authority'],intake=M['map_schema'],P=Kpin['identities']['P'],timestamp=Kpin['identities']['timestamp']);assert prov['identity_domains']==expected_ids
expected_sources={}
for field in ('domain','version','F','K','H','R','representation','authority','map_schema'):
 if field in ('domain','version'):v=dict(path=str(ROOT/C['root']/'offline_review/manual.py'),locator='domain/version',kind='accepted schema constant')
 elif field in ('F','K'):v=dict(path=str(Fp if field=='F' else Kp),locator='whole canonical file bytes',kind='exact byte digest')
 else:v=dict(path=str(Kp),locator='/'+field,kind='JSON pointer')
 expected_sources['/'+field]=v
for i in range(2):
 for key in ('occurrence_id','decision'):expected_sources['/entries/'+str(i)+'/'+key]=dict(path=str(Kp),locator='/entries/'+str(i)+'/'+key,kind='JSON pointer')
assert len(prov['field_mapping'])==len(expected_sources)==13
assert {x['target']:x['source'] for x in prov['field_mapping']}==expected_sources
for x in prov['field_mapping']:assert type(x['derivation']) is str and x['derivation']
assert all(v is False for v in prov['scope'].values()) and len(prov['scope'])==7
report=read(out/'REPORT.md').decode('utf-8')
for word in [digest(M),M['F'],M['K'],Fpin['supporting_freeze_sha256'],'13','27','129527','CP2','A/T/input/N']:assert word in report
files=['M.json','PROVENANCE.json','REPORT.md'];final='--final' in sys.argv
if final:
 files+=['VERIFICATION.json','MANIFEST.json'];v=json.loads(read(out/'VERIFICATION.json'));manifest=json.loads(read(out/'MANIFEST.json'))
 for name,data in [('VERIFICATION.json',v),('MANIFEST.json',manifest)]:assert read(out/name)==canon(data)
 assert v['independent_script']['path']==str(Path(__file__).resolve()) and v['independent_script']['sha256']==sha(read(Path(__file__).resolve()))
 assert v['core_result']['RESULT']=='PASS' and v['core_result']['identities']==expected_ids and v['core_result']['leaf_count']==13 and v['core_result']['reference_count']==27
 for row in v['core_result']['files']:assert row==record(out/row['path'])
 assert v['pinned_references']==t['pinned_references'] and v['production_result']['RESULT']=='PASS'
 rows=[record(out/name) for name in sorted(files) if name!='MANIFEST.json'];assert manifest['files']==rows and manifest['collection_sha256']==digest(rows)
 for s in v['scripts']+[v['independent_script']]:
  b=read(Path(s['path']));assert len(b)==s['bytes'] and sha(b)==s['sha256']
assert {p.name for p in out.iterdir()}==set(files)
head=git('rev-parse','HEAD').decode().strip()
if head!=t['baseline_commit']:
 assert git('rev-parse','HEAD^').decode().strip()==t['baseline_commit']
 assert sorted(git('diff-tree','--no-commit-id','--name-only','-r','HEAD').decode().splitlines())==sorted(t['output_directory']+'/'+n for n in files)
for path in git('diff','--name-only',t['baseline_commit']).decode().splitlines():assert path in [t['output_directory']+'/'+n for n in files]
assert not network and not any(n.startswith('offline_review') for n in sys.modules)
result=dict(RESULT='PASS',phase='final' if final else 'core',identities=expected_ids,entries=M['entries'],top_level_fields=10,leaf_count=13,reference_count=27,files=[record(out/n) for n in sorted(files)],old_records=129527,old_records_sha256=sha(base),preserved_trees={n:t[n]['tree'] for n in ('accepted_C','accepted_K','accepted_F')},network_events=network,candidate_imports=[],source_or_private_reads=0,F_manifest_decoded=False,old_C_bulk_validation=False,new_acquisition_authorized=False,limits='Derived F/K composition only; historical review/token/time truth inherited unchanged. No new user A/T/input/N, no full package or original source review.')
print(json.dumps(result,sort_keys=True,separators=(',',':')))
