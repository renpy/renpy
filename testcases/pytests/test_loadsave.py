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
Tests for the safe replacement of files written by renpy.loadsave: safe_rename, and the SaveRecord that uses it.

These are data-loss tests. A save, or the previous copy of a save, must survive whatever the filesystem refuses
to do, and files moved aside to make room must never be restored or left behind.
"""

import os
import stat

import pytest

import renpy
from renpy.loadsave import SaveRecord, safe_rename

# The unique part of the name of a file that has been moved aside.
UNIQUE = "0123456789abcdef0123456789abcdef"


################################################################################
# Failures that must not lose the existing save (safe_rename and SaveRecord.write_file)
################################################################################


@pytest.fixture
def save_files(tmp_path):
    """A new save written to "save.new" next to an existing save it should replace. Returns (old, new)."""

    old = tmp_path / "save.new"
    new = tmp_path / "save"
    old.write_bytes(b"new save")
    new.write_bytes(b"previous save")
    return old, new


def test_failure_other_than_refusal_preserves_existing_save_and_removes_temporary_file(mocker, save_files):
    """
    When replacing the save fails with anything but a permission error, moving the save wouldn't help. The error
    propagates after a single attempt, the existing save is kept, and the temporary new file is removed so it doesn't
    linger next to the save.
    """

    old, new = save_files
    replacement = mocker.patch("renpy.loadsave.os.replace", side_effect=OSError("replace failed"))

    with pytest.raises(OSError, match="replace failed"):
        safe_rename(old, new)

    assert replacement.call_count == 1
    assert not old.exists()
    assert new.read_bytes() == b"previous save"


def test_transient_refusal_without_destination_succeeds(mocker, tmp_path):
    """
    When a first-time rename is refused once and then works, there's nothing to move aside or delete. The missing
    .old file must not be reported as a failure, as the new save is in place.
    """

    old = tmp_path / "save.new"
    new = tmp_path / "save"
    old.write_bytes(b"new save")
    replace = os.replace

    def refuse_once(source, destination):
        if replacement.call_count == 1:
            raise PermissionError("temporary failure")
        replace(source, destination)

    replacement = mocker.patch("renpy.loadsave.os.replace", side_effect=refuse_once)

    safe_rename(old, new)

    assert new.read_bytes() == b"new save"
    assert [path.name for path in tmp_path.iterdir()] == ["save"]


def test_failed_save_record_does_not_record_success_or_leave_temporary_file(mocker, tmp_path):
    """
    When writing a SaveRecord fails at the rename, the record doesn't remember the file as written,
    no ".new" file is left behind, and the previous save is unchanged.

    first_filename is how a record that is saved to several slots copies the first written file instead
    of rewriting it, so it must not point at a file that was never written. Signing is patched out
    because no save token is set up.
    """

    mocker.patch.object(renpy.savetoken, "sign_data", return_value=b"")
    mocker.patch("renpy.loadsave.os.replace", side_effect=OSError("replace failed"))
    filename = tmp_path / "save"
    filename.write_bytes(b"previous save")
    record = SaveRecord(None, "", "{}", b"log")

    with pytest.raises(OSError, match="replace failed"):
        record.write_file(str(filename))

    assert record.first_filename is None
    assert not (tmp_path / "save.new").exists()
    assert filename.read_bytes() == b"previous save"


################################################################################
# A destination another program has open (Windows semantics)
################################################################################


def test_replaces_save_another_program_has_open(windows_replace, save_files):
    """A save that can't be replaced directly is moved aside and replaced, leaving no other files behind (#7491)."""

    old, new = save_files

    safe_rename(old, new)

    assert new.read_bytes() == b"new save"
    assert [path.name for path in new.parent.iterdir()] == ["save"]


def test_save_that_cannot_be_moved_aside_is_preserved(mocker, save_files):
    """
    When the other program also blocks deletion, the error propagates, the save is kept, and the temporary file is
    removed. Every os.replace fails, which is what a file opened without delete sharing does on Windows.
    """

    old, new = save_files
    mocker.patch("renpy.loadsave.os.replace", side_effect=PermissionError("sharing violation"))

    with pytest.raises(PermissionError, match="sharing violation"):
        safe_rename(old, new)

    assert new.read_bytes() == b"previous save"
    assert [path.name for path in new.parent.iterdir()] == ["save"]


