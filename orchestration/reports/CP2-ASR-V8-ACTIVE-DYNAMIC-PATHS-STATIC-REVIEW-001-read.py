"""Bounded read of the sole authorized envelope. Never executes its contents."""
import os, stat, json, hashlib, pathlib, datetime, sys
ROOT=pathlib.Path('/Users/orderly_ray/Leader/orchestration')
ID='CP2-ASR-V8-ACTIVE-DYNAMIC-PATHS-STATIC-REVIEW-001'
def sha(b):return hashlib.sha256(b).hexdigest()
def can(x):return (json.dumps(x,sort_keys=True,ensure_ascii=True,separators=(',',':'))+'\n').encode()
def identity(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def load():
    t=json.loads((ROOT/'tasks'/(ID+'.json')).read_bytes());spec=t['retained_object']
    for key in ('formal_decision','user_approval','approved_request','predecessor_acceptance','derived_input'):
        d=t[key];b=pathlib.Path(d['path']).read_bytes();assert len(b)==d['bytes'] and sha(b)==d['sha256']
    p=pathlib.Path(spec['unique_retained_path']);fd=os.open('/',os.O_RDONLY|os.O_DIRECTORY);directories=[]
    try:
        walked=''
        for part in p.parts[1:-1]:
            child=os.open(part,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=fd);os.close(fd);fd=child
            walked+='/'+part;s=os.fstat(fd)
            if walked.startswith('/private/tmp/think-acquisition-v8-quarantine-3_hb53be'):
                assert stat.S_IMODE(s.st_mode)==0o700
                directories.append({'path':walked,'mode':'0700','nofollow':True})
        bodyfd=os.open(p.name,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK,dir_fd=fd)
        try:
            s=os.fstat(bodyfd);assert stat.S_ISREG(s.st_mode) and s.st_nlink==1 and stat.S_IMODE(s.st_mode)==0o600 and s.st_size==spec['envelope_bytes']
            chunks=[];remaining=s.st_size+1
            while remaining:
                b=os.read(bodyfd,min(65536,remaining))
                if not b:break
                chunks.append(b);remaining-=len(b)
            raw=b''.join(chunks);assert identity(s)==identity(os.fstat(bodyfd))
        finally:os.close(bodyfd)
    finally:os.close(fd)
    assert len(raw)==spec['envelope_bytes'] and sha(raw)==spec['envelope_sha256']
    envelope=json.loads(raw);assert can(envelope)==raw
    body=envelope['text'].encode('utf-8');assert len(body)==spec['body_bytes'] and sha(body)==spec['body_sha256']
    assert hashlib.sha1(b'blob '+str(len(body)).encode()+b'\0'+body).hexdigest()==spec['git_blob']==envelope['blob_sha']
    assert envelope['path']=='sherpa-onnx/csrc/online-recognizer.h' and envelope['role']=='cpp_source_header'
    assert envelope['sha256']==sha(body) and envelope['bytes']==len(body)
    # Small independent lexical walk, used only to verify the seven frozen carriers.
    channel={};i=0;n=len(body)
    while i<n:
        start=i
        if body[i:i+2]==b'//':
            j=body.find(b'\n',i);i=n if j<0 else j;kind='line_comment'
        elif body[i:i+2]==b'/*':
            j=body.find(b'*/',i+2);assert j>=0;i=j+2;kind='block_comment'
        elif body[i] in (34,39):
            quote=body[i];i+=1
            while i<n:
                if body[i]==92:i+=2
                elif body[i]==quote:i+=1;break
                else:i+=1
            kind='string_literal' if quote==34 else 'char_literal'
        else:i+=1;kind='code'
        for pos in range(start,i):channel[pos]=kind
    lines=body.splitlines(keepends=True);starts=[];offset=0
    for line in lines:starts.append(offset);offset+=len(line)
    tuples=[]
    for x in spec['targets']:
        a,b=x['start'],x['end'];line=x['line'];start=starts[line-1];physical=lines[line-1]
        assert start<=a<b<=start+len(physical) and body[:a].count(b'\n')+1==line
        carrier=channel[a];assert all(channel[pos]==carrier for pos in range(a,b))
        expected='line_comment' if x['kind']=='new_comment' else 'string_literal' if line==15 else 'code';assert carrier==expected
        historical=physical[:-2] if physical.endswith(b'\r\n') else physical[:-1] if physical.endswith(b'\n') else physical
        token=body[a:b].decode('ascii');assert token in ('decoder','hotwords_file','hotwords')
        tuples.append(dict(x,raw_token=token,token_sha256=sha(body[a:b]),carrier=carrier,line_start=start,line_end=start+len(physical),physical_line_sha256=sha(physical),historical_line_sha256=sha(historical),rule='dynamic_paths',detector='path_pattern'))
    return t,body,lines,starts,tuples,dict(path=str(p),bytes=len(raw),sha256=sha(raw),identity=identity(s),regular_singlelink=True,mode='0600',stable_fd=True,nofollow=True,directories=directories)
if __name__=='__main__':
    t,body,lines,starts,tuples,checked=load()
    selected=[int(x) for x in sys.argv[1].split(',')]
    assert selected==sorted(set(selected)) and all(1<=x<=len(lines) for x in selected)
    ranges=[dict(line=k,start=starts[k-1],end=starts[k-1]+len(lines[k-1]),sha256=sha(lines[k-1])) for k in selected]
    receipt=dict(task_id=ID,read_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),script_sha256=sha(pathlib.Path(__file__).read_bytes()),checked=checked,occurrences=tuples,human_visible=ranges,other_body_reads=0,network_calls=0,thirdparty_executed=False,candidate_scanner_controller_executed=False)
    out=pathlib.Path(sys.argv[2]);assert out.parent==ROOT/'reports'
    with out.open('x') as f:json.dump(receipt,f,indent=2);f.write('\n')
    for k in selected:print(str(k)+': '+lines[k-1].decode().rstrip('\r\n'))
