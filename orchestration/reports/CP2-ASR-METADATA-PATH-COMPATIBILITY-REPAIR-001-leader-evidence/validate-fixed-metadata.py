from pathlib import Path
import os, stat, json, hashlib, tempfile, sys, re
REPORT=Path('/Users/orderly_ray/Leader/orchestration/reports/CP2-ASR-METADATA-PATH-COMPATIBILITY-REPAIR-001')
COPY=Path('/var/folders/lg/xdzs0w2s2zz_rf8frygyzbl00000gn/T/think-leader-v4-8gm0ym1x')
BUNDLE='642d29885efb5df375564d0ebeec0875d4701e5dfc816934de329d3c2dda42d0'
PINS=[('commit.json',2336,'e020549c1a78964acc8e400091ee54ba29f29ffd08e5b919a1bf06801dd68089'),('tree.json',2742250,'7643e529ba6588e5dbe425acb624569218596a6316a1be9bc7d55bacd105ccd2')]
sha=lambda b:hashlib.sha256(b).hexdigest()
canon=lambda o:(json.dumps(o,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False)+'\n').encode('ascii')
def safe_read(path,size,pin):
    parts=Path(path).parts;fd=os.open('/',os.O_RDONLY|os.O_DIRECTORY)
    try:
        for part in parts[1:-1]:
            nxt=os.open(part,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=fd);os.close(fd);fd=nxt
        f=os.open(parts[-1],os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK,dir_fd=fd)
        try:
            s=os.fstat(f);assert stat.S_ISREG(s.st_mode) and s.st_nlink==1 and s.st_size==size and size<=8388608
            chunks=[];total=0
            while True:
                data=os.read(f,min(65536,size+1-total))
                if not data:break
                chunks.append(data);total+=len(data);assert total<=size
            raw=b''.join(chunks);assert len(raw)==size and sha(raw)==pin
            a=os.fstat(f);assert (s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns)==(a.st_dev,a.st_ino,a.st_size,a.st_mtime_ns)
            return raw
        finally:os.close(f)
    finally:os.close(fd)
if sys.argv[1]=='copy':
    # This phase runs only after successful independent synthetic verification.
    loc=Path(tempfile.mkdtemp(prefix='think-v4-fixed-metadata-',dir='/private/tmp'));out=[]
    for name,size,pin in PINS:
        raw=safe_read('/private/tmp/think-frozen-metadata-preflight-_6wsajyf/'+name,size,pin)
        dst=loc/name;fd=os.open(dst,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
        try:
            with os.fdopen(fd,'wb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
        except:raise
        out.append({'name':name,'bytes':size,'sha256':pin})
    REPORT.with_name(REPORT.name+'-metadata-location.json').write_text(json.dumps({'directory':str(loc),'records':out},indent=2)+'\n');print(loc)
else:
    loc=Path(json.loads(REPORT.with_name(REPORT.name+'-metadata-location.json').read_text())['directory'])
    raw=[safe_read(loc/name,size,pin) for name,size,pin in PINS]
    files=sorted(list((COPY/'offline_review').glob('*.py'))+list((COPY/'tests').glob('*.py'))+[COPY/x for x in ['audit.py','verify.py','network_guard.py','recalculate.py','SCHEMA.md']])
    actual=sha(canon([{'path':p.relative_to(COPY).as_posix(),'sha256':sha(p.read_bytes())} for p in files]));assert actual==BUNDLE
    sys.path.insert(0,str(COPY))
    from network_guard import NetworkGuard
    guard=NetworkGuard();guard.__enter__()
    from offline_review.protocol import Trust,input_document,parse_input,parse_commit,parse_tree
    original=json.loads(raw[1]);trust=Trust(BUNDLE,PINS[0][2],PINS[1][2])
    inp=canon(input_document(trust,len(raw[0]),len(raw[1])));parsed_input=parse_input(inp,trust);commit=parse_commit(raw[0]);index=parse_tree(raw[1])
    assert index.raw_bytes==raw[1] and index.raw_sha256==sha(raw[1]);assert index.document==original and list(index.records)==original['tree'] and list(index.values())==original['tree']
    paths=[x['path'] for x in original['tree']];assert list(index)==paths and index.original_indices=={p:i for i,p in enumerate(paths)}
    assert index.collection_sha256==sha(canon(original['tree']))
    strict=lambda p:bool(re.fullmatch(r'[A-Za-z0-9_./-]+',p)) and all(s not in ('','.','..') for s in p.split('/'))
    unsupported=[p for p in paths if not strict(p)]
    scope=lambda p:p=='LICENSE' or (p.startswith('sherpa-onnx/csrc/') and p.endswith(('.h','.cc')))
    assert len(paths)==8585 and len(set(paths))==8585 and len(unsupported)==171 and not any(scope(p) for p in unsupported)
    zero=guard.evidence();assert not zero['actual_network_events'] and not zero['trapped_workload_calls'];guard.__exit__()
    result={'RESULT':'PASS','candidate_bundle_sha256':BUNDLE,'input_sha256':sha(inp),'input_bytes':len(inp),'raw_inputs':[{'name':n,'bytes':s,'sha256':h} for n,s,h in PINS],'canonical_input':'PASS','commit':'PASS','tree':'PASS','entry_count':8585,'duplicate_paths':0,'old_rule_unsupported_names':171,'unsupported_names_in_acquisition_scope':0,'raw_bytes_document_records_attributes_order_indices_preserved':True,'collection_sha256':index.collection_sha256,'zero_network':zero,'real_body_requests':0,'calls':'Only input_document/parse_input/parse_commit/parse_tree and metadata representation. No controller, run_input, transport or blob decode.','scope':'Identity parser compatibility only; no allowlist, authorization or source verdict.'}
    REPORT.with_name(REPORT.name+'-real-metadata.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
