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

import os
import stat

import pytest

import renpy
import renpy.util


def make_directory(path, mode):
    """Creates a directory with exactly `mode`, skipping the test if the filesystem won't hold the requested bits."""

    path.mkdir()
    os.chmod(path, mode)

    actual = stat.S_IMODE(os.stat(path).st_mode)
    if actual != mode:
        pytest.skip(f"The filesystem stored mode {actual:o} when {mode:o} was requested.")

    return path


def test_expose_directory_keeps_setgid_directory_on_android(tmp_path, mocker):
    """
    An Android setgid directory is left exactly as it was.

    Android's external app directories are setgid so that new files inherit ext_data_rw, and chmod would clear that
    bit. A mode without full group access is used so the test notices any chmod, not just one that clears setgid.
    """

    mocker.patch.object(renpy, "android", True)
    directory = make_directory(tmp_path / "saves", 0o2750)

    renpy.util.expose_directory(str(directory))

    assert stat.S_IMODE(os.stat(directory).st_mode) == 0o2750


def test_expose_directory_grants_group_access_on_android(tmp_path, mocker):
    """An Android directory that isn't setgid, such as app-private storage, still gets group access."""

    mocker.patch.object(renpy, "android", True)
    directory = make_directory(tmp_path / "saves", 0o700)

    renpy.util.expose_directory(str(directory))

    assert stat.S_IMODE(os.stat(directory).st_mode) == 0o770


def test_expose_directory_ignores_other_platforms(tmp_path, mocker):
    """Other platforms keep whatever permissions the directory already has."""

    mocker.patch.object(renpy, "android", False)
    directory = make_directory(tmp_path / "saves", 0o700)

    renpy.util.expose_directory(str(directory))

    assert stat.S_IMODE(os.stat(directory).st_mode) == 0o700


################################################################################
# repair_directory
################################################################################


@pytest.fixture
def damaged(tmp_path, mocker):
    """
    A setgid `files` directory holding a `saves` directory that lost setgid, as older versions left it on Android.

    The umask is the one bootstrap sets on Android, which is what gives new directories group access.
    """

    mocker.patch.object(renpy, "android", True)
    old_umask = os.umask(0o007)

    try:
        parent = make_directory(tmp_path / "files", 0o2770)
        saves = parent / "saves"
        saves.mkdir()
        os.chmod(saves, 0o770)

        (saves / "1-1.save").write_bytes(b"save")
        os.utime(saves / "1-1.save", ns=(1_000_000_000, 2_000_000_000))
        (saves / "sync").mkdir()
        os.chmod(saves / "sync", 0o770)
        (saves / "sync" / "nested.save").write_bytes(b"nested")

        yield saves

    finally:
        os.umask(old_umask)


def sibling_names(saves):
    """Returns the names in the directory containing `saves`, which shows any leftover repair directories."""

    return sorted(os.listdir(saves.parent))


def assert_saves_intact(saves):
    """Checks that the fixture's save data is all readable at `saves`."""

    assert (saves / "1-1.save").read_bytes() == b"save"
    assert (saves / "sync" / "nested.save").read_bytes() == b"nested"


def copy_saves(saves, name, mode=0o2770):
    """Copies the fixture's files to a sibling of `saves`, as an interrupted repair would have left them."""

    target = saves.parent / name
    target.mkdir()
    os.chmod(target, mode)
    (target / "sync").mkdir()
    (target / "1-1.save").write_bytes(b"save")
    (target / "sync" / "nested.save").write_bytes(b"nested")
    return target


def test_repair_directory_restores_setgid_and_keeps_data(damaged):
    """A damaged directory, and those inside it, become setgid, with their files and modification times unchanged."""

    renpy.util.repair_directory(str(damaged))

    assert renpy.util.is_setgid(damaged)
    assert renpy.util.is_setgid(damaged / "sync")
    assert_saves_intact(damaged)
    assert os.stat(damaged / "1-1.save").st_mtime_ns == 2_000_000_000
    assert sibling_names(damaged) == ["saves"]


