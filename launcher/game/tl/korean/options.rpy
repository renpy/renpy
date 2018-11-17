translate korean strings:

    # options.rpy:1
    old "## This file contains options that can be changed to customize your game."
    new "## 이 파일은 귀하의 게임 커스텀으로 변경될 수 있는 옵션을 포함합니다."

    # options.rpy:4
    old "## Lines beginning with two '#' marks are comments, and you shouldn't uncomment them. Lines beginning with a single '#' mark are commented-out code, and you may want to uncomment them when appropriate."
    new "## 두 개의 '#' 표시로 시작되는 줄은 주석이며, 그것을 없애지 말아야 합니다. 한 개의 '#' 표시로 시작되는 줄은 주석 처리된 코드로 필요한 경우 제거해도 됩니다."

    # options.rpy:10
    old "## Basics"
    new "## 기본"

    # options.rpy:12
    old "## A human-readable name of the game. This is used to set the default window title, and shows up in the interface and error reports."
    new "## 인간이 읽을 수 있는 게임의 이름. 기본 윈도우의 제목으로 사용되며, 인터페이스와 오류 보고에서 보여집니다."

    # options.rpy:15
    old "## The _() surrounding the string marks it as eligible for translation."
    new "## 문자열을 _()로 둘러 쌓으면 씌우면 번역의 대상으로 표시됩니다."

    # options.rpy:17
    old "Ren'Py 7 Default GUI"
    new "렌파이 7 기본 GUI"

    # options.rpy:20
    old "## Determines if the title given above is shown on the main menu screen. Set this to False to hide the title."
    new "## 위에 주어진 제목이 주 메뉴 화면에 표시되는지 결정합니다. 제목을 숨기려면 이것을 False로 설정하십시오."

    # options.rpy:26
    old "## The version of the game."
    new "## 게임의 버전입니다."

    # options.rpy:31
    old "## Text that is placed on the game's about screen. Place the text between the triple-quotes, and leave a blank line between paragraphs."
    new "## 게임의 about 스크린에 배치되는 텍스트입니다. 텍스트를 삼중 따옴표 사이에 배치하고 단락 사이에 빈 줄을 남겨 둡니다."

    # options.rpy:38
    old "## A short name for the game used for executables and directories in the built distribution. This must be ASCII-only, and must not contain spaces, colons, or semicolons."
    new "## 배포판의 실행 파일과 디렉토리에 사용되는 게임의 약식 이름. 이것은 ASCII 전용이어야 하며 공백, 콜론 또는 세미콜론을 포함해서는 안 됩니다."

    # options.rpy:45
    old "## Sounds and music"
    new "## 음악과 음향"

    # options.rpy:47
    old "## These three variables control which mixers are shown to the player by default. Setting one of these to False will hide the appropriate mixer."
    new "## 이 세 가지 변수는 기본적으로 플레이어에 표시되는 믹서를 제어합니다. 이들 중 하나를 False로 설정하면 해당 믹서가 숨겨집니다."

    # options.rpy:56
    old "## To allow the user to play a test sound on the sound or voice channel, uncomment a line below and use it to set a sample sound to play."
    new "## 사용자가 음향 또는 음성 채널에서 테스트 사운드를 재생할 수 있게 하려면 아래 줄의 주석을 제거하고 이를 사용하여 재생할 샘플 사운드를 설정하십시오."

    # options.rpy:63
    old "## Uncomment the following line to set an audio file that will be played while the player is at the main menu. This file will continue playing into the game, until it is stopped or another file is played."
    new "## 플레이어가 주 메뉴에 있을 때 재생할 오디오 파일을 설정하려면 다음 줄의 주석 처리를 제거하십시오. 이 파일은 중지되거나 다른 파일이 재생 될 때까지 계속 재생합니다."

    # options.rpy:70
    old "## Transitions"
    new "## 번역"

    # options.rpy:72
    old "## These variables set transitions that are used when certain events occur. Each variable should be set to a transition, or None to indicate that no transition should be used."
    new "## 이러한 변수는 특정 이벤트가 발생할 때 사용되는 전환을 설정합니다. 각 변수는 전환으로 설정해야 하며, 전환을 사용하지 말아야 한다는 것을 나타내려면 None으로 설정해야 합니다."

    # options.rpy:76
    old "## Entering or exiting the game menu."
    new "## 게임 메뉴에 진입하거나 나갑니다."

    # options.rpy:82
    old "## Between screens of the game menu."
    new "## 게임 메뉴 화면 사이입니다."

    # options.rpy:87
    old "## A transition that is used after a game has been loaded."
    new "## 게임이 로드된 후 사용되는 전환입니다."

    # options.rpy:92
    old "## Used when entering the main menu after the game has ended."
    new "## 게임 종료 후 주 메뉴에 진입할 때 사용됩니다."

    # options.rpy:97
    old "## A variable to set the transition used when the game starts does not exist. Instead, use a with statement after showing the initial scene."
    new "## 게임을 시작할 때 사용되는 전환을 설정하는 변수가 없습니다. 대신, 초기 장면을 표시한 후 with 문을 사용하십시오."

    # options.rpy:102
    old "## Window management"
    new "## 창 관리"

    # options.rpy:104
    old "## This controls when the dialogue window is displayed. If \"show\", it is always displayed. If \"hide\", it is only displayed when dialogue is present. If \"auto\", the window is hidden before scene statements and shown again once dialogue is displayed."
    new "## 이것은 대사 창이 표시됐을 때 제어합니다. 만약 \"show\"면, 그것은 상항 표시됩니다. 만약 \"hide\"면, 그것은 대사가 주어질 때만 표시됩니다. 만약 \"auto\"면, 창은 장면(scene) 문 앞에 숨겨져 대화 상자가 표시되면 다시 표시됩니다."

    # options.rpy:109
    old "## After the game has started, this can be changed with the \"window show\", \"window hide\", and \"window auto\" statements."
    new "## 게임이 시작된 후에는 \"window show\", \"window hide\", 그리고 \"window auto\" 문을 사용하여 변경할 수 있습니다."

    # options.rpy:115
    old "## Transitions used to show and hide the dialogue window"
    new "## 대화 창을 표시하고 숨기는 데 사용되는 전환"

    # options.rpy:121
    old "## Preference defaults"
    new "## 환경설정 기본값"

    # options.rpy:123
    old "## Controls the default text speed. The default, 0, is infinite, while any other number is the number of characters per second to type out."
    new "## 기본 글자 속도를 제어합니다. 기본적으로, 0은 즉시이며 다른 숫자는 초당 입력 할 문자 수입니다."

    # options.rpy:129
    old "## The default auto-forward delay. Larger numbers lead to longer waits, with 0 to 30 being the valid range."
    new "## 기본 auto-forward 지연 시간입니다. 숫자가 클수록 대기 시간이 길어지며, 0 ~ 30이 유효한 범위가 됩니다."

    # options.rpy:135
    old "## Save directory"
    new "## 세이브 디렉토리"

    # options.rpy:137
    old "## Controls the platform-specific place Ren'Py will place the save files for this game. The save files will be placed in:"
    new "## 렌파이는 이 게임에 대한 저장 파일을 플랫폼 별로 배치합니다. 세이브 파일들은 여기에 있습니다:"

    # options.rpy:140
    old "## Windows: %APPDATA\\RenPy\\<config.save_directory>"
    new "## 윈도우즈: %APPDATA\\RenPy\\<config.save_directory>"

    # options.rpy:142
    old "## Macintosh: $HOME/Library/RenPy/<config.save_directory>"
    new "## 매킨토시: $HOME/Library/RenPy/<config.save_directory>"

    # options.rpy:144
    old "## Linux: $HOME/.renpy/<config.save_directory>"
    new "## 리눅스: $HOME/.renpy/<config.save_directory>"

    # options.rpy:146
    old "## This generally should not be changed, and if it is, should always be a literal string, not an expression."
    new "## 이것은 일반적으로 변경해서는 안 되며, 항상 표현형식이 아닌 정확한 문자열이어야 합니다."

    # options.rpy:152
    old "## Icon ########################################################################'"
    new "## 아이콘 #######################################################################'"

    # options.rpy:154
    old "## The icon displayed on the taskbar or dock."
    new "## 작업 표시 줄 또는 독에 표시되는 아이콘."

    # options.rpy:159
    old "## Build configuration"
    new "## 빌드 구성"

    # options.rpy:161
    old "## This section controls how Ren'Py turns your project into distribution files."
    new "## 이 섹션은 렌파이가 프로젝트를 배포 파일로 만드는 방법을 제어합니다."

    # options.rpy:166
    old "## The following functions take file patterns. File patterns are case- insensitive, and matched against the path relative to the base directory, with and without a leading /. If multiple patterns match, the first is used."
    new "## 다음 함수는 파일 패턴을 사용합니다. 파일 패턴은 대/소문자를 구분하지 않으며, /의 유무와 관계없이 기본 디렉터리의 상대 경로와 일치합니다. 여러 패턴이 일치하면 첫 번째 패턴이 사용됩니다."

    # options.rpy:171
    old "## In a pattern:"
    new "## 패턴 있음:"

    # options.rpy:173
    old "## / is the directory separator."
    new "## / 는 디렉토리 구분 기호입니다."

    # options.rpy:175
    old "## * matches all characters, except the directory separator."
    new "## * 는 디렉토리 구분자를 제외한 모든 문자와 일치합니다."

    # options.rpy:177
    old "## ** matches all characters, including the directory separator."
    new "## ** 는 디렉토리 구분자를 포함해 모든 문자와 일치합니다."

    # options.rpy:179
    old "## For example, \"*.txt\" matches txt files in the base directory, \"game/**.ogg\" matches ogg files in the game directory or any of its subdirectories, and \"**.psd\" matches psd files anywhere in the project."
    new "## 예를 들어, \"*.txt\" 는 기본 디렉토리의 txt 파일들과 일치하고, \"game/**.ogg\" 는 게임 디렉토리 또는 그 서브 디렉토리의 ogg 파일들과 일치하며, \"**.psd\" 는 프로젝트에서 모든 곳의 psd 파일들과 일치합니다."

    # options.rpy:183
    old "## Classify files as None to exclude them from the built distributions."
    new "## 파일을 None으로 분류하여 배포판으로부터 제외하십시오."

    # options.rpy:191
    old "## To archive files, classify them as 'archive'."
    new "## 파일을 아카이브하려면 'archive'로 분류하십시오."

    # options.rpy:196
    old "## Files matching documentation patterns are duplicated in a mac app build, so they appear in both the app and the zip file."
    new "## 파일들의 매칭 문서 패턴은 맥앱(Mac App) 빌드에서 중복되므로 app 및 zip 파일에 모두 나타납니다."

    # options.rpy:202
    old "## Set this to a string containing your Apple Developer ID Application to enable codesigning on the Mac. Be sure to change it to your own Apple-issued ID."
    new "## 맥(Mac)에서 코드 서명을 사용하려면 Apple Developer ID Application이 포함된 문자열로 설정하십시오. 애플(Apple)에서 발행한 ID로 변경하십시오."

    # options.rpy:209
    old "## A Google Play license key is required to download expansion files and perform in-app purchases. It can be found on the \"Services & APIs\" page of the Google Play developer console."
    new "## 확장 파일을 다운로드하고 인앱 구매를 수행하려면 Google Play 라이센스 키가 필요합니다. Google Play 개발자 콘솔의 \"서비스 및 API\"페이지에서 확인할 수 있습니다."

    # options.rpy:216
    old "## The username and project name associated with an itch.io project, separated by a slash."
    new "## itch.io 프로젝트와 연관된 사용자 이름과 프로젝트 이름이며 슬래시로 구분됩니다."
