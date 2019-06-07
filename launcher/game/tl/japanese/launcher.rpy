
translate japanese strings:

    # about.rpy:39
    old "[version!q]"
    new "[version!q]"

    # about.rpy:43
    old "View license"
    new "ライセンス"

    # add_file.rpy:28
    old "FILENAME"
    new "ファイル名"

    # add_file.rpy:28
    old "Enter the name of the script file to create."
    new "作成するスクリプトファイル名を入力してください。"

    # add_file.rpy:31
    old "The filename must have the .rpy extension."
    new "ファイル名は拡張子 .rpy を持つ必要があります。"

    # add_file.rpy:39
    old "The file already exists."
    new "ファイルは既に存在します。"

    # add_file.rpy:42
    old "# Ren'Py automatically loads all script files ending with .rpy. To use this\n# file, define a label and jump to it from another file.\n"
    new "# Ren'Py は .rpy で終わるすべてのスクリプトファイルを自動的にロードします。このファイルを使用するためにはラベルを定義し、他のファイルからそこにジャンプしてください。\n"

    # android.rpy:30
    old "To build Android packages, please download RAPT, unzip it, and place it into the Ren'Py directory. Then restart the Ren'Py launcher."
    new "Android パッケージをビルドするには、RAPT をダウンロード・展開し、Ren'Py のディレクトリーに設置して下さい。その後、Ren'Py を再起動して下さい。"

    # android.rpy:31
    old "An x86 Java Development Kit is required to build Android packages on Windows. The JDK is different from the JRE, so it's possible you have Java without having the JDK.\n\nPlease {a=http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html}download and install the JDK{/a}, then restart the Ren'Py launcher."
    new "Windows では、Android パッケージのビルドに 32-bit の Java 開発キットが必要です。JDK は JRE とは異なるため、JDK が無くても Java が利用できます。\n\n{a=http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html}JDK のダウンロードとインストール{/a}を行い、Ren'Py ランチャーを再起動して下さい。"

    # android.rpy:32
    old "RAPT has been installed, but you'll need to install the Android SDK before you can build Android packages. Choose Install SDK to do this."
    new "RAPT のインストールは終了しましたが、Android パッケージをビルドする前に Android SDK もインストールする必要があります。SDKをインストールしてください。"

    # android.rpy:33
    old "RAPT has been installed, but a key hasn't been configured. Please create a new key, or restore android.keystore."
    new "RAPT のインストールは終了しましたが、キーが設定されていません。新しいキーを作成するか、android.keystore を修復してください。"

    # android.rpy:34
    old "The current project has not been configured. Use \"Configure\" to configure it before building."
    new "現在のプロジェクトは設定がされていません。「設定」を使用してビルド前に設定してください。"

    # android.rpy:35
    old "Choose \"Build\" to build the current project, or attach an Android device and choose \"Build & Install\" to build and install it on the device."
    new "「ビルド」を選択して現在のプロジェクトをビルドするか、Android デバイスを接続して「ビルドとインストール」を選択し、そのデバイスにインストールしてください。"

    # android.rpy:37
    old "Attempts to emulate an Android phone.\n\nTouch input is emulated through the mouse, but only when the button is held down. Escape is mapped to the menu button, and PageUp is mapped to the back button."
    new "Android Phone をエミュレートします。\n\nタッチ入力のエミュレートはマウスを利用しますが、ボタン押下時のみ反応します。Escape はメニューボタン、PageUp はバックボタンに割り当てられています。"

    # android.rpy:38
    old "Attempts to emulate an Android tablet.\n\nTouch input is emulated through the mouse, but only when the button is held down. Escape is mapped to the menu button, and PageUp is mapped to the back button."
    new "Android tablet をエミュレートします。\n\nタッチ入力のエミュレートはマウスを利用しますが、ボタン押下時のみ反応します。Escape はメニューボタン、PageUp はバックボタンに割り当てられています。"

    # android.rpy:39
    old "Attempts to emulate a televison-based Android console, like the OUYA or Fire TV.\n\nController input is mapped to the arrow keys, Enter is mapped to the select button, Escape is mapped to the menu button, and PageUp is mapped to the back button."
    new "OUYA や Fire TV のようなテレビで動作する Android デバイスをエミュレートします。\n\nコントローラーの入力は矢印キー、Enter はセレクトボタン、Escape はメニューボタン、PageUp はバックボタンに割り当てられています。"

    # android.rpy:41
    old "Downloads and installs the Android SDK and supporting packages. Optionally, generates the keys required to sign the package."
    new "Android SDK をダウンロード後インストールします。署名に必要なキーを任意で生成します。"

    # android.rpy:42
    old "Configures the package name, version, and other information about this project."
    new "このプロジェクトについてパッケージ名とバージョン、その他の情報を設定してください。"

    # android.rpy:43
    old "Opens the file containing the Google Play keys in the editor.\n\nThis is only needed if the application is using an expansion APK. Read the documentation for more details."
    new "Google Play key を含むファイルをエディターで開いてください。\n\nこの処理はアプリが拡張 APK を使用する場合のみ必要となります。詳細はドキュメントを参照してください。"

    # android.rpy:44
    old "Builds the Android package."
    new "Android パッケージをビルドします。"

    # android.rpy:45
    old "Builds the Android package, and installs it on an Android device connected to your computer."
    new "Android パッケージをビルドし、コンピューターに接続された Android デバイスにインストールします。"

    # android.rpy:46
    old "Builds the Android package, installs it on an Android device connected to your computer, then launches the app on your device."
    new "Android パッケージをビルドして、接続された Android にインストール、 そのデバイスでアプリを起動します。"

    # android.rpy:48
    old "Connects to an Android device running ADB in TCP/IP mode."
    new "TCP/IP モードで ADB を実行し、Android デバイスに接続します。"

    # android.rpy:49
    old "Disconnects from an Android device running ADB in TCP/IP mode."
    new "TCP/IP モードで ADB を実行し、Android デバイスとの接続を解除します。"

    # android.rpy:50
    old "Retrieves the log from the Android device and writes it to a file."
    new "Android デバイスからログを獲得し、ファイルに書き出します。"

    # android.rpy:240
    old "Copying Android files to distributions directory."
    new "Android ファイルを distributions ディレクトリにコピーしています。"

    # android.rpy:304
    old "Android: [project.current.name!q]"
    new "Android: [project.current.name!q]"

    # android.rpy:324
    old "Emulation:"
    new "エミュレーター:"

    # android.rpy:333
    old "Phone"
    new "Phone"

    # android.rpy:337
    old "Tablet"
    new "Tablet"

    # android.rpy:341
    old "Television"
    new "Television"

    # android.rpy:353
    old "Build:"
    new "ビルド:"

    # android.rpy:361
    old "Install SDK & Create Keys"
    new "SDKのインストール & キーの作成"

    # android.rpy:365
    old "Configure"
    new "構成の設定"

    # android.rpy:369
    old "Build Package"
    new "パッケージのビルド"

    # android.rpy:373
    old "Build & Install"
    new "ビルドとインストール"

    # android.rpy:377
    old "Build, Install & Launch"
    new "ビルドとインストール、起動"

    # android.rpy:388
    old "Other:"
    new "その他:"

    # android.rpy:396
    old "Remote ADB Connect"
    new "リモートADB接続"

    # android.rpy:400
    old "Remote ADB Disconnect"
    new "リモートADB接続解除"

    # android.rpy:404
    old "Logcat"
    new "Logcat"

    # android.rpy:437
    old "Before packaging Android apps, you'll need to download RAPT, the Ren'Py Android Packaging Tool. Would you like to download RAPT now?"
    new "Android アプリをパッケージングする前に、RAPT (Ren'Py Android Packaging Tool) をダウンロードする必要があります。今すぐダウンロードしますか？"

    # android.rpy:496
    old "Remote ADB Address"
    new "リモート ADB アドレス"

    # android.rpy:496
    old "Please enter the IP address and port number to connect to, in the form \"192.168.1.143:5555\". Consult your device's documentation to determine if it supports remote ADB, and if so, the address and port to use."
    new "接続先の IP アドレスとポート番号を \"192.168.1.143:5555\" の形式で入力して下さい。デバイスのドキュメントを読んでリモート ADB 接続をサポートしているかを確認してください。サポートしているなら、そのアドレスとポート番号を使用してください。"

    # android.rpy:508
    old "Invalid remote ADB address"
    new "不正なリモート ADB アドレスです。"

    # android.rpy:508
    old "The address must contain one exactly one ':'."
    new "アドレスは必ずひとつ ':' を含まなければなりません。"

    # android.rpy:512
    old "The host may not contain whitespace."
    new "ホストは空白を含んではいけません。"

    # android.rpy:518
    old "The port must be a number."
    new "ポートは数字でなければなりません。"

    # android.rpy:544
    old "Retrieving logcat information from device."
    new "デバイスから logcat のインフォメーションを獲得しています。"

    # choose_directory.rpy:73
    old "Ren'Py was unable to run python with tkinter to choose the directory. Please install the python-tk or tkinter package."
    new "Ren'Py は tkinter でディレクトリーを選択出来ません。 python-tk か tkinter をインストールしてください。"

    # choose_theme.rpy:303
    old "Could not change the theme. Perhaps options.rpy was changed too much."
    new "テーマを変更出来ません。 options.rpy が変更されすぎているかもしれません。"

    # choose_theme.rpy:370
    old "Planetarium"
    new "プラネタリウム"

    # choose_theme.rpy:425
    old "Choose Theme"
    new "テーマ選択"

    # choose_theme.rpy:438
    old "Theme"
    new "テーマ"

    # choose_theme.rpy:463
    old "Color Scheme"
    new "カラースキーム"

    # choose_theme.rpy:495
    old "Continue"
    new "続行"

    # consolecommand.rpy:84
    old "INFORMATION"
    new "情報"

    # consolecommand.rpy:84
    old "The command is being run in a new operating system console window."
    new "このコマンドは、OS のコンソールウィンドウで実行されています。"

    # distribute.rpy:443
    old "Scanning project files..."
    new "プロジェクトをスキャンしています…"

    # distribute.rpy:459
    old "Building distributions failed:\n\nThe build.directory_name variable may not include the space, colon, or semicolon characters."
    new "配布物のビルドに失敗しました:\n\nbuild.directory_name 変数にスペース、コロン、セミコロンを含めてはいけません。"

    # distribute.rpy:504
    old "No packages are selected, so there's nothing to do."
    new "パッケージが選択されていないため、何もすることがありません。"

    # distribute.rpy:516
    old "Scanning Ren'Py files..."
    new "Ren'Py ファイルをスキャンしています…"

    # distribute.rpy:569
    old "All packages have been built.\n\nDue to the presence of permission information, unpacking and repacking the Linux and Macintosh distributions on Windows is not supported."
    new "全てのパッケージのビルドを終了しました。\n\nパーミッション情報のために、Windows 上での Linux や Macintosh 用の配布物の解凍、再圧縮はサポートされません。"

    # distribute.rpy:752
    old "Archiving files..."
    new "ファイルをアーカイブしています…"

    # distribute.rpy:1050
    old "Unpacking the Macintosh application for signing..."
    new "署名のため、Macintosh application を展開しています…"

    # distribute.rpy:1060
    old "Signing the Macintosh application..."
    new "Macintosh application に署名しています…"

    # distribute.rpy:1082
    old "Creating the Macintosh DMG..."
    new "Macintosh DMG を作成しています…"

    # distribute.rpy:1091
    old "Signing the Macintosh DMG..."
    new "Macintosh DMG に署名しています…"

    # distribute.rpy:1248
    old "Writing the [variant] [format] package."
    new "[variant] [format] パッケージを書き出しています。"

    # distribute.rpy:1261
    old "Making the [variant] update zsync file."
    new "[variant] のアップデート用 zsync ファイルを書き出しています。"

    # distribute.rpy:1404
    old "Processed {b}[complete]{/b} of {b}[total]{/b} files."
    new "{b}[total]{/b} 中 {b}[complete]{/b} ファイルを処理しました。"

    # distribute_gui.rpy:157
    old "Build Distributions: [project.current.name!q]"
    new "配布物のビルド: [project.current.name!q]"

    # distribute_gui.rpy:171
    old "Directory Name:"
    new "ディレクトリー名:"

    # distribute_gui.rpy:175
    old "Executable Name:"
    new "実行ファイル名:"

    # distribute_gui.rpy:185
    old "Actions:"
    new "アクション:"

    # distribute_gui.rpy:193
    old "Edit options.rpy"
    new "options.rpyを編集"

    # distribute_gui.rpy:194
    old "Add from clauses to calls, once"
    new "from節をcallに加える"

    # distribute_gui.rpy:195
    old "Refresh"
    new "更新"

    # distribute_gui.rpy:199
    old "Upload to itch.io"
    new "itch.ioにアップロードする"

    # distribute_gui.rpy:215
    old "Build Packages:"
    new "ビルドするパッケージ:"

    # distribute_gui.rpy:234
    old "Options:"
    new "設定:"

    # distribute_gui.rpy:239
    old "Build Updates"
    new "アップデートをビルド"

    # distribute_gui.rpy:241
    old "Add from clauses to calls"
    new "from 節を call ステートメントに加える"

    # distribute_gui.rpy:242
    old "Force Recompile"
    new "強制再コンパイル"

    # distribute_gui.rpy:246
    old "Build"
    new "ビルド"

    # distribute_gui.rpy:250
    old "Adding from clauses to call statements that do not have them."
    new "from 節がない call ステートメントに from 節を加えています"

    # distribute_gui.rpy:271
    old "Errors were detected when running the project. Please ensure the project runs without errors before building distributions."
    new "プロジェクトの実行時にエラーを検出しました。配布物をビルドする前に、エラーなしでプロジェクトが実行するようにしてください。"

    # distribute_gui.rpy:288
    old "Your project does not contain build information. Would you like to add build information to the end of options.rpy?"
    new "プロジェクトにビルド情報がありません。options.rpy の末尾にビルド情報を追加しますか？"

    # editor.rpy:150
    old "{b}Recommended.{/b} A beta editor with an easy to use interface and features that aid in development, such as spell-checking. Editra currently lacks the IME support required for Chinese, Japanese, and Korean text input."
    new "{b}推奨{/b} 使いやすいインターフェースと、スペルチュックのような開発を補助する機能を持つベータエディターです。Editra は現在、中国、韓国、日本語の入力に必要な IME のサポートに欠陥があります。"

    # editor.rpy:151
    old "{b}Recommended.{/b} A beta editor with an easy to use interface and features that aid in development, such as spell-checking. Editra currently lacks the IME support required for Chinese, Japanese, and Korean text input. On Linux, Editra requires wxPython."
    new "{b}推奨{/b} 使いやすいインターフェースと、スペルチュックのような開発を補助する機能を持つベータエディターです。Editra は現在、中国、韓国、日本語の入力に必要な IME のサポートに欠陥があります。Linux では Editra は wxpython を必要とします。"

    # editor.rpy:167
    old "This may have occured because wxPython is not installed on this system."
    new "このエラーは wxPython がこのシステムにインストールされていないため発生したと思われます。"

    # editor.rpy:169
    old "Up to 22 MB download required."
    new "最大 22 MB のダウンロードが必要です。"

    # editor.rpy:182
    old "A mature editor that requires Java."
    new "Java を必要とする成熟したエディターです。"

    # editor.rpy:182
    old "1.8 MB download required."
    new "1.8 MB のダウンロードが必要です。"

    # editor.rpy:182
    old "This may have occured because Java is not installed on this system."
    new "このエラーは Java がこのシステムにインストールされていないため発生しましたと思われます。"

    # editor.rpy:191
    old "Invokes the editor your operating system has associated with .rpy files."
    new "オペレーティングシステムで .rpy ファイルに関連づけたエディターを実行します。"

    # editor.rpy:207
    old "Prevents Ren'Py from opening a text editor."
    new "Ren'Py のテキストエディターの実行を停止します。"

    # editor.rpy:359
    old "An exception occured while launching the text editor:\n[exception!q]"
    new "テキストエディターの選択中にエラーが発生しました:\n[exception!q]"

    # editor.rpy:457
    old "Select Editor"
    new "エディターを選択してください"

    # editor.rpy:472
    old "A text editor is the program you'll use to edit Ren'Py script files. Here, you can select the editor Ren'Py will use. If not already present, the editor will be automatically downloaded and installed."
    new "テキストエディタは Ren'Py スクリプトファイルを編集するためのプログラムです。ここで Ren'Py が使用するエディターを選択できます。選択したエディターが存在しなければ、自動的にダウンロード・インストールされます。"

    # editor.rpy:494
    old "Cancel"
    new "キャンセル"

    # front_page.rpy:35
    old "Open [text] directory."
    new "[text] ディレクトリーを開きます。"

    # front_page.rpy:93
    old "refresh"
    new "更新"

    # front_page.rpy:120
    old "+ Create New Project"
    new "＋新規プロジェクトの作成"

    # front_page.rpy:130
    old "Launch Project"
    new "プロジェクトの起動"

    # front_page.rpy:147
    old "[p.name!q] (template)"
    new "[p.name!q] (テンプレート)"

    # front_page.rpy:149
    old "Select project [text]."
    new "プロジェクト [text] を選択します。"

    # front_page.rpy:165
    old "Tutorial"
    new "Tutorial"

    # front_page.rpy:166
    old "The Question"
    new "The Question"

    # front_page.rpy:182
    old "Active Project"
    new "アクティブなプロジェクト"

    # front_page.rpy:190
    old "Open Directory"
    new "ディレクトリーを開く"

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
    new "ファイルを編集する"

    # front_page.rpy:214
    old "All script files"
    new "すべてのスクリプト"

    # front_page.rpy:223
    old "Navigate Script"
    new "スクリプトナビゲーション"

    # front_page.rpy:234
    old "Check Script (Lint)"
    new "スクリプトチェック(Lint)"

    # front_page.rpy:237
    old "Change/Update GUI"
    new "GUIを変更・更新"

    # front_page.rpy:239
    old "Change Theme"
    new "テーマ変更"

    # front_page.rpy:242
    old "Delete Persistent"
    new "永続データ削除"

    # front_page.rpy:251
    old "Build Distributions"
    new "配布物のビルド"

    # front_page.rpy:253
    old "Android"
    new "Android"

    # front_page.rpy:254
    old "iOS"
    new "iOS"

    # front_page.rpy:255
    old "Generate Translations"
    new "翻訳の生成"

    # front_page.rpy:256
    old "Extract Dialogue"
    new "台詞の抽出"

    # front_page.rpy:272
    old "Checking script for potential problems..."
    new "スクリプトの潜在的な問題をチェックしています…"

    # front_page.rpy:287
    old "Deleting persistent data..."
    new "永続データを削除しています…"

    # front_page.rpy:295
    old "Recompiling all rpy files into rpyc files..."
    new "すべての rpy ファイルを rpyc ファイルにコンパイルしています。"

    # gui7.rpy:236
    old "Select Accent and Background Colors"
    new "アクセントカラーとバックグラウンドカラーを選択"

    # gui7.rpy:250
    old "Please click on the color scheme you wish to use, then click Continue. These colors can be changed and customized later."
    new "使用したいカラースキームをクリックした後、続行をクリックしてください。カラーは後で変更・カスタマイズすることができます。"

    # gui7.rpy:294
    old "{b}Warning{/b}\nContinuing will overwrite customized bar, button, save slot, scrollbar, and slider images.\n\nWhat would you like to do?"
    new "{b}警告{/b}\n続行すると、カスタマイズしたバー・ボタン・セーブスロット・スクロールバー・スライダーの画像が上書きされます。\n\nそれでもよろしいでしょうか？"

    # gui7.rpy:294
    old "Choose new colors, then regenerate image files."
    new "新しいカラーを選び、画像を再生成する"

    # gui7.rpy:294
    old "Regenerate the image files using the colors in gui.rpy."
    new "gui.rpy のカラーを元に、画像を再生成する"

    # gui7.rpy:314
    old "PROJECT NAME"
    new "プロジェクト名"

    # gui7.rpy:314
    old "Please enter the name of your project:"
    new "プロジェクト名を入力してください:"

    # gui7.rpy:322
    old "The project name may not be empty."
    new "プロジェクト名が空です。"

    # gui7.rpy:327
    old "[project_name!q] already exists. Please choose a different project name."
    new "[project_name!q] は既に存在します。違う名前を選択してください。"

    # gui7.rpy:330
    old "[project_dir!q] already exists. Please choose a different project name."
    new "[project_dir!q] は既に存在します。違う名前を選択してください。"

    # gui7.rpy:341
    old "What resolution should the project use? Although Ren'Py can scale the window up and down, this is the initial size of the window, the size at which assets should be drawn, and the size at which the assets will be at their sharpest.\n\nThe default of 1280x720 is a reasonable compromise."
    new "どの解像度をこのプロジェクトに使用しますか？ Ren'py はウィンドウを拡大縮小することができますが、この設定は最初のウィンドウサイズ、描画される各アセットのサイズ、アセットが最もシャープに見えるサイズを決定します。\n\nデフォルトの 1280x720 が理にかなった推奨サイズです。"

    # gui7.rpy:389
    old "Creating the new project..."
    new "新しいプロジェクトを作成中…"

    # gui7.rpy:391
    old "Updating the project..."
    new "プロジェクトを更新しています…"

    # interface.rpy:107
    old "Documentation"
    new "ドキュメント"

    # interface.rpy:108
    old "Ren'Py Website"
    new "Ren'Pyサイト"

    # interface.rpy:109
    old "Ren'Py Games List"
    new "Ren'Pyゲームリスト"

    # interface.rpy:117
    old "update"
    new "アップデート"

    # interface.rpy:119
    old "preferences"
    new "設定"

    # interface.rpy:120
    old "quit"
    new "終了"

    # interface.rpy:232
    old "Due to package format limitations, non-ASCII file and directory names are not allowed."
    new "パッケージフォーマットの制限により、アスキーコード以外のファイル、ディレクトリー名は許可されません。"

    # interface.rpy:327
    old "ERROR"
    new "エラー"

    # interface.rpy:356
    old "While [what!qt], an error occured:"
    new "[what!qt] 中にエラーが発生しました:"

    # interface.rpy:356
    old "[exception!q]"
    new "[exception!q]"

    # interface.rpy:375
    old "Text input may not contain the {{ or [[ characters."
    new "{{ または [[ はテキスト入力出来ません。"

    # interface.rpy:380
    old "File and directory names may not contain / or \\."
    new "ファイル、ディレクトリーが / または \\. を含んでいるかもしれません。"

    # interface.rpy:386
    old "File and directory names must consist of ASCII characters."
    new "ファイル、ディレクトリー名はアスキーコードの文字列でなければなりません。"

    # interface.rpy:454
    old "PROCESSING"
    new "処理中"

    # interface.rpy:471
    old "QUESTION"
    new "質問"

    # interface.rpy:484
    old "CHOICE"
    new "選択"

    # ios.rpy:28
    old "To build iOS packages, please download renios, unzip it, and place it into the Ren'Py directory. Then restart the Ren'Py launcher."
    new "iOS パッケージをビルドするには、  renios をダウンロードして、Ren'Py ディレクトリーに配置、ランチャーを再起動してください。"

    # ios.rpy:29
    old "The directory in where Xcode projects will be placed has not been selected. Choose 'Select Directory' to select it."
    new "'Select Directory' から、 xcode プロジェクトが配置されるディレクトリーを選択してください。"

    # ios.rpy:30
    old "There is no Xcode project corresponding to the current Ren'Py project. Choose 'Create Xcode Project' to create one."
    new "現在の Ren'Py プロジェクトに対応する Xcode プロジェクトがありません。'Create Xcode Project' から作成してください。"

    # ios.rpy:31
    old "An Xcode project exists. Choose 'Update Xcode Project' to update it with the latest game files, or use Xcode to build and install it."
    new "Xcode プロジェクトが存在します。'Update Xcode Project' を選択して最新のゲームファイルに更新するか、 Xcode を使用してそれをビルド、インストールしてください。"

    # ios.rpy:33
    old "Attempts to emulate an iPhone.\n\nTouch input is emulated through the mouse, but only when the button is held down."
    new "iPhone をエミュレートします。\n\nタッチ入力のエミュレートはマウスを利用しますが、ボタン押下時のみ反応します"

    # ios.rpy:34
    old "Attempts to emulate an iPad.\n\nTouch input is emulated through the mouse, but only when the button is held down."
    new "iPad をエミュレートします。\n\nタッチ入力のエミュレートはマウスを利用しますが、ボタン押下時のみ反応します"

    # ios.rpy:36
    old "Selects the directory where Xcode projects will be placed."
    new "Xcode プロジェクトが配置されるディレクトリーを選択します。"

    # ios.rpy:37
    old "Creates an Xcode project corresponding to the current Ren'Py project."
    new "現在の Ren'PY プロジェクトに対応する Xcode プロジェクトを作成します。"

    # ios.rpy:38
    old "Updates the Xcode project with the latest game files. This must be done each time the Ren'Py project changes."
    new "最新のゲームファイルに Xcode プロジェクトを更新します。更新は Ren'Py プロジェクトが変更される度に行わなければなりません。"

    # ios.rpy:39
    old "Opens the Xcode project in Xcode."
    new "Xcode から Xcode プロジェクトを開きます。"

    # ios.rpy:41
    old "Opens the directory containing Xcode projects."
    new "対応する Xcode プロジェクトを開きます。"

    # ios.rpy:126
    old "The Xcode project already exists. Would you like to rename the old project, and replace it with a new one?"
    new "その Xcode プロジェクトは既に存在します。古いプロジェクトをリネームするか、新しいもので置き換えますか？"

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
    new "Xcode プロジェクトディレクトリー選択"

    # ios.rpy:268
    old "Create Xcode Project"
    new "Xcode プロジェクト作成"

    # ios.rpy:272
    old "Update Xcode Project"
    new "Xcode プロジェクト更新"

    # ios.rpy:277
    old "Launch Xcode"
    new "Xcode 起動"

    # ios.rpy:312
    old "Open Xcode Projects Directory"
    new "Xcode プロジェクトディレクトリー開く"

    # ios.rpy:345
    old "Before packaging iOS apps, you'll need to download renios, Ren'Py's iOS support. Would you like to download renios now?"
    new "iOS アプリをパッケージする前に、renios をダウンロードする必要があります。 renios をダウンロードしますか？"

    # ios.rpy:354
    old "XCODE PROJECTS DIRECTORY"
    new "XCODE PROJECTS DIRECTORY"

    # ios.rpy:354
    old "Please choose the Xcode Projects Directory using the directory chooser.\n{b}The directory chooser may have opened behind this window.{/b}"
    new "Xcode プロジェクトディレクトリーを選択してください。\n{b}ディレクトリー選択ウィンドウはこのウィンドウの裏に開くかもしれません。{/b}"

    # ios.rpy:359
    old "Ren'Py has set the Xcode Projects Directory to:"
    new "Ren'Py は Xcode プロジェクトディレクトリーを以下に設定しました:"

    # itch.rpy:60
    old "The built distributions could not be found. Please choose 'Build' and try again."
    new "ビルドされた配布物が見つかりません。ビルドを選択し、やり直してください。"

    # itch.rpy:91
    old "No uploadable files were found. Please choose 'Build' and try again."
    new "アップロードできるファイルが見つかりません。ビルドを選択し、やり直してください。"

    # itch.rpy:99
    old "The butler program was not found."
    new "butler プログラムが見つかりません。"

    # itch.rpy:99
    old "Please install the itch.io app, which includes butler, and try again."
    new "butler を含む itch.io app をインストールして、やり直してください。"

    # itch.rpy:108
    old "The name of the itch project has not been set."
    new "itch project の名前が設定されていません。"

    # itch.rpy:108
    old "Please {a=https://itch.io/game/new}create your project{/a}, then add a line like \n{vspace=5}define build.itch_project = \"user-name/game-name\"\n{vspace=5} to options.rpy."
    new "{a=https://itch.io/game/new}プロジェクトを作成{/a}して、options.rpy に次のような命令を追加してください。\n{vspace=5}define build.itch_project = \"user-name/game-name\"\n{vspace=5}"

    # mobilebuild.rpy:109
    old "{a=%s}%s{/a}"
    new "{a=%s}%s{/a}"

    # navigation.rpy:168
    old "Navigate: [project.current.name]"
    new "ナビゲーション: [project.current.name]"

    # navigation.rpy:177
    old "Order: "
    new "並び順:"

    # navigation.rpy:178
    old "alphabetical"
    new "アルファベット順"

    # navigation.rpy:180
    old "by-file"
    new "ファイル順"

    # navigation.rpy:182
    old "natural"
    new "記載順"

    # navigation.rpy:194
    old "Category:"
    new "カテゴリー:"

    # navigation.rpy:196
    old "files"
    new "ファイル"

    # navigation.rpy:197
    old "labels"
    new "ラベル"

    # navigation.rpy:198
    old "defines"
    new "定義"

    # navigation.rpy:199
    old "transforms"
    new "変換"

    # navigation.rpy:200
    old "screens"
    new "スクリーン"

    # navigation.rpy:201
    old "callables"
    new "関数"

    # navigation.rpy:202
    old "TODOs"
    new "TODO"

    # navigation.rpy:241
    old "+ Add script file"
    new "＋スクリプトファイルを追加する。"

    # navigation.rpy:249
    old "No TODO comments found.\n\nTo create one, include \"# TODO\" in your script."
    new "TODO コメントは見つかりません。\n\n作成には \"# TODO\" をスクリプトに加えてください。"

    # navigation.rpy:256
    old "The list of names is empty."
    new "名前のリストはありません。"

    # new_project.rpy:38
    old "New GUI Interface"
    new "New GUI インターフェース"

    # new_project.rpy:48
    old "Both interfaces have been translated to your language."
    new "どちらのインターフェースも日本語に翻訳されています。"

    # new_project.rpy:50
    old "Only the new GUI has been translated to your language."
    new "New GUI のみが日本語に翻訳されています。"

    # new_project.rpy:52
    old "Only the legacy theme interface has been translated to your language."
    new "Legacy Theme のみが日本語に翻訳されています。"

    # new_project.rpy:54
    old "Neither interface has been translated to your language."
    new "どちらのインターフェースも日本語に翻訳されていません。"

    # new_project.rpy:63
    old "The projects directory could not be set. Giving up."
    new "プロジェクトディレクトリーを設定出来ません。キャンセルします。"

    # new_project.rpy:69
    old "Which interface would you like to use? The new GUI has a modern look, supports wide screens and mobile devices, and is easier to customize. Legacy themes might be necessary to work with older example code.\n\n[language_support!t]\n\nIf in doubt, choose the new GUI, then click Continue on the bottom-right."
    new "どちらのインターフェースを使用しますか？ New GUI はモダンな外見で、ワイドスクリーンとモバイルデバイスをサポートし、カスタマイズも容易です。Legacy Theme は古いコード例を利用するのに必要になるでしょう。\n\n[language_support!t]\n\n判断がつかない場合は、New GUI を選択して、右下の続行をクリックしてください。"

    # new_project.rpy:69
    old "Legacy Theme Interface"
    new "Legacy Theme インターフェース"

    # new_project.rpy:90
    old "Choose Project Template"
    new "テンプレートを選んでください"

    # new_project.rpy:108
    old "Please select a template to use for your new project. The template sets the default font and the user interface language. If your language is not supported, choose 'english'."
    new "新しいプロジェクトで使用するテンプレートを選択してください。Ren'Py はデフォルトのフォントとユーザーインターフェイスの言語を設定します。あなたの言語がサポートされていないなら 'english' を選択してください。"

    # preferences.rpy:64
    old "Launcher Preferences"
    new "ランチャー設定"

    # preferences.rpy:85
    old "Projects Directory:"
    new "プロジェクトディレクトリー:"

    # preferences.rpy:92
    old "[persistent.projects_directory!q]"
    new "[persistent.projects_directory!q]"

    # preferences.rpy:94
    old "Projects directory: [text]"
    new "プロジェクトディレクトリー: [text]"

    # preferences.rpy:96
    old "Not Set"
    new "未設定"

    # preferences.rpy:111
    old "Text Editor:"
    new "テキストエディター:"

    # preferences.rpy:117
    old "Text editor: [text]"
    new "テキストエディター: [text]"

    # preferences.rpy:133
    old "Update Channel:"
    new "アップデートチャンネル:"

    # preferences.rpy:153
    old "Navigation Options:"
    new "ナビゲーション設定:"

    # preferences.rpy:157
    old "Include private names"
    new "内部使用の名前を含める"

    # preferences.rpy:158
    old "Include library names"
    new "ライブラリの名前を含める"

    # preferences.rpy:168
    old "Launcher Options:"
    new "ランチャー設定:"

    # preferences.rpy:172
    old "Hardware rendering"
    new "ハードウェアレンダリング"

    # preferences.rpy:173
    old "Show templates"
    new "テンプレートの表示"

    # preferences.rpy:174
    old "Show edit file section"
    new "ファイル編集を表示する"

    # preferences.rpy:175
    old "Large fonts"
    new "フォントを大きくする"

    # preferences.rpy:178
    old "Console output"
    new "コンソール出力"

    # preferences.rpy:199
    old "Open launcher project"
    new "ランチャーのプロジェクトを開く"

    # preferences.rpy:213
    old "Language:"
    new "言語:"

    # project.rpy:47
    old "After making changes to the script, press shift+R to reload your game."
    new "スクリプトに変更を加えた後、Shift+R を押すとゲームをリロードします。"

    # project.rpy:47
    old "Press shift+O (the letter) to access the console."
    new "Shift+O（英字）を押すとコンソールを表示します。"

    # project.rpy:47
    old "Press shift+D to access the developer menu."
    new "Shift+D を押すと開発者メニューを表示します。"

    # project.rpy:47
    old "Have you backed up your projects recently?"
    new "最近ゲームのバックアップはしましたか？"

    # project.rpy:229
    old "Launching the project failed."
    new "プロジェクトの起動に失敗しました。"

    # project.rpy:229
    old "Please ensure that your project launches normally before running this command."
    new "このコマンドを実行する前に、プロジェクトが通常通り起動することを確認して下さい。"

    # project.rpy:242
    old "Ren'Py is scanning the project..."
    new "Ren'Py プロジェクトをスキャンしています…"

    # project.rpy:568
    old "Launching"
    new "起動中"

    # project.rpy:597
    old "PROJECTS DIRECTORY"
    new "プロジェクトディレクトリー"

    # project.rpy:597
    old "Please choose the projects directory using the directory chooser.\n{b}The directory chooser may have opened behind this window.{/b}"
    new "プロジェクトディレクトリーを選択してください。\n{b}ディレクトリー選択画面がこのウィンドウの下に隠れている場合があります。{/b}"

    # project.rpy:597
    old "This launcher will scan for projects in this directory, will create new projects in this directory, and will place built projects into this directory."
    new "ランチャーはこのディレクトリーでプロジェクトをスキャンし、新しいプロジェクトを作成し、ビルドしたプロジェクトを出力します。"

    # project.rpy:602
    old "Ren'Py has set the projects directory to:"
    new "Ren'Py は以下にプロジェクトディレクトリーを設定します:"

    # translations.rpy:63
    old "Translations: [project.current.name!q]"
    new "翻訳: [project.current.name!q]"

    # translations.rpy:104
    old "The language to work with. This should only contain lower-case ASCII characters and underscores."
    new "翻訳に使う言語。半角小文字の ASCII 文字とアンダースコアのみが使用できます。"

    # translations.rpy:130
    old "Generate empty strings for translations"
    new "翻訳を空の文字列で生成する"

    # translations.rpy:148
    old "Generates or updates translation files. The files will be placed in game/tl/[persistent.translate_language!q]."
    new "翻訳ファイルを生成、または更新します。翻訳ファイルは、game/tl/[persistent.translate_language!q] に置かれます。"

    # translations.rpy:168
    old "Extract String Translations"
    new "文字列の翻訳を抽出"

    # translations.rpy:170
    old "Merge String Translations"
    new "文字列の翻訳を併合"

    # translations.rpy:175
    old "Replace existing translations"
    new "既にある翻訳を置き換える"

    # translations.rpy:176
    old "Reverse languages"
    new "言語を反転させる"

    # translations.rpy:180
    old "Update Default Interface Translations"
    new "デフォルトインターフェースの翻訳を更新する"

    # translations.rpy:200
    old "The extract command allows you to extract string translations from an existing project into a temporary file.\n\nThe merge command merges extracted translations into another project."
    new "抽出コマンドは、既存のプロジェクトから文字列の翻訳（台詞以外の翻訳）を一時ファイルとして抽出します。\n\n併合コマンドは、抽出した翻訳を他のプロジェクトに併合します。"

    # translations.rpy:224
    old "Ren'Py is generating translations...."
    new "Ren'Py は翻訳を生成しています…"

    # translations.rpy:235
    old "Ren'Py has finished generating [language] translations."
    new "Ren'Py は [language] の翻訳ファイルを生成しました。"

    # translations.rpy:248
    old "Ren'Py is extracting string translations..."
    new "Ren'Py は文字列の翻訳を抽出しています…"

    # translations.rpy:251
    old "Ren'Py has finished extracting [language] string translations."
    new "Ren'Py は [language] の文字列の翻訳を抽出しました。"

    # translations.rpy:271
    old "Ren'Py is merging string translations..."
    new "Ren'Py は文字列の翻訳を併合しています…"

    # translations.rpy:274
    old "Ren'Py has finished merging [language] string translations."
    new "Ren'Py は [language] の文字列の翻訳を併合しました。"

    # translations.rpy:282
    old "Updating default interface translations..."
    new "デフォルトインターフェースの翻訳を更新しています…"

    # translations.rpy:306
    old "Extract Dialogue: [project.current.name!q]"
    new "台詞の抽出: [project.current.name!q]"

    # translations.rpy:322
    old "Format:"
    new "フォーマット:"

    # translations.rpy:330
    old "Tab-delimited Spreadsheet (dialogue.tab)"
    new "タブ区切りのスプレッドシート (dialogue.tab)"

    # translations.rpy:331
    old "Dialogue Text Only (dialogue.txt)"
    new "台詞のテキストのみ (dialogue.txt)"

    # translations.rpy:344
    old "Strip text tags from the dialogue."
    new "台詞からテキストタグを取り除く"

    # translations.rpy:345
    old "Escape quotes and other special characters."
    new "引用符や他の特殊文字をエスケープする"

    # translations.rpy:346
    old "Extract all translatable strings, not just dialogue."
    new "台詞だけでなく、翻訳可能なすべての文字列を抽出する"

    # translations.rpy:374
    old "Ren'Py is extracting dialogue...."
    new "Ren'Py は台詞を抽出しています…"

    # translations.rpy:378
    old "Ren'Py has finished extracting dialogue. The extracted dialogue can be found in dialogue.[persistent.dialogue_format] in the base directory."
    new "Ren'Py は台詞の抽出を終了しました。抽出した台詞は、base ディレクトリーの、[persistent.dialogue_format] にあります。"

    # updater.rpy:75
    old "Select Update Channel"
    new "アップデートチャンネルを選択してください"

    # updater.rpy:86
    old "The update channel controls the version of Ren'Py the updater will download. Please select an update channel:"
    new "アップデートチャンネルはアップデーターがダウンロードする Ren'Py のバージョンを制御します。アップデートチャンネルを選択してください。"

    # updater.rpy:91
    old "Release"
    new "Release"

    # updater.rpy:97
    old "{b}Recommended.{/b} The version of Ren'Py that should be used in all newly-released games."
    new "{b}推奨{/b} 新しくリリースする全てのゲームに使用すべき Ren'Py のバージョンです。"

    # updater.rpy:102
    old "Prerelease"
    new "Prerelease"

    # updater.rpy:108
    old "A preview of the next version of Ren'Py that can be used for testing and taking advantage of new features, but not for final releases of games."
    new "テストや新機能利用のために使用される Ren'Py の次期バージョンのプレビューです。\nゲームの最終リリースには向きません。"

    # updater.rpy:114
    old "Experimental"
    new "Experimental"

    # updater.rpy:120
    old "Experimental versions of Ren'Py. You shouldn't select this channel unless asked by a Ren'Py developer."
    new "Ren'Py の試験的なバージョンです。開発者に頼まれない限りこのバージョンを使用するべきではありません。"

    # updater.rpy:126
    old "Nightly"
    new "Nightly"

    # updater.rpy:132
    old "The bleeding edge of Ren'Py development. This may have the latest features, or might not run at all."
    new "Ren'Py の開発版で極めて不安定です。このバージョンには最新の機能が含まれていますが、全く動かないかもしれません。"

    # updater.rpy:152
    old "An error has occured:"
    new "エラーが発生しました。"

    # updater.rpy:154
    old "Checking for updates."
    new "更新をチェックしています。"

    # updater.rpy:156
    old "Ren'Py is up to date."
    new "Ren'Py は最新です。"

    # updater.rpy:158
    old "[u.version] is now available. Do you want to install it?"
    new "[u.version] が利用可能です。インストールしますか？"

    # updater.rpy:160
    old "Preparing to download the update."
    new "アップデートのダウンロード準備をしています。"

    # updater.rpy:162
    old "Downloading the update."
    new "アップデートをダウンロードしています。"

    # updater.rpy:164
    old "Unpacking the update."
    new "アップデートを解凍しています。"

    # updater.rpy:166
    old "Finishing up."
    new "更新を完了しました。"

    # updater.rpy:168
    old "The update has been installed. Ren'Py will restart."
    new "アップデートをインストールしました。Ren'Py を再起動します。"

    # updater.rpy:170
    old "The update has been installed."
    new "アップデートをインストールしました。"

    # updater.rpy:172
    old "The update was cancelled."
    new "アップデートをキャンセルしました。"

    # updater.rpy:189
    old "Ren'Py Update"
    new "Ren'Py アップデート"

    # updater.rpy:195
    old "Proceed"
    new "続行"

    # choose_directory.rpy:104
    old "The selected projects directory is not writable."
    new "選択されたプロジェクトディレクトリーは、書き込み不可です。"

    # distribute.rpy:1061
    old "Signing the Macintosh application...\n(This may take a long time.)"
    new "Macintosh application に署名しています…\n（この処理にはしばらくかかります。）"

    # front_page.rpy:91
    old "PROJECTS:"
    new "プロジェクト:"


