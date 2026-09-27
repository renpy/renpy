init python:
    import asyncio

    async def async_tasks_waiter():
        await asyncio.sleep(60)

    def test_texture_passes():
        class Draw:
            pending = 0
            processed = 0

            def ready_one_texture(self):
                if not self.pending:
                    return False

                self.pending -= 1
                self.processed += 1
                return True

        interface = renpy.display.interface
        draw = Draw()
        draw.pending = 2
        old_draw = renpy.display.draw
        old_runner = renpy.asyncio.default_runner
        old_task = interface.texture_task
        old_force_prediction = interface.force_prediction
        old_budget = renpy.config.minimum_prediction_time_ns
        runner = renpy.asyncio.Runner()

        try:
            renpy.display.draw = draw
            renpy.asyncio.default_runner = runner
            interface.texture_task = None
            interface.force_prediction = False
            renpy.config.minimum_prediction_time_ns = 0

            interface.run_async(False)
            first_task = interface.texture_task
            assert not first_task.done()
            assert draw.processed == 1

            interface.run_async(False)
            assert interface.texture_task is first_task
            assert draw.processed == 2

            for _ in range(10):
                interface.run_async(False)
                if interface.texture_task.done():
                    break

            assert draw.processed == 2
            assert interface.texture_task.done()
            assert not runner.tasks

            draw.pending = 1
            for _ in range(10):
                interface.run_async(False)
                if interface.texture_task.done():
                    break

            assert interface.texture_task is not first_task
            assert interface.texture_task.done()
            assert draw.processed == 3
            assert not runner.tasks
        finally:
            renpy.display.draw = old_draw
            renpy.asyncio.default_runner = old_runner
            interface.texture_task = old_task
            interface.force_prediction = old_force_prediction
            renpy.config.minimum_prediction_time_ns = old_budget
            runner.close()

    def test_preload_yields():
        cache = renpy.display.im.Cache.__new__(renpy.display.im.Cache)
        cache.preloads = []
        cache.keep_preloading = False
        cache.get_decode_pool = lambda: None
        cache.cleanout = lambda: True
        old_sleep = renpy.display.predict.predict_sleep
        runtime_renpy = renpy.display.im.renpy
        old_emscripten = runtime_renpy.emscripten
        pauses = []

        async def pause():
            pauses.append(True)

        try:
            renpy.display.predict.predict_sleep = pause
            runtime_renpy.emscripten = False
            renpy.asyncio.run_sync(cache.preload_thread_pass())
            assert not pauses

            runtime_renpy.emscripten = True
            renpy.asyncio.run_sync(cache.preload_thread_pass())
            assert len(pauses) == 2
        finally:
            renpy.display.predict.predict_sleep = old_sleep
            runtime_renpy.emscripten = old_emscripten


screen async_tasks_restart_marker():
    text "Restart marker"


testsuite async_tasks:
    testcase texture_work_each_idle_pass:
        $ test_texture_passes()

    testcase preload_yields_only_on_web:
        $ test_preload_yields()

    testcase restart_cancels_old_tasks:
        $ task = renpy.asyncio.create_task(async_tasks_waiter())
        $ renpy.asyncio.run_for_ns(1)
        assert eval not task.done()
        run Show("async_tasks_restart_marker")
        assert eval task.cancelled()
        run Hide("async_tasks_restart_marker")
