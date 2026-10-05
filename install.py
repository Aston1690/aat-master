#!/usr/bin/env python3
"""One-time local setup. Does not authenticate, launch models or publish work."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import venv

ROOT = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_sources():
    for name, expected in json.loads((ROOT / 'source-pins.json').read_text(encoding='utf-8')).items():
        path = (ROOT / name).resolve()
        if not path.is_relative_to(ROOT) or not path.is_file() or digest(path) != expected:
            raise RuntimeError('Packaged source changed: ' + name)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--codex-home', type=Path, default=Path(os.environ.get('CODEX_HOME', str(Path.home() / '.codex'))))
    parser.add_argument('--config-home', type=Path, default=Path.home() / '.config')
    parser.add_argument('--skip-browser-download', action='store_true', help='Use an existing Chromium or CHROMIUM_PATH; verify it separately.')
    args = parser.parse_args()
    if sys.version_info < (3, 11):
        parser.error('Python 3.11 or newer is required.')
    verify_sources()
    for tool in ['codex', 'node', 'npm']:
        if not shutil.which(tool):
            parser.error('Install ' + tool + ' before setup.')
    home = args.codex_home.expanduser().resolve()
    target = home / 'skills' / 'aat-master'
    skill = ROOT / '.agents' / 'skills' / 'aat-master'
    registry = args.config_home.expanduser().resolve() / 'aat-master' / 'runtime.json'
    state_path = ROOT / 'runtime' / 'installation.json'
    previous = json.loads(state_path.read_text(encoding='utf-8')) if state_path.exists() else {}
    existing_profiles = previous.get('profiles', {})
    # Refuse unrelated installations instead of overwriting existing team settings.
    managed_copy = False
    if target.exists() and not target.is_symlink() and previous.get('installed_skill_source') == str(skill):
        old_files = previous.get('installed_skill_files', {})
        actual_files = {str(p) for p in target.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
        managed_copy = bool(old_files) and actual_files == set(old_files) and all(Path(p).is_file() and digest(Path(p)) == h for p, h in old_files.items())
    if (target.exists() or target.is_symlink()) and not (target.is_symlink() and target.resolve() == skill) and not managed_copy:
        parser.error('An AAT Master installation already exists or was edited. Back it up outside active skills before installing this checkout.')
    if registry.exists() and json.loads(registry.read_text(encoding='utf-8')).get('runtime_root') != str(ROOT / 'runtime'):
        parser.error('Another runtime is connected. Back up its registry before installing this checkout.')
    profiles = {}
    runtime_literal = str(ROOT / 'runtime').replace('\\', '\\\\').replace('"', '\\"')
    for template in sorted((ROOT / 'profiles').glob('*.toml')):
        destination = home / template.name
        content = template.read_text(encoding='utf-8').replace('@RUNTIME_ROOT@', runtime_literal)
        if destination.exists() and destination.read_text(encoding='utf-8') != content:
            if existing_profiles.get(str(destination)) != digest(destination):
                parser.error('Existing model profile differs: ' + destination.name)
        profiles[destination] = content
    runtime = ROOT / 'runtime'
    venv.EnvBuilder(with_pip=True, symlinks=os.name != 'nt').create(runtime / '.venv')
    python = runtime / '.venv' / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
    subprocess.run([str(python), '-m', 'pip', 'install', '-r', str(runtime / 'requirements.txt')], check=True)
    subprocess.run([shutil.which('npm'), 'ci', '--ignore-scripts', '--prefix', str(runtime / 'tools')], check=True)
    if not args.skip_browser_download:
        subprocess.run([shutil.which('node'), str(runtime / 'tools/node_modules/playwright-core/cli.js'), 'install', 'chromium'], check=True)
    home.mkdir(parents=True, exist_ok=True)
    for destination, content in profiles.items():
        destination.write_text(content, encoding='utf-8')
    target.parent.mkdir(parents=True, exist_ok=True)
    installed_skill_files = {}
    if os.name == 'nt':
        # Windows user accounts need no Administrator/Developer Mode for a managed copy.
        if managed_copy:
            for name in previous['installed_skill_files']:
                Path(name).unlink()
        shutil.copytree(skill, target, dirs_exist_ok=True, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        (target / 'runtime-location.json').write_text(json.dumps({'runtime_root': str(runtime)}, indent=2) + '\n', encoding='utf-8')
        installed_skill_files = {str(p): digest(p) for p in target.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
    elif not target.is_symlink():
        target.symlink_to(skill, target_is_directory=True)
    registry.parent.mkdir(parents=True, exist_ok=True)
    registry.write_text(json.dumps({'runtime_root': str(runtime)}, indent=2) + '\n', encoding='utf-8')
    state_path.write_text(json.dumps({'profiles': {str(p): digest(p) for p in profiles}, 'installed_skill_source': str(skill), 'installed_skill_files': installed_skill_files}, indent=2) + '\n', encoding='utf-8')
    subprocess.run([str(python), str(runtime / 'team.py'), 'status'], check=True)
    print('Installed AAT Master. Keep this checkout in place. Start a fresh Astra session and invoke $aat-master.')
    print('If T3 shows a stale skills list, fully quit and reopen T3. No client job or live model probe has run.')


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, RuntimeError, subprocess.CalledProcessError) as exc:
        print('Setup stopped: ' + str(exc), file=sys.stderr)
        sys.exit(1)