translate japanese strings:

    # android.rpy:304
    old "Android: [project.current.display_name!q]"
    new "Android: [project.current.display_name!q]"

    # distribute_gui.rpy:157
    old "Build Distributions: [project.current.display_name!q]"
    new "配布物のビルド: [project.current.display_name!q]"

    # interface.rpy:136
    old "Ren'Py Sponsor Information"
    new "Ren'Pyスポンサー情報"

    # ios.rpy:211
    old "iOS: [project.current.display_name!q]"
    new "iOS: [project.current.display_name!q]"

    # navigation.rpy:168
    old "Navigate: [project.current.display_name!q]"
    new "ナビゲーション: [project.current.display_name!q]"

    # new_project.rpy:71
    old "You will be creating an [new_project_language]{#this substitution may be localized} language project. Change the launcher language in preferences to create a project in another language."
    new "日本語のプロジェクトを作成します。別の言語のプロジェクトを作成するには、設定でランチャーの言語を変更してください。"

    # preferences.rpy:187
    old "Force new tutorial"
    new "新チュートリアルを使用"

    # preferences.rpy:189
    old "Legacy options"
    new "古いオプションを表示"

    # preferences.rpy:194
    old "Sponsor message"
    new "スポンサーメッセージ表示"

    # translations.rpy:92
    old "Translations: [project.current.display_name!q]"
    new "翻訳の生成: [project.current.display_name!q]"

    # translations.rpy:337
    old "Extract Dialogue: [project.current.display_name!q]"
    new "台詞の抽出: [project.current.display_name!q]"


