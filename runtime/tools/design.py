#!/usr/bin/env python3
"""Helper commands for the team's design skills. The skills decide the design; this only does the
mechanical parts the same way on every PC. Run from the repository root (on Windows use "py -3").

  py -3 tools/design.py status                                   is this PC ready?
  py -3 tools/design.py new <deliverable> --client <slug> [--options N] [--name <short name>]   (two variants by default)
  py -3 tools/design.py brief <case> --gdoc <Google Doc link>    saves the brief text into the case
  py -3 tools/design.py assets <client> --drive <folder link> | --folder <path>   brand files into clients/<client>/brand
  py -3 tools/design.py prototype <case> personal|business       banner only: copies the bundled prototype
  py -3 tools/design.py fonts <client> "Work Sans" "Lato" ...     Google Fonts families into clients/<client>/brand/fonts
                                                                 (from the team font library in fonts/, no download)
  py -3 tools/design.py fontlib list | add "<Family>" ...         the team font library (owner: add, then commit fonts/)
  py -3 tools/design.py png <file.html> <out.png> --size 1080x1350   (sizes: WxH, A4, A4-landscape, letter, 16:9)
  py -3 tools/design.py pdf <out.pdf> --size 1080x1350 --title "..." --author "..." <slide-01.html> <slide-02.html> ...
  py -3 tools/design.py preview <option-N/preview/index.html>    banner: desktop, mobile and phone views + geometry
  py -3 tools/design.py fullpng <page.html> <out.png> --width 640   the whole page as one PNG (email concept, pages)
  py -3 tools/design.py pagecheck <page.html|http://localhost:port/...> ... [--widths 1440,1024,768,390,320] [--motion]
                                                                 landing page, website, email: full-page screenshots at
                                                                 every width, JavaScript off, reduced motion, links,
                                                                 hidden focus, labels, console errors
  py -3 tools/design.py emailcheck <newsletter.html> [--text newsletter.txt] [--production]   email mechanics
  py -3 tools/design.py site <case>                              banner: local review site, Banner 1 / Banner 2 ...
  py -3 tools/design.py inspect <files...> [--size WxH] [--max-bytes N] [--format png|jpeg|pdf]
  py -3 tools/design.py sheet <out.png> <images...>              contact sheet (a review aid only)
  py -3 tools/design.py review <case>                            independent Codex review of every option

Pictures: tools/codex_image.py. Nothing here uploads, posts, deploys or sends anything.
"""
import argparse
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import tomllib
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / '.agents' / 'skills'
DELIVERABLES = ('linkedin-banner', 'linkedin-static', 'linkedin-carousel', 'bip', 'email-newsletter',
                'landing-page-director', 'website')
PAGE_DELIVERABLES = ('landing-page-director', 'website')
OPTION_FOLDERS = {
    'linkedin-banner': ('source', 'images', 'exports', 'assets', 'preview', 'previews'),
    'linkedin-static': ('source', 'images', 'exports', 'assets'),
    'linkedin-carousel': ('source', 'images', 'exports', 'assets'),
    'bip': ('source', 'images', 'exports', 'assets'),
    'email-newsletter': ('source', 'images', 'exports', 'assets', 'previews', 'checks'),
    'landing-page-director': ('site', 'images', 'exports', 'previews', 'checks'),
    'website': ('site', 'images', 'exports', 'previews', 'checks'),
}
PAGE_SIZES = {'a4': (794, 1123), 'a4-landscape': (1123, 794), 'letter': (816, 1056), 'letter-landscape': (1056, 816),
              '16:9': (1920, 1080), 'slides': (1920, 1080)}
sys.path.insert(0, str(ROOT / 'tools'))



class Stop(Exception):
    pass


def now():
    return dt.datetime.now().astimezone().isoformat(timespec='seconds')


def config():
    with open(ROOT / 'config.toml', 'rb') as fh:
        return tomllib.load(fh)


def work_root():
    return Path(os.environ.get('AA_WORK_DIR') or (ROOT / 'work'))


def slug(text):
    s = re.sub(r'[^a-z0-9]+', '-', str(text).lower()).strip('-')
    if not s:
        raise Stop(f'cannot make a folder name from {text!r}')
    return s[:60]


def size(text):
    if (text or '').strip().lower() in PAGE_SIZES:
        return PAGE_SIZES[text.strip().lower()]
    m = re.fullmatch(r'\s*(\d+)\s*[xX]\s*(\d+)\s*', text or '')
    if not m:
        raise Stop('--size must look like 1080x1350, or A4, A4-landscape, letter, letter-landscape, 16:9')
    return int(m.group(1)), int(m.group(2))


def case_dir(arg):
    p = Path(arg)
    for c in (p, ROOT / p, work_root() / p):
        if (c / 'case.json').is_file():
            return c.resolve()
    raise Stop(f'no case folder at {arg} (it should contain case.json; "new" makes one)')


def load_case(c):
    return json.loads((c / 'case.json').read_text(encoding='utf-8'))


def save_case(c, data):
    (c / 'case.json').write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def node():
    exe = shutil.which('node')
    if not exe:
        raise Stop('Node.js is not installed or not on PATH. Run install\\install.ps1.')
    if not (ROOT / 'tools' / 'node_modules' / 'playwright-core').is_dir():
        raise Stop('the browser helper is not installed. Run install\\install.ps1 (it runs npm ci in tools).')
    return exe


def render(*args):
    r = subprocess.run([node(), str(ROOT / 'tools' / 'render.mjs'), *map(str, args)], capture_output=True, text=True,
                       encoding='utf-8', errors='replace', cwd=str(ROOT))
    line = (r.stdout or '').strip().splitlines()[-1:] or ['']
    try:
        data = json.loads(line[0])
    except json.JSONDecodeError:
        raise Stop(f'the browser helper failed: {(r.stderr or r.stdout).strip()[-600:]}') from None
    if not data.get('ok'):
        raise Stop(f'the browser helper failed: {data.get("error")}')
    return data


# ---------------------------------------------------------------- new case

NOTES_TEMPLATE = """# Case notes: {deliverable} for {client}

Created {created}. The skill asks for these records. Fill every line; write "unresolved" rather than guess.

## Request and scope
- Deliverable and scope (full production, or audit / prompt / specification only):
- Destination (banner: personal profile, Company Page or Group) and the evidence for it:
- Audience, objective, intended impression:
- Variants: {options} (team default is two; say if the designer or a numbered brief changed it):
- Posts or slides per variant, and where that number comes from:

## Specification
- Canvas (pixels), final format, byte limit:
- Source of the specification and the date checked (or "brief-supplied, unverified"):

## Sources
- Brief source (link or file) and date read:
- Approved copy source:
- Brand assets used (file, where it came from, sha256 from "design.py inspect"):
- Supplied imagery:

## Option, copy and export checklist
| Variant (option) | Assigned copy (exact) | Visual thesis (idea or composition, not colour) | Export file(s) | Preview |
|---|---|---|---|---|

## Image plan (one line per picture: option, post or slide, subject, role, source or prompt, saved path, crop)

## Unresolved items and claims to flag

## QA record (agent QA, Codex review, human approval and upload are recorded separately)
- Agent QA:
- Codex review:
- Preview geometry calibrated or simulated:
- Human designer review: not yet
- Actual upload checked: no (never uploaded by an agent)
"""

