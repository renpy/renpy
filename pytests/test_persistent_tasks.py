"""Tests for the cooperative persistent-data tasks and their interaction with the interface."""

from concurrent.futures import Future
from types import SimpleNamespace

import pytest

import renpy
from renpy import persistent
from renpy.display.core import Interface


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


def test_save_yields_between_major_operations(mocker, location):
    """
    The save task yields between dumping, compressing, signing, and writing, so a long save does not block
    the interaction loop. Each step is recorded in order, and the task yields three times before the write.
    The pending flag is cleared once the write has happened.
    """

    events = []

    mocker.patch.object(persistent, "dumps", side_effect=lambda *a, **kw: events.append("dump") or b"data")
    mocker.patch.object(persistent.zlib, "compress", side_effect=lambda *a: events.append("compress") or b"zip")
    mocker.patch.object(renpy.savetoken, "sign_data", side_effect=lambda *a: events.append("sign") or "sig")
    mocker.patch.object(location, "save_persistent", side_effect=lambda data, **kwargs: events.append(("write", data)))

    task = persistent.save_task()
    for _ in range(3):
        assert next(task) is None
        events.append("yield")
    with pytest.raises(StopIteration):
        next(task)

    assert events == ["dump", "yield", "compress", "yield", "sign", "yield", ("write", b"zipsig")]
    assert not persistent.pending_save


def test_sync_entry_points_and_restart(mocker, location, encoding):
    """
    The synchronous entry points (check_update, update, and save) run their tasks to completion. check_update
    merges data written by another process and restarts the interaction. Writes made through these entry
    points are foreground writes, so they are not marked as background.
    """

    location.data = [(5, object())]
    merge = mocker.patch.object(persistent, "merge")
    restart = mocker.patch.object(renpy.exports, "restart_interaction")

    assert persistent.check_update() is None
    merge.assert_called_once()
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


def test_late_background_failure_does_not_retry(mocker, location, encoding):
    """
    A background write that fails after its save task has finished is not retried. The failure is reported
    through the future, pending_save stays cleared, and persistent_mtime is not advanced.
    """

    future = Future()
    mocker.patch.object(location, "save_persistent", return_value=future)

    renpy.asynctask.run_sync(persistent.save_task())

    future.set_exception(OSError("disk error"))
    assert not persistent.pending_save
    assert persistent.persistent_mtime == 0


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


@pytest.mark.parametrize("emscripten", [False, True], ids=["desktop", "web"])
def test_interface_runs_platform_persistent_maintenance(mocker, emscripten):
    """
    The interface's filesystem task runs exactly one persistent-maintenance task for the platform. Desktop
    runs check_update_task and the web runs update_task. Both are patched to a single yield, and the
    interface is marked as having done its persistent work afterwards.
    """

    interface = SimpleNamespace(did_autosave=True, did_persistent=False)

    def maintenance():
        """A maintenance task that finishes after one step."""

        yield

    mocker.patch.object(renpy, "emscripten", emscripten)
    check = mocker.patch.object(persistent, "check_update_task", side_effect=maintenance)
    update = mocker.patch.object(persistent, "update_task", side_effect=maintenance)

    renpy.asynctask.run_sync(Interface.run_filesystem_task(interface))

    assert check.call_count == (not emscripten)
    assert update.call_count == emscripten
    assert interface.did_persistent


def test_interface_retries_after_cancellation(mocker):
    """
    Cancelling the interface's filesystem task while check_update_task is running runs the maintenance task's
    cleanup and leaves did_persistent unset, so the next interaction retries the maintenance.
    """

    interface = SimpleNamespace(did_autosave=True, did_persistent=False)
    cleaned = []

    def maintenance():
        """A maintenance task that records when it is cleaned up."""

        try:
            yield
        finally:
            cleaned.append(True)

    mocker.patch.object(renpy, "emscripten", False)
    mocker.patch.object(persistent, "check_update_task", side_effect=maintenance)

    task = Interface.run_filesystem_task(interface)
    assert next(task) is None
    task.close()

    assert not interface.did_persistent
    assert cleaned == [True]
