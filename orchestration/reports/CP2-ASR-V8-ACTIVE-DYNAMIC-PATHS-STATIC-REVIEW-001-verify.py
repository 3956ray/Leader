"""Independent standard-library verification; does not import the review reader."""
import os,sys,stat,pathlib,json,hashlib,re,datetime
events=[]
def guard(event,args):
    if event.startswith(('socket.','urllib.','http.client.')) or event in ('subprocess.Popen','os.system','os.exec','os.posix_spawn'):
        events.append(event);raise RuntimeError('network/process execution forbidden')
sys.addaudithook(guard)
root=pathlib.Path('/Users/orderly_ray/Leader/orchestration/reports')
prefix='CP2-ASR-V8-ACTIVE-DYNAMIC-PATHS-STATIC-REVIEW-001'
def sha(b):return hashlib.sha256(b).hexdigest()
def can(x):return (json.dumps(x,sort_keys=True,ensure_ascii=True,separators=(',',':'))+'\n').encode()
raw_report=(root/(prefix+'.json')).read_bytes();report=json.loads(raw_report)
assert sha(raw_report)=='f5d1f99d54084aec6757038f726ae455395e334ac0b120c5f254791c1bcbda8b'
assert sha((root/(prefix+'.md')).read_bytes())=='a6ec5534ed6b2bcd7b6ae41dd34576f3465ef7df2494c614755a00e809acd39b'
for d in [report[k] for k in ('task','formal_decision','user_approval','approved_request')]+report['read_receipts']+report['trusted_scripts']:
    raw=pathlib.Path(d['path']).read_bytes();assert len(raw)==d['bytes'] and sha(raw)==d['sha256']
p=pathlib.Path('/private/tmp/think-acquisition-v8-quarantine-3_hb53be/source_v8_once/body-0002.json')
fd=os.open('/',os.O_RDONLY|os.O_DIRECTORY)
try:
    for i,part in enumerate(p.parts[1:-1],1):
        new=os.open(part,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=fd);os.close(fd);fd=new
        if i>=3:assert stat.S_IMODE(os.fstat(fd).st_mode)==0o700
    f=os.open(p.name,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK,dir_fd=fd)
    try:
        a=os.fstat(f);assert stat.S_ISREG(a.st_mode) and a.st_nlink==1 and a.st_size==8579 and stat.S_IMODE(a.st_mode)==0o600
        raw=b''
        while len(raw)<=8579:
            piece=os.read(f,8580-len(raw))
            if not piece:break
            raw+=piece
        z=os.fstat(f)
        for k in ('st_dev','st_ino','st_mode','st_nlink','st_size','st_mtime_ns','st_ctime_ns'):assert getattr(a,k)==getattr(z,k)
    finally:os.close(f)
finally:os.close(fd)
assert len(raw)==8579 and sha(raw)==report['source']['current_envelope_sha256']
envelope=json.loads(raw);body=envelope['text'].encode();assert len(body)==7939 and sha(body)==report['source']['body_sha256']
assert hashlib.sha1(b'blob 7939\0'+body).hexdigest()==report['source']['blob']==envelope['blob_sha']
lines=body.splitlines(keepends=True);offsets=[0]
for line in lines:offsets.append(offsets[-1]+len(line))
expected=[(15,404,411),(110,3577,3590),(143,4756,4769),(156,5350,5363),(156,5364,5377),(64,2139,2146),(132,4297,4310)]
items=report['occurrences'];assert len(items)==7 and len({x['occurrence_id'] for x in items})==7
for entry,target in zip(items,expected):
    i=entry['identity'];line,start,end=target
    assert (i['line'],i['start'],i['end'])==target and i['source']==report['source']
    assert sha(can(i))==entry['occurrence_id'] and not entry['operational_authority'] and not entry['clearance']
    physical=lines[line-1];historical=physical.rstrip(b'\r\n')
    assert i['line_start']==offsets[line-1] and i['line_end']==offsets[line]
    assert i['physical_line_sha256']==sha(physical) and i['historical_line_sha256']==sha(historical)
    assert i['raw_token']==body[start:end].decode() and i['token_sha256']==sha(body[start:end])
    assert i['rule']=='dynamic_paths' and i['detector']=='path_pattern'
    if line in (64,132):
        assert physical.lstrip().startswith(b'///') and not historical.endswith(b'\\') and i['carrier']=='line_comment'
        assert entry['judgment']=='comment_only_nonoperative_for_this_body'
    elif line==15:
        match=re.fullmatch(rb'\s*#include\s+"([^"]+)"\s*',physical);assert match and i['carrier']=='string_literal'
        assert offsets[line-1]+match.start(1)<=start<end<=offsets[line-1]+match.end(1)
        assert entry['judgment']=='locally_nonoperative_but_reachability_unresolved'
    else:
        assert i['carrier']=='code' and not any(x in physical for x in (b'//',b'/*',b'"',b"'"))
        assert entry['judgment']=='operative_or_policy_relevant_in_this_body'
