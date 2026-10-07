import unittest
from unittest.mock import patch

import renpy
from unittests.renpy_test_support import initialize_renpy

initialize_renpy()

from renpy.display.layout import Null
from renpy.display.particle import SnowBlossom, SnowBlossomFactory


def midpoint(a, b):
    return (a + b) / 2


class TestSnowBlossom(unittest.TestCase):
    def setUp(self):
        self.image = Null()

    def blossom(self, **kwargs):
        return SnowBlossom(
            self.image, count=4, xspeed=0, yspeed=100, distribution=midpoint, **kwargs
        )

    def assert_filled(self, blossom, st):
        self.assertEqual(len(blossom.particles), 4)
        for sprite, particle in blossom.particles:
            self.assertEqual(particle.start, st)
            self.assertEqual(sprite.y, renpy.config.screen_height // 2)

    def test_fast_initializes_at_nonzero_time(self):
        for animation in (False, True):
            with self.subTest(animation=animation):
                blossom = self.blossom(fast=True, animation=animation)
                blossom.update_callback(5.0)
                self.assert_filled(blossom, 5.0)

    def test_fast_initializes_each_duplicate(self):
        original = self.blossom(fast=True, animation=True)
        first = original._duplicate(None)
        first.update_callback(0.0)
        self.assert_filled(first, 0.0)

        second = original._duplicate(None)
        second.update_callback(5.0)
        self.assert_filled(second, 5.0)
        self.assert_filled(first, 0.0)

    def test_fast_initializes_after_load(self):
        blossom = self.blossom(fast=True, animation=True)
        blossom.update_callback(0.0)
        blossom.after_setstate()
        blossom.update_callback(5.0)
        self.assert_filled(blossom, 5.0)
        self.assertEqual(len(blossom.sm.children), 4)

    def test_fast_initializes_when_time_resets(self):
        blossom = self.blossom(fast=True)
        blossom.update_callback(5.0)
        blossom.update_callback(0.0)
        self.assert_filled(blossom, 0.0)
        self.assertEqual(len(blossom.sm.children), 4)

    def test_fast_replacements_still_start_at_edge(self):
        blossom = self.blossom(fast=True)
        blossom.update_callback(0.0)
        blossom.update_callback(100.0)
        self.assertEqual(blossom.particles, [])

        blossom.update_callback(101.0)
        self.assertEqual(len(blossom.particles), 1)
        sprite, particle = blossom.particles[0]
        self.assertEqual(particle.start, 101.0)
        self.assertEqual(sprite.y, -50)

    def test_nonfast_preserves_gradual_start(self):
        with patch("renpy.display.particle.random.uniform", side_effect=midpoint):
            blossom = self.blossom(fast=False, start=10)

        blossom.update_callback(0.0)
        self.assertEqual(len(blossom.particles), 1)
        self.assertEqual(blossom.particles[0][0].y, -50)
        blossom.update_callback(1.0)
        self.assertEqual(len(blossom.particles), 1)
        blossom.update_callback(5.0)
        self.assertEqual(len(blossom.particles), 2)

    def test_factory_preserves_zero_time_initialization(self):
        factory = SnowBlossomFactory(self.image, 4, 0, 100, 50, 0, True, distribution=midpoint)
        self.assertEqual(len(factory.create([], 0.0)), 4)
