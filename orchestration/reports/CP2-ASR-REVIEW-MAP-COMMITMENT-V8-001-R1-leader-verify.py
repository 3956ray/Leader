"""Read-only Leader verification of fixed K delivery, no candidate imports or private reads."""
import base64
import datetime as dt
import hashlib
import json
from pathlib import Path
import stat
import subprocess

L=Path('/Users/orderly_ray/Leader')
Q=Path('/Users/orderly_ray/Projects/think')
TMP=Path('/private/tmp/think-k-v8-r1-w90e8ogk')
TASK='CP2-ASR-REVIEW-MAP-COMMITMENT-V8-001-R1'
HEAD='f48f4831c9d733080dab97932604f4ecf1e4cbc2'
def sha(b): return hashlib.sha256(b).hexdigest()
def canonical(x): return (json.dumps(x,sort_keys=True,ensure_ascii=True,allow_nan=False,separators=(',',':'))+'\n').encode('ascii')
def digest(x): return sha(canonical(x))
def load(p): return json.loads(p.read_bytes())
def git(*args): return subprocess.check_output(['git','-C',str(Q),*args])
def textgit(*args): return git(*args).decode().strip()
def checked(p):
    st=p.lstat()
    assert stat.S_ISREG(st.st_mode) and st.st_nlink==1, str(p)
    for parent in p.parents:
        assert not parent.is_symlink(),str(parent)
    return p.read_bytes()
taskbytes=checked(L/'orchestration/tasks'/f'{TASK}.json')
assert sha(taskbytes)=='9e0b08359157e76dc53c3ce5c19adf745756e02a32aab38ef2d9553d602839a1'
t=json.loads(taskbytes)
assert checked(TMP/'task.json')==taskbytes
assert textgit('rev-parse','HEAD')==HEAD
assert textgit('rev-parse','HEAD^')==t['baseline_commit']
assert not git('status','--porcelain=v1','--untracked-files=all')
directory=t['output_directory'];out=Q/directory
names=sorted(['H.json','R.json','representation.json','K.json','PROVENANCE.json','VERIFICATION.json','MANIFEST.json','REPORT.md'])
assert sorted(p.name for p in out.iterdir())==names
paths=[directory+'/'+n for n in names]
changes=git('diff','--name-status','HEAD^','HEAD').decode().splitlines()
assert changes==['A\t'+p for p in paths]
old=git('ls-tree','-r','-z','HEAD^')
new=git('ls-tree','-r','-z','HEAD')
retained=[r for r in new.split(b'\0') if r and r.split(b'\t',1)[1].decode() not in paths]
assert b'\0'.join(retained)+b'\0'==old
assert len(retained)==129515 and sha(old)=='1e19cb590ab7514bd238c70b1be32bc2ea140e83ab16183d194ddfd8e6964c13'
records=[]
for name,path in zip(names,paths):
    b=checked(Q/path)
    blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
    assert git('ls-tree','HEAD','--',path).decode().strip()==f'100644 blob {blob}\t{path}'
    assert git('cat-file','blob',blob)==b
    records.append(dict(path=name,bytes=len(b),sha256=sha(b),git_blob=blob,mode='100644',type='blob'))
    if name.endswith('.json'):assert canonical(json.loads(b))==b
manifest=load(out/'MANIFEST.json')
assert manifest['files']==[r for r in records if r['path']!='MANIFEST.json']
assert digest(manifest['files'])==manifest['collection_sha256']=='373565745d67451ddd95dee5d26e0db9705384e2100d6331bb9fe2c35baa9eeb'
prov=load(out/'PROVENANCE.json');ver=load(out/'VERIFICATION.json')
sources=load(TMP/'source-identities.json')
assert sources==prov['sources'] and len(sources)==14
expected={str(L/r['path']):r['sha256'] for r in t['derived_inputs']+[t['accepted_C_report']]}
expected.update({str(Q/'doc/cp2-review-token-provenance-decision-2026-09-06.md'):t['formal_decision_sha256'],str(Q/'doc/cp2-manual-capability-evidence-decision-2026-09-06.md'):t['non_time_formal_decision_sha256'],str(Q/'doc/cp2-review-timestamp-representation-decision-2026-09-06.md'):t['timestamp_formal_decision_sha256'],str(Q/t['historical_H']['freeze_path']):t['historical_H']['freeze_sha256']})
actual={}
for r in sources:
    p=Path(r['path']);p=p if p.is_absolute() else L/p
    assert str(p) in expected and r['sha256']==expected[str(p)]
    b=checked(p);assert len(b)==r['bytes'] and sha(b)==r['sha256']
    actual[str(p)]=r['sha256']
