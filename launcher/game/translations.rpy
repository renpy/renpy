# Copyright 2004-2019 Tom Rothamel <pytom@bishoujo.us>
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

    import re
    import tempfile

    if persistent.translate_language is None:
        persistent.translate_language = "english"

    if persistent.generate_empty_strings is None:
        persistent.generate_empty_strings = True

    if persistent.replace_translations is None:
        persistent.replace_translations = False

    if persistent.reverse_languages is None:
        persistent.reverse_languages = False

    def CheckLanguage():
        return SensitiveIf(re.match(r'^\w+$', persistent.translate_language))


    strings_json = None

    def get_strings_json():

        global strings_json

        if strings_json is not None:
            return strings_json

        try:
            tempdir = os.path.join(config.basedir, "tmp")

            try:
                os.makedirs(os.path.join(config.basedir, "tmp"))
            except:
                pass

            write_test = os.path.join(tempdir, "writetest.txt")

            if os.path.exists(write_test):
                os.unlink(write_test)

            with open(write_test, "w"):
                pass

            os.unlink(write_test)

        except:
            tempdir = tempfile.mkdtemp()

        strings_json = os.path.join(tempdir, "strings.json")
        return strings_json



screen translate:

    default tt = Tooltip(None)
    $ state = AndroidState()

    frame:
        style_group "l"
        style "l_root"

        window:

            has vbox

            label _("Translations: [project.current.display_name!q]")

            add HALF_SPACER

            hbox:

                # Left side.
                frame:
                    style "l_indent"
                    xmaximum ONEHALF
                    xfill True

                    has vbox

                    frame:
                        style "l_indent"
                        has vbox

                        text _("Language:")

                        add HALF_SPACER

                        frame style "l_indent":

                            input style "l_default":
                                value FieldInputValue(persistent, "translate_language")
                                size 24
                                color INPUT_COLOR
                                allow interface.TRANSLATE_LETTERS
                # Left side.
                frame:
                    style "l_indent"
                    xmaximum ONEHALF
                    xfill True

                    has vbox

                    frame:
                        style "l_indent"
                        has vbox

                        text _("The language to work with. This should only contain lower-case ASCII characters and underscores.")

            add SPACER

            hbox:

                frame:
                    style "l_indent"
                    xmaximum ONEHALF
                    xfill True

                    has vbox

                    add SEPARATOR2
                    add HALF_SPACER

                    frame:
                        style "l_indent"
                        has vbox

                        textbutton _("Generate Translations"):
                            text_size 24
                            action [ CheckLanguage(), Jump("generate_translations") ]

                        add HALF_SPACER

                        textbutton _("Generate empty strings for translations") style "l_checkbox" action ToggleField(persistent, "generate_empty_strings")


                frame:
                    style "l_indent"
                    xmaximum ONEHALF
                    xfill True

                    has vbox

                    add SEPARATOR2

                    frame:
                        style "l_indent"
                        top_padding 10

                        has vbox

                        text _("Generates or updates translation files. The files will be placed in game/tl/[persistent.translate_language!q].")

            add SPACER

            hbox:

                frame:
                    style "l_indent"
                    xmaximum ONEHALF
                    xfill True

                    has vbox

                    add SEPARATOR2
                    add HALF_SPACER

                    frame:
                        style "l_indent"
                        has vbox

                        textbutton _("Extract String Translations"):
                            action [ CheckLanguage(), Jump("extract_strings") ]
                        textbutton _("Merge String Translations"):
                            action [ CheckLanguage(), Jump("merge_strings") ]

                        add HALF_SPACER

                        textbutton _("Replace existing translations") style "l_checkbox" action ToggleField(persistent, "replace_translations")
                        textbutton _("Reverse languages") style "l_checkbox" action ToggleField(persistent, "reverse_languages")

                        add HALF_SPACER

                        textbutton _("Update Default Interface Translations"):
                            action [ Jump("update_renpy_strings") ]



                frame:
                    style "l_indent"
                    xmaximum ONEHALF
                    xfill True

                    has vbox

                    add SEPARATOR2

                    frame:
                        style "l_indent"
                        top_padding 10

                        has vbox

                        text _("The extract command allows you to extract string translations from an existing project into a temporary file.\n\nThe merge command merges extracted translations into another project.")

    textbutton _("Return") action Jump("front_page") style "l_left_button"


