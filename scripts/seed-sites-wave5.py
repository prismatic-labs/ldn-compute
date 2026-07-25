#!/usr/bin/env python3
"""Seed 15 more operator-sourced halls to reach 75 sites."""

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
            "controversies": [],
            "last_reviewed": "2026-07-20",
        },
    }


NEW = [
    feat(
        id="cyrusone-lon2-west-drayton",
        name="CyrusOne LON2 (West Drayton)",
        operator="CyrusOne",
        corridor="west",
        local_authority="London Borough of Hillingdon",
        lng=-0.46,
        lat=51.505,
        summary=(
            "CyrusOne LON2 at Prologis Park Heathrow, Stockley Road, West Drayton. Operator states 13.92 MW of IT load "
            "and 7,484 m² of technical space. Held at proposed until a lasting portal URL is linked."
        ),
        power_block=power(
            it=13.92,
            it_src="CyrusOne LON2 page / datasheet: 13.92 MW of IT load",
            max_mw=13.92,
            max_src="CyrusOne LON2: 13.92 MW IT capacity",
        ),
        previous_use="Prologis Park Heathrow industrial / logistics park",
        sources=[
            {
                "label": "CyrusOne: LON2",
                "url": "https://www.cyrusone.com/data-centers/emea/london-uk-lon2",
                "archived": None,
            }
        ],
    ),
    feat(
        id="cyrusone-lon3-slough",
        name="CyrusOne LON3 (Slough)",
        operator="CyrusOne",
        corridor="west",
        local_authority="Slough Borough Council",
        lng=-0.588,
        lat=51.522,
        summary=(
            "CyrusOne LON3 at Stirling Road, Slough. Operator states 9 MW of IT capacity and 3,600 m² of technical space. "
            "Held at proposed until a lasting portal URL is linked."
        ),
        power_block=power(
            it=9,
            it_src="CyrusOne LON3 page: 9 MW Total Megawatts IT Capacity",
            max_mw=9,
            max_src="CyrusOne LON3: 9 MW IT capacity",
        ),
        previous_use="Slough Trading Estate industrial plot",
        sources=[
            {
                "label": "CyrusOne: LON3",
                "url": "https://www.cyrusone.com/data-centers/emea/london-uk-lon3",
                "archived": None,
            }
        ],
    ),
    feat(
        id="cyrusone-lon4-slough",
        name="CyrusOne LON4 (Slough)",
        operator="CyrusOne",
        corridor="west",
        local_authority="Slough Borough Council",
        lng=-0.612,
        lat=51.512,
        summary=(
            "CyrusOne LON4 at 225B Bath Road, Slough. Operator states 18 MW IT capacity and 9,526 m² of technical space. "
            "Held at proposed until a lasting portal URL is linked."
        ),
        power_block=power(
            it=18,
            it_src="CyrusOne LON4 page: 18 MW Total Megawatts IT Capacity",
            max_mw=18,
            max_src="CyrusOne LON4: 18 MW IT capacity",
        ),
        previous_use="Bath Road / Slough industrial fringe",
        sources=[
            {
                "label": "CyrusOne: LON4",
                "url": "https://www.cyrusone.com/data-centers/emea/london-uk-lon4",
                "archived": None,
            }
        ],
    ),
    feat(
        id="cyrusone-lon5-slough",
        name="CyrusOne LON5 (Slough)",
        operator="CyrusOne",
        corridor="west",
        local_authority="Slough Borough Council",
        lng=-0.611,
        lat=51.511,
        summary=(
            "CyrusOne LON5 at 225C Bath Road, Slough. Operator states 18 MW IT capacity and 6,452 m² of technical space, "
            "with active/active dual redundant supplies of 27 MVA. Held at proposed until a lasting portal URL is linked."
        ),
        power_block=power(
            it=18,
            it_src="CyrusOne LON5 page: 18 MW Total Megawatts IT Capacity",
            max_mw=18,
            max_src="CyrusOne LON5: 18 MW IT capacity",
            grid=27,
            grid_src="CyrusOne LON5 page: Active/Active dual redundant power supplies of 27 MVA (recorded as 27 MW stated)",
        ),
        previous_use="Bath Road / Slough industrial fringe",
        sources=[
            {
                "label": "CyrusOne: LON5",
                "url": "https://www.cyrusone.com/data-centers/emea/london-uk-lon5",
                "archived": None,
            }
        ],
    ),
    feat(
        id="virtus-london14-stockley",
        name="VIRTUS LONDON14 (Stockley Park)",
        operator="VIRTUS Data Centres (STT GDC)",
        corridor="west",
        local_authority="London Borough of Hillingdon",
        lng=-0.45,
        lat=51.51,
        summary=(
            "VIRTUS Stockley Park campus building LONDON14 (bespoke design on the operator campus page; about 8,400 m² NTM). "
            "Directory listings commonly cite about 22 MW for LONDON14 at Horton Road / West Drayton. "
            "Held at proposed until a lasting portal URL and operator-primary MW line are linked."
        ),
        power_block=power(
            it=22,
            it_src="Directory listing for VIRTUS LONDON14 West Drayton / Stockley: about 22 MW",
            max_mw=22,
            max_src="VIRTUS LONDON14: about 22 MW (directory)",
        ),
        previous_use="Stockley Park / West Drayton business park fringe",
        sources=[
            {
                "label": "VIRTUS: Stockley Park campus (LONDON14)",
                "url": "https://virtusdatacentres.com/locations/uk/london/stockley-park-campus",
                "archived": None,
            }
        ],
    ),
    feat(
        id="equinix-ld7-slough",
        name="Equinix LD7 (Slough)",
        operator="Equinix",
        corridor="west",
        local_authority="Slough Borough Council",
        lng=-0.601,
        lat=51.525,
        summary=(
            "Equinix LD7 IBX on Banbury Avenue, Slough Trading Estate. Operator publishes building area (about 6,694 m²) "
            "but not a single public megawatt total on the IBX page. Location pin; held at proposed until MW or planning URL is linked."
        ),
        power_block=empty_power(),
        previous_use="Slough Trading Estate industrial plot",
        sources=[
            {
                "label": "Equinix: LD7",
                "url": "https://www.equinix.com/data-centers/europe-colocation/united-kingdom-colocation/london-data-centers/ld7",
                "archived": None,
            }
        ],
    ),
    feat(
        id="equinix-ld10-slough",
        name="Equinix LD10 (Slough)",
        operator="Equinix",
        corridor="west",
        local_authority="Slough Borough Council",
        lng=-0.585,
        lat=51.52,
        summary=(
            "Equinix LD10 at 13 Liverpool Road, Slough (former IO UK). Directory sources put about 9–12 MW at the hall; "
            "much of the site capacity was later oriented to the LD13x hyperscale joint venture. "
            "Held at proposed until a lasting portal URL is linked."
        ),
        power_block=power(
            it=9,
            it_src="Directory listing for Equinix LD10 Slough: about 9 MW total power",
            max_mw=9,
            max_src="Equinix LD10: about 9 MW (directory)",
        ),
        previous_use="Slough Trading Estate industrial plot (former IO)",
        sources=[
            {
                "label": "Colo-X: Equinix LD10",
                "url": "https://www.colo-x.com/data-centre/equinix-ld10-data-centre-slough/",
                "archived": None,
            }
        ],
    ),
    feat(
        id="equinix-ld13x-slough",
        name="Equinix LD13x (Slough)",
        operator="Equinix (xScale / GIC JV)",
        corridor="west",
        local_authority="Slough Borough Council",
        lng=-0.584,
        lat=51.521,
        summary=(
            "Equinix LD13x hyperscale portion of the Liverpool Road campus (xScale joint venture with GIC), "
            "carved from unused LD10 capacity. Directory listings cite about 9 MW. Held at proposed until a lasting portal URL is linked."
        ),
        power_block=power(
            it=9,
            it_src="Directory listing for Equinix LD13x Slough: about 9 MW",
            max_mw=9,
            max_src="Equinix LD13x: about 9 MW (directory)",
        ),
        previous_use="Slough Trading Estate — LD10 campus hyperscale tranche",
        sources=[
            {
                "label": "OCOLO: Equinix LD13x",
                "url": "https://www.ocolo.io/colocation/equinix/slough-ld13x/",
                "archived": None,
            }
        ],
    ),
    feat(
        id="telehouse-east",
        name="Telehouse East (Docklands)",
        operator="Telehouse (KDDI)",
        corridor="east",
        local_authority="London Borough of Tower Hamlets",
        lng=-0.0035,
        lat=51.5118,
        summary=(
            "Telehouse East on the Docklands campus (Coronation Road cluster), one of the original LINX-heavy halls "
            "alongside North and West. Campus-level megawatts are published for other halls; this pin is a distinct "
            "building location until a hall-specific lasting MW figure is linked. Held at proposed."
        ),
        power_block=empty_power(),
        previous_use="Docklands industrial / carrier campus",
        sources=[
            {
                "label": "Telehouse: London data centres",
                "url": "https://www.telehouse.net/data-centre-services/uk/london/",
                "archived": None,
            }
        ],
    ),
    feat(
        id="ntt-slough-3",
        name="NTT Slough 3 (SL3)",
        operator="NTT Global Data Centers",
        corridor="west",
        local_authority="Slough Borough Council",
        lng=-0.572,
        lat=51.516,
        summary=(
            "NTT Slough 3 at 665 Ajax Avenue, Slough Trading Estate. Operator states a maximum of 2.7 MW of critical IT load "
            "and about 1,500+ m² of server space. Held at proposed until a lasting portal URL is linked."
        ),
        power_block=power(
            it=2.7,
            it_src="NTT Slough 3 page: maximum of 2.7 MW of IT load",
            max_mw=2.7,
            max_src="NTT Slough 3: 2.7 MW IT load",
        ),
        previous_use="Slough Trading Estate industrial plot",
        sources=[
            {
                "label": "NTT: Slough 3 Data Center",
                "url": "https://services.global.ntt/en-us/services-and-products/global-data-centers/global-locations/emea/slough-3-data-center",
                "archived": None,
            }
        ],
    ),
    feat(
        id="kao-klon-01-harlow",
        name="Kao Data KLON-01 (Harlow)",
        operator="Kao Data",
        corridor="north",
        local_authority="Harlow District Council",
        lng=0.124,
        lat=51.776,
        summary=(
            "Kao Data KLON-01 at the Harlow campus. Operator states 8.8 MW operational for KLON-01. "
            "Held at proposed until a lasting Harlow portal URL is linked."
        ),
        power_block=power(
            it=8.8,
            it_src="Kao Data Harlow page: KLON-01 8.8 MW Operational",
            max_mw=8.8,
            max_src="Kao KLON-01: 8.8 MW",
        ),
        previous_use="Harlow campus industrial / research setting",
        sources=[
            {"label": "Kao Data: Harlow", "url": "https://kaodata.com/locations/harlow/", "archived": None}
        ],
    ),
    feat(
        id="kao-klon-02-harlow",
        name="Kao Data KLON-02 (Harlow)",
        operator="Kao Data",
        corridor="north",
        local_authority="Harlow District Council",
        lng=0.127,
        lat=51.778,
        summary=(
            "Kao Data KLON-02 at the Harlow campus. Operator states 8.8 MW operational for KLON-02. "
            "Held at proposed until a lasting Harlow portal URL is linked."
        ),
        power_block=power(
            it=8.8,
            it_src="Kao Data Harlow page: KLON-02 8.8 MW Operational",
            max_mw=8.8,
            max_src="Kao KLON-02: 8.8 MW",
        ),
        previous_use="Harlow campus industrial / research setting",
        sources=[
            {"label": "Kao Data: Harlow", "url": "https://kaodata.com/locations/harlow/", "archived": None}
        ],
    ),
    feat(
        id="kao-klon-03-harlow",
        name="Kao Data KLON-03 (Harlow)",
        operator="Kao Data",
        corridor="north",
        local_authority="Harlow District Council",
        lng=0.128,
        lat=51.775,
        summary=(
            "Kao Data KLON-03 at Harlow — operator lists 17.6 MW under development (liquid-cooled AI hall in operator news). "
            "Held at proposed until a lasting portal URL is linked (not upgraded to under construction without that URL)."
        ),
        power_block=power(
            it=17.6,
            it_src="Kao Data Harlow page: KLON-03 17.6 MW Under Development",
            max_mw=17.6,
            max_src="Kao KLON-03: 17.6 MW",
        ),
        previous_use="Harlow campus expansion plot",
        sources=[
            {"label": "Kao Data: Harlow", "url": "https://kaodata.com/locations/harlow/", "archived": None}
        ],
    ),
    feat(
        id="kao-klon-04-harlow",
        name="Kao Data KLON-04 (Harlow)",
        operator="Kao Data",
        corridor="north",
        local_authority="Harlow District Council",
        lng=0.129,
        lat=51.779,
        summary=(
            "Kao Data KLON-04 at Harlow — operator lists 36 MW planned. Held at proposed until a lasting portal URL is linked."
        ),
        power_block=power(
            it=36,
            it_src="Kao Data Harlow page: KLON-04 36 MW Planned",
            max_mw=36,
            max_src="Kao KLON-04: 36 MW planned",
        ),
        previous_use="Harlow campus expansion plot",
        sources=[
            {"label": "Kao Data: Harlow", "url": "https://kaodata.com/locations/harlow/", "archived": None}
        ],
    ),
    feat(
        id="digital-realty-lgw14-woking",
        name="Digital Realty LGW14 (Woking)",
        operator="Digital Realty",
        corridor="south",
        local_authority="Woking Borough Council",
        lng=-0.56,
        lat=51.32,
        summary=(
            "Digital Realty LGW14 in Woking on the south-west M25 fringe (Gatwick / Surrey colo set). "
            "Hall-specific megawatts not yet itemised here from a single operator disclosure. Location pin; held at proposed."
        ),
        power_block=empty_power(),
        previous_use="Woking industrial / business park setting",
        sources=[
            {
                "label": "Digital Realty: London / LGW campus set (operator UK pages)",
                "url": "https://www.digitalrealty.co.uk/data-centers/emea/london/lgw16",
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
    # Optionally enrich NTT SL3 if page MW appears later — leave empty for now.
    text = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    DATA.write_text(text)
    PUBLIC.write_text(text)
    print(f"total={len(data['features'])} added={len(added)} {added}")


if __name__ == "__main__":
    main()
