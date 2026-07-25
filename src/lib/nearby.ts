import type { BestPower, OperationalReality, SiteFeature } from "./types";
import { bestPower } from "./units";

export interface LatLng {
  lat: number;
  lng: number;
}

export interface NearbyResult {
  site: SiteFeature;
  km: number;
  best: BestPower | null;
}

export interface NearbyOptions {
  minMw?: number;
  maturity?: "all" | "operating" | "pipeline";
  includeClosed?: boolean;
  limit?: number;
}

const PIPELINE_REALITIES: ReadonlySet<OperationalReality> = new Set([
  "pipeline",
  "consented",
  "under_construction",
]);

/** Great-circle distance in kilometres. */
export function haversineKm(aLat: number, aLng: number, bLat: number, bLng: number): number {
  const R = 6371;
  const dLat = ((bLat - aLat) * Math.PI) / 180;
  const dLng = ((bLng - aLng) * Math.PI) / 180;
  const s =
    Math.sin(dLat / 2) ** 2 +
    Math.cos((aLat * Math.PI) / 180) *
      Math.cos((bLat * Math.PI) / 180) *
      Math.sin(dLng / 2) ** 2;
  return 2 * R * Math.asin(Math.sqrt(s));
}

/**
 * Sites nearest a point, filtered by size / maturity / closed, sorted by distance.
 * Pure so the ranking that powers /nearby is unit-tested. `hiddenUndisclosed`
 * counts sites dropped only because a size floor is set and their power is unknown.
 */
export function rankNearby(
  sites: SiteFeature[],
  point: LatLng,
  opts: NearbyOptions = {},
): { results: NearbyResult[]; hiddenUndisclosed: number } {
  const { minMw = 0, maturity = "all", includeClosed = false, limit = 20 } = opts;
  let hiddenUndisclosed = 0;

  const results = sites
    .map((site): NearbyResult => {
      const best = bestPower(site.properties.power);
      const [lng, lat] = site.geometry.coordinates;
      return { site, best, km: haversineKm(point.lat, point.lng, lat, lng) };
    })
    .filter((r) => {
      const p = r.site.properties;
      if (!includeClosed && p.status === "decommissioned") return false;
      if (minMw > 0) {
        const mw = r.best?.quantity.value ?? null;
        if (mw == null) {
          hiddenUndisclosed += 1;
          return false;
        }
        if (mw < minMw) return false;
      }
      if (maturity === "operating" && p.operational_reality !== "operating") return false;
      if (maturity === "pipeline" && !PIPELINE_REALITIES.has(p.operational_reality as OperationalReality))
        return false;
      return true;
    })
    .sort((a, b) => a.km - b.km)
    .slice(0, limit);

  return { results, hiddenUndisclosed };
}
