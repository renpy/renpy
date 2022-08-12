
# game/tutorial_screen_displayables.rpy:3
translate japanese screen_displayables_7c897a6d:

    # e "There are quite a few screen displayables. Here, I'll tell you about some of the most important ones."
    e "Ren'Pyには非常にたくさんのスクリーンdisplayableがあります。ここでは、最も重要ないくつかについてお話いたします。"

# game/tutorial_screen_displayables.rpy:9
translate japanese screen_displayables_menu_fef7b441:

    # e "What would you like to know about?" nointeract
    e "何について知りたいですか？" nointeract

# game/tutorial_screen_displayables.rpy:49
translate japanese screen_displayable_properties_76c5639a:

    # e "There are a few properties that every screen language displayable shares. Here, I'll demonstrate them for you."
    e "各スクリーン言語displayableに共通するいくつかのプロパティがあります。ここでは、それらについて説明します。"

# game/tutorial_screen_displayables.rpy:57
translate japanese screen_displayable_properties_527d4b4e:

    # e "First off, every screen language displayable supports the position properties. When the container a displayable is in supports it, you can use properties like align, anchor, pos, and so so on."
    e "最初に、各スクリーン言語displayableは位置プロパティをサポートしています。displayableを含むコンテナがサポートしていれば、align、anchor、posなどといったプロパティを使用できます。"

# game/tutorial_screen_displayables.rpy:69
translate japanese screen_displayable_properties_8aff26dd:

    # e "The at property applies a transform to the displayable, the same way the at clause in the show statement does."
    e "atプロパティは、showステートメント内のatの部分と同じように、displayableにTransformを適用します。"

# game/tutorial_screen_displayables.rpy:106
translate japanese screen_displayable_properties_2ed40a70:

    # e "The id property is mostly used with the say screen, which is used to show dialogue. Outside of the say screen, it isn't used much."
    e "idプロパティは主にsayスクリーンと共に用いられ、ダイアログの表示に使用されます。sayスクリーン以外にはあまり使われません。"

# game/tutorial_screen_displayables.rpy:108
translate japanese screen_displayable_properties_da5733d1:

    # e "It tells Ren'Py which displayables are the background window, 'who' is speaking, and 'what' is being said. This used to apply per-Character styles, and help with auto-forward mode."
    e "idプロパティは、どのdisplayableがウィンドウの背景なのか、「誰が」話しているのか、「何」を言っているのかをRen'Pyに教えます。これはキャラクター別のスタイルを適用したり、オートモートで役立ちます。"

# game/tutorial_screen_displayables.rpy:123
translate japanese screen_displayable_properties_cc09fade:

    # e "The style property lets you specify the style of a single displayable."
    e "スタイルプロパティによっては個別にdisplayableのスタイルを指定できます。"

# game/tutorial_screen_displayables.rpy:144
translate japanese screen_displayable_properties_a7f4e25c:

    # e "The style_prefix property sets the prefix of the style that's used for a displayable and its children."
    e "style_prefixプロパティは、displayableとその子に使用されるスタイルの接頭辞を設定します。"

# game/tutorial_screen_displayables.rpy:146
translate japanese screen_displayable_properties_6bdb0723:

    # e "For example, when the style_prefix property is 'green', the vbox has the 'green_vbox' style, and the text in it has the 'green_text' style."
    e "例えば、style_prefixプロパティが'green'のとき、vboxは'green_vbox'スタイル、その中のテキストは'green_text'スタイルとなります。"

# game/tutorial_screen_displayables.rpy:150
translate japanese screen_displayable_properties_8a3a8635:

    # e "There are a few more properties than these, and you can find the rest in the documentation. But these are the ones you can expect to see in your game, in the default screens."
    e "他にも更にいくつかのプロパティがあり、ドキュメントにてご覧いただけます。ですが、これらはあなたの作品内でもデフォルトのスクリーンの中で見ることができるものです。"

# game/tutorial_screen_displayables.rpy:156
translate japanese add_displayable_ec121c5c:

    # e "Sometimes you'll have a displayable, like an image, that you want to add to a screen."
    e "時にdisplayableをimageのようにスクリーンに追加したい場合があるでしょう。"

# game/tutorial_screen_displayables.rpy:165
translate japanese add_displayable_7ec3e2b0:

    # e "This can be done using the add statement, which adds an image or other displayable to the screen."
    e "これはaddステートメントにより可能です。addステートメントは、画像やdisplayableをスクリーンに追加します。"

# game/tutorial_screen_displayables.rpy:167
translate japanese add_displayable_7112a377:

    # e "There are a few ways to refer to the image. If it's in the images directory or defined with the image statement, you can just put the name inside a quoted string."
    e "画像を参照するにはいくつかの方法があります。もし画像がimageディレクトリにあるかimageステートメントで定義されているのなら、その名前をダブルクォーテーションで囲まれた文字列として与えるだけです。"

# game/tutorial_screen_displayables.rpy:176
translate japanese add_displayable_8ba81c26:

    # e "An image can also be referred to by it's filename, relative to the game directory."
    e "画像はgameディレクトリからの相対パスのファイル名でも参照できます。"

