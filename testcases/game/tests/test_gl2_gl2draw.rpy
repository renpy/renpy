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

    class test_gl2draw__HeldTexture(renpy.Displayable):
        """
        Draws a texture loaded once with renpy.load_rgba, which is kept across display resets, as a creator-defined
        displayable can. The texture is kept on the class, so the displayable can still be saved, and so dropping it
        isn't recorded in the rollback log, which would keep it alive.
        """

        tex = None

        def render(self, width, height, st, at):
            cls = test_gl2draw__HeldTexture

            if cls.tex is None:
                cls.tex = renpy.load_rgba(b"\xff\x00\x00\xff" * (64 * 64), (64, 64))

            rv = renpy.Render(64, 64)
            rv.blit(cls.tex, (0, 0))
            return rv

define test_gl2draw__held = test_gl2draw__HeldTexture()


label test_gl2draw__scene:
    scene expression Solid("#336")
    show expression Text("GL context {b}recovery{/b}", size=60, color="#fc0") as test_gl2draw__text:
        xalign 0.5 yalign 0.4

    pause

    return


label test_gl2draw__held_scene:
    # Each test loads its own texture, rather than using one left by an earlier test.
    $ test_gl2draw__HeldTexture.tex = None

    scene expression Solid("#336")
    show expression test_gl2draw__held as test_gl2draw__held:
        align (0.5, 0.5)

    pause

    # Drop the held texture, so it can be freed.
    hide test_gl2draw__held
    $ test_gl2draw__HeldTexture.tex = None

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

    testcase kept_context_keeps_held_texture:
        description "A texture a displayable keeps still draws after a display reset that keeps the GL context"
        # Resetting the texture loader once deleted every texture still allocated, so this one drew as black.

        run Start("test_gl2draw__held_scene")
        pause 0.5

        $ test_gl2draw__before = renpy.exports.screenshot_to_bytes(None)

        $ renpy.display.interface.display_reset = True
        pause 0.5

        assert eval renpy.exports.screenshot_to_bytes(None) == test_gl2draw__before

    testcase kept_context_frees_held_texture:
        description "A texture kept across a display reset that keeps the GL context is freed once it's dropped"
        # Treating every full reset as a new context abandoned such textures, leaking their memory.

        run Start("test_gl2draw__held_scene")
        pause 0.3

        $ renpy.display.interface.display_reset = True
        pause 0.3

        $ test_gl2draw__count_before = renpy.get_texture_size()[1]

        click
        pause 0.3

        assert eval renpy.get_texture_size()[1] == test_gl2draw__count_before - 1

    testcase replaced_context_frees_new_texture:
        description "A texture loaded after the GL context is replaced is freed once it's dropped"
        # Textures record the context generation they were loaded in, and only ones from the current generation
        # are deleted, so a texture missing that record would leak.

        $ test_gl2draw__force_new_context()
        pause 0.3

        run Start("test_gl2draw__held_scene")
        pause 0.3

        $ test_gl2draw__count_before = renpy.get_texture_size()[1]

        click
        pause 0.3

        assert eval renpy.get_texture_size()[1] == test_gl2draw__count_before - 1

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