def test_repair_directory_gives_setgid_directory_group_access(damaged):
    """A setgid directory its group can't enter is rebuilt, since chmod would clear the bit on Android."""

    os.chmod(damaged, 0o2700)

    renpy.util.repair_directory(str(damaged))

    assert stat.S_IMODE(os.stat(damaged).st_mode) == 0o2770
    assert_saves_intact(damaged)
    assert sibling_names(damaged) == ["saves"]


def test_repair_directory_runs_once(damaged):
    """Once repaired, a directory isn't copied again, as this runs on every startup."""

    renpy.util.repair_directory(str(damaged))
    inode = os.stat(damaged).st_ino

    renpy.util.repair_directory(str(damaged))

    assert os.stat(damaged).st_ino == inode


def test_repair_directory_ignores_directory_outside_setgid_parent(damaged):
    """A directory whose parent isn't setgid, such as one in app-private storage, was never damaged."""

    os.chmod(damaged.parent, 0o770)
    inode = os.stat(damaged).st_ino

    renpy.util.repair_directory(str(damaged))

    assert os.stat(damaged).st_ino == inode
    assert not renpy.util.is_setgid(damaged)


def test_repair_directory_ignores_other_platforms(damaged, mocker):
    """Nothing is repaired off Android."""

    mocker.patch.object(renpy, "android", False)

    renpy.util.repair_directory(str(damaged))

    assert not renpy.util.is_setgid(damaged)


def test_repair_directory_keeps_original_when_copy_fails(damaged, mocker):
    """A failed copy, like running out of space, leaves the saves where they were and removes the partial copy."""

    mocker.patch.object(renpy.util.shutil, "copyfile", side_effect=OSError("No space left"))

    renpy.util.repair_directory(str(damaged))

    assert not renpy.util.is_setgid(damaged)
    assert_saves_intact(damaged)
    assert sibling_names(damaged) == ["saves"]


def test_repair_directory_undoes_swap_when_rename_fails(damaged, mocker):
    """If the copy can't be moved into place, the original directory goes back to its name."""

    real_rename = os.rename

    def fail_moving_repair(src, dst):
        if src.endswith(renpy.util.REPAIR_SUFFIX):
            raise OSError("Rename failed")

        real_rename(src, dst)

    mocker.patch.object(renpy.util.os, "rename", side_effect=fail_moving_repair)

    renpy.util.repair_directory(str(damaged))

    assert not renpy.util.is_setgid(damaged)
    assert_saves_intact(damaged)
    assert sibling_names(damaged) == ["saves"]


def test_repair_directory_recovers_after_undo_fails(damaged, mocker):
    """If the swap can't be undone either, the complete copy is kept, and a later call can finish the swap with it."""

    real_rename = os.rename

    def fail_after_moving_original(src, dst):
        if not src.endswith(renpy.util.REPLACED_SUFFIX) and not src.endswith(renpy.util.REPAIR_SUFFIX):
            real_rename(src, dst)
            return

        raise OSError("Rename failed")

    patch = mocker.patch.object(renpy.util.os, "rename", side_effect=fail_after_moving_original)

    renpy.util.repair_directory(str(damaged))

    assert not damaged.exists()
    assert sorted(os.listdir(damaged.parent)) == [
        "saves" + renpy.util.REPAIR_SUFFIX,
        "saves" + renpy.util.REPLACED_SUFFIX,
    ]

    mocker.stop(patch)
    renpy.util.repair_directory(str(damaged))

    assert renpy.util.is_setgid(damaged)
    assert_saves_intact(damaged)
    assert sibling_names(damaged) == ["saves"]