# game/tutorial_screen_displayables.rpy:185
translate japanese add_displayable_1f5571e3:

    # e "Other displayables can also be added using the add statement. Here, we add the Solid displayable, showing a solid block of color."
    e "その他のdisplayableもaddステートメントで追加できます。ここで、Solid displayableを追加し単色のブロックを表示してみます。"

# game/tutorial_screen_displayables.rpy:195
translate japanese add_displayable_0213ffa2:

    # e "In addition to the displayable, the add statement can be given transform properties. These can place or otherwise transform the displayable being added."
    e "displayableに加え、addステートメントではtransformプロパティを与えることもできます。これにより、追加されたdisplayableを配置したりTransformしたりできます。"

# game/tutorial_screen_displayables.rpy:207
translate japanese add_displayable_3a56a464:

    # e "Of course, the add statement can also take the at property, letting you give it a more complex transform."
    e "もちろん、addステートメントはatプロパティも取りますし、更に複雑なTransformを与えることもできます。"

# game/tutorial_screen_displayables.rpy:222
translate japanese text_displayable_96f88225:

    # e "The screen language text statement adds a text displayable to the screen. It takes one argument, the text to be displayed."
    e "スクリーン言語のtextステートメントはテキストdisplayableをスクリーンに与えます。これは、表示するテキストを引数として取ります。"

# game/tutorial_screen_displayables.rpy:224
translate japanese text_displayable_1ed1a8c2:

    # e "In addition to the common properties that all displayables take, text takes the text style properties. For example, size sets the size of the text."
    e "全てのdisplayableが取る共通のプロパティに加え、textはテキストスタイルのプロパティ取ります。例えば、sizeはテキストの大きさを設定します。"

# game/tutorial_screen_displayables.rpy:234
translate japanese text_displayable_9351d9dd:

    # e "The text displayable can also interpolate values enclosed in square brackets."
    e "テキストdisplayableには角括弧で囲まれた値を挿入もできます。"

# game/tutorial_screen_displayables.rpy:236
translate japanese text_displayable_32d76ccb:

    # e "When text is displayed in a screen using the text statement variables defined in the screen take precedence over those defined outside it."
    e "スクリーン内でtextステートメントを使用してテキストが表示される場合、スクリーン内で定義されたものは外で定義された変数よりも優先されます。"

# game/tutorial_screen_displayables.rpy:238
translate japanese text_displayable_7e84a5d1:

    # e "Those variables may be parameters given to the screen, defined with the default or python statements, or set using the SetScreenVariable action."
    e "これらの変数は恐らくスクリーンに与えられたか、defaultまたはpythonステートメントによって定義されるか、SetScreenVariableアクションによって設定されたパラメータでしょう。"

# game/tutorial_screen_displayables.rpy:247
translate japanese text_displayable_8bc866c4:

    # e "There's not much more to say about text in screens, as it works the same way as all other text in Ren'Py."
    e "スクリーン内のテキストは、Ren'Pyに含まれる他の全てのテキストと同じように振舞いますので、これ以上言うことはありません。"

# game/tutorial_screen_displayables.rpy:255
translate japanese layout_displayables_d75efbae:

    # e "The layout displayables take other displayables and lay them out on the screen."
    e "レイアウトdisplayableは他のdisplayableを取り、スクリーン上に配置します。"

# game/tutorial_screen_displayables.rpy:269
translate japanese layout_displayables_9a15144d:

    # e "For example, the hbox displayable takes its children and lays them out horizontally."
    e "例えば、hbox displayableはその子を取り水平に配置します。"

# game/tutorial_screen_displayables.rpy:284
translate japanese layout_displayables_48eff197:

    # e "The vbox displayable is similar, except it takes its children and arranges them vertically."
    e "vbox displayableも、子を取って垂直に並べるという点以外は同様です。"

# game/tutorial_screen_displayables.rpy:286
translate japanese layout_displayables_74de8a66:

    # e "Both of the boxes take the box style properties, the most useful of which is spacing, the amount of space to leave between children."
    e "いずれのボックスもボックススタイルのプロパティを取ります。最も便利なのはspacingで、これは子の間に残すスペースの量を指します。"

# game/tutorial_screen_displayables.rpy:301
translate japanese layout_displayables_a156591f:

    # e "The grid displayable displays its children in a grid of equally-sized cells. It takes two arguments, the number of columns and the number of rows."
    e "グリッドdisplayableは、同じサイズのセルで構成されるグリッドの中に子を表示します。これは２つの引数を取ります、列数と行数です。"

# game/tutorial_screen_displayables.rpy:303
translate japanese layout_displayables_126f5816:

    # e "The grid has to be full, or Ren'Py will produce an error. Notice how in this example, the empty cell is filled with a null."
    e "グリッドは全て埋められていなければいけません、そうでなければRen'Pyはエラーを出します。この例でどのようにしているかに注目してください、空のセルはnullで埋められています。"

# game/tutorial_screen_displayables.rpy:305
translate japanese layout_displayables_bfaaaf9b:

    # e "Like the boxes, grid uses the spacing property to specify the space between cells."
    e "このボックスのように、gridはセルの間のスペースを指定するためにspacingプロパティを使います。"

# game/tutorial_screen_displayables.rpy:321
translate japanese layout_displayables_3e931106:

    # e "Grid also takes the transpose property, to make it fill top-to-bottom before it fills left-to-right."
    e "グリッドはtransposeプロパティも取ります。左から右へと埋めるより先に上から下へと埋めることができます。"

