import { useEffect, useId, useRef, useState } from "react";
import maplibregl from "maplibre-gl";
import type { Corridor, SiteFeature } from "../lib/types";
import { circleScale, mapRadiusMetres, statusColour } from "../lib/mapScale";
import {
  ellipseCollectionForSites,
  emptyEllipseCollection,
} from "../lib/pcaEllipse";
import { formatNumber, powerKindLabel, bestPower } from "../lib/units";

interface Props {
  sites: SiteFeature[];
  baseUrl: string;
  center: [number, number];
  zoom: number;
  /** One-line headline stat shown in the overlay panel (e.g. running vs pipeline MW). */
  stat?: string;
}

const CORRIDORS: Array<{ id: Corridor; label: string }> = [
  { id: "west", label: "West / Slough–Heathrow" },
  { id: "east", label: "Docklands / East" },
  { id: "north", label: "North fringe" },
  { id: "south", label: "South fringe" },
  { id: "inner", label: "Inner" },
];

/** Geographic framing extents [SW, NE] so zoom isn't pinned to the tight site cluster. */
const CORRIDOR_BOUNDS: Record<Corridor, [[number, number], [number, number]]> = {
  west: [
    [-0.72, 51.42],
    [-0.18, 51.58],
  ],
  east: [
    [-0.08, 51.46],
    [0.32, 51.58],
  ],
  north: [
    [-0.55, 51.62],
    [0.2, 51.8],
  ],
  south: [
    [-0.28, 51.1],
    [0.05, 51.45],
  ],
  inner: [
    [-0.12, 51.5],
    [-0.04, 51.54],
  ],
};

const SITES_SOURCE = "lcr-sites";
const CLUSTER_LAYER = "lcr-clusters";
const CLUSTER_COUNT_LAYER = "lcr-cluster-count";
const ELLIPSE_SOURCE = "lcr-pca-ellipse";
const ELLIPSE_FILL = "lcr-pca-ellipse-fill";
const ELLIPSE_LINE = "lcr-pca-ellipse-line";
/** Distinct from corridor ink: statistical overlay, not a site filter. */
const ELLIPSE_COLOR = "#c44536";
const ELLIPSE_TIP =
  "Principal-component ellipse of the visible pins (about 95% of the cloud). A statistical footprint of where sites sit, not the M25 and not a planning boundary.";
/** Max zoom at which points may still cluster; above this every site is its own marker. */
const CLUSTER_MAX_ZOOM = 11;
/** Pixel radius for grouping — lower = less greedy (nearby campuses stay separate longer). */
const CLUSTER_RADIUS = 32;

type CorridorVisibility = Record<Corridor, boolean>;
type ZoomFocus = "all" | Corridor;

const ALL_VISIBLE: CorridorVisibility = {
  west: true,
  east: true,
  north: true,
  south: true,
  inner: true,
};

function filteredCollection(
  all: SiteFeature[],
  visibility: CorridorVisibility,
): GeoJSON.FeatureCollection {
  return {
    type: "FeatureCollection",
    features: all.filter((s) => visibility[s.properties.corridor]),
  };
}

/**
 * One click: frame the *next* break of this bubble (child clusters / points),
 * not a dive into the cluster centroid (which for a metro-wide “50” can land
 * somewhere meaningless like Twyford).
 */