NOTES_TEMPLATE_OTHER = """# Case notes: {deliverable} for {client}

Created {created}. The skill asks for these records. Fill every line; write "unresolved" rather than guess.

## Request and scope
- Deliverable and scope (full production, or audit / prompt / specification only):
- Task mode (new design, redesign, clone or approved-template adaptation, scoped edit) and the evidence for it:
- Audience, purpose, primary action:
- Requested output inventory: every deliverable asked for, with its copy source, format, destination and expected
  file name or route (the handover is checked against this list):
- Variants: {options}, and where the count came from (the designer's message, a numbered brief, or the standing team
  instruction: two for a new design, one for a clone, template adaptation or narrow edit):
- What one variant contains (pages and routes, sections, the issue, the page or slide count) and where that comes from:

## Specification
- Format: document or slides and page size, print needs and printer specification (BIP); concept, production email or
  both, sending platform, subject and preheader (newsletter); routes, existing stack, build/lint/test commands and the
  widths checked (landing page, website):
- Source of each requirement and the date checked (or "brief-supplied, unverified"):

## Links, forms and deployment (landing page, website)
- Every call to action, navigation and footer link and download, with its exact destination or "not supplied":
- Each form: where submissions go, field mapping, consent copy, confirmation behaviour, authorised test destination,
  or "not supplied: prototype":
- Vercel team, project and target (preview or production), who authorised it and when, or "not authorised":
- Delivery scope in this repository: local build. A person deploys and does the live checks; agents never deploy.
- Dependencies: which optional specialist skills were available, and the fallback used (.agents/skills/DEPENDENCIES.md):

## Sources
- Brief source (link or file) and date read:
- Approved copy source and the evidence that it is approved:
- Brand assets used (file, where it came from, sha256 from "design.py inspect"), fonts and their licences:
- Supplied imagery:

## Option checklist
| Variant (option) | Visual thesis (idea or composition, not colour) | Source (editable) | Exports and screenshots |
|---|---|---|---|

## Image and reference plan
One line per picture or section reference: option, use, subject, prompt, saved path, crop; for references, whether
agent-selected or user-approved.

## Unresolved items and claims to flag

## QA record (agent QA, Codex review, human approval and any sending or publishing are recorded separately)
- Agent QA (pass, fail, not tested or not applicable per REVIEW.md item, with evidence):
- Checks run (build, type, lint, tests; design.py pagecheck widths; design.py emailcheck; PDF reopened):
- Email-client tests (client, version or service, date, result) or "not tested":
- Motion watched by a person in a real browser (desktop, phone, reduced motion) or "not tested":
- Codex review:
- Human designer review: not yet
- Sent, deployed or published: no (never by an agent)
"""


def cmd_new(a):
    if a.deliverable not in DELIVERABLES:
        raise Stop(f'deliverable must be one of {", ".join(DELIVERABLES)}')
    if a.options < 1 or a.options > 10:
        raise Stop('--options must be between 1 and 10')
    client = slug(a.client)
    base = work_root() / client
    name = dt.date.today().strftime('%Y%m%d') + '-' + a.deliverable + (f'-{slug(a.name)}' if a.name else '')
    c = base / name
    n = 2
    while c.exists():
        c = base / f'{name}-{n}'
        n += 1
    for sub in ('brief', 'review'):
        (c / sub).mkdir(parents=True)
    for i in range(1, a.options + 1):
        for sub in OPTION_FOLDERS[a.deliverable]:
            (c / f'option-{i}' / sub).mkdir(parents=True)
    save_case(c, {'deliverable': a.deliverable, 'client': client, 'options': a.options, 'created': now(), 'round': 0,
                  'reviews': []})
    template = NOTES_TEMPLATE if a.deliverable.startswith('linkedin-') else NOTES_TEMPLATE_OTHER
    (c / 'case-notes.md').write_text(template.format(deliverable=a.deliverable, client=client, created=now(), options=a.options),
                                     encoding='utf-8')
    brand = ROOT / 'clients' / client / 'brand'
    print(f'Case folder: {c}')
    print(f'Options: {a.options}. Skill: .agents/skills/{a.deliverable}/SKILL.md and REVIEW.md')
    if not brand.is_dir():
        print(f'Note: no brand folder yet at {brand}. Put the client\'s verified logo files, fonts and brand guide there '
              '(copied unchanged), or record in case-notes.md where they came from.')
    return 0


def cmd_brief(a):
    c = case_dir(a.case)
    m = re.search(r'/document/d/([A-Za-z0-9_-]+)', a.gdoc)
    if not m:
        raise Stop('that is not a Google Doc link')
    url = f'https://docs.google.com/document/d/{m.group(1)}/export?format=txt'
    tab = re.search(r'tab=(t\.[A-Za-z0-9_-]+)', a.gdoc)
    if tab:
        url += f'&tab={tab.group(1)}'
    try:
        with urllib.request.urlopen(url, timeout=60) as r:
            text = r.read().decode('utf-8', 'replace')
    except Exception as exc:  # noqa: BLE001
        raise Stop(f'could not read the Google Doc ({exc}). Share it as "Anyone with the link can view", or save the '
                   'brief text into the case as brief/brief-source.txt') from None
    if '<html' in text[:500].lower():
        raise Stop('Google returned a sign-in page. Share the doc as "Anyone with the link can view", or save the brief '
                   'text into brief/brief-source.txt')
    out = c / 'brief' / 'brief-source.txt'
    with open(out, 'a', encoding='utf-8') as fh:
        fh.write(f'[Source: {a.gdoc}, read {now()}]\n{text.strip()}\n\n')
    print(f'Brief text saved to {out} ({len(text)} characters). Copy the client\'s words from it exactly.')
    return 0


ASSET_EXT = {'.png', '.svg', '.jpg', '.jpeg', '.webp', '.gif', '.ttf', '.otf', '.woff', '.woff2', '.pdf', '.txt', '.md',
             '.docx', '.ai', '.eps', '.psd'}


def _safe_part(name):
    """Windows cannot keep a trailing space or dot in a folder or file name, and a few characters are not allowed at
    all; Drive allows them. Make each path part safe, keeping it recognisable."""
    name = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '_', name).rstrip(' .')
    return name or '_'


def drive_download(url, target):
    """Downloads a public Drive folder file by file (gdown), with Windows-safe names. Files are copied unchanged."""
    try:
        import gdown
    except ImportError:
        raise Stop('the Drive helper is not installed. Run: py -3 -m pip install --user -r requirements.txt') from None
    try:
        listing = gdown.download_folder(url=url, output=str(target), quiet=True, skip_download=True,
                                        remaining_ok=True)
    except Exception as exc:  # noqa: BLE001
        raise Stop('could not read the Drive folder. Share it as "Anyone with the link can view", or download it by hand '
                   f'and use --folder. ({str(exc)[-300:]})') from None
    if not listing:
        raise Stop('the Drive folder looks empty, or it is not shared as "Anyone with the link can view"')
    target.mkdir(parents=True, exist_ok=True)
    failed = []
    for item in listing:
        rel = Path(item.path.replace('\\', '/'))
        dest = target.joinpath(*[_safe_part(x) for x in rel.parts])
        dest.parent.mkdir(parents=True, exist_ok=True)
        try:
            gdown.download(id=item.id, output=str(dest), quiet=True)
        except Exception:  # noqa: BLE001
            failed.append(str(rel))
    if failed:
        print(f'Note: {len(failed)} Drive file(s) could not be downloaded: {failed[:10]}')


