
translate simplified_chinese strings:

    # about.rpy:39
    old "[version!q]"
    new "[version!q]"

    # about.rpy:43
    old "View license"
    new "查看许可证"

    # add_file.rpy:28
    old "FILENAME"
    new "文件名"

    # add_file.rpy:28
    old "Enter the name of the script file to create."
    new "请输入文件名来创建脚本文件。"

    # add_file.rpy:31
    old "The filename must have the .rpy extension."
    new "文件必须以 .rpy 为扩展名。"

    # add_file.rpy:39
    old "The file already exists."
    new "文件已存在。"

    # add_file.rpy:42
    old "# Ren'Py automatically loads all script files ending with .rpy. To use this\n# file, define a label and jump to it from another file.\n"
    new "# Ren'Py 自动加载所有扩展名为 .rpy 的脚本。要使用此\n# 文件，请先从其他文件中定义一个标签并跳转过来。\n"

    # android.rpy:30
    old "To build Android packages, please download RAPT, unzip it, and place it into the Ren'Py directory. Then restart the Ren'Py launcher."
    new "要生成安卓应用包，请下载 RAPT，并解压到 Ren'Py 目录中。之后重启 Ren'Py。"

    # android.rpy:31
    old "A Java 8 Development Kit is required to build Android packages on Windows. The JDK is different from the JRE, so it's possible you have Java without having the JDK.\n\nPlease {a=http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html}download and install the JDK{/a}, then restart the Ren'Py launcher."
    new "要在 Windows 中创建安卓应用包，您需要 Java 8 开发套件（JDK）。JDK 不同于 JRE，所以您可能已安装过 Java 但尚未安装 JDK。\n\n请{a=http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html}下载并安装 JDK{/a}，然后重启 Ren'Py。"

    # android.rpy:32
    old "RAPT has been installed, but you'll need to install the Android SDK before you can build Android packages. Choose Install SDK to do this."
    new "RAPT 已安装，但您还需要安装安卓 SDK 才可以生成安卓应用包。请继续安装 SDK。"

    # android.rpy:33
    old "RAPT has been installed, but a key hasn't been configured. Please create a new key, or restore android.keystore."
    new "RAPT 已完成安装，但密钥尚未进行过配置。请创建一个新密钥，或恢复 android.keystore 文件。"

    # android.rpy:34
    old "The current project has not been configured. Use \"Configure\" to configure it before building."
    new "当前工程尚未配置过。请在生成前使用“配置”来进行配置。"

    # android.rpy:35
    old "Choose \"Build\" to build the current project, or attach an Android device and choose \"Build & Install\" to build and install it on the device."
    new "选择“生成”来生成当前工程，或者在添加安卓设备之后，选择“生成并安装”来生成并安装到设备中。"

    # android.rpy:37
    old "Attempts to emulate an Android phone.\n\nTouch input is emulated through the mouse, but only when the button is held down. Escape is mapped to the menu button, and PageUp is mapped to the back button."
    new "尝试模拟为安卓手机。\n\n鼠标将仅在按键按下时模拟为触屏输入。Esc 和 PageUp 键将分别重映射为手机的菜单键和返回键。"

    # android.rpy:38
    old "Attempts to emulate an Android tablet.\n\nTouch input is emulated through the mouse, but only when the button is held down. Escape is mapped to the menu button, and PageUp is mapped to the back button."
    new "尝试模拟为安卓平板。\n\nEsc 和 PageUp 键将分别重映射为平板的菜单键和返回键。"

    # android.rpy:39
    old "Attempts to emulate a televison-based Android console, like the OUYA or Fire TV.\n\nController input is mapped to the arrow keys, Enter is mapped to the select button, Escape is mapped to the menu button, and PageUp is mapped to the back button."
    new "尝试模拟为基于电视的安卓平台，例如 OUYA 或 Fire TV。\n\n键盘方向键将重映射为手柄方向键，Enter、Esc 和 PageUp 键将分别重映射为手柄的选择键、菜单键和返回键。"

    # android.rpy:41
    old "Downloads and installs the Android SDK and supporting packages. Optionally, generates the keys required to sign the package."
    new "下载并安装安卓 SDK 以及支持包。另外，生成密钥后才能对应用包进行签名。"

    # android.rpy:42
    old "Configures the package name, version, and other information about this project."
    new "配置应用包名称、版本号以及关于此工程的一些其他信息。"

    # android.rpy:43
    old "Opens the file containing the Google Play keys in the editor.\n\nThis is only needed if the application is using an expansion APK. Read the documentation for more details."
    new "在编辑器中打开包含有 Google Play 密钥的文件。\n\n仅当您的应用使用了扩展 APK 时才需要进行此操作。更多详情请参阅说明文档。"

    # android.rpy:44
    old "Builds the Android package."
    new "生成安卓应用包。"

    # android.rpy:45
    old "Builds the Android package, and installs it on an Android device connected to your computer."
    new "生成安卓应用包，并将其安装到连接至此计算机的安卓设备中。"

    # android.rpy:46
    old "Builds the Android package, installs it on an Android device connected to your computer, then launches the app on your device."
    new "生成安卓应用包，将其安装到连接至此计算机的安卓设备中，并在您的设备上打开此应用。"

    # android.rpy:48
    old "Retrieves the log from the Android device and writes it to a file."
    new "从安卓设备接收日志并将其写入至文件。"

    # android.rpy:50
    old "Selects the Debug build, which can be accessed through Android Studio. Changing between debug and release builds requires an uninstall from your device."
    new "选择构建调试版，可经由 Android Studio 访问。切换调试版和发布版需要从您的设备卸载应用。"

    # android.rpy:51
    old "Selects the Release build, which can be uploaded to stores. Changing between debug and release builds requires an uninstall from your device."
    new "选择构建发布版，可上传至商店。切换调试版和发布版需要从您的设备卸载应用。"

    # android.rpy:245
    old "Copying Android files to distributions directory."
    new "正在复制安卓文件到分发版目录。"

    # android.rpy:313
    old "Android: [project.current.display_name!q]"
    new "安卓：[project.current.display_name!q]"

    # android.rpy:333
    old "Emulation:"
    new "模拟："

    # android.rpy:342
    old "Phone"
    new "手机"

    # android.rpy:346
    old "Tablet"
    new "平板"

    # android.rpy:350
    old "Television"
    new "电视"

    # android.rpy:362
    old "Build:"
    new "生成："

    # android.rpy:373
    old "Debug"
    new "调试版"

    # android.rpy:377
    old "Release"
    new "发布版"

    # android.rpy:384
    old "Install SDK & Create Keys"
    new "安装 SDK 并创建密钥"

    # android.rpy:388
    old "Configure"
    new "配置"

    # android.rpy:392
    old "Build Package"
    new "生成应用包"

    # android.rpy:396
    old "Build & Install"
    new "生成应用包并安装"

    # android.rpy:400
    old "Build, Install & Launch"
    new "生成应用包，安装并启动"

    # android.rpy:411
    old "Other:"
    new "其他："

    # android.rpy:419
    old "Logcat"
    new "Logcat"

    # android.rpy:452
    old "Before packaging Android apps, you'll need to download RAPT, the Ren'Py Android Packaging Tool. Would you like to download RAPT now?"
    new "在为安卓应用打包之前，您需要先下载 RAPT，即 Ren'Py 安卓打包工具。您希望现在就开始下载 RAPT 吗？"

    # android.rpy:505
    old "Retrieving logcat information from device."
    new "正在从设备接收 logcat 信息。"

    # androidstrings.rpy:7
    old "{} is not a directory."
    new "{} 不是目录。"

    # androidstrings.rpy:8
    old "{} does not contain a Ren'Py game."
    new "{} 不包含 Ren'Py 游戏。"

    # androidstrings.rpy:9
    old "Run configure before attempting to build the app."
    new "在尝试构建应用前执行配置。"

    # androidstrings.rpy:10
    old "Google Play support is enabled, but build.google_play_key is not defined."
    new "Google Play 支持已启用，但 build.google_play_key 尚未定义。"

    # androidstrings.rpy:11
    old "Updating project."
    new "正在更新工程。"

    # androidstrings.rpy:12
    old "Creating assets directory."
    new "正在创建资源目录。"

    # androidstrings.rpy:13
    old "Creating expansion file."
    new "正在创建扩展文件。"

    # androidstrings.rpy:14
    old "Packaging internal data."
    new "正在打包内部数据。"

    # androidstrings.rpy:15
    old "I'm using Gradle to build the package."
    new "正在使用 Gradle 构建应用包。"

    # androidstrings.rpy:16
    old "Uploading expansion file."
    new "正在上传扩展文件。"

    # androidstrings.rpy:17
    old "The build seems to have failed."
    new "构建似乎已失败。"

    # androidstrings.rpy:18
    old "Launching app."
    new "正在启动应用。"

    # androidstrings.rpy:19
    old "The build seems to have succeeded."
    new "构建似乎已成功。"

    # androidstrings.rpy:20
    old "The armeabi-v7a version works on most phones or tablets, while the x86_64 version works on the simulator and chromebooks."
    new "armeabi-v7a 版用于多数手机或平板，而 x86_64 版用于模拟器和 Chromebook。"

    # androidstrings.rpy:21
    old "What is the full name of your application? This name will appear in the list of installed applications."
    new "您应用的全名是什么？此名称将显示在已安装的应用列表中。"

    # androidstrings.rpy:22
    old "What is the short name of your application? This name will be used in the launcher, and for application shortcuts."
    new "您应用的简称是什么？此名称将用于启动器和应用图标。"

    # androidstrings.rpy:23
    old "What is the name of the package?\n\nThis is usually of the form com.domain.program or com.domain.email.program. It may only contain ASCII letters and dots. It must contain at least one dot."
    new "应用包的名称是什么？\n\n此名称一般是以 com.domain.program 或 com.domain.email.program 的形式出现。名称中只能包含 ASCII 字母和点。名称中必须至少包含一个点。"

    # androidstrings.rpy:24
    old "The package name may not be empty."
    new "应用包名称不能为空。"

    # androidstrings.rpy:25
    old "The package name may not contain spaces."
    new "应用包名称不能包含空格。"

    # androidstrings.rpy:26
    old "The package name must contain at least one dot."
    new "应用包名称必须至少包含一个点。"

    # androidstrings.rpy:27
    old "The package name may not contain two dots in a row, or begin or end with a dot."
    new "应用包名称不能包含连续两个点，或在开始和末尾的地方出现点。"

    # androidstrings.rpy:28
    old "Each part of the package name must start with a letter, and contain only letters, numbers, and underscores."
    new "应用包名称的每一部分必须以字母开始，并只包含字母、数字和下划线。"

    # androidstrings.rpy:29
    old "{} is a Java keyword, and can't be used as part of a package name."
    new "{} 是 Java 关键字，不能用于应用包名称。"

    # androidstrings.rpy:30
    old "What is the application's version?\n\nThis should be the human-readable version that you would present to a person. It must contain only numbers and dots."
    new "应用的版本号是什么？\n\n此版本号是您打算向用户展示的，可阅读的版本号。版本号仅能包含数字和点。"

    # androidstrings.rpy:31
    old "The version number must contain only numbers and dots."
    new "版本号只能包含数字和点。"

    # androidstrings.rpy:32
    old "What is the version code?\n\nThis must be a positive integer number, and the value should increase between versions."
    new "版本代码是什么？\n\n版本代码必须是正整数，且版本之间的数值仅允许增加。"

    # androidstrings.rpy:33
    old "The numeric version must contain only numbers."
    new "版本代码应仅包含数字。"

    # androidstrings.rpy:34
    old "How would you like your application to be displayed?"
    new "您希望您的应用如何显示？"

    # androidstrings.rpy:35
    old "In landscape orientation."
    new "横屏模式。"

    # androidstrings.rpy:36
    old "In portrait orientation."
    new "竖屏模式。"

    # androidstrings.rpy:37
    old "In the user's preferred orientation."
    new "以用户希望的模式。"

    # androidstrings.rpy:38
    old "Which app store would you like to support in-app purchasing through?"
    new "您希望通过哪种应用商店支持应用内购买？"

    # androidstrings.rpy:39
    old "Google Play."
    new "Google Play。"

    # androidstrings.rpy:40
    old "Amazon App Store."
    new "亚马逊应用商店。"

    # androidstrings.rpy:41
    old "Both, in one app."
    new "以上全部，集成在一个应用中。"

    # androidstrings.rpy:42
    old "Neither."
    new "不支持内购。"

    # androidstrings.rpy:43
    old "Would you like to create an expansion APK?"
    new "您希望创建扩展 APK 吗？"

    # androidstrings.rpy:44
    old "No. Size limit of 100 MB on Google Play, but can be distributed through other stores and sideloaded."
    new "否。Google Play 上的大小限制为 100 MB，但可以通过其他商店和渠道分发。"

    # androidstrings.rpy:45
    old "Yes. 2 GB size limit, but won't work outside of Google Play. (Read the documentation to get this to work.)"
    new "是。上限为 2 GB，但在 Google Play 之外无法使用。（详情请阅读文档）"

    # androidstrings.rpy:46
    old "Do you want to allow the app to access the Internet?"
    new "您是否允许该应用访问互联网？"

    # androidstrings.rpy:47
    old "Do you want to automatically update the generated project?"
    new "您希望自动更新已生成的工程吗？"

    # androidstrings.rpy:48
    old "Yes. This is the best choice for most projects."
    new "是。此为大多数工程的最佳选择。"

    # androidstrings.rpy:49
    old "No. This may require manual updates when Ren'Py or the project configuration changes."
    new "否。当 Ren'Py 或工程配置发生变化时需要手动更新。"

    # androidstrings.rpy:50
    old "Unknown configuration variable: {}"
    new "未知的配置变量：{}"

    # androidstrings.rpy:51
    old "I'm compiling a short test program, to see if you have a working JDK on your system."
    new "正在编译一个简短的测试程序，来测试您的操作系统内是否有可用的 JDK。"

    # androidstrings.rpy:52
    old "I was unable to use javac to compile a test file. If you haven't installed the Java Development Kit yet, please download it from:\n\nhttp://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html\n\nThe JDK is different from the JRE, so it's possible you have Java without having the JDK. Without a working JDK, I can't continue."
    new "无法使用 javac 编译测试文件。如果您尚未安装 Java 开发套件（JDK）。如果您尚未安装 JDK，请从以下地址安装：\n\nhttp://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html\n\nJDK 不同于 JRE，所以您可能已安装过 Java 但尚未安装 JDK。若缺乏可用的 JDK，程序将无法继续。"

    # androidstrings.rpy:53
    old "The version of Java on your computer does not appear to be JDK 8, which is the only version supported by the Android SDK. If you need to install JDK 8, you can download it from:\n\nhttp://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html\n\nYou can also set the JAVA_HOME environment variabe to use a different version of Java."
    new "您计算机上的 Java 版本似乎不是 JDK 8，这是 Android SDK 支持的唯一版本。如果您需要安装 JDK 8，您可以从以下地址下载：\n\nhttp://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html\n\n您还可以设置 JAVA_HOME 环境变量来使用不同版本的 Java。"

    # androidstrings.rpy:54
    old "The JDK is present and working. Good!"
    new "JDK 存在并正在工作。不错！"

    # androidstrings.rpy:55
    old "The Android SDK has already been unpacked."
    new "Android SDK 已被解压。"

    # androidstrings.rpy:56
    old "Do you accept the Android SDK Terms and Conditions?"
    new "您是否接受 Android SDK 条款和条件？"

    # androidstrings.rpy:57
    old "I'm downloading the Android SDK. This might take a while."
    new "正在下载 Android SDK。这可能需要一段时间。"

    # androidstrings.rpy:58
    old "I'm extracting the Android SDK."
    new "正在提取 Android SDK。"

    # androidstrings.rpy:59
    old "I've finished unpacking the Android SDK."
    new "解压 Android SDK 已完成。"

    # androidstrings.rpy:60
    old "I'm about to download and install the required Android packages. This might take a while."
    new "即将下载并安装所需的安卓软件包。这可能需要一段时间。"

    # androidstrings.rpy:61
    old "I was unable to accept the Android licenses."
    new "无法接受安卓许可证。"

    # androidstrings.rpy:62
    old "I was unable to install the required Android packages."
    new "无法安装所需的安卓软件包。"

    # androidstrings.rpy:63
    old "I've finished installing the required Android packages."
    new "已完成安装所需的安卓软件包。"

    # androidstrings.rpy:64
    old "You set the keystore yourself, so I'll assume it's how you want it."
    new "您选择自行设置密钥库，假定您已完成。"

    # androidstrings.rpy:65
    old "You've already created an Android keystore, so I won't create a new one for you."
    new "您已创建了安卓密钥库，将不再为您创建新密钥库。"

    # androidstrings.rpy:66
    old "I can create an application signing key for you. Signing an application with this key allows it to be placed in the Android Market and other app stores.\n\nDo you want to create a key?"
    new "Ren'Py 可以为您创建应用程序签名密钥。使用此密钥签名应用将允许其上传到安卓市场和其他应用商店中。\n\n您要创建密钥吗？"

    # androidstrings.rpy:67
    old "I will create the key in the android.keystore file.\n\nYou need to back this file up. If you lose it, you will not be able to upgrade your application.\n\n\\You also need to keep the key safe. If evil people get this file, they could make fake versions of your application, and potentially steal your users' data.\n\nWill you make a backup of android.keystore, and keep it in a safe place?"
    new "即将在 android.keystore 文件中创建密钥。\n\n您需要备份此文件。如果该文件丢失，您将无法更新您的应用。\n\n\\您还需要将密钥文件放置到安全的位置。若攻击者获取此文件，就可以假冒您的应用，并窃取用户数据。\n\n您是否会备份 android.keystore 并将其置于安全的位置？"

    # androidstrings.rpy:68
    old "Please enter your name or the name of your organization."
    new "请输入您的名称或您组织的名称。"

    # androidstrings.rpy:69
    old "Could not create android.keystore. Is keytool in your path?"
    new "无法创建 android.keystore。您是否将 keytool 放置在了相同的目录？"

    # androidstrings.rpy:70
    old "I've finished creating android.keystore. Please back it up, and keep it in a safe place."
    new "已完成创建 android.keystore。请将其备份并放置于安全的位置。"

    # androidstrings.rpy:71
    old "It looks like you're ready to start packaging games."
    new "看起来您已准备好开始打包游戏了。"

    # choose_directory.rpy:87
    old "Ren'Py was unable to run python with tkinter to choose the directory. Please install the python-tk or tkinter package."
    new "Ren'Py 无法使用 Python 的 Tkinter 来选择目录。请安装 Python-tk 或 Tkinter 支持包。"

    # choose_directory.rpy:104
    old "The selected projects directory is not writable."
    new "所选的工程目录无法执行写操作。"

    # choose_theme.rpy:303
    old "Could not change the theme. Perhaps options.rpy was changed too much."
    new "无法更改主题。可能 options.rpy 已被过度修改。"

    # choose_theme.rpy:370
    old "Planetarium"
    new "Planetarium"

    # choose_theme.rpy:425
    old "Choose Theme"
    new "选择主题"

    # choose_theme.rpy:438
    old "Theme"
    new "主题"

    # choose_theme.rpy:463
    old "Color Scheme"
    new "配色方案"

    # choose_theme.rpy:495
    old "Continue"
    new "继续"

    # consolecommand.rpy:84
    old "INFORMATION"
    new "信息"

    # consolecommand.rpy:84
    old "The command is being run in a new operating system console window."
    new "此命令正在一个新打开的系统控制台中运行。"

    # distribute.rpy:444
    old "Scanning project files..."
    new "正在扫描工程文件……"

    # distribute.rpy:460
    old "Building distributions failed:\n\nThe build.directory_name variable may not include the space, colon, or semicolon characters."
    new "生成分发版失败：\n\n参数 build.directory_name 不能包含空格、冒号和分号。"

    # distribute.rpy:505
    old "No packages are selected, so there's nothing to do."
    new "因未选择任何打包平台，故未执行任何操作。"

    # distribute.rpy:517
    old "Scanning Ren'Py files..."
    new "正在扫描 Ren'Py 文件……"

    # distribute.rpy:572
    old "All packages have been built.\n\nDue to the presence of permission information, unpacking and repacking the Linux and Macintosh distributions on Windows is not supported."
    new "所有的分发包已生成。\n\n由于包内写入了权限信息，因此不支持在 Windows 上解包并重新打包 Linux 和 Macintosh 分发版。"

    # distribute.rpy:755
    old "Archiving files..."
    new "正在封装文件……"

    # distribute.rpy:1068
    old "Unpacking the Macintosh application for signing..."
    new "正在解包 Macintosh 应用并签名……"

    # distribute.rpy:1078
    old "Signing the Macintosh application...\n(This may take a long time.)"
    new "正在签名 Macintosh 应用……\n（可能需要很长时间。）"

    # distribute.rpy:1100
    old "Creating the Macintosh DMG..."
    new "正在创建 Macintosh DMG……"

    # distribute.rpy:1109
    old "Signing the Macintosh DMG..."
    new "正在签名 Macintosh DMG……"

    # distribute.rpy:1304
    old "Writing the [variant] [format] package."
    new "正在写入 [variant] 版 [format] 包。"

    # distribute.rpy:1317
    old "Making the [variant] update zsync file."
    new "正在制作 [variant] 版更新同步文件。"

    # distribute.rpy:1427
    old "Processed {b}[complete]{/b} of {b}[total]{/b} files."
    new "已处理 {b}[complete]{/b} / {b}[total]{/b} 个文件。"

    # distribute_gui.rpy:162
    old "Build Distributions: [project.current.display_name!q]"
    new "生成分发版：[project.current.display_name!q]"

    # distribute_gui.rpy:176
    old "Directory Name:"
    new "目录名："

    # distribute_gui.rpy:180
    old "Executable Name:"
    new "可执行程序名："

    # distribute_gui.rpy:190
    old "Actions:"
    new "操作："

    # distribute_gui.rpy:198
    old "Edit options.rpy"
    new "编辑 options.rpy"

    # distribute_gui.rpy:199
    old "Add from clauses to calls, once"
    new "向 call 语句添加 from 从句，执行一次"

    # distribute_gui.rpy:200
    old "Refresh"
    new "刷新"

    # distribute_gui.rpy:204
    old "Upload to itch.io"
    new "上传到 itch.io"

    # distribute_gui.rpy:220
    old "Build Packages:"
    new "生成分发包："

    # distribute_gui.rpy:239
    old "Options:"
    new "选项："

    # distribute_gui.rpy:244
    old "Build Updates"
    new "生成更新"

    # distribute_gui.rpy:246
    old "Add from clauses to calls"
    new "向 call 语句添加 from 从句"

    # distribute_gui.rpy:247
    old "Force Recompile"
    new "强制重新编译"

    # distribute_gui.rpy:270
    old "Build"
    new "生成"

    # distribute_gui.rpy:274
    old "Adding from clauses to call statements that do not have them."
    new "正在向 call 语句添加缺失的 from 从句。"

    # distribute_gui.rpy:295
    old "Errors were detected when running the project. Please ensure the project runs without errors before building distributions."
    new "运行工程时检测到错误。请在生成分发版之前确保工程能够正常运行。"

    # distribute_gui.rpy:312
    old "Your project does not contain build information. Would you like to add build information to the end of options.rpy?"
    new "您的工程尚未包含生成信息。您希望在 options.rpy 末端添加生成信息吗？"

    # dmgcheck.rpy:50
    old "Ren'Py is running from a read only folder. Some functionality will not work."
    new "Ren'Py 目前正从只读文件夹中运行。某些功能将无法工作。"

    # dmgcheck.rpy:50
    old "This is probably because Ren'Py is running directly from a Macintosh drive image. To fix this, quit this launcher, copy the entire %s folder somewhere else on your computer, and run Ren'Py again."
    new "这可能是由于 Ren'Py 直接从 Macintosh 磁盘镜像中运行导致的。要修复此问题，退出启动器，复制整个 %s 文件夹到您计算机的其他任意位置，并重新运行 Ren'Py。"

    # editor.rpy:152
    old "(Recommended) A modern and approachable text editor."
    new "（推荐）一个现代化且人性化的文本编辑器。"

    # editor.rpy:164
    old "Up to 150 MB download required."
    new "需要下载最多 150 MB 的文件。"

    # editor.rpy:178
    old "A mature editor. Editra lacks the IME support required for Chinese, Japanese, and Korean text input."
    new "一个成熟的编辑器。Editra 缺乏对中日韩输入法的良好支持。"

    # editor.rpy:179
    old "A mature editor. Editra lacks the IME support required for Chinese, Japanese, and Korean text input. On Linux, Editra requires wxPython."
    new "一个成熟的编辑器。Editra 缺乏对中日韩输入法的良好支持。在 Linux 系统运行 Editra 需要安装 wxPython。"

    # editor.rpy:195
    old "This may have occured because wxPython is not installed on this system."
    new "这可能是由于您的系统中尚未安装 wxPython 造成的。"

    # editor.rpy:197
    old "Up to 22 MB download required."
    new "需要下载最多 22 MB 的文件。"

    # editor.rpy:210
    old "A mature editor that requires Java."
    new "一个成熟的编辑器，需要安装 Java。"

    # editor.rpy:210
    old "1.8 MB download required."
    new "需要下载 1.8 MB 的文件。"

    # editor.rpy:210
    old "This may have occured because Java is not installed on this system."
    new "这可能是由于您的系统中尚未安装 Java 造成的。"

    # editor.rpy:219
    old "System Editor"
    new "操作系统编辑器"

    # editor.rpy:219
    old "Invokes the editor your operating system has associated with .rpy files."
    new "调用您操作系统已关联到 .rpy 文件的编辑器。"

    # editor.rpy:235
    old "None"
    new "无"

    # editor.rpy:235
    old "Prevents Ren'Py from opening a text editor."
    new "禁止 Ren'Py 自动打开文本编辑器。"

    # editor.rpy:338
    old "Edit [text]."
    new "编辑 [text]。"

    # editor.rpy:387
    old "An exception occured while launching the text editor:\n[exception!q]"
    new "启动编辑器时出现异常：\n[exception!q]"

    # editor.rpy:519
    old "Select Editor"
    new "选择编辑器"

    # editor.rpy:534
    old "A text editor is the program you'll use to edit Ren'Py script files. Here, you can select the editor Ren'Py will use. If not already present, the editor will be automatically downloaded and installed."
    new "文本编辑器是指您用来编辑 Ren'Py 脚本的程序。在这里您可以选择 Ren'Py 要使用的编辑器。若您选择的编辑器不存在，Ren'Py 将会自动下载并安装此编辑器。"

    # front_page.rpy:35
    old "Open [text] directory."
    new "打开 [text] 目录。"

    # front_page.rpy:91
    old "PROJECTS:"
    new "工程："

    # front_page.rpy:93
    old "refresh"
    new "刷新"

    # front_page.rpy:120
    old "+ Create New Project"
    new "+ 创建新工程"

    # front_page.rpy:130
    old "Launch Project"
    new "启动工程"

    # front_page.rpy:147
    old "[p.name!q] (template)"
    new "[p.name!q]（模板）"

    # front_page.rpy:149
    old "Select project [text]."
    new "选择工程 [text]。"

    # front_page.rpy:165
    old "Tutorial"
    new "教程"

    # front_page.rpy:166
    old "The Question"
    new "The Question"

    # front_page.rpy:182
    old "Active Project"
    new "活跃工程"

    # front_page.rpy:190
    old "Open Directory"
    new "打开目录"

    # front_page.rpy:195
    old "game"
    new "game"

    # front_page.rpy:196
    old "base"
    new "base"

    # front_page.rpy:197
    old "images"
    new "images"

    # front_page.rpy:198
    old "gui"
    new "gui"

    # front_page.rpy:204
    old "Edit File"
    new "编辑文件"

    # front_page.rpy:215
    old "Open project"
    new "打开工程"

    # front_page.rpy:217
    old "All script files"
    new "全部脚本文件"

    # front_page.rpy:221
    old "Actions"
    new "操作"

    # front_page.rpy:230
    old "Navigate Script"
    new "定位脚本"

    # front_page.rpy:231
    old "Check Script (Lint)"
    new "检查脚本并分析统计"

    # front_page.rpy:234
    old "Change/Update GUI"
    new "更改/更新 GUI"

    # front_page.rpy:236
    old "Change Theme"
    new "更改主题"

    # front_page.rpy:239
    old "Delete Persistent"
    new "删除持久化数据"

    # front_page.rpy:248
    old "Build Distributions"
    new "生成分发版"

    # front_page.rpy:250
    old "Android"
    new "安卓"

    # front_page.rpy:251
    old "iOS"
    new "iOS"

    # front_page.rpy:252
    old "Generate Translations"
    new "生成翻译文件"

    # front_page.rpy:253
    old "Extract Dialogue"
    new "导出对话"

    # front_page.rpy:270
    old "Checking script for potential problems..."
    new "正在检查脚本中的潜在问题……"

    # front_page.rpy:285
    old "Deleting persistent data..."
    new "正在删除持久化数据……"

    # front_page.rpy:293
    old "Recompiling all rpy files into rpyc files..."
    new "正在将全部的 rpy 文件重新编译为 rpyc 文件……"

    # gui7.rpy:252
    old "Select Accent and Background Colors"
    new "选择主要部件和背景颜色"

    # gui7.rpy:266
    old "Please click on the color scheme you wish to use, then click Continue. These colors can be changed and customized later."
    new "请点击您希望使用的配色方案，然后点击“继续”。这些颜色稍后也可更改及自定义。"

    # gui7.rpy:311
    old "{b}Warning{/b}\nContinuing will overwrite customized bar, button, save slot, scrollbar, and slider images.\n\nWhat would you like to do?"
    new "{b}警告{/b}\n继续将会覆盖自定义的状态条、按钮、存档位、滑条和滑块图。\n\n您希望执行哪种操作？"

    # gui7.rpy:311
    old "Choose new colors, then regenerate image files."
    new "选择新配色，然后重新生成图像文件。"

    # gui7.rpy:311
    old "Regenerate the image files using the colors in gui.rpy."
    new "使用 gui.rpy 中的配色重新生成图像文件。"

    # gui7.rpy:331
    old "PROJECT NAME"
    new "工程名称"

    # gui7.rpy:331
    old "Please enter the name of your project:"
    new "请输入新工程的名称："

    # gui7.rpy:339
    old "The project name may not be empty."
    new "工程名不能为空。"

    # gui7.rpy:344
    old "[project_name!q] already exists. Please choose a different project name."
    new "[project_name!q] 已存在。请指定一个不同的工程名称。"

    # gui7.rpy:347
    old "[project_dir!q] already exists. Please choose a different project name."
    new "[project_dir!q] 已存在。请指定一个不同的工程名称。"

    # gui7.rpy:358
    old "What resolution should the project use? Although Ren'Py can scale the window up and down, this is the initial size of the window, the size at which assets should be drawn, and the size at which the assets will be at their sharpest.\n\nThe default of 1280x720 is a reasonable compromise."
    new "您希望该工程使用哪种基础分辨率？虽然 Ren'Py 可以向上或向下缩放窗口，此分辨率将是窗口的初始化尺寸、资源绘制的基础分辨率以及资源显示最清晰的分辨率。\n\n默认的 1280x720 是折中方案。"

    # gui7.rpy:358
    old "Custom. The GUI is optimized for a 16:9 aspect ratio."
    new "自定义。GUI 在 16:9 的情况下是最优的。"

    # gui7.rpy:373
    old "WIDTH"
    new "宽度"

    # gui7.rpy:373
    old "Please enter the width of your game, in pixels."
    new "请输入游戏宽度的像素数。"

    # gui7.rpy:378
    old "The width must be a number."
    new "宽度必须是数字。"

    # gui7.rpy:380
    old "HEIGHT"
    new "高度"

    # gui7.rpy:380
    old "Please enter the height of your game, in pixels."
    new "请输入游戏高度的像素数。"

    # gui7.rpy:385
    old "The height must be a number."
    new "高度必须是数字。"

    # gui7.rpy:427
    old "Creating the new project..."
    new "正在创建新工程……"

    # gui7.rpy:429
    old "Updating the project..."
    new "正在更新工程……"

    # interface.rpy:119
    old "Documentation"
    new "说明文档"

    # interface.rpy:120
    old "Ren'Py Website"
    new "Ren'Py 官方网站"

    # interface.rpy:121
    old "Ren'Py Games List"
    new "Ren'Py 游戏列表"

    # interface.rpy:129
    old "update"
    new "更新"

    # interface.rpy:131
    old "preferences"
    new "设置"

    # interface.rpy:132
    old "quit"
    new "退出"

    # interface.rpy:136
    old "Ren'Py Sponsor Information"
    new "Ren'Py 赞助者信息"

    # interface.rpy:258
    old "Due to package format limitations, non-ASCII file and directory names are not allowed."
    new "由于包格式限制，无法使用非 ASCII 文件名和目录名。"

    # interface.rpy:354
    old "ERROR"
    new "错误"

    # interface.rpy:400
    old "Text input may not contain the {{ or [[ characters."
    new "文本输入不能包含 {{ 或 [[ 字符。"

    # interface.rpy:405
    old "File and directory names may not contain / or \\."
    new "文件名或目录名不能包含 / 或 \\。"

    # interface.rpy:411
    old "File and directory names must consist of ASCII characters."
    new "文件名或目录名必须仅由 ASCII 字符组成，不能包含中文。"

    # interface.rpy:479
    old "PROCESSING"
    new "正在处理"

    # interface.rpy:496
    old "QUESTION"
    new "问题"

    # interface.rpy:509
    old "CHOICE"
    new "选择"

    # ios.rpy:28
    old "To build iOS packages, please download renios, unzip it, and place it into the Ren'Py directory. Then restart the Ren'Py launcher."
    new "要生成 iOS 应用包，请下载 renios，放置到 Ren'Py 目录中并重启 Ren'Py。"

    # ios.rpy:29
    old "The directory in where Xcode projects will be placed has not been selected. Choose 'Select Directory' to select it."
    new "Xcode 工程的存放目录尚未被指定。选择“指定目录”来指定。"

    # ios.rpy:30
    old "There is no Xcode project corresponding to the current Ren'Py project. Choose 'Create Xcode Project' to create one."
    new "尚无与目前 Ren'Py 工程对应的 Xcode 工程。选择“创建 Xcode 工程”来进行创建。"

    # ios.rpy:31
    old "An Xcode project exists. Choose 'Update Xcode Project' to update it with the latest game files, or use Xcode to build and install it."
    new "该 Xcode 工程已经存在。选择“更新 Xcode 工程”更新为最新的游戏文件，或使用 Xcode 来生成并安装。"

    # ios.rpy:33
    old "Attempts to emulate an iPhone.\n\nTouch input is emulated through the mouse, but only when the button is held down."
    new "尝试模拟为 iPhone。\n\n鼠标将仅在按键按下时模拟为触屏输入。"

    # ios.rpy:34
    old "Attempts to emulate an iPad.\n\nTouch input is emulated through the mouse, but only when the button is held down."
    new "尝试模拟为 iPad。\n\n鼠标将仅在按键按下时模拟为触屏输入。"

    # ios.rpy:36
    old "Selects the directory where Xcode projects will be placed."
    new "请指定放置 Xcode 工程的目录。"

    # ios.rpy:37
    old "Creates an Xcode project corresponding to the current Ren'Py project."
    new "创建与当前 Ren'Py 工程对应的 Xcode 工程。"

    # ios.rpy:38
    old "Updates the Xcode project with the latest game files. This must be done each time the Ren'Py project changes."
    new "以最新的游戏文件更新 Xcode 工程。此操作应在每次 Ren'Py 工程出现更改时执行一次。"

    # ios.rpy:39
    old "Opens the Xcode project in Xcode."
    new "在 Xcode 中打开 Xcode 工程。"

    # ios.rpy:41
    old "Opens the directory containing Xcode projects."
    new "打开包含 Xcode 工程的目录。"

    # ios.rpy:126
    old "The Xcode project already exists. Would you like to rename the old project, and replace it with a new one?"
    new "Xcode 工程已经存在。您希望重命名旧工程，并用新工程将其替换吗？"

    # ios.rpy:211
    old "iOS: [project.current.display_name!q]"
    new "iOS：[project.current.display_name!q]"

    # ios.rpy:240
    old "iPhone"
    new "iPhone"

    # ios.rpy:244
    old "iPad"
    new "iPad"

    # ios.rpy:264
    old "Select Xcode Projects Directory"
    new "指定 Xcode 工程目录"

    # ios.rpy:268
    old "Create Xcode Project"
    new "创建 Xcode 工程"

    # ios.rpy:272
    old "Update Xcode Project"
    new "更新 Xcode 工程"

    # ios.rpy:277
    old "Launch Xcode"
    new "启动 Xcode"

    # ios.rpy:312
    old "Open Xcode Projects Directory"
    new "打开 Xcode 工程目录"

    # ios.rpy:345
    old "Before packaging iOS apps, you'll need to download renios, Ren'Py's iOS support. Would you like to download renios now?"
    new "在为 iOS 应用打包之前，您需要先下载 renios，即 Ren'Py iOS 支持套件。您希望现在就开始下载 renios 吗？"

    # ios.rpy:354
    old "XCODE PROJECTS DIRECTORY"
    new "XCODE 工程目录"

    # ios.rpy:354
    old "Please choose the Xcode Projects Directory using the directory chooser.\n{b}The directory chooser may have opened behind this window.{/b}"
    new "请使用弹出的目录选择窗口来指定 Xcode 工程目录。\n{b}目录选择窗口可能会被本窗口覆盖。{/b}"

    # ios.rpy:359
    old "Ren'Py has set the Xcode Projects Directory to:"
    new "Ren'Py 已将 Xcode 工程目录设置为："

    # itch.rpy:60
    old "The built distributions could not be found. Please choose 'Build' and try again."
    new "未找到已生成的分发版。请使用“生成”重试。"

    # itch.rpy:98
    old "No uploadable files were found. Please choose 'Build' and try again."
    new "未找到可上传的文件。请使用“生成”重试。"

    # itch.rpy:106
    old "The butler program was not found."
    new "未找到管理程序。"

    # itch.rpy:106
    old "Please install the itch.io app, which includes butler, and try again."
    new "itch.io 应用中包含管理程序。请安装 itch.io 应用并重试。"

    # itch.rpy:115
    old "The name of the itch project has not been set."
    new "Itch 工程名尚未设置。"

    # itch.rpy:115
    old "Please {a=https://itch.io/game/new}create your project{/a}, then add a line like \n{vspace=5}define build.itch_project = \"user-name/game-name\"\n{vspace=5} to options.rpy."
    new "请{a=https://itch.io/game/new}创建您的工程{/a}，并在 options.rpy 里新增诸如\n{vspace=5}define build.itch_project = \"user-name/game-name\"\n{vspace=5} 的内容。"

    # mobilebuild.rpy:110
    old "{a=%s}%s{/a}"
    new "{a=%s}%s{/a}"

    # navigation.rpy:168
    old "Navigate: [project.current.display_name!q]"
    new "定位：[project.current.display_name!q]"

    # navigation.rpy:178
    old "Order: "
    new "排序方式："

    # navigation.rpy:179
    old "alphabetical"
    new "字母"

    # navigation.rpy:181
    old "by-file"
    new "按文件分类"

    # navigation.rpy:183
    old "natural"
    new "出现顺序"

    # navigation.rpy:195
    old "Category:"
    new "类别："

    # navigation.rpy:198
    old "files"
    new "文件"

    # navigation.rpy:199
    old "labels"
    new "标签"

    # navigation.rpy:200
    old "defines"
    new "定义"

    # navigation.rpy:201
    old "transforms"
    new "变换"

    # navigation.rpy:202
    old "screens"
    new "屏幕"

    # navigation.rpy:203
    old "callables"
    new "可调用"

    # navigation.rpy:204
    old "TODOs"
    new "待办事项"

    # navigation.rpy:243
    old "+ Add script file"
    new "+ 添加脚本文件"

    # navigation.rpy:251
    old "No TODO comments found.\n\nTo create one, include \"# TODO\" in your script."
    new "目前尚无待办事项。将“# TODO”包含到脚本中即可创建。"

    # navigation.rpy:258
    old "The list of names is empty."
    new "列表为空。"

    # new_project.rpy:38
    old "New GUI Interface"
    new "新 GUI 界面"

    # new_project.rpy:48
    old "Both interfaces have been translated to your language."
    new "所有界面均已翻译至您的语言。"

    # new_project.rpy:50
    old "Only the new GUI has been translated to your language."
    new "仅有新 GUI 已翻译至您的语言。"

    # new_project.rpy:52
    old "Only the legacy theme interface has been translated to your language."
    new "仅有传统主题界面已翻译至您的语言。"

    # new_project.rpy:54
    old "Neither interface has been translated to your language."
    new "尚无界面翻译至您的语言。"

    # new_project.rpy:63
    old "The projects directory could not be set. Giving up."
    new "工程目录无法设定。操作取消。"

    # new_project.rpy:71
    old "You will be creating an [new_project_language] language project. Change the launcher language in preferences to create a project in another language."
    new "您将创建一个 [new_project_language] 语言的工程。要创建其他语言的工程，请在设置里更改启动器语言。"

    # new_project.rpy:79
    old "Which interface would you like to use? The new GUI has a modern look, supports wide screens and mobile devices, and is easier to customize. Legacy themes might be necessary to work with older example code.\n\n[language_support!t]\n\nIf in doubt, choose the new GUI, then click Continue on the bottom-right."
    new "您希望使用哪种界面？新 GUI 具有更现代的设计，可支持宽屏和移动设备，定制起来也更容易。对于较早的示范代码，传统主题可能是必须的。\n\n[language_support!t]\n\n如有疑问，请选择新 GUI，并点击右下角的“继续”。"

    # new_project.rpy:79
    old "Legacy Theme Interface"
    new "传统主题界面"

    # new_project.rpy:100
    old "Choose Project Template"
    new "指定工程模板"

    # new_project.rpy:118
    old "Please select a template to use for your new project. The template sets the default font and the user interface language. If your language is not supported, choose 'english'."
    new "请指定一个新工程要使用的模板。模板已预先设置了默认字体和用户界面语言。如果您的语言暂未支持，请选择“英语”。"

    # preferences.rpy:73
    old "Launcher Preferences"
    new "启动器设置"

    # preferences.rpy:94
    old "Projects Directory:"
    new "工程目录："

    # preferences.rpy:101
    old "[persistent.projects_directory!q]"
    new "[persistent.projects_directory!q]"

    # preferences.rpy:103
    old "Projects directory: [text]"
    new "工程目录：[text]"

    # preferences.rpy:105
    old "Not Set"
    new "未指定"

    # preferences.rpy:120
    old "Text Editor:"
    new "文本编辑器："

    # preferences.rpy:126
    old "Text editor: [text]"
    new "文本编辑器：[text]"

    # preferences.rpy:145
    old "Navigation Options:"
    new "定位选项："

    # preferences.rpy:149
    old "Include private names"
    new "包含私有名称"

    # preferences.rpy:150
    old "Include library names"
    new "包含库名称"

    # preferences.rpy:160
    old "Launcher Options:"
    new "启动器选项："

    # preferences.rpy:164
    old "Hardware rendering"
    new "硬件渲染"

    # preferences.rpy:165
    old "Show edit file section"
    new "显示编辑文件部件"

    # preferences.rpy:166
    old "Large fonts"
    new "大字体"

    # preferences.rpy:169
    old "Console output"
    new "控制台输出"

    # preferences.rpy:173
    old "Force new tutorial"
    new "强制新手教程"

    # preferences.rpy:177
    old "Legacy options"
    new "传统选项"

    # preferences.rpy:180
    old "Show templates"
    new "显示模板"

    # preferences.rpy:182
    old "Sponsor message"
    new "赞助者信息"

    # preferences.rpy:202
    old "Open launcher project"
    new "打开启动器工程"

    # preferences.rpy:216
    old "Language:"
    new "语言："

    # project.rpy:49
    old "After making changes to the script, press shift+R to reload your game."
    new "在对脚本进行更改之后，按 Shift+R 来重新载入游戏。"

    # project.rpy:49
    old "Press shift+O (the letter) to access the console."
    new "按 Shift+O（字母 O）来打开控制台。"

    # project.rpy:49
    old "Press shift+D to access the developer menu."
    new "按 Shift+D 打开开发者菜单。"

    # project.rpy:49
    old "Have you backed up your projects recently?"
    new "您最近备份过您的工程吗？"

    # project.rpy:281
    old "Launching the project failed."
    new "启动工程失败。"

    # project.rpy:281
    old "Please ensure that your project launches normally before running this command."
    new "在执行此命令之前，请确保您的工程可正常运行。"

    # project.rpy:297
    old "Ren'Py is scanning the project..."
    new "Ren'Py 正在扫描工程……"

    # project.rpy:729
    old "Launching"
    new "启动中"

    # project.rpy:763
    old "PROJECTS DIRECTORY"
    new "工程目录"

    # project.rpy:763
    old "Please choose the projects directory using the directory chooser.\n{b}The directory chooser may have opened behind this window.{/b}"
    new "请使用弹出的目录选择窗口来指定工程目录。\n{b}目录选择窗口可能会被本窗口覆盖。{/b}"

    # project.rpy:763
    old "This launcher will scan for projects in this directory, will create new projects in this directory, and will place built projects into this directory."
    new "该启动器将会在此目录里扫描工程、创建新工程以及将生成的工程放置在此。"

    # project.rpy:768
    old "Ren'Py has set the projects directory to:"
    new "Ren'Py 已将工程目录设置为："

    # translations.rpy:91
    old "Translations: [project.current.display_name!q]"
    new "翻译：[project.current.display_name!q]"

    # translations.rpy:132
    old "The language to work with. This should only contain lower-case ASCII characters and underscores."
    new "生效的语言。该字段应仅包含小写 ASCII 字符和下划线。"

    # translations.rpy:158
    old "Generate empty strings for translations"
    new "为翻译生成空字串"

    # translations.rpy:176
    old "Generates or updates translation files. The files will be placed in game/tl/[persistent.translate_language!q]."
    new "生成或更新翻译文件。文件将放置在 game/tl/[persistent.translate_language!q]。"

    # translations.rpy:196
    old "Extract String Translations"
    new "导出字串翻译"

    # translations.rpy:198
    old "Merge String Translations"
    new "合并字串翻译"

    # translations.rpy:203
    old "Replace existing translations"
    new "替换已存在的翻译"

    # translations.rpy:204
    old "Reverse languages"
    new "反转语言"

    # translations.rpy:208
    old "Update Default Interface Translations"
    new "更新默认界面翻译"

    # translations.rpy:228
    old "The extract command allows you to extract string translations from an existing project into a temporary file.\n\nThe merge command merges extracted translations into another project."
    new "导出命令可使您从现有的工程中导出字串翻译至临时文件。\n\n合并命令将合并导出的翻译至其他工程。"

    # translations.rpy:252
    old "Ren'Py is generating translations...."
    new "Ren'Py 正在生成翻译文件……"

    # translations.rpy:263
    old "Ren'Py has finished generating [language] translations."
    new "Ren'Py 已完成 [language] 翻译文件的生成。"

    # translations.rpy:276
    old "Ren'Py is extracting string translations..."
    new "Ren'Py 正在导出字串翻译……"

    # translations.rpy:279
    old "Ren'Py has finished extracting [language] string translations."
    new "Ren'Py 已完成 [language] 字串翻译的导出。"

    # translations.rpy:299
    old "Ren'Py is merging string translations..."
    new "Ren'Py 正在合并字串翻译……"

    # translations.rpy:302
    old "Ren'Py has finished merging [language] string translations."
    new "Ren'Py 已完成 [language] 字串翻译的合并。"

    # translations.rpy:313
    old "Updating default interface translations..."
    new "正在更新默认界面翻译……"

    # translations.rpy:342
    old "Extract Dialogue: [project.current.display_name!q]"
    new "导出对话：[project.current.display_name!q]"

    # translations.rpy:358
    old "Format:"
    new "格式："

    # translations.rpy:366
    old "Tab-delimited Spreadsheet (dialogue.tab)"
    new "以制表符分隔的表格 (dialogue.tab)"

    # translations.rpy:367
    old "Dialogue Text Only (dialogue.txt)"
    new "仅对话文本 (dialogue.txt)"

    # translations.rpy:380
    old "Strip text tags from the dialogue."
    new "在对话中忽略文本标签。"

    # translations.rpy:381
    old "Escape quotes and other special characters."
    new "避开引号和其他特殊符号。"

    # translations.rpy:382
    old "Extract all translatable strings, not just dialogue."
    new "导出所有的可翻译字串，而非仅对话。"

    # translations.rpy:410
    old "Ren'Py is extracting dialogue...."
    new "Ren'Py 正在导出对话……"

    # translations.rpy:414
    old "Ren'Py has finished extracting dialogue. The extracted dialogue can be found in dialogue.[persistent.dialogue_format] in the base directory."
    new "Ren'Py 已完成导出对话。导出的对话可在基础目录下的 dialogue.[persistent.dialogue_format] 文件中找到。"

    # updater.rpy:63
    old "{b}Recommended.{/b} The version of Ren'Py that should be used in all newly-released games."
    new "{b}建议使用。{/b}此版本的 Ren'Py 应当用于全部新发布的游戏。"

    # updater.rpy:65
    old "Prerelease"
    new "预发布版"

    # updater.rpy:66
    old "A preview of the next version of Ren'Py that can be used for testing and taking advantage of new features, but not for final releases of games."
    new "Ren'Py 下个版本的预览版，可以用来测试和体验新功能，但不应该作为游戏的最终发布版本。"

    # updater.rpy:68
    old "Experimental"
    new "试验版"

    # updater.rpy:69
    old "Experimental versions of Ren'Py. You shouldn't select this channel unless asked by a Ren'Py developer."
    new "Ren'Py 的试验版。除非应 Ren'Py 开发者的要求，否则您不应选择这个通道。"

    # updater.rpy:71
    old "Nightly"
    new "每夜版"

    # updater.rpy:72
    old "The bleeding edge of Ren'Py development. This may have the latest features, or might not run at all."
    new "Ren'Py 的尖端开发版。此版本可能包含最新的功能，也可能甚至根本无法运行。"

    # updater.rpy:90
    old "Select Update Channel"
    new "选择更新通道"

    # updater.rpy:101
    old "The update channel controls the version of Ren'Py the updater will download."
    new "更新通道用于控制更新器所下载的 Ren'Py 版本。"

    # updater.rpy:110
    old "• This version is installed and up-to-date."
    new "• 该版本已安装并已更新至最新。"

    # updater.rpy:118
    old "%B %d, %Y"
    new "%Y-%m-%d"

    # updater.rpy:140
    old "An error has occured:"
    new "发生错误："

    # updater.rpy:142
    old "Checking for updates."
    new "正在检查更新。"

    # updater.rpy:144
    old "Ren'Py is up to date."
    new "Ren'Py 已更新到最新版本。"

    # updater.rpy:146
    old "[u.version] is now available. Do you want to install it?"
    new "[u.version] 现已可用。您希望现在安装吗？"

    # updater.rpy:148
    old "Preparing to download the update."
    new "正在准备下载更新。"

    # updater.rpy:150
    old "Downloading the update."
    new "正在下载更新。"

    # updater.rpy:152
    old "Unpacking the update."
    new "正在解压更新。"

    # updater.rpy:154
    old "Finishing up."
    new "完成。"

    # updater.rpy:156
    old "The update has been installed. Ren'Py will restart."
    new "更新已安装。Ren'Py 即将重启。"

    # updater.rpy:158
    old "The update has been installed."
    new "更新已安装。"

    # updater.rpy:160
    old "The update was cancelled."
    new "更新已取消。"

    # updater.rpy:177
    old "Ren'Py Update"
    new "Ren'Py 更新"

    # updater.rpy:183
    old "Proceed"
    new "继续"

    # updater.rpy:188
    old "Fetching the list of update channels"
    new "正在获取更新通道列表"
