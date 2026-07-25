import { describe, expect, it } from "vitest";
import { pcaEllipseFeature } from "./pcaEllipse";

describe("pcaEllipseFeature", () => {
  it("returns null for fewer than three points", () => {
    expect(pcaEllipseFeature([[-0.5, 51.5], [-0.4, 51.5]])).toBeNull();
  });

  it("returns a closed polygon for a spread of London-scale points", () => {
    const feature = pcaEllipseFeature([
      [-0.6, 51.52],
      [-0.55, 51.52],
      [-0.5, 51.51],
      [-0.01, 51.51],
      [0.0, 51.5],
      [0.02, 51.51],
      [-0.1, 51.65],
      [-0.12, 51.36],
    ]);
    expect(feature).not.toBeNull();
    expect(feature!.geometry.type).toBe("Polygon");
    const ring = feature!.geometry.coordinates[0]!;
    expect(ring.length).toBeGreaterThan(16);
    expect(ring[0]).toEqual(ring[ring.length - 1]);
  });
});
