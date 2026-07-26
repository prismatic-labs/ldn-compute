# Phase 0 research log

Public mirror: `/research` on the site.

§3 protocol status for seed sites on the map (Greater London and M25 fringe). Seed data in `data/sites.geojson` is **not** a complete regional census until checklist items below are closed and further sites are verified. The map now holds **81** dossiers spanning west, east, north, south and inner fringes; Slough alone is still under-sampled at hall level. Campus aggregates that overlap building pins are flagged `role: "aggregate"` and excluded from the regional total (Equinix Slough, Kao Harlow, Telehouse Docklands).

## Hard rule

Planning-milestone statuses (`in_planning`, `approved`) need a `planning_ref.url` that opens the live application or SoS decision page (not a search form). Factual states are evidenced instead by a resolving source URL: `operating` for halls in service, `decommissioned` for halls that operated and later closed.

## Site checklist

| Site | Portal ref | Live URL | Power | Notes |
|---|---|---|---|---|
| Manor Farm (Poyle) | `3366043` | [GOV.UK](https://www.gov.uk/government/publications/recovered-appeal-land-at-manor-farm-and-land-north-of-wraysbury-reservoir-poyle-road-slough-ref-3366043-10-june-2026) | 107 / 147 MW | `approved` |
| Yondr Slough campus | unknown | null | 100 MW | held at `proposed` |
| Pure DC Premier Park | unknown | null | 56 MW IT | held at `proposed` |
| Ada Docklands | `24/02660/REM` | null | 70 / 210 MW | held at `proposed` |
| Bidder Street | `24/00088/FUL` | [Newham](https://pa.newham.gov.uk/online-applications/applicationDetails.do?activeTab=summary&keyVal=S7B5SDJYHK500) | null | `in_planning` |
| Truman Grey Eagle | `PA/24/01450` | null | ~4 MW | held at `proposed` |
| Equinix Slough (LD4–LD10) | unknown | null | ~67 MW | operating campus; held at `proposed` |
| Equinix LD8 Harbour Exchange | unknown | null | null | location; held at `proposed` |
| Equinix LD9 Powergate | unknown | null | null | location; held at `proposed` |
| VIRTUS LONDON4 Slough | unknown | null | 27 MW IT | held at `proposed` |
| VIRTUS LONDON3 Slough | unknown | null | 7.2 MW IT | held at `proposed` |
| VIRTUS LONDON9 Slough | unknown | null | 24 MW IT | held at `proposed` |
| VIRTUS LONDON10 Slough | unknown | null | 6.6 MW IT | held at `proposed` |
| VIRTUS LONDON11 Slough | unknown | null | 13 MW IT | held at `proposed` |
| VIRTUS LONDON12 Slough | unknown | null | 21 MW IT | held at `proposed` |
| VIRTUS LONDON19 Slough | unknown | null | 32.5 MW | held at `proposed` |
| VIRTUS LONDON5 Stockley | unknown | null | 24 MW IT | held at `proposed` |
| VIRTUS LONDON6 Stockley | unknown | null | 16 MW IT | held at `proposed` |
| VIRTUS LONDON7 Stockley | unknown | null | 28 MW IT | held at `proposed` |
| VIRTUS LONDON8 Stockley | unknown | null | 18 MW IT | held at `proposed` |
| VIRTUS LONDON2 Hayes | unknown | null | 11.4 MW IT | held at `proposed` |
| VIRTUS LONDON1 Enfield | unknown | null | 4.2 MW IT | held at `proposed` |
| CyrusOne LON1 Slough | unknown | null | 8.72 MW IT | held at `proposed` |
| Iron Mountain LON-1 | unknown | null | 8.7 MW | held at `proposed` |
| Iron Mountain LON-2 | unknown | null | 27 MW | held at `proposed` |
| Iron Mountain LON-3 | unknown | null | 25 MW | in development; held at `proposed` |
| NTT London 1 Dagenham | unknown | null | 32 / 64 MW | held at `proposed` |
| NTT Slough 2 | unknown | null | 1.8 MW IT | held at `proposed` |
| Telehouse Docklands | unknown | null | ~40 MW campus | held at `proposed` |
| Telehouse North Two | unknown | null | ~73 MW | held at `proposed` |
| Telehouse West | unknown | null | ~18 MW | held at `proposed` |
| Telehouse West Two | unknown | null | 33 MW | groundbreaking 2025; held at `proposed` |
| Telehouse South | unknown | null | null | location; held at `proposed` |
| Global Switch London East | unknown | null | ~87 MW | held at `proposed` |
| Global Switch London North | unknown | null | ~18 MW | held at `proposed` |
| Vantage LHR1 PowerGate | unknown | null | 55 MW | held at `proposed` |
| Vantage LHR2 Park Royal | unknown | null | 20 MW | held at `proposed` |
| Serverfarm LON1 Feltham | unknown | null | ~11.4 MW IT | secondary MW; held at `proposed` |
| Digital Realty Slough | unknown | null | null | location seed; MW TBD |
| Digital Realty Docklands | unknown | null | null | location seed; MW TBD |

## Added 2026-07-20 (named metro projects previously missing)

- Google Waltham Cross (operational 2025), Equinix South Mimms (~250 MW), Digital Reef East Havering "London Data Freeport" (~600 MW), Colt DCS Hayes (~160 MW campus), Microsoft Park Royal (~£1bn, distinct from Pure/SEGRO Premier Park). All held at `proposed` pending lasting portal URLs; power `null` where the operator discloses none (Google, Microsoft).

## Not yet on the map

- Stack Infrastructure and EdgeConneX London campuses; Colt Welwyn Garden City (only Colt Hayes is mapped).
- Further Slough Trading Estate halls (remaining Equinix / Digital Realty buildings as separate pins).
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
