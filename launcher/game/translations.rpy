init python:

    if persistent.translate_language is None:
        persistent.translate_language = "english"

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
        else:
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