async function zoomToFirstSegmentation(
  map: maplibregl.Map,
  source: maplibregl.GeoJSONSource,
  clusterId: number,
  center: [number, number],
) {
  try {
    const [expansionZoom, children] = await Promise.all([
      source.getClusterExpansionZoom(clusterId),
      source.getClusterChildren(clusterId),
    ]);

    const bounds = new maplibregl.LngLatBounds();
    for (const child of children) {
      if (child.geometry.type === "Point") {
        bounds.extend(child.geometry.coordinates as [number, number]);
      }
    }

    // Cap at the expansion zoom so we stop at first segmentation, not street level.
    const maxZoom = Math.min(Math.max(expansionZoom + 0.2, map.getZoom() + 0.5), CLUSTER_MAX_ZOOM + 1);

    if (!bounds.isEmpty() && children.length > 0) {
      map.fitBounds(bounds, {
        padding: { top: 72, bottom: 72, left: 56, right: 56 },
        maxZoom,
        duration: 550,
        essential: true,
      });
      return;
    }

    map.easeTo({
      center,
      zoom: maxZoom,
      duration: 550,
      essential: true,
    });
  } catch {
    map.easeTo({
      center,
      zoom: Math.min(map.getZoom() + 1.25, CLUSTER_MAX_ZOOM + 1),
      duration: 550,
      essential: true,
    });
  }
}

function makeSiteMarkerEl(site: SiteFeature): HTMLButtonElement {
  const scale = circleScale(site.properties);
  const el = document.createElement("button");
  el.type = "button";
  el.className = "lcr-marker";
  el.setAttribute("aria-label", site.properties.name);
  el.dataset.corridor = site.properties.corridor;
  const r = Math.max(14, mapRadiusMetres(scale) / 280);
  const colour = statusColour(site.properties.status);
  const dashed = scale.mode !== "power";
  el.style.width = `${r * 2}px`;
  el.style.height = `${r * 2}px`;
  el.style.borderRadius = "50%";
  el.style.border = dashed ? `2.5px dashed ${colour}` : `2px solid ${colour}`;
  // Whisper of fill on dashed rings so sites stay visible on Positron
  el.style.background = dashed ? `${colour}28` : `${colour}33`;
  el.style.cursor = "pointer";
  el.style.padding = "0";
  return el;
}

