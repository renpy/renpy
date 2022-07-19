
# game/indepth_character.rpy:11
translate japanese demo_character_e7e1b1bb:

    # e "We've already seen how to define a Character in Ren'Py. But I want to go into a bit more detail as to what a Character is."
    e "Ren'Pyでのキャラクターの定義方法はすでに見たでしょうが、キャラクターとは何かをより詳しく紹介したいです。"

# game/indepth_character.rpy:17
translate japanese demo_character_d7908a94:

    # e "Here are couple of additional characters."
    e "こちらは2組の追加キャラクターです。"

# game/indepth_character.rpy:19
translate japanese demo_character_275ef8b9:

    # e "Each statement creates a Character object, and gives it a single argument, a name. If the name is None, no name is displayed."
    e "各ステートメントはキャラクターオブジェクトを作成し、引数として名前を与えます。名前がNoneなら名前は表示されません。"

# game/indepth_character.rpy:21
translate japanese demo_character_a63aea0c:

    # e "This can be followed by named arguments that set properties of the character. A named argument is a property name, an equals sign, and a value."
    e "これにキャラクターのプロパティーを設定する名前付き引数が続きます。名前付き引数はプロパティー名と等号、値です。"

# game/indepth_character.rpy:23
translate japanese demo_character_636a502e:

    # e "Multiple arguments should be separated with commas, like they are here. Let's see those characters in action."
    e "複数の引数はこのようにコンマで分割しましょう。さあ、これらのキャラクターが実際に動作するところを見ましょうか。"

# game/indepth_character.rpy:27
translate japanese demo_character_44b54e1d:

    # e_shout "I can shout!"
    e_shout "私は叫べる！"

# game/indepth_character.rpy:29
translate japanese demo_character_a9646dd8:

    # e_whisper "And I can speak in a whisper."
    e_whisper "私はささやける"

# game/indepth_character.rpy:31
translate japanese demo_character_79793208:

    # e "This example shows how the name Character is a bit of a misnomer. Here, we have multiple Characters in use, but you see it as me speaking."
    e "この例ではキャラクターという名称が少し不適切に思えるかもしれません。ここで複数のキャラクターを使用しましたが、私一人が話しているように見えるでしょう。"

# game/indepth_character.rpy:33
translate japanese demo_character_5d5d7482:

    # e "It's best to think of a Character as repesenting a name and style, rather than a single person."
    e "キャラクターを一個人ではなく、名前とスタイルの代表と考えるとよいです。"

# game/indepth_character.rpy:37
translate japanese demo_character_66d08d98:

    # e "There are a lot of properties that can be given to Characters, most of them prefixed styles."
    e "キャラクターに与えられるたくさんのプロパティーがあり、ほとんどが接頭辞付きのスタイルです。"

# game/indepth_character.rpy:39
translate japanese demo_character_7e0d75aa:

    # e "Properties beginning with window apply to the textbox, those with what apply to the the dialogue, and those with who to the name of Character speaking."
    e "windowで始まるプロパティーはテキストボックスに適用され、whatで始まるものは台詞に適用され、whoで始まるものは発言しているキャラクターの名前に適用されます。"

# game/indepth_character.rpy:41
translate japanese demo_character_56703784:

    # e "If you leave a prefix out, the style customizes the name of the speaker."
    e "接頭辞がないと、そのスタイルは発言しているキャラクターの名前をカスタムします。"

# game/indepth_character.rpy:43
translate japanese demo_character_b456f0a9:

    # e "There are quite a few different properties that can be set this way. Here are some of the most useful."
    e "かなりたくさんのプロパティーがこの方法で設定されますが、こちらは最も便利なものとなります。"

# game/indepth_character.rpy:48
translate japanese demo_character_31ace18e:

    # e1 "The window_background property sets the image that's used for the background of the textbox, which should be the same size as the default in gui/textbox.png."
    e1 "window_backgroundプロパティーはテキストボックスの背景に使用される画像を設定します。画像はデフォルトではgui/textbox.pngと同じサイズであるべきです。"

# game/indepth_character.rpy:54
translate japanese demo_character_18ba073d:

    # e1a "If it's set to None, the textbox has no background window."
    e1a "Noneに設定するとテキストボックスには背景がなくなります。"

# game/indepth_character.rpy:59
translate japanese demo_character_5a26445c:

    # e2 "The who_color and what_color properties set the color of the character's name and dialogue text, respectively."
    e2 "who_colorとwhat_colorプロパティーはそれぞれキャラクター名と台詞テキストの色を設定します。"

# game/indepth_character.rpy:61
translate japanese demo_character_88a18c32:

    # e2 "The colors are strings containing rgb hex codes, the same sort of colors understood by a web browser."
    e2 "色はrgbの16進数コードの文字列で、ウェブブラウザと同じ形式です。"

# game/indepth_character.rpy:67
translate japanese demo_character_ed690751:

    # e3 "Similarly, the who_font and what_font properties set the font used by the different kinds of text."
    e3 "同様に、who_fontとwhat_fontプロパティーはそれぞれのテキストのフォントに設定されます。"

