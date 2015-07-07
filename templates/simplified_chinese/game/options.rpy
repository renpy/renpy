## 本文件包含部分可用于修改与定制的选项代码，
## 它将会起作用于您的游戏之中。但这只是很多选项中的一部分，
## 您还可以对它进行很多自由的添加与修改。
##
## 以两个“#”号开头的行是注释行，您不应该清除这些注释。
## 而以单个“#”号开头的行是反注释或备用参数，您可以在有必要的时候
## 选择清除掉这些行
##
## 译注：Ren'py引擎对空格等符号有着严格的要求，并且不能识别Tab制表符，
## 无论是在此输入参数，还是今后编辑游戏脚本时，请务必小心空格的数量，
## 同时不能存在Tab制表符，否则将会导致整个工程无法启动！

init -1 python hide:

    ## 此选项可供调整开发者工具的开关，
    ## 在游戏正式发布之前，应设置为False，
    ## 以避免用户使用开发者工具进行游戏作弊。

    config.developer = True

    ## 此选项控制游戏窗口的分辨率。

    config.screen_width = 800
    config.screen_height = 600

    ## 当Ren'py项目以窗口化运行时，
    ## 此选项控制窗口的标题名称。
    ## 译注：需要命名为非英文字符时，需要在双引号前加“u”以表示Unicode字符，
    ## 但即使命名为英文名称也不一定需要将“u”去掉。

    config.window_title = u"PROJECT_NAME"

    # 此选项控制游戏的名称与版本号，
    # 并将它们反馈至debug工具与日志中。
    #
    # 译注：此选项通常针对开发者，SDK主界面的项目名称、开发过程中的traceback.txt、
    # 编译时的可执行程序名称、以及压缩包名称中会有所体现，但与上述窗口标题无关。
    config.name = "PROJECT_NAME"
    config.version = "0.0"

    #########################################
    # 主题

    ## 接着，我们就希望使用到主题功能。theme.roundrect
    ## 代表着使用圆角矩形特性的主题。
    ##
    ## 主题功能拥有几个参数
    ## 可使您对主题进行一定的自定义。

    theme.roundrect(

        ## 空闲控件的颜色。
        ## 译注：控件通常体现在按钮上，此处为鼠标指针未指向时的颜色。
        widget = "#003c78",

        ## 被指向控件的颜色。
        widget_hover = "#0050a0",

        ## 控件内文本颜色。
        widget_text = "#c8ffff",

        ## 被选中控件内的文本颜色。
        ## 例：当前使用的参数。
        widget_selected = "#ffffc8",

        ## 被屏蔽控件的颜色。
        disabled = "#404040",

        ## 被屏蔽控件内文本的颜色。
        disabled_text = "#c8c8c8",

        ## 信息框内的文本颜色。
        label = "#ffffff",

        ## 含框架的控件颜色。
        frame = "#6496c8",

        ## 若设置为True，则游戏内窗口显示为圆角。
        ## 若为False，则游戏内窗口显示为矩形。
        rounded_window = False,

        ## 主菜单的背景。
        ## 此处可以以“#”开头代表一个颜色，或引用一个文件。
        ## 切记，图片文件的分辨率要与实际窗口的分辨率相同。
        mm_root = "#dcebff",

        ## 游戏内菜单的背景。
        ## 使用方法与注意事项同上。
        gm_root = "#dcebff",

        ## 主题的设置到此结束。
        ## 主题控制着多个可视性效果，若需要修改，
        ## 请参见下方参数。
        )


    #########################################
    ## 此处的设定可允许您修改含有对话或旁白的文本框背景。
    ## 通过引用一个文件来修改它。

    ## 文本框的背景。在Frame后的括号中，两个数字分别代表
    ## 左右边距和上下边距。

    # style.window.background = Frame("frame.png", 12, 12)

    ## 留边参数是环绕在游戏窗口周围的区域，
    ## 这些部分是不会显示背景的。

    # style.window.left_margin = 6
    # style.window.right_margin = 6
    # style.window.top_margin = 6
    # style.window.bottom_margin = 6

    ## 填充参数是游戏窗口内的区域，
    ## 这些部分会显示背景。
    ##
    ## 译注：留边与填充参数极少使用，参数后的数字指的是厚度。

    # style.window.left_padding = 6
    # style.window.right_padding = 6
    # style.window.top_padding = 6
    # style.window.bottom_padding = 6

    ## 此参数控制窗口最低高度，并包含留边与填充参数。

    # style.window.yminimum = 250


    #########################################
    ## 此处参数可使您修改主菜单放置的位置。

    ## 此参数的原理是在可视化元素内寻找一个定位点(anchor)，
    ## 以及在游戏屏幕上寻找一个位置点(pos)。
    ## 接着我们会将两个点进行重合。
    ## 
    ## 译注：可视化元素内的定位点可假想为一个图片中指定的点，
    ## 当pos参数指定一个游戏窗口内的位置（点）后，
    ## 引擎便会将图片中指定的点与窗口中指定好的点进行重合放置。
    ## 默认情况下，两轴的anchor都为0.5时，定位点位于可视化元素中心。

    ## 定位点与位置点均可使用整数或小数表达。
    ## 如果设置为整数，则会被理解为距离左上角的像素数量。
    ## 如果设置为小数，则会被理解为游戏窗口分数化的位置。
    ## 
    ## 译注：分数化位置不难理解，如0.5，则代表游戏窗口的二分之一处，
    ## 此时xy两轴依旧有效。

    # style.mm_menu_frame.xpos = 0.5
    # style.mm_menu_frame.xanchor = 0.5
    # style.mm_menu_frame.ypos = 0.75
    # style.mm_menu_frame.yanchor = 0.5


    #########################################
    ## 此处可修改Ren'py游戏内的默认字体。

    ## 引用一个字体文件。

    style.default.font = "tl/None/DroidSansFallback.ttf"
    style._default.font = "tl/None/DroidSansFallback.ttf"

    ## 修改字体大小。

    # style.default.size = 22

    ## 注意此参数仅能修改部分字体的大小，
    ## 一些按钮拥有它们自己的风格参数。


    #########################################
    ## 此参数可使您修改Ren'py游戏内使用的一些声音。

    ## 若为False，您的游戏内将不会包含任何声音效果。

    config.has_sound = True

    ## 若您的游戏内不包含任何音乐，请设置为False。

    config.has_music = True

    ## 若您的游戏含有人物语音，请设置为True。

    config.has_voice = False

    ## 设置在您点击按钮和图片映射时的效果音。

    # style.button.activate_sound = "click.wav"
    # style.imagemap.activate_sound = "click.wav"

    ## 设置在您进入和退出游戏内菜单时的声音效果。

    # config.enter_sound = "click.wav"
    # config.exit_sound = "click.wav"

    ## 设置一个声音用于测试音量大小。

    # config.sample_sound = "click.wav"

    ## 设置用户位于主菜单时的音乐。

    # config.main_menu_music = "main_menu_theme.ogg"


    #########################################
    ## 帮助

    ## 此参数可让您控制Ren'py游戏内的“帮助”选项。
    ## 它可以是：
    ## - 脚本中的一个label，用于在点击后向用户显示一段帮助。
    ## - 游戏根目录下的一个文件，点击后将会打开网页浏览器。
    ## - 若为None，则关闭此功能。
    ##
    ## 译注：label通常用于游戏剧情脚本，如script.rpy中，label start:
    ## 指的就是点击开始游戏时指向的label。label中可包含对话、旁白、
    ## 选项、背景、声音等参数。
    config.help = "README.html"


    #########################################
    ## 转场特效

    ## 从游戏中进入游戏内菜单时的转场特效。
    config.enter_transition = None

    ## 退出菜单回到游戏时的转场特效。
    config.exit_transition = None

    ## 在游戏菜单内进行切换时的转场特效。
    config.intra_transition = None

    ## 从主菜单进入游戏内菜单时的转场特效。
    config.main_game_transition = None

    ## 退出菜单回到主菜单时的转场特效。
    config.game_main_transition = None

    ## 从封面进入主菜单时的转场特效。
    ## 译注：封面(splashscreen)指的是打开游戏时
    ## 先看到的一些发行商图片或游戏宣传视频等。
    ## 封面需要另外添加代码实现，请参见官方文档。
    config.end_splash_transition = None

    ## 当游戏结束时返回主菜单的转场特效。
    config.end_game_transition = None

    ## 当一个进度被加载时的转场特效。
    config.after_load_transition = None

    ## 当一个游戏内窗口显示时的转场特效。
    ## 译注：游戏内窗口多指文本框。
    config.window_show_transition = None

    ## 当一个游戏内窗口被隐藏时的转场特效。
    config.window_hide_transition = None

    ## 当显示完ADV模式下的文本后直接转为NVL模式文本时的转场特效。
    ## 译注：ADV模式是指文本位于屏幕底部文本框中的游戏模式，
    ## NVL模式是指文本全屏显示的游戏模式。
    config.adv_nvl_transition = dissolve

    ## 当显示完NVL模式的文本后直接转为ADV模式文本时的转场特效。
    config.nvl_adv_transition = dissolve

    ## 当确认取消按钮出现时的转场特效。
    config.enter_yesno_transition = None

    ## 当确认取消按钮隐藏时的转场特效
    config.exit_yesno_transition = None

    ## 当进入回放时的转场特效。
    config.enter_replay_transition = None

    ## 当退出回放时的转场特效。
    config.exit_replay_transition = None

    ## 当图像被say参数附带属性进行修改时的转场特效。
    config.say_attribute_transition = None

    #########################################
    ## 此处可使您修改游戏存档数据存放的目录。
    ## 这需要在游戏开发之初，在任何init代码都未被运行之前就进行设置，
    ## 以便在init中找到正确的永久性数据信息。
python early:
    config.save_directory = "PROJECT_NAME-UNIQUE"

init -1 python hide:
    #########################################
    ## 环境设置中的默认选项。

    ## 注意：这些选项仅会在第一次运行游戏时生效。
    ## 若需要再生效一次，请删除：
    ## game/saves/persistent

    ## 是否开启全屏幕模式？

    config.default_fullscreen = False

    ## 默认的每秒显示文字数量，0为无限。

    config.default_text_cps = 0

    ## 默认的自动阅读模式等待时间。

    config.default_afm_time = 10

    #########################################
    ## 您可以从此处开始进行更多的自定义设置。
