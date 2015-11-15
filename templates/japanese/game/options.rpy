## This file contains some of the options that can be changed to customize
## your Ren'Py game. It only contains the most common options... there
## is quite a bit more customization you can do.
## ゲームをカスタマイズするオプションを記述したファイルです。
## 本ファイルは一般的なオプションのみを記述していますが、
## それ以上のカスタマイズも可能です。

## Lines beginning with two '#' marks are comments, and you shouldn't
## uncomment them. Lines beginning with a single '#' mark are
## commented-out code, and you may want to uncomment them when
## appropriate.
## ２つの#から始まる行はコメントで、非コメント化することはできません。
## 一つの#から始まる行はコメント化されたコードで、必要があれば
## 非コメント化して利用できます。

init -1 python hide:

    ## Should we enable the use of developer tools? This should be
    ## set to False before the game is released, so the user can't
    ## cheat using developer tools.
    ## 開発者ツールを使用するかどうか決めます。
    ## ユーザーが利用できないように、ゲームをリリースする前に
    ## False にセットする必要があります。

    config.developer = True

    ## These control the width and height of the screen.
    ## スクリーンのサイズを変更します。

    config.screen_width = 800
    config.screen_height = 600

    ## This controls the title of the window, when Ren'Py is
    ## running in a window.
    ## ゲームがウインドウモードで起動している時の
    ## ウインドウタイトルを変更します。

    config.window_title = u"PROJECT_NAME"

    # These control the name and version of the game, that are reported
    # with tracebacks and other debugging logs.
    # ゲームの名前とバージョンを変更します。
    # トレースバックなどのデバッグ用ログに記載されます。

    config.name = "PROJECT_NAME"
    config.version = "0.0"

    #########################################
    # Themes
    # テーマ

    ## 訳注：現在のバージョンでは、ほとんどのカスタマイズはスタイルと
    ## スクリーンで行われます。そのため、本項目は未翻訳です。

    ## We then want to call a theme function. theme.roundrect is
    ## a theme that features the use of rounded rectangles.
    ##
    ## The theme function takes a number of parameters that can
    ## customize the color scheme.

    theme.roundrect(
        ## Theme: Roundrect
        ## Color scheme: Basic Blue

        ## The color of an idle widget face.
        widget = "#003c78",

        ## The color of a focused widget face.
        widget_hover = "#0050a0",

        ## The color of the text in a widget.
        widget_text = "#c8ffff",

        ## The color of the text in a selected widget. (For
        ## example, the current value of a preference.)
        widget_selected = "#ffffc8",

        ## The color of a disabled widget face.
        disabled = "#404040",

        ## The color of disabled widget text.
        disabled_text = "#c8c8c8",

        ## The color of informational labels.
        label = "#ffffff",

        ## The color of a frame containing widgets.
        frame = "#6496c8",

        ## The background of the main menu. This can be a color
        ## beginning with '#', or an image filename. The latter
        ## should take up the full height and width of the screen.
        mm_root = "#dcebff",

        ## The background of the game menu. This can be a color
        ## beginning with '#', or an image filename. The latter
        ## should take up the full height and width of the screen.
        gm_root = "#dcebff",

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
    ## 以下の項目は、ダイアログとナレーション表示するウインドウを、
    ## 画像で置き換えてカスタマイズします。

    ## 訳注：より詳細なカスタマイズは  screen で行ないます。
    ## screen 内で記述されたスタイルは init python 内で記述された
    ## スタイルより優先されます。

    ## The background of the window. In a Frame, the two numbers
    ## are the size of the left/right and top/bottom borders,
    ## respectively.
    ## ウィンドウの背景です。Frame を使う場合、２つの数字は
    ## 左右、上下それぞれの枠のサイズです。

    # style.window.background = Frame("frame.png", 12, 12)

    ## Margin is space surrounding the window, where the background
    ## is not drawn.
    ## マージンは、ウインドウ背景の外側のスペースを意味します。

    # style.window.left_margin = 6
    # style.window.right_margin = 6
    # style.window.top_margin = 6
    # style.window.bottom_margin = 6

    ## Padding is space inside the window, where the background is
    ## drawn.
    ## パディングは、ウインドウ背景の内側のスペースを意味します。

    # style.window.left_padding = 6
    # style.window.right_padding = 6
    # style.window.top_padding = 6
    # style.window.bottom_padding = 6

    ## This is the minimum height of the window, including the margins
    ## and padding.
    ## マージンとパッディングを含んだウインドウの最小の高さです

    # style.window.yminimum = 250

    ## 訳注：以下は原文にはない追加コードです。

    ## フレームに使う画像を変更します。
    ## フレームはボタンなどを囲む枠に使われます。

    # style.frame.background = Frame("frame.png", 12, 12)

    ## ボタンに使う画像を変更します。

    # style.button.insensitive_background =  Frame("button_insensitive.png",12,12)
    # style.button.idle_background = Frame("button_idele.png",12,12)
    # style.button.hover_background = Frame("button_hover.png",12,12)
    # style.button.selected_idle_background = Frame("button_selected_idle.png",12,12)
    # style.button.selected_hover_background  Frame("button_selected_hover.png",12,12)

    ## ファイルスロットに使う画像を変更します。

    # style.large_button.insensitive_background =  Frame("button_insensitive.png",12,12)
    # style.large_button.idle_background = Frame("button_idele.png",12,12)
    # style.large_button.hover_background = Frame("button_hover.png",12,12)
    # style.large_button.selected_idle_background = Frame("button_selected_idle.png",12,12)
    # style.large_button.selected_hover_background  Frame("button_selected_hover.png",12,12)

    ## バーに使う画像を変更します。
    ## 使用する画像の両端に僅かな透明ピクセルがないと、綺麗に表示されません。

    # style.bar.left_bar = Frame("left_bar.png", 12,12)
    # style.bar.right_bar = Frame("right_bar.png", 12,12)
    # style.bar.thumb = None

    ## スライダーに使う画像を変更します。
    ## スライダーは、preferences で使われる、左右にドラッグできるバーです。

    # style.slider.left_bar =  Frame("left_slider.png", 12,12)
    # style.slider.right_bar =  Frame("right_slider.png", 12,12)
    # style.slider.thumb = None
    # style.slider.hover_left_bar = Frame("hover_left_bar.png", 12,12)

    ## スクロールバーに使う画像を変更します。
    ## スクロールバーは、viewport で使われます。

    # style.scrollbar.left_bar = Frame("scrollbar.png", 12,12)
    # style.scrollbar.right_bar = Frame("scrollbar.png", 12,12)
    # style.scrollbar.thumb = Frame("thumb.png", 12, 12)

    # style.vscrollbar.top_lbar = Frame("vscrollbar.png", 12,12)
    # style.vscrollbar.bottom_bar = Frame("vscrollbar.png", 12,12)
    # style.vscrollbar.thumb = Frame("vthumb.png", 12, 12)


    #########################################
    ## This lets you change the placement of the main menu.
    ## 以下の項目はメインメニューの位置を変更します。

    ## 訳注：現在のバージョンでは通常 screen でカスタマイズします。

    ## The way placement works is that we find an anchor point
    ## inside a displayable, and a position (pos) point on the
    ## screen. We then place the displayable so the two points are
    ## at the same place.
    ## 位置の決定は、まず画像内の anchor の座標を調べ、その座標を
    ## 与えられた pos の座標に配置します。

    ## An anchor/pos can be given as an integer or a floating point
    ## number. If an integer, the number is interpreted as a number
    ## of pixels from the upper-left corner. If a floating point,
    ## the number is interpreted as a fraction of the size of the
    ## displayable or screen.
    ## anchor と pos は整数か小数の値を取ります。
    ## 整数の場合は、画面左上から数えたピクセル数になります。
    ## 小数の場合は、画像や画面全体を１として、それに比例
    ## した分数値になります


    # style.mm_menu_frame.xpos = 0.5
    # style.mm_menu_frame.xanchor = 0.5
    # style.mm_menu_frame.ypos = 0.75
    # style.mm_menu_frame.yanchor = 0.5


    #########################################
    ## These let you customize the default font used for text in Ren'Py.
    ## 以下の項目は、デフォルトのフォントをカスタマイズします。

    ## The file containing the default font.
    ## デフォルトフォントを設定します。

    style.default.font = "tl/None/MTLc3m.ttf"
    style._default.font = "tl/None/MTLc3m.ttf"

    ## The default size of text.
    ## デフォルトのテキストサイズを変更します。

    # style.default.size = 22

    ## Note that these only change the size of some of the text. Other
    ## buttons have their own styles.
    ## この設定で、全てのテキストサイズが変更されるわけではありません。
    ## ボタンにはそれぞれ固有のスタイルがあります。

    ## 訳注：以下は原文にはない追加コードです。


    ## 日本語の禁則処理を設定します。
    ## "japanese-strict", "japapese-normal", "japanese-loose"から選択します。

    style.default.language = "japanese-strict"
    style._default.language = "japanese-strict"

    ## ダイアログとナレーションのテキストを変更します。

    # style.say_dialogue.size = 22
    # style.say_thought.size = 22

    ## centered や show text で使用するテキストを変更します。

    # style.centered_text.size = 22
    # style.vcentered_text.size = 22

    ## キャラクター名表示用のテキストを変更します。デフォルトでは太文字
    ## ですが、アウトラインと置き換えた方が見やすいかもしれません。

    # style.say_label.size = 22
    # style.say_label.bold = False
    # style.say_label.outlines=[(1,"#000d"), (1,"#0009",2,2)]

    ## label のテキストを変更します。
    ## label は preferences の各項目名として使われます。

    # style.label_text.size = 22

    ## button のテキストを変更します

    # style.button_text.size = 22
    # style.large_button_text.size = 16

    ## それ以外のスクリーン用テキストを変更します。
    # style.text.size = 22

    ## ルビの位置を微調整します。

    # style.ruby_text.size = 12
    # style.ruby_text.yoffset = -20

    ## ルビが振れるようにダイアログとナレーションの行間を広げます。

    # style.say_dialogue.line_leading = 12
    # style.say_thought.line_leading = 12


    #########################################
    ## These settings let you change some of the sounds that are used by
    ## Ren'Py.
    ## 以下の項目はゲーム内のサウンドの振る舞いを変更します。

    ## Set this to False if the game does not have any sound effects.
    ## False に設定すると効果音が鳴らなくなります。

    config.has_sound = True

    ## Set this to False if the game does not have any music.
    ## False 設定にすると音楽が流れなくなります。

    config.has_music = True

    ## Set this to True if the game has voicing.
    ## ボイスを使用するなら True に+設定してください。

    config.has_voice = False

    ## Sounds that are used when button and imagemaps are clicked.
    ## ボタンやイメージボタンをクリックした時に鳴らす効果音。

    # style.button.activate_sound = "click.wav"
    # style.imagemap.activate_sound = "click.wav"

    ## Sounds that are used when entering and exiting the game menu.
    # ゲームメニューに出入りする時に鳴らす効果音。

    # config.enter_sound = "click.wav"
    # config.exit_sound = "click.wav"

    ## A sample sound that can be played to check the sound volume.
    ## ボリュームチェック時に鳴らすサンプル効果音。

    # config.sample_sound = "click.wav"

    ## Music that is played while the user is at the main menu.
    ## メインメニューで流れる音楽。

    # config.main_menu_music = "main_menu_theme.ogg"


    #########################################
    ## Help.
    ## ヘルプ

    ## This lets you configure the help option on the Ren'Py menus.
    ## It may be:
    ## - A label in the script, in which case that label is called to
    ##   show help to the user.
    ## - A file name relative to the base directory, which is opened in a
    ##   web browser.
    ## - None, to disable help.
    ## メニュー、もしくは F1 で呼び出されるヘルプを設定します。
    ## スクリプトにある label 名の場合、そのラベルを呼び出します。
    ## ベースディレクトリにあるファイル名の場合、ウェブブラウザで
    ## そのファイルを開きます。
    ## None に設定するとヘルプを無効にします。

    config.help = "README.html"


    #########################################
    ## Transitions.
    ## トランジション

    ## 訳注：スクリーンをカスタマイズすると、メニュー展開時によりダイナミックな
    ## アニメーションを行うことができます。ただし、メニューを閉じる場合には以下
    ## の方法しか使えません。

    ## Used when entering the game menu from the game.
    ## ゲームメニューを開いた時のトランジション。
    config.enter_transition = None

    ## Used when exiting the game menu to the game.
    ## ゲームメニューを閉じた時のトランジション。
    config.exit_transition = None

    ## Used between screens of the game menu.
    ## ゲームメニュー内の項目を切り替える時のトランジション。
    config.intra_transition = None

    ## Used when entering the game menu from the main menu.
    ## メインメニューからゲームメニューに移行する時のトランジション。
    config.main_game_transition = None

    ## Used when returning to the main menu from the game.
    ## ゲームを中断してメインメニューに戻る時のトランジション。
    config.game_main_transition = None

    ## Used when entering the main menu from the splashscreen.
    ## スプラッシュスクリーンからメインメニューに移行する時のトランジション。
    config.end_splash_transition = None

    ## Used when entering the main menu after the game has ended.
    ## ゲームを終了してメインメニューに戻る時のトランジション。
    config.end_game_transition = None

    ## Used when a game is loaded.
    ## ゲームをロードした時のトランジション。
    config.after_load_transition = None

    ## Used when the window is shown.
    ## ノベルウィンドウを表示する時のトランジション。
    config.window_show_transition = None

    ## Used when the window is hidden.
    ## ノベルウィンドウを閉じる時のトランジション。
    config.window_hide_transition = None

    ## Used when showing NVL-mode text directly after ADV-mode text.
    ## アドベンチャーモードからノベルモードへ移行する時のトランジション。
    config.adv_nvl_transition = dissolve

    ## Used when showing ADV-mode text directly after NVL-mode text.
    ## ノベルモードからアドベンチャーモードへ移行する時のトランジション。
    config.nvl_adv_transition = dissolve

    ## Used when yesno is shown.
    ## イエス・ノープロンプトを表示する時のトランジション。
    config.enter_yesno_transition = None

    ## Used when the yesno is hidden.
    ## イエス・ノープロンプトを閉じる時のトランジション。
    config.exit_yesno_transition = None

    ## Used when entering a replay
    ## リプレイモードに入る時のトランジション。
    config.enter_replay_transition = None

    ## Used when exiting a replay
    ## リプレイモードを終える時のトランジション。
    config.exit_replay_transition = None

    ## Used when the image is changed by a say statement with image attributes.
    ## キャラクターにイメージタグを関連付けている場合に、画像属性付きの
    ## say ステートメントで表示を置き換える時に行われるトランジション。
    config.say_attribute_transition = None


    #########################################
    ## This is the name of the directory where the game's data is
    ## stored. (It needs to be set early, before any other init code
    ## is run, so the persistent information can be found by the init code.)
    ## 以下の項目はゲームデータがセーブされるディレクトリ名です。
    ## （他の init コードで使用するデータを参照できるように、 全ての init コードより
    ## 前の python early でセットしておく必要があります。）

    ## 訳注：コメントアウトすると、ゲーム本体のディレクトリに置かれます。
    ## 開発中や、インストーラーなしで配布する場合、コメントアウトした方が
    ## 便利かもしれません。

python early:
    config.save_directory = "PROJECT_NAME-UNIQUE"

init -1 python hide:
    #########################################
    ## Default values of Preferences.
    ## 環境設定の初期値。

    ## Note: These options are only evaluated the first time a
    ## game is run. To have them run a second time, delete
    ## game/saves/persistent
    ## 注釈：以下のオプションはゲームが最初に起動した時にのみ
    ## 参照されます。 再び参照させたい場合は、 persistent data を
    ## 消去してください。

    ## 訳注：config で設定される値はセーブされませんが、設定はいつでも可能です。
    ## このため、ゲーム中に一時的に利用できるものもあります。

    ## Should we start in fullscreen mode?
    ## フルスクリーンモードで起動するかどうか。

    config.default_fullscreen = False

    ## The default text speed in characters per second. 0 is infinite.
    ## デフォルト文字表示速度。０だと無限に時間がかかります。

    config.default_text_cps = 0

    ## The default auto-forward time setting.
    ## 自動文字送りのデフォルト速度を設定します。

    config.default_afm_time = 10

    #########################################
    ## More customizations can go here.
    ## 他のカスタマイズは以下に記述します。
    ## 訳注：以下は原文にはない追加コードです。

    # テキストがウィンドウの許可された領域からはみ出ると text_overflow.txt
    # に記録します。
    # config.debug_text_overflow = False

    # オートリロードを有効化します。オートリロードが有効だと
    # スクリプト変更を検出し、自動でリロードします。
    # config.autoreload = False

    ## マウスホイールで読み進められるようにします。
    # config.keymap['dismiss'].append('mousedown_5')

    ## Mac と Lunux 用のウインドウアイコンを設定。
    # config.window_icon = None

    ## Windows 用のウインドウアイコンを設定。
    ## サイズは 32x32 でなければなりません。
    # config.windows_icon =None

    ## イメージキャッシュの最大値を設定。
    ## 極端に高すぎるとクラッシュする可能性があります。
    # config.image_cache_size = 8

    ## スキップ機能の設定。
    ## 一時的にスキップを止めたい場合、 config.skipping = None を使います。
    # config.allow_skipping = True

    ## スキップの速度を変更します。
    # config.skip_delay = 25

    ## > による高速スキップを開発者モード以外でも行うかどうか。
    # config.fast_skipping = False

    ## ロールバック機能の設定。
    ## 一時的にロールバックを止めたい場合 renpy.block_rollback() を使います。
    ## hard_rollback_limit は記録されるロールバックの量です。
    # config.rollback_enabled = True
    # config.hard_rollback_limit = 100

    ## セーブスロットのサムネイルサイズを変更します。
    # config.thumbnail_height = 75
    # config.thumbnail_width = 100

    ## キャラクターにイメージタグを関連付けて表示している場合、
    ## True に設定すると、画面に表示されてないキャラクターの画像のみが
    ## サイドイメージとして表示されます。
    # config.side_image_only_not_showing = False

    ## at 節を使わない場合に適応される transform を変更します。
    # config.default_transform = default

    ## デフォルトレイヤー。
    # config.layers = [ 'master',  'transient', 'screens', 'overlay' ]

    ## トップレイヤーの追加。
    ## トップレイヤーはトランジションの影響を受けません。
    # config.top_layers = [ ]

    ## ロールバックをノベルモード用に変更します。
    # config.nvl_paged_rollback = True

    ## 選択肢表示をノベルモードで行います。
    # menu = nvl_menu

    ## マウスドラッグでウィンドウサイズの変更が可能かどうか設定します。
    # config.gl_resize = True

    ## ゲーム起動時にウィンドウを中央に表示します。
    # import os
    # os.environ['SDL_VIDEO_CENTERED'] = '1'

    ## 音楽のフェードアウトの初期値を設定します。
    # config.fade_music = 0.0

    ## 次の項目を "{filename}.ogg" のように設定すると、
    ## test だけで test.ogg を再生できるようになります
    # config.voice_filename_format = "{filename}"

    ## デフォルトサウンドチャンネル
    ## file_prefix にパス名、file_suffix に拡張子を補うと、
    ## ファイル名のみで再生できるようになります。
    # renpy.music.register_channel("music", mixer="music" loop = True, file_prefix="", file_suffix="")
    # renpy.music.register_channel("sound", mixer="sfx", loop = False, file_prefix="", file_suffix="")
    # renpy.music.register_channel("voice", mixer="voice", loop = False, file_prefix="", file_suffix="")

    ## キーリピート
    ## (.3,.03) の場合、押しっぱなしにして.3秒後、.03秒間隔でリピートされます。
    # config.key_repeat = (.3, .03)


## This section contains information about how to build your project into
## distribution files.
## 以下ではディストリビューション作成のための情報を記載しています。

init python:

    ## The name that's used for directories and archive files. For example, if
    ## this is 'mygame-1.0', the windows distribution will be in the
    ## directory 'mygame-1.0-win', in the 'mygame-1.0-win.zip' file.
    ## ディレクトリとアーカイブの名前です。例えば、'mygame-1.0' の場合、
    ## ウィンドウズ用のディストリビューションは 'mygame-1.0-win.zip' となり、
    ## 展開すると 'mygame-1.0-win' となります。
    build.directory_name = "PROJECT_NAME-1.0"

    ## The name that's uses for executables - the program that users will run
    ## to start the game. For example, if this is 'mygame', then on Windows,
    ## users can click 'mygame.exe' to start the game.
    ## 実行ファイル - ゲームをスタートするプログラムの名前です。
    ## 例えば、'maygame' の場合、ウィンドウズでは 'mygame.exe' を
    ## クリックするとゲームがスタートします。
    build.executable_name = "PROJECT_NAME"

    ## If True, Ren'Py will include update information into packages. This
    ## allows the updater to run.
    ## True に設定すると、アップデート情報がパッケージに含まれます。
    ## アップデータを動作させるのに必要です。
    build.include_update = False

    ## File patterns:
    ## ファイルバターン

    ## The following functions take file patterns. File patterns are case-
    ## insensitive, and matched against the path relative to the base
    ## directory, with and without a leading /. If multiple patterns match,
    ## the first is used.
    ## 以下の機能ではファイルパターンを必要とします。
    ## ファイルパターンは大文字と小文字を区別しません。
    ## また、ベースディレクトリからの相対パスを / を用いて参照します。
    ## 適合するパターンが複数あれば、最初のものが優先されます。

    ## In a pattern:
    ## パターンにおいて、

    ## /
    ##     Is the directory separator.
    ##     これはディレクトリのセパレータを意味します。

    ## *
    ##     Matches all characters, except the directory separator.
    ##     これはセパレータを除く任意の文字列を意味します。

    ## **
    ##     Matches all characters, including the directory separator.
    ##     これはセパレータを含む任意の文字列を意味します。

    ## For example:
    ## 例えば、

    ## *.txt
    ##     Matches txt files in the base directory.
    ##     これはベースディレクトリにある任意の txt ファイル を意味します。

    ## game/**.ogg
    ##     Matches ogg files in the game directory or any of its subdirectories.
    ##     これは game ディレクトリ以下にある任意の ogg ファイルを意味します。

    ## **.psd
    ##    Matches psd files anywhere in the project.
    ##    これはプロジェクトにある全ての psd ファイルを意味します。

    ## Classify files as None to exclude them from the built distributions.
    ## None に分類したファイルはディストリビューションに含まれません。

    build.classify('**~', None)
    build.classify('**.bak', None)
    build.classify('**/.**', None)
    build.classify('**/#**', None)
    build.classify('**/thumbs.db', None)

    ## To archive files, classify them as 'archive'.
    ## アーカイブに含めるには、'archive' に分類します。

    # build.classify('game/**.png', 'archive')
    # build.classify('game/**.jpg', 'archive')

    ## Files matching documentation patterns are duplicated in a mac app
    ## build, so they appear in both the app and the zip file.
    ## documentation に適合するファイルは、mac 用ディストリビューション
    ## において、app と zip の双方に含まれます。

    build.documentation('*.html')
    build.documentation('*.txt')

