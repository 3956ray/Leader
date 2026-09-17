"""One fixed retained object; hash-only context and two exact token slices.
Never import the old verifier, candidate, transport or third-party source.
"""
import sys
if sys.flags.optimize != 0:
    raise SystemExit("token_provenance_blocked: optimized Python is prohibited")
NETWORK_EVENTS = []
def guard(event, args):
    if event.startswith(('socket.', 'http.client.', 'subprocess.')) or event in ('os.system','os.fork','os.forkpty','os.posix_spawn','os.exec'):
        NETWORK_EVENTS.append(event)
        raise RuntimeError('forbidden capability')
sys.addaudithook(guard)
import os, stat, json, hashlib, base64
from pathlib import Path
from datetime import datetime, timezone, timedelta
BASE = Path('/Users/orderly_ray/Leader')
TASK = 'CP2-ASR-REVIEW-TOKEN-PROVENANCE-COMPLETION-001'
TASK_SHA = '971da8c613afdb57d47c8ba408154f217a3eb796e9013da592bdb43dfc3abfd9'
def sha(raw):return hashlib.sha256(raw).hexdigest()
def canonical(value):return (json.dumps(value,sort_keys=True,ensure_ascii=True,separators=(',',':'),allow_nan=False)+'\n').encode('ascii')
def ref(path):
    raw=path.read_bytes();return {'path':str(path),'bytes':len(raw),'sha256':sha(raw)}
def publish(path,raw):
    with path.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
def strict(raw):
    def pairs(rows):
        d={}
        for k,v in rows:
            if k in d:raise ValueError('duplicate field')
            d[k]=v
        return d
    return json.loads(raw.decode('utf-8'),object_pairs_hook=pairs)