# game/tutorial_screen_displayables.rpy:338
translate japanese layout_displayables_afdc1b11:

    # e "And just to demonstrate that all cells are equally-sized, here's what happens when once child is bigger than the others."
    e "また、全てのセルが同じサイズとなるという実演に過ぎませんが、１つの子だけ他より大きければこのようになります。"

# game/tutorial_screen_displayables.rpy:353
translate japanese layout_displayables_a23e2826:

    # e "The fixed displayable displays the children using Ren'Py's normal placement algorithm. This lets you place displayables anywhere in the screen."
    e "fixed displayableはRen'Pyの通常の配置アルゴリズムを使って子を表示します。これによりスクリーンのどのにでもDislayableを配置できます。"

# game/tutorial_screen_displayables.rpy:355
translate japanese layout_displayables_fd3926ca:

    # e "By default, the layout expands to fill all the space available to it. To prevent that, we use the xsize and ysize properties to set its size in advance."
    e "デフォルトでは、レイアウトは利用可能なスペースを埋めるように拡張されます。これを防ぐため、xsizeやysizeプロパティを使って予めサイズを設定しておくことができます。"

# game/tutorial_screen_displayables.rpy:369
translate japanese layout_displayables_eff42786:

    # e "When a non-layout displayable is given two or more children, it's not necessary to create a fixed. A fixed is automatically added, and the children are added to it."
    e "non-layout displayableに２つまたはそれ以上の子を与えられたとしても、必ずしもfixedを生成する必要はありません。fixedが自動で追加され、その中に子が与えられます。"

# game/tutorial_screen_displayables.rpy:384
translate japanese layout_displayables_c32324a7:

    # e "Finally, there's one convenience to save space. When many displayables are nested, adding a layout to each could cause crazy indent levels."
    e "最後に、スペースを節約するのに便利な機能が１つあります。多くのdisplayableがネストしているとき、それらにレイアウトを追加するとインデントのレベルがおかしくなることがあります。"

# game/tutorial_screen_displayables.rpy:386
translate japanese layout_displayables_d7fa0f28:

    # e "The has statement creates a layout, and then adds all further children of its parent to that layout. It's just a convenience to make screens more readable."
    e "hasステートメントはレイアウトを生成し、その親の次からの子をそのレイアウトに追加します。これは単にスクリーンを読みやすくするのに便利です。"

# game/tutorial_screen_displayables.rpy:395
translate japanese window_displayables_14beb786:

    # e "In the default GUI that Ren'Py creates for a game, most user interface elements expect some sort of background."
    e "Ren'Pyがゲーム向けに生成するデフォルトのGUIにおいて、ほとんどのユーザーインターフェース要素は何らかの背景を持つと想定されています。"

# game/tutorial_screen_displayables.rpy:405
translate japanese window_displayables_495d332b:

    # e "Without the background, text can be hard to read. While a frame isn't strictly required, many screens have one or more of them."
    e "背景が無いと、テキストを読むのは困難です。フレームは必ず必要というわけではありませんが、多くのスクリーンは１つまたはそれ以上のフレームを持ちます。"

# game/tutorial_screen_displayables.rpy:417
translate japanese window_displayables_2c0565ab:

    # e "But when I add a background, it's much easier. That's why there are two displayables that are intended to give backgrounds to user interface elements."
    e "ですが、背景を追加するとはるかに読みやすくなります。そのため、ユーザーインターフェイス要素に背景を与えることを目的とした２つのdisplayableがあります。"

# game/tutorial_screen_displayables.rpy:419
translate japanese window_displayables_c7d0968c:

    # e "The two displayables are frame and window. Frame is the one we use above, and it's designed to provide a background for arbitrary parts of the user interface."
    e "この２つのdisplayableというのが、frameとwindowです。frameは上で使用しているもので、ユーザーインターフェイスの任意の部分に背景を与えるように設計されています。"

# game/tutorial_screen_displayables.rpy:423
translate japanese window_displayables_7d843f62:

    # e "On the other hand, the window displayable is very specific. It's used to provide the text window. If you're reading what I'm saying, you're looking at the text window right now."
    e "一方、window displayableは非常に具体的です。これはテキストウィンドウに用いられます。もし私が何を言っているか読んでいるのであれば、ちょうど今あなたはテキストウィンドウを見ているということです。"

# game/tutorial_screen_displayables.rpy:425
translate japanese window_displayables_de5963e4:

    # e "Both frames and windows can be given window style properties, allowing you to change things like the background, margins, and padding around the window."
    e "frameとwindowはいずれもウィンドウスタイルのプロパティを与えることができ、背景やマージン、ウィンドウの周囲の余白を変更できます。"

# game/tutorial_screen_displayables.rpy:433
translate japanese button_displayables_ea626553:

    # e "One of the most flexible displayables is the button displayable, and its textbutton and imagebutton variants."
    e "最も融通の利くdisplayableはbutton displayable、そしてその亜種であるtextbuttonとimagebuttonです。"

