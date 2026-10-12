import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from unittests.renpy_test_support import initialize_renpy

initialize_renpy()

import renpy
from renpy.loadsave import SaveRecord, safe_rename


class TestSafeRename(unittest.TestCase):
    def test_transient_failure_retries_without_removing_existing_save(self):
        with tempfile.TemporaryDirectory() as directory:
            old = Path(directory) / "save.new"
            new = Path(directory) / "save"
            old.write_bytes(b"new save")
            new.write_bytes(b"previous save")
            replace = os.replace

            def fail_once(source, destination):
                self.assertEqual(new.read_bytes(), b"previous save")
                if replacement.call_count == 1:
                    raise OSError("temporary failure")
                replace(source, destination)

            with patch("renpy.loadsave.os.replace", side_effect=fail_once) as replacement:
                safe_rename(old, new)

            self.assertEqual(replacement.call_count, 2)
            self.assertEqual(new.read_bytes(), b"new save")
            self.assertFalse(old.exists())

    def test_repeated_failure_preserves_existing_save_and_removes_temporary_file(self):
        with tempfile.TemporaryDirectory() as directory:
            old = Path(directory) / "save.new"
            new = Path(directory) / "save"
            old.write_bytes(b"new save")
            new.write_bytes(b"previous save")

            with (
                patch("renpy.loadsave.os.replace", side_effect=OSError("replace failed")) as replacement,
                self.assertRaisesRegex(OSError, "replace failed"),
            ):
                safe_rename(old, new)

            self.assertEqual(replacement.call_count, 2)
            self.assertFalse(old.exists())
            self.assertEqual(new.read_bytes(), b"previous save")

    def test_failed_save_record_does_not_record_success_or_leave_temporary_file(self):
        with (
            tempfile.TemporaryDirectory() as directory,
            patch.object(renpy.savetoken, "sign_data", return_value=b""),
            patch("renpy.loadsave.os.replace", side_effect=OSError("replace failed")),
        ):
            filename = Path(directory) / "save"
            filename.write_bytes(b"previous save")
            record = SaveRecord(None, "", "{}", b"log")

            with self.assertRaisesRegex(OSError, "replace failed"):
                record.write_file(str(filename))

            self.assertIsNone(record.first_filename)
            self.assertFalse(Path(str(filename) + ".new").exists())
            self.assertEqual(filename.read_bytes(), b"previous save")
