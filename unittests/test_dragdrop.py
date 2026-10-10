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
        for event_type in (renpy.pygame.MOUSEMOTION, renpy.pygame.KEYDOWN):
            with self.subTest(event_type=event_type), patch.object(renpy.display.focus, "get_grab", return_value=None):
                event = renpy.pygame.event.Event(event_type)
                with patch.object(dragdrop, "map_event", return_value=False):
                    self.assertIsNone(drag.event(event, 3, 4, 0))
                drag.child.event.assert_called_once_with(event, 3, 4, 0)
                drag.child.event.reset_mock()

    def test_child_result_stops_click_handling(self):
        clicked = Mock()
        drag = self.make_drag(draggable=False, clicked=clicked)
        drag.child.event.return_value = "child result"
        event = renpy.pygame.event.Event(renpy.pygame.MOUSEBUTTONUP)
        with patch.object(renpy.display.focus, "get_grab", return_value=None):
            self.assertEqual(drag.event(event, 3, 4, 0), "child result")
        drag.child.event.assert_called_once()
        clicked.assert_not_called()

    def test_droppable_click_preserves_result_and_ignore_event(self):
        for result in (None, "clicked"):
            with self.subTest(result=result):
                clicked = Mock(return_value=result)
                drag = self.make_drag(draggable=False, clicked=clicked)
                drag.click_time = 1
                event = renpy.pygame.event.Event(renpy.pygame.MOUSEBUTTONUP)
                with (
                    patch.object(renpy.display.focus, "get_grab", return_value=None),
                    patch.object(dragdrop, "map_event", side_effect=lambda ev, name: name == "drag_deactivate"),
                ):
                    if result is None:
                        with self.assertRaises(IgnoreEvent):
                            drag.event(event, 3, 4, 2)
                    else:
                        self.assertEqual(drag.event(event, 3, 4, 2), result)
                self.assertIsNone(drag.click_time)
                clicked.assert_called_once_with(drag)
                drag.child.event.assert_called_once_with(event, 3, 4, 2)

    def test_joined_move_updates_every_member_before_callback(self):
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
                first.drag_joined = lambda drag: [(first, 0, 0), (second, 20, 30)]
                first.grab_x = first.grab_y = 0

                def dragging(joined):
                    self.assertEqual(joined, [first, second])
                    self.assertEqual([(d.x, d.y) for d in joined], [(5, 7), (25, 37)])
                    self.assertEqual(group.positions["0"], (5, 7, first.old_position))
                    self.assertEqual(group.positions["1"], (25, 37, second.old_position))
                    return result

                first.dragging = Mock(side_effect=dragging)
                event = renpy.pygame.event.Event(renpy.pygame.MOUSEMOTION)
                with (
                    patch.object(renpy.display.focus, "get_grab", return_value=first),
                    patch.object(dragdrop, "map_event", return_value=False),
                    patch.object(dragdrop, "redraw") as redraw,
                    patch.object(first, "update_style_prefix"),
                ):
                    if result is None:
                        with self.assertRaises(IgnoreEvent):
                            first.event(event, 5, 7, 0)
                    else:
                        self.assertEqual(first.event(event, 5, 7, 0), result)
                first.dragging.assert_called_once_with([first, second])
                self.assertEqual([call.args for call in redraw.call_args_list], [(first, 0), (second, 0)])
                for drag in (first, second):
                    self.assertEqual((drag.target_x, drag.target_y), (drag.x, drag.y))
                first.child.event.assert_not_called()