translate japanese strings:

    # dmgcheck.rpy:50
    old "Ren'Py is running from a read only folder. Some functionality will not work."
    new "Ren'Py が読み取り専用フォルダーで起動しています。使えない機能があります。"

    # dmgcheck.rpy:50
    old "This is probably because Ren'Py is running directly from a Macintosh drive image. To fix this, quit this launcher, copy the entire %s folder somewhere else on your computer, and run Ren'Py again."
    new "原因は Ren'Py が Macintosh drive image から直接起動しているためだと思われます.。この問題を解決するには、ランチャーを閉じて %s フォルダー全体をコンピューターのどこか別の場所へ移動してから、もう一度 Ren'Py を起動してみてください。"

    # gui7.rpy:357
    old "Custom. The GUI is optimized for a 16:9 aspect ratio."
    new "カスタム。GUI は 16:9 のアスペクト比に最適化されています。"

    # gui7.rpy:372
    old "WIDTH"
    new "画面の幅"

    # gui7.rpy:372
    old "Please enter the width of your game, in pixels."
    new "ピクセルでゲーム画面の幅を入力してください。"

    # gui7.rpy:377
    old "The width must be a number."
    new "画面の幅は数字でなければなりません。"

    # gui7.rpy:379
    old "HEIGHT"
    new "画面の高さ"

    # gui7.rpy:379
    old "Please enter the height of your game, in pixels."
    new "ピクセルでゲーム画面の高さを入力してください。"

    # gui7.rpy:384
    old "The height must be a number."
    new "画面の高さは数字でなければなりません。"


