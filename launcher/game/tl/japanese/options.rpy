
translate japanese strings:

    # options.rpy:1
    old "## This file contains options that can be changed to customize your game."
    new "## このファイルはゲームをカスタマイズする基本的なオプションを記載しています。"

    # options.rpy:4
    old "## Lines beginning with two '#' marks are comments, and you shouldn't uncomment them. Lines beginning with a single '#' mark are commented-out code, and you may want to uncomment them when appropriate."
    new "## 二つの'#'で始まる行はコメントなのでアンコメント（#を消してコメントをコードに戻すこと）してはいけません。一つの'#'で始まる行はコメントアウト（#を加えてコードをコメント化し、実行できなくすること）されたコードで、必要に応じてアンコメントできます。"

    # options.rpy:10
    old "## Basics"
    new "## 基本"

    # options.rpy:12
    old "## A human-readable name of the game. This is used to set the default window title, and shows up in the interface and error reports."
    new "## 人の目で読み取れるゲーム名。ゲーム名はデフォルトのウィンドウタイトルに使われる他、インターフェースやエラーリポートにも表示されます。"

    # options.rpy:15
    old "## The _() surrounding the string marks it as eligible for translation."
    new "## _() で囲まれた文字列は翻訳時に生成されるファイルに記載されます。"

    # options.rpy:17
    old "Ren'Py 7 Default GUI"
    new "Ren'Py 7 デフォルトのGUI"

    # options.rpy:20
    old "## Determines if the title given above is shown on the main menu screen. Set this to False to hide the title."
    new "## 上で定義したタイトルをメインメニュースクリーン（ゲーム起動後、最初に表示されるスクリーン）に表示するかどうか決めます。False にすると表示しません。"

    # options.rpy:26
    old "## The version of the game."
    new "## ゲームのバージョン。"

    # options.rpy:31
    old "## Text that is placed on the game's about screen. To insert a blank line between paragraphs, write \\n\\n."
    new "## About（バージョン情報）スクリーンに表示されるテキスト。パラグラフ間に空白の行を挿入したい場合は、\\n\\n と書いてください。"

    # options.rpy:37
    old "## A short name for the game used for executables and directories in the built distribution. This must be ASCII-only, and must not contain spaces, colons, or semicolons."
    new "## 実行ファイルやビルドされた配布物のディレクトリー名に使われる、ゲームの簡易名。簡易名は ASCII 文字（半角英数字）のみで構成され、スペース・コロン・セミコロンなどを含んでは行けません。"

    # options.rpy:44
    old "## Sounds and music"
    new "## サウンドと音楽"

    # options.rpy:46
    old "## These three variables control which mixers are shown to the player by default. Setting one of these to False will hide the appropriate mixer."
    new "## 以下の変数はデフォルトで使用されるミキサー（同じ効果を共有するチャンネルの集まり）を制御します。False にしたミキサーは利用できなくなります。"

    # options.rpy:55
    old "## To allow the user to play a test sound on the sound or voice channel, uncomment a line below and use it to set a sample sound to play."
    new "## サウンドやボイスの設定画面で、ユーザーがテストサウンドを再生可能にする場合、以下の行をアンコメントしてサンプルサウンドを指定します。"

    # options.rpy:62
    old "## Uncomment the following line to set an audio file that will be played while the player is at the main menu. This file will continue playing into the game, until it is stopped or another file is played."
    new "## 次の行をアンコメントしてオーディオファイルを指定すると、メインメニューで再生されます。このファイルは、停止するか他の音楽が再生されない限りゲーム中で流れ続けます。"

    # options.rpy:69
    old "## Transitions"
    new "## トランジション"

    # options.rpy:71
    old "## These variables set transitions that are used when certain events occur. Each variable should be set to a transition, or None to indicate that no transition should be used."
    new "## 以下の変数は、メニュー切り替えなどのイベントに対するトランジションを設定します。各変数にはトランジションを指定します。トランジションを使わない場合は None に設定します。"

    # options.rpy:75
    old "## Entering or exiting the game menu."
    new "## ゲームメニュー（ゲーム中、右クリックで表示されるメニュー）を開いたり閉じたりする時のトランジション。"

    # options.rpy:81
    old "## A transition that is used after a game has been loaded."
    new "## ゲームデータをロードした後に使われるトランジション。"

    # options.rpy:86
    old "## Used when entering the main menu after the game has ended."
    new "## ゲーム終了後、メインメニューに戻る時のトランジション。"

    # options.rpy:91
    old "## A variable to set the transition used when the game starts does not exist. Instead, use a with statement after showing the initial scene."
    new "## メインメニューからゲームを開始する時のトランジションは、ここでは設定できません。代わりに、ゲーム開始後の最初のシーンで with ステートメントを使ってください。"

    # options.rpy:96
    old "## Window management"
    new "## テキストウィンドウの管理"

    # options.rpy:98
    old "## This controls when the dialogue window is displayed. If \"show\", it is always displayed. If \"hide\", it is only displayed when dialogue is present. If \"auto\", the window is hidden before scene statements and shown again once dialogue is displayed."
    new "## 次の変数は、台詞を表示するテキストウィンドウの挙動を制御します。\"show\" であれば常に表示、\"hide\" であれば台詞が表示されているときにのみ表示します。\"auto\" であれば scene ステートメントの直前に非表示にして、say ステートメントの直前に再表示します。"

    # options.rpy:103
    old "## After the game has started, this can be changed with the \"window show\", \"window hide\", and \"window auto\" statements."
    new "## ゲーム開始後でも \"window show\"、\"window hide\"、\"window auto\" ステートメントで変更することができます。"

    # options.rpy:109
    old "## Transitions used to show and hide the dialogue window"
    new "## テキストウィンドウを表示したり、非表示にしたりする時のトランジション。"

    # options.rpy:115
    old "## Preference defaults"
    new "## 環境設定のデフォルト"

    # options.rpy:117
    old "## Controls the default text speed. The default, 0, is infinite, while any other number is the number of characters per second to type out."
    new "## デフォルトの文字表示速度。数字は一秒に表示する文字数で、デフォルト値の 0 は無限（一瞬で表示）を意味します。"

    # options.rpy:123
    old "## The default auto-forward delay. Larger numbers lead to longer waits, with 0 to 30 being the valid range."
    new "## デフォルトのオート待ち時間。0 から 30 までの数字を取り、数字が大きいほど待ち時間が長くなります。"

    # options.rpy:129
    old "## Save directory"
    new "## セーブディレクトリー"

    # options.rpy:131
    old "## Controls the platform-specific place Ren'Py will place the save files for this game. The save files will be placed in:"
    new "## プラットフォームごとの Ren'Py がゲームのセーブデータを作成する場所を制御します。セーブファイルは以下の場所に作成されます："

    # options.rpy:134
    old "## Windows: %APPDATA%\\RenPy\\<config.save_directory>"
    new "## Windows: %APPDATA%\\RenPy\\<config.save_directory>"

    # options.rpy:136
    old "## Macintosh: $HOME/Library/RenPy/<config.save_directory>"
    new "## Macintosh: $HOME/Library/RenPy/<config.save_directory>"

    # options.rpy:138
    old "## Linux: $HOME/.renpy/<config.save_directory>"
    new "## Linux: $HOME/.renpy/<config.save_directory>"

    # options.rpy:140
    old "## This generally should not be changed, and if it is, should always be a literal string, not an expression."
    new "## この値は一般的に変更するべきではありません。もし変更する場合、式や変数ではなく文字列で直接指定しなければなりません。"

    # options.rpy:146
    old "## Icon"
    new "## アイコン"

    # options.rpy:148
    old "## The icon displayed on the taskbar or dock."
    new "## タスクバーやダックに表示されるアイコン。"

    # options.rpy:153
    old "## Build configuration"
    new "## ビルド設定"

    # options.rpy:155
    old "## This section controls how Ren'Py turns your project into distribution files."
    new "## このセクションは、プロジェクトを配布物にビルドするときの挙動を制御します。"

    # options.rpy:160
    old "## The following functions take file patterns. File patterns are case- insensitive, and matched against the path relative to the base directory, with and without a leading /. If multiple patterns match, the first is used."
    new "## 以下の機能はファイルパターン（ワイルドカード等で複数ファイルを指定する文字列）を利用します。ファイルパターンは、大文字小文字を区別せず、ベースディレクトリーからの相対パスを参照します（最初の / は無視します）。複数のパターンが一致した場合、先に定義した方が優先されます。"

    # options.rpy:165
    old "## In a pattern:"
    new "## パターンは以下の記号を使用します："

    # options.rpy:167
    old "## / is the directory separator."
    new "## / はディレクトリーのセパレーターです。"

    # options.rpy:169
    old "## * matches all characters, except the directory separator."
    new "## * はディレクトリーセパレーターを除く、すべての文字に一致します。"

    # options.rpy:171
    old "## ** matches all characters, including the directory separator."
    new "## ** はディレクトリーセパレーターを含む、すべての文字に一致します。"

    # options.rpy:173
    old "## For example, \"*.txt\" matches txt files in the base directory, \"game/**.ogg\" matches ogg files in the game directory or any of its subdirectories, and \"**.psd\" matches psd files anywhere in the project."
    new "## 例えば、\"*.txt\" はベースディレクトリーにある全ての txt ファイルに一致し、 \"game/**.ogg\" はゲームディレクトリー及びそのサブディレクトリーにある全ての ogg ファイルに一致し、\"**.psd\" はプロジェクトのあらゆる psd ファイルに一致します。"

    # options.rpy:177
    old "## Classify files as None to exclude them from the built distributions."
    new "## classify（分類）を None に設定したファイルは配布物から除外されます。"

    # options.rpy:185
    old "## To archive files, classify them as 'archive'."
    new "## アーカイブ（書庫化・暗号化）したいファイルは 'archive'（または任意の文字列）に分類します。"

    # options.rpy:190
    old "## Files matching documentation patterns are duplicated in a mac app build, so they appear in both the app and the zip file."
    new "## documentation（ドキュメント）に指定したパターンと一致するファイルは mac 用アプリのビルドで複製され、app と zip のどちらにも含まれるようになります。"

    # options.rpy:196
    old "## A Google Play license key is required to download expansion files and perform in-app purchases. It can be found on the \"Services & APIs\" page of the Google Play developer console."
    new "## 拡張をダウンロードしたり、アプリ内課金を行う場合には、Google Play ライセンスキーが必要です。キーは Google Play developer console の \"Services & APIs\" にあります。"

    # options.rpy:203
    old "## The username and project name associated with an itch.io project, separated by a slash."
    new "## itch.io project に関連付けられたユーザー名とプロジェクト名。二つの名前はスラッシュで分けてください。"

    # options.rpy:196
    old "## Set this to a string containing your Apple Developer ID Application to enable codesigning on the Mac. Be sure to change it to your own Apple-issued ID."
    new "## Mac のコード署名を有効にするために Apple Developer ID アプリケーション を含む文字列を設定します。必ず Apple が発行したあなたの ID に変更してください。"

    # options.rpy:81
    old "## Between screens of the game menu."
    new "## ゲームメニューのスクリーンを切り替える時のトランジション。"

    # options.rpy:31
    old "## Text that is placed on the game's about screen. Place the text between the triple-quotes, and leave a blank line between paragraphs."
    new "## About（バージョン情報）スクリーンに表示されるテキスト。トリプルクオートの間にテキストを入力します。段落の間には空行を挿入して下さい。"

    # gui/game/options.rpy:47
    old "## These three variables control, among other things, which mixers are shown to the player by default. Setting one of these to False will hide the appropriate mixer."
    new "## これらの3つの変数は、特に、どのミキサーがデフォルトでプレーヤーに表示されるかを制御します。これらのいずれかをFalseに設定すると、適切なミキサーが非表示になります。"

translate japanese strings:

    # gui/game/options.rpy:203
    old "## A Google Play license key is required to perform in-app purchases. It can be found in the Google Play developer console, under \"Monetize\" > \"Monetization Setup\" > \"Licensing\"."
    new "## アプリ内課金を行うには、Google Playのライセンスキーが必要です。Google Play開発者コンソールの「収益化」→「収益化のセットアップ」→「ライセンス」で確認することができます。"

translate japanese strings:

    # gui/game/options.rpy:140
    old "## Windows: %APPDATA\\RenPy\\<config.save_directory>"
    new "## Windows: %APPDATA\\RenPy\\<config.save_directory>"

