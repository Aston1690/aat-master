// Headless Chromium helper for tools/design.py. Not run by hand.
//   node tools/render.mjs png <file.html> <out.png> <width> <height>
//   node tools/render.mjs pdfpage <file.html> <out.pdf> <width> <height>
//   node tools/render.mjs shots <file.html> <outdir> <viewport,viewport,...>   (e.g. desktop:1280,mobile:390,phone:360)
//   node tools/render.mjs fullpng <file.html|http://localhost:port/...> <out.png> <width>
//   node tools/render.mjs audit <file.html|http://localhost:port/...> <outdir> <widths> <prefix> [motion]
// Prints one JSON line with what it measured. Loads local files only (and the localhost server named as the target);
// any request to the internet is blocked, so a page that depends on something online fails loudly instead of
// rendering differently later.
import fs from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { chromium } from 'playwright-core';
import { resolveChromium } from './browser_path.mjs';

const [cmd, file, out, a, b] = process.argv.slice(2);
if (!cmd || !file || !out) { console.error('usage: see the top of tools/render.mjs'); process.exit(2); }
const exe = resolveChromium({ playwrightChromium: chromium }).path;
const browser = await chromium.launch({ executablePath: exe, headless: true });
const blocked = [];
const isUrl = /^https?:\/\//i.test(file);
const target = isUrl ? new URL(file) : null;
if (target && !['localhost', '127.0.0.1', '[::1]'].includes(target.hostname)) {
  console.log(JSON.stringify({ ok: false, error: 'only a local file or a localhost address can be opened', blocked }));
  process.exit(1);
}
const targetHref = isUrl ? file : pathToFileURL(path.resolve(file)).href;

async function open(width, height, scale = 1, options = {}) {
  const ctx = await browser.newContext({ viewport: { width, height }, deviceScaleFactor: scale, ...options });
  const page = await ctx.newPage();
  page._console = []; page._failed = [];
  page.on('console', (m) => { if (m.type() === 'error') page._console.push(m.text().slice(0, 300)); });
  page.on('pageerror', (e) => page._console.push('page error: ' + String(e && e.message || e).slice(0, 300)));
  page.on('requestfailed', (r) => { const u = r.url(); if (!blocked.includes(u)) page._failed.push(u.slice(0, 300)); });
  await page.route('**/*', (r) => {
    const u = r.request().url();
    if (u.startsWith('file:') || u.startsWith('data:') || u.startsWith('blob:')) return r.continue();
    if (target && new URL(u).host === target.host) return r.continue();
    blocked.push(u); return r.abort();
  });
  await page.goto(targetHref, { waitUntil: 'load' });
  await page.evaluate(async () => {
    await document.fonts.ready;
    await Promise.all([...document.images].map((i) => (i.complete ? null : new Promise((ok) => { i.onload = i.onerror = ok; }))));
  });
  return page;
}

async function measure(page) {
  return page.evaluate(() => {
    const d = document.documentElement;
    const broken = [...document.images].filter((i) => !i.naturalWidth).map((i) => i.getAttribute('src'));
    const fonts = [...document.fonts].map((f) => `${f.family} ${f.weight} ${f.status}`);
    const box = (sel) => { const e = document.querySelector(sel); if (!e) return null; const r = e.getBoundingClientRect(); return { x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height) }; };
    return { scrollWidth: d.scrollWidth, scrollHeight: d.scrollHeight, brokenImages: broken, fonts, cover: box('.cover'), avatar: box('.avatar'), heading: box('h1') };
  });
}

async function settle(page) {
  // Scroll through the page so lazy images and scroll-triggered reveals run, then back to the top.
  await page.evaluate(async () => {
    const step = Math.max(200, Math.floor(window.innerHeight * 0.7));
    for (let y = 0; y < document.documentElement.scrollHeight; y += step) {
      window.scrollTo(0, y);
      await new Promise((ok) => setTimeout(ok, 120));
    }
    window.scrollTo(0, 0);
  });
  await page.waitForTimeout(700);
  await page.evaluate(async () => {
    await document.fonts.ready;
    await Promise.all([...document.images].map((i) => (i.complete ? null : new Promise((ok) => { i.onload = i.onerror = ok; setTimeout(ok, 5000); }))));
  });
}

