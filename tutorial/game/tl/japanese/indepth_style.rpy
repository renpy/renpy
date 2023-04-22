
# game/indepth_style.rpy:40
translate japanese new_gui_17a0326e:

    # e "When you create a new project, Ren'Py will automatically create a GUI - a Graphical User Interface - for it."
    e "新しいプロジェクトを作成すると、それに対して自動的にGUI(Graphical User Interface)が作成されます。"

# game/indepth_style.rpy:42
translate japanese new_gui_12c814ed:

    # e "It defines the look of both in-game interface, like this text box, and out-of-game interface like the main and game menus."
    e "これがこのテキストボックスのようなゲーム中のインターフェースとメインメニューやゲームメニューのようなゲーム外のインターフェースの両方を定義します。"

# game/indepth_style.rpy:44
translate japanese new_gui_0a2a73bb:

    # e "The default GUI is meant to be nice enough for a simple project. With a few small changes, it's what you're seeing in this game."
    e "デフォルトのGUIは簡単なプロジェクトには十分でしょう。少し変更すれば、このゲームのようになります。"

# game/indepth_style.rpy:46
translate japanese new_gui_22adf68e:

    # e "The GUI is also meant to be easy for an intermediate creator to customize. Customizing the GUI consists of changing the image files in the gui directory, and changing variables in gui.rpy."
    e "GUIは慣れた製作者なら簡単にカスタマイズできます。GUIのカスタマイズはguiディレクトリの画像ファイルの置き換えとgui.rpyの変数変更で行います。"

# game/indepth_style.rpy:48
translate japanese new_gui_da21de30:

    # e "At the same time, even when customized, the default GUI might be too recognizable for an extremely polished game. That's why we've made it easy to totally replace."
    e "同時に、カスタマイズしてさえ、殊に洗練されたゲームに対してはデフォルトGUIははっきりし過ぎるかもしれません。そのために全体的な置き換えを簡単にしています" #TODO

# game/indepth_style.rpy:50
translate japanese new_gui_45765574:

    # e "We've put an extensive guide to customizing the GUI on the Ren'Py website. So if you want to learn more, visit the {a=https://www.renpy.org/doc/html/gui.html}GUI customization guide{/a}."
    e "Ren'PyウェブサイトのGUIカスタマイズに膨大なガイドがありますので、詳細は{a=https://ja.renpy.org/doc/html/gui.html}GUIカスタマイズガイド{/a}を参照してください。"

# game/indepth_style.rpy:58
translate japanese styles_fa345a38:

    # e "Ren'Py has a powerful style system that controls what displayables look like."
    e "Ren'PyにはDisplayableの外見を制御するパワフルなスタイルシステムがあります。"

# game/indepth_style.rpy:60
translate japanese styles_6189ee12:

    # e "While the default GUI uses variables to provide styles with sensible defaults, if you're replacing the GUI or creating your own screens, you'll need to learn about styles yourself."
    e "デフォルトGUIでは変数を使ってスタイルにデフォルトの値を提供していましたが、GUIを置き換えたり自分でスクリーンを作成するならスタイルを学ばなけれあばなりません。"

# game/indepth_style.rpy:66
translate japanese styles_menu_a4a6913e:

    # e "What would you like to know about styles?" nointeract
    e "スタイルについて何を知りたいですか？" nointeract

# game/indepth_style.rpy:98
translate japanese style_basics_9a79ef89:

    # e "Styles let a displayable look different from game to game, or even inside the same game."
    e "スタイルはDisplayableにゲームごとにも、同じゲーム内でも多様な外見をとらせます。"

# game/indepth_style.rpy:103
translate japanese style_basics_48777f2c:

    # e "Both of these buttons use the same displayables. But since different styles have been applied, the buttons look different from each other."
    e "これらのボタンはどちらも同じDisplayableですが、異なるスタイルが適用されているため、ボタンの外観が互いに異なっています。"

# game/indepth_style.rpy:108
translate japanese style_basics_57704d8c:

    # e "Styles are a combination of information from four different places."
    e "スタイルは4つの異なる指定方法からの情報で構成されます。"

# game/indepth_style.rpy:121
translate japanese style_basics_144731f6:

    # e "The first place Ren'Py can get style information from is part of a screen. Each displayable created by a screen can take a style name and style properties."
    e "Ren'Pyにスタイルの情報を指定できる一つ目の方法はスクリーンに含めることです。スクリーンで作成される各Displayableはスタイル名とスタイルプロパティーをとれます。"

# game/indepth_style.rpy:138
translate japanese style_basics_67e48162:

    # e "When a screen displayable contains text, style properties prefixed with text_ apply to that text."
    e "スクリーンDisplayableにテキストがあれば、text_が接頭辞につくスタイルプロパティーがそのテキストに適用されます。"

# game/indepth_style.rpy:151
translate japanese style_basics_03516b4a:

    # e "The next is as part of a displayable created in an image statement. Style properties are just arguments to the displayable."
    e "二つ目の方法はimageステートメントで作成されるDisplayableの含めることです。スタイルプロパティーは単にDisplayableの引数になります。"

# game/indepth_style.rpy:160
translate japanese style_basics_ccc0d1ca:

    # egreen "Style properties can also be given as arguments when defining a character."
    egreen "スタイルプロパティーはキャラクター定義時にも引数として与えられます。"

