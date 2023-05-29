translate schinese strings:

    # gui/game/options.rpy:1
    old "## This file contains options that can be changed to customize your game."
    new "## 此文件包含有可自定义您游戏的设置。"

    # gui/game/options.rpy:4
    old "## Lines beginning with two '#' marks are comments, and you shouldn't uncomment them. Lines beginning with a single '#' mark are commented-out code, and you may want to uncomment them when appropriate."
    new "## 以“##”开头的语句是注释，您不应该对其取消注释。以“#”开头的语句是注释掉的代码，在适用的时候您可能需要对其取消注释。"

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
    new "## 决定上面给出的标题是否显示在标题界面屏幕。设置为 False 来隐藏标题。"

    # gui/game/options.rpy:26
    old "## The version of the game."
    new "## 游戏版本号。"

    # gui/game/options.rpy:31
    old "## Text that is placed on the game's about screen. Place the text between the triple-quotes, and leave a blank line between paragraphs."
    new "## 放置在游戏内“关于”屏幕上的文本。将文本放在三个引号之间，并在段落之间留出空行。"

    # gui/game/options.rpy:38
    old "## A short name for the game used for executables and directories in the built distribution. This must be ASCII-only, and must not contain spaces, colons, or semicolons."
    new "## 在构建的发布版中，可执行文件和目录所使用的短名称。此处仅限使用 ASCII 字符，并且不能包含空格、冒号或分号。"

    # gui/game/options.rpy:45
    old "## Sounds and music"
    new "## 音效和音乐"

    # gui/game/options.rpy:47
    old "## These three variables control, among other things, which mixers are shown to the player by default. Setting one of these to False will hide the appropriate mixer."
    new "## 这三个变量控制哪些内置的混音器会默认显示给用户。将其中一个设置为 False 将隐藏对应的混音器。"

    # gui/game/options.rpy:56
    old "## To allow the user to play a test sound on the sound or voice channel, uncomment a line below and use it to set a sample sound to play."
    new "## 为了让用户在音效或语音轨道上播放测试音频，请取消对下面一行的注释并设置播放的样本声音。"

    # gui/game/options.rpy:63
    old "## Uncomment the following line to set an audio file that will be played while the player is at the main menu. This file will continue playing into the game, until it is stopped or another file is played."
    new "## 将以下语句取消注释就可以设置标题界面播放的背景音乐文件。此文件将在整个游戏中持续播放，直至音乐停止或其他文件开始播放。"

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
    new "## 用于控制在游戏开始标签不存在时转场的变量。作为替代，在显示初始化场景后使用 with 语句。"

    # gui/game/options.rpy:102
    old "## Window management"
    new "## 窗口管理"

    # gui/game/options.rpy:104
    old "## This controls when the dialogue window is displayed. If \"show\", it is always displayed. If \"hide\", it is only displayed when dialogue is present. If \"auto\", the window is hidden before scene statements and shown again once dialogue is displayed."
    new "## 此命令控制对话框窗口何时显示。若为 show，对话框将总是显示。若为 hide，对话框仅在对话出现时显示。若为 auto，对话框会在 scene 语句前隐藏，并在有新对话时重新显示。"

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
    new "## 控制默认的文字显示速度。默认的 0 为瞬间，而其他数字则是每秒显示出的字符数。"

    # gui/game/options.rpy:129
    old "## The default auto-forward delay. Larger numbers lead to longer waits, with 0 to 30 being the valid range."
    new "## 默认的自动前进延迟。数字越大，等待时间越长，有效范围为 0 - 30。"

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
    new "## 该语句通常不应变更，若要变更，应为有效字符串而不是表达式。"

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
    new "## 此部分控制 Ren'Py 如何将您的项目转变为发行版文件。"

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
    new "## 将文件列为 None 来使其从构建的发行版中排除。"

    # gui/game/options.rpy:191
    old "## To archive files, classify them as 'archive'."
    new "## 若要封装文件，需将其列为“archive”。"

    # gui/game/options.rpy:196
    old "## Files matching documentation patterns are duplicated in a mac app build, so they appear in both the app and the zip file."
    new "## 匹配为文档模式的文件会在 Mac 应用程序构建中被复制，因此它们同时出现在 APP 和 ZIP 文件中。"

    # gui/game/options.rpy:203
    old "## A Google Play license key is required to perform in-app purchases. It can be found in the Google Play developer console, under \"Monetize\" > \"Monetization Setup\" > \"Licensing\"."
    new "## 执行应用内购需要一个 Google Play 许可密钥。许可密钥可以在 Google Play 开发者控制台的“Monetize” > “Monetization Setup” > “Licensing”页面找到。"

    # gui/game/options.rpy:210
    old "## The username and project name associated with an itch.io project, separated by a slash."
    new "## 与 itch.io 项目相关的用户名和项目名，以 / 分隔。"
