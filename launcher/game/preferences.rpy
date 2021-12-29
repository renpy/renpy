# Copyright 2004-2021 Tom Rothamel <pytom@bishoujo.us>
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
    if persistent.show_edit_funcs is None:
        persistent.show_edit_funcs = True

    if persistent.windows_console is None:
        persistent.windows_console = False

    def scan_translations():

        languages = renpy.known_languages()

        if not languages:
            return None

        rv = [ ( "English", None) ]

        for i in languages:
            rv.append((i.title(), i))

        for i in (("Schinese", "schinese"), ("Tchinese", "tchinese")):
            if i in rv:
                rv.remove(i)
                rv.append(({"schinese": "Simplified Chinese", "tchinese": "Traditional Chinese"}.get(i[1]), i[1]))

        rv.sort()

        if ("Piglatin", "piglatin") in rv:
            rv.remove(("Piglatin", "piglatin"))
            rv.append(("Pig Latin", "piglatin"))

        return rv

    show_legacy = os.path.exists(os.path.join(config.renpy_base, "templates", "english", "game", "script.rpy"))

    class RestartAtPreferences(Action):
        def __call__(self):
            renpy.session["launcher_start_label"] = "preferences"
            renpy.utter_restart()

default persistent.legacy = False
default persistent.force_new_tutorial = False
default persistent.sponsor_message = True
default persistent.daily_update_check = False

screen preferences:

    $ translations = scan_translations()

    frame:
        style_group "l"
        style "l_root"
        alt "Preferences"

        window:

            has vbox

            label _("Launcher Preferences")

            add HALF_SPACER

            hbox:

                frame:
                    style "l_indent"
                    xmaximum ONETHIRD
                    xfill True

                    has vbox

                    # Projects directory selection.
                    add SEPARATOR2

                    frame:
                        style "l_indent"
                        yminimum 75
                        has vbox

                        text _("Projects Directory:")

                        add HALF_SPACER


                        frame style "l_indent":
                            if persistent.projects_directory:
                                textbutton _("[persistent.projects_directory!q]"):
                                    action Jump("projects_directory_preference")
                                    alt _("Projects directory: [text]")
                            else:
                                textbutton _("Not Set"):
                                    action Jump("projects_directory_preference")
                                    alt _("Projects directory: [text]")


                    add SPACER

                    # Text editor selection.
                    add SEPARATOR2

                    frame:
                        style "l_indent"
                        yminimum 75
                        has vbox

                        text _("Text Editor:")

                        add HALF_SPACER

                        frame style "l_indent":
                            if persistent.editor:
                                textbutton persistent.editor action Jump("editor_preference") alt _("Text editor: [text]")
                            else:
                                textbutton _("Not Set") action Jump("editor_preference") alt _("Text editor: [text]")

                    add SPACER

                    add SEPARATOR2

                    frame:
                        style "l_indent"
                        yminimum 75
                        has vbox

                        text _("Actions:")

                        add HALF_SPACER

                        textbutton _("Install libraries") style "l_nonbox" action Jump("install")
                        textbutton _("Open launcher project") style "l_nonbox" action [ project.Select("launcher"), Jump("front_page") ]
                        textbutton _("Reset window size") style "l_nonbox" action Preference("display", 1.0)


                frame:
                    style "l_indent"
                    xmaximum ONETHIRD
                    xfill True

                    has vbox
                    add SEPARATOR2

                    frame:
                        style "l_indent"
                        yminimum 75
                        has vbox

                        text _("Navigation Options:")

                        add HALF_SPACER

                        textbutton _("Include private names") style "l_checkbox" action ToggleField(persistent, "navigate_private")
                        textbutton _("Include library names") style "l_checkbox" action ToggleField(persistent, "navigate_library")

                    add SPACER
                    add SEPARATOR2

                    frame:
                        style "l_indent"
                        yminimum 75
                        has vbox

                        text _("Launcher Options:")

                        add HALF_SPACER

                        textbutton _("Show edit file section") style "l_checkbox" action ToggleField(persistent, "show_edit_funcs")
                        textbutton _("Large fonts") style "l_checkbox" action [ ToggleField(persistent, "large_print"), renpy.utter_restart ]

                        if renpy.windows:
                            textbutton _("Console output") style "l_checkbox" action ToggleField(persistent, "windows_console")

                        if project.manager.get("oldtutorial"):

                           textbutton _("Force new tutorial") style "l_checkbox" action [ ToggleField(persistent, "force_new_tutorial"), project.SelectTutorial(True) ]

                        if show_legacy:

                            textbutton _("Legacy options") style "l_checkbox" action ToggleField(persistent, "legacy")

                            if persistent.legacy:
                                textbutton _("Show templates") style "l_checkbox" action ToggleField(persistent, "show_templates")

                        textbutton _("Sponsor message") style "l_checkbox" action ToggleField(persistent, "sponsor_message")

                        if ability.can_update:
                            textbutton _("Daily check for update") style "l_checkbox" action [ToggleField(persistent, "daily_update_check"), SetField(persistent, "last_update_check", None)] selected persistent.daily_update_check

                        add HALF_SPACER

                        textbutton _("Default theme") style "l_checkbox" action [SetField(persistent, "theme", None), RestartAtPreferences() ]
                        # textbutton _("Clear theme") style "l_checkbox" action [SetField(persistent, "theme", "clear", None), RestartAtPreferences() ]
                        textbutton _("Dark theme") style "l_checkbox" action [SetField(persistent, "theme", "dark", None), RestartAtPreferences()]
                        textbutton _("Custom theme") style "l_checkbox" action [SetField(persistent, "theme", "custom", None), RestartAtPreferences()]


                if translations:

                    frame:
                        style "l_indent"
                        xmaximum ONETHIRD
                        xfill True

                        has vbox

                        # Text editor selection.
                        add SEPARATOR2

                        frame:
                            style "l_indent"
                            yminimum 75
                            has vbox

                            text _("Language:")

                            add HALF_SPACER

                            viewport:
                                scrollbars "vertical"
                                mousewheel True

                                has vbox

                                # frame style "l_indent":

                                for tlname, tlvalue in translations:
                                    textbutton tlname action [ Language(tlvalue), project.SelectTutorial(True) ] style "l_list"


    textbutton _("Return") action Jump("front_page") style "l_left_button"

label projects_directory_preference:
    call choose_projects_directory
    jump preferences


label preferences:
    call screen preferences
    jump preferences
