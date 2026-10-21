
translate tchinese strings:

    # screens.rpy:9
    old "## Styles"
    new "## 樣式"

    # screens.rpy:87
    old "## In-game screens"
    new "## 遊戲內畫面"

    # screens.rpy:91
    old "## Say screen"
    new "## say 畫面"

    # screens.rpy:93
    old "## The say screen is used to display dialogue to the player. It takes two parameters, who and what, which are the name of the speaking character and the text to be displayed, respectively. (The who parameter can be None if no name is given.)"
    new "## say 畫面用於向玩家顯示對話。它接受 who 和 what 兩個參數，分別代表說話角色的名稱與要顯示的文字。（沒有名稱時，who 可以是 None。）"

    # screens.rpy:98
    old "## This screen must create a text displayable with id \"what\", as Ren'Py uses this to manage text display. It can also create displayables with id \"who\" and id \"window\" to apply style properties."
    new "## 此畫面必須建立 id 為 \"what\" 的文字可顯示物，讓 Ren'Py 管理文字顯示。也可以建立 id 為 \"who\" 和 \"window\" 的可顯示物，以套用樣式屬性。"

    # screens.rpy:169
    old "## Input screen"
    new "## 輸入畫面"

    # screens.rpy:171
    old "## This screen is used to display renpy.input. The prompt parameter is used to pass a text prompt in."
    new "## 此畫面用於顯示 renpy.input。prompt 參數用來傳入文字提示。"

    # screens.rpy:174
    old "## This screen must create an input displayable with id \"input\" to accept the various input parameters."
    new "## 此畫面必須建立 id 為 \"input\" 的輸入可顯示物，以接受各種輸入參數。"

    # screens.rpy:205
    old "## Choice screen"
    new "## 選擇畫面"

    # screens.rpy:207
    old "## This screen is used to display the in-game choices presented by the menu statement. The one parameter, items, is a list of objects, each with caption and action fields."
    new "## 此畫面用於顯示 menu 語句提供的遊戲內選項。唯一的參數 items 是物件清單，每個物件都有 caption 和 action 欄位。"

    # screens.rpy:221
    old "## When this is true, menu captions will be spoken by the narrator. When false, menu captions will be displayed as empty buttons."
    new "## 若此值為 true，旁白會讀出選單文字；若為 false，選單文字會顯示為空按鈕。"

    # screens.rpy:244
    old "## Quick Menu screen"
    new "## 快捷選單畫面"

    # screens.rpy:246
    old "## The quick menu is displayed in-game to provide easy access to the out-of-game menus."
    new "## 快速選單會顯示在遊戲內，方便存取遊戲外的選單。"

    # screens.rpy:261
    old "Back"
    new "返回"

    # screens.rpy:262
    old "History"
    new "歷史"

    # screens.rpy:263
    old "Skip"
    new "跳過"

    # screens.rpy:264
    old "Auto"
    new "自動"

    # screens.rpy:265
    old "Save"
    new "儲存"

    # screens.rpy:266
    old "Q.Save"
    new "快速儲存"

    # screens.rpy:267
    old "Q.Load"
    new "快速載入"

    # screens.rpy:268
    old "Prefs"
    new "設定"

    # screens.rpy:271
    old "## This code ensures that the quick_menu screen is displayed in-game, whenever the player has not explicitly hidden the interface."
    new "## 只要玩家沒有明確隱藏介面，此程式碼就會確保 quick_menu 畫面顯示在遊戲內。"

    # screens.rpy:291
    old "## Navigation screen"
    new "## 導覽畫面"

    # screens.rpy:293
    old "## This screen is included in the main and game menus, and provides navigation to other menus, and to start the game."
    new "## 此畫面會包含在主選單與遊戲選單中，提供前往其他選單及開始遊戲的導覽。"

    # screens.rpy:308
    old "Start"
    new "開始"

    # screens.rpy:316
    old "Load"
    new "載入"

    # screens.rpy:318
    old "Preferences"
    new "設定"

    # screens.rpy:322
    old "End Replay"
    new "結束回放"

    # screens.rpy:326
    old "Main Menu"
    new "主選單"

    # screens.rpy:328
    old "About"
    new "關於"

    # screens.rpy:332
    old "## Help isn't necessary or relevant to mobile devices."
    new "## 對行動裝置而言，說明既不必要也不適用。"

    # screens.rpy:333
    old "Help"
    new "說明"

    # screens.rpy:335
    old "## The quit button is banned on iOS and unnecessary on Android."
    new "## iOS 禁用離開按鈕，Android 上則不需要此按鈕。"

    # screens.rpy:336
    old "Quit"
    new "離開"

    # screens.rpy:350
    old "## Main Menu screen"
    new "## 主選單畫面"

    # screens.rpy:352
    old "## Used to display the main menu when Ren'Py starts."
    new "## 用於在 Ren'Py 啟動時顯示主選單。"

    # screens.rpy:369
    old "## The use statement includes another screen inside this one. The actual contents of the main menu are in the navigation screen."
    new "## use 語句在該畫面中包含另一個畫面。主選單的實際內容在導覽畫面中。"

    # screens.rpy:413
    old "## Game Menu screen"
    new "## 遊戲選單畫面"

    # screens.rpy:415
    old "## This lays out the basic common structure of a game menu screen. It's called with the screen title, and displays the background, title, and navigation."
    new "## 這會配置遊戲選單畫面的基本結構。呼叫時傳入畫面標題，並顯示背景、標題與導覽。"

    # screens.rpy:418
    old "## The scroll parameter can be None, or one of \"viewport\" or \"vpgrid\". This screen is intended to be used with one or more children, which are transcluded (placed) inside it."
    new "## scroll 參數可以是 None、\"viewport\" 或 \"vpgrid\"。此畫面供一個或多個子項目使用，子項目會嵌入其中。"

    # screens.rpy:476
    old "Return"
    new "返回"

    # screens.rpy:539
    old "## About screen"
    new "## 關於畫面"

    # screens.rpy:541
    old "## This screen gives credit and copyright information about the game and Ren'Py."
    new "## 此畫面提供遊戲與 Ren'Py 的致謝及版權資訊。"

    # screens.rpy:544
    old "## There's nothing special about this screen, and hence it also serves as an example of how to make a custom screen."
    new "## 此畫面沒有特殊功能，也可作為建立自訂畫面的範例。"

    # screens.rpy:551
    old "## This use statement includes the game_menu screen inside this one. The vbox child is then included inside the viewport inside the game_menu screen."
    new "## 此 use 語句會將 game_menu 畫面包含在本畫面中，vbox 子項目則會包含在 game_menu 畫面的 viewport 內。"

    # screens.rpy:561
    old "Version [config.version!t]\n"
    new "版本 [config.version!t]\n"

    # screens.rpy:563
    old "## gui.about is usually set in options.rpy."
    new "## gui.about 通常在 options.rpy 中設定。"

    # screens.rpy:567
    old "Made with {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only].\n\n[renpy.license!t]"
    new "使用 {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only] 製作。 \n\n[renpy.license!t]"

    # screens.rpy:570
    old "## This is redefined in options.rpy to add text to the about screen."
    new "## 這是在 options.rpy 中重新定義，以將文字新增至關於畫面。"

    # screens.rpy:582
    old "## Load and Save screens"
    new "## 載入和儲存畫面"

    # screens.rpy:584
    old "## These screens are responsible for letting the player save the game and load it again. Since they share nearly everything in common, both are implemented in terms of a third screen, file_slots."
    new "## 這些畫面讓玩家儲存並載入遊戲。由於兩者大致相同，因此都透過第三個畫面 file_slots 實作。"

    # screens.rpy:607
    old "Page {}"
    new "頁面 {}"

    # screens.rpy:607
    old "Automatic saves"
    new "自動儲存"

    # screens.rpy:607
    old "Quick saves"
    new "快速儲存"

    # screens.rpy:613
    old "## This ensures the input will get the enter event before any of the buttons do."
    new "## 這確保輸入將在任何按鈕之前獲得輸入事件。"

    # screens.rpy:629
    old "## The grid of file slots."
    new "## 存檔槽的網格。"

    # screens.rpy:649
    old "{#file_time}%A, %B %d %Y, %H:%M"
    new "{#file_time}%A, %B %d %Y, %H:%M"

    # screens.rpy:649
    old "empty slot"
    new "空白存檔欄位"

    # screens.rpy:657
    old "## Buttons to access other pages."
    new "## 存取其他頁面的按鈕。"

    # screens.rpy:666
    old "<"
    new "<"

    # screens.rpy:668
    old "{#auto_page}A"
    new "{#auto_page}A"

    # screens.rpy:670
    old "{#quick_page}Q"
    new "{#quick_page}Q"

    # screens.rpy:676
    old ">"
    new ">"

    # screens.rpy:711
    old "## Preferences screen"
    new "## 首選項畫面"

    # screens.rpy:713
    old "## The preferences screen allows the player to configure the game to better suit themselves."
    new "## 偏好設定畫面讓玩家調整遊戲以符合自己的需求。"

    # screens.rpy:738
    old "Display"
    new "顯示"

    # screens.rpy:739
    old "Window"
    new "視窗"

    # screens.rpy:740
    old "Fullscreen"
    new "全螢幕"

    # screens.rpy:744
    old "Rollback Side"
    new "回退側"

    # screens.rpy:745
    old "Disable"
    new "停用"

    # screens.rpy:746
    old "Left"
    new "左"

    # screens.rpy:747
    old "Right"
    new "右"

    # screens.rpy:752
    old "Unseen Text"
    new "未讀文字"

    # screens.rpy:753
    old "After Choices"
    new "選項後"

    # screens.rpy:754
    old "Transitions"
    new "過渡"

    # screens.rpy:756
    old "## Additional vboxes of type \"radio_pref\" or \"check_pref\" can be added here, to add additional creator-defined preferences."
    new "## 可以在此處新增 \"radio_pref\" 或 \"check_pref\" 類型的其他 vbox，以新增其他建立者定義的首選項。"

    # screens.rpy:767
    old "Text Speed"
    new "文字顯示速度"

    # screens.rpy:771
    old "Auto-Forward Time"
    new "自動前進時間"

    # screens.rpy:778
    old "Music Volume"
    new "音樂音量"

    # screens.rpy:785
    old "Sound Volume"
    new "音效音量"

    # screens.rpy:791
    old "Test"
    new "測試"

    # screens.rpy:795
    old "Voice Volume"
    new "語音音量"

    # screens.rpy:806
    old "Mute All"
    new "全部靜音"

    # screens.rpy:882
    old "## History screen"
    new "## 歷史畫面"

    # screens.rpy:884
    old "## This is a screen that displays the dialogue history to the player. While there isn't anything special about this screen, it does have to access the dialogue history stored in _history_list."
    new "## 此畫面向玩家顯示對話歷史。它沒有特殊功能，但必須存取儲存在 _history_list 中的對話歷史。"

    # screens.rpy:894
    old "## Avoid predicting this screen, as it can be very large."
    new "## 避免預測此畫面，因為它可能非常大。"

    # screens.rpy:905
    old "## This lays things out properly if history_height is None."
    new "## history_height 為 None 時，這會正確排列內容。"

    # screens.rpy:914
    old "## Take the color of the who text from the Character, if set."
    new "## 從角色中取得 who 文字的顏色（如果已設定）。"

    # screens.rpy:921
    old "The dialogue history is empty."
    new "對話歷史記錄為空。"

    # screens.rpy:965
    old "## Help screen"
    new "## 幫助畫面"

    # screens.rpy:967
    old "## A screen that gives information about key and mouse bindings. It uses other screens (keyboard_help, mouse_help, and gamepad_help) to display the actual help."
    new "## 此畫面提供按鍵與滑鼠綁定資訊，並使用 keyboard_help、mouse_help 和 gamepad_help 畫面顯示詳細說明。"

    # screens.rpy:986
    old "Keyboard"
    new "鍵盤"

    # screens.rpy:987
    old "Mouse"
    new "滑鼠"

    # screens.rpy:990
    old "Gamepad"
    new "遊戲手柄"

    # screens.rpy:1003
    old "Enter"
    new "Enter"

    # screens.rpy:1004
    old "Advances dialogue and activates the interface."
    new "推進對話並啟用介面。"

    # screens.rpy:1007
    old "Space"
    new "空白鍵"

    # screens.rpy:1008
    old "Advances dialogue without selecting choices."
    new "無需選擇即可推進對話。"

    # screens.rpy:1011
    old "Arrow Keys"
    new "方向鍵"

    # screens.rpy:1012
    old "Navigate the interface."
    new "導覽介面。"

    # screens.rpy:1015
    old "Escape"
    new "Escape"

    # screens.rpy:1016
    old "Accesses the game menu."
    new "存取遊戲選單。"

    # screens.rpy:1019
    old "Ctrl"
    new "Ctrl"

    # screens.rpy:1020
    old "Skips dialogue while held down."
    new "按住時跳過對話。"

    # screens.rpy:1023
    old "Tab"
    new "Tab"

    # screens.rpy:1024
    old "Toggles dialogue skipping."
    new "切換對話跳過。"

    # screens.rpy:1027
    old "Page Up"
    new "上翻頁鍵"

    # screens.rpy:1028
    old "Rolls back to earlier dialogue."
    new "回退到較早的對話。"

    # screens.rpy:1031
    old "Page Down"
    new "下翻頁鍵"

    # screens.rpy:1032
    old "Rolls forward to later dialogue."
    new "前進到較晚的對話。"

    # screens.rpy:1036
    old "Hides the user interface."
    new "隱藏使用者介面。"

    # screens.rpy:1040
    old "Takes a screenshot."
    new "截取螢幕截圖。"

    # screens.rpy:1044
    old "Toggles assistive {a=https://www.renpy.org/l/voicing}self-voicing{/a}."
    new "切換輔助{a=https://www.renpy.org/l/voicing}自動朗讀{/a}。"

    # screens.rpy:1050
    old "Left Click"
    new "左鍵"

    # screens.rpy:1054
    old "Middle Click"
    new "中鍵"

    # screens.rpy:1058
    old "Right Click"
    new "右鍵"

    # screens.rpy:1062
    old "Mouse Wheel Up"
    new "滑鼠滾輪向上"

    # screens.rpy:1066
    old "Mouse Wheel Down"
    new "滑鼠滾輪向下"

    # screens.rpy:1073
    old "Right Trigger\nA/Bottom Button"
    new "右扳機鍵\nA／底部按鈕"

    # screens.rpy:1074
    old "Advance dialogue and activates the interface."
    new "推進對話並啟動介面。"

    # screens.rpy:1078
    old "Roll back to earlier dialogue."
    new "回滾到之前的對話。"

    # screens.rpy:1081
    old "Right Shoulder"
    new "右肩鍵"

    # screens.rpy:1082
    old "Roll forward to later dialogue."
    new "前進到稍後的對話。"

    # screens.rpy:1085
    old "D-Pad, Sticks"
    new "十字鍵，搖桿"

    # screens.rpy:1089
    old "Start, Guide"
    new "開始，向導"

    # screens.rpy:1090
    old "Access the game menu."
    new "存取遊戲選單。"

    # screens.rpy:1093
    old "Y/Top Button"
    new "Y/頂鍵"

    # screens.rpy:1096
    old "Calibrate"
    new "校準"

    # screens.rpy:1124
    old "## Additional screens"
    new "## 附加畫面"

    # screens.rpy:1128
    old "## Confirm screen"
    new "## 確認畫面"

    # screens.rpy:1130
    old "## The confirm screen is called when Ren'Py wants to ask the player a yes or no question."
    new "## Ren'Py 要詢問玩家是非問題時，會呼叫確認畫面。"

    # screens.rpy:1137
    old "## Ensure other screens do not get input while this screen is displayed."
    new "## 確保顯示此畫面時其他畫面不會收到輸入。"

    # screens.rpy:1161
    old "Yes"
    new "是"

    # screens.rpy:1162
    old "No"
    new "否"

    # screens.rpy:1164
    old "## Right-click and escape answer \"no\"."
    new "## 右鍵點選或按 Escape 會回答 \"no\"。"

    # screens.rpy:1191
    old "## Skip indicator screen"
    new "## 跳過提示畫面"

    # screens.rpy:1193
    old "## The skip_indicator screen is displayed to indicate that skipping is in progress."
    new "## skip_indicator 畫面會在跳過進行時顯示提示。"

    # screens.rpy:1208
    old "Skipping"
    new "跳過中"

    # screens.rpy:1215
    old "## This transform is used to blink the arrows one after another."
    new "## 此變換用於使箭頭依序閃爍。"

    # screens.rpy:1247
    old "## Notify screen"
    new "## 通知畫面"

    # screens.rpy:1249
    old "## The notify screen is used to show the player a message. (For example, when the game is quicksaved or a screenshot has been taken.)"
    new "## 通知畫面用於向玩家顯示訊息（例如快速儲存遊戲或擷取螢幕截圖時）。"

    # screens.rpy:1286
    old "## NVL screen"
    new "## NVL 畫面"

    # screens.rpy:1288
    old "## This screen is used for NVL-mode dialogue and menus."
    new "## 此畫面用於 NVL 模式對話和選單。"

    # screens.rpy:1301
    old "## Displays dialogue in either a vpgrid or the vbox."
    new "## 在 vpgrid 或 vbox 中顯示對話。"

    # screens.rpy:1314
    old "## Displays the menu, if given. The menu may be displayed incorrectly if config.narrator_menu is set to True, as it is above."
    new "## 顯示選單（如果有）。 如果 config.narrator_menu 設定為 True ，選單可能會顯示不正確，如上所示。"

    # screens.rpy:1344
    old "## This controls the maximum number of NVL-mode entries that can be displayed at once."
    new "## 這會控制一次最多顯示多少個 NVL 模式項目。"

    # screens.rpy:1406
    old "## Mobile Variants"
    new "## 行動裝置變體"

    # screens.rpy:1413
    old "## Since a mouse may not be present, we replace the quick menu with a version that uses fewer and bigger buttons that are easier to touch."
    new "## 行動裝置可能沒有滑鼠，因此將快速選單替換為按鈕較少、較大且更容易觸控的版本。"

    # screens.rpy:1429
    old "Menu"
    new "選單"

    # gui/game/screens.rpy:114
    old "## If there's a side image, display it above the text. Do not display on the phone variant - there's no room."
    new "## 如果有側面影像，請將其顯示在文字上方。不要顯示在手機版本上 - 沒有空間。"

    # gui/game/screens.rpy:120
    old "## Make the namebox available for styling through the Character object."
    new "## 使名稱框可用於透過角色物件進行樣式設定。"

    # gui/game/screens.rpy:241
    old "## Ensure this appears on top of other screens."
    new "## 確保它出現在其他螢幕的頂端。"

    # gui/game/screens.rpy:280
    old "## Main and Game Menu Screens"
    new "## 主選單和遊戲選單畫面"

    # gui/game/screens.rpy:329
    old "## The quit button is banned on iOS and unnecessary on Android and Web."
    new "## 結束按鈕在 iOS 上被禁止，在 Android 和 Web 上則不必要。"

    # gui/game/screens.rpy:352
    old "## This ensures that any other menu screen is replaced."
    new "## 這可確保替換任何其他選單畫面。"

    # gui/game/screens.rpy:357
    old "## This empty frame darkens the main menu."
    new "## 這個空框使主選單變暗。"

    # gui/game/screens.rpy:429
    old "## Reserve space for the navigation section."
    new "## 為導覽部分保留空間。"

    # gui/game/screens.rpy:612
    old "## The page name, which can be edited by clicking on a button."
    new "## 頁面名稱，可以透過點選按鈕進行編輯。"

    # gui/game/screens.rpy:672
    old "## range(1, 10) gives the numbers from 1 to 9."
    new "## range(1, 10) 給出從 1 到 9 的數字。"

    # gui/game/screens.rpy:680
    old "Upload Sync"
    new "上傳同步"

    # gui/game/screens.rpy:684
    old "Download Sync"
    new "下載同步"

    # gui/game/screens.rpy:925
    old "## This determines what tags are allowed to be displayed on the history screen."
    new "## 這決定了允許在歷史螢幕上顯示哪些標籤。"

    # gui/game/screens.rpy:1053
    old "Opens the accessibility menu."
    new "開啟輔助功能選單。"

    # gui/game/screens.rpy:1086
    old "Left Trigger\nLeft Shoulder"
    new "左扳機 \n 左肩鍵"

    # gui/game/screens.rpy:1098
    old "Start, Guide, B/Right Button"
    new "開始、Guide、B／右側按鈕"

    # gui/game/screens.rpy:1251
    old "## We have to use a font that has the BLACK RIGHT-POINTING SMALL TRIANGLE glyph in it."
    new "## 我們必須使用帶有黑色右指小三角形字形的字型。"

    # gui/game/screens.rpy:1323
    old "## Displays the menu, if given. The menu may be displayed incorrectly if config.narrator_menu is set to True."
    new "## 顯示選單（如果給定）。如果 config.narrator_menu 設定為 True，則選單可能無法正確顯示。"

    # gui/game/screens.rpy:1413
    old "## Bubble screen"
    new "## 氣泡畫面"

    # gui/game/screens.rpy:1415
    old "## The bubble screen is used to display dialogue to the player when using speech bubbles. The bubble screen takes the same parameters as the say screen, must create a displayable with the id of \"what\", and can create displayables with the \"namebox\", \"who\", and \"window\" ids."
    new "## 使用對話氣泡時，bubble 畫面會向玩家顯示對話。它接受與 say 畫面相同的參數，必須建立 id 為 \"what\" 的可顯示物，也可以建立 id 為 \"namebox\"、\"who\" 和 \"window\" 的可顯示物。"

    # gui/game/screens.rpy:96
    old "## https://www.renpy.org/doc/html/screen_special.html#say"
    new "## https://www.renpy.org/doc/html/screen_special.html#say"

    # gui/game/screens.rpy:173
    old "## https://www.renpy.org/doc/html/screen_special.html#input"
    new "## https://www.renpy.org/doc/html/screen_special.html#input"

    # gui/game/screens.rpy:206
    old "## https://www.renpy.org/doc/html/screen_special.html#choice"
    new "## https://www.renpy.org/doc/html/screen_special.html#choice"

    # gui/game/screens.rpy:348
    old "## https://www.renpy.org/doc/html/screen_special.html#main-menu"
    new "## https://www.renpy.org/doc/html/screen_special.html#main-menu"

    # gui/game/screens.rpy:583
    old "## https://www.renpy.org/doc/html/screen_special.html#save https://www.renpy.org/doc/html/screen_special.html#load"
    new "## https://www.renpy.org/doc/html/screen_special.html#save https://www.renpy.org/doc/html/screen_special.html#load"

    # gui/game/screens.rpy:726
    old "## https://www.renpy.org/doc/html/screen_special.html#preferences"
    new "## https://www.renpy.org/doc/html/screen_special.html#preferences"

    # gui/game/screens.rpy:886
    old "## https://www.renpy.org/doc/html/history.html"
    new "## https://www.renpy.org/doc/html/history.html"

    # gui/game/screens.rpy:1142
    old "## https://www.renpy.org/doc/html/screen_special.html#confirm"
    new "## https://www.renpy.org/doc/html/screen_special.html#confirm"

    # gui/game/screens.rpy:1205
    old "## https://www.renpy.org/doc/html/screen_special.html#skip-indicator"
    new "## https://www.renpy.org/doc/html/screen_special.html#skip-indicator"

    # gui/game/screens.rpy:1261
    old "## https://www.renpy.org/doc/html/screen_special.html#notify-screen"
    new "## https://www.renpy.org/doc/html/screen_special.html#notify-screen"

    # gui/game/screens.rpy:1299
    old "## https://www.renpy.org/doc/html/screen_special.html#nvl"
    new "## https://www.renpy.org/doc/html/screen_special.html#nvl"

    # gui/game/screens.rpy:1420
    old "## https://www.renpy.org/doc/html/bubble.html#bubble-screen"
    new "## https://www.renpy.org/doc/html/bubble.html#bubble-screen"

