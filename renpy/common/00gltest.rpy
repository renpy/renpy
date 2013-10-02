# Copyright 2004-2013 Tom Rothamel <pytom@bishoujo.us>
# See LICENSE.txt for license details.

# This contains code to choose between OpenGL and Software rendering, when
# a system supports both.

init -1500:

    python hide:
        import os
        store.__dxwebsetup = os.path.join(config.renpy_base, "lib", "windows-i686", "dxwebsetup.exe")

    python:
        class _SetRenderer(Action):
            """
            Sets the preferred renderer to one of "auto", "angle", "gl", or
            "sw".
            """

            def __init__(self, renderer):
                self.renderer = renderer

            def __call__(self):
                _preferences.renderer = self.renderer
                renpy.restart_interaction()

            def get_selected(self):
                return _preferences.renderer == self.renderer

    # This is displayed to ask the user to choose the renderer he or she
    # wants to use. It takes no parameters, doesn't return anything, and
    # is expected to call _SetRenderer actions and quit when done.
    #
    # This screen can be customized by the creator, provided the actions
    # remain available.
    screen _choose_renderer:

        frame:
            style_group ""

            xalign .5
            yalign .33
            xpadding 20
            ypadding 20

            xmaximum 400

            has vbox

            label _("Graphics Acceleration")

            null height 10

            textbutton _("Automatically Choose"):
                action _SetRenderer("auto")
                xfill True

            if renpy.renpy.windows:
                textbutton _("Force Angle/DirectX Renderer"):
                    action _SetRenderer("angle")
                    xfill True

            textbutton _("Force OpenGL Renderer"):
                action _SetRenderer("gl")
                xfill True

            textbutton _("Force Software Renderer"):
                action _SetRenderer("sw")
                xfill True

            null height 10

            text _("Changes will take effect the next time this program is run.") substitute True

            null height 10

            textbutton _(u"Quit"):
                action Quit(confirm=False)
                xfill True

            if not renpy.display.interface.safe_mode:
                textbutton _("Return"):
                    action Return(0)
                    xfill True


    # This is displayed when a display performance problem occurs.
    #
    # `problem` is the kind of problem that is occuring. It can be:
    # - "sw" if the software renderer was selected.
    # - "slow" if the performance test failed.
    # - "fixed" if we're operating w/o shaders.
    # - other things, added in the future.
    #
    # `url` is the url of a web page on renpy.org that will include
    # info on troubleshooting display problems.
    screen _performance_warning:

        frame:
            style_group ""

            xalign .5
            yalign .33

            xpadding 20
            ypadding 20

            xmaximum 400

            has vbox

            label _("Performance Warning")

            null height 10

            if problem == "sw":
                text _("This computer is using software rendering.")
            elif problem == "fixed":
                text _("This computer is not using shaders.")
            elif problem == "slow":
                text _("This computer is displaying graphics slowly.")
            else:
                text _("This computer has a problem displaying graphics: [problem].") substitute True

            null height 10

            if directx_update:
                text _("Its graphics drivers may be out of date or not operating correctly. This can lead to slow or incorrect graphics display. Updating DirectX could fix this problem.")
            else:
                text _("Its graphics drivers may be out of date or not operating correctly. This can lead to slow or incorrect graphics display.")

            if directx_update:
                null height 10

                textbutton _("Update DirectX"):
                    action directx_update
                    xfill True

            null height 10

            textbutton _("Continue, Show this warning again"):
                action Return(True)
                xfill True

            textbutton _("Continue, Don't show warning again"):
                action Return(False)
                xfill True

            null height 10

            textbutton _("Quit"):
                action Quit(confirm=False)
                xfill True

    # Used while a directx update is ongoing.
    screen _directx_update:

        frame:
            style_group ""

            xalign .5
            yalign .33

            xpadding 20
            ypadding 20

            xmaximum 400

            has vbox

            label _("Updating DirectX.")

            null height 10

            text _("DirectX web setup has been started. It may start minimized in the taskbar. Please follow the prompts to install DirectX.")

            null height 10

            text _("{b}Note:{/b} Microsoft's DirectX web setup program will, by default, install the Bing toolbar. If you do not want this toolbar, uncheck the appropriate box.")

            null height 10

            text _("When setup finishes, please click below to restart this program.")

            textbutton _("Restart") action Return(True)



