"""Independent offline checks of this attempt only; no product imports or writes."""
import base64, hashlib, json, pathlib, re, stat

LEADER = pathlib.Path('/Users/orderly_ray/Leader')
DOC = pathlib.Path('/Users/orderly_ray/Projects/think/doc/security-reviews/sherpa-onnx-narrow-source-acquisition-v8/2026-09-06')
DRIVER = pathlib.Path('/private/tmp/think-acquisition-v8-driver-w125vAFT')
RUN = pathlib.Path('/private/tmp/think-acquisition-v8-quarantine-3_hb53be/source_v8_once')
PREFIX = 'CP2-ASR-NARROW-SOURCE-ACQUISITION-V8-001'
def sha(b): return hashlib.sha256(b).hexdigest()
def can(x): return (json.dumps(x, sort_keys=True, ensure_ascii=True, separators=(',', ':'), allow_nan=False)+'\n').encode()
def dig(x): return sha(can(x))
def read(p):
    s=p.lstat(); assert stat.S_ISREG(s.st_mode) and s.st_nlink==1
    b=p.read_bytes(); z=p.lstat()
    fields=('st_dev','st_ino','st_mode','st_nlink','st_size','st_mtime_ns','st_ctime_ns')
    assert len(b)==s.st_size and all(getattr(s,k)==getattr(z,k) for k in fields)
    return b
def obj(p): return json.loads(read(p))
task=obj(LEADER/'orchestration/tasks'/ (PREFIX+'.json'))
assert sha(read(LEADER/'orchestration/tasks'/(PREFIX+'.json')))=='91692cef13c28e15672b62726e008923ecfacbb8ab317b521966dda301e83ac3'
for key in ('user_approval','approved_request','predecessor_acceptance'):
    x=task[key]; b=read(pathlib.Path(x['path'])); assert len(b)==x['bytes'] and sha(b)==x['sha256']
for x in task['mapping_files']:
    b=read(pathlib.Path(x['path'])); assert b==read(DRIVER/pathlib.Path(x['path']).name)
    assert len(b)==x['bytes'] and sha(b)==x['sha256']
driver=read(DRIVER/'driver.py'); assert sha(driver)=='8af745d6a0a30ac10d91c5a6cdc4bea6824c62be55a3eaebb9589a2092d6cd11'
marker=obj(DRIVER/'consumed.json'); execution=obj(DRIVER/'execution.json')
assert execution['run_input_calls']==1 and execution['marker_sha256']==sha(read(DRIVER/'consumed.json'))
assert marker['attempt_limit']==1 and marker['driver_sha256']==sha(driver)
assert marker['identities']==task['identities'] and marker['approval']==task['user_approval'] and marker['request']==task['approved_request']
assert marker['plan']['run_path']==str(RUN) and marker['created_at']<=execution['started_at']<=execution['stopped_at']
assert all(marker[k] is None for k in ('connection_factory','review','fault'))
rerun=obj(LEADER/'orchestration/reports'/(PREFIX+'-leader-rerun.json'))
assert rerun==obj(DRIVER/'verified-evidence.json') and rerun['file_count']==93
manifest=obj(DOC/'evidence-manifest.json')
assert manifest['run_inventory']==rerun['inventory'] and manifest['run_collection_sha256']==rerun['inventory_collection_sha256']
for key in ('quarantine','trusted_driver_snapshot'):
    inv=manifest[key]; root=pathlib.Path(inv['root'])
    assert inv['file_count']==len(inv['files']) and dig(inv['files'])==inv['collection_sha256']
    assert inv['total_bytes']==sum(x['bytes'] for x in inv['files'])
    for x in inv['files']:
        p=root/x['path'];b=read(p)
        assert len(b)==x['bytes'] and sha(b)==x['sha256'] and stat.S_IMODE(p.lstat().st_mode)==0o600
    if key=='quarantine': assert sorted(p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file())==sorted(x['path'] for x in inv['files'])
