# Copyright 2004-2016 Tom Rothamel <pytom@bishoujo.us>
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

init python:
    import gui7
    import os

    from store import config

    for fn in [ "gui.rpy", "options.rpy", "script.rpy" ]:
        fn = os.path.join(config.renpy_base, "gui", "game", fn)
        if os.path.exists(fn):
            config.translate_files.append(fn)

    config.translate_comments = config.translate_files


    COLORS = [
        "#99ccff",
        "#cc3300",
        "#cc6600",
        "#66cc00",
        "#00cc99",
        "#0099cc",
        "#0066cc",
        "#9933ff",
        "#cc0066",
        "#cc0000",
    ]

    COLOR_OPTIONS = [
        (i, "#000000", False) for i in COLORS
    ] + [
        (i, "#ffffff", True) for i in COLORS
    ]


#     LIGHT_COLORS = [
#         "#cc6600",
#         "#0099ff",
#         "#cc0066",
#         "#990000",
#         "#000000",
#         "#003366",
#         "#006666",
#         "#000066",
#         "#660066",
#         "#336600",
#     ]


screen gui_swatches():

    default color = (None, None)

    grid 5 4:

        for accent, bg, light in COLOR_OPTIONS:

            frame:
                style "empty"
                xysize (85, 60)

                add Color(accent).replace_hsv_saturation(.5).replace_value(1.0)
                add Color(bg).opacity(.8)

                button:
                    style "empty"

                    if light:
                        selected_background "#000"
                    else:
                        selected_background "#fff"

                    xpadding 3
                    ypadding 3
                    xmargin 10
                    ymargin 10

                    action SetScreenVariable("gui_color", (accent, bg, light))

                    idle_child Solid(accent)
                    hover_child Solid(Color(accent).tint(.6))


screen choose_gui_color():

    frame:
        style_group "l"
        style "l_root"

        window:
            has vbox

            label _("Select Accent and Background Colors")

            frame:
                style "l_indent"

                has hbox:
                    yfill True

                frame:
                    style "l_default"
                    xsize 350

                    has vbox

                    text _("Please click on the color scheme you wish to use, then click Continue. These colors can be changed and customized later.")

                    add SPACER

                    use gui_swatches()


                # Preview
                frame:
                    style "l_default"
                    background Frame(PATTERN, 0, 0, tile=True)
                    xpadding 5
                    ypadding 5

                    xfill True
                    yfill True
                    xmargin 20
                    bottom_margin 6

                    use theme_demo

    textbutton _("Back") action Jump("front_page") style "l_left_button"

    if gui_color:
        textbutton _("Continue") action Return(True) style "l_right_button"



label new_gui_project:

    $ gui_color = None

    call screen choose_gui_color

    python hide:

        project_name = interface.input(
            _("PROJECT NAME"),
            _("Please enter the name of your project:"),
            filename=True,
            cancel=Jump("front_page"))

        project_name = project_name.strip()
        if not project_name:
            interface.error(_("The project name may not be empty."))

        project_dir = os.path.join(persistent.projects_directory, project_name)

        if project.manager.get(project_name) is not None:
            interface.error(_("[project_name!q] already exists. Please choose a different project name."), project_name=project_name)

        if os.path.exists(project_dir):
            interface.error(_("[project_dir!q] already exists. Please choose a different project name."), project_dir=project_dir)
