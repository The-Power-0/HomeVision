# DataVision

**[中文文档](README_zh-CN.md)**

DataVision is a heavily customized fork of the open-source [TV Bro](https://github.com/truefedex/tv-bro) browser, rebuilt as an **Android TV data-dashboard kiosk app**. It displays any web page fullscreen on an Android TV for long-term unattended operation — ideal for data dashboards, monitoring walls and digital signage.

- Package name: `im.xcode.datavision`
- Version: 1.0.0
- Rendering engine: GeckoView (bundled, no system WebView required)
- Default dashboard URL: none (a first-launch wizard guides you through configuration)

## Key Features

### Kiosk Display Mode
- Fullscreen display of the configured dashboard page on launch; all browser UI is hidden (address bar, menus, tabs, virtual cursor menu)
- First launch without a configured URL opens Settings automatically
- On every subsequent launch the **last visited page is restored**
- Changing the dashboard URL in Settings forces the new URL to open on next launch (one-time, then "restore last page" behavior resumes)
- An on-screen hint is shown on first launch (long press MENU/BACK to exit)

### Network Auto-Recovery
- Automatic retries on load failure: 5s → 10s → 30s backoff, then every 30s (retries the current page URL)
- Instant reload of the current page when network connectivity returns
- Optional periodic auto-reload ("auto reload interval" in Settings, minutes, 0 = off)

### 4K Display Optimization
- TV displays often report high density (e.g. 240dpi), which makes web viewports scale up. `DensityOneContextWrapper` forces GeckoView's rendering density to 1.0 so the web viewport maps 1:1 to physical pixels (equivalent to Chrome at 100% zoom). The app's own UI keeps the native density.

### Built-in Auto-Update
- On launch the app checks `latest_version.json` in this repository (release channel). When a new version is found, a changelog dialog is shown; the APK matching the device CPU architecture is downloaded and installed
- Enabled by default for sideloaded installs; can be disabled in Settings → Version

### Other Customizations
- The dashboard host is automatically exempted from ad blocking so chart/data components are never broken
- TV Bro logo and quick-link shortcuts removed from the internal home page
- Chinese localization for all kiosk-related UI texts
- Screen kept awake while kiosk is active

## Usage

| Action | How |
|---|---|
| Exit kiosk mode | Long press **BACK** or **MENU** on the remote (~1s) — Settings opens directly |
| Change dashboard URL | Exit kiosk → Settings → Kiosk mode URL → save → restart when prompted |
| Re-enter kiosk | Automatic on next app launch (no manual step) |
| Disable TV screensaver | Must be disabled in the TV system settings, or via ADB: `adb shell settings put secure screensaver_enabled 0` (an app cannot block the system screensaver) |

## Building

Requirements: Android SDK + JDK (Gradle Wrapper downloads dependencies automatically).

```powershell
# Release build + ABI splits (recommended)
.\gradlew.bat :app:assembleGenericGeckoIncludedRelease -PenableAbiSplits

# Sign with the local debug keystore (quick testing only)
powershell -ExecutionPolicy Bypass -File .\tools\sign_apks.ps1
```

Artifacts are written to `app\build\outputs\apk\genericGeckoIncluded\release\`:

| File | Architecture | Size |
|---|---|---|
| `app-generic-geckoIncluded-arm64-v8a-release.apk` | arm64 (most TVs) | ~179 MB |
| `app-generic-geckoIncluded-armeabi-v7a-release.apk` | arm32 | ~143 MB |
| `app-generic-geckoIncluded-x86_64-release.apk` | x86_64 (emulators) | ~196 MB |

Notes:
- Without `-PenableAbiSplits` a universal APK (~495 MB) containing all ABIs is produced
- The `geckoExcluded` flavor (~3 MB) relies on the system WebView and does not support the DPI fix; it is generally not recommended
- For real distribution use a release keystore (`KEYSTORE_PATH` etc., see `build.gradle.kts`); **updates require the same signing key**

## Releasing & Auto-Update

A GitHub Actions release pipeline is included (`.github/workflows/release.yml`):

1. Configure `KEYSTORE_BASE64`, `KEYSTORE_PASSWORD`, `KEY_ALIAS`, `KEY_PASSWORD` in Settings → Secrets
2. Actions → Release → Run workflow, enter the version (e.g. `1.1.0`)
3. The pipeline builds, signs, creates the Release and uploads the APKs (file names end with `-arm64-v8a.apk` etc. so the updater can match the device architecture)
4. After releasing, update `latest_version.json` in the repo root: point `latestVersionCode`/`latestVersionName` at the new version, update download URLs and changelog, push to main
5. Installed devices pick up the new version on next launch and prompt to update

Important: `versionCode` in `build.gradle.kts` must be incremented accordingly, otherwise the update check will not trigger.

## Key Customization Files

| File | Purpose |
|---|---|
| `app\common\...\Config.kt` | Kiosk settings (mode switch, dashboard URL, auto-reload interval) |
| `app\...\activity\main\MainActivity.kt` | Kiosk lifecycle, key-based exit, network recovery, launch restore |
| `app\gecko\...\GeckoWebEngine.kt` | Applies the density wrapper at GeckoView creation points |
| `app\gecko\...\DensityOneContextWrapper.kt` | DPI fix core (density=1.0 context wrapper) |
| `app\gecko\...\delegates\MyNavigationDelegate.kt` | Auto retry on load failure (exponential backoff) |
| `app\...\dialogs\settings\MainSettingsView.kt` | Kiosk settings UI |
| `app\src\main\assets\pages\home\index.html` | Internal home page (logo/quick links removed) |
| `app\src\main\res\values-zh\strings.xml` | Chinese localization of kiosk texts |

## Helper Tools (`tools\` directory)

| Script | Purpose |
|---|---|
| `sign_apks.ps1` | Batch-sign release APKs with the local debug keystore (auto-detects the SDK) |
| `list_apks.ps1` | List build artifacts with sizes |
| `find_sdk.ps1` | Locate the local Android SDK / build-tools |
| `verify_url_in_apk.ps1` | Verify that a given string (e.g. a default dashboard URL) is baked into an APK |

## License & Attribution

This project is derived from the TV Bro sources. Per TV Bro's [BSD-derived license](LICENSE.md): derived apps must not use the name "TV Bro", the original icon or the original application id, and must state the attribution in the UI. This app shows "Based on TV Bro sources" on its About page with a link to the original project.

- Original project: https://github.com/truefedex/tv-bro