# game/indepth_character.rpy:74
translate japanese demo_character_8dfa6426:

    # e4 "Setting the who_bold, what_italic, and what_size properties makes the name bold, and the dialogue text italic at a size of 20 pixels."
    e4 "who_bold,  what_italic,  who_sizeプロパティーは名前を太く、イタリックで20ピクセルサイズにします。"

# game/indepth_character.rpy:76
translate japanese demo_character_20e83c32:

    # e4 "Of course, the what_bold, who_italic and who_size properties also exist, even if they're not used here."
    e4 "勿論ここでは使いませんが、who_bold,  who_italic,  who_sizeプロパティーもあります。"

# game/indepth_character.rpy:83
translate japanese demo_character_e4cbb1f2:

    # e5 "The what_outlines property puts an outline around the text."
    e5 "what_outlinesプロパティーはテキスト回りにアウトラインを置きます。"

# game/indepth_character.rpy:85
translate japanese demo_character_71535ecf:

    # e5 "It's a little complicated since it takes a list with a tuple in it, with the tuple being four things in parenthesis, and the list the square brackets around them."
    e5 "タプルのリストをとるのでこれは少し複雑で、括弧で囲まれた4要素のタプルとそれを囲む角括弧のリストです。"

# game/indepth_character.rpy:87
translate japanese demo_character_e9ac7482:

    # e5 "The first number is the size of the outline, in pixels. That's followed by a string giving the hex-code of the color of the outline, and the x and y offsets."
    e5 "最初の数字はアウトラインのピクセルでのサイズで、アウトラインの16進数のカラーコード文字列、x, yオフセットが続きます。"

# game/indepth_character.rpy:93
translate japanese demo_character_ea72d988:

    # e6 "When the outline size is 0 and the offsets are given, what_outlines can also act as a drop-shadow behind the text."
    e6 "アウトラインサイズが0でオフセットがあると、what_outlinesはテキストの後ろの陰として振舞います。"

# game/indepth_character.rpy:99
translate japanese demo_character_8d35ebcd:

    # e7 "The what_xalign and what_textalign properties control the alignment of text, with 0.0 being left, 0.5 being center, and 1.0 being right."
    e7 "what_xalignとwhat_textalignプロパティーはテキストのアライメントを制御し、0.0は左、0.5は中央, 1.0は右となります。"

# game/indepth_character.rpy:101
translate japanese demo_character_7c75906c:

    # e7 "The what_xalign property controls where all the text itself is placed within the textbox, while what_textalign controls where rows of text are placed relative to each other."
    e7 "what_xalignプロパティーはテキストボックスのすべてのテキストを制御し、what_textalignはテキスト行ごとの相対的な位置を制御します。"

# game/indepth_character.rpy:103
translate japanese demo_character_e2811c1c:

    # e7 "Generally you'll want to to set them both what_xalign and what_textalign to the same value."
    e7 "一般的に、what_xalignとwhat_textalignは同じ値に設定します。"

# game/indepth_character.rpy:105
translate japanese demo_character_baa52234:

    # e7 "Setting what_layout to 'subtitle' puts Ren'Py in subtitle mode, which tries to even out the length of every line of text in a block."
    e7 "what_layoutを'subtitle'にするとRen'Pyはサブタイトルモードになり、ブロック中のすべてのテキスト行の長さをそろえようとします。"

# game/indepth_character.rpy:110
translate japanese demo_character_41190f01:

    # e8 "These properties can be combined to achieve many different effects."
    e8 "これらのプロパティーを組合せて多様な効果を得られます。"

# game/indepth_character.rpy:124
translate japanese demo_character_aa12d9ca:

    # e8 "This example hides the background and shows dialogue centered and outlined, as if the game is being subtitled."
    e8 "この例では背景を消し、台詞をアウトラインをつけて中央に表示しています。"

# game/indepth_character.rpy:133
translate japanese demo_character_a7f243e5:

    # e9 "There are two interesting non-style properties, what_prefix and what_suffix. These can put text at the start and end of a line of dialogue."
    e9 "2つの面白い非スタイルプロパティー、what_prefixとwhat_suffixがあります。これらは台詞行の最初と最後にテキストを追加します。"

# game/indepth_character.rpy:139
translate japanese demo_character_f9b0052f:

    # e "By using kind, you can copy properties from one character to another, changing only what you need to."
    e "kindを使用すると、必要なところだけ変更してあるキャラクターから他のキャラクターにプロパティーをコピーできます。"

# game/indepth_character.rpy:148
translate japanese demo_character_6dfce4b7:

    # l8 "Like this! Finally I get some more dialogue around here."
    l8 "このようにね！最後に台詞が貰えたわ。"

# game/indepth_character.rpy:157
translate japanese demo_character_68d9e46c:

    # e "The last thing you have to know is that there's a special character, narrator, that speaks narration. Got it?"
    e "最後に知っておくべきことはナレーションをする特別なキャラクターnarratorです。わかりましたか？"

# game/indepth_character.rpy:159
translate japanese demo_character_0c8f314a:

    # "I think I do."
    "そう思います。"