@pytest.mark.parametrize(
    "with_repair",
    [False, True],
    ids=["replaced_only", "repair_and_replaced"],
)
def test_repair_directory_keeps_saves_when_something_else_created_directory(damaged, with_repair):
    """
    A new setgid `saves` isn't proof of a finished repair.

    The save token system can create the directory holding only its keys. It inherits setgid from its parent, so the
    originals must only be deleted if the directory actually holds them.
    """

    replaced = damaged.parent / ("saves" + renpy.util.REPLACED_SUFFIX)
    os.rename(damaged, replaced)

    if with_repair:
        copy_saves(damaged, "saves" + renpy.util.REPAIR_SUFFIX)

    damaged.mkdir()
    (damaged / "security_keys.txt").write_bytes(b"keys")
    assert renpy.util.is_setgid(damaged)

    renpy.util.repair_directory(str(damaged))

    assert_saves_intact(replaced)


def test_repair_directory_keeps_original_with_unsupported_entry(damaged):
    """An entry that can't be copied stops the repair, since replacing the directory would lose it."""

    os.symlink("1-1.save", damaged / "link")

    renpy.util.repair_directory(str(damaged))

    assert os.path.islink(damaged / "link")
    assert not renpy.util.is_setgid(damaged)
    assert sibling_names(damaged) == ["saves"]


def test_repair_directory_needs_group_access(damaged):
    """If new directories wouldn't get group access, nothing is gained by copying, and it would repeat every launch."""

    os.umask(0o077)
    inode = os.stat(damaged).st_ino

    renpy.util.repair_directory(str(damaged))

    assert os.stat(damaged).st_ino == inode
    assert sibling_names(damaged) == ["saves"]


def test_repair_directory_finishes_interrupted_swap(damaged):
    """After a crash between the two renames, the complete copy is used even though `saves` is missing."""

    copy_saves(damaged, "saves" + renpy.util.REPAIR_SUFFIX)
    os.rename(damaged, str(damaged) + renpy.util.REPLACED_SUFFIX)

    renpy.util.repair_directory(str(damaged))

    assert renpy.util.is_setgid(damaged)
    assert_saves_intact(damaged)
    assert sibling_names(damaged) == ["saves"]


def test_repair_directory_restores_original_without_copy(damaged):
    """With only the original left, it's moved back and then repaired normally, so no saves appear to vanish."""

    os.rename(damaged, str(damaged) + renpy.util.REPLACED_SUFFIX)

    renpy.util.repair_directory(str(damaged))

    assert renpy.util.is_setgid(damaged)
    assert_saves_intact(damaged)
    assert sibling_names(damaged) == ["saves"]


def test_repair_directory_finishes_interrupted_delete(damaged):
    """After a crash while deleting the original, the swap is complete and only the deletion remains."""

    os.rename(damaged, str(damaged) + renpy.util.REPLACED_SUFFIX)
    copy_saves(damaged, "saves")

    renpy.util.repair_directory(str(damaged))

    assert renpy.util.is_setgid(damaged)
    assert_saves_intact(damaged)
    assert sibling_names(damaged) == ["saves"]


def test_repair_directory_discards_interrupted_copy(damaged):
    """A partial copy from a crash isn't trusted: it's rebuilt from the original."""

    partial = damaged.parent / ("saves" + renpy.util.REPAIR_SUFFIX)
    partial.mkdir()
    (partial / "1-1.save").write_bytes(b"truncated")

    renpy.util.repair_directory(str(damaged))

    assert renpy.util.is_setgid(damaged)
    assert_saves_intact(damaged)
    assert sibling_names(damaged) == ["saves"]


def test_repair_directory_deletes_nothing_in_unknown_state(damaged):
    """A replaced directory beside a `saves` that was never swapped isn't a state repair produces, so it's preserved."""

    other = copy_saves(damaged, "saves" + renpy.util.REPLACED_SUFFIX)

    renpy.util.repair_directory(str(damaged))

    assert_saves_intact(damaged)
    assert_saves_intact(other)
