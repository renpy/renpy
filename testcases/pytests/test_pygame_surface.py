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


# Blitting


BLIT_CASES = {
    "whole_source": ((20, 10), (5, 4), (2, 3), None, None, (2, 3, 5, 4)),
    "area_skips_first_row": ((304, 60), (304, 50), (0, 0), (0, 1, 304, 49), None, (0, 0, 304, 49)),
    "negative_area_offset": ((20, 10), (5, 4), (2, 3), (-2, -1, 5, 4), None, (4, 4, 3, 3)),
    "dest_off_top_left": ((20, 10), (5, 4), (-2, -1), None, None, (0, 0, 3, 3)),
    "dest_off_bottom_right": ((20, 10), (5, 4), (18, 8), None, None, (18, 8, 2, 2)),
    "clip_rect": ((20, 10), (5, 4), (2, 2), None, (3, 3, 4, 4), (3, 3, 4, 3)),
    "area_too_large_for_sdl": ((20, 10), (5, 4), (2, 3), (0, 0, 2**31 - 1, 4), None, (2, 3, 5, 4)),
    "area_end_overflows_int": ((20, 10), (5, 4), (0, 0), (1, 0, 2**31 - 1, 4), None, (0, 0, 4, 4)),
    "area_outside_source": ((20, 10), (5, 4), (2, 3), (10, 10, 5, 5), None, (2, 3, 0, 0)),
    "negative_area_outside_source": ((20, 10), (5, 4), (2, 3), (-10, 0, 5, 4), None, (12, 3, 0, 0)),
    "dest_beyond_top_left": ((20, 10), (5, 4), (-10, -10), None, None, (0, 0, 0, 0)),
    "dest_beyond_bottom_right": ((20, 10), (5, 4), (30, 20), None, None, (30, 20, 0, 0)),
    "dest_outside_clip_rect": ((20, 10), (5, 4), (-10, 1), None, (3, 3, 4, 4), (3, 3, 0, 0)),
}


@pytest.mark.parametrize("special_flags", [0, pygame.BLEND_RGBA_MAX], ids=["plain", "blend"])
@pytest.mark.parametrize(
    "dest_size, source_size, dest, area, clip, expected",
    list(BLIT_CASES.values()),
    ids=list(BLIT_CASES),
)
def test_blit_returns_drawn_rect(dest_size, source_size, dest, area, clip, expected, special_flags):
    """
    blit returns the rectangle of destination pixels it changed, taking the area, a negative area offset, the
    destination bounds, and the clip rectangle into account. Every pixel inside that rectangle, and none outside it,
    is drawn, each from the source pixel that the area and destination line up with it.

    The expected rectangles follow pygame-ce, including where nothing is drawn: the size is zero, and the position is
    the destination moved right and down by a negative area offset, then up to the clip rectangle's top-left corner if
    it was above or left of it.

    Each opaque source pixel stores its own x (modulo 256) in green and its y in blue. On a transparent black
    destination, both a plain blit and BLEND_RGBA_MAX copy the source pixel unchanged, so the pixel check is the same
    for both paths, and it catches a blit that copies the wrong part of the source into the right rectangle. SDL refuses
    to draw an area wide enough to overflow, and adding an area's offset to its size can overflow an int, so the cases
    with huge areas check that the drawn pixels still match the returned rectangle.
    """

    target = pygame.Surface(dest_size, pygame.SRCALPHA, 32)
    target.fill((0, 0, 0, 0))

    if clip is not None:
        target.set_clip(clip)

    source = pygame.Surface(source_size, pygame.SRCALPHA, 32)

    for sx in range(source_size[0]):
        for sy in range(source_size[1]):
            source.set_at((sx, sy), (255, sx % 256, sy, 255))

    rect = target.blit(source, dest, area, special_flags)
    assert tuple(rect) == expected

    # A blit is a translation: destination (px, py) is drawn from source (px + offset_x, py + offset_y).
    area_x, area_y = area[:2] if area is not None else (0, 0)
    offset_x = area_x - dest[0]
    offset_y = area_y - dest[1]

    x, y, w, h = expected
    width, height = dest_size

    drawn = {
        (px, py): tuple(target.get_at((px, py)))
        for px in range(width)
        for py in range(height)
        if target.get_at((px, py))[3]
    }

    assert drawn == {
        (px, py): (255, (px + offset_x) % 256, py + offset_y, 255)
        for px in range(x, x + w)
        for py in range(y, y + h)
    }