# game/indepth_style.rpy:162
translate japanese style_basics_013ab314:

    # egreen "Arguments beginning with who_ are style properties applied to the character's name, while those beginning with what_ are applied to the character's dialogue."
    egreen "who_で始まる引数はキャラクター名に、what_はキャラクターの台詞に適用されるスタイルプロパティーです。"

# game/indepth_style.rpy:164
translate japanese style_basics_dbe80939:

    # egreen "Style properties that don't have a prefix are also applied to the character's name."
    egreen "接頭辞のないスタイルプロパティーもキャラクター名に適用されます。"

# game/indepth_style.rpy:174
translate japanese style_basics_ac6a8414:

    # e "Finally, there is the the style statement, which creates or changes a named style. By giving Text the style argument, we tell it to use the blue_text style."
    e "最後はstyleステートメントで、これは名前つきのスタイルを作成または変更します。Textにstyle引数を与えて、blue_textスタイルを使用するよう指示します。"

# game/indepth_style.rpy:180
translate japanese style_basics_3d9bdff7:

    # e "A style property can inherit from a parent. If a style property is not given in a style, it comes from the parent of that style."
    e "スタイルプロパティーは親から継承されます。スタイルで指定されないスタイルプロパティーはそのスタイルの親から継承されます。"

# game/indepth_style.rpy:182
translate japanese style_basics_49c5fbfe:

    # e "By default the parent of the style has the same name, with the prefix up to the the first underscore removed. If the style does not have an underscore in its name, 'default' is used."
    e "デフォルトでは、スタイルの親は最初の接頭辞が除去された同じ名前であり、スタイル名にアンダースコアがなければ'default'が使用されます。"

# game/indepth_style.rpy:184
translate japanese style_basics_6ab170a3:

    # e "For example, blue_text inherits from text, which in turn inherits from default. The default style defines all properties, so it doesn't inherit from anything."
    e "例えば、blue_textはtextから、次にtextはdefaultから継承されます。defaultスタイルはすべてのプロパティーを定義し、他からは継承されません。"

# game/indepth_style.rpy:190
translate japanese style_basics_f78117a7:

    # e "The parent can be explicitly changed by giving the style statement an 'is' clause. In this case, we're explictly setting the style to the parent of text."
    e "親は'is'を与えて明示的に変更できます。この例では、スタイルの親にtextを設定しています。"

# game/indepth_style.rpy:194
translate japanese style_basics_6007040b:

    # e "Each displayable has a default style name. By default, it's usually the lower-case displayable name, like 'text' for Text, or 'button' for buttons."
    e "各Displayableにはデフォルトのスタイル名があり、Textに対する'text', buttonに体する'button'のように通常そのDisplayableの小文字となります。"

# game/indepth_style.rpy:196
translate japanese style_basics_35db9a05:

    # e "In a screen, a displayable can be given the style_prefix property to give a prefix for that displayable and it's children."
    e "スクリーンでは、Displayableにstyle_prefixプロパティーを与えて、そのDisplayableとその子に対する接頭辞を指定できます。"

# game/indepth_style.rpy:198
translate japanese style_basics_422a87f7:

    # e "For example, a text displayable with a style_prefix of 'help' will be given the style 'help_text'."
    e "例えば、style_prefixが'help'のtext Displayableは'help_text'スタイルが適用されます。"

# game/indepth_style.rpy:200
translate japanese style_basics_bad2e207:

    # e "Lastly, when a displayable is a button, or inside a button, it can take style prefixes."
    e "最後に、Displayableがbuttonまたはbutton内部のものならば、スタイル接頭辞が受け取とれます。"

# game/indepth_style.rpy:202
translate japanese style_basics_22ed20a1:

    # e "The prefixes idle_, hover_, and insensitive_ are used when the button is unfocused, focused, and unfocusable."
    e "idle_,  hover_,  insensitive_接頭辞はそのボタンがそれぞれフォーカスされていない、いる、できない場合に使用されます。"

# game/indepth_style.rpy:204
translate japanese style_basics_7a58037e:

    # e "These can be preceded by selected_ to change how the button looks when it represents a selected value or screen."
    e "これらはselected_より優先されボタンの外観を変更します。"

# game/indepth_style.rpy:233
translate japanese style_basics_0cdcb8c3:

    # e "This screen shows the style prefixes in action. You can click on a button to select it, or click outside to advance."
    e "このスクリーンはアクションに応じてそのスタイル接頭辞で表示します。ボタンはクリックで選択でき、他をクリックすれば先へ進めます。"

# game/indepth_style.rpy:240
translate japanese style_basics_aed05094:

    # e "Those are the basics of styles. If GUI customization isn't enough for you, styles let you customize just about everything in Ren'Py."
    e "これらがスタイルの基本です。GUIカスタマイズでは不満ならば、スタイルを用いてRen'Pyのすべてをカスタマイズできます。"

# game/indepth_style.rpy:253
translate japanese style_general_81f3c8ff:

    # e "The first group of style properties that we'll go over are the general style properties. These work with every displayable, or at least many different ones."
    e "紹介する最初のスタイルプロパティーは一般的なスタイルプロパティーです。これらはすべてのDisplayableないしは多くの場所で動作します。"

