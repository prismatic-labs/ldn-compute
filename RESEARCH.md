# Phase 0 research log

Public mirror: `/research` on the site.

§3 protocol status for seed sites on the map (Greater London and M25 fringe). Seed data in `data/sites.geojson` is **not** a complete regional census until checklist items below are closed and further sites are verified. The map now holds **89** dossiers spanning west, east, north, south and inner fringes; Slough alone is still under-sampled at hall level. Campus aggregates that overlap building pins are flagged `role: "aggregate"` and excluded from the regional total **and from the map itself** — only their individual hall pins render, so the campus dossier exists as a data record and detail page but not as a marker (Equinix Slough, Kao Harlow, Telehouse Docklands).

## Hard rule

Planning-milestone statuses (`in_planning`, `approved`) need a `planning_ref.url` that opens the live application or SoS decision page (not a search form). Factual states are evidenced instead by a resolving source URL: `operating` for halls in service, `decommissioned` for halls that operated and later closed.

## Site checklist

`data/sites.geojson` is the source of truth for status. The earlier per-hall census listed operating colocation campuses as `proposed` pending a planning portal URL; that has been reconciled — under the hard rule an in-service hall is a **factual** state evidenced by a resolving operator/source URL, so the ~60 operating halls are `operating` (not planning-gated). The tables below track only the sites that are **not** plainly operating, plus outstanding URL/evidence debt.

### Planning-gated — `approved` / `in_planning` (need a resolving `planning_ref.url`)

