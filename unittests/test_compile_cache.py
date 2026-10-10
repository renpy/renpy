import io
import tempfile
import unittest
import zlib
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import renpy
from unittests.renpy_test_support import initialize_renpy

initialize_renpy()

from renpy import python, substitutions
from renpy.compat.pickle import dumps


class TestCompileCache(unittest.TestCase):
    def setUp(self):
        self.cache = python.CompileCache()
        p = patch.object(python, "compile_cache", self.cache)
        p.start()
        self.addCleanup(p.stop)

    def test_interpolation_distinguishes_sources_with_same_hash(self):
        self.assertEqual(python.hash32("40895872"), 3253015106)
        self.assertEqual(python.hash32("485050582"), 3253015106)

        with patch.object(renpy.config, "interpolate_exprs", True):
            self.assertEqual(substitutions.interpolate("[40895872] [485050582]", {}), "40895872 485050582")

        self.cache.reload()
        self.assertEqual(python.py_eval("485050582", {}, {}), 485050582)
        self.assertEqual(python.py_eval("40895872", {}, {}), 40895872)

    def test_bytecode_round_trip_preserves_colliding_sources(self):
        sources = ("result = 40895872", "result = 485050582")
        for source in sources:
            python.py_compile(source, "exec", hashcode=3253015106)

        with (
            tempfile.TemporaryDirectory() as directory,
            patch.object(renpy, "macapp", False),
            patch.object(renpy.game, "args", SimpleNamespace(compile_python=False)),
            patch.object(renpy.loader, "get_path", side_effect=lambda name: str(Path(directory) / Path(name).name)),
        ):
            self.cache.save()
            data = (Path(directory) / Path(python.CompileCache.BYTECODE_FILE).name).read_bytes()
            loaded = python.CompileCache()
            with patch.object(renpy.loader, "load", return_value=io.BytesIO(data)):
                loaded.load()

        self.assertEqual(len(loaded.old_bytecode_cache), 2)
        with patch.object(python, "compile_cache", loaded):
            for source, expected in zip(sources, (40895872, 485050582)):
                namespace = {}
                exec(python.py_compile(source, "exec", hashcode=3253015106), namespace)
                self.assertEqual(namespace["result"], expected)

    def test_old_bytecode_version_is_discarded(self):
        key = (3253015106, 1, "<none>", "eval", python.CompileCache.MAGIC_NUMBER, 0, 0)
        data = zlib.compress(dumps((1, {key: b"stale bytecode"})))
        with (
            patch.object(renpy.game, "args", SimpleNamespace(compile_python=False)),
            patch.object(renpy.loader, "load", return_value=io.BytesIO(data)),
        ):
            self.cache.load()

        self.assertEqual(self.cache.old_bytecode_cache, {})
