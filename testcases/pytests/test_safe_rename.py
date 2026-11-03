import importlib.util
import json
import os
import pathlib
import stat
import sys

import pytest

import renpy
from renpy import savelocation
from renpy.compat.pickle import loads
from renpy.loadsave import SaveRecord, safe_rename
from renpy.persistent import _MultiPersistent

# The unique part of the name of a file that has been moved aside.
UNIQUE = "0123456789abcdef0123456789abcdef"


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


@pytest.fixture
def windows_replace(mocker):
    """
    Patches os.replace to refuse an existing destination, as Windows does when another program has it open.

    The program is assumed to allow deletion, so moving the file to an unused name still works. Returns the mock, so
    a test can extend its behavior. os.replace is patched module-wide, so the real function is captured first.
    """

    replace = os.replace

    def refuse_existing(source, destination):
        if os.path.exists(destination):
            raise PermissionError("destination is open")
        replace(source, destination)

    return mocker.patch("renpy.loadsave.os.replace", side_effect=refuse_existing)


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


@pytest.fixture
def location(mocker, tmp_path):
    """A FileLocation in a temporary directory. Exposing files is patched out, as these tests don't need it."""

    mocker.patch.object(renpy.util, "expose_directory")
    mocker.patch.object(renpy.util, "expose_file")
    return savelocation.FileLocation(str(tmp_path))


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


def test_renpy_safe_rename_is_public():
    """Games and common scripts such as JSONDB reach this function as renpy.safe_rename."""

    assert renpy.exports.safe_rename is safe_rename


def test_scan_does_not_list_leftover_as_a_slot(location, tmp_path):
    """Leftovers can stay until the next safe_rename, and the scan must not mistake them for saves."""

    (tmp_path / f"1-1{renpy.savegame_suffix}").write_bytes(b"new save")
    aside = tmp_path / f"1-1{renpy.savegame_suffix}.{UNIQUE}.old"
    aside.write_bytes(b"previous save")

    location.scan()

    assert list(location.mtimes) == ["1-1"]
    assert aside.exists()


@pytest.fixture
def slots(location, tmp_path):
    """Writes saves to slots 1-1 and 1-2, which tests rename between. Returns their paths."""

    source = tmp_path / f"1-1{renpy.savegame_suffix}"
    destination = tmp_path / f"1-2{renpy.savegame_suffix}"
    source.write_bytes(b"source save")
    destination.write_bytes(b"destination save")
    return source, destination


def test_rename_moves_save_to_new_slot(location, slots):
    """A rename without failures replaces the destination, and leaves no temporary file behind."""

    _, destination = slots

    location.rename("1-1", "1-2")

    assert destination.read_bytes() == b"source save"
    assert [path.name for path in destination.parent.iterdir()] == [destination.name]


@pytest.mark.parametrize("error", [OSError("rename failed"), PermissionError("rename failed")])
def test_rename_keeps_save_when_moving_it_to_temporary_name_fails(mocker, location, slots, error):
    """
    The source is the player's save, not a temporary file, so a failed rename must not delete it. Other moves use the
    real os.replace, captured first because os.replace is patched module-wide.
    """

    source, destination = slots
    replace = os.replace

    def refuse_temporary(from_filename, to_filename):
        if to_filename.endswith(savelocation.tmp):
            raise error
        replace(from_filename, to_filename)

    mocker.patch("renpy.loadsave.os.replace", side_effect=refuse_temporary)

    with pytest.raises(OSError, match="rename failed"):
        location.rename("1-1", "1-2")

    assert source.read_bytes() == b"source save"
    assert destination.read_bytes() == b"destination save"


@pytest.mark.parametrize("error", [OSError("rename failed"), PermissionError("rename failed")])
def test_rename_restores_save_when_moving_it_to_new_slot_fails(mocker, location, slots, error):
    """
    When the save has reached its temporary name but can't reach the new slot, it goes back to its original name.

    A PermissionError for every move involving the destination stands for another program blocking both replacing and
    moving that file, so the destination is kept too. Other moves use the real os.replace, captured first because
    os.replace is patched module-wide.
    """

    source, destination = slots
    replace = os.replace

    def refuse_destination(from_filename, to_filename):
        if str(destination) in (from_filename, to_filename):
            raise error
        replace(from_filename, to_filename)

    mocker.patch("renpy.loadsave.os.replace", side_effect=refuse_destination)

    with pytest.raises(OSError, match="rename failed"):
        location.rename("1-1", "1-2")

    assert source.read_bytes() == b"source save"
    assert destination.read_bytes() == b"destination save"
    assert sorted(path.name for path in source.parent.iterdir()) == sorted([source.name, destination.name])


def test_rename_restores_save_after_destination_is_moved_aside(mocker, location, slots):
    """
    When the destination can be moved aside but the save still can't take its place, the save goes back to its
    original name. The destination stays discarded, as safe_rename never restores a .old file.
    """

    source, destination = slots
    replace = os.replace

    def refuse_replacing_destination(from_filename, to_filename):
        if to_filename == str(destination):
            raise PermissionError("refused")
        replace(from_filename, to_filename)

    mocker.patch("renpy.loadsave.os.replace", side_effect=refuse_replacing_destination)

    with pytest.raises(PermissionError, match="refused"):
        location.rename("1-1", "1-2")

    assert source.read_bytes() == b"source save"
    assert not destination.exists()
    assert [path.read_bytes() for path in source.parent.glob("*.old")] == [b"destination save"]


