﻿
translate korean strings:

    # screens.rpy:9
    old "## Styles"
    new "## 스타일"

    # screens.rpy:87
    old "## In-game screens"
    new "## 게임내 스크린"

    # screens.rpy:91
    old "## Say screen"
    new "## Say 스크린"

    # screens.rpy:93
    old "## The say screen is used to display dialogue to the player. It takes two parameters, who and what, which are the name of the speaking character and the text to be displayed, respectively. (The who parameter can be None if no name is given.)"
    new "## Say 스크린은 플레이어에게 대사를 출력할 때 씁니다. 화자 who와 대사 what, 두 개의 매개변수를 받습니다. (화자 이름이 없으면 who는 None일 수 있음)"

    # screens.rpy:98
    old "## This screen must create a text displayable with id \"what\", as Ren'Py uses this to manage text display. 
    It can also create displayables with id \"who\" and id \"window\" to apply style properties."
    new "## 이 스크린은 id \"what\"을 가진 텍스트 디스플레이어블을 생성해야 합니다. (이 디스플레이어블은 렌파이의 대사 출력에 필요합니다.) id \"who\" 와 id \"window\" 디스플레이블이 존재할 경우 관련 스타일 속성이 적용됩니다."

    # screens.rpy:102
    old "## https://www.renpy.org/doc/html/screen_special.html#say"
    new "## https://www.renpy.org/doc/html/screen_special.html#say"

    # screens.rpy:169
    old "## Input screen"
    new "## Input 스크린"

    # screens.rpy:171
    old "## This screen is used to display renpy.input. The prompt parameter is used to pass a text prompt in."
    new "## 플레이어 입력을 받는 renpy.input을 출력할 때 쓰이는 스크린입니다. prompt 매개변수를 통해 입력 지문을 표시할 수 있습니다."
    
    # screens.rpy:174
    old "## This screen must create an input displayable with id \"input\" to accept the various input parameters."
    new "## 이 스크린은 id \"input\"을 가진 input 디스플레이어블을 생성해야 합니다."

    # screens.rpy:177
    old "## http://www.renpy.org/doc/html/screen_special.html#input"
    new "## http://www.renpy.org/doc/html/screen_special.html#input"

    # screens.rpy:205
    old "## Choice screen"
    new "## Choice 스크린"

    # screens.rpy:207
    old "## This screen is used to display the in-game choices presented by the menu statement. The one parameter, items, is a list of objects, each with caption and action fields."
    new "## menu 명령어로 생성된 게임내 선택지를 출력하는 스크린입니다. 한 개의 매개변수 items를 받고, 이는 선택지 내용(caption)과 선택지 결과(action)이 있는 오브젝트가 들어있는 리스트입니다."

    # screens.rpy:211
    old "## http://www.renpy.org/doc/html/screen_special.html#choice"
    new "## http://www.renpy.org/doc/html/screen_special.html#choice"

    # screens.rpy:221
    old "## When this is true, menu captions will be spoken by the narrator. When false, menu captions will be displayed as empty buttons."
    new "## True일 경우 narrator 캐릭터를 통해 지문을 표시합니다. False일 경우 지문이 비활성화 선택지로 표시됩니다."

    # screens.rpy:244
    old "## Quick Menu screen"
    new "## Quick Menu 스크린"

    # screens.rpy:246
    old "## The quick menu is displayed in-game to provide easy access to the out-of-game menus."
    new "## 퀵메뉴는 게임 외 메뉴 접근성을 높여주기 위해 게임 내에 표시됩니다."

    # screens.rpy:261
    old "Back"
    new "뒤로"

    # screens.rpy:262
    old "History"
    new "History"

    # screens.rpy:263
    old "Skip"
    new "스킵"

    # screens.rpy:264
    old "Auto"
    new "자동진행"

    # screens.rpy:265
    old "Save"
    new "저장하기"

    # screens.rpy:266
    old "Q.Save"
    new "퀵세이브"

    # screens.rpy:267
    old "Q.Load"
    new "퀵로드"

    # screens.rpy:268
    old "Prefs"
    new "설정"

    # screens.rpy:271
    old "## This code ensures that the quick_menu screen is displayed in-game, whenever the player has not explicitly hidden the interface."
    new "## 플레이어가 UI(스크린)을 일부러 숨기지 않는 한 퀵메뉴가 게임 내에 오버레이로 출력되게 합니다."

    # screens.rpy:291
    old "## Navigation screen"
    new "## Navigation 스크린"

    # screens.rpy:293
    old "## This screen is included in the main and game menus, and provides navigation to other menus, and to start the game."
    new "## 이 스크린은 메인메뉴와 게임외 메뉴에 포함되어 다른 메뉴로 이동하거나 게임을 시작/종료할 수 있게 합니다."

    # screens.rpy:308
    old "Start"
    new "시작하기"

    # screens.rpy:316
    old "Load"
    new "로드"

    # screens.rpy:318
    old "Preferences"
    new "환경 설정"

    # screens.rpy:322
    old "End Replay"
    new "리플레이 기"기

    # screens.rpy:326
    old "Main Menu"
    new "메인 메뉴"

    # screens.rpy:328
    old "About"
    new "렌파이란"

    # screens.rpy:332
    old "## Help isn't necessary or relevant to mobile devices."
    new "## 도움말 메뉴는 모바일 디바이스와 맞지 않아 불필요합니다."

    # screens.rpy:333
    old "Help"
    new "도움말"

    # screens.rpy:335
    old "## The quit button is banned on iOS and unnecessary on Android."
    new "## 종료 버튼은 iOS 규정에 어긋나고 안드로이드에는 불필요합니다."

    # screens.rpy:336
    old "Quit"
    new "끝내기"

    # screens.rpy:350
    old "## Main Menu screen"
    new "## Main Menu 스크린"

    # screens.rpy:352
    old "## Used to display the main menu when Ren'Py starts."
    new "## 렌파이가 시작할 때 메인메뉴를 출력합니다."

    # screens.rpy:354
    old "## http://www.renpy.org/doc/html/screen_special.html#main-menu"
    new "## http://www.renpy.org/doc/html/screen_special.html#main-menu"

    # screens.rpy:369
    old "## The use statement includes another screen inside this one. The actual contents of the main menu are in the navigation screen."
    new "## use 명령어로 스크린 내에 다른 스크린을 불러옵니다. 메인 메뉴 스크린의 내용물은 navigation 스크린에 있습니다."

    # screens.rpy:413
    old "## Game Menu screen"
    new "## Game Menu 스크린"

    # screens.rpy:415
    old "## This lays out the basic common structure of a game menu screen. It's called with the screen title, and displays the background, title, and navigation."
    new "## 게임 메뉴의 기본 틀입니다. 매개변수 title로 스크린 제목을 정하고, 배경, 제목, 그리고 navigation 스크린을 출력합니다."

    # screens.rpy:418
    old "## The scroll parameter can be None, or one of \"viewport\" or \"vpgrid\". When this screen is intended to be used with one or more children, which are transcluded (placed) inside it."
    new "## scroll 매개변수는, None, \"viewport\" 혹은 \"vpgrid\" 중 하나여야 합니다. transclude 명령어를 통해 다른 스크린을 이 스크린 내부에 불러옵니다."

    # screens.rpy:476
    old "Return"
    new "돌아가기"

    # screens.rpy:539
    old "## About screen"
    new "## About 스크린"

    # screens.rpy:541
    old "## This screen gives credit and copyright information about the game and Ren'Py."
    new "## 이 스크린은 게임과 렌파이 엔진 크레딧과 저작권 정보를 표시합니다."

    # screens.rpy:544
    old "## There's nothing special about this screen, and hence it also serves as an example of how to make a custom screen."
    new "## 특별할 것이 없으므로 스크린을 새로 커스터마이징하여 만드는 예제이기도 합니다."

    # screens.rpy:551
    old "## This use statement includes the game_menu screen inside this one. The vbox child is then included inside the viewport inside the game_menu screen."
    new "## 이 use 명령어로 game_menu 스크린을 이 스크린 내에 불러옵니다. use 명령어 하위블럭(vbox 내용)은 game_menu 스크린 내 transclude 명령어가 있는 곳에 다시 불려집니다."

