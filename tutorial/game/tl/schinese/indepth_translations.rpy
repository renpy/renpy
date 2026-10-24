
# game/indepth_translations.rpy:12
translate schinese translations_c4ef181f:

    # e "Ren'Py includes support for translating your game into languages other than the one it was originally written in."
    e "Ren'Py 支持把游戏翻译成最初编写语言以外的其他语言。"

# game/indepth_translations.rpy:14
translate schinese translations_20b9a600:

    # e "This includes the translation of every string in the game, including dialogue, menu choice, and interface strings, and of images and other assets."
    e "这包括游戏中的所有字符串（对话、菜单选项和界面文字），以及图像和其他资源的本地化。"

# game/indepth_translations.rpy:16
translate schinese translations_07c7643c:

    # e "While Ren'Py can find dialogue and menu choice strings for you, you'll have to indicate which other strings need translation."
    e "Ren'Py 可以自动找出对话和菜单选项字符串，但其他需要翻译的字符串必须由你标记。"

# game/indepth_translations.rpy:20
translate schinese translations_317d73e5:

    # e "For example, here is how we define a character and her name."
    e "例如，下面这样定义一个角色和她的名字。"

# game/indepth_translations.rpy:24
translate schinese translations_ab0f3c94:

    # e "To mark Lucy's name as translatable, we surround it by parentheses preceded by a single underscore."
    e "要把 Lucy 的名字标记为可翻译，只需在它外面加上由单个下划线引出的括号。"

# game/indepth_translations.rpy:26
translate schinese translations_c81acfc7:

    # e "Notice how we don't translate the reddish color that we use for her name. That stays the same for all languages."
    e "注意，我们没有翻译用于她名字的红色。这个颜色在所有语言中都保持不变。"

# game/indepth_translations.rpy:33
translate schinese translations_8272a0ef:

    # e "Once that's done, you can generate the translation files. That's done by going to the launcher, and clicking translate."
    e "完成后，就可以生成翻译文件。打开启动器并点击“翻译”即可。"

# game/indepth_translations.rpy:35
translate schinese translations_fde34832:

    # e "After you type in the name of the language you'll be translating to, choosing Generate Translations will scan your game and create translation files."
    e "输入目标语言名称后，选择“生成翻译”就会扫描游戏并创建翻译文件。"

# game/indepth_translations.rpy:37
translate schinese translations_e2ebb4af:

    # e "The files will be generated in game/tl/language, where language is the name of the language you typed in."
    e "文件会生成在 game/tl/language 目录中，其中 language 是你输入的语言名称。"

# game/indepth_translations.rpy:39
translate schinese translations_28ec40b9:

    # e "You'll need to edit those files to include translations for everything in your game."
    e "你需要编辑这些文件，为游戏中的所有内容提供翻译。"

# game/indepth_translations.rpy:41
translate schinese translations_f6d3fd2d:

    # e "If you want to localize image files, you can also place them in game/tl/language."
    e "如果要本地化图像文件，也可以把它们放在 game/tl/language 中。"

# game/indepth_translations.rpy:48
translate schinese translations_71bf6e72:

    # e "If the default fonts used by the game do not support the language you are translating to, you will have to change them."
    e "如果游戏使用的默认字体不支持目标语言，就必须更换字体。"

# game/indepth_translations.rpy:50
translate schinese translations_82c9748e:

    # e "The translate python statement can be used to set the values of gui variables to change the font."
    e "可以使用 translate python 语句设置 gui 变量的值，从而更换字体。"

# game/indepth_translations.rpy:52
translate schinese translations_a0042025:

    # e "The translate style statement sets style properties more directly."
    e "translate style 语句可以更直接地设置样式属性。"

# game/indepth_translations.rpy:54
translate schinese translations_b10990ce:

    # e "If you need to add new files, such as font files, you can place them into the game/tl/language directory where Ren'Py will find them."
    e "如果需要添加字体文件等新文件，可以把它们放入 game/tl/language 目录，Ren'Py 会在那里找到它们。"

# game/indepth_translations.rpy:58
translate schinese translations_01fcacc2:

    # e "Finally, you'll have to add support for picking the language of the game. That usually goes into the preferences screen, found in screens.rpy."
    e "最后，还需要加入选择游戏语言的功能。通常可以在 screens.rpy 的 preferences 屏幕中完成。"

# game/indepth_translations.rpy:60
translate schinese translations_a91befcc:

    # e "Here's an excerpt of the preferences screen of this tutorial. The Language action tells Ren'Py to change the language. It takes a string giving a language name, or None."
    e "这是本教程 preferences 屏幕的一段代码。Language 动作会告诉 Ren'Py 切换语言，它接收表示语言名称的字符串，或 None。"

# game/indepth_translations.rpy:62
translate schinese translations_9b7d6401:

    # e "The None language is special, as it's the default language that the visual novel was written in. Since this tutorial was written in English, Language(None) selects English."
    e "None 语言比较特殊，它表示视觉小说编写时使用的默认语言。本教程以英语编写，因此 Language(None) 会选择英语。"
