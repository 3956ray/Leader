"""Complete only the target comment, constructor and enclosing type anchors."""
import pathlib,runpy,re,json,datetime,hashlib
root=pathlib.Path('/Users/orderly_ray/Leader/orchestration/reports')
prefix='CP2-ASR-V8-ACTIVE-DYNAMIC-PATHS-STATIC-REVIEW-001'
reader=root/(prefix+'-read.py');raw=reader.read_bytes()
api=runpy.run_path(str(reader));t,body,lines,starts,tuples,checked=api['load']()
selected=set([66,67,68,69,146,147,148,149,150,151,152,161,162,163,164,165,166])
anchors=[]
for target in (64,110,143):
    for kind in (b'namespace',b'(?:struct|class)'):
        matches=[k for k,line in enumerate(lines[:target],1) if re.match(rb'\s*'+kind+rb'\s+[A-Za-z_]\w*\s*\{',line)]
        assert matches
        selected.add(matches[-1]);anchors.append({'target_line':target,'anchor_line':matches[-1]})
selected=sorted(selected);sha=api['sha']
receipt=dict(task_id=prefix,read_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),script_sha256=sha(pathlib.Path(__file__).read_bytes()),reader_sha256=sha(raw),checked=checked,occurrences=tuples,human_visible=[dict(line=k,start=starts[k-1],end=starts[k-1]+len(lines[k-1]),sha256=sha(lines[k-1])) for k in selected],anchors=anchors,other_body_reads=0,network_calls=0,thirdparty_executed=False,candidate_scanner_controller_executed=False)
with (root/(prefix+'-read-3.json')).open('x') as f:json.dump(receipt,f,indent=2);f.write('\n')
for k in selected:print(str(k)+': '+lines[k-1].decode().rstrip('\r\n'))