# game/tutorial_screen_displayables.rpy:443
translate japanese button_displayables_372dcc0f:

    # e "A button is a displayable that when selected runs an action. Buttons can be selected by clicking with the mouse, by touch, or with the keyboard and controller."
    e "buttonは選択されたときにアクションを実行するためのdisplayableです。buttonはマウスでのクリックやタッチ、キーボードやコントローラーで選択できます。"

# game/tutorial_screen_displayables.rpy:445
translate japanese button_displayables_a6b270ff:

    # e "Actions can do many things, like setting variables, showing screens, jumping to a label, or returning a value. There are many {a=https://www.renpy.org/doc/html/screen_actions.html}actions in the Ren'Py documentation{/a}, and you can also write your own."
    e "アクションによって、変数の設定やスクリーンの表示、ラベルへの移動、値を返すなど多様なことができます。{a=https://ja.renpy.org/doc/html/screen_actions.html}Ren'Pyドキュメンテーション{/a}にはたくさんのアクションが掲載されていますし、あなた自身のアクションを記述もできます。"

# game/tutorial_screen_displayables.rpy:458
translate japanese button_displayables_4c600d20:

    # e "It's also possible to run actions when a button gains and loses focus."
    e "ボタンがフォーカスを得る、又は失うときにアクションを実行も可能です。"

# game/tutorial_screen_displayables.rpy:473
translate japanese button_displayables_47af4bb9:

    # e "A button takes another displayable as children. Since that child can be a layout, it can takes as many children as you want."
    e "ボタンは別のdisplayableを子として取ります。子がレイアウトでもよく、そうすればあなたの望むがままにたくさんの子を取ることができます。"

# game/tutorial_screen_displayables.rpy:483
translate japanese button_displayables_d01adde3:

    # e "In many cases, buttons will be given text. To make that easier, there's the textbutton displayable that takes the text as an argument."
    e "多くの場合、ボタンにはテキストが与えられます。これをより簡単にするため、引数としてテキストを取るtextbutton displayableがあります。"

# game/tutorial_screen_displayables.rpy:485
translate japanese button_displayables_01c551b3:

    # e "Since the textbutton displayable manages the style of the button text for you, it's the kind of button that's used most often in the default GUI."
    e "textbutton displayableはボタンテキストのスタイルを管理するため、デフォルトのGUIで最も頻繁に使用される種類のボタンです。"

# game/tutorial_screen_displayables.rpy:498
translate japanese button_displayables_6911fb9b:

    # e "There's also the imagebutton, which takes displayables, one for each state the button can be in, and displays them as the button."
    e "imagebuttonもあります、これはボタンの状態ごとに１つのdisplayableを取り、ボタンとして表示します。"

# game/tutorial_screen_displayables.rpy:500
translate japanese button_displayables_49720fa6:

    # e "An imagebutton gives you the most control over what a button looks like, but is harder to translate and won't look as good if the game window is resized."
    e "imagebuttonを使用するとボタンの外観を最も細かく定めることができますが、翻訳が難しくなったり、ゲームのウィンドウサイズを変更すると見栄えが悪くなったりします。"

# game/tutorial_screen_displayables.rpy:522
translate japanese button_displayables_e8d40fc8:

    # e "Buttons take Window style properties, that are used to specify the background, margins, and padding. They also take Button-specific properties, like a sound to play on hover."
    e "ボタンはウィンドウスタイルのプロパティを取り、これらは背景やマージン、余白の指定に用いられます。hover時に再生される効果音など、ボタン特有のプロパティも取ります。"

# game/tutorial_screen_displayables.rpy:524
translate japanese button_displayables_1e40e311:

    # e "When used with a button, style properties can be given prefixes like idle and hover to make the property change with the button state."
    e "ボタンで使用する際、スタイルプロパティにidleやhoverなどの接頭辞を与えることで、ボタンの状態に応じてプロパティを変更できます。"

# game/tutorial_screen_displayables.rpy:526
translate japanese button_displayables_220b020d:

    # e "A text button also takes Text style properties, prefixed with text. These are applied to the text displayable it creates internally."
    e "テキストボタンはtextという接頭辞を付けることでテキストスタイルのプロパティも取ります。これらは内部で生成されるtext displayableに適用されます。"

# game/tutorial_screen_displayables.rpy:558
translate japanese button_displayables_b89d12aa:

    # e "Of course, it's prety rare we'd ever customize a button in a screen like that. Instead, we'd create custom styles and tell Ren'Py to use them."
    e "もちろん、このようにスクリーン内でボタンをカスタマイズすることは非常に稀です。代わりに、カスタムスタイルを作りRen'Pyにそれを使うよう指示します。"

# game/tutorial_screen_displayables.rpy:577
translate japanese bar_displayables_946746c2:

    # e "The bar and vbar displayables are flexible displayables that show bars representing a value. The value can be static, animated, or adjustable by the player."
    e "barおよびvbar displayableは、値を表すバーを表示する柔軟なdisplayableです。値は静的としたり、アニメーションとしたり、プレイヤーに調整させることができます。"

# game/tutorial_screen_displayables.rpy:579
translate japanese bar_displayables_af3a51b8:

    # e "The value property gives a BarValue, which is an object that determines the bar's value and range. Here, a StaticValue sets the range to 100 and the value to 66, making a bar that's two thirds full."
    e "valueプロパティは、バーの値とレンジを決定するオブジェクトであるBarValueを与えます。ここで、SaticValueでレンジを100・値を66に設定すると、バーの三分の二が埋まります。"

