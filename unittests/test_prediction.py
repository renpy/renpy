import asyncio
import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import renpy

renpy.import_all()

from renpy.display import predict
from renpy.sl2 import slast


class TestScreenPredictionPause(unittest.TestCase):
    def test_screen_pause_yields_without_postponing_async_sleep(self):
        old_predicting = predict.predicting
        old_deadline = predict.next_predict_pause_ns

        try:
            predict.predicting = True
            predict.next_predict_pause_ns = 0
            context = SimpleNamespace(yield_prediction=True)

            with patch.object(slast.time, "perf_counter_ns", return_value=1_000_000):
                self.assertEqual(list(slast.predict_pause(context)), [None])
                self.assertEqual(predict.next_predict_pause_ns, 0)

                with patch.object(predict.asyncio, "sleep", new_callable=AsyncMock) as sleep:
                    asyncio.run(predict.predict_sleep())

                sleep.assert_awaited_once_with(0)
                self.assertEqual(predict.next_predict_pause_ns, 1_100_000)
                self.assertEqual(list(slast.predict_pause(context)), [])

                predict.predicting = False
                predict.next_predict_pause_ns = 0
                self.assertEqual(list(slast.predict_pause(context)), [])
        finally:
            predict.predicting = old_predicting
            predict.next_predict_pause_ns = old_deadline
