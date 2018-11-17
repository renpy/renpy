translate korean strings:

    # screens.rpy:9
    old "## Styles"
    new "## 스타일"

    # screens.rpy:81
    old "## In-game screens"
    new "## 게임내 스크린"

    # screens.rpy:85
    old "## Say screen"
    new "## Say 스크린"

    # screens.rpy:87
    old "## The say screen is used to display dialogue to the player. It takes two parameters, who and what, which are the name of the speaking character and the text to be displayed, respectively. (The who parameter can be None if no name is given.)"
    new "## Say 스크린은 플레이어에게 대사를 출력할 때 씁니다. 화자 who와 대사 what, 두 개의 매개변수를 받습니다. (화자 이름이 없으면 who는 None일 수 있음)"

    # screens.rpy:92
    old "## This screen must create a text displayable with id \"what\", as Ren'Py uses this to manage text display. It can also create displayables with id \"who\" and id \"window\" to apply style properties."
    new "## 이 스크린은 id \"what\"을 가진 텍스트 디스플레이어블을 생성해야 합니다. (이 디스플레이어블은 렌파이의 대사 출력에 필요합니다.) id \"who\" 와 id \"window\" 디스플레이블이 존재할 경우 관련 스타일 속성이 적용됩니다."

    # screens.rpy:96
    old "## https://www.renpy.org/doc/html/screen_special.html#say"
    new "## https://www.renpy.org/doc/html/screen_special.html#say"

    # screens.rpy:114
    old "## If there's a side image, display it above the text. Do not display on the phone variant - there's no room."
    new "## 사이드 이미지가 있는 경우 글자 위에 표시합니다. 휴대폰 환경에서는 보이지 않습니다."

     # screens.rpy:120
    old "## Make the namebox available for styling through the Character object."
    new "## Character 객체를 통해 스타일을 지정할 수 있도록 namebox를 사용할 수 있게 만듭니다."

    # screens.rpy:164
    old "## Input screen"
    new "## Input 스크린"

    # screens.rpy:166
    old "## This screen is used to display renpy.input. The prompt parameter is used to pass a text prompt in."
    new "## 플레이어 입력을 받는 renpy.input을 출력할 때 쓰이는 스크린입니다. prompt 매개변수를 통해 입력 지문을 표시할 수 있습니다."

    # screens.rpy:169
    old "## This screen must create an input displayable with id \"input\" to accept the various input parameters."
    new "## 이 스크린은 id \"input\"을 가진 input 디스플레이어블을 생성해야 합니다."

    # screens.rpy:172
    old "## https://www.renpy.org/doc/html/screen_special.html#input"
    new "## https://www.renpy.org/doc/html/screen_special.html#input"

    # screens.rpy:199
    old "## Choice screen"
    new "## Choice 스크린"

    # screens.rpy:201
    old "## This screen is used to display the in-game choices presented by the menu statement. The one parameter, items, is a list of objects, each with caption and action fields."
    new "## menu 명령어로 생성된 게임내 선택지를 출력하는 스크린입니다. 한 개의 매개변수 items를 받고, 이는 선택지 내용(caption)과 선택지 결과(action)이 있는 오브젝트가 들어있는 리스트입니다."

    # screens.rpy:205
    old "## https://www.renpy.org/doc/html/screen_special.html#choice"
    new "## https://www.renpy.org/doc/html/screen_special.html#choice"

    # screens.rpy:215
    old "## When this is true, menu captions will be spoken by the narrator. When false, menu captions will be displayed as empty buttons."
    new "## True일 경우 narrator 캐릭터를 통해 지문을 표시합니다. False일 경우 지문이 비활성화 선택지로 표시됩니다."

    # screens.rpy:238
    old "## Quick Menu screen"
    new "## Quick Menu 스크린"

    # screens.rpy:240
    old "## The quick menu is displayed in-game to provide easy access to the out-of-game menus."
    new "## 퀵메뉴는 게임 외 메뉴 접근성을 높여주기 위해 게임 내에 표시됩니다."

    # screens.rpy:256
    old "Back"
    new "되감기"

    # screens.rpy:257
    old "History"
    new "대사록"

    # screens.rpy:258
    old "Skip"
    new "넘기기"

    # screens.rpy:259
    old "Auto"
    new "자동진행"

    # screens.rpy:260
    old "Save"
    new "저장하기"

    # screens.rpy:261
    old "Q.Save"
    new "Q.저장하기"

    # screens.rpy:262
    old "Q.Load"
    new "Q.불러오기"

    # screens.rpy:263
    old "Prefs"
    new "설정"

    # screens.rpy:266
    old "## This code ensures that the quick_menu screen is displayed in-game, whenever the player has not explicitly hidden the interface."
    new "## 플레이어가 UI(스크린)을 일부러 숨기지 않는 한 퀵메뉴가 게임 내에 오버레이로 출력되게 합니다."

    # screens.rpy:284
    old "## Main and Game Menu Screens"
    new "## Main과 Game Menu 스크린"

    # screens.rpy:287
    old "## Navigation screen"
    new "## Navigation 스크린"

    # screens.rpy:289
    old "## This screen is included in the main and game menus, and provides navigation to other menus, and to start the game."
    new "## 이 스크린은 메인메뉴와 게임외 메뉴에 포함되어 다른 메뉴로 이동하거나 게임을 시작/종료할 수 있게 합니다."

    # screens.rpy:304
    old "Start"
    new "시작하기"

    # screens.rpy:312
    old "Load"
    new "불러오기"

    # screens.rpy:314
    old "Preferences"
    new "환경설정"

    # screens.rpy:318
    old "End Replay"
    new "리플레이 끝내기"

    # screens.rpy:322
    old "Main Menu"
    new "메인 메뉴"

    # screens.rpy:324
    old "About"
    new "버전정보"

    # screens.rpy:328
    old "## Help isn't necessary or relevant to mobile devices."
    new "## 도움말 메뉴는 모바일 디바이스와 맞지 않아 불필요합니다."

    # screens.rpy:329
    old "Help"
    new "조작방법"

    # screens.rpy:331
    old "## The quit button is banned on iOS and unnecessary on Android."
    new "## 종료 버튼은 iOS 규정에 어긋나고 안드로이드에는 불필요합니다."

    # screens.rpy:332
    old "Quit"
    new "종료하기"

    # screens.rpy:346
    old "## Main Menu screen"
    new "## Main Menu 스크린"

    # screens.rpy:348
    old "## Used to display the main menu when Ren'Py starts."
    new "## 렌파이가 시작할 때 메인메뉴를 출력합니다."

    # screens.rpy:354
    old "## https://www.renpy.org/doc/html/screen_special.html#main-menu"
    new "## https://www.renpy.org/doc/html/screen_special.html#main-menu"

    # screens.rpy:365
    old "## The use statement includes another screen inside this one. The actual contents of the main menu are in the navigation screen."
    new "## use 명령어로 스크린 내에 다른 스크린을 불러옵니다. 메인 메뉴 스크린의 내용물은 navigation 스크린에 있습니다."

    # screens.rpy:408
    old "## Game Menu screen"
    new "## Game Menu 스크린"

    # screens.rpy:410
    old "## This lays out the basic common structure of a game menu screen. It's called with the screen title, and displays the background, title, and navigation."
    new "## 게임 메뉴의 기본 틀입니다. 매개변수 title로 스크린 제목을 정하고, 배경, 제목, 그리고 navigation 스크린을 출력합니다."

    # screens.rpy:413
    old "## The scroll parameter can be None, or one of \"viewport\" or \"vpgrid\". When this screen is intended to be used with one or more children, which are transcluded (placed) inside it."
    new "## scroll 매개변수는, None, \"viewport\" 혹은 \"vpgrid\" 중 하나여야 합니다. transclude 명령어를 통해 다른 스크린을 이 스크린 내부에 불러옵니다."

    # screens.rpy:473
    old "Return"
    new "돌아가기"

    # screens.rpy:536
    old "## About screen"
    new "## About 스크린"

    # screens.rpy:538
    old "## This screen gives credit and copyright information about the game and Ren'Py."
    new "## 이 스크린은 게임과 렌파이 엔진 크레딧과 저작권 정보를 표시합니다."

    # screens.rpy:541
    old "## There's nothing special about this screen, and hence it also serves as an example of how to make a custom screen."
    new "## 특별할 것이 없으므로 스크린을 새로 커스터마이징하여 만드는 예제이기도 합니다."

    # screens.rpy:548
    old "## This use statement includes the game_menu screen inside this one. The vbox child is then included inside the viewport inside the game_menu screen."
    new "## 이 use 명령어로 game_menu 스크린을 이 스크린 내에 불러옵니다. use 명령어 하위블럭(vbox 내용)은 game_menu 스크린 내 transclude 명령어가 있는 곳에 다시 불려집니다."

    # screens.rpy:558
    old "Version [config.version!t]\n"
    new "버젼 [config.version!t]\n"

    # screens.rpy:560
    old "## gui.about is usually set in options.rpy."
    new "## gui.about 의 내용은 보통 options.rpy에 있습니다."

    # screens.rpy:564
    old "Made with {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only].\n\n[renpy.license!t]"
    new "{a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only] 으로 만들어진 게임.\n\n[renpy.license!t]"

    # screens.rpy:577
    old "## This is redefined in options.rpy to add text to the about screen."
    new "## options.rpy에서 규정된 내용이 about 스크린에 추가됩니다."

    # screens.rpy:579
    old "## Load and Save screens"
    new "## Load 그리고 Save 스크린"

    # screens.rpy:581
    old "## These screens are responsible for letting the player save the game and load it again. Since they share nearly everything in common, both are implemented in terms of a third screen, file_slots."
    new "## 이 스크린은 세이브/로드에 쓰입니다. 거의 동일하기 때문에, file_slots 스크린을 불러와서 씁니다."

    # screens.rpy:585
    old "## https://www.renpy.org/doc/html/screen_special.html#save https://www.renpy.org/doc/html/screen_special.html#load"
    new "## https://www.renpy.org/doc/html/screen_special.html#save https://www.renpy.org/doc/html/screen_special.html#load"

    # screens.rpy:604
    old "Page {}"
    new "{} 페이지"

    # screens.rpy:604
    old "Automatic saves"
    new "자동 세이브"

    # screens.rpy:604
    old "Quick saves"
    new "퀵세이브"

    # screens.rpy:610
    old "## This ensures the input will get the enter event before any of the buttons do."
    new "## input이 세이브/로드 버튼보다 먼저 엔터에 반응하도록 합니다."

    # screens.rpy:614
    old "## The page name, which can be edited by clicking on a button."
    new "## 페이지 제목을 플레이어가 수정할 수 있음."

    # screens.rpy:626
    old "## The grid of file slots."
    new "## 파일 슬롯 그리드."

    # screens.rpy:646
    old "{#file_time}%A, %B %d %Y, %H:%M"
    new "{#file_time}%A, %B %d %Y, %H:%M"

    # screens.rpy:646
    old "empty slot"
    new "빈 슬롯"

    # screens.rpy:654
    old "## Buttons to access other pages."
    new "## 페이지 이동 버튼."

    # screens.rpy:663
    old "<"
    new "<"

    # screens.rpy:666
    old "{#auto_page}A"
    new "{#auto_page}자동"

    # screens.rpy:669
    old "{#quick_page}Q"
    new "{#quick_page}퀵"

    # screens.rpy:671
    old "## range(1, 10) gives the numbers from 1 to 9."
    new "## 범위(1, 10)는 1부터 9까지 숫자를 제공합니다."

    # screens.rpy:675
    old ">"
    new ">"

    # screens.rpy:710
    old "## Preferences screen"
    new "## Preferences 스크린"

    # screens.rpy:712
    old "## The preferences screen allows the player to configure the game to better suit themselves."
    new "## Preferences 스크린에서는 각종 환경설정을 플레이어가 지정할 수 있습니다."

    # screens.rpy:715
    old "## https://www.renpy.org/doc/html/screen_special.html#preferences"
    new "## https://www.renpy.org/doc/html/screen_special.html#preferences"

    # screens.rpy:732
    old "Display"
    new "화면 모드"

    # screens.rpy:733
    old "Window"
    new "창 화면"

    # screens.rpy:734
    old "Fullscreen"
    new "전체 화면"

    # screens.rpy:738
    old "Rollback Side"
    new "측면 되감기"

    # screens.rpy:739
    old "Disable"
    new "비활성화"

    # screens.rpy:740
    old "Left"
    new "화면 왼쪽 클릭"

    # screens.rpy:741
    old "Right"
    new "화면 오른쪽 클릭"

    # screens.rpy:746
    old "Unseen Text"
    new "읽지 않은 지문"

    # screens.rpy:747
    old "After Choices"
    new "선택지 이후"

    # screens.rpy:748
    old "Transitions"
    new "화면 전환 효과"

    # screens.rpy:750
    old "## Additional vboxes of type \"radio_pref\" or \"check_pref\" can be added here, to add additional creator-defined preferences."
    new "## \"radio_pref\" 나 \"check_pref\" 를 추가하여 그 외에도 환경설정 항목을 추가할 수 있습니다."

    # screens.rpy:761
    old "Text Speed"
    new "텍스트 속도"

    # screens.rpy:765
    old "Auto-Forward Time"
    new "자동 진행 시간"

    # screens.rpy:772
    old "Music Volume"
    new "배경음 음량"

    # screens.rpy:779
    old "Sound Volume"
    new "효과음 음량"

    # screens.rpy:785
    old "Test"
    new "테스트"

    # screens.rpy:789
    old "Voice Volume"
    new "음성 음량"

    # screens.rpy:800
    old "Mute All"
    new "모두 음소거"

    # screens.rpy:876
    old "## History screen"
    new "## History 스크린"

    # screens.rpy:878
    old "## This is a screen that displays the dialogue history to the player. While there isn't anything special about this screen, it does have to access the dialogue history stored in _history_list."
    new "## 지난 대사록을 출력합니다. _history_list 에 저장된 대사 기록을 확인합니다."

    # screens.rpy:882
    old "## https://www.renpy.org/doc/html/history.html"
    new "## https://www.renpy.org/doc/html/history.html"

    # screens.rpy:888
    old "## Avoid predicting this screen, as it can be very large."
    new "## 이 스크린은 내용이 아주 많을 수 있으므로 prediction을 끕니다."

    # screens.rpy:899
    old "## This lays things out properly if history_height is None."
    new "## history_height 이 None일 경우 레이아웃이 틀어지지 않게 합니다."

    # screens.rpy:909
    old "## Take the color of the who text from the Character, if set."
    new "## 화자 Character에 화자 색깔이 지정되어 있으면 불러옵니다."

    # screens.rpy:918
    old "The dialogue history is empty."
    new "대사가 없습니다."

    # screens.rpy:921
    old "## This determines what tags are allowed to be displayed on the history screen."
    new "## 이것은 대사록 화면에 표시할 수 있는 태그를 결정합니다."

    # screens.rpy:968
    old "## Help screen"
    new "## Help 스크린"

    # screens.rpy:970
    old "## A screen that gives information about key and mouse bindings. It uses other screens (keyboard_help, mouse_help, and gamepad_help) to display the actual help."
    new "## 입력장치의 기능을 설명합니다. 각 입력장치별 설정은 keyboard_help, mouse_help, gamepad_help 스크린을 각각 불러와서 출력합니다."

    # screens.rpy:989
    old "Keyboard"
    new "키보드"

    # screens.rpy:990
    old "Mouse"
    new "마우스"

    # screens.rpy:993
    old "Gamepad"
    new "게임패드"

    # screens.rpy:1006
    old "Enter"
    new "엔터(Enter)"

    # screens.rpy:1007
    old "Advances dialogue and activates the interface."
    new "대사 진행 및 UI (선택지 포함) 선택."

    # screens.rpy:1010
    old "Space"
    new "스페이스(Space)"

    # screens.rpy:1011
    old "Advances dialogue without selecting choices."
    new "대사를 진행하되 선택지는 선택하지 않음."

    # screens.rpy:1014
    old "Arrow Keys"
    new "화살표 키"

    # screens.rpy:1015
    old "Navigate the interface."
    new "UI 이동."

    # screens.rpy:1018
    old "Escape"
    new "이스케이프(Esc)"

    # screens.rpy:1019
    old "Accesses the game menu."
    new "게임 메뉴 불러옴."

    # screens.rpy:1022
    old "Ctrl"
    new "컨트롤(Ctrl)"

    # screens.rpy:1023
    old "Skips dialogue while held down."
    new "누르고 있는 동안 대사를 스킵."

    # screens.rpy:1026
    old "Tab"
    new "탭(Tab)"

    # screens.rpy:1027
    old "Toggles dialogue skipping."
    new "대사 스킵 토글."

    # screens.rpy:1030
    old "Page Up"
    new "페이지 업(Page Up)"

    # screens.rpy:1031
    old "Rolls back to earlier dialogue."
    new "이전 대사로 롤백."

    # screens.rpy:1034
    old "Page Down"
    new "페이지 다운(Page Down)"

    # screens.rpy:1035
    old "Rolls forward to later dialogue."
    new "이후 대사로 롤포워드."

    # screens.rpy:1039
    old "Hides the user interface."
    new "UI를 숨김."

    # screens.rpy:1043
    old "Takes a screenshot."
    new "스크린샷 저장."

    # screens.rpy:1047
    old "Toggles assistive {a=https://www.renpy.org/l/voicing}self-voicing{/a}."
    new "{a=https://www.renpy.org/l/voicing}대사 읽어주기 기능{/a} 토글."

    # screens.rpy:1056
    old "Left Click"
    new "클릭"

    # screens.rpy:1057
    old "Middle Click"
    new "가운데 버튼이나 휠버튼 클릭"

    # screens.rpy:1061
    old "Right Click"
    new "우클릭"

    # screens.rpy:1065
    old "Mouse Wheel Up\nClick Rollback Side"
    new "휠 위로\n롤백 클릭"

    # screens.rpy:1069
    old "Mouse Wheel Down"
    new "휠 아래로"

    # screens.rpy:1076
    old "Right Trigger\nA/Bottom Button"
    new "오른쪽 트리거(RT)\nA버튼/아래 버튼"

    # screens.rpy:1084
    old "Right Shoulder"
    new "오른쪽 범퍼(RB)"

    # screens.rpy:1085
    old "D-Pad, Sticks"
    new "D-Pad, 아날로그 스틱"

    # screens.rpy:1093
    old "Start, Guide"
    new "스타트 버튼/가이드 버튼"

    # screens.rpy:1097
    old "Y/Top Button"
    new "Y버튼/위 버튼"

    # screens.rpy:1100
    old "Calibrate"
    new "조정"

    # screens.rpy:1128
    old "## Additional screens"
    new "## 그 외 스크린"

    # screens.rpy:1132
    old "## Confirm screen"
    new "## Confirm 스크린"

    # screens.rpy:1134
    old "## The confirm screen is called when Ren'Py wants to ask the player a yes or no question."
    new "## 게임 입력 관련 예/아니오 질문을 플레이어에게 할 때 이 스크린을 표시합니다."

    # screens.rpy:1137
    old "## https://www.renpy.org/doc/html/screen_special.html#confirm"
    new "## https://www.renpy.org/doc/html/screen_special.html#confirm"

    # screens.rpy:1141
    old "## Ensure other screens do not get input while this screen is displayed."
    new "## 이 스크린이 출력 중일 때 다른 스크린과 상호작용할 수 없게 합니다."

    # screens.rpy:1165
    old "Yes"
    new "네"

    # screens.rpy:1166
    old "No"
    new "아니오"

    # screens.rpy:1168
    old "## Right-click and escape answer \"no\"."
    new "## 우클릭과 esc는 '아니오'를 입력하는 것과 같습니다."

    # screens.rpy:1195
    old "## Skip indicator screen"
    new "## Skip indicator 스크린"

    # screens.rpy:1197
    old "## The skip_indicator screen is displayed to indicate that skipping is in progress."
    new "## Skip_indicator 스크린은 스킵 중일 때 \"스킵 중\"을 표시하기 위해 출력됩니다."

    # screens.rpy:1200
    old "## https://www.renpy.org/doc/html/screen_special.html#skip-indicator"
    new "## https://www.renpy.org/doc/html/screen_special.html#skip-indicator"

    # screens.rpy:1212
    old "Skipping"
    new "넘기는 중"

    # screens.rpy:1219
    old "## This transform is used to blink the arrows one after another."
    new "## 이 transform으로 화살표를 순서대로 페이드인/페이드아웃합니다."

    # screens.rpy:1246
    old "## We have to use a font that has the BLACK RIGHT-POINTING SMALL TRIANGLE glyph in it."
    new "## BLACK RIGHT-POINTING SMALL TRIANGLE 글리프가 있는 글꼴을 사용해야 합니다."

    # screens.rpy:1251
    old "## Notify screen"
    new "## Notify 스크린"

    # screens.rpy:1253
    old "## The notify screen is used to show the player a message. (For example, when the game is quicksaved or a screenshot has been taken.)"
    new "## Notify 스크린으로 플레이어에게 메시지를 출력합니다. (예를 들어 '퀵세이브 완료'나 '스크린샷 저장 완료')"

    # screens.rpy:1256
    old "## https://www.renpy.org/doc/html/screen_special.html#notify-screen"
    new "## https://www.renpy.org/doc/html/screen_special.html#notify-screen"

    # screens.rpy:1290
    old "## NVL screen"
    new "## NVL 스크린"

    # screens.rpy:1292
    old "## This screen is used for NVL-mode dialogue and menus."
    new "## NVL모드 대사와 선택지를 출력합니다."

    # screens.rpy:1294
    old "## https://www.renpy.org/doc/html/screen_special.html#nvl"
    new "## https://www.renpy.org/doc/html/screen_special.html#nvl"

    # screens.rpy:1305
    old "## Displays dialogue in either a vpgrid or the vbox."
    new "## vpgrid나 vbox 내에 대사를 출력합니다."

    # screens.rpy:1318
    old "## Displays the menu, if given. The menu may be displayed incorrectly if config.narrator_menu is set to True, as it is above."
    new "## 선택지가 있을 경우, 선택지 출력. config.narrator_menu가 True일 경우 선택지가 비정상적으로 출력될 수 있습니다. (디폴트는 True입니다.)"

    # screens.rpy:1348
    old "## This controls the maximum number of NVL-mode entries that can be displayed at once."
    new "## 동시에 출력될 수 있는 NVL 대사의 최대치를 조정합니다."

    # screens.rpy:1410
    old "## Mobile Variants"
    new "## 모바일 버전"

    # screens.rpy:1417
    old "## Since a mouse may not be present, we replace the quick menu with a version that uses fewer and bigger buttons that are easier to touch."
    new "## 마우스가 없고 화면이 작을 가능성이 높으므로, 퀵메뉴 버튼의 크기를 키우고 가짓수를 줄입니다."

    # screens.rpy:1433
    old "Menu"
    new "메뉴"
