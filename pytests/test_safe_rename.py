import os

import pytest

import renpy
from renpy.loadsave import SaveRecord, safe_rename


@pytest.fixture
def save_files(tmp_path):
    """A new save written to "save.new" next to an existing save it should replace. Returns (old, new)."""

    old = tmp_path / "save.new"
    new = tmp_path / "save"
    old.write_bytes(b"new save")
    new.write_bytes(b"previous save")
    return old, new


def test_transient_failure_retries_without_removing_existing_save(mocker, save_files):
    """
    When replacing the save fails once, safe_rename retries and succeeds.

    The existing save must still be intact at each attempt: deleting it before replacing it would lose
    the player's save if the replacement then failed. os.replace is patched module-wide, so the real
    function is captured first.
    """

    old, new = save_files
    replace = os.replace

    def fail_once(source, destination):
        assert new.read_bytes() == b"previous save"
        if replacement.call_count == 1:
            raise OSError("temporary failure")
        replace(source, destination)

    replacement = mocker.patch("renpy.loadsave.os.replace", side_effect=fail_once)

    safe_rename(old, new)

    assert replacement.call_count == 2
    assert new.read_bytes() == b"new save"
    assert not old.exists()


def test_repeated_failure_preserves_existing_save_and_removes_temporary_file(mocker, save_files):
    """
    When both attempts to replace the save fail, the error propagates, the existing save is kept, and
    the temporary new file is removed so it doesn't linger next to the save.
    """

    old, new = save_files
    replacement = mocker.patch("renpy.loadsave.os.replace", side_effect=OSError("replace failed"))

    with pytest.raises(OSError, match="replace failed"):
        safe_rename(old, new)

    assert replacement.call_count == 2
    assert not old.exists()
    assert new.read_bytes() == b"previous save"


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
