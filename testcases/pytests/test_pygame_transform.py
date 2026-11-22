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


def single_bucket(index, count=1):
    """
    Returns the histogram expected when `count` pixels all differ by `index`.
    """

    rv = [0] * 256
    rv[index] = count
    return rv


@pytest.mark.parametrize(
    ("color_a", "color_b", "premultiplied", "expected"),
    [
        ((10, 20, 30, 255), (10, 20, 30, 255), True, 0),
        ((10, 20, 30, 255), (10, 20, 40, 128), True, 127),
        ((255, 0, 0, 64), (0, 0, 0, 64), True, 64),
        ((255, 0, 0, 64), (0, 0, 0, 64), False, 255),
        ((255, 255, 255, 0), (0, 0, 0, 0), True, 0),
        ((255, 255, 255, 0), (0, 0, 0, 0), False, 255),
        ((200, 0, 0, 3), (0, 0, 0, 3), True, 3),
        ((1, 0, 0, 1), (0, 0, 0, 1), True, 1),
    ],
)
def test_difference_histogram_compares_channels(color_a, color_b, premultiplied, expected):
    """
    _difference_histogram puts a pixel in the bucket for its largest difference in any channel, in units of
    0-255.

    With premultiplied colors, a red difference of 255 at alpha 64 counts as 64, and fully transparent
    pixels compare equal whatever their stored colors. That is what lets Live2D tests ignore invisible
    color changes in nearly transparent pixels. Alpha differences count unscaled. The last two cases check
    that fractional differences round up (600/255 to 3, and 1/255 to 1), so a tiny difference is never
    counted as identical and a limit of n/255 is exact.
    """

    histogram = transform._difference_histogram(make_pixel(color_a), make_pixel(color_b), premultiplied)
    assert histogram == single_bucket(expected)


def test_difference_histogram_counts_every_pixel():
    """
    Every pixel is counted once, in the bucket for its own difference, including a pixel far from the
    origin. That checks that every row and column is scanned and that the pitch is respected.
    """

    a = pygame.Surface((257, 129))
    b = a.copy()
    b.set_at((256, 128), (0, 0, 0, 9))
    b.set_at((0, 0), (0, 0, 0, 2))
    b.set_at((1, 0), (0, 0, 0, 2))

    expected = [0] * 256
    expected[0] = 257 * 129 - 3
    expected[2] = 2
    expected[9] = 1

    assert transform._difference_histogram(a, b) == expected
    assert transform._difference_histogram(b, a) == expected


def test_difference_histogram_rejects_different_sizes():
    """
    Surfaces of different sizes raise an error rather than reading past the end of the smaller one.
    """

    with pytest.raises(pygame.error):
        transform._difference_histogram(pygame.Surface((10, 10)), pygame.Surface((10, 11)))
