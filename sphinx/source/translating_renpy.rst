.. _translating-renpy:

==================
Translating Ren'Py
==================


It is possible to translate Ren'Py itself. A complete translation translates
the GUI, various Ren'Py messages, new projects, and the launcher. This should
cover most gameplay and development scenarios. Right now, not every error
message can be translated.

To create a new translation:

1. Open the Ren'Py launcher.
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
    This file contains comments that are placed into the default GUI.

launcher.rpy
    This file contains strings that are displayed as part of the launcher.

obsolete.rpy
    The file contains strings that are not used by modern Ren'Py.

options.rpy
    This file contains strings that are used to translate the comments in
    the default options.rpy file.

screens.rpy
    This file contains strings that are used by the default gui, and the
    comments in the default screens.rpy file.

script.rpym
    The contents of this file are copied, verbatim, into script.rpy
    when a new project is created.

style.rpy
    This file does not exist by default, but should be created when needed.
    It configures the launcher styles, and the font that is used by a
    generated game.


Changing Fonts
--------------

Ren'Py ships with a default font (DejaVuSans) that covers most western
languages, but other fonts are often needed. A font can be configured by
editing launcher/game/tl/language/style.rpy, and adding::

    init python:
        translate_font("language", "myfont.ttf")

Where "language" is the language in question (for example, "japanese"), and
"myfont.ttf" is the font that should be used (for example, "MTLc3m.ttf").
The font file should be placed in the launcher/game/tl/language directory,
so it can be found by the launcher.


Changing the Launcher Style
---------------------------

The styles used by the launcher can be configured by setting variables
in a ``translate python`` block. The following variables are available. The
names are a bit confusing, as they reflect the English-language translation.

These variables are only available in the launcher.

.. var:: gui.LIGHT_FONT = "Roboto-Light.ttf"

    The path to the font used for normal text in the launcher.

.. var:: gui.REGULAR_FONT = "Roboto-Regular.ttf"

    The path to the font used for heavy-weight text in the launcher.

.. var:: gui.REGULAR_BOLD = False

    If True, heavy-weight text is bolded.

.. var:: gui.FONT_SCALE = 1.0

    A scaling factor that is applied to all text in the launcher.

A ``translate python`` block is used to set these variables. For example, the
following is used to change the fonts in the Arabic translation of
Ren'Py::

    translate arabic python:
        gui.REGULAR_FONT = "DejaVuSans.ttf"
        gui.LIGHT_FONT = "DejaVuSans.ttf"
        gui.FONT_SCALE = .9
        gui.REGULAR_BOLD = True


Functions
---------

The following functions are used to configure translation in the launcher.
They should be called from the ``init python`` block.

.. function:: translate_font(language, font)

    This is used to set a font for `language`. The font is used in the
    launcher, and also used to in games generated in that language. The
    font file should be placed in game/fonts.

    `font`
        A string giving the name of the font file.


.. function:: translate_define(language, define, value, help=None)

    This is used to set a define when generating a game. For example, it can
    be used to change the size of a font.

    `language`
        The language involved.

    `define`
        The name of the define.

    `value`
        A string giving the value the define should be set to. (ie. "10",
        "False", or "'Font.ttf'").

    `comment`
        If not None, a comment that will be generated before the define. The
        comment will only be generated if the define does not exist in
        gui.rpy. There is no need to use "## ", as the comment will be
        added and wrapped automatically.

    For example, the following changes the size of dialogue text::

        translate_define("martian", "gui.text_size", 12)

