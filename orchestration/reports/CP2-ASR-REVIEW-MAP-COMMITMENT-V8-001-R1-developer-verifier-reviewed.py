"""Independent standard-library verifier; never imports the candidate or source.
Gregorian computation is self-contained integer arithmetic, not datetime.
--core checks six documents; --final additionally checks VERIFICATION/MANIFEST.
"""
import sys,json,hashlib,base64,re,stat
from pathlib import Path
ROOT=Path(__file__).resolve().parent
PROJECT=Path('/Users/orderly_ray/Projects/think')
LEADER=Path('/Users/orderly_ray/Leader')
network_events=[]
def deny(event,args):
    if event.startswith(('socket.','http.client.','subprocess.')) or event in ('os.system','os.fork','os.forkpty','os.posix_spawn','os.exec'):
        network_events.append(event);raise RuntimeError('forbidden capability')
sys.addaudithook(deny)
def canon(v):return (json.dumps(v,ensure_ascii=True,allow_nan=False,sort_keys=True,separators=(',',':'))+'\n').encode('ascii')
def sha(b):return hashlib.sha256(b).hexdigest()
def digest(v):return sha(canon(v))
def load(p):return json.loads(p.read_bytes())
def file_record(p):
    b=p.read_bytes();s=p.lstat();assert stat.S_ISREG(s.st_mode) and s.st_nlink==1
    return dict(path=p.name,bytes=len(b),sha256=sha(b),git_blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),mode='100644',type='blob')
t=load(ROOT/'task.json');assert sha((ROOT/'task.json').read_bytes())=='9e0b08359157e76dc53c3ce5c19adf745756e02a32aab38ef2d9553d602839a1'
out=PROJECT/t['output_directory']
source_records=load(ROOT/'source-identities.json');inputs={}
for row in source_records:
    p=Path(row['path']);p=p if p.is_absolute() else LEADER/p
    b=p.read_bytes();assert len(b)==row['bytes'] and sha(b)==row['sha256']
    # Old verify.py and historical freeze are opaque hashes, never decoded.
    if p.suffix=='.json' and not row.get('read','').startswith('opaque'):
        inputs[p.name]=json.loads(b)
for row in t['derived_inputs']+[t['accepted_C_report']]:
    b=(LEADER/row['path']).read_bytes();assert sha(b)==row['sha256'];assert len(b)==row.get('bytes',len(b))
    if not row['path'].endswith('.py'):assert (ROOT/'inputs'/Path(row['path']).name).read_bytes()==b
