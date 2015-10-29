
translate simplified_chinese strings:

    # game/android.rpy:30
    old "To build Android packages, please download RAPT, unzip it, and place it into the Ren'Py directory. Then restart the Ren'Py launcher."
    new "要生成安卓应用包，请下载 RAPT，并解压到 Ren'Py 目录中。之后重启 Ren'Py。"

    # game/android.rpy:31
    old "A 32-bit Java Development Kit is required to build Android packages on Windows. The JDK is different from the JRE, so it's possible you have Java without having the JDK.\n\nPlease {a=http://www.oracle.com/technetwork/java/javase/downloads/index.html}download and install the JDK{/a}, then restart the Ren'Py launcher."
    new "要在 Windows 中创建安卓应用包，您需要一个 32 位的 Java 开发套件（JDK）。JDK 不同于 JRE，所以您可能已安装过 Java 但尚未安装 JDK。\n\n请{a=http://www.oracle.com/technetwork/java/javase/downloads/index.html}下载并安装 JDK{/a}，然后重启 Ren'Py。"

    # game/android.rpy:32
    old "RAPT has been installed, but you'll need to install the Android SDK before you can build Android packages. Choose Install SDK to do this."
    new "RAPT 已安装，但您还需要安装安卓 SDK 才可以生成安卓应用包。点击安装 SDK 来继续。"

    # game/android.rpy:33
    old "RAPT has been installed, but a key hasn't been configured. Please create a new key, or restore android.keystore."
    new "RAPT 已完成安装，但密钥尚未进行过配置。请创建一个新密钥，或将参数 android.keystore 恢复。"

    # game/android.rpy:34
    old "The current project has not been configured. Use \"Configure\" to configure it before building."
    new "当前工程尚未配置过。请在生成前使用“配置”来进行配置。"

    # game/android.rpy:35
    old "Choose \"Build\" to build the current project, or attach an Android device and choose \"Build & Install\" to build and install it on the device."
    new "选择“生成”来生成当前工程，或者在添加安卓设备之后，选择“生成并安装”来生成并安装到设备中。"

    # game/android.rpy:37
    old "Attempts to emulate an Android phone.\n\nTouch input is emulated through the mouse, but only when the button is held down. Escape is mapped to the menu button, and PageUp is mapped to the back button."
    new "尝试模拟为安卓手机。\n\n鼠标将仅在按键按下时模拟为触屏输入。Esc 和 PageUp 键将分别重映射为手机的菜单键和返回键。"

    # game/android.rpy:38
    old "Attempts to emulate an Android tablet.\n\nTouch input is emulated through the mouse, but only when the button is held down. Escape is mapped to the menu button, and PageUp is mapped to the back button."
    new "尝试模拟为安卓平板。\n\nEsc 和 PageUp 键将分别重映射为平板的菜单键和返回键。"

    # game/android.rpy:39
    old "Attempts to emulate a televison-based Android console, like the OUYA or Fire TV.\n\nController input is mapped to the arrow keys, Enter is mapped to the select button, Escape is mapped to the menu button, and PageUp is mapped to the back button."
    new "尝试模拟为基于电视的安卓平台，例如 OUYA 或 Fire TV。\n\n键盘方向键将重映射为手柄方向键，Enter、Esc 和 PageUp 键将分别重映射为手柄的选择键、菜单键和返回键。"

    # game/android.rpy:41
    old "Downloads and installs the Android SDK and supporting packages. Optionally, generates the keys required to sign the package."
    new "下载并安装安卓 SDK 以及支持包。另外，对应用包签名需要生成密钥。"

    # game/android.rpy:42
    old "Configures the package name, version, and other information about this project."
    new "配置应用包名称、版本号以及关于此工程的一些其他信息。"

    # game/android.rpy:43
    old "Opens the file containing the Google Play keys in the editor.\n\nThis is only needed if the application is using an expansion APK. Read the documentation for more details."
    new "在编辑器中打开包含有 Google Play 密钥的文件。\n\n仅当您的应用使用了扩展 APK 时才需要进行此操作。更多详情请查阅说明文档。"

    # game/android.rpy:44
    old "Builds the Android package."
    new "生成安卓应用包。"

    # game/android.rpy:45
    old "Builds the Android package, and installs it on an Android device connected to your computer."
    new "生成安卓应用包，并将其安装到连接至此计算机的安卓设备中。"

    # game/android.rpy:46
    old "Builds the Android package, installs it on an Android device connected to your computer, then launches the app on your device."
    new "生成安卓应用包，将其安装到连接至此计算机的安卓设备中，并在您的设备上打开此应用。"

    # game/android.rpy:48
    old "Connects to an Android device running ADB in TCP/IP mode."
    new "连接到一台正在 TCP/IP 模式下运行 ADB 的安卓设备。"

    # game/android.rpy:49
    old "Disconnects from an Android device running ADB in TCP/IP mode."
    new "从一台正在 TCP/IP 模式下运行 ADB 的安卓设备断开连接。"

    # game/android.rpy:253
    old "Android: [project.current.name!q]"
    new "安卓：[project.current.name!q]"

    # game/android.rpy:273
    old "Emulation:"
    new "模拟："

    # game/android.rpy:282
    old "Phone"
    new "手机"

    # game/android.rpy:286
    old "Tablet"
    new "平板"

    # game/android.rpy:290
    old "Television"
    new "电视"

    # game/android.rpy:302
    old "Build:"
    new "生成："

    # game/android.rpy:310
    old "Install SDK & Create Keys"
    new "安装 SDK 并创建密钥"

    # game/android.rpy:314
    old "Configure"
    new "配置"

    # game/android.rpy:318
    old "Build Package"
    new "生成应用包"

    # game/android.rpy:322
    old "Build & Install"
    new "生成应用包并安装"

    # game/android.rpy:326
    old "Build, Install & Launch"
    new "生成应用包，安装并启动"

    # game/android.rpy:337
    old "Other:"
    new "其他："

    # game/android.rpy:345
    old "Remote ADB Connect"
    new "远程 ADB 连接"

    # game/android.rpy:349
    old "Remote ADB Disconnect"
    new "远程 ADB 断开连接"

    # game/android.rpy:382
    old "Before packaging Android apps, you'll need to download RAPT, the Ren'Py Android Packaging Tool. Would you like to download RAPT now?"
    new "在为安卓应用打包之前，您需要先下载 RAPT，即 Ren'Py 安卓打包工具。您希望现在就开始下载 RAPT 吗？"

    # game/android.rpy:435
    old "Remote ADB Address"
    new "远程 ADB 地址"

    # game/android.rpy:435
    old "Please enter the IP address and port number to connect to, in the form \"192.168.1.143:5555\". Consult your device's documentation to determine if it supports remote ADB, and if so, the address and port to use."
    new "请输入要连接的 IP 地址和端口号，格式为“192.168.1.143:5555”。请查阅您设备的说明文档来确认您的设备是否支持远程 ADB，如果是，请确认可用的 IP 地址和端口号。"

    # game/android.rpy:447
    old "Invalid remote ADB address"
    new "无效的远程 ADB 地址"

    # game/android.rpy:447
    old "The address must contain one exactly one ':'."
    new "地址中必须有且仅有一个“:”。"

    # game/android.rpy:451
    old "The host may not contain whitespace."
    new "主机地址不能包含空格。"

    # game/android.rpy:457
    old "The port must be a number."
    new "端口号必须为数字。"