bundle=DRIVER/'candidate'
records=[{'path':p.relative_to(bundle).as_posix(),'sha256':sha(read(p))} for p in sorted(p for p in bundle.rglob('*') if p.is_file())]
assert len(records)==28 and dig(records)==task['identities']['C']
assert stat.S_IMODE(RUN.lstat().st_mode)==0o700
assert sorted(p.name for p in RUN.iterdir())==sorted(x['path'] for x in rerun['inventory'])
for x in rerun['inventory']:
    p=RUN/x['path'];b=read(p)
    assert len(b)==x['bytes'] and sha(b)==x['sha256'] and stat.S_IMODE(p.lstat().st_mode)==0o600
t=obj(RUN/'terminal.json')
assert t['stop_reason']=='denylist_capability' and t['source_verdict']=='insufficient_evidence' and t['fixed_point'] is False
assert t['body_files']==2 and t['body_bytes']==19297 and len(t['calls'])==2 and t['ledger_count']==25
assert t['pending_seeds']==task['scope_contract']['frozen_policy']['seeds'][2:] and t['pending_internal']==[]
assert t['persistence_errors']==[] and t['license_review_status']=='manual_review' and t['scanner_status']=='pending'
assert t['effective_comment_review_status']==t['capability_review_status']=='pending'
assert t['release_hash']==task['identities']['C'] and t['input_hash']==task['identities']['input'] and t['policy_hash']==task['identities']['policy']
assert t['manual_authority']['T']==obj(DRIVER/'T.json')
for k in ('F','M','A'): assert t['manual_authority'][k]==task['identities'][k]
for k,v in execution.items():
    if k in t: assert v==t[k]
def archive(a):
    out=[]
    for item in a['parts']:
        b=read(RUN/item['file']); assert sha(b)==item['sha256']
        o=json.loads(b); raw=base64.b64decode(o['content'],validate=True)
        assert sha(raw)==o['sha256'] and len(raw)==o['bytes']==item['bytes'];out.append(raw)
    raw=b''.join(out); assert sha(raw)==a['sha256'] and len(raw)==a['bytes'];return raw
rawmeta={x['kind']:archive(x['archive']) for x in t['metadata_imports']}
assert sorted(rawmeta)==['commit','tree']
for k,x in zip(('commit','tree'),task['metadata']): assert len(rawmeta[k])==x['bytes'] and sha(rawmeta[k])==x['sha256']
assert len(json.loads(rawmeta['tree'])['tree'])==8585
assert t['raw_bytes']==sum(map(len,rawmeta.values()))+t['blob_raw_bytes']==2771747
assert t['blob_raw_bytes']==27161 and t['raw_bytes']<16777216
package=json.loads(archive(t['manual_package_archive'])); assert can(package)==read(DRIVER/'manual-package.json')
report=json.loads(archive(t['source_analyses'][0]['archive']))
body=obj(RUN/'body-0002.json')['text'].encode()
assert sha(body)=='382e6bcc6e26079419c0a0f972d89b6c48de5d9ecda49ceca592bd0786482836'
assert report['guard']['classification']=='canonical_header_guard'
assert report['lexical_issues']==report['directive_issues']==report['file_safety_issues']==[]
policy=task['scope_contract']['frozen_policy']['source_semantics']['detectors']
diagnostics=[]
for e in report['capabilities']:
    token=body[e['start']:e['end']].decode();line=report['lines'][e['line']-1]
    assert e['line']==body[:e['start']].count(b'\n')+1
    assert line['start']<=e['start']<e['end']<=line['end']
    carrier=[s for s in report['channels'] if s['start']<=e['start'] and e['end']<=s['end']]
    assert len(carrier)==1 and carrier[0]['definite']
    c=carrier[0]['channel']; assert (e['classification']=='comment_capability_mention')==(c in ('line_comment','block_comment'))
    if e['rule']=='dynamic_paths': assert re.fullmatch(policy['dynamic_paths'],token)
    else: assert e['rule']=='websocket' and token=='websocket'
    diagnostics.append({'line':e['line'],'start':e['start'],'end':e['end'],'rule':e['rule'],'classification':e['classification'],'carrier':c,'token_sha256':sha(token.encode())})
