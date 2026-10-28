# Release notes

## HomeVision

For HomeVision-specific features and verified builds, see [README.md](README.md)
and [GitHub Actions](https://github.com/The-Power-0/HomeVision/actions).
HomeVision has not yet published its first production release. The version
numbers in the inherited DataVision notes below refer to **DataVision**, not
HomeVision, and do not describe the current WebView-only build.

## Historical upstream: DataVision 1.0.0 (English translation)

The immediate upstream [DataVision](https://github.com/ayumilove/DataVision)
originally adapted TV Bro into a dashboard kiosk application with:

- A different app name, launcher icon, and application ID (`im.xcode.datavision`).
- Fullscreen launch of a configured dashboard with browser chrome hidden; settings guidance if no URL is configured.
- Long-press Back or Menu to exit kiosk and open settings.
- Restoration of the last opened page on launch; updated dashboard URLs applied on a following launch.
- Network recovery with 5-second, 10-second, and 30-second retry intervals and immediate reload when connectivity returns.
- Optional interval-based page reload in minutes.
- A GeckoView 4K display-density override, to prevent oversized web content on TVs.
- An upstream automatic-update feature based on a GitHub release manifest.
- Ad-blocking exemptions for the configured dashboard host.
- Removal of original TV Bro branding and quick links from the internal home page.
- Additional localized text for kiosk-related settings.
- Release builds supporting ABI splits, with large GeckoView-based APKs.

These are **historical upstream notes only**. Current HomeVision uses Android
system WebView by default, has its own app identity, and disables its inherited
in-app automatic updater. Do not use these notes to guide HomeVision releases.

## Licensing and attribution

HomeVision derives from DataVision and TV Bro. Preserve [LICENSE.md](LICENSE.md),
follow the [attribution document](docs/HOMEVISION_ATTRIBUTION.md), and complete
the [third-party license review](docs/HOMEVISION_THIRD_PARTY_LICENSE_REVIEW.md)
before redistributing a production APK.
