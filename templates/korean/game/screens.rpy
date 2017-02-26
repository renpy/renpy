# 이 파일에는 저작권이 없습니다.
# 원하는 스크린을 만들 수 있도록 마음껏 수정하세요.

##############################################################################
# 대사 화면
#
# ADV모드 대사를 표시할 때 사용하는 스크린.
# http://www.renpy.org/doc/html/screen_special.html#say
screen say:

    # side_image 와 two_window 의 기본값
    default side_image = None
    default two_window = False

    # 창을 1개 사용할지, 2개 사용할지 결정합니다.
    if not two_window:

        # 창을 1개 쓰는 대사창
        window:
            id "window"

            has vbox:
                style "say_vbox"

            if who:
                text who id "who"

            text what id "what"

    else:

        # 이름과 대사, 창을 2개 쓰는 대사창
        vbox:
            style "say_two_window_vbox"

            if who:
                window:
                    style "say_who_window"

                    text who:
                        id "who"

            window:
                id "window"

                has vbox:
                    style "say_vbox"

                text what id "what"

    # 사이드 이미지가 있다면 텍스트 위에 표시한다.
    if side_image:
        add side_image
    else:
        add SideImage() xalign 0.0 yalign 1.0

    # Use the quick menu.
    use quick_menu


##############################################################################
# 선택지 화면
#
# 게임 내 선택지를 표시할 때 사용하는 스크린.
# http://www.renpy.org/doc/html/screen_special.html#choice

screen choice:

    window:
        style "menu_window"
        xalign 0.5
        yalign 0.5

        vbox:
            style "menu"
            spacing 2

            for caption, action, chosen in items:

                if action:

                    button:
                        action action
                        style "menu_choice_button"

                        text caption style "menu_choice"

                else:
                    text caption style "menu_caption"

init -2:
    $ config.narrator_menu = True

    style menu_window is default

    style menu_choice is button_text:
        clear

    style menu_choice_button is button:
        xminimum int(config.screen_width * 0.75)
        xmaximum int(config.screen_width * 0.75)


##############################################################################
# 텍스트 입력 화면
#
# renpy.input을 나타낼 때 사용하는 스크린.
# http://www.renpy.org/doc/html/screen_special.html#input

screen input:

    window style "input_window":
        has vbox

        text prompt style "input_prompt"
        input id "input" style "input_text"

    use quick_menu

##############################################################################
# 비주얼노벨 대사 화면
#
# NVL모드의 대사와 선택지를 나타낼 때 사용하는 스크린.
# http://www.renpy.org/doc/html/screen_special.html#nvl

screen nvl:

    window:
        style "nvl_window"

        has vbox:
            style "nvl_vbox"

        # 대사를 표시한다.
        for who, what, who_id, what_id, window_id in dialogue:
            window:
                id window_id

                has hbox:
                    spacing 10

                if who is not None:
                    text who id who_id

                text what id what_id

        # 선택지가 있다면 선택지를 나타낸다.
        if items:

            vbox:
                id "menu"

                for caption, action, chosen in items:

                    if action:

                        button:
                            style "nvl_menu_choice_button"
                            action action

                            text caption style "nvl_menu_choice"

                    else:

                        text caption style "nvl_dialogue"

    add SideImage() xalign 0.0 yalign 1.0

    use quick_menu

##############################################################################
# 메인 메뉴 화면
#
# 렌파이 게임이 처음 시작되었을 때 나타나는 메인 메뉴를 표시하는 스크린
# http://www.renpy.org/doc/html/screen_special.html#main-menu

screen main_menu:

    # 다른 메뉴 스크린과 교체될 수 있도록 태그를 지정한다.
    tag menu

    # 메인 메뉴 배경 화면.
    window:
        style "mm_root"

    # 메인 메뉴 버튼.
    frame:
        style_group "mm"
        xalign .98
        yalign .98

        has vbox

        textbutton _("Start Game") action Start()
        textbutton _("Load Game") action ShowMenu("load")
        textbutton _("Preferences") action ShowMenu("preferences")
        textbutton _("Help") action Help()
        textbutton _("Quit") action Quit(confirm=False)

