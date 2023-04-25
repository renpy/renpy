# Copyright 2004-2023 Tom Rothamel <pytom@bishoujo.us>
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
    from math import ceil

    if persistent.show_edit_funcs is None:
        persistent.show_edit_funcs = True

    if persistent.windows_console is None:
        persistent.windows_console = False

    def scan_translations(piglatin=True):

        languages = renpy.known_languages()

        if not languages:
            return None

        languages.remove("piglatin")

        rv = [(i, renpy.translate_string("{#language name and font}", i)) for i in languages ]
        rv.sort(key=lambda a : renpy.filter_text_tags(a[1], allow=[]).lower())

        rv.insert(0, (None, "English"))

        if piglatin:
            rv.append(("piglatin", "Igpay Atinlay"))

        bound = ceil(len(rv)/3.)
        return (rv[:bound], rv[bound:2*bound], rv[2*bound:])

    show_legacy = os.path.exists(os.path.join(config.renpy_base, "templates", "english", "game", "script.rpy"))

    class RestartAtPreferences(Action):
        def __call__(self):
            renpy.session["launcher_start_label"] = "preferences"
            renpy.utter_restart()

default persistent.legacy = False
default persistent.force_new_tutorial = False
default persistent.sponsor_message = True
default persistent.daily_update_check = True
default persistent.daily_update_check_once = False

# Keep the default update check from triggering until tomorrow.
default persistent.last_update_check = datetime.date.today()

init python:
    if not persistent.daily_update_check_once:
        persistent.daily_update_check_once = True
        persistent.daily_update_check = True


default preference_tab = "general"

