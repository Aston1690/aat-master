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
    for name, expected in json.loads((ROOT / 'source-pins.json').read_text()).items():
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
    if os.name != 'posix':
        parser.error('This release supports macOS/Linux; Windows requires a Linux environment and separate validation.')
    verify_sources()
    for tool in ['codex', 'node', 'npm']:
        if not shutil.which(tool):
            parser.error('Install ' + tool + ' before setup.')
    home = args.codex_home.expanduser().resolve()
    target = home / 'skills' / 'aat-master'
    skill = ROOT / '.agents' / 'skills' / 'aat-master'
    registry = args.config_home.expanduser().resolve() / 'aat-master' / 'runtime.json'
    state_path = ROOT / 'runtime' / 'installation.json'
    previous = json.loads(state_path.read_text()) if state_path.exists() else {}
    existing_profiles = previous.get('profiles', {})
    # Refuse unrelated installations instead of overwriting existing team settings.
    if (target.exists() or target.is_symlink()) and not (target.is_symlink() and target.resolve() == skill):
        parser.error('An AAT Master installation already exists. Back it up outside active skills before installing this checkout.')
    if registry.exists() and json.loads(registry.read_text()).get('runtime_root') != str(ROOT / 'runtime'):
        parser.error('Another runtime is connected. Back up its registry before installing this checkout.')
    profiles = {}
    runtime_literal = str(ROOT / 'runtime').replace('\\', '\\\\').replace('"', '\\"')
    for template in sorted((ROOT / 'profiles').glob('*.toml')):
        destination = home / template.name
        content = template.read_text().replace('@RUNTIME_ROOT@', runtime_literal)
        if destination.exists() and destination.read_text() != content:
            if existing_profiles.get(str(destination)) != digest(destination):
                parser.error('Existing model profile differs: ' + destination.name)
        profiles[destination] = content
    runtime = ROOT / 'runtime'
    venv.EnvBuilder(with_pip=True, symlinks=True).create(runtime / '.venv')
    python = runtime / '.venv' / 'bin' / 'python'
    subprocess.run([str(python), '-m', 'pip', 'install', '-r', str(runtime / 'requirements.txt')], check=True)
    subprocess.run(['npm', 'ci', '--ignore-scripts', '--prefix', str(runtime / 'tools')], check=True)
    if not args.skip_browser_download:
        subprocess.run(['node', str(runtime / 'tools/node_modules/playwright-core/cli.js'), 'install', 'chromium'], check=True)
    home.mkdir(parents=True, exist_ok=True)
    for destination, content in profiles.items():
        destination.write_text(content)
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.is_symlink():
        target.symlink_to(skill, target_is_directory=True)
    registry.parent.mkdir(parents=True, exist_ok=True)
    registry.write_text(json.dumps({'runtime_root': str(runtime)}, indent=2) + '\n')
    state_path.write_text(json.dumps({'profiles': {str(p): digest(p) for p in profiles}}, indent=2) + '\n')
    subprocess.run([str(python), str(runtime / 'team.py'), 'status'], check=True)
    print('Installed AAT Master. Keep this checkout in place. Start a fresh Astra session and invoke $aat-master.')
    print('If T3 shows a stale skills list, fully quit and reopen T3. No client job or live model probe has run.')


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, RuntimeError, subprocess.CalledProcessError) as exc:
        print('Setup stopped: ' + str(exc), file=sys.stderr)
        sys.exit(1)
