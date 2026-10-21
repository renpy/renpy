translate schinese strings:

    # gui/game/options.rpy:1
    old "## This file contains options that can be changed to customize your game."
    new "## 此文件包含有可自定义您游戏的设置。"

    # gui/game/options.rpy:4
    old "## Lines beginning with two '#' marks are comments, and you shouldn't uncomment them. Lines beginning with a single '#' mark are commented-out code, and you may want to uncomment them when appropriate."
    new "## 以两个“#”开头的行是注释，不应取消注释。以一个“#”开头的行是被注释掉的代码，可在需要时取消注释。"

    # gui/game/options.rpy:10
    old "## Basics"
    new "## 基础"

    # gui/game/options.rpy:12
    old "## A human-readable name of the game. This is used to set the default window title, and shows up in the interface and error reports."
    new "## 用户可读的游戏名称。此命令用来设置默认窗口标题，并且会在界面和错误报告中出现。"

    # gui/game/options.rpy:15
    old "## The _() surrounding the string marks it as eligible for translation."
    new "## 带有 _() 的字符串表示其可被翻译。"

    # gui/game/options.rpy:17
    old "Ren'Py 7 Default GUI"
    new "Ren'Py 7 默认 GUI"

    # gui/game/options.rpy:20
    old "## Determines if the title given above is shown on the main menu screen. Set this to False to hide the title."
    new "## 决定上方的标题是否显示在主菜单界面。设为 False 可隐藏标题。"

    # gui/game/options.rpy:26
    old "## The version of the game."
    new "## 游戏版本号。"

    # gui/game/options.rpy:31
    old "## Text that is placed on the game's about screen. Place the text between the triple-quotes, and leave a blank line between paragraphs."
    new "## 显示在游戏“关于”界面的文字。请将文字放在三引号之间，并在段落之间留出空行。"

    # gui/game/options.rpy:38
    old "## A short name for the game used for executables and directories in the built distribution. This must be ASCII-only, and must not contain spaces, colons, or semicolons."
    new "## 用于发行版中可执行文件和目录的游戏短名称。只能使用 ASCII 字符，且不得包含空格、冒号或分号。"

    # gui/game/options.rpy:45
    old "## Sounds and music"
    new "## 音效和音乐"

    # gui/game/options.rpy:47
    old "## These three variables control, among other things, which mixers are shown to the player by default. Setting one of these to False will hide the appropriate mixer."
    new "## 这三个变量控制哪些内置的混音器会默认显示给用户。将其中一个设置为 False 将隐藏对应的混音器。"

    # gui/game/options.rpy:56
    old "## To allow the user to play a test sound on the sound or voice channel, uncomment a line below and use it to set a sample sound to play."
    new "## 若要允许用户在音效或语音通道播放测试音频，请取消下面某行的注释，并设置要播放的示例音频。"

    # gui/game/options.rpy:63
    old "## Uncomment the following line to set an audio file that will be played while the player is at the main menu. This file will continue playing into the game, until it is stopped or another file is played."
    new "## 取消下面一行的注释可设置主菜单播放的音频文件。该文件会继续播放到游戏中，直到停止或播放其他文件。"

    # gui/game/options.rpy:70
    old "## Transitions"
    new "## 转场"

    # gui/game/options.rpy:72
    old "## These variables set transitions that are used when certain events occur. Each variable should be set to a transition, or None to indicate that no transition should be used."
    new "## 这些变量用来控制某些事件发生时的转场。每一个变量都应设置成一个转场，或者是 None 来表示无转场。"

    # gui/game/options.rpy:76
    old "## Entering or exiting the game menu."
    new "## 进入或退出游戏菜单。"

    # gui/game/options.rpy:82
    old "## Between screens of the game menu."
    new "## 各个游戏菜单之间的转场。"

    # gui/game/options.rpy:87
    old "## A transition that is used after a game has been loaded."
    new "## 载入游戏后使用的转场。"

    # gui/game/options.rpy:92
    old "## Used when entering the main menu after the game has ended."
    new "## 在游戏结束之后进入主菜单时使用的转场。"

    # gui/game/options.rpy:97
    old "## A variable to set the transition used when the game starts does not exist. Instead, use a with statement after showing the initial scene."
    new "## 没有用于设置游戏开始时转场的变量。请在显示初始场景后使用 with 语句。"

    # gui/game/options.rpy:102
    old "## Window management"
    new "## 窗口管理"

    # gui/game/options.rpy:104
    old "## This controls when the dialogue window is displayed. If \"show\", it is always displayed. If \"hide\", it is only displayed when dialogue is present. If \"auto\", the window is hidden before scene statements and shown again once dialogue is displayed."
    new "## 控制对话窗口何时显示。设为 \"show\" 时始终显示；设为 \"hide\" 时仅在有对话时显示；设为 \"auto\" 时在 scene 语句前隐藏，并在显示对话后再次显示。"

    # gui/game/options.rpy:109
    old "## After the game has started, this can be changed with the \"window show\", \"window hide\", and \"window auto\" statements."
    new "## 在游戏开始后，可以用 window show、window hide 和 window auto 语句来改变其状态。"

    # gui/game/options.rpy:115
    old "## Transitions used to show and hide the dialogue window"
    new "## 用于显示和隐藏对话框窗口的转场"

    # gui/game/options.rpy:121
    old "## Preference defaults"
    new "## 默认设置"

    # gui/game/options.rpy:123
    old "## Controls the default text speed. The default, 0, is infinite, while any other number is the number of characters per second to type out."
    new "## 控制默认文字速度。默认值 0 表示瞬间显示，其他数值表示每秒显示的字符数。"

    # gui/game/options.rpy:129
    old "## The default auto-forward delay. Larger numbers lead to longer waits, with 0 to 30 being the valid range."
    new "## 默认自动推进延迟。数值越大等待越久，有效范围为 0 到 30。"

    # gui/game/options.rpy:135
    old "## Save directory"
    new "## 存档目录"

    # gui/game/options.rpy:137
    old "## Controls the platform-specific place Ren'Py will place the save files for this game. The save files will be placed in:"
    new "## 控制 Ren'Py 放置游戏存档的特定操作系统目录。存档文件将放置在："

    # gui/game/options.rpy:140
    old "## Windows: %APPDATA\\RenPy\\<config.save_directory>"
    new "## Windows：%APPDATA\\RenPy\\<config.save_directory>"

    # gui/game/options.rpy:142
    old "## Macintosh: $HOME/Library/RenPy/<config.save_directory>"
    new "## Macintosh：$HOME/Library/RenPy/<config.save_directory>"

    # gui/game/options.rpy:144
    old "## Linux: $HOME/.renpy/<config.save_directory>"
    new "## Linux：$HOME/.renpy/<config.save_directory>"

    # gui/game/options.rpy:146
    old "## This generally should not be changed, and if it is, should always be a literal string, not an expression."
    new "## 通常不应更改此项；如果更改，必须使用字面字符串，而不是表达式。"

    # gui/game/options.rpy:152
    old "## Icon"
    new "## 图标"

    # gui/game/options.rpy:154
    old "## The icon displayed on the taskbar or dock."
    new "## 在任务栏或 Dock 上显示的图标。"

    # gui/game/options.rpy:159
    old "## Build configuration"
    new "## 构建配置"

    # gui/game/options.rpy:161
    old "## This section controls how Ren'Py turns your project into distribution files."
    new "## 此部分控制 Ren'Py 如何将项目生成发行文件。"

    # gui/game/options.rpy:166
    old "## The following functions take file patterns. File patterns are case- insensitive, and matched against the path relative to the base directory, with and without a leading /. If multiple patterns match, the first is used."
    new "## 以下函数接受文件模式。文件模式不区分大小写，并与基础目录的相对路径相匹配，包括或不包括 /。如果多个模式匹配，则使用第一个模式。"

    # gui/game/options.rpy:171
    old "## In a pattern:"
    new "## 在一个模式中："

    # gui/game/options.rpy:173
    old "## / is the directory separator."
    new "## / 是目录分隔符。"

    # gui/game/options.rpy:175
    old "## * matches all characters, except the directory separator."
    new "## * 匹配所有字符，目录分隔符除外。"

    # gui/game/options.rpy:177
    old "## ** matches all characters, including the directory separator."
    new "## ** 匹配所有字符，包括目录分隔符。"

    # gui/game/options.rpy:179
    old "## For example, \"*.txt\" matches txt files in the base directory, \"game/**.ogg\" matches ogg files in the game directory or any of its subdirectories, and \"**.psd\" matches psd files anywhere in the project."
    new "## 例如，“*.txt”匹配基础目录中的 txt 文件，“game/**.ogg”匹配游戏目录或任何子目录中的 ogg 文件，“**.psd”匹配项目中任何位置的 psd 文件。"

    # gui/game/options.rpy:183
    old "## Classify files as None to exclude them from the built distributions."
    new "## 将文件归类为 None 可将其排除在生成的发行文件之外。"

    # gui/game/options.rpy:191
    old "## To archive files, classify them as 'archive'."
    new "## 若要将文件打包进归档，请将其归类为 'archive'。"

    # gui/game/options.rpy:196
    old "## Files matching documentation patterns are duplicated in a mac app build, so they appear in both the app and the zip file."
    new "## 匹配为文档模式的文件会在 Mac 应用程序构建中被复制，因此它们同时出现在 APP 和 ZIP 文件中。"

    # gui/game/options.rpy:203
    old "## A Google Play license key is required to perform in-app purchases. It can be found in the Google Play developer console, under \"Monetize\" > \"Monetization Setup\" > \"Licensing\"."
    new "## 执行应用内购需要一个 Google Play 许可密钥。许可密钥可以在 Google Play 开发者控制台的“Monetize” > “Monetization Setup” > “Licensing”页面找到。"

    # gui/game/options.rpy:210
    old "## The username and project name associated with an itch.io project, separated by a slash."
    new "## 与 itch.io 项目相关的用户名和项目名，以 / 分隔。"