def test_failure_to_delete_moved_aside_save_does_not_fail_the_save(mocker, windows_replace, save_files):
    """
    The new save is already in place when the moved-aside file is deleted, so failing to delete it isn't an error.
    The file stays for a later safe_rename to clean up.
    """

    old, new = save_files
    mocker.patch("renpy.loadsave.os.unlink", side_effect=PermissionError("delete failed"))

    safe_rename(old, new)

    assert new.read_bytes() == b"new save"
    assert [path.read_bytes() for path in new.parent.glob("*.old")] == [b"previous save"]


def test_file_moved_aside_earlier_does_not_block_a_later_replacement(mocker, windows_replace, save_files):
    """
    A file moved aside earlier may still be open and undeletable, so each move needs a name of its own. The fake
    os.replace refuses an existing destination, so reusing a name would fail the second replacement.
    """

    old, new = save_files
    mocker.patch("renpy.loadsave.os.unlink", side_effect=PermissionError("delete failed"))

    safe_rename(old, new)
    old.write_bytes(b"newer save")
    safe_rename(old, new)

    assert new.read_bytes() == b"newer save"
    assert sorted(path.read_bytes() for path in new.parent.glob("*.old")) == [b"new save", b"previous save"]


def test_existing_save_is_discarded_when_new_save_cannot_be_moved_into_place(windows_replace, save_files):
    """
    Moving the existing save aside only makes room for the new one, so it isn't moved back if the new save can't take
    its place. The error propagates, and the moved file is left for a later safe_rename to delete.
    """

    old, new = save_files
    refuse_existing = windows_replace.side_effect

    def refuse_source(source, destination):
        if source == old:
            raise PermissionError("refused")
        refuse_existing(source, destination)

    windows_replace.side_effect = refuse_source

    with pytest.raises(PermissionError, match="refused"):
        safe_rename(old, new)

    assert not new.exists()
    assert not old.exists()
    assert [path.read_bytes() for path in new.parent.glob("*.old")] == [b"previous save"]


def test_refused_rename_without_destination_propagates_error(mocker, tmp_path):
    """
    With no destination there's nothing to move aside, so the PermissionError from the rename is what propagates,
    rather than the FileNotFoundError that moving the missing destination would raise.
    """

    old = tmp_path / "save.new"
    old.write_bytes(b"new save")
    replace = os.replace

    def refuse_source(source, destination):
        if source == old:
            raise PermissionError("refused")
        replace(source, destination)

    mocker.patch("renpy.loadsave.os.replace", side_effect=refuse_source)

    with pytest.raises(PermissionError, match="refused"):
        safe_rename(old, tmp_path / "save")


def test_read_only_save_is_replaced_and_moved_aside_file_is_deleted(mocker, windows_replace, save_files):
    """
    A read-only save is replaced like any other, and the moved-aside file is still deleted. os.unlink is patched to
    refuse read-only files as Windows does. It checks the mode bits, so the test behaves the same when run as root.
    """

    old, new = save_files
    new.chmod(stat.S_IREAD)
    unlink = os.unlink

    def refuse_read_only(path):
        if not os.stat(path).st_mode & stat.S_IWRITE:
            raise PermissionError("file is read-only")
        unlink(path)

    mocker.patch("renpy.loadsave.os.unlink", side_effect=refuse_read_only)

    safe_rename(old, new)

    assert new.read_bytes() == b"new save"
    assert [path.name for path in new.parent.iterdir()] == ["save"]


################################################################################
# Files moved aside, and cleaning up leftovers
################################################################################


@pytest.mark.parametrize("original", [f"1-1{renpy.savegame_suffix}", "persistent", "persistent.new"])
@pytest.mark.parametrize("original_exists", [True, False])
def test_safe_rename_deletes_leftover_and_never_restores_it(save_files, tmp_path, original, original_exists):
    """
    Every call removes files moved aside earlier, even when nothing is locked now and the file belongs to another
    name in the directory. Such a file is discarded whether or not its original exists, as restoring it could bring
    back a save the player deleted.
    """

    old, new = save_files

    if original_exists:
        (tmp_path / original).write_bytes(b"current")

    (tmp_path / f"{original}.{UNIQUE}.old").write_bytes(b"previous")

    safe_rename(old, new)

    expected = {new.name, original} if original_exists else {new.name}
    assert {path.name for path in tmp_path.iterdir()} == expected
    assert new.read_bytes() == b"new save"

    if original_exists:
        assert (tmp_path / original).read_bytes() == b"current"


