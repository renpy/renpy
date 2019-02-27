translate simplified_chinese strings:

    # options.rpy:1
    old "## This file contains options that can be changed to customize your game."
    new "## 此文件包含有可自定义您游戏的设置。"

    # options.rpy:4
    old "## Lines beginning with two '#' marks are comments, and you shouldn't uncomment them. Lines beginning with a single '#' mark are commented-out code, and you may want to uncomment them when appropriate."
    new "## 以“##”开头的语句是注释，您不应该对其取消注释。以“#”开头的语句是注释掉的代码，在适用的时候您可能需要对其取消注释。"

    # options.rpy:10
    old "## Basics"
    new "## 基础"

    # options.rpy:12
    old "## A human-readable name of the game. This is used to set the default window title, and shows up in the interface and error reports."
    new "## 用户可读的游戏名称。此命令用来设置默认窗口标题，并且会在界面和错误报告中出现。"

    # options.rpy:15
    old "## The _() surrounding the string marks it as eligible for translation."
    new "## 带有 _() 的字符串表示其可被翻译。"

    # options.rpy:17
    old "Ren'Py 7 Default GUI"
    new "Ren'Py 7 默认 GUI"

    # options.rpy:20
    old "## Determines if the title given above is shown on the main menu screen. Set this to False to hide the title."
    new "## 决定上面给出的标题是否显示在主界面屏幕。设置为 False 来隐藏标题。"

    # options.rpy:26
    old "## The version of the game."
    new "## 游戏版本号。"

    # options.rpy:31
    old "## Text that is placed on the game's about screen. Place the text between the triple-quotes, and leave a blank line between paragraphs."
    new "## 放置在游戏“关于”屏幕的文本。将文本放在三个引号之间，并在段落之间留一个空行。"

    # options.rpy:38
    old "## A short name for the game used for executables and directories in the built distribution. This must be ASCII-only, and must not contain spaces, colons, or semicolons."
    new "## 在生成的发布版中，可执行文件和目录所使用的短名称。此处必须是仅 ASCII 字符，并且不得包含空格、冒号和分号。"

    # options.rpy:45
    old "## Sounds and music"
    new "## 音效和音乐"

    # options.rpy:47
    old "## These three variables control which mixers are shown to the player by default. Setting one of these to False will hide the appropriate mixer."
    new "## 这三个变量控制默认显示给用户的混音器。任一设置为 False 将隐藏对应的混音器。"

    # options.rpy:56
    old "## To allow the user to play a test sound on the sound or voice channel, uncomment a line below and use it to set a sample sound to play."
    new "## 允许用户在音效或语音轨道上播放测试音频文件，将以下语句取消注释并设置样音就可以使用。"

    # options.rpy:63
    old "## Uncomment the following line to set an audio file that will be played while the player is at the main menu. This file will continue playing into the game, until it is stopped or another file is played."
    new "## 将以下语句取消注释就可以设置主界面播放的背景音乐文件。此文件将在整个游戏中持续播放，直至音乐停止或其他文件开始播放。"

    # options.rpy:70
    old "## Transitions"
    new "## 转场"

    # options.rpy:72
    old "## These variables set transitions that are used when certain events occur. Each variable should be set to a transition, or None to indicate that no transition should be used."
    new "## 这些变量用来控制某些事件发生时的转场。每一个变量都应设置成一个转场，或者是 None 来表示无转场。"

    # options.rpy:76
    old "## Entering or exiting the game menu."
    new "## 进入或退出游戏菜单。"

    # options.rpy:82
    old "## Between screens of the game menu."
    new "## 各个游戏菜单之间的转场。"

    # options.rpy:87
    old "## A transition that is used after a game has been loaded."
    new "## 载入游戏后使用的转场。"

    # options.rpy:92
    old "## Used when entering the main menu after the game has ended."
    new "## 在游戏结束之后进入主菜单时使用的转场。"

    # options.rpy:97
    old "## A variable to set the transition used when the game starts does not exist. Instead, use a with statement after showing the initial scene."
    new "## 用于控制在游戏开始标签不存在时转场的变量。作为替代，在显示初始化场景后使用 with 声明。"

    # options.rpy:102
    old "## Window management"
    new "## 窗口管理"

    # options.rpy:104
    old "## This controls when the dialogue window is displayed. If \"show\", it is always displayed. If \"hide\", it is only displayed when dialogue is present. If \"auto\", the window is hidden before scene statements and shown again once dialogue is displayed."
    new "## 此命令控制对话框窗口何时显示。如果是“show”，对话框将永远显示。如果是“hide”，仅在存在对话时显示。如果是“auto”，对话框会在 scene 声明前隐藏，并在有新对话时重新显示。"

    # options.rpy:109
    old "## After the game has started, this can be changed with the \"window show\", \"window hide\", and \"window auto\" statements."
    new "## 在游戏开始后，此变量可通过“window show”、“window hide”和“window auto”声明来改变。"

    # options.rpy:115
    old "## Transitions used to show and hide the dialogue window"
    new "## 用于显示和隐藏对话框窗口的转场"

    # options.rpy:121
    old "## Preference defaults"
    new "## 默认设置"

    # options.rpy:123
    old "## Controls the default text speed. The default, 0, is infinite, while any other number is the number of characters per second to type out."
    new "## 控制默认的文字显示速度。默认的 0 是瞬间，而其他数字则是每秒显示出的字符数。"

    # options.rpy:129
    old "## The default auto-forward delay. Larger numbers lead to longer waits, with 0 to 30 being the valid range."
    new "## 默认的自动前进延迟。越大的数字会产生越长的等待，有效范围为 0 - 30。"

    # options.rpy:135
    old "## Save directory"
    new "## 存档目录"

    # options.rpy:137
    old "## Controls the platform-specific place Ren'Py will place the save files for this game. The save files will be placed in:"
    new "## 控制 Ren'Py 为此游戏放置存档的，基于平台的特定目录。存档文件将放置在："

    # options.rpy:140
    old "## Windows: %APPDATA\\RenPy\\<config.save_directory>"
    new "## Windows：%APPDATA\\RenPy\\<config.save_directory>"

    # options.rpy:142
    old "## Macintosh: $HOME/Library/RenPy/<config.save_directory>"
    new "## Macintosh：$HOME/Library/RenPy/<config.save_directory>"

    # options.rpy:144
    old "## Linux: $HOME/.renpy/<config.save_directory>"
    new "## Linux：$HOME/.renpy/<config.save_directory>"

    # options.rpy:146
    old "## This generally should not be changed, and if it is, should always be a literal string, not an expression."
    new "## 该命令一般不应变更，若要变更，应为有效字符串而不是表达式。"

    # options.rpy:152
    old "## Icon"
    new "## 图标"

    # options.rpy:154
    old "## The icon displayed on the taskbar or dock."
    new "## 在任务栏或 Dock 上显示的图标。"

    # options.rpy:159
    old "## Build configuration"
    new "## 生成配置"

    # options.rpy:161
    old "## This section controls how Ren'Py turns your project into distribution files."
    new "## 这部分控制 Ren'Py 如何将您的工程转变为发行版文件。"

    # options.rpy:166
    old "## The following functions take file patterns. File patterns are case- insensitive, and matched against the path relative to the base directory, with and without a leading /. If multiple patterns match, the first is used."
    new "## 以下功能为指定文件模式。文件模式大小写不敏感，且匹配基础目录相关的路径，包括或不包括 /。如果多个文件模式匹配，将执行第一个。"

    # options.rpy:171
    old "## In a pattern:"
    new "## 在一个文件模式中："

    # options.rpy:173
    old "## / is the directory separator."
    new "## / 是目录分隔符。"

    # options.rpy:175
    old "## * matches all characters, except the directory separator."
    new "## * 匹配所有字符，目录分隔符除外。"

    # options.rpy:177
    old "## ** matches all characters, including the directory separator."
    new "## ** 匹配所有字符，包括目录分隔符。"

    # options.rpy:179
    old "## For example, \"*.txt\" matches txt files in the base directory, \"game/**.ogg\" matches ogg files in the game directory or any of its subdirectories, and \"**.psd\" matches psd files anywhere in the project."
    new "## 例如，“*.txt”匹配基础目录中所有的 txt 文件，“game/**.ogg”匹配所有的游戏目录或子目录中的 ogg 文件，“**.psd”匹配工程中任何位置的 psd 文件。"

    # options.rpy:183
    old "## Classify files as None to exclude them from the built distributions."
    new "## 将文件列为 None 来使其从已生成的分发版中排除。"

    # options.rpy:191
    old "## To archive files, classify them as 'archive'."
    new "## 若要打包文件，需将其列为“archive”。"

    # options.rpy:196
    old "## Files matching documentation patterns are duplicated in a mac app build, so they appear in both the app and the zip file."
    new "## 匹配为文档模式的文件，将在 Mac 应用的生成中复制，因此它们同时存在于 app 和 zip 文件中。"

    # options.rpy:202
    old "## Set this to a string containing your Apple Developer ID Application to enable codesigning on the Mac. Be sure to change it to your own Apple-issued ID."
    new "## 在 Mac 上将此设置为包含有您 Apple Developer ID Application 的字符串来启用代码签名。确保将其更改为您自己的，由苹果签发的 ID。"

    # options.rpy:209
    old "## A Google Play license key is required to download expansion files and perform in-app purchases. It can be found on the \"Services & APIs\" page of the Google Play developer console."
    new "## 需要一个 Google Play 授权密钥来下载扩展文件并执行应用内购。授权密钥可以在 Google Play 开发者控制台的“服务和 API”页面找到。"

    # options.rpy:216
    old "## The username and project name associated with an itch.io project, separated by a slash."
    new "## 与 itch.io 工程关联的用户名和工程名，以斜杠分隔。"
