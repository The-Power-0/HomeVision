# HomeVision privacy information (pre-release)

**Document updated:** October 28, 2026

HomeVision is an independent Android TV / Fire TV dashboard-browser fork derived from
[DataVision](https://github.com/ayumilove/DataVision) and
[TV Bro](https://github.com/truefedex/tv-bro).
This document replaces an inherited upstream privacy description. Before public
redistribution, the app's code, dependencies, and actual network behavior must be
reviewed to confirm all statements in the final privacy notice.

## On-device information

HomeVision supports locally stored browser and kiosk configuration, including the
dashboard URL, reload preferences, browsing history used for page restoration,
cookies, and web-storage/cache data. These can reveal sensitive information about
the dashboards viewed. Anyone with access to an unlocked device or its debugging
interface may be able to inspect local data.

The project does not intentionally add a HomeVision-operated analytics or crash
reporting service. **This is not a verified guarantee that the application or its
third-party components make no other requests or collect no data.** Review all
runtime dependencies and app network behavior before treating that as a published
privacy assurance.

## Websites and network traffic

The app connects to the dashboard URLs and other sites that users configure or
visit. Sites, authentication providers, loaded content, network providers, and
intermediate infrastructure may process requests, cookies, IP addresses, and
other usage information according to their own terms and privacy practices.
The Home Assistant dashboard used during development is **not bundled** with
HomeVision; its operator controls that server's data handling.

## Private browsing

The inherited private/incognito browsing mode uses a separate browsing context.
Private browsing does not make network traffic anonymous and does not prevent
visited websites or networks from observing activity. Do not rely on it as a
security boundary without further technical validation.

## Children and sensitive content

HomeVision is designed to display configured dashboards on television devices;
it is not specifically intended for children. The person administering the
screen should control access to the dashboards and any sensitive information
displayed or stored.

## Changes and questions

Updates to this document should be reflected in the repository before public
releases. For issues with this fork, use the
[HomeVision issue tracker](https://github.com/The-Power-0/HomeVision/issues).
The upstream sources remain credited in [LICENSE.md](LICENSE.md) and
[the attribution notice](docs/HOMEVISION_ATTRIBUTION.md).

*This pre-release notice is provided for transparency and is not legal advice.*
