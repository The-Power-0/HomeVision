#!/usr/bin/env python3
"""HomeVision WebView-only build checks used by both regular and release CI.

This is a narrow, deterministic guard, not a complete SBOM or legal audit.

Usage:
  python3 scripts/homevision_ci_guard.py source
  python3 scripts/homevision_ci_guard.py dependency path/to/dependency-report.txt
  python3 scripts/homevision_ci_guard.py apk path/to/build.apk
"""
from __future__ import annotations

import re
import struct
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def require_bytes(path: str, minimum: int = 1) -> bytes:
    file = ROOT / path
    if not file.is_file():
        fail(f"Missing required file: {path}")
    raw = file.read_bytes()
    if len(raw) < minimum:
        fail(f"Missing/truncated required file: {path} ({len(raw)} bytes)")
    return raw


def require_text(path: str) -> str:
    return require_bytes(path).decode('utf-8-sig')


def verify_png(path: str, width: int, height: int) -> None:
    raw = require_bytes(path, 1000)
    if raw[:8] != b'\x89PNG\r\n\x1a\n' or raw[12:16] != b'IHDR':
        fail(f'Invalid PNG: {path}')
    actual = struct.unpack('>II', raw[16:24])
    if actual != (width, height):
        fail(f'{path}: PNG dimension mismatch: {actual} != {(width,height)}')


def verify_source() -> None:
    gradle = require_text('app/build.gradle.kts')
    manifest = require_text('app/src/main/AndroidManifest.xml')
    main = require_text('app/src/main/java/com/phlox/tvwebbrowser/activity/main/MainActivity.kt')
    strings = require_text('app/src/main/res/values/strings.xml')
    catalog = require_text('gradle/libs.versions.toml')
    db = require_text('app/src/main/java/com/phlox/tvwebbrowser/singleton/AppDatabase.kt')
    tab = require_text('app/common/src/main/java/com/phlox/tvwebbrowser/model/WebTabState.kt')

    if 'applicationId = "com.homevision.tv"' not in gradle:
        fail('Unexpected app ID')
    if not re.search(r'versionName\s*=\s*"\d+\.\d+\.\d+"',gradle):
        fail('Missing semantic versionName')
    if not re.search(r'versionCode\s*=\s*\d+',gradle):
        fail('Missing integer versionCode')
    if '"geckoIncludedImplementation"(project(":app:gecko"))' not in gradle:
        fail('Gecko source-set boundary unexpectedly changed; review manually')
    if '@drawable/homevision_launcher' not in manifest or '@drawable/homevision_banner' not in manifest:
        fail('Manifest branding resource names changed')
    verify_png('app/src/main/res/drawable-nodpi/homevision_launcher.png',512,512)
    verify_png('app/src/main/res/drawable-nodpi/homevision_banner.png',1280,720)
    if (ROOT / 'app/src/main/res/drawable/homevision_launcher.xml').exists():
        fail('Legacy HomeVision launcher vector still present')
    if (ROOT / 'app/src/main/res/drawable/homevision_banner.xml').exists():
        fail('Legacy HomeVision banner vector still present')
    # C14: never package obsolete upstream launcher, banner or homepage artwork.
    legacy_artwork = (
        'app/src/main/assets/pages/home/logo.png',
        'app/src/main/res/drawable-mdpi/ic_launcher.png',
        'app/src/main/res/drawable-hdpi/ic_launcher.png',
        'app/src/main/res/drawable-xhdpi/ic_launcher.png',
        'app/src/main/res/drawable-xxhdpi/ic_launcher.png',
        'app/src/main/res/drawable-xxxhdpi/ic_launcher.png',
        'app/src/main/res/drawable-xhdpi/banner.png',
    )
    for obsolete in legacy_artwork:
        if (ROOT / obsolete).exists():
            fail(f'Obsolete upstream branding image returned: {obsolete}')
    tab_adapter = require_text('app/src/main/java/com/phlox/tvwebbrowser/activity/main/view/tabs/TabsAdapter.kt')
    download_service = require_text('app/src/main/java/com/phlox/tvwebbrowser/service/downloads/DownloadService.kt')
    tab_layout = require_text('app/src/main/res/layout/view_horizontal_webtab_item.xml')
    home_html = require_text('app/src/main/assets/pages/home/index.html')
    if 'R.drawable.ic_launcher' in tab_adapter or 'R.drawable.ic_launcher' in download_service:
        fail('Obsolete launcher reference remains in Kotlin source')
    if '@drawable/ic_launcher' in tab_layout:
        fail('Obsolete launcher reference remains in tab layout')
    if 'logo.png' in home_html:
        fail('Legacy homepage logo still referenced')
    if 'R.drawable.ic_home_grey_900_24dp' not in tab_adapter:
        fail('Lightweight fallback favicon missing')
    if 'R.drawable.ic_file_download_grey_900' not in download_service:
        fail('Download notification icon missing')
    if any(token in main for token in ('showKioskHintIfNeeded','kioskHintShown','R.string.kiosk_mode_hint')):
        fail('Kiosk startup toast still referenced')
    if '<string name="kiosk_mode_hint"' in strings:
        fail('Unused kiosk startup string still present')
    for token in ('scheduleKioskAutoReload()', 'private fun exitKioskMode()', 'HomeVision: Cursor mode',
                  'HomeVision: Spatial mode', 'kiosk_url_not_configured'):
        if token not in main:
            fail(f'Expected kiosk/nav behavior missing: {token}')
    for token in ('ADD adblock INTEGER;', "DROP TABLE IF EXISTS 'adblocklist'", 'createAdBlockListTable(db)'):
        if token not in db:
            fail(f'Historic Room schema migration removed: {token}')
    if 'var adblock: Boolean? = null' not in tab:
        fail('Historic Room column removed; upgrade migration required')

    for token in ('ad-block', 'com.brave', 'brave.adblock'):
        if token.lower() in gradle.lower() or token.lower() in catalog.lower():
            fail(f'Ad-blocking dependency declaration reintroduced: {token}')

    for path in ('LICENSE.md','docs/HOMEVISION_ATTRIBUTION.md',
                 'docs/HOMEVISION_THIRD_PARTY_LICENSE_REVIEW.md',
                 'app/src/main/assets/homevision/TV_BRO_LICENSE.md',
                 'app/src/main/assets/homevision/ATTRIBUTION.md',
                 'app/src/main/assets/homevision/SEGMENTED_BUTTON_LICENSE.txt',
                 'app/src/main/assets/homevision/PINNED_SECTION_LISTVIEW_NOTICE.txt',
                 'app/src/main/assets/homevision/APACHE_2_0_LICENSE.txt'):
        require_bytes(path, 90)
    segmented=require_text('app/src/main/assets/homevision/SEGMENTED_BUTTON_LICENSE.txt')
    if 'BSD 2-Clause License' not in segmented or 'Fedir Tsapana' not in segmented:
        fail('Segmented-button license text is missing copyright/terms')
    pinned=require_text('app/src/main/assets/homevision/PINNED_SECTION_LISTVIEW_NOTICE.txt')
    if 'Sergej Shafarenka' not in pinned or 'Apache' not in pinned:
        fail('Pinned-section-listview attribution missing')
    apache=require_text('app/src/main/assets/homevision/APACHE_2_0_LICENSE.txt')
    if 'Apache License' not in apache or 'Version 2.0' not in apache:
        fail('Apache-2.0 license text missing')
    print('PASS: Source, branding, kiosk, Room migration and license-notice safeguards')


