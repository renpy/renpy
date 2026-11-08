import gc
import io
import warnings
import weakref

import pytest

from renpy import pygame

pytestmark = pytest.mark.usefixtures("surface_deallocation")


def test_owned_surface_accounting_and_weakref_release():
    """
    An owned surface adds its pixel size to total_size, and the accounting is reversed once the
    surface is garbage collected.

    The weakref confirms the surface itself is released, not just that the counter moved. gc.collect()
    runs first so that unrelated garbage from earlier tests does not change the baseline.
    """

    gc.collect()
    original_size = pygame.surface.total_size
    surface = pygame.Surface((32, 64))
    reference = weakref.ref(surface)
    assert pygame.surface.total_size == original_size + surface.__sizeof__()
    del surface
    assert reference() is None
    assert pygame.surface.total_size == original_size
    pygame.surface._quit_surface_deallocation()


def test_nested_subsurfaces_retain_pixels_and_release_parent():
    """
    A nested subsurface keeps its pixels readable after the parent and intermediate subsurface are
    deleted, and the parent is released only when the last view of it goes away.

    The subsurfaces keep their parent alive, so the weakref to the original surface stays live until
    `nested` is deleted. Reading a pixel through `nested` after the parent references are dropped checks
    that the shared pixel storage was not freed early.
    """

    original_size = pygame.surface.total_size
    surface = pygame.Surface((32, 32))
    surface.fill((12, 34, 56, 255))
    reference = weakref.ref(surface)
    child = surface.subsurface((1, 1, 16, 16))
    nested = child.subsurface((1, 1, 8, 8))
    del surface, child
    assert reference() is not None
    assert tuple(nested.get_at((0, 0))) == (12, 34, 56, 255)
    del nested
    assert reference() is None
    assert pygame.surface.total_size == original_size
    pygame.surface._quit_surface_deallocation()


def test_repeated_shutdown_and_late_surface_release():
    """
    Surfaces that outlive a shutdown of the deallocation tracker are still released cleanly, and
    repeated shutdowns and re-initializations do not corrupt total_size.

    Each iteration shuts the tracker down while the surface and subsurface are still alive, then
    releases them after the shutdown. Quitting twice in a row checks that the second call is harmless.
    """

    original_size = pygame.surface.total_size
    for _ in range(10):
        pygame.surface._init_surface_deallocation()
        surface = pygame.Surface((32, 32))
        child = surface.subsurface((0, 0, 16, 16))
        pygame.surface._quit_surface_deallocation()
        pygame.surface._quit_surface_deallocation()
        del child, surface
    assert pygame.surface.total_size == original_size


def test_cyclic_subsurface_release():
    """
    Cyclic garbage collection releases a parent and its subsurface without relying on the parent
    reference surviving until deallocation, and restores pixel-storage accounting.
    """

    class CyclicSurface(pygame.Surface):
        """Allows a parent to hold a reference back to its subsurface."""

    gc.collect()
    original_size = pygame.surface.total_size
    surface = CyclicSurface((32, 32))
    child = surface.subsurface((0, 0, 16, 16))
    surface.child = child
    parent_reference = weakref.ref(surface)
    child_reference = weakref.ref(child)
    assert child.__sizeof__() == 0
    assert pygame.surface.total_size == original_size + surface.__sizeof__()

    del child, surface
    gc.collect()
    pygame.surface._quit_surface_deallocation()

    assert parent_reference() is None
    assert child_reference() is None
    assert pygame.surface.total_size == original_size


def test_subsurface_bursts_and_uninitialized_wrapper():
    """
    Creating many surfaces and subsurfaces in a burst leaves total_size unchanged, and a zero-sized
    surface built without a size also leaves no accounting behind.

    Deallocation is queued, so the tracker is shut down at the end to flush anything still pending
    before total_size is compared.
    """

    original_size = pygame.surface.total_size
    for _ in range(1000):
        surface = pygame.Surface((32, 32))
        child = surface.subsurface((0, 0, 16, 16))
        del child, surface
    empty = pygame.Surface(())
    del empty
    pygame.surface._quit_surface_deallocation()
    assert pygame.surface.total_size == original_size


def test_invalid_construction_does_not_leak_or_warn():
    """
    A Surface with a negative width raises AssertionError without emitting a warning or changing
    total_size.

    Deallocation must be safe for a surface that never got a pixel buffer, so the warnings are
    recorded and must stay empty.
    """

    original_size = pygame.surface.total_size
    with warnings.catch_warnings(record=True) as messages:
        warnings.simplefilter("always")
        with pytest.raises(AssertionError):
            pygame.Surface((-1, 32))
    assert messages == []
    assert pygame.surface.total_size == original_size


def test_surface_factories_preserve_pixels_and_accounting():
    """
    Each surface-producing factory (convert, convert_alpha, copy, rotozoom, smoothscale, and image
    load) returns a surface with the expected pixel color and size, and all of them are released so
    total_size returns to its original value.

    The PNG round trip through an in-memory buffer covers image.load. The loop variable `copy` is
    deleted explicitly so no reference to the last copy keeps its pixels alive.
    """

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
        assert tuple(copy.get_at((0, 0))) == (12, 34, 56, 255)
    assert [copy.get_size() for copy in copies] == [(4, 4)] * 4 + [(8, 8), (4, 4)]
    del copy, copies, surface
    pygame.surface._quit_surface_deallocation()
    assert pygame.surface.total_size == original_size
