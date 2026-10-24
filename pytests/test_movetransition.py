import unittest

from unittests.renpy_test_support import initialize_renpy

initialize_renpy()

from renpy.display.displayable import place
from renpy.display.movetransition import MoveInterpolate
from renpy.display.transform import Transform


def warp_quadratically(t: float) -> float:
    return t * t


class TestMoveInterpolate(unittest.TestCase):
    """Placement contracts shared by custom and built-in move transitions."""

    def test_horizontal_entrance_preserves_height_and_offsets(self) -> None:
        # A 100x80 image in a 1000x500 area ends at x=417, accounting for its
        # half-width anchor and seven-pixel offset. The vertical anchor is 20px.
        for ypos, expected_y in ((-0.16, -89), (0.3, 141)):
            for side, xpos, xanchor, start_x in (
                ("left", 0.0, 1.0, -93),
                ("right", 1.0, 0.0, 1007),
            ):
                for time_warp, midpoint in ((None, 0.5), (warp_quadratically, 0.25)):
                    with self.subTest(ypos=ypos, side=side, time_warp=time_warp):
                        image = Transform(
                            xpos=0.46,
                            ypos=ypos,
                            xanchor=0.5,
                            yanchor=0.25,
                            xoffset=7,
                            yoffset=11,
                        )
                        entrance = Transform(image, xpos=xpos, xanchor=xanchor)
                        move = MoveInterpolate(1.0, entrance, image, False, time_warp)

                        # Supply the geometry/time normally recorded by render,
                        # keeping this placement test independent of a GPU.
                        move.screen_width, move.screen_height = 1000, 500
                        move.child_width, move.child_height = 100, 80
                        for st, fraction in ((0.0, 0.0), (0.5, midpoint), (1.0, 1.0), (1.5, 1.0)):
                            move.st = st
                            x, y = place(1000, 500, 100, 80, move.get_placement())
                            self.assertAlmostEqual(x, start_x + fraction * (417 - start_x))
                            self.assertAlmostEqual(y, expected_y)

    def test_explicit_vertical_entrance_is_interpolated(self) -> None:
        image = Transform(xpos=0.46, ypos=-0.16, xanchor=0.5, yanchor=0.25)
        entrance = Transform(image, xpos=1.0, xanchor=0.0, ypos=1.0, yanchor=1.0)
        move = MoveInterpolate(1.0, entrance, image, False, None)
        move.screen_width, move.screen_height = 1000, 500
        move.child_width, move.child_height = 100, 80

        # Bottom-aligned starts at 500-80=420; the destination is -80-20=-100.
        for st, expected in ((0.0, (1000, 420)), (0.5, (705, 160)), (1.0, (410, -100))):
            with self.subTest(st=st):
                move.st = st
                x, y = place(1000, 500, 100, 80, move.get_placement())
                self.assertAlmostEqual(x, expected[0])
                self.assertAlmostEqual(y, expected[1])
