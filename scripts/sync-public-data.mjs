/**
 * Single source of truth: `data/` is authored; `public/data/` is the published
 * copy the site links to for downloads. This copies data/ → public/data/ so the
 * two can never drift. Wired into predev/prebuild; also runnable via `npm run sync:data`.
 */
import { readdirSync, copyFileSync, mkdirSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const src = join(root, "data");
const dest = join(root, "public", "data");

mkdirSync(dest, { recursive: true });

let copied = 0;
let unchanged = 0;
for (const name of readdirSync(src, { withFileTypes: true })) {
  if (!name.isFile()) continue; // published data is flat files only
  const from = join(src, name.name);
  const to = join(dest, name.name);
  let same = false;
  try {
    same = readFileSync(from).equals(readFileSync(to));
  } catch {
    same = false; // destination missing
  }
  if (same) {
    unchanged += 1;
    continue;
  }
  copyFileSync(from, to);
  copied += 1;
}

console.log(`sync:data — ${copied} copied, ${unchanged} already in sync (data/ → public/data/)`);
