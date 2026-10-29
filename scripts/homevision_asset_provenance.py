#!/usr/bin/env python3
"""HomeVision C14.6 v2 inherited asset provenance guard.

source: validates 23 inherited assets against exact Git blob hashes in
        docs/HOMEVISION_INHERITED_ASSETS.csv. Changes must be reviewed and
        manifest refreshed intentionally, never silently.
apk:    checks the known inherited assets stored under assets/ remain packaged
        unmodified, plus the bundled provenance notice. Nine-patch PNGs are
        compiled by AAPT2 and cannot be byte-compared with source PNGs.
"""
from __future__ import annotations
import csv
import subprocess
import re
import sys
import zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
MANIFEST=ROOT/'docs/HOMEVISION_INHERITED_ASSETS.csv'
NOTICE='assets/homevision/BUNDLED_ASSET_PROVENANCE.md'

def fail(message: str):
    raise SystemExit('FAIL: '+message)

def git_blob_hash(raw: bytes, source_path: str) -> str:
    """Return canonical Git blob ID using path-specific checkout filters.

    Windows may check out text resources as CRLF, though Git stores them as LF.
    Let Git apply the clean filter; do not normalize arbitrary binary bytes.
    """
    result=subprocess.run(
        ['git','hash-object','--stdin','--path='+source_path],
        cwd=ROOT, input=raw, capture_output=True,
    )
    if result.returncode:
        fail('Could not hash asset with Git filters: '+source_path+'; '+result.stderr.decode(errors='replace'))
    digest=result.stdout.decode('ascii').strip()
    if not re.fullmatch(r'[0-9a-f]{40}',digest):
        fail('Invalid Git object ID for '+source_path)
    return digest

def load_manifest():
    if not MANIFEST.is_file(): fail('Missing asset provenance manifest')
    with MANIFEST.open(encoding='utf-8-sig',newline='') as f:
        rows=list(csv.DictReader(f))
    if len(rows)!=23: fail(f'Expected 23 reviewed inherited assets, got {len(rows)}')
    required={'path','git_blob_sha1','matched_upstream','provenance_scope','license_review'}
    if not required.issubset(rows[0]): fail('Incomplete provenance manifest fields')
    paths=set()
    for row in rows:
        path=row['path']
        if path in paths or not path.startswith('app/src/main/') or '..' in Path(path).parts:
            fail('Invalid or duplicated asset path: '+path)
        paths.add(path)
        if not re.fullmatch(r'[0-9a-f]{40}',row['git_blob_sha1']):
            fail('Invalid Git blob hash: '+path)
        if not row['license_review']:
            fail('No license-review note for '+path)
    return rows

def source():
    for row in load_manifest():
        path=ROOT/row['path']
        if not path.is_file(): fail('Tracked inherited resource missing: '+row['path'])
        digest=git_blob_hash(path.read_bytes(),row['path'])
        if digest!=row['git_blob_sha1']:
            fail('Inherited asset changed: '+row['path']+f'\n expected {row["git_blob_sha1"]}, actual {digest}; review provenance before updating manifest')
    txt=(ROOT/'app/src/main/assets/homevision/BUNDLED_ASSET_PROVENANCE.md')
    if not txt.is_file() or 'Search-engine logos' not in txt.read_text(encoding='utf-8'):
        fail('Required bundled asset notice missing')
    print('PASS: 23 inherited resources match documented upstream blobs; bundled asset provenance notice exists')

def apk(apk_path: Path):
    rows=load_manifest()
    with zipfile.ZipFile(apk_path) as z:
        names=set(z.namelist())
        if NOTICE not in names or z.getinfo(NOTICE).file_size<250:
            fail('Bundled asset provenance notice absent from APK')
        checked=0
        for row in rows:
            path=row['path']
            if not path.startswith('app/src/main/assets/'):
                continue # AAPT2 compiles Android drawable nine-patches.
            relative='assets/'+path.removeprefix('app/src/main/assets/')
            if relative not in names:
                fail('Inherited web asset absent from APK: '+relative)
            packaged=z.read(relative)
            # Packaged assets are copied from the working tree, and on Windows
            # may therefore contain CRLF even though the canonical blob is LF.
            if packaged!=(ROOT/path).read_bytes():
                fail('Web asset bytes differ from checked-out source: '+relative)
            if git_blob_hash(packaged,path)!=row['git_blob_sha1']:
                fail('Packaged asset differs from audited upstream blob: '+relative)
            checked+=1
    print(f'PASS: {checked} inherited web assets match the working tree and upstream Git blobs; bundled notice present')

if __name__=='__main__':
    if len(sys.argv)==2 and sys.argv[1]=='source':source()
    elif len(sys.argv)==3 and sys.argv[1]=='apk':apk(Path(sys.argv[2]))
    else:fail('Usage: homevision_asset_provenance.py source | apk PATH')
