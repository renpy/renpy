init python:
    def generator_tasks_waiter():
        global generator_task_cleaned
        try:
            while True:
                yield
        finally:
            generator_task_cleaned = True


screen generator_tasks_restart_marker():
    text "Restart marker"


testsuite generator_tasks:
    testcase restart_cancels_old_tasks:
        $ generator_task_cleaned = False
        $ task = renpy.asynctask.create_task(generator_tasks_waiter())
        $ renpy.asynctask.run_for_ns(1)
        assert eval not task.done()
        run Show("generator_tasks_restart_marker")
        assert eval task.cancelled()
        assert eval generator_task_cleaned
        run Hide("generator_tasks_restart_marker")
