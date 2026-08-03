import unittest

from renpy.versions import _make_version_string


class TestVersions(unittest.TestCase):
    def test_official_version(self):
        version = _make_version_string((8, 6, 0, 26080401), "main", True, False, False)
        self.assertEqual(version, "8.6.0.26080401")

    def test_official_nightly_version(self):
        version = _make_version_string((8, 6, 0, 26080401), "main", True, True, False)
        self.assertEqual(version, "8.6.0.26080401+nightly")

    def test_unofficial_branch_version(self):
        version = _make_version_string((8, 6, 0, 26080401), "topic", False, False, True)
        self.assertEqual(version, "8.6.0.26080401+unofficial.dirty.topic")
