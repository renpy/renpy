import pytest

from renpy import pygame
from renpy.pygame import transform

pytestmark = pytest.mark.usefixtures("surface_deallocation")


def make_pixel(color):
    """
    Returns a 1x1 surface filled with `color`.
    """

    surface = pygame.Surface((1, 1))
    surface.set_at((0, 0), color)
    return surface


@pytest.mark.parametrize(
    ("color_a", "color_b", "premultiplied", "expected"),
    [
        ((10, 20, 30, 255), (10, 20, 30, 255), True, 0.0),
        ((10, 20, 30, 255), (10, 20, 40, 128), True, 127.0),
        ((255, 0, 0, 64), (0, 0, 0, 64), True, 64.0),
        ((255, 0, 0, 64), (0, 0, 0, 64), False, 255.0),
        ((255, 255, 255, 0), (0, 0, 0, 0), True, 0.0),
        ((255, 255, 255, 0), (0, 0, 0, 0), False, 255.0),
        ((200, 0, 0, 3), (0, 0, 0, 3), True, 600 / 255),
    ],
)
def test_max_difference_compares_channels(color_a, color_b, premultiplied, expected):
    """
    _max_difference returns the largest difference in any channel, in units of 0-255.

    With premultiplied colors, a red difference of 255 at alpha 64 counts as 64, and fully transparent
    pixels compare equal whatever their stored colors. That is what lets Live2D tests ignore invisible
    color changes in nearly transparent pixels. The last case checks that the result isn't rounded to an
    integer, as tests compare it to small limits. Alpha differences count unscaled.
    """

    assert transform._max_difference(make_pixel(color_a), make_pixel(color_b), premultiplied) == pytest.approx(
        expected
    )


def test_max_difference_finds_one_pixel_in_a_large_surface():
    """
    A difference in a single pixel far from the origin is found, so every row and column is scanned
    rather than just the first row or the pitch being ignored.
    """

    a = pygame.Surface((257, 129))
    b = a.copy()
    b.set_at((256, 128), (0, 0, 0, 9))

    assert transform._max_difference(a, b) == 9.0
    assert transform._max_difference(b, a) == 9.0


def test_max_difference_rejects_different_sizes():
    """
    Surfaces of different sizes raise an error rather than reading past the end of the smaller one.
    """

    with pytest.raises(pygame.error):
        transform._max_difference(pygame.Surface((10, 10)), pygame.Surface((10, 11)))