# screens.rpy:561
    old "Version [config.version!t]\n"
    new "버젼 [config.version!t]\n"

    # screens.rpy:563
    old "## gui.about is usually set in options.rpy."
    new "## gui.about 의 내용은 보통 options.rpy에 있습니다."

    # screens.rpy:567
    old "Made with {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only].\n\n[renpy.license!t]"
    new "{a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only] 으로 만들어진 게임.\n\n[renpy.license!t]"

    # screens.rpy:570
    old "## This is redefined in options.rpy to add text to the about screen."
    new "## options.rpy에서 규정된 내용이 about 스크린에 추가됩니다."

    # screens.rpy:582
    old "## Load and Save screens"
    new "## Load and Save 스크린"

    # screens.rpy:584
    old "## These screens are responsible for letting the player save the game and load it again. Since they share nearly everything in common, both are implemented in terms of a third screen, file_slots."
    new "## 이 스크린은 세이브/로드에 쓰입니다. 거의 동일하기 때문에, file_slots 스크린을 불러와서 씁니다."

    # screens.rpy:588
    old "## https://www.renpy.org/doc/html/screen_special.html#save https://www.renpy.org/doc/html/screen_special.html#load"
    new "## https://www.renpy.org/doc/html/screen_special.html#save https://www.renpy.org/doc/html/screen_special.html#load"

    # screens.rpy:607
    old "Page {}"
    new "{} 페이지"

    # screens.rpy:607
    old "Automatic saves"
    new "자동 세이브"

    # screens.rpy:607
    old "Quick saves"
    new "퀵세이브"

    # screens.rpy:613
    old "## This ensures the input will get the enter event before any of the buttons do."
    new "## input (페이지 제목을 플레이어가 수정할 수 있음)이 세이브/로드 버튼보다 먼저 엔터에 반응하도록 합니다."

    # screens.rpy:629
    old "## The grid of file slots."
    new "## 파일 슬롯 그리드."

    # screens.rpy:649
    old "{#file_time}%A, %B %d %Y, %H:%M"
    new "{#file_time}%A, %B %d %Y, %H:%M"

    # screens.rpy:649
    old "empty slot"
    new "빈 슬롯"

    # screens.rpy:657
    old "## Buttons to access other pages."
    new "## 페이지 이동 버튼."

    # screens.rpy:666
    old "<"
    new "<"

    # screens.rpy:668
    old "{#auto_page}A"
    new "{#auto_page}자동"

    # screens.rpy:670
    old "{#quick_page}Q"
    new "{#quick_page}퀵"

    # screens.rpy:676
    old ">"
    new ">"

    # screens.rpy:711
    old "## Preferences screen"
    new "## Preferences screen"

    # screens.rpy:713
    old "## The preferences screen allows the player to configure the game to better suit themselves."
    new "## Preferences 스크린에서는 각종 환경설정을 플레이어가 지정할 수 있습니다."

    # screens.rpy:716
    old "## https://www.renpy.org/doc/html/screen_special.html#preferences"
    new "## https://www.renpy.org/doc/html/screen_special.html#preferences"

    # screens.rpy:738
    old "Display"
    new "화면 모드"

    # screens.rpy:739
    old "Window"
    new "창 모드"

    # screens.rpy:740
    old "Fullscreen"
    new "전체 화면 모드"

    # screens.rpy:744
    old "Rollback Side"
    new "롤백 클릭 옵션"

    # screens.rpy:745
    old "Disable"
    new "비활성화"

    # screens.rpy:746
    old "Left"
    new "화면 왼쪽 클릭"

    # screens.rpy:747
    old "Right"
    new "화면 오른쪽 클릭"

    # screens.rpy:752
    old "Unseen Text"
    new "읽지 않은 텍스트까지 모두 스킵"

    # screens.rpy:753
    old "After Choices"
    new "선택지 이후에도 스킵"

    # screens.rpy:754
    old "Transitions"
    new "화면 전환 효과를 모두 스킵"

    # screens.rpy:756
    old "## Additional vboxes of type \"radio_pref\" or \"check_pref\" can be added here, to add additional creator-defined preferences."
    new "## \"radio_pref\" 나 \"check_pref\" 를 추가하여 그 외에도 환경설정 항목을 추가할 수 있습니다."

    # screens.rpy:767
    old "Text Speed"
    new "텍스트 속도"

    # screens.rpy:771
    old "Auto-Forward Time"
    new "자동 진행 시간"

    # screens.rpy:778
    old "Music Volume"
    new "배경음악 크기"

    # screens.rpy:785
    old "Sound Volume"
    new "효과음 크기"

    # screens.rpy:791
    old "Test"
    new "테스트"

    # screens.rpy:795
    old "Voice Volume"
    new "음성 크기"

    # screens.rpy:806
    old "Mute All"
    new "모두 음소거"

    # screens.rpy:882
    old "## History screen"
    new "## History 스크린"

    # screens.rpy:884
    old "## This is a screen that displays the dialogue history to the player. While there isn't anything special about this screen, it does have to access the dialogue history stored in _history_list."
    new "## 지난 대사록을 출력합니다. _history_list 에 저장된 대사 기록을 확인합니다."

    # screens.rpy:888
    old "## https://www.renpy.org/doc/html/history.html"
    new "## https://www.renpy.org/doc/html/history.html"

    # screens.rpy:894
    old "## Avoid predicting this screen, as it can be very large."
    new "## 이 스크린은 내용이 아주 많을 수 있으므로 prediction을 끕니다."

    # screens.rpy:905
    old "## This lays things out properly if history_height is None."
    new "## history_height 이 None일 경우 레이아웃이 틀어지지 않게 합니다."

    # screens.rpy:914
    old "## Take the color of the who text from the Character, if set."
    new "## 화자 Character에 화자 색깔이 지정되어 있으면 불러옵니다."

    # screens.rpy:921
    old "The dialogue history is empty."
    new "대사가 없습니다."

    # screens.rpy:965
    old "## Help screen"
    new "## Help 스크린"

    # screens.rpy:967
    old "## A screen that gives information about key and mouse bindings. It uses other screens (keyboard_help, mouse_help, and gamepad_help) to display the actual help."
    new "## 입력장치의 기능을 설명합니다. 각 입력장치별 설정은 keyboard_help, mouse_help, gamepad_help 스크린을 각각 불러와서 출력합니다."

    # screens.rpy:986
    old "Keyboard"
    new "키보드"

    # screens.rpy:987
    old "Mouse"
    new "마우스"

    # screens.rpy:990
    old "Gamepad"
    new "게임패드"

    # screens.rpy:1003
    old "Enter"
    new "Enter"

    # screens.rpy:1004
    old "Advances dialogue and activates the interface."
    new "대사 진행 및 UI (선택지 포함) 선택."

    # screens.rpy:1007
    old "Space"
    new "Space"

    # screens.rpy:1008
    old "Advances dialogue without selecting choices."
    new "대사를 진행하되 선택지는 선택하지 않음."

    # screens.rpy:1011
    old "Arrow Keys"
    new "화살표 키"

    # screens.rpy:1012
    old "Navigate the interface."
    new "UI 이동."

    # screens.rpy:1015
    old "Escape"
    new "Esc"

    # screens.rpy:1016
    old "Accesses the game menu."
    new "게임 메뉴 불러옴."

    # screens.rpy:1019
    old "Ctrl"
    new "Ctrl"

    # screens.rpy:1020
    old "Skips dialogue while held down."
    new "누르고 있는 동안 대사를 스킵."

    # screens.rpy:1023
    old "Tab"
    new "Tab"

    # screens.rpy:1024
    old "Toggles dialogue skipping."
    new "대사 스킵 토글."

    # screens.rpy:1027
    old "Page Up"
    new "Page Up"

    # screens.rpy:1028
    old "Rolls back to earlier dialogue."
    new "이전 대사로 롤백."

    # screens.rpy:1031
    old "Page Down"
    new "Page Down"

    # screens.rpy:1032
    old "Rolls forward to later dialogue."
    new "이후 대사로 롤포워드."

    # screens.rpy:1036
    old "Hides the user interface."
    new "UI를 숨김."

    # screens.rpy:1040
    old "Takes a screenshot."
    new "스크린샷 저장."

    # screens.rpy:1044
    old "Toggles assistive {a=https://www.renpy.org/l/voicing}self-voicing{/a}."
    new "{a=https://www.renpy.org/l/voicing}대사 읽어주기 기능{/a} 토글."

    # screens.rpy:1050
    old "Left Click"
    new "클릭"

    # screens.rpy:1054
    old "Middle Click"
    new "가운데버튼이나 휠버튼 클릭"

    # screens.rpy:1058
    old "Right Click"
    new "우클릭"

    # screens.rpy:1062
    old "Mouse Wheel Up\nClick Rollback Side"
    new "휠 위로\n롤백 클릭"

    # screens.rpy:1066
    old "Mouse Wheel Down"
    new "휠 아래로"

    # screens.rpy:1073
    old "Right Trigger\nA/Bottom Button"
    new "오른쪽 트리거(RT)\nA버튼/아래 버튼"

    # screens.rpy:1074
    old "Advance dialogue and activates the interface."
    new "대사 진행 및 UI (선택지 포함) 선택."

    # screens.rpy:1078
    old "Roll back to earlier dialogue."
    new "이전 대사로 롤백."

    # screens.rpy:1081
    old "Right Shoulder"
    new "오른쪽 범퍼(RB)"

    # screens.rpy:1082
    old "Roll forward to later dialogue."
    new "이후 대사로 롤포워드."

    # screens.rpy:1085
    old "D-Pad, Sticks"
    new "D-Pad, 아날로그 스틱"

    # screens.rpy:1089
    old "Start, Guide"
    new "스타스 버튼/가이드 버튼"

    # screens.rpy:1090
    old "Access the game menu."
    new "게임 메뉴 불러옴."

    # screens.rpy:1093
    old "Y/Top Button"
    new "Y버튼/위 버튼"

    # screens.rpy:1096
    old "Calibrate"
    new "조정"

    # screens.rpy:1124
    old "## Additional screens"
    new "## 그 외 스크린"

    # screens.rpy:1128
    old "## Confirm screen"
    new "## Confirm 스크린"

    # screens.rpy:1130
    old "## The confirm screen is called when Ren'Py wants to ask the player a yes or no question."
    new "## 게임 입력 관련 예/아니오 질문을 플레이어에게 할 때 이 스크린을 표시합니다."

    # screens.rpy:1133
    old "## http://www.renpy.org/doc/html/screen_special.html#confirm"
    new "## http://www.renpy.org/doc/html/screen_special.html#confirm"

    # screens.rpy:1137
    old "## Ensure other screens do not get input while this screen is displayed."
    new "## 이 스크린이 출력 중일 때 다른 스크린과 상호작용할 수 없게 합니다."

    # screens.rpy:1161
    old "Yes"
    new "네"

    # screens.rpy:1162
    old "No"
    new "아니오"

    # screens.rpy:1164
    old "## Right-click and escape answer \"no\"."
    new "## 우클릭과 esc는 '아니오'를 입력하는 것과 같습니다."

    # screens.rpy:1191
    old "## Skip indicator screen"
    new "## Skip indicator 스크린"

    # screens.rpy:1193
    old "## The skip_indicator screen is displayed to indicate that skipping is in progress."
    new "## Skip_indicator 스크린은 스킵 중일 때 "스킵 중"을 표시하기 위해 출력됩니다."

    # screens.rpy:1196
    old "## https://www.renpy.org/doc/html/screen_special.html#skip-indicator"
    new "## https://www.renpy.org/doc/html/screen_special.html#skip-indicator"

    # screens.rpy:1208
    old "Skipping"
    new "스킵 중"

    # screens.rpy:1215
    old "## This transform is used to blink the arrows one after another."
    new "## 이 transform으로 화살표를 순서대로 페이드인/페이드아웃합니다."

    # screens.rpy:1247
    old "## Notify screen"
    new "## Notify 스크린"

    # screens.rpy:1249
    old "## The notify screen is used to show the player a message. (For example, when the game is quicksaved or a screenshot has been taken.)"
    new "## Notify 스크린으로 플레이어에게 메시지를 출력합니다. (예를 들어 '퀵세이브 완료'나 '스크린샷 저장 완료')"

    # screens.rpy:1252
    old "## https://www.renpy.org/doc/html/screen_special.html#notify-screen"
    new "## https://www.renpy.org/doc/html/screen_special.html#notify-screen"

    # screens.rpy:1286
    old "## NVL screen"
    new "## NVL 스크린"

    # screens.rpy:1288
    old "## This screen is used for NVL-mode dialogue and menus."
    new "## NVL모드 대사와 선택지를 출력합니다."

    # screens.rpy:1290
    old "## http://www.renpy.org/doc/html/screen_special.html#nvl"
    new "## http://www.renpy.org/doc/html/screen_special.html#nvl"

    # screens.rpy:1301
    old "## Displays dialogue in either a vpgrid or the vbox."
    new "## vpgrid나 vbox 내에 대사를 출력합니다."

    # screens.rpy:1314
    old "## Displays the menu, if given. The menu may be displayed incorrectly if config.narrator_menu is set to True, as it is above."
    new "## 선택지가 있을 경우, 선택지 출력. config.narrator_menu가 True일 경우 선택지가 비정상적으로 출력될 수 있습니다. (디폴트는 True입니다.)"

    # screens.rpy:1344
    old "## This controls the maximum number of NVL-mode entries that can be displayed at once."
    new "## 동시에 출력될 수 있는 NVL 대사의 최대치를 조정합니다."

    # screens.rpy:1406
    old "## Mobile Variants"
    new "## 모바일 버젼"

    # screens.rpy:1413
    old "## Since a mouse may not be present, we replace the quick menu with a version that uses fewer and bigger buttons that are easier to touch."
    new "## 마우스가 없고 화면이 작을 가능성이 높으므로, 퀵메뉴 버튼의 크기를 키우고 가짓수를 줄입니다."

    # screens.rpy:1429
    old "Menu"
    new "메뉴"

