#!/usr/bin/env python3
"""Remap only live gym orchestration paths/role IDs; historical evidence is immutable."""
import argparse,json,subprocess,sys,uuid
from pathlib import Path
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--apply',action='store_true')
p.add_argument('--leader-thread',required=True)
p.add_argument('--pm-thread',required=True)
p.add_argument('--dev-thread',required=True)
a=p.parse_args()
leader=Path(__file__).resolve().parents[1]; base=leader.parent
roles={'leader':a.leader_thread,'product_manager':a.pm_thread,'developer':a.dev_thread}
for value in roles.values():
 uuid.UUID(value)
 if not value.startswith('01'): p.error('Use actual new Codex thread IDs starting with 01')
if len(set(roles.values())) != 3: p.error('Three distinct role threads are required')
roots={'/Users/orderly_ray/Leader':leader,'/Users/orderly_ray/Documents/Products Manager':base/'ProductManager','/Users/orderly_ray/Projects/gym-miniapp':base/'gym-miniapp'}
for root in roots.values():
 if not root.is_dir(): p.error('Missing sibling checkout: '+str(root))
def mapped(value):
 if isinstance(value,dict): return {k:mapped(v) for k,v in value.items()}
 if isinstance(value,list): return [mapped(v) for v in value]
 if isinstance(value,str):
  for old,new in roots.items(): value=value.replace(old,str(new))
 return value
folder=leader/'projects/gym-miniapp/orchestration'
project=mapped(json.loads((folder/'project.json').read_text())); project['threads']=roles
project['leader_root']=str(leader/'projects/gym-miniapp'); project['target_repo']=str(base/'gym-miniapp')
task=mapped(json.loads((folder/'current-task.json').read_text())); task['assigned_thread_id']=roles[task['owner']]
for path in project['canonical_sources']:
 if not Path(path).is_file(): p.error('Missing canonical source: '+path)
import hashlib
for source in task['input_documents']:
 if hashlib.sha256(Path(source['path']).read_bytes()).hexdigest()!=source['sha256']: p.error('Source hash mismatch: '+source['path'])
if a.apply:
 for name,value in [('project',project),('current-task',task)]:
  (folder/(name+'.json')).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
 result=subprocess.run([sys.executable,str(leader/'scripts/leader_check.py'),'--root',str(folder.parent)])
 raise SystemExit(result.returncode)
print('PASS: paths, nine document hashes and role IDs checked; dry-run only. Add --apply to write live routing. No dispatch or tool security changes.')
