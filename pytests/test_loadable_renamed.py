import pytest

import renpy
from renpy import loader


@pytest.fixture(autouse=True)
def loader_state(mocker):
    """
    Isolates the loader from real game files. The rename table is set to old.png -> new.png, the loader
    caches and archive lists are emptied, and load_core is patched to fail, so any availability check that
    opens a file fails the test instead of touching the disk.
    """

    mocker.patch.object(renpy.config, "renamed_files", {"old.png": "new.png"})
    mocker.patch.object(loader, "lower_map", {})
    mocker.patch.object(loader, "loadable_cache", {})
    mocker.patch.object(loader, "apks", [])
    mocker.patch.object(loader, "archives", [])
    mocker.patch.object(loader, "remote_files", {})
    mocker.patch.object(loader, "load_core", side_effect=AssertionError("availability check opened a file"))


def test_local_rename_checks_availability_and_uses_target_cache(mocker):
    """
    A renamed file is available when its target is, and the answer is cached under the target name.
    Both spellings of the old name resolve through the rename table (case-insensitively), but the target
    is only checked once.
    """

    transfn = mocker.patch.object(loader, "transfn", return_value="new.png")
    assert loader.loadable_core("OLD.png") is True
    assert loader.loadable_core("old.png") is True
    transfn.assert_called_once_with("new.png")
    mocker.stop(transfn)

    assert loader.loadable_cache["new.png"] is True


def test_missing_target_returns_false(mocker):
    """
    When the renamed target can't be found, the renamed file is reported unavailable and that result is
    cached under the target name, so a repeated check doesn't look again.
    """

    transfn = mocker.patch.object(loader, "transfn", side_effect=FileNotFoundError)
    assert loader.loadable_core("old.png") is False
    assert loader.loadable_core("old.png") is False
    mocker.stop(transfn)

    assert loader.loadable_cache["new.png"] is False


def test_remote_target_is_available_without_download(mocker):
    """
    A renamed target listed in remote_files counts as available without being downloaded. The file is
    absent locally (transfn raises), and load_core is patched to fail, so a download attempt would fail
    the test.
    """

    loader.remote_files["new.png"] = {"type": "image", "size": 100}
    mocker.patch.object(loader, "transfn", side_effect=FileNotFoundError)
    assert loader.loadable_core("old.png")
    assert loader.loadable_core("old.png")


def test_chained_renames_use_cached_final_target(mocker):
    """
    When the renamed target has a cached result, a chain of renames resolves to the final target and uses
    that cache entry, so the file system is never checked.
    """

    renpy.config.renamed_files["new.png"] = "final.png"
    loader.loadable_cache["final.png"] = True
    transfn = mocker.patch.object(loader, "transfn")
    assert loader.loadable_core("old.png") is True
    transfn.assert_not_called()
