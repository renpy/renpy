import unittest
from unittest.mock import Mock

from unittests.renpy_test_support import initialize_renpy

initialize_renpy()

from renpy.display.render import Render


class TestFocusMask(unittest.TestCase):
    def test_callable_receives_width_and_height(self):
        render = Render(120, 60)
        displayable = object()
        result = Mock(return_value=True)
        mask = Mock(return_value=result)
        render.add_focus(displayable, None, 0, 0, 120, 60, 10, 5, mask)

        self.assertEqual(render.focus_at_point(30, 20, None), (displayable, None, None))
        mask.assert_called_once_with(20, 15)
        result.assert_called_once_with(20, 15, 110, 55)

    def test_clipped_callable_preserves_coordinates_and_dimensions(self):
        for subpixel in (False, True):
            with self.subTest(subpixel=subpixel):
                render = Render(120, 60)
                displayable = object()
                result = Mock(return_value=True)
                mask = Mock(return_value=result)
                render.add_focus(displayable, None, 0, 0, 120, 60, 0, 0, mask)
                clipped = render.subsurface((20, 10, 70, 30), focus=True, subpixel=subpixel)
                clipped = clipped.subsurface((5, 4, 40, 20), focus=True, subpixel=subpixel)

                self.assertEqual(clipped.focus_at_point(3, 2, None), (displayable, None, None))
                mask.assert_called_once_with(28, 16)
                result.assert_called_once_with(28, 16, 120, 60)
                for point in ((-1, 2), (40, 2), (3, -1), (3, 20)):
                    self.assertIsNone(clipped.focus_at_point(*point, None))
                self.assertEqual(mask.call_count, 1)

    def test_render_mask_still_clips(self):
        render = Render(120, 60)
        mask = Render(120, 60)
        displayable = object()
        render.add_focus(displayable, None, 0, 0, 120, 60, 0, 0, mask)
        clipped = render.subsurface((20, 10, 70, 30), focus=True)

        self.assertEqual(clipped.focuses[0][:8], (displayable, None, 0, 0, 70, 30, 0, 0))
        self.assertEqual(clipped.focuses[0][8].get_size(), (70, 30))
