import sys, json, hashlib, random, base64
from datetime import datetime, timedelta
from pathlib import Path
root=Path('/Users/orderly_ray/Projects/think/tools/asr_review_acquisition_v8')
sys.path[:0]=[str(root),str(root/'tests')]
from network_guard import NetworkGuard
with NetworkGuard() as guard:
    from offline_review.timestamps import represent,validate
    from offline_review.policy import Rejected,canonical,digest
    from recalculate import independent_timestamp,verify_terminal
    from timestamp_support import case,INVALID
    from test_manual_intake import execute
    rng=random.Random(873142)
    checks=accepted=rejected=0;fingerprint=hashlib.sha256()
    def compare(y,m,d,h,mi,s,f,offset,zone=None):
        global checks,accepted,rejected
        zone=zone or (('+' if offset>=0 else '-')+f'{abs(offset)//60:02d}:{abs(offset)%60:02d}')
        raw=f'{y:04d}-{m:02d}-{d:02d}T{h:02d}:{mi:02d}:{s:02d}'+('.'+f if f else '')+zone
        checks+=1;fingerprint.update(raw.encode()+b'\n')
        try:
            utc=datetime(y,m,d,h,mi,s,int(f.ljust(6,'0')) if f else 0)-timedelta(minutes=offset)
        except (ValueError,OverflowError):
            for function,exception in [(represent,Rejected),(independent_timestamp,AssertionError)]:
                try:function(raw)
                except exception:pass
                else:raise AssertionError(('accepted_invalid',raw))
            rejected+=1;return
        a=represent(raw);b=independent_timestamp(raw);assert a==b,(raw,a,b)
        delta=utc-datetime(1970,1,1)
        micro=(delta.days*86400+delta.seconds)*1000000+delta.microseconds
        expected=f'{utc.year:04d}-{utc.month:02d}-{utc.day:02d}T{utc.hour:02d}:{utc.minute:02d}:{utc.second:02d}'+('.'+f'{utc.microsecond:06d}'[:len(f)] if f else '')+'Z'
        assert a['reviewed_at_utc']==expected and a['instant_microseconds']==micro
        assert a['fraction_digits']==len(f) and a['offset_minutes']==offset and a['reviewed_at_raw']==raw
        assert validate(a)==a
        accepted+=1
    for i in range(20000):
        digits=rng.randrange(7);f=''.join(str(rng.randrange(10)) for _ in range(digits))
        compare(rng.randrange(1,10000),rng.randrange(1,13),rng.randrange(1,32),rng.randrange(24),rng.randrange(60),rng.randrange(60),f,rng.randrange(-840,841))
    for y in range(1,10000):compare(y,2,29,0,0,0,'000001',0,'Z')
    for y,m,d,h,mi,s in [(1,1,1,0,0,0),(9999,12,31,23,59,59)]:
        for off in range(-840,841):compare(y,m,d,h,mi,s,'999999',off)
    for raw in INVALID.values():
        for function,exception in [(represent,Rejected),(independent_timestamp,AssertionError)]:
            try:function(raw)
            except exception:pass
            else:raise AssertionError(('accepted_bad_syntax',raw))
    controller=[]
    names=['time_input_schema7','time_domain_H','time_domain_R','time_domain_representation','time_domain_K','time_domain_M','time_domain_T','time_equal_fraction','time_equal_zero_zone','time_tamper_raw_domain','time_tamper_utc_domain','time_tamper_instant_float','time_invalid_utc_underflow','time_invalid_utc_overflow']
    schema_mutant_rejected=False
    for name in names:
        b,fault=case(name);p=Path(__file__).parent/name;t,records=execute(b,p,fault)
        assert not t['calls'] and 'manual_authority_verified' not in [r['event'] for r in records]
        (p/'input.json').write_bytes(b[0])
        (p/'manual-driver.json').write_bytes(canonical(dict(raw_package_base64=base64.b64encode(b[5]).decode(),independent_pins=b[3].manual_pins.document())))
        (p/'imported-metadata.json').write_bytes(canonical(dict(commit=b[1].decode(),tree=b[2].decode())))
        (p/'io-observations.json').write_bytes(canonical(dict(trace=b[4].trace,receipts=b[4].observed,read_sizes=b[4].read_sizes)))
        assert verify_terminal(p,t)==len(records)
        if name=='time_input_schema7':
            wrong=dict(t,stop_reason='missing_review_evidence');wrong['evidence_hash']=digest({k:v for k,v in wrong.items() if k!='evidence_hash'})
            (p/'terminal.json').write_bytes(canonical(wrong))
            try:verify_terminal(p,wrong)
            except AssertionError:schema_mutant_rejected=True
            else:raise AssertionError('schema stop assertion not enforced')
            (p/'terminal.json').write_bytes(canonical(t))
        controller.append(dict(case=name,stop_reason=t['stop_reason'],calls=len(t['calls']),independent_terminal='PASS'))
    result=dict(candidate='1fe85740a185a63ca4f35df2abd22ae410f82fbb',calendar_cases=checks,accepted=accepted,rejected=rejected,
        syntax_cases=len(INVALID),input_fingerprint=fingerprint.hexdigest(),controller=controller,schema_mutant_rejected=schema_mutant_rejected,network=guard.evidence())
    (Path(__file__).parent/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
