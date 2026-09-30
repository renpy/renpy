import gc
import io
import unittest
import warnings
import weakref

from renpy import pygame


class TestSurfaceDeallocation(unittest.TestCase):
    def setUp(self):
        pygame.surface._init_surface_deallocation()
        self.addCleanup(pygame.surface._init_surface_deallocation)
        self.addCleanup(pygame.surface._quit_surface_deallocation)

    def test_owned_surface_accounting_and_weakref_release(self):
        gc.collect()
        original_size = pygame.surface.total_size
        surface = pygame.Surface((32, 64))
        reference = weakref.ref(surface)
        self.assertEqual(pygame.surface.total_size, original_size + surface.__sizeof__())
        del surface
        self.assertIsNone(reference())
        self.assertEqual(pygame.surface.total_size, original_size)
        pygame.surface._quit_surface_deallocation()

    def test_nested_subsurfaces_retain_pixels_and_release_parent(self):
        original_size = pygame.surface.total_size
        surface = pygame.Surface((32, 32))
        surface.fill((12, 34, 56, 255))
        reference = weakref.ref(surface)
        child = surface.subsurface((1, 1, 16, 16))
        nested = child.subsurface((1, 1, 8, 8))
        del surface, child
        self.assertIsNotNone(reference())
        self.assertEqual(tuple(nested.get_at((0, 0))), (12, 34, 56, 255))
        del nested
        self.assertIsNone(reference())
        self.assertEqual(pygame.surface.total_size, original_size)
        pygame.surface._quit_surface_deallocation()

    def test_repeated_shutdown_and_late_surface_release(self):
        original_size = pygame.surface.total_size
        for _ in range(10):
            pygame.surface._init_surface_deallocation()
            surface = pygame.Surface((32, 32))
            child = surface.subsurface((0, 0, 16, 16))
            pygame.surface._quit_surface_deallocation()
            pygame.surface._quit_surface_deallocation()
            del child, surface
        self.assertEqual(pygame.surface.total_size, original_size)

    def test_subsurface_bursts_and_uninitialized_wrapper(self):
        original_size = pygame.surface.total_size
        for _ in range(1000):
            surface = pygame.Surface((32, 32))
            child = surface.subsurface((0, 0, 16, 16))
            del child, surface
        empty = pygame.Surface(())
        del empty
        pygame.surface._quit_surface_deallocation()
        self.assertEqual(pygame.surface.total_size, original_size)

    def test_invalid_construction_does_not_leak_or_warn(self):
        original_size = pygame.surface.total_size
        with warnings.catch_warnings(record=True) as messages:
            warnings.simplefilter("always")
            with self.assertRaises(AssertionError):
                pygame.Surface((-1, 32))
        self.assertEqual(messages, [])
        self.assertEqual(pygame.surface.total_size, original_size)

    def test_surface_factories_preserve_pixels_and_accounting(self):
        original_size = pygame.surface.total_size
        surface = pygame.Surface((4, 4))
        surface.fill((12, 34, 56, 255))
        data = io.BytesIO()
        pygame.image.save(surface, data, namehint=".png")
        data.seek(0)
        copies = [
            surface.convert(),
            surface.convert_alpha(),
            surface.copy(),
            pygame.transform.rotozoom(surface, 0.0, 1.0),
            pygame.transform.smoothscale(surface, (8, 8)),
            pygame.image.load(data, namehint=".png"),
        ]
        for copy in copies:
            self.assertEqual(tuple(copy.get_at((0, 0))), (12, 34, 56, 255))
        self.assertEqual([copy.get_size() for copy in copies], [(4, 4)] * 4 + [(8, 8), (4, 4)])
        del copy, copies, surface
        pygame.surface._quit_surface_deallocation()
        self.assertEqual(pygame.surface.total_size, original_size)


if __name__ == "__main__":
    unittest.main()