# game/tutorial_screen_displayables.rpy:581
translate japanese bar_displayables_62f8b0ab:

    # e "A list of all the BarValues that can be used is found {a=https://www.renpy.org/doc/html/screen_actions.html#bar-values}in the Ren'Py documentation{/a}."
    e "全てのBarValueの一覧は{a=https://ja.renpy.org/doc/html/screen_actions.html#bar-values}Ren'Pyのドキュメント{/a}で見ることができます。"

# game/tutorial_screen_displayables.rpy:583
translate japanese bar_displayables_5212eb0a:

    # e "In this example, we give the frame the xsize property. If we didn't do that, the bar would expand to fill all available horizontal space."
    e "こちらの例では、フレームにxsiseプロパティを与えています。そうしなければ、バーは拡張されて水平方向の領域を可能な限り埋め尽くしてしまいます。"

# game/tutorial_screen_displayables.rpy:600
translate japanese bar_displayables_67295018:

    # e "There are a few different bar styles that are defined in the default GUI. The styles are selected by the style property, with the default selected by the value."
    e "いくつかの種類のバースタイルがデフォルトのGUIで定義されていります。そのスタイルはスタイルプロパティーによって選択され、デフォルトは値によって選択されます。"

# game/tutorial_screen_displayables.rpy:602
translate japanese bar_displayables_1b037b21:

    # e "The top style is the 'bar' style. It's used to display values that the player can't adjust, like a life or progress bar."
    e "一つ目のスタイルは'bar'スタイルです。これはライフや進捗といった、プレイヤーが調整できない値を表示します。"

# game/tutorial_screen_displayables.rpy:604
translate japanese bar_displayables_c2aa4725:

    # e "The middle stye is the 'slider' value. It's used for values the player is expected to adjust, like a volume preference."
    e "真ん中のスタイルは'slider'の値です。これはボリュームの設定のようにプレイヤーが調整可能な値に対し使用されます。"

# game/tutorial_screen_displayables.rpy:606
translate japanese bar_displayables_2fc44226:

    # e "Finally, the bottom style is the 'scrollbar' style, which is used for horizontal scrollbars. When used as a scrollbar, the thumb in the center changes size to reflect the visible area of a viewport."
    e "最後に、一番下のスタイルは'scrollbar'スタイルで、これは水平なスクロールバーに用いられます。スクロールバーとして使用すると、中央のつまみのサイズがビューポートの表示領域に応じて変更されます。"

# game/tutorial_screen_displayables.rpy:623
translate japanese bar_displayables_26eb88bf:

    # e "The vbar displayable is similar to the bar displayable, except it uses vertical styles - 'vbar', 'vslider', and 'vscrollbar' - by default."
    e "vbar displayableはbar displayableと似ていますが、verticalスタイルを使用します。デフォルトでは'vbar'や'vslider'、'vscrollbar'がこれに当たります。"

# game/tutorial_screen_displayables.rpy:626
translate japanese bar_displayables_11cf8af2:

    # e "Bars take the Bar style properties, which can customize the look and feel greatly. Just look at the difference between the bar, slider, and scrollbar styles."
    e "バーはバースタイルのプロパティを取り、見た目や雰囲気を大幅に変更できます。bar、slider、scrollbaのスタイルの違いをご確認ください。"

# game/tutorial_screen_displayables.rpy:635
translate japanese imagemap_displayables_d62fad02:

    # e "Imagemaps use two or more images to show buttons and bars. Let me start by showing you an example of an imagemap in action."
    e "イメージマップはボタンやバーを表示するのに２つもしくはそれ以上の画像を使用します。それでは、実際にイメージマップの例をお見せします。"

# game/tutorial_screen_displayables.rpy:657
translate japanese swimming_405542a5:

    # e "You chose swimming."
    e "swimminを選びました。"

# game/tutorial_screen_displayables.rpy:659
translate japanese swimming_264b5873:

    # e "Swimming seems like a lot of fun, but I didn't bring my bathing suit with me."
    e "水泳は楽しそうですが、私は水着を持ってきませんでした。"

# game/tutorial_screen_displayables.rpy:665
translate japanese science_83e5c0cc:

    # e "You chose science."
    e "scienceを選びました。"

# game/tutorial_screen_displayables.rpy:667
translate japanese science_319cdf4b:

    # e "I've heard that some schools have a competitive science team, but to me research is something that can't be rushed."
    e "敵対する科学チームがいくつかの学校にあったので大変でしたが、私にとって研究は急ぐことのできないものでした。"

# game/tutorial_screen_displayables.rpy:672
translate japanese art_d2a94440:

    # e "You chose art."
    e "artを選びました。"

# game/tutorial_screen_displayables.rpy:674
translate japanese art_e6af6f1d:

    # e "Really good background art is hard to make, which is why so many games use filtered photographs. Maybe you can change that."
    e "本当に良い背景画は作るのが大変で、ゆえに多くのゲームにはフィルターをかけた写真が用いられます。きっとあなたはそれを変えることができるでしょう。"

# game/tutorial_screen_displayables.rpy:680
translate japanese home_373ea9a5:

    # e "You chose to go home."
    e "go homeを選びました。"