orig=inputs['CP2-ASR-REAL-COMMENT-CAPABILITY-REVIEW-001.json'];raw=(ROOT/'inputs/CP2-ASR-REAL-COMMENT-CAPABILITY-REVIEW-001.json').read_bytes()
review_ver=inputs['CP2-ASR-REAL-COMMENT-CAPABILITY-REVIEW-001-verification.json'];auth=inputs['CP2-ASR-REAL-COMMENT-REVIEW-AUTHORIZATION-001-approved.json'];request=inputs['CP2-ASR-REAL-COMMENT-REVIEW-AUTHORIZATION-001.json']
P=inputs['CP2-ASR-REVIEW-TOKEN-PROVENANCE-COMPLETION-001-P.json'];pa=inputs['CP2-ASR-REVIEW-TOKEN-PROVENANCE-COMPLETION-001-acceptance.json'];pv=inputs['CP2-ASR-REVIEW-TOKEN-PROVENANCE-COMPLETION-001-verification.json']
P_hash=t['derived_inputs'][6]['sha256'];assert digest(P)==P_hash
assert pa['RESULT']=='ACCEPTED' and pa['P']['sha256']==P_hash and pa['P']['bytes']==7092
assert pv['RESULT']=='PASS' and pv['P_sha256']==P_hash and pv['P_bytes']==7092 and pv['whole_P_reconstructed_equal'] is True and pv['exact_slice_count']==2
assert pv['network_events']==[] and P['operational_authority'] is False and all(v is False for v in P['effect'].values())
assert orig['binding']==review_ver['binding']==auth['binding']==request['binding']
assert orig['RESULT']=='COMPLETE' and orig['review_status']=='ACCEPTED_BY_LEADER' and review_ver['RESULT']=='PASS'
assert auth['request_sha256']==orig['request_sha256']==t['derived_inputs'][3]['sha256']
assert orig['authorization_record_sha256']==t['derived_inputs'][2]['sha256']
assert orig['verification_report_sha256']==t['derived_inputs'][1]['sha256'] and orig['verification_script_sha256']==t['derived_inputs'][4]['sha256']
pr=P['original_review'];history=t['historical_H']
expected_review=dict(approval_sha256=orig['authorization_record_sha256'],historical_context_freeze_commit=history['commit'],historical_context_freeze_sha256=history['freeze_sha256'],original_formal_decision_sha256=orig['formal_decision_sha256'],report_sha256=sha(raw),request_sha256=orig['request_sha256'],reviewed_at=orig['reviewed_at'],reviewer=orig['reviewer'],verification_report_sha256=orig['verification_report_sha256'],verification_script_sha256=orig['verification_script_sha256'])
assert pr==expected_review and orig['freeze_commit']==request['freeze_commit']==history['commit']
assert P['created_at']!=pr['reviewed_at']
contracts=load(ROOT/'contracts.json');C=t['accepted_C'];ca=inputs['CP2-ASR-REVIEW-TIMESTAMP-REPRESENTATION-OFFLINE-001-acceptance.json']
assert ca['RESULT']=='ACCEPTED' and ca['candidate_commit']==C['commit'] and ca['candidate_tree']==C['tree'] and ca['bundle_sha256']==C['bundle']
for name in ['intake','policy']:assert digest(contracts[name])==C[name]
for name in ['semantic','role']:assert digest(contracts[name])==history[name]
# Rebuild intake constants independently rather than trust producer's contract object.
time_contract=dict(domain='think-review-timestamp-v1',version=1,raw_bytes_limit=128,grammar='YYYY-MM-DDTHH:MM:SS[.1..6 digits](Z|+HH:MM|-HH:MM)',calendar='proleptic Gregorian; raw and UTC years0001..9999',fraction_digits=[0,6],offset_minutes=[-840,840],unknown_offset='-00:00 rejected',epoch='1970-01-01T00:00:00Z',instant_microseconds=[-62135596800000000,253402300799999999],raw_hash_domain='sha256-reviewed-at-raw-ascii-v1',utc_hash_domain='sha256-reviewed-at-utc-ascii-v1',conversion='exact integer microseconds; UTC same fraction digits; reject UTC overflow',identity='exact raw and UTC ASCII hashes plus entire canonical object; instant equality is not identity')
def domain(n):return 'think-manual-'+n+'-v'+str(1 if n in ('H','R','occurrence') else 2 if n=='representation' else 8)
historical_line='sha256-original-physical-line-without-LF-or-CRLF-v1';physical_line='sha256-original-physical-line-including-LF-or-CRLF-v1'
intake=dict(version=8,package_bytes=262144,occurrences=64,text_bytes=128,revision='v8-lossless-review-timestamp',timestamp=time_contract,original_report='R=SHA256(exact original bytes); representation=canonical independent digest',envelope_permissions='historical regular/0600; source Git blob/100644',domains={n:domain(n) for n in ('package','H','R','representation','K','F','M','A','T','N','occurrence','adjudication','rejection')},C='sha256-canonical-sorted-candidate-path-sha256-collection',line_domains=[historical_line,physical_line],decisions=['comment_only_nonoperative_for_this_body','forbidden','unresolved','pending'],dag=['H>R','H/R/C>K','C/K>F','F/K/R>M','F/M>A','F/M/A>T','F/M/T+input>N'],historic_envelope='R-only; never equal execution envelope; exact source object must match',pending='append-only effective status; original report stays pending',hard_stops='all original stops outrank manual comment clearance',canonical='sorted keys,ascii,compact,no nonfinite,one LF; no self digest')
assert canon(intake)==canon(contracts['intake']) and digest(intake)==C['intake']
cp=PROJECT/'tools/asr_review_acquisition_v8';bundle=load(ROOT/'bundle.json')
actual_paths=sorted([str(p.relative_to(cp)) for p in (cp/'offline_review').glob('*.py')]+[str(p.relative_to(cp)) for p in (cp/'tests').glob('*.py')]+['audit.py','verify.py','network_guard.py','recalculate.py','SCHEMA.md'])
assert actual_paths==[x['path'] for x in bundle] and len(bundle)==28
for row in bundle:assert sha((cp/row['path']).read_bytes())==row['sha256']
assert digest(bundle)==C['bundle']
for row in load(ROOT/'modules.json'):
    b=(PROJECT/row['path']).read_bytes();assert sha(b)==row['sha256'] and len(b)==row['bytes'];assert (ROOT/Path(row['path']).relative_to('tools/asr_review_acquisition_v8')).read_bytes()==b