init -1500 python:
    # The image that we fill the screen with in GL-test mode.
    config.gl_test_image = "black"

    class __GLTest(renpy.Displayable):
        """
         This counts the number of times it's been rendered, and
         the number of seconds it's been displayed, and uses them
         to make the decisions as to if OpenGL is working or not.
         """

        def __init__(self, frames, fps, timeout):
            super(__GLTest, self).__init__()

            self.target = 1.0 * frames / fps
            self.frames = frames
            self.timeout = timeout

            self.times = [ ]
            self.success = False

            renpy.renpy.display.log.write("- Target is {0} frames in {1} seconds.".format(frames, self.target))

        def render(self, width, height, st, at):
            rv = renpy.Render(width, height)

            if self.success:
                return rv

            self.times.append(st)

            renpy.redraw(self, 0)

            renpy.renpy.display.log.write("- Frame drawn at %f seconds." % st)

            if len(self.times) >= self.frames:
                frames_timing = self.times[-1] - self.times[-self.frames]

                renpy.renpy.display.log.write("- %f seconds to render %d frames.", frames_timing, self.frames)

                if frames_timing <= self.target:
                    self.success = True
                    renpy.timeout(0)

            return rv

        def event(self, ev, x, y, st):

            if self.success:
                return True

            if st > self.timeout:
                return False

            renpy.timeout(self.timeout - st)

    config.performance_test = True

    def __gl_test():

        import os

        # If we've entered safe mode, display the renderer choice screen.
        # This screen will cause us to quit.

        if _restart:
            return

        if not config.gl_enable:
            return

        if renpy.display.interface.safe_mode:
            renpy.call_in_new_context("_choose_renderer")

        if not config.performance_test:
            return

        _gl_performance_test()

    def _gl_performance_test():

        import os

        if not _preferences.performance_test and "RENPY_PERFORMANCE_TEST" not in os.environ:
            return

        # Don't bother on androuid - there's nothing the user can do.
        if renpy.renpy.android:
            return

        renpy.renpy.display.log.write("Performance test:")

        # This will cause the screen to start displaying.
        ui.pausebehavior(0)
        ui.interact(suppress_underlay=True, suppress_overlay=True)

        # The problem we have.
        problem = None

        renderer_info = renpy.get_renderer_info()

        # Software renderer check.
        if config.renderer != "sw" and renderer_info["renderer"] == "sw":
            problem = "sw"

        # Speed check.
        if problem is None:

            # The parameters of the performance test. If we do not hit FPS fps
            # over FRAMES frames before DELAY seconds are up, we fail.
            FRAMES = 5
            FPS = 15
            DELAY = 1.5

            renpy.transition(Dissolve(DELAY), always=True, force=True)
            ui.add(__GLTest(FRAMES, FPS, DELAY))
            result = ui.interact(suppress_overlay=True, suppress_underlay=True)

            if not result:
                problem = "slow"

        # Lack of shaders check.
        if problem is None:
            if not "RENPY_GL_ENVIRON" in os.environ:
                if renderer_info["renderer"] == "gl" and renderer_info["environ"] == "fixed":
                    problem = "fixed"

        if problem is None:
            return

        if renpy.renpy.windows and os.path.exists(__dxwebsetup):
            directx_update = Jump("_directx_update")
        else:
            directx_update = None

        # Give the warning message to the user.
        renpy.show_screen("_performance_warning", problem=problem, directx_update=directx_update, _transient=True)
        result = ui.interact(suppress_overlay=True, suppress_underlay=True)


        # Store the user's choice, and continue.
        _preferences.performance_test = result
        return


label _gl_test:

    # Show the test image.
    scene
    show expression config.gl_test_image

    $ __gl_test()

    # Hide the test image.
    scene

    return

# We can assume we're on windows here. We're also always restart once we
# make it here.
label _directx_update:

    if renpy.has_label("directx_update"):
        jump expression "directx_update"

label _directx_update_main:

    python hide:

        # Start dxsetup. We have to go through startfile to ensure that UAC
        # doesn't cause problems.
        os.startfile(__dxwebsetup)

        renpy.show_screen("_directx_update")
        ui.interact(suppress_overlay=True, suppress_underlay=True)

        renpy.quit(relaunch=True)

label _choose_renderer:
    scene expression "#000"

    $ renpy.call_screen("_choose_renderer")
    return
