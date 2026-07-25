import { useMemo, useState } from "react";
import type { SiteFeature } from "../lib/types";
import { formatMw, formatNumber, powerKindLabel } from "../lib/units";
import { statusColour } from "../lib/mapScale";
import { rankNearby } from "../lib/nearby";

interface Props {
  sites: SiteFeature[];
  baseUrl: string;
}

const SIZE_OPTIONS = [
  { label: "Any size", value: 0 },
  { label: "10 MW or more", value: 10 },
  { label: "50 MW or more", value: 50 },
  { label: "100 MW or more", value: 100 },
];

const MATURITY_OPTIONS = [
  { label: "All", value: "all" },
  { label: "Operating now", value: "operating" },
  { label: "Pipeline (not yet built)", value: "pipeline" },
];

function km(v: number): string {
  return v < 10 ? `${formatNumber(v, 1)} km` : `${formatNumber(v)} km`;
}

export default function NearbyFinder({ sites, baseUrl }: Props) {
  const [postcode, setPostcode] = useState("");
  const [point, setPoint] = useState<{ lat: number; lng: number; label: string } | null>(null);
  const [minMw, setMinMw] = useState(0);
  const [maturity, setMaturity] = useState<"all" | "operating" | "pipeline">("all");
  const [includeClosed, setIncludeClosed] = useState(false);
  const [state, setState] = useState<"idle" | "loading" | "error">("idle");
  const [errMsg, setErrMsg] = useState("");

  async function search() {
    const pc = postcode.trim();
    if (!pc) return;
    setState("loading");
    setErrMsg("");
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), 8000);
    try {
      const res = await fetch(
        `https://api.postcodes.io/postcodes/${encodeURIComponent(pc)}`,
        { signal: controller.signal },
      );
      if (!res.ok) {
        throw new Error(res.status === 404 ? "Postcode not found. Check it and try again." : "Lookup failed.");
      }
      const j = await res.json();
      const r = j.result;
      setPoint({
        lat: r.latitude,
        lng: r.longitude,
        label: `${r.postcode} · ${[r.admin_ward, r.admin_district].filter(Boolean).join(", ")}`,
      });
      setState("idle");
    } catch (err) {
      setPoint(null);
      setState("error");
      const e = err as Error;
      setErrMsg(
        e.name === "AbortError"
          ? "The postcode lookup timed out. Try again."
          : e instanceof TypeError
            ? "Could not reach the postcode service. Check your connection and try again."
            : e.message,
      );
    } finally {
      clearTimeout(timer);
    }
  }

  const { results, hiddenUndisclosed } = useMemo(
    () =>
      point
        ? rankNearby(sites, point, { minMw, maturity, includeClosed })
        : { results: [], hiddenUndisclosed: 0 },
    [point, sites, minMw, maturity, includeClosed],
  );

  return (
    <div>
      <form onSubmit={(e) => { e.preventDefault(); void search(); }} className="grid gap-3 sm:grid-cols-[1fr_auto] items-end">
        <div className="grid gap-3 sm:grid-cols-3">
          <label className="block text-sm">
            <span className="text-[var(--muted)]">Postcode</span>
            <input
              type="text"
              value={postcode}
              onChange={(e) => setPostcode((e.target as HTMLInputElement).value)}
              placeholder="e.g. SW1A 0AA"
              autoComplete="postal-code"
              className="mt-1 w-full border border-[var(--line)] rounded px-2 py-1.5 bg-transparent"
            />
          </label>
          <label className="block text-sm">
            <span className="text-[var(--muted)]">Minimum size</span>
            <select
              value={minMw}
              onChange={(e) => setMinMw(Number((e.target as HTMLSelectElement).value))}
              className="mt-1 w-full border border-[var(--line)] rounded px-2 py-1.5 bg-transparent"
            >
              {SIZE_OPTIONS.map((o) => (
                <option key={o.value} value={o.value}>{o.label}</option>
              ))}
            </select>
          </label>
          <label className="block text-sm">
            <span className="text-[var(--muted)]">Maturity</span>
            <select
              value={maturity}
              onChange={(e) => setMaturity((e.target as HTMLSelectElement).value as "all" | "operating" | "pipeline")}
              className="mt-1 w-full border border-[var(--line)] rounded px-2 py-1.5 bg-transparent"
            >
              {MATURITY_OPTIONS.map((o) => (
                <option key={o.value} value={o.value}>{o.label}</option>
              ))}
            </select>
          </label>
        </div>
        <button
          type="submit"
          className="border border-[var(--ink)] rounded px-4 py-1.5 text-sm hover:bg-[var(--ink)] hover:text-[var(--paper)] transition-colors"
        >
          Find
        </button>
      </form>

      <label className="flex items-center gap-2 mt-3 text-sm text-[var(--muted)]">
        <input
          type="checkbox"
          checked={includeClosed}
          onChange={(e) => setIncludeClosed((e.target as HTMLInputElement).checked)}
        />
        Include closed sites
      </label>

      <div aria-live="polite" className="mt-6">
        {state === "loading" && <p className="text-[var(--muted)]">Looking up postcode…</p>}
        {state === "error" && <p className="text-[var(--amber)]">{errMsg}</p>}

        {point && state !== "loading" && (
          <>
            <p className="text-sm text-[var(--muted)]">
              Nearest mapped sites to <strong className="text-[var(--ink)]">{point.label}</strong>
              {results.length === 0 && " — none match these filters."}
            </p>

            {results.length > 0 && (
              <ol className="mt-4 list-none p-0 m-0 divide-y divide-[var(--line)] border-y border-[var(--line)]">
                {results.map((r) => {
                  const p = r.site.properties;
                  return (
                    <li key={p.id} className="py-3 flex items-baseline gap-3">
                      <span className="font-tabular text-sm text-[var(--muted)] w-16 shrink-0">{km(r.km)}</span>
                      <span className="flex-1">
                        <a href={`${baseUrl}/site/${p.id}`} className="font-medium">
                          {p.name}
                        </a>
                        <span className="block text-xs text-[var(--muted)]">
                          {p.operator}
                          {" · "}
                          {r.best
                            ? `${formatMw(r.best.quantity.value)} MW ${powerKindLabel(r.best.kind)}`
                            : "size not disclosed"}
                        </span>
                      </span>
                      <span
                        className="text-xs px-1.5 py-0.5 rounded self-center capitalize whitespace-nowrap"
                        style={{ color: statusColour(p.status), border: `1px solid ${statusColour(p.status)}` }}
                      >
                        {(p.operational_reality ?? p.status).replaceAll("_", " ")}
                      </span>
                    </li>
                  );
                })}
              </ol>
            )}

            {hiddenUndisclosed > 0 && (
              <p className="text-xs text-[var(--muted)] mt-3">
                {hiddenUndisclosed} nearby {hiddenUndisclosed === 1 ? "site has" : "sites have"} undisclosed
                power and {hiddenUndisclosed === 1 ? "is" : "are"} hidden by the size filter.
              </p>
            )}
          </>
        )}
      </div>

      <p className="text-xs text-[var(--muted)] mt-8 max-w-2xl">
        This finds the nearest schemes <em>we track</em>. The map is not a census of every data centre, so
        small server rooms below the size threshold will not appear. Postcodes are looked up via
        {" "}
        <a href="https://postcodes.io" rel="noopener noreferrer">postcodes.io</a> (Ordnance Survey / ONS
        open data); the postcode you enter is sent there to get a location.
      </p>
    </div>
  );
}