init -2:

    # 모든 메인 메뉴 버튼이 같은 크기가 되도록 한다.
    style mm_button:
        size_group "mm"



##############################################################################
# 네비게이션 화면
#
# 게임 메뉴 네비게이션 버튼과 배경 화면을 표시하는 스크린이 포함된 스크린.
# http://www.renpy.org/doc/html/screen_special.html#navigation
screen navigation:

    # 게임 메뉴 배경 화면.
    window:
        style "gm_root"

    # 여러 가지 버튼.
    frame:
        style_group "gm_nav"
        xalign .98
        yalign .98

        has vbox

        textbutton _("Return") action Return()
        textbutton _("Preferences") action ShowMenu("preferences")
        textbutton _("Save Game") action ShowMenu("save")
        textbutton _("Load Game") action ShowMenu("load")
        textbutton _("Main Menu") action MainMenu()
        textbutton _("Help") action Help()
        textbutton _("Quit") action Quit()

init -2:

    # 모든 네비게이션 버튼이 같은 크기가 되도록 한다.
    style gm_nav_button:
        size_group "gm_nav"


##############################################################################
# 저장하기, 불러오기 화면
#
# 게임을 저장하거나 불러올 수 있는 화면.
# http://www.renpy.org/doc/html/screen_special.html#save
# http://www.renpy.org/doc/html/screen_special.html#load

# 저장하기와 불러오기는 기능이 비슷하기 때문에, file_picker라는 스크린 하나에 통합했습니다.
# 그리고 file_picker 스크린을 load 및 save 스크린에 간단히 추가했습니다.

screen file_picker:

    frame:
        style "file_picker_frame"

        has vbox

        # 페이지를 선택할 수 있는 버튼.
        hbox:
            style_group "file_picker_nav"

            textbutton _("Previous"):
                action FilePagePrevious()

            textbutton _("Auto"):
                action FilePage("auto")

            textbutton _("Quick"):
                action FilePage("quick")

            for i in range(1, 9):
                textbutton str(i):
                    action FilePage(i)

            textbutton _("Next"):
                action FilePageNext()

        $ columns = 2
        $ rows = 5

        # 파일 슬롯 행렬을 표시한다.
        grid columns rows:
            transpose True
            xfill True
            style_group "file_picker"

            # 1번부터 10번까지의 파일 슬롯 열 개를 표시한다.
            for i in range(1, columns * rows + 1):

                # 각 파일 슬롯은 버튼이다.
                button:
                    action FileAction(i)
                    xfill True

                    has hbox

                    # 스크린샷을 추가한다.
                    add FileScreenshot(i)

                    $ file_name = FileSlotName(i, columns * rows)
                    $ file_time = FileTime(i, empty=_("Empty Slot."))
                    $ save_name = FileSaveName(i)

                    text "[file_name]. [file_time!t]\n[save_name!t]"

                    key "save_delete" action FileDelete(i)


screen save:

    # 다른 메뉴 스크린으로 교체할 수 있도록 태그를 추가한다.
    tag menu

    use navigation
    use file_picker

screen load:

    # 다른 메뉴 스크린으로 교체할 수 있도록 태그를 추가한다.
    tag menu

    use navigation
    use file_picker

init -2:
    style file_picker_frame is menu_frame
    style file_picker_nav_button is small_button
    style file_picker_nav_button_text is small_button_text
    style file_picker_button is large_button
    style file_picker_text is large_button_text


##############################################################################
# 환경설정 화면
#
# 환경설정을 변경할 수 있는 스크린.
# http://www.renpy.org/doc/html/screen_special.html#prefereces

