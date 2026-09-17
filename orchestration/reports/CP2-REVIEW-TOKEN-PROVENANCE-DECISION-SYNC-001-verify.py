import json,hashlib,stat,subprocess,re
from pathlib import Path
from datetime import datetime,timezone,timedelta
b=Path('/Users/orderly_ray/Leader');o=b/'orchestration';repo=Path('/Users/orderly_ray/Projects/think');tid='CP2-REVIEW-TOKEN-PROVENANCE-DECISION-SYNC-001';head='8a2d85d824f12cdc186f84514037698c88237dcb';parent='1fe85740a185a63ca4f35df2abd22ae410f82fbb'
def git(*args):return subprocess.check_output(['git',*args],cwd=repo)
def sha(x):return hashlib.sha256(x).hexdigest()
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
assert git('rev-parse','HEAD').decode().strip()==head and git('rev-parse','HEAD^').decode().strip()==parent and not git('status','--porcelain')
items=[('AGENTS.md',15375,'1c90ce42692395e95b09b85a0d3b0211a4836e850c93117f7e0ec36150d5efa1'),('doc/README.md',15068,'c8bd5312384a26a3d6a77b6f846ff9f3be79d11995d5298a22c7ba38d979d83b'),('doc/cp2-review-token-provenance-decision-2026-09-06.md',9458,'20da8a661354e4d87d57effb2f70997bbe38aab700fad43304271bccba1ab153'),('doc/development-guide-v0.1-2026-09-04.md',40090,'1d8d3405fd6b66e0764d81d1b32dbb36c57544b5c8dcb284a7a91d5cb017f60f'),('doc/prd-v0.1-2026-09-04.md',63461,'3cce758ccff443bdb7ea9368f3c585e4179653228c5071b0353b3991ce99ded7')]
names={x[0] for x in items};assert set(git('diff','--name-only',parent,head).decode().splitlines())==names
assert not git('diff','--check',parent,head)
refs=[];links=0;external=0;historical=0
for name,size,h in items:
 p=repo/name;raw=p.read_bytes();s=p.lstat();assert stat.S_ISREG(s.st_mode) and s.st_nlink==1 and len(raw)==size and sha(raw)==h
 assert raw==git('show',head+':'+name);blob=git('rev-parse',head+':'+name).decode().strip();assert hashlib.sha1(b'blob '+str(size).encode()+b'\0'+raw).hexdigest()==blob;refs.append(dict(path=name,bytes=size,sha256=h,blob=blob))
 for link in re.findall(r'\]\(([^)]+)\)',raw.decode()):
  if '://' in link or link.startswith('#'):external+=1;continue
  if link.startswith('../../raw/'):historical+=1;continue
  assert (p.parent/link.split('#')[0]).resolve().exists(),(name,link);links+=1
for row in json.loads((o/'current-task.json').read_bytes())['formal_sources']:assert (repo/row['destination']).read_bytes()==Path(row['path']).read_bytes()
def oldtree(commit):
 rows=git('ls-tree','-r','-z',commit).split(b'\0');return [x for x in rows if x and x.split(b'\t',1)[1].decode() not in names]
a=oldtree(parent);assert a==oldtree(head) and len(a)==129510
# Explicit NUL-terminated original git record sequence.
collection=sha(b'\0'.join(a)+b'\0');assert collection=='93c485ea4a43f86348504e1cd309c2e645c596b4a016597f6a88986ba3c93681'
unchanged={n:git('rev-parse',head+':'+n).decode().strip() for n in ['tools','doc/security-reviews','app']}
for n,h in unchanged.items():assert git('rev-parse',parent+':'+n).decode().strip()==h
r={'RESULT':'PASS','commit':head,'parent':parent,'root_tree':git('rev-parse',head+'^{tree}').decode().strip(),'five_files':refs,'formal_copies_byte_equal':True,'local_markdown_links':links,'external_or_anchor_not_fetched':external,'historical_raw_links_not_followed':historical,'old_git_records_exact':len(a),'old_git_records_nul_sha256':collection,'unchanged_trees':unchanged,'worktree_clean':True,'scope':'five-document-only sync; no P/private/source/network/candidate workload; scope semantics separately reviewed against formal decision'};write(o/'reports'/(tid+'-verification.json'),r)
now=datetime.now(timezone(timedelta(hours=8))).isoformat();t=json.loads((o/'current-task.json').read_bytes());assert t['task_id']==tid;t.update(status='completed',completed_at=now,candidate_commit=head);write(o/'tasks'/(tid+'-completed.json'),t);s=json.loads((o/'state.json').read_bytes());s.update(state='AWAITING_REVIEW',updated_at=now);write(o/'current-task.json',t);write(o/'state.json',s)
ap=o/'reports'/(tid+'-acceptance.json');write(ap,dict(task_id=tid,RESULT='ACCEPTED',accepted_at=now,commit=head,parent=parent,verification_report=str(o/'reports'/(tid+'-verification.json')),verification_sha256=sha((o/'reports'/(tid+'-verification.json')).read_bytes()),formal_decision_sha256=items[2][2],formal_prd_sha256=items[4][2],criteria=['Exact five paths and two formal copies; three entrypoints align with acceptedv8/Kblocked/Pnotstarted and Leader-onlysame-objecttwo-slice supplement under existingreview authority.','129510oldGitrecords andtools/securityreviews/app trees unchanged,localnavigation valid,cleancommit; no source/P/K execution.'],limitations=['P and exact token bytes not yet verified; no runtime/closure/CP2 conclusion.'],next='Separate Leader-owned P completion and separate acceptance, then new K task.'))
t.update(status='accepted',accepted_at=now,acceptance_report=str(ap.relative_to(b)),acceptance_sha256=sha(ap.read_bytes()));write(o/'tasks'/(tid+'-accepted.json'),t);write(o/'current-task.json',t);s.update(state='ACCEPTED',last_accepted_task_id=tid,last_developer_result='8a2d85d five-docsync independently accepted; LeaderP next.');s['observations'].append('Accepted8a2d85d exact5doc tokenP sync:2formalbytecopies64local links129510oldGitrecords unchanged; existingreview authority confirmed; LeaderP separate task next.');write(o/'state.json',s);print(json.dumps({'verification':r,'acceptance_sha256':sha(ap.read_bytes())}))
