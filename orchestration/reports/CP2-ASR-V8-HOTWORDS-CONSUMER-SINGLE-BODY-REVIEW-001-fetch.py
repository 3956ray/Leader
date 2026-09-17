"""One fixed authorized blob acquisition. First-party, no target execution."""
import base64
import hashlib
import http.client
import json
import os
from pathlib import Path
import ssl
import stat
import time
from datetime import datetime, timezone

ROOT = Path('/private/tmp/think-hotword-single-a4a7efb3bf5b4476b68937ee3333c8d7')
REPORTS = Path('/Users/orderly_ray/Leader/orchestration/reports')
APPROVAL = REPORTS / 'CP2-ASR-V8-HOTWORDS-CONSUMER-AUTHORIZATION-001-approved.json'
REQUEST = REPORTS / 'CP2-ASR-V8-HOTWORDS-CONSUMER-AUTHORIZATION-PREPARATION-001-request.json'
APPROVAL_SHA = '2cc71640231337f3984a465b8ad6ae08482bfc1cb45338d43b98e6661114935d'
REQUEST_SHA = '0c08c5cfd1c3cc3ebe2daf32ea128bf91f171ed72a29639b953918c735fd562d'
BLOB = '20d4646bb5c6ffbe714848cc497e1809113d5195'
BODY_SHA = 'c872eb5cdf4f4e25b133e79cfd156343782f61a344efba7b3aef4a6f3d1e1b79'
HOST = 'api.github.com'
ENDPOINT = '/repos/k2-fsa/sherpa-onnx/git/blobs/' + BLOB
CAP = 65536

def sha(b):
    return hashlib.sha256(b).hexdigest()

def reject_constant(value):
    raise ValueError("nonstandard_json_constant")

def unique_pairs(pairs):
    out = {}
    for k, v in pairs:
        if k in out:
            raise ValueError('duplicate_json_key')
        out[k] = v
    return out

def read_pinned(path, digest):
    fd = os.open(str(path), os.O_RDONLY | os.O_NOFOLLOW)
    try:
        s = os.fstat(fd)
        if not stat.S_ISREG(s.st_mode) or s.st_nlink != 1 or s.st_size > 20000:
            raise ValueError('unsafe_input')
        b = os.read(fd, 20001)
        if len(b) != s.st_size or sha(b) != digest:
            raise ValueError('input_identity')
        return json.loads(b, object_pairs_hook=unique_pairs, parse_constant=reject_constant)
    finally:
        os.close(fd)

