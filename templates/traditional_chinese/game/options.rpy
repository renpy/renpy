## This file contains some of the options that can be changed to customize
## your Ren'Py game. It only contains the most common options... there
## is quite a bit more customization you can do.
##
## Lines beginning with two '#' marks are comments, and you shouldn't
## uncomment them. Lines beginning with a single '#' mark are
## commented-out code, and you may want to uncomment them when
## appropriate.

init -1 python hide:

    ## Should we enable the use of developer tools? This should be
    ## set to False before the game is released, so the user can't
    ## cheat using developer tools.

    config.developer = True

    ## These control the width and height of the screen.
    ## 這些控制螢幕的寬度和高度。

    config.screen_width = 800
    config.screen_height = 600

    ## This controls the title of the window, when Ren'Py is
    ## running in a window.

    config.window_title = u"PROJECT_NAME"

    # These control the name and version of the game, that are reported
    # with tracebacks and other debugging logs.
    # 當 Ren'Py 啓動時，此參數控制視窗的標題。
    # 并在一個視窗中運行。
    config.name = "PROJECT_NAME"
    config.version = "0.0"

    #########################################
    # Themes
    # 主題

    ## We then want to call a theme function. theme.roundrect is
    ## a theme that features the use of rounded rectangles.
    ##
    ## The theme function takes a number of parameters that can
    ## customize the color scheme.

    theme.regal(
        ## Theme: Regal
        ## Color scheme: Tree Frog

        ## The color of an idle widget face.
        widget = "#1c140d",

        ## The color of a focused widget face.
        widget_hover = "#86827e",

        ## The color of the text in a widget.
        widget_text = "#cbe86b",

        ## The color of the text in a selected widget. (For
        ## example, the current value of a preference.)
        widget_selected = "#f2e9e1",

        ## The color of a disabled widget face.
        disabled = "#ffffff",

        ## The color of disabled widget text.
        disabled_text = "#1c140d",

        ## The color of informational labels.
        label = "#1c140d",

        ## The color of a frame containing widgets.
        frame = "#cbe86b",

        ## The background of the main menu. This can be a color
        ## beginning with '#', or an image filename. The latter
        ## should take up the full height and width of the screen.
        mm_root = "#ffffff",

        ## The background of the game menu. This can be a color
        ## beginning with '#', or an image filename. The latter
        ## should take up the full height and width of the screen.
        gm_root = "#ffffff",

        ## If this is True, the in-game window is rounded. If False,
        ## the in-game window is square.
        rounded_window = False,

        ## And we're done with the theme. The theme will customize
        ## various styles, so if we want to change them, we should
        ## do so below.
        )


    #########################################
    ## These settings let you customize the window containing the
    ## dialogue and narration, by replacing it with an image.

    ## The background of the window. In a Frame, the two numbers
    ## are the size of the left/right and top/bottom borders,
    ## respectively.

    # style.window.background = Frame("frame.png", 12, 12)

    ## Margin is space surrounding the window, where the background
    ## is not drawn.

    # style.window.left_margin = 6
    # style.window.right_margin = 6
    # style.window.top_margin = 6
    # style.window.bottom_margin = 6

    ## Padding is space inside the window, where the background is
    ## drawn.

    # style.window.left_padding = 6
    # style.window.right_padding = 6
    # style.window.top_padding = 6
    # style.window.bottom_padding = 6

    ## This is the minimum height of the window, including the margins
    ## and padding.

    # style.window.yminimum = 250


    #########################################
    ## This lets you change the placement of the main menu.

    ## The way placement works is that we find an anchor point
    ## inside a displayable, and a position (pos) point on the
    ## screen. We then place the displayable so the two points are
    ## at the same place.

    ## An anchor/pos can be given as an integer or a floating point
    ## number. If an integer, the number is interpreted as a number
    ## of pixels from the upper-left corner. If a floating point,
    ## the number is interpreted as a fraction of the size of the
    ## displayable or screen.

    # style.mm_menu_frame.xpos = 0.5
    # style.mm_menu_frame.xanchor = 0.5
    # style.mm_menu_frame.ypos = 0.75
    # style.mm_menu_frame.yanchor = 0.5


    #########################################
    ## These let you customize the default font used for text in Ren'Py.
    ## 可以在以下各項中自訂預設字型。

    ## The file containing the default font.
    ## 設定預設字型。

    style.default.font = "tl/None/DroidSansFallback.ttf"
    style._default.font = "tl/None/DroidSansFallback.ttf"

    ## The default size of text.
    ## 更改預設文字的大小。

    # style.default.size = 22

    ## Note that these only change the size of some of the text. Other
    ## buttons have their own styles.
    ## 以上設定，可以變更某些文本的大小。
    ## 對其他都設定為他們自己的按鈕的文本樣式。



    #########################################
    ## These settings let you change some of the sounds that are used by
    ## Ren'Py.

    ## Set this to False if the game does not have any sound effects.

    config.has_sound = True

    ## Set this to False if the game does not have any music.

    config.has_music = True

    ## Set this to True if the game has voicing.

    config.has_voice = False

    ## Sounds that are used when button and imagemaps are clicked.

    # style.button.activate_sound = "click.wav"
    # style.imagemap.activate_sound = "click.wav"

    ## Sounds that are used when entering and exiting the game menu.

    # config.enter_sound = "click.wav"
    # config.exit_sound = "click.wav"

    ## A sample sound that can be played to check the sound volume.

    # config.sample_sound = "click.wav"

    ## Music that is played while the user is at the main menu.

    # config.main_menu_music = "main_menu_theme.ogg"


    #########################################
    ## Help.
    ## 説明。

    ## This lets you configure the help option on the Ren'Py menus.
    ## It may be:
    ## - A label in the script, in which case that label is called to
    ##   show help to the user.
    ## - A file name relative to the base directory, which is opened in a
    ##   web browser.
    ## - None, to disable help.
    ## 這允許您配置 Ren'Py 選單中的説明選項。
    config.help = "README.html"


    #########################################
    ## Transitions.
    ## 過渡。

    ## Used when entering the game menu from the game.
    ## 進入遊戲選單（右鍵選單）時的轉場方式。
    config.enter_transition = None

    ## Used when exiting the game menu to the game.
    ## 脫離遊戲選單（右鍵選單）時的轉場方式。
    config.exit_transition = None

    ## Used between screens of the game menu.
    ## 在主選單、遊戲選單、設定畫面、存讀檔畫面中交叉切換時的內部轉場方式。
    config.intra_transition = None

    ## Used when entering the game menu from the main menu.
    ## 遷移到遊戲選單從主選單中的過渡時間。
    config.main_game_transition = None

    ## Used when returning to the main menu from the game.
    ## 過渡時間暫停遊戲並返回到主選單。
    config.game_main_transition = None

    ## Used when entering the main menu from the splashscreen.
    ## 開啟遊戲，第一次進入主選單時的轉場方式。
    config.end_splash_transition = None

    ## Used when entering the main menu after the game has ended.
    ## 遊戲結束（碰到 return）跳回主選單時的轉場方式。
    config.end_game_transition = None

    ## Used when a game is loaded.
    ## 在 load 畫面載入遊戲時採用的轉場方式。
    config.after_load_transition = None

    ## Used when the window is shown.
    ## 顯式秀出對話框時使用的轉場方式（不過您目前還不知道怎麼操作）。
    config.window_show_transition = None

    ## Used when the window is hidden.
    ## 顯式關閉對話框時使用的轉場方式（不過您目前還不知道怎麼操作）。
    config.window_hide_transition = None

    ## Used when showing NVL-mode text directly after ADV-mode text.
    ## 當在 ADV-mode 文字後直接顯示 NVL-mode 文字時使用。
    config.adv_nvl_transition = dissolve

    ## Used when showing ADV-mode text directly after NVL-mode text.
    ## 當在 NVL-mode 文字後直接顯示 ADV-mode 文字時使用。
    config.nvl_adv_transition = dissolve

    ## Used when yesno is shown.
    ## 當顯示怒氣衝衝時使用。
    config.enter_yesno_transition = None

    ## Used when the yesno is hidden.
    ## 當怒氣衝衝處於隱藏狀態時使用。
    config.exit_yesno_transition = None

    ## Used when entering a replay
    ## 當進入重播時使用
    config.enter_replay_transition = None

    ## Used when exiting a replay
    ## 當退出重播時使用
    config.exit_replay_transition = None

    ## Used when the image is changed by a say statement with image attributes.
    ## 圖像由對話語句向圖像屬性更改時使用。
    config.say_attribute_transition = None

    #########################################
    ## This is the name of the directory where the game's data is
    ## stored. (It needs to be set early, before any other init code
    ## is run, so the persistent information can be found by the init code.)
    ## 遊戲資料存儲在硬碟中的路徑名稱。
    ## 它需要及早設定，在初始化代碼運行之前，所以持續的資訊可以通過初始化代碼中找到。
python early:
    config.save_directory = "PROJECT_NAME-UNIQUE"

init -1 python hide:
    #########################################
    ## Default values of Preferences.
    ## 首選項的預設值。

    ## Note: These options are only evaluated the first time a
    ## game is run. To have them run a second time, delete
    ## game/saves/persistent
    ## 注釋：僅當運行的遊戲第一次來計算的值時，此選項才可用。
    ## 如果你想要應用的修改後的遊戲值請返回到
    ## game/saves/persistent 請刪除該檔。

    ## Should we start in fullscreen mode?
    ## 全螢幕模式嗎？

    config.default_fullscreen = False

    ## The default text speed in characters per second. 0 is infinite.
    ## 預設文本字元 / 秒的表示速度。0 表示無限。

    config.default_text_cps = 0

    ## The default auto-forward time setting.
    ## 設定預設自動前進時間。

    config.default_afm_time = 10

    #########################################
    ## More customizations can go here.