def cmd_assets(a):
    """Copies the client's files unchanged into clients/<client>/brand/source/ and lists each one in SOURCES.md
    (where it came from, when, size, sha256). It chooses nothing: the main thread and the designer decide which file
    is the logo, the portrait or supplied imagery."""
    import hashlib
    client = slug(a.client)
    brand = ROOT / 'clients' / client / 'brand'
    src_root = brand / 'source'
    src_root.mkdir(parents=True, exist_ok=True)
    rows = []
    with tempfile.TemporaryDirectory() as tmp:
        pulls = []
        for url in a.drive:
            target = Path(tmp) / f'drive-{len(pulls)}'
            drive_download(url, target)
            pulls.append((target, url))
        for folder in a.folder:
            f = Path(folder).expanduser()
            if not f.is_dir():
                raise Stop(f'no folder {f}')
            pulls.append((f, str(f)))
        for base, origin in pulls:
            for p in sorted(base.rglob('*')):
                if not p.is_file() or p.suffix.lower() not in ASSET_EXT:
                    continue
                rel = p.relative_to(base)
                dest = src_root / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(p, dest)
                rows.append((str(dest.relative_to(brand)).replace('\\', '/'), origin, dest.stat().st_size,
                             hashlib.sha256(dest.read_bytes()).hexdigest()[:16]))
    if not rows:
        raise Stop('no image, font or document files found in that source')
    sources = brand / 'SOURCES.md'
    new = not sources.exists()
    with open(sources, 'a', encoding='utf-8') as fh:
        if new:
            fh.write(f'# Brand sources for {client}\n\nFiles copied unchanged. Nothing here has been chosen or verified yet.\n\n'
                     '| File | Where it came from | Copied | Bytes | sha256 (first 16) |\n|---|---|---|---|---|\n')
        for f, origin, size, sha in rows:
            fh.write(f'| {f} | {origin} | {now()} | {size} | {sha} |\n')
    print(f'Copied {len(rows)} files into {src_root}. Listed in {sources}.')
    for f, *_ in rows[:40]:
        print(f'  {f}')
    print('Nothing is chosen yet: look at the files, then record in case-notes.md which is the logo, portrait, fonts and '
          'imagery, and ask the designer where it is unclear.')
    return 0


FONT_LIB = ROOT / 'fonts'                    # the team font library, in the repository (shared through GitHub)
FONT_CACHE = FONT_LIB / '_downloaded'        # families this PC had to download; kept here, never downloaded again
FONT_LICENCES = ('OFL.txt', 'LICENSE.txt', 'UFL.txt')
FONT_EXT = ('.ttf', '.otf', '.woff2', '.woff')


def font_key(family):
    return re.sub(r'[^a-z0-9]', '', family.lower())


def font_files(folder):
    return sorted(p for p in folder.iterdir() if p.suffix.lower() in FONT_EXT) if folder.is_dir() else []


def find_font(family):
    """The folder holding this family on this PC (the team library first, then this PC's own downloads), or None."""
    for base, where in ((FONT_LIB, 'in the team font library'), (FONT_CACHE, 'in this PC\'s font downloads')):
        d = base / font_key(family)
        if font_files(d):
            return d, where
    return None, None


def google_font_download(family, dest):
    """Official files for one Google Fonts family from the google/fonts repository, unchanged, with its licence and
    METADATA.pb, into dest/. Returns False when the family is not on Google Fonts."""
    key = font_key(family)
    base = meta = None
    for lic in ('ofl', 'apache', 'ufl'):
        url = f'https://raw.githubusercontent.com/google/fonts/main/{lic}/{key}/METADATA.pb'
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                meta = r.read().decode('utf-8')
            base = url.rsplit('/', 1)[0]
            break
        except Exception:  # noqa: BLE001
            continue
    if not meta:
        return False
    tmp = dest.with_name(dest.name + '.part')
    shutil.rmtree(tmp, ignore_errors=True)
    tmp.mkdir(parents=True)
    names = sorted(set(re.findall(r'filename:\s*"([^"]+)"', meta)))
    got = 0
    for name in names + list(FONT_LICENCES):
        try:
            with urllib.request.urlopen(f'{base}/{urllib.request.quote(name)}', timeout=120) as r:
                data = r.read()
        except Exception:  # noqa: BLE001
            if name in names:
                shutil.rmtree(tmp, ignore_errors=True)
                raise Stop(f'could not download {name} for {family}; check the internet connection and run it again') from None
            continue  # only one of the licence names exists for each family
        (tmp / name.replace('[', '_').replace(']', '_')).write_bytes(data)
        got += name in names
    (tmp / 'METADATA.pb').write_text(meta, encoding='utf-8')
    display = (re.search(r'^name:\s*"([^"]+)"', meta, re.M) or [None, family])[1]
    (tmp / 'SOURCE.txt').write_text(f'{display}\nOfficial Google Fonts files, unchanged, from {base}/\n'
                                    f'Downloaded {now()}. Licence file in this folder.\n', encoding='utf-8')
    shutil.rmtree(dest, ignore_errors=True)
    tmp.rename(dest)
    return got > 0


def write_font_index():
    rows = []
    for d in sorted(p for p in FONT_LIB.iterdir() if p.is_dir() and not p.name.startswith('_')):
        meta = (d / 'METADATA.pb').read_text(encoding='utf-8') if (d / 'METADATA.pb').exists() else ''
        name = (re.search(r'^name:\s*"([^"]+)"', meta, re.M) or [None, d.name])[1]
        lic = (re.search(r'^license:\s*"([^"]+)"', meta, re.M) or [None, '?'])[1]
        files = ', '.join(f.name for f in font_files(d))
        rows.append(f'| {name} | `fonts/{d.name}/` | {lic} | {files} |')
    (FONT_LIB / 'INDEX.md').write_text(
        '# Team font library\n\nOfficial Google Fonts files, unchanged, each folder with its licence (all open licences '
        'that allow sharing), METADATA.pb and SOURCE.txt.\n`py -3 tools/design.py fonts <client> "<Family>"` copies a '
        'family from here into the client\'s brand folder with no download.\nAdd a family for everyone: '
        '`py -3 tools/design.py fontlib add "<Family>"`, then commit `fonts/` through a pull request.\n\n'
        '| Family | Folder | Licence | Files |\n|---|---|---|---|\n' + '\n'.join(rows) + '\n', encoding='utf-8')
    return len(rows)


def cmd_fonts(a):
    """Puts Google Fonts families into clients/<client>/brand/fonts/ with their licences, listed in SOURCES.md. It
    takes them from the team font library (fonts/) with no download; a family not in the library is downloaded once
    from the official google/fonts repository into fonts/_downloaded/ and kept there for every later job on this PC.
    A brand font that is not on Google Fonts must come from the client."""
    import hashlib
    client = slug(a.client)
    dest = ROOT / 'clients' / client / 'brand' / 'fonts'
    dest.mkdir(parents=True, exist_ok=True)
    rows, missing, downloaded = [], [], []
    for family in a.families:
        folder, where = find_font(family)
        if not folder:
            folder = FONT_CACHE / font_key(family)
            if not google_font_download(family, folder):
                missing.append(family)
                continue
            where = 'downloaded now (once) and kept in this PC\'s font downloads'
            downloaded.append(family)
        origin = (folder / 'SOURCE.txt').read_text(encoding='utf-8').splitlines()[1] if (folder / 'SOURCE.txt').exists() else ''
        for f in font_files(folder) + [folder / n for n in FONT_LICENCES if (folder / n).exists()]:
            name = f'{font_key(family)}-{f.name}' if f.name in FONT_LICENCES else f.name
            shutil.copyfile(f, dest / name)
            data = (dest / name).read_bytes()
            rows.append((f'fonts/{name}', f'{folder.relative_to(ROOT).as_posix()}/ ({where}); {origin}', len(data),
                         hashlib.sha256(data).hexdigest()[:16]))
        print(f'{family}: {where} ({folder.relative_to(ROOT).as_posix()}/)')
    if rows:
        sources = dest.parent / 'SOURCES.md'
        new = not sources.exists()
        with open(sources, 'a', encoding='utf-8') as fh:
            if new:
                fh.write(f'# Brand sources for {client}\n\n| File | Where it came from | Copied | Bytes | sha256 (first 16) |\n'
                         '|---|---|---|---|---|\n')
            for f, origin, size, sha in rows:
                fh.write(f'| {f} | {origin} | {now()} | {size} | {sha} |\n')
        print(f'Copied {len(rows)} font and licence files into {dest}:')
        for f, *_ in rows:
            print(f'  {f}')
        print('A file with "_wght_" in its name is a variable font: declare it once with font-weight 100 900.')
    if downloaded:
        print(f'Kept on this PC for next time: {", ".join(downloaded)}. To share with the team, the owner runs '
              f'py -3 tools/design.py fontlib add "{downloaded[0]}" and commits fonts/.')
    if missing:
        print(f'NOT on Google Fonts (ask the client for the files): {", ".join(missing)}')
    return 1 if missing else 0


