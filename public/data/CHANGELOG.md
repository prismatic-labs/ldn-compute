## 2026-08-07 — Tier-1 stress-test patch (86 dossiers)

- **Truman Grey Eagle** `proposed` → `approved`: Secretary of State allowed the recovered Truman Brewery appeals on 29 July 2026 (incl. Grey Eagle Street B8 data centre PA/24/01450); linked the GOV.UK decision page.
- Added **Greystoke Woodlands Park (Iver)** `approved` — SoS allowed appeal 3347353 on 9 July 2025 (up to 72,000 m² / ~90 MW); flagged the live judicial review the Government has conceded (“serious logical error”, permission expected to be quashed). Distinct from CyrusOne LON6 at Seven Hills Road.
- Added **Pure DC Brent Cross (LON01)** `operating` — ~90 MW campus; Building 1 (~20 MW) live since 2024 and fully leased, Building 2 (~70 MW) under construction. Distinct from Pure/SEGRO Premier Park (LON02).
- Added **CyrusOne LON7 / Honey Monster (Southall)** `in_planning` — Ealing committee resolved to grant 15 Jul 2026 (ref 253874FUL); the live Ealing Public Access page still shows "Pending Consideration" (no decision notice), so mapped `in_planning` against that resolving URL, not `approved`.
- Added **Equinix Wexham Road (former AkzoNobel)** — Slough outline P/00072/152 with s106 completed 30 Jul 2026; held at `status: proposed` / `operational_reality: consented` per the hard rule (Slough's Public Access portal is currently unreachable, no resolving URL).
- New-pin coordinates geocoded from OSM/Nominatim (Southall UB2 4AE, Wexham Road, Priestley Way/Brent Cross, Slough Road/Iver); confirm against building footprints in a later pass. Source snapshots to archive.org still pending (Wayback rate-limited at time of writing).

## 2026-07-20 — Reach 75

- Added 15 halls: CyrusOne LON2–LON5, VIRTUS LONDON14, Equinix LD7/LD10/LD13x, Telehouse East, NTT Slough 3 (2.7 MW), Kao KLON-01–04 as separate pins, Digital Realty LGW14 Woking.
- Map total **75** dossiers. Campus aggregate pins (Equinix Slough, Kao Harlow) still sit alongside building pins — compare may double-count until aggregates are retired.

## 2026-07-20 — Important-campus wave (60 sites)

- Added CorScale Court Lane Iver (`approved`, 140 MW, SoS 3337981), CyrusOne LON6 Iver Heath (90 MW), SEGRO Thorney Iver (location), Digital Realty LGW15/LGW16 Crawley (Gatwick fringe), Equinix LD4/LD5/LD6 as separate Slough pins, GTR GB One (40.5 MW), Digital Realty LON1 Hanbury Street.
- Coordinate box widened south for Crawley / Gatwick. Note: Equinix campus aggregate pin still present alongside LD4–LD6 (compare totals may double-count until campus pin is retired).

## 2026-07-20 — Orbital fringe + Silicon Roundabout

- Added north/south/east-fringe dossiers: Abbots Langley (SoS `approved`), NTT Hemel HH1–HH4, Kao Harlow, Ark Elstree, Pulsant Croydon, Thurrock Arena Essex (`in_planning`), Digital Realty Oliver’s Yard (Old Street).
- Re-homed VIRTUS Enfield to `north`. Corridor labels are compass fringes (M25 is the whole ring, not “north only”).
- Cluster click no longer caps below the cluster ceiling (Docklands “5” can split); Telehouse pins slightly spread.

## 2026-07-20 — Density pass (40 sites + clustering)

- Map now clusters nearby markers when zoomed out (MapLibre); click or zoom in to split. Scale legend notes numbered clusters.
- Seed count raised to **40** dossiers: Iron Mountain LON-1/2/3; VIRTUS L3/L9/L10/L11/L12/L19 Slough, L2 Hayes, L1 Enfield, L6/L7/L8 Stockley; NTT Slough 2; Equinix LD8 & LD9; Telehouse West / West Two / South; Serverfarm LON1 Feltham; Digital Realty Docklands location seed.
- East Zoom frame extended north for Enfield. Still under-samples Slough’s full facility count; many campuses remain `proposed` pending lasting portal URLs.

## 2026-07-20 — Operating-campus wave

- Added campus dossiers for Equinix Slough (LD4–LD10), VIRTUS LONDON4 & LONDON5, CyrusOne LON1, NTT London 1 Dagenham, Telehouse Docklands + North Two, Global Switch London East & North, Vantage LHR1 & LHR2, Digital Realty Slough (location; MW TBD).
- All new operating campuses held at `proposed` until lasting planning portal URLs exist (same hard rule as Yondr / Pure).
- East corridor zoom bounds widened to include Dagenham.

## 2026-07-20 — Phase 0 bootstrap

- Forked from Yorkshire Compute Belt as **The London Compute Ring** (sub-brand **Capital Compute**).
- Geography: Greater London and M25 fringe; corridors `west` | `east` | `inner` with Display + Zoom controls.
- Status enum adds `decommissioned` (closed after operating); colour in map/compare legends.
- Seed dossiers: Manor Farm (SoS `approved`), Yondr Slough campus, Pure Premier Park, Ada Docklands, Bidder Street (`in_planning`), Truman Grey Eagle.
- Local-consumption table retargeted to London boroughs + Slough (DESNZ 2024 rows; verify against stacked CSV).