# game/indepth_style.rpy:264
translate japanese style_general_a8d99699:

    # e "Every displayable takes the position properties, which control where it can be placed on screen. Since I've already mentioned them, I won't repeat them here."
    e "全てのDisplayableは位置プロパティーをとり、スクリーンのどこに配置されるかを制御します。既に述べているのでここでは省きます。"

# game/indepth_style.rpy:275
translate japanese style_general_58d4a18f:

    # e "The xmaximum and ymaximum properties set the maximum width and height of the displayable, respectively. This will cause Ren'Py to shrink things, if possible."
    e "xmaximumとymaximumプロパティーはそれぞれDisplayableの最大幅と高さを設定します。これは可能ならばRen'Pyに対象を縮めさせます。"

# game/indepth_style.rpy:277
translate japanese style_general_cae9a39f:

    # e "Sometimes, the shrunken size will be smaller than the size given by xmaximum and ymaximum."
    e "ときに、縮んだサイズはxmaximumとymaximumで指定したサイズより小さくなります。"

# game/indepth_style.rpy:279
translate japanese style_general_5928c24e:

    # e "Similarly, the xminimum and yminimum properties set the minimum width and height. If the displayable is smaller, Ren'Py will try to make it bigger."
    e "同様に、xminimumとyminimumプロパティーも最小の幅と高さを設定します。そのDisplayableがより小さければ、Ren'Pyは拡大します。"

# game/indepth_style.rpy:289
translate japanese style_general_35a8ee5e:

    # e "The xsize and ysize properties set the minimum and maximum size to the same value, fixing the size."
    e "xsizeとysizeプロパティーは最小と最大サイズの値を同じにしてサイズを固定します。"

# game/indepth_style.rpy:291
translate japanese style_general_fcfb0640:

    # e "These only works for displayables than can be resized. Some displayables, like images, can't be made bigger or smaller."
    e "これらはリサイズ可能なDisplayableに対してのみ動作します。画像のようないくつかのDisplayableは拡大縮小できません。"

# game/indepth_style.rpy:299
translate japanese style_general_cd5cc97c:

    # e "The area property takes a tuple - a parenthesis bounded list of four items. The first two give the position, and the second two the size."
    e "areaプロパティーは4要素のタプルをとり、最初の2つが位置を、残りがサイズを指定します。"

# game/indepth_style.rpy:308
translate japanese style_general_e5a58f0b:

    # e "Finally, the alt property changes the text used by self-voicing for the hearing impaired."
    e "最後に、altプロパティーは聴覚障害者向けのセルフボイシングで使用されるテキストを変更します。"

# game/indepth_style.rpy:335
translate japanese style_text_fe457b8f:

    # e "The text style properties apply to text and input displayables."
    e "textスタイルプロパティーはTextとInput Displayableに使用されます。"

# game/indepth_style.rpy:337
translate japanese style_text_7ab53f03:

    # e "Text displayables can be created implicitly or explicitly. For example, a textbutton creates a text displayable with a style ending in button_text."
    e "Text Displayableは暗黙的にまたは明示的に作成されます。例えば、テキストボタンはbutton_textで終わるスタイルのtext Displayableを作成します。"

# game/indepth_style.rpy:339
translate japanese style_text_6dd42a57:

    # e "These can also be set in gui.rpy by changing or defining variables with names like gui.button_text_size."
    e "これらはgui.rpyでgui.button_text_sizeのような名前の変数を変更または定義しても設定できます。"

# game/indepth_style.rpy:347
translate japanese style_text_c689130e:

    # e "The bold style property makes the text bold. This can be done using an algorithm, rather than a different version of the font."
    e "boldスタイルプロパティーはテキストを太字にします。これはフォントを替えずにアルゴリズムで実行します。"

# game/indepth_style.rpy:355
translate japanese style_text_3420bfe4:

    # e "The color property changes the color of the text. It takes hex color codes, just like everything else in Ren'Py."
    e "colorプロパティーはテキストの色を変更します。他と同様に16進数のコードをとります。"

# game/indepth_style.rpy:363
translate japanese style_text_14bd6327:

    # e "The first_indent style property determines how far the first line is indented."
    e "first_indentプロパティーは最初の行のインデント量を決めます。"

# game/indepth_style.rpy:371
translate japanese style_text_779ac517:

    # e "The font style property changes the font the text uses. Ren'Py takes TrueType and OpenType fonts, and you'll have to include the font file as part of your visual novel."
    e "fontスタイルプロパティーはテキストのフォントを変更します。TrueTypeとOpenTypeフォントが使用でき、そのフォントファイルをあなたのビジュアルノベルに含めなければなりません。"

# game/indepth_style.rpy:379
translate japanese style_text_917e2bca:

    # e "The size property changes the size of the text."
    e "sizeプロパティーはテキストのサイズを変更します。"

# game/indepth_style.rpy:388
translate japanese style_text_1a46cd43:

    # e "The italic property makes the text italic. Again, this is better done with a font, but for short amounts of text Ren'Py can do it for you."
    e "italicプロパティーはテキストをイタリックにします。これはフォントを変更する方がよいのですが、少量のテキストに使えます。"

# game/indepth_style.rpy:397
translate japanese style_text_472f382d:

    # e "The justify property makes the text justified, lining all but the last line up on the left and the right side."
    e "justifyプロパティーはテキストをすべてに両端ぞろえで並べますが、最終行は左または右側に寄せます。"

