import json,hashlib,ast,subprocess,re
from pathlib import Path
repo=Path('/Users/orderly_ray/Projects/think');p=repo/'tools/asr_review_acquisition_v8';old=repo/'tools/asr_review_acquisition_v7';out=Path('/Users/orderly_ray/Leader/orchestration/reports');pre='CP2-ASR-REVIEW-TIMESTAMP-REPRESENTATION-OFFLINE-001'
def sha(b):return hashlib.sha256(b).hexdigest()
d=json.loads((p/'provenance.json').read_bytes());assert len(d['source_files'])==26
for row in d['source_files']:
 b=subprocess.check_output(['git','show',d['source_commit']+':tools/asr_review_acquisition_v7/'+row['path']],cwd=repo);new=(p/row['path']).read_bytes()
 assert sha(b)==row['sha256'] and len(b)==row['bytes'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==row['git_blob']
 assert new!=b if row['changed'] else new==b
 assert sha(new)==row['candidate_sha256'] and len(new)==row['candidate_bytes']
def methods(root):
 result={}
 for f in (root/'tests').glob('test_*.py'):
  src=f.read_text()
  for c in ast.parse(src).body:
   if isinstance(c,ast.ClassDef):
    for m in c.body:
     if isinstance(m,ast.FunctionDef) and m.name.startswith('test_'):result[f.stem+'.'+c.name+'.'+m.name]=ast.get_source_segment(src,m)
 return result
om=methods(old);nm=methods(p);assert len(om)==167 and len(nm)==174 and all(om[k]==nm[k] for k in om)
assert len(d['old_methods'])==167
for r in d['old_methods']:assert r['unchanged'] and sha(om[r['test']].encode())==r['sha256']
delivery=json.loads((p/'evidence/delivery.json').read_bytes())
for name,h in delivery['formal_pins'].items():assert sha((repo/name).read_bytes())==h
raw=json.loads((p/'evidence/static-raw.json').read_bytes());ctx=json.loads((p/'evidence/static-context.json').read_bytes());count=0;files={};ports=0
for r in raw['findings']:
 if r['rule_id'].startswith('IOC-DAAM-PORT-'):
  ports+=1
  name=r['path']
  if name not in files:files[name]=(p/name).read_text().splitlines()
  line=files[name][r['line']-1]
  matches=list(re.finditer(r['rule_id'].rsplit('-',1)[1],line))
  for m in matches:
   a,b=m.span()
   while a>0 and line[a-1] in '0123456789abcdefABCDEF':a-=1
   while b<len(line) and line[b] in '0123456789abcdefABCDEF':b+=1
   assert b-a in (40,64),(name,line[a:b]);count+=1
assert ports==2535 and count==3739,(ports,count)
diff=json.loads((p/'evidence/static-diff-raw.json').read_bytes());assert diff['verdict']=='low_indicators' and not diff['findings']
r={'RESULT':'PASS','source_files_git_verified':26,'old_method_sources_exact':167,'new_methods':7,'formal_pins_verified':delivery['formal_pins'],'port_findings':ports,'port_matches_independently_context_checked':count,'original_scan_verdict':raw['verdict'],'diff_scan_verdict':diff['verdict'],'scope':'first-party source and new scan evidence only'}
(out/(pre+'-baseline.json')).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
