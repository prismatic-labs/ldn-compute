#!/usr/bin/env python3
"""Seed high-priority missing campuses: Iver fringe, Gatwick/Crawley, more west halls."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "sites.geojson"
PUBLIC = ROOT / "public" / "data" / "sites.geojson"
NULL = {"id": None, "url": None}


def qty(value, source, unit="MW"):
    return {
        "value": value,
        "unit": unit,
        "basis": "stated",
        "source": source,
        "page": None,
        "archived": None,
    }


def power(*, it=None, it_src=None, max_mw=None, max_src=None, grid=None, grid_src=None):
    it_q = qty(it, it_src) if it is not None else None
    max_q = qty(max_mw, max_src) if max_mw is not None else (deepcopy(it_q) if it_q else None)
    return {
        "grid_connection_mw": qty(grid, grid_src) if grid is not None else None,
        "it_load_mw": it_q,
        "phase_1_mw": None,
        "max_proposed_mw": max_q,
    }


def empty_power():
    return {
        "grid_connection_mw": None,
        "it_load_mw": None,
        "phase_1_mw": None,
        "max_proposed_mw": None,
    }


def feat(
    *,
    id,
    name,
    operator,
    corridor,
    local_authority,
    lng,
    lat,
    summary,
    power_block,
    sources,
    status="proposed",
    planning_ref=None,
    timeline=None,
    previous_use,
    land_type="industrial_active",
    acres=None,
    acres_src=None,
    controversies=None,
):
    return {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [lng, lat]},
        "properties": {
            "id": id,
            "name": name,
            "operator": operator,
            "status": status,
            "local_authority": local_authority,
            "corridor": corridor,
            "summary": summary,
            "power": power_block,
            "land": {
                "acres": qty(acres, acres_src, "acres") if acres is not None else None,
                "previous_use": previous_use,
                "land_type": land_type,
                "alc_grades": None,
            },
            "timeline": timeline or [],
            "sources": sources,
            "planning_ref": planning_ref or deepcopy(NULL),
            "water_litres_pa": None,
            "grid_connection": None,
            "cooling": None,
            "claims_on_record": [],
            "operator_response": None,
            "controversies": controversies or [],
            "last_reviewed": "2026-07-20",
        },
    }


NEW = [
    feat(
        id="corscale-iver-court-lane",
        name="CorScale Iver (Court Lane)",
        operator="CorScale / Affinius Capital",
        corridor="west",
        local_authority="Buckinghamshire Council",
        lng=-0.505,
        lat=51.508,
        status="approved",
        planning_ref={
            "id": "3337981",
            "url": "https://www.gov.uk/government/publications/recovered-appeal-court-lane-industrial-estate-court-lane-iver-ref-3337981-6-december-2024",
        },
        summary=(
            "Hyperscale campus on Court Lane Industrial Estate, Iver (between Slough and Hayes on the M25 fringe). "
            "Outline consent for up to 65,000 m² GEA across two data centre buildings. SoS recovered appeal allowed "
            "6 December 2024. Decision materials cite a 140 MW grid connection reserved; trade reporting treats the campus as about 140 MW."
        ),
        power_block=power(
            it=140,
            it_src="SoS decision / DCD: 140 MW grid connection reserved for Court Lane Iver campus",
            max_mw=140,
            max_src="CorScale Court Lane Iver: about 140 MW (grid connection reserved)",
            grid=140,
            grid_src="SoS recovered appeal decision: 140 MW grid connection reserved",
        ),
        acres=14,
        acres_src="DCD / CorScale reporting: 14-acre Court Lane site",
        previous_use="Court Lane Industrial Estate (waste transfer, recycling, storage, offices); Grade II farmhouse retained",
        land_type="brownfield",
        timeline=[
            {
                "date": "2024-12-06",
                "event": "Secretary of State allows recovered appeal 3337981 (outline data centre)",
                "source": "https://www.gov.uk/government/publications/recovered-appeal-court-lane-industrial-estate-court-lane-iver-ref-3337981-6-december-2024",
            },
            {
                "date": "2026-07",
                "event": "Operator targets predevelopment works from July 2026; completion targeted late 2029",
                "source": "https://www.datacenterdynamics.com/en/news/corscale-targets-2029-launch-date-for-140mw-data-center-campus-outside-london-uk/",
            },
        ],
        controversies=[
            {
                "summary": "Buckinghamshire refused as inappropriate Green Belt development; overturned at recovered appeal",
                "source": "https://www.datacenterdynamics.com/en/news/angela-rayner-overrules-council-and-approves-data-center-planned-for-buckinghamshire-uk/",
                "label": "procedural",
            }
        ],
        sources=[
            {
                "label": "GOV.UK: recovered appeal 3337981",
                "url": "https://www.gov.uk/government/publications/recovered-appeal-court-lane-industrial-estate-court-lane-iver-ref-3337981-6-december-2024",
                "archived": None,
            },
            {
                "label": "DCD: CorScale 140 MW Iver",
                "url": "https://www.datacenterdynamics.com/en/news/corscale-targets-2029-launch-date-for-140mw-data-center-campus-outside-london-uk/",
                "archived": None,
            },
        ],
    ),
    feat(
        id="cyrusone-lon6-iver-heath",
        name="CyrusOne LON6 (Iver Heath)",
        operator="CyrusOne",
        corridor="west",
        local_authority="Buckinghamshire Council",
        lng=-0.52,
        lat=51.54,
        summary=(
            "CyrusOne LON6 at Seven Hills Road, Iver Heath. Operator states 90 MW of IT capacity across ten 9 MW data halls "
            "(30,000 m²) and 160 MVA power capacity via 132 kV feeds. Held at proposed until a lasting Buckinghamshire "
            "Public Access URL for the live consent is linked."
        ),
        power_block=power(
            it=90,
            it_src="CyrusOne LON6 page: 90 MW Total Megawatts IT Capacity",
            max_mw=90,
            max_src="CyrusOne LON6: 90 MW IT capacity",
            grid=160,
            grid_src="CyrusOne LON6 page: 160 MVA power capacity via 132 kV feeds (recorded as 160 MW stated)",
        ),
        previous_use="Iver Heath industrial / countryside fringe plot",
        sources=[
            {
                "label": "CyrusOne: LON6 Iver Heath",
                "url": "https://www.cyrusone.com/data-centers/emea/london-uk-lon6",
                "archived": None,
            }
        ],
    ),
    feat(
        id="segro-iver-thorney",
        name="SEGRO Iver (Thorney Business Park)",
        operator="SEGRO",
        corridor="west",
        local_authority="Buckinghamshire Council",
        lng=-0.50,
        lat=51.512,
        summary=(
            "SEGRO data centre campus at Thorney Business Park / Thorney Lane, Iver (M25 fringe between Slough and Hayes). "
            "Planning materials describe a hybrid multi-building campus (DC1 in detail plus further outline floorspace). "
            "Committee / press report planning permission for a three-building campus. Campus megawatts not yet pinned to a "
            "single operator MW line here. Held at proposed until lasting portal URL and stated MW are linked."
        ),
        power_block=empty_power(),
        acres=19.5,
        acres_src="SEGRO planning statement: about 7.9 ha data centre redevelopment within ~18.3 ha red line (about 19.5 acres for DC plot)",
        previous_use="Thorney Business Park industrial / former gravel workings",
        land_type="brownfield",
        sources=[
            {
                "label": "DCD: SEGRO Iver planning go-ahead",
                "url": "https://www.datacenterdynamics.com/en/news/segro-gets-green-light-for-three-data-centers-in-slough-uk/",
                "archived": None,
            }
        ],
    ),
    feat(
        id="digital-realty-lgw15-crawley",
        name="Digital Realty LGW15 (Crawley Unit 1)",
        operator="Digital Realty",
        corridor="south",
        local_authority="Crawley Borough Council",
        lng=-0.178,
        lat=51.138,
        summary=(
            "Digital Realty Crawley Unit 1 (LGW15) on the Manor Royal estate, between Crawley and Gatwick — the main "
            "scale colo campus on the south M23 fringe. Directory listings cite about 18 MW. Campus has a large 132 kV / "
            "72 MVA power position shared with Unit 2. Held at proposed until a lasting portal URL is linked."
        ),
        power_block=power(
            it=18,
            it_src="Directory listing for Digital Realty LGW15 Crawley Unit 1: about 18 MW",
            max_mw=18,
            max_src="Digital Realty LGW15: about 18 MW (directory)",
        ),
        previous_use="Manor Royal industrial / business park",
        sources=[
            {
                "label": "OCOLO: Digital Realty LGW15",
                "url": "https://www.ocolo.io/colocation/digital-realty/london-lgw15-crawley-unit-1/",
                "archived": None,
            },
            {
                "label": "Digital Realty: LGW16 campus context (72 MVA)",
                "url": "https://www.digitalrealty.co.uk/data-centers/emea/london/lgw16",
                "archived": None,
            },
        ],
    ),
    feat(
        id="digital-realty-lgw16-crawley",
        name="Digital Realty LGW16 (Crawley Unit 2)",
        operator="Digital Realty",
        corridor="south",
        local_authority="Crawley Borough Council",
        lng=-0.172,
        lat=51.136,
        summary=(
            "Digital Realty Crawley Unit 2 (LGW16) on Connect Way, Manor Royal. Colo-X states 12 MW IT load across four halls; "
            "some directories cite about 16 MW total power. Part of the Gatwick Diamond / south London metro campus with "
            "72 MVA campus power availability. Held at proposed until a lasting portal URL is linked."
        ),
        power_block=power(
            it=12,
            it_src="Colo-X: Digital Realty Crawley Unit 2 — 12 MW of IT load",
            max_mw=12,
            max_src="Digital Realty LGW16: 12 MW IT (Colo-X)",
        ),
        previous_use="Manor Royal industrial / business park",
        sources=[
            {
                "label": "Colo-X: Digital Realty Crawley Unit 2",
                "url": "https://www.colo-x.com/data-centre/digital-realty-crawley-unit2-data-centre/",
                "archived": None,
            },
            {
                "label": "Digital Realty: LGW16",
                "url": "https://www.digitalrealty.co.uk/data-centers/emea/london/lgw16",
                "archived": None,
            },
        ],
    ),
    feat(
        id="equinix-ld4-slough",
        name="Equinix LD4 (Slough)",
        operator="Equinix",
        corridor="west",
        local_authority="Slough Borough Council",
        lng=-0.596,
        lat=51.5235,
        summary=(
            "Equinix LD4 IBX on Buckingham Avenue, Slough Trading Estate — the original core of the Slough interconnection campus. "
            "Trade directories commonly assign about 16 MW IT to LD4 within the wider LD4–LD10 cluster. "
            "Held at proposed until a lasting Slough Public Access URL is linked."
        ),
        power_block=power(
            it=16,
            it_src="Secondary trade / directory reporting of Equinix LD4 IT power (about 16 MW)",
            max_mw=16,
            max_src="Equinix LD4: about 16 MW IT (secondary)",
        ),
        previous_use="Slough Trading Estate industrial plot",
        sources=[
            {
                "label": "Colo-X: Equinix LD4",
                "url": "https://www.colo-x.com/data-centre/equinix-ld4-slough/",
                "archived": None,
            }
        ],
    ),
    feat(
        id="equinix-ld5-slough",
        name="Equinix LD5 (Slough)",
        operator="Equinix",
        corridor="west",
        local_authority="Slough Borough Council",
        lng=-0.593,
        lat=51.5245,
        summary=(
            "Equinix LD5 IBX on Buckingham Avenue, Slough Trading Estate. Trade directories commonly assign about 25 MW IT to LD5. "
            "Held at proposed until a lasting Slough Public Access URL is linked."
        ),
        power_block=power(
            it=25,
            it_src="Secondary trade / directory reporting of Equinix LD5 IT power (about 25 MW)",
            max_mw=25,
            max_src="Equinix LD5: about 25 MW IT (secondary)",
        ),
        previous_use="Slough Trading Estate industrial plot",
        sources=[
            {
                "label": "Colo-X: Equinix LD5",
                "url": "https://www.colo-x.com/data-centre/equinix-ld5-slough/",
                "archived": None,
            }
        ],
    ),
    feat(
        id="equinix-ld6-slough",
        name="Equinix LD6 (Slough)",
        operator="Equinix",
        corridor="west",
        local_authority="Slough Borough Council",
        lng=-0.5975,
        lat=51.522,
        summary=(
            "Equinix LD6 IBX on the Slough Trading Estate opposite LD4. Trade directories commonly assign about 16 MW IT to LD6. "
            "Held at proposed until a lasting Slough Public Access URL is linked."
        ),
        power_block=power(
            it=16,
            it_src="Secondary trade / directory reporting of Equinix LD6 IT power (about 16 MW)",
            max_mw=16,
            max_src="Equinix LD6: about 16 MW IT (secondary)",
        ),
        previous_use="Slough Trading Estate industrial plot",
        sources=[
            {
                "label": "Equinix: LD6",
                "url": "https://www.equinix.com/data-centers/europe-colocation/united-kingdom-colocation/london-data-centers/ld6",
                "archived": None,
            }
        ],
    ),
    feat(
        id="gtr-slough-gb-one",
        name="GTR GB One (Slough)",
        operator="Global Technical Realty",
        corridor="west",
        local_authority="Slough Borough Council",
        lng=-0.619,
        lat=51.518,
        summary=(
            "Global Technical Realty GB One campus in Slough. Operator states a 40.5 MW campus across three independent "
            "buildings (13.5 MW IT load each). Held at proposed until a lasting portal URL is linked."
        ),
        power_block=power(
            it=40.5,
            it_src="GTR London GB One page: 40.5 MW campus (3 × 13.5 MW IT load)",
            max_mw=40.5,
            max_src="GTR GB One: 40.5 MW campus IT load",
        ),
        previous_use="Slough Trading Estate industrial plot",
        sources=[
            {
                "label": "GTR: London GB One",
                "url": "https://globaltechnicalrealty.com/locations/london-gb-one/",
                "archived": None,
            }
        ],
    ),
    feat(
        id="digital-realty-hanbury-street",
        name="Digital Realty LON1 (Hanbury Street)",
        operator="Digital Realty",
        corridor="inner",
        local_authority="London Borough of Tower Hamlets",
        lng=-0.07,
        lat=51.519,
        summary=(
            "Digital Realty LON1 at 11 Hanbury Street, Spitalfields — part of the London City Campus with Oliver's Yard. "
            "Operator publishes building size (about 5,400 m²) but not a single public megawatt total on the LON1 page. "
            "Location pin near Brick Lane / Truman. Held at proposed."
        ),
        power_block=empty_power(),
        previous_use="East London / Spitalfields commercial building",
        sources=[
            {
                "label": "Digital Realty: LON1 Hanbury Street",
                "url": "https://www.digitalrealty.co.uk/data-centers/emea/london/lon1",
                "archived": None,
            }
        ],
    ),
]


def main():
    data = json.loads(DATA.read_text())
    existing = {f["properties"]["id"] for f in data["features"]}
    added = []
    for f in NEW:
        if f["properties"]["id"] in existing:
            continue
        data["features"].append(f)
        added.append(f["properties"]["id"])
    text = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    DATA.write_text(text)
    PUBLIC.write_text(text)
    print(f"total={len(data['features'])} added={len(added)} {added}")


if __name__ == "__main__":
    main()
