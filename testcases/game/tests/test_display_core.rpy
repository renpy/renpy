# Tests for the interaction loop in renpy/display/core.py.

# ==============
# == Fixtures ==
# ==============

init python:

    class display_core__SlowMotionCounter(renpy.Displayable):
        """
        A displayable that takes longer to render than the timer in display_core__restarting_timer_screen waits
        between restarts, and counts the mouse motion events it receives.
        """

        motion = 0

        def render(self, width, height, st, at):
            import time
            time.sleep(0.04)

            renpy.redraw(self, 0)
            return renpy.Render(width, height)

        def event(self, ev, x, y, st):
            if ev.type == renpy.display.core.pygame.MOUSEMOTION:
                display_core__SlowMotionCounter.motion += 1

    display_core__counter = display_core__SlowMotionCounter()

screen display_core__restarting_timer_screen():
    add display_core__counter
    timer 0.03 repeat True action Function(renpy.restart_interaction)


# ==============
# === Tests ====
# ==============

testsuite display_core:

    testcase motion_reaches_displayables_while_timer_restarts:
        description "Mouse motion reaches displayables while a repeating timer restarts the interaction faster than a frame can be drawn."
        # GH-7566: https://github.com/renpy/renpy/issues/7566

        run Show("display_core__restarting_timer_screen")
        assert screen "display_core__restarting_timer_screen"
        $ display_core__SlowMotionCounter.motion = 0

        move pos (100, 100)
        pause 0.2
        move pos (200, 150)
        pause 0.2
        move pos (300, 200)
        pause 0.2

        assert eval display_core__SlowMotionCounter.motion > 0

        run Hide("display_core__restarting_timer_screen")
