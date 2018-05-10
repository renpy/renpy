
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
    new "파일 이름에는 반드시 .rpy 확장자가 적혀있어야 합니다."

    # add_file.rpy:39
    old "The file already exists."
    new "이 파일 이름은 이미 존재합니다."

    # add_file.rpy:42
    old "# Ren'Py automatically loads all script files ending with .rpy. To use this\n# file, define a label and jump to it from another file.\n"
    new "# 렌파이는 자동으로 파일 이름이 .rpy 로 끝나는 스크립트 파일을 불러옵니다. \n# 파일을 사용하려면, 레이블을 정의하여 다른 파일에서 해당 레이블로 점프하세요.\n"

    # android.rpy:30
    old "To build Android packages, please download RAPT, unzip it, and place it into the Ren'Py directory. Then restart the Ren'Py launcher."
    new "안드로이드 패키지를 만드려면, RAPT 파일을 내려받은 뒤에 렌파이 디렉토리에 압축 해제하세요. 그 다음 렌파이 런처를 재시작하세요."

    # android.rpy:31
    old "An x86 Java Development Kit is required to build Android packages on Windows. The JDK is different from the JRE, so it's possible you have Java without having the JDK.\n\nPlease {a=http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html}download and install the JDK{/a}, then restart the Ren'Py launcher."
    new "윈도우에서 안드로이드 패키지를 만드려면 32비트 JDK가 필요합니다. JDK는 JRE와 다르므로 PC에 JDK가 없는 자바가 설치되어 있을 수 있습니다.\n\n{a=http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html}JDK를 내려받아 설치한 뒤{/a}, 렌파이 런처를 재시작해주세요."

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
    old "Connects to an Android device running ADB in TCP/IP mode."
    new "TCP/IP 모드로 실행 중인 ADB를 안드로이드 기기에 연결합니다."

    # android.rpy:49
    old "Disconnects from an Android device running ADB in TCP/IP mode."
    new "TCP/IP 모드로 실행 중인 ADB를 안드로이드 기기에서 연결 해제합니다."

    # android.rpy:50
    old "Retrieves the log from the Android device and writes it to a file."
    new "Retrieves the log from the Android device and writes it to a file."

    # android.rpy:240
    old "Copying Android files to distributions directory."
    new "안드로이드 파일을 패키지 경로에 복사하는 중."

    # android.rpy:304
    old "Android: [project.current.name!q]"
    new "안드로이드: [project.current.name!q]"

    # android.rpy:324
    old "Emulation:"
    new "에뮬레이션:"

    # android.rpy:333
    old "Phone"
    new "스마트폰"

    # android.rpy:337
    old "Tablet"
    new "태블릿"

    # android.rpy:341
    old "Television"
    new "TV"

    # android.rpy:353
    old "Build:"
    new "만들기:"

    # android.rpy:361
    old "Install SDK & Create Keys"
    new "SDK 설치 & 키 생성하기"

    # android.rpy:365
    old "Configure"
    new "설정하기"

    # android.rpy:369
    old "Build Package"
    new "패키지 만들기"

    # android.rpy:373
    old "Build & Install"
    new "패키지 만들기 & 설치"

    # android.rpy:377
    old "Build, Install & Launch"
    new "패키지를 만들어 설치하고 실행하기"

    # android.rpy:388
    old "Other:"
    new "기타:"

    # android.rpy:396
    old "Remote ADB Connect"
    new "ADB 연결"

    # android.rpy:400
    old "Remote ADB Disconnect"
    new "원격 ADB 연결 해제"

    # android.rpy:404
    old "Logcat"
    new "Logcat"

    # android.rpy:437
    old "Before packaging Android apps, you'll need to download RAPT, the Ren'Py Android Packaging Tool. Would you like to download RAPT now?"
    new "안드로이드 앱을 만들기 전에, 렌파이 안드로이드 패키징 도구(RAPT)를 내려받아야합니다. RAPT를 내려받으시겠습니까?"

    # android.rpy:496
    old "Remote ADB Address"
    new "원격 ADB 주소"

    # android.rpy:496
    old "Please enter the IP address and port number to connect to, in the form \"192.168.1.143:5555\". Consult your device's documentation to determine if it supports remote ADB, and if so, the address and port to use."
    new "\"192.168.1.143:5555\" 형식으로 연결할 기기의 IP주소와 포트를 입력하세요.  문서를 참고하여 기기가 원격 ADB를 지원하는지 확인한 다음, 사용할 주소와 포트를 입력하세요."

    # android.rpy:508
    old "Invalid remote ADB address"
    new "사용할 수 없는 원격 ADB 주소"

    # android.rpy:508
    old "The address must contain one exactly one ':'."
    new "주소에는 ':' 한 개가 포함되어야 합니다."

    # android.rpy:512
    old "The host may not contain whitespace."
    new "호스트 주소에는 공백이 없어야 합니다."

    # android.rpy:518
    old "The port must be a number."
    new "포트는 반드시 숫자이어야 합니다."

    # android.rpy:544
    old "Retrieving logcat information from device."
    new "Retrieving logcat information from device."

    # choose_directory.rpy:73
    old "Ren'Py was unable to run python with tkinter to choose the directory. Please install the python-tk or tkinter package."
    new "프로젝트 경로를 선택하는 tkinter를 구동하지 못했습니다. python-tk나 tkinter 패키지를 설치하세요."

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
    new "The command is being run in a new operating system console window."

    # distribute.rpy:443
    old "Scanning project files..."
    new "프로젝트 파일 살펴보는 중..."

    # distribute.rpy:459
    old "Building distributions failed:\n\nThe build.directory_name variable may not include the space, colon, or semicolon characters."
    new "배포판 만들기에 실패했습니다.\n\n build.directory_name 변수에는 공백이나 콜론, 세미 콜론 문자를 입력할 수 없습니다."

    # distribute.rpy:504
    old "No packages are selected, so there's nothing to do."
    new "선택된 패키지가 없으므로 할 수 있는 작업이 없습니다."

    # distribute.rpy:516
    old "Scanning Ren'Py files..."
    new "렌파이 파일 살펴보는 중..."

    # distribute.rpy:569
    old "All packages have been built.\n\nDue to the presence of permission information, unpacking and repacking the Linux and Macintosh distributions on Windows is not supported."
    new "패키지를 전부 작성했습니다.\n\n 권한 정보로 인해 리눅스와 매킨토시 배포판을 윈도우에서 압축해제하거나 재압축하는 것은 지원하지 않습니다."

    # distribute.rpy:752
    old "Archiving files..."
    new "파일 압축 중..."

    # distribute.rpy:1050
    old "Unpacking the Macintosh application for signing..."
    new "Unpacking the Macintosh application for signing..."

    # distribute.rpy:1060
    old "Signing the Macintosh application..."
    new "Signing the Macintosh application..."

    # distribute.rpy:1082
    old "Creating the Macintosh DMG..."
    new "Creating the Macintosh DMG..."

    # distribute.rpy:1091
    old "Signing the Macintosh DMG..."
    new "Signing the Macintosh DMG..."

    # distribute.rpy:1248
    old "Writing the [variant] [format] package."
    new "[variant] [format] 패키지 작성 중."

    # distribute.rpy:1261
    old "Making the [variant] update zsync file."
    new "[variant] 업데이트 zsync 파일 생성 중."

    # distribute.rpy:1404
    old "Processed {b}[complete]{/b} of {b}[total]{/b} files."
    new "총 {b}[total]{/b}개의 파일 중에서 {b}[complete]{/b} 파일 완료."

    # distribute_gui.rpy:157
    old "Build Distributions: [project.current.name!q]"
    new "[project.current.name!q] 배포판 만들기"

    # distribute_gui.rpy:171
    old "Directory Name:"
    new "디렉토리 이름:"

    # distribute_gui.rpy:175
    old "Executable Name:"
    new "실행 파일 이름:"

    # distribute_gui.rpy:185
    old "Actions:"
    new "작업:"

    # distribute_gui.rpy:193
    old "Edit options.rpy"
    new "options.rpy 수정하기"

    # distribute_gui.rpy:194
    old "Add from clauses to calls, once"
    new "from 절을 call 문에 추가하기(1회)"

    # distribute_gui.rpy:195
    old "Refresh"
    new "새로고침"

    # distribute_gui.rpy:199
    old "Upload to itch.io"
    new "Upload to itch.io"

    # distribute_gui.rpy:215
    old "Build Packages:"
    new "만들 패키지:"

    # distribute_gui.rpy:234
    old "Options:"
    new "설정:"

    # distribute_gui.rpy:239
    old "Build Updates"
    new "업데이트 파일 만들기"

    # distribute_gui.rpy:241
    old "Add from clauses to calls"
    new "from 절을 call 문에 추가하기"

    # distribute_gui.rpy:242
    old "Force Recompile"
    new "강제 재컴파일"

    # distribute_gui.rpy:246
    old "Build"
    new "만들기"

    # distribute_gui.rpy:250
    old "Adding from clauses to call statements that do not have them."
    new "from 절이 없는 call 문에 from 절을 추가합니다."

    # distribute_gui.rpy:271
    old "Errors were detected when running the project. Please ensure the project runs without errors before building distributions."
    new "프로젝트를 실행하던 도중 오류를 발견했습니다. 배포판을 작성하기 전에 프로젝트가 오류 없이 실행되는지 확인하세요."

    # distribute_gui.rpy:288
    old "Your project does not contain build information. Would you like to add build information to the end of options.rpy?"
    new "프로젝트에 배포판 정보가 없습니다. options.rpy 끝부분에 배포판 정보를 추가하겠습니까?"

    # editor.rpy:150
    old "{b}Recommended.{/b} A beta editor with an easy to use interface and features that aid in development, such as spell-checking. Editra currently lacks the IME support required for Chinese, Japanese, and Korean text input."
    new "{b}추천.{/b} 인터페이스를 사용하기 쉬우며 맞춤법 검사 등 개발을 편리하게 해주는 기능이 있는 에디터입니다. 에디트라는 현재 중국어, 일본어, 한국어 텍스트를 입력할 때 필요한 IME를 지원하지 않습니다."

    # editor.rpy:151
    old "{b}Recommended.{/b} A beta editor with an easy to use interface and features that aid in development, such as spell-checking. Editra currently lacks the IME support required for Chinese, Japanese, and Korean text input. On Linux, Editra requires wxPython."
    new "{b}추천.{/b} 인터페이스를 사용하기 쉬우며 맞춤법 검사 등 개발을 편리하게 해주는 기능이 있는 에디터입니다. 에디트라는 현재 중국어, 일본어, 한국어 텍스트를 입력할 때 필요한 IME를 지원하지 않습니다. 에디트라를 리눅스에서 실행하려면 wxPython이 필요합니다."

    # editor.rpy:167
    old "This may have occured because wxPython is not installed on this system."
    new "wxPython이 설치되지 않아 문제가 발생했을 가능성이 있습니다."

    # editor.rpy:169
    old "Up to 22 MB download required."
    new "22MB 내려받기 필요."

    # editor.rpy:182
    old "A mature editor that requires Java."
    new "Java를 사용하는 완성도 높은 에디터."

    # editor.rpy:182
    old "1.8 MB download required."
    new "1.8MB 내려받기 필요."

    # editor.rpy:182
    old "This may have occured because Java is not installed on this system."
    new "Java가 설치되지 않아 문제가 발생했을 수도 있습니다."

    # editor.rpy:191
    old "Invokes the editor your operating system has associated with .rpy files."
    new "OS에서 .rpy 파일을 열 때 사용하는 에디터를 실행합니다."

    # editor.rpy:207
    old "Prevents Ren'Py from opening a text editor."
    new "렌파이가 스크립트 에디터를 실행하지 못하도록 합니다."

    # editor.rpy:359
    old "An exception occured while launching the text editor:\n[exception!q]"
    new "스크립트 에디터를 실행하던 도중 예외가 발생했습니다:\n[exception!q]"

    # editor.rpy:457
    old "Select Editor"
    new "에디터 선택하기"

    # editor.rpy:472
    old "A text editor is the program you'll use to edit Ren'Py script files. Here, you can select the editor Ren'Py will use. If not already present, the editor will be automatically downloaded and installed."
    new "스크립트 에디터란 렌파이 스크립트 파일을 수정할 때 사용하는 프로그램입니다. 이곳에서는 렌파이가 실행시킬 에디터를 선택할 수 있습니다. 에디터가 없다면 에디터를 자동으로 다운로드해 설치합니다."

    # editor.rpy:494
    old "Cancel"
    new "취소"

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
    new "The Question"

    # front_page.rpy:182
    old "Active Project"
    new "진행 중인 프로젝트"

    # front_page.rpy:190
    old "Open Directory"
    new "폴더 열기"

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

    # front_page.rpy:214
    old "All script files"
    new "모든 스크립트 파일"

    # front_page.rpy:223
    old "Navigate Script"
    new "스크립트 살펴보기"

    # front_page.rpy:234
    old "Check Script (Lint)"
    new "스크립트 확인 (오류 검사)"

    # front_page.rpy:237
    old "Change/Update GUI"
    new "Change/Update GUI"

    # front_page.rpy:239
    old "Change Theme"
    new "테마 바꾸기"

    # front_page.rpy:242
    old "Delete Persistent"
    new "지속 데이터 삭제하기"

    # front_page.rpy:251
    old "Build Distributions"
    new "배포판 만들기"

    # front_page.rpy:253
    old "Android"
    new "안드로이드"

    # front_page.rpy:254
    old "iOS"
    new "iOS"

    # front_page.rpy:255
    old "Generate Translations"
    new "번역 파일 만들기"

    # front_page.rpy:256
    old "Extract Dialogue"
    new "대사 추출하기"

    # front_page.rpy:272
    old "Checking script for potential problems..."
    new "스크립트에서 문제가 발생할 수 있는지를 확인하고 있습니다..."

    # front_page.rpy:287
    old "Deleting persistent data..."
    new "지속 데이터를 삭제하고 있습니다... "

    # front_page.rpy:295
    old "Recompiling all rpy files into rpyc files..."
    new "모든 rpy 파일을 rpyc 파일로 재컴파일하는 중..."

    # gui7.rpy:236
    old "Select Accent and Background Colors"
    new "Select Accent and Background Colors"

    # gui7.rpy:250
    old "Please click on the color scheme you wish to use, then click Continue. These colors can be changed and customized later."
    new "Please click on the color scheme you wish to use, then click Continue. These colors can be changed and customized later."

    # gui7.rpy:294
    old "{b}Warning{/b}\nContinuing will overwrite customized bar, button, save slot, scrollbar, and slider images.\n\nWhat would you like to do?"
    new "{b}Warning{/b}\nContinuing will overwrite customized bar, button, save slot, scrollbar, and slider images.\n\nWhat would you like to do?"

    # gui7.rpy:294
    old "Choose new colors, then regenerate image files."
    new "Choose new colors, then regenerate image files."

    # gui7.rpy:294
    old "Regenerate the image files using the colors in gui.rpy."
    new "Regenerate the image files using the colors in gui.rpy."

    # gui7.rpy:314
    old "PROJECT NAME"
    new "프로젝트 이름"

    # gui7.rpy:314
    old "Please enter the name of your project:"
    new "프로젝트 이름을 입력하세요:"

    # gui7.rpy:322
    old "The project name may not be empty."
    new "프로젝트 이름을 입력하지 않았습니다."

    # gui7.rpy:327
    old "[project_name!q] already exists. Please choose a different project name."
    new "[project_name!q]는 이미 존재합니다. 다른 프로젝트 이름을 선택하세요."

    # gui7.rpy:330
    old "[project_dir!q] already exists. Please choose a different project name."
    new "[project_dir!q]는 이미 존재합니다. 다른 프로젝트 이름을 선택하세요."

    # gui7.rpy:341
    old "What resolution should the project use? Although Ren'Py can scale the window up and down, this is the initial size of the window, the size at which assets should be drawn, and the size at which the assets will be at their sharpest.\n\nThe default of 1280x720 is a reasonable compromise."
    new "What resolution should the project use? Although Ren'Py can scale the window up and down, this is the initial size of the window, the size at which assets should be drawn, and the size at which the assets will be at their sharpest.\n\nThe default of 1280x720 is a reasonable compromise."

    # gui7.rpy:389
    old "Creating the new project..."
    new "Creating the new project..."

    # gui7.rpy:391
    old "Updating the project..."
    new "Updating the project..."

    # interface.rpy:107
    old "Documentation"
    new "매뉴얼"

    # interface.rpy:108
    old "Ren'Py Website"
    new "렌파이 공식 홈페이지"

    # interface.rpy:109
    old "Ren'Py Games List"
    new "렌파이 게임 목록"

    # interface.rpy:117
    old "update"
    new "업데이트"

    # interface.rpy:119
    old "preferences"
    new "환경설정"

    # interface.rpy:120
    old "quit"
    new "종료"

    # interface.rpy:232
    old "Due to package format limitations, non-ASCII file and directory names are not allowed."
    new "패키지 형식에 제한이 있으므로 ASCII가 아닌 문자가 입력된 파일 이름이나 디렉토리 이름은 사용할 수 없습니다."

    # interface.rpy:327
    old "ERROR"
    new "오류"

    # interface.rpy:356
    old "While [what!q], an error occured:"
    new "[what!q] 도중, 에러가 발생했습니다:"

    # interface.rpy:356
    old "[exception!q]"
    new "[exception!q]"

    # interface.rpy:375
    old "Text input may not contain the {{ or [[ characters."
    new "글자를 입력할 때는 {{나 [[ 문자는 없어야 합니다."

    # interface.rpy:380
    old "File and directory names may not contain / or \\."
    new "파일 및 디렉토리 이름에는 / 나 \\가 없어야 합니다."

    # interface.rpy:386
    old "File and directory names must consist of ASCII characters."
    new "파일이나 디렉토리 이름은 ASCII 문자로 지어야 합니다."

    # interface.rpy:454
    old "PROCESSING"
    new "처리 중"

    # interface.rpy:471
    old "QUESTION"
    new "확인"

    # interface.rpy:484
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
    new "The built distributions could not be found. Please choose 'Build' and try again."

    # itch.rpy:91
    old "No uploadable files were found. Please choose 'Build' and try again."
    new "No uploadable files were found. Please choose 'Build' and try again."

    # itch.rpy:99
    old "The butler program was not found."
    new "The butler program was not found."

    # itch.rpy:99
    old "Please install the itch.io app, which includes butler, and try again."
    new "Please install the itch.io app, which includes butler, and try again."

    # itch.rpy:108
    old "The name of the itch project has not been set."
    new "The name of the itch project has not been set."

    # itch.rpy:108
    old "Please {a=https://itch.io/game/new}create your project{/a}, then add a line like \n{vspace=5}define build.itch_project = \"user-name/game-name\"\n{vspace=5} to options.rpy."
    new "Please {a=https://itch.io/game/new}create your project{/a}, then add a line like \n{vspace=5}define build.itch_project = \"user-name/game-name\"\n{vspace=5} to options.rpy."

    # mobilebuild.rpy:109
    old "{a=%s}%s{/a}"
    new "{a=%s}%s{/a}"

    # navigation.rpy:168
    old "Navigate: [project.current.name]"
    new "[project.current.name] 살펴보기"

    # navigation.rpy:177
    old "Order: "
    new "순서: "

    # navigation.rpy:178
    old "alphabetical"
    new "알파벳 순서로"

    # navigation.rpy:180
    old "by-file"
    new "파일 별로"

    # navigation.rpy:182
    old "natural"
    new "생성된 순서대로"

    # navigation.rpy:194
    old "Category:"
    new "종류:"

    # navigation.rpy:196
    old "files"
    new "파일"

    # navigation.rpy:197
    old "labels"
    new "레이블"

    # navigation.rpy:198
    old "defines"
    new "정의"

    # navigation.rpy:199
    old "transforms"
    new "트랜스폼"

    # navigation.rpy:200
    old "screens"
    new "스크린"

    # navigation.rpy:201
    old "callables"
    new "콜러블"

    # navigation.rpy:202
    old "TODOs"
    new "해야할 작업"

    # navigation.rpy:241
    old "+ Add script file"
    new "+ 새 스크립트 파일 추가하기"

    # navigation.rpy:249
    old "No TODO comments found.\n\nTo create one, include \"# TODO\" in your script."
    new "TODO 주석을 발견하지 못했습니다.\n\nTODO 주석을 만드려면 스크립트 파일에 \"# TODO\" 를 적으세요."

    # navigation.rpy:256
    old "The list of names is empty."
    new "이름 목록이 비었습니다."

    # new_project.rpy:38
    old "New GUI Interface"
    new "New GUI Interface"

    # new_project.rpy:48
    old "Both interfaces have been translated to your language."
    new "Both interfaces have been translated to your language."

    # new_project.rpy:50
    old "Only the new GUI has been translated to your language."
    new "Only the new GUI has been translated to your language."

    # new_project.rpy:52
    old "Only the legacy theme interface has been translated to your language."
    new "Only the legacy theme interface has been translated to your language."

    # new_project.rpy:54
    old "Neither interface has been translated to your language."
    new "Neither interface has been translated to your language."

    # new_project.rpy:63
    old "The projects directory could not be set. Giving up."
    new "프로젝트 경로를 설정할 수 없습니다. 취소 중."

    # new_project.rpy:69
    old "Which interface would you like to use? The new GUI has a modern look, supports wide screens and mobile devices, and is easier to customize. Legacy themes might be necessary to work with older example code.\n\n[language_support!t]\n\nIf in doubt, choose the new GUI, then click Continue on the bottom-right."
    new "Which interface would you like to use? The new GUI has a modern look, supports wide screens and mobile devices, and is easier to customize. Legacy themes might be necessary to work with older example code.\n\n[language_support!t]\n\nIf in doubt, choose the new GUI, then click Continue on the bottom-right."

    # new_project.rpy:69
    old "Legacy Theme Interface"
    new "Legacy Theme Interface"

    # new_project.rpy:90
    old "Choose Project Template"
    new "프로젝트의 서식을 선택하세요"

    # new_project.rpy:108
    old "Please select a template to use for your new project. The template sets the default font and the user interface language. If your language is not supported, choose 'english'."
    new "새 프로젝트에서 사용할 서식을 선택하세요. 서식은 기본 사용 폰트와 UI 언어를 설정합니다. 본인이 사용하는 언어가 지원되지 않는다면, 'english' 를 선택하세요."

    # preferences.rpy:64
    old "Launcher Preferences"
    new "런처 환경설정"

    # preferences.rpy:85
    old "Projects Directory:"
    new "프로젝트 경로:"

    # preferences.rpy:92
    old "[persistent.projects_directory!q]"
    new "[persistent.projects_directory!q]"

    # preferences.rpy:94
    old "Projects directory: [text]"
    new "프로젝트 경로: [text]"

    # preferences.rpy:96
    old "Not Set"
    new "설정되지 않음"

    # preferences.rpy:111
    old "Text Editor:"
    new "스크립트 에디터:"

    # preferences.rpy:117
    old "Text editor: [text]"
    new "텍스트 에디터: [text]"

    # preferences.rpy:133
    old "Update Channel:"
    new "업데이트 경로:"

    # preferences.rpy:153
    old "Navigation Options:"
    new "스크립트 살펴보기 옵션:"

    # preferences.rpy:157
    old "Include private names"
    new "개인 이름을 포함한다"

    # preferences.rpy:158
    old "Include library names"
    new "라이브러리 이름을 포함한다"

    # preferences.rpy:168
    old "Launcher Options:"
    new "런처 옵션:"

    # preferences.rpy:172
    old "Hardware rendering"
    new "하드웨어 렌더링"

    # preferences.rpy:173
    old "Show templates"
    new "서식 표시하기"

    # preferences.rpy:174
    old "Show edit file section"
    new "파일 수정하기 영역 표시하기"

    # preferences.rpy:175
    old "Large fonts"
    new "글자 크게 표시하기"

    # preferences.rpy:178
    old "Console output"
    new "콘솔 출력"

    # preferences.rpy:199
    old "Open launcher project"
    new "런처 프로젝트 열기"

    # preferences.rpy:213
    old "Language:"
    new "언어:"

    # project.rpy:47
    old "After making changes to the script, press shift+R to reload your game."
    new "스크립트를 변경한 다음에는 Shift+R를 눌러 게임을 다시 불러오세요."

    # project.rpy:47
    old "Press shift+O (the letter) to access the console."
    new "Shift+O로 콘솔을 엽니다."

    # project.rpy:47
    old "Press shift+D to access the developer menu."
    new "Shift+D로 개발자 메뉴를 엽니다."

    # project.rpy:47
    old "Have you backed up your projects recently?"
    new "프로젝트는 자주 백업합시다!"

    # project.rpy:229
    old "Launching the project failed."
    new "프로젝트를 실행하지 못했습니다."

    # project.rpy:229
    old "Please ensure that your project launches normally before running this command."
    new "이 명령을 실행하기 전에 프로젝트를 정상적으로 실행했는지 확인하세요."

    # project.rpy:242
    old "Ren'Py is scanning the project..."
    new "프로젝트를 살펴보고 있습니다..."

    # project.rpy:568
    old "Launching"
    new "실행 중"

    # project.rpy:597
    old "PROJECTS DIRECTORY"
    new "프로젝트 경로"

    # project.rpy:597
    old "Please choose the projects directory using the directory chooser.\n{b}The directory chooser may have opened behind this window.{/b}"
    new "경로 선택창을 이용하여 프로젝트가 저장된 경로를 선택하세요.\n{b}경로 선택창이 런처 창 뒤에서 열렸을 수도 있습니다."

    # project.rpy:597
    old "This launcher will scan for projects in this directory, will create new projects in this directory, and will place built projects into this directory."
    new "런처가 이 경로를 살펴보고 이 경로에서 새 프로젝트를 생성하며 프로젝트 배포판을 만듭니다."

    # project.rpy:602
    old "Ren'Py has set the projects directory to:"
    new "렌파이가 프로젝트 경로를 다음과 같이 설정했습니다."

    # translations.rpy:63
    old "Translations: [project.current.name!q]"
    new "Translations: [project.current.name!q]"

    # translations.rpy:104
    old "The language to work with. This should only contain lower-case ASCII characters and underscores."
    new "The language to work with. This should only contain lower-case ASCII characters and underscores."

    # translations.rpy:130
    old "Generate empty strings for translations"
    new "번역 파일 생성 시 빈 문자열 만들기"

    # translations.rpy:148
    old "Generates or updates translation files. The files will be placed in game/tl/[persistent.translate_language!q]."
    new "Generates or updates translation files. The files will be placed in game/tl/[persistent.translate_language!q]."

    # translations.rpy:168
    old "Extract String Translations"
    new "Extract String Translations"

    # translations.rpy:170
    old "Merge String Translations"
    new "Merge String Translations"

    # translations.rpy:175
    old "Replace existing translations"
    new "Replace existing translations"

    # translations.rpy:176
    old "Reverse languages"
    new "Reverse languages"

    # translations.rpy:180
    old "Update Default Interface Translations"
    new "Update Default Interface Translations"

    # translations.rpy:200
    old "The extract command allows you to extract string translations from an existing project into a temporary file.\n\nThe merge command merges extracted translations into another project."
    new "The extract command allows you to extract string translations from an existing project into a temporary file.\n\nThe merge command merges extracted translations into another project."

    # translations.rpy:224
    old "Ren'Py is generating translations...."
    new "번역 파일을 만들고 있습니다..."

    # translations.rpy:235
    old "Ren'Py has finished generating [language] translations."
    new "[language] 번역 파일을 만들었습니다."

    # translations.rpy:248
    old "Ren'Py is extracting string translations..."
    new "Ren'Py is extracting string translations..."

    # translations.rpy:251
    old "Ren'Py has finished extracting [language] string translations."
    new "Ren'Py has finished extracting [language] string translations."

    # translations.rpy:271
    old "Ren'Py is merging string translations..."
    new "Ren'Py is merging string translations..."

    # translations.rpy:274
    old "Ren'Py has finished merging [language] string translations."
    new "Ren'Py has finished merging [language] string translations."

    # translations.rpy:282
    old "Updating default interface translations..."
    new "Updating default interface translations..."

    # translations.rpy:306
    old "Extract Dialogue: [project.current.name!q]"
    new "Extract Dialogue: [project.current.name!q]"

    # translations.rpy:322
    old "Format:"
    new "Format:"

    # translations.rpy:330
    old "Tab-delimited Spreadsheet (dialogue.tab)"
    new "Tab-delimited Spreadsheet (dialogue.tab)"

    # translations.rpy:331
    old "Dialogue Text Only (dialogue.txt)"
    new "Dialogue Text Only (dialogue.txt)"

    # translations.rpy:344
    old "Strip text tags from the dialogue."
    new "Strip text tags from the dialogue."

    # translations.rpy:345
    old "Escape quotes and other special characters."
    new "Escape quotes and other special characters."

    # translations.rpy:346
    old "Extract all translatable strings, not just dialogue."
    new "Extract all translatable strings, not just dialogue."

    # translations.rpy:374
    old "Ren'Py is extracting dialogue...."
    new "대사를 추출하고 있습니다..."

    # translations.rpy:378
    old "Ren'Py has finished extracting dialogue. The extracted dialogue can be found in dialogue.[persistent.dialogue_format] in the base directory."
    new "Ren'Py has finished extracting dialogue. The extracted dialogue can be found in dialogue.[persistent.dialogue_format] in the base directory."

    # updater.rpy:75
    old "Select Update Channel"
    new "업데이트 경로 선택"

    # updater.rpy:86
    old "The update channel controls the version of Ren'Py the updater will download. Please select an update channel:"
    new "업데이트 경로는 업데이터가 다운로드할 렌파이 버전을 제어합니다. 업데이트 경로를 선택해주세요:"

    # updater.rpy:91
    old "Release"
    new "배포판"

    # updater.rpy:97
    old "{b}Recommended.{/b} The version of Ren'Py that should be used in all newly-released games."
    new "{b}추천.{/b} 새로 배포되는 게임에서 사용할 렌파이 버전."

    # updater.rpy:102
    old "Prerelease"
    new "선배포판"

    # updater.rpy:108
    old "A preview of the next version of Ren'Py that can be used for testing and taking advantage of new features, but not for final releases of games."
    new "렌파이의 다음 버전을 테스트하거나 새로운 기능을 미리 이용할 수 있으나 게임을 최종적으로 배포하기에는 적합하지 않은 선배포 버전. "

    # updater.rpy:114
    old "Experimental"
    new "실험용"

    # updater.rpy:120
    old "Experimental versions of Ren'Py. You shouldn't select this channel unless asked by a Ren'Py developer."
    new "렌파이 실험용 버전. 렌파이 개발자에게 요구받은 것이 아니라면 이 경로를 선택하지 마십시오."

    # updater.rpy:126
    old "Nightly"
    new "야간용"

    # updater.rpy:132
    old "The bleeding edge of Ren'Py development. This may have the latest features, or might not run at all."
    new "검증되지 않은 렌파이 최신 버전. 최신 기능이 포함되어 있거나 전혀 실행되지 않을 수도 있습니다."

    # updater.rpy:152
    old "An error has occured:"
    new "오류가 발생했습니다:"

    # updater.rpy:154
    old "Checking for updates."
    new "업데이트 확인 중."

    # updater.rpy:156
    old "Ren'Py is up to date."
    new "렌파이가 최신 버전입니다."

    # updater.rpy:158
    old "[u.version] is now available. Do you want to install it?"
    new "[u.version] 버전을 내려받을 수 있습니다. 설치할까요?"

    # updater.rpy:160
    old "Preparing to download the update."
    new "업데이트 파일 내려받기 준비."

    # updater.rpy:162
    old "Downloading the update."
    new "업데이트 파일 내려받는 중."

    # updater.rpy:164
    old "Unpacking the update."
    new "업데이트 파일 압축해제 중."

    # updater.rpy:166
    old "Finishing up."
    new "마무리 중."

    # updater.rpy:168
    old "The update has been installed. Ren'Py will restart."
    new "업데이트를 설치했습니다. 렌파이를 재시작합니다."

    # updater.rpy:170
    old "The update has been installed."
    new "업데이트를 설치했습니다."

    # updater.rpy:172
    old "The update was cancelled."
    new "업데이트가 취소되었습니다."

    # updater.rpy:189
    old "Ren'Py Update"
    new "렌파이 업데이트"

    # updater.rpy:195
    old "Proceed"
    new "다음으로"

