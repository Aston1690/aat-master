#!/usr/bin/env python3
"""Connect AAT Master to the installed runtime; do not duplicate its workflow."""
import json
import os
from pathlib import Path
import subprocess
import sys


def resolve_runtime():
    override = os.environ.get('AAT_RUNTIME_ROOT')
    if override:
        root = Path(override).expanduser()
    else:
        bundled = Path(__file__).resolve().parents[4] / 'runtime'
        if (bundled / 'team.py').is_file():
            root = bundled
            return validate_runtime(root)
        registry = Path.home() / '.config' / 'aat-master' / 'runtime.json'
        if not registry.is_file():
            raise ValueError('AAT runtime is not connected: missing machine-local runtime.json')
        data = json.loads(registry.read_text())
        value = data.get('runtime_root')
        if not isinstance(value, str) or not value.strip():
            raise ValueError('AAT runtime registry needs a non-empty runtime_root')
        root = Path(value).expanduser()
    return validate_runtime(root)


def validate_runtime(root):
    if not root.is_absolute():
        raise ValueError('AAT runtime_root must be absolute')
    root = root.resolve()
    required = ['team.py', 'config.toml', 'installation.json', 'AGENTS.md',
                'RUN-A-JOB.md', '.venv/bin/python']
    missing = [name for name in required if not (root / name).is_file()]
    if missing:
        raise ValueError('AAT runtime is incomplete: ' + ', '.join(missing))
    if not (root / '.agents' / 'skills').is_dir():
        raise ValueError('AAT canonical specialist skills are missing')
    return root


def main():
    if len(sys.argv) < 2:
        print('Usage: runtime.py locate | status | <team.py command and arguments>', file=sys.stderr)
        return 2
    try:
        root = resolve_runtime()
        if sys.argv[1] == 'locate':
            if len(sys.argv) != 2:
                raise ValueError('locate takes no arguments')
            print(json.dumps({'runtime_root': str(root),
                              'instructions': str(root / 'AGENTS.md'),
                              'procedure': str(root / 'RUN-A-JOB.md'),
                              'skills_root': str(root / '.agents' / 'skills')}, indent=2))
            return 0
        command = [str(root / '.venv' / 'bin' / 'python'), str(root / 'team.py')]
        return subprocess.run(command + sys.argv[1:]).returncode
    except (OSError, ValueError, TypeError, AttributeError) as exc:
        print('STOP: ' + str(exc), file=sys.stderr)
        return 3


if __name__ == '__main__':
    sys.exit(main())