def cmd_fontlib(a):
    """Lists the team font library, or adds Google Fonts families to it (for the repository owner, who then commits
    fonts/ through a pull request so every PC gets them with git pull)."""
    FONT_LIB.mkdir(exist_ok=True)
    if a.action == 'add':
        missing = []
        for family in a.families:
            key = font_key(family)
            cached = FONT_CACHE / key
            if font_files(FONT_LIB / key):
                print(f'{family}: already in the library')
            elif font_files(cached):
                shutil.move(str(cached), str(FONT_LIB / key))
                print(f'{family}: moved from this PC\'s downloads into the library')
            elif google_font_download(family, FONT_LIB / key):
                print(f'{family}: added')
            else:
                missing.append(family)
        if missing:
            print(f'NOT on Google Fonts: {", ".join(missing)}')
    n = write_font_index()
    have = sorted(p.name for p in FONT_LIB.iterdir() if p.is_dir() and not p.name.startswith('_') and font_files(p))
    extra = sorted(p.name for p in FONT_CACHE.iterdir() if font_files(p)) if FONT_CACHE.is_dir() else []
    print(f'Team font library: {n} families ({", ".join(have)}). List: fonts/INDEX.md')
    if extra:
        print(f'Also on this PC only (fonts/_downloaded): {", ".join(extra)}')
    return 0


def cmd_prototype(a):
    c = case_dir(a.case)
    case = load_case(c)
    if case['deliverable'] != 'linkedin-banner':
        raise Stop('prototypes are for linkedin-banner cases only')
    src = SKILLS / 'linkedin-banner' / 'assets' / 'prototypes'
    for i in range(1, case['options'] + 1):
        dest = c / f'option-{i}' / 'preview'
        if (dest / 'index.html').exists():
            print(f'option-{i}/preview/index.html already exists; left as it is')
            continue
        dest.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src / f'{a.destination}.html', dest / 'index.html')
        shutil.copyfile(src / 'styles.css', dest / 'styles.css')
        shutil.copytree(src / 'assets', dest / 'assets', dirs_exist_ok=True)
    case['prototype'] = a.destination
    save_case(c, case)
    print(f'The {a.destination} prototype is in option-N/preview/ for every option (index.html, styles.css, assets/). '
          'Put the final export and the real portrait or company logo in that preview/assets/ folder and point '
          'index.html at them, so each preview folder stands on its own.')
    return 0


# ---------------------------------------------------------------- rendering

def cmd_png(a):
    w, h = size(a.size)
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    d = render('png', a.html, out, w, h)
    report(d, a.html)
    print(f'Saved {out} ({w}x{h}). Look at it at full size and at phone size before you go on.')
    return 1 if (d['brokenImages'] or d['blocked'] or d['overflow']) else 0


def report(d, what):
    if d.get('brokenImages'):
        print(f'PROBLEM in {what}: images that did not load: {d["brokenImages"]}')
    if d.get('blocked'):
        print(f'PROBLEM in {what}: it asks for files on the internet, which are blocked (put them in the case): {d["blocked"][:5]}')
    if d.get('overflow'):
        print(f'PROBLEM in {what}: the page is larger than the canvas ({d["scrollWidth"]}x{d["scrollHeight"]}); '
              'something runs past the edge')
    bad_fonts = [f for f in d.get('fonts', []) if not f.endswith('loaded')]
    if bad_fonts:
        print(f'PROBLEM in {what}: fonts not loaded: {bad_fonts}. The brand font must be a local file in the case.')


def cmd_pdf(a):
    from pypdf import PdfReader, PdfWriter
    w, h = size(a.size)
    if not a.html:
        raise Stop('list the slide HTML files in order')
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    writer = PdfWriter()
    problems = 0
    with tempfile.TemporaryDirectory() as tmp:
        for i, page in enumerate(a.html, 1):
            one = Path(tmp) / f'{i:03d}.pdf'
            d = render('pdfpage', page, one, w, h)
            report(d, page)
            problems += bool(d['brokenImages'] or d['blocked'] or d['overflow'])
            r = PdfReader(str(one))
            if len(r.pages) != 1:
                raise Stop(f'{page} made {len(r.pages)} PDF pages instead of 1; something runs past the canvas')
            pg = r.pages[0]
            # Chrome rounds the page height up to a whole point (1350 px = 1012.5 pt becomes 1013.04 pt). Trim the
            # blank sliver at the bottom so the page is exactly the canvas: 1 px = 0.75 pt.
            from pypdf.generic import RectangleObject
            top = float(pg.mediabox.top)
            box = RectangleObject([0, top - h * 0.75, w * 0.75, top])
            pg.mediabox = box
            pg.cropbox = box
            writer.add_page(pg)
        meta = {}
        if a.title:
            meta['/Title'] = a.title
        if a.author:
            meta['/Author'] = a.author
        writer.add_metadata(meta)
        with open(out, 'wb') as fh:
            writer.write(fh)
    info = pdf_info(out)
    print(f'Saved {out}: {info["pages"]} pages, live text on {info["pages_with_text"]} of them. '
          'Reopen it and compare every page with its PNG.')
    return 1 if problems else 0


def cmd_preview(a):
    html = Path(a.html).resolve()
    if not html.is_file():
        raise Stop(f'no file {html}')
    out = Path(a.out).resolve() if a.out else html.parent.parent / 'previews'
    d = render('shots', html, out, a.views)
    geometry = {'made': now(), 'preview': str(html), 'kind': 'simulation from the bundled prototype, not measured on '
                'LinkedIn', 'views': {}}
    for name, v in d['views'].items():
        report(v, f'{html.name} at {v["width"]} px')
        geometry['views'][name] = {k: v.get(k) for k in ('width', 'file', 'cover', 'avatar', 'heading', 'brokenImages')}
    (out / 'geometry.json').write_text(json.dumps(geometry, indent=2) + '\n', encoding='utf-8')
    print(f'Saved {", ".join(Path(v["file"]).name for v in d["views"].values())} and geometry.json in {out}. '
          'Look at every view: essential words, logo and subject clear of the profile image and the crop.')
    return 0


def option_folder(path):
    """The option-N folder a file belongs to, or None."""
    for parent in Path(path).resolve().parents:
        if re.fullmatch(r'option-\d+', parent.name):
            return parent
    return None


def cmd_fullpng(a):
    """The whole page as one PNG at one width (email concept exports, full landing page captures)."""
    w = int(a.width)
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    d = render('fullpng', a.target, out, w)
    report(d, a.target)
    for msg in d.get('console', []):
        print(f'PROBLEM in {a.target}: browser console error: {msg}')
    print(f'Saved {out} ({w}x{d["height"]}). Look at the whole length, including the CTA and footer.')
    return 1 if (d['brokenImages'] or d['blocked'] or d['overflow'] or d.get('console')) else 0


