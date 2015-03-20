# Copyright 2004-2015 Tom Rothamel <pytom@bishoujo.us>
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

label extract_dialogue:

    python:

        CHOICES = [
            ("tab", "Tab-delimited Spreadsheet (dialogue.tab)"),
            ("txt", "Dialogue Text Only (dialogue.txt)"),
            ]

        format = interface.choice(
            _("What format would you like for the extracted dialogue?"),
            CHOICES,
            persistent.dialogue_format,
            cancel=Jump("front_page"))

        persistent.dialogue_format = format

        args = [ "dialogue" ]

        if format == "txt":
            args.append("--text")

        interface.processing(_("Ren'Py is extracting dialogue...."))
        project.current.launch(args, wait=True)
        project.current.update_dump(force=True)

        interface.info(_("Ren'Py has finished extracting dialogue. The extracted dialogue can be found in dialogue.[format] in the base directory."))


    jump front_page