# game/indepth_style.rpy:405
translate japanese style_text_87b075f8:

    # e "The kerning property kerns the text. When it's negative, characters are closer together. When positive, characters are farther apart."
    e "kerningプロパティーはテキストのカーニングをします。負なら文字は互いに近づき、正なら離れます。"

# game/indepth_style.rpy:415
translate japanese style_text_fe7dec14:

    # e "The line_leading and line_spacing properties put spacing before each line, and between lines, respectively."
    e "line_leading, line_spacingプロパティーはそれぞれ各行の前と行同士の間にスペースを置きます。"

# game/indepth_style.rpy:424
translate japanese style_text_aee9277a:

    # e "The outlines property puts outlines around text. This takes a list of tuples, which is a bit complicated."
    e "outlinesプロパティーはテキスト回りにアウトラインを付けます。これは少し複雑なタプルのリストをとります。"

# game/indepth_style.rpy:426
translate japanese style_text_b4c5190f:

    # e "But if you ignore the brackets and parenthesis, you have the width of the outline, the color, and then horizontal and vertical offsets."
    e "しかし、括弧を無視すればそれぞれアウトラインの幅と色、水平、垂直方向のオフセットです。"

# game/indepth_style.rpy:434
translate japanese style_text_5a0c2c02:

    # e "The rest_indent property controls the indentation of lines after the first one."
    e "rest_indentプロパティーは一行目以降の行のインデントを制御します。"

# game/indepth_style.rpy:443
translate japanese style_text_430c1959:

    # e "The textalign property controls the positioning of multiple lines of text inside the text displayable. For example, 0.5 means centered."
    e "textalignプロパティーはtext Displayable内の複数行の配置を制御します。例えば、0.5は中央です。"

# game/indepth_style.rpy:445
translate japanese style_text_19aa0833:

    # e "It doesn't change the position of the text displayable itself. For that, you'll often want to set the textalign and xalign to the same value."
    e "text Displayable自体の位置は変更しません。そのため、textalignとxalignは同じ値にすることが多いでしょう。"

# game/indepth_style.rpy:455
translate japanese style_text_efc3c392:

    # e "When both textalign and xalign are set to 1.0, the text is properly right-justified."
    e "textalignとxalignが共に1.0だと、テキストは右寄せになります。"

# game/indepth_style.rpy:464
translate japanese style_text_43be63b9:

    # e "The underline property underlines the text."
    e "underlineプロパティーはテキストにアンダーラインを引きます。"

# game/indepth_style.rpy:471
translate japanese style_text_343f6d34:

    # e "Those are the most common text style properties, but not the only ones. Here are a few more that you might need in special circumstances."
    e "これらはよく使われるtextスタイルプロパティーですが、これだけではありません。ここで、特定の状況で必要となるものを紹介します。"

# game/indepth_style.rpy:479
translate japanese style_text_e7204a95:

    # e "By default, text in Ren'Py is antialiased, to smooth the edges. The antialias property can turn that off, and make the text a little more jagged."
    e "デフォルトでは、Ren'Pyのテキストはアンチエイリアシングでエッジを滑らかにしています。antialiasプロパティーはオフにしてテキストを少しジャギーにできます。"

# game/indepth_style.rpy:487
translate japanese style_text_a5316e4c:

    # e "The adjust_spacing property is a very subtle one, that only matters when a player resizes the window. When True, characters will be shifted a bit so the Text has the same relative spacing."
    e "adjust_spacingプロパティーはプレイヤーがウィンドウをリサイズするときのみ問題になり、Trueなら文字は少しずれてテキストは相対的に同じスペースを保ちます。"

# game/indepth_style.rpy:496
translate japanese style_text_605d4e4a:

    # e "When False, the text won't jump around as much. But it can be a little wider or narrower based on screen size."
    e "Falseなら、それほど大きな変化にはなりませんが、ウィンドウのサイズに応じて少し広く、または狭くなるかもしれません。"

# game/indepth_style.rpy:505
translate japanese style_text_acf8a0e1:

    # e "The layout property has a few special values that control where lines are broken. The 'nobreak' value disables line breaks entirely, making the text wider."
    e "layoutプロパティーは特別な値でどこで行を改行するかを制御します。'nobreak'は改行を完全に停止し、テキストを広くします。"

# game/indepth_style.rpy:516
translate japanese style_text_785729cf:

    # e "When the layout property is set to 'subtitle', the line breaking algorithm is changed to try to make all lines even in length, as subtitles usually are."
    e "layoutプロパティーが'subtitle'ではサイブタイトルが通常するようにすべての行の長さをそろえようとするアルゴリズムに変更します。"

# game/indepth_style.rpy:524
translate japanese style_text_9c26f218:

    # e "The strikethrough property draws a line through the text. It seems pretty unlikely you'd want to use this one."
    e "strikethroughプロパティーはテキストに斜線を引きます。これを使いたい機会はあまりありそうもありませんが。"

# game/indepth_style.rpy:534
translate japanese style_text_c7229243:

    # e "The vertical style property places text in a vertical layout. It's meant for Asian languages with special fonts."
    e "verticalスタイルプロパティーはテキストを縦書きにします。アジア言語用の特別なフォントが必要です。"

