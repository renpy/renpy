example translate_font:
    translate japanese python:
        gui.text_font = "MTLc3m.ttf"
        gui.name_text_font = "MTLc3m.ttf"
        gui.interface_text_font = "MTLc3m.ttf"

    translate japanese style default:
        language "japanese-strict"

label translations:

    e "Ren'Py includes support for translating your game into languages other than the one it was originally written in."

    e "This includes the translation of every string in the game, including dialogue, menu choice, and interface strings, and of images and other assets."

    e "While Ren'Py can find dialogue and menu choice strings for you, you'll have to indicate which other strings need translation."

    show example characters

    e "For example, here is how we define a character and her name."

    show example characters showtrans

    e "To mark Lucy's name as translatable, we surround it by parentheses preceded by a single underscore."

    e "Notice how we don't translate the reddish color that we use for her name. That stays the same for all languages."

    hide example

    show launcher translate at launcher_place
    with moveinleft

    e "Once that's done, you can generate the translation files. That's done by going to the launcher, and clicking translate."

    e "After you type in the name of the language you'll be translating to, choosing Generate Translations will scan your game and create translation files."

    e "The files will be generated in game/tl/language, where language is the name of the language you typed in."

    e "You'll need to edit those files to include translations for everything in your game."

    e "If you want to localize image files, you can also place them in game/tl/language."

    hide launcher
    with moveoutleft

    show example translate_font large

    e "If the default fonts used by the game do not support the language you are translating to, you will have to change them."

    e "The translate python statement can be used to set the values of gui variables to change the font."

    e "The translate style statement sets style properties more directly."

    e "If you need to add new files, such as font files, you can place them into the game/tl/language directory where Ren'Py will find them."

    show example language_picker large

    e "Finally, you'll have to add support for picking the language of the game. That usually goes into the preferences screen, found in screens.rpy."

    e "Here's an excerpt of the preferences screen of this tutorial. The Language action tells Ren'Py to change the language. It takes a string giving a language name, or None."

    e "The None language is special, as it's the default language that the visual novel was written in. Since this tutorial was written in English, Language(None) selects English."

    return