assert actual==expected
for r in t['derived_inputs']+[t['accepted_C_report']]:
    if not r['path'].endswith('.py'):assert checked(TMP/'inputs'/Path(r['path']).name)==checked(L/r['path'])
bundle=load(TMP/'bundle.json');cp=Q/'tools/asr_review_acquisition_v8'
assert len(bundle)==28 and bundle==sorted(bundle,key=lambda r:r['path'])
assert all(set(r)=={'path','sha256'} and '..' not in Path(r['path']).parts and not Path(r['path']).is_absolute() for r in bundle)
for r in bundle:assert sha(checked(cp/r['path']))==r['sha256']
assert digest(bundle)==t['accepted_C']['bundle']
modules=load(TMP/'modules.json');assert modules==ver['module_identities'] and len(modules)==8
for r in modules:
    p=Path(r['path']);rel=p.relative_to('tools/asr_review_acquisition_v8');assert '..' not in p.parts
    b=checked(Q/p);assert sha(b)==r['sha256'] and len(b)==r['bytes'] and checked(TMP/rel)==b
    assert textgit('rev-parse','HEAD:'+str(p))==r['blob']
contracts=load(TMP/'contracts.json')
for k in ('policy','intake'):assert digest(contracts[k])==t['accepted_C'][k]
for k in ('semantic','role'):assert digest(contracts[k])==t['historical_H'][k]
raw=checked(L/t['derived_inputs'][0]['path']);R0=json.loads(raw)
P=load(L/t['derived_inputs'][6]['path']);pa=load(L/t['derived_inputs'][7]['path'])
assert pa['RESULT']=='ACCEPTED' and pa['P']['sha256']==digest(P)==t['derived_inputs'][6]['sha256']
assert P['operational_authority'] is False and R0['reviewed_at']==P['original_review']['reviewed_at']!=P['created_at']
hv=load(L/t['derived_inputs'][5]['path'])['verification'];hist=t['historical_H']
assert hv['commit']==hist['commit'] and hv['new_files']['freeze.json']['sha256']==hist['freeze_sha256']
for k,v in [('bundle','bundle_sha256'),('policy','policy_sha256'),('semantic','semantic_contract_sha256'),('role','role_contract_sha256')]:assert hist[k]==hv[v]
H=dict(domain='think-manual-H-v1',version=1,context_release=hist['freeze_sha256'],**{k:hist[k] for k in ('bundle','policy','semantic','role')})
R=dict(domain='think-manual-R-v1',version=1,sha256=sha(raw),bytes=len(raw),content_base64=base64.b64encode(raw).decode('ascii'),hash_domain='sha256-exact-original-report-bytes-v1')
b=R0['binding'];s=P['source_identity'];e=P['envelope_identity']
for sk,bk in [('commit','upstream_commit'),('tree','upstream_tree'),('path','source_path'),('git_blob','git_blob_sha1'),('body_sha256','body_sha256'),('body_bytes','body_bytes')]:assert s[sk]==b[bk]
assert e['sha256']==b['envelope_sha256'] and e['bytes']==b['envelope_bytes'] and e['permissions']=='0600'
obj=dict(blob=s['git_blob'],body_bytes=s['body_bytes'],body_sha256=s['body_sha256'],commit=s['commit'],git_mode='100644',git_type='blob',path=s['path'],role=s['role'],tree=s['tree'],historical_envelope=dict(bytes=e['bytes'],domain='historical-private-file-bytes-and-permissions-v1',file_type='regular',permissions='0600',sha256=e['sha256']))
rows=[]
assert len(P['occurrences'])==len(R0['targets'])==2
for p,r in zip(P['occurrences'],R0['targets']):
    for k in ('line','rule','decision','line_sha256','physical_line_sha256','line_byte_start','line_byte_end','token_byte_start','token_byte_end'):assert p[k]==r[k]
    token=p['token_ascii'].encode('ascii')
    assert token==base64.b64decode(p['token_base64'],validate=True)==bytes.fromhex(p['token_hex'])
    assert len(token)==9==p['token_bytes'] and sha(token)==p['token_sha256']
    i=dict(domain='think-manual-occurrence-v1',version=1,object=obj,rule=r['rule'],detector='deny_literal',line=r['line'],line_start=r['line_byte_start'],line_end=r['line_byte_end'],historical_line_domain='sha256-original-physical-line-without-LF-or-CRLF-v1',historical_line_sha256=r['line_sha256'],physical_line_domain='sha256-original-physical-line-including-LF-or-CRLF-v1',physical_line_sha256=r['physical_line_sha256'],token_start=r['token_byte_start'],token_end=r['token_byte_end'],raw_token=p['token_ascii'])
    rows.append(dict(identity=i,occurrence_id=digest(i),decision=r['decision']))