screen preferences():

    default translations = scan_translations()

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

                    add HALF_SPACER

                    textbutton _("General") action SetVariable("preference_tab", "general") style "l_list"
                    textbutton _("Options") action SetVariable("preference_tab", "options") style "l_list"
                    textbutton _("Theme") action SetVariable("preference_tab", "theme") style "l_list"
                    textbutton _("Install Libraries") action SetVariable("preference_tab", "install") style "l_list"
                    textbutton _("Actions") action SetVariable("preference_tab", "actions") style "l_list"


                if preference_tab == "general":

                    frame:
                        style "l_indent"
                        xmaximum TWOTHIRDS
                        xfill True

                        has vbox

                        # Projects directory selection.
                        add SEPARATOR2


                        frame:
                            style "l_indent"

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
                            has vbox

                            text _("Language:")

                            add HALF_SPACER

                            hbox:
                                for tran in translations:
                                    vbox:
                                        for tlid, tlname in tran:
                                            textbutton tlname:
                                                xmaximum (TWOTHIRDS//3)
                                                action [Language(tlid), project.SelectTutorial(True)]
                                                style "l_list"

                elif preference_tab == "options":

                    frame:
                        style "l_indent"
                        xmaximum TWOTHIRDS
                        xfill True

                        has vbox
                        add SEPARATOR2

                        frame:
                            style "l_indent"
                            has vbox

                            text _("Navigation Options:")

                            add HALF_SPACER

                            textbutton _("Include private names") style "l_checkbox" action ToggleField(persistent, "navigate_private")
                            textbutton _("Include library names") style "l_checkbox" action ToggleField(persistent, "navigate_library")

                        add SPACER
                        add SEPARATOR2

                        frame:
                            style "l_indent"
                            has vbox

                            text _("Launcher Options:")

                            add HALF_SPACER

                            textbutton _("Show edit file section") style "l_checkbox" action ToggleField(persistent, "show_edit_funcs")
                            textbutton _("Large fonts") style "l_checkbox" action [ ToggleField(persistent, "large_print"), renpy.utter_restart ]

                            if renpy.windows:
                                textbutton _("Console output") style "l_checkbox" action ToggleField(persistent, "windows_console")

                            textbutton _("Sponsor message") style "l_checkbox" action ToggleField(persistent, "sponsor_message")

                            if ability.can_update:
                                textbutton _("Daily check for update") style "l_checkbox" action [ToggleField(persistent, "daily_update_check"), SetField(persistent, "last_update_check", None)] selected persistent.daily_update_check


                elif preference_tab == "theme":

                    frame:
                        style "l_indent"
                        xmaximum TWOTHIRDS
                        xfill True

                        has vbox

                        # Projects directory selection.
                        add SEPARATOR2

                        frame:
                            style "l_indent"
                            has vbox

                            text _("Launcher Theme:")

                            add HALF_SPACER

                            textbutton _("Default theme") style "l_checkbox" action [SetField(persistent, "theme", None), RestartAtPreferences() ]
                            textbutton _("Dark theme") style "l_checkbox" action [SetField(persistent, "theme", "dark"), RestartAtPreferences()]
                            textbutton _("Custom theme") style "l_checkbox" action [SetField(persistent, "theme", "custom"), RestartAtPreferences()]

                            add SPACER

                            text _("Information about creating a custom theme can be found {a=https://www.renpy.org/doc/html/skins.html}in the Ren'Py Documentation{/a}.")

                elif preference_tab == "install":

                    frame:
                        style "l_indent"
                        xmaximum TWOTHIRDS
                        xfill True

                        has vbox

                        add SEPARATOR2

                        frame:
                            style "l_indent"
                            has vbox

                            text _("Install Libraries:")

                            add HALF_SPACER

                            use install_preferences


                elif preference_tab == "actions":

                    frame:
                        style "l_indent"
                        xmaximum TWOTHIRDS
                        xfill True

                        has vbox

                        add SEPARATOR2

                        frame:
                            style "l_indent"
                            has vbox

                            text _("Actions:")

                            add HALF_SPACER

                            textbutton _("Open launcher project") style "l_nonbox" action [ project.Select("launcher"), Jump("front_page") ]
                            textbutton _("Reset window size") style "l_nonbox" action Preference("display", 1.0)
                            textbutton _("Clean temporary files") style "l_nonbox" action Jump("clean_tmp")


    textbutton _("Return") action Jump("front_page") style "l_left_button"

label clean_tmp:
    python hide:
        installer.processing(_("Cleaning temporary files..."))
        installer._clean("renpy:tmp", 0)
        time.sleep(0.5)

    jump preferences

label projects_directory_preference:
    call choose_projects_directory
    jump preferences


label preferences:
    call screen preferences
    jump preferences


screen choose_language():
    default local_lang = _preferences.language
    default chosen_lang = _preferences.language
    default translations = scan_translations(piglatin=False)

    add BACKGROUND

    vbox:
        xalign .5
        yalign .5

        fixed:
            ysize 0

            text renpy.translate_string(_("{#in language font}Welcome! Please choose a language"), local_lang):
                xalign .5
                yanchor 1.0
                ypos 1.0

                style "l_label_text"

                size 36
                textalign .5
                layout "subtitle"

        add SPACER
        add SPACER

        hbox:
            xalign .5
            for tran in translations:
                vbox:
                    for tlid, tlname in tran:
                        textbutton tlname:
                            xmaximum (TWOTHIRDS//3)
                            action [ SetScreenVariable("chosen_lang", tlid), Language(tlid), project.SelectTutorial(True), Return() ]
                            hovered SetScreenVariable("local_lang", tlid)
                            unhovered SetScreenVariable("local_lang", chosen_lang)
                            style "l_list"
                            text_xalign .5

        add SPACER
        add SPACER

        $ lang_name = renpy.translate_string("{#language name and font}", local_lang)

        fixed:
            ysize 0

            textbutton renpy.translate_string(_("{#in language font}Start using Ren'Py in [lang_name]"), local_lang):
                xalign .5
                action [Language(chosen_lang), project.SelectTutorial(True), Return()]
                style "l_default"
                text_style "l_default"

                text_size 30
                text_textalign .5
                text_layout "subtitle"


label choose_language:
    call screen choose_language
    return


translate None strings:
    # game/new_project.rpy:77
    old "{#language name and font}"
    new "English"
