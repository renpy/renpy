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


def test_get_buffer_returns_pixel_bytes():
    """
    get_buffer gives access to the surface's pixels, with a pixel's channels at its offset.

    The channels are compared sorted, as their order depends on the surface's pixel format.
    """

    surface = pygame.Surface((2, 2), pygame.SRCALPHA, 32)
    surface.fill((0, 0, 0, 0))
    surface.set_at((1, 0), (10, 20, 30, 40))
    buffer = surface.get_buffer()
    assert len(buffer) == surface.get_pitch() + 8
    assert buffer[:4] == bytes(4)
    assert sorted(buffer[4:8]) == [10, 20, 30, 40]


def test_get_buffer_stays_within_subsurface_parent():
    """
    A subsurface's buffer ends with its last pixel.

    The subsurface is at the parent's bottom right corner, so a buffer of height * pitch bytes would
    read past the end of the parent's pixels.
    """

    surface = pygame.Surface((4, 4), pygame.SRCALPHA, 32)
    surface.fill((0, 0, 0, 0))
    child = surface.subsurface((2, 2, 2, 2))
    child.set_at((1, 1), (10, 20, 30, 40))
    buffer = child.get_buffer()
    assert len(buffer) == child.get_pitch() + 8
    assert sorted(buffer[-4:]) == [10, 20, 30, 40]


@pytest.mark.parametrize("subsurface", [False, True])
def test_get_buffer_writes_change_pixels(subsurface):
    """
    Writing to the buffer changes the surface directly, including through a subsurface, where the write
    also reaches the parent.

    The bytes come from another surface of the same format, so the test doesn't depend on channel order.
    """

    source = pygame.Surface((1, 1), pygame.SRCALPHA, 32)
    source.fill((10, 20, 30, 40))
    pixel = bytes(source.get_buffer())

    parent = pygame.Surface((2, 2), pygame.SRCALPHA, 32)
    parent.fill((0, 0, 0, 0))
    surface = parent.subsurface((1, 1, 1, 1)) if subsurface else parent
    surface.get_buffer()[:4] = pixel

    assert tuple(parent.get_at((1, 1) if subsurface else (0, 0))) == (10, 20, 30, 40)


def test_get_buffer_keeps_surface_alive():
    """
    The buffer points at the surface's own pixels, so it must keep the surface alive after every other
    reference is gone, and must release it afterwards.
    """

    gc.collect()
    original_size = pygame.surface.total_size
    surface = pygame.Surface((4, 4), pygame.SRCALPHA, 32)
    surface.fill((1, 1, 1, 1))
    reference = weakref.ref(surface)
    buffer = surface.get_buffer()

    del surface
    gc.collect()
    assert reference() is not None
    assert set(buffer) == {1}

    buffer.release()
    del buffer
    assert reference() is None
    pygame.surface._quit_surface_deallocation()
    assert pygame.surface.total_size == original_size


@pytest.mark.parametrize("size", [(), (0, 0)])
def test_get_buffer_of_empty_surface_is_empty(size):
    """
    A surface with no pixels gives an empty buffer. An empty size builds a surface with no SDL surface
    at all, which must not be dereferenced.
    """

    assert len(pygame.Surface(size).get_buffer()) == 0
