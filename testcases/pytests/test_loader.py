# Copyright 2004-2026 Tom Rothamel <pytom@bishoujo.us>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


"""
Tests for renpy.loader: availability checks for renamed files, and the directories searched when a file is loaded by
name.
"""

from types import SimpleNamespace

import pytest

import renpy
from renpy import loader

################################################################################
# Renamed files
################################################################################


@pytest.fixture
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


@pytest.mark.usefixtures("loader_state")
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


@pytest.mark.usefixtures("loader_state")
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


@pytest.mark.usefixtures("loader_state")
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


@pytest.mark.usefixtures("loader_state")
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


################################################################################
# Search prefixes
################################################################################


@pytest.fixture
def loader_config(mocker):
    """
    Gives the tests a known search path and no language. search_prefixes is reduced to the game directory, so each
    expected list shows only what the directory argument adds.
    """

    mocker.patch.object(renpy.config, "search_prefixes", [""])
    mocker.patch.object(renpy.config, "tl_directory", "tl")
    mocker.patch.object(renpy.config, "add_to_special_directories", True)
    mocker.patch.object(renpy.config, "loadable_callback", None)
    mocker.patch.object(renpy.config, "audio_directories", ["audio"])
    mocker.patch.object(renpy.config, "image_directories", ["images"])
    mocker.patch.object(
        renpy.config, "special_directory_map", {"images": ["images"], "audio": ["audio"], "fonts": ["fonts"]}
    )
    mocker.patch.object(renpy.game, "preferences", SimpleNamespace(language=None))


@pytest.mark.parametrize(
    "directory,variable",
    [
        ("audio", "audio_directories"),
        ("images", "image_directories"),
    ],
)
@pytest.mark.usefixtures("loader_config")
def test_configured_directories_follow_mapped(mocker, directory, variable):
    """
    Configured directories are searched after the mapped ones, so a file found before this feature existed still
    resolves to the same path.
    """

    mocker.patch.object(renpy.config, variable, ["common/" + directory, "full/" + directory])

    assert loader.get_prefixes(tl=False, directory=directory) == [
        "",
        directory + "/",
        "common/" + directory + "/",
        "full/" + directory + "/",
    ]


@pytest.mark.usefixtures("loader_config")
def test_directories_are_normalized_and_deduplicated(mocker):
    """
    Slashes are stripped as the namespace scan does, and a directory that is listed twice, or is also a mapped
    directory, is only searched once.
    """

    mocker.patch.object(renpy.config, "audio_directories", ["/audio/", "full/audio/", "full/audio"])

    assert loader.get_prefixes(tl=False, directory="audio") == ["", "audio/", "full/audio/"]


@pytest.mark.usefixtures("loader_config")
def test_empty_list_keeps_mapped_directories(mocker):
    """
    Games declaring older compatibility have an empty list, and must still search the mapped directory as before.
    """

    mocker.patch.object(renpy.config, "audio_directories", [])

    assert loader.get_prefixes(tl=False, directory="audio") == ["", "audio/"]


@pytest.mark.usefixtures("loader_config")
def test_other_directories_are_unaffected(mocker):
    """
    Only audio and images have a matching variable. Fonts and unmapped names search what they always did, and neither
    variable leaks into them.
    """

    mocker.patch.object(renpy.config, "audio_directories", ["full/audio"])
    mocker.patch.object(renpy.config, "image_directories", ["full/images"])

    assert loader.get_prefixes(tl=False, directory="fonts") == ["", "fonts/"]
    assert loader.get_prefixes(tl=False, directory="other") == ["", "other/"]
    assert loader.get_prefixes(tl=False) == [""]


@pytest.mark.usefixtures("loader_config")
def test_special_directory_map_keeps_priority(mocker):
    """
    A customized special_directory_map is searched first, in its own order, and its entries are not repeated.
    """

    mocker.patch.dict(renpy.config.special_directory_map, {"audio": ["first", "full/audio"]})
    mocker.patch.object(renpy.config, "audio_directories", ["full/audio", "last"])

    assert loader.get_prefixes(tl=False, directory="audio") == ["", "first/", "full/audio/", "last/"]


@pytest.mark.usefixtures("loader_config")
def test_special_directory_map_is_not_modified(mocker):
    """
    Lookups must not write the configured directories back into the map, as config can't change after init.
    """

    mocker.patch.object(renpy.config, "audio_directories", ["full/audio"])

    loader.get_prefixes(tl=False, directory="audio")

    assert renpy.config.special_directory_map["audio"] == ["audio"]


@pytest.mark.usefixtures("loader_config")
def test_configured_directories_get_translated_prefixes(mocker):
    """
    A translated copy of a file in a configured directory takes priority over the original, as in a mapped directory.
    """

    mocker.patch.object(renpy.game, "preferences", SimpleNamespace(language="french"))
    mocker.patch.object(renpy.config, "audio_directories", ["full/audio"])

    assert loader.get_prefixes(directory="audio") == [
        "tl/french/",
        "",
        "tl/french/audio/",
        "audio/",
        "tl/french/full/audio/",
        "full/audio/",
    ]


@pytest.mark.usefixtures("loader_config")
def test_compatibility_variable_disables_search(mocker):
    """
    With config.add_to_special_directories False, as for games declaring compatibility with Ren'Py 8.5 or earlier, only
    the mapped directories are searched, even when the game sets the lists itself.
    """

    mocker.patch.object(renpy.config, "add_to_special_directories", False)
    mocker.patch.object(renpy.config, "audio_directories", ["full/audio"])
    mocker.patch.object(renpy.config, "image_directories", ["full/images"])

    assert loader.get_prefixes(tl=False, directory="audio") == ["", "audio/"]
    assert loader.get_prefixes(tl=False, directory="images") == ["", "images/"]
