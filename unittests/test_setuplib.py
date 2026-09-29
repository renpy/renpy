import os
import subprocess
import sys
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch

import setup as renpy_setup
from scripts.setuplib import _build_lock


class TestBuildLock(unittest.TestCase):
    def test_setup_holds_lock_through_build(self):
        events = []

        @contextmanager
        def record_lock(path):
            self.assertEqual(path, Path("tmp/.cython.lock"))
            events.append("locked")
            try:
                yield
            finally:
                events.append("unlocked")

        def build():
            events.append("build")
            self.assertEqual(events, ["locked", "build"])

        cwd = Path.cwd()
        try:
            with (
                patch.object(renpy_setup.setuplib, "_build_lock", record_lock),
                patch.object(renpy_setup, "_build", build),
            ):
                renpy_setup.main()
        finally:
            os.chdir(cwd)

        self.assertEqual(events, ["locked", "build", "unlocked"])

    def test_other_process_waits_for_build(self):
        root = Path(__file__).resolve().parents[1]
        child_code = (
            "import sys\n"
            "from pathlib import Path\n"
            "from scripts.setuplib import _build_lock\n"
            "print('ready', flush=True)\n"
            "with _build_lock(Path(sys.argv[1])):\n"
            "    print('acquired', flush=True)\n"
        )

        with tempfile.TemporaryDirectory(dir=root / "tmp") as directory:
            lock_path = Path(directory) / ".cython.lock"
            child = None
            try:
                with _build_lock(lock_path):
                    child = subprocess.Popen(
                        [sys.executable, "-c", child_code, str(lock_path)],
                        cwd=root,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                    )
                    assert child.stdout is not None
                    self.assertEqual(child.stdout.readline(), "ready\n")
                    with self.assertRaises(subprocess.TimeoutExpired):
                        child.communicate(timeout=0.2)

                stdout, stderr = child.communicate(timeout=10)
                self.assertEqual(child.returncode, 0, stderr)
                self.assertIn("acquired\n", stdout)
            finally:
                if child is not None and child.poll() is None:
                    child.kill()
                    child.communicate()