def page_prefix(target):
    if re.match(r'https?://', target, re.I):
        from urllib.parse import urlparse
        route = urlparse(target).path.strip('/')
    else:
        parts = Path(target).resolve().parts
        route = '/'.join(parts[parts.index('site') + 1:]) if 'site' in parts else Path(target).name
        route = re.sub(r'(^|/)index\.html?$', '', route)
        route = re.sub(r'\.html?$', '', route)
    return slug(route) if route.strip('/') else 'home'


def cmd_pagecheck(a):
    """Opens each page in headless Chromium at every width (1440, 1024, 768, 390, 320 by default), full-page, after
    scrolling through it so lazy images and reveals run; then once with JavaScript off and once with reduced motion at
    the widest and the 390 px width. Saves the screenshots (option-N/previews/) and every measurement
    (option-N/checks/<page>.json), and prints a PROBLEM line for each mechanical defect it can see. It does not judge
    design and does not watch motion: a person still watches the real page."""
    bad = 0
    for target in a.targets:
        is_url = bool(re.match(r'https?://', target, re.I))
        if not is_url and not Path(target).is_file():
            raise Stop(f'no file {target}')
        opt = None if is_url else option_folder(target)
        out = Path(a.out) if a.out else (opt / 'previews' if opt else Path(target).resolve().parent / 'previews')
        out_opt = option_folder(out / 'x')
        checks = (out_opt / 'checks') if out_opt else (out.parent / 'checks')
        checks.mkdir(parents=True, exist_ok=True)
        prefix = a.name or page_prefix(target)
        args = ['audit', target, out, a.widths, prefix] + (['motion'] if a.motion else [])
        d = render(*args)
        problems = []
        normal_len = max([v.get('visibleText') or 0 for v in d['views'] if v['mode'] == 'normal'] or [0])
        seen = {}  # the same defect at several widths or modes is one line
        for v in d['views']:
            where = f'{v["mode"]} {v["width"]}'
            found = []
            if v['overflow']:
                found.append(f'the page is wider than the window ({v["scrollWidth"]} px): something runs past the edge, '
                             'so the page scrolls sideways')
            if v['brokenImages']:
                found.append(f'images that did not load: {v["brokenImages"][:5]}')
            bad_fonts = [f for f in v.get('fonts', []) if not f.endswith('loaded')]
            if bad_fonts and v['mode'] != 'nojs':
                found.append(f'fonts not loaded: {bad_fonts[:5]}')
            if v['console'] and v['mode'] != 'nojs':
                found.append(f'browser console errors: {v["console"][:3]}')
            if v['failed']:
                found.append(f'requests that failed: {v["failed"][:3]}')
            if v['mode'] == 'nojs' and normal_len and (v.get('visibleText') or 0) < 0.6 * normal_len:
                found.append(f'with JavaScript off only {v.get("visibleText")} of about {normal_len} characters of text '
                             'are visible; critical content must not depend on a script')
            for f in found:
                seen.setdefault(f, []).append(where)
        for f, wheres in seen.items():
            problems.append(f'{prefix}: {f} (at {", ".join(wheres)} px)')
        dom = d.get('dom') or {}
        if d.get('blocked'):
            problems.append(f'{prefix}: asks for files on the internet, which are blocked (keep fonts, images and '
                            f'scripts inside the site): {sorted(set(d["blocked"]))[:5]}')
        if dom.get('anchorsMissing'):
            problems.append(f'{prefix}: links to anchors that do not exist on the page: {dom["anchorsMissing"][:10]}')
        if dom.get('emptyLinks'):
            problems.append(f'{prefix}: links with no destination (empty or "#"): {dom["emptyLinks"][:10]}')
        if dom.get('hiddenFocusable') or dom.get('hiddenFocusableNarrow'):
            hid = sorted(set((dom.get('hiddenFocusable') or []) + (dom.get('hiddenFocusableNarrow') or [])))
            problems.append(f'{prefix}: hidden elements that keyboard focus still reaches (a closed menu, for example; '
                            f'a skip link that appears on focus is fine): {hid[:5]}')
        if dom.get('unnamedControls'):
            problems.append(f'{prefix}: links or buttons with no accessible name: {dom["unnamedControls"][:5]}')
        if dom.get('inputsNoLabel'):
            problems.append(f'{prefix}: form fields with no label: {dom["inputsNoLabel"][:5]}')
        if dom.get('imgsNoAlt'):
            problems.append(f'{prefix}: images with no alt attribute: {dom["imgsNoAlt"][:5]}')
        if len(dom.get('h1') or []) != 1:
            problems.append(f'{prefix}: {len(dom.get("h1") or [])} h1 headings (expected exactly one)')
        if not dom.get('title'):
            problems.append(f'{prefix}: no page title')
        if not dom.get('lang'):
            problems.append(f'{prefix}: no lang attribute on <html>')
        missing_local, external = [], []
        for link in dom.get('links') or []:
            href = (link.get('href') or '').strip()
            if not href or href.startswith(('#', 'mailto:', 'tel:', 'javascript:', 'data:')):
                continue
            if re.match(r'(https?:)?//', href, re.I):
                external.append(href)
                continue
            if is_url:
                continue
            path = href.split('#')[0].split('?')[0]
            if not path:
                continue
            dest = (Path(target).resolve().parent / urllib.request.url2pathname(path)).resolve()
            if path.endswith('/') or dest.is_dir():
                dest = dest / 'index.html'
            if not dest.exists():
                missing_local.append(href)
        if missing_local:
            problems.append(f'{prefix}: links to local pages or files that do not exist: {missing_local[:10]}')
        record = {'checked': now(), 'target': d.get('target'), 'widths': a.widths, 'views': d['views'], 'dom': dom,
                  'external_links': sorted(set(external)), 'missing_local_links': missing_local,
                  'blocked': sorted(set(d.get('blocked') or [])), 'problems': problems,
                  'not_checked_here': ['colour contrast', 'motion quality (a person watches the real page)',
                                       'menus and forms operated by hand', 'email clients', 'design quality']}
        (checks / f'{prefix}.json').write_text(json.dumps(record, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
        shots = sorted({Path(v['file']).name for v in d['views']})
        print(f'{prefix}: {len(shots)} full-page screenshots in {out}; measurements in {checks / (prefix + ".json")}')
        if external:
            print(f'  external links to confirm against the brief: {sorted(set(external))[:12]}')
        if a.motion:
            print(f'  scroll frames in {out / "motion"} (still frames do not prove motion works; a person watches it)')
        for msg in problems:
            print(f'PROBLEM {msg}')
        bad += bool(problems)
    print('Look at every screenshot yourself: the full length at every width, the hero, the final CTA and the footer.')
    return 1 if bad else 0


EMAIL_TAGS = re.compile(r'(\{\{[^}]{1,80}\}\}|\*\|[A-Z0-9_:]{1,40}\|\*|%%[^%\s]{1,60}%%|\{\$[a-z0-9_]{1,40}\}|\[\[[^\]]{1,60}\]\])',
                        re.I)


def cmd_emailcheck(a):
    """Mechanical checks on an email HTML file (and its plain-text version). It cannot test an email client; it reports
    what a send-ready email must have, so missing items are visible."""
    from html.parser import HTMLParser
    src = Path(a.html)
    if not src.is_file():
        raise Stop(f'no file {src}')
    html = src.read_text(encoding='utf-8', errors='replace')

    class P(HTMLParser):
        def __init__(self):
            super().__init__(convert_charrefs=True)
            self.tags, self.imgs, self.links, self.text, self.styles, self.skip = {}, [], [], [], [], 0
            self.cur_link = None

        def handle_starttag(self, tag, attrs):
            d = dict(attrs)
            self.tags[tag] = self.tags.get(tag, 0) + 1
            if tag in ('style', 'script', 'title'):
                self.skip += 1
            if tag == 'img':
                self.imgs.append(d)
            if tag == 'a':
                self.cur_link = {'href': d.get('href'), 'text': ''}
                self.links.append(self.cur_link)
            if d.get('style'):
                self.styles.append(d['style'])
            if tag == 'link' and 'stylesheet' in (d.get('rel') or ''):
                self.styles.append('EXTERNAL STYLESHEET ' + (d.get('href') or ''))

        def handle_endtag(self, tag):
            if tag in ('style', 'script', 'title') and self.skip:
                self.skip -= 1
            if tag == 'a':
                self.cur_link = None

        def handle_data(self, data):
            if self.skip:
                if data.strip():
                    self.styles.append(data)
                return
            self.text.append(data)
            if self.cur_link is not None:
                self.cur_link['text'] += data

    pr = P()
    pr.feed(html)
    css = '\n'.join(pr.styles).lower()
    text = ' '.join(' '.join(pr.text).split())
    size_kb = round(len(html.encode('utf-8')) / 1024, 1)
    problems, notes = [], []
    forbidden = {t: n for t, n in pr.tags.items() if t in ('script', 'form', 'iframe', 'video', 'audio', 'object',
                                                           'embed', 'input', 'select', 'textarea')}
    if forbidden:
        problems.append(f'elements email clients drop or block: {forbidden}')
    for pat, why in ((r'display\s*:\s*grid', 'CSS grid'), (r'position\s*:\s*(absolute|fixed|sticky)', 'positioning'),
                     (r'@import', '@import'), (r'external stylesheet', 'an external stylesheet')):
        if re.search(pat, css):
            (problems if a.production else notes).append(f'{why} is used; many email clients ignore it')
    if size_kb > 102:
        problems.append(f'the HTML is {size_kb} KB; Gmail clips messages over about 102 KB')
    no_alt = [i.get('src') for i in pr.imgs if i.get('alt') is None]
    no_size = [i.get('src') for i in pr.imgs if not i.get('width')]
    not_https = [i.get('src') for i in pr.imgs if not (i.get('src') or '').lower().startswith('https://')]
    if no_alt:
        problems.append(f'images with no alt attribute: {no_alt[:8]}')
    if no_size:
        (problems if a.production else notes).append(f'images with no width attribute: {no_size[:8]}')
    if not_https:
        (problems if a.production else notes).append(
            f'images that are not on an https address (fine for a concept or a handover draft; not send-ready until the '
            f'sender has hosted paths): {not_https[:8]}')
    empty = [l['text'].strip()[:60] or '(no text)' for l in pr.links if not (l['href'] or '').strip() or l['href'].strip() == '#']
    if empty:
        problems.append(f'links with no destination: {empty[:8]}')
    tags = sorted(set(EMAIL_TAGS.findall(html)))
    unsub = bool(re.search(r'unsubscribe|opt[ -]?out|preferences', html, re.I))
    if a.production and not unsub:
        problems.append('no unsubscribe or preference link or tag found; the sending platform\'s required footer must be '
                        'supplied, never invented')
    plain = None
    if a.text:
        tp = Path(a.text)
        if not tp.is_file():
            problems.append(f'plain-text file {tp} is missing')
        else:
            plain = tp.read_text(encoding='utf-8', errors='replace')
    elif a.production:
        problems.append('no plain-text version given (--text); production email needs one with the same message')
    coverage = None
    if plain is not None:
        words = lambda t: re.findall(r'[a-z0-9]+(?:[\'’][a-z]+)?', t.lower())
        hw, pw = words(text), set(words(plain))
        coverage = round(100 * sum(w in pw for w in hw) / max(1, len(hw)))
        if coverage < 90:
            problems.append(f'only {coverage}% of the HTML\'s words appear in the plain-text version')
        hrefs = sorted({l['href'] for l in pr.links if (l['href'] or '').startswith('http')})
        missing_links = [h for h in hrefs if h not in plain]
        if missing_links:
            problems.append(f'links in the HTML that are missing from the plain text: {missing_links[:8]}')
    record = {'checked': now(), 'file': str(src), 'mode': 'production' if a.production else 'concept', 'html_kb': size_kb,
              'images': pr.imgs, 'links': pr.links, 'merge_tags': tags, 'unsubscribe_found': unsub,
              'plain_text_word_coverage_percent': coverage, 'visible_text': text[:20000], 'problems': problems,
              'notes': notes, 'not_checked_here': ['rendering in any email client (Gmail, Outlook, Apple Mail)',
                                                   'dark mode and image blocking in real clients', 'deliverability']}
    opt = option_folder(src)
    out = (opt / 'checks') if opt else src.parent
    out.mkdir(parents=True, exist_ok=True)
    (out / f'email-check-{src.stem}.json').write_text(json.dumps(record, indent=2, ensure_ascii=False) + '\n',
                                                     encoding='utf-8')
    print(f'{src.name}: {size_kb} KB, {len(pr.imgs)} images, {len(pr.links)} links, merge tags {tags or "none"}, '
          f'unsubscribe {"found" if unsub else "not found"}' +
          (f', plain text carries {coverage}% of the words' if coverage is not None else ''))
    print(f'Saved {out / f"email-check-{src.stem}.json"}')
    for m in notes:
        print(f'NOTE {m}')
    for m in problems:
        print(f'PROBLEM {m}')
    print('No email client was tested by this check. Record real client tests (client, version or service, date, '
          'result) separately, or say "not tested".')
    return 1 if problems else 0


def cmd_site(a):
    c = case_dir(a.case)
    case = load_case(c)
    if case['deliverable'] != 'linkedin-banner':
        raise Stop('the review site is for linkedin-banner cases')
    site = c / 'review-site'
    if site.exists():
        shutil.rmtree(site)
    n = case['options']
    for i in range(1, n + 1):
        src = c / f'option-{i}' / 'preview'
        if not (src / 'index.html').is_file():
            raise Stop(f'option-{i}/preview/index.html is missing')
        dest = site / f'banner-{i}'
        shutil.copytree(src, dest)
        if n > 1:
            current = ' aria-current="page"'
            links = ''.join(f'<a href="../banner-{k}/index.html"{current if k == i else ""}>Banner {k}</a>'
                            for k in range(1, n + 1))
            page = (dest / 'index.html').read_text(encoding='utf-8')
            page = re.sub(r'(<body[^>]*>)', lambda m: m.group(1) + f'<nav class="view-nav">{links}</nav>', page, count=1)
            (dest / 'index.html').write_text(page, encoding='utf-8')
    (site / 'index.html').write_text('<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" '
                                     'content="0; url=banner-1/index.html"><a href="banner-1/index.html">Banner 1</a>\n',
                                     encoding='utf-8')
    print(f'Local review site: {site / "index.html"} ({n} banner{"s" if n > 1 else ""}). It stays on this PC; '
          'publishing it is a person\'s decision.')
    return 0


# ---------------------------------------------------------------- inspection

def pdf_info(p):
    from pypdf import PdfReader
    r = PdfReader(str(p))
    sizes, with_text = [], 0
    for pg in r.pages:
        box = pg.mediabox
        sizes.append((round(float(box.width) / 0.75), round(float(box.height) / 0.75)))
        with_text += bool((pg.extract_text() or '').strip())
    meta = r.metadata or {}
    return {'pages': len(r.pages), 'sizes_px': sorted(set(sizes)), 'pages_with_text': with_text,
            'title': meta.get('/Title'), 'author': meta.get('/Author'), 'creator': meta.get('/Creator'),
            'producer': meta.get('/Producer')}


def sniff(p):
    head = Path(p).read_bytes()[:12]
    if head.startswith(b'\x89PNG\r\n\x1a\n'):
        return 'png'
    if head.startswith(b'\xff\xd8\xff'):
        return 'jpeg'
    if head.startswith(b'%PDF'):
        return 'pdf'
    if head.startswith(b'RIFF') and head[8:12] == b'WEBP':
        return 'webp'
    return 'unknown'


def cmd_inspect(a):
    import hashlib
    from PIL import Image
    want = size(a.size) if a.size else None
    bad = 0
    for f in a.files:
        p = Path(f)
        if not p.is_file():
            print(f'FAIL {f}: missing')
            bad += 1
            continue
        kind = sniff(p)
        ext = p.suffix.lower().lstrip('.').replace('jpg', 'jpeg')
        row = {'file': str(p), 'format': kind, 'extension_matches': ext == kind, 'bytes': p.stat().st_size,
               'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
        problems = []
        if kind in ('png', 'jpeg', 'webp'):
            with Image.open(p) as im:
                row.update(width=im.width, height=im.height, mode=im.mode,
                           icc_profile='yes' if im.info.get('icc_profile') else 'none')
            if want and (row['width'], row['height']) != want:
                problems.append(f'size {row["width"]}x{row["height"]}, expected {want[0]}x{want[1]}')
            if row['mode'] not in ('RGB', 'RGBA'):
                problems.append(f'colour mode {row["mode"]}, expected RGB')
        elif kind == 'pdf':
            row.update(pdf_info(p))
            # PDF sizes are in points (1 px = 0.75 pt), so Chrome's rounding can show 1 px either way
            if want and not all(abs(w_ - want[0]) <= 1 and abs(h_ - want[1]) <= 1 for w_, h_ in row['sizes_px']):
                problems.append(f'page sizes {row["sizes_px"]}, expected {want[0]}x{want[1]}')
        else:
            problems.append('not a PNG, JPEG, WebP or PDF file')
        if not row['extension_matches']:
            problems.append(f'the file is really {kind} but is named .{p.suffix.lstrip(".")}')
        if a.format and kind != a.format.replace('jpg', 'jpeg'):
            problems.append(f'format {kind}, expected {a.format}')
        if a.max_bytes and row['bytes'] > a.max_bytes:
            problems.append(f'{row["bytes"]} bytes, over the limit of {a.max_bytes}')
        bad += bool(problems)
        print(('FAIL ' if problems else 'OK   ') + json.dumps(row, ensure_ascii=False) +
              (f'\n     problems: {"; ".join(problems)}' if problems else ''))
    return 1 if bad else 0


def cmd_sheet(a):
    from PIL import Image, ImageDraw
    ims = [Image.open(f).convert('RGB') for f in a.images]
    if not ims:
        raise Stop('give the images')
    cell = 360
    cols = min(len(ims), a.columns)
    rows = (len(ims) + cols - 1) // cols
    thumbs = []
    for im in ims:
        im = im.copy()
        im.thumbnail((cell, cell))
        thumbs.append(im)
    sheet = Image.new('RGB', (cols * (cell + 16) + 16, rows * (cell + 40) + 16), 'white')
    draw = ImageDraw.Draw(sheet)
    for k, (im, f) in enumerate(zip(thumbs, a.images)):
        x, y = 16 + (k % cols) * (cell + 16), 16 + (k // cols) * (cell + 40)
        sheet.paste(im, (x, y))
        draw.text((x, y + im.height + 6), Path(f).name, fill='black')
    sheet.save(a.out)
    print(f'Saved {a.out}. A contact sheet is a review aid only; every final file still needs its own look.')
    return 0


# ---------------------------------------------------------------- review

def review_images(c, n, deliverable=''):
    imgs = []
    for i in range(1, n + 1):
        o = c / f'option-{i}'
        for sub in ('exports', 'previews'):
            imgs += sorted(p for p in (o / sub).glob('*') if p.suffix.lower() in ('.png', '.jpg', '.jpeg', '.webp'))
    if deliverable.startswith('linkedin-'):
        return imgs

    def rank(p):
        # Most useful first, so the image limit cuts the least useful: exports, then every page at the widest and
        # 390 px, then JavaScript-off and reduced-motion at 390 px, then the other widths.
        name = p.stem
        if p.parent.name == 'exports':
            return 0
        if re.search(r'-normal-(1440|390)$', name) or not re.search(r'-(normal|nojs|reduced)-\d+$', name):
            return 1
        if re.search(r'-(nojs|reduced)-390$', name):
            return 2
        return 3
    return sorted(imgs, key=lambda p: (rank(p), str(p)))


def tile_tall(src, dest):
    """A very tall full-page screenshot becomes unreadable when an image model scales it to fit. Cut it into strips and
    lay them side by side (read the columns left to right), so the reviewer sees it near full size."""
    from PIL import Image
    with Image.open(src) as im:
        w, h = im.size
        if h <= 2.2 * w:
            return None
        cols = max(2, min(6, round((h / w) ** 0.5)))
        strip = -(-h // cols)
        gap = 24
        sheet = Image.new('RGB', (cols * w + (cols - 1) * gap, strip), (128, 128, 128))
        for k in range(cols):
            part = im.crop((0, k * strip, w, min(h, (k + 1) * strip))).convert('RGB')
            sheet.paste(part, (k * (w + gap), 0))
        dest.parent.mkdir(parents=True, exist_ok=True)
        sheet.save(dest)
        return cols


def tool_facts(c):
    """Facts about every export, measured by this tool (not by the builder), so the reviewer has them even if it cannot
    run a command: file format, size, colour mode, bytes, and for PDFs the page count, page sizes, metadata and the
    text on each page."""
    from PIL import Image
    out = []
    for p in sorted(c.glob('option-*/exports/*')):
        if not p.is_file():
            continue
        rel = str(p.relative_to(c)).replace('\\', '/')
        kind = sniff(p)
        row = {'file': rel, 'format': kind, 'bytes': p.stat().st_size}
        if kind in ('png', 'jpeg', 'webp'):
            with Image.open(p) as im:
                row.update(width=im.width, height=im.height, mode=im.mode)
        elif kind == 'pdf':
            from pypdf import PdfReader
            info = pdf_info(p)
            row.update(info)
            row['text_by_page'] = [(pg.extract_text() or '').strip()[:1500] for pg in PdfReader(str(p)).pages]
        out.append(row)
    return out


def render_pdf_pages(pdf, outdir, width=540):
    """Every PDF page as a PNG (pypdfium2), so the reviewer can see the PDF itself without running a command."""
    import pypdfium2 as pdfium
    outdir.mkdir(parents=True, exist_ok=True)
    doc = pdfium.PdfDocument(str(pdf))
    files = []
    for i in range(len(doc)):
        page = doc[i]
        scale = width / page.get_width()
        img = page.render(scale=scale).to_pil().convert('RGB')
        f = outdir / f'{pdf.stem}-page-{i + 1:02d}.png'
        img.save(f)
        files.append(f)
    doc.close()
    return files


def page_vs_png(page_png, slide_png):
    """Mean absolute difference (0 to 255) between a rendered PDF page and the exported PNG it should match."""
    from PIL import Image, ImageChops, ImageStat
    with Image.open(page_png) as a, Image.open(slide_png) as b:
        b2 = b.convert('RGB').resize(a.size)
        return round(sum(ImageStat.Stat(ImageChops.difference(a.convert('RGB'), b2)).mean) / 3, 1)


def text_files(c, limit=30000):
    """The brief and copy files, and each builder's notes, verbatim (capped), for the reviewer."""
    out = []
    for p in sorted(list((c / 'brief').rglob('*')) + list(c.glob('option-*/notes.md'))):
        if p.is_file() and p.suffix.lower() in ('.md', '.txt', '.json', '.csv'):
            t = p.read_text(encoding='utf-8', errors='replace')
            out.append((str(p.relative_to(c)).replace('\\', '/'), t[:limit] + ('\n[cut]' if len(t) > limit else '')))
    return out


def review_copy(c, dest):
    """A throwaway copy of the case for the reviewer, plus the skill folder as _skill/. Codex on Windows cannot run
    any command in read-only mode (openai/codex, Windows sandbox), so the reviewer works in this copy with
    workspace-write: it can open and inspect every file, and nothing it does can reach the real case folder."""
    shutil.copytree(c, dest, ignore=shutil.ignore_patterns('.codex-image', 'review-site', 'review'))
    return dest


def case_manifest(c):
    """sha256 of every file the reviewer judges (not review/, pictures' scratch folders or the review site), so the
    next round can be told exactly what changed."""
    import hashlib
    out = {}
    for f in sorted(c.rglob('*')):
        rel = f.relative_to(c)
        if (not f.is_file() or rel.parts[0] in ('review', 'review-site') or '.codex-image' in rel.parts
                or str(rel) == 'case.json'):
            continue
        out[str(rel).replace('\\', '/')] = hashlib.sha256(f.read_bytes()).hexdigest()
    return out


def cmd_review(a):
    raise Stop('Use team.py review CASE. The legacy review parser is disabled in this local runtime.')

# ---------------------------------------------------------------- status

def cmd_status(_a):
    ok = True

    def line(good, text, fix=''):
        nonlocal ok
        ok &= good
        print(('OK    ' if good else 'FIX   ') + text + ('' if good else f'  ->  {fix}'))

    line(sys.version_info >= (3, 11), f'Python {sys.version.split()[0]}', 'install Python 3.11 or newer')
    for mod in ('PIL', 'pypdf', 'gdown', 'pypdfium2'):
        try:
            __import__(mod)
            line(True, f'Python package {mod}')
        except ImportError:
            line(False, f'Python package {mod}', 'run install\\install.ps1')
    line(bool(shutil.which('node')), 'Node.js', 'install Node.js LTS from nodejs.org')
    line((ROOT / 'tools' / 'node_modules' / 'playwright-core').is_dir(), 'browser helper (tools/node_modules)',
         'run install\\install.ps1')
    if shutil.which('node') and (ROOT / 'tools' / 'node_modules').is_dir():
        with tempfile.TemporaryDirectory() as tmp:
            page = Path(tmp) / 't.html'
            page.write_text('<body style="margin:0;background:#2a6">ok</body>', encoding='utf-8')
            try:
                render('png', page, Path(tmp) / 't.png', 200, 100)
                line(True, 'headless Chromium renders')
            except Stop as exc:
                line(False, f'headless Chromium: {exc}', 'run install\\install.ps1')
    nlib = len([p for p in FONT_LIB.iterdir() if p.is_dir() and not p.name.startswith('_') and font_files(p)]) if FONT_LIB.is_dir() else 0
    line(nlib > 0, f'team font library: {nlib} families in fonts/ (no font download during jobs)', 'git pull')
    line(bool(shutil.which('codex')), 'Codex CLI (pictures and review)', 'install Codex and sign in')
    from kit_codex import is_set_up, kit_home
    line(is_set_up(), f'kit Codex folder {kit_home()}', 'py -3 tools/kit_codex.py setup (optional but recommended)')
    import gpt_image
    img = config().get('images', {})
    engine = img.get('engine', 'auto')
    if engine == 'auto':
        engine = ('openrouter' if gpt_image.openrouter_key_present() else
                  'api' if gpt_image.api_key_present() else 'codex')
    print('INFO  pictures: ' + {
        'openrouter': f'{img.get("openrouter_model", "openai/gpt-image-2.5-sunburst")} via OpenRouter (OPENROUTER_API_KEY is set)',
        'api': f'{img.get("model", "gpt-image-2.5-sunburst")} via the OpenAI Images API (OPENAI_API_KEY is set)',
        'codex': 'the Codex subscription (Codex picks the model; each picture records what it reported)'}[engine])
    print('Ready.' if ok else 'Fix the lines marked FIX, then run this again.')
    return 0 if ok else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    # status is provided by team.py
    p = sub.add_parser('new')
    p.add_argument('deliverable')
    p.add_argument('--client', required=True)
    p.add_argument('--options', type=int, default=2)  # two variants, like the design kit
    p.add_argument('--name')
    p = sub.add_parser('brief')
    p.add_argument('case')
    p.add_argument('--gdoc', required=True)
    p = sub.add_parser('assets')
    p.add_argument('client')
    p.add_argument('--drive', action='append', default=[])
    p.add_argument('--folder', action='append', default=[])
    p = sub.add_parser('fonts')
    p.add_argument('client')
    p.add_argument('families', nargs='+')
    p = sub.add_parser('fontlib')
    p.add_argument('action', choices=('list', 'add'))
    p.add_argument('families', nargs='*')
    p = sub.add_parser('prototype')
    p.add_argument('case')
    p.add_argument('destination', choices=('personal', 'business'))
    p = sub.add_parser('png')
    p.add_argument('html')
    p.add_argument('out')
    p.add_argument('--size', required=True)
    p = sub.add_parser('pdf')
    p.add_argument('out')
    p.add_argument('html', nargs='+')
    p.add_argument('--size', required=True)
    p.add_argument('--title')
    p.add_argument('--author')
    p = sub.add_parser('fullpng')
    p.add_argument('target')
    p.add_argument('out')
    p.add_argument('--width', required=True)
    p = sub.add_parser('pagecheck')
    p.add_argument('targets', nargs='+')
    p.add_argument('--widths', default='1440,1024,768,390,320')
    p.add_argument('--out')
    p.add_argument('--name')
    p.add_argument('--motion', action='store_true')
    p = sub.add_parser('emailcheck')
    p.add_argument('html')
    p.add_argument('--text')
    p.add_argument('--production', action='store_true')
    p = sub.add_parser('preview')
    p.add_argument('html')
    p.add_argument('--out')
    p.add_argument('--views', default='desktop:1280,mobile:390,phone:360')
    p = sub.add_parser('site')
    p.add_argument('case')
    p = sub.add_parser('inspect')
    p.add_argument('files', nargs='+')
    p.add_argument('--size')
    p.add_argument('--max-bytes', type=int)
    p.add_argument('--format', choices=('png', 'jpeg', 'jpg', 'pdf'))
    p = sub.add_parser('sheet')
    p.add_argument('out')
    p.add_argument('images', nargs='+')
    p.add_argument('--columns', type=int, default=4)
    p = sub.add_parser('review')
    p.add_argument('case')
    p.add_argument('--dry-run', action='store_true')
    a = ap.parse_args(argv)
    try:
        if a.cmd not in ('png','pdf','fullpng','pagecheck','emailcheck','preview','site','inspect','sheet','prototype'):
            raise Stop('This runtime exposes local export/inspection helpers only. Use team.py for jobs/review; keep source retrieval and client assets in the client folder.')
        return globals()['cmd_' + a.cmd](a)
    except subprocess.TimeoutExpired:
        print('STOP: Codex did not finish in time. Run the review again once; if it fails again, tell the designer.',
              file=sys.stderr)
        return 3
    except Stop as exc:
        print(f'STOP: {exc}', file=sys.stderr)
        return 3


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    sys.exit(main())
