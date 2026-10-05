"""Native OS checks; no model calls, credentials or client work."""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'runtime'))
import team


class PlatformTests(unittest.TestCase):
    def test_utf8_case_round_trip(self):
        with tempfile.TemporaryDirectory(prefix='aat space ') as folder:
            path = Path(folder) / 'résumé.json'
            value = {'copy': 'Café — résumé 日本語'}
            team.write(path, value)
            self.assertEqual(team.read(path), value)
            self.assertIn('日本語', path.read_bytes().decode('utf-8'))

    def test_process_lock_contention_and_release(self):
        with tempfile.TemporaryDirectory(prefix='aat lock ') as folder:
            path = Path(folder) / 'task.lock'
            script = (
                'import sys; from pathlib import Path; '
                f'sys.path.insert(0, {str(ROOT / "runtime")!r}); import team\n'
                'try:\n'
                f' with team.lock(Path({str(path)!r})): pass\n'
                'except team.Stop: sys.exit(7)\n'
            )
            with team.lock(path):
                held = subprocess.run([sys.executable, '-c', script])
                self.assertEqual(held.returncode, 7)
            released = subprocess.run([sys.executable, '-c', script])
            self.assertEqual(released.returncode, 0)

    def test_lock_released_after_failure(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'task.lock'
            with self.assertRaises(ValueError):
                with team.lock(path):
                    raise ValueError('fixture')
            with team.lock(path):
                pass

    def test_installed_master_and_profiles(self):
        state = team.read(ROOT / 'runtime/installation.json')
        team.pins()
        self.assertEqual(len(state['profiles']), 3)
        if os.name == 'nt':
            self.assertGreaterEqual(len(state['installed_skill_files']), 5)
            candidates = [Path(p) for p in state['installed_skill_files'] if p.endswith('runtime.py')]
            self.assertEqual(len(candidates), 1)
            wrapper = candidates[0]
        else:
            wrapper = ROOT / '.agents/skills/aat-master/scripts/runtime.py'
        result = subprocess.run([sys.executable, str(wrapper), 'locate'], capture_output=True, text=True, encoding='utf-8', check=True)
        self.assertEqual(Path(json.loads(result.stdout)['runtime_root']), ROOT / 'runtime')
        subprocess.run([sys.executable, str(wrapper), 'status'], check=True, capture_output=True)

    def test_codex_transport_executable(self):
        # Exercises Windows .cmd shims when npm supplies one; does not authenticate.
        result = subprocess.run([shutil.which('codex'), '--version'], capture_output=True, text=True, encoding='utf-8', check=True)
        self.assertIn('codex', result.stdout.lower())

    def test_png_renderer_with_spaced_unicode_paths(self):
        with tempfile.TemporaryDirectory(prefix='aat render ') as folder:
            root = Path(folder)
            source = root / 'café source.html'
            output = root / 'café output.png'
            source.write_text('<!doctype html><meta charset="utf-8"><h1>Café — test</h1>', encoding='utf-8')
            result = subprocess.run([shutil.which('node'), str(ROOT / 'runtime/tools/render.mjs'), 'png', str(source), str(output), '600', '300'], capture_output=True, text=True, encoding='utf-8', check=True)
            self.assertTrue(json.loads(result.stdout.splitlines()[-1])['ok'])
            from PIL import Image
            with Image.open(output) as image:
                self.assertEqual(image.size, (600, 300))


if __name__ == '__main__':
    unittest.main(verbosity=2)
