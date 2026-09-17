import json,hashlib,re,difflib,subprocess
from pathlib import Path
from datetime import datetime,timezone,timedelta
b=Path('/Users/orderly_ray/Leader');o=b/'orchestration';kb=Path('/Users/orderly_ray/Documents/Products Manager/product-knowledge-base');repo=Path('/Users/orderly_ray/Projects/think');tid='CP2-ASR-REVIEW-TOKEN-PROVENANCE-DECISION-001'
def sha(x):return hashlib.sha256(x).hexdigest()
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
items=[('raw/SRC-20260906-think-cp2-token-provenance-01.md',3519,'e2a57b91319fc930d922c5ae3eb0a684892d669e4a548333296e1c71b17f007d'),('ideas/personal-thought-archive/cp2-review-token-provenance-decision-2026-09-06.md',9458,'20da8a661354e4d87d57effb2f70997bbe38aab700fad43304271bccba1ab153'),('ideas/personal-thought-archive/prd-v0.1-2026-09-04.md',63461,'3cce758ccff443bdb7ea9368f3c585e4179653228c5071b0353b3991ce99ded7'),('INDEX.md',9746,'4a3b35a625316773a8460ea1da778de316487fe3f13ce6328430358ab084175a'),('LOG.md',37018,'fbbfc70809361672242e47414e7c7fae8f90f6a255ff0de9831a633b')]
# LOG hash copied exactly from PM delivery.
items[-1]=('LOG.md',37018,'fbbfc7080936162bf5e61372242e47414e7c7fae8f90f6a255ff0de9831a633b')
refs=[];links=[]
for name,size,h in items:
 p=kb/name;raw=p.read_bytes();assert len(raw)==size and sha(raw)==h,name;refs.append(dict(path=str(p),bytes=size,sha256=h))
 for link in re.findall(r'\]\(([^)]+)\)',raw.decode()):
  if '://' in link or link.startswith('#'):continue
  target=(p.parent/link.split('#')[0]).resolve();assert target.exists(),(name,link);links.append(dict(source=name,target=str(target)))
old=(repo/'doc/prd-v0.1-2026-09-04.md').read_bytes();new=(kb/items[2][0]).read_bytes();assert sha(old)=='ca6477c0bb4e40913be6861b5299ae4b0121650552da3aa1cd4acbd46c91528f'
a=old.decode().splitlines();c=new.decode().splitlines();ops=[]
for tag,i,j,k,l in difflib.SequenceMatcher(a=a,b=c).get_opcodes():
 if tag!='equal':
  assert (i<49 or a[i].startswith('状态：`v7 R1 C accepted;')),(i,a[i]);ops.append(dict(operation=tag,old_start=i+1,old_end=j,new_start=k+1,new_end=l))
source=(kb/items[0][0]).read_text();localpins=[o/'tasks'/ (tid+'.json'),o/'reports/CP2-ASR-REVIEW-TOKEN-PROVENANCE-AUDIT-001-report.json',o/'reports/CP2-ASR-REVIEW-TIMESTAMP-REPRESENTATION-OFFLINE-001-acceptance.json']
localpins += [o/'reports'/n for n in ['CP2-ASR-REAL-COMMENT-REVIEW-AUTHORIZATION-001.json','CP2-ASR-REAL-COMMENT-REVIEW-AUTHORIZATION-001-approved.json','CP2-ASR-REAL-COMMENT-CAPABILITY-REVIEW-001.json','CP2-ASR-REAL-COMMENT-CAPABILITY-REVIEW-001-verification.json','CP2-ASR-REAL-COMMENT-CAPABILITY-REVIEW-001-verify.py']]
localpins += [repo/'tools/asr_review_acquisition_v8'/n for n in ['SCHEMA.md','offline_review/manual.py']]
for p in localpins:assert sha(p.read_bytes()) in source,p
assert len([p for p in (kb/'raw').glob('*.md') if re.search(r'^source_id: SRC-20260906-think-cp2-token-provenance-01$',p.read_text(),re.M)])==1
subprocess.run(['git','diff','--check','--',*[x[0] for x in items]],cwd=kb,check=True,capture_output=True)
assert not subprocess.check_output(['git','status','--porcelain'],cwd=repo);assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo).decode().strip()=='1fe85740a185a63ca4f35df2abd22ae410f82fbb'
report={'RESULT':'PASS','formal_files':refs,'local_links_verified':len(links),'source_pins_verified':len(localpins),'prd_change_hunks':ops,'source_id_unique':True,'knowledge_lint':'missing script previously established; PM LOG accurately records partial, manual checks performed','product_head':'1fe85740a185a63ca4f35df2abd22ae410f82fbb','product_worktree_clean':True,'KB_scope':'Five task files verified; unrelated pre-existing uncommitted/untracked KB state not attributed or changed','authority_review':'Original exact request/approval permit same retained object/two hits offline; no once-onlyread term. New product decision narrows to two existing slices and preserves all acquisition prohibitions; no new user permission needed within scope.','scope_review':'Only P evidencecompletion with separate acceptance; old R/time/decision/v8/schema unchanged; no K/F/M/A/T/N/newacquisition/CP2approval.'};write(o/'reports'/(tid+'-verification.json'),report);print(json.dumps(report,ensure_ascii=False))
now=datetime.now(timezone(timedelta(hours=8))).isoformat();t=json.loads((o/'current-task.json').read_bytes());assert t['task_id']==tid;t.update(status='completed',completed_at=now);write(o/'tasks'/(tid+'-completed.json'),t);s=json.loads((o/'state.json').read_bytes());s.update(state='AWAITING_REVIEW',updated_at=now);write(o/'current-task.json',t);write(o/'state.json',s)
accept={'task_id':tid,'RESULT':'ACCEPTED','accepted_at':now,'product_decision':'APPROVED','formal_files':refs,'verification_report':str(o/'reports'/(tid+'-verification.json')),'verification_sha256':sha((o/'reports'/(tid+'-verification.json')).read_bytes()),'authority_review':report['authority_review'],'scope_review':report['scope_review'],'limitations':['Real token bytes/P not yet inspected or generated; no source/closure/runtime/license/device or CP2 conclusion.'],'next':'Five-document sync only; after independent acceptance, separate Leader P task under existing exact offline review authorization.'};ap=o/'reports'/(tid+'-acceptance.json');write(ap,accept)
t.update(status='accepted',accepted_at=now,acceptance_report=str(ap.relative_to(b)),acceptance_sha256=sha(ap.read_bytes()));write(o/'tasks'/(tid+'-accepted.json'),t);write(o/'current-task.json',t);s.update(state='ACCEPTED',last_accepted_task_id=tid);s['observations'].append('Accepted PM token provenance decision20da8a:5formalhashes/sourcepins/links/PRDdelta verified. Same-object/two-slice append-onlyP covered by persistent originalreview authorization; no newuserquestion or acquisitionauthority. Five-docsync next, noP yet.');write(o/'state.json',s);print(json.dumps({'acceptance_sha256':sha(ap.read_bytes())}))