hv=inputs['CP2-ASR-SOURCE-SEMANTICS-RELEASE-FREEZE-001-acceptance.json']['verification']
assert hv['commit']==history['commit'] and hv['new_files']['freeze.json']['sha256']==history['freeze_sha256']
for name,key in [('bundle','bundle_sha256'),('policy','policy_sha256'),('semantic','semantic_contract_sha256'),('role','role_contract_sha256')]:assert history[name]==hv[key]
H=dict(domain=domain('H'),version=1,context_release=history['freeze_sha256'],**{k:history[k] for k in ('bundle','policy','semantic','role')})
R=dict(domain=domain('R'),version=1,sha256=sha(raw),bytes=len(raw),content_base64=base64.b64encode(raw).decode('ascii'),hash_domain='sha256-exact-original-report-bytes-v1')
b=orig['binding'];s=P['source_identity'];e=P['envelope_identity']
assert s==dict(commit=b['upstream_commit'],tree=b['upstream_tree'],path=b['source_path'],git_blob=b['git_blob_sha1'],body_sha256=b['body_sha256'],body_bytes=b['body_bytes'],role='cpp_source_header')
assert e==dict(bytes=b['envelope_bytes'],file_type='regular',nlink=1,nofollow=True,path=b['private_envelope'],permissions=b['required_file_mode'],private_parent_permissions=b['required_parent_modes'],sha256=b['envelope_sha256'])
assert b['required_type']=='regular single-link with no symlink parent' and e['permissions']=='0600' and e['private_parent_permissions']=='0700'
assert review_ver['body_envelope_regular_singlelink_0600'] is True and review_ver['body_and_blob_hashes_verified'] is True
assert contracts['role']['seeds'][s['path']]==s['role'] and contracts['policy']['mode']=='100644' and contracts['policy']['type']=='blob'
obj=dict(commit=s['commit'],tree=s['tree'],path=s['path'],blob=s['git_blob'],body_sha256=s['body_sha256'],body_bytes=s['body_bytes'],role=s['role'],git_type='blob',git_mode='100644',historical_envelope=dict(sha256=e['sha256'],bytes=e['bytes'],file_type=e['file_type'],permissions=e['permissions'],domain='historical-private-file-bytes-and-permissions-v1'))
assert obj['commit']==contracts['policy']['commit'] and obj['tree']==contracts['policy']['tree']
rows=[];token_evidence=[]
assert len(orig['targets'])==len(P['occurrences'])==len(review_ver['targets'])==len(b['targets'])==2
for i,(r,p,v) in enumerate(zip(orig['targets'],P['occurrences'],review_ver['targets'])):
    for k in ('line','rule','line_sha256','physical_line_sha256','line_byte_start','line_byte_end','token_byte_start','token_byte_end'):assert r[k]==p[k]==v[k]
    assert r['decision']==p['decision']=='comment_only_nonoperative_for_this_body'
    assert r['source_path']==s['path'] and r['body_sha256']==s['body_sha256']
    assert b['targets'][i]==dict(line=r['line'],line_sha256=r['line_sha256'])
    token=p['token_ascii'].encode('ascii');assert len(token)==p['token_bytes']==r['token_byte_end']-r['token_byte_start']==9
    assert all(32<=c<=126 for c in token) and token.lower().decode()==p['rule']==b['rule']
    assert base64.b64decode(p['token_base64'],validate=True)==bytes.fromhex(p['token_hex'])==token
    assert base64.b64encode(token).decode()==p['token_base64'] and token.hex()==p['token_hex']
    assert sha(token)==p['token_sha256'] and p['token_hash_domain']=='sha256-original-token-bytes-at-absolute-interval-v1'
    assert p['historical_line_hash_domain']==historical_line and p['physical_line_hash_domain']==physical_line
    assert r['line_starts_with_comment_marker'] is True and r['ends_with_continuation'] is False
    assert r['rule'] in contracts['semantic']['detectors']['deny'] and r['rule']=='websocket'
    # Static reviewed semantics.py:194-207: only deny_literal yields websocket;
    # other branches yield file_audio or dynamic_paths. No scanner invocation.
    identity=dict(domain=domain('occurrence'),version=1,object=obj,rule=r['rule'],detector='deny_literal',line=r['line'],line_start=r['line_byte_start'],line_end=r['line_byte_end'],historical_line_domain=historical_line,historical_line_sha256=r['line_sha256'],physical_line_domain=physical_line,physical_line_sha256=r['physical_line_sha256'],token_start=r['token_byte_start'],token_end=r['token_byte_end'],raw_token=p['token_ascii'])
    assert 0<=identity['line_start']<=identity['token_start']<identity['token_end']<=identity['line_end']<=obj['body_bytes']
    rows.append(dict(identity=identity,occurrence_id=digest(identity),decision=r['decision']))
    token_evidence.append(dict(line=r['line'],start=r['token_byte_start'],end=r['token_byte_end'],bytes=len(token),sha256=sha(token),P_path='/occurrences/'+str(i)+'/token_ascii'))
