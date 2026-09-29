import os
import tempfile
import threading
import unittest
from collections import deque
from concurrent.futures import Future
from types import SimpleNamespace
from unittest.mock import patch

import renpy

renpy.import_all()

from renpy import savelocation


class TestBackgroundPersistentWrites(unittest.TestCase):
    def setUp(self):
        for name, value in [
            ("scan_thread", None),
            ("quit_scan_thread", False),
            ("persistent_writes", deque()),
        ]:
            p = patch.object(savelocation, name, value)
            p.start()
            self.addCleanup(p.stop)

        p = patch.object(renpy, "emscripten", False)
        p.start()
        self.addCleanup(p.stop)

        p = patch.object(renpy.loadsave, "location", SimpleNamespace(scan=lambda: None))
        p.start()
        self.addCleanup(p.stop)

    def start_worker(self):
        worker = threading.Thread(target=savelocation.run_scan_thread)
        savelocation.scan_thread = worker
        worker.start()
        self.addCleanup(savelocation.quit)

    def test_file_write_is_queued_and_sync_write_waits_in_order(self):
        self.start_worker()
        location = savelocation.FileLocation.__new__(savelocation.FileLocation)
        started = threading.Event()
        release = threading.Event()
        finished = threading.Event()
        writes = []
        second_results = []

        def write(data):
            if data == b"first":
                started.set()
                self.assertTrue(release.wait(2))
            writes.append(data)
            return 10

        location._save_persistent = write
        first = location.save_persistent(b"first", background=True)
        self.assertIsInstance(first, Future)
        self.assertTrue(started.wait(2))

        def save_second():
            try:
                second_results.append(location.save_persistent(b"second"))
            finally:
                finished.set()

        second = threading.Thread(target=save_second)
        second.start()
        try:
            self.assertFalse(finished.wait(0.02))
            release.set()
            second.join(2)
            self.assertFalse(second.is_alive())
            self.assertEqual(first.result(2), 10)
            self.assertEqual(second_results, [None])
            self.assertEqual(writes, [b"first", b"second"])
        finally:
            release.set()
            second.join(2)

    def test_multi_location_preserves_reverse_order_and_single_job(self):
        self.start_worker()
        writes = []
        location = savelocation.MultiLocation()

        for index in (1, 2):
            file_location = savelocation.FileLocation.__new__(savelocation.FileLocation)
            file_location.active = True
            file_location.directory = str(index)
            file_location.persistent_mtime = index
            file_location._save_persistent = lambda data, index=index: writes.append((index, data)) or index
            location.add(file_location)

        future = location.save_persistent(b"data", background=True)
        self.assertIsInstance(future, Future)
        self.assertEqual(future.result(2), 2)
        self.assertEqual(writes, [(2, b"data"), (1, b"data")])
        self.assertEqual(savelocation.pause_syncfs_count, 0)

    def test_quit_drains_queued_writes(self):
        self.start_worker()
        location = savelocation.FileLocation.__new__(savelocation.FileLocation)
        started = threading.Event()
        release = threading.Event()
        writes = []

        def write(data):
            if data == b"first":
                started.set()
                self.assertTrue(release.wait(2))
            writes.append(data)

        location._save_persistent = write
        first = location.save_persistent(b"first", background=True)
        self.assertTrue(started.wait(2))
        second = location.save_persistent(b"second", background=True)
        quitter = threading.Thread(target=savelocation.quit)
        quitter.start()
        try:
            self.assertTrue(quitter.is_alive())
        finally:
            release.set()
            quitter.join(2)

        self.assertFalse(quitter.is_alive())
        self.assertEqual(writes, [b"first", b"second"])
        self.assertIsNone(first.result(2))
        self.assertIsNone(second.result(2))

    def test_reinit_drains_old_worker_before_replacing_it(self):
        self.start_worker()
        old_worker = savelocation.scan_thread
        location = savelocation.FileLocation.__new__(savelocation.FileLocation)
        started = threading.Event()
        release = threading.Event()

        def write(data):
            started.set()
            self.assertTrue(release.wait(2))

        location._save_persistent = write
        pending = location.save_persistent(b"data", background=True)
        self.assertTrue(started.wait(2))
        fake_location = SimpleNamespace(directory="save-dir", active=True, scan=lambda: None)

        with (
            patch.object(renpy.loadsave, "location", None),
            patch.object(renpy.config, "savedir", "save-dir"),
            patch.object(renpy.config, "extra_savedirs", []),
            patch.object(renpy, "mobile", True),
            patch.object(savelocation, "FileLocation", return_value=fake_location),
        ):
            initializer = threading.Thread(target=savelocation.init)
            initializer.start()
            try:
                self.assertTrue(initializer.is_alive())
            finally:
                release.set()
                initializer.join(2)

            self.assertFalse(initializer.is_alive())
            self.assertIsNone(pending.result(2))
            self.assertFalse(old_worker.is_alive())
            self.assertIsNot(savelocation.scan_thread, old_worker)
            self.assertTrue(savelocation.scan_thread.is_alive())

    def test_late_failure_is_logged_and_sync_failure_propagates(self):
        self.start_worker()
        location = savelocation.FileLocation.__new__(savelocation.FileLocation)
        location._save_persistent = lambda data: (_ for _ in ()).throw(OSError("write failed"))
        logged = threading.Event()

        with (
            patch.object(renpy.display.log, "write") as log_write,
            patch.object(renpy.display.log, "exception", side_effect=lambda: logged.set()) as log_exception,
        ):
            future = location.save_persistent(b"data", background=True)
            with self.assertRaisesRegex(OSError, "write failed"):
                future.result(2)
            self.assertTrue(logged.wait(2))

            with self.assertRaisesRegex(OSError, "write failed"):
                location.save_persistent(b"data")

            log_write.assert_called_once_with("Writing persistent.")
            log_exception.assert_called_once()

        location._save_persistent = lambda data: 10
        self.assertIsNone(location.save_persistent(b"later"))
        self.assertTrue(savelocation.scan_thread.is_alive())

    def test_fallback_without_worker_or_on_emscripten(self):
        location = savelocation.FileLocation.__new__(savelocation.FileLocation)
        writes = []
        location._save_persistent = lambda data: writes.append(data)

        self.assertIsNone(location.save_persistent(b"no-worker", background=True))
        self.start_worker()
        with patch.object(renpy, "emscripten", True):
            self.assertIsNone(location.save_persistent(b"web", background=True))

        self.assertEqual(writes, [b"no-worker", b"web"])

    def test_real_file_write_and_failed_write_balance_syncfs(self):
        with (
            tempfile.TemporaryDirectory(dir=os.getcwd()) as directory,
            patch.object(renpy.util, "expose_directory"),
            patch.object(renpy.util, "expose_file"),
            patch.object(savelocation, "syncfs"),
        ):
            location = savelocation.FileLocation(directory)
            self.assertIsNone(location.save_persistent(b"data"))

            with open(location.persistent, "rb") as saved:
                self.assertEqual(saved.read(), b"data")
            self.assertEqual(location.persistent_mtime, os.path.getmtime(location.persistent))

            with (
                patch.object(savelocation, "safe_rename", side_effect=OSError("rename failed")),
                self.assertRaisesRegex(OSError, "rename failed"),
            ):
                location.save_persistent(b"new data")

            self.assertEqual(savelocation.pause_syncfs_count, 0)