screen preferences:

    tag menu

    # 네비게이션 스크린을 포함한다.
    use navigation

    # 환경설정 메뉴들을 3x1 행렬로 배치한다.
    grid 3 1:
        style_group "prefs"
        xfill True

        # 첫 번째 열.
        vbox:
            frame:
                style_group "pref"
                has vbox

                label _("Display")
                textbutton _("Window") action Preference("display", "window")
                textbutton _("Fullscreen") action Preference("display", "fullscreen")

            frame:
                style_group "pref"
                has vbox

                label _("Transitions")
                textbutton _("All") action Preference("transitions", "all")
                textbutton _("None") action Preference("transitions", "none")

            frame:
                style_group "pref"
                has vbox

                label _("Text Speed")
                bar value Preference("text speed")

            frame:
                style_group "pref"
                has vbox

                textbutton _("Joystick...") action Preference("joystick")

        # 두 번째 열
        vbox:
            frame:
                style_group "pref"
                has vbox

                label _("Skip")
                textbutton _("Seen Messages") action Preference("skip", "seen")
                textbutton _("All Messages") action Preference("skip", "all")

            frame:
                style_group "pref"
                has vbox

                textbutton _("Begin Skipping") action Skip()

            frame:
                style_group "pref"
                has vbox

                label _("After Choices")
                textbutton _("Stop Skipping") action Preference("after choices", "stop")
                textbutton _("Keep Skipping") action Preference("after choices", "skip")

            frame:
                style_group "pref"
                has vbox

                label _("Auto-Forward Time")
                bar value Preference("auto-forward time")

                if config.has_voice:
                    textbutton _("Wait for Voice") action Preference("wait for voice", "toggle")

        # 세 번째 열
        vbox:
            frame:
                style_group "pref"
                has vbox

                label _("Music Volume")
                bar value Preference("music volume")

            frame:
                style_group "pref"
                has vbox

                label _("Sound Volume")
                bar value Preference("sound volume")

                if config.sample_sound:
                    textbutton _("Test"):
                        action Play("sound", config.sample_sound)
                        style "soundtest_button"

            if config.has_voice:
                frame:
                    style_group "pref"
                    has vbox

                    label _("Voice Volume")
                    bar value Preference("voice volume")

                    textbutton _("Voice Sustain") action Preference("voice sustain", "toggle")
                    if config.sample_voice:
                        textbutton _("Test"):
                            action Play("voice", config.sample_voice)
                            style "soundtest_button"

init -2:
    style pref_frame:
        xfill True
        xmargin 5
        top_margin 5

    style pref_vbox:
        xfill True

    style pref_button:
        size_group "pref"
        xalign 1.0

    style pref_slider:
        xmaximum 192
        xalign 1.0

    style soundtest_button:
        xalign 1.0


##############################################################################
# 예/아니오 확인 화면
#
# 예 또는 아니오를 묻는 스크린.
# http://www.renpy.org/doc/html/screen_special.html#yesno-prompt

screen yesno_prompt:

    modal True

    window:
        style "gm_root"

    frame:
        style_group "yesno"

        xfill True
        xmargin .05
        ypos .1
        yanchor 0
        ypadding .05

        has vbox:
            xalign .5
            yalign .5
            spacing 30

        label _(message):
            xalign 0.5

        hbox:
            xalign 0.5
            spacing 100

            textbutton _("Yes") action yes_action
            textbutton _("No") action no_action

    # 마우스 우클릭과 esc 키는 No 버튼과 같다.
    key "game_menu" action no_action

init -2:
    style yesno_button:
        size_group "yesno"

    style yesno_label_text:
        text_align 0.5
        layout "subtitle"


##############################################################################
# 단축 메누 화면
#
# say 스크린에 기본적으로 포함되어 일부 유용한 기능을
# 빠르게 사용할 수 있는 버튼이 포함된 스크린.
screen quick_menu:

    # 게임 내 단축 메뉴를 추가한다.
    hbox:
        style_group "quick"

        xalign 1.0
        yalign 1.0

        textbutton _("Back") action Rollback()
        textbutton _("Save") action ShowMenu('save')
        textbutton _("Q.Save") action QuickSave()
        textbutton _("Q.Load") action QuickLoad()
        textbutton _("Skip") action Skip()
        textbutton _("F.Skip") action Skip(fast=True, confirm=True)
        textbutton _("Auto") action Preference("auto-forward", "toggle")
        textbutton _("Prefs") action ShowMenu('preferences')

init -2:
    style quick_button:
        is default
        background None
        xpadding 5

    style quick_button_text:
        is default
        size 12
        idle_color "#8888"
        hover_color "#ccc"
        selected_idle_color "#cc08"
        selected_hover_color "#cc0"
        insensitive_color "#4448"