assert [x['line'] for x in diagnostics if x['classification']=='denylist_capability']==[15,110,143,156,156]
assert [x['line'] for x in diagnostics if x['classification']=='comment_capability_mention']==[57,60,64,132]
matches=[]
for x in package['representation']['occurrences']:
    i=x['identity'];start,end=i['token_start'],i['token_end']
    assert body[start:end].decode()==i['raw_token'] and dig(i)==x['occurrence_id']
    physical=body[i['line_start']:i['line_end']]; historical=physical[:-2] if physical.endswith(b'\r\n') else physical[:-1] if physical.endswith(b'\n') else physical
    assert sha(physical)==i['physical_line_sha256'] and sha(historical)==i['historical_line_sha256']
    assert any(e['start']==start and e['end']==end and e['line']==i['line'] and e['rule']==i['rule'] and e['detector']==i['detector'] for e in report['capabilities'])
    matches.append(x['occurrence_id'])
assert len(matches)==2
reject=obj(RUN/'manual-adjudication-0002.json')
assert reject['domain']=='think-manual-rejection-v8' and reject['reason']=='manual_complete_matching' and reject['hard_stop']=='denylist_capability'
assert reject['original_report_sha256']==dig(report) and reject['effective_comment_review_status']=='pending'
events=[obj(RUN/('event-%04d.json'%i)) for i in range(1,26)]
assert [e['sequence'] for e in events if e['event']=='authorize']==[13,19]
assert [e['sequence'] for e in events if e['event']=='before_request']==[14,20]
assert [e['event'] for e in events[22:]]==['parsed','manual_capability_adjudication','terminal_checkpoint']
scanroot=RUN.parent/'scanner-reports';scan=obj(scanroot/'scan-report.json')
assert scan['verdict']=='manual_review' and scan['risk_score']==32 and scan['summary']=={'medium':4} and scan['block_signals']==[]
assert scan['stats']['candidates']==scan['stats']['text_files']==93
assert all(scan['stats'][k]==0 for k in ('archives','binary_files','skipped_large','skipped_limit','unreadable'))
scancontexts=[]
for f in scan['findings']:
    assert f['rule_id']=='IOC-DAAM-PORT-8086' and f['line']==1 and not f['reachable']
    o=obj(RUN/f['path']);a=o['state']['source_analyses'] if 'state' in o else o['source_analyses']
    h=a[0]['archive']['parts'][1]['sha256'];assert h==sha(read(RUN/'source-analysis-0002-0002.json')) and '8086' in h
    assert read(RUN/f['path']).count(b'8086')==1
    scancontexts.append({'path':f['path'],'matches':1,'entire_match_is_stored_part_sha256':True})
print(json.dumps({'RESULT':'PASS','run_files':93,'private_collection':rerun['inventory_collection_sha256'],'marker_sha256':execution['marker_sha256'],'terminal_sha256':sha(read(RUN/'terminal.json')),'ledger_hash':t['ledger_hash'],'requests':2,'decoded_bytes':19297,'raw_bytes':2771747,'source_stop':t['stop_reason'],'comment_set':{'expected':2,'actual':4,'matching_original_ids':matches,'clearance':False},'active_capabilities':5,'capability_diagnostics':diagnostics,'scanner_context':scancontexts,'scanner_raw_verdict':'manual_review','scope':'Read-only current attempt; no old private source, no network, no scanner or candidate execution. Source/runtime/license approval not established.','limitations':['Raw HTTP response bodies/headers are not retained; blob_raw count cannot be reconstructed from wire bytes.','Persisted chain plus reviewed driver/transport supports single-run/no-successor conclusion; no independent packet capture.','Base64 archive contents are not recursively scanned by scanner; source/body semantics separately checked above.']},sort_keys=True,indent=2))
