==================
Translating Ren'Py
==================


It is possible to translate Ren'Py itself. A complete translation translates
the GUI, various Ren'Py messages, new projects, and the launcher. This should
cover most gameplay and development scenarios. Right now, not every error
message can be translated.

To create a new translation:

1. Open the Ren'PY launcher.
2. On the preferences page, choose "Open launcher project".
3. Choose "Generate Translations."
4. Enter the name of the language to translate to. This should consist of
   lower-case ASCII characters and underscores, so "japanese", "russian",
   or "ancient_klingon" are all valid language names.
5. Choose "Generate Translations."

The same procedure can be used to update a language translation. To access
the created translation, return to the preferences, then choose the newly
created language. Note that by default, the translation will be a copy of
the English translation.

Translation Files
-----------------

The translation files live in launcher/game/tl/`language`/. With the
exception of script.rpy, all files consist of string translations that
can be translated using the :ref:`string translation <string-translations>`
syntax. Some strings might begin with "## ". These are comments that
are translated, wrapped, and included in the options.rpy and gui.rpy
files.

The translation files are:

common.rpy
    This file contains interface messages (strings) that Ren'Py may present to the
    player.

developer.rpy
    This file contains strings that are only of interest to creators,
    and not players.

error.rpy
    This file contains strings that are displayed to the developer or player
    when Ren'Py has a problem.

gui.rpy
    This file contains comments that are placed into the default GUI code.

launcher.rpy
    This file contains strings that are displayed as part of the launcher.

obsolete.rpy
    The file contains strings that are not used by modern Ren'Py code.

options.rpy
    This file contains strings that are used to translate the comments in
    the default options.rpy file.

screens.rpy
    This file contains strings that are used by the default gui, and the
    comments in the default screens.rpy file.

script.rpym
    The contents of this file are copied, verbatim, into script.rpy
    when a new project is created.


Non-Western Languages
---------------------

Ren'Py ships with a default font that covers most western languages, but not
ideographic languages like Chinese and Japanese. It's necessary to change
the default font when translating into an ideographic language.
