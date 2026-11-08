"""Placement contracts shared by custom and built-in move transitions."""

import pytest

from renpy.display.displayable import place
from renpy.display.movetransition import MoveInterpolate
from renpy.display.transform import Transform


def warp_quadratically(t: float) -> float:
    """A time warp that reaches the halfway point a quarter of the way through."""

    return t * t


def make_move(entrance, image, time_warp):
    """
    Creates a one-second MoveInterpolate from `entrance` to `image`, with the geometry that render
    would normally record filled in: a 100x80 child in a 1000x500 area. This keeps the placement tests
    independent of a GPU.
    """

    move = MoveInterpolate(1.0, entrance, image, False, time_warp)
    move.screen_width, move.screen_height = 1000, 500
    move.child_width, move.child_height = 100, 80
    return move


@pytest.mark.parametrize(
    ("time_warp", "midpoint"), [(None, 0.5), (warp_quadratically, 0.25)], ids=["linear", "quadratic"]
)
@pytest.mark.parametrize(
    ("side", "xpos", "xanchor", "start_x"), [("left", 0.0, 1.0, -93), ("right", 1.0, 0.0, 1007)], ids=["left", "right"]
)
@pytest.mark.parametrize(("ypos", "expected_y"), [(-0.16, -89), (0.3, 141)], ids=["offscreen-y", "onscreen-y"])
def test_horizontal_entrance_preserves_height_and_offsets(
    ypos, expected_y, side, xpos, xanchor, start_x, time_warp, midpoint
):
    """
    An entrance that only sets x positions moves horizontally while keeping the image's own vertical
    placement and its offsets.

    A 100x80 image in a 1000x500 area ends at x=417, accounting for its half-width anchor and
    seven-pixel offset. The vertical anchor is 20px. Parametrized over entering from the left and right,
    over a y position that is partly offscreen and one that is onscreen, and over a linear and a
    quadratic time warp (whose midpoint fraction is 0.25 instead of 0.5). Placement is checked at the
    start, the midpoint, the end, and after the end, where it must stay at the destination.
    """

    image = Transform(xpos=0.46, ypos=ypos, xanchor=0.5, yanchor=0.25, xoffset=7, yoffset=11)
    entrance = Transform(image, xpos=xpos, xanchor=xanchor)
    move = make_move(entrance, image, time_warp)

    for st, fraction in ((0.0, 0.0), (0.5, midpoint), (1.0, 1.0), (1.5, 1.0)):
        move.st = st
        x, y = place(1000, 500, 100, 80, move.get_placement())
        assert x == pytest.approx(start_x + fraction * (417 - start_x), abs=1e-7), f"st={st}"
        assert y == pytest.approx(expected_y, abs=1e-7), f"st={st}"


@pytest.mark.parametrize(("st", "expected"), [(0.0, (1000, 420)), (0.5, (705, 160)), (1.0, (410, -100))])
def test_explicit_vertical_entrance_is_interpolated(st, expected):
    """
    When the entrance sets its own y position, the vertical position is interpolated too, not just the
    horizontal one.

    Bottom-aligned, the move starts at 500-80=420; the destination is -80-20=-100. Parametrized over
    the start, midpoint, and end of the move.
    """

    image = Transform(xpos=0.46, ypos=-0.16, xanchor=0.5, yanchor=0.25)
    entrance = Transform(image, xpos=1.0, xanchor=0.0, ypos=1.0, yanchor=1.0)
    move = make_move(entrance, image, None)

    move.st = st
    x, y = place(1000, 500, 100, 80, move.get_placement())
    assert x == pytest.approx(expected[0], abs=1e-7)
    assert y == pytest.approx(expected[1], abs=1e-7)
