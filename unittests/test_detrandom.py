import unittest
from types import SimpleNamespace
from unittest.mock import patch

import renpy
from unittests.renpy_test_support import initialize_renpy

initialize_renpy()

from renpy.revertable import DetRandom


class TestDetRandom(unittest.TestCase):
    def setUp(self):
        self.recorded = []
        self.context = SimpleNamespace(force_checkpoint=False)

        for name, value in [
            ("log", SimpleNamespace(current=SimpleNamespace(random=self.recorded))),
            ("context", lambda: self.context),
        ]:
            p = patch.object(renpy.game, name, value)
            p.start()
            self.addCleanup(p.stop)

        self.rng = DetRandom()
        self.rng.seed(12345)

    def test_existing_seeded_sequences_are_unchanged(self):
        self.assertEqual(
            [self.rng.randint(1, 100) for _ in range(10)],
            [85, 42, 32, 31, 69, 29, 14, 99, 99, 62],
        )
        self.assertEqual(
            [self.rng.choice("abcdefghij") for _ in range(10)],
            list("giahdjfchd"),
        )
        self.assertEqual(
            [self.rng.randrange(3, 100, 7) for _ in range(10)],
            [3, 66, 52, 80, 38, 31, 10, 3, 52, 10],
        )

    def test_getrandbits_records_and_replays(self):
        widths = (1, 31, 32, 33, 64, 127)
        values = [self.rng.getrandbits(k) for k in widths]
        recorded = self.recorded[:]

        self.assertEqual(len(recorded), sum((k + 31) // 32 for k in widths))
        self.assertTrue(self.context.force_checkpoint)

        for k, value in zip(widths, values):
            self.assertGreaterEqual(value, 0)
            self.assertLess(value, 1 << k)

        self.rng.pushback(recorded)
        self.recorded.clear()
        self.assertEqual([self.rng.getrandbits(k) for k in widths], values)
        self.assertEqual(self.recorded, recorded)
        self.assertEqual(self.rng.stack, [])

    def test_randbytes_records_and_replays(self):
        lengths = (0, 1, 8, 17)
        values = [self.rng.randbytes(n) for n in lengths]
        recorded = self.recorded[:]

        self.assertEqual([len(value) for value in values], list(lengths))
        self.assertEqual(len(recorded), sum((n + 3) // 4 for n in lengths))

        self.rng.pushback(recorded)
        self.recorded.clear()
        self.assertEqual([self.rng.randbytes(n) for n in lengths], values)
        self.assertEqual(self.recorded, recorded)

    def test_zero_and_invalid_widths_do_not_consume_randomness(self):
        self.assertEqual(self.rng.getrandbits(0), 0)

        for k in (-1, -32):
            with self.assertRaises(ValueError):
                self.rng.getrandbits(k)

        with self.assertRaises(TypeError):
            self.rng.getrandbits(1.5)

        self.assertEqual(self.recorded, [])
        self.assertFalse(self.context.force_checkpoint)
