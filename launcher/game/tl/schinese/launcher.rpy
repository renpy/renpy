translate schinese strings:

    # game/about.rpy:39
    old "[version!q]"
    new "[version!q]"

    # game/about.rpy:43
    old "View license"
    new "查看许可证"

    # game/add_file.rpy:28
    old "FILENAME"
    new "文件名"

    # game/add_file.rpy:28
    old "Enter the name of the script file to create."
    new "请输入要创建的脚本文件的名称。"

    # game/add_file.rpy:37
    old "The file name may not be empty."
    new "文件名不能为空。"

    # game/add_file.rpy:41
    old "The filename must have the .rpy extension."
    new "文件必须以 .rpy 为扩展名。"

    # game/add_file.rpy:50
    old "The file already exists."
    new "文件已存在。"

    # game/add_file.rpy:61
    old "# Ren'Py automatically loads all script files ending with .rpy. To use this\n# file, define a label and jump to it from another file.\n"
    new "# Ren'Py 自动加载所有扩展名为 .rpy 的脚本文件。要使用此\n# 文件，请先定义一个标签并从另一个文件跳转到此。\n"

    # game/android.rpy:34
    old "To build Android packages, please download RAPT, unzip it, and place it into the Ren'Py directory. Then restart the Ren'Py launcher."
    new "要构建安卓应用包，请下载 RAPT，并解压到 Ren'Py 目录中。之后重启 Ren'Py。"

    # game/android.rpy:35
    old "A 64-bit/x64 Java [JDK_REQUIREMENT] Development Kit is required to build Android packages on Windows. The JDK is different from the JRE, so it's possible you have Java without having the JDK.\n\nPlease {a=https://www.renpy.org/jdk/[JDK_REQUIREMENT]}download and install the JDK{/a}, then restart the Ren'Py launcher."
    new "在 Windows 中构建安卓应用包需要 64 位/x64 Java 8 开发套件（JDK）。JDK 不同于 JRE，所以您可能已安装过 Java 但尚未安装 JDK。\n\n请{a=https://www.renpy.org/jdk/[JDK_REQUIREMENT]}下载并安装 JDK{/a}，然后重启 Ren'Py。"

    # game/android.rpy:36
    old "RAPT has been installed, but you'll need to install the Android SDK before you can build Android packages. Choose Install SDK to do this."
    new "RAPT 已安装，但您还需要安装安卓 SDK 才可以构建安卓应用包。请继续安装 SDK。"

    # game/android.rpy:39
    old "RAPT has been installed, but a key hasn't been configured. Please generate new keys, or copy android.keystore and bundle.keystore to the base directory."
    new "RAPT 已安装，但尚未配置密钥。请生成新的密钥，或将 android.keystore 和 bundle.keystore 复制到基础目录中。"

    # game/android.rpy:39
    old "The current project has not been configured. Use \"Configure\" to configure it before building."
    new "当前项目尚未配置过。请在构建前使用“配置”来进行配置。"

    # game/android.rpy:40
    old "Please select if you want a Play Bundle (for Google Play), or a Universal APK (for sideloading and other app stores)."
    new "请选择您是否需要 Play Bundle（用于 Google Play）或是 Universal APK（用于侧载和其他应用商店）。"

    # game/android.rpy:41
    old "Choose \"Build\" to build the current project, or attach an Android device and choose \"Build & Install\" to build and install it on the device."
    new "选择“构建”来构建当前项目，或者在添加安卓设备之后，选择“构建并安装”来构建并安装到设备中。"

    # game/android.rpy:43
    old "Attempts to emulate an Android phone.\n\nTouch input is emulated through the mouse, but only when the button is held down. Escape is mapped to the menu button, and PageUp is mapped to the back button."
    new "尝试模拟为安卓手机。\n\n鼠标将仅在按键按下时模拟为触屏输入。Esc 和 PageUp 键将分别重映射为手机的菜单键和返回键。"

    # game/android.rpy:44
    old "Attempts to emulate an Android tablet.\n\nTouch input is emulated through the mouse, but only when the button is held down. Escape is mapped to the menu button, and PageUp is mapped to the back button."
    new "尝试模拟为安卓平板。\n\nEsc 和 PageUp 键将分别重映射为平板的菜单键和返回键。"

    # game/android.rpy:45
    old "Attempts to emulate a televison-based Android console.\n\nController input is mapped to the arrow keys, Enter is mapped to the select button, Escape is mapped to the menu button, and PageUp is mapped to the back button."
    new "尝试模拟为基于电视的安卓游戏机。\n\n键盘方向键将重映射为手柄方向键，Enter、Esc 和 PageUp 键将分别重映射为手柄的选择键、菜单键和返回键。"

    # game/android.rpy:47
    old "Downloads and installs the Android SDK and supporting packages."
    new "下载并安装安卓 SDK 以及支持包。"

    # game/android.rpy:49
    old "Generates the keys required to sign the package."
    new "生成对应用包进行签名所需的密钥。"

    # game/android.rpy:48
    old "Configures the package name, version, and other information about this project."
    new "配置此项目的应用包名称、版本号和其他信息。"

    # game/android.rpy:49
    old "Opens the file containing the Google Play keys in the editor.\n\nThis is only needed if the application is using an expansion APK. Read the documentation for more details."
    new "在编辑器中打开包含有 Google Play 密钥的文件。\n\n仅当应用使用扩展 APK 时才需要进行此操作。更多详情请参阅说明文档。"

    # game/android.rpy:50
    old "Builds the Android package."
    new "构建安卓应用包。"

    # game/android.rpy:51
    old "Builds the Android package, and installs it on an Android device connected to your computer."
    new "构建安卓应用包，并将其安装到连接至此计算机的安卓设备中。"

    # game/android.rpy:52
    old "Builds the Android package, installs it on an Android device connected to your computer, then launches the app on your device."
    new "构建安卓应用包，将其安装到连接至此计算机的安卓设备中，并在您的设备上打开此应用。"

    # game/android.rpy:54
    old "Retrieves the log from the Android device and writes it to a file."
    new "从安卓设备接收日志并将其写入至文件。"

    # game/android.rpy:55
    old "Lists the connected devices."
    new "列出所连接的设备。"

    # game/android.rpy:56
    old "Pairs with a device over Wi-Fi, on Android 11+."
    new "通过 Wi-Fi 与设备配对，适用于安卓 11+ 系统。"

    # game/android.rpy:57
    old "Connects to a device over Wi-Fi, on Android 11+."
    new "通过 Wi-Fi 连接到设备，适用于安卓 11+ 系统。"

    # game/android.rpy:58
    old "Disconnects a device connected over Wi-Fi."
    new "断开通过 Wi-Fi 连接的设备。"

    # game/android.rpy:60
    old "Removes Android temporary files."
    new "删除安卓临时文件。"

    # game/android.rpy:62
    old "Builds an Android App Bundle (ABB), intended to be uploaded to Google Play. This can include up to 2GB of data."
    new "构建 Android App Bundle (ABB)，旨在上传至 Google Play。可容纳多达 2GB 的数据。"

    # game/android.rpy:63
    old "Builds a Universal APK package, intended for sideloading and stores other than Google Play. This can include up to 2GB of data."
    new "构建 Universal APK 包，用于侧载和 Google Play 以外的商店。可容纳多达 2GB 的数据。"

    # game/android.rpy:266
    old "Copying Android files to distributions directory."
    new "正在复制安卓文件到发行版目录。"

    # game/android.rpy:335
    old "Android: [project.current.display_name!q]"
    new "安卓：[project.current.display_name!q]"

    # game/android.rpy:355
    old "Emulation:"
    new "模拟："

    # game/android.rpy:364
    old "Phone"
    new "手机"

    # game/android.rpy:368
    old "Tablet"
    new "平板"

    # game/android.rpy:372
    old "Television"
    new "电视"

    # game/android.rpy:384
    old "Build:"
    new "构建："

    # game/android.rpy:391
    old "Install SDK & Create Keys"
    new "安装 SDK 并创建密钥"

    # game/android.rpy:395
    old "Configure"
    new "配置"

    # game/android.rpy:401
    old "Play Bundle"
    new "Play Bundle"

    # game/android.rpy:406
    old "Universal APK"
    new "Universal APK"

    # game/android.rpy:413
    old "Build Package"
    new "构建应用包"

    # game/android.rpy:417
    old "Build & Install"
    new "构建并安装"

    # game/android.rpy:421
    old "Build, Install & Launch"
    new "构建、安装并启动"

    # game/android.rpy:427
    old "Force Recompile"
    new "强制重新编译"

    # game/android.rpy:444
    old "Other:"
    new "其他："

    # game/android.rpy:456
    old "List Devices"
    new "列出设备"

    # game/android.rpy:460
    old "Wi-Fi Debugging Pair"
    new "Wi-Fi 调试配对"

    # game/android.rpy:464
    old "Wi-Fi Debugging Connect"
    new "Wi-Fi 调试连接"

    # game/android.rpy:468
    old "Wi-Fi Debugging Disconnect"
    new "Wi-Fi 调试断开"

    # game/android.rpy:472
    old "Clean"
    new "清理"

    # game/android.rpy:497
    old "Before packaging Android apps, you'll need to download RAPT, the Ren'Py Android Packaging Tool. Would you like to download RAPT now?"
    new "在打包安卓应用之前，您需要先下载 Ren'Py 安卓打包工具 RAPT。您希望现在下载 RAPT 吗？"

    # game/android.rpy:550
    old "Retrieving logcat information from device."
    new "正在从设备检索 Logcat 信息。"

    # game/android.rpy:569
    old "Wi-Fi Pairing Code"
    new "Wi-Fi 配对码"

    # game/android.rpy:569
    old "If supported, this can be found in 'Developer options', 'Wireless debugging', 'Pair device with pairing code'."
    new "如果支持，可在“开发者选项”-“无线调试”-“使用配对码配对设备”中找到。"

    # game/android.rpy:576
    old "Pairing Host & Port"
    new "配对主机和端口"

    # game/android.rpy:592
    old "IP Address & Port"
    new "IP 地址和端口"

    # game/android.rpy:592
    old "If supported, this can be found in 'Developer options', 'Wireless debugging'."
    new "如果支持，可在“开发者选项”-“无线调试”中找到。"

    # game/android.rpy:608
    old "This can be found in 'List Devices'."
    new "可在“列出设备”中找到。"

    # game/android.rpy:628
    old "Cleaning up Android project."
    new "正在清理安卓项目。"

    # game/androidstrings.rpy:7
    old "{} is not a directory."
    new "{} 不是目录。"

    # game/androidstrings.rpy:8
    old "{} does not contain a Ren'Py game."
    new "{} 不包含 Ren'Py 游戏。"

    # game/androidstrings.rpy:10
    old "Run configure before attempting to build the app."
    new "请在尝试构建应用之前先进行配置。"

    # game/androidstrings.rpy:11
    old "Updating project."
    new "正在更新项目。"

    # game/androidstrings.rpy:12
    old "Creating assets directory."
    new "正在创建资源目录。"

    # game/androidstrings.rpy:13
    old "Packaging internal data."
    new "正在打包内部数据。"

    # game/androidstrings.rpy:14
    old "I'm using Gradle to build the package."
    new "正在使用 Gradle 构建应用包。"

    # game/androidstrings.rpy:15
    old "The build seems to have failed."
    new "构建似乎已失败。"

    # game/androidstrings.rpy:16
    old "I'm installing the bundle."
    new "正在安装 Bundle。"

    # game/androidstrings.rpy:17
    old "Installing the bundle appears to have failed."
    new "安装 Bundle 似乎已失败。"

    # game/androidstrings.rpy:18
    old "Launching app."
    new "正在启动应用。"

    # game/androidstrings.rpy:19
    old "Launching the app appears to have failed."
    new "启动应用似乎已失败。"

    # game/androidstrings.rpy:20
    old "The build seems to have succeeded."
    new "构建似乎已成功。"

    # game/androidstrings.rpy:21
    old "What is the full name of your application? This name will appear in the list of installed applications."
    new "应用的全名是什么？此名称将出现在已安装的应用列表中。"

    # game/androidstrings.rpy:22
    old "What is the short name of your application? This name will be used in the launcher, and for application shortcuts."
    new "应用的简称是什么？此名称将用于启动器和应用图标。"

    # game/androidstrings.rpy:23
    old "What is the name of the package?\n\nThis is usually of the form com.domain.program or com.domain.email.program. It may only contain ASCII letters and dots. It must contain at least one dot."
    new "应用的包名称是什么？\n\n此名称通常是 com.domain.program 或 com.domain.email.program 的形式。名称中只能包含 ASCII 字母和点。名称中应包含至少一个点。"

    # game/androidstrings.rpy:24
    old "The package name may not be empty."
    new "应用包名称不能为空。"

    # game/androidstrings.rpy:25
    old "The package name may not contain spaces."
    new "应用包名称不能包含空格。"

    # game/androidstrings.rpy:26
    old "The package name must contain at least one dot."
    new "应用包名称应包含至少一个点。"

    # game/androidstrings.rpy:27
    old "The package name may not contain two dots in a row, or begin or end with a dot."
    new "应用包名称不能包含连续两个点，或在开始和末尾的地方出现点。"

    # game/androidstrings.rpy:28
    old "Each part of the package name must start with a letter, and contain only letters, numbers, and underscores."
    new "应用包名称的每一部分必须以字母开头，并且应仅含字母、数字和下划线。"

    # game/androidstrings.rpy:29
    old "{} is a Java keyword, and can't be used as part of a package name."
    new "{} 是 Java 关键字，不能用于应用包名称。"

    # game/androidstrings.rpy:30
    old "What is the application's version?\n\nThis should be the human-readable version that you would present to a person. It must contain only numbers and dots."
    new "应用的版本号是什么？\n\n此版本号是您打算向用户展示的可读版本号。版本号应仅含数字和点。"

    # game/androidstrings.rpy:31
    old "The version number must contain only numbers and dots."
    new "版本号应仅含数字和点。"

    # game/androidstrings.rpy:32
    old "How much RAM (in GB) do you want to allocate to Gradle?\nThis must be a positive integer number."
    new "您希望为 Gradle 分配多少 GB 的内存？\n\n必须为正整数。"

    # game/androidstrings.rpy:33
    old "The RAM size must contain only numbers and be positive."
    new "内存大小应为正整数。"

    # game/androidstrings.rpy:34
    old "How would you like your application to be displayed?"
    new "您希望您的应用如何显示？"

    # game/androidstrings.rpy:35
    old "In landscape orientation."
    new "横屏模式。"

    # game/androidstrings.rpy:36
    old "In portrait orientation."
    new "竖屏模式。"

    # game/androidstrings.rpy:37
    old "In the user's preferred orientation."
    new "以用户希望的模式。"

    # game/androidstrings.rpy:38
    old "Do you want to automatically update the Java source code?"
    new "您希望自动更新 Java 源代码吗？"

    # game/androidstrings.rpy:39
    old "Yes. This is the best choice for most projects."
    new "是。此为大多数项目的最佳选择。"

    # game/androidstrings.rpy:40
    old "No. This may require manual updates when Ren'Py or the project configuration changes."
    new "否。当 Ren'Py 或项目配置发生变化时需要手动更新。"

    # game/androidstrings.rpy:41
    old "Unknown configuration variable: {}"
    new "未知的配置变量：{}"

    # game/androidstrings.rpy:42
    old "I'm compiling a short test program, to see if you have a working JDK on your system."
    new "正在编译一个简短的程序，来测试您的操作系统内是否有可用的 JDK。"

    # game/androidstrings.rpy:43
    old "I was unable to use javac to compile a test file. If you haven't installed the Java Development Kit yet, please download it from:\n\n{a=https://adoptium.net/?variant=openjdk8}https://adoptium.net/?variant=openjdk8{/a}\n\nThe JDK is different from the JRE, so it's possible you have Java without having the JDK. Please make sure you installed the 'JavaSoft (Oracle) registry keys'.\n\nWithout a working JDK, I can't continue."
    new "无法使用 javac 编译测试文件。如果您尚未安装 Java 开发套件（JDK），请从以下地址安装：\n\n{a=https://adoptium.net/?variant=openjdk8}https://adoptium.net/?variant=openjdk8{/a}\n\nJDK 不同于 JRE，所以您可能已安装过 Java 但尚未安装 JDK。请确保您安装了“JavaSoft (Oracle) 注册表项。”\n\n若缺乏可用的 JDK，程序将无法继续。"

    # game/androidstrings.rpy:44
    old "The version of Java on your computer does not appear to be JDK 8, which is the only version supported by the Android SDK. If you need to install JDK 8, you can download it from:\n\n{a=https://adoptium.net/?variant=openjdk8}https://adoptium.net/?variant=openjdk8{/a}\n\nYou can also set the JAVA_HOME environment variable to use a different version of Java."
    new "您计算机上的 Java 版本似乎不是 JDK 8，这是 Android SDK 支持的唯一版本。如果您需要安装 JDK 8，您可以从以下地址下载：\n\n{a=https://adoptium.net/?variant=openjdk8}https://adoptium.net/?variant=openjdk8{/a}\n\n您还可以设置 JAVA_HOME 环境变量来使用不同版本的 Java。"

    # game/androidstrings.rpy:45
    old "The JDK is present and working. Good!"
    new "JDK 存在且运行正常。太棒了！"

    # game/androidstrings.rpy:46
    old "The Android SDK has already been unpacked."
    new "Android SDK 已被解压。"

    # game/androidstrings.rpy:47
    old "Do you accept the Android SDK Terms and Conditions?"
    new "您是否接受 Android SDK 条款和条件？"

    # game/androidstrings.rpy:48
    old "I'm downloading the Android SDK. This might take a while."
    new "正在下载 Android SDK。这可能需要一段时间。"

    # game/androidstrings.rpy:49
    old "I'm extracting the Android SDK."
    new "正在提取 Android SDK。"

    # game/androidstrings.rpy:50
    old "I've finished unpacking the Android SDK."
    new "解压 Android SDK 已完成。"

    # game/androidstrings.rpy:51
    old "I'm about to download and install the required Android packages. This might take a while."
    new "即将下载并安装所需的安卓软件包。这可能需要一段时间。"

    # game/androidstrings.rpy:52
    old "I was unable to accept the Android licenses."
    new "无法接受安卓许可证。"

    # game/androidstrings.rpy:54
    old "I was unable to install the required Android packages."
    new "无法安装所需的安卓软件包。"

    # game/androidstrings.rpy:55
    old "I've finished installing the required Android packages."
    new "已完成安装所需的安卓软件包。"

    # game/androidstrings.rpy:56
    old "Please enter your name or the name of your organization."
    new "请输入您的名称或您组织的名称。"

    # game/androidstrings.rpy:57
    old "I can create an application signing key for you. This key is required to create Universal APK for sideloading and stores other than Google Play.\n\nDo you want to create a key?"
    new "Ren'Py 可以为您创建应用程序签名密钥。此密钥是创建 Universal APK 以进行侧载和上传至 Google Play 以外的商店所必需的。\n\n您要创建密钥吗？"

    # game/androidstrings.rpy:58
    old "I will create the key in the android.keystore file.\n\nYou need to back this file up. If you lose it, you will not be able to upgrade your application.\n\nYou also need to keep the key safe. If evil people get this file, they could make fake versions of your application, and potentially steal your users' data.\n\nWill you make a backup of android.keystore, and keep it in a safe place?"
    new "即将在 android.keystore 文件中创建密钥。\n\n您需要备份此文件。如果该文件丢失，您将无法更新您的应用。\n\n您还需要将密钥文件放置到安全的位置。若攻击者获取此文件，就可以假冒您的应用，并窃取用户数据。\n\n您是否会备份 android.keystore 并将其置于安全的位置？"

    # game/androidstrings.rpy:59
    old "Could not create android.keystore. Is keytool in your path?"
    new "无法创建 android.keystore。您是否将 Keytool 放置在了指定目录？"

    # game/androidstrings.rpy:60
    old "I've finished creating android.keystore. Please back it up, and keep it in a safe place."
    new "已完成创建 android.keystore。请将其备份并放置于安全的位置。"

    # game/androidstrings.rpy:61
    old "I can create a bundle signing key for you. This key is required to build an Android App Bundle (AAB) for upload to Google Play.\n\nDo you want to create a key?"
    new "Ren'Py 可以为您创建应用程序签名密钥。此密钥是创建 Android App Bundle (AAB) 以上传至 Google Play 商店所必需的。\n\n您要创建密钥吗？"

    # game/androidstrings.rpy:62
    old "I will create the key in the bundle.keystore file.\n\nYou need to back this file up. If you lose it, you will not be able to upgrade your application.\n\nYou also need to keep the key safe. If evil people get this file, they could make fake versions of your application, and potentially steal your users' data.\n\nWill you make a backup of bundle.keystore, and keep it in a safe place?"
    new "即将在 bundle.keystore 文件中创建密钥。\n\n您需要备份此文件。如果该文件丢失，您将无法更新您的应用。\n\n您还需要将密钥文件放置到安全的位置。若攻击者获取此文件，就可以假冒您的应用，并窃取用户数据。\n\n您是否会备份 bundle.keystore 并将其置于安全的位置？"

    # game/androidstrings.rpy:63
    old "Could not create bundle.keystore. Is keytool in your path?"
    new "无法创建 bundle.keystore。您是否将 Keytool 放置在了指定目录？"

    # game/androidstrings.rpy:64
    old "I've opened the directory containing android.keystore and bundle.keystore. Please back them up, and keep them in a safe place."
    new "包含 android.keystore 和 bundle.keystore 的目录已打开。请备份它们，并将其置于安全的位置。"

    # game/androidstrings.rpy:65
    old "It looks like you're ready to start packaging games."
    new "看起来您已准备好开始打包游戏了。"

    # game/choose_directory.rpy:67
    old "Select Projects Directory"
    new "选择项目目录"

    # game/choose_directory.rpy:79
    old "The selected projects directory is not writable."
    new "所选的项目目录无法执行写入操作。"

    # game/choose_theme.rpy:304
    old "Could not change the theme. Perhaps options.rpy was changed too much."
    new "无法更改主题。可能 options.rpy 已被过度修改。"

    # game/choose_theme.rpy:426
    old "Choose Theme"
    new "选择主题"

    # game/choose_theme.rpy:439
    old "Theme"
    new "主题"

    # game/choose_theme.rpy:464
    old "Color Scheme"
    new "配色方案"

    # game/choose_theme.rpy:496
    old "Continue"
    new "继续"

    # game/choose_theme.rpy:508 此处与 While 连用
    old "changing the theme"
    new "更改主题"

    # game/consolecommand.rpy:91
    old "INFORMATION"
    new "信息"

    # game/consolecommand.rpy:91
    old "The command is being run in a new operating system console window."
    new "此命令正在新的操作系统控制台窗口中运行。"

    # game/distribute.rpy:490
    old "Scanning project files..."
    new "正在扫描项目文件……"

    # game/distribute.rpy:516
    old "Building distributions failed:\n\nThe build.directory_name variable may not include the space, colon, or semicolon characters."
    new "构建分发失败：\n\n变量 build.directory_name 不能包含空格、冒号和分号。"

    # game/distribute.rpy:562
    old "No packages are selected, so there's nothing to do."
    new "因未选择任何打包平台，故未执行任何操作。"

    # game/distribute.rpy:574
    old "Scanning Ren'Py files..."
    new "正在扫描 Ren'Py 文件……"

    # game/distribute.rpy:643
    old "All packages have been built.\n\nDue to the presence of permission information, unpacking and repacking the Linux and Macintosh distributions on Windows is not supported."
    new "已构建所有的分发包。\n\n由于存在权限信息，因此不支持在 Windows 上解包并重新打包 Linux 和 Macintosh 发行版。"

    # game/distribute.rpy:846
    old "Archiving files..."
    new "正在封装文件……"

    # game/distribute.rpy:1207
    old "Unpacking the Macintosh application for signing..."
    new "正在解压 Macintosh 应用并签名……"

    # game/distribute.rpy:1217
    old "Signing the Macintosh application...\n(This may take a long time.)"
    new "正在签名 Macintosh 应用……\n（可能需要很长时间。）"

    # game/distribute.rpy:1240
    old "Creating the Macintosh DMG..."
    new "正在创建 Macintosh DMG……"

    # game/distribute.rpy:1251
    old "Signing the Macintosh DMG..."
    new "正在签名 Macintosh DMG……"

    # game/distribute.rpy:1472
    old "Writing the [variant] [format] package."
    new "正在写入 [variant] 版 [format] 包。"

    # game/distribute.rpy:1485
    old "Making the [variant] update zsync file."
    new "正在制作 [variant] 版更新同步文件。"

    # game/distribute.rpy:1598
    old "Processed {b}[complete]{/b} of {b}[total]{/b} files."
    new "已处理 {b}[complete]{/b} / {b}[total]{/b} 个文件。"

    # game/distribute.rpy:1659
    old "Recompiling all rpy files into rpyc files..."
    new "正在将全部的 rpy 文件重新编译为 rpyc 文件……"

    # game/distribute.rpy:1674
    old "Copying files..."
    new "正在复制文件……"

    # game/distribute_gui.rpy:157
    old "Build Distributions: [project.current.display_name!q]"
    new "构建发行版：[project.current.display_name!q]"

    # game/distribute_gui.rpy:171
    old "Directory Name:"
    new "目录名："

    # game/distribute_gui.rpy:175
    old "Executable Name:"
    new "可执行程序名："

    # game/distribute_gui.rpy:185
    old "Actions:"
    new "操作："

    # game/distribute_gui.rpy:193
    old "Edit options.rpy"
    new "编辑 options.rpy"

    # game/distribute_gui.rpy:194
    old "Add from clauses to calls, once"
    new "向 call 语句添加 from 从句，执行一次"

    # game/distribute_gui.rpy:195
    old "Update old-game"
    new "更新 old-game"

    # game/distribute_gui.rpy:196
    old "Refresh"
    new "刷新"

    # game/distribute_gui.rpy:200
    old "Upload to itch.io"
    new "上传到 itch.io"

    # game/distribute_gui.rpy:216
    old "Build Packages:"
    new "构建分发包："

    # game/distribute_gui.rpy:235
    old "Options:"
    new "选项："

    # game/distribute_gui.rpy:240
    old "Build Updates"
    new "构建更新"

    # game/distribute_gui.rpy:242
    old "Add from clauses to calls"
    new "向 call 语句添加 from 从句"

    # game/distribute_gui.rpy:247
    old "Build"
    new "构建"

    # game/distribute_gui.rpy:251
    old "Adding from clauses to call statements that do not have them."
    new "正在向 call 语句添加缺失的 from 从句。"

    # game/distribute_gui.rpy:275
    old "Errors were detected when running the project. Please ensure the project runs without errors before building distributions."
    new "运行项目时检测到错误。请确保项目运行时没有错误，然后再构建分发。"

    # game/distribute_gui.rpy:294
    old "Your project does not contain build information. Would you like to add build information to the end of options.rpy?"
    new "您的项目尚未包含构建信息。您希望在 options.rpy 末端添加构建信息吗？"

    # game/dmgcheck.rpy:50
    old "Ren'Py is running from a read only folder. Some functionality will not work."
    new "Ren'Py 目前正在从只读文件夹运行。某些功能将无法工作。"

    # game/dmgcheck.rpy:50
    old "This is probably because Ren'Py is running directly from a Macintosh drive image. To fix this, quit this launcher, copy the entire %s folder somewhere else on your computer, and run Ren'Py again."
    new "这可能是由于 Ren'Py 直接从 Macintosh 磁盘镜像中运行导致的。要解决此问题，退出 Ren'Py，将整个 %s 文件夹复制到计算机上的其他位置，然后再次运行 Ren'Py。"

    # game/editor.rpy:152
    old "A modern editor with many extensions including advanced Ren'Py integration."
    new "具有许多扩展功能的现代编辑器，包括高级 Ren'Py 集成。"

    # game/editor.rpy:153
    old "A modern editor with many extensions including advanced Ren'Py integration.\n{a=jump:reinstall_vscode}Upgrade Visual Studio Code to the latest version.{/a}"
    new "具有许多扩展功能的现代编辑器，包括高级 Ren'Py 集成。\n{a=jump:reinstall_vscode}将 Visual Studio Code 升级到最新版本。{/a}"

    # game/editor.rpy:162
    old "Visual Studio Code"
    new "Visual Studio Code"

    # game/editor.rpy:162
    old "Up to 110 MB download required."
    new "需要下载最多 110 MB 的文件。"

    # game/editor.rpy:175
    old "A modern and approachable text editor."
    new "现代化且人性化的文本编辑器。"

    # game/editor.rpy:187
    old "Atom"
    new "Atom"

    # game/editor.rpy:187
    old "Up to 150 MB download required."
    new "需要下载最多 150 MB 的文件。"

    # game/editor.rpy:200
    old "jEdit"
    new "jEdit"

    # game/editor.rpy:200
    old "A mature editor that requires Java."
    new "成熟的编辑器，需要安装 Java。"

    # game/editor.rpy:200
    old "1.8 MB download required."
    new "需要下载 1.8 MB 的文件。"

    # game/editor.rpy:200
    old "This may have occured because Java is not installed on this system."
    new "这可能是由于您的系统中尚未安装 Java 造成的。"

    # game/editor.rpy:209
    old "Visual Studio Code (System)"
    new "Visual Studio Code（操作系统）"

    # game/editor.rpy:209
    old "Uses a copy of Visual Studio Code that you have installed outside of Ren'Py. It's recommended you install the language-renpy extension to add support for Ren'Py files."
    new "使用您在 Ren'Py 之外安装的 Visual Studio Code 副本。建议您安装 language-renpy 扩展来增加对 Ren'Py 文件的支持。"

    # game/editor.rpy:215
    old "System Editor"
    new "操作系统编辑器"

    # game/editor.rpy:215
    old "Invokes the editor your operating system has associated with .rpy files."
    new "调用您操作系统与 .rpy 文件关联的编辑器。"

    # game/editor.rpy:234
    old "None"
    new "无"

    # game/editor.rpy:234
    old "Prevents Ren'Py from opening a text editor."
    new "阻止 Ren'Py 打开文本编辑器。"

    # game/editor.rpy:341
    old "Edit [text]."
    new "编辑 [text]。"

    # game/editor.rpy:390
    old "An exception occured while launching the text editor:\n[exception!q]"
    new "启动编辑器时发生异常：\n[exception!q]"

    # game/editor.rpy:522
    old "Select Editor"
    new "选择编辑器"

    # game/editor.rpy:537
    old "A text editor is the program you'll use to edit Ren'Py script files. Here, you can select the editor Ren'Py will use. If not already present, the editor will be automatically downloaded and installed."
    new "文本编辑器是用于编辑 Ren'Py 脚本文件的程序。在这里您可以选择 Ren'Py 要使用的编辑器。若您选择的编辑器不存在，Ren'Py 将会自动下载并安装此编辑器。"

    # game/front_page.rpy:58
    old "PROJECTS:"
    new "项目："

    # game/front_page.rpy:60
    old "refresh"
    new "刷新"

    # game/front_page.rpy:87
    old "+ Create New Project"
    new "+ 创建新项目"

    # game/front_page.rpy:97
    old "Launch Project"
    new "启动项目"

    # game/front_page.rpy:114
    old "[p.name!q] (template)"
    new "[p.name!q]（模板）"

    # game/front_page.rpy:116
    old "Select project [text]."
    new "选择项目 [text]。"

    # game/front_page.rpy:132
    old "Tutorial"
    new "教程"

    # game/front_page.rpy:149
    old "Active Project"
    new "活跃项目"

    # game/front_page.rpy:157
    old "Open Directory"
    new "打开目录"

    # game/front_page.rpy:162
    old "game"
    new "game"

    # game/front_page.rpy:163
    old "base"
    new "base"

    # game/front_page.rpy:164
    old "images"
    new "images"

    # game/front_page.rpy:165
    old "audio"
    new "audio"

    # game/front_page.rpy:166
    old "gui"
    new "gui"

    # game/front_page.rpy:171
    old "Edit File"
    new "编辑文件"

    # game/front_page.rpy:182
    old "Open project"
    new "打开项目"

    # game/front_page.rpy:184
    old "All script files"
    new "全部脚本文件"

    # game/front_page.rpy:188
    old "Actions"
    new "操作"

    # game/front_page.rpy:197
    old "Navigate Script"
    new "定位脚本"

    # game/front_page.rpy:198
    old "Check Script (Lint)"
    new "使用 Lint 检查脚本"

    # game/front_page.rpy:201
    old "Change/Update GUI"
    new "更改/更新 GUI"

    # game/front_page.rpy:203
    old "Change Theme"
    new "更改主题"

    # game/front_page.rpy:206
    old "Delete Persistent"
    new "删除持久化数据"

    # game/front_page.rpy:215
    old "Build Distributions"
    new "构建发行版"

    # game/front_page.rpy:217
    old "Android"
    new "安卓"

    # game/front_page.rpy:218
    old "iOS"
    new "iOS"

    # game/front_page.rpy:219
    old "Web"
    new "网页"

    # game/front_page.rpy:219
    old "(Beta)"
    new "（测试版）"

    # game/front_page.rpy:223
    old "Generate Translations"
    new "生成翻译"

    # game/front_page.rpy:224
    old "Extract Dialogue"
    new "提取对话"

    # game/front_page.rpy:262
    old "Checking script for potential problems..."
    new "正在检查脚本中的潜在问题……"

    # game/front_page.rpy:277
    old "Deleting persistent data..."
    new "正在删除持久化数据……"

    # game/gui7.rpy:243
    old "Select Accent and Background Colors"
    new "选择强调色和背景色"

    # game/gui7.rpy:257
    old "Please click on the color scheme you wish to use, then click Continue. These colors can be changed and customized later."
    new "请点击您希望使用的颜色方案，然后点击“继续”。这些颜色稍后也可更改及自定义。"

    # game/gui7.rpy:302
    old "{b}Warning{/b}\nContinuing will overwrite customized bar, button, save slot, scrollbar, and slider images.\n\nWhat would you like to do?"
    new "{b}警告{/b}\n继续将会覆盖自定义的状态条、按钮、存档位和滑条滑块图。\n\n您希望执行哪种操作？"

    # game/gui7.rpy:302
    old "{size=-4}\n\nThis will not overwrite gui/main_menu.png, gui/game_menu.png, and gui/window_icon.png, but will create files that do not exist.{/size}"
    new "{size=-4}\n\n这不会覆盖 gui/main_menu.png、gui/game_menu.png 和 gui/window_icon.png，但会创建不存在的文件。{/size}"

    # game/gui7.rpy:302
    old "Choose new colors, then regenerate image files."
    new "选择新颜色，然后重新生成图像文件。"

    # game/gui7.rpy:302
    old "Regenerate the image files using the colors in gui.rpy."
    new "使用 gui.rpy 中的颜色重新生成图像文件。"

    # game/gui7.rpy:333
    old "What resolution should the project use? Although Ren'Py can scale the window up and down, this is the initial size of the window, the size at which assets should be drawn, and the size at which the assets will be at their sharpest.\n\nThe default of [default_size[0]]x[default_size[1]] is a reasonable compromise."
    new "项目使用哪种基准分辨率？虽然 Ren'Py 可以向上或向下缩放窗口，但此分辨率将是窗口的初始尺寸、资源绘制的基准尺寸以及资源显示最清晰的尺寸。\n\n默认的 [default_size[0]]x[default_size[1]] 是合理的折中方案。"

    # game/gui7.rpy:333
    old "Custom. The GUI is optimized for a 16:9 aspect ratio."
    new "自定义。GUI 针对 16:9 的宽高比进行了优化。"

    # game/gui7.rpy:350
    old "WIDTH"
    new "宽度"

    # game/gui7.rpy:350
    old "Please enter the width of your game, in pixels."
    new "请输入游戏的宽度，单位为像素。"

    # game/gui7.rpy:360
    old "The width must be a number."
    new "宽度必须是数字。"

    # game/gui7.rpy:366
    old "HEIGHT"
    new "高度"

    # game/gui7.rpy:366
    old "Please enter the height of your game, in pixels."
    new "请输入游戏的高度，单位为像素。"

    # game/gui7.rpy:376
    old "The height must be a number."
    new "高度必须是数字。"

    # game/gui7.rpy:420
    old "Creating the new project..."
    new "正在创建新项目……"

    # game/gui7.rpy:422
    old "Updating the project..."
    new "正在更新项目……"

    # game/gui7.rpy:424 此处与 While 连用
    old "creating a new project"
    new "创建新项目"

    # game/gui7.rpy:428 此处与 While 连用
    old "activating the new project"
    new "激活新项目"

    # game/install.rpy:33
    old "Could not install [name!t], as a file matching [zipglob] was not found in the Ren'Py SDK directory."
    new "无法安装 [name!t]，因为在 Ren'Py SDK 目录中找不到匹配 [zipglob] 的文件。"

    # game/install.rpy:79
    old "Successfully installed [name!t]."
    new "已成功安装 [name!t]。"

    # game/install.rpy:114
    old "This screen allows you to install libraries that can't be distributed with Ren'Py. Some of these libraries may require you to agree to a third-party license before being used or distributed."
    new "此界面允许您安装 Ren'Py 无法分发的库。其中一些库可能会要求您在使用或分发之前同意第三方许可。"

    # game/install.rpy:120
    old "Install Steam Support"
    new "安装 Steam 支持包"

    # game/install.rpy:129
    old "Before installing Steam support, please make sure you are a {a=https://partner.steamgames.com/}Steam partner{/a}."
    new "在安装 Steam 支持包之前，请确保您是 {a=https://partner.steamgames.com/}Steam 合作伙伴{/a}。"

    # game/install.rpy:141
    old "Steam support has already been installed."
    new "Steam 支持包已安装。"

    # game/install.rpy:145
    old "Install Live2D Cubism SDK for Native"
    new "安装 Live2D Cubism SDK for Native"

    # game/install.rpy:159
    old "Install Libraries"
    new "安装库"

    # game/install.rpy:185
    old "The {a=https://www.live2d.com/en/download/cubism-sdk/download-native/}Cubism SDK for Native{/a} adds support for displaying Live2D models. Place CubismSdkForNative-4-{i}version{/i}.zip in the Ren'Py SDK directory, and then click Install. Distributing a game with Live2D requires you to accept a license from Live2D, Inc."
    new "{a=https://www.live2d.com/en/download/cubism-sdk/download-native/}Cubism SDK for Native{/a} 增加了对显示 Live2D 模型的支持。将 CubismSdkForNative-4-{i}version{/i}.zip 放在 Ren'Py SDK 目录中，然后点击“安装”。使用 Live2D 分发游戏需要您接受 Live2D 公司的许可。"

    # game/install.rpy:189
    old "Live2D in Ren'Py doesn't support the Web, Android x86_64 (including emulators and Chrome OS), and must be added to iOS projects manually. Live2D must be reinstalled after upgrading Ren'Py or installing Android support."
    new "Ren'Py 中的 Live2D 不支持网页版和安卓 x86_64（包括模拟器和 Chrome OS），且必须手动添加至 iOS 项目中。更新 Ren'Py 或安装安卓支持包后需要重新安装 Live2D。"

    # game/install.rpy:194
    old "Open Ren'Py SDK Directory"
    new "打开 Ren'Py SDK 目录"

    # game/installer.rpy:10
    old "Downloading [extension.download_file]."
    new "正在下载 [extension.download_file]。"

    # game/installer.rpy:11
    old "Could not download [extension.download_file] from [extension.download_url]:\n{b}[extension.download_error]"
    new "无法从 [extension.download_url] 下载 [extension.download_file]：\n{b}[extension.download_error]"

    # game/installer.rpy:12
    old "The downloaded file [extension.download_file] from [extension.download_url] is not correct."
    new "从 [extension.download_url] 下载的文件 [extension.download_file] 不正确。"

    # game/interface.rpy:122
    old "Documentation"
    new "说明文档"

    # game/interface.rpy:123
    old "Ren'Py Website"
    new "Ren'Py 官方网站"

    # game/interface.rpy:124
    old "[interface.version]"
    new "[interface.version]"

    # game/interface.rpy:131
    old "update"
    new "更新"

    # game/interface.rpy:136
    old "preferences"
    new "设置"

    # game/interface.rpy:137
    old "quit"
    new "退出"

    # game/interface.rpy:141
    old "Ren'Py Sponsor Information"
    new "Ren'Py 赞助者信息"

    # game/interface.rpy:269
    old "Due to package format limitations, non-ASCII file and directory names are not allowed."
    new "由于包格式限制，无法使用非 ASCII 文件名和目录名。"

    # game/interface.rpy:365
    old "ERROR"
    new "错误"

    # game/interface.rpy:377
    old "opening the log file"
    new "打开日志文件"

    # game/interface.rpy:399
    old "While [what!qt], an error occured:"
    new "[what!qt]时出错："

    # game/interface.rpy:399
    old "[exception!q]"
    new "[exception!q]"

    # game/interface.rpy:432
    old "Text input may not contain the {{ or [[ characters."
    new "文本输入不能包含 {{ 或 [[ 字符。"

    # game/interface.rpy:437
    old "File and directory names may not contain / or \\."
    new "文件名或目录名不能包含 / 或 \\。"

    # game/interface.rpy:443
    old "File and directory names must consist of ASCII characters."
    new "文件名或目录名必须仅由 ASCII 字符组成，不能包含中文。"

    # game/interface.rpy:511
    old "PROCESSING"
    new "正在处理"

    # game/interface.rpy:528
    old "QUESTION"
    new "问题"

    # game/interface.rpy:541
    old "CHOICE"
    new "选择"

    # game/ios.rpy:28
    old "To build iOS packages, please download renios, unzip it, and place it into the Ren'Py directory. Then restart the Ren'Py launcher."
    new "要构建 iOS 应用包，请下载 renios 并解压至 Ren'Py 目录中。之后重启 Ren'Py。"

    # game/ios.rpy:29
    old "The directory in where Xcode projects will be placed has not been selected. Choose 'Select Directory' to select it."
    new "尚未指定 Xcode 项目所在的目录。选择“指定目录”来指定。"

    # game/ios.rpy:30
    old "There is no Xcode project corresponding to the current Ren'Py project. Choose 'Create Xcode Project' to create one."
    new "当前 Ren'Py 项目尚无对应的 Xcode 项目。选择“创建 Xcode 项目”来进行创建。"

    # game/ios.rpy:31
    old "An Xcode project exists. Choose 'Update Xcode Project' to update it with the latest game files, or use Xcode to build and install it."
    new "该 Xcode 项目已经存在。选择“更新 Xcode 项目”更新为最新的游戏文件，或使用 Xcode 来构建并安装。"

    # game/ios.rpy:33
    old "Attempts to emulate an iPhone.\n\nTouch input is emulated through the mouse, but only when the button is held down."
    new "尝试模拟为 iPhone。\n\n鼠标将仅在按键按下时模拟为触屏输入。"

    # game/ios.rpy:34
    old "Attempts to emulate an iPad.\n\nTouch input is emulated through the mouse, but only when the button is held down."
    new "尝试模拟为 iPad。\n\n鼠标将仅在按键按下时模拟为触屏输入。"

    # game/ios.rpy:36
    old "Selects the directory where Xcode projects will be placed."
    new "请指定 Xcode 项目所在的目录。"

    # game/ios.rpy:37
    old "Creates an Xcode project corresponding to the current Ren'Py project."
    new "创建与当前 Ren'Py 项目对应的 Xcode 项目。"

    # game/ios.rpy:38
    old "Updates the Xcode project with the latest game files. This must be done each time the Ren'Py project changes."
    new "以最新的游戏文件更新 Xcode 项目。此操作应在每次 Ren'Py 项目出现更改时执行一次。"

    # game/ios.rpy:39
    old "Opens the Xcode project in Xcode."
    new "在 Xcode 中打开 Xcode 项目。"

    # game/ios.rpy:41
    old "Opens the directory containing Xcode projects."
    new "打开包含 Xcode 项目的目录。"

    # game/ios.rpy:139
    old "The Xcode project already exists. Would you like to rename the old project, and replace it with a new one?"
    new "Xcode 项目已经存在。您希望重命名旧项目并用新项目替换它吗？"

    # game/ios.rpy:269
    old "iOS: [project.current.display_name!q]"
    new "iOS：[project.current.display_name!q]"

    # game/ios.rpy:298
    old "iPhone"
    new "iPhone"

    # game/ios.rpy:302
    old "iPad"
    new "iPad"

    # game/ios.rpy:322
    old "Select Xcode Projects Directory"
    new "指定 Xcode 项目目录"

    # game/ios.rpy:326
    old "Create Xcode Project"
    new "创建 Xcode 项目"

    # game/ios.rpy:330
    old "Update Xcode Project"
    new "更新 Xcode 项目"

    # game/ios.rpy:335
    old "Launch Xcode"
    new "启动 Xcode"

    # game/ios.rpy:358
    old "Open Xcode Projects Directory"
    new "打开 Xcode 项目目录"

    # game/ios.rpy:379
    old "There are known issues with the iOS simulator on Apple Silicon. Please test on x86_64 or iOS devices."
    new "Apple Silicon 上的 iOS 模拟器存在已知问题。请在 x86_64 或 iOS 设备上进行测试。"

    # game/ios.rpy:395
    old "Before packaging iOS apps, you'll need to download renios, Ren'Py's iOS support. Would you like to download renios now?"
    new "在打包 iOS 应用之前，您需要先下载 Ren'Py iOS 支持包 renios。您希望现在下载 renios 吗？"

    # game/ios.rpy:404
    old "XCODE PROJECTS DIRECTORY"
    new "XCODE 项目目录"

    # game/ios.rpy:404
    old "Please choose the Xcode Projects Directory using the directory chooser.\n{b}The directory chooser may have opened behind this window.{/b}"
    new "请使用弹出的目录选择窗口来指定 Xcode 项目目录。\n{b}目录选择窗口可能会被本窗口覆盖。{/b}"

    # game/ios.rpy:409
    old "Ren'Py has set the Xcode Projects Directory to:"
    new "Ren'Py 已将 Xcode 项目目录设置为："

    # game/itch.rpy:43
    old "Downloading the itch.io butler."
    new "正在下载 itch.io 工具 Butler。"

    # game/itch.rpy:96
    old "The built distributions could not be found. Please choose 'Build' and try again."
    new "未找到已构建的发行版。请点击“构建”重试。"

    # game/itch.rpy:134
    old "No uploadable files were found. Please choose 'Build' and try again."
    new "未找到可上传的文件。请点击“构建”重试。"

    # game/itch.rpy:140
    old "The butler program was not found."
    new "未找到 Butler 工具。"

    # game/itch.rpy:140
    old "Please install the itch.io app, which includes butler, and try again."
    new "itch.io 应用中包含 Butler 工具。请安装 itch.io 应用并重试。"

    # game/itch.rpy:149
    old "The name of the itch project has not been set."
    new "尚未设置 itch 项目名。"

    # game/itch.rpy:149
    old "Please {a=https://itch.io/game/new}create your project{/a}, then add a line like \n{vspace=5}define build.itch_project = \"user-name/game-name\"\n{vspace=5} to options.rpy."
    new "请{a=https://itch.io/game/new}创建您的项目{/a}，并在 options.rpy 里添加类似以下代码：\n{vspace=5}define build.itch_project = \"user-name/game-name\""

    # game/mobilebuild.rpy:114
    old "{a=%s}%s{/a}"
    new "{a=%s}%s{/a}"

    # game/navigation.rpy:168
    old "Navigate: [project.current.display_name!q]"
    new "定位：[project.current.display_name!q]"

    # game/navigation.rpy:178
    old "Order: "
    new "排序方式："

    # game/navigation.rpy:179
    old "alphabetical"
    new "名称"

    # game/navigation.rpy:181
    old "by-file"
    new "按文件分组"

    # game/navigation.rpy:183
    old "natural"
    new "出现顺序"

    # game/navigation.rpy:195
    old "Category:"
    new "类别："

    # game/navigation.rpy:198
    old "files"
    new "文件"

    # game/navigation.rpy:199
    old "labels"
    new "标签"

    # game/navigation.rpy:200
    old "defines"
    new "定义"

    # game/navigation.rpy:201
    old "transforms"
    new "变换"

    # game/navigation.rpy:202
    old "screens"
    new "屏幕"

    # game/navigation.rpy:203
    old "callables"
    new "可调用"

    # game/navigation.rpy:204
    old "TODOs"
    new "待办事项"

    # game/navigation.rpy:243
    old "+ Add script file"
    new "+ 添加脚本文件"

    # game/navigation.rpy:251
    old "No TODO comments found.\n\nTo create one, include \"# TODO\" in your script."
    new "未找到 TODO 注释。要创建一个，请在脚本中加入“# TODO”即可。"

    # game/navigation.rpy:258
    old "The list of names is empty."
    new "列表为空。"

    # game/new_project.rpy:38
    old "New GUI Interface"
    new "新 GUI 界面"

    # game/new_project.rpy:48
    old "Both interfaces have been translated to your language."
    new "两种界面均已翻译成您的语言。"

    # game/new_project.rpy:50
    old "Only the new GUI has been translated to your language."
    new "仅有新 GUI 已翻译成您的语言。"

    # game/new_project.rpy:52
    old "Only the legacy theme interface has been translated to your language."
    new "仅有传统主题界面已翻译成您的语言。"

    # game/new_project.rpy:54
    old "Neither interface has been translated to your language."
    new "两种界面均未翻译成您的语言。"

    # game/new_project.rpy:63
    old "The projects directory could not be set. Giving up."
    new "项目目录无法设置。操作取消。"

    # game/new_project.rpy:70
    old "Which interface would you like to use? The new GUI has a modern look, supports wide screens and mobile devices, and is easier to customize. Legacy themes might be necessary to work with older example code.\n\n[language_support!t]\n\nIf in doubt, choose the new GUI, then click Continue on the bottom-right."
    new "您希望使用哪种界面？新 GUI 具有更现代的设计，可支持宽屏和移动设备，定制起来也更容易。对于较早的示范代码，传统主题可能是必须的。\n\n[language_support!t]\n\n如有疑问，请选择新 GUI，并点击右下角的“继续”。"

    # game/new_project.rpy:70
    old "Legacy Theme Interface"
    new "传统主题界面"

    # game/new_project.rpy:77
    old "{#language name and font}"
    new "{font=SourceHanSansLite.ttf}简体中文{/font}"

    # game/new_project.rpy:81
    old "You will be creating an [new_project_language]{#this substitution may be localized} language project. Change the launcher language in preferences to create a project in another language."
    new "即将创建[new_project_language]语言的项目。要创建其他语言的项目，请在设置中更改 Ren'Py 语言。"

    # game/new_project.rpy:86
    old "PROJECT NAME"
    new "项目名称"

    # game/new_project.rpy:86
    old "Please enter the name of your project:"
    new "请输入新项目的名称："

    # game/new_project.rpy:96
    old "The project name may not be empty."
    new "项目名不能为空。"

    # game/new_project.rpy:102
    old "[project_name!q] already exists. Please choose a different project name."
    new "[project_name!q] 已经存在。请选择一个不同的项目名称。"

    # game/new_project.rpy:106
    old "[project_dir!q] already exists. Please choose a different project name."
    new "[project_dir!q] 已经存在。请选择一个不同的项目名称。"

    # game/new_project.rpy:124
    old "Choose Project Template"
    new "选择项目模板"

    # game/new_project.rpy:142
    old "Please select a template to use for your new project. The template sets the default font and the user interface language. If your language is not supported, choose 'english'."
    new "请为您的新项目选择一个模板。模板已预置了默认字体和用户界面语言。如果您的语言未受支持，请选择“英语”。"

    # game/preferences.rpy:88
    old "Launcher Preferences"
    new "启动器设置"

    # game/preferences.rpy:106
    old "General"
    new "一般"

    # game/preferences.rpy:107
    old "Options"
    new "选项"

    # game/preferences.rpy:131
    old "Projects Directory:"
    new "项目目录："

    # game/preferences.rpy:138
    old "[persistent.projects_directory!q]"
    new "[persistent.projects_directory!q]"

    # game/preferences.rpy:140
    old "Projects directory: [text]"
    new "项目目录：[text]"

    # game/preferences.rpy:142
    old "Not Set"
    new "未指定"

    # game/preferences.rpy:155
    old "Text Editor:"
    new "文本编辑器："

    # game/preferences.rpy:161
    old "Text editor: [text]"
    new "文本编辑器：[text]"

    # game/preferences.rpy:173
    old "Language:"
    new "语言："

    # game/preferences.rpy:200
    old "Navigation Options:"
    new "定位选项："

    # game/preferences.rpy:204
    old "Include private names"
    new "包含私有名称"

    # game/preferences.rpy:205
    old "Include library names"
    new "包含库名称"

    # game/preferences.rpy:214
    old "Launcher Options:"
    new "启动器选项："

    # game/preferences.rpy:218
    old "Show edit file section"
    new "显示编辑文件部件"

    # game/preferences.rpy:219
    old "Large fonts"
    new "大字体"

    # game/preferences.rpy:222
    old "Console output"
    new "控制台输出"

    # game/preferences.rpy:224
    old "Sponsor message"
    new "赞助者信息"

    # game/preferences.rpy:227
    old "Daily check for update"
    new "每日检查更新"

    # game/preferences.rpy:246
    old "Launcher Theme:"
    new "启动器主题："

    # game/preferences.rpy:250
    old "Default theme"
    new "默认主题"

    # game/preferences.rpy:251
    old "Dark theme"
    new "深色主题"

    # game/preferences.rpy:252
    old "Custom theme"
    new "自定义主题"

    # game/preferences.rpy:256
    old "Information about creating a custom theme can be found {a=https://www.renpy.org/doc/html/skins.html}in the Ren'Py Documentation{/a}."
    new "有关创建自定义主题的信息可以{a=https://www.renpy.cn/doc/skins.html}在 Ren'Py 文档中找到{/a}。"

    # game/preferences.rpy:273
    old "Install Libraries:"
    new "安装库："

    # game/preferences.rpy:299
    old "Open launcher project"
    new "打开启动器项目"

    # game/preferences.rpy:300
    old "Reset window size"
    new "重置窗口大小"

    # game/preferences.rpy:301
    old "Clean temporary files"
    new "清理临时文件"

    # game/preferences.rpy:308
    old "Cleaning temporary files..."
    new "正在清理临时文件……"

    # game/preferences.rpy:338
    old "{#in language font}Welcome! Please choose a language"
    new "{font=SourceHanSansLite.ttf}欢迎！请选择一种语言"

    # game/preferences.rpy:373
    old "{#in language font}Start using Ren'Py in [lang_name]"
    new "{font=SourceHanSansLite.ttf}开始以[lang_name]使用 Ren'Py"

    # game/project.rpy:46
    old "After making changes to the script, press shift+R to reload your game."
    new "在对脚本进行更改之后，按 Shift+R 重新加载游戏。"

    # game/project.rpy:46
    old "Press shift+O (the letter) to access the console."
    new "按 Shift+O（字母）打开控制台。"

    # game/project.rpy:46
    old "Press shift+D to access the developer menu."
    new "按 Shift+D 打开开发者菜单。"

    # game/project.rpy:46
    old "Have you backed up your projects recently?"
    new "您最近是否备份过您的项目？"

    # game/project.rpy:280
    old "Launching the project failed."
    new "启动项目失败。"

    # game/project.rpy:280
    old "This may be because the project is not writeable."
    new "这可能是由于此项目无法执行写入操作。"

    # game/project.rpy:282
    old "Please ensure that your project launches normally before running this command."
    new "在执行此命令之前，请确保您的项目可正常运行。"

    # game/project.rpy:298
    old "Ren'Py is scanning the project..."
    new "Ren'Py 正在扫描项目……"

    # game/project.rpy:751
    old "Launching"
    new "启动中"

    # game/project.rpy:793
    old "PROJECTS DIRECTORY"
    new "项目目录"

    # game/project.rpy:793
    old "Please choose the projects directory using the directory chooser.\n{b}The directory chooser may have opened behind this window.{/b}"
    new "请使用弹出的目录选择窗口来指定项目目录。\n{b}目录选择窗口可能会被本窗口覆盖。{/b}"

    # game/project.rpy:793
    old "This launcher will scan for projects in this directory, will create new projects in this directory, and will place built projects into this directory."
    new "该启动器将会在此目录里扫描项目、创建新项目以及将构建的项目放置在此。"

    # game/project.rpy:798
    old "Ren'Py has set the projects directory to:"
    new "Ren'Py 已将项目目录设置为："

    # game/translations.rpy:91
    old "Translations: [project.current.display_name!q]"
    new "翻译：[project.current.display_name!q]"

    # game/translations.rpy:132
    old "The language to work with. This should only contain lower-case ASCII characters and underscores."
    new "生效的语言。该字段应仅包含小写 ASCII 字符和下划线。"

    # game/translations.rpy:158
    old "Generate empty strings for translations"
    new "为翻译生成空字串"

    # game/translations.rpy:176
    old "Generates or updates translation files. The files will be placed in game/tl/[persistent.translate_language!q]."
    new "生成或更新翻译文件。文件将放置在 game/tl/[persistent.translate_language!q]。"

    # game/translations.rpy:196
    old "Extract String Translations"
    new "提取字串翻译"

    # game/translations.rpy:198
    old "Merge String Translations"
    new "合并字串翻译"

    # game/translations.rpy:203
    old "Replace existing translations"
    new "替换已存在的翻译"

    # game/translations.rpy:204
    old "Reverse languages"
    new "反转语言"

    # game/translations.rpy:208
    old "Update Default Interface Translations"
    new "更新默认界面翻译"

    # game/translations.rpy:228
    old "The extract command allows you to extract string translations from an existing project into a temporary file.\n\nThe merge command merges extracted translations into another project."
    new "提取命令允许您从现有的项目中提取字串翻译至临时文件。\n\n合并命令将合并提取的翻译至其他项目。"

    # game/translations.rpy:252
    old "Ren'Py is generating translations...."
    new "Ren'Py 正在生成翻译文件……"

    # game/translations.rpy:263
    old "Ren'Py has finished generating [language] translations."
    new "Ren'Py 已生成 [language] 翻译文件。"

    # game/translations.rpy:276
    old "Ren'Py is extracting string translations..."
    new "Ren'Py 正在导出字串翻译……"

    # game/translations.rpy:279
    old "Ren'Py has finished extracting [language] string translations."
    new "Ren'Py 已导出 [language] 字串翻译。"

    # game/translations.rpy:299
    old "Ren'Py is merging string translations..."
    new "Ren'Py 正在合并字串翻译……"

    # game/translations.rpy:302
    old "Ren'Py has finished merging [language] string translations."
    new "Ren'Py 已合并 [language] 字串翻译。"

    # game/translations.rpy:313
    old "Updating default interface translations..."
    new "正在更新默认界面翻译……"

    # game/translations.rpy:342
    old "Extract Dialogue: [project.current.display_name!q]"
    new "提取对话：[project.current.display_name!q]"

    # game/translations.rpy:358
    old "Format:"
    new "格式："

    # game/translations.rpy:366
    old "Tab-delimited Spreadsheet (dialogue.tab)"
    new "以制表符分隔的表格 (dialogue.tab)"

    # game/translations.rpy:367
    old "Dialogue Text Only (dialogue.txt)"
    new "仅对话文本 (dialogue.txt)"

    # game/translations.rpy:380
    old "Strip text tags from the dialogue."
    new "在对话中忽略文本标签。"

    # game/translations.rpy:381
    old "Escape quotes and other special characters."
    new "避开引号和其他特殊符号。"

    # game/translations.rpy:382
    old "Extract all translatable strings, not just dialogue."
    new "提取所有的可翻译字串，而非仅对话。"

    # game/translations.rpy:391
    old "Language (or None for the default language):"
    new "语言（若为默认语言则填 None）："

    # game/translations.rpy:428
    old "Ren'Py is extracting dialogue...."
    new "Ren'Py 正在提取对话……"

    # game/translations.rpy:432
    old "Ren'Py has finished extracting dialogue. The extracted dialogue can be found in dialogue.[persistent.dialogue_format] in the base directory."
    new "Ren'Py 已完成对话提取。提取的对话可在基础目录下的 dialogue.[persistent.dialogue_format] 文件中找到。"

    # game/updater.rpy:63
    old "Release"
    new "发布版"

    # game/updater.rpy:64
    old "Release (Ren'Py 8, Python 3)"
    new "发布版 (Ren'Py 8, Python 3)"

    # game/updater.rpy:65
    old "Release (Ren'Py 7, Python 2)"
    new "发布版 (Ren'Py 7, Python 2)"

    # game/updater.rpy:66
    old "{b}Recommended.{/b} The version of Ren'Py that should be used in all newly-released games."
    new "{b}建议使用。{/b}在所有新发布的游戏中都应该使用的 Ren'Py 版本。"

    # game/updater.rpy:68
    old "Prerelease"
    new "预发布版"

    # game/updater.rpy:69
    old "Prerelease (Ren'Py 8, Python 3)"
    new "预发布版 (Ren'Py 8, Python 3)"

    # game/updater.rpy:70
    old "Prerelease (Ren'Py 7, Python 2)"
    new "预发布版 (Ren'Py 7, Python 2)"

    # game/updater.rpy:71
    old "A preview of the next version of Ren'Py that can be used for testing and taking advantage of new features, but not for final releases of games."
    new "Ren'Py 下个版本的预览，可用于测试和体验新功能，但不适用于游戏的最终发布。"

    # game/updater.rpy:73
    old "Experimental"
    new "试验版"

    # game/updater.rpy:74
    old "Experimental versions of Ren'Py. You shouldn't select this channel unless asked by a Ren'Py developer."
    new "Ren'Py 试验版。除非应 Ren'Py 开发者的要求，否则您不应选择此通道。"

    # game/updater.rpy:76
    old "Nightly"
    new "每夜版"

    # game/updater.rpy:77
    old "Nightly (Ren'Py 8, Python 3)"
    new "每夜版 (Ren'Py 8, Python 3)"

    # game/updater.rpy:78
    old "Nightly (Ren'Py 7, Python 2)"
    new "每夜版 (Ren'Py 7, Python 2)"

    # game/updater.rpy:79
    old "The bleeding edge of Ren'Py development. This may have the latest features, or might not run at all."
    new "Ren'Py 的尖端开发版。此版本也许包含了最新的功能，但也可能根本无法运行。"

    # game/updater.rpy:96
    old "Select Update Channel"
    new "选择更新通道"

    # game/updater.rpy:107
    old "The update channel controls the version of Ren'Py the updater will download."
    new "更新通道决定了更新程序所下载的 Ren'Py 版本。"

    # game/updater.rpy:115
    old "• {a=https://www.renpy.org/doc/html/changelog.html}View change log{/a}"
    new "• {a=https://www.renpy.org/doc/html/changelog.html}查看更新日志{/a}"

    # game/updater.rpy:117
    old "• {a=https://www.renpy.org/dev-doc/html/changelog.html}View change log{/a}"
    new "• {a=https://www.renpy.org/dev-doc/html/changelog.html}查看更新日志{/a}"

    # game/updater.rpy:123
    old "• This version is installed and up-to-date."
    new "• 该版本已安装并且是最新的。"

    # game/updater.rpy:135
    old "%B %d, %Y"
    new "%Y-%m-%d"

    # game/updater.rpy:157
    old "An error has occured:"
    new "发生错误："

    # game/updater.rpy:159
    old "Checking for updates."
    new "正在检查更新。"

    # game/updater.rpy:161
    old "Ren'Py is up to date."
    new "Ren'Py 已更新到最新版本。"

    # game/updater.rpy:163
    old "[u.version] is now available. Do you want to install it?"
    new "[u.version] 现已可用。您希望现在安装吗？"

    # game/updater.rpy:165
    old "Preparing to download the update."
    new "正在准备下载更新。"

    # game/updater.rpy:167
    old "Downloading the update."
    new "正在下载更新。"

    # game/updater.rpy:169
    old "Unpacking the update."
    new "正在解压更新。"

    # game/updater.rpy:171
    old "Finishing up."
    new "完成。"

    # game/updater.rpy:173
    old "The update has been installed. Ren'Py will restart."
    new "更新已安装。Ren'Py 即将重启。"

    # game/updater.rpy:175
    old "The update has been installed."
    new "更新已安装。"

    # game/updater.rpy:177
    old "The update was cancelled."
    new "更新已取消。"

    # game/updater.rpy:194
    old "Ren'Py Update"
    new "Ren'Py 更新"

    # game/updater.rpy:200
    old "Proceed"
    new "继续"

    # game/updater.rpy:214
    old "Fetching the list of update channels"
    new "正在获取更新通道列表"

    # game/updater.rpy:219 此处与 While 连用
    old "downloading the list of update channels"
    new "下载更新通道列表"

    # game/web.rpy:242
    old "Preparing progressive download"
    new "正在准备渐进式下载"

    # game/web.rpy:277
    old "Web: [project.current.display_name!q]"
    new "网页：[project.current.display_name!q]"

    # game/web.rpy:307
    old "Build Web Application"
    new "构建网页应用"

    # game/web.rpy:308
    old "Build and Open in Browser"
    new "构建应用并在浏览器中打开"

    # game/web.rpy:309
    old "Open in Browser"
    new "在浏览器中打开"

    # game/web.rpy:310
    old "Open build directory"
    new "打开构建目录"

    # game/web.rpy:332
    old "Images and music can be downloaded while playing. A 'progressive_download.txt' file will be created so you can configure this behavior."
    new "图像和音乐可以在进行游戏时下载。引擎将创建 progressive_download.txt 文件，以便您配置此行为。"

    # game/web.rpy:336
    old "Current limitations in the web platform mean that loading large images may cause audio or framerate glitches, and lower performance in general. Movies aren't supported."
    new "目前网络平台的限制意味着加载大型图像可能会导致音频或帧数故障，并降低总体性能。目前不支持视频。"

    # game/web.rpy:344
    old "This feature is not supported in Ren'Py 8."
    new "Ren'Py 8 暂不支持这一功能。"

    # game/web.rpy:344
    old "We will restore support in a future release of Ren'Py 8. Until then, please use Ren'Py 7 for web support."
    new "我们将在未来的 Ren'Py 8 版本中恢复支持这项功能。在那之前，请使用 Ren'Py 7 制作网页版。"

    # game/web.rpy:348
    old "Before packaging web apps, you'll need to download RenPyWeb, Ren'Py's web support. Would you like to download RenPyWeb now?"
    new "在打包网页应用之前，您需要先下载 Ren'Py 网页支持包 RenPyWeb。您希望现在下载 RenPyWeb 吗？"

    # game/android.rpy:383
    old "Install SDK"
    # Automatic translation.
    new "安装 SDK"

    # game/android.rpy:387
    old "Generate Keys"
    # Automatic translation.
    new "生成密钥"

    # game/androidstrings.rpy:38
    old "Which app store would you like to support in-app purchasing through?"
    new "您希望通过哪个应用商店支持应用内购买？"

    # game/androidstrings.rpy:40
    old "Amazon App Store."
    new "亚马逊（Amazon）应用商店。"

    # game/androidstrings.rpy:41
    old "Both, in one app."
    new "在一个应用程序中同时支持两者。"

    # game/androidstrings.rpy:42
    old "Neither."
    new "以上都不需要。"

    # game/androidstrings.rpy:63
    old "I found an android.keystore file in the rapt directory. Do you want to use this file?"
    new "我在 RAPT 目录中找到了一个 android.keystore 文件。您希望使用这个文件吗？"

    # game/androidstrings.rpy:66
    old "\n\nSaying 'No' will prevent key creation."
    new "\n\n选择“否”将阻止密钥创建。"

    # game/androidstrings.rpy:69
    old "I found a bundle.keystore file in the rapt directory. Do you want to use this file?"
    new "我在 RAPT 目录中找到了一个 bundle.keystore 文件。您希望使用这个文件吗？"

    # game/distribute_gui.rpy:231
    old "(DLC)"
    new "（DLC）"

    # game/project.rpy:46
    old "Lint checks your game for potential mistakes, and gives you statistics."
    new "Lint 工具会检查您的游戏中可能的错误，并为您提供统计数据。"

    # game/web.rpy:485
    old "Creating package..."
    new "正在创建应用包……"

    # game/updater.rpy:79
    old "A nightly build of fixes to the release version of Ren'Py."
    new "对 Ren'Py 发布版进行修正的每夜构建。"
