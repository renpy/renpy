
translate japanese strings:

    # gui.rpy:2
    old "## Initialization"
    new "## 初期化"

    # gui.rpy:5
    old "## The init offset statement causes the init code in this file to run before init code in any other file."
    new "## このファイルは GUI をカスタマイズする基本的なオプションを記載しています。次の init offset ステートメントは、このファイルの init コードを他のファイルよりも先に実行しています。"

    # gui.rpy:9
    old "## Calling gui.init resets the styles to sensible default values, and sets the width and height of the game."
    new "## まず最初に gui.init を実行して、スタイルを扱いやすい初期値にリセットし、ゲームの横幅と縦幅を設定します。"

    # gui.rpy:17
    old "## GUI Configuration Variables"
    new "## GUI 設定変数"

    # gui.rpy:21
    old "## Colors"
    new "## カラー"

    # gui.rpy:23
    old "## The colors of text in the interface."
    new "## インターフェースのテキストのカラー。"

    # gui.rpy:25
    old "## An accent color used throughout the interface to label and highlight text."
    new "## アクセントカラー。タイトル・ラベル・ハイライトされたテキスト・ボタンの背景・スライダーのつまみ等、インターフェイスの様々な場所で使います。"

    # gui.rpy:29
    old "## The color used for a text button when it is neither selected nor hovered."
    new "## selected（選択中）でも hover（フォーカス中）でもない状態のテキストボタンのカラー。"

    # gui.rpy:32
    old "## The small color is used for small text, which needs to be brighter/darker to achieve the same effect."
    new "## スモールカラー。クイックメニューなどの、明るさを調節する必要のある小さなテキストボタンに使います。"

    # gui.rpy:36
    old "## The color that is used for buttons and bars that are hovered."
    new "## hover（フォーカス中）のテキストボタンのカラー。また、バーの充足部分（左側）やスライダーのつまみ等の画像を再生成するときにも使われます。"

    # gui.rpy:39
    old "## The color used for a text button when it is selected but not focused. A button is selected if it is the current screen or preference value."
    new "## selected（選択中）のテキストボタンのカラー。ボタンが現在のスクリーンであったり、環境設定の値と一致したりすると、ボタンは選択中になります。"

    # gui.rpy:43
    old "## The color used for a text button when it cannot be selected."
    new "## insensitive (選択不可能）なテキストボタンのカラー。"

    # gui.rpy:46
    old "## Colors used for the portions of bars that are not filled in. These are not used directly, but are used when re-generating bar image files."
    new "## バーの非充足部分（右側）やスライダーの背景部分のカラー。バーやスライダーのカラーは直接使われず、 GUI を変更・更新した場合の画像生成に使われます。"

    # gui.rpy:51
    old "## The colors used for dialogue and menu choice text."
    new "## text_color は台詞や選択肢のテキストのカラーです。interface_text_color はヒストリーやヘルプなどそれ以外のテキストのカラーです。"

    # gui.rpy:56
    old "## Fonts and Font Sizes"
    new "## フォントとフォントサイズ"

    # gui.rpy:58
    old "## The font used for in-game text."
    new "## ゲーム内の台詞や選択肢に使われるフォント。"

    # gui.rpy:61
    old "## The font used for character names."
    new "## キャラクターの名前に使われるフォント。"

    # gui.rpy:64
    old "## The font used for out-of-game text."
    new "## ゲームメニューなどのインターフェースに使われるテキストのフォント。"

    # gui.rpy:67
    old "## The size of normal dialogue text."
    new "## 一般的な台詞のテキストサイズ。"

    # gui.rpy:70
    old "## The size of character names."
    new "## キャラクターの名前のテキストサイズ。"

    # gui.rpy:73
    old "## The size of text in the game's user interface."
    new "## インターフェースのテキストサイズ。"

    # gui.rpy:76
    old "## The size of labels in the game's user interface."
    new "## インターフェースのラベル（見出し）のテキストサイズ。"

    # gui.rpy:79
    old "## The size of text on the notify screen."
    new "## notify（通知）スクリーンのテキストサイズ。"

    # gui.rpy:82
    old "## The size of the game's title."
    new "## ゲームタイトルのテキストサイズ。"

    # gui.rpy:86
    old "## Main and Game Menus"
    new "## メインメニューとゲームメニュー"

    # gui.rpy:88
    old "## The images used for the main and game menus."
    new "## メインメニューとゲームメニューの背景画像。メインメニューはゲーム起動時に最初に表示されるメニュー、ゲームメニューはゲーム中右クリックで呼び出せるメニューです。画像を変えたい場合は gui ディレクトリーにある該当の画像を入れ替えてください。"

    # gui.rpy:92
    old "## Should we show the name and version of the game?"
    new "## メインメニューにゲームタイトルとそのバージョンを表示するかどうか。True なら表示します。（この変数は options.rpy で再定義されるため、options.rpy の同じ文を消去しないと反映されません）"

    # gui.rpy:96
    old "## Dialogue"
    new "## ダイアローグ（台詞）"

    # gui.rpy:98
    old "## These variables control how dialogue is displayed on the screen one line at a time."
    new "## 以下の変数は、一度に表示される台詞とキャラクターの名前を、どのようにスクリーンに表示するか制御します。"

    # gui.rpy:101
    old "## The height of the textbox containing dialogue."
    new "## 台詞を表示するテキストボックスの高さ。テキストボックスの画像を変えたい場合は gui/textbox.png の画像を入れ替えます。"

    # gui.rpy:104
    old "## The placement of the textbox vertically on the screen. 0.0 is the top, 0.5 is center, and 1.0 is the bottom."
    new "## 画面に対する、テキストボックスの垂直方向の位置。 0.0 は上端、0.5 は中央、 1.0 は下端になります。"

    # gui.rpy:109
    old "## The placement of the speaking character's name, relative to the textbox. These can be a whole number of pixels from the left or top, or 0.5 to center."
    new "## テキストボックスに対する、キャラクター名の位置。左上からのピクセル数で指定するか 0.0 から 1.0 までの小数で指定します。 0.5 は中央に表示。"

    # gui.rpy:114
    old "## The horizontal alignment of the character's name. This can be 0.0 for left-aligned, 0.5 for centered, and 1.0 for right-aligned."
    new "## キャラクター名の文字揃え。 0.0 は左揃え、0.5 は中央揃え、 1.0 は右揃えになります。0.0 以外にした場合、キャラクター名の位置の調整も必要になります。"

    # gui.rpy:118
    old "## The width, height, and borders of the box containing the character's name, or None to automatically size it."
    new "## キャラクター名を表示するネームボックスのサイズ。None にすると、自動的に決定されます。画像を変えたい場合は gui/textbox.png の画像を入れ替えます（デフォルト画像は透明なので表示されません）。"

    # gui.rpy:123
    old "## The borders of the box containing the character's name, in left, top, right, bottom order."
    new "## ネームボックスのボーダーのサイズ。左、上、右、下の順で指定します。ボックスのサイズは、その中に表示されるキャラクター名のサイズから更にボーダー分拡張したサイズになります。"

    # gui.rpy:127
    old "## If True, the background of the namebox will be tiled, if False, the background of the namebox will be scaled."
    new "## True に設定すると、ネームボックスの背景画像をスケーリングではなくタイリングで表示します。"

    # gui.rpy:132
    old "## The placement of dialogue relative to the textbox. These can be a whole number of pixels relative to the left or top side of the textbox, or 0.5 to center."
    new "## テキストボックスに対する、台詞の位置。左上からのピクセル数で指定するか 0.0 から 1.0 までの小数で指定します。 0.5 だと中央に表示。"

    # gui.rpy:138
    old "## The maximum width of dialogue text, in pixels."
    new "## 台詞の最大ピクセル幅。このピクセル幅以上の台詞は折り返して表示されます。"

    # gui.rpy:141
    old "## The horizontal alignment of the dialogue text. This can be 0.0 for left-aligned, 0.5 for centered, and 1.0 for right-aligned."
    new "## 台詞の文字揃え。 0.0 は左揃え、0.5 は中央揃え、 1.0 は右揃えになります。0.0 以外にした場合、台詞の位置の調整も必要になります。"

    # gui.rpy:146
    old "## Buttons"
    new "## ボタン"

    # gui.rpy:148
    old "## These variables, along with the image files in gui/button, control aspects of how buttons are displayed."
    new "## 以下の変数は、ボタンをどのように表示するか制御します。画像を変えたい場合は gui/button ディレクトリーにある各 background.png の画像を入れ替えます（デフォルト画像は透明なので表示されません）。ボタンの状態に合わせて画像を変えたい場合は、ファイル名に idle_、hover_、selected_、selected_hover_ の接頭辞を付けます。"

    # gui.rpy:151
    old "## The width and height of a button, in pixels. If None, Ren'Py computes a size."
    new "## ボタンの縦幅と横幅。None にすると自動的に計算されます。"

    # gui.rpy:155
    old "## The borders on each side of the button, in left, top, right, bottom order."
    new "## ボタンのボーダーのサイズ。左、上、右、下の順で指定します。ボタンのサイズは、その中のテキストやオブジェクトのサイズから更にボーダー分拡張したサイズになります。"

    # gui.rpy:158
    old "## If True, the background image will be tiled. If False, the background image will be linearly scaled."
    new "## True に設定すると、ボタンの背景画像をスケーリングではなくタイリングで表示します。"

    # gui.rpy:162
    old "## The font used by the button."
    new "## ボタンのテキストに使用するフォント。"

    # gui.rpy:165
    old "## The size of the text used by the button."
    new "## ボタンのテキストのサイズ。"

    # gui.rpy:168
    old "## The color of button text in various states."
    new "## 状態別のボタンのテキストのカラー。idle は選択可能、hover はフォーカス中、selected は選択中、insensitive は選択不可能な状態です。"

    # gui.rpy:174
    old "## The horizontal alignment of the button text. (0.0 is left, 0.5 is center, 1.0 is right)."
    new "## ボタンのフレームに対する、テキストの文字揃え。 0.0 は左揃え、0.5 は中央揃え、 1.0 は右揃えになります。"

    # gui.rpy:179
    old "## These variables override settings for different kinds of buttons. Please see the gui documentation for the kinds of buttons available, and what each is used for."
    new "## 以下の変数は、様々なボタンの種類ごとにボタンの基本設定を上書きします。詳細は gui ドキュメンテーションを参考にしてください。"

    # gui.rpy:183
    old "## These customizations are used by the default interface:"
    new "## デフォルトのインターフェースには、radio、check、confirm、page、quick、navigation、choice、slot、test、help、nvl のボタンが用意されています。radio と check は環境設定の各項目のボタン（デフォルトでは同じ画像）。confirm は確認画面の選択肢、page は セーブ・ロード画面のページ切り替え、quick はクイックメニュー、 navigation はゲームメニューのメニュー切り替えに使うボタンです。"

    # gui.rpy:198
    old "## You can also add your own customizations, by adding properly-named variables. For example, you can uncomment the following line to set the width of a navigation button."
    new "## 上記以外にも、接頭辞と接尾辞を適切に組み合わせた変数名を追加すれば、様々なカスタマイズが可能になります。例えば、次の行をアンコメントすると navigation（メニュー切り替え）ボタンの横幅を指定することができます。"

    # gui.rpy:205
    old "## Choice Buttons"
    new "## Choice（選択）ボタン"

    # gui.rpy:207
    old "## Choice buttons are used in the in-game menus."
    new "## Choice ボタンは、ゲーム内の選択肢に使うボタンです。"

    # gui.rpy:220
    old "## File Slot Buttons"
    new "## File Slot（ファイルスロット）ボタン"

    # gui.rpy:222
    old "## A file slot button is a special kind of button. It contains a thumbnail image, and text describing the contents of the save slot. A save slot uses image files in gui/button, like the other kinds of buttons."
    new "## File slot は特別なボタンで、セーブデータのサムネイル画像と詳細情報を含んでいます。他のボタンと同じように gui/button ディレクトリーにある slot_ の接頭辞が付いた背景画像を使います。"

    # gui.rpy:226
    old "## The save slot button."
    new "## File slot ボタンの設定。"

    # gui.rpy:234
    old "## The width and height of thumbnails used by the save slots."
    new "## File slot に使われるサムネイル画像の横幅と縦幅。"

    # gui.rpy:238
    old "## The number of columns and rows in the grid of save slots."
    new "## １ページあたりの File slot の列数（cols）と行数（rows）。"

    # gui.rpy:243
    old "## Positioning and Spacing"
    new "## 配置と間隔"

    # gui.rpy:245
    old "## These variables control the positioning and spacing of various user interface elements."
    new "## 以下の変数は、インターフェースの様々な要素の位置と間隔を制御します。"

    # gui.rpy:248
    old "## The position of the left side of the navigation buttons, relative to the left side of the screen."
    new "## 画面左端からの navigation（メニュー切り替え）ボタンの位置。"

    # gui.rpy:252
    old "## The vertical position of the skip indicator."
    new "## 画面上端からの skip indicator（スキップ表示）スクリーンの位置。"

    # gui.rpy:255
    old "## The vertical position of the notify screen."
    new "## 画面上端からの notify（通知）スクリーンの位置。"

    # gui.rpy:258
    old "## The spacing between menu choices."
    new "## ゲーム中の choice（選択）ボタンの間隔。"

    # gui.rpy:261
    old "## Buttons in the navigation section of the main and game menus."
    new "## メインメニューやゲームメニューの navigation（メニュー切り替え）ボタンの間隔。"

    # gui.rpy:264
    old "## Controls the amount of spacing between preferences."
    new "## 環境設定の各項目の間隔。"

    # gui.rpy:267
    old "## Controls the amount of spacing between preference buttons."
    new "## 環境設定の各項目にある、各ボタンの間隔。"

    # gui.rpy:270
    old "## The spacing between file page buttons."
    new "## セーブ・ロード画面の file page（ページ切り替え）ボタンの間隔。"

    # gui.rpy:273
    old "## The spacing between file slots."
    new "## セーブ・ロード画面の file slot（ファイルスロット）ボタン間隔。"

    # gui.rpy:277
    old "## Frames"
    new "## フレーム"

    # gui.rpy:279
    old "## These variables control the look of frames that can contain user interface components when an overlay or window is not present."
    new "## 以下の変数は、インターフェースのコンポーネントを収納するフレームを制御します。フレームは、ウィンドウやオーバーレイが用意されていない場面で使われます。"

    # gui.rpy:282
    old "## Generic frames that are introduced by player code."
    new "## 一般的なフレーム。デフォルトのインターフェースでは使われず、開発者の書いたコードでのみ使用します。画像は gui/frame.png。"

    # gui.rpy:285
    old "## The frame that is used as part of the confirm screen."
    new "## confirm（確認）スクリーンに使用するフレーム。画像は gui/overlay/confirm.png。"

    # gui.rpy:288
    old "## The frame that is used as part of the skip screen."
    new "## skip indicator（スキップ表示）スクリーンに使用するフレーム。画像は gui/skip.png。"

    # gui.rpy:291
    old "## The frame that is used as part of the notify screen."
    new "## notify（通知）スクリーンに使用するフレーム。画像は gui/notify.png。"

    # gui.rpy:294
    old "## Should frame backgrounds be tiled?"
    new "## True に設定すると、フレームの背景画像をスケーリングではなくタイリングで表示します。"

    # gui.rpy:298
    old "## Bars, Scrollbars, and Sliders"
    new "## バー・スクロールバー・スライダー"

    # gui.rpy:300
    old "## These control the look and size of bars, scrollbars, and sliders."
    new "## 以下の変数は、バー・スライダー・スクロールバーの外見を制御します。"

    # gui.rpy:302
    old "## The default GUI only uses sliders and vertical scrollbars. All of the other bars are only used in creator-written code."
    new "## デフォルトの GUI はスライダーと垂直スクロールバーだけを使用します。他のバーは開発者が追加したコードでのみ使われます。"

    # gui.rpy:305
    old "## The height of horizontal bars, scrollbars, and sliders. The width of vertical bars, scrollbars, and sliders."
    new "## バー・スクロールバー・スライダーの各々の太さ（水平バーでは縦幅、垂直バーでは横幅）。"

    # gui.rpy:311
    old "## True if bar images should be tiled. False if they should be linearly scaled."
    new "## True に設定すると、バーの背景をスケーリングではなくタイリングで表示します。"

    # gui.rpy:316
    old "## Horizontal borders."
    new "## 水平バーのボーダー。画像はそれぞれ、 gui/bar/left.png 及び right.png、gui/slider/horizontal_**.png、gui/scrollbar/horizontal_**.png。"

    # gui.rpy:321
    old "## Vertical borders."
    new "## 垂直バーのボーダー。画像はそれぞれ、gui/bar/bottom.png 及び top.png、gui/slider/vertical_**.png、gui/scrollbar/vartical_**.png。"

    # gui.rpy:326
    old "## What to do with unscrollable scrollbars in the gui. \"hide\" hides them, while None shows them."
    new "## スクロール不可能なスクロールバーをどう扱うか。 \"hide\" なら非表示、None なら表示します。"

    # gui.rpy:331
    old "## History"
    new "## ヒストリー"

    # gui.rpy:333
    old "## The history screen displays dialogue that the player has already dismissed."
    new "## History（履歴）スクリーンは、プレイヤーが見終わった台詞を表示します。"

    # gui.rpy:335
    old "## The number of blocks of dialogue history Ren'Py will keep."
    new "## ヒストリーのエントリー（１台詞）を最大いくつまで保持するか。"

    # gui.rpy:338
    old "## The height of a history screen entry, or None to make the height variable at the cost of performance."
    new "## History スクリーンにおける、エントリーの高さ。None にすると可変になりますが、パフォーマンスが低下します。"

    # gui.rpy:342
    old "## The position, width, and alignment of the label giving the name of the speaking character."
    new "## キャラクター名の縦座標・横座標・横幅・文字揃え。"

    # gui.rpy:349
    old "## The position, width, and alignment of the dialogue text."
    new "## 台詞の縦座標・横座標・横幅・文字揃え。"

    # gui.rpy:356
    old "## NVL-Mode"
    new "## NVL モード"

    # gui.rpy:358
    old "## The NVL-mode screen displays the dialogue spoken by NVL-mode characters."
    new "## NVL（ノベル）スクリーンは、 NVL モード（全画面方式）のキャラクターの台詞を表示するスクリーンです。"

    # gui.rpy:360
    old "## The borders of the background of the NVL-mode background window."
    new "## NVL モードに使用する背景のボーダー。画像は gui/nvl.png。"

    # gui.rpy:363
    old "## The height of an NVL-mode entry. Set this to None to have the entries dynamically adjust height."
    new "## NVL モードにおける、エントリー（１台詞）の高さ。None にすると可変になります。"

    # gui.rpy:367
    old "## The spacing between NVL-mode entries when gui.nvl_height is None, and between NVL-mode entries and an NVL-mode menu."
    new "## NVL モードにおいて、gui.nvl_height を None に設定した場合の各エントリーの間隔。また、台詞と選択肢との間隔にも使われます。"

    # gui.rpy:384
    old "## The position, width, and alignment of nvl_thought text (the text said by the nvl_narrator character.)"
    new "## nvl_thought（モノローグ）の縦座標・横座標・横幅・文字揃え。"

    # gui.rpy:391
    old "## The position of nvl menu_buttons."
    new "## NVL モードにおける、選択肢の横座標と文字揃え。"

    # gui.rpy:398
    old "## Mobile devices"
    new "## モバイルデバイス"

    # gui.rpy:403
    old "## This increases the size of the quick buttons to make them easier to touch on tablets and phones."
    new "## タブレットやスマートフォンでタッチしやすいように、 quick ボタンのサイズを大きくします。"

    # gui.rpy:409
    old "## This changes the size and spacing of various GUI elements to ensure they are easily visible on phones."
    new "## スマートフォンで見やすいように、GUI の各要素のサイズと間隔を変更します。"

    # gui.rpy:413
    old "## Font sizes."
    new "## フォントサイズ。"

    # gui.rpy:421
    old "## Adjust the location of the textbox."
    new "## テキストボックスの位置を調整。"

    # gui.rpy:427
    old "## Change the size and spacing of items in the game menu."
    new "## ゲームメニューの各項目のサイズと間隔を変更。"

    # gui.rpy:436
    old "## File button layout."
    new "## ファイルスロットの配置。"

    # gui.rpy:440
    old "## NVL-mode."
    new "## NVL モード。"

    # gui.rpy:456
    old "## Quick buttons."
    new "## Quick ボタン。"

    # gui.rpy:395
    old "## Localization"
    new "## 多言語対応"

    # gui.rpy:397
    old "## This controls where a line break is permitted. The default is suitable for most languages. A list of available values can be found at https://www.renpy.org/doc/html/style_properties.html#style-property-language"
    new "## 次の変数は改行・禁則処理を制御します。デフォルトの値が推奨です。他の値は https://www.renpy.org/doc/html/style_properties.html#style-property-language を参照してください。"

    # gui.rpy:276
    old "## The position of the main menu text."
    new "## メインメニューのテキストの文字揃え。"

    # gui.rpy:434
    old "## Change the size and spacing of various things."
    new "## 様々なサイズとスペーシングを変更。"

    # gui.rpy:5
    old "## The init offset statement causes the initialization statements in this file to run before init statements in any other file."
    new "## このファイルは GUI をカスタマイズする基本的なオプションを記載しています。次の init offset ステートメントにより、このファイルの init 文は他のファイルの init 文よりも先に実行されます。"

    # gui.rpy:282
    old "## Generic frames."
    new "## 一般的なフレーム。デフォルトのインターフェースでは未使用です。画像は gui/frame.png。"

    # gui.rpy:302
    old "## The default GUI only uses sliders and vertical scrollbars. All of the other bars are only used in creator-written screens."
    new "## デフォルトの GUI はスライダーと垂直スクロールバーだけを使用します。他のバーは開発者が追加したスクリーンでのみ使われます。"

    # gui.rpy:363
    old "## The maximum number of NVL-mode entries Ren'Py will display. When more entries than this are to be show, the oldest entry will be removed."
    new "## NVL モードにおける、一度に表示されるエントリー（１台詞）の最大数。この値以上のエントリーを表示しようとすると、一番古いエントリーが取り除かれます。"


    # gui/game/gui.rpy:14
    old "## Enable checks for invalid or unstable properties in screens or transforms"
    new "## スクリーンやトランスフォームのプロパティが無効または不安定であることをチェックできるようにする。"

    # gui/game/gui.rpy:347
    old "## Additional space to add between history screen entries."
    new "## history screen の追加の行間を設定します。"

