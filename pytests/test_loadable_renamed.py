import unittest
from unittest.mock import patch

import renpy
from unittests.renpy_test_support import initialize_renpy

initialize_renpy()

from renpy import loader


class TestLoadableRenamed(unittest.TestCase):
    def setUp(self):
        for owner, name, value in [
            (renpy.config, "renamed_files", {"old.png": "new.png"}),
            (loader, "lower_map", {}),
            (loader, "loadable_cache", {}),
            (loader, "apks", []),
            (loader, "archives", []),
            (loader, "remote_files", {}),
        ]:
            p = patch.object(owner, name, value)
            p.start()
            self.addCleanup(p.stop)

        p = patch.object(loader, "load_core", side_effect=AssertionError("availability check opened a file"))
        p.start()
        self.addCleanup(p.stop)

    def test_local_rename_checks_availability_and_uses_target_cache(self):
        with patch.object(loader, "transfn", return_value="new.png") as transfn:
            self.assertIs(loader.loadable_core("OLD.png"), True)
            self.assertIs(loader.loadable_core("old.png"), True)
            transfn.assert_called_once_with("new.png")

        self.assertIs(loader.loadable_cache["new.png"], True)

    def test_missing_target_returns_false(self):
        with patch.object(loader, "transfn", side_effect=FileNotFoundError):
            self.assertIs(loader.loadable_core("old.png"), False)
            self.assertIs(loader.loadable_core("old.png"), False)

        self.assertIs(loader.loadable_cache["new.png"], False)

    def test_remote_target_is_available_without_download(self):
        loader.remote_files["new.png"] = {"type": "image", "size": 100}
        with patch.object(loader, "transfn", side_effect=FileNotFoundError):
            self.assertTrue(loader.loadable_core("old.png"))
            self.assertTrue(loader.loadable_core("old.png"))

    def test_chained_renames_use_cached_final_target(self):
        renpy.config.renamed_files["new.png"] = "final.png"
        loader.loadable_cache["final.png"] = True
        with patch.object(loader, "transfn") as transfn:
            self.assertIs(loader.loadable_core("old.png"), True)
            transfn.assert_not_called()
