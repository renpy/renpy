
# game/indepth_translations.rpy:12
translate tchinese translations_c4ef181f:

    # e "Ren'Py includes support for translating your game into languages other than the one it was originally written in."
    e "Ren'Py 支援將遊戲翻譯成原始語言以外的其他語言。"

# game/indepth_translations.rpy:14
translate tchinese translations_20b9a600:

    # e "This includes the translation of every string in the game, including dialogue, menu choice, and interface strings, and of images and other assets."
    e "這包括遊戲中每個字串的翻譯，例如對話、選單選項和介面字串，也包括圖片及其他資源。"

# game/indepth_translations.rpy:16
translate tchinese translations_07c7643c:

    # e "While Ren'Py can find dialogue and menu choice strings for you, you'll have to indicate which other strings need translation."
    e "Ren'Py 能幫你找出對話和選單選項字串，但其他需要翻譯的字串就必須由你標示。"

# game/indepth_translations.rpy:20
translate tchinese translations_317d73e5:

    # e "For example, here is how we define a character and her name."
    e "例如，以下是定義角色及其姓名的方式。"

# game/indepth_translations.rpy:24
translate tchinese translations_ab0f3c94:

    # e "To mark Lucy's name as translatable, we surround it by parentheses preceded by a single underscore."
    e "若要將 Lucy 的名字標記為可翻譯，只要在它外圍加上前置底線即可。"

# game/indepth_translations.rpy:26
translate tchinese translations_c81acfc7:

    # e "Notice how we don't translate the reddish color that we use for her name. That stays the same for all languages."
    e "注意，我們沒有翻譯她名字使用的紅色；所有語言都會維持相同。"

# game/indepth_translations.rpy:33
translate tchinese translations_8272a0ef:

    # e "Once that's done, you can generate the translation files. That's done by going to the launcher, and clicking translate."
    e "完成後就能產生翻譯檔案。開啟啟動器，點擊「產生翻譯檔案」。"

# game/indepth_translations.rpy:35
translate tchinese translations_fde34832:

    # e "After you type in the name of the language you'll be translating to, choosing Generate Translations will scan your game and create translation files."
    e "輸入目標語言名稱後，選擇「產生翻譯檔案」，就會掃描遊戲並建立翻譯檔案。"

# game/indepth_translations.rpy:37
translate tchinese translations_e2ebb4af:

    # e "The files will be generated in game/tl/language, where language is the name of the language you typed in."
    e "檔案會產生在 game/tl/language 目錄，其中 language 是你輸入的語言名稱。"

# game/indepth_translations.rpy:39
translate tchinese translations_28ec40b9:

    # e "You'll need to edit those files to include translations for everything in your game."
    e "你需要編輯這些檔案，為遊戲中的所有內容加入翻譯。"

# game/indepth_translations.rpy:41
translate tchinese translations_f6d3fd2d:

    # e "If you want to localize image files, you can also place them in game/tl/language."
    e "如果要本地化圖片檔案，也可以把它們放在 game/tl/language 中。"

# game/indepth_translations.rpy:48
translate tchinese translations_71bf6e72:

    # e "If the default fonts used by the game do not support the language you are translating to, you will have to change them."
    e "如果遊戲使用的預設字型不支援目標語言，就必須更換字型。"

# game/indepth_translations.rpy:50
translate tchinese translations_82c9748e:

    # e "The translate python statement can be used to set the values of gui variables to change the font."
    e "translate 語句可用來設定 GUI 變數的值，藉此變更字型。"

# game/indepth_translations.rpy:52
translate tchinese translations_a0042025:

    # e "The translate style statement sets style properties more directly."
    e "translate style 語句可以更直接地設定樣式屬性。"

# game/indepth_translations.rpy:54
translate tchinese translations_b10990ce:

    # e "If you need to add new files, such as font files, you can place them into the game/tl/language directory where Ren'Py will find them."
    e "如果需要加入新檔案，例如字型檔案，可以放入 game/tl/language 目錄，Ren'Py 就能找到它們。"

# game/indepth_translations.rpy:58
translate tchinese translations_01fcacc2:

    # e "Finally, you'll have to add support for picking the language of the game. That usually goes into the preferences screen, found in screens.rpy."
    e "最後，還要加入讓玩家選擇遊戲語言的功能。通常會在 screens.rpy 的偏好設定畫面中完成。"

# game/indepth_translations.rpy:60
translate tchinese translations_a91befcc:

    # e "Here's an excerpt of the preferences screen of this tutorial. The Language action tells Ren'Py to change the language. It takes a string giving a language name, or None."
    e "以下是本教學偏好設定畫面的節錄。Language 動作會要求 Ren'Py 變更語言，參數可以是語言名稱字串或 None。"

# game/indepth_translations.rpy:62
translate tchinese translations_9b7d6401:

    # e "The None language is special, as it's the default language that the visual novel was written in. Since this tutorial was written in English, Language(None) selects English."
    e "None 語言很特殊，代表視覺小說的預設語言。由於本教學以英文撰寫，Language(None) 會選取英文。"