def test_safe_rename_deletes_what_an_earlier_call_left_behind(mocker, windows_replace, save_files):
    """
    A moved-aside file that was still open when its call finished is removed by the next call. This also checks that
    the names safe_rename gives these files are ones it recognizes, or they would never be deleted.
    """

    old, new = save_files
    unlink = mocker.patch("renpy.loadsave.os.unlink", side_effect=PermissionError("still open"))

    safe_rename(old, new)
    assert len(list(new.parent.glob("*.old"))) == 1

    mocker.stop(unlink)
    mocker.stop(windows_replace)

    old.write_bytes(b"newer save")
    safe_rename(old, new)

    assert [path.name for path in new.parent.iterdir()] == [new.name]
    assert new.read_bytes() == b"newer save"


def test_safe_rename_succeeds_when_leftover_cannot_be_deleted(mocker, save_files, tmp_path):
    """A leftover that's still open is kept for a later call, and mustn't stop this rename."""

    old, new = save_files
    aside = tmp_path / f"other.{UNIQUE}.old"
    aside.write_bytes(b"previous save")
    mocker.patch("renpy.loadsave.os.unlink", side_effect=PermissionError("still open"))

    safe_rename(old, new)

    assert aside.exists()
    assert new.read_bytes() == b"new save"


def test_safe_rename_succeeds_when_directory_cannot_be_listed(mocker, save_files):
    """Cleanup is only housekeeping, so failing to list the directory mustn't stop the rename."""

    old, new = save_files
    mocker.patch("renpy.loadsave.os.listdir", side_effect=PermissionError("listing refused"))

    safe_rename(old, new)

    assert new.read_bytes() == b"new save"


def test_safe_rename_cleans_up_for_a_name_without_a_directory(monkeypatch, save_files, tmp_path):
    """A bare filename has an empty directory name, which os.listdir can't list. It means the current directory."""

    old, new = save_files
    aside = tmp_path / f"other.{UNIQUE}.old"
    aside.write_bytes(b"previous save")
    monkeypatch.chdir(tmp_path)

    safe_rename(old.name, new.name)

    assert not aside.exists()
    assert new.read_bytes() == b"new save"


def test_safe_rename_leaves_unrelated_files_alone(save_files, tmp_path):
    """
    The directory can hold other files, so a .old file is only cleaned up if it has the unique part of the name.
    """

    old, new = save_files
    names = ["notes.old", f"1-1{renpy.savegame_suffix}.old", "notes.0123abcd.old", f"notes.{UNIQUE}.old.txt"]

    for name in names:
        (tmp_path / name).write_bytes(b"keep")

    safe_rename(old, new)

    assert sorted(path.name for path in tmp_path.iterdir()) == sorted([*names, new.name])


def test_refused_replacement_of_directory_does_not_move_it_aside(mocker, tmp_path):
    """
    Windows refuses to replace a directory with a permission error, as it does an open file. Moving the directory
    aside would succeed, and the rename would then appear to work while the directory stayed under a .old name
    forever, so the error is reported instead. Only public callers can pass a directory.
    """

    source = tmp_path / "source"
    source.write_bytes(b"data")
    directory = tmp_path / "directory"
    directory.mkdir()
    (directory / "file").write_bytes(b"keep")
    replace = os.replace

    def refuse_directory(source, destination):
        if os.path.isdir(destination):
            raise PermissionError("destination is a directory")
        replace(source, destination)

    mocker.patch("renpy.loadsave.os.replace", side_effect=refuse_directory)

    with pytest.raises(PermissionError, match="destination is a directory"):
        safe_rename(source, directory)

    assert (directory / "file").read_bytes() == b"keep"
    assert not list(tmp_path.glob("*.old"))
    assert not source.exists()


################################################################################
# Public API
################################################################################


def test_renpy_safe_rename_is_public():
    """Games and common scripts such as JSONDB reach this function as renpy.safe_rename."""

    assert renpy.exports.safe_rename is safe_rename