# game/indepth_style.rpy:540
translate japanese style_text_724bd5e0:

    # e "And those are the text style properties. There might be a lot of them, but we want to give you a lot of control over how you present text to your players."
    e "これらがtextスタイルプロパティーです。多いかもしれませんが、プレイヤーへのテキスト表示を制御する多くの方法を提供できたと思います。"

# game/indepth_style.rpy:580
translate japanese style_button_300b6af5:

    # e "Next up, we have the window and button style properties. These apply to windows like the text window at the bottom of this screen and frames like the ones we show examples in."
    e "次に、windowとbuttonスタイルプロパティーを紹介します。これらはこの画面下部のテキストウィンドウのようなウィンドウと例に表示しているもののようなフレームに適用されます。"

# game/indepth_style.rpy:582
translate japanese style_button_255a18e4:

    # e "These properties also apply to buttons, in-game and out-of-game. To Ren'Py, a button is a window you can click."
    e "これらのプロパティーはゲーム内またはゲーム外のボタンにも適用されます。Ren'Pyにとってはボタンはクリックできるウィンドウです。"

# game/indepth_style.rpy:593
translate japanese style_button_9b53ce93:

    # e "I'll start off with this style, which everything will inherit from. To make our lives easier, it inherits from the default style, rather than the customizes buttons in this game's GUI."
    e "このスタイルから始めます。これはすべてのスタイルが継承します。簡単のため、ゲームのGUIでカスタマイズされたボタンではなくデフォルトスタイルから継承します。"

# game/indepth_style.rpy:595
translate japanese style_button_aece4a8c:

    # e "The first style property is the background property. It adds a background to the a button or window. Since this is a button, idle and hover variants choose different backgrounds when focused."
    e "最初のスタイルプロパティーはbackgroundプロパティーです。ボタンやウィンドウに背景を加えます。これはボタンなのでフォーカスに合わせてidleとhoverで異なる背景を選びます。"

# game/indepth_style.rpy:597
translate japanese style_button_b969f04a:

    # e "We also center the two buttons, using the xalign position property."
    e "xalign位置プロパティーを使用して2つのボタンを中央寄せもしています。"

# game/indepth_style.rpy:601
translate japanese style_button_269ae069:

    # e "We've also customized the style of the button's text, using this style. It centers the text and makes it change color when hovered."
    e "ボタンのテキストのスタイルもカスタマイズします。テキストを中央寄せし、ホバー時には色を変えます。"

# game/indepth_style.rpy:612
translate japanese style_button_1009f3e1:

    # e "Without any padding around the text, the button looks odd. Ren'Py has padding properties that add space inside the button's background."
    e "テキスト回りをパッディングしないとボタンが奇妙に見えます。Ren'Pyには padding プロパティーがあり、ボタンの背景の内側に空間を追加します。"

# game/indepth_style.rpy:621
translate japanese style_button_5bdfa45a:

    # e "More commonly used are the xpadding and ypadding style properties, which add the same padding to the left and right, or the top and bottom, respectively."
    e "よく使われるのはxpaddingとypaddingスタイルプロパティーで、それぞれ左右または上下に同じ値のパッディングをします。"

# game/indepth_style.rpy:629
translate japanese style_button_81283d42:

    # e "The margin style properties work the same way, except they add space outside the background. The full set exists: left_margin, right_margin, top_margin, bottom_margin, xmargin, and ymargin."
    e "marginスタイルプロパティーも背景の外側に空間を追加する以外は同様に動作します。次のセットが用意されています: left_margin, right_margin, top_margin, bottom_margin, xmargin, ymargin"

# game/indepth_style.rpy:638
translate japanese style_button_0b7aca6b:

    # e "The size_group style property takes a string. Ren'Py will make sure that all the windows or buttons with the same size_group string are the same size."
    e "size_groupスタイルプロパティーは文字列をとります。Ren'Pyは同じsize_groupに属するすべてのウィンドウやボタンが同じサイズになると保証します。"

# game/indepth_style.rpy:647
translate japanese style_button_4c6da7d9:

    # e "Alternatively, the xfill and yfill style properties make a button take up all available space in the horizontal or vertical directions."
    e "他にxfillとyfillスタイルプロパティーは水平または垂直方向ですべての利用可能な空間までボタンを広げてもよいです。"

# game/indepth_style.rpy:657
translate japanese style_button_fd5338b2:

    # e "The foreground property gives a displayable that is placed on top of the contents and background of the window or button."
    e "foregroundプロパティーはウィンドウやボタンの中身と背景の一番上に配置されるDisplayableを指定します。"

# game/indepth_style.rpy:659
translate japanese style_button_b8af697c:

    # e "One way to use it is to provide extra decorations to a button that's serving as a checkbox. Another would be to use it with a Frame to provide a glossy shine that overlays the button's contents."
    e "チェックボックスのようなものがあるボタンに追加の修飾をするのに使ったり、ボタンを覆う鮮やかな光沢のようなフレームに使うとよいでしょう。"

# game/indepth_style.rpy:668
translate japanese style_button_c0b1b62e:

    # e "There are also a few style properties that only apply to buttons. The hover_sound and activate_sound properties play sound files when a button is focused and activated, respectively."
    e "ボタンにのみ適用されるスタイルプロパティーも少しあります。hover_soundやactivate_soundプロパティーはボタンがフォーカスされたり押されたときにそれぞれファイルを再生します。"