# game/tutorial_screen_displayables.rpy:686
translate japanese imagemap_done_48eca0a4:

    # e "Anyway..."
    e "ところで…"

# game/tutorial_screen_displayables.rpy:691
translate japanese imagemap_done_a60635a1:

    # e "To demonstrate how imagemaps are put together, I'll show you the five images that make up a smaller imagemap."
    e "イメージマップの組み立て方を実演するために、イメージマップを構成する５つの画像をお見せします。"

# game/tutorial_screen_displayables.rpy:697
translate japanese imagemap_done_ac9631ef:

    # e "The idle image is used for the background of the imagemap, for hotspot buttons that aren't focused or selected, and for the empty part of an unfocused bar."
    e "idleイメージはイメージマップの背景や、フォーカスも選択もされない状態のボタン、フォーカスの当たっていないバーの空の部分となります。"

# game/tutorial_screen_displayables.rpy:703
translate japanese imagemap_done_123b5924:

    # e "The hover image is used for hotspots that are focused but not selected, and for the empty part of a focused bar."
    e "hover画像は、フォーカスは当たっているが選択されていないhotspotや、空の部分はフォーカスが当たったときのバーとして使用されます。"

# game/tutorial_screen_displayables.rpy:705
translate japanese imagemap_done_37f538dc:

    # e "Notice how both the bar and button are highlighted in this image. When we display them as part of a screen, only one of them will show up as focused."
    e "バーとボタンの両方が、このイメージの中のどこでハイライトされるかに注目してください。1つのスクリーンの一部として表示しているときは、いずれか一方のみがフォーカスされているものとして表示されます。"

# game/tutorial_screen_displayables.rpy:711
translate japanese imagemap_done_c76b072d:

    # e "Selected images like this selected_idle image are used for parts of the bar that are filled, and for selected buttons, like the current screen and a checked checkbox."
    e "このselected_idle画像のようなSelected imagesは、埋め尽くされたバーの部分や、現在のスクリーン、チェックされた状態のチェックボックスのように選択されているボタンに用いられます。"

# game/tutorial_screen_displayables.rpy:717
translate japanese imagemap_done_241a4112:

    # e "Here's the selected_hover image. The button here will never be shown, since it will never be marked as selected."
    e "これはselected_hober画像です。ここでのボタンは選択済としてマークされることがないため、この画像は表示されません。"

# game/tutorial_screen_displayables.rpy:723
translate japanese imagemap_done_3d8f454c:

    # e "Finally, an insensitive image can be given, which is used when a hotspot can't be interacted with."
    e "最後に、insensitive画像を与えることができます。これはhotspotに干渉できないときに使用されます。"

# game/tutorial_screen_displayables.rpy:728
translate japanese imagemap_done_ca286729:

    # e "Imagemaps aren't limited to just images. Any displayable can be used where an image is expected."
    e "イメージマップは画像だけに限定されません。画像が要求される部分に対してdisplayableを使用することも可能です。"

# game/tutorial_screen_displayables.rpy:743
translate japanese imagemap_done_6060b17f:

    # e "Here's an imagemap built using those five images. Now that it's an imagemap, you can interact with it if you want to."
    e "こちらが、これまでの５つの画像から生成されたイメージマップになります。今はイメージマップとなっていますので、もし触ってみたければ操作できます。"

# game/tutorial_screen_displayables.rpy:755
translate japanese imagemap_done_c817794d:

    # e "To make this a little more concise, we can replace the five images with the auto property, which replaces '%%s' with 'idle', 'hover', 'selected_idle', 'selected_hover', or 'insensitive' as appropriate."
    e "これをもう少し簡単にするために、５つの画像を自動プロパティに置き換えることができます、こうすることで'%%s'が'idle'や'hover'、'selected_idle'、'selected_hover'、'insensitive'に適切に置換されます。"

# game/tutorial_screen_displayables.rpy:757
translate japanese imagemap_done_c1ed91b8:

    # e "Feel free to omit the selected and insensitive images if your game doesn't need them. Ren'Py will use the idle or hover images to replace them."
    e "もしあなたのゲームが必要としないなら、selectedイメージやinsensitiveイメージは省いてしまってかまいません。Ren'Pyはidle画像やhover画像を使ってこれらを置換します。"

# game/tutorial_screen_displayables.rpy:759
translate japanese imagemap_done_166f75db:

    # e "The hotspot and hotbar statements describe areas of the imagemap that should act as buttons or bars, respectively."
    e "hotspotステートメントやhotbarステートメントはそれぞれ、ボタンやバーとして振舞うべきイメージマップの領域を定めます。"

# game/tutorial_screen_displayables.rpy:761
translate japanese imagemap_done_becb9688:

    # e "Both take the coordinates of the area, in (x, y, width, height) format."
    e "いずれも(x座標, y座標, 幅, 高さ)という形式で領域の座標を取ります。"

# game/tutorial_screen_displayables.rpy:763
translate japanese imagemap_done_fd56baa2:

    # e "A hotspot takes an action that is run when the hotspot is activated. It can also take actions that are run when it's hovered and unhovered, just like a button can."
    e "hotspotはアクティブになったときにアクションを実行します。ボタンのように、フォーカスされたりフォーカスを失ったりしたときにもアクションを取ることができます。"