def verify_dependency(path: Path) -> None:
    raw=path.read_text(encoding='utf-8-sig')
    if 'genericGeckoExcluded' not in raw:
        fail('Dependency report is not from genericGeckoExcluded')
    regex=re.compile(r'(?i)(?:com\.github\.truefedex:ad-block|com\.brave[.:]|brave\.adblock|(?:org\.mozilla\.)?geckoview)')
    lines=[x.strip() for x in raw.splitlines() if regex.search(x)]
    if lines:
        fail('Unexpected runtime libraries:\n'+'\n'.join(lines[:20]))
    print('PASS: Resolved WebView runtime has no Brave ad-block or GeckoView dependencies')


def verify_apk(path: Path) -> None:
    if not path.is_file():
        fail(f'APK missing: {path}')
    size=path.stat().st_size
    if not (100_000 < size < 25_000_000):
        fail(f'Unexpected APK size: {size} bytes')
    required_assets=('TV_BRO_LICENSE.md','ATTRIBUTION.md','SEGMENTED_BUTTON_LICENSE.txt',
                     'PINNED_SECTION_LISTVIEW_NOTICE.txt','APACHE_2_0_LICENSE.txt')
    with zipfile.ZipFile(path) as archive:
        names=set(archive.namelist())
        for name in required_assets:
            key='assets/homevision/'+name
            if key not in names or archive.getinfo(key).file_size < 90:
                fail(f'Missing or empty bundled license/notice: {key}')
        native=sorted(x for x in names if x.startswith('lib/') and x.endswith('.so'))
        if native:
            fail('Unexpected native binaries in WebView-only APK:\n'+'\n'.join(native[:30]))
        # C14: inspect actual compiled resources, not just names in the source tree.
        obsolete_apk = sorted(name for name in names if
            name == 'assets/pages/home/logo.png' or
            re.fullmatch(r'res/drawable-(?:mdpi|hdpi|xhdpi|xxhdpi|xxxhdpi)-v4/(?:ic_launcher|banner)\.png', name)
        )
        if obsolete_apk:
            fail('Legacy branding still packaged in APK:\n' + '\n'.join(obsolete_apk))
    print(f'PASS: APK {path.name} ({size:,} bytes) has required notices and no native binaries')


def main() -> None:
    if len(sys.argv)<2 or sys.argv[1] not in ('source','dependency','apk'):
        fail('Usage: homevision_ci_guard.py source | dependency PATH | apk PATH')
    mode=sys.argv[1]
    if mode=='source':
        if len(sys.argv)!=2: fail('source does not accept arguments')
        verify_source()
    elif mode=='dependency':
        if len(sys.argv)!=3: fail('dependency requires a Gradle report path')
        verify_dependency(Path(sys.argv[2]))
    else:
        if len(sys.argv)!=3: fail('apk requires a file path')
        verify_apk(Path(sys.argv[2]))

if __name__=='__main__':
    main()