function auditDom(page) {
  return page.evaluate(() => {
    const vis = (el) => {
      if (!el.checkVisibility || !el.checkVisibility()) return 'none';
      const r = el.getBoundingClientRect();
      if (getComputedStyle(el).visibility === 'hidden') return 'none';
      if (!el.checkVisibility({ checkOpacity: true }) || r.width < 1 || r.height < 1 ||
          r.right <= 0 || r.bottom + window.scrollY <= 0 || el.closest('[aria-hidden="true"],[inert]')) return 'hidden';
      return 'shown';
    };
    const name = (el) => {
      const by = (el.getAttribute('aria-labelledby') || '').split(/\s+/).map((id) => document.getElementById(id)?.innerText || '').join(' ');
      const lab = el.labels ? [...el.labels].map((l) => l.innerText).join(' ') : '';
      const alt = [...el.querySelectorAll('img[alt],svg[aria-label]')].map((i) => i.getAttribute('alt') || i.getAttribute('aria-label')).join(' ');
      return (el.getAttribute('aria-label') || by || lab || el.innerText || el.value || el.getAttribute('title') || alt || el.getAttribute('placeholder') || '').trim();
    };
    const focusable = [...document.querySelectorAll('a[href],button,input,select,textarea,summary,[tabindex]')]
      .filter((el) => !el.disabled && el.tabIndex >= 0 && el.type !== 'hidden');
    const hiddenFocusable = focusable.filter((el) => vis(el) === 'hidden').map((el) => el.outerHTML.slice(0, 160));
    const unnamed = focusable.filter((el) => !el.matches('input,select,textarea') && vis(el) === 'shown' && !name(el)).map((el) => el.outerHTML.slice(0, 160));
    const links = [...document.querySelectorAll('a')].map((a) => ({ href: a.getAttribute('href'), text: (a.innerText || a.getAttribute('aria-label') || '').trim().slice(0, 80) }));
    const anchorsMissing = links.filter((l) => l.href && l.href.startsWith('#') && l.href.length > 1 && !document.getElementById(decodeURIComponent(l.href.slice(1)))).map((l) => l.href);
    const emptyLinks = links.filter((l) => !l.href || l.href === '#').map((l) => l.text || '(no text)');
    const imgsNoAlt = [...document.images].filter((i) => !i.hasAttribute('alt')).map((i) => i.getAttribute('src'));
    const imgsNoSize = [...document.images].filter((i) => !i.getAttribute('width') && !i.style.width && !i.style.aspectRatio).length;
    const meta = (n) => document.querySelector(`meta[name="${n}"]`)?.getAttribute('content') || null;
    return {
      title: document.title || null, description: meta('description'), lang: document.documentElement.lang || null,
      h1: [...document.querySelectorAll('h1')].map((h) => h.innerText.trim().slice(0, 120)),
      links, anchorsMissing, emptyLinks, imgsNoAlt, imgsNoSize, hiddenFocusable, unnamedControls: unnamed,
      inputsNoLabel: [...document.querySelectorAll('input:not([type=hidden]):not([type=submit]):not([type=button]),select,textarea')].filter((el) => !name(el)).map((el) => el.outerHTML.slice(0, 160)),
      forms: [...document.forms].map((f) => ({ action: f.getAttribute('action'), method: f.method })),
      scripts: [...document.scripts].map((x) => x.src || '(inline)'),
      text: document.body ? document.body.innerText.slice(0, 20000) : '',
    };
  });
}