label translate:
    call screen translate

# Common code to create the new translations in the current game.
label generate_translations_common:

    python:

        language = persistent.translate_language

        args = [ "translate", language ]

        if language == "rot13":
            args.append("--rot13")
        elif language == "piglatin":
            args.append("--piglatin")
        elif persistent.generate_empty_strings:
            args.append("--empty")

        interface.processing(_("Ren'Py is generating translations...."))
        project.current.launch(args, wait=True)
        project.current.update_dump(force=True)

    return

# Code to generate translations by themselves.
label generate_translations:
    call generate_translations_common

    python:
        interface.info(_("Ren'Py has finished generating [language] translations."))

    jump front_page


label extract_strings:

    python:

        language = persistent.translate_language

        args = [ "extract_strings", language,  get_strings_json() ]

        interface.processing(_("Ren'Py is extracting string translations..."))
        project.current.launch(args, wait=True)

        interface.info(_("Ren'Py has finished extracting [language] string translations."))

    jump front_page

label merge_strings:

    call generate_translations_common

    python:

        language = persistent.translate_language

        args = [ "merge_strings", language,  get_strings_json() ]

        if persistent.replace_translations:
            args.append("--replace")

        if persistent.reverse_languages:
            args.append("--reverse")

        interface.processing(_("Ren'Py is merging string translations..."))
        project.current.launch(args, wait=True)

        interface.info(_("Ren'Py has finished merging [language] string translations."))

    jump front_page



label update_renpy_strings_common:
    python:

        language = _preferences.language

        interface.processing(_("Updating default interface translations..."))

        renpy.translation.extract.extract_strings_core(language, get_strings_json())

        args = [ "translate", "None", "--common-only", "--strings-only", "--max-priority", "399", "--no-todo" ]
        project.current.launch(args, wait=True)

        args = [ "merge_strings", "None",  get_strings_json() ]
        project.current.launch(args, wait=True)

    return


label update_renpy_strings:
    call update_renpy_strings_common
    jump front_page



screen extract_dialogue:

    frame:
        style_group "l"
        style "l_root"

        window:

            has vbox

            label _("Extract Dialogue: [project.current.display_name!q]")

            add HALF_SPACER

            frame:
                style "l_indent"
                xfill True

                has vbox

                add SEPARATOR2

                frame:
                    style "l_indent"
                    has vbox

                    text _("Format:")

                    add HALF_SPACER

                    frame:
                        style "l_indent"
                        has vbox

                        textbutton _("Tab-delimited Spreadsheet (dialogue.tab)") action SetField(persistent, "dialogue_format", "tab")
                        textbutton _("Dialogue Text Only (dialogue.txt)") action SetField(persistent, "dialogue_format", "txt")

                add SPACER
                add SEPARATOR2

                frame:
                    style "l_indent"
                    has vbox

                    text _("Options:")

                    add HALF_SPACER

                    textbutton _("Strip text tags from the dialogue.") action ToggleField(persistent, "dialogue_notags") style "l_checkbox"
                    textbutton _("Escape quotes and other special characters.") action ToggleField(persistent, "dialogue_escape") style "l_checkbox"
                    textbutton _("Extract all translatable strings, not just dialogue.") action ToggleField(persistent, "dialogue_strings") style "l_checkbox"


    textbutton _("Cancel") action Jump("front_page") style "l_left_button"
    textbutton _("Continue") action Jump("start_extract_dialogue") style "l_right_button"

label extract_dialogue:

    call screen extract_dialogue

label start_extract_dialogue:

    python:

        args = [ "dialogue" ]

        if persistent.dialogue_format == "txt":
            args.append("--text")

        if persistent.dialogue_strings:
            args.append("--strings")

        if persistent.dialogue_notags:
            args.append("--notags")

        if persistent.dialogue_escape:
            args.append("--escape")

        interface.processing(_("Ren'Py is extracting dialogue...."))
        project.current.launch(args, wait=True)
        project.current.update_dump(force=True)

        interface.info(_("Ren'Py has finished extracting dialogue. The extracted dialogue can be found in dialogue.[persistent.dialogue_format] in the base directory."))

    jump front_page
