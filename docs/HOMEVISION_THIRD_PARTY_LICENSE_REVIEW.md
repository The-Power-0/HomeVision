# HomeVision third-party licensing and reproducible build safeguards

Updated for HomeVision 1.0.4. **This is a partial source-level license audit, not a
legal compliance certification or a complete transitive-dependency SBOM.**
HomeVision is based on DataVision and TV Bro. Preserve `LICENSE.md`, the original
TV Bro license inside the APK, and both upstream project attributions.

## Confirmed direct dependencies (WebView-only flavor)

| Component | Coordinates / provenance | Identified license | Included notice |
|---|---|---|---|
| TV Bro source / DataVision derivative | `https://github.com/truefedex/tv-bro` and `https://github.com/ayumilove/DataVision` | Original inherited `LICENSE.md` (special source terms; do not relabel it) | `assets/homevision/TV_BRO_LICENSE.md`, `assets/homevision/ATTRIBUTION.md` |
| Segmented Button | `com.github.truefedex:segmented-button:v1.0.0` | BSD-2-Clause, copyright 2018 Fedir Tsapana; verified against the `v1.0.0` GitHub tag | `assets/homevision/SEGMENTED_BUTTON_LICENSE.txt` (complete source license) |
| Pinned Section ListView | `de.halfbit:pinned-section-listview:1.0.0` | Apache-2.0, copyright 2013-2016 Sergej Shafarenka; project source and Maven metadata | `assets/homevision/PINNED_SECTION_LISTVIEW_NOTICE.txt`, `assets/homevision/APACHE_2_0_LICENSE.txt` |

Upstream evidence: [segmented-button v1.0.0 license](https://github.com/truefedex/segmented-button/blob/v1.0.0/LICENSE),
[pinned-section-listview source project](https://github.com/beworker/pinned-section-listview),
[Maven repository metadata](https://mvnrepository.com/artifact/de.halfbit/pinned-section-listview/1.0.0),
[Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0).

## Dependency families still requiring a full transitive review

- AndroidX (AppCompat, WebKit, ConstraintLayout, RecyclerView, Lifecycle, Room),
  Kotlin standard library, Kotlin Coroutines, and their runtime dependencies.
- Confirm exact resolved versions, all published license metadata, copyright/NOTICE
  requirements, and whether those notices must be reproduced in binary distribution.
- Build-only Gradle/KSP/Android Gradle Plugin packages must be tracked separately
  from libraries actually bundled into the APK.
- Audit any inherited bundled HTML, fonts, images, scripts, or upstream icons
  separately; replacing launcher/banner does not prove all assets are cleared.
- Before public distribution, produce a full resolved-component inventory with
  pinned versions and corresponding license texts; seek legal review as needed.

## Safeguards applied by CI

The script `scripts/homevision_ci_guard.py` checks the WebView flavor at source,
resolved-dependency-report and APK levels. Both CI workflows run it; the signed
release workflow additionally checks its release APK before the publish step.

- Confirms `com.homevision.tv`, semantic version metadata, the new PNG launcher and
  widescreen banner, removal of the old vectors, and removal of the noisy kiosk
  startup toast while preserving existing kiosk/nav behavior.
- Confirms historical Room migrations and tab column are retained so existing
  installations can be upgraded without a destructive data migration.
- Rejects Brave ad-block / GeckoView dependencies in the resolved WebView-only
  runtime graph and rejects any packaged native `.so` libraries in that flavor.
- Verifies that TV Bro attribution and the named third-party license/notice files
  are present and nonempty inside the built APK.
- Retains a build artifact containing the dependency report to facilitate ongoing
  manual licensing review.

**Limits:** These checks do not prove the absence of all unused classes, analyze
transitive licenses, ensure that every required notice was discovered, or replace
real-device regression testing. They also do not validate the optional Gecko flavor,
which is not intended for the user's Fire TV deployment. Do not treat a successful
CI run as authorization to publish a public release.

## Pre-public-release checklist

1. Verify About UI on Fire TV credits TV Bro and DataVision with working links.
2. Review *all* direct and transitive runtime licenses and NOTICE obligations.
3. Inspect the final signed APK, verify its signing certificate, package name,
   compiled version, app icon/banner, APK/native inventory, and bundled notices.
4. Validate in-place upgrades, startup, dashboard, Back/long-press gestures,
   cursor/spatial navigation, network recovery, and error paths on Fire OS 7/8.
5. Review release notes and source history for accurate upstream attribution.
6. Keep signed-release workflow manually triggered until all checks are completed.
