# The London Compute Ring

A public, open-source map of the physical footprint of AI and cloud infrastructure across Greater London and the M25 fringe: data centres, power, land, and water, with sourced figures assembled in one place.

**Site name (fixed):** The London Compute Ring  
**Sub-brand (PNG export / social only):** Capital Compute  
**Suggested domains:** londoncomputering.uk (GitHub Pages until secured)  
**Repo slug:** `ldn-compute`

## Stance

Disclosed, not neutral: make the physical and environmental cost of the regional compute build-out visible and comparable. Within that stance: every number sourced or null, claims shown as claims, no adjective advocacy. See [`/methodology`](./src/pages/methodology.astro).

## v0

1. Map homepage (MapLibre)
2. Site dossiers (seed → §3 verification; see `RESEARCH.md`)
3. `src/lib/units.ts` (capacity / load / energy discipline)
4. Methodology page
5. Compare view + PNG export
6. Sortable `/sites` table (crawlable spine)

## Develop

```bash
npm install
npm test
npm run validate:data
npm run dev
```

Base path for GitHub Pages: `/ldn-compute`.

## Data

- `data/sites.geojson` — FeatureCollection, coordinates **`[lng, lat]`**
- `data/schema.json` — JSON Schema (`$version` from day one)
- `data/local_consumption.json` — DESNZ LA electricity totals
- `data/config.json` — region + contacts (not London-hardcoded in code paths)
- `data/CHANGELOG.md` — corrections log

Contributions: GitHub Issue Forms and email `marco@prismaticlabs.ai` (subject: `London Compute Ring: correction`). Review queue only; nothing writes the data store from the public.

## Maintenance

Maintained by Prismatic Labs (`marco@prismaticlabs.ai`). Freshness is mostly event-driven (a site is updated when its status changes); the ~20 active planning cases are swept about monthly, and the wider map targets a review age within `staleness_banner_days` (90; see `data/config.json`), past which a site-wide staleness banner shows. Corrections and new sites come in via the review queue (`/contribute`, GitHub Issue Forms, email) and are logged in `data/CHANGELOG.md`. CI (`.github/workflows/ci.yml`) runs lint + tests + `validate:data` + build on every push and PR, so no change lands that breaks the schema or editorial rules.

## More from Prismatic Labs

[The Yorkshire Compute Belt](https://prismatic-labs.github.io/yorkshire-compute-belt/) · [Cloud Kettle Index](https://prismatic-labs.github.io/cloud-kettle-index/) · [CULM](https://prismatic-labs.github.io/culm/)

## License

Content and data: sources remain with their publishers; site code MIT (see `LICENSE` when added).
