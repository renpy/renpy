
translate japanese strings:

    # screens.rpy:9
    old "## Styles"
    new "## スタイル"

    # screens.rpy:87
    old "## In-game screens"
    new "## ゲーム内のスクリーン"

    # screens.rpy:91
    old "## Say screen"
    new "## Say（発話）スクリーン"

    # screens.rpy:93
    old "## The say screen is used to display dialogue to the player. It takes two parameters, who and what, which are the name of the speaking character and the text to be displayed, respectively. (The who parameter can be None if no name is given.)"
    new "## Say スクリーンはプレイヤーにダイアローグ（台詞）を表示するのに使います。who、what の二つのパラメーターをとり、who は発話しているキャラクターの名前、what は表示されるテキストを意味します。（キャラクターの名前がない場合 who は None になります）"

    # screens.rpy:98
    old "## This screen must create a text displayable with id \"what\", as Ren'Py uses this to manage text display. It can also create displayables with id \"who\" and id \"window\" to apply style properties."
    new "## このスクリーンは、テキストを表示するために \"what\" のＩＤを持つ text displayable を必ず作成しなければなりません。また、スタイルのプロパティを適用するために、ＩＤ \"who\" とＩＤ \"window\" を持つ text displayable も作成するといいでしょう。"

    # screens.rpy:102
    old "## https://www.renpy.org/doc/html/screen_special.html#say"
    new "## https://ja.renpy.org/doc/html/screen_special.html#say"

    # screens.rpy:119
    old "## If there's a side image, display it above the text. Do not display on the phone variant - there's no room."
    new "## サイドイメージ（テキストボックス横に表示するイメージ）があれば、テキストの上に表示します。ただし variant（画面のタイプ）が phone の場合は、スペースが足りないので表示しません。"

    # screens.rpy:169
    old "## Input screen"
    new "## Input（入力）スクリーン"

    # screens.rpy:171
    old "## This screen is used to display renpy.input. The prompt parameter is used to pass a text prompt in."
    new "## renpy.input を表示するのに使うスクリーンです。prompt のパラメーターは、プロンプト（入力ボックスの隣に表示されるテキスト）を表示するのに使います。"

    # screens.rpy:174
    old "## This screen must create an input displayable with id \"input\" to accept the various input parameters."
    new "## このスクリーンは input のパラメーター を受け付けるために \"input\" をＩＤに持つ input displayable を作成する必要があります。"

    # screens.rpy:177
    old "## http://www.renpy.org/doc/html/screen_special.html#input"
    new "## http://ja.renpy.org/doc/html/screen_special.html#input"

    # screens.rpy:205
    old "## Choice screen"
    new "## Choice（選択）スクリーン"

    # screens.rpy:207
    old "## This screen is used to display the in-game choices presented by the menu statement. The one parameter, items, is a list of objects, each with caption and action fields."
    new "## このスクリーンは、ゲーム内の選択肢を表示する menu ステートメントに使います。items のパラメーターは caption（選択肢のテキスト）と action（クリック時の実行内容）を要素に持つオブジェクトのリスト（配列）です。"

    # screens.rpy:211
    old "## http://www.renpy.org/doc/html/screen_special.html#choice"
    new "## http://ja.renpy.org/doc/html/screen_special.html#choice"

    # screens.rpy:221
    old "## When this is true, menu captions will be spoken by the narrator. When false, menu captions will be displayed as empty buttons."
    new "## 次が True の場合、menu の見出しテキストを narrator を使って say（発話）スクリーンで表示します。 False の場合、選択肢の上に押せないボタンとして表示します。"

    # screens.rpy:244
    old "## Quick Menu screen"
    new "## Quick Menu（クイックメニュー）スクリーン"

    # screens.rpy:246
    old "## The quick menu is displayed in-game to provide easy access to the out-of-game menus."
    new "## クイックメニューはゲーム中に常時表示されるスクリーンで、ゲーム外の機能に素早くアクセスすることができます。"

    # screens.rpy:251
    old "## Ensure this appears on top of other screens."
    new "## 他のスクリーンの上に表示する。"

    # screens.rpy:261
    old "Back"
    new "ロールバック"

    # screens.rpy:262
    old "History"
    new "ヒストリー"

    # screens.rpy:263
    old "Skip"
    new "スキップ"

    # screens.rpy:264
    old "Auto"
    new "オート"

    # screens.rpy:265
    old "Save"
    new "セーブ"

    # screens.rpy:266
    old "Q.Save"
    new "Q.セーブ"

    # screens.rpy:267
    old "Q.Load"
    new "Q.ロード"

    # screens.rpy:268
    old "Prefs"
    new "設定"

    # screens.rpy:271
    old "## This code ensures that the quick_menu screen is displayed in-game, whenever the player has not explicitly hidden the interface."
    new "## 次のコードは、プレイヤーが明示的にインターフェースを隠さない限り quick_menu スクリーンが常にゲーム中に表示されるようにしています。"

    old "## Main and Game Menu Screens"
    new "## メインメニュースクリーンとゲームメニュースクリーン"

    # screens.rpy:291
    old "## Navigation screen"
    new "## Navigation（ナビゲーション）スクリーン"

    # screens.rpy:293
    old "## This screen is included in the main and game menus, and provides navigation to other menus, and to start the game."
    new "## このスクリーンはメインメニューとゲームメニューに表示され、各メニュー間を移動したり、ゲームをスタートしたりする機能を提供しています。"

    # screens.rpy:308
    old "Start"
    new "スタート"

    # screens.rpy:316
    old "Load"
    new "ロード"

    # screens.rpy:318
    old "Preferences"
    new "環境設定"

    # screens.rpy:322
    old "End Replay"
    new "リプレイ終了"

    # screens.rpy:326
    old "Main Menu"
    new "メインメニュー"

    # screens.rpy:328
    old "About"
    new "バージョン情報"

    # screens.rpy:332
    old "## Help isn't necessary or relevant to mobile devices."
    new "## モバイルデバイスにはヘルプは不要であるか不適切です。"

    # screens.rpy:333
    old "Help"
    new "ヘルプ"

    # screens.rpy:335
    old "## The quit button is banned on iOS and unnecessary on Android."
    new "## 終了ボタンは iOS では使えず Android では不要です。"

    # screens.rpy:336
    old "Quit"
    new "終了"

    # screens.rpy:350
    old "## Main Menu screen"
    new "## Main Menu（メインメニュー）スクリーン"

    # screens.rpy:352
    old "## Used to display the main menu when Ren'Py starts."
    new "## Ren'Py が起動した時に表示されるメインメニューを表示するスクリーンです。"

    # screens.rpy:354
    old "## http://www.renpy.org/doc/html/screen_special.html#main-menu"
    new "## http://ja.renpy.org/doc/html/screen_special.html#main-menu"

    # screens.rpy:357
    old "## This ensures that any other menu screen is replaced."
    new "## 次のコードは、同じタグを持つ他のメニュースクリーンが表示された時にスクリーンを置換します。"

    # screens.rpy:364
    old "## This empty frame darkens the main menu."
    new "## 次の空のフレームは gui/overlay/main_menu.png を表示してメインメニューを暗くしています。"

    # screens.rpy:369
    old "## The use statement includes another screen inside this one. The actual contents of the main menu are in the navigation screen."
    new "## use ステートメントは、他のスクリーンを現在のスクリーンの内に表示するのに使います。メインメニューの実際のコンテンツは navigation（ナビゲーション）スクリーンです。"

    # screens.rpy:413
    old "## Game Menu screen"
    new "## Game Menu（ゲームメニュー）スクリーン"

    # screens.rpy:415
    old "## This lays out the basic common structure of a game menu screen. It's called with the screen title, and displays the background, title, and navigation."
    new "## このスクリーンは、様々なゲームメニューの基本的な共通構造をレイアウトします。各ゲームメニュースクリーンによって呼び出され、背景・現在のスクリーンタイトル・ナビゲーションを表示します。"

    # screens.rpy:418
    old "## The scroll parameter can be None, or one of \"viewport\" or \"vpgrid\". This screen is intended to be used with one or more children, which are transcluded (placed) inside it."
    new "## scroll パラメーターは None 、\"viewport\" 、\"vpgrid\" のいずれかをとります。呼び出し親のスクリーンのコンテンツは、このスクリーンの中の transclude の部分に配置されます。"

    # screens.rpy:435
    old "## Reserve space for the navigation section."
    new "## 次のフレームはナビゲーションを表示するスペースを空けています。"

    # screens.rpy:476
    old "Return"
    new "戻る"

    # screens.rpy:539
    old "## About screen"
    new "## About（バージョン情報）スクリーン"

    # screens.rpy:541
    old "## This screen gives credit and copyright information about the game and Ren'Py."
    new "## このスクリーンは、本ゲームと Ren'Py に関するコピーライトとクレジットを表示します。"

    # screens.rpy:544
    old "## There's nothing special about this screen, and hence it also serves as an example of how to make a custom screen."
    new "## このスクリーンは特別なことをしていません。そのためカスタムスクリーン作成の例として利用していきます。"

    # screens.rpy:551
    old "## This use statement includes the game_menu screen inside this one. The vbox child is then included inside the viewport inside the game_menu screen."
    new "## 次の use ステートメントは game_menu（ゲームメニュー）スクリーンをこのスクリーンの内に表示しています。use 文の子（内包されたオブジェクト）の vbox は game_menu スクリーンの中の viewport に配置されます。"

    # screens.rpy:561
    old "Version [config.version!t]\n"
    new "バージョン [config.version!t]\n"

    # screens.rpy:563
    old "## gui.about is usually set in options.rpy."
    new "## gui.about は、通常 options.rpy で設定します。"

    # screens.rpy:567
    old "Made with {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only].\n\n[renpy.license!t]"
    new "Made with {a=https://ja.renpy.org/}Ren'Py{/a} [renpy.version_only].\n\n[renpy.license!t]"

    # screens.rpy:570
    old "## This is redefined in options.rpy to add text to the about screen."
    new "## 次の変数は about スクリーンにテキストを表示します。この変数は options.rpy で再定義されるため、options.rpy の同じコードを消去しないと反映されません。"

    # screens.rpy:582
    old "## Load and Save screens"
    new "## Load and Save（セーブ・ロード）スクリーン"

    # screens.rpy:584
    old "## These screens are responsible for letting the player save the game and load it again. Since they share nearly everything in common, both are implemented in terms of a third screen, file_slots."
    new "## 以下のスクリーンは、プレイヤーがゲームデータをセーブ・ロードできるようにします。どちらも構造はほとんど等しいため、第三の file_slots（ファイルスロット）スクリーンで実装しています。"

    # screens.rpy:588
    old "## https://www.renpy.org/doc/html/screen_special.html#save https://www.renpy.org/doc/html/screen_special.html#load"
    new "## https://ja.renpy.org/doc/html/screen_special.html#save https://ja.renpy.org/doc/html/screen_special.html#load"

    # screens.rpy:607
    old "Page {}"
    new "ページ {}"

    # screens.rpy:607
    old "Automatic saves"
    new "オートセーブ"

    # screens.rpy:607
    old "Quick saves"
    new "クイックセーブ"

    # screens.rpy:613
    old "## This ensures the input will get the enter event before any of the buttons do."
    new "## 次の文は、ページ名の input のイベントがより後に定義したボタンよりも優先されるように、重なり順を反転しています。"

    # screens.rpy:615
    old "## The page name, which can be edited by clicking on a button."
    new "## ページ名。クリックすると編集できるように、ボタンとして表示しています。"

    # screens.rpy:629
    old "## The grid of file slots."
    new "## ファイルスロットを配置するグリッド。"

    # screens.rpy:649
    old "{#file_time}%A, %B %d %Y, %H:%M"
    new "{#file_time}%Y年%m月%d日(%a) %H時%M分"

    # screens.rpy:649
    old "empty slot"
    new "空のスロット"

    # screens.rpy:657
    old "## Buttons to access other pages."
    new "## 他のページにアクセスするボタン。"

    # screens.rpy:666
    old "<"
    new "<"

    # screens.rpy:668
    old "{#auto_page}A"
    new "{#auto_page}A"

    # screens.rpy:670
    old "{#quick_page}Q"
    new "{#quick_page}Q"

    # screens.rpy:670
    old "## range(1, 10) gives the numbers from 1 to 9."
    new "## range(1, 10) は１から９までの数字を生成します。"

    # screens.rpy:676
    old ">"
    new ">"

    # screens.rpy:711
    old "## Preferences screen"
    new "## Preferences（環境設定）スクリーン"

    # screens.rpy:713
    old "## The preferences screen allows the player to configure the game to better suit themselves."
    new "## Preferences スクリーンは、各プレイヤーがゲームを自分に合う環境にカスタマイズできるようにします。"

    # screens.rpy:716
    old "## https://www.renpy.org/doc/html/screen_special.html#preferences"
    new "## https://ja.renpy.org/doc/html/screen_special.html#preferences"

    # screens.rpy:738
    old "Display"
    new "ディスプレイ"

    # screens.rpy:739
    old "Window"
    new "ウィンドウ"

    # screens.rpy:740
    old "Fullscreen"
    new "フルスクリーン"

    # screens.rpy:744
    old "Rollback Side"
    new "ロールバック\nサイド"

    # screens.rpy:745
    old "Disable"
    new "無効"

    # screens.rpy:746
    old "Left"
    new "レフト"

    # screens.rpy:747
    old "Right"
    new "ライト"

    # screens.rpy:752
    old "Unseen Text"
    new "未読テキスト"

    # screens.rpy:753
    old "After Choices"
    new "選択肢後"

    # screens.rpy:754
    old "Transitions"
    new "トランジション"

    # screens.rpy:756
    old "## Additional vboxes of type \"radio_pref\" or \"check_pref\" can be added here, to add additional creator-defined preferences."
    new "## この場所に \"radio_pref\" または \"check_pref\" をスタイルに持つ vbox を追加して、開発者が定義した環境設定を増やすことができます。"

    # screens.rpy:767
    old "Text Speed"
    new "文字表示速度"

    # screens.rpy:771
    old "Auto-Forward Time"
    new "オート待ち時間"

    # screens.rpy:778
    old "Music Volume"
    new "音楽の音量"

    # screens.rpy:785
    old "Sound Volume"
    new "効果音の音量"

    # screens.rpy:791
    old "Test"
    new "テスト"

    # screens.rpy:795
    old "Voice Volume"
    new "ボイスの音量"

    # screens.rpy:806
    old "Mute All"
    new "全てミュート"

    # screens.rpy:882
    old "## History screen"
    new "## History（履歴）スクリーン"

    # screens.rpy:884
    old "## This is a screen that displays the dialogue history to the player. While there isn't anything special about this screen, it does have to access the dialogue history stored in _history_list."
    new "## このスクリーンは、ダイアローグヒストリー（台詞の履歴）を表示します。このスクリーンに特別なものはありませんが、_history_list に保存されたダイアローグヒストリーにアクセスする必要があります。"

    # screens.rpy:888
    old "## https://www.renpy.org/doc/html/history.html"
    new "## https://ja.renpy.org/doc/html/history.html"

    # screens.rpy:894
    old "## Avoid predicting this screen, as it can be very large."
    new "## データが大きくなりすぎる可能性があるため、このスクリーンを予測しないようにしています。"

    # screens.rpy:905
    old "## This lays things out properly if history_height is None."
    new "## 次の文は history_height が None の場合でもレイアウトが正しくなるようにしています。"

    # screens.rpy:914
    old "## Take the color of the who text from the Character, if set."
    new "## キャラクター名のカラーが設定されている場合、その情報を獲得して色付けします。"

    # screens.rpy:921
    old "The dialogue history is empty."
    new "ヒストリーはありません。"

    # screens.rpy:965
    old "## Help screen"
    new "## Help（ヘルプ）スクリーン"

    # screens.rpy:967
    old "## A screen that gives information about key and mouse bindings. It uses other screens (keyboard_help, mouse_help, and gamepad_help) to display the actual help."
    new "## キーやマウスの割り当てに関する情報を表示するスクリーン。実際のヘルプは他のスクリーン（keyboard_help、mouse_help、gamepad_help）を使います。"

    # screens.rpy:986
    old "Keyboard"
    new "キーボード"

    # screens.rpy:987
    old "Mouse"
    new "マウス"

    # screens.rpy:990
    old "Gamepad"
    new "ゲームパッド"

    # screens.rpy:1003
    old "Enter"
    new "エンター"

    # screens.rpy:1004
    old "Advances dialogue and activates the interface."
    new "台詞を読み進める。またはボタンを選択する。"

    # screens.rpy:1007
    old "Space"
    new "スペース"

    # screens.rpy:1008
    old "Advances dialogue without selecting choices."
    new "台詞を読み進める。ただしボタンは選択しない。"

    # screens.rpy:1011
    old "Arrow Keys"
    new "方向キー"

    # screens.rpy:1012
    old "Navigate the interface."
    new "インターフェースを移動する。"

    # screens.rpy:1015
    old "Escape"
    new "ESC"

    # screens.rpy:1016
    old "Accesses the game menu."
    new "ゲームメニューを開く。"

    # screens.rpy:1019
    old "Ctrl"
    new "Ctrl"

    # screens.rpy:1020
    old "Skips dialogue while held down."
    new "押し続けている間スキップする。"

    # screens.rpy:1023
    old "Tab"
    new "Tab"

    # screens.rpy:1024
    old "Toggles dialogue skipping."
    new "スキップモードに切り替える。"

    # screens.rpy:1027
    old "Page Up"
    new "Page Up"

    # screens.rpy:1028
    old "Rolls back to earlier dialogue."
    new "前の台詞に戻る。"

    # screens.rpy:1031
    old "Page Down"
    new "Page Down"

    # screens.rpy:1032
    old "Rolls forward to later dialogue."
    new "ロールバック中、次の台詞に進む。"

    # screens.rpy:1036
    old "Hides the user interface."
    new "インターフェースを隠す。"

    # screens.rpy:1040
    old "Takes a screenshot."
    new "スクリーンショットを撮る。"

    # screens.rpy:1044
    old "Toggles assistive {a=https://www.renpy.org/l/voicing}self-voicing{/a}."
    new "{a=https://ja.renpy.org/l/voicing}セルフボイシング{/a}を有効化する。"

    # screens.rpy:1050
    old "Left Click"
    new "左クリック"

    # screens.rpy:1054
    old "Middle Click"
    new "中クリック"

    # screens.rpy:1058
    old "Right Click"
    new "右クリック"

    # screens.rpy:1062
    old "Mouse Wheel Up"
    new "マウスホイール上回転"

    # screens.rpy:1066
    old "Mouse Wheel Down"
    new "マウスホイール下回転"

    # screens.rpy:1073
    old "Right Trigger\nA/Bottom Button"
    new "Ｒトリガー\nＡ／下ボタン"

    old "Left Trigger\nLeft Shoulder"
    new "Ｌトリガー\nＬボタン"

    # screens.rpy:1081
    old "Right Shoulder"
    new "Ｒボタン"

    # screens.rpy:1085
    old "D-Pad, Sticks"
    new "方向パッド\n左右スティック"

    # screens.rpy:1089
    old "Start, Guide"
    new "スタート、ガイド"

    # screens.rpy:1093
    old "Y/Top Button"
    new "Ｙ／上ボタン"

    # screens.rpy:1096
    old "Calibrate"
    new "キャリブレート"

    # screens.rpy:1124
    old "## Additional screens"
    new "## 付加的なスクリーン"

    # screens.rpy:1128
    old "## Confirm screen"
    new "## Confirm（確認）スクリーン"

    # screens.rpy:1130
    old "## The confirm screen is called when Ren'Py wants to ask the player a yes or no question."
    new "## Confirm スクリーンは、 Ren'Py がプレイヤーに「はい・いいえ」で答える質問をする時に使います。"

    # screens.rpy:1133
    old "## http://www.renpy.org/doc/html/screen_special.html#confirm"
    new "## http://ja.renpy.org/doc/html/screen_special.html#confirm"

    # screens.rpy:1137
    old "## Ensure other screens do not get input while this screen is displayed."
    new "## 次の文は、このスクリーンが表示されている間、他のスクリーンの反応を無視するようにしています。"

    # screens.rpy:1161
    old "Yes"
    new "はい"

    # screens.rpy:1162
    old "No"
    new "いいえ"

    # screens.rpy:1164
    old "## Right-click and escape answer \"no\"."
    new "## 右クリックで「いいえ」と答える。"

    # screens.rpy:1191
    old "## Skip indicator screen"
    new "## Skip indicator（スキップ表示）スクリーン"

    # screens.rpy:1193
    old "## The skip_indicator screen is displayed to indicate that skipping is in progress."
    new "## Skip_indicator スクリーンは、スキップ中であることを表示するスクリーンです。"

    # screens.rpy:1196
    old "## https://www.renpy.org/doc/html/screen_special.html#skip-indicator"
    new "## https://ja.renpy.org/doc/html/screen_special.html#skip-indicator"

    # screens.rpy:1208
    old "Skipping"
    new "スキップ中"

    # screens.rpy:1215
    old "## This transform is used to blink the arrows one after another."
    new "## 矢印を次から次へと点滅させる transform（変換）。"

    # screens.rpy:1247
    old "## Notify screen"
    new "## Notify（通知）スクリーン"

    # screens.rpy:1249
    old "## The notify screen is used to show the player a message. (For example, when the game is quicksaved or a screenshot has been taken.)"
    new "## Notify スクリーンは、プレイヤーに短いメッセージを表示するのに使います。（例えばクイックセーブをしたり、スクリーンショットを撮った時。）"

    # screens.rpy:1252
    old "## https://www.renpy.org/doc/html/screen_special.html#notify-screen"
    new "## https://ja.renpy.org/doc/html/screen_special.html#notify-screen"

    # screens.rpy:1286
    old "## NVL screen"
    new "## NVL（ノベル）スクリーン"

    # screens.rpy:1288
    old "## This screen is used for NVL-mode dialogue and menus."
    new "## このスクリーンは NVL モード（全画面方式）の台詞と選択肢を表示します。"

    # screens.rpy:1290
    old "## http://www.renpy.org/doc/html/screen_special.html#nvl"
    new "## http://ja.renpy.org/doc/html/screen_special.html#nvl"

    # screens.rpy:1301
    old "## Displays dialogue in either a vpgrid or the vbox."
    new "## gui.nvl_height が設定されていれば vpgrid で等間隔に表示、そうでなければ vbox で可変的に表示します。"

    # screens.rpy:1314
    old "## Displays the menu, if given. The menu may be displayed incorrectly if config.narrator_menu is set to True, as it is above."
    new "## 選択肢があれば表示。config.narrator_menu が初期設定である True のままの場合、正しく表示されないことがあります。"

    # screens.rpy:1344
    old "## This controls the maximum number of NVL-mode entries that can be displayed at once."
    new "## 次の文は一度に表示される NVL モードのエントリー（１台詞）の最大数を制御します。"

    # screens.rpy:1406
    old "## Mobile Variants"
    new "## モバイル用の別設定"

    # screens.rpy:1413
    old "## Since a mouse may not be present, we replace the quick menu with a version that uses fewer and bigger buttons that are easier to touch."
    new "## マウスが使用できないので、ボタンが大きくて数が少ないクイックメニューに置き換えて、タッチしやすいようにしています。"

    # screens.rpy:1429
    old "Menu"
    new "メニュー"

    # screens.rpy:1233
    old "## We have to use a font that has the BLACK RIGHT-POINTING SMALL TRIANGLE glyph in it."
    new "## 小さな黒い矢印型のグリフが入ったフォントが必要になります。"

    # screens.rpy:120
    old "## Make the namebox available for styling through the Character object."
    new "## namebox を Character オブジェクトから使えるスタイルの接頭辞として追加します。（例：namebox_background)"

    # screens.rpy:172
    old "## https://www.renpy.org/doc/html/screen_special.html#input"
    new "## https://ja.renpy.org/doc/html/screen_special.html#input"

    # screens.rpy:205
    old "## https://www.renpy.org/doc/html/screen_special.html#choice"
    new "## https://ja.renpy.org/doc/html/screen_special.html#choice"

    # screens.rpy:350
    old "## https://www.renpy.org/doc/html/screen_special.html#main-menu"
    new "## https://ja.renpy.org/doc/html/screen_special.html#main-menu"

    # screens.rpy:916
    old "## This determines what tags are allowed to be displayed on the history screen."
    new "## 履歴画面に表示できるタグを決定します。"

    # screens.rpy:1132
    old "## https://www.renpy.org/doc/html/screen_special.html#confirm"
    new "## https://ja.renpy.org/doc/html/screen_special.html#confirm"

    # screens.rpy:1289
    old "## https://www.renpy.org/doc/html/screen_special.html#nvl"
    new "## https://ja.renpy.org/doc/html/screen_special.html#nvl"

    # gui/game/screens.rpy:333
    old "## The quit button is banned on iOS and unnecessary on Android and Web."
    new "## 終了ボタンはiOSでは使用できません。また、AndroidやWebでは必要ありません。"

    # gui/game/screens.rpy:1049
    old "Opens the accessibility menu."
    new "アクセシビリティーメニューを開きます。"

    # gui/game/screens.rpy:1307
    old "## Displays the menu, if given. The menu may be displayed incorrectly if config.narrator_menu is set to True."
    new "## 指定されれば選択肢を表示します。config.narrator_menuがTrueだと、メニューは正常に表示されないでしょう。"


    # gui/game/screens.rpy:676
    old "Upload Sync"
    new "同期のアップロード"

    # gui/game/screens.rpy:680
    old "Download Sync"
    new "同期のダウンロード"

    # gui/game/screens.rpy:1410
    old "## Bubble screen"
    new "## バブルスクリーン"

    # gui/game/screens.rpy:1412
    old "## The bubble screen is used to display dialogue to the player when using speech bubbles. The bubble screen takes the same parameters as the say screen, must create a displayable with the id of \"what\", and can create displayables with the \"namebox\", \"who\", and \"window\" ids."
    new "## バブルスクリーンは、吹き出しを使用する際に、プレイヤーにダイアログを表示するために使用されます。バブルスクリーンはSayスクリーンと同じパラメータを持ち、idが \"what \"のdisplayableを作成しなければならず、idが \"namebox\", \"who\", \"window \"のdisplayableを作成できます。"

    # gui/game/screens.rpy:1417
    old "## https://www.renpy.org/doc/html/bubble.html#bubble-screen"
    new "## https://www.renpy.org/doc/html/bubble.html#bubble-screen"

    # gui/game/screens.rpy:1098
    old "Start, Guide, B/Right Button"
    new "スタート、ガイド、 B / Right ボタン"

