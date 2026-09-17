import sys, json, copy
from pathlib import Path
root=Path('/Users/orderly_ray/Projects/think/tools/asr_review_acquisition_v7')
sys.path[:0]=[str(root),str(root/'tests')]
from network_guard import NetworkGuard
with NetworkGuard() as guard:
    from manual_support import bundle, attach, rebuild
    from offline_review.manual import ManualPins
    from offline_review.policy import digest
    from test_manual_intake import execute
    results=[]
    for name in ('control','historical_0600','external_report_identity'):
        b=bundle();p=copy.deepcopy(b[6]);pins=b[3].manual_pins
        if name=='historical_0600':
            p['R']['object']['historical_envelope']['mode']='0600'
            pins=rebuild(p,b[3].release_hash)
        if name=='external_report_identity':
            # Completely authored historical report identity, distinct from normalized R.
            p['K']['R']=digest({'accepted_existing_report':'Self-authored older report format'})
            p['F']['K']=digest(p['K'])
            p['M'].update(F=digest(p['F']),K=digest(p['K']),R=p['K']['R'])
            p['A'].update(F=digest(p['F']),M=digest(p['M']))
            pins=ManualPins(b[3].release_hash,digest(p['F']),digest(p['M']),digest(p['A']))
        b=attach(b,p,pins)
        terminal,records=execute(b,Path(__file__).parent/name)
        results.append({'case':name,'stop_reason':terminal['stop_reason'],
            'calls':len(terminal['calls']),'effective_status':terminal.get('effective_comment_review_status'),
            'authority_records':sum(r['event']=='manual_authority_verified' for r in records)})
    report={'results':results,'network':guard.evidence(),'only_authored_fixtures':True}
    (Path(__file__).parent/'results.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
