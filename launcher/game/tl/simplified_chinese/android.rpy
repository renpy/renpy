
translate simplified_chinese strings:

    # game/android.rpy:13
    old "A 32-bit Java Development Kit is required to build Android packages on Windows. The JDK is different from the JRE, so it's possible you have Java without having the JDK.\n\nPlease {a=http://www.oracle.com/technetwork/java/javase/downloads/index.html}download and install the JDK{/a}, then restart the Ren'Py launcher."
    new "需要一个32位的Java开发套件（JDK）来在windows中创建安卓包。JDK不同于JRE，所以你可能有Java但不包含JDK。\n\n请 {a=http://www.oracle.com/technetwork/java/javase/downloads/index.html} 下载和安装JDK{/a}，然后重启Ren'Py启动器。"

    # game/android.rpy:14
    old "To build Android packages, please download RAPT (from {a=http://www.renpy.org/dl/android}here{/a}), unzip it, and place it into the Ren'Py directory. Then restart the Ren'Py launcher."
    new "要创建安卓安装包，请下载PART（从{a=http://www.renpy.org/dl/android}这里{/a}下载），解压到Ren'Py目录下。然后重启Ren'Py启动器。"

    # game/android.rpy:15
    old "RAPT has been installed, but you'll need to install the Android SDK before you can build Android packages. Choose Install SDK to do this."
    new "RAPT已经安装了，但是你还需要安装安卓SDK才可以构建安卓包。选择安装SDK来实现这个。"

    # game/android.rpy:16
    old "RAPT has been installed, but a key hasn't been configured. Please create a new key, or restore android.keystore."
    new "RAPT已经安装了，但是一个KEY已经被配置过。请创建一个新的KEY，或者恢复android.keystore。"

    # game/android.rpy:17
    old "The current project has not been configured. Use \"Configure\" to configure it before building."
    new "当前工程已经被配置好。使用\"配置\"来在构建前配置它。"

    # game/android.rpy:18
    old "Choose \"Build\" to build the current project, or attach an Android device and choose \"Build & Install\" to build and install it on the device."
    new "选择\"构建\"来构建当前工程，或者选择\"构建并安装\"来添加到一个安卓设备中构建安装。"

    # game/android.rpy:20
    old "Attempts to emulate an Android phone.\n\nTouch input is emulated through the mouse, but only when the button is held down. Escape is mapped to the menu button, and PageUp is mapped to the back button."
    new "想要模拟一个安卓手机.\n\n触摸输入会模拟成为鼠标，仅模拟按键按下。Esc按键映射为（手机的）菜单键，PageUp键被映射为（手机的）返回键。"

    # game/android.rpy:21
    old "Attempts to emulate an Android tablet.\n\nTouch input is emulated through the mouse, but only when the button is held down. Escape is mapped to the menu button, and PageUp is mapped to the back button."
    new "想要模拟一个安卓平板。\n\n触摸输入会模拟成为鼠标，仅模拟按键按下。Esc按键映射为（平板的）菜单键，PageUp键被映射为（平板的）返回键。"

    # game/android.rpy:22
    old "Attempts to emulate an OUYA console.\n\nController input is mapped to the arrow keys, Enter is mapped to the select button, Escape is mapped to the menu button, and PageUp is mapped to the back button."
    new "想要模拟一个{a=http://baike.baidu.com/view/8992952.htm}OUYA{/a}控制器。\n\n控制器的按键映射为（OUYA的）方向键，回车映射为（OUYA的）select按键，Esc按键映射为（OUYA的）菜单（MENU）键，PageUp按键被映射到（OUYA的）返回键。\nP.S.这个是基于安卓4.0的一款家用游戏主机。不错哦！亲~"

    # game/android.rpy:24
    old "Downloads and installs the Android SDK and supporting packages. Optionally, generates the keys required to sign the package."
    new "下载和安装安卓SDK以及支持包。配置，声称KEY来签名安装包。"

    # game/android.rpy:25
    old "Configures the package name, version, and other information about this project."
    new "配置包名称，版本以及其他关于工程的信息。"

    # game/android.rpy:26
    old "Opens the file containing the Google Play keys in the editor.\n\nThis is only needed if the application is using an expansion APK. Read the documentation for more details."
    new "在编辑器中打开包含Google Play keys的文件。\n\n只在你的应用需要一个拓展APK包时才需要。阅读文档来了解详情。"

    # game/android.rpy:27
    old "Builds the Android package."
    new "构建安卓包。"

    # game/android.rpy:28
    old "Builds the Android package, and installs it on an Android device connected to your computer."
    new "构建安卓包，并安装到已连接到电脑的安卓设备上。"

    # game/android.rpy:148
    old "{a=%s}%s{/a}"
    new "{a=%s}%s{/a}"

    # game/android.rpy:371
    old "Android: [project.current.name!q]"
    new "安卓： [project.current.name!q]"

    # game/android.rpy:391
    old "Emulation:"
    new "仿真"

    # game/android.rpy:399
    old "Phone"
    new "手机"

    # game/android.rpy:403
    old "Tablet"
    new "平板"

    # game/android.rpy:407
    old "Television / OUYA"
    new "电视/OUYA"

    # game/android.rpy:419
    old "Build:"
    new "构建："

    # game/android.rpy:427
    old "Install SDK & Create Keys"
    new "安装 SDK并创建Keys"

    # game/android.rpy:431
    old "Configure"
    new "配置"

    # game/android.rpy:435
    old "Build Package"
    new "构建安装包"

    # game/android.rpy:439
    old "Build & Install"
    new "构建并安装"


translate simplified_chinese strings:

    # game/android.rpy:30
    old "To build Android packages, please download RAPT, unzip it, and place it into the Ren'Py directory. Then restart the Ren'Py launcher."
    new "要创建安卓包，请下载RAPT，解压并将其放到Ren'Py目录下，然后重启Ren'Py启动器。"

    # game/android.rpy:506
    old "Before packaging Android apps, you'll need to download RAPT, the Ren'Py Android Packaging Tool. Would you like to download RAPT now?"
    new "在打包安卓APPS前，你必须下载RAPT，Ren'Py的安卓封装工具。你需要现在下载RAPT吗？"

