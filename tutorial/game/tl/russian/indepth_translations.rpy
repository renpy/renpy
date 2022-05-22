
# game/indepth_translations.rpy:12
translate russian translations_c4ef181f:

    # e "Ren'Py includes support for translating your game into languages other than the one it was originally written in."
    e "Ren'Py поддерживает перевод игр на другой язык."

# game/indepth_translations.rpy:14
translate russian translations_20b9a600:

    # e "This includes the translation of every string in the game, including dialogue, menu choice, and interface strings, and of images and other assets."
    e "Это относится к переводу каждой строки в игре, включая диалоги, выборы в меню, строки интерфейса, плюс изображения и некоторые другие вещи."

# game/indepth_translations.rpy:16
translate russian translations_07c7643c:

    # e "While Ren'Py can find dialogue and menu choice strings for you, you'll have to indicate which other strings need translation."
    e "В то время как Ren'Py может обнаружить диалоги и выборы, остальные строки вам нужно обозначить, как доcтупные для перевода."

# game/indepth_translations.rpy:20
translate russian translations_317d73e5:

    # e "For example, here is how we define a character and her name."
    e "Например, так мы обычно определяем персонажа и её имя."

# game/indepth_translations.rpy:24
translate russian translations_ab0f3c94:

    # e "To mark Lucy's name as translatable, we surround it by parentheses preceded by a single underscore."
    e "Чтобы отметить имя Люси как доступное для перевода, мы добавляем к нему слева скобку и подчёркивание."

# game/indepth_translations.rpy:26
translate russian translations_c81acfc7:

    # e "Notice how we don't translate the reddish color that we use for her name. That stays the same for all languages."
    e "Заметьте, нам не нужно переводить красный цвет её имени. Он останется одинаковым для всех языков."

# game/indepth_translations.rpy:33
translate russian translations_8272a0ef:

    # e "Once that's done, you can generate the translation files. That's done by going to the launcher, and clicking translate."
    e "Когда всё будет готово, вы можете создать файлы переводов. Это можно сделать в лаунчере, нажав на 'создать переводы'."

# game/indepth_translations.rpy:35
translate russian translations_fde34832:

    # e "After you type in the name of the language you'll be translating to, choosing Generate Translations will scan your game and create translation files."
    e "После того, как вы напишите имя языка, на который вы будете переводить, нажатие на 'Создать переводы' просканирует вашу игру и создаст необходимые файлы."

# game/indepth_translations.rpy:37
translate russian translations_e2ebb4af:

    # e "The files will be generated in game/tl/language, where language is the name of the language you typed in."
    e "Файлы будут сгенерированы в папке game/tl/имя языка, где именем языка будет то, которое вы написали."

# game/indepth_translations.rpy:39
translate russian translations_28ec40b9:

    # e "You'll need to edit those files to include translations for everything in your game."
    e "Вам потребуется отредактировать эти файлы, чтобы внедрить перевод в вашу игру."

# game/indepth_translations.rpy:41
translate russian translations_f6d3fd2d:

    # e "If you want to localize image files, you can also place them in game/tl/language."
    e "Если вы хотите перевести и файлы изображений, вы также можете положить их в game/tl/имя языка."

# game/indepth_translations.rpy:48
translate russian translations_71bf6e72:

    # e "If the default fonts used by the game do not support the language you are translating to, you will have to change them."
    e "Если стандартные шрифты игры не поддерживают язык перевода, вам потребуется их изменить."

# game/indepth_translations.rpy:50
translate russian translations_82c9748e:

    # e "The translate python statement can be used to set the values of gui variables to change the font."
    e "Оператор translate python может использоваться для изменения переменных, необходимых для смены шрифта."

# game/indepth_translations.rpy:52
translate russian translations_a0042025:

    # e "The translate style statement sets style properties more directly."
    e "Параметр translate style же устанавливает стилевые настройки более прямым путём."

# game/indepth_translations.rpy:54
translate russian translations_b10990ce:

    # e "If you need to add new files, such as font files, you can place them into the game/tl/language directory where Ren'Py will find them."
    e "Если вам нужно добавить новые файлы, например, шрифты, вы можете положить их в папку game/tl/имя языка, где Ren'Py их найдёт."

# game/indepth_translations.rpy:58
translate russian translations_01fcacc2:

    # e "Finally, you'll have to add support for picking the language of the game. That usually goes into the preferences screen, found in screens.rpy."
    e "И самое главное, вам надо будет добавить поддержку выбора языка в игру. Чаще всего, она устанавливается на экран настроек в screens.rpy."

# game/indepth_translations.rpy:60
translate russian translations_a91befcc:

    # e "Here's an excerpt of the preferences screen of this tutorial. The Language action tells Ren'Py to change the language. It takes a string giving a language name, or None."
    e "Вот фрагмент экрана настроек для этого обучения. Действие Language говорит Ren'Py изменить язык. В строке может быть выражение с названием языка или просто None."

# game/indepth_translations.rpy:62
translate russian translations_9b7d6401:

    # e "The None language is special, as it's the default language that the visual novel was written in. Since this tutorial was written in English, Language(None) selects English."
    e "Язык None — особенный. Это стандартный язык, на котором пишется визуальная новелла. Учитывая, что оригинал обучения был написан на английском языке, Language(None) выберет языком английский."

