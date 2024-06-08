
translate tchinese strings:

    # options.rpy:1
    old "## This file contains options that can be changed to customize your game."
    new "## 此文件包含可以更改以自訂您的遊戲的選項。"

    # options.rpy:4
    old "## Lines beginning with two '#' marks are comments, and you shouldn't uncomment them. Lines beginning with a single '#' mark are commented-out code, and you may want to uncomment them when appropriate."
    new "## 以兩個'#' 標記開頭的行是註釋，您不應取消註釋它們。以單一'#' 標記開頭的行是註解掉的程式碼，您可能需要在適當的時候取消註解它們。"

    # options.rpy:10
    old "## Basics"
    new "## 基礎"

    # options.rpy:12
    old "## A human-readable name of the game. This is used to set the default window title, and shows up in the interface and error reports."
    new "## 一個人類可讀的遊戲名稱。這用於設定預設視窗標題，並顯示在介面和錯誤報告中。"

    # options.rpy:15
    old "## The _() surrounding the string marks it as eligible for translation."
    new "## 字串周圍的 _() 標記其為符合翻譯條件。"

    # options.rpy:17
    old "Ren'Py 7 Default GUI"
    new "Ren'Py 7 默認 GUI"

    # options.rpy:20
    old "## Determines if the title given above is shown on the main menu screen. Set this to False to hide the title."
    new "## 決定上面給出的標題是否顯示在主選單畫面上。將其設為 False 以隱藏標題。"

    # options.rpy:26
    old "## The version of the game."
    new "## 遊戲的版本"

    # options.rpy:31
    old "## Text that is placed on the game's about screen. To insert a blank line between paragraphs, write \\n\\n."
    new "## 放置在遊戲的關於螢幕上的文字。要在段落之間插入空行，請寫入 \\n\\n."

    # options.rpy:37
    old "## A short name for the game used for executables and directories in the built distribution. This must be ASCII-only, and must not contain spaces, colons, or semicolons."
    new "## 遊戲的短名稱，用於建立發行版中的可執行檔和目錄。它必須只是 ASCII，並且不能包含空格、冒號或分號。"

    # options.rpy:44
    old "## Sounds and music"
    new "## 聲音和音樂"

    # options.rpy:46
    old "## These three variables control which mixers are shown to the player by default. Setting one of these to False will hide the appropriate mixer."
    new "## 這三個變數控制預設向播放器顯示哪些混音器。將其中一個設定為 False 將隱藏對應的混音器。"

    # options.rpy:55
    old "## To allow the user to play a test sound on the sound or voice channel, uncomment a line below and use it to set a sample sound to play."
    new "## 要允許用戶在聲音或語音通道上播放測試聲音，請取消註釋下面的行並使用它來設定要播放的範例聲音。"

    # options.rpy:62
    old "## Uncomment the following line to set an audio file that will be played while the player is at the main menu. This file will continue playing into the game, until it is stopped or another file is played."
    new "## 取消註解以下行以設定玩家在主選單時播放的音訊檔案。該檔案將繼續在遊戲中播放，直到停止或播放另一個檔案。"

    # options.rpy:69
    old "## Transitions"
    new "## 過渡"

    # options.rpy:71
    old "## These variables set transitions that are used when certain events occur. Each variable should be set to a transition, or None to indicate that no transition should be used."
    new "## 這些變數設定在發生某些事件時使用的過渡。每個變數都應設定為過渡，或 None 表示不應使用任何過渡。"

    # options.rpy:75
    old "## Entering or exiting the game menu."
    new "## 進入或退出遊戲選單。"

    # options.rpy:81
    old "## A transition that is used after a game has been loaded."
    new "## 遊戲載入後使用的過渡。"

    # options.rpy:86
    old "## Used when entering the main menu after the game has ended."
    new "## 在遊戲結束後進入主選單時使用。"

    # options.rpy:91
    old "## A variable to set the transition used when the game starts does not exist. Instead, use a with statement after showing the initial scene."
    new "## 用於設定遊戲開始時使用的過渡的變數不存在。相反，需要在顯示初始場景後使用 with 語句。"

    # options.rpy:96
    old "## Window management"
    new "## 視窗管理"

    # options.rpy:98
    old "## This controls when the dialogue window is displayed. If \"show\", it is always displayed. If \"hide\", it is only displayed when dialogue is present. If \"auto\", the window is hidden before scene statements and shown again once dialogue is displayed."
    new "## 這控制何時顯示對話視窗。如果 \"show\" ，則始終顯示。如果 \"hide\" ，則僅在存在對話時顯示。如果 \"auto\" ，則視窗在場景陳述之前隱藏，並在顯示對話後再次顯示。"

    # options.rpy:103
    old "## After the game has started, this can be changed with the \"window show\", \"window hide\", and \"window auto\" statements."
    new "## 遊戲開始後，可以使用 \"window show\", \"window hide\", 和 \"window auto\" 語句更改。"

    # options.rpy:109
    old "## Transitions used to show and hide the dialogue window"
    new "## 用於顯示和隱藏對話視窗的轉換"

    # options.rpy:115
    old "## Preference defaults"
    new "## 首選項預設值"

    # options.rpy:117
    old "## Controls the default text speed. The default, 0, is infinite, while any other number is the number of characters per second to type out."
    new "## 控制預設文字速度。預設值 0 是無限的，而任何其他數字是每秒鍵入的字元數。"

    # options.rpy:123
    old "## The default auto-forward delay. Larger numbers lead to longer waits, with 0 to 30 being the valid range."
    new "## 預設自動轉送延遲。數字越大，等待時間越長，有效範圍為 0 到 30。"

    # options.rpy:129
    old "## Save directory"
    new "## 儲存檔目錄"

    # options.rpy:131
    old "## Controls the platform-specific place Ren'Py will place the save files for this game. The save files will be placed in:"
    new "## 控制Ren'Py將放置該遊戲的儲存文檔的平台特定位置。儲存文檔將放置在："

    # options.rpy:134
    old "## Windows: %APPDATA\\RenPy\\<config.save_directory>"
    new "## Windows: %APPDATA\\RenPy\\<config.save_directory>"

    # options.rpy:136
    old "## Macintosh: $HOME/Library/RenPy/<config.save_directory>"
    new "## Macintosh: $HOME/Library/RenPy/<config.save_directory>"

    # options.rpy:138
    old "## Linux: $HOME/.renpy/<config.save_directory>"
    new "## Linux: $HOME/.renpy/<config.save_directory>"

    # options.rpy:140
    old "## This generally should not be changed, and if it is, should always be a literal string, not an expression."
    new "## 通常不應更改，如果更改，則應始終是文字字串，而不是表達式。"

    # options.rpy:146
    old "## Icon ########################################################################'"
    new "## 圖標 ########################################################################'"

    # options.rpy:148
    old "## The icon displayed on the taskbar or dock."
    new "## 顯示在工作列或擴充座上的圖示。"

    # options.rpy:153
    old "## Build configuration"
    new "## 構置配置"

    # options.rpy:155
    old "## This section controls how Ren'Py turns your project into distribution files."
    new "## 本節控制Ren'Py如何將您的專案轉換為釋出版。"

    # options.rpy:160
    old "## The following functions take file patterns. File patterns are case- insensitive, and matched against the path relative to the base directory, with and without a leading /. If multiple patterns match, the first is used."
    new "## 以下函數採用檔案模式。 檔案模式不區分大小寫，並與相對於基底目錄的路徑進行匹配，無論是否有前導 /。 如果多個模式匹配，則使用第一個模式。"

    # options.rpy:165
    old "## In a pattern:"
    new "## 在一個模式中："

    # options.rpy:167
    old "## / is the directory separator."
    new "## / 是目錄分隔符號。"

    # options.rpy:169
    old "## * matches all characters, except the directory separator."
    new "## * 匹配目錄分隔符號之外的所有字元。"

    # options.rpy:171
    old "## ** matches all characters, including the directory separator."
    new "## ** 匹配所有字符，包括目錄分隔符。"

    # options.rpy:173
    old "## For example, \"*.txt\" matches txt files in the base directory, \"game/**.ogg\" matches ogg files in the game directory or any of its subdirectories, and \"**.psd\" matches psd files anywhere in the project."
    new "## 就比如， \"*.txt\" 匹配 base 目錄中的txt文件， \"game/**.ogg\" 匹配遊戲目錄或其任何子目錄中的 ogg 文件，和 \"**.psd\" 匹配專案中任意位置的 psd 檔案。"

    # options.rpy:177
    old "## Classify files as None to exclude them from the built distributions."
    new "## 將檔案分類為 None 以將它們從建置的釋出版中排除。"

    # options.rpy:185
    old "## To archive files, classify them as 'archive'."
    new "## 要歸檔文件，請將其分類為 'archive' 。"

    # options.rpy:190
    old "## Files matching documentation patterns are duplicated in a mac app build, so they appear in both the app and the zip file."
    new "## 與文件模式匹配的文件在 Mac 應用程式建置中會重複，因此它們會同時出現在應用程式和 zip 檔案中。"

    # options.rpy:196
    old "## A Google Play license key is required to download expansion files and perform in-app purchases. It can be found on the \"Services & APIs\" page of the Google Play developer console."
    new "## 下載擴充檔案和執行應用程式內購買需要 Google Play 許可證金鑰。 它可以在 Google Play 開發者控制台的 \"Services & APIs\" 頁面上找到。"

    # options.rpy:203
    old "## The username and project name associated with an itch.io project, separated by a slash."
    new "## 與 itch.io 項目關聯的使用者名稱和項目名稱，以斜線分隔。"

    # gui/game/options.rpy:31
    old "## Text that is placed on the game's about screen. Place the text between the triple-quotes, and leave a blank line between paragraphs."
    new "## 放置在遊戲的關於螢幕上的文字。將文字放在三引號之間，並在段落之間留一個空行。"

    # gui/game/options.rpy:47
    old "## These three variables control, among other things, which mixers are shown to the player by default. Setting one of these to False will hide the appropriate mixer."
    new "## 這三個變數控制預設向播放器顯示哪些混音器。將其中之一設為 False 將隱藏相應的混音器。"

    # gui/game/options.rpy:82
    old "## Between screens of the game menu."
    new "## 在遊戲選單畫面之間。"

    # gui/game/options.rpy:152
    old "## Icon"
    new "## 圖標"

    # gui/game/options.rpy:203
    old "## A Google Play license key is required to perform in-app purchases. It can be found in the Google Play developer console, under \"Monetize\" > \"Monetization Setup\" > \"Licensing\"."
    new "## 執行應用程式內購買需要 Google Play 許可證密鑰。它可以在 Google Play 開發者控制台的 \"Monetize\" > \"Monetization Setup\" > \"Licensing\" 下找到。"

