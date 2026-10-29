# C14.6 — HomeVision inherited visual asset provenance

**Base:** HomeVision commit `821affa25af2f7a8362d645ec8db34783ff57b6d`, version 1.0.4 (pre-release).

## Verified byte identities

Comparison of public GitHub repository trees establishes **23 current assets
identical at the Git blob level** to the original DataVision repository at
`6d4558d4945e2c3fde4015798cb686075f973922`:

| Group | Files | What is established |
|---|---:|---|
| Search-engine PNG favicons | 7 | Byte-identical to DataVision and TV Bro master |
| Homepage SVG assets (including warning icon) | 5 | 4 byte-identical to both DataVision and TV Bro; certificate-warning SVG matches DataVision |
| Android drawable nine-patch tab backgrounds | 10 | Byte-identical to DataVision; not independently compared to all historical TV Bro branches |
| `generic_injects.js` | 1 | Byte-identical to DataVision; modified relative to TV Bro master |

**This proves source provenance, not the legal right to redistribute every
individual asset.** The inherited TV Bro source license is retained verbatim,
but corporate/search-engine logos can be separately trademarked or copyrighted.
The SVG illustrations include editor metadata and do not establish separately
verifiable licensing; an origin in an open-source repository is insufficient
by itself to conclude that every third-party image is cleared.

`index.html` and `warning-certificate.html` are inherited and modified pages;
this audit does not claim byte identity for them. The 2 HomeVision branded PNGs
were produced for this fork and are not represented as upstream assets.

## Usage review

- `pages/home/index.html` references all seven `favicons/*.png` images in its
  search-engine chooser, plus `mic.svg`, `search.svg`, `more.svg`, and
  `ic_not_available.svg` in the homepage UI.
- `pages/warning-certificate.html` references `pages/ic_warning.svg` for its
  SSL warning view. Keep certificate warning functionality intact.
- `webtab_horizontal_bkg_selector.xml` references `@drawable/tab_patch`, so
  do not delete the nine-patch density variants without redesigning tab visuals.
- `generic_injects.js` contains blob download and media playback handlers;
  retain until independently refactored and tested.

## Safeguards

`scripts/homevision_asset_provenance.py source` compares each tracked resource
with its documented Git blob hash. `... apk <file.apk>` verifies packaged web
assets and the in-APK provenance notice; it **does not compare compiled Android
nine-patches byte-for-byte**, because Android's asset processor can transform
them. Existing APK/source guards separately enforce the absence of obsolete
launcher/banner images and the presence of HomeVision branding.

## Outstanding public release requirements

1. Confirm acceptable redistribution/usage of the six search-engine brand
   marks and the generic custom-search image. If provenance/permission remains
   unclear, replace them with generic, original icons or a text-only chooser,
   without removing search functionality.
2. Independently identify the SVG/9-patch creators or replace these assets with
   original or clearly licensed equivalents if needed.
3. Inspect `META-INF` and published AAR/JAR POM/NOTICE files for all actual
   resolved runtime components; the existing Gradle coordinate audit alone is
   not sufficient for an artifact-level legal clearance.
4. Verify TV Bro/DataVision attribution inside the Fire TV About UI, and
   ensure the product privacy notice/link matches actual HomeVision behavior.
5. Run in-place upgrade and regression testing on Fire OS before a signed
   public release. This change adds no runtime/visual behavior itself.

## Repositories compared

- https://github.com/truefedex/tv-bro
- https://github.com/ayumilove/DataVision
- https://github.com/The-Power-0/HomeVision

See the accompanying CSV for exact per-file Git blob identifiers and caveats.
