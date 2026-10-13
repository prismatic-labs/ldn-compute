import { describe, expect, it } from "vitest";
import { getItemizedSites, regionalTotals, siteBestPower } from "./sites";
import type { PowerBlock, SiteFeature } from "./types";

function mw(value: number): PowerBlock {
  return {
    grid_connection_mw: null,
    it_load_mw: null,
    phase_1_mw: null,
    max_proposed_mw: { value, unit: "MW", basis: "stated", source: "test" },
  };
}

function site(
  id: string,
  power: PowerBlock,
  extra: Partial<SiteFeature["properties"]> = {},
): SiteFeature {
  return {
    type: "Feature",
    geometry: { type: "Point", coordinates: [0, 51.5] },
    properties: {
      id,
      name: id,
      operator: "test",
      status: "proposed",
      local_authority: "test",
      corridor: "west",
      planning_ref: { id: null, url: null },
      power,
      water_litres_pa: null,
      land: { acres: null, previous_use: null, land_type: "industrial_active" },
      grid_connection: null,
      cooling: null,
      claims_on_record: [],
      operator_response: null,
      timeline: [],
      controversies: [],
      sources: [],
      last_reviewed: "2026-07-20",
      ...extra,
    },
  };
}

describe("regionalTotals", () => {
  it("excludes campus aggregate pins from megawatts and count so halls are not double-counted", () => {
    const sites = [
      site("hall-a", mw(16)),
      site("hall-b", mw(25)),
      site("campus", mw(41), { role: "aggregate" }),
    ];
    const totals = regionalTotals(sites);
    expect(totals.count).toBe(2);
    expect(totals.aggregateCount).toBe(1);
    expect(totals.disclosedMw).toBe(41); // halls only, not 41 + 41
  });

  it("counts undisclosed-power sites but not aggregates", () => {
    const noPower: PowerBlock = {
      grid_connection_mw: null,
      it_load_mw: null,
      phase_1_mw: null,
      max_proposed_mw: null,
    };
    const totals = regionalTotals([
      site("known", mw(10)),
      site("unknown", noPower),
      site("campus", mw(10), { role: "aggregate" }),
    ]);
    expect(totals.count).toBe(2);
    expect(totals.undisclosedPower).toBe(1);
    expect(totals.aggregateCount).toBe(1);
  });
});

describe("getItemizedSites", () => {
  it("drops campus aggregates so tables/compare never rank them beside their halls", () => {
    const sites = [
      site("hall-a", mw(16)),
      site("campus", mw(41), { role: "aggregate" }),
      site("hall-b", mw(25)),
    ];
    const itemized = getItemizedSites(sites);
    expect(itemized.map((f) => f.properties.id)).toEqual(["hall-a", "hall-b"]);
  });

  it("keeps real dataset campus overlays out of the itemized list", () => {
    const itemized = getItemizedSites();
    expect(itemized.some((f) => f.properties.role === "aggregate")).toBe(false);
  });

  it("itemized MW equals regionalTotals MW (map and headline agree)", () => {
    // The map is fed getItemizedSites; the headline uses regionalTotals over all
    // sites (aggregates filtered internally). Closed sites appear on the map but
    // are excluded from the footprint total, so exclude them here too.
    const itemized = getItemizedSites().filter(
      (f) => f.properties.status !== "decommissioned",
    );
    // Use the same selector the headline uses, rather than re-implementing the
    // field priority here: a hand-rolled chain silently drops the MVA exclusion
    // and the two totals then disagree for reasons the test cannot see.
    const itemizedMw = itemized.reduce(
      (sum, f) => sum + (siteBestPower(f.properties)?.quantity.value ?? 0),
      0,
    );
    expect(regionalTotals().disclosedMw).toBe(itemizedMw);
  });
});