def main():
    tp=BASE/'orchestration/tasks'/(TASK+'.json');traw=tp.read_bytes();assert sha(traw)==TASK_SHA
    task=strict(traw);assert task['owner']=='leader'
    refs=task['fixed_references'];contents={}
    for row in refs:
        path=Path(row['path']);raw=path.read_bytes();assert len(raw)==row['bytes'] and sha(raw)==row['sha256'];contents[path.name]=raw
    R=strict(contents['CP2-ASR-REAL-COMMENT-CAPABILITY-REVIEW-001.json']);V=strict(contents['CP2-ASR-REAL-COMMENT-CAPABILITY-REVIEW-001-verification.json']);Q=strict(contents['CP2-ASR-REAL-COMMENT-REVIEW-AUTHORIZATION-001.json']);A=strict(contents['CP2-ASR-REAL-COMMENT-REVIEW-AUTHORIZATION-001-approved.json'])
    B=task['fixed_binding'];assert R['binding']==V['binding']==Q['binding']==A['binding']==B and A['user_response']=='批准'
    assert R['verification_report_sha256']==sha(contents['CP2-ASR-REAL-COMMENT-CAPABILITY-REVIEW-001-verification.json']) and R['verification_script_sha256']==sha(contents['CP2-ASR-REAL-COMMENT-CAPABILITY-REVIEW-001-verify.py'])
    assert R['authorization_record_sha256']==sha(contents['CP2-ASR-REAL-COMMENT-REVIEW-AUTHORIZATION-001-approved.json']) and R['request_sha256']==A['request_sha256']==sha(contents['CP2-ASR-REAL-COMMENT-REVIEW-AUTHORIZATION-001.json'])
    assert R['freeze_commit']=='d78577b8bac1108791e0c4ba3c7a0cd672958c94'
    fixed=task['fixed_targets'];assert [(x['line'],x['token_byte_start'],x['token_byte_end']) for x in fixed]==[(57,1893,1902),(60,1972,1981)]
    for x,r,v in zip(fixed,R['targets'],V['targets']):
        assert all(x[k]==r[k] for k in x)
        assert all(x[k]==v[k] for k in x if k!='decision')
    assert len(fixed)==len(R['targets'])==len(V['targets'])==2
    target=Path(B['private_envelope']);assert str(target)=='/private/tmp/think-asr-v5-acquisition-hqssnorn/run/body-0002.json'
    directory=os.open('/',os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW);chain=[]
    try:
        for index,part in enumerate(target.parts[1:-1]):
            child=os.open(part,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=directory);os.close(directory);directory=child
            st=os.fstat(directory);assert stat.S_ISDIR(st.st_mode)
            if index>=2:assert stat.S_IMODE(st.st_mode)==0o700 and st.st_uid==os.getuid()
            chain.append({'component':part,'directory':True,'nofollow':True,'mode':format(stat.S_IMODE(st.st_mode),'04o')})
        fd=os.open(target.name,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK,dir_fd=directory)
        try:
            before=os.fstat(fd);assert stat.S_ISREG(before.st_mode) and before.st_nlink==1 and stat.S_IMODE(before.st_mode)==0o600 and before.st_uid==os.getuid() and before.st_size==8579==B['envelope_bytes']
            raw=os.read(fd,8580);assert len(raw)==8579 and os.read(fd,1)==b''
            after=os.fstat(fd);assert (before.st_dev,before.st_ino,before.st_size,before.st_mtime_ns,before.st_ctime_ns)==(after.st_dev,after.st_ino,after.st_size,after.st_mtime_ns,after.st_ctime_ns)
            assert sha(raw)==B['envelope_sha256']
        finally:os.close(fd)
    finally:os.close(directory)
    obj=strict(raw);assert type(obj['text']) is str
    body=obj['text'].encode('utf-8');assert b'\0' not in body and len(body)==7939==B['body_bytes'] and sha(body)==B['body_sha256']
    assert hashlib.sha1(b'blob '+str(len(body)).encode()+b'\0'+body).hexdigest()==B['git_blob_sha1']
    assert obj['path']==B['source_path'] and obj['role']=='cpp_source_header' and obj['sha256']==B['body_sha256'] and obj['blob_sha']==B['git_blob_sha1'] and type(obj['bytes']) is int and obj['bytes']==7939
    physical=body.splitlines(keepends=True);records=[]
    for x in fixed:
        start=sum(map(len,physical[:x['line']-1]));line=physical[x['line']-1];end=start+len(line)
        assert start==x['line_byte_start'] and end==x['line_byte_end']
        historical=line[:-2] if line.endswith(b'\r\n') else line[:-1] if line.endswith(b'\n') else line
        assert sha(line)==x['physical_line_sha256'] and sha(historical)==x['line_sha256']
        a,z=x['token_byte_start'],x['token_byte_end'];assert start<=a<z<=end and z-a==9
        token=body[a:z];assert len(token)==9 and all(32<=c<=126 for c in token) and token.lower()==b'websocket' and x['rule']=='websocket' and x['decision']=='comment_only_nonoperative_for_this_body'
        ascii_value=token.decode('ascii');b64=base64.b64encode(token).decode('ascii');hex_value=token.hex()
        assert base64.b64decode(b64,validate=True)==bytes.fromhex(hex_value)==ascii_value.encode('ascii')==token
        records.append({**x,'historical_line_hash_domain':'sha256-original-physical-line-without-LF-or-CRLF-v1','physical_line_hash_domain':'sha256-original-physical-line-including-LF-or-CRLF-v1','token_ascii':ascii_value,'token_base64':b64,'token_hex':hex_value,'token_bytes':9,'token_hash_domain':'sha256-original-token-bytes-at-absolute-interval-v1','token_sha256':sha(token)})
    assert len(records)==2 and not NETWORK_EVENTS
    for row in refs:assert ref(Path(row['path']))==row
    script=ref(Path(__file__).absolute())
    P={'domain':'think-manual-token-provenance-v1','version':1,'task':{'id':TASK,'contract_sha256':TASK_SHA},'created_at':datetime.now(timezone(timedelta(hours=8))).isoformat(timespec='microseconds'),'producer_script':script,'references':refs,'authority_basis':task['authority'],'original_review':{'report_sha256':sha(contents['CP2-ASR-REAL-COMMENT-CAPABILITY-REVIEW-001.json']),'verification_report_sha256':R['verification_report_sha256'],'verification_script_sha256':R['verification_script_sha256'],'request_sha256':R['request_sha256'],'approval_sha256':R['authorization_record_sha256'],'historical_context_freeze_commit':R['freeze_commit'],'historical_context_freeze_sha256':sha(contents['freeze.json']),'original_formal_decision_sha256':R['formal_decision_sha256'],'reviewer':R['reviewer'],'reviewed_at':R['reviewed_at']},'source_identity':{'commit':B['upstream_commit'],'tree':B['upstream_tree'],'path':B['source_path'],'body_sha256':B['body_sha256'],'body_bytes':B['body_bytes'],'git_blob':B['git_blob_sha1'],'role':'cpp_source_header'},'envelope_identity':{'path':str(target),'sha256':B['envelope_sha256'],'bytes':B['envelope_bytes'],'file_type':'regular','nlink':1,'permissions':'0600','private_parent_permissions':'0700','nofollow':True},'read_receipt':{'private_files_read':1,'envelope_bytes_read':8579,'directory_chain':chain,'stable_descriptor_identity':True,'context_use':'hash and interval verification only; no semantic inspection','source_bytes_exported':18,'exported_intervals':[[1893,1902],[1972,1981]],'actual_network_events':NETWORK_EVENTS},'occurrences':records,'operational_authority':False,'effect':{'original_R_modified':False,'new_review_decision':False,'pending_cleared':False,'acquisition_authorized':False,'K_created':False},'scope':'Exact token byte provenance only. Original review time/decision unchanged; no field/API/source/runtime/license/CP2 approval.'}
    ppath=BASE/task['outputs']['P'];praw=canonical(P);assert not ppath.exists();publish(ppath,praw)
    result={'RESULT':'token_provenance_complete_for_acceptance','P':ref(ppath),'script':script,'task_sha256':TASK_SHA,'private_files_read':1,'exact_token_intervals':[[1893,1902],[1972,1981]],'source_bytes_exported':18,'old_references_unchanged':True,'network_events':NETWORK_EVENTS,'independent_acceptance':'pending'}
    publish(BASE/task['outputs']['producer_result'],canonical(result));print(json.dumps({'RESULT':result['RESULT'],'P_sha256':sha(praw),'P_bytes':len(praw),'tokens':2}))
if __name__=='__main__':main()
