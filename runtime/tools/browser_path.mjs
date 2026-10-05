// Shared Chromium resolver for tools/render.mjs (taken from the AA design kit).
// Order: explicit path (--chromium or config [paths] chromium) -> CHROMIUM_PATH ->
// Playwright's own chromium.executablePath() if that file exists -> newest chromium-* in any
// Playwright cache (macOS ~/Library/Caches/ms-playwright, Linux ~/.cache/ms-playwright,
// Windows %LOCALAPPDATA%\ms-playwright, or PLAYWRIGHT_BROWSERS_PATH).
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';

export function cacheRoots() {
  const roots = [];
  if (process.env.PLAYWRIGHT_BROWSERS_PATH && process.env.PLAYWRIGHT_BROWSERS_PATH !== '0') roots.push(process.env.PLAYWRIGHT_BROWSERS_PATH);
  roots.push(path.join(os.homedir(), 'Library/Caches/ms-playwright'));
  roots.push(path.join(os.homedir(), '.cache/ms-playwright'));
  if (process.env.LOCALAPPDATA) roots.push(path.join(process.env.LOCALAPPDATA, 'ms-playwright'));
  roots.push(path.join(os.homedir(), 'AppData', 'Local', 'ms-playwright'));
  return roots;
}

function binariesIn(dir) {
  // chrome-mac*/<App>.app/Contents/MacOS/<exe>, chrome-linux*/chrome, chrome-win/chrome.exe
  const out = [];
  let subs = [];
  try { subs = fs.readdirSync(dir); } catch { return out; }
  for (const s of subs.filter((n) => n.startsWith('chrome-'))) {
    const base = path.join(dir, s);
    let entries = [];
    try { entries = fs.readdirSync(base); } catch { continue; }
    for (const e of entries) {
      if (e.endsWith('.app')) {
        const macos = path.join(base, e, 'Contents', 'MacOS');
        try { for (const x of fs.readdirSync(macos)) out.push(path.join(macos, x)); } catch { /* ignore */ }
      } else if (e === 'chrome' || e === 'chrome.exe') {
        out.push(path.join(base, e));
      }
    }
  }
  return out.filter((p) => { try { return fs.statSync(p).isFile(); } catch { return false; } });
}

export function scanCaches(roots = cacheRoots()) {
  const found = [];
  for (const r of roots) {
    let names = [];
    try { names = fs.readdirSync(r); } catch { continue; }
    for (const n of names) {
      const m = /^chromium-(\d+)$/.exec(n);
      if (!m) continue;
      for (const b of binariesIn(path.join(r, n))) found.push({ rev: Number(m[1]), path: b });
    }
  }
  found.sort((a, b) => b.rev - a.rev);
  return found.map((f) => f.path);
}

// Returns { path, source } or throws with the list of places tried.
export function resolveChromium({ explicit = '', playwrightChromium = null } = {}) {
  const tried = [];
  const exists = (p) => { try { return !!p && fs.statSync(p).isFile(); } catch { return false; } };
  if (explicit) { if (exists(explicit)) return { path: explicit, source: 'explicit' }; tried.push(`explicit: ${explicit}`); }
  const env = process.env.CHROMIUM_PATH;
  if (env) { if (exists(env)) return { path: env, source: 'CHROMIUM_PATH' }; tried.push(`CHROMIUM_PATH: ${env}`); }
  if (playwrightChromium) {
    let own = '';
    try { own = playwrightChromium.executablePath(); } catch { /* ignore */ }
    if (exists(own)) return { path: own, source: 'playwright' };
    tried.push(`playwright executablePath(): ${own || 'unavailable'}`);
  }
  const cached = scanCaches();
  if (cached.length) return { path: cached[0], source: 'cache' };
  tried.push(`caches: ${cacheRoots().join(', ')}`);
  throw new Error('No Chromium found. Tried ' + tried.join('; ') +
    '. Fix: run npm exec --prefix runtime/tools -- playwright-core install chromium, or set CHROMIUM_PATH.');
}
