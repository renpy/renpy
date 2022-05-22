
# game/indepth_translations.rpy:12
translate korean translations_c4ef181f:

    # e "Ren'Py includes support for translating your game into languages other than the one it was originally written in."
    e "렌파이는 처음에 작성한 언어가 아닌 다른 언어로 게임을 번역할 수 있도록 지원하고 있어."

# game/indepth_translations.rpy:14
translate korean translations_20b9a600:

    # e "This includes the translation of every string in the game, including dialogue, menu choice, and interface strings, and of images and other assets."
    e "여기에는 지문, 분기 선택 및 인터페이스 문자열, 이미지 및 기타 자산을 포함하는 게임의 모든 문자열에 대한 번역이 포함돼."

# game/indepth_translations.rpy:16
translate korean translations_07c7643c:

    # e "While Ren'Py can find dialogue and menu choice strings for you, you'll have to indicate which other strings need translation."
    e "렌파이가 지문과 분기 선택 문자열을 찾을 수 있긴 하지만, 번역이 필요한 다른 문자열을 표시해줄 필요가 있어."

# game/indepth_translations.rpy:20
translate korean translations_317d73e5:

    # e "For example, here is how we define a character and her name."
    e "이건 캐릭터와 이름을 정의하는 방법에 대한 예시야."

# game/indepth_translations.rpy:24
translate korean translations_ab0f3c94:

    # e "To mark Lucy's name as translatable, we surround it by parentheses preceded by a single underscore."
    e "루시의 이름을 번역 가능한 것으로 표시하려면 괄호와 그 앞에 하나의 밑줄을 붙여야 해."

# game/indepth_translations.rpy:26
translate korean translations_c81acfc7:

    # e "Notice how we don't translate the reddish color that we use for her name. That stays the same for all languages."
    e "그녀의 이름으로 사용하는 붉은 색을 번역하지 않는 방법에 주목해. 모든 언어에 대해 똑같은 방법이야."

# game/indepth_translations.rpy:33
translate korean translations_8272a0ef:

    # e "Once that's done, you can generate the translation files. That's done by going to the launcher, and clicking translate."
    e "작업을 완료하면 번역 파일을 생성할 수 있어. 런처로 이동하여 번역 파일 만들기를 클릭하면 돼."

# game/indepth_translations.rpy:35
translate korean translations_fde34832:

    # e "After you type in the name of the language you'll be translating to, choosing Generate Translations will scan your game and create translation files."
    e "번역할 언어의 이름을 입력하고 번역파일 만들기를 선택하면, 게임을 스캔한 뒤 번역 파일을 만들 거야."

# game/indepth_translations.rpy:37
translate korean translations_e2ebb4af:

    # e "The files will be generated in game/tl/language, where language is the name of the language you typed in."
    e "파일들은 네가 언어의 이름으로 입력한 이름으로 game/tl/language에 생성될 거야."

# game/indepth_translations.rpy:39
translate korean translations_28ec40b9:

    # e "You'll need to edit those files to include translations for everything in your game."
    e "게임의 모든 내용이 번역본에 포함되도록 파일을 편집해야 돼."

# game/indepth_translations.rpy:41
translate korean translations_f6d3fd2d:

    # e "If you want to localize image files, you can also place them in game/tl/language."
    e "만약 이미지 파일의 현지화를 원한다면, 이미지 파일들을 game/tl/language에 같은 이름의 파일을 넣으면 돼."

# game/indepth_translations.rpy:48
translate korean translations_71bf6e72:

    # e "If the default fonts used by the game do not support the language you are translating to, you will have to change them."
    e "게임에서 사용하는 기본 글꼴이 번역할 언어를 지원하지 않는 경우에는 글꼴을 변경해야 하고."

# game/indepth_translations.rpy:50
translate korean translations_82c9748e:

    # e "The translate python statement can be used to set the values of gui variables to change the font."
    e "translate python 문은 gui 변수의 값을 설정하여 글꼴을 변경할 수 있어."

# game/indepth_translations.rpy:52
translate korean translations_a0042025:

    # e "The translate style statement sets style properties more directly."
    e "translate style 문은 스타일 속성을 보다 직접적으로 설정해."

# game/indepth_translations.rpy:54
translate korean translations_b10990ce:

    # e "If you need to add new files, such as font files, you can place them into the game/tl/language directory where Ren'Py will find them."
    e "글꼴 파일과 같은 새 파일을 추가해야 하는 경우에는 렌파이가 찾을 수 있게 game/tl/language 디렉토리에 저장할 수 있어."

# game/indepth_translations.rpy:58
translate korean translations_01fcacc2:

    # e "Finally, you'll have to add support for picking the language of the game. That usually goes into the preferences screen, found in screens.rpy."
    e "마지막으로 게임 언어 선택 기능을 추가해야 돼. 일반적으로 screen.rpy에 있는 preferences 스크린에 작성할 수 있어."

# game/indepth_translations.rpy:60
translate korean translations_a91befcc:

    # e "Here's an excerpt of the preferences screen of this tutorial. The Language action tells Ren'Py to change the language. It takes a string giving a language name, or None."
    e "이건 이 길라잡이의 환경 설정 화면의 일부야. Language 액션은 렌파이에게 언어 변경을 지시하고, 언어 이름을 제공하는 문자열 또는 None을 사용하지."

# game/indepth_translations.rpy:62
translate korean translations_9b7d6401:

    # e "The None language is special, as it's the default language that the visual novel was written in. Since this tutorial was written in English, Language(None) selects English."
    e "None 언어는 비주얼 노벨이 작성된 기본 언어이기 때문에 특별해. 이 길라잡이는 영어를 기본으로 작성되었으므로 English는 Language(None)을 선택해."

