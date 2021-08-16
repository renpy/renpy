
# game/indepth_translations.rpy:12
translate schinese translations_c4ef181f:

    # e "Ren'Py includes support for translating your game into languages other than the one it was originally written in."
    e "Ren'Py支持将游戏翻译成不同于最初编写的语言。"

# game/indepth_translations.rpy:14
translate schinese translations_20b9a600:

    # e "This includes the translation of every string in the game, including dialogue, menu choice, and interface strings, and of images and other assets."
    e "这包括对游戏中的每个字符串的翻译，包括对话、菜单选项和界面字符串，以及对图像和其他资源的翻译。"

# game/indepth_translations.rpy:16
translate schinese translations_07c7643c:

    # e "While Ren'Py can find dialogue and menu choice strings for you, you'll have to indicate which other strings need translation."
    e "Ren'Py可以帮你找到对话和菜单选项的字符串，但是其他需要翻译的字符串要你来指出。"

# game/indepth_translations.rpy:20
translate schinese translations_317d73e5:

    # e "For example, here is how we define a character and her name."
    e "例如，我们如何定义一个角色和她的名字。"

# game/indepth_translations.rpy:24
translate schinese translations_ab0f3c94:

    # e "To mark Lucy's name as translatable, we surround it by parentheses preceded by a single underscore."
    e "为了将Lucy的名字标记为可翻译，我们在它周围加上下划线。"

# game/indepth_translations.rpy:26
translate schinese translations_c81acfc7:

    # e "Notice how we don't translate the reddish color that we use for her name. That stays the same for all languages."
    e "注意我们没有翻译她名字的红色。在所有语言都是一样的。"

# game/indepth_translations.rpy:33
translate schinese translations_8272a0ef:

    # e "Once that's done, you can generate the translation files. That's done by going to the launcher, and clicking translate."
    e "完成后，就可以生成翻译文件。打开启动器，点击“生成翻译文件”。"

# game/indepth_translations.rpy:35
translate schinese translations_fde34832:

    # e "After you type in the name of the language you'll be translating to, choosing Generate Translations will scan your game and create translation files."
    e "输入要翻译的语言名称后，选择“生成翻译文件”将扫描游戏并创建翻译文件。"

# game/indepth_translations.rpy:37
translate schinese translations_e2ebb4af:

    # e "The files will be generated in game/tl/language, where language is the name of the language you typed in."
    e "文件将在 game/tl/language 目录下生成， language 是您键入的语言的名称。"

# game/indepth_translations.rpy:39
translate schinese translations_28ec40b9:

    # e "You'll need to edit those files to include translations for everything in your game."
    e "你需要编辑这些文件来实现对游戏内容的翻译。"

# game/indepth_translations.rpy:41
translate schinese translations_f6d3fd2d:

    # e "If you want to localize image files, you can also place them in game/tl/language."
    e "如果要本地化图像文件，也可以将它们放在 game/tl/language 中。"

# game/indepth_translations.rpy:48
translate schinese translations_71bf6e72:

    # e "If the default fonts used by the game do not support the language you are translating to, you will have to change them."
    e "如果游戏使用的默认字体不支持您要翻译的语言，您必须换一个。"

# game/indepth_translations.rpy:50
translate schinese translations_82c9748e:

    # e "The translate python statement can be used to set the values of gui variables to change the font."
    e "translate语句可用于设置gui变量的值以更改字体。"

# game/indepth_translations.rpy:52
translate schinese translations_a0042025:

    # e "The translate style statement sets style properties more directly."
    e "translate style语句更直接地设置样式属性。"

# game/indepth_translations.rpy:54
translate schinese translations_b10990ce:

    # e "If you need to add new files, such as font files, you can place them into the game/tl/language directory where Ren'Py will find them."
    e "如果需要添加新文件，例如字体文件，可以将它们放入 game/tl/language 目录，Ren'Py会找到它们。"

# game/indepth_translations.rpy:58
translate schinese translations_01fcacc2:

    # e "Finally, you'll have to add support for picking the language of the game. That usually goes into the preferences screen, found in screens.rpy."
    e "最后，您必须添加多语言支持的选项。一般可以在 screens.rpy 的首选项（preferences）界面找到。"

# game/indepth_translations.rpy:60
translate schinese translations_a91befcc:

    # e "Here's an excerpt of the preferences screen of this tutorial. The Language action tells Ren'Py to change the language. It takes a string giving a language name, or None."
    e "这是本教程的首选项界面的节选。Language动作让Ren'Py改变语言。它需要语言名称的字符串，或者None。"

# game/indepth_translations.rpy:62
translate schinese translations_9b7d6401:

    # e "The None language is special, as it's the default language that the visual novel was written in. Since this tutorial was written in English, Language(None) selects English."
    e "None语言是特殊的，它是视觉小说的默认语言。由于本教程是用英语写的，Language(None)选择英语。"
