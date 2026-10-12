import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

import renpy
from unittests.renpy_test_support import initialize_renpy

initialize_renpy()

from renpy.display import dragdrop
from renpy.display.core import IgnoreEvent
from renpy.display.dragdrop import Drag
from renpy.display.layout import Null


class TestDragEvents(unittest.TestCase):
    def setUp(self):
        patcher = patch.object(renpy.game, "log", SimpleNamespace(mutated={}))
        patcher.start()
        self.addCleanup(patcher.stop)

    def make_drag(self, **kwargs):
        drag = Drag(Null(), **kwargs)
        drag.last_x = drag.last_y = 0
        drag.is_focused = Mock(return_value=True)
        drag.child.event = Mock(return_value=None)
        return drag

    def test_ungrabbed_child_gets_event_once(self):
        drag = self.make_drag(draggable=False)
        event = renpy.pygame.event.Event(renpy.pygame.KEYDOWN)
        with (
            patch.object(renpy.display.focus, "get_grab", return_value=None),
            patch.object(dragdrop, "map_event", return_value=False),
        ):
            self.assertIsNone(drag.event(event, 3, 4, 0))
        drag.child.event.assert_called_once_with(event, 3, 4, 0)

    def test_joined_move_updates_each_position_before_callback(self):
        for result in (None, "dragging"):
            with self.subTest(result=result):
                first = self.make_drag(drag_raise=False)
                second = self.make_drag()
                group = Mock(positions={})
                group.get_best_drop = Mock(return_value=None)

                for index, drag in enumerate((first, second)):
                    drag.drag_name = str(index)
                    drag.drag_group = group
                    drag.parent_width = drag.parent_height = 200
                    drag.w = drag.h = 10
                    drag.old_position = (index * 20, index * 30, 0, 0, 0, 0)

                first.drag_joined = lambda drag, first=first, second=second: [(first, 0, 0), (second, 20, 30)]
                first.grab_x = first.grab_y = 0
                callback_positions = []

                def dragging(joined, result=result, snapshots=callback_positions):
                    snapshots.append(tuple((drag.x, drag.y) for drag in joined))
                    return result

                first.dragging = Mock(side_effect=dragging)
                event = renpy.pygame.event.Event(renpy.pygame.MOUSEMOTION)
                with (
                    patch.object(renpy.display.focus, "get_grab", return_value=first),
                    patch.object(dragdrop, "map_event", return_value=False),
                    patch.object(dragdrop, "redraw"),
                    patch.object(first, "update_style_prefix"),
                ):
                    if result is None:
                        with self.assertRaises(IgnoreEvent):
                            first.event(event, 5, 7, 0)
                    else:
                        self.assertEqual(first.event(event, 5, 7, 0), result)

                first.dragging.assert_called_once_with([first, second])
                self.assertEqual(callback_positions, [((5, 7), (25, 37))])
                self.assertEqual(group.positions["0"], (5, 7, first.old_position))
                self.assertEqual(group.positions["1"], (25, 37, second.old_position))
                for drag in (first, second):
                    self.assertEqual((drag.target_x, drag.target_y), (drag.x, drag.y))
