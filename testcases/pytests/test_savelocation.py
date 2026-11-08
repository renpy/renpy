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
Tests for renpy/savelocation.py: FileLocation's safe rename and scan behavior, loading persistent data while
the scan thread publishes it, and the background worker that performs queued persistent writes.
"""

import os
import tempfile
import threading
from collections import deque
from concurrent.futures import Future
from types import SimpleNamespace

import pytest

import renpy
from renpy import savelocation

# The unique part of the name of a file that has been moved aside.
UNIQUE = "0123456789abcdef0123456789abcdef"


################################################################################
# Safe rename and scan
################################################################################


@pytest.fixture
def location(mocker, tmp_path):
    """A FileLocation in a temporary directory. Exposing files is patched out, as these tests don't need it."""

    mocker.patch.object(renpy.util, "expose_directory")
    mocker.patch.object(renpy.util, "expose_file")
    return savelocation.FileLocation(str(tmp_path))


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


################################################################################
# Loading persistent data
################################################################################


@pytest.fixture
def bare_location():
    """A bare FileLocation that already holds persistent data with mtime 1, without scanning the disk."""

    location = savelocation.FileLocation.__new__(savelocation.FileLocation)
    location.persistent_mtime = 1
    location.persistent_data = "old data"
    return location


@pytest.mark.parametrize("consume", [False, True])
def test_load_waits_for_scan_publication(bare_location, consume):
    """
    load_persistent waits for disk_lock, so it returns the data the scan thread publishes rather than
    the stale data visible before.

    The test holds disk_lock as the scan thread does while it updates the mtime and data, and checks
    that the loader has started but has not finished within 20 ms. With consume=True the loaded data is
    also cleared from the location; otherwise it stays.
    """

    location = bare_location

    started = threading.Event()
    finished = threading.Event()
    results = []

    def load():
        started.set()
        try:
            results.extend(location.load_persistent(consume=consume))
        finally:
            finished.set()

    worker = threading.Thread(target=load)
    try:
        with savelocation.disk_lock:
            worker.start()
            assert started.wait(2)
            assert not finished.wait(0.02)
            location.persistent_mtime = 2
            location.persistent_data = "new data"
    finally:
        worker.join(2)

    assert not worker.is_alive()
    assert results == [(2, "new data")]
    assert location.persistent_data == (None if consume else "new data")


def test_consume_is_once_and_lock_is_reentrant(bare_location):
    """
    Data loaded with consume=True is returned only once, and load_persistent works while the caller
    already holds disk_lock.

    disk_lock must be reentrant, or the nested acquisition inside load_persistent would deadlock. The
    mtime is left alone when the data is consumed.
    """

    location = bare_location

    with savelocation.disk_lock:
        assert location.load_persistent() == [(1, "old data")]
        assert location.load_persistent(consume=True) == [(1, "old data")]
        assert location.load_persistent(consume=True) == []

    assert location.persistent_mtime == 1


################################################################################
# Background worker for persistent writes
################################################################################

# Each test runs against a real worker thread, so ordering and blocking are checked with events
# rather than sleeps. Module state is patched per test so the worker is the only scan thread.


@pytest.fixture
def scan_state(mocker):
    """Reset the scan-thread globals and stub the location scan so each test starts clean."""
    mocker.patch.object(savelocation, "scan_thread", None)
    mocker.patch.object(savelocation, "quit_scan_thread", False)
    mocker.patch.object(savelocation, "persistent_writes", deque())
    mocker.patch.object(renpy, "emscripten", False)
    mocker.patch.object(renpy.loadsave, "location", SimpleNamespace(scan=lambda: None))


@pytest.fixture
def start_worker(request, scan_state):
    """Return a function that starts the scan worker and quits it at teardown."""

    def start():
        """Start ``run_scan_thread`` on a new thread and register it as the active scan thread."""
        worker = threading.Thread(target=savelocation.run_scan_thread)
        savelocation.scan_thread = worker
        worker.start()
        return worker

    request.addfinalizer(savelocation.quit)
    return start


def make_file_location():
    """Return a FileLocation without running its constructor, so tests can stub ``_save_persistent``."""
    return savelocation.FileLocation.__new__(savelocation.FileLocation)


def test_file_write_is_queued_and_sync_write_waits_in_order(start_worker):
    """A background write runs on the worker, a sync write queued behind it waits, and both run in order."""
    start_worker()
    location = make_file_location()
    started = threading.Event()
    release = threading.Event()
    finished = threading.Event()
    writes = []
    second_results = []

    def write(data):
        if data == b"first":
            started.set()
            assert release.wait(2)
        writes.append(data)
        return 10

    location._save_persistent = write
    first = location.save_persistent(b"first", background=True)
    assert isinstance(first, Future)
    assert started.wait(2)

    def save_second():
        try:
            second_results.append(location.save_persistent(b"second"))
        finally:
            finished.set()

    second = threading.Thread(target=save_second)
    second.start()
    try:
        assert not finished.wait(0.02)
        release.set()
        second.join(2)
        assert not second.is_alive()
        assert first.result(2) == 10
        assert second_results == [None]
        assert writes == [b"first", b"second"]
    finally:
        release.set()
        second.join(2)