export default function SiteMap({ sites, baseUrl, center, zoom, stat }: Props) {
  const containerRef = useRef<HTMLDivElement>(null);
  const mapRef = useRef<maplibregl.Map | null>(null);
  const markersRef = useRef<Map<string, maplibregl.Marker>>(new Map());
  const sitesByIdRef = useRef<Map<string, SiteFeature>>(new Map());
  const [selected, setSelected] = useState<SiteFeature | null>(null);
  const [visibleCorridors, setVisibleCorridors] =
    useState<CorridorVisibility>(ALL_VISIBLE);
  const [showEllipse, setShowEllipse] = useState(false);
  const [zoomFocus, setZoomFocus] = useState<ZoomFocus>("all");
  const visibleCorridorsRef = useRef(visibleCorridors);
  visibleCorridorsRef.current = visibleCorridors;
  const showEllipseRef = useRef(showEllipse);
  showEllipseRef.current = showEllipse;
  const panelId = useId();

  useEffect(() => {
    sitesByIdRef.current = new Map(sites.map((s) => [s.properties.id, s]));
  }, [sites]);

  useEffect(() => {
    if (!containerRef.current || mapRef.current) return;

    const map = new maplibregl.Map({
      container: containerRef.current,
      // OpenFreeMap: MapLibre-native, no API key. OSM raster tiles often block embedded clients.
      style: "https://tiles.openfreemap.org/styles/positron",
      center,
      zoom,
      cooperativeGestures: true,
      attributionControl: { compact: true },
    });

    map.addControl(new maplibregl.NavigationControl({ showCompass: false }), "top-right");
    mapRef.current = map;
    // Stable Map instance; capture it so the cleanup below doesn't read a ref
    // that lint (rightly) warns may have changed by teardown.
    const markers = markersRef.current;

    const syncUnclusteredMarkers = () => {
      if (!map.getSource(SITES_SOURCE) || !map.isSourceLoaded(SITES_SOURCE)) return;

      const rendered = map.querySourceFeatures(SITES_SOURCE, {
        filter: ["!", ["has", "point_count"]],
      });
      const visibleIds = new Set<string>();
      for (const f of rendered) {
        const id = f.properties?.id as string | undefined;
        if (!id || visibleIds.has(id)) continue;
        visibleIds.add(id);
        const site = sitesByIdRef.current.get(id);
        if (!site) continue;

        let marker = markersRef.current.get(id);
        if (!marker) {
          const el = makeSiteMarkerEl(site);
          el.addEventListener("click", (e) => {
            e.stopPropagation();
            const current = sitesByIdRef.current.get(id);
            if (current) setSelected(current);
          });
          marker = new maplibregl.Marker({ element: el, anchor: "center" })
            .setLngLat(site.geometry.coordinates as [number, number])
            .addTo(map);
          markersRef.current.set(id, marker);
        }
      }

      for (const [id, marker] of markersRef.current) {
        if (!visibleIds.has(id)) {
          marker.remove();
          markersRef.current.delete(id);
        }
      }
    };

    map.on("load", () => {
      map.addSource(SITES_SOURCE, {
        type: "geojson",
        data: filteredCollection(sites, visibleCorridorsRef.current),
        cluster: true,
        clusterMaxZoom: CLUSTER_MAX_ZOOM,
        clusterRadius: CLUSTER_RADIUS,
        promoteId: "id",
      });

      map.addLayer({
        id: CLUSTER_LAYER,
        type: "circle",
        source: SITES_SOURCE,
        filter: ["has", "point_count"],
        paint: {
          "circle-color": "#1a1d1f",
          "circle-opacity": 0.88,
          "circle-radius": [
            "step",
            ["get", "point_count"],
            16,
            4,
            20,
            10,
            26,
            20,
            32,
          ],
          "circle-stroke-width": 2,
          "circle-stroke-color": "#f7f6f2",
        },
      });

      map.addLayer({
        id: CLUSTER_COUNT_LAYER,
        type: "symbol",
        source: SITES_SOURCE,
        filter: ["has", "point_count"],
        layout: {
          "text-field": ["get", "point_count_abbreviated"],
          "text-size": 12,
          "text-allow-overlap": true,
        },
        paint: {
          "text-color": "#f7f6f2",
        },
      });

      const visibleSites = sites.filter(
        (s) => visibleCorridorsRef.current[s.properties.corridor],
      );
      map.addSource(ELLIPSE_SOURCE, {
        type: "geojson",
        data: showEllipseRef.current
          ? ellipseCollectionForSites(visibleSites)
          : emptyEllipseCollection(),
      });
      map.addLayer({
        id: ELLIPSE_FILL,
        type: "fill",
        source: ELLIPSE_SOURCE,
        paint: {
          "fill-color": ELLIPSE_COLOR,
          "fill-opacity": 0.08,
        },
      });
      map.addLayer({
        id: ELLIPSE_LINE,
        type: "line",
        source: ELLIPSE_SOURCE,
        paint: {
          "line-color": ELLIPSE_COLOR,
          "line-width": 2,
          "line-opacity": 0.85,
          "line-dasharray": [2.5, 1.75],
        },
      });

      const onClusterClick = (e: maplibregl.MapLayerMouseEvent) => {
        e.originalEvent.stopPropagation();
        const hit =
          e.features?.[0] ??
          map.queryRenderedFeatures(e.point, {
            layers: [CLUSTER_LAYER, CLUSTER_COUNT_LAYER],
          })[0];
        if (!hit || hit.geometry.type !== "Point") return;
        // GeoJSON properties are often strings; MapLibre needs a numeric cluster id.
        const clusterId = Number(hit.properties?.cluster_id);
        if (!Number.isFinite(clusterId)) return;
        const source = map.getSource(SITES_SOURCE) as maplibregl.GeoJSONSource;
        const coords = hit.geometry.coordinates as [number, number];
        void zoomToFirstSegmentation(map, source, clusterId, coords);
      };

      // Count labels sit on top of the circle; listen on both so a click anywhere on the bubble works.
      map.on("click", CLUSTER_LAYER, onClusterClick);
      map.on("click", CLUSTER_COUNT_LAYER, onClusterClick);

      for (const layer of [CLUSTER_LAYER, CLUSTER_COUNT_LAYER]) {
        map.on("mouseenter", layer, () => {
          map.getCanvas().style.cursor = "pointer";
        });
        map.on("mouseleave", layer, () => {
          map.getCanvas().style.cursor = "";
        });
      }

      map.on("render", syncUnclusteredMarkers);
      syncUnclusteredMarkers();
    });

    return () => {
      map.off("render", syncUnclusteredMarkers);
      for (const marker of markers.values()) marker.remove();
      markers.clear();
      map.remove();
      mapRef.current = null;
    };
  }, [sites, center, zoom]);

  useEffect(() => {
    const map = mapRef.current;
    if (!map) return;
    const source = map.getSource(SITES_SOURCE) as maplibregl.GeoJSONSource | undefined;
    if (!source) return;
    const visible = sites.filter((s) => visibleCorridors[s.properties.corridor]);
    source.setData(filteredCollection(sites, visibleCorridors));

    const ellipseSource = map.getSource(ELLIPSE_SOURCE) as maplibregl.GeoJSONSource | undefined;
    if (ellipseSource) {
      ellipseSource.setData(
        showEllipse ? ellipseCollectionForSites(visible) : emptyEllipseCollection(),
      );
    }

    if (selected && !visibleCorridors[selected.properties.corridor]) {
      setSelected(null);
    }
  }, [visibleCorridors, selected, sites, showEllipse]);

  const best = selected ? bestPower(selected.properties.power) : null;
  const scale = selected ? circleScale(selected.properties) : null;

  function toggleCorridorDisplay(id: Corridor) {
    setVisibleCorridors((prev) => {
      const next = { ...prev, [id]: !prev[id] };
      // Keep at least one corridor on so the map never goes blank by accident.
      if (!Object.values(next).some(Boolean)) return prev;
      return next;
    });
  }

  function flyToFocus(id: ZoomFocus) {
    const map = mapRef.current;
    if (!map) return;
    setZoomFocus(id);

    if (id === "all") {
      map.flyTo({ center, zoom, essential: true });
      return;
    }

    const [sw, ne] = CORRIDOR_BOUNDS[id];
    const bounds = new maplibregl.LngLatBounds(sw, ne);
    // Still include any sites slightly outside the geographic frame.
    for (const site of sites.filter((s) => s.properties.corridor === id)) {
      bounds.extend(site.geometry.coordinates as [number, number]);
    }
    map.fitBounds(bounds, {
      padding: { top: 72, bottom: 48, left: 36, right: 36 },
      maxZoom: 9.2,
      duration: 900,
      essential: true,
    });
  }

  return (
    <div
      className="relative w-full bg-[var(--paper)]"
      style={{ height: "100dvh", minHeight: "100vh" }}
    >
      <div
        ref={containerRef}
        className="absolute inset-0"
        style={{ width: "100%", height: "100%" }}
        role="application"
        aria-label="Map of data centre sites"
      />

      <div className="pointer-events-none absolute left-0 top-0 z-10 p-2.5 sm:p-3">
        <div className="pointer-events-auto max-w-[18.5rem] rounded border border-[var(--line)] bg-[var(--map-panel)] px-3 py-2 shadow-sm sm:max-w-xs">
          <a href={`${baseUrl}/`} className="wordmark block mb-1 no-underline text-[0.7rem]">
            The London Compute Ring
          </a>
          <p className="m-0 text-[0.75rem] text-[var(--ink)] font-display tracking-tight leading-snug">
            AI and cloud leave a physical footprint: power, land, and water. This map puts data centres
            across Greater London and the M25 fringe, and those figures, where communities can see them.
          </p>
          {stat && (
            <p className="m-0 mt-1.5 text-[0.72rem] font-tabular text-[var(--muted)]">{stat}</p>
          )}
          <nav className="mt-1.5 flex flex-wrap items-center gap-x-2.5 gap-y-0.5 text-[0.75rem]" aria-label="Site">
            <a href={`${baseUrl}/nearby`} className="text-[var(--ink)]/75 no-underline hover:text-[var(--ink)]">Near you</a>
            <a href={`${baseUrl}/pipeline`} className="text-[var(--ink)]/75 no-underline hover:text-[var(--ink)]">Pipeline</a>
            <a href={`${baseUrl}/sites`} className="text-[var(--ink)]/75 no-underline hover:text-[var(--ink)]">Sites</a>
            <a href={`${baseUrl}/compare`} className="text-[var(--ink)]/75 no-underline hover:text-[var(--ink)]">Compare</a>
            <a href={`${baseUrl}/research`} className="text-[var(--ink)]/75 no-underline hover:text-[var(--ink)]">Research</a>
            <a href={`${baseUrl}/methodology`} className="text-[var(--ink)]/75 no-underline hover:text-[var(--ink)]">Methodology</a>
            <a href={`${baseUrl}/contribute`} className="text-[var(--ink)]/75 no-underline hover:text-[var(--ink)]">Contribute</a>
          </nav>

          <div className="mt-2 border-t border-[var(--line)] pt-2">
            <p className="m-0 mb-1.5 text-[0.65rem] uppercase tracking-wider text-[var(--muted)]">
              Display
            </p>
            <div
              className="flex flex-wrap gap-1.5"
              role="group"
              aria-label="Show or hide sites by area"
            >
              {CORRIDORS.map(({ id, label }) => {
                const on = visibleCorridors[id];
                return (
                  <button
                    key={`display-${id}`}
                    type="button"
                    aria-pressed={on}
                    onClick={() => toggleCorridorDisplay(id)}
                    className="rounded border px-2 py-1 text-[0.7rem] leading-none cursor-pointer transition-colors"
                    style={{
                      borderColor: on ? "var(--ink)" : "var(--line)",
                      background: on ? "var(--ink)" : "transparent",
                      color: on ? "var(--paper)" : "var(--muted)",
                    }}
                  >
                    {label}
                  </button>
                );
              })}
            </div>
            <div className="relative mt-1.5 inline-block group/ellipse">
              <button
                type="button"
                aria-pressed={showEllipse}
                aria-describedby={`${panelId}-ellipse-tip`}
                onClick={() => setShowEllipse((v) => !v)}
                className="rounded border px-2 py-1 text-[0.7rem] leading-none cursor-pointer transition-colors"
                style={{
                  borderColor: ELLIPSE_COLOR,
                  background: showEllipse ? ELLIPSE_COLOR : "transparent",
                  color: showEllipse ? "var(--paper)" : ELLIPSE_COLOR,
                }}
              >
                Footprint ellipse
              </button>
              <span
                id={`${panelId}-ellipse-tip`}
                role="tooltip"
                className="pointer-events-none absolute left-0 top-full z-30 mt-1.5 w-[min(16.5rem,calc(100vw-3rem))] rounded border border-[var(--line)] bg-[var(--paper)] px-2.5 py-2 text-[0.65rem] leading-snug text-[var(--ink)] shadow-sm opacity-0 invisible group-hover/ellipse:opacity-100 group-hover/ellipse:visible group-focus-within/ellipse:opacity-100 group-focus-within/ellipse:visible"
              >
                {ELLIPSE_TIP}
              </span>
            </div>
            {showEllipse && (
              <p className="m-0 mt-1.5 text-[0.65rem] leading-snug" style={{ color: ELLIPSE_COLOR }}>
                Dashed red outline is a statistical spread of the visible pins (~95%), not a ring or
                planning boundary.
              </p>
            )}
            <p className="m-0 mt-2.5 mb-1.5 text-[0.65rem] uppercase tracking-wider text-[var(--muted)]">
              Zoom
            </p>
            <div
              className="flex flex-wrap gap-1.5"
              role="group"
              aria-label="Zoom map to an area"
            >
              {(
                [
                  { id: "all" as const, label: "All" },
                  ...CORRIDORS,
                ] as Array<{ id: ZoomFocus; label: string }>
              ).map(({ id, label }) => {
                const on = zoomFocus === id;
                return (
                  <button
                    key={`zoom-${id}`}
                    type="button"
                    aria-pressed={on}
                    onClick={() => flyToFocus(id)}
                    className="rounded border px-2 py-1 text-[0.7rem] leading-none cursor-pointer transition-colors"
                    style={{
                      borderColor: on ? "var(--ink)" : "var(--line)",
                      background: "transparent",
                      color: on ? "var(--ink)" : "var(--muted)",
                      boxShadow: on ? "inset 0 0 0 1px var(--ink)" : "none",
                    }}
                  >
                    {label}
                  </button>
                );
              })}
            </div>
          </div>
        </div>
      </div>

      <ScaleBar />

      {selected && (
        <aside
          id={panelId}
          className="absolute z-20 bg-[var(--map-panel)] border border-[var(--line)] shadow-sm
            inset-x-0 bottom-0 max-h-[55vh] overflow-auto rounded-t-lg p-4
            sm:inset-x-auto sm:bottom-auto sm:right-4 sm:top-24 sm:w-96 sm:max-h-[70vh] sm:rounded-md"
          aria-label={`${selected.properties.name} summary`}
        >
          <div className="flex items-start justify-between gap-3">
            <div>
              <p className="m-0 text-xs uppercase tracking-wider text-[var(--muted)]">{selected.properties.status.replaceAll("_", " ")}</p>
              <h2 className="font-display text-xl m-0 mt-1">{selected.properties.name}</h2>
              <p className="m-0 mt-1 text-sm text-[var(--muted)]">{selected.properties.operator} · {selected.properties.local_authority}</p>
            </div>
            <button
              type="button"
              className="text-[var(--muted)] border-0 bg-transparent cursor-pointer text-lg leading-none"
              onClick={() => setSelected(null)}
              aria-label="Close panel"
            >
              ×
            </button>
          </div>
          <p className="text-sm mt-3 mb-0">{selected.properties.summary}</p>
          <dl className="grid grid-cols-[auto_1fr] gap-x-3 gap-y-1 text-sm mt-3 mb-0">
            <dt className="text-[var(--muted)]">Stated size</dt>
            <dd className="m-0 font-tabular">
              {best ? (
                <>
                  <span>
                    {formatNumber(best.quantity.value)} megawatts · {powerKindLabel(best.kind)}
                  </span>
                  <span className="block text-xs text-[var(--muted)] font-sans font-normal mt-0.5 leading-snug">
                    How large the scheme claims to be, not how much electricity it will use day to day.
                  </span>
                  <span className="block text-xs text-[var(--muted)] font-sans font-normal mt-0.5 leading-snug">
                    Source: {best.quantity.source}
                  </span>
                </>
              ) : scale?.mode === "acreage_undisclosed" ? (
                "Not disclosed; circle sized by site area"
              ) : scale?.mode === "location_only" ? (
                "Not disclosed; marker shows location only"
              ) : (
                "Not disclosed"
              )}
            </dd>
            <dt className="text-[var(--muted)]">Site area</dt>
            <dd className="m-0 font-tabular">
              {selected.properties.land.acres
                ? `${formatNumber(selected.properties.land.acres.value)} acres`
                : scale?.mode === "location_only"
                  ? "Not disclosed"
                  : "Unknown"}
              {" · "}
              {selected.properties.land.land_type === "brownfield"
                ? "brownfield"
                : selected.properties.land.land_type === "agricultural"
                  ? "farmland"
                  : "industrial"}
            </dd>
          </dl>
          <p className="mt-4 mb-0">
            <a href={`${baseUrl}/site/${selected.properties.id}`}>Full site details →</a>
          </p>
        </aside>
      )}

      <style>{`
        .maplibregl-coop-gesture-screen { background: rgba(247,246,242,0.85) !important; color: #1a1d1f !important; }
      `}</style>
    </div>
  );
}

