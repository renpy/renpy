# 此檔屬於公共領域，
# 請為屬於您的遊戲螢幕內容自由地定制。

##############################################################################
# Say
#
# 用於顯示adv-mode對話的螢幕。
# http://www.renpy.org/doc/html/screen_special.html#say
screen say:

    # 側邊圖(side_image)與雙文字方塊的預設值。
    default side_image = None
    default two_window = False

    # 決定單文字方塊或雙文字方塊的變數：
    if not two_window:

        # 單文字方塊。
        window:
            id "window"

            has vbox:
                style "say_vbox"

            if who:
                text who id "who"

            text what id "what"

    else:

        # 雙文字方塊。
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

    # 如果存在側邊圖，將其顯示于文字上方。
    if side_image:
        add side_image
    else:
        add SideImage() xalign 0.0 yalign 1.0

    # 使用快速選單。
    use quick_menu


##############################################################################
# Choice
#
# 顯示遊戲內選項的螢幕。
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
# Input
#
# 用於顯示renpy.input()對應效果的螢幕。
# http://www.renpy.org/doc/html/screen_special.html#input

screen input:

    window style "input_window":
        has vbox

        text prompt style "input_prompt"
        input id "input" style "input_text"

    use quick_menu

##############################################################################
# Nvl
#
# 用於顯示nvl-mode對話與選項的螢幕。
# http://www.renpy.org/doc/html/screen_special.html#nvl

screen nvl:

    window:
        style "nvl_window"

        has vbox:
            style "nvl_vbox"

        # 顯示對話。
        for who, what, who_id, what_id, window_id in dialogue:
            window:
                id window_id

                has hbox:
                    spacing 10

                if who is not None:
                    text who id who_id

                text what id what_id

        # 顯示選項，如果有。
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
# Main Menu
#
# 用於初次啟動時顯示Ren'py遊戲主選單的螢幕。
# http://www.renpy.org/doc/html/screen_special.html#main-menu

screen main_menu:

    # 確保其他的選單螢幕被替換。
    tag menu

    # 主選單背景。
    window:
        style "mm_root"

    # 主選單按鈕。
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

    # 使所有選單按鈕的大小一致。
    style mm_button:
        size_group "mm"



##############################################################################
# Navigation
#
# 遊戲螢幕內的另一個螢幕，用於顯示
# 遊戲選項的導航與背景。
# 注釋：參見Ren'py引擎SDK附帶的tutorial。
# http://www.renpy.org/doc/html/screen_special.html#navigation
screen navigation:

    # 遊戲選單的背景。
    window:
        style "gm_root"

    # 不同的按鈕。
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

    # 使所有導航選項按鈕大小相同。
    style gm_nav_button:
        size_group "gm_nav"


##############################################################################
# Save, Load
#
# 使用者能夠存檔與讀檔的螢幕。
# http://www.renpy.org/doc/html/screen_special.html#save
# http://www.renpy.org/doc/html/screen_special.html#load

# 因為存檔與讀檔都非常相似，
# 因此我們將它們混合到一個螢幕中，file_picker。
# 於是我們就用file_picker螢幕來實現簡單的存檔與讀檔。

screen file_picker:

    frame:
        style "file_picker_frame"

        has vbox

        # 頂部的按鈕可允許使用者選擇
        # 存檔的頁數。
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

        # 顯示存檔位網格。
        grid columns rows:
            transpose True
            xfill True
            style_group "file_picker"

            # 顯示十個存檔位，編號為1-10。
            for i in range(1, columns * rows + 1):

                # 每個存檔位都是一個按鈕。
                button:
                    action FileAction(i)
                    xfill True

                    has hbox

                    # 添加螢幕截圖。
                    add FileScreenshot(i)

                    $ file_name = FileSlotName(i, columns * rows)
                    $ file_time = FileTime(i, empty=_("Empty Slot."))
                    $ save_name = FileSaveName(i)

                    text "[file_name]. [file_time!t]\n[save_name!t]"

                    key "save_delete" action FileDelete(i)


screen save:

    # 確保其他任何選單都被覆蓋。
    tag menu

    use navigation
    use file_picker

screen load:

    # 確保其他任何選單都被覆蓋。
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
# Preferences
#
# 允許使用者更改偏好設置的螢幕。
# http://www.renpy.org/doc/html/screen_special.html#prefereces

screen preferences:

    tag menu

    # 包含導航選項。
    use navigation

    # 縱向放置導航選項于三個寬列中。
    grid 3 1:
        style_group "prefs"
        xfill True

        # 左側縱欄。
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

        # 中間縱欄
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
        # 右側縱欄
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
# Yes/No Prompt
#
# 用於詢問使用者確定與否的螢幕。
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

    # 按右鍵進行回避並回答「否」。
    key "game_menu" action no_action

init -2:
    style yesno_button:
        size_group "yesno"

    style yesno_label_text:
        text_align 0.5
        layout "subtitle"


##############################################################################
# Quick Menu
#
# 包含在預設的say螢幕中的螢幕，
# 用於快速訪問某些實用功能。
# 注釋：也就是文字方塊下方的存檔、讀檔等按鈕。
screen quick_menu:

    # 添加一個遊戲內快速訪問的選單。
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

