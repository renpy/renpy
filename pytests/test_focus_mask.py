import threading
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from unittests.renpy_test_support import initialize_renpy

initialize_renpy()

import renpy
from renpy.display import behavior
from renpy.display.displayable import Displayable
from renpy.display.render import Render


def make_style(**properties: object) -> SimpleNamespace:
    """
    Returns a stand-in for the style properties used when rendering a displayable, as styles are not built
    in unit tests.
    """

    return SimpleNamespace(xmaximum=None, ymaximum=None, debug=False, **properties)


class FailingMask(Displayable):
    """
    A focus mask whose render fails like an image with a missing file, recording the value of
    renpy.display.im.thread_local.raise_image_load_exceptions seen while rendering.
    """

    def __init__(self) -> None:
        super().__init__()
        self.style = make_style()
        self.raise_image_load_exceptions: list[object] = []
        self.config_raise_image_load_exceptions: list[object] = []

    def render(self, width: int, height: int, st: float, at: float) -> Render:
        self.raise_image_load_exceptions.append(renpy.display.im.thread_local.raise_image_load_exceptions)
        self.config_raise_image_load_exceptions.append(renpy.config.raise_image_load_exceptions)
        raise FileNotFoundError("Couldn't find file 'missing_mask.png'.")


class CallableMask(Displayable):
    """
    A focus mask that is both a displayable and callable, like a Transform.
    """

    def __init__(self) -> None:
        super().__init__()
        self.style = make_style()

    def render(self, width: int, height: int, st: float, at: float) -> Render:
        return Render(width, height)

    def __call__(self, *args: object) -> bool:
        raise AssertionError("A displayable focus mask must be rendered, not called.")


class TestRenderFocusMask(unittest.TestCase):
    def setUp(self) -> None:
        behavior.focus_mask_errors_logged.clear()

    def render_mask(self, mask: object, raise_image_load_exceptions: bool) -> object:
        thread_local = renpy.display.im.thread_local

        with patch.object(thread_local, "raise_image_load_exceptions", raise_image_load_exceptions):
            try:
                return behavior.render_focus_mask(mask, 40, 20, 0, 0)
            finally:
                self.assertIs(thread_local.raise_image_load_exceptions, raise_image_load_exceptions)

    def test_broken_mask_raises_original_exception_when_load_exceptions_enabled(self) -> None:
        mask = FailingMask()

        with self.assertRaises(FileNotFoundError) as cm:
            self.render_mask(mask, True)

        self.assertIn("While rendering the focus_mask", "\n".join(cm.exception.__notes__))

    def test_broken_mask_is_ignored_and_logged_once_when_load_exceptions_disabled(self) -> None:
        mask = FailingMask()

        with patch.object(renpy.display, "log") as log:
            self.assertIsNone(self.render_mask(mask, False))
            self.assertIsNone(self.render_mask(mask, False))

        self.assertEqual(mask.raise_image_load_exceptions, [True, True])
        self.assertEqual(mask.config_raise_image_load_exceptions, [renpy.config.raise_image_load_exceptions] * 2)
        log.write.assert_called_once()
        log.exception.assert_called_once()

    def test_control_exceptions_are_not_ignored(self) -> None:
        mask = FailingMask()
        mask.render = Mock(side_effect=renpy.game.JumpException("start"))

        with self.assertRaises(renpy.game.JumpException):
            self.render_mask(mask, False)

    def test_mask_kinds(self) -> None:
        true_mask = Render(40, 20)
        function = Mock()

        self.assertIsNone(behavior.render_focus_mask(None, 40, 20, 0, 0, true_mask))
        self.assertIs(behavior.render_focus_mask(True, 40, 20, 0, 0, true_mask), true_mask)
        self.assertIs(behavior.render_focus_mask(function, 40, 20, 0, 0), function)
        self.assertIsInstance(behavior.render_focus_mask(CallableMask(), 40, 20, 0, 0), Render)

        with self.assertRaises(TypeError):
            behavior.render_focus_mask(42, 40, 20, 0, 0)


class TestImageThreadLocal(unittest.TestCase):
    def test_new_thread_starts_from_config(self) -> None:
        values = []

        with patch.object(renpy.config, "raise_image_load_exceptions", True):
            thread = threading.Thread(
                target=lambda: values.append(renpy.display.im.thread_local.raise_image_load_exceptions)
            )
            thread.start()
            thread.join()

        self.assertEqual(values, [True])


class TestMouseAreaFocusMask(unittest.TestCase):
    def hover(self, focus_mask: object, x: int, y: int) -> bool:
        mousearea = behavior.MouseArea()
        mousearea.style = make_style(focus_mask=focus_mask)
        mousearea.width = 40
        mousearea.height = 20

        with (
            patch.object(renpy.display.focus, "get_grab", return_value=None),
            patch.object(renpy.display.focus, "pending_focus_type", "mouse"),
            patch.object(renpy.display.im.thread_local, "raise_image_load_exceptions", False),
            patch.object(renpy.display, "log"),
        ):
            mousearea.event(Mock(type=0), x, y, 0)

        return mousearea.is_hovered

    def test_callable_mask(self) -> None:
        mask = Mock(side_effect=lambda x, y: x < 10)

        self.assertTrue(self.hover(mask, 5, 5))
        self.assertFalse(self.hover(mask, 15, 5))
        self.assertFalse(self.hover(mask, -5, 5))

    def test_broken_mask_falls_back_to_area(self) -> None:
        self.assertTrue(self.hover(FailingMask(), 5, 5))
        self.assertFalse(self.hover(FailingMask(), 50, 5))


class TestFocusMask(unittest.TestCase):
    def test_callable_receives_displayable_dimensions(self):
        render = Render(120, 60)
        displayable = object()
        result = Mock(return_value=True)
        mask = Mock(return_value=result)
        render.add_focus(displayable, None, 0, 0, 120, 60, 10, 5, mask)

        self.assertEqual(render.focus_at_point(30, 20, None), (displayable, None, None))
        mask.assert_called_once_with(20, 15)
        result.assert_called_once_with(20, 15, 110, 55)

    def test_callable_mask_remains_focusable_after_nested_clipping(self):
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
                    with self.subTest(point=point):
                        self.assertIsNone(clipped.focus_at_point(*point, None))

                self.assertEqual(mask.call_count, 1)


if __name__ == "__main__":
    unittest.main()
