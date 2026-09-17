"""Read-only verification of the fixed stage1 evidence, never load target code."""
import hashlib
import json
import stat
import unicodedata
import zipfile
from pathlib import Path

ROOT = Path('/private/tmp/think-vosk-artifact-review/CP2-VOSK-ARTIFACT-STATIC-REVIEW-001/attempts/07a96480-78dd-4040-8d30-5bc8d44a7ed0')


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()


def verify():
    ledger = json.loads((ROOT / 'reports/acquisition-ledger.json').read_text())
    expected = {
        'runtime': 'https://repo.maven.apache.org/maven2/com/alphacephei/vosk-android/0.3.75/vosk-android-0.3.75.aar',
        'model': 'https://alphacephei.com/vosk/models/vosk-model-small-cn-0.22.zip',
    }
    assert ledger['result'] == 'COMPLETE' and ledger['adoption_gate'] == 'blocked'
    assert len(ledger['attempts']) == 2 and ledger['seconds'] < 1800
    assert [a['object'] for a in ledger['attempts']] == ['runtime', 'model']
    output = []
    for a in ledger['attempts']:
        assert a['url'] == expected[a['object']] and a['method'] == 'GET'
        assert a['http'] == 200 and a['attempt'] == 1 and a['hop'] == 0
        assert a['seconds'] < 180 and a['bytes'] <= 64 * 1024**2
        p = Path(a['path'])
        assert p.parent == ROOT / 'artifacts' and stat.S_ISREG(p.lstat().st_mode)
        assert stat.S_IMODE(p.stat().st_mode) == 0o600
        assert p.stat().st_size == a['bytes'] == int(a['headers']['content-length'])
        assert digest(p) == a['sha256']
        inv = json.loads((ROOT / 'reports' / (a['object'] + '-inventory.json')).read_text())
        assert inv['sha256'] == a['sha256'] and inv['result'] == 'basic_inventory_complete'
        read_total = 0
        with zipfile.ZipFile(p) as z:
            infos = z.infolist()
            assert len(infos) == len(inv['members']) <= 10000
            assert sum(i.file_size for i in infos) == inv['declared_expansion'] <= 512 * 1024**2
            keys = set()
            for info, row in zip(infos, inv['members']):
                assert row['name'] == info.filename and row['declared'] == info.file_size
                assert row['compressed'] == info.compress_size
                assert not info.flag_bits & 1 and info.file_size <= 128 * 1024**2
                assert not info.filename.startswith('/') and '\\' not in info.filename
                assert all(x not in ('', '.', '..') for x in info.filename.rstrip('/').split('/'))
                assert stat.S_IFMT(info.external_attr >> 16) in (0, stat.S_IFDIR, stat.S_IFREG)
                key = unicodedata.normalize('NFC', info.filename.rstrip('/')).casefold()
                assert key not in keys
                keys.add(key)
                if row['coverage'] == 'full':
                    assert info.file_size <= 2 * 1024**2
                    with z.open(info) as member:
                        body = member.read(2 * 1024**2 + 1)
                    assert len(body) == row['read_bytes'] == info.file_size
                    assert hashlib.sha256(body).hexdigest() == row['sha256'] and row['crc'] == 'verified'
                    read_total += len(body)
                else:
                    assert row['read_bytes'] == 0 and row['crc'] == 'Unknown'
            assert read_total == inv['expanded_bytes']
        output.append({'object': a['object'], 'bytes': a['bytes'], 'sha256': a['sha256'],
                       'members': len(infos), 'verified_text_bytes': read_total})
    assert sum(x['bytes'] for x in output) == ledger['network_body_bytes'] == 57371392
    assert sum(x['verified_text_bytes'] for x in output) == ledger['expanded_bytes'] == ledger['text_bytes'] == 715
    assert not any((ROOT / 'unpacked').iterdir())
    return {'RESULT': 'PASS', 'files': output, 'network_rechecked': False,
            'target_executed': False, 'binary_contents_reviewed': False,
            'scope': 'Retained artifacts, outer inventory and previously read small text members only'}


if __name__ == '__main__':
    print(json.dumps(verify(), indent=2))