# game/tutorial_screen_displayables.rpy:765
translate japanese imagemap_done_5660a6a2:

    # e "A hotbar takes a BarValue object that describes how full the bar is, and the range of values the bar should display, just like a bar and vbar does."
    e "hotbarはどのようにバーが埋められているかを描画するBarValueオブジェクトを取り、barやvbarと同じように、バーが表示すべき値のレンジを取ります。"

# game/tutorial_screen_displayables.rpy:772
translate japanese imagemap_done_10496a29:

    # e "A useful pattern is to define a screen with an imagemap that has hotspots that jump to labels, and call that using the call screen statement."
    e "便利なパターンは、ラベルにジャンプするhotspotを持つイメージマップを含むスクリーンを定義し、call screenステートメントを使って呼び出すという使い方です。"

# game/tutorial_screen_displayables.rpy:774
translate japanese imagemap_done_dcb45224:

    # e "That's what we did in the school example I showed before. Here's the script for it. It's long, but the imagemap itself is fairly simple."
    e "これは先ほどお見せした学校の例で使用した方法です。こちらはそのスクリプトです。長いですが、イメージマップ自体はとてもシンプルです。"

# game/tutorial_screen_displayables.rpy:778
translate japanese imagemap_done_5b5bc5e5:

    # e "Imagemaps have pluses and minuses. On one hand, they are easy for a designer to create, and can look very good. At the same time, they can be hard to translate, and text baked into images may be blurry when the window is scaled."
    e "イメージマップには長所と短所があります。デザイナーにとっては生成が容易ですし見た目も良くできます。同時に、翻訳は難しいですし、ウィンドウを拡大縮小したときに画像に含まれる文字がぼやけてしまいます。"

# game/tutorial_screen_displayables.rpy:780
translate japanese imagemap_done_b6cebf2b:

    # e "It's up to you and your team to decide if imagemaps are right for your project."
    e "プロジェクトにおいてイメージマップが適切かどうかの判断は、あなた或いはあなたのチーム次第です。"

# game/tutorial_screen_displayables.rpy:787
translate japanese viewport_displayables_e509d50d:

    # e "Sometimes, you'll want to display something bigger than the screen. That's what the viewport displayable is for."
    e "時にスクリーンより大きなものを表示したくなることがあるかと思います。そのようなときに使えるのがビューポートです。"

# game/tutorial_screen_displayables.rpy:803
translate japanese viewport_displayables_9853b0e3:

    # e "Here's an example of a simple viewport, used to display a single image that's far bigger than the screen. Since the viewport will expand to the size of the screen, we use the xysize property to make it smaller."
    e "こちらはビューポートの例です、スクリーンより大きな１枚絵を表示しています。ビューポートがスクリーンのサイズより大きくなってしまうときは、xysizeプロパティで小さくします。"

# game/tutorial_screen_displayables.rpy:805
translate japanese viewport_displayables_778668c8:

    # e "By default the viewport can't be moved, so we give the draggable, mousewheel, and arrowkeys properties to allow it to be moved in multiple ways."
    e "デフォルトのままではビューポートが動かせないので、draggableプロパティやmousewheelプロパティ、arrowkeysプロパティを与えて多様な方法で動かせるようにします。"

# game/tutorial_screen_displayables.rpy:820
translate japanese viewport_displayables_bbd63377:

    # e "When I give the viewport the edgescroll property, the viewport automatically scrolls when the mouse is near its edges. The two numbers are the size of the edges, and the speed in pixels per second."
    e "ビューポートにedgescrollプロパティを与えると、マウスが端に近づいたときにビューポートが自動でスクロールします。２つの数字はエッヂの大きさと、１秒あたりに進むピクセル数で表される速さです。"

# game/tutorial_screen_displayables.rpy:839
translate japanese viewport_displayables_7c4678ee:

    # e "Giving the viewport the scrollbars property surrounds it with scrollbars. The scrollbars property can take 'both', 'horizontal', and 'vertical' as values."
    e "ビューポートを囲うスクロールバーのプロパティを与えます。スクロールバープロパティは値として'both'、'horizontal'、'vertical'を取ります。"

# game/tutorial_screen_displayables.rpy:841
translate japanese viewport_displayables_197953b5:

    # e "The spacing property controls the space between the viewport and its scrollbars, in pixels."
    e "spacingプロパティはビューポートとそのスクロールバーとの間隔をピクセル数で制御します。"

# game/tutorial_screen_displayables.rpy:864
translate japanese viewport_displayables_54dd6e7b:

    # e "The xinitial and yinitial properties set the initial amount of scrolling, as a fraction of the amount that can be scrolled."
    e "xinitialプロパティとyinitialプロパティは、全体に対するスクロールされた量の割合でもってスクロールの初期値を指定します。"

# game/tutorial_screen_displayables.rpy:885
translate japanese viewport_displayables_c047efb5:

    # e "Finally, there's the child_size property. To explain what it does, I first have to show you what happens when we don't have it."
    e "最後に、child_sizeプロパティがあります。これがどのようなものか説明するために、これが無いと何が起きるかを始めにお見せします。"

