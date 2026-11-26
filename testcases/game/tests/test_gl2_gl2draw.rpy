# This file tests how the GL2 renderer recovers its GL context.

# ==============
# == Fixtures ==
# ==============

init python:

    def test_gl2draw__force_new_context():
        """
        Requests what a Windows restore from minimized does: the next display reset destroys the GL context and
        creates a new one.
        """

        renpy.display.interface.gl_context_force_new = True
        renpy.display.interface.display_reset = True

    def test_gl2draw__post(event_type):
        """
        Posts a window event of `event_type`, as SDL would.
        """

        renpy.pygame.event.post(renpy.pygame.event.Event(event_type))


label test_gl2draw__scene:
    scene expression Solid("#336")
    show expression Text("GL context {b}recovery{/b}", size=60, color="#fc0") as test_gl2draw__text:
        xalign 0.5 yalign 0.4

    pause

    return


# ==============
# === Tests ====
# ==============

testsuite gl2draw:
    after testcase:
        if not screen "main_menu":
            run MainMenu(confirm=False, save=False)

    testcase force_new_context:
        description "The scene renders the same after the GL context is destroyed and recreated"
        # Shaders and textures from the old context must all be replaced. Programs freed after the new context
        # had reused their numbers once deleted the new solid-color program, so solids stopped drawing.

        run Start("test_gl2draw__scene")
        pause 0.5

        $ test_gl2draw__before = renpy.exports.screenshot_to_bytes(None)

        $ test_gl2draw__force_new_context()
        pause 0.5
        assert eval not renpy.display.interface.gl_context_force_new

        $ test_gl2draw__force_new_context()
        pause 0.5

        assert eval renpy.exports.screenshot_to_bytes(None) == test_gl2draw__before

    testcase minimize_tracking:
        description "A restore or maximize only counts as unminimizing after a minimize"
        # On Windows, unminimizing replaces the GL context; the replacement itself is covered by
        # force_new_context, since it can't be triggered on other platforms.

        run Start("test_gl2draw__scene")
        pause 0.3

        $ test_gl2draw__post(renpy.pygame.WINDOWMAXIMIZED)
        pause 0.2
        assert eval not renpy.display.interface.window_minimized

        $ test_gl2draw__post(renpy.pygame.WINDOWMINIMIZED)
        pause 0.2
        assert eval renpy.display.interface.window_minimized

        $ test_gl2draw__post(renpy.pygame.WINDOWRESTORED)
        pause 0.5
        assert eval not renpy.display.interface.window_minimized
        assert eval not renpy.display.interface.gl_context_force_new