# Reconstruct the configuration syntax/data flow without relying on the first reader.
field=re.fullmatch(rb'\s*std::string\s+(\w+)\s*;\s*',lines[109]);assert field
name=field.group(1)
assert re.search(rb'const\s+std::string\s*&\s*'+name+rb'\s*,',lines[142])
init=re.fullmatch(rb'\s*(\w+)\((\w+)\),\s*',lines[155]);assert init and init.group(1)==init.group(2)==name
assert lines[136].strip()==b'OnlineRecognizerConfig(' and re.search(rb'hotwords_buf\(hotwords_buf\)\s*\{\}',lines[163])
assert b'from the' in lines[130] and name in lines[131] and b'hotwords_buf' in lines[129]
seen_lines=set();receipt_objects=[]
for d in report['read_receipts']:
    receipt=json.loads(pathlib.Path(d['path']).read_bytes());receipt_objects.append(receipt)
    assert receipt['checked']['path']==str(p) and receipt['checked']['sha256']==sha(raw)
    assert receipt['other_body_reads']==receipt['network_calls']==0 and not receipt['thirdparty_executed']
    for x in receipt['human_visible']:
        k=x['line'];assert (x['start'],x['end'])==(offsets[k-1],offsets[k]) and x['sha256']==sha(lines[k-1]);seen_lines.add(k)
assert sorted(seen_lines)==report['human_visible_lines'] and sum(len(lines[k-1]) for k in seen_lines)==report['human_visible_bytes_unique']
assert len(seen_lines)<len(lines) and report['unique_retained_files']==[str(p)]
for item in items:assert set(item['visible_evidence_lines'])<=seen_lines
for text in (raw_report,(root/(prefix+'.md')).read_bytes()):
    assert body not in text and b'"body_base64"' not in text and b'"text"' not in text
    assert all(line.strip() not in text for line in lines if len(line.strip())>=30)
assert report['stop']['pending_cleared'] is False and report['stop']['new_adjudications']==0
assert not report['controls']['new_acquisition_authorized'] and events==[]
result={'RESULT':'PASS','task_id':prefix,'verified_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'review_sha256':sha(raw_report),'markdown_sha256':sha((root/(prefix+'.md')).read_bytes()),'verifier_sha256':sha(pathlib.Path(__file__).read_bytes()),'unique_retained_path':str(p),'retained_reads_this_verification':1,'other_body_reads':0,'nofollow_regular_singlelink0600_private0700':True,'exact_envelope_body_gitblob':True,'occurrences':7,'unique_occurrence_ids':7,'active_policy_relevant':4,'active_literal_include_unresolved':1,'comments_local_nonoperative_without_clearance':2,'human_visible_lines':len(seen_lines),'human_visible_bytes':report['human_visible_bytes_unique'],'complete_header_displayed':False,'independent_config_data_flow':'field declaration, const-reference constructor argument, member-initializer target/source, empty constructor body confirmed','network_or_subprocess_guard_events':events,'source_execution':False,'product_or_old_evidence_changes':False,'limits':['Verifies local syntax/identity and narrow report; cannot establish downstream semantics, actual file access, business API exposure or runtime reachability.','Verification is a fourth read of the same authorized object, with no additional human source display; three prior review read receipts remain immutable.']}
print(json.dumps(result,indent=2))
