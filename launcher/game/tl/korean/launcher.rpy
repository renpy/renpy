translate korean strings:

    # about.rpy:39
    old "[version!q]"
    new "[version!q]"

    # about.rpy:43
    old "View license"
    new "라이선스 보기"

    # add_file.rpy:28
    old "FILENAME"
    new "파일이름"

    # add_file.rpy:28
    old "Enter the name of the script file to create."
    new "새로 만들 스크립트 파일 이름을 입력하세요."

    # add_file.rpy:31
    old "The filename must have the .rpy extension."
    new "파일의 확장자는 반드시 .rpy 이어야 합니다."

    # add_file.rpy:39
    old "The file already exists."
    new "파일이 이미 존재합니다."

    # add_file.rpy:42
    old "# Ren'Py automatically loads all script files ending with .rpy. To use this\n# file, define a label and jump to it from another file.\n"
    new "# 렌파이는 자동으로 파일 이름이 .rpy 로 끝나는 스크립트 파일을 불러옵니다. \n# 파일을 사용하려면, 레이블을 정의하여 다른 파일에서 해당 레이블로 점프하세요.\n"

    # android.rpy:30
    old "To build Android packages, please download RAPT, unzip it, and place it into the Ren'Py directory. Then restart the Ren'Py launcher."
    new "안드로이드 패키지를 만드려면, RAPT 파일을 내려받은 뒤에 렌파이 디렉토리에 압축 해제하세요. 그 다음 렌파이 런처를 재시작하세요."

    # android.rpy:31
    old "A 64-bit/x64 Java 8 Development Kit is required to build Android packages on Windows. The JDK is different from the JRE, so it's possible you have Java without having the JDK.\n\nPlease {a=http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html}download and install the JDK{/a}, then restart the Ren'Py launcher."
    new "윈도우에서 안드로이드 패키지를 만드려면 64비트 JDK가 필요합니다. JDK는 JRE와 다르므로 PC에 JDK가 없는 자바가 설치되어 있을 수 있습니다.\n\n{a=http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html}JDK를 내려받아 설치한 뒤{/a}, 렌파이 런처를 재시작해주세요."

    # android.rpy:32
    old "RAPT has been installed, but you'll need to install the Android SDK before you can build Android packages. Choose Install SDK to do this."
    new "RAPT는 설치되었으나 안드로이드 패키지를 만드려면 안드로이드 SDK를 설치해야 합니다. SDK 설치하기 버튼을 눌러 설치하세요."

    # android.rpy:33
    old "RAPT has been installed, but a key hasn't been configured. Please create a new key, or restore android.keystore."
    new "RAPT가 설치되었으나 키가 설정되지 않았습니다. 새 키를 만들거나 android.keystore 파일을 복구하세요."

    # android.rpy:34
    old "The current project has not been configured. Use \"Configure\" to configure it before building."
    new "현재 선택된 프로젝트의 환경 설정이 이루어지지 않았습니다. \"설정하기\" 버튼으로 패키지를 만들기 전에 설정하세요."

    # android.rpy:35
    old "Choose \"Build\" to build the current project, or attach an Android device and choose \"Build & Install\" to build and install it on the device."
    new "\"패키지 만들기\"로 현재 선택된 프로젝트의 패키지를 만들거나, 안드로이드 기기를 연결하고 \"패키지 만들기 & 설치하기\"로 연결된 기기에 패키지를 설치하세요."

    # android.rpy:37
    old "Attempts to emulate an Android phone.\n\nTouch input is emulated through the mouse, but only when the button is held down. Escape is mapped to the menu button, and PageUp is mapped to the back button."
    new "안드로이드 폰 환경을 모방하여 프로젝트를 실행합니다.\n\n터치 입력은 마우스 버튼이 눌린 때에만 마우스로 대신합니다. 메뉴 버튼은 Esc 키, 뒤로 버튼은 PageUp 키가 대신합니다."

    # android.rpy:38
    old "Attempts to emulate an Android tablet.\n\nTouch input is emulated through the mouse, but only when the button is held down. Escape is mapped to the menu button, and PageUp is mapped to the back button."
    new "안드로이드 태블릿 환경을 모방하여 프로젝트를 실행합니다.\n\n터치 입력은 마우스 버튼이 눌린 때에만 마우스로 대신합니다. 메뉴 버튼은 Esc 키, 뒤로 버튼은 PageUp 키가 대신합니다."

    # android.rpy:39
    old "Attempts to emulate a televison-based Android console, like the OUYA or Fire TV.\n\nController input is mapped to the arrow keys, Enter is mapped to the select button, Escape is mapped to the menu button, and PageUp is mapped to the back button."
    new "OUYA나 Fire TV 같은 TV기반 안드로이드 콘솔 환경을 모방하여 게임을 실행합니다. 컨트롤러 입력은 화살표 키, 선택 버튼은 Enter 키, 메뉴 버튼은 Esc 키, 뒤로 버튼은 PageUp 키가 대신합니다."

    # android.rpy:41
    old "Downloads and installs the Android SDK and supporting packages. Optionally, generates the keys required to sign the package."
    new "안드로이드 SDK 파일과 기타 패키지를 내려받고 설치합니다. 추가적으로 패키지에 사인할 때에 필요한 키를 생성합니다."

    # android.rpy:42
    old "Configures the package name, version, and other information about this project."
    new "이 프로젝트의 패키지 이름과 버전, 기타 정보를 설정합니다."

    # android.rpy:43
    old "Opens the file containing the Google Play keys in the editor.\n\nThis is only needed if the application is using an expansion APK. Read the documentation for more details."
    new "구글 플레이 키가 적힌 파일을 에디터로 엽니다.\n\n어플리케이션이 APK 확장자일 때에만 필요합니다. 자세한 내용은 문서를 참조해주세요."

    # android.rpy:44
    old "Builds the Android package."
    new "안드로이드 패키지를 만듭니다."

    # android.rpy:45
    old "Builds the Android package, and installs it on an Android device connected to your computer."
    new "안드로이드 패키지를 만들고, 현재 컴퓨터에 연결된 안드로이드 기기에 패키지를 설치합니다."

    # android.rpy:46
    old "Builds the Android package, installs it on an Android device connected to your computer, then launches the app on your device."
    new "안드로이드 패키지를 만들어 컴퓨터와 연결된 안드로이드 기기에 설치한 뒤 기기에서 설치한 앱을 실행합니다."

    # android.rpy:48
    old "Retrieves the log from the Android device and writes it to a file."
    new "안드로이드 기기와 쓰여진 파일로부터 로그를 검색합니다."

    # android.rpy:50
    old "Selects the Debug build, which can be accessed through Android Studio. Changing between debug and release builds requires an uninstall from your device."
    new "안드로이드 스튜디오를 통해 액세스할 수 있는 디버그 빌드를 선택합니다. 디버그 빌드와 배포판 빌드를 변경하려면 장치에서 제거해야 합니다."

    # android.rpy:51
    old "Selects the Release build, which can be uploaded to stores. Changing between debug and release builds requires an uninstall from your device."
    new "상점에 업로드할 수 있는 배포판 빌드를 선택합니다. 디버그 빌드와 배포판 빌드를 변경하려면 장치에서 제거해야 합니다."

    # android.rpy:245
    old "Copying Android files to distributions directory."
    new "안드로이드 파일을 패키지 경로에 복사하는 중."

    # android.rpy:313
    old "Android: [project.current.name!q]"
    new "안드로이드: [project.current.name!q]"

    # android.rpy:333
    old "Emulation:"
    new "에뮬레이션:"

    # android.rpy:342
    old "Phone"
    new "스마트폰"

    # android.rpy:346
    old "Tablet"
    new "태블릿"

    # android.rpy:350
    old "Television"
    new "TV"

    # android.rpy:362
    old "Build:"
    new "만들기:"

    # android.rpy:373
    old "Debug"
    new "디버그"

    # android.rpy:377
    old "Release"
    new "배포판"

    # android.rpy:384
    old "Install SDK & Create Keys"
    new "SDK 설치 & 키 생성하기"

    # android.rpy:388
    old "Configure"
    new "설정하기"

    # android.rpy:392
    old "Build Package"
    new "패키지 만들기"

    # android.rpy:396
    old "Build & Install"
    new "패키지 만들기 & 설치"

    # android.rpy:400
    old "Build, Install & Launch"
    new "패키지를 만들어 설치하고 실행하기"

    # android.rpy:411
    old "Other:"
    new "기타:"

    # android.rpy:419
    old "Logcat"
    new "로그캣"

    # android.rpy:452
    old "Before packaging Android apps, you'll need to download RAPT, the Ren'Py Android Packaging Tool. Would you like to download RAPT now?"
    new "안드로이드 앱을 만들기 전에, 렌파이 안드로이드 패키징 도구(RAPT)를 내려받아야합니다. RAPT를 내려받으시겠습니까?"

    # android.rpy:505
    old "Retrieving logcat information from device."
    new "기기로부터 로그캣 정보를 검색합니다."

    # androidstrings.rpy:7
    old "{} is not a directory."
    new "{}는 디렉토리가 아닙니다."

    # androidstrings.rpy:8
    old "{} does not contain a Ren'Py game."
    new "{}는 렌파이 게임이 포함돼있지 않습니다."

    # androidstrings.rpy:9
    old "Run configure before attempting to build the app."
    new "앱을 빌드하기 전에 \"설정하기\"를 실행하십시오."

    # androidstrings.rpy:10
    old "Google Play support is enabled, but build.google_play_key is not defined."
    new "구글 플레이 지원은 활성화됐지만 build.google_play_key가 정의되지 않았습니다."

    # androidstrings.rpy:11
    old "Updating project."
    new "프로젝트를 업데이트하는 중입니다."

    # androidstrings.rpy:12
    old "Creating assets directory."
    new "assets 디렉토리를 생성합니다."

    # androidstrings.rpy:13
    old "Creating expansion file."
    new "확장 파일을 생성합니다."

    # androidstrings.rpy:14
    old "Packaging internal data."
    new "내부 데이터를 패키징합니다."

    # androidstrings.rpy:15
    old "I'm using Gradle to build the package."
    new "패키지를 빌드하기 위해 요람(Gradle)을 사용합니다."

    # androidstrings.rpy:16
    old "Uploading expansion file."
    new "확장 파일을 구성합니다."

    # androidstrings.rpy:17
    old "The build seems to have failed."
    new "빌드에 실패했습니다."

    # androidstrings.rpy:18
    old "Launching app."
    new "앱을 런칭합니다."

    # androidstrings.rpy:19
    old "The build seems to have succeeded."
    new "빌드를 성공했습니다."

    # androidstrings.rpy:20
    old "The arm64-v8a version works on newer Android devices, the armeabi-v7a version works on older devices, and the x86_64 version works on the simulator and chromebooks."
    new "arm64-v8a 버전은 최신, armeabi-v7a 버전은 구형 안드로이드 휴대폰과 태블릿에서 작동하며, x86_64 버전은 시뮬레이터와 크롬북에서 작동합니다."

    # androidstrings.rpy:21
    old "What is the full name of your application? This name will appear in the list of installed applications."
    new "애플리케이션의 전체 이름을 무엇인가요? 이것은 설치된 애플리케이션 목록에 표시됩니다."

    # androidstrings.rpy:22
    old "What is the short name of your application? This name will be used in the launcher, and for application shortcuts."
    new "애플리케이션의 짧은 이름은 무엇인가요? 이것은 런처와 애플리케이션 숏컷에 사용됩니다."

    # androidstrings.rpy:23
    old "What is the name of the package?\n\nThis is usually of the form com.domain.program or com.domain.email.program. It may only contain ASCII letters and dots. It must contain at least one dot."
    new "패키지의 이름은 무엇입니까？\n\n이것은 일반적으로 com.domain.program 또는 com.domain.email.program 형식입니다. ASCII 문자와 점만 포함할 수 있습니다. 하나 이상의 점이 있어야 합니다."

    # androidstrings.rpy:24
    old "The package name may not be empty."
    new "패키지 이름은 비워둘 수 없습니다."

    # androidstrings.rpy:25
    old "The package name may not contain spaces."
    new "패키지 이름은 공백을 포함할 수 없습니다."

    # androidstrings.rpy:26
    old "The package name must contain at least one dot."
    new "패키지 이름은 하나 이상의 점을 포함해야 합니다."

    # androidstrings.rpy:27
    old "The package name may not contain two dots in a row, or begin or end with a dot."
    new "패키지 이름은 행에 두 개의 점이 포함될 수 없으며, 점으로 시작되거나 끝날 수 없습니다."

    # androidstrings.rpy:28
    old "Each part of the package name must start with a letter, and contain only letters, numbers, and underscores."
    new "패키지 이름의 각 부분은 문자로 시작해야 하며, 문자와 숫자, 그리고 밑줄만 포함해야 합니다."

    # androidstrings.rpy:29
    old "{} is a Java keyword, and can't be used as part of a package name."
    new "{} 는 자바 키워드이며 패키지 이름의 부분으로 사용될 수 없습니다."

    # androidstrings.rpy:30
    old "What is the application's version?\n\nThis should be the human-readable version that you would present to a person. It must contain only numbers and dots."
    new "애플리케이션의 버전은 어떻게 되나요?\n\n이것은 사람이 읽을 수 있어야 하며 숫자와 점만 포함될 수 있습니다."

    # androidstrings.rpy:31
    old "The version number must contain only numbers and dots."
    new "버전 넘버는 숫자와 점만을 포함해야 합니다."

    # androidstrings.rpy:32
    old "What is the version code?\n\nThis must be a positive integer number, and the value should increase between versions."
    new "버전 코드는 어떻게 되나요?\n\n이것은 양의 정수여야 하며, 값은 버전에 따라 증가할 수 있습니다."

    # androidstrings.rpy:33
    old "The numeric version must contain only numbers."
    new "버전의 숫자는 숫자만 포함해야 합니다."

    # androidstrings.rpy:34
    old "How would you like your application to be displayed?"
    new "애플리케이션을 어떻게 표시할까요?"

    # androidstrings.rpy:35
    old "In landscape orientation."
    new "가로(Landscape) 방향으로."

    # androidstrings.rpy:36
    old "In portrait orientation."
    new "세로(Portrait) 방향으로"

    # androidstrings.rpy:37
    old "In the user's preferred orientation."
    new "사용자가 선호하는 방향으로."

    # androidstrings.rpy:38
    old "Which app store would you like to support in-app purchasing through?"
    new "인앱 구매를 지원하려는 앱 스토어가 있습니까?"

    # androidstrings.rpy:39
    old "Google Play."
    new "구글 플레이."

    # androidstrings.rpy:40
    old "Amazon App Store."
    new "아마존 앱 스토어."

    # androidstrings.rpy:41
    old "Both, in one app."
    new "모두, 하나의 앱에."

    # androidstrings.rpy:42
    old "Neither."
    new "지원하지 않음."

    # androidstrings.rpy:43
    old "Would you like to create an expansion APK?"
    new "확장 APK를 생성하시겠습니까?"

    # androidstrings.rpy:44
    old "No. Size limit of 100 MB on Google Play, but can be distributed through other stores and sideloaded."
    new "아니오. 구글 플레이의 100 MB 크기 제한으로, 하지만 다른 스토어 및 사이드로드를 통해 배포할 수 있습니다."

    # androidstrings.rpy:45
    old "Yes. 2 GB size limit, but won't work outside of Google Play. (Read the documentation to get this to work.)"
    new "네. 2GB 크기 제한으로, 하지만 구글 플레이 외부에서 작동하지 않습니다. (이 기능을 사용하려면 설명서를 읽으십시오.)"

    # androidstrings.rpy:46
    old "Do you want to allow the app to access the Internet?"
    new "앱이 인터넷에 액세스하도록 허용하시겠습니까?"

    # androidstrings.rpy:47
    old "Do you want to automatically update the generated project?"
    new "생성된 프로젝트를 자동으로 업데이트하시겠습니까?"

    # androidstrings.rpy:48
    old "Yes. This is the best choice for most projects."
    new "예. 이것은 대부분의 프로젝트에 적합합니다."

    # androidstrings.rpy:49
    old "No. This may require manual updates when Ren'Py or the project configuration changes."
    new "아니오. 렌파이 또는 프로젝트 구성이 변경되면 수동 업데이트가 필요할 수 있습니다."

    # androidstrings.rpy:50
    old "Unknown configuration variable: {}"
    new "알 수 없는 환경 변수: {}"

    # androidstrings.rpy:51
    old "I'm compiling a short test program, to see if you have a working JDK on your system."
    new "시스템에 작동하는 JDK가 있는지 확인하기 위해 간단한 테스트 프로그램을 컴파일하고 있습니다."

    # androidstrings.rpy:52
    old "I was unable to use javac to compile a test file. If you haven't installed the Java Development Kit yet, please download it from:\n\nhttp://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html\n\nThe JDK is different from the JRE, so it's possible you have Java without having the JDK. Without a working JDK, I can't continue."
    new "javac를 사용하여 테스트 파일을 컴파일할 수 없습니다. 자바 개발 키트를 아직 설치하지 않은 경우 아래에서 설치하세요:\n\nhttp://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html\n\nJDK는 JRE와 다르므로 JDK가 없어도 Java를 사용할 수 있습니다. 작동하는 JDK가 없으면 계속할 수 없습니다."

    # androidstrings.rpy:53
    old "The version of Java on your computer does not appear to be JDK 8, which is the only version supported by the Android SDK. If you need to install JDK 8, you can download it from:\n\nhttp://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html\n\nYou can also set the JAVA_HOME environment variable to use a different version of Java."
    new "컴퓨터에 설치된 자바 버전은 안드로이드 SDK에서 지원하는 유일한 버전인 JDK 8이 아닙니다. JDK 8은 아래에서 설치할 수 있습니다:\n\nhttp://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html\n\n다른 버전의 자바를 사용하도록 JAVA_HOME 환경 변수를 설정할 수도 있습니다."

    # androidstrings.rpy:54
    old "The JDK is present and working. Good!"
    new "JDK가 잘 작동하고 있네요！"

    # androidstrings.rpy:55
    old "The Android SDK has already been unpacked."
    new "안드로이드 SDK가 이미 설치돼 있습니다."

    # androidstrings.rpy:56
    old "Do you accept the Android SDK Terms and Conditions?"
    new "안드로이드 SDK 이용 약관에 동의하십니까?"

    # androidstrings.rpy:57
    old "I'm downloading the Android SDK. This might take a while."
    new "안드로이드 SDK를 내려받는 중입니다. 다소 시간이 소요될 수 있습니다."

    # androidstrings.rpy:58
    old "I'm extracting the Android SDK."
    new "안드로이드 SDK의 압축을 풀고 있습니다."

    # androidstrings.rpy:59
    old "I've finished unpacking the Android SDK."
    new "안드로이드 SDK의 설치를 완료했습니다."

    # androidstrings.rpy:60
    old "I'm about to download and install the required Android packages. This might take a while."
    new "필요한 안드로이드 패키지를 설치하고 있습니다. 다소 시간이 소요될 수 있습니다."

    # androidstrings.rpy:61
    old "I was unable to accept the Android licenses."
    new "안드로이드 라이선스를 수락할 수 없었습니다."

    # androidstrings.rpy:62
    old "I was unable to install the required Android packages."
    new "필요한 안드로이드 패키지를 설치할 수 없었습니다."

    # androidstrings.rpy:63
    old "I've finished installing the required Android packages."
    new "필요한 안드로이드 패키지의 설치가 완료됐습니다."

    # androidstrings.rpy:64
    old "You set the keystore yourself, so I'll assume it's how you want it."
    new "키스토어(keystore)를 설정합니다."

    # androidstrings.rpy:65
    old "You've already created an Android keystore, so I won't create a new one for you."
    new "이미 안드로이드 키스토어(keystore)를 만들었습니다."

    # androidstrings.rpy:66
    old "I can create an application signing key for you. Signing an application with this key allows it to be placed in the Android Market and other app stores.\n\nDo you want to create a key?"
    new "애플리케이션 서명 키를 만들 수 있습니다. 이 키를 사용하여 애플리케이션에 서명하면 안드로이드 상점 및 기타 앱 스토어에 배포할 수 있습니다.\n\n키를 만드시겠습니까?"

    # androidstrings.rpy:67
    old "I will create the key in the android.keystore file.\n\nYou need to back this file up. If you lose it, you will not be able to upgrade your application.\n\n\\You also need to keep the key safe. If evil people get this file, they could make fake versions of your application, and potentially steal your users' data.\n\nWill you make a backup of android.keystore, and keep it in a safe place?"
    new "android.keystore 파일에 키를 생성할 것입니다.\n\n애플리케이션의 업그레이드에 필요하기 때문에 파일을 반드시 백업하시기 바랍니다.\n\n또한 키를 안전한 곳에 보과해야 합니다."

    # androidstrings.rpy:68
    old "Please enter your name or the name of your organization."
    new "당신의 이름과 단체 이름을 기입하십시오."

    # androidstrings.rpy:69
    old "Could not create android.keystore. Is keytool in your path?"
    new "android.keystore를 생성하지 못했습니다. 키툴(keytool)이 경로에 있습니까?"

    # androidstrings.rpy:70
    old "I've finished creating android.keystore. Please back it up, and keep it in a safe place."
    new "android.keystore를 생성했습니다. 백업하시고, 안전한 곳에 보관하십시오."

    # androidstrings.rpy:71
    old "It looks like you're ready to start packaging games."
    new "게임을 패키징할 준비가 됐습니다."

    # choose_directory.rpy:87
    old "Ren'Py was unable to run python with tkinter to choose the directory. Please install the python-tk or tkinter package."
    new "프로젝트 경로를 선택하는 tkinter를 구동하지 못했습니다. python-tk나 tkinter 패키지를 설치하세요."

    # choose_directory.rpy:104
    old "The selected projects directory is not writable."
    new "선택한 프로젝트 디렉토리에 쓸 수 없습니다."

    # choose_theme.rpy:303
    old "Could not change the theme. Perhaps options.rpy was changed too much."
    new "테마를 바꿀 수 없습니다. options.rpy의 내용이 크게 변경되었을 가능성이 있습니다."

    # choose_theme.rpy:370
    old "Planetarium"
    new "Planetarium"

    # choose_theme.rpy:425
    old "Choose Theme"
    new "테마 선택하기"

    # choose_theme.rpy:438
    old "Theme"
    new "테마"

    # choose_theme.rpy:463
    old "Color Scheme"
    new "색상 배색"

    # choose_theme.rpy:495
    old "Continue"
    new "계속하기"

    # consolecommand.rpy:84
    old "INFORMATION"
    new "알림"

    # consolecommand.rpy:84
    old "The command is being run in a new operating system console window."
    new "커맨드가 새로운 운영체제 콘솔 창에서 실행 중입니다."

    # distribute.rpy:444
    old "Scanning project files..."
    new "프로젝트 파일 살펴보는 중..."

    # distribute.rpy:460
    old "Building distributions failed:\n\nThe build.directory_name variable may not include the space, colon, or semicolon characters."
    new "배포판 만들기에 실패했습니다.\n\n build.directory_name 변수에는 공백이나 콜론, 세미 콜론 문자를 입력할 수 없습니다."

    # distribute.rpy:505
    old "No packages are selected, so there's nothing to do."
    new "선택된 패키지가 없으므로 할 수 있는 작업이 없습니다."

    # distribute.rpy:517
    old "Scanning Ren'Py files..."
    new "렌파이 파일 살펴보는 중..."

    # distribute.rpy:572
    old "All packages have been built.\n\nDue to the presence of permission information, unpacking and repacking the Linux and Macintosh distributions on Windows is not supported."
    new "패키지를 전부 작성했습니다.\n\n 권한 정보로 인해 리눅스와 매킨토시 배포판을 윈도우에서 압축해제하거나 재압축하는 것은 지원하지 않습니다."

    # distribute.rpy:755
    old "Archiving files..."
    new "파일 압축 중..."

    # distribute.rpy:1068
    old "Unpacking the Macintosh application for signing..."
    new "서명을 위해 매킨토시 애플리케이션을 압축해제하는 중입니다..."

    # distribute.rpy:1078
    old "Signing the Macintosh application...\n(This may take a long time.)"
    new "매킨토시 애플리케이션을 서명하는 중입니다...\n(꽤 시간이 걸릴 것입니다.)"

    # distribute.rpy:1100
    old "Creating the Macintosh DMG..."
    new "매킨토시 DMG를 생성하는 중입니다..."

    # distribute.rpy:1109
    old "Signing the Macintosh DMG..."
    new "매킨토시 DMG에 서명하는 중입니다..."

    # distribute.rpy:1304
    old "Writing the [variant] [format] package."
    new "[variant] [format] 패키지 작성 중."

    # distribute.rpy:1317
    old "Making the [variant] update zsync file."
    new "[variant] 업데이트 zsync 파일 생성 중."

    # distribute.rpy:1427
    old "Processed {b}[complete]{/b} of {b}[total]{/b} files."
    new "총 {b}[total]{/b}개의 파일 중에서 {b}[complete]{/b} 파일 완료."

    # distribute_gui.rpy:162
    old "Build Distributions: [project.current.name!q]"
    new "[project.current.name!q] 배포판 만들기"

    # distribute_gui.rpy:176
    old "Directory Name:"
    new "디렉토리 이름:"

    # distribute_gui.rpy:180
    old "Executable Name:"
    new "실행 파일 이름:"

    # distribute_gui.rpy:190
    old "Actions:"
    new "작업:"

    # distribute_gui.rpy:198
    old "Edit options.rpy"
    new "options.rpy 수정하기"

    # distribute_gui.rpy:199
    old "Add from clauses to calls, once"
    new "from 절을 call 문에 추가하기(1회)"

    # distribute_gui.rpy:200
    old "Refresh"
    new "새로고침"

    # distribute_gui.rpy:204
    old "Upload to itch.io"
    new "itch.io로 업로드"

    # distribute_gui.rpy:220
    old "Build Packages:"
    new "만들 패키지:"

    # distribute_gui.rpy:239
    old "Options:"
    new "설정:"

    # distribute_gui.rpy:244
    old "Build Updates"
    new "업데이트 파일 만들기"

    # distribute_gui.rpy:246
    old "Add from clauses to calls"
    new "from 절을 call 문에 추가하기"

    # distribute_gui.rpy:247
    old "Force Recompile"
    new "강제 재컴파일"

    # distribute_gui.rpy:270
    old "Build"
    new "만들기"

    # distribute_gui.rpy:274
    old "Adding from clauses to call statements that do not have them."
    new "from 절이 없는 call 문에 from 절을 추가합니다."

    # distribute_gui.rpy:295
    old "Errors were detected when running the project. Please ensure the project runs without errors before building distributions."
    new "프로젝트를 실행하던 도중 오류를 발견했습니다. 배포판을 작성하기 전에 프로젝트가 오류 없이 실행되는지 확인하세요."

    # distribute_gui.rpy:312
    old "Your project does not contain build information. Would you like to add build information to the end of options.rpy?"
    new "프로젝트에 배포판 정보가 없습니다. options.rpy 끝부분에 배포판 정보를 추가하겠습니까?"

    # dmgcheck.rpy:50
    old "Ren'Py is running from a read only folder. Some functionality will not work."
    new "렌파이가 읽기 전용 폴더에서 실행되고 있습니다. 일부 기능이 작동하지 않을 수 있습니다."

    # dmgcheck.rpy:50
    old "This is probably because Ren'Py is running directly from a Macintosh drive image. To fix this, quit this launcher, copy the entire %s folder somewhere else on your computer, and run Ren'Py again."
    new "이것은 렌파이가 매킨토시 드라이브 이미지에서 직접 실행되기 때문일 수 있습니다. 해결을 위해 이 런처를 종료하고, %s 폴더 전체를 컴퓨터의 다른 곳에 복사하고 렌파이를 다시 실행하십시오."

    # editor.rpy:152
    old "(Recommended) A modern and approachable text editor."
    new "(추천) 현대적이고 친숙한 텍스트 편집기."

    # editor.rpy:164
    old "Up to 150 MB download required."
    new "150 MB의 용량이 필요합니다."

    # editor.rpy:178
    old "A mature editor. Editra lacks the IME support required for Chinese, Japanese, and Korean text input."
    new "에디트라(Editra)는 현재 중국어, 일본어, 한국어 텍스트를 입력할 때 필요한 IME를 지원하지 않습니다."

    # editor.rpy:179
    old "A mature editor. Editra lacks the IME support required for Chinese, Japanese, and Korean text input. On Linux, Editra requires wxPython."
    new "에디트라(Editra)는 현재 중국어, 일본어, 한국어 텍스트를 입력할 때 필요한 IME를 지원하지 않습니다. 리눅스에서, 에디트라는 wxPython이 필요합니다."

    # editor.rpy:195
    old "This may have occured because wxPython is not installed on this system."
    new "wxPython이 설치되지 않아 문제가 발생했을 가능성이 있습니다."

    # editor.rpy:197
    old "Up to 22 MB download required."
    new "22MB 내려받기 필요."

    # editor.rpy:210
    old "A mature editor that requires Java."
    new "자바(Java)를 사용하는 완성도 높은 에디터."

    # editor.rpy:210
    old "1.8 MB download required."
    new "1.8MB 내려받기 필요."

    # editor.rpy:210
    old "This may have occured because Java is not installed on this system."
    new "자바(Java)가 설치되지 않아 문제가 발생했을 수도 있습니다."

    # editor.rpy:219
    old "System Editor"
    new "시스템 편집기"

    # editor.rpy:219
    old "Invokes the editor your operating system has associated with .rpy files."
    new "OS에서 .rpy 파일을 열 때 사용하는 에디터를 실행합니다."

    # editor.rpy:235
    old "None"
    new "없음"

    # editor.rpy:235
    old "Prevents Ren'Py from opening a text editor."
    new "렌파이가 텍스트 에디터를 실행하지 못하도록 합니다."

    # editor.rpy:338
    old "Edit [text]."
    new "[text] 편집."

    # editor.rpy:387
    old "An exception occured while launching the text editor:\n[exception!q]"
    new "스크립트 에디터를 실행하던 도중 예외가 발생했습니다:\n[exception!q]"

    # editor.rpy:519
    old "Select Editor"
    new "에디터 선택하기"

    # editor.rpy:534
    old "A text editor is the program you'll use to edit Ren'Py script files. Here, you can select the editor Ren'Py will use. If not already present, the editor will be automatically downloaded and installed."
    new "스크립트 에디터란 렌파이 스크립트 파일을 수정할 때 사용하는 프로그램입니다. 이곳에서는 렌파이가 실행시킬 에디터를 선택할 수 있습니다. 에디터가 없다면 에디터를 자동으로 다운로드해 설치합니다."

    # front_page.rpy:35
    old "Open [text] directory."
    new "[text] 경로를 엽니다."

    # front_page.rpy:93
    old "refresh"
    new "새로고침"

    # front_page.rpy:120
    old "+ Create New Project"
    new "+ 새 프로젝트 만들기"

    # front_page.rpy:130
    old "Launch Project"
    new "프로젝트 실행"

    # front_page.rpy:147
    old "[p.name!q] (template)"
    new "[p.name!q] (서식)"

    # front_page.rpy:149
    old "Select project [text]."
    new "[text] 프로젝트를 선택합니다."

    # front_page.rpy:165
    old "Tutorial"
    new "길라잡이"

    # front_page.rpy:166
    old "The Question"
    new "물음(The Question)"

    # front_page.rpy:182
    old "Active Project"
    new "진행 중인 프로젝트"

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
    new "파일 수정하기"

    # front_page.rpy:215
    old "Open Directory"
    new "폴더 열기"

    # front_page.rpy:217
    old "All script files"
    new "모든 스크립트 파일"

    # front_page.rpy:221
    old "Actions"
    new "작업"

    # front_page.rpy:230
    old "Navigate Script"
    new "스크립트 살펴보기"

    # front_page.rpy:231
    old "Check Script (Lint)"
    new "스크립트 확인 (오류 검사)"

    # front_page.rpy:234
    old "Change/Update GUI"
    new "GUI 변경/업데이트"

    # front_page.rpy:236
    old "Change Theme"
    new "테마 바꾸기"

    # front_page.rpy:239
    old "Delete Persistent"
    new "지속 데이터 삭제하기"

    # front_page.rpy:248
    old "Build Distributions"
    new "배포판 만들기"

    # front_page.rpy:250
    old "Android"
    new "안드로이드"

    # front_page.rpy:251
    old "iOS"
    new "iOS"

    # front_page.rpy:252
    old "Generate Translations"
    new "번역 파일 만들기"

    # front_page.rpy:253
    old "Extract Dialogue"
    new "대사 추출하기"

    # front_page.rpy:270
    old "Checking script for potential problems..."
    new "스크립트에서 문제가 발생할 수 있는지를 확인하고 있습니다..."

    # front_page.rpy:285
    old "Deleting persistent data..."
    new "지속 데이터를 삭제하고 있습니다... "

    # front_page.rpy:293
    old "Recompiling all rpy files into rpyc files..."
    new "모든 rpy 파일을 rpyc 파일로 재컴파일하는 중..."

    # gui7.rpy:252
    old "Select Accent and Background Colors"
    new "강조와 배경 색상 선택"

    # gui7.rpy:266
    old "Please click on the color scheme you wish to use, then click Continue. These colors can be changed and customized later."
    new "원하는 색상 스키마를 선택하고 다음을 누르세요. 이러한 색상과 사용자 지정은 나중에 변경할 수 있습니다."

    # gui7.rpy:311
    old "{b}Warning{/b}\nContinuing will overwrite customized bar, button, save slot, scrollbar, and slider images.\n\nWhat would you like to do?"
    new "{b}경고g{/b}\n계속하면 사용자 지정된 막대, 버튼, 저장 슬롯, 스크롤바, 그리고 슬라이더 이미지들을 덮어씌웁니다.\n\n무엇을 하고 싶으세요?"

    # gui7.rpy:311
    old "Choose new colors, then regenerate image files."
    new "새로운 색상을 선택하면 이미지 파일들이 재생성됩니다."

    # gui7.rpy:311
    old "Regenerate the image files using the colors in gui.rpy."
    new "gui.rpy에서 사용하는 색상으로 이미지 파일 재생성."

    # gui7.rpy:331
    old "PROJECT NAME"
    new "프로젝트 이름"

    # gui7.rpy:331
    old "Please enter the name of your project:"
    new "프로젝트 이름을 입력하세요:"

    # gui7.rpy:339
    old "The project name may not be empty."
    new "프로젝트 이름을 입력하지 않았습니다."

    # gui7.rpy:344
    old "[project_name!q] already exists. Please choose a different project name."
    new "[project_name!q]는 이미 존재합니다. 다른 프로젝트 이름을 선택하세요."

    # gui7.rpy:347
    old "[project_dir!q] already exists. Please choose a different project name."
    new "[project_dir!q]는 이미 존재합니다. 다른 프로젝트 이름을 선택하세요."

    # gui7.rpy:358
    old "What resolution should the project use? Although Ren'Py can scale the window up and down, this is the initial size of the window, the size at which assets should be drawn, and the size at which the assets will be at their sharpest.\n\nThe default of 1280x720 is a reasonable compromise."
    new "프로젝트에서 어떤 해상도를 사용하나요? 렌파이가 창을 위아래로 확장 할 수 있지만, 이것은 창의 초기 크기, 에셋이 그려지는 크기, 애셋이 가장 선명하게 될 크기입니다.\n\n1280x720의 기본값은 적절한 절충안입니다."

    # gui7.rpy:358
    old "Custom. The GUI is optimized for a 16:9 aspect ratio."
    new "사용자 정의. GUI는 종회비 16:9로 최적화되어 있습니다."

    # gui7.rpy:373
    old "WIDTH"
    new "너비"

    # gui7.rpy:373
    old "Please enter the width of your game, in pixels."
    new "게임의 너비를 픽셀로 입력해주세요."

    # gui7.rpy:378
    old "The width must be a number."
    new "너비는 숫자여야 합니다."

    # gui7.rpy:380
    old "HEIGHT"
    new "높이"

    # gui7.rpy:380
    old "Please enter the height of your game, in pixels."
    new "게임의 높이를 픽셀로 입력해주세요."

    # gui7.rpy:385
    old "The height must be a number."
    new "높이는 숫자여야 합니다."

    # gui7.rpy:427
    old "Creating the new project..."
    new "새 프로젝트를 만드는 중..."

    # gui7.rpy:429
    old "Updating the project..."
    new "프로젝트 업데이트중..."

    # interface.rpy:119
    old "Documentation"
    new "매뉴얼"

    # interface.rpy:120
    old "Ren'Py Website"
    new "렌파이 공식 홈페이지"

    # interface.rpy:121
    old "Ren'Py Games List"
    new "렌파이 게임 목록"

    # interface.rpy:129
    old "update"
    new "업데이트"

    # interface.rpy:131
    old "preferences"
    new "환경설정"

    # interface.rpy:132
    old "quit"
    new "종료"

    # interface.rpy:136
    old "Ren'Py Sponsor Information"
    new "렌파이 후원자 정보"

    # interface.rpy:258
    old "Due to package format limitations, non-ASCII file and directory names are not allowed."
    new "패키지 형식에 제한이 있으므로 ASCII가 아닌 문자가 입력된 파일 이름이나 디렉토리 이름은 사용할 수 없습니다."

    # interface.rpy:354
    old "ERROR"
    new "오류"

    # interface.rpy:400
    old "Text input may not contain the {{ or [[ characters."
    new "글자를 입력할 때는 {{나 [[ 문자는 없어야 합니다."

    # interface.rpy:405
    old "File and directory names may not contain / or \\."
    new "파일 및 디렉토리 이름에는 / 나 \\가 없어야 합니다."

    # interface.rpy:411
    old "File and directory names must consist of ASCII characters."
    new "파일이나 디렉토리 이름은 ASCII 문자로 지어야 합니다."

    # interface.rpy:479
    old "PROCESSING"
    new "처리 중"

    # interface.rpy:496
    old "QUESTION"
    new "확인"

    # interface.rpy:509
    old "CHOICE"
    new "선택"

    # ios.rpy:28
    old "To build iOS packages, please download renios, unzip it, and place it into the Ren'Py directory. Then restart the Ren'Py launcher."
    new "iOS 배포판을 만드려면 renios 패키지를 다운받은 후, 렌'파이 디렉터리에 압축을 해제하세요. 그 다음, 렌'파이를 재시작하세요."

    # ios.rpy:29
    old "The directory in where Xcode projects will be placed has not been selected. Choose 'Select Directory' to select it."
    new "Xcode 프로젝트가 생성될 폴더가 지정되지 않았습니다. '경로 선택' 버튼을 눌러 경로를 선택하세요."

    # ios.rpy:30
    old "There is no Xcode project corresponding to the current Ren'Py project. Choose 'Create Xcode Project' to create one."
    new "현재 렌'파이 프로젝트에 대응하는 Xcode 프로젝트가 없습니다. 'Xcode 프로젝트 만들기'를 눌러 프로젝트를 만드세요."

    # ios.rpy:31
    old "An Xcode project exists. Choose 'Update Xcode Project' to update it with the latest game files, or use Xcode to build and install it."
    new "이미 Xcode 프로젝트가 존재합니다. 'Xcode 프로젝트 업데이트'를 눌러 프로젝트를 최신 파일로 업데이트하거나, Xcode를 이용해 프로젝트를 빌드하세요."

    # ios.rpy:33
    old "Attempts to emulate an iPhone.\n\nTouch input is emulated through the mouse, but only when the button is held down."
    new "iPhone 환경을 모방하여 프로젝트를 실행합니다.\n\n터치 입력은 마우스로 대체합니다. 그러나 마우스를 클릭할 때만 활성화됩니다."

    # ios.rpy:34
    old "Attempts to emulate an iPad.\n\nTouch input is emulated through the mouse, but only when the button is held down."
    new "iPhone 환경을 모방하여 프로젝트를 실행합니다.\n\n터치 입력은 마우스로 대체합니다. 그러나 마우스를 클릭할 때만 활성화됩니다."

    # ios.rpy:36
    old "Selects the directory where Xcode projects will be placed."
    new "Xcode 프로젝트가 위치할 경로를 선택합니다."

    # ios.rpy:37
    old "Creates an Xcode project corresponding to the current Ren'Py project."
    new "현재 프로젝트에 대응하는 Xcode 프로젝트를 만듭니다."

    # ios.rpy:38
    old "Updates the Xcode project with the latest game files. This must be done each time the Ren'Py project changes."
    new "Xcode 프로젝트 파일을 최신 게임 파일으로 업데이트합니다. 이 작업은 프로젝트에 변경 사항이 생길 때마다 행해져야 합니다."

    # ios.rpy:39
    old "Opens the Xcode project in Xcode."
    new "Xcode에서 Xcode 프로젝트를 엽니다."

    # ios.rpy:41
    old "Opens the directory containing Xcode projects."
    new "Xcode 프로젝트가 있는 경로를 엽니다."

    # ios.rpy:126
    old "The Xcode project already exists. Would you like to rename the old project, and replace it with a new one?"
    new "Xcode 프로젝트가 이미 존재합니다. 이전 프로젝트의 이름을 바꾸고 새 프로젝트 파일로 교체하겠습니까?"

    # ios.rpy:211
    old "iOS: [project.current.name!q]"
    new "iOS: [project.current.name!q]"

    # ios.rpy:240
    old "iPhone"
    new "iPhone"

    # ios.rpy:244
    old "iPad"
    new "iPad"

    # ios.rpy:264
    old "Select Xcode Projects Directory"
    new "경로 선택하기"

    # ios.rpy:268
    old "Create Xcode Project"
    new "Xcode 프로젝트 만들기"

    # ios.rpy:272
    old "Update Xcode Project"
    new "Xcode 프로젝트 업데이트하기"

    # ios.rpy:277
    old "Launch Xcode"
    new "Xcode 실행하기"

    # ios.rpy:312
    old "Open Xcode Projects Directory"
    new "Xcode 프로젝트 경로 열기"

    # ios.rpy:345
    old "Before packaging iOS apps, you'll need to download renios, Ren'Py's iOS support. Would you like to download renios now?"
    new "iOS 앱을 패키징하기 전, 렌파이 iOS 서포트(renios)를 다운로드할 필요가 있습니다. 지금 다운로드하겠습니까?"

    # ios.rpy:354
    old "XCODE PROJECTS DIRECTORY"
    new "Xcode 프로젝트 경로"

    # ios.rpy:354
    old "Please choose the Xcode Projects Directory using the directory chooser.\n{b}The directory chooser may have opened behind this window.{/b}"
    new "경로 선택창을 이용하여 Xcode 프로젝트 경로를 선택하세요.\n{b}경로 선택 창이 이 창의 뒤에 열렸을 수도 있습니다."

    # ios.rpy:359
    old "Ren'Py has set the Xcode Projects Directory to:"
    new "렌'파이가 Xcode 프로젝트 경로를 다음과 같이 설정했습니다:"

    # itch.rpy:60
    old "The built distributions could not be found. Please choose 'Build' and try again."
    new "빌드된 배포판을 찾을 수 없습니다. '빌드'를 선택하고 다시 시도하세요."

    # itch.rpy:98
    old "No uploadable files were found. Please choose 'Build' and try again."
    new "업로드가능한 파일이 없습니다. '빌드'를 선택하고 다시 시도하세요."

    # itch.rpy:106
    old "The butler program was not found."
    new "집사(butler) 프로그램이 없습니다."

    # itch.rpy:106
    old "Please install the itch.io app, which includes butler, and try again."
    new "집사(butler)를 포함한 itch.io 앱을 설치하고 다시 시도하세요."

    # itch.rpy:115
    old "The name of the itch project has not been set."
    new "itch 프로젝트의 이름이 설정되지 않았습니다."

    # itch.rpy:115
    old "Please {a=https://itch.io/game/new}create your project{/a}, then add a line like \n{vspace=5}define build.itch_project = \"user-name/game-name\"\n{vspace=5} to options.rpy."
    new "{a=https://itch.io/game/new}프로젝트를 만드세요{/a}, 그리고 options.rpy에 다음과 같은 라인을 작성하세요: \n{vspace=5}define build.itch_project = \"user-name/game-name\"\n{vspace=5}."

    # mobilebuild.rpy:110
    old "{a=%s}%s{/a}"
    new "{a=%s}%s{/a}"

    # navigation.rpy:168
    old "Navigate: [project.current.name]"
    new "[project.current.name] 살펴보기"

    # navigation.rpy:178
    old "Order: "
    new "순서: "

    # navigation.rpy:179
    old "alphabetical"
    new "알파벳 순서로"

    # navigation.rpy:181
    old "by-file"
    new "파일 별로"

    # navigation.rpy:183
    old "natural"
    new "생성된 순서대로"

    # navigation.rpy:195
    old "Category:"
    new "종류:"

    # navigation.rpy:198
    old "files"
    new "파일"

    # navigation.rpy:199
    old "labels"
    new "레이블"

    # navigation.rpy:200
    old "defines"
    new "정의"

    # navigation.rpy:201
    old "transforms"
    new "트랜스폼"

    # navigation.rpy:202
    old "screens"
    new "스크린"

    # navigation.rpy:206
    old "callables"
    new "콜러블"

    # navigation.rpy:204
    old "TODOs"
    new "해야할 작업"

    # navigation.rpy:243
    old "+ Add script file"
    new "+ 새 스크립트 파일 추가하기"

    # navigation.rpy:251
    old "No TODO comments found.\n\nTo create one, include \"# TODO\" in your script."
    new "TODO 주석을 발견하지 못했습니다.\n\nTODO 주석을 만드려면 스크립트 파일에 \"# TODO\" 를 적으세요."

    # navigation.rpy:258
    old "The list of names is empty."
    new "이름 목록이 비었습니다."

    # new_project.rpy:38
    old "New GUI Interface"
    new "새로운 GUI 인터페이스"

    # new_project.rpy:48
    old "Both interfaces have been translated to your language."
    new "모든 인터페이스는 귀하의 언어로 번역됐습니다."

    # new_project.rpy:50
    old "Only the new GUI has been translated to your language."
    new "새로운 GUI만 귀하의 언어로 번역됐습니다."

    # new_project.rpy:52
    old "Only the legacy theme interface has been translated to your language."
    new "레거시 테마 인터페이스가 귀하의 언어로 번역됐습니다."

    # new_project.rpy:54
    old "Neither interface has been translated to your language."
    new "어느 인터페이스도 귀하의 언어로 번역되지 않았습니다."

    # new_project.rpy:63
    old "The projects directory could not be set. Giving up."
    new "프로젝트 경로를 설정할 수 없습니다. 취소 중."

    # new_project.rpy:71
    old "You will be creating an [new_project_language] language project. Change the launcher language in preferences to create a project in another language."
    new "[new_project_language] 언어 프로젝트를 생성할 것입니다. 다른 언어로 프로젝트를 생성하려면 환경설정에서 런처 언어를 변경하십시오."

    # new_project.rpy:79
    old "Which interface would you like to use? The new GUI has a modern look, supports wide screens and mobile devices, and is easier to customize. Legacy themes might be necessary to work with older example code.\n\n[language_support!t]\n\nIf in doubt, choose the new GUI, then click Continue on the bottom-right."
    new "어떤 인터페이스를 사용하고 싶으세요? 새로운 GUI는 현대적인 스타일로, 와이드 스크린과 휴대기기를 지원하며 쉽게 커스텀 가능합니다. 레거시 테마는 작업에 오래된 예제 코드가 필요할 수 있습니다.\n\n[language_support!t]\n\n의심스럽다면 새로운 GUI를 선택한 다음, 오른쪽 하단의 계속하기를 클릭하십시오."

    # new_project.rpy:79
    old "Legacy Theme Interface"
    new "레거시 테마 인터페이스"

    # new_project.rpy:100
    old "Choose Project Template"
    new "프로젝트의 서식을 선택하세요"

    # new_project.rpy:118
    old "Please select a template to use for your new project. The template sets the default font and the user interface language. If your language is not supported, choose 'english'."
    new "새 프로젝트에서 사용할 서식을 선택하세요. 서식은 기본 사용 폰트와 UI 언어를 설정합니다. 본인이 사용하는 언어가 지원되지 않는다면, 'english' 를 선택하세요."

    # preferences.rpy:73
    old "Launcher Preferences"
    new "런처 환경설정"

    # preferences.rpy:94
    old "Projects Directory:"
    new "프로젝트 경로:"

    # preferences.rpy:101
    old "[persistent.projects_directory!q]"
    new "[persistent.projects_directory!q]"

    # preferences.rpy:103
    old "Projects directory: [text]"
    new "프로젝트 경로: [text]"

    # preferences.rpy:105
    old "Not Set"
    new "설정되지 않음"

    # preferences.rpy:120
    old "Text Editor:"
    new "텍스트 에디터:"

    # preferences.rpy:126
    old "Text editor: [text]"
    new "텍스트 에디터: [text]"

    # preferences.rpy:145
    old "Navigation Options:"
    new "스크립트 살펴보기 옵션:"

    # preferences.rpy:149
    old "Include private names"
    new "개인 이름을 포함한다"

    # preferences.rpy:150
    old "Include library names"
    new "라이브러리 이름을 포함한다"

    # preferences.rpy:160
    old "Launcher Options:"
    new "런처 옵션:"

    # preferences.rpy:164
    old "Hardware rendering"
    new "하드웨어 렌더링"

    # preferences.rpy:165
    old "Show edit file section"
    new "파일 수정하기 영역 표시하기"

    # preferences.rpy:166
    old "Large fonts"
    new "글자 크게 표시하기"

    # preferences.rpy:169
    old "Console output"
    new "콘솔 출력"

    # preferences.rpy:173
    old "Force new tutorial"
    new "새 튜토리얼 적용"

    # preferences.rpy:177
    old "Legacy options"
    new "레거시 옵션"

    # preferences.rpy:180
    old "Show templates"
    new "탬플릿 보기"

    # preferences.rpy:182
    old "Sponsor message"
    new "스폰서 메시지"

    # preferences.rpy:202
    old "Open launcher project"
    new "런처 프로젝트 열기"

    # preferences.rpy:216
    old "Language:"
    new "언어:"

    # project.rpy:49
    old "After making changes to the script, press shift+R to reload your game."
    new "스크립트를 변경한 다음에는 Shift+R를 눌러 게임을 다시 불러오세요."

    # project.rpy:49
    old "Press shift+O (the letter) to access the console."
    new "Shift+O로 콘솔을 엽니다."

    # project.rpy:49
    old "Press shift+D to access the developer menu."
    new "Shift+D로 개발자 메뉴를 엽니다."

    # project.rpy:49
    old "Have you backed up your projects recently?"
    new "프로젝트는 자주 백업합시다!"

    # project.rpy:281
    old "Launching the project failed."
    new "프로젝트를 실행하지 못했습니다."

    # project.rpy:281
    old "Please ensure that your project launches normally before running this command."
    new "이 명령을 실행하기 전에 프로젝트를 정상적으로 실행했는지 확인하세요."

    # project.rpy:297
    old "Ren'Py is scanning the project..."
    new "프로젝트를 살펴보고 있습니다..."

    # project.rpy:729
    old "Launching"
    new "실행 중"

    # project.rpy:763
    old "PROJECTS DIRECTORY"
    new "프로젝트 경로"

    # project.rpy:763
    old "Please choose the projects directory using the directory chooser.\n{b}The directory chooser may have opened behind this window.{/b}"
    new "경로 선택창을 이용하여 프로젝트가 저장된 경로를 선택하세요.\n{b}경로 선택창이 런처 창 뒤에서 열렸을 수도 있습니다."

    # project.rpy:763
    old "This launcher will scan for projects in this directory, will create new projects in this directory, and will place built projects into this directory."
    new "런처가 이 경로를 살펴보고 이 경로에서 새 프로젝트를 생성하며 프로젝트 배포판을 만듭니다."

    # project.rpy:768
    old "Ren'Py has set the projects directory to:"
    new "렌파이가 프로젝트 경로를 다음과 같이 설정했습니다."

    # translations.rpy:91
    old "Translations: [project.current.name!q]"
    new "번역: [project.current.name!q]"

    # translations.rpy:132
    old "The language to work with. This should only contain lower-case ASCII characters and underscores."
    new "작업할 언어. 소문자 ASCII 문자와 밑줄만 포함해야 합니다."

    # translations.rpy:158
    old "Generate empty strings for translations"
    new "번역 파일 생성 시 빈 문자열 만들기"

    # translations.rpy:176
    old "Generates or updates translation files. The files will be placed in game/tl/[persistent.translate_language!q]."
    new "번역 파일을 생성하거나 업데이트합니다. 파일들은 in game/tl/[persistent.translate_language!q]에 배치됩니다."

    # translations.rpy:196
    old "Extract String Translations"
    new "문자열 번역 추출"

    # translations.rpy:198
    old "Merge String Translations"
    new "문자열 번역 병합"

    # translations.rpy:203
    old "Replace existing translations"
    new "기존 번역 대체"

    # translations.rpy:204
    old "Reverse languages"
    new "역방향 언어"

    # translations.rpy:208
    old "Update Default Interface Translations"
    new "기본 인터페이스 번역 업데이트"

    # translations.rpy:228
    old "The extract command allows you to extract string translations from an existing project into a temporary file.\n\nThe merge command merges extracted translations into another project."
    new "추출 명령은 기존 프로젝트의 문자열 번역을 임시 파일로 추출 할 수 있습니다.\n\n병합 명령은 추출된 번역을 다른 프로젝트로 병합합니다."

    # translations.rpy:252
    old "Ren'Py is generating translations...."
    new "번역 파일을 만들고 있습니다..."

    # translations.rpy:263
    old "Ren'Py has finished generating [language] translations."
    new "[language] 번역 파일을 만들었습니다."

    # translations.rpy:276
    old "Ren'Py is extracting string translations..."
    new "문자열 번역을 추출하고 있습니다..."

    # translations.rpy:279
    old "Ren'Py has finished extracting [language] string translations."
    new "[language] 문자열 번역 추출을 완료했습니다."

    # translations.rpy:299
    old "Ren'Py is merging string translations..."
    new "문자열 번역을 병합하고 있습니다..."

    # translations.rpy:302
    old "Ren'Py has finished merging [language] string translations."
    new "[language] 문자열 번역 병합을 완료했습니다."

    # translations.rpy:313
    old "Updating default interface translations..."
    new "기본 인터페이스 번역을 업데이트하고 있습니다..."

    # translations.rpy:342
    old "Extract Dialogue: [project.current.name!q]"
    new "다이얼로그 추출: [project.current.name!q]"

    # translations.rpy:358
    old "Format:"
    new "포맷:"

    # translations.rpy:366
    old "Tab-delimited Spreadsheet (dialogue.tab)"
    new "탭으로 구분되는 스프레드시트 (dialogue.tab)"

    # translations.rpy:367
    old "Dialogue Text Only (dialogue.txt)"
    new "대사 글자만 (dialogue.txt)"

    # translations.rpy:380
    old "Strip text tags from the dialogue."
    new "텍스트 태그를 대사에서 제거합니다."

    # translations.rpy:381
    old "Escape quotes and other special characters."
    new "따옴표와 기타 특수 문자를 제거합니다."

    # translations.rpy:382
    old "Extract all translatable strings, not just dialogue."
    new "모든 번역 가능한 문자열을 추출합니다."

    # translations.rpy:410
    old "Ren'Py is extracting dialogue...."
    new "대사를 추출하고 있습니다..."

    # translations.rpy:414
    old "Ren'Py has finished extracting dialogue. The extracted dialogue can be found in dialogue.[persistent.dialogue_format] in the base directory."
    new "대사 추출을 완료했습니다. 추출된 대사는 기본 디렉토리의 dialogue.[persistent.dialogue_format]에서 찾을 수 있습니다."

    # updater.rpy:63
    old "{b}Recommended.{/b} The version of Ren'Py that should be used in all newly-released games."
    new "{b}추천.{/b} 새로 배포되는 게임에서 사용할 렌파이 버전."

    # updater.rpy:65
    old "Prerelease"
    new "선배포판"

    # updater.rpy:66
    old "A preview of the next version of Ren'Py that can be used for testing and taking advantage of new features, but not for final releases of games."
    new "렌파이의 다음 버전을 테스트하거나 새로운 기능을 미리 이용할 수 있으나 게임을 최종적으로 배포하기에는 적합하지 않은 선배포 버전. "

    # updater.rpy:68
    old "Experimental"
    new "실험용"

    # updater.rpy:69
    old "Experimental versions of Ren'Py. You shouldn't select this channel unless asked by a Ren'Py developer."
    new "렌파이 실험용 버전. 렌파이 개발자에게 요구받은 것이 아니라면 이 경로를 선택하지 마십시오."

    # updater.rpy:71
    old "Nightly"
    new "야간용"

    # updater.rpy:72
    old "The bleeding edge of Ren'Py development. This may have the latest features, or might not run at all."
    new "검증되지 않은 렌파이 최신 버전. 최신 기능이 포함되어 있거나 전혀 실행되지 않을 수도 있습니다."

    # updater.rpy:90
    old "Select Update Channel"
    new "업데이트 채널 선택"

    # updater.rpy:101
    old "The update channel controls the version of Ren'Py the updater will download."
    new "업데이트 채널은 업데이터가 내려받을 렌파이의 버전을 제어합니다."

    # updater.rpy:110
    old "• This version is installed and up-to-date."
    new "• 최신 버전이 설치돼 있습니다."

    # updater.rpy:118
    old "%B %d, %Y"
    new "%Y년 %m월 %d일"

    # updater.rpy:140
    old "An error has occured:"
    new "오류가 발생했습니다:"

    # updater.rpy:142
    old "Checking for updates."
    new "업데이트 확인 중."

    # updater.rpy:144
    old "Ren'Py is up to date."
    new "렌파이가 최신 버전입니다."

    # updater.rpy:146
    old "[u.version] is now available. Do you want to install it?"
    new "[u.version] 버전을 내려받을 수 있습니다. 설치할까요?"

    # updater.rpy:148
    old "Preparing to download the update."
    new "업데이트 파일 내려받기 준비."

    # updater.rpy:150
    old "Downloading the update."
    new "업데이트 파일 내려받는 중."

    # updater.rpy:152
    old "Unpacking the update."
    new "업데이트 파일 압축해제 중."

    # updater.rpy:154
    old "Finishing up."
    new "마무리 중."

    # updater.rpy:156
    old "The update has been installed. Ren'Py will restart."
    new "업데이트를 설치했습니다. 렌파이를 재시작합니다."

    # updater.rpy:158
    old "The update has been installed."
    new "업데이트를 설치했습니다."

    # updater.rpy:160
    old "The update was cancelled."
    new "업데이트가 취소되었습니다."

    # updater.rpy:177
    old "Ren'Py Update"
    new "렌파이 업데이트"

    # updater.rpy:183
    old "Proceed"
    new "다음으로"

    # front_page.rpy:252
    old "Web"
    new "웹"

    # front_page.rpy:252
    old "Web (Beta)"
    new "웹 (베타)"

    # interface.rpy:394
    old "While [what!qt], an error occured:"
    new "[what!qt]에 오류가 발생했습니다:"

    # interface.rpy:394
    old "[exception!q]"
    new "[exception!q]"

    # itch.rpy:43
    old "Downloading the itch.io butler."
    new "itch.io 집사를 내려받는 중"

    # web.rpy:118
    old "Web: [project.current.display_name!q]"
    new "웹: [project.current.display_name!q]"

    # web.rpy:148
    old "Build Web Application"
    new "웹 애플리케이션 빌드"

    # web.rpy:149
    old "Build and Open in Browser"
    new "빌드 및 브라우저에서 열기"

    # web.rpy:150
    old "Open in Browser"
    new "브라우저에서 열기"

    # web.rpy:151
    old "Open build directory"
    new "빌드 디렉토리 열기"

    # web.rpy:154
    old "Support:"
    new "지원:"

    # web.rpy:162
    old "RenPyWeb Home"
    new "렌파이웹 누리집"

    # web.rpy:163
    old "Beuc's Patreon"
    new "Beuc의 페이트리온"

    # web.rpy:181
    old "Ren'Py web applications require the entire game to be downloaded to the player's computer before it can start."
    new "렌파이 웹 애플리케이션은 게임을 시작하기 전에 전체 게임을 플레이어의 컴퓨터에 다운로드해야 합니다."

    # web.rpy:185
    old "Current limitations in the web platform mean that loading large images, audio files, or movies may cause audio or framerate glitches, and lower performance in general."
    new "웹 플랫폼의 현재 제한 사항은 큰 이미지나 오디오 파일, 또는 동영상을 불러오면 오디오 또는 프레임 결함이 발생하고 일반적으로 성능이 저하될 수 있음을 의미합니다."

    # web.rpy:194
    old "Before packaging web apps, you'll need to download RenPyWeb, Ren'Py's web support. Would you like to download RenPyWeb now?"
    new "웹 앱을 패키징하려면 렌파이의 웹 지원인 렌파이웹(RenpyWeb)이 필요합니다. 지금 내려받으시겠습니까?"

    # updater.rpy:188
    old "Fetching the list of update channels"
    new "업데이트 채널 목록 가져오기"

    # choose_theme.rpy:507
    old "changing the theme"
    new "테마를 바꾸는 중"

    # gui7.rpy:429
    old "creating a new project"
    new "새 프로젝트를 만드는 중"

    # gui7.rpy:433
    old "activating the new project"
    new "새 프로젝트를 활성화하는 중"

    # interface.rpy:372
    old "opening the log file"
    new "로그 파일을 여는 중"

    # updater.rpy:194
    old "downloading the list of update channels"
    new "업데이트 채널의 목록을 내려받는 중"

    # updater.rpy:198
    old "parsing the list of update channels"
    new "업데이트 채널의 목록을 분석하는 중"