function ScaleBar() {
  const refs = [
    { label: "5 MW", mw: 5 },
    { label: "100 MW", mw: 100 },
    { label: "1 GW", mw: 1000 },
  ];
  const statusKeys: Array<{ label: string; colour: string }> = [
    { label: "Proposed", colour: statusColour("proposed") },
    { label: "In planning", colour: statusColour("in_planning") },
    { label: "Approved", colour: statusColour("approved") },
    { label: "Building", colour: statusColour("under_construction") },
    { label: "Operating", colour: statusColour("operating") },
    { label: "Decommissioned", colour: statusColour("decommissioned") },
  ];
  return (
    <div
      className="absolute bottom-3 left-3 z-10 max-w-[17.5rem] rounded-md border border-[var(--line)] bg-[var(--map-panel)] px-3 py-2.5 text-xs shadow-sm"
      aria-label="How to read map circles. Colour is planning status. Outline style is whether power is disclosed. Size is megawatts or site area. Nearby sites group into numbered clusters when zoomed out."
    >
      <p className="m-0 mb-2 font-display tracking-wide uppercase text-[0.65rem] text-[var(--muted)]">
        How to read the circles
      </p>

      <p className="m-0 mb-1 text-[0.65rem] text-[var(--muted)]">
        Colour = planning status
      </p>
      <ul className="m-0 mb-2.5 list-none grid grid-cols-2 grid-rows-3 grid-flow-col gap-x-3 gap-y-1 p-0 text-[0.7rem] leading-snug text-[var(--ink)]">
        {statusKeys.map((s) => (
          <li key={s.label} className="flex items-center gap-1.5 min-w-0">
            <span
              className="inline-block shrink-0 rounded-full border-2"
              style={{
                width: 12,
                height: 12,
                borderColor: s.colour,
                background: `${s.colour}66`,
              }}
              aria-hidden
            />
            <span className="truncate">{s.label}</span>
          </li>
        ))}
      </ul>

      <p className="m-0 mb-1 text-[0.65rem] text-[var(--muted)]">
        Outline = size disclosed
      </p>
      <ul className="m-0 mb-2.5 list-none space-y-1.5 p-0 text-[0.7rem] leading-snug text-[var(--ink)]">
        <li className="flex items-center gap-2">
          <span
            className="inline-block shrink-0 rounded-full border-2 border-[var(--ink)] bg-[var(--ink)]/20"
            style={{ width: 14, height: 14 }}
            aria-hidden
          />
          <span>Solid fill: megawatts published</span>
        </li>
        <li className="flex items-center gap-2">
          <span
            className="inline-block shrink-0 rounded-full border-2 border-dashed border-[var(--ink)] bg-transparent"
            style={{ width: 14, height: 14 }}
            aria-hidden
          />
          <span>Dashed: megawatts not disclosed (sized by site area, or location only if area unknown)</span>
        </li>
      </ul>
      <p className="m-0 mb-2 text-[0.65rem] text-[var(--muted)] leading-snug">
        Grey demos above are style only, not a status colour. Numbered dark circles group nearby sites: click to frame the next split of that group.
      </p>

      <p className="m-0 mb-1.5 text-[0.65rem] text-[var(--muted)]">
        Size = stated megawatts when known
      </p>
      <div className="flex items-end gap-3">
        {refs.map((r) => {
          const px = 8 + Math.sqrt(r.mw / 1000) * 28;
          return (
            <div key={r.label} className="flex flex-col items-center gap-1">
              <span
                className="rounded-full border-2 border-[var(--ink)] bg-[var(--ink)]/15"
                style={{ width: px, height: px }}
                aria-hidden
              />
              <span className="font-tabular text-[var(--ink)]">{r.label}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
