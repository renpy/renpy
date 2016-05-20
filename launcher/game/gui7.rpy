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


    DARK_COLORS = [
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


    LIGHT_COLORS = [
        "#cc6600",
        "#0099ff",
        "#cc0066",
        "#990000",
        "#000000",
        "#003366",
        "#006666",
        "#000066",
        "#660066",
        "#336600",
    ]


screen gui_swatches():

    default color = (None, None)

    hbox:

        frame:
            style "empty"
            background "#000000"
            ypadding 13

            has vbox

            for i in DARK_COLORS:

                button:
                    style "empty"

                    selected_background "#fff"

                    xpadding 3
                    ypadding 3
                    xmargin 15
                    ymargin 2

                    xysize (100, 40)

                    action SetScreenVariable("color", (False, i))

                    idle_child Solid(i)
                    hover_child Solid(Color(i).tint(.6))

        frame:
            style "empty"
            background "#ffffff"
            ypadding 13

            has vbox

            for i in DARK_COLORS:

                button:
                    style "empty"

                    selected_background "#fff"

                    xpadding 3
                    ypadding 3
                    xmargin 15
                    ymargin 2

                    xysize (100, 40)

                    action SetScreenVariable("color", (False, i))

                    idle_child Solid(i)
                    hover_child Solid(Color(i).tint(.8))

        frame:
            style "empty"
            background "#d0ffff"
            ypadding 13

            has vbox

            for i in LIGHT_COLORS:

                button:
                    style "empty"

                    selected_background "#fff"

                    xpadding 3
                    ypadding 3
                    xmargin 15
                    ymargin 2

                    xysize (100, 40)

                    action SetScreenVariable("color", (False, i))

                    idle_child Solid(i)
                    hover_child Solid(Color(i).tint(.8))





label new_gui_project:

    call screen gui_swatches

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