assert rows[0]['occurrence_id']!=rows[1]['occurrence_id'] and rows[0]['identity']['token_end']<=rows[1]['identity']['token_start']
# Independent integer Gregorian conversion; offsets move wall-clock minutes,
# civil date adjustment and epoch day count do not use datetime or producer code.
def leap(y):return y%4==0 and (y%100!=0 or y%400==0)
def months(y):return [31,29 if leap(y) else 28,31,30,31,30,31,31,30,31,30,31]
time_raw=orig['reviewed_at'];assert time_raw==pr['reviewed_at'] and time_raw.isascii()
m=re.fullmatch(r'([0-9]{4})-([0-9]{2})-([0-9]{2})T([0-9]{2}):([0-9]{2}):([0-9]{2})\.([0-9]{6})([+-])([0-9]{2}):([0-9]{2})',time_raw);assert m
Y,M,D,hh,mm,ss=map(int,m.groups()[:6]);frac=m[7];oh,om=int(m[9]),int(m[10]);offset=(oh*60+om)*(1 if m[8]=='+' else -1)
assert 1<=Y<=9999 and 1<=M<=12 and 1<=D<=months(Y)[M-1] and hh<24 and mm<60 and ss<60 and abs(offset)<=840 and om<60
micro=int(frac);days=sum(366 if leap(y) else 365 for y in range(1970,Y))+sum(months(Y)[:M-1])+D-1
instant=((days*24+hh)*3600+mm*60+ss-offset*60)*1000000+micro
uy,um,ud=Y,M,D;minute=hh*60+mm-offset
while minute<0:
    minute+=1440;ud-=1
    if ud==0:
        um-=1
        if um==0:uy-=1;um=12
        ud=months(uy)[um-1]
while minute>=1440:
    minute-=1440;ud+=1
    if ud>months(uy)[um-1]:
        ud=1;um+=1
        if um==13:uy+=1;um=1
