import unittest
from types import SimpleNamespace
from unittest.mock import patch

import renpy
from unittests.renpy_test_support import initialize_renpy

initialize_renpy()

from renpy.display import predict
from renpy.sl2 import slast


class TestScreenPredictionPause(unittest.TestCase):
    def test_cancelled_prediction_pause_restores_ui_state(self):
        old_predicting = predict.predicting
        old_deadline = predict.next_predict_pause_ns
        old_screen = renpy.ui.screen
        old_stack = renpy.ui.stack
        old_at_stack = renpy.ui.at_stack
        old_imagemap_stack = renpy.ui.imagemap_stack
        old_add_tag = renpy.ui.add_tag
        old_screen_stack = renpy.display.screen.current_screen_stack
        old_current_screen = renpy.display.screen._current_screen

        try:
            predict.predicting = True
            predict.next_predict_pause_ns = 0
            pause = predict.predict_sleep()
            self.assertIsNone(next(pause))
            self.assertFalse(predict.predicting)
            pause.close()

            self.assertTrue(predict.predicting)
            self.assertIs(renpy.ui.screen, old_screen)
            self.assertIs(renpy.ui.stack, old_stack)
            self.assertIs(renpy.ui.at_stack, old_at_stack)
            self.assertIs(renpy.ui.imagemap_stack, old_imagemap_stack)
            self.assertIs(renpy.ui.add_tag, old_add_tag)
            self.assertIs(renpy.display.screen.current_screen_stack, old_screen_stack)
            self.assertIs(renpy.display.screen._current_screen, old_current_screen)
        finally:
            predict.predicting = old_predicting
            predict.next_predict_pause_ns = old_deadline

    def test_screen_pause_does_not_postpone_prediction_yield(self):
        old_predicting = predict.predicting
        old_deadline = predict.next_predict_pause_ns

        try:
            predict.predicting = True
            predict.next_predict_pause_ns = 0
            context = SimpleNamespace(yield_prediction=True)

            with patch.object(slast.time, "perf_counter_ns", return_value=1_000_000):
                self.assertEqual(list(slast.predict_pause(context)), [None])
                self.assertEqual(predict.next_predict_pause_ns, 0)

                pause = predict.predict_sleep()
                self.assertIsNone(next(pause))
                with self.assertRaises(StopIteration):
                    next(pause)

                self.assertEqual(predict.next_predict_pause_ns, 1_100_000)
                self.assertEqual(list(slast.predict_pause(context)), [])

                predict.predicting = False
                predict.next_predict_pause_ns = 0
                self.assertEqual(list(slast.predict_pause(context)), [])
        finally:
            predict.predicting = old_predicting
            predict.next_predict_pause_ns = old_deadline