def persist(name, data):
    fd = os.open(str(ROOT / name), os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    try:
        with os.fdopen(fd, 'wb', closefd=False) as f:
            f.write(data)
            f.flush()
            os.fsync(fd)
        s = os.fstat(fd)
        if not stat.S_ISREG(s.st_mode) or s.st_nlink != 1 or stat.S_IMODE(s.st_mode) != 0o600 or s.st_size != len(data):
            raise ValueError('unsafe_output')
    finally:
        os.close(fd)
    dfd = os.open(str(ROOT), os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        os.fsync(dfd)
    finally:
        os.close(dfd)
    return {'name': name, 'bytes': len(data), 'sha256': sha(data)}

def encoded(d):
    return (json.dumps(d, sort_keys=True, indent=2) + '\n').encode('utf-8')

def main():
    os.umask(0o077)
    st = ROOT.lstat()
    if not stat.S_ISDIR(st.st_mode) or stat.S_IMODE(st.st_mode) != 0o700 or st.st_uid != os.getuid() or any(ROOT.iterdir()):
        raise ValueError('root_not_fresh_private_directory')
    approval = read_pinned(APPROVAL, APPROVAL_SHA)
    request = read_pinned(REQUEST, REQUEST_SHA)
    if approval['RESULT'] != 'APPROVED' or approval['request_json']['sha256'] != REQUEST_SHA or approval['candidate'] != request['candidate']:
        raise ValueError('authority_mismatch')
    c = request['candidate']
    if (c['git_blob'], c['mode'], c['decoded_bytes'], c['expected_body_sha256']) != (BLOB, '100644', 8993, BODY_SHA):
        raise ValueError('candidate_mismatch')
    marker = {'authority_sha256': APPROVAL_SHA, 'request_sha256': REQUEST_SHA, 'started_at': datetime.now(timezone.utc).isoformat(), 'no_retry': True}
    marker_ref = persist('attempt-consumed.json', encoded(marker))
    result = {'status': 'BLOCKED', 'attempt_marker': marker_ref, 'request_sha256': REQUEST_SHA, 'approval_sha256': APPROVAL_SHA, 'endpoint': ENDPOINT, 'requests_started': 0, 'metadata_requests': 0, 'redirects_followed': 0, 'retries': 0, 'root': str(ROOT), 'files': [], 'body_verified': False}
    conn = None
    started = time.monotonic()
    try:
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        ctx.load_default_certs()
        conn = http.client.HTTPSConnection(HOST, timeout=10, context=ctx)
        result['requests_started'] = 1
        conn.request('GET', ENDPOINT, headers={'User-Agent': 'think-single-body-static-review', 'Accept': 'application/vnd.github+json', 'Accept-Encoding': 'identity', 'Connection': 'close'})
        response = conn.getresponse()
        result['http_status'] = response.status
        headers = response.getheaders()
        framing = {}
        for key, value in headers:
            key = key.lower()
            if key in ('content-length', 'content-encoding', 'transfer-encoding'):
                if key in framing:
                    raise ValueError('ambiguous_http_framing')
                framing[key] = value
        result['framing'] = framing
        if response.status != 200:
            raise ValueError('http_non_200_no_follow')
        if framing.get('content-encoding', 'identity').lower() != 'identity':
            raise ValueError('compressed_response')
        if 'transfer-encoding' in framing and ('content-length' in framing or framing['transfer-encoding'].lower() != 'chunked'):
            raise ValueError('unsupported_http_framing')
        if 'content-length' in framing:
            n = framing['content-length']
            if not n.isascii() or not n.isdigit() or int(n) >= CAP:
                raise ValueError('invalid_or_oversized_length')
        raw = response.read(CAP)
        result['response_entity_bytes'] = len(raw)
        result['files'].append(persist('response.json', raw))
        if len(raw) >= CAP:
            raise ValueError('response_entity_cap')
        if 'content-length' in framing and len(raw) != int(framing['content-length']):
            raise ValueError('response_truncated')
        data = json.loads(raw.decode('utf-8', errors='strict'), object_pairs_hook=unique_pairs, parse_constant=reject_constant)
        if type(data) is not dict or data.get('sha') != BLOB or type(data.get('size')) is not int or data['size'] != 8993 or data.get('encoding') != 'base64':
            raise ValueError('blob_envelope_identity')
        content = data.get('content')
        if type(content) is not str or any(ch not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=\n' for ch in content):
            raise ValueError('invalid_base64_alphabet')
        compact = content.replace('\n', '')
        body = base64.b64decode(compact, validate=True)
        if base64.b64encode(body).decode('ascii') != compact:
            raise ValueError('noncanonical_base64')
        if len(body) != 8993 or len(body) > 262144 or sha(body) != BODY_SHA:
            raise ValueError('decoded_identity')
        if hashlib.sha1(b'blob ' + str(len(body)).encode('ascii') + b'\0' + body).hexdigest() != BLOB:
            raise ValueError('git_blob_identity')
        body.decode('utf-8', errors='strict')
        if b'\0' in body:
            raise ValueError('nul_in_body')
        result['files'].append(persist('online-recognizer.cc', body))
        result.update(status='ACQUIRED_FOR_STATIC_REVIEW_ONLY', body_verified=True, decoded_bytes=len(body), git_blob=BLOB, body_sha256=sha(body))
    except Exception as exc:
        result['stop_reason'] = type(exc).__name__ + ':' + str(exc)[:180]
    finally:
        if conn is not None:
            conn.close()
        result['elapsed_seconds'] = round(time.monotonic() - started, 3)
        result['ended_at'] = datetime.now(timezone.utc).isoformat()
        terminal = persist('acquisition-terminal.json', encoded(result))
        print(json.dumps({'terminal': terminal, 'status': result['status'], 'requests_started': result['requests_started'], 'body_verified': result['body_verified'], 'root': str(ROOT)}))

if __name__ == '__main__':
    main()