utc='%04d-%02d-%02dT%02d:%02d:%02d.%sZ'%(uy,um,ud,minute//60,minute%60,ss,frac)
assert utc=='2026-09-05T22:48:22.579140Z' and offset==480 and micro==579140 and instant==1788648502579140
stamp=dict(domain='think-review-timestamp-v1',version=1,reviewed_at_raw=time_raw,reviewed_at_utc=utc,fraction_digits=6,offset_minutes=offset,epoch='1970-01-01T00:00:00Z',instant_microseconds=instant,raw_hash=dict(domain='sha256-reviewed-at-raw-ascii-v1',sha256=sha(time_raw.encode('ascii'))),utc_hash=dict(domain='sha256-reviewed-at-utc-ascii-v1',sha256=sha(utc.encode('ascii'))))
rep=dict(domain=domain('representation'),version=2,original_report_sha256=sha(raw),H=digest(H),authority=orig['authorization_record_sha256'],request=orig['request_sha256'],verification_report=orig['verification_report_sha256'],verification_script=orig['verification_script_sha256'],reviewer=orig['reviewer'],reviewed_at=stamp,object=obj,occurrences=rows)
K=dict(domain=domain('K'),version=8,C=C['bundle'],H=digest(H),R=sha(raw),representation=digest(rep),authority=rep['authority'],entries=[{k:r[k] for k in ('occurrence_id','decision')} for r in rows],map_schema=digest(intake),operational_authority=False)
for name,obj_expected in [('H',H),('R',R),('representation',rep),('K',K)]:assert (out/(name+'.json')).read_bytes()==canon(obj_expected)
assert base64.b64decode(load(out/'R.json')['content_base64'],validate=True)==raw and len(raw)==7051
assert not any(n.startswith('offline_review') for n in sys.modules)
provenance=load(out/'PROVENANCE.json');assert provenance['P']['sha256']==P_hash and provenance['P']['acceptance_sha256']==t['predecessor_acceptance_sha256']
assert provenance['sources']==source_records
# Exhaustive coverage of all canonical object leaf fields, including copies of object identity.
def leaves(v,p=''):
    if isinstance(v,dict):
        for k,x in v.items():yield from leaves(x,p+'/'+k)
    elif isinstance(v,list):
        for i,x in enumerate(v):yield from leaves(x,p+'/'+str(i))
    else:yield p
mapped=[m['target'] for m in provenance['field_mapping']]
expected_targets=[name+'.json#'+p for name,obj_expected in [('H',H),('R',R),('representation',rep),('K',K)] for p in leaves(obj_expected)]
assert sorted(mapped)==sorted(expected_targets) and len(mapped)==len(set(mapped))
for record in provenance['field_mapping']:assert record['sources'] and record['derivation']
for name in ('H','R','representation','K','PROVENANCE'):
    b=(out/(name+'.json')).read_bytes();assert canon(json.loads(b))==b
files=['H.json','R.json','representation.json','K.json','PROVENANCE.json','REPORT.md']
if '--final' in sys.argv:
    files+=['VERIFICATION.json','MANIFEST.json'];assert set(p.name for p in out.iterdir())==set(files)
    v=load(out/'VERIFICATION.json');assert v['independent_script']['sha256']==sha(Path(__file__).read_bytes()) and v['P']['sha256']==P_hash
    for rec in v['core_result']['files']:assert rec==file_record(out/rec['path'])
    assert v['core_result']['RESULT']=='PASS' and v['production_result']['RESULT']=='PASS'
    manifest=load(out/'MANIFEST.json');expected_records=[file_record(out/n) for n in sorted(files) if n!='MANIFEST.json']
    assert manifest['files']==expected_records and manifest['collection_sha256']==digest(expected_records)
    for n in ('VERIFICATION','MANIFEST'):assert (out/(n+'.json')).read_bytes()==canon(load(out/(n+'.json')))
result=dict(RESULT='PASS',phase='final' if '--final' in sys.argv else 'core',files=[file_record(out/n) for n in sorted(files)],identities=dict(H=digest(H),original_R=sha(raw),R_wrapper=digest(R),representation=digest(rep),K=digest(K),C=C['bundle'],intake=digest(intake),P=P_hash,P_acceptance=t['predecessor_acceptance_sha256'],timestamp=digest(stamp)),timestamp=stamp,occurrence_ids=[r['occurrence_id'] for r in rows],token_evidence=token_evidence,field_mapping_leaves=len(mapped),sources_rehashed=len(source_records),bundle_files_rehashed=len(bundle),independent_module_imports=[],network_events=network_events,limits='Derived references and arithmetic only; original body/line/blob/envelope truth inherited from accepted reports, not re-read; configured source Git mode/type from accepted contract; no full package, future objects, controller or runtime validation.')
assert network_events==[]
print(json.dumps(result,sort_keys=True,separators=(',',':')))