| Site | Portal ref | Live URL | Power | Status |
|---|---|---|---|---|
| Manor Farm (Poyle) | `3366043` | [GOV.UK](https://www.gov.uk/government/publications/recovered-appeal-land-at-manor-farm-and-land-north-of-wraysbury-reservoir-poyle-road-slough-ref-3366043-10-june-2026) | ~72 MW IT (+100 MW BESS) | `approved` |
| Truman Grey Eagle | `PA/24/01450` | [GOV.UK](https://www.gov.uk/government/publications/recovered-appeal-sites-on-and-around-the-site-of-truman-brewery-tower-hamlets-london-refs-3367041-3367172-3367179-and-3367369-29-july-2026) | ~4–5.2 MW | `approved` — SoS allowed 29 Jul 2026 |
| Abbots Langley (Bedmond Rd) | `3346061` | [GOV.UK](https://www.gov.uk/government/publications/recovered-appeal-land-off-bedmond-road-abbots-langley-ref-3346061-12-may-2025) | ~96 MW IT | `approved` |
| CorScale Iver (Court Lane) | `3337981` | [GOV.UK](https://www.gov.uk/government/publications/recovered-appeal-court-lane-industrial-estate-court-lane-iver-ref-3337981-6-december-2024) | 140 MW | `approved` |
| Greystoke Woodlands Park (Iver) | `3347353` | [SoS decision](https://www.slough.gov.uk/downloads/file/5111/cd-7-01-appeal-decision-relating-to-woodlands-park-landfill-site-dated-9-july-2025-reference-3347353-) | ~90 MW | `approved` — under judicial review; Govt conceded, quash expected |
| Bidder Street | `24/00088/FUL` | [Newham](https://pa.newham.gov.uk/online-applications/applicationDetails.do?activeTab=summary&keyVal=S7B5SDJYHK500) | undisclosed | `in_planning` |
| Thurrock (Arena Essex) | `25/00573/OUT` | [Thurrock](https://regs.thurrock.gov.uk/online-applications/applicationDetails.do?activeTab=summary&keyVal=SW5PMMQGMBJ00) | undisclosed | `in_planning` |
| CyrusOne LON7 / Honey Monster (Southall) | `253874FUL` | [Ealing](https://pam.ealing.gov.uk/online-applications/applicationDetails.do?activeTab=summary&keyVal=T42GBOJM0KW00) | undisclosed | `in_planning` — committee resolved to grant 15 Jul 2026; portal shows "Pending Consideration" |

### Held at `proposed` — consented, no lasting portal URL

| Site | Portal ref | Power | operational_reality |
|---|---|---|---|
| Pure DC / SEGRO Premier Park | unknown | 56 MW IT | consented (OPDC committee approval Mar 2026) |
| CyrusOne LON6 (Iver Heath) | unknown | 90 MW | consented |
| SEGRO Iver (Thorney) | unknown | — | consented |
| Equinix South Mimms | unknown | ~250 MW | consented |
| Colt DCS Hayes | unknown | ~160 MW | consented |
| Global Switch London South | unknown | ~40 MW | consented |
| Equinix Wexham Rd (former AkzoNobel) | `P/00072/152` | undisclosed | consented (outline Nov 2025, s106 30 Jul 2026; Slough portal unreachable) |

### Held at `proposed` — building or pipeline

| Site | Power | operational_reality |
|---|---|---|
| Ada Docklands (`24/02660/REM`) | up to 210 MW | under_construction |
| Microsoft Park Royal | ~96 MW | under_construction |
| Iron Mountain LON-3 | 25 MW | under_construction |
| Telehouse West Two | 33 MW | under_construction |
| Equinix LD14 (Slough, Banbury Ave) | ~30 MW | under_construction (Slough BC approval May 2024; no lasting portal URL) |
| Kao KLON-03 (Harlow) | 17.6 MW | under_construction |
| Ark Elstree | ~200 MW | pipeline |
| Kao KLON-04 (Harlow) | 36 MW | pipeline |
| Digital Reef (East Havering) | up to 600 MW | pipeline |

Everything else on the map is `operating` (source-evidenced) — including the former "held at `proposed`" colocation halls (Yondr Slough, Equinix LD-series incl. LD11x, all VIRTUS London halls, CyrusOne LON1–5, Iron Mountain LON-1/2, NTT Dagenham/Slough/Hemel, Telehouse North/North Two/West/South/East, Global Switch East/North, Vantage LHR1/2, Serverfarm LON1, Digital Realty Slough/Docklands, Google Waltham Cross, Pure DC Brent Cross) — or `decommissioned` (Netwise London Central).

**Campus itemisation.** With Telehouse North added, the **Telehouse Docklands** aggregate is now fully decomposed into its halls (North, North Two, West, West Two, South, East); the **Equinix Slough** aggregate is likewise complete against the operator roster (LD4/5/6/7/10/11x/13x/14). Both are therefore retire-candidates — once dropped, the campus is represented purely by its hall pins (see the `role: "aggregate"` note above). Two open flags: Telehouse's public roster lists North/East/West/North Two/Central/West Two (not "South"), so the existing `telehouse-south` (Blackwall Yard) pin needs a source check; and **Telehouse Central** (2026 administration building) is deliberately not mapped as it is office/admin, not a data hall.

## Added 2026-07-20 (named metro projects previously missing)

- Google Waltham Cross (operational 2025), Equinix South Mimms (~250 MW), Digital Reef East Havering "London Data Freeport" (~600 MW), Colt DCS Hayes (~160 MW campus), Microsoft Park Royal (~£1bn, distinct from Pure/SEGRO Premier Park). Google Waltham Cross is now `operating`; the rest remain held at `proposed` pending lasting portal URLs (see the checklist above). Power `null` where the operator discloses none (Google, Microsoft).

## Coordinates verified 2026-07-26 (OSM / Nominatim geocoding pass)

Pin coordinates were re-derived from OpenStreetMap building footprints (Overpass) and Nominatim address geocoding, replacing hand-seeded placeholders that the exact-coordinate uniqueness rule had nudged up to ~3 km off their real position. Corrected clusters: Telehouse and Global Switch (Blackwall), the Slough Trading Estate cluster (Equinix LD4–LD10, VIRTUS London 3/4/9/10/11, CyrusOne LON1/LON3, Iron Mountain LON-1, NTT Slough, Digital Realty LHR26), Stockley VIRTUS (London 5–8), Kao Harlow (KLON-01/02/03), and the Digital Realty LGW/LHR halls; plus Google Waltham Cross, Vantage LHR2, Ada Docklands, Serverfarm LON1.

Still campus-approximate (placed adjacent to the verified operator campus; the individual building is not yet confirmed against a footprint): VIRTUS London 12 and London 19 (Slough), Iron Mountain LON-2 and LON-3, NTT Slough 3, and Equinix LD13x. Confirm these against operator site plans.

## Not yet on the map

- Stack Infrastructure and EdgeConneX London campuses; Colt Welwyn Garden City (only Colt Hayes is mapped).
- Further Slough Trading Estate halls (remaining Digital Realty buildings as separate pins; Equinix Slough is now fully itemised LD4/5/6/7/10/11x/13x/14).
- Decommissioned or closed halls (status `decommissioned` is ready in schema).
- Smaller rented server halls and city hosting rooms: inventory separately.
- Kao Harlow, Abbots Langley, and Pulsant Croydon are now mapped (removed from this list).

## Outstanding

1. Snapshot every cited URL to archive.org at ingestion.
2. Lasting Public Access URLs for operating campuses (then upgrade many from `proposed` to `operating`).
3. Page-level MW citations inside planning PDFs / operator datasheets (replace secondary Brightlio / directory figures where possible).
4. Verify coordinates against red-line drawings / campus site plans.
5. Confirm DESNZ local-authority electricity rows against the latest stacked CSV.
6. Thames Water per-capita figure: confirm against latest published number used in `units.ts`.
7. Itemise Digital Realty Slough and Docklands megawatts from operator disclosures.
8. Prefer operator-primary MW for Serverfarm LON1 (currently secondary).