# game/indepth_style.rpy:677
translate japanese style_button_02fa647e:

    # e "Finally, the focus_mask property applies to partially transparent buttons. When it's set to True, only areas of the button that aren't transparent cause a button to focus."
    e "最後に、focus_maskプロパティーは一部が透明なボタンに適用されます。Trueに設定されるとそのボタンの不透明な部分だけがフォーカスをとります。"

# game/indepth_style.rpy:757
translate japanese style_bar_414d454a:

    # e "To demonstrate styles, let me first show two of the images we'll be using. This is the image we're using for parts of the bar that are empty."
    e "スタイルのデモンストレーションのため、まずは2つの画像を表示します。これは空のバーの画像です。"

# game/indepth_style.rpy:761
translate japanese style_bar_9422b7b0:

    # e "And here's what we use for parts of the bar that are full."
    e "それてこちらは満タンのバーの画像です。"

# game/indepth_style.rpy:773
translate japanese style_bar_8ae6a14b:

    # e "The left_bar and right_bar style properties, and their hover variants, give displayables for the left and right side of the bar. By default, the value is shown on the left."
    e "left_barとright_barスタイルプロパティーとそれぞれのhoverバージョンはバーの左右の側のDisplayableを指定します。デフォルトでは左側に値が表示されます。"

# game/indepth_style.rpy:775
translate japanese style_bar_7f0f50e5:

    # e "Also by default, both the left and right displayables are rendered at the full width of the bar, and then cropped to the appropriate size."
    e "また、デフォルトでは左右のDisplayableはバーの最大幅でレンダリングされ、適切なサイズに切り取られます。"

# game/indepth_style.rpy:777
translate japanese style_bar_9ef4f62f:

    # e "We give the bar the ysize property to set how tall it is. We could also give it xsize to choose how wide, but here it's limited by the width of the frame it's in."
    e "バーにはysizeプロパティーで高さを指定します。xsizeで幅も指定できますが、ここでは表示されるフレームの幅で制限しています。"

# game/indepth_style.rpy:790
translate japanese style_bar_d4c29710:

    # e "When the bar_invert style property is True, the bar value is displayed on the right side of the bar. The left_bar and right_bar displayables might also need to be swapped."
    e "bar_invertスタイルプロパティーがTrueだと、バーの値はバーの右側で表示されます。left_barとright_barのDisplayableは交換する必要があるでしょう。"

# game/indepth_style.rpy:804
translate japanese style_bar_cca67222:

    # e "The bar_resizing style property causes the bar images to be resized to represent the value, rather than being rendered at full size and cropped."
    e "bar_resizingスタイルプロパティーはバー画像をフルサイズでレンダリングして切り取るのではなくそれぞれの値にリサイズします。"

# game/indepth_style.rpy:817
translate japanese style_bar_7d361bac:

    # e "The thumb style property gives a thumb image, that's placed based on the bars value. In the case of a scrollbar, it's resized if possible."
    e "thumbスタイルプロパティーはつまみの画像を指定し、それはバーの値に応じて配置されます。スクロールバーでは可能ならリサイズされます。"

# game/indepth_style.rpy:819
translate japanese style_bar_b6dfb61b:

    # e "Here, we use it with the base_bar style property, which sets both bar images to the same displayable."
    e "ここではbase_barスタイルプロパティーを使用して両方の画像を同じDisplayableにします。"

# game/indepth_style.rpy:834
translate japanese style_bar_996466ad:

    # e "The left_gutter and right_gutter properties set a gutter on the left or right size of the bar. The gutter is space the bar can't be dragged into, that can be used for borders."
    e "left_gutterとright_gutterプロパティーはバーの左右のガッターサイズを設定します。ガッターはドラッグできないバーの領域で、輪郭に使用できます。"

# game/indepth_style.rpy:849
translate japanese style_bar_fa41a83c:

    # e "The bar_vertical style property displays a vertically oriented bar. All of the other properties change names - left_bar becomes top_bar, while right_bar becomes bottom_bar."
    e "bar_verticalスタイルプロパティーは縦方向のバーを表示します。他のプロパティーもすべて left_barがtop_bar, right_barがbottom_barのように名前を変えます。"

# game/indepth_style.rpy:854
translate japanese style_bar_5d33c5dc:

    # e "Finally, there's one style we can't show here, and it's unscrollable. It controls what happens when a scrollbar can't be moved at all."
    e "最後に、ここでは表示できないスクロールできないスタイル、unscrollableがあります。スクロールバーが動かせないときの挙動を制御します。"

# game/indepth_style.rpy:856
translate japanese style_bar_e8e32280:

    # e "By default, it's shown. But if unscrollable is 'insensitive', the bar becomes insensitive. If it's 'hide', the bar is hidden, but still takes up space."
    e "デフォルトでは unscrollableが'insensitive'なら無効状態(insensitive)にします。'hide'ならばバーは表示されませんが、場所だけはとります。"

# game/indepth_style.rpy:860
translate japanese style_bar_f1292000:

    # e "That's it for the bar properties. By using them, a creator can customize bars, scrollbars, and sliders."
    e "それらを使用して製作者はバーやスクロールバー、スライダーをカスタマイズ出来ます。"