translate japanese strings:

    # editor.rpy:152
    old "(Recommended) A modern and approachable text editor."
    new "（推奨）モダンで親しみやすいテキストエディターです。"

    # editor.rpy:164
    old "Up to 150 MB download required."
    new "最大 150 MB のダウンロードが必要です。"

    # editor.rpy:178
    old "A mature editor. Editra lacks the IME support required for Chinese, Japanese, and Korean text input."
    new "成熟したエディターです。Editra は中国語・韓国語・日本語の入力に必要な IME のサポートに欠陥があります。"

    # editor.rpy:179
    old "A mature editor. Editra lacks the IME support required for Chinese, Japanese, and Korean text input. On Linux, Editra requires wxPython."
    new "成熟したエディターです。Editra は中国語・韓国語・日本語の入力に必要な IME のサポートに欠陥があります。Linux では Editra は wxpython を必要とします。"

    # editor.rpy:219
    old "System Editor"
    new "システムエディタ―"

    # editor.rpy:235
    old "None"
    new "無効"

    # editor.rpy:338
    old "Edit [text]."
    new "Edit [text]."

    # front_page.rpy:215
    old "Open project"
    new "プロジェクトを開く"

    # front_page.rpy:221
    old "Actions"
    new "アクション"


translate japanese strings:

    # game/add_file.rpy:37
    old "The file name may not be empty."
    new "ファイル名が与えられていません。"

    # game/android.rpy:31
    old "A 64-bit/x64 Java 8 Development Kit is required to build Android packages on Windows. The JDK is different from the JRE, so it's possible you have Java without having the JDK.\n\nPlease {a=http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html}download and install the JDK{/a}, then restart the Ren'Py launcher."
    new "ウィンドウズでアンドロイドパッケージをビルドするには、 64-bit/x64 Java 8 Development Kit が必要になります。 JDK は JRE とは違うもので、Java には含まれていません。\n\n{a=http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html}から JDK をダンロードしてインストールし{/a}、それから Ren'Py ランチャーを再起動してください。"

    # game/android.rpy:50
    old "Selects the Debug build, which can be accessed through Android Studio. Changing between debug and release builds requires an uninstall from your device."
    new "Android Studio からアクセスできるデバッグビルドを選択する。 デバッグビルドとリリースビルドを切り替えるには、デバイスからアンインストールする必要があります。"

    # game/android.rpy:51
    old "Selects the Release build, which can be uploaded to stores. Changing between debug and release builds requires an uninstall from your device."
    new "ストアへアップロード可能なリリースビルドを選択する。 デバッグビルドとリリースビルドを切り替えるには、デバイスからアンインストールする必要があります。"

    # game/androidstrings.rpy:7
    old "{} is not a directory."
    new "{} はディレクトリーではありません。"

    # game/androidstrings.rpy:8
    old "{} does not contain a Ren'Py game."
    new "{} に Ren'Py のゲームは含まれていません。"

    # game/androidstrings.rpy:9
    old "Run configure before attempting to build the app."
    new "アプリをビルドする前に構成を変更する。"

    # game/androidstrings.rpy:10
    old "Google Play support is enabled, but build.google_play_key is not defined."
    new "Google Play サポートは有効になりましたが、 build.google_play_key が定義されていません。"

    # game/androidstrings.rpy:11
    old "Updating project."
    new "プロジェクトを更新しています。"

    # game/androidstrings.rpy:12
    old "Creating assets directory."
    new "アセットディレクトリーを作成しています"

    # game/androidstrings.rpy:13
    old "Creating expansion file."
    new "拡張ファイルを作成しています。"

    # game/androidstrings.rpy:14
    old "Packaging internal data."
    new "内部データをパッケージングしています。"

    # game/androidstrings.rpy:15
    old "I'm using Gradle to build the package."
    new "パッケージのビルドに Gradle を使用しています。"

    # game/androidstrings.rpy:16
    old "Uploading expansion file."
    new "拡張ファイルをアップロードしています。"

    # game/androidstrings.rpy:17
    old "The build seems to have failed."
    new "ビルドに失敗したようです"

    # game/androidstrings.rpy:18
    old "Launching app."
    new "アプリを起動しています。"

    # game/androidstrings.rpy:19
    old "The build seems to have succeeded."
    new "ビルドに成功したようです。"

    # game/androidstrings.rpy:20
    old "The arm64-v8a version works on newer Android devices, the armeabi-v7a version works on older devices, and the x86_64 version works on the simulator and chromebooks."
    new "arm64-v8a version は新しいアンドロイドデバイスで動きます。 armeabi-v7a version は古いデバイスで動きます。 the x86_64 version はシミュレーターやクロームブックで動きます。"

    # game/androidstrings.rpy:21
    old "What is the full name of your application? This name will appear in the list of installed applications."
    new "アプリのフルネームはなんですか？ フルネームはインストール済みアプリの一覧に表示されます。"

    # game/androidstrings.rpy:22
    old "What is the short name of your application? This name will be used in the launcher, and for application shortcuts."
    new "アプリのショートネームは何ですか？　ショートネームはランチャーやショートカットで使われます。"

    # game/androidstrings.rpy:23
    old "What is the name of the package?\n\nThis is usually of the form com.domain.program or com.domain.email.program. It may only contain ASCII letters and dots. It must contain at least one dot."
    new "パッケージ名はなんですか？\n\nこれは通常 com.domain.program や com.domain.email.program の形を取ります。 ASCII 文字とドットのみで構成され、最低一つのドットを含まなければなりません。"

    # game/androidstrings.rpy:24
    old "The package name may not be empty."
    new "パッケージ名が与えられていません。"

    # game/androidstrings.rpy:25
    old "The package name may not contain spaces."
    new "パッケージ名はスペースを含んではいけません。"

    # game/androidstrings.rpy:26
    old "The package name must contain at least one dot."
    new "パッケージ名は最低一つのドットを含まなければなりません。"

    # game/androidstrings.rpy:27
    old "The package name may not contain two dots in a row, or begin or end with a dot."
    new "パッケージ名は２つのドットが連続したり、最初や最後がドットになってはいけません。"

    # game/androidstrings.rpy:28
    old "Each part of the package name must start with a letter, and contain only letters, numbers, and underscores."
    new "パッケージ名の各部分は文字から始めまり、文字・数字・アンダースコアのみを使用しなければなりません"

    # game/androidstrings.rpy:29
    old "{} is a Java keyword, and can't be used as part of a package name."
    new "{} は Java のキーワードのため、パッケージ名に使用することはできません。."

    # game/androidstrings.rpy:30
    old "What is the application's version?\n\nThis should be the human-readable version that you would present to a person. It must contain only numbers and dots."
    new "アプリケーションのバージョンはなんですか？\n\nバージョンは他の人に分かりやすい名前にします。数字とドットのみが使用できます。"

    # game/androidstrings.rpy:31
    old "The version number must contain only numbers and dots."
    new "バージョンナンバーは数字とドットのみが使用できます。"

    # game/androidstrings.rpy:32
    old "What is the version code?\n\nThis must be a positive integer number, and the value should increase between versions."
    new "バージョンコードは何ですか？\n\nこれは正の整数で、バージョンが上がるごとに増えていきます。"

    # game/androidstrings.rpy:33
    old "The numeric version must contain only numbers."
    new "バージョンコードは数字のみが使用できます。"

    # game/androidstrings.rpy:34
    old "How would you like your application to be displayed?"
    new "どのようにアプリケーションを表示したいですか？"

    # game/androidstrings.rpy:35
    old "In landscape orientation."
    new "ランドスケープ（横向き）"

    # game/androidstrings.rpy:36
    old "In portrait orientation."
    new "ポートレイト（縦向き）"

    # game/androidstrings.rpy:37
    old "In the user's preferred orientation."
    new "ユーザーが選択した向き"

    # game/androidstrings.rpy:38
    old "Which app store would you like to support in-app purchasing through?"
    new "アプリ内課金をどのアプリストアに対応させますか？"

    # game/androidstrings.rpy:39
    old "Google Play."
    new "Google Play"

    # game/androidstrings.rpy:40
    old "Amazon App Store."
    new "Amazon App Store"

    # game/androidstrings.rpy:41
    old "Both, in one app."
    new "一つのアプリで両方とも"

    # game/androidstrings.rpy:42
    old "Neither."
    new "どちらも対応させない"

    # game/androidstrings.rpy:43
    old "Would you like to create an expansion APK?"
    new "APK 拡張ファイルを作成しますか？"

    # game/androidstrings.rpy:44
    old "No. Size limit of 100 MB on Google Play, but can be distributed through other stores and sideloaded."
    new "いいえ。Google Play では１００ＭＢのサイズ制限がありますが、他のストアを通したり、直接配布することが可能です。"

    # game/androidstrings.rpy:45
    old "Yes. 2 GB size limit, but won't work outside of Google Play. (Read the documentation to get this to work.)"
    new "はい。２ＧＢのサイズまで作成できますが、 Google Play 以外では動きません。（ドキュメンテーションを参照してください。）"

    # game/androidstrings.rpy:46
    old "Do you want to allow the app to access the Internet?"
    new "アプリのインターネット接続を許可しますか？"

    # game/androidstrings.rpy:47
    old "Do you want to automatically update the generated project?"
    new "作成したプロジェクトを自動的に更新させますか？"

    # game/androidstrings.rpy:48
    old "Yes. This is the best choice for most projects."
    new "はい。多くのプロジェクトで最良の選択です。"

    # game/androidstrings.rpy:49
    old "No. This may require manual updates when Ren'Py or the project configuration changes."
    new "いいえ。Ren'Py やプロジェクトの構成が変更されるごとに、手動でアップデートする必要があります。"

    # game/androidstrings.rpy:50
    old "Unknown configuration variable: {}"
    new "未知の構成変数: {}"

    # game/androidstrings.rpy:51
    old "I'm compiling a short test program, to see if you have a working JDK on your system."
    new "小さなテストプログラムをコンパイルして、あなたのシステムで JDK が動作するか確認しています。"

    # game/androidstrings.rpy:52
    old "I was unable to use javac to compile a test file. If you haven't installed the Java Development Kit yet, please download it from:\n\nhttp://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html\n\nThe JDK is different from the JRE, so it's possible you have Java without having the JDK. Without a working JDK, I can't continue."
    new "テストファイルのコンパイルに javac が利用できません。Java Development Kit をダウンロードしていないなら、\n\nhttp://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html\n\nからダウンロードしてください。 JDK は JRE とは違うもので、Java には含まれていません。JDK がなければ継続できません。"

    # game/androidstrings.rpy:53
    old "The version of Java on your computer does not appear to be JDK 8, which is the only version supported by the Android SDK. If you need to install JDK 8, you can download it from:\n\nhttp://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html\n\nYou can also set the JAVA_HOME environment variable to use a different version of Java."
    new "あなたのコンピューターにある Java のバージョンは JDK 8 ではないようです。JDK 8 は Android SDK がサポートする唯一のバージョンです。JDK 8 は:\n\nhttp://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html\n\nからダウンロードできます。 異なるバージョンの JAVA を使う場合は、JAVA_HOME の環境変数を設定します。"

    # game/androidstrings.rpy:54
    old "The JDK is present and working. Good!"
    new "JDK が動作することを確認しました。"

    # game/androidstrings.rpy:55
    old "The Android SDK has already been unpacked."
    new "Android SDK の解凍は完了しています。"

    # game/androidstrings.rpy:56
    old "Do you accept the Android SDK Terms and Conditions?"
    new "Android SDK の契約内容・条件を承諾しますか？"

    # game/androidstrings.rpy:57
    old "I'm downloading the Android SDK. This might take a while."
    new "Android SDK をダウンロードしています。この処理にはしばらくかかります。"

    # game/androidstrings.rpy:58
    old "I'm extracting the Android SDK."
    new "Android SDK を解凍しています。"

    # game/androidstrings.rpy:59
    old "I've finished unpacking the Android SDK."
    new "Android SDK の解凍を完了しました。"

    # game/androidstrings.rpy:60
    old "I'm about to download and install the required Android packages. This might take a while."
    new "必要な Android パッケージをダウンロードしてインストールしようとしています。この処理にはしばらくかかります。"

    # game/androidstrings.rpy:61
    old "I was unable to accept the Android licenses."
    new "Android ライセンスを承諾出来ませんでした。"

    # game/androidstrings.rpy:62
    old "I was unable to install the required Android packages."
    new "必要な Android パッケージをインストールできませんでした。"

    # game/androidstrings.rpy:63
    old "I've finished installing the required Android packages."
    new "必要な Android パッケージのインストールが終了しました。"

    # game/androidstrings.rpy:64
    old "You set the keystore yourself, so I'll assume it's how you want it."
    new "keystore が設定されているため、あなた自身で設定したいのだと判断しました。"

    # game/androidstrings.rpy:65
    old "You've already created an Android keystore, so I won't create a new one for you."
    new "Android keystore が既に作成済みのため、新しい keystore の作成は行いません。"

    # game/androidstrings.rpy:66
    old "I can create an application signing key for you. Signing an application with this key allows it to be placed in the Android Market and other app stores.\n\nDo you want to create a key?"
    new "アプリケーションに署名するキーを発行できます。このキーでアプリケーションに署名すると、アンドロイドマーケットや他のストアで配布できるようになります。\n\nキーを作成しますか？"

    # game/androidstrings.rpy:67
    old "I will create the key in the android.keystore file.\n\nYou need to back this file up. If you lose it, you will not be able to upgrade your application.\n\n\\You also need to keep the key safe. If evil people get this file, they could make fake versions of your application, and potentially steal your users' data.\n\nWill you make a backup of android.keystore, and keep it in a safe place?"
    new "android.keystore ファイルを作成します。\n\nこのファイルはバックアップしてください。もし失くした場合はアプリをアップグレードすることが出来なくなります。\n\nまた、このファイルは安全な場所に保管してください。このファイルが悪意のある人間の手に渡ると、アプリのフェイクバージョンを作られたり、ユーザーデータを盗まれる恐れがあります。\n\nandroid.keystore のバックアップを作成し、安全な場所に保存しますか？"

    # game/androidstrings.rpy:68
    old "Please enter your name or the name of your organization."
    new "あなたの名前か組織名を入力してください。"

    # game/androidstrings.rpy:69
    old "Could not create android.keystore. Is keytool in your path?"
    new "android.keystore を作成できませんでした。keytool があなたのパスに存在しますか？"

    # game/androidstrings.rpy:70
    old "I've finished creating android.keystore. Please back it up, and keep it in a safe place."
    new "android.keystore の作成を終了しました。 このファイルをバックアップして、安全な場所に保管してください。"

    # game/androidstrings.rpy:71
    old "It looks like you're ready to start packaging games."
    new "ゲームのパッケージングの準備が整ったようです。"

    # game/choose_theme.rpy:507
    old "changing the theme"
    new "テーマを変更しています。"

    # game/front_page.rpy:252
    old "Web"
    new "Web"

    # game/front_page.rpy:252
    old "(Beta)"
    new "(Beta)"

    # game/gui7.rpy:429
    old "creating a new project"
    new "新しいプロジェクトを作成しています。"

    # game/gui7.rpy:433
    old "activating the new project"
    new "新しいプロジェクトを認証しています。"

    # game/interface.rpy:372
    old "opening the log file"
    new "ログファイルを開いています。"

    # game/itch.rpy:43
    old "Downloading the itch.io butler."
    new "itch.io butler をダウンロードしています。"

    # game/updater.rpy:101
    old "The update channel controls the version of Ren'Py the updater will download."
    new "アップロードチャンネルはアップデーターのバージョンをコントロールします。"

    # game/updater.rpy:110
    old "• This version is installed and up-to-date."
    new "• このバージョンは最新の状態でインストールされています。"

    # game/updater.rpy:118
    old "%B %d, %Y"
    new "%B %d, %Y"

    # game/updater.rpy:188
    old "Fetching the list of update channels"
    new "アップデートチャンネルのリストを取得しています。"

    # game/updater.rpy:194
    old "downloading the list of update channels"
    new "アップデートチャンネルのリストをダウンロードしています。"

    # game/updater.rpy:198
    old "parsing the list of update channels"
    new "アップデートチャンネルのリストを解析しています。"

    # game/web.rpy:118
    old "Web: [project.current.display_name!q]"
    new "Web: [project.current.display_name!q]"

    # game/web.rpy:148
    old "Build Web Application"
    new "ウェブアプリケーションをビルドする"

    # game/web.rpy:149
    old "Build and Open in Browser"
    new "ビルドしてブラウザで開く"

    # game/web.rpy:150
    old "Open in Browser"
    new "ブラウザで開く"

    # game/web.rpy:151
    old "Open build directory"
    new "ビルドしたディレクトリーを開く"

    # game/web.rpy:155
    old "Support:"
    new "サポート:"

    # game/web.rpy:163
    old "RenPyWeb Home"
    new "RenPyWeb ホーム"

    # game/web.rpy:164
    old "Beuc's Patreon"
    new "Beuc's Patreon"

    # game/web.rpy:182
    old "Ren'Py web applications require the entire game to be downloaded to the player's computer before it can start."
    new "Ren'Py ウェブアプリケーションは、ゲームをスタートする前に、プレイヤーのコンピューターにデータを全てダウンロードする必要があります。"

    # game/web.rpy:186
    old "Current limitations in the web platform mean that loading large images, audio files, or movies may cause audio or framerate glitches, and lower performance in general."
    new "現在のウェブプラットホームの限界により、一般的なパフォーマンスの低下や、大きな画像・音声・動画ファイルのロードによる音声やフレームレートの異常が発生します。"

    # game/web.rpy:195
    old "Before packaging web apps, you'll need to download RenPyWeb, Ren'Py's web support. Would you like to download RenPyWeb now?"
    new "ウェブアプリをパッケージングするために、RenPyWeb (Ren'Py's web support) をダウンロードする必要があります。 RenPyWeb をダウンロードしますか？"

