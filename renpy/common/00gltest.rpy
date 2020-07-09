# Copyright 2004-2020 Tom Rothamel <pytom@bishoujo.us>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# This contains code to choose between OpenGL and Software rendering, when
# a system supports both.

init -1500:

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

            has side "c b":
                spacing gui._scale(10)
                xfill True
                yfill True

            fixed:

                vbox:

                    xmaximum 0.48

                    label _("Renderer")

                    null height 10

                    textbutton _("Automatically Choose"):
                        action _SetRenderer("auto")
                        style_suffix "radio_button"

                    if not config.gl2:

                        if renpy.renpy.windows:
                            textbutton _("Force ANGLE Renderer"):
                                action _SetRenderer("angle")
                                style_suffix "radio_button"

                        textbutton _("Force GL Renderer"):
                            action _SetRenderer("gl")
                            style_suffix "radio_button"

                        textbutton _("Force GLES Renderer"):
                            action _SetRenderer("gles")
                            style_suffix "radio_button"

                    if renpy.renpy.windows:
                        textbutton _("Force ANGLE2 Renderer"):
                            action _SetRenderer("angle2")
                            style_suffix "radio_button"

                    textbutton _("Force GL2 Renderer"):
                        action _SetRenderer("gl2")
                        style_suffix "radio_button"

                    textbutton _("Force GLES2 Renderer"):
                        action _SetRenderer("gles2")
                        style_suffix "radio_button"


                    null height 10

                    label _("Gamepad")

                    null height 10

                    textbutton _("Enable"):
                        action SetField(_preferences, "pad_enabled", True)
                        style_suffix "radio_button"

                    textbutton _("Disable"):
                        action SetField(_preferences, "pad_enabled", False)
                        style_suffix "radio_button"

                    null height 10

                    textbutton _("Calibrate"):
                        action ui.invokesinnewcontext(_gamepad.calibrate)
                        xfill True

                vbox:

                    xmaximum 0.48
                    xpos 0.5

                    label _("Powersave")

                    null height 10

                    textbutton _("Enable"):
                        action Preference("gl powersave", True)
                        style_suffix "radio_button"

                    textbutton _("Disable"):
                        action Preference("gl powersave", False)
                        style_suffix "radio_button"

                    null height 10

                    label _("Framerate")

                    null height 10

                    textbutton _("Screen"):
                        action Preference("gl framerate", None)
                        style_suffix "radio_button"

                    textbutton _("60"):
                        action Preference("gl framerate", 60)
                        style_suffix "radio_button"

                    textbutton _("30"):
                        action Preference("gl framerate", 30)
                        style_suffix "radio_button"

                    null height 10

                    label _("Tearing")

                    null height 10

                    textbutton _("Enable"):
                        action Preference("gl tearing", True)
                        style_suffix "radio_button"

                    textbutton _("Disable"):
                        action Preference("gl tearing", False)
                        style_suffix "radio_button"

                    null height 10

            vbox:

                text _("Changes will take effect the next time this program is run.") substitute True

                null height 10

                hbox:
                    spacing gui._scale(25)

                    textbutton _(u"Quit"):
                        action Quit(confirm=False)
                        yalign 1.0

                    if not renpy.display.interface.safe_mode:
                        textbutton _("Return"):
                            action Return(0)
                            yalign 1.0


    # This is displayed when a display performance problem occurs.
    #
    # `problem` is the kind of problem that is occuring. It can be:
    # - "sw" if the software renderer was selected.
    # - other things, added in the future.
    #
    # `url` is the url of a web page on renpy.org that will include
    # info on troubleshooting display problems.
    screen _performance_warning:

        frame:
            style_group ""

            has vbox

            label _("Performance Warning")

            null height 10

            if problem == "sw":
                text _("This computer is using software rendering.")
            else:
                text _("This computer has a problem displaying graphics: [problem].") substitute True

            null height 10

            text _("Its graphics drivers may be out of date or not operating correctly. This can lead to slow or incorrect graphics display.")

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


init -1500 python:
    # The image that we fill the screen with in GL-test mode.
    config.gl_test_image = "black"

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

        performance_test = os.environ.get("RENPY_PERFORMANCE_TEST", None)

        if performance_test is not None:
            performance_test = int(performance_test)

        if performance_test == 0:
            return

        if not _preferences.performance_test and not performance_test:
            return

        # Don't bother on android or ios or emscripten - there's nothing the user can do.
        if renpy.mobile:
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

        if problem is None:
            return

        directx_update = None

        # Give the warning message to the user.
        renpy.show_screen("_performance_warning", problem=problem, directx_update=directx_update, _transient=True)
        result = ui.interact(suppress_overlay=True, suppress_underlay=True)

        # Store the user's choice, and continue.
        _preferences.performance_test = result
        return


label _gl_test:

    # Show the test image.
    scene black
    show expression config.gl_test_image
    with None

    $ __gl_test()

    # Hide the test image.
    scene black

    return

label _choose_renderer:
    scene expression "#000"

    $ renpy.shown_window()
    $ renpy.show_screen("_choose_renderer",  _transient=True)
    $ ui.interact(suppress_overlay=True, suppress_underlay=True)
    return
