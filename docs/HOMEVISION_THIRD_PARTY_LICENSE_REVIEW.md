# HomeVision third-party license review checklist

This checklist is part of the pre-release gate. HomeVision has modified DataVision's dependency graph and does not ship GeckoView in the WebView-only flavor, but the fork still includes AndroidX, Kotlin, Kotlin Coroutines, Room, and other components. Review both **direct and transitive** dependencies and all bundled assets before publishing an APK.

Reviewed source: upstream `gradle/libs.versions.toml` (as inspected October 27, 2026):

| Declared dependency | Audit action |
|---|---|
| AndroidX AppCompat / WebKit / ConstraintLayout / RecyclerView / Lifecycle / Room | Verify actual published AAR license notices, typically Apache-2.0; preserve any NOTICE files where required |
| Kotlin stdlib and Coroutines | Verify Kotlin/JetBrains notices and any transitive licenses |
| `com.github.truefedex:segmented-button` | Inspect the exact GitHub tag and license; don't assume TV Bro's special license automatically covers separate libraries |
| Brave-derived ad-block (removed from source in 1.0.3) | Verify resolved runtime dependencies and APK contain no ad-block AAR or native libraries; preserve historical database migrations for compatibility |
| `de.halfbit:pinned-section-listview` | Verify license, copyright and any required acknowledgment |
| Gradle plugins/KSP/Android Gradle Plugin | Distinguish build-time tools from bundled runtime material; still preserve license info when distributing build scripts |
| GeckoView | Not intended to be packaged in genericGeckoExcluded; validate APK contents/build variant |
| Original DataVision icons, images and webpages | HomeVision replaces launcher icon/banner; audit other bundled assets for attribution/trademark obligations |

**Required manual verification before public release:**

1. Open the app's About section on an actual Fire TV and verify visible "Based on TV Bro sources" and a working link to https://github.com/truefedex/tv-bro; don't remove inherited attribution.
2. Keep `LICENSE.md` from upstream unchanged and bundle it as `assets/homevision/TV_BRO_LICENSE.md` inside the APK.
3. Keep HomeVision's separate `HOMEVISION_ATTRIBUTION.md` crediting both TV Bro and DataVision.
4. Run Gradle dependency reporting for the WebView flavor and review upstream dependency repositories and their release licenses. Do not publish until the licenses of directly included libraries and bundled content are verified.
5. Inspect the signed APK's asset and native library inventory, not just its source. Ensure GeckoView native libraries and original launcher imagery aren't being used.
6. The application ID and display name must be different from TV Bro's; logo and banner must be new.

This is a legal audit checklist, not legal advice or a guarantee that all third-party licenses have been identified. Update it each time dependencies change.