def test_multi_location_preserves_reverse_order_and_single_job(start_worker):
    """A MultiLocation write runs each location in reverse order as one background job and returns its result."""
    start_worker()
    writes = []
    location = savelocation.MultiLocation()

    for index in (1, 2):
        file_location = make_file_location()
        file_location.active = True
        file_location.directory = str(index)
        file_location.persistent_mtime = index
        file_location._save_persistent = lambda data, index=index: writes.append((index, data)) or index
        location.add(file_location)

    future = location.save_persistent(b"data", background=True)
    assert isinstance(future, Future)
    assert future.result(2) == 2
    assert writes == [(2, b"data"), (1, b"data")]
    assert savelocation.pause_syncfs_count == 0


def test_quit_drains_queued_writes(start_worker):
    """Calling quit while a write is in progress waits for the queued writes to finish before returning."""
    start_worker()
    location = make_file_location()
    started = threading.Event()
    release = threading.Event()
    writes = []

    def write(data):
        if data == b"first":
            started.set()
            assert release.wait(2)
        writes.append(data)

    location._save_persistent = write
    first = location.save_persistent(b"first", background=True)
    assert started.wait(2)
    second = location.save_persistent(b"second", background=True)
    quitter = threading.Thread(target=savelocation.quit)
    quitter.start()
    try:
        assert quitter.is_alive()
    finally:
        release.set()
        quitter.join(2)

    assert not quitter.is_alive()
    assert writes == [b"first", b"second"]
    assert first.result(2) is None
    assert second.result(2) is None


def test_reinit_drains_old_worker_before_replacing_it(start_worker, mocker):
    """Calling init while a write is pending drains the old worker before a new scan thread replaces it."""
    start_worker()
    old_worker = savelocation.scan_thread
    location = make_file_location()
    started = threading.Event()
    release = threading.Event()

    def write(data):
        started.set()
        assert release.wait(2)

    location._save_persistent = write
    pending = location.save_persistent(b"data", background=True)
    assert started.wait(2)
    fake_location = SimpleNamespace(directory="save-dir", active=True, scan=lambda: None)

    mocker.patch.object(renpy.loadsave, "location", None)
    mocker.patch.object(renpy.config, "savedir", "save-dir")
    mocker.patch.object(renpy.config, "extra_savedirs", [])
    mocker.patch.object(renpy, "mobile", True)
    mocker.patch.object(savelocation, "FileLocation", return_value=fake_location)

    initializer = threading.Thread(target=savelocation.init)
    initializer.start()
    try:
        assert initializer.is_alive()
    finally:
        release.set()
        initializer.join(2)

    assert not initializer.is_alive()
    assert pending.result(2) is None
    assert not old_worker.is_alive()
    assert savelocation.scan_thread is not old_worker
    assert savelocation.scan_thread.is_alive()


def test_late_failure_is_logged_and_sync_failure_propagates(start_worker, mocker):
    """A failing background write is logged and raised from its future; a later sync failure still raises."""
    start_worker()
    location = make_file_location()
    location._save_persistent = lambda data: (_ for _ in ()).throw(OSError("write failed"))
    logged = threading.Event()

    log_write = mocker.patch.object(renpy.display.log, "write")
    log_exception = mocker.patch.object(renpy.display.log, "exception", side_effect=lambda: logged.set())

    future = location.save_persistent(b"data", background=True)
    with pytest.raises(OSError, match="write failed"):
        future.result(2)
    assert logged.wait(2)

    with pytest.raises(OSError, match="write failed"):
        location.save_persistent(b"data")

    log_write.assert_called_once_with("Writing persistent.")
    log_exception.assert_called_once()

    location._save_persistent = lambda data: 10
    assert location.save_persistent(b"later") is None
    assert savelocation.scan_thread.is_alive()


def test_fallback_without_worker_or_on_emscripten(start_worker, mocker):
    """Background writes fall back to running inline when no worker is running or when on emscripten."""
    location = make_file_location()
    writes = []
    location._save_persistent = lambda data: writes.append(data)

    assert location.save_persistent(b"no-worker", background=True) is None
    start_worker()
    mocker.patch.object(renpy, "emscripten", True)
    assert location.save_persistent(b"web", background=True) is None

    assert writes == [b"no-worker", b"web"]


def test_real_file_write_and_failed_write_balance_syncfs(scan_state, mocker):
    """A real file write leaves the saved bytes and mtime in place; a failed rename propagates without leaking syncfs pauses.

    Directory and file exposure are patched out, since they touch the real filesystem outside the temp directory.
    """
    with tempfile.TemporaryDirectory(dir=os.getcwd()) as directory:
        mocker.patch.object(renpy.util, "expose_directory")
        mocker.patch.object(renpy.util, "expose_file")
        mocker.patch.object(savelocation, "syncfs")

        location = savelocation.FileLocation(directory)
        assert location.save_persistent(b"data") is None

        with open(location.persistent, "rb") as saved:
            assert saved.read() == b"data"
        assert location.persistent_mtime == os.path.getmtime(location.persistent)

        mocker.patch.object(savelocation, "safe_rename", side_effect=OSError("rename failed"))
        with pytest.raises(OSError, match="rename failed"):
            location.save_persistent(b"new data")

        assert savelocation.pause_syncfs_count == 0
