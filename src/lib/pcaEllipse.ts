/**
 * PCA / covariance ellipse for a set of map points.
 * Works in a local metre frame so longitude isn’t stretched at UK latitudes.
 */

export type LngLat = [number, number];

const CHI2_95_2DF = 5.991; // ~95% of a bivariate normal cloud
const METRES_PER_DEG_LAT = 110_540;

function mean(xs: number[]): number {
  let s = 0;
  for (const x of xs) s += x;
  return s / xs.length;
}

/** Symmetric 2×2 eigen-decomposition. Returns [λ1, λ2, v1x, v1y] with λ1 ≥ λ2. */
function eigen2x2(a: number, b: number, c: number): [number, number, number, number] {
  const tr = a + c;
  const det = a * c - b * b;
  const disc = Math.max(0, tr * tr - 4 * det);
  const s = Math.sqrt(disc);
  let l1 = (tr + s) / 2;
  let l2 = (tr - s) / 2;
  if (l1 < l2) {
    const t = l1;
    l1 = l2;
    l2 = t;
  }

  let v1x: number;
  let v1y: number;
  if (Math.abs(b) > 1e-12) {
    v1x = l1 - c;
    v1y = b;
  } else if (a >= c) {
    v1x = 1;
    v1y = 0;
  } else {
    v1x = 0;
    v1y = 1;
  }
  const n = Math.hypot(v1x, v1y) || 1;
  return [l1, l2, v1x / n, v1y / n];
}

/**
 * Build a GeoJSON Polygon for the ~95% covariance ellipse of the points.
 * Returns null if there aren’t enough spread-out sites.
 */
export function pcaEllipseFeature(
  points: LngLat[],
  steps = 64,
): GeoJSON.Feature<GeoJSON.Polygon> | null {
  if (points.length < 3) return null;

  const lngs = points.map((p) => p[0]);
  const lats = points.map((p) => p[1]);
  const meanLng = mean(lngs);
  const meanLat = mean(lats);
  const cosLat = Math.cos((meanLat * Math.PI) / 180);
  const metresPerDegLng = METRES_PER_DEG_LAT * Math.max(0.2, cosLat);

  const xs: number[] = [];
  const ys: number[] = [];
  for (const [lng, lat] of points) {
    xs.push((lng - meanLng) * metresPerDegLng);
    ys.push((lat - meanLat) * METRES_PER_DEG_LAT);
  }

  const n = xs.length;
  let sxx = 0;
  let sxy = 0;
  let syy = 0;
  for (let i = 0; i < n; i++) {
    sxx += xs[i]! * xs[i]!;
    sxy += xs[i]! * ys[i]!;
    syy += ys[i]! * ys[i]!;
  }
  // Sample covariance (n-1) so a few sites don’t inflate the ellipse.
  const denom = Math.max(1, n - 1);
  const cxx = sxx / denom;
  const cxy = sxy / denom;
  const cyy = syy / denom;

  const [l1, l2, ux, uy] = eigen2x2(cxx, cxy, cyy);
  // Ignore near-degenerate clouds (all sites almost on one spot).
  if (l1 < 1e4) return null; // < ~100 m std on major axis

  const a = Math.sqrt(Math.max(l1, 0) * CHI2_95_2DF);
  const b = Math.sqrt(Math.max(l2, 0) * CHI2_95_2DF);
  const vx = -uy; // second axis (perpendicular)
  const vy = ux;

  const ring: LngLat[] = [];
  for (let i = 0; i <= steps; i++) {
    const t = (i / steps) * Math.PI * 2;
    const px = Math.cos(t) * a;
    const py = Math.sin(t) * b;
    // Rotate into map metres, then back to lng/lat.
    const mx = ux * px + vx * py;
    const my = uy * px + vy * py;
    ring.push([meanLng + mx / metresPerDegLng, meanLat + my / METRES_PER_DEG_LAT]);
  }

  return {
    type: "Feature",
    properties: {
      kind: "pca_ellipse",
      n: points.length,
      label: "Footprint ellipse (~95% of visible pins)",
    },
    geometry: {
      type: "Polygon",
      coordinates: [ring],
    },
  };
}

export function emptyEllipseCollection(): GeoJSON.FeatureCollection {
  return { type: "FeatureCollection", features: [] };
}

export function ellipseCollectionForSites(
  sites: Array<{ geometry: { coordinates: number[] } }>,
): GeoJSON.FeatureCollection {
  const points: LngLat[] = sites.map((s) => [
    s.geometry.coordinates[0]!,
    s.geometry.coordinates[1]!,
  ]);
  const feature = pcaEllipseFeature(points);
  return {
    type: "FeatureCollection",
    features: feature ? [feature] : [],
  };
}