# game/indepth_style.rpy:959
translate japanese style_box_5fd535f4:

    # e "The hbox displayable is used to lay its children out horizontally. By default, there's no spacing between children, so they run together."
    e "hbox Displayableを使用してその子を水平に配置できます。デフォルトでは子の間には空間はなく、横に並びます。"

# game/indepth_style.rpy:965
translate japanese style_box_0111e5dc:

    # e "Similarly, the vbox displayable is used to lay its children out vertically. Both support style properties that control placement."
    e "vbox Displayableは単純に子を縦に並べます。共に配置を制御するスタイルプロパティーをサポートします。"

# game/indepth_style.rpy:970
translate japanese style_box_5a44717b:

    # e "To make the size of the box displayable obvious, I'll add a highlight to the box itself, and not the frame containing it."
    e "box Displayableのサイズを可視化するため、ボックス自体をハイライトします。 フレームにボックスがあるわけではありません。"

# game/indepth_style.rpy:978
translate japanese style_box_239e7a8f:

    # e "Boxes support the xfill and yfill style properties. These properties make a box expand to fill the available space, rather than the space of the largest child."
    e "ボックスはxfillとyfillスタイルプロパティーをサポートします。これらのプロパティーはボックスをその最大の子ではなく利用可能な空間を埋めるまで拡張します。"

# game/indepth_style.rpy:988
translate japanese style_box_e513c946:

    # e "The spacing style property takes a value in pixels, and adds that much spacing between each child of the box."
    e "spacingスタイルプロパティーはピクセル数で値をとり、ボックスの子の子の間のスペースにします。"

# game/indepth_style.rpy:998
translate japanese style_box_6ae4f94d:

    # e "The first_spacing style property is similar, but it only adds space between the first and second children. This is useful when the first child is a title that needs different spacing."
    e "first_spacingプロパティーも同じですが、1つ目と2つ目の子の間だけスペースを空けます。これは最初の子をタイトルで、異なるスペースが必要なときに便利です。"

# game/indepth_style.rpy:1008
translate japanese style_box_0c518d9f:

    # e "The box_reverse style property reverses the order of entries in the box."
    e "box_reverseスタイルプロパティーはボックス内の順番を逆にします。"

# game/indepth_style.rpy:1021
translate japanese style_box_f73c1422:

    # e "We'll switch back to a horizontal box for our next example."
    e "次の例のためにボックスを水平方向に戻します。"

# game/indepth_style.rpy:1031
translate japanese style_box_285592bb:

    # e "The box_wrap style property fills the box with children until it's full, then starts again on the next line."
    e "box_wrapスタイルプロパティーはボックスが満杯になるまで子で埋め、次の行でも同じようにします。"

# game/indepth_style.rpy:1044
translate japanese style_box_a7637552:

    # e "Grids bring with them two more style properties. The xspacing and yspacing properties control spacing in the horizontal and vertical directions, respectively."
    e "グリッドには2つ以上のスタイルプロパティーがあり、xspacingとyspacingプロパティーはそれぞれ水平垂直方向の空間を制御します。"

# game/indepth_style.rpy:1051
translate japanese style_box_4006f74b:

    # e "Lastly, we have the fixed layout. The fixed layout usually expands to fill all space, and shows its children from back to front."
    e "最後にfixedレイアウトです。fixedは通常すべての空間を埋めるまで広がり、その子を後ろから前の順で表示します。"

# game/indepth_style.rpy:1053
translate japanese style_box_4a2866f0:

    # e "But of course, we have some style properties that can change that."
    e "もちろんこれを変更できるスタイルプロパティーもあります。"

# game/indepth_style.rpy:1062
translate japanese style_box_66e042c4:

    # e "When the xfit style property is True, the fixed lays out all its children as if it was full size, and then shrinks in width to fit them. The yfit style works the same way, but in height."
    e "xfitスタイルプロパティーがTrueなら、fixedはそのすべての子に十分なサイズであるよう、幅をフィットするよう圧縮して配置します。yfitスタイルも高さ方向である以外同じです。"

# game/indepth_style.rpy:1070
translate japanese style_box_6a593b10:

    # e "The order_reverse style property changes the order in which the children are shown. Instead of back-to-front, they're displayed front-to-back."
    e "order_reverseスタイルプロパティーは子の表示順を変更します。後ろから前の代りに前から後ろの順に表示されます。"

# game/indepth_style.rpy:1082
translate japanese style_inspector_21bc0709:

    # e "Sometimes it's hard to figure out what style is being used for a particular displayable. The displayable inspector can help with that."
    e "特定のDisplayableに対してどのスタイルが使用されているか理解するのが難しいときもあります。Displayableインスペクターはそんなとき助けになれます。"

# game/indepth_style.rpy:1084
translate japanese style_inspector_243c50f0:

    # e "To use it, place the mouse over a portion of the Ren'Py user interface, and hit shift+I. That's I for inspector."
    e "使用にはマウスをRen'Pyユーザーインターフェースの一部に置いて、Shift+Iを押します。IはインスペクターのIです。"

# game/indepth_style.rpy:1086
translate japanese style_inspector_bcbdc396:

    # e "Ren'Py will pop up a list of displayables the mouse is over. Next to each is the name of the style that displayable uses."
    e "マウスの下にあるDisplayableのリストをポップアップします。隣りがそのDisplayableが使用しているスタイルの名前です。"

