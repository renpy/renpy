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

    if persistent.translate_language is None:
        persistent.translate_language = "english"

    if persistent.generate_empty_strings is None:
        persistent.generate_empty_strings = True

label translate:

    python:

        language = interface.input(_("Create or Update Translations"), _("Please enter the name of the language for which you want to create or update translations."), filename=True, default=persistent.translate_language, cancel=Jump("front_page"))

        language = language.strip()

        if not language:
            interface.error(_("The language name can not be the empty string."))

        persistent.translate_language = language

        args = [ "translate", language ]

        if language == "rot13":
            args.append("--rot13")
        elif persistent.generate_empty_strings:
            args.append("--empty")

        interface.processing(_("Ren'Py is generating translations...."))
        project.current.launch(args, wait=True)
        project.current.update_dump(force=True)

        interface.info(_("Ren'Py has finished generating [language] translations."))

    jump front_page

screen extract_dialogue:

    frame:
        style_group "l"
        style "l_root"

        window:

            has vbox

            label _("Extract Dialogue: [project.current.name!q]")

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
