"""Independent P acceptance reader; never imports or executes the producer."""
import sys
if sys.flags.optimize != 0:
    raise SystemExit("token_provenance_blocked: optimized Python is prohibited")
CAPABILITIES=[]
def deny(event,args):
    if event.startswith(('socket.','http.client.','subprocess.')) or event in ('os.system','os.fork','os.forkpty','os.posix_spawn','os.exec'):
        CAPABILITIES.append(event)
        raise RuntimeError('forbidden capability')
sys.addaudithook(deny)
import os,json,hashlib,stat,base64,re
from pathlib import Path
from datetime import datetime
ROOT=Path('/Users/orderly_ray/Leader')
TID='CP2-ASR-REVIEW-TOKEN-PROVENANCE-COMPLETION-001'
TH='971da8c613afdb57d47c8ba408154f217a3eb796e9013da592bdb43dfc3abfd9'
def digest(raw):return hashlib.sha256(raw).hexdigest()
def enc(obj):return (json.dumps(obj,ensure_ascii=True,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
def doc(raw):
    def pairs(values):
        d={}
        for key,value in values:
            assert key not in d;d[key]=value
        return d
    return json.loads(raw,object_pairs_hook=pairs)
def main():
    tr=(ROOT/'orchestration/tasks'/(TID+'.json')).read_bytes();assert digest(tr)==TH;t=doc(tr)
    pb=(ROOT/t['outputs']['P']).read_bytes();P=doc(pb);assert enc(P)==pb
    production=doc((ROOT/t['outputs']['producer_result']).read_bytes())
    assert production['RESULT']=='token_provenance_complete_for_acceptance' and production['P']=={'path':str(ROOT/t['outputs']['P']),'bytes':len(pb),'sha256':digest(pb)}
    values={}
    for x in t['fixed_references']:
        raw=Path(x['path']).read_bytes();assert len(raw)==x['bytes'] and digest(raw)==x['sha256'];values[Path(x['path']).name]=raw
    r=doc(values['CP2-ASR-REAL-COMMENT-CAPABILITY-REVIEW-001.json']);v=doc(values['CP2-ASR-REAL-COMMENT-CAPABILITY-REVIEW-001-verification.json']);q=doc(values['CP2-ASR-REAL-COMMENT-REVIEW-AUTHORIZATION-001.json']);approval=doc(values['CP2-ASR-REAL-COMMENT-REVIEW-AUTHORIZATION-001-approved.json']);B=t['fixed_binding']
    assert r['binding']==v['binding']==q['binding']==approval['binding']==B and approval['user_response']=='批准'
    assert r['request_sha256']==approval['request_sha256']==digest(values['CP2-ASR-REAL-COMMENT-REVIEW-AUTHORIZATION-001.json'])
    assert r['authorization_record_sha256']==digest(values['CP2-ASR-REAL-COMMENT-REVIEW-AUTHORIZATION-001-approved.json'])
    assert r['verification_report_sha256']==digest(values['CP2-ASR-REAL-COMMENT-CAPABILITY-REVIEW-001-verification.json']) and r['verification_script_sha256']==digest(values['CP2-ASR-REAL-COMMENT-CAPABILITY-REVIEW-001-verify.py'])
    # This acceptance stage reopens only the one authorized object, through descriptors.
    components=('private','tmp','think-asr-v5-acquisition-hqssnorn','run');chain=[];descriptors=[]
    try:
        parent=os.open('/',os.O_DIRECTORY|os.O_RDONLY|os.O_NOFOLLOW);descriptors.append(parent)
        for part in components:
            parent=os.open(part,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=parent);descriptors.append(parent);s=os.fstat(parent)
            assert stat.S_ISDIR(s.st_mode)
            if part in components[2:]:assert stat.S_IMODE(s.st_mode)==448 and s.st_uid==os.getuid()
            chain.append(dict(component=part,directory=True,nofollow=True,mode=format(stat.S_IMODE(s.st_mode),'04o')))
        f=os.open('body-0002.json',os.O_RDONLY|os.O_NONBLOCK|os.O_NOFOLLOW,dir_fd=parent);descriptors.append(f);before=os.fstat(f)
        assert stat.S_ISREG(before.st_mode) and stat.S_IMODE(before.st_mode)==384 and before.st_nlink==1 and before.st_uid==os.getuid() and before.st_size==8579
        chunks=[];remaining=8579
        while remaining:
            chunk=os.read(f,min(remaining,2048));assert chunk;chunks.append(chunk);remaining-=len(chunk)
        assert os.read(f,1)==b'';after=os.fstat(f)
        for attribute in ['st_dev','st_ino','st_size','st_mtime_ns','st_ctime_ns','st_nlink','st_mode','st_uid']:assert getattr(before,attribute)==getattr(after,attribute)
        envelope=b''.join(chunks);assert digest(envelope)==B['envelope_sha256'] and len(envelope)==B['envelope_bytes']
    finally:
        for fd in reversed(descriptors):os.close(fd)
    e=doc(envelope);body=e['text'].encode('utf8')
    assert len(body)==B['body_bytes']==7939 and digest(body)==B['body_sha256'] and b'\0' not in body
    assert hashlib.sha1(b'blob 7939\x00'+body).hexdigest()==B['git_blob_sha1']
    assert (e['path'],e['role'],e['sha256'],e['blob_sha'],e['bytes'])==(B['source_path'],'cpp_source_header',B['body_sha256'],B['git_blob_sha1'],7939)
    # LF boundary walk, independent of producer splitlines/sum implementation.
    boundaries=[0]
    for pos,byte in enumerate(body):
        if byte==10:boundaries.append(pos+1)
    if boundaries[-1]!=len(body):boundaries.append(len(body))
    expected_rows=[]
    assert len(r['targets'])==len(v['targets'])==len(t['fixed_targets'])==2
    for i,x in enumerate(t['fixed_targets']):
        assert all(r['targets'][i][k]==value for k,value in x.items())
        assert all(v['targets'][i][k]==value for k,value in x.items() if k!='decision')
        n=x['line'];a,z=boundaries[n-1:n+1];assert (a,z)==(x['line_byte_start'],x['line_byte_end'])
        line=body[a:z];cut=z
        if cut>a and body[cut-1]==10:cut-=1
        if cut>a and body[cut-1]==13:cut-=1
        assert digest(line)==x['physical_line_sha256'] and digest(body[a:cut])==x['line_sha256']
        left,right=x['token_byte_start'],x['token_byte_end'];assert (left,right)==[(1893,1902),(1972,1981)][i] and a<=left<right<=z
        token=body[left:right];assert len(token)==9 and all(32<=v<=126 for v in token) and token.decode('ascii').lower()=='websocket'
        assert x['rule']=='websocket' and x['decision']=='comment_only_nonoperative_for_this_body'
        row={**x,'historical_line_hash_domain':'sha256-original-physical-line-without-LF-or-CRLF-v1','physical_line_hash_domain':'sha256-original-physical-line-including-LF-or-CRLF-v1','token_ascii':token.decode('ascii'),'token_base64':base64.b64encode(token).decode(),'token_hex':token.hex(),'token_bytes':9,'token_hash_domain':'sha256-original-token-bytes-at-absolute-interval-v1','token_sha256':digest(token)}
        expected_rows.append(row)
    scriptpath=ROOT/t['outputs']['producer'];script=scriptpath.read_bytes();scriptref=dict(path=str(scriptpath),bytes=len(script),sha256=digest(script))
    assert P['producer_script']==production['script']==scriptref
    assert re.fullmatch(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d{6}\+08:00',P['created_at']) and datetime.fromisoformat(P['created_at'])>=datetime.fromisoformat(t['prepared_at'])
    expected={'domain':'think-manual-token-provenance-v1','version':1,'task':{'id':TID,'contract_sha256':TH},'created_at':P['created_at'],'producer_script':scriptref,'references':t['fixed_references'],'authority_basis':t['authority'],'original_review':{'report_sha256':digest(values['CP2-ASR-REAL-COMMENT-CAPABILITY-REVIEW-001.json']),'verification_report_sha256':r['verification_report_sha256'],'verification_script_sha256':r['verification_script_sha256'],'request_sha256':r['request_sha256'],'approval_sha256':r['authorization_record_sha256'],'historical_context_freeze_commit':r['freeze_commit'],'historical_context_freeze_sha256':digest(values['freeze.json']),'original_formal_decision_sha256':r['formal_decision_sha256'],'reviewer':r['reviewer'],'reviewed_at':r['reviewed_at']},'source_identity':{'commit':B['upstream_commit'],'tree':B['upstream_tree'],'path':B['source_path'],'body_sha256':B['body_sha256'],'body_bytes':B['body_bytes'],'git_blob':B['git_blob_sha1'],'role':'cpp_source_header'},'envelope_identity':{'path':B['private_envelope'],'sha256':B['envelope_sha256'],'bytes':B['envelope_bytes'],'file_type':'regular','nlink':1,'permissions':'0600','private_parent_permissions':'0700','nofollow':True},'read_receipt':{'private_files_read':1,'envelope_bytes_read':8579,'directory_chain':chain,'stable_descriptor_identity':True,'context_use':'hash and interval verification only; no semantic inspection','source_bytes_exported':18,'exported_intervals':[[1893,1902],[1972,1981]],'actual_network_events':[]},'occurrences':expected_rows,'operational_authority':False,'effect':{'original_R_modified':False,'new_review_decision':False,'pending_cleared':False,'acquisition_authorized':False,'K_created':False},'scope':'Exact token byte provenance only. Original review time/decision unchanged; no field/API/source/runtime/license/CP2 approval.'}
    assert enc(expected)==pb and not CAPABILITIES
    for item in t['fixed_references']:assert digest(Path(item['path']).read_bytes())==item['sha256']
    verification={'RESULT':'PASS','P_sha256':digest(pb),'P_bytes':len(pb),'task_sha256':TH,'independent_verifier':{'path':str(Path(__file__).absolute()),'bytes':Path(__file__).stat().st_size,'sha256':digest(Path(__file__).read_bytes())},'producer_script':scriptref,'independent_private_files_read':1,'exact_slice_count':2,'unique_token_source_bytes':18,'whole_P_reconstructed_equal':True,'source_output_minimization':'Expected strict full P object reconstructed; no line/header/adjacent contents permitted; only18 token sourcebytes encoded','all_original_references_unchanged':True,'network_events':CAPABILITIES,'scope':'Separate acceptance stage only, no producer/candidate/oldscript execution; no K or new decision/acquisition.'}
    path=ROOT/t['outputs']['verification']
    with path.open('xb') as out:out.write(enc(verification));out.flush();os.fsync(out.fileno())
    print(json.dumps({'RESULT':'PASS','P_sha256':digest(pb),'tokens_independently_verified':2}))
if __name__=='__main__':main()
