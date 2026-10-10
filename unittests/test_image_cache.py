import unittest
from unittest.mock import Mock, patch

import renpy
from unittests.renpy_test_support import initialize_renpy

initialize_renpy()

from renpy.display import im
from renpy.display.render import Render


class TestUncachedImages(unittest.TestCase):
    def setUp(self):
        renpy.pygame.surface._init_surface_deallocation()
        self.addCleanup(renpy.pygame.surface._quit_surface_deallocation)
        with patch.object(renpy, "emscripten", True):
            self.cache = im.Cache()
        self.draw = Mock()
        self.draw.ready_one_texture.return_value = False
        self.draw.load_texture.side_effect = lambda surface, **kwargs: surface
        patcher = patch.object(renpy.display, "draw", self.draw)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.addCleanup(self.draw.reset_mock)
        self.addCleanup(self.cache.cache.clear)

    def assert_uncached(self):
        self.assertEqual(self.cache.cache, {})
        self.assertEqual(self.cache.cache_size, 0)

    def test_plain_surface_reloads_without_caching(self):
        image = im.Null(cache=False)
        first = self.cache.get(image)
        second = self.cache.get(image)
        self.assertIsInstance(first, renpy.pygame.Surface)
        self.assertIsNot(first, second)
        self.draw.load_texture.assert_not_called()
        self.assert_uncached()

    def test_texture_and_image_render(self):
        image = im.Null(cache=False)
        texture = self.cache.get(image, texture=True)
        self.assertIs(texture, self.draw.load_texture.call_args.args[0])
        with patch.object(im, "cache", self.cache):
            render = image.render(100, 100, 0, 0)
        self.assertIsInstance(render, Render)
        self.assertEqual(render.get_size(), (1, 1))
        self.assertEqual(self.draw.load_texture.call_count, 2)
        self.assert_uncached()

    def test_bounds_oversampling_and_texture_properties_match_cached_images(self):
        surface = renpy.pygame.Surface((12, 8))
        surface.fill((0, 0, 0, 0))
        surface.fill((255, 255, 255, 255), (4, 2, 4, 4))
        with (
            patch.object(renpy.config, "optimize_texture_bounds", True),
            patch.object(renpy.config, "expand_texture_bounds", 0),
            patch.object(im.Null, "load", return_value=surface),
            patch.object(im.Null, "get_oversample", return_value=2),
            patch.object(im.Null, "pixel_perfect", True),
        ):
            renders = [
                self.cache.get(im.Null(cache=cache, mipmap=True), render=True)
                for cache in (False, True)
            ]
        self.assertEqual([r.get_size() for r in renders], [(6, 4), (6, 4)])
        self.assertEqual([r.children[0][1:3] for r in renders], [(2, 1), (2, 1)])
        self.assertEqual([r.children[0][0].get_size() for r in renders], [(4, 4), (4, 4)])
        self.assertEqual([r.properties for r in renders], [{"pixel_perfect": True}] * 2)
        self.assertEqual(len(self.cache.cache), 1)
        for call in self.draw.load_texture.call_args_list:
            self.assertEqual(call.kwargs, {"properties": {"mipmap": True}})

    def test_prediction_converts_texture_without_caching(self):
        self.assertIsNone(self.cache.get(im.Null(cache=False), predict=True, render=True))
        self.draw.load_texture.assert_called_once()
        self.draw.ready_one_texture.assert_not_called()
        self.assert_uncached()
