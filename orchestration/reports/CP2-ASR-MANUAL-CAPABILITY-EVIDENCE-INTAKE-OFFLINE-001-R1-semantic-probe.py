import sys, json, copy, base64, hashlib
from pathlib import Path
root=Path('/Users/orderly_ray/Projects/think/tools/asr_review_acquisition_v7')
sys.path[:0]=[str(root),str(root/'tests')]
from network_guard import NetworkGuard
with NetworkGuard() as guard:
    from manual_support import bundle, attach, rebuild, case, R1_POSITIVE, R1_NEGATIVE
    from offline_review.manual import ManualPins, CLEAR
    from offline_review.policy import digest, canonical
    from test_manual_intake import execute
    results=[]
    names=list(R1_POSITIVE+R1_NEGATIVE)+['changed_original_stale_representation','container_digest_as_original','new_original_stale_trust']
    for name in names:
        if name in R1_POSITIVE+R1_NEGATIVE:b,fault=case(name)
        else:
            b=bundle();p=copy.deepcopy(b[6]);pins=b[3].manual_pins;fault=None
            if name=='container_digest_as_original':
                p['R']['sha256']=digest(p['R'])
            else:
                raw=base64.b64decode(p['R']['content_base64'])+b'\n'
                sha=hashlib.sha256(raw).hexdigest()
                p['R'].update(sha256=sha,bytes=len(raw),content_base64=base64.b64encode(raw).decode())
                if name=='new_original_stale_trust':
                    p['representation']['original_report_sha256']=sha
                    rebuild(p,b[3].release_hash,refresh_original=False)
            b=attach(b,p,pins)
        directory=Path(__file__).parent/name
        terminal,records=execute(b,directory,fault)
        if name in R1_POSITIVE:
            assert len(terminal['calls'])==10 and terminal['effective_comment_review_status']==CLEAR
            p=b[6];original=base64.b64decode(p['R']['content_base64'])
            assert original!=canonical(json.loads(original))
            original_hash=hashlib.sha256(original).hexdigest()
            assert p['K']['R']==p['M']['R']==original_hash
            assert p['K']['representation']==p['M']['representation']==digest(p['representation'])!=original_hash
            addition=json.loads((directory/terminal['manual_capability_adjudications'][0]['file']).read_bytes())
            assert addition['review_report']==original_hash
            assert addition['review_representation']==digest(p['representation'])
        else:
            assert not terminal['calls']
            assert 'manual_authority_verified' not in [r['event'] for r in records]
            assert 'effective_comment_review_status' not in terminal
        results.append({'case':name,'stop_reason':terminal['stop_reason'],
            'calls':len(terminal['calls']),'effective_status':terminal.get('effective_comment_review_status')})
    report={'candidate':'443bbb5dc73e52dc11610ba766fdda23a0923b80','results':results,
        'positive':len(R1_POSITIVE),'negative':len(names)-len(R1_POSITIVE),
        'network':guard.evidence(),'only_authored_fixtures':True}
    (Path(__file__).parent/'results.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
