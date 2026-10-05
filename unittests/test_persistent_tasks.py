import unittest
from concurrent.futures import Future
from types import SimpleNamespace
from unittest.mock import patch

import renpy
from unittests.renpy_test_support import initialize_renpy

initialize_renpy()

from renpy import persistent
from renpy.display.core import Interface


class Location:
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


class TestPersistentTasks(unittest.TestCase):
    def setUp(self):
        self.location = Location()
        self.game_persistent = SimpleNamespace(_changed={}, value=1)

        for target, name, value in [
            (renpy.loadsave, "location", self.location),
            (renpy.game, "persistent", self.game_persistent),
            (renpy.config, "save_persistent", True),
            (persistent, "backup", {"value": 0}),
            (persistent, "persistent_mtime", 0),
            (persistent, "pending_save", False),
        ]:
            p = patch.object(target, name, value)
            p.start()
            self.addCleanup(p.stop)

        renpy.asynctask.reset()
        self.addCleanup(renpy.asynctask.reset)

    def test_save_yields_between_major_operations(self):
        events = []

        with (
            patch.object(persistent, "dumps", side_effect=lambda *a, **kw: events.append("dump") or b"data"),
            patch.object(persistent.zlib, "compress", side_effect=lambda *a: events.append("compress") or b"zip"),
            patch.object(renpy.savetoken, "sign_data", side_effect=lambda *a: events.append("sign") or "sig"),
            patch.object(
                self.location, "save_persistent", side_effect=lambda data, **kwargs: events.append(("write", data))
            ),
        ):
            task = persistent.save_task()
            for _ in range(3):
                self.assertIsNone(next(task))
                events.append("yield")
            with self.assertRaises(StopIteration):
                next(task)

        self.assertEqual(events, ["dump", "yield", "compress", "yield", "sign", "yield", ("write", b"zipsig")])
        self.assertFalse(persistent.pending_save)

    def test_sync_entry_points_and_restart(self):
        self.location.data = [(5, object())]

        with (
            patch.object(persistent, "merge") as merge,
            patch.object(persistent, "dumps", return_value=b"data"),
            patch.object(persistent.zlib, "compress", return_value=b"zip"),
            patch.object(renpy.savetoken, "sign_data", return_value="sig"),
            patch.object(renpy.exports, "restart_interaction") as restart,
        ):
            self.assertIsNone(persistent.check_update())
            merge.assert_called_once()
            restart.assert_called_once()
            self.assertEqual(persistent.persistent_mtime, 5)
            self.assertEqual(self.location.saved, [b"zipsig"])

            self.assertIsNone(persistent.update(True))
            self.assertIsNone(persistent.save())

        self.assertEqual(self.location.saved, [b"zipsig"] * 3)
        self.assertEqual(self.location.background_modes, [False] * 3)

    def test_task_save_queues_without_waiting_for_disk(self):
        future = Future()
        with (
            patch.object(persistent, "dumps", return_value=b"data"),
            patch.object(persistent.zlib, "compress", return_value=b"zip"),
            patch.object(renpy.savetoken, "sign_data", return_value="sig"),
            patch.object(self.location, "save_persistent", return_value=future) as save,
        ):
            renpy.asynctask.run_sync(persistent.save_task())

        save.assert_called_once_with(b"zipsig", background=True)
        self.assertFalse(future.done())
        self.assertFalse(persistent.pending_save)
        self.assertEqual(persistent.persistent_mtime, 0)

        future.set_result(9)
        self.assertEqual(persistent.persistent_mtime, 9)

    def test_late_background_failure_does_not_retry(self):
        future = Future()
        with (
            patch.object(persistent, "dumps", return_value=b"data"),
            patch.object(persistent.zlib, "compress", return_value=b"zip"),
            patch.object(renpy.savetoken, "sign_data", return_value="sig"),
            patch.object(self.location, "save_persistent", return_value=future),
        ):
            renpy.asynctask.run_sync(persistent.save_task())

        future.set_exception(OSError("disk error"))
        self.assertFalse(persistent.pending_save)
        self.assertEqual(persistent.persistent_mtime, 0)

    def test_completed_background_write_mtime_is_not_overwritten_by_update(self):
        persistent.backup["value"] = 1
        self.location.data = [(5, object())]
        write = Future()
        write.add_done_callback(persistent._background_save_completed)

        with patch.object(persistent, "merge", side_effect=lambda other: write.set_result(10)):
            renpy.asynctask.run_sync(persistent.update_task())

        self.assertEqual(persistent.persistent_mtime, 10)

    def test_unchanged_update_does_not_save(self):
        persistent.backup["value"] = 1

        with patch.object(persistent, "dumps") as dumps:
            self.assertIsNone(persistent.update())

        dumps.assert_not_called()
        self.assertFalse(persistent.pending_save)
        self.assertEqual(self.location.saved, [])

    def test_cancelled_update_retries_pending_save(self):
        with (
            patch.object(persistent, "dumps", return_value=b"data"),
            patch.object(persistent.zlib, "compress", return_value=b"zip"),
            patch.object(renpy.savetoken, "sign_data", return_value="sig"),
        ):
            task = renpy.asynctask.create_task(persistent.update_task())
            renpy.asynctask.run_for_ns(1)

            self.assertFalse(task.done())
            self.assertTrue(persistent.pending_save)
            self.assertEqual(persistent.backup["value"], 1)
            renpy.asynctask.reset()

            self.assertIsNone(persistent.check_update())
            self.assertEqual(self.location.saved, [b"zipsig"])
            self.assertFalse(persistent.pending_save)

    def test_cancelled_after_merge_does_not_drop_consumed_data(self):
        other = object()
        self.location.data = [(5, other)]

        with (
            patch.object(persistent, "merge") as merge,
            patch.object(persistent, "dumps", return_value=b"data"),
            patch.object(persistent.zlib, "compress", return_value=b"zip"),
            patch.object(renpy.savetoken, "sign_data", return_value="sig"),
        ):
            task = renpy.asynctask.create_task(persistent.update_task())
            renpy.asynctask.run_for_ns(1)
            renpy.asynctask.run_for_ns(1)

            self.assertFalse(task.done())
            merge.assert_called_once_with(other)
            self.assertEqual(self.location.data, [])
            self.assertEqual(persistent.persistent_mtime, 5)
            renpy.asynctask.reset()

            self.assertIsNone(persistent.check_update())
            self.assertEqual(self.location.saved, [b"zipsig"])
            merge.assert_called_once_with(other)

    def test_cancelled_save_retries_on_next_check(self):
        with (
            patch.object(persistent, "dumps", return_value=b"data"),
            patch.object(persistent.zlib, "compress", return_value=b"zip"),
            patch.object(renpy.savetoken, "sign_data", return_value="sig"),
        ):
            task = renpy.asynctask.create_task(persistent.save_task())
            renpy.asynctask.run_for_ns(1)

            self.assertFalse(task.done())
            self.assertTrue(persistent.pending_save)
            renpy.asynctask.reset()

            self.assertIsNone(persistent.check_update())
            self.assertEqual(self.location.saved, [b"zipsig"])
            self.assertFalse(persistent.pending_save)

    def test_interface_runs_platform_persistent_maintenance(self):
        for emscripten in (False, True):
            with self.subTest(emscripten=emscripten):
                interface = SimpleNamespace(did_autosave=True, did_persistent=False)

                def maintenance():
                    yield

                with (
                    patch.object(renpy, "emscripten", emscripten),
                    patch.object(persistent, "check_update_task", side_effect=maintenance) as check,
                    patch.object(persistent, "update_task", side_effect=maintenance) as update,
                ):
                    renpy.asynctask.run_sync(Interface.run_filesystem_task(interface))

                self.assertEqual(check.call_count, not emscripten)
                self.assertEqual(update.call_count, emscripten)
                self.assertTrue(interface.did_persistent)

    def test_interface_retries_after_cancellation(self):
        interface = SimpleNamespace(did_autosave=True, did_persistent=False)
        cleaned = []

        def maintenance():
            try:
                yield
            finally:
                cleaned.append(True)

        with (
            patch.object(renpy, "emscripten", False),
            patch.object(persistent, "check_update_task", side_effect=maintenance),
        ):
            task = Interface.run_filesystem_task(interface)
            self.assertIsNone(next(task))
            task.close()

        self.assertFalse(interface.did_persistent)
        self.assertEqual(cleaned, [True])
