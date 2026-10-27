"""Tests for queuing persistent writes onto the background save-location scan thread.

Each test runs against a real worker thread, so ordering and blocking are checked with events
rather than sleeps. Module state is patched per test so the worker is the only scan thread.
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


@pytest.fixture(autouse=True)
def scan_state(mocker):
    """Reset the scan-thread globals and stub the location scan so each test starts clean."""
    mocker.patch.object(savelocation, "scan_thread", None)
    mocker.patch.object(savelocation, "quit_scan_thread", False)
    mocker.patch.object(savelocation, "persistent_writes", deque())
    mocker.patch.object(renpy, "emscripten", False)
    mocker.patch.object(renpy.loadsave, "location", SimpleNamespace(scan=lambda: None))


@pytest.fixture
def start_worker(request):
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


def test_real_file_write_and_failed_write_balance_syncfs(mocker):
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
