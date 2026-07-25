#!/usr/bin/env python3
"""Append wave-2 London/M25 site dossiers to data/sites.geojson."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "sites.geojson"
PUBLIC = ROOT / "public" / "data" / "sites.geojson"

NULL_PLANNING = {"id": None, "url": None}


def qty(value: float, source: str) -> dict:
    return {
        "value": value,
        "unit": "MW",
        "basis": "stated",
        "source": source,
        "page": None,
        "archived": None,
    }


def power_block(
    *,
    it: float | None = None,
    it_src: str | None = None,
    max_mw: float | None = None,
    max_src: str | None = None,
    grid: float | None = None,
    grid_src: str | None = None,
) -> dict:
    it_q = qty(it, it_src) if it is not None and it_src else None
    max_q = (
        qty(max_mw, max_src)
        if max_mw is not None and max_src
        else (deepcopy(it_q) if it_q else None)
    )
    return {
        "grid_connection_mw": qty(grid, grid_src) if grid is not None and grid_src else None,
        "it_load_mw": it_q,
        "phase_1_mw": None,
        "max_proposed_mw": max_q,
    }


def empty_power() -> dict:
    return {
        "grid_connection_mw": None,
        "it_load_mw": None,
        "phase_1_mw": None,
        "max_proposed_mw": None,
    }


def feature(
    *,
    id: str,
    name: str,
    operator: str,
    corridor: str,
    local_authority: str,
    lng: float,
    lat: float,
    summary: str,
    power: dict,
    sources: list[dict],
    timeline: list[dict] | None = None,
    previous_use: str,
    land_type: str = "industrial_active",
) -> dict:
    return {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [lng, lat]},
        "properties": {
            "id": id,
            "name": name,
            "operator": operator,
            "status": "proposed",
            "local_authority": local_authority,
            "corridor": corridor,
            "summary": summary,
            "power": power,
            "land": {
                "acres": None,
                "previous_use": previous_use,
                "land_type": land_type,
                "alc_grades": None,
            },
            "timeline": timeline or [],
            "sources": sources,
            "planning_ref": deepcopy(NULL_PLANNING),
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
    feature(
        id="iron-mountain-lon1-slough",
        name="Iron Mountain LON-1 (Slough)",
        operator="Iron Mountain Data Centers",
        corridor="west",
        local_authority="Slough Borough Council",
        lng=-0.598,
        lat=51.524,
        summary=(
            "Iron Mountain LON-1 on Dundee Road in the Slough Trading Estate corridor. "
            "Operator London pages state about 8.7 MW total capacity and 10,400 m² at LON-1. "
            "Operator presents the hall as operating; held at proposed until a lasting Slough Public Access URL is linked."
        ),
        power=power_block(
            it=8.7,
            it_src="Iron Mountain London data centres page: 10,400 m² / 8.7 MW at LON-1",
            max_mw=8.7,
            max_src="Iron Mountain: 8.7 MW at LON-1",
        ),
        sources=[
            {
                "label": "Iron Mountain: London data centres",
                "url": "https://www.ironmountain.com/en-gb/data-centers/locations/london-data-center",
                "archived": None,
            }
        ],
        previous_use="Former banking data centre (operator description)",
    ),
    feature(
        id="iron-mountain-lon2-slough",
        name="Iron Mountain LON-2 (Slough)",
        operator="Iron Mountain Data Centers",
        corridor="west",
        local_authority="Slough Borough Council",
        lng=-0.59,
        lat=51.521,
        summary=(
            "Iron Mountain LON-2 on Buckingham Avenue, Slough Trading Estate. "
            "Operator London pages state about 27 MW capacity and 25,000 m² at LON-2. "
            "Held at proposed until a lasting planning portal URL is linked."
        ),
        power=power_block(
            it=27,
            it_src="Iron Mountain London data centres page: 25,000 m² / 27 MW at LON-2",
            max_mw=27,
            max_src="Iron Mountain: 27 MW at LON-2",
        ),
        sources=[
            {
                "label": "Iron Mountain: London data centres",
                "url": "https://www.ironmountain.com/en-gb/data-centers/locations/london-data-center",
                "archived": None,
            }
        ],
        previous_use="Slough Trading Estate industrial plot",
    ),
    feature(
        id="iron-mountain-lon3-slough",
        name="Iron Mountain LON-3 (Slough)",
        operator="Iron Mountain Data Centers",
        corridor="west",
        local_authority="Slough Borough Council",
        lng=-0.589,
        lat=51.52,
        summary=(
            "Iron Mountain LON-3 on Buckingham Avenue, marketed as in development with expected completion in 2026. "
            "Operator pages state about 25 MW capacity and 5,220 m². Held at proposed until a lasting planning portal URL is linked."
        ),
        power=power_block(
            it=25,
            it_src="Iron Mountain London data centres page: 5,220 m² / 25 MW at LON-3",
            max_mw=25,
            max_src="Iron Mountain: 25 MW at LON-3",
        ),
        sources=[
            {
                "label": "Iron Mountain: London data centres",
                "url": "https://www.ironmountain.com/en-gb/data-centers/locations/london-data-center",
                "archived": None,
            }
        ],
        timeline=[
            {
                "date": "2026",
                "event": "Operator expects LON-3 completion in 2026",
                "source": "https://www.ironmountain.com/en-gb/data-centers/locations/london-data-center",
            }
        ],
        previous_use="Slough Trading Estate industrial plot",
    ),
    feature(
        id="virtus-london3-slough",
        name="VIRTUS LONDON3 (Slough)",
        operator="VIRTUS Data Centres (STT GDC)",
        corridor="west",
        local_authority="Slough Borough Council",
        lng=-0.582,
        lat=51.519,
        summary=(
            "VIRTUS Slough campus building LONDON3. Operator site lists 7.2 MW IT load and 3,000 m² net technical space. "
            "Held at proposed until a lasting Slough Public Access URL is linked."
        ),
        power=power_block(
            it=7.2,
            it_src="VIRTUS Slough campus listing: LONDON3 7.2 MW",
            max_mw=7.2,
            max_src="VIRTUS LONDON3: 7.2 MW IT load",
        ),
        sources=[
            {
                "label": "VIRTUS: LONDON3 Slough",
                "url": "https://virtusdatacentres.com/locations/uk/london/london-3-slough",
                "archived": None,
            },
            {
                "label": "VIRTUS: LONDON9 page (campus MW list)",
                "url": "https://virtusdatacentres.com/locations/uk/london/slough-london9",
                "archived": None,
            },
        ],
        previous_use="Slough Trading Estate industrial plot",
    ),
    feature(
        id="virtus-london9-slough",
        name="VIRTUS LONDON9 (Slough)",
        operator="VIRTUS Data Centres (STT GDC)",
        corridor="west",
        local_authority="Slough Borough Council",
        lng=-0.578,
        lat=51.521,
        summary=(
            "VIRTUS Slough campus building LONDON9. Operator states over 10,000 m² net technical space and 24 MW of IT load. "
            "Held at proposed until a lasting Slough Public Access URL is linked."
        ),
        power=power_block(
            it=24,
            it_src="VIRTUS LONDON9 page: 24 MW of IT load",
            max_mw=24,
            max_src="VIRTUS LONDON9: 24 MW IT load",
        ),
        sources=[
            {
                "label": "VIRTUS: LONDON9 Slough",
                "url": "https://virtusdatacentres.com/locations/uk/london/slough-london9",
                "archived": None,
            }
        ],
        previous_use="Slough Trading Estate industrial plot",
    ),
    feature(
        id="virtus-london10-slough",
        name="VIRTUS LONDON10 (Slough)",
        operator="VIRTUS Data Centres (STT GDC)",
        corridor="west",
        local_authority="Slough Borough Council",
        lng=-0.577,
        lat=51.518,
        summary=(
            "VIRTUS Slough campus building LONDON10. Operator campus listing states 6.6 MW IT load and 3,000 m² net technical space. "
            "Held at proposed until a lasting planning portal URL is linked."
        ),
        power=power_block(
            it=6.6,
            it_src="VIRTUS Slough campus listing: LONDON10 6.6 MW",
            max_mw=6.6,
            max_src="VIRTUS LONDON10: 6.6 MW IT load",
        ),
        sources=[
            {
                "label": "VIRTUS: LONDON9 page (campus MW list)",
                "url": "https://virtusdatacentres.com/locations/uk/london/slough-london9",
                "archived": None,
            }
        ],
        previous_use="Slough Trading Estate industrial plot",
    ),
    feature(
        id="virtus-london11-slough",
        name="VIRTUS LONDON11 (Slough)",
        operator="VIRTUS Data Centres (STT GDC)",
        corridor="west",
        local_authority="Slough Borough Council",
        lng=-0.576,
        lat=51.522,
        summary=(
            "VIRTUS Slough campus building LONDON11. Operator campus listing states 13 MW IT load and 5,500 m² net technical space. "
            "Held at proposed until a lasting planning portal URL is linked."
        ),
        power=power_block(
            it=13,
            it_src="VIRTUS Slough campus listing: LONDON11 13 MW",
            max_mw=13,
            max_src="VIRTUS LONDON11: 13 MW IT load",
        ),
        sources=[
            {
                "label": "VIRTUS: LONDON9 page (campus MW list)",
                "url": "https://virtusdatacentres.com/locations/uk/london/slough-london9",
                "archived": None,
            }
        ],
        previous_use="Slough Trading Estate industrial plot",
    ),
    feature(
        id="virtus-london12-slough",
        name="VIRTUS LONDON12 (Slough)",
        operator="VIRTUS Data Centres (STT GDC)",
        corridor="west",
        local_authority="Slough Borough Council",
        lng=-0.574,
        lat=51.519,
        summary=(
            "VIRTUS Slough campus building LONDON12. Operator campus listing states 21 MW IT load and 7,800 m² net technical space. "
            "Held at proposed until a lasting planning portal URL is linked."
        ),
        power=power_block(
            it=21,
            it_src="VIRTUS Slough campus listing: LONDON12 21 MW",
            max_mw=21,
            max_src="VIRTUS LONDON12: 21 MW IT load",
        ),
        sources=[
            {
                "label": "VIRTUS: LONDON9 page (campus MW list)",
                "url": "https://virtusdatacentres.com/locations/uk/london/slough-london9",
                "archived": None,
            }
        ],
        previous_use="Slough Trading Estate industrial plot",
    ),
    feature(
        id="virtus-london19-slough",
        name="VIRTUS LONDON19 (Slough)",
        operator="VIRTUS Data Centres (STT GDC)",
        corridor="west",
        local_authority="Slough Borough Council",
        lng=-0.573,
        lat=51.523,
        summary=(
            "VIRTUS Slough campus building LONDON19. Operator campus listing states 32.5 MW. "
            "Held at proposed until a lasting planning portal URL is linked."
        ),
        power=power_block(
            it=32.5,
            it_src="VIRTUS Slough campus listing: LONDON19 32.5 MW",
            max_mw=32.5,
            max_src="VIRTUS LONDON19: 32.5 MW",
        ),
        sources=[
            {
                "label": "VIRTUS: LONDON9 page (campus MW list)",
                "url": "https://virtusdatacentres.com/locations/uk/london/slough-london9",
                "archived": None,
            }
        ],
        previous_use="Slough Trading Estate industrial plot",
    ),
    feature(
        id="virtus-london2-hayes",
        name="VIRTUS LONDON2 (Hayes)",
        operator="VIRTUS Data Centres (STT GDC)",
        corridor="west",
        local_authority="London Borough of Hillingdon",
        lng=-0.425,
        lat=51.505,
        summary=(
            "VIRTUS LONDON2 at Hayes, west London. Operator datasheet states 11.4 MW of IT load and over 6,000 m² net technical space, "
            "with a 20 MVA incoming supply. Held at proposed until a lasting planning portal URL is linked."
        ),
        power=power_block(
            it=11.4,
            it_src="VIRTUS LONDON2 Hayes datasheet: 11.4 MW of IT load",
            max_mw=11.4,
            max_src="VIRTUS LONDON2: 11.4 MW IT load",
            grid=20,
            grid_src="VIRTUS LONDON2 datasheet: 20 MVA incoming diversely routed supply (recorded as 20 MW stated)",
        ),
        sources=[
            {
                "label": "VIRTUS: LONDON2 Hayes datasheet (PDF)",
                "url": "https://virtusdatacentres.com/images/datasheets/Virtus-datasheet-London2-RP2006152.pdf",
                "archived": None,
            }
        ],
        previous_use="West London industrial / warehouse setting",
    ),
    feature(
        id="virtus-london1-enfield",
        name="VIRTUS LONDON1 (Enfield)",
        operator="VIRTUS Data Centres (STT GDC)",
        corridor="east",
        local_authority="London Borough of Enfield",
        lng=-0.048,
        lat=51.652,
        summary=(
            "VIRTUS LONDON1 at Enfield on the north London / M25 fringe. Operator states over 2,900 m² net technical space and 4.2 MW of IT load. "
            "Held at proposed until a lasting planning portal URL is linked."
        ),
        power=power_block(
            it=4.2,
            it_src="VIRTUS LONDON1 Enfield page: 4.2 MW of IT load",
            max_mw=4.2,
            max_src="VIRTUS LONDON1: 4.2 MW IT load",
        ),
        sources=[
            {
                "label": "VIRTUS: LONDON1 Enfield",
                "url": "https://virtusdatacentres.com/locations/uk/london/enfield-campus",
                "archived": None,
            }
        ],
        previous_use="North London industrial setting",
    ),
    feature(
        id="virtus-london6-stockley",
        name="VIRTUS LONDON6 (Stockley Park)",
        operator="VIRTUS Data Centres (STT GDC)",
        corridor="west",
        local_authority="London Borough of Hillingdon",
        lng=-0.448,
        lat=51.512,
        summary=(
            "VIRTUS Stockley Park campus building LONDON6. Operator lists 16 MW IT load and 7,000 m² net technical space. "
            "Held at proposed until a lasting planning portal URL is linked."
        ),
        power=power_block(
            it=16,
            it_src="VIRTUS Stockley / Enfield campus listing: LONDON6 16 MW",
            max_mw=16,
            max_src="VIRTUS LONDON6: 16 MW IT load",
        ),
        sources=[
            {
                "label": "VIRTUS: Enfield campus (Stockley MW list)",
                "url": "https://virtusdatacentres.com/locations/uk/london/enfield-campus",
                "archived": None,
            }
        ],
        previous_use="Stockley Park business park / industrial fringe",
    ),
    feature(
        id="virtus-london7-stockley",
        name="VIRTUS LONDON7 (Stockley Park)",
        operator="VIRTUS Data Centres (STT GDC)",
        corridor="west",
        local_authority="London Borough of Hillingdon",
        lng=-0.446,
        lat=51.514,
        summary=(
            "VIRTUS Stockley Park campus building LONDON7. Operator lists 28 MW IT load and 13,000 m² net technical space. "
            "Held at proposed until a lasting planning portal URL is linked."
        ),
        power=power_block(
            it=28,
            it_src="VIRTUS Stockley / Enfield campus listing: LONDON7 28 MW",
            max_mw=28,
            max_src="VIRTUS LONDON7: 28 MW IT load",
        ),
        sources=[
            {
                "label": "VIRTUS: Enfield campus (Stockley MW list)",
                "url": "https://virtusdatacentres.com/locations/uk/london/enfield-campus",
                "archived": None,
            }
        ],
        previous_use="Stockley Park business park / industrial fringe",
    ),
    feature(
        id="virtus-london8-stockley",
        name="VIRTUS LONDON8 (Stockley Park)",
        operator="VIRTUS Data Centres (STT GDC)",
        corridor="west",
        local_authority="London Borough of Hillingdon",
        lng=-0.444,
        lat=51.511,
        summary=(
            "VIRTUS Stockley Park campus building LONDON8. Operator lists 18 MW IT load and 7,000 m² net technical space. "
            "Held at proposed until a lasting planning portal URL is linked."
        ),
        power=power_block(
            it=18,
            it_src="VIRTUS Stockley / Enfield campus listing: LONDON8 18 MW",
            max_mw=18,
            max_src="VIRTUS LONDON8: 18 MW IT load",
        ),
        sources=[
            {
                "label": "VIRTUS: Enfield campus (Stockley MW list)",
                "url": "https://virtusdatacentres.com/locations/uk/london/enfield-campus",
                "archived": None,
            }
        ],
        previous_use="Stockley Park business park / industrial fringe",
    ),
    feature(
        id="ntt-slough-2",
        name="NTT Slough 2 (SL2)",
        operator="NTT Global Data Centers",
        corridor="west",
        local_authority="Slough Borough Council",
        lng=-0.575,
        lat=51.517,
        summary=(
            "NTT Slough 2 on Ajax Avenue, Slough Trading Estate. Operator states a maximum of 1.8 MW of critical IT load "
            "with dual HV grid connections. Held at proposed until a lasting Slough Public Access URL is linked."
        ),
        power=power_block(
            it=1.8,
            it_src="NTT Slough 2 page: 1.8 MW of critical IT load",
            max_mw=1.8,
            max_src="NTT Slough 2: 1.8 MW IT load",
        ),
        sources=[
            {
                "label": "NTT: Slough 2 Data Center",
                "url": "https://services.global.ntt/en-us/services-and-products/global-data-centers/global-locations/emea/slough-2-data-center",
                "archived": None,
            }
        ],
        previous_use="Slough Trading Estate industrial plot",
    ),
    feature(
        id="equinix-ld8-docklands",
        name="Equinix LD8 (Harbour Exchange)",
        operator="Equinix",
        corridor="east",
        local_authority="London Borough of Tower Hamlets",
        lng=-0.021,
        lat=51.499,
        summary=(
            "Equinix LD8 IBX at Harbour Exchange Square in the Docklands interconnection cluster. "
            "Operator publishes building area (about 12,769 m²) but not a single campus megawatt figure on the public IBX page. "
            "Location pin only for stated size until a lasting MW disclosure or planning URL is linked. Held at proposed."
        ),
        power=empty_power(),
        sources=[
            {
                "label": "Equinix: LD8",
                "url": "https://www.equinix.com/data-centers/europe-colocation/united-kingdom-colocation/london-data-centers/ld8",
                "archived": None,
            }
        ],
        previous_use="Docklands office / exchange campus",
    ),
    feature(
        id="equinix-ld9-powergate",
        name="Equinix LD9 (Powergate)",
        operator="Equinix",
        corridor="west",
        local_authority="London Borough of Ealing",
        lng=-0.278,
        lat=51.528,
        summary=(
            "Equinix LD9 at Powergate Business Park (Volt Avenue), west London, near other Park Royal / Powergate halls. "
            "Operator publishes building area (about 15,372 m²) but not a single public megawatt total on the IBX page. "
            "Location pin only for stated size until MW or planning URL is linked. Held at proposed."
        ),
        power=empty_power(),
        sources=[
            {
                "label": "Equinix: LD9",
                "url": "https://www.equinix.com/data-centers/europe-colocation/united-kingdom-colocation/london-data-centers/ld9",
                "archived": None,
            }
        ],
        previous_use="Powergate / Park Royal industrial estate",
    ),
    feature(
        id="telehouse-west",
        name="Telehouse West (Docklands)",
        operator="Telehouse (KDDI)",
        corridor="east",
        local_authority="London Borough of Tower Hamlets",
        lng=-0.002,
        lat=51.51,
        summary=(
            "Telehouse West on the Docklands campus (Coronation Road area), part of the LINX-heavy interconnection cluster. "
            "Operator London materials cite about 18 MW total power capacity for the West hall context (2.7 MW per floor in published figures). "
            "Held at proposed until a lasting planning portal URL is linked."
        ),
        power=power_block(
            it=18,
            it_src="Telehouse London pages: West / campus power figures citing 18 MW total power capacity (2.7 MW per floor)",
            max_mw=18,
            max_src="Telehouse West: about 18 MW total power capacity (operator London materials)",
        ),
        sources=[
            {
                "label": "Telehouse: London data centres",
                "url": "https://www.telehouse.net/data-centre-services/uk/london/",
                "archived": None,
            }
        ],
        previous_use="Docklands industrial / carrier campus",
    ),
    feature(
        id="telehouse-west-two",
        name="Telehouse West Two (Docklands)",
        operator="Telehouse (KDDI)",
        corridor="east",
        local_authority="London Borough of Tower Hamlets",
        lng=-0.001,
        lat=51.509,
        summary=(
            "Telehouse West Two on the Docklands campus. Operator October 2025 announcement: groundbreaking on a £275m hall, "
            "completion targeted for 2028, overall building capacity of 33 MW (up to 4.4 MW per floor). "
            "Held at proposed until a lasting planning portal URL is linked (not upgraded to under construction without that URL)."
        ),
        power=power_block(
            it=33,
            it_src="Telehouse West Two groundbreaking release: overall building capacity of 33 MW",
            max_mw=33,
            max_src="Telehouse West Two: 33 MW building capacity",
        ),
        sources=[
            {
                "label": "Telehouse: West Two groundbreaking",
                "url": "https://www.telehouse.com/2025/10/23/telehouse-breaks-ground-on-new-275m-data-centre-telehouse-west-two/",
                "archived": None,
            }
        ],
        timeline=[
            {
                "date": "2025-10",
                "event": "Operator announces groundbreaking; completion targeted for 2028",
                "source": "https://www.telehouse.com/2025/10/23/telehouse-breaks-ground-on-new-275m-data-centre-telehouse-west-two/",
            }
        ],
        previous_use="Docklands campus expansion plot",
    ),
    feature(
        id="telehouse-south",
        name="Telehouse South (Blackwall Yard)",
        operator="Telehouse (KDDI)",
        corridor="east",
        local_authority="London Borough of Tower Hamlets",
        lng=0.005,
        lat=51.508,
        summary=(
            "Telehouse South at Blackwall Yard, opened 2022 about 300 metres from the main Docklands campus. "
            "Campus-level megawatts are published for other halls; this pin is location-led until a hall-specific lasting MW figure "
            "or planning URL is linked. Held at proposed."
        ),
        power=empty_power(),
        sources=[
            {
                "label": "Telehouse: London data centres",
                "url": "https://www.telehouse.net/data-centre-services/uk/london/",
                "archived": None,
            }
        ],
        timeline=[
            {
                "date": "2022",
                "event": "Telehouse South opened at Blackwall Yard",
                "source": "https://www.telehouse.net/data-centre-services/uk/london/",
            }
        ],
        previous_use="Blackwall Yard riverside industrial",
    ),
    feature(
        id="serverfarm-lon1-feltham",
        name="Serverfarm LON1 (Feltham)",
        operator="Serverfarm",
        corridor="west",
        local_authority="London Borough of Hounslow",
        lng=-0.408,
        lat=51.448,
        summary=(
            "Serverfarm LON1 in Feltham on the west London / Heathrow fringe. Trade and directory sources commonly cite about "
            "11.4 MW of IT capacity for the hall. Held at proposed until a lasting planning portal URL and operator-primary MW page are linked."
        ),
        power=power_block(
            it=11.4,
            it_src="Secondary trade / directory reporting of Serverfarm LON1 Feltham IT capacity (about 11.4 MW)",
            max_mw=11.4,
            max_src="Serverfarm LON1 Feltham: about 11.4 MW IT (secondary sources)",
        ),
        sources=[
            {
                "label": "Serverfarm: London",
                "url": "https://www.serverfarmllc.com/locations/london/",
                "archived": None,
            }
        ],
        previous_use="West London industrial / warehouse setting",
    ),
    feature(
        id="digital-realty-docklands",
        name="Digital Realty Docklands (Harbour Exchange)",
        operator="Digital Realty",
        corridor="east",
        local_authority="London Borough of Tower Hamlets",
        lng=-0.019,
        lat=51.5,
        summary=(
            "Digital Realty (former Interxion) presence in the Harbour Exchange / Docklands interconnection cluster. "
            "Operator London metro footprint spans multiple facilities; this pin is a Docklands location seed until "
            "hall-specific megawatts and a lasting planning URL are linked. Held at proposed."
        ),
        power=empty_power(),
        sources=[
            {
                "label": "Digital Realty: London",
                "url": "https://www.digitalrealty.com/data-centers/emea/united-kingdom/london",
                "archived": None,
            }
        ],
        previous_use="Docklands office / exchange campus",
    ),
]


def main() -> None:
    data = json.loads(DATA.read_text())
    existing = {f["properties"]["id"] for f in data["features"]}
    added = []
    for f in NEW:
        fid = f["properties"]["id"]
        if fid in existing:
            continue
        data["features"].append(f)
        added.append(fid)
    text = json.dumps(data, indent=2) + "\n"
    DATA.write_text(text)
    PUBLIC.write_text(text)
    print(f"total={len(data['features'])} added={len(added)} ids={added}")


if __name__ == "__main__":
    main()
