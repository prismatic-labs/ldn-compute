/**
 * CI validator for data/sites.geojson against data/schema.json
 * plus editorial hard rules from the build plan.
 */
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import Ajv2020 from "ajv/dist/2020.js";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const schema = JSON.parse(readFileSync(join(root, "data/schema.json"), "utf8"));
const data = JSON.parse(readFileSync(join(root, "data/sites.geojson"), "utf8"));

const ajv = new Ajv2020({ allErrors: true, strict: false });
const validate = ajv.compile(schema);

const errors: string[] = [];

if (!validate(data)) {
  for (const e of validate.errors ?? []) {
    errors.push(`schema: ${e.instancePath} ${e.message}`);
  }
}

const ABOVE = new Set([
  "in_planning",
  "approved",
  "under_construction",
  "operating",
  "decommissioned",
  "refused",
  "withdrawn",
]);

const ids = new Set<string>();
const coords = new Map<string, string>();
const roleById = new Map<string, string | undefined>();
const partOfRefs: Array<{ id: string; target: string }> = [];

for (const feature of data.features ?? []) {
  const p = feature.properties;
  if (ids.has(p.id)) errors.push(`duplicate id: ${p.id}`);
  ids.add(p.id);
  roleById.set(p.id, p.role);
  if (p.part_of) partOfRefs.push({ id: p.id, target: p.part_of });

  const [lng, lat] = feature.geometry.coordinates;
  // Overlapping pins hide one site under another on the map. Distinct facilities
  // must have distinct coordinates (nudge approximate placeholders apart).
  const key = `${lng},${lat}`;
  if (coords.has(key)) {
    errors.push(`${p.id}: shares exact coordinates [${key}] with ${coords.get(key)}`);
  } else {
    coords.set(key, p.id);
  }

  if (lng < -0.85 || lng > 0.35 || lat < 51.1 || lat > 51.82) {
    errors.push(`${p.id}: coordinates look outside Greater London / M25 fringe box (got [lng,lat]=[${lng},${lat}])`);
  }

  if (ABOVE.has(p.status)) {
    // A closed site is evidenced by any resolving source (operator/news page),
    // not a live planning application — the rest still need a planning URL.
    if (p.status === "decommissioned") {
      const hasSourceUrl = (p.sources ?? []).some((s: { url?: string }) => s.url);
      if (!p.planning_ref?.url && !hasSourceUrl) {
        errors.push(`${p.id}: status "decommissioned" requires a resolving source URL`);
      }
    } else if (!p.planning_ref?.url) {
      errors.push(`${p.id}: status "${p.status}" requires planning_ref.url`);
    } else if (
      /search\.do/i.test(p.planning_ref.url) &&
      !/applicationDetails|\/application\//i.test(p.planning_ref.url)
    ) {
      errors.push(
        `${p.id}: planning_ref.url must resolve to the live application, not a search form (${p.planning_ref.url})`,
      );
    }
  }

  // operational_reality is load-bearing (drives the pipeline view) and separate
  // from the URL-gated status, so keep the two consistent.
  const reality = p.operational_reality;
  if (!reality) {
    errors.push(`${p.id}: missing operational_reality`);
  } else if (reality === "closed" && p.status !== "decommissioned") {
    errors.push(`${p.id}: operational_reality "closed" requires status "decommissioned"`);
  } else if (p.status === "decommissioned" && reality !== "closed") {
    errors.push(`${p.id}: status "decommissioned" requires operational_reality "closed"`);
  } else if (p.status === "approved" && reality === "pipeline") {
    errors.push(`${p.id}: status "approved" is inconsistent with operational_reality "pipeline"`);
  }

  // Every non-null quantity must carry basis + source
  const checkQty = (path: string, q: unknown) => {
    if (q == null) return;
    if (typeof q !== "object") {
      errors.push(`${path}: expected quantity object or null`);
      return;
    }
    const o = q as Record<string, unknown>;
    for (const k of ["value", "unit", "basis", "source"]) {
      if (o[k] == null || o[k] === "") errors.push(`${path}: missing ${k}`);
    }
  };

  checkQty(`${p.id}.power.grid_connection_mw`, p.power?.grid_connection_mw);
  checkQty(`${p.id}.power.it_load_mw`, p.power?.it_load_mw);
  checkQty(`${p.id}.power.phase_1_mw`, p.power?.phase_1_mw);
  checkQty(`${p.id}.power.max_proposed_mw`, p.power?.max_proposed_mw);
  checkQty(`${p.id}.water_litres_pa`, p.water_litres_pa);
  checkQty(`${p.id}.land.acres`, p.land?.acres);
}

// part_of must point at an existing campus dossier flagged role: "aggregate".
for (const { id, target } of partOfRefs) {
  if (!ids.has(target)) {
    errors.push(`${id}: part_of "${target}" does not exist`);
  } else if (roleById.get(target) !== "aggregate") {
    errors.push(`${id}: part_of "${target}" is not a role:"aggregate" campus`);
  }
}

// ---- Non-blocking evidence report: methodology targets vs current data ----
// Warnings, not errors — they never fail the build; they track evidence debt.
let statedUncorroborated = 0;
let planningNoPage = 0;
let sourcesTotal = 0;
let sourcesArchived = 0;
let noWater = 0;
for (const feature of data.features ?? []) {
  const p = feature.properties;
  const quantities = [
    p.power?.grid_connection_mw,
    p.power?.it_load_mw,
    p.power?.phase_1_mw,
    p.power?.max_proposed_mw,
    p.land?.acres,
  ];
  for (const q of quantities) {
    if (!q) continue;
    if (q.basis === "stated" && !p.planning_ref?.url) statedUncorroborated += 1;
    if (q.basis === "planning_doc" && !q.page) planningNoPage += 1;
  }
  for (const s of p.sources ?? []) {
    sourcesTotal += 1;
    if (s.archived) sourcesArchived += 1;
  }
  if (p.water_litres_pa == null) noWater += 1;
}
const total = data.features?.length ?? 0;
console.warn("evidence report (non-blocking — methodology targets not yet met):");
console.warn(` - ${statedUncorroborated} stated figures not corroborated by a planning URL`);
console.warn(` - ${planningNoPage} planning_doc figures missing a page reference`);
console.warn(` - ${sourcesArchived}/${sourcesTotal} sources archived`);
console.warn(` - ${noWater}/${total} sites without a water figure`);

if (errors.length) {
  console.error("validate:sites failed:\n" + errors.map((e) => ` - ${e}`).join("\n"));
  process.exit(1);
}

console.log(`validate:sites ok — ${data.features.length} features, $version ${data.$version}`);
