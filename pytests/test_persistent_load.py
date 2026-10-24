import threading
import unittest

from unittests.renpy_test_support import initialize_renpy

initialize_renpy()

from renpy import savelocation


class TestPersistentLoad(unittest.TestCase):
    def setUp(self):
        self.location = savelocation.FileLocation.__new__(savelocation.FileLocation)
        self.location.persistent_mtime = 1
        self.location.persistent_data = "old data"

    def test_load_waits_for_scan_publication(self):
        for consume in (False, True):
            with self.subTest(consume=consume):
                self.location.persistent_mtime = 1
                self.location.persistent_data = "old data"
                started = threading.Event()
                finished = threading.Event()
                results = []

                def load(started=started, results=results, consume=consume, finished=finished):
                    started.set()
                    try:
                        results.extend(self.location.load_persistent(consume=consume))
                    finally:
                        finished.set()

                worker = threading.Thread(target=load)
                try:
                    with savelocation.disk_lock:
                        worker.start()
                        self.assertTrue(started.wait(2))
                        self.assertFalse(finished.wait(0.02))
                        self.location.persistent_mtime = 2
                        self.location.persistent_data = "new data"
                finally:
                    worker.join(2)

                self.assertFalse(worker.is_alive())
                self.assertEqual(results, [(2, "new data")])
                self.assertEqual(self.location.persistent_data, None if consume else "new data")

    def test_consume_is_once_and_lock_is_reentrant(self):
        with savelocation.disk_lock:
            self.assertEqual(self.location.load_persistent(), [(1, "old data")])
            self.assertEqual(self.location.load_persistent(consume=True), [(1, "old data")])
            self.assertEqual(self.location.load_persistent(consume=True), [])

        self.assertEqual(self.location.persistent_mtime, 1)
