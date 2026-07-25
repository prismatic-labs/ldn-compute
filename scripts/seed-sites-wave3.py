#!/usr/bin/env python3
"""Seed outer-ring + Silicon Roundabout sites; re-home Enfield to north."""

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
        id="abbots-langley-bedmond",
        name="Abbots Langley data centre (Bedmond Road)",
        operator="Greystoke Land",
        corridor="north",
        local_authority="Three Rivers District Council",
        lng=-0.414,
        lat=51.706,
        status="approved",
        planning_ref={
            "id": "3346061",
            "url": "https://www.gov.uk/government/publications/recovered-appeal-land-off-bedmond-road-abbots-langley-ref-3346061-12-may-2025",
        },
        summary=(
            "Hyperscale campus of up to 84,000 m² across two buildings off Bedmond Road, Abbots Langley, plus a country park. "
            "Coverage puts IT load at about 96 MW. Secretary of State recovered appeal allowed 12 May 2025."
        ),
        power_block=power(
            it=96,
            it_src="DCD / decision coverage: about 96 MW IT load for Bedmond Road campus",
            max_mw=96,
            max_src="Abbots Langley: about 96 MW IT load",
        ),
        acres=81.5,
        acres_src="Appeal materials: about 33 ha development site (about 81.5 acres)",
        land_type="agricultural",
        previous_use="Green Belt / grey-belt land off Bedmond Road",
        timeline=[
            {
                "date": "2025-05-12",
                "event": "Secretary of State allows recovered appeal 3346061",
                "source": "https://www.gov.uk/government/publications/recovered-appeal-land-off-bedmond-road-abbots-langley-ref-3346061-12-may-2025",
            }
        ],
        sources=[
            {
                "label": "GOV.UK: recovered appeal 3346061",
                "url": "https://www.gov.uk/government/publications/recovered-appeal-land-off-bedmond-road-abbots-langley-ref-3346061-12-may-2025",
                "archived": None,
            }
        ],
        controversies=[
            {
                "summary": "Three Rivers refused; Green Belt / grey-belt dispute at recovered appeal",
                "source": "https://www.gov.uk/government/publications/recovered-appeal-land-off-bedmond-road-abbots-langley-ref-3346061-12-may-2025",
                "label": "procedural",
            }
        ],
    ),
    feat(
        id="ntt-hemel-hh1",
        name="NTT Hemel Hempstead 1 (HH1)",
        operator="NTT Global Data Centers",
        corridor="north",
        local_authority="Dacorum Borough Council",
        lng=-0.4345,
        lat=51.7642,
        summary=(
            "NTT Hemel Hempstead 1 at Boundary Way / Centro. About 2 MW of IT load. North M25 cluster marketed into the London metro. "
            "Held at proposed until a lasting portal URL is linked."
        ),
        power_block=power(it=2, it_src="NTT / PeeringDB HH1: about 2 MW IT load", max_mw=2, max_src="NTT HH1: 2 MW"),
        previous_use="Maylands industrial / business park",
        sources=[{"label": "PeeringDB: NTT Hemel HH1", "url": "https://www.peeringdb.com/fac/9031", "archived": None}],
    ),
    feat(
        id="ntt-hemel-hh2",
        name="NTT Hemel Hempstead 2 (HH2)",
        operator="NTT Global Data Centers",
        corridor="north",
        local_authority="Dacorum Borough Council",
        lng=-0.4421,
        lat=51.765,
        summary=(
            "NTT Hemel Hempstead 2 on Maylands Avenue. Secondary sources put maximum client IT load around 6.2 MW. "
            "Held at proposed until a lasting portal URL is linked."
        ),
        power_block=power(
            it=6.2,
            it_src="Secondary reporting of NTT Hemel HH2 maximum client IT load (about 6.2 MW)",
            max_mw=6.2,
            max_src="NTT HH2: about 6.2 MW IT (secondary)",
        ),
        previous_use="Maylands industrial / business park",
        sources=[{"label": "PeeringDB: NTT Hemel HH2", "url": "https://www.peeringdb.com/fac/9032", "archived": None}],
    ),
    feat(
        id="ntt-hemel-hh3",
        name="NTT Hemel Hempstead 3 (HH3)",
        operator="NTT Global Data Centers",
        corridor="north",
        local_authority="Dacorum Borough Council",
        lng=-0.4367,
        lat=51.7619,
        summary=(
            "NTT Hemel Hempstead 3. Operator states a maximum of 20 MW of IT load. "
            "Held at proposed until a lasting portal URL is linked."
        ),
        power_block=power(
            it=20,
            it_src="NTT Hemel Hempstead 3 page: maximum of 20 MW of IT load",
            max_mw=20,
            max_src="NTT HH3: 20 MW IT load",
        ),
        previous_use="Maylands industrial / business park",
        sources=[
            {
                "label": "NTT: Hemel Hempstead 3",
                "url": "https://services.global.ntt/en-us/services-and-products/global-data-centers/global-locations/emea/hemel-hempstead-3-data-center",
                "archived": None,
            }
        ],
    ),
    feat(
        id="ntt-hemel-hh4",
        name="NTT Hemel Hempstead 4 (HH4)",
        operator="NTT Global Data Centers",
        corridor="north",
        local_authority="Dacorum Borough Council",
        lng=-0.43,
        lat=51.755,
        summary=(
            "NTT Hemel Hempstead 4 at Blossom Way. Operator states a maximum of 12 MW IT load; on-site substation 60 MVA. "
            "Held at proposed until a lasting portal URL is linked."
        ),
        power_block=power(
            it=12,
            it_src="NTT Hemel Hempstead 4 page: maximum of 12 MW IT load",
            max_mw=12,
            max_src="NTT HH4: 12 MW IT load",
            grid=60,
            grid_src="NTT HH4: on-site substation delivering 60 MVA (recorded as 60 MW stated)",
        ),
        previous_use="Maylands / Blossom Way industrial setting",
        sources=[
            {
                "label": "NTT: Hemel Hempstead 4",
                "url": "https://services.global.ntt/en-us/services-and-products/global-data-centers/global-locations/emea/hemel-hempstead-4-data-center",
                "archived": None,
            }
        ],
    ),
    feat(
        id="kao-harlow-campus",
        name="Kao Data Harlow campus",
        operator="Kao Data",
        corridor="north",
        local_authority="Harlow District Council",
        lng=0.126,
        lat=51.777,
        summary=(
            "Kao Data campus on London Road, Harlow (M11 corridor). Operator: KLON-01/02 at 8.8 MW each (operational), "
            "KLON-03 17.6 MW under development, KLON-04 36 MW planned; about 71 MW ITE when complete. "
            "Held at proposed until lasting Harlow portal URLs are linked."
        ),
        power_block=power(
            it=17.6,
            it_src="Kao Data Harlow: KLON-01+02 operational 8.8 MW each (17.6 MW)",
            max_mw=71,
            max_src="Kao Data Harlow: about 71 MW ITE load across four buildings when complete",
        ),
        acres=15,
        acres_src="Kao Data Harlow page: 15-acre campus",
        previous_use="Harlow industrial / former research campus setting",
        sources=[{"label": "Kao Data: Harlow", "url": "https://kaodata.com/locations/harlow/", "archived": None}],
    ),
    feat(
        id="ark-elstree-watford",
        name="Ark Elstree campus (former Mercure Hotel)",
        operator="Ark Data Centres",
        corridor="north",
        local_authority="Hertsmere Borough Council",
        lng=-0.33,
        lat=51.655,
        summary=(
            "Proposed redevelopment of the former Mercure Hotel / Hilfield Park site near Watford–Elstree. "
            "Operator cites 250 MVA from 2028; trade reporting about 200 MW campus. "
            "Held at proposed until a lasting Hertsmere Public Access URL is linked."
        ),
        power_block=power(
            it=200,
            it_src="DCD / trade reporting: about 200 MW Ark Elstree / Watford campus",
            max_mw=200,
            max_src="Ark Elstree: about 200 MW (trade reporting)",
            grid=250,
            grid_src="Ark Elstree page: 250 MVA delivered from 2028 (recorded as 250 MW stated)",
        ),
        previous_use="Former Mercure Hotel / Hilfield Park",
        land_type="brownfield",
        sources=[
            {"label": "Ark: Elstree", "url": "https://www.ark-d-c.com/locations/elstree", "archived": None},
            {
                "label": "DCD: 200 MW Watford campus",
                "url": "https://www.datacenterdynamics.com/en/news/ark-plans-200mw-data-center-campus-in-watford-uk/",
                "archived": None,
            },
        ],
    ),
    feat(
        id="pulsant-croydon-ln1",
        name="Pulsant Croydon LN-1",
        operator="Pulsant",
        corridor="south",
        local_authority="London Borough of Croydon",
        lng=-0.125,
        lat=51.365,
        summary=(
            "Pulsant regional edge hall at Imperial Way, Croydon. Operator datasheet: 1.35 MW IT power, 2.5 MW incoming. "
            "Held at proposed until a lasting Croydon Public Access URL is linked."
        ),
        power_block=power(
            it=1.35,
            it_src="Pulsant Croydon LN-1 datasheet: Total IT Power 1.35 MW",
            max_mw=1.35,
            max_src="Pulsant Croydon LN-1: 1.35 MW IT",
            grid=2.5,
            grid_src="Pulsant Croydon LN-1 datasheet: Total Incoming Power 2.5 MW",
        ),
        previous_use="Imperial Way industrial estate, Croydon",
        sources=[
            {
                "label": "Pulsant: Croydon LN-1",
                "url": "https://www.pulsant.com/colocation-south-london-datacentre",
                "archived": None,
            }
        ],
    ),
    feat(
        id="thurrock-arena-essex",
        name="Thurrock data centre (Arena Essex)",
        operator="Global Infrastructure UK / Google (reported end user)",
        corridor="east",
        local_authority="Thurrock Council",
        lng=0.28,
        lat=51.49,
        status="in_planning",
        planning_ref={
            "id": "25/00573/OUT",
            "url": "https://regs.thurrock.gov.uk/online-applications/applicationDetails.do?activeTab=summary&keyVal=SW5PMMQGMBJ00",
        },
        summary=(
            "Hybrid application for a hyperscale campus on the former Arena Essex raceway site, Purfleet / West Thurrock "
            "(about 52 ha). Up to four data centre buildings (up to 130,500 m² GEA). Press identifies Google as intended operator. "
            "Hall megawatts not yet itemised from a single clear MW line. Live Thurrock portal."
        ),
        power_block=empty_power(),
        acres=128,
        acres_src="Planning / press: about 52 hectares (about 128 acres)",
        land_type="brownfield",
        previous_use="Former Arena Essex motorsport / speedway and fishing lake",
        controversies=[
            {
                "summary": "Large local interest; carbon / AI footprint coverage of the hyperscale proposal",
                "source": "https://www.theguardian.com/technology/2025/sep/15/google-datacentre-kent-co2-thurrock-uk-ai",
                "label": "campaign",
            }
        ],
        sources=[
            {
                "label": "Thurrock Public Access: 25/00573/OUT",
                "url": "https://regs.thurrock.gov.uk/online-applications/applicationDetails.do?activeTab=summary&keyVal=SW5PMMQGMBJ00",
                "archived": None,
            },
            {
                "label": "Guardian: Thurrock hyperscale",
                "url": "https://www.theguardian.com/technology/2025/sep/15/google-datacentre-kent-co2-thurrock-uk-ai",
                "archived": None,
            },
        ],
    ),
    feat(
        id="digital-realty-olivers-yard",
        name="Digital Realty Oliver's Yard (LHR18)",
        operator="Digital Realty",
        corridor="inner",
        local_authority="London Borough of Islington",
        lng=-0.087,
        lat=51.527,
        summary=(
            "Colocation hall at Oliver's Yard / City Road, about 100 yards from Old Street roundabout (Silicon Roundabout / Tech City). "
            "Directory sources put about 2.3 MW customer power (some listings cite about 4 MW total power). "
            "Held at proposed until a lasting planning portal URL is linked."
        ),
        power_block=power(
            it=2.3,
            it_src="Colo-X: Oliver's Yard about 2.3 MW of customer power",
            max_mw=2.3,
            max_src="Digital Realty Oliver's Yard: about 2.3 MW customer power (directory)",
        ),
        previous_use="Converted tech / colo building near Old Street",
        sources=[
            {
                "label": "Colo-X: Digital Realty Oliver's Yard",
                "url": "https://www.colo-x.com/data-centre/digital-realty-trust-olivers-yard/",
                "archived": None,
            }
        ],
    ),
]


def main():
    data = json.loads(DATA.read_text())
    for f in data["features"]:
        if f["properties"]["id"] == "virtus-london1-enfield":
            f["properties"]["corridor"] = "north"
        # Spread Telehouse campus pins slightly so they are not one stacked coordinate.
        spreads = {
            "telehouse-docklands": (-0.006, 51.5115),
            "telehouse-north-two": (-0.0035, 51.5128),
            "telehouse-west": (-0.0075, 51.5102),
            "telehouse-west-two": (-0.0055, 51.5094),
            "telehouse-south": (0.0065, 51.5075),
        }
        sid = f["properties"]["id"]
        if sid in spreads:
            f["geometry"]["coordinates"] = list(spreads[sid])

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