# game/indepth_style.rpy:1088
translate japanese style_inspector_d981e5c8:

    # e "You can click on the name of the style to see where it gets its properties from."
    e "そのスタイル名をクリックするとそのプロパティーをどこから所得しているかが見れます。"

# game/indepth_style.rpy:1090
translate japanese style_inspector_ef46b86d:

    # e "By default, the inspector only shows interface elements like screens, and not images. Type shift+alt+I if you'd like to see images as well."
    e "デフォルトではインスペクターは画像ではなくスクリーンのようなインターフェースの要素のみ表示します。Shift+Alt+Iを押すと画像も同様に見れます。"

# game/indepth_style.rpy:1092
translate japanese style_inspector_b59c6b69:

    # e "You can try the inspector right now, by hovering this text and hitting shift+I."
    e "このテキストにマウスを当てて、Shift+Iを押せばここでインスペクターを試せます。"

translate japanese strings:

    # game/indepth_style.rpy:20
    old "Button 1"
    new "Button 1"

    # game/indepth_style.rpy:22
    old "Button 2"
    new "Button 2"

    # game/indepth_style.rpy:66
    old "Style basics."
    new "スタイルの基本"

    # game/indepth_style.rpy:66
    old "General style properties."
    new "一般的スタイル"

    # game/indepth_style.rpy:66
    old "Text style properties."
    new "テキストスタイルプロパティー"

    # game/indepth_style.rpy:66
    old "Window and Button style properties."
    new "ウィンドウとボタンスタイルプロパティー"

    # game/indepth_style.rpy:66
    old "Bar style properties."
    new "バースタイルプロパティー"

    # game/indepth_style.rpy:66
    old "Box, Grid, and Fixed style properties."
    new "ボックス、グリッド, Fixedスタイルプロパティー"

    # game/indepth_style.rpy:66
    old "The Displayable Inspector."
    new "Displayable インスペクター"

    # game/indepth_style.rpy:66
    old "That's all I want to know."
    new "これで十分です。"

    # game/indepth_style.rpy:112
    old "This text is colored green."
    new "緑のテキスト"

    # game/indepth_style.rpy:126
    old "Danger"
    new "危険"

    # game/indepth_style.rpy:142
    old "This text is colored red."
    new "赤のテキスト"

    # game/indepth_style.rpy:170
    old "This text is colored blue."
    new "青のテキスト"

    # game/indepth_style.rpy:248
    old "Orbiting Earth in the spaceship, I saw how beautiful our planet is.\n–Yuri Gagarin"
    new "Orbiting Earth in the spaceship, I saw how beautiful our planet is.\n–Yuri Gagarin"

    # game/indepth_style.rpy:303
    old "\"Orbiting Earth in the spaceship, I saw how beautiful our planet is.\" Said by Yuri Gagarin."
    new "\"Orbiting Earth in the spaceship, I saw how beautiful our planet is.\" Said by Yuri Gagarin."

    # game/indepth_style.rpy:326
    old "Vertical"
    new "縦書き"

    # game/indepth_style.rpy:329
    old "Far better it is to dare mighty things, to win glorious triumphs, even though checkered by failure, than to rank with those poor spirits who neither enjoy nor suffer much, because they live in the gray twilight that Far better it is to dare mighty things, to win glorious triumphs, even though checkered by failure, than to rank with those poor spirits who neither enjoy nor suffer much, because they live in the gray twilight that knows not victory nor defeat.\n\n–Theodore Rooseveltknows not victory nor defeat.\n\n–Theodore Roosevelt"
    new "Far better it is to dare mighty things, to win glorious triumphs, even though checkered by failure, than to rank with those poor spirits who neither enjoy nor suffer much, because they live in the gray twilight that Far better it is to dare mighty things, to win glorious triumphs, even though checkered by failure, than to rank with those poor spirits who neither enjoy nor suffer much, because they live in the gray twilight that knows not victory nor defeat.\n\n–Theodore Rooseveltknows not victory nor defeat.\n\n–Theodore Roosevelt"

    # game/indepth_style.rpy:561
    old "Top Choice"
    new "Top Choice"

    # game/indepth_style.rpy:566
    old "Bottom Choice"
    new "Bottom Choice"

    # game/indepth_style.rpy:877
    old "First Child"
    new "First Child"

    # game/indepth_style.rpy:878
    old "Second Child"
    new "Second Child"

    # game/indepth_style.rpy:879
    old "Third Child"
    new "Third Child"

    # game/indepth_style.rpy:882
    old "Fourth Child"
    new "Fourth Child"

    # game/indepth_style.rpy:883
    old "Fifth Child"
    new "Fifth Child"

    # game/indepth_style.rpy:884
    old "Sixth Child"
    new "Sixth Child"


translate japanese strings:

    # game/indepth_style.rpy:329
    old "Far better it is to dare mighty things, to win glorious triumphs, even though checkered by failure, than to rank with those poor spirits who neither enjoy nor suffer much, because they live in the gray twilight that knows not victory nor defeat.\n\n–Theodore Roosevelt"
    new "Far better it is to dare mighty things, to win glorious triumphs, even though checkered by failure, than to rank with those poor spirits who neither enjoy nor suffer much, because they live in the gray twilight that knows not victory nor defeat.\n\n–Theodore Roosevelt"
