
# game/indepth_translations.rpy:12
translate japanese translations_c4ef181f:

    # e "Ren'Py includes support for translating your game into languages other than the one it was originally written in."
    e "Ren'Pyは開発されたオリジナルの言語から他の言語への翻訳をサポートしています。"

# game/indepth_translations.rpy:14
translate japanese translations_20b9a600:

    # e "This includes the translation of every string in the game, including dialogue, menu choice, and interface strings, and of images and other assets."
    e "これには台詞、メニュー、インターフェース、画像やその他のアセットに含まれる文字列を含むゲーム中すべての文字列の翻訳を含みます。"

# game/indepth_translations.rpy:16
translate japanese translations_07c7643c:

    # e "While Ren'Py can find dialogue and menu choice strings for you, you'll have to indicate which other strings need translation."
    e "Ren'Pyは台詞と選択肢の文字列検出できますが、他の文字列は翻訳を必要とするかを明示しなければなりません。"

# game/indepth_translations.rpy:20
translate japanese translations_317d73e5:

    # e "For example, here is how we define a character and her name."
    e "例えばこちらはキャラクターとその名前の定義の仕方です。。"

# game/indepth_translations.rpy:24
translate japanese translations_ab0f3c94:

    # e "To mark Lucy's name as translatable, we surround it by parentheses preceded by a single underscore."
    e "mark Lucyの名前を翻訳対象にするにはアンダースコア1つを接頭辞にする括弧が必要です。"

# game/indepth_translations.rpy:26
translate japanese translations_c81acfc7:

    # e "Notice how we don't translate the reddish color that we use for her name. That stays the same for all languages."
    e "彼女の名前に使用した色は翻訳していないことに注目してください。すべての言語で同じにしています。"

# game/indepth_translations.rpy:33
translate japanese translations_8272a0ef:

    # e "Once that's done, you can generate the translation files. That's done by going to the launcher, and clicking translate."
    e "いったんこれをすれば、翻訳ファイルを生成できます。生成はランチャーの翻訳をクリックすればできます。"

# game/indepth_translations.rpy:35
translate japanese translations_fde34832:

    # e "After you type in the name of the language you'll be translating to, choosing Generate Translations will scan your game and create translation files."
    e "翻訳先の言語名を入力して翻訳の生成を選べばゲームをスキャンして翻訳ファイルを生成できます。"

# game/indepth_translations.rpy:37
translate japanese translations_e2ebb4af:

    # e "The files will be generated in game/tl/language, where language is the name of the language you typed in."
    e "game/tl/languageにファイルは生成されます。languageは入力した言語名になります。"

# game/indepth_translations.rpy:39
translate japanese translations_28ec40b9:

    # e "You'll need to edit those files to include translations for everything in your game."
    e "ファイルを編集してゲームのすべてに対する翻訳を作成しなければなりません。"

# game/indepth_translations.rpy:41
translate japanese translations_f6d3fd2d:

    # e "If you want to localize image files, you can also place them in game/tl/language."
    e "画像ファイルをローカライズしたければ、それらもgame/tl/languageファイルに配置できます。"

# game/indepth_translations.rpy:48
translate japanese translations_71bf6e72:

    # e "If the default fonts used by the game do not support the language you are translating to, you will have to change them."
    e "ゲームのデフォルトフォントが翻訳した言語をサポートしていないならば、それらも変更しなければなりません。"

# game/indepth_translations.rpy:50
translate japanese translations_82c9748e:

    # e "The translate python statement can be used to set the values of gui variables to change the font."
    e "translate pythonステートメントでgui変数の値をそのフォントに変更できます。"

# game/indepth_translations.rpy:52
translate japanese translations_a0042025:

    # e "The translate style statement sets style properties more directly."
    e "translate style ステートメントはスタイルプロパティーをより直接的に設定できます。"

# game/indepth_translations.rpy:54
translate japanese translations_b10990ce:

    # e "If you need to add new files, such as font files, you can place them into the game/tl/language directory where Ren'Py will find them."
    e "フォントファイルのように新しいファイルを追加する必要があればgame/tl/languageディレクトリに配置すればRen'Pyで読み込みます。"

# game/indepth_translations.rpy:58
translate japanese translations_01fcacc2:

    # e "Finally, you'll have to add support for picking the language of the game. That usually goes into the preferences screen, found in screens.rpy."
    e "最後に、ゲームに言語選択のサポートを追加しなければなりません。それは通常screens.rpyの設定画面で行います。"

# game/indepth_translations.rpy:60
translate japanese translations_a91befcc:

    # e "Here's an excerpt of the preferences screen of this tutorial. The Language action tells Ren'Py to change the language. It takes a string giving a language name, or None."
    e "こちらはこのチュートリアルの設定画面の抜粋です。LanguageアクションはRen'Pyに言語の変更を通知します。これは言語名の文字列またはNoneをとります。"

# game/indepth_translations.rpy:62
translate japanese translations_9b7d6401:

    # e "The None language is special, as it's the default language that the visual novel was written in. Since this tutorial was written in English, Language(None) selects English."
    e "None言語は特別で、そのビジュアルノベルが作成されたデフォルトの言語です。このチュートリアルは英語で書かれているので、Language(None)は英語を選択します。"

