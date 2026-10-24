import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

from unittests import renpy_test_support


class TestRenpyInitialization(unittest.TestCase):
    def test_initializes_once_in_fresh_process(self):
        code = """
from unittest.mock import patch
import renpy
from unittests.renpy_test_support import initialize_renpy

with patch.object(renpy, "import_all", wraps=renpy.import_all) as startup:
    initialize_renpy()
    snapshot = renpy.backup.objects_pickle
    initialize_renpy()
    startup.assert_called_once_with()
    assert renpy.backup.objects_pickle is snapshot
    assert renpy.exports.store is renpy.store
"""
        result = subprocess.run(
            [sys.executable, "-c", code],
            cwd=Path(__file__).resolve().parent.parent,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_failed_initialization_propagates_and_can_retry(self):
        with (
            patch.object(renpy_test_support, "_initialized", False),
            patch.object(
                renpy_test_support.renpy, "import_all", side_effect=[RuntimeError("startup failed"), None]
            ) as startup,
        ):
            with self.assertRaisesRegex(RuntimeError, "startup failed"):
                renpy_test_support.initialize_renpy()

            self.assertFalse(renpy_test_support._initialized)
            renpy_test_support.initialize_renpy()
            self.assertTrue(renpy_test_support._initialized)
            renpy_test_support.initialize_renpy()
            self.assertEqual(startup.call_count, 2)