def test_rename_leaves_save_at_temporary_name_when_it_cannot_be_moved_back(mocker, location, slots):
    """If the save can't be moved back to its original name, the file still exists under its temporary name."""

    source, destination = slots
    replace = os.replace

    def refuse_both(from_filename, to_filename):
        if to_filename == str(destination):
            raise OSError("rename failed")
        if to_filename == str(source):
            raise OSError("restore failed")
        replace(from_filename, to_filename)

    mocker.patch("renpy.loadsave.os.replace", side_effect=refuse_both)

    with pytest.raises(OSError, match="restore failed"):
        location.rename("1-1", "1-2")

    assert [path.read_bytes() for path in source.parent.glob(f"*{savelocation.tmp}")] == [b"source save"]


def test_failed_persistent_write_keeps_new_file_when_persistent_is_moved_aside(mocker, location, tmp_path):
    """
    If the persistent file has been moved aside and the new data can't take its place, persistent.new is the only
    current copy on disk. It's loaded in place of the persistent file, so it must not be removed.
    """

    persistent = tmp_path / "persistent"
    persistent.write_bytes(b"previous data")
    replace = os.replace

    def refuse_replacing_persistent(from_filename, to_filename):
        if to_filename == str(persistent):
            raise PermissionError("refused")
        replace(from_filename, to_filename)

    mocker.patch("renpy.loadsave.os.replace", side_effect=refuse_replacing_persistent)

    with pytest.raises(PermissionError, match="refused"):
        location.save_persistent(b"new data")

    assert (tmp_path / "persistent.new").read_bytes() == b"new data"


@pytest.fixture
def multipersistent(tmp_path):
    """A MultiPersistent stored in a temporary directory over an existing file. Returns (object, path)."""

    path = tmp_path / "multi"
    path.write_bytes(b"previous data")

    mp = _MultiPersistent()
    mp._filename = str(path)
    mp._name = "multi"
    mp._save_on_quit = False
    mp.value = 1
    return mp, path


def test_multipersistent_replaces_file_another_program_has_open(windows_replace, multipersistent):
    """MultiPersistent data goes through safe_rename, so a refused replacement moves the old file out of the way."""

    mp, path = multipersistent

    mp.save()

    assert loads(path.read_bytes()).value == 1
    assert [p.name for p in path.parent.iterdir()] == [path.name]


def test_failed_multipersistent_write_keeps_existing_file(mocker, multipersistent):
    """
    This used to delete the file before moving the new one into place, so a failure could lose it. The error still
    reaches the caller, and the new data stays in the .new file, as it did before.
    """

    mp, path = multipersistent
    mocker.patch("renpy.loadsave.os.replace", side_effect=OSError("disk error"))

    with pytest.raises(OSError, match="disk error"):
        mp.save()

    assert path.read_bytes() == b"previous data"
    assert loads(path.with_name("multi.new").read_bytes()).value == 1


@pytest.fixture
def jsondb(mocker, tmp_path):
    """
    A JSONDB stored in a temporary directory over an existing file, with one changed entry. Returns (object, path).

    Common scripts don't run during engine startup in these tests, but a _ren.py file is also valid Python, so the
    module is loaded from its source. JSONDBs are created during init, and save at exit, so those are patched out.
    """

    source = pathlib.Path(renpy.__file__).parent / "common" / "00db_ren.py"
    spec = importlib.util.spec_from_file_location("test_00db_ren", source)

    # Keeps bytecode for this file out of renpy/common, where a distribution could pick it up.
    mocker.patch.object(sys, "dont_write_bytecode", True)

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    mocker.patch.object(renpy.exports, "is_init_phase", return_value=True)
    mocker.patch.object(renpy.exports, "loadable", return_value=False)
    mocker.patch.object(renpy.config, "gamedir", str(tmp_path))
    mocker.patch.object(renpy.config, "developer", True)
    mocker.patch.object(renpy.config, "at_exit_callbacks", [])

    path = tmp_path / "db.json"
    path.write_text("previous data")

    db = module.JSONDB("db.json")
    db["entry"]["key"] = "value"
    return db, path


def test_jsondb_replaces_file_another_program_has_open(windows_replace, jsondb):
    """A JSONDB goes through renpy.safe_rename, so a refused replacement moves the old file out of the way."""

    db, path = jsondb

    db.save()

    assert json.loads(path.read_text()) == {"entry": {"key": "value"}}
    assert [p.name for p in path.parent.iterdir()] == [path.name]


def test_failed_jsondb_write_keeps_existing_file(mocker, jsondb):
    """
    This used to delete the file before moving the new one into place, so a failure could lose it. The error still
    reaches the caller, and the new data stays in the .new file, as it did before.
    """

    db, path = jsondb
    mocker.patch("renpy.loadsave.os.replace", side_effect=OSError("disk error"))

    with pytest.raises(OSError, match="disk error"):
        db.save()

    assert path.read_text() == "previous data"
    assert json.loads(path.with_name("db.json.new").read_text()) == {"entry": {"key": "value"}}