try {
  if (cmd === 'fullpng') {
    const w = Number(a);
    if (!(w > 0)) throw new Error('width must be a number');
    const page = await open(w, 900);
    await settle(page);
    const m = await measure(page);
    await page.screenshot({ path: out, fullPage: true });
    console.log(JSON.stringify({ ok: true, file: out, width: w, height: m.scrollHeight, overflow: m.scrollWidth > w,
      console: page._console, failed: page._failed, ...m, blocked }));
  } else if (cmd === 'audit') {
    fs.mkdirSync(out, { recursive: true });
    const widths = (a || '1440,1024,768,390,320').split(',').map(Number);
    const prefix = b || 'page';
    const motion = process.argv[7] === 'motion';
    const pick = [widths[0], widths.includes(390) ? 390 : widths[widths.length - 1]];
    const runs = widths.map((w) => ['normal', w, {}])
      .concat([...new Set(pick)].map((w) => ['nojs', w, { javaScriptEnabled: false }]))
      .concat([...new Set(pick)].map((w) => ['reduced', w, { reducedMotion: 'reduce' }]));
    const views = []; let dom = null;
    for (const [mode, w, opts] of runs) {
      const page = await open(w, w >= 1024 ? 900 : 844, 1, opts);
      if (mode !== 'nojs') await settle(page);
      const m = await measure(page);
      const shot = path.join(out, `${prefix}-${mode}-${w}.png`);
      await page.screenshot({ path: shot, fullPage: true });
      if (mode === 'normal' && w === widths[0]) dom = await auditDom(page);
      if (mode === 'normal' && w === pick[1]) {
        const small = await auditDom(page);
        dom.hiddenFocusableNarrow = small.hiddenFocusable; dom.textNarrow = small.text.slice(0, 4000);
      }
      m.visibleText = await page.evaluate(() => {
        // characters of text that a reader can actually see (not hidden by opacity, visibility or display)
        let n = 0; const w = document.createTreeWalker(document.body || document.documentElement, NodeFilter.SHOW_TEXT);
        while (w.nextNode()) {
          const el = w.currentNode.parentElement; const t = w.currentNode.textContent.trim();
          if (t && el && el.checkVisibility({ checkOpacity: true, checkVisibilityCSS: true })) n += t.length;
        }
        return n;
      });
      if (motion && mode === 'normal' && pick.includes(w)) {
        const dir = path.join(out, 'motion'); fs.mkdirSync(dir, { recursive: true });
        await page.evaluate(() => window.scrollTo(0, 0));
        const total = m.scrollHeight; const vh = page.viewportSize().height; let k = 0;
        for (let y = 0; y < total && k < 24; y += Math.floor(vh * 0.6), k++) {
          await page.evaluate((yy) => window.scrollTo(0, yy), y);
          await page.waitForTimeout(450);
          await page.screenshot({ path: path.join(dir, `${prefix}-${w}-frame-${String(k + 1).padStart(2, '0')}.png`) });
        }
      }
      views.push({ mode, width: w, file: shot, overflow: m.scrollWidth > w, scrollWidth: m.scrollWidth,
        scrollHeight: m.scrollHeight, brokenImages: m.brokenImages, fonts: m.fonts, console: page._console,
        failed: page._failed, visibleText: m.visibleText });
      await page.context().close();
    }
    console.log(JSON.stringify({ ok: true, target: targetHref, views, dom, blocked }));
  } else if (cmd === 'png' || cmd === 'pdfpage') {
    const w = Number(a), h = Number(b);
    if (!(w > 0 && h > 0)) throw new Error('width and height must be numbers');
    const page = await open(w, h);
    const m = await measure(page);
    if (cmd === 'png') await page.screenshot({ path: out, clip: { x: 0, y: 0, width: w, height: h } });
    else await page.pdf({ path: out, width: `${w}px`, height: `${h}px`, printBackground: true, pageRanges: '1', margin: { top: 0, right: 0, bottom: 0, left: 0 } });
    console.log(JSON.stringify({ ok: true, file: out, width: w, height: h, overflow: m.scrollWidth > w || m.scrollHeight > h, ...m, blocked }));
  } else if (cmd === 'shots') {
    fs.mkdirSync(out, { recursive: true });
    const result = {};
    for (const spec of (a || 'desktop:1280,mobile:390,phone:360').split(',')) {
      const [name, width] = spec.split(':');
      const page = await open(Number(width), 900);
      const m = await measure(page);
      const shot = path.join(out, `${name}-${width}.png`);
      await page.screenshot({ path: shot, fullPage: true });
      result[name] = { width: Number(width), file: shot, ...m };
      await page.context().close();
    }
    console.log(JSON.stringify({ ok: true, views: result, blocked }));
  } else {
    throw new Error(`unknown command ${cmd}`);
  }
} catch (e) {
  console.log(JSON.stringify({ ok: false, error: String(e && e.message || e), blocked }));
  process.exitCode = 1;
} finally {
  await browser.close();
}
