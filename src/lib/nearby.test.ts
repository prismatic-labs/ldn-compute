import { describe, expect, it } from "vitest";
import { haversineKm, rankNearby } from "./nearby";
import type { OperationalReality, PowerBlock, SiteFeature, SiteStatus } from "./types";

function mkPower(mw: number | null): PowerBlock {
  return {
    grid_connection_mw: null,
    it_load_mw: null,
    phase_1_mw: null,
    max_proposed_mw: mw == null ? null : { value: mw, unit: "MW", basis: "stated", source: "t" },
  };
}

function site(
  id: string,
  lng: number,
  lat: number,
  opts: { mw?: number | null; status?: SiteStatus; reality?: OperationalReality } = {},
): SiteFeature {
  const { mw = null, status = "proposed", reality = "operating" } = opts;
  return {
    type: "Feature",
    geometry: { type: "Point", coordinates: [lng, lat] },
    properties: {
      id,
      name: id,
      operator: "t",
      status,
      local_authority: "t",
      corridor: "inner",
      planning_ref: { id: null, url: null },
      power: mkPower(mw),
      water_litres_pa: null,
      land: { acres: null, previous_use: null, land_type: "industrial_active" },
      grid_connection: null,
      cooling: null,
      claims_on_record: [],
      operator_response: null,
      timeline: [],
      controversies: [],
      sources: [],
      last_reviewed: "2026-07-25",
      operational_reality: reality,
    },
  };
}

const POINT = { lat: 51.5, lng: -0.12 };

describe("haversineKm", () => {
  it("is zero for the same point and positive otherwise", () => {
    expect(haversineKm(51.5, -0.12, 51.5, -0.12)).toBe(0);
    // ~0.12° of longitude at 51.5°N is roughly 8 km.
    const d = haversineKm(51.5, -0.12, 51.5, 0);
    expect(d).toBeGreaterThan(7);
    expect(d).toBeLessThan(10);
  });
});

describe("rankNearby", () => {
  const sites = [
    site("c-far", -0.05, 51.5, { mw: 5, reality: "consented" }),
    site("a-here", -0.12, 51.5, { mw: null, reality: "operating" }),
    site("b-mid", -0.1, 51.5, { mw: 20, reality: "pipeline" }),
  ];

  it("sorts by distance ascending", () => {
    const { results } = rankNearby(sites, POINT);
    expect(results.map((r) => r.site.properties.id)).toEqual(["a-here", "b-mid", "c-far"]);
  });

  it("applies a size floor and counts undisclosed sites it hides", () => {
    const { results, hiddenUndisclosed } = rankNearby(sites, POINT, { minMw: 10 });
    expect(results.map((r) => r.site.properties.id)).toEqual(["b-mid"]); // c-far 5MW excluded, a-here null excluded
    expect(hiddenUndisclosed).toBe(1); // a-here
  });

  it("filters by maturity (pipeline includes consented + under_construction)", () => {
    expect(rankNearby(sites, POINT, { maturity: "operating" }).results.map((r) => r.site.properties.id)).toEqual(["a-here"]);
    expect(rankNearby(sites, POINT, { maturity: "pipeline" }).results.map((r) => r.site.properties.id)).toEqual(["b-mid", "c-far"]);
  });

  it("excludes closed sites unless includeClosed is set", () => {
    const withClosed = [...sites, site("d-closed", -0.11, 51.5, { mw: 1, status: "decommissioned", reality: "closed" })];
    expect(rankNearby(withClosed, POINT).results.some((r) => r.site.properties.id === "d-closed")).toBe(false);
    expect(rankNearby(withClosed, POINT, { includeClosed: true }).results.some((r) => r.site.properties.id === "d-closed")).toBe(true);
  });

  it("respects the limit", () => {
    expect(rankNearby(sites, POINT, { limit: 2 }).results).toHaveLength(2);
  });
});