stampraw=R0['reviewed_at']
assert stampraw=='2026-09-06T06:48:22.579140+08:00'
d=dt.datetime.fromisoformat(stampraw);u=d.astimezone(dt.timezone.utc)
delta=u-dt.datetime(1970,1,1,tzinfo=dt.timezone.utc)
instant=delta.days*86400000000+delta.seconds*1000000+delta.microseconds
utc=u.isoformat(timespec='microseconds').replace('+00:00','Z')
stamp=dict(domain='think-review-timestamp-v1',version=1,reviewed_at_raw=stampraw,reviewed_at_utc=utc,fraction_digits=6,offset_minutes=d.utcoffset().seconds//60,epoch='1970-01-01T00:00:00Z',instant_microseconds=instant,raw_hash=dict(domain='sha256-reviewed-at-raw-ascii-v1',sha256=sha(stampraw.encode('ascii'))),utc_hash=dict(domain='sha256-reviewed-at-utc-ascii-v1',sha256=sha(utc.encode('ascii'))))
assert instant==1788648502579140 and utc=='2026-09-05T22:48:22.579140Z'
rep=dict(domain='think-manual-representation-v2',version=2,original_report_sha256=sha(raw),H=digest(H),authority=R0['authorization_record_sha256'],request=R0['request_sha256'],verification_report=R0['verification_report_sha256'],verification_script=R0['verification_script_sha256'],reviewer=R0['reviewer'],reviewed_at=stamp,object=obj,occurrences=rows)
K=dict(domain='think-manual-K-v8',version=8,C=t['accepted_C']['bundle'],H=digest(H),R=sha(raw),representation=digest(rep),authority=rep['authority'],entries=[{k:r[k] for k in ('occurrence_id','decision')} for r in rows],map_schema=t['accepted_C']['intake'],operational_authority=False)
for name,value in [('H',H),('R',R),('representation',rep),('K',K)]:assert checked(out/(name+'.json'))==canonical(value)
script=checked(TMP/'verify.py');assert sha(script)=='b6418d70ffd467a26d3dc316b7dc10caee7a4ce1f93582550b399ab017824315' and len(script)==17659
assert ver['independent_script']['sha256']==sha(script)
for row in ver['scripts']+[c['output'] for c in ver['commands'] if 'output' in c]:
    path=Path(row['path']);assert path.parent==TMP
    data=checked(path);assert sha(data)==row['sha256'] and len(data)==row['bytes']
assert ver['production_result']==load(TMP/'production.json') and ver['core_result']==load(TMP/'core-result.json')
assert textgit('rev-parse','HEAD')==HEAD and not git('status','--porcelain=v1','--untracked-files=all')
result=dict(RESULT='PASS',task_id=TASK,commit=HEAD,parent=t['baseline_commit'],root_tree=textgit('rev-parse','HEAD^{tree}'),output_tree=textgit('rev-parse','HEAD:'+directory),worktree_clean=True,files=records,old_git_records=len(retained),old_tree_record_sha256=sha(old),manifest_collection=manifest['collection_sha256'],sources_verified=len(sources),bundle_files=28,module_files=8,canonical_objects_rebuilt=['H','R','representation','K'],identities=dict(H=digest(H),original_R=sha(raw),representation=digest(rep),K=digest(K),P=digest(P),P_acceptance=t['predecessor_acceptance_sha256'],timestamp=digest(stamp)),occurrence_ids=[r['occurrence_id'] for r in rows],independent_time_method='datetime civil arithmetic with integer timedelta days/seconds/microseconds; exact fixed ISO value asserted first; no floating timestamp',developer_verifier_preflight='PASS; exact reviewed script and bounded local data inputs checked before separate execution',limitations=['No private/source pointers followed; source truth inherited from accepted R/P.','No candidate/controller/transport/P or historical verifier execution; no new authority.'])
print(json.dumps(result,sort_keys=True,indent=2))
