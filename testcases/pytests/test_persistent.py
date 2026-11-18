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
Tests for renpy/persistent.py: the cooperative save, update, and check_update tasks, and the MultiPersistent
files that are written through safe_rename.
"""

from concurrent.futures import Future
from types import SimpleNamespace

import pytest

import renpy
from renpy import persistent
from renpy.compat.pickle import loads
from renpy.persistent import _MultiPersistent

################################################################################
# Persistent tasks: save_task, update_task, and check_update
################################################################################


class Location:
    """
    Stands in for the save location. It holds persistent data to be loaded and records writes, so tests
    can inspect them without touching the filesystem.
    """

    def __init__(self):
        self.data = []
        self.saved = []
        self.background_modes = []

    def load_persistent(self, *, consume=False):
        rv = list(self.data)
        if consume:
            self.data.clear()
        return rv

    def save_persistent(self, data, background=False):
        self.saved.append(data)
        self.background_modes.append(background)


@pytest.fixture
def location():
    """A fake save location that holds no persistent data yet."""

    return Location()


@pytest.fixture
def game_persistent():
    """Stands in for renpy.game.persistent, with no fields changed since the last save."""

    return SimpleNamespace(_changed={}, value=1)


@pytest.fixture(autouse=True)
def persistent_state(mocker, location, game_persistent):
    """
    Points the persistent module at the fake location and game persistent, with a clean backup and mtime.
    The async task runner is reset before and after each test so a task left over from one test cannot run
    during another.
    """

    mocker.patch.object(renpy.loadsave, "location", location)
    mocker.patch.object(renpy.game, "persistent", game_persistent)
    mocker.patch.object(renpy.config, "save_persistent", True)
    mocker.patch.object(persistent, "backup", {"value": 0})
    mocker.patch.object(persistent, "persistent_mtime", 0)
    mocker.patch.object(persistent, "pending_save", False)

    renpy.asynctask.reset()
    yield
    renpy.asynctask.reset()


@pytest.fixture
def encoding(mocker):
    """
    Replaces pickling, compression, and signing with fixed values, so the data written to the location is
    always b"zipsig".
    """

    mocker.patch.object(persistent, "dumps", return_value=b"data")
    mocker.patch.object(persistent.zlib, "compress", return_value=b"zip")
    mocker.patch.object(renpy.savetoken, "sign_data", return_value="sig")


def test_save_yields_between_major_operations(location, encoding):
    """
    The save task yields to the event loop more than once before it writes, so a long save does not block
    the interaction loop. Nothing is written at any of those yields, the write happens once the task is
    resumed after them, and the pending flag is cleared afterwards.

    The exact number and placement of the yields is deliberately not pinned, only that the work is split up.
    """

    task = persistent.save_task()
    yields = 0

    while True:
        try:
            assert next(task) is None
        except StopIteration:
            break

        yields += 1
        assert location.saved == []

    assert yields >= 2
    assert location.saved == [b"zipsig"]
    assert not persistent.pending_save


def test_sync_entry_points_and_restart(mocker, location, game_persistent, encoding):
    """
    The synchronous entry points (check_update, update, and save) run their tasks to completion. check_update
    merges data written by another process into the persistent object, saves the result, and restarts the
    interaction. Writes made through these entry points are foreground writes, so they are not marked as
    background.

    The other process's data is a stand-in object with a field the current persistent object lacks, stamped
    long ago, so the merge keeps it. restart_interaction is patched because there is no interface to restart.
    """

    location.data = [(5, SimpleNamespace(_changed={"extra": 1.0}, extra=3))]
    restart = mocker.patch.object(renpy.exports, "restart_interaction")

    assert persistent.check_update() is None
    assert game_persistent.extra == 3
    restart.assert_called_once()
    assert persistent.persistent_mtime == 5
    assert location.saved == [b"zipsig"]

    assert persistent.update(True) is None
    assert persistent.save() is None

    assert location.saved == [b"zipsig"] * 3
    assert location.background_modes == [False] * 3


def test_task_save_queues_without_waiting_for_disk(mocker, location, encoding):
    """
    A save task hands its write to the background thread and finishes without waiting for the disk. The
    persistent_mtime only advances when the returned future completes successfully, so it stays at 0 until
    then.
    """

    future = Future()
    save = mocker.patch.object(location, "save_persistent", return_value=future)

    renpy.asynctask.run_sync(persistent.save_task())

    save.assert_called_once_with(b"zipsig", background=True)
    assert not future.done()
    assert not persistent.pending_save
    assert persistent.persistent_mtime == 0

    future.set_result(9)
    assert persistent.persistent_mtime == 9


def test_completed_background_write_mtime_is_not_overwritten_by_update(mocker, location):
    """
    When a background write completes while update_task is merging, its result becomes persistent_mtime.
    The loaded data has the older mtime 5, but the final value must be the completed write's mtime, 10.
    The write's done callback is wired up by hand here, as save_task would do.
    """

    persistent.backup["value"] = 1
    location.data = [(5, object())]
    write = Future()
    write.add_done_callback(persistent._background_save_completed)

    mocker.patch.object(persistent, "merge", side_effect=lambda other: write.set_result(10))

    renpy.asynctask.run_sync(persistent.update_task())

    assert persistent.persistent_mtime == 10


def test_unchanged_update_does_not_save(mocker, location):
    """
    When the persistent data matches the backup, update does not encode anything, leaves pending_save clear,
    and writes nothing to the location.
    """

    persistent.backup["value"] = 1
    dumps = mocker.patch.object(persistent, "dumps")

    assert persistent.update() is None

    dumps.assert_not_called()
    assert not persistent.pending_save
    assert location.saved == []


def test_cancelled_update_retries_pending_save(location, encoding):
    """
    An update cancelled before it writes leaves pending_save set, so the next check_update retries the save.
    run_for_ns(1) advances the task by one step before reset cancels it. The backup has already been updated
    to the new state at that point.
    """

    task = renpy.asynctask.create_task(persistent.update_task())
    renpy.asynctask.run_for_ns(1)

    assert not task.done()
    assert persistent.pending_save
    assert persistent.backup["value"] == 1
    renpy.asynctask.reset()

    assert persistent.check_update() is None
    assert location.saved == [b"zipsig"]
    assert not persistent.pending_save


def test_cancelled_after_merge_does_not_drop_consumed_data(mocker, location, encoding):
    """
    Data consumed from the location before a cancellation is merged once and not lost. After the cancel the
    location no longer holds it, so the retry in check_update must not merge it again.
    """

    other = object()
    location.data = [(5, other)]
    merge = mocker.patch.object(persistent, "merge")

    task = renpy.asynctask.create_task(persistent.update_task())
    renpy.asynctask.run_for_ns(1)
    renpy.asynctask.run_for_ns(1)

    assert not task.done()
    merge.assert_called_once_with(other)
    assert location.data == []
    assert persistent.persistent_mtime == 5
    renpy.asynctask.reset()

    assert persistent.check_update() is None
    assert location.saved == [b"zipsig"]
    merge.assert_called_once_with(other)


def test_cancelled_save_retries_on_next_check(location, encoding):
    """
    A save cancelled partway through leaves pending_save set, and the next check_update performs the save so
    the data is not lost. run_for_ns(1) advances the task by one step before reset cancels it.
    """

    task = renpy.asynctask.create_task(persistent.save_task())
    renpy.asynctask.run_for_ns(1)

    assert not task.done()
    assert persistent.pending_save
    renpy.asynctask.reset()

    assert persistent.check_update() is None
    assert location.saved == [b"zipsig"]
    assert not persistent.pending_save


################################################################################
# MultiPersistent files
################################################################################


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
