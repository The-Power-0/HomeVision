# HomeVision

**HomeVision** is a lightweight Android TV / Fire TV browser fork designed to display a user-configured web dashboard fullscreen, with remote-friendly kiosk navigation.

**Project lineage:** [HomeVision](https://github.com/The-Power-0/HomeVision) is derived from [DataVision by ayumilove](https://github.com/ayumilove/DataVision), which is derived from [TV Bro by Fedir Tsapana](https://github.com/truefedex/tv-bro). HomeVision is an independent derivative project, not an official release or endorsement of either upstream project.

> **Status: pre-release.** Version 1.0.1 has been built and tested on a Living Room Fire TV Stick. Public release is intentionally on hold pending an in-app attribution/branding review, third-party dependency and asset license audit, and verification of the GitHub production-signing pipeline.

## What HomeVision changes

Compared with the upstream DataVision application:

- **System WebView build:** the intended HomeVision APK is the `genericGeckoExcluded` flavor, using Android's installed WebView rather than bundling Mozilla GeckoView. A Windows-built 1.0.1 debug APK was approximately 10.7 MiB. Actual sizes depend on build type and toolchain.
- **Independent identity:** app label `HomeVision`, Android package `com.homevision.tv`, and HomeVision launcher icon/banner.
- **Fullscreen dashboard kiosk:** preserves DataVision's configurable kiosk URL, page restoration, and network recovery behavior.
- **Spatial navigation by default:** when a page finishes loading in kiosk/WebView mode, the virtual cursor is disabled so D-pad focus navigation can be used on supported web pages.
- **Remote navigation toggle:** hold the remote's **Fast Forward** key for approximately **3 seconds** to switch between spatial navigation and the virtual cursor. Repeat to switch back. A brief confirmation appears on screen. The remote must deliver Android `KEYCODE_MEDIA_FAST_FORWARD`; support is device-dependent.
- **Kiosk Back handling:** custom behavior supports escaping web-dashboard overlays without accidentally leaving kiosk mode. Actual behavior depends on the webpage's navigation and focus handling.
- **No in-app automatic APK updates:** the `generic` flavor currently sets `BUILT_IN_AUTO_UPDATE` to `false`. Updates are managed externally; do not follow DataVision's older `latest_version.json` auto-update instructions for HomeVision.

The original DataVision/TV Bro source tree and several broader browser features remain in this fork. HomeVision is **not** a rewrite, and choosing the WebView build does not imply that all unused source has been removed.

## Platform and configuration

- Intended for Android TV and Amazon Fire TV devices with a usable system WebView.
- Builds use JDK 17 or another compatible JDK, Android SDK Platform 36 / Build Tools 36.0.0, and the repository's Gradle wrapper.
- Fire OS 7 and Fire OS 8 coverage across all target devices is still being validated; do not assume every remote sends identical keys.
- A dashboard web application and its authentication are **not bundled**. Configure your own URL in HomeVision's kiosk settings; the Home Assistant dashboard used during development is a separate project.

### Remote controls

| Action | Behavior |
| --- | --- |
| D-pad | Spatial focus navigation where the loaded webpage supports it |
| Fast Forward held ~3 seconds | Toggle spatial navigation / virtual cursor in WebView kiosk mode |
| Back | Kiosk/web-page Back handling, including supported overlay dismissal |
| Long Back or Menu | Inherited kiosk exit/settings behavior; confirm on each device |
| Reload or new page load | Restores spatial mode in WebView kiosk mode |

## Building HomeVision

On Windows, from the repository root:

```powershell
# Build the small, system-WebView debug APK
.\gradlew.bat :app:assembleGenericGeckoExcludedDebug --no-daemon --console=plain

# Run the unit-test task
.\gradlew.bat :app:testGenericGeckoExcludedDebugUnitTest --no-daemon --console=plain
```

Debug APK output:

`app/build/outputs/apk/genericGeckoExcluded/debug/app-generic-geckoExcluded-debug.apk`

For a **production-signed** APK, set `KEYSTORE_PATH`, `KEYSTORE_PASSWORD`, `KEY_ALIAS`, and `KEY_PASSWORD` securely in the build environment and run:

```powershell
.\gradlew.bat :app:assembleGenericGeckoExcludedRelease --no-daemon --console=plain
```

Release APK output is under `app/build/outputs/apk/genericGeckoExcluded/release/`. Verify the actual APK package/version and signer with Android SDK `aapt` and `apksigner` before distribution. **Never commit a keystore, signing password, or encoded keystore to this repository.**

### APK update / signing compatibility

Android normally requires the **same signing certificate** for an in-place APK update. A debug-signed HomeVision build cannot be replaced directly by a release APK using a different signing certificate. Plan any transition carefully: uninstalling an app generally deletes its stored settings, web data, and authentication session. Keep the existing installation and backups intact until the migration is tested.

## GitHub Actions

- [HomeVision CI](.github/workflows/homevision-ci.yml) builds and tests the WebView-only debug variant and uploads a short-lived build artifact. CI succeeded for version 1.0.1.
- [HomeVision Signed Release](.github/workflows/homevision-release.yml) is a **manual publishing workflow**. It expects the four encrypted repository secrets `KEYSTORE_BASE64`, `KEYSTORE_PASSWORD`, `KEY_ALIAS`, and `KEY_PASSWORD`. A successful invocation publishes a GitHub release: do **not** run it as a signing test.
- A local production-signed 1.0.1 APK has passed Android signature and package checks. The GitHub-hosted production-signing path and pre-release licensing requirements are not yet fully verified.

The original DataVision release workflow is retained as historical reference at `docs/DATAVISION_ORIGINAL_RELEASE_WORKFLOW.yml.txt`.

## License, provenance, and redistribution

TV Bro's original, **nonstandard BSD-derived license** is preserved verbatim in [LICENSE.md](LICENSE.md) and bundled in the app at `app/src/main/assets/homevision/TV_BRO_LICENSE.md`. Read the full license rather than assuming ordinary BSD-3-Clause terms apply.

For a **modified binary distribution**, its stated conditions include:

1. The derived application must **not** use `TV Bro` as its application name.
2. It must not reuse the original TV Bro application icon or Android application ID.
3. Its graphical About UI must state that it uses TV Bro's sources **and link to** [the original TV Bro project](https://github.com/truefedex/tv-bro).
4. Source redistribution must retain the original copyright notice, conditions, and disclaimer. Preserve notices accompanying binary distribution as required.

Credit is also due to [DataVision by ayumilove](https://github.com/ayumilove/DataVision), HomeVision's immediate parent. See [HomeVision attribution](docs/HOMEVISION_ATTRIBUTION.md) and the [third-party license review](docs/HOMEVISION_THIRD_PARTY_LICENSE_REVIEW.md).

**Before any public APK release, verify these remaining items:**

- Confirm that the About screen visibly and accurately attributes both DataVision and TV Bro and that the TV Bro source hyperlink works. Remove or replace inherited upstream branding where inappropriate without removing required attribution.
- Audit direct and transitive runtime dependencies, their license/NOTICE obligations, and bundled icons, graphics, data, and other assets in the **actual release APK**. The existing checklist is not a completed audit.
- Verify the release certificate matches the permanent signing key, test installation on intended Fire TV/Android TV versions, and confirm the release workflow produces the correct version and artifact.
- Keep the full license, required notices, and attribution accessible with released binaries.

This README documents the current implementation and release gates; it does not certify that every redistribution obligation has already been met.

## Upstream projects

- [DataVision](https://github.com/ayumilove/DataVision) — dashboard-kiosk customization and immediate source upstream.
- [TV Bro](https://github.com/truefedex/tv-bro) — original Android TV browser code and license, copyright © 2019 Fedir Tsapana.