# game/tutorial_screen_displayables.rpy:887
translate japanese viewport_displayables_c563019f:

    # e "As you can see, the text wraps. That's because Ren'Py is offering it space that isn't big enough."
    e "ご覧の通り、テキストが折り返されます。これはRen'Pyが十分に大きくないスペースを提供しているためです。" #TODO(折り返されて表示されない)

# game/tutorial_screen_displayables.rpy:909
translate japanese viewport_displayables_4bcf0ad0:

    # e "When we give the screen a child_size, it offers more space to its children, allowing scrolling. It takes a horizontal and vertical size. If one component is None, it takes the size of the viewport."
    e "child_sizeを与えると、その子よりも大きなスペースを提供してスクロールを可能にします。これは水平および垂直方向のサイズを取ります。いずれかがNoneであればビューポートのサイズを取ります。"

# game/tutorial_screen_displayables.rpy:936
translate japanese viewport_displayables_ae4ff821:

    # e "Finally, there's the vpgrid displayable. It combines a viewport and a grid into a single displayable, except it's more efficient than either, since it doesn't have to draw every child."
    e "最後に、vpgrid displayableというものがあります。これはビューポートとグリッドを１つのdisplayableに兼ね備えたものです。それぞれの子を描画する必要がないので、個別に使うより効果的です。"

# game/tutorial_screen_displayables.rpy:938
translate japanese viewport_displayables_71fa0b8f:

    # e "It takes the cols and rows properties, which give the number of rows and columns of children. If one is omitted, Ren'Py figures it out from the other and the number of children."
    e "これはcolsプロパティとrowsプロパティを取り、子の行数(row)と列数(column)を与えることができます。一方が省略されると、もう一方と子の数からRen'Pyが計算します。"

translate japanese strings:

    # game/tutorial_screen_displayables.rpy:9
    old "Common properties all displayables share."
    new "全てのdisplayableが持つ共通のプロパティ"

    # game/tutorial_screen_displayables.rpy:9
    old "Adding images and other displayables."
    new "画像やその他のdisplayableを追加"

    # game/tutorial_screen_displayables.rpy:9
    old "Text."
    new "テキスト"

    # game/tutorial_screen_displayables.rpy:9
    old "Boxes and other layouts."
    new "ボックスとその他のレイアウト"

    # game/tutorial_screen_displayables.rpy:9
    old "Windows and frames."
    new "ウィンドウとフレーム"

    # game/tutorial_screen_displayables.rpy:9
    old "Buttons."
    new "ボタン"

    # game/tutorial_screen_displayables.rpy:9
    old "Bars."
    new "バー"

    # game/tutorial_screen_displayables.rpy:9
    old "Viewports."
    new "ビューポート"

    # game/tutorial_screen_displayables.rpy:9
    old "Imagemaps."
    new "イメージマップ"

    # game/tutorial_screen_displayables.rpy:9
    old "That's all for now."
    new "今は十分です。"

    # game/tutorial_screen_displayables.rpy:55
    old "This uses position properties."
    new "これは位置プロパティを使っています。"

    # game/tutorial_screen_displayables.rpy:63
    old "And the world turned upside down..."
    new "そして世界は上下に反転します…"

    # game/tutorial_screen_displayables.rpy:115
    old "Flight pressure in tanks."
    new "タンク飛行圧力"

    # game/tutorial_screen_displayables.rpy:116
    old "On internal power."
    new "内部電源オン"

    # game/tutorial_screen_displayables.rpy:117
    old "Launch enabled."
    new "発射可能"

    # game/tutorial_screen_displayables.rpy:118
    old "Liftoff!"
    new "発射！"

    # game/tutorial_screen_displayables.rpy:232
    old "The answer is [answer]."
    new "答えは[answer]。"

    # game/tutorial_screen_displayables.rpy:244
    old "Text tags {color=#c8ffc8}work{/color} in screens."
    new "スクリーン内でもテキストタグは{color=#c8ffc8}有効です{/color}。"

    # game/tutorial_screen_displayables.rpy:336
    old "Bigger"
    new "より大きい"

    # game/tutorial_screen_displayables.rpy:401
    old "This is a screen."
    new "これはスクリーンです"

    # game/tutorial_screen_displayables.rpy:402
    old "Okay"
    new "了解"

    # game/tutorial_screen_displayables.rpy:440
    old "You clicked the button."
    new "あなたはボタンを押しました。"

    # game/tutorial_screen_displayables.rpy:441
    old "Click me."
    new "私をクリックしてください。"

    # game/tutorial_screen_displayables.rpy:453
    old "You hovered the button."
    new "ボタンにフォーカスしました。"

    # game/tutorial_screen_displayables.rpy:454
    old "You unhovered the button."
    new "ボタンから離れました。"

    # game/tutorial_screen_displayables.rpy:470
    old "Heal"
    new "治癒"

    # game/tutorial_screen_displayables.rpy:479
    old "This is a textbutton."
    new "これはテキストボタンです。"

    # game/tutorial_screen_displayables.rpy:539
    old "Or me."
    new "もしくは私。"

    # game/tutorial_screen_displayables.rpy:541
    old "You clicked the other button."
    new "他のボタンをクリックしました。"

    # game/tutorial_screen_displayables.rpy:880
    old "This text is wider than the viewport."
    new "このテキストはビューポートより幅が広いです。"
