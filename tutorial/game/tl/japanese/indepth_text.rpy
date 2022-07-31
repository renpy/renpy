
# game/indepth_text.rpy:22
translate japanese a_label_8d79d234:

    # e "You just clicked to jump to a label."
    e "ジャンプラベルをクリックしましたね。"

# game/indepth_text.rpy:28
translate japanese text_578c4060:

    # e "Sometimes, when showing text, we'll want to change the way some of the text is displayed."
    e "テキスト表示時にその表示を変更したいときがあります。"

# game/indepth_text.rpy:31
translate japanese text_60750345:

    # e "For example, we might want to have text that is {b}bold{/b}, {i}italic{/i}, {s}struckthrough{/s}, or {u}underlined{/u}."
    e "例えば、{b}太字{/b}, {i}イタリック{/i}, {s}斜線{/s}, or {u}下線{/u}です。"

# game/indepth_text.rpy:33
translate japanese text_5e1a6ee8:

    # e "That's what text tags are for."
    e "これがテキストタグの目的です。"

# game/indepth_text.rpy:37
translate japanese text_38c63ec8:

    # e "Text tags are contained in braces, like the {{b} tag above. When a text tag takes a closing tag, the closing tag begins with a slash, like {{/b} does."
    e "テキストタグは、上記の{{b}のような中括弧に含まれます。テキストタグに閉じタグがあるときは、閉じタグは{{/b}のようにスラッシュで始まります。"

# game/indepth_text.rpy:39
translate japanese text_1760f9c8:

    # e "We've already seen the b, i, s, and u tags, but there are lot more than those. I'll show you the rest of them."
    e "b, i, s, uタグをすでに見ましたが、もっと多くのタグがあります。残りを表示しましょう。"

# game/indepth_text.rpy:43
translate japanese text_a620251f:

    # e "The a text tag can {a=https://www.renpy.org}link to a website{/a} or {a=jump:a_label}jump to a label{/a}."
    e "テキストタグで{a=https://ja.renpy.org}ウェブサイトへのリンク{/a}や{a=jump:a_label}ラベルへのジャンプ{/a}ができます。"

# game/indepth_text.rpy:49
translate japanese after_a_label_d22d5f4a:

    # e "The alpha text tag makes text {alpha=.5}translucent{/alpha}."
    e "alphaテキストタグは、テキストを{alpha=.5}半透明{/alpha}にします。"

# game/indepth_text.rpy:53
translate japanese after_a_label_7c2c3cd2:

    # e "The color text tag changes the {color=#0080c0}color{/color} of the text."
    e "カラーテキストタグは、テキストの{color=#0080c0}色{/color}を変更します。"

# game/indepth_text.rpy:57
translate japanese after_a_label_3f81fe7b:

    # e "The cps text tag {cps=25}makes text type itself out slowly{/cps}, even if slow text is off."
    e "cpsテキストタグは、たとえテキストが瞬間的に表示されるよう設定していても{cps=25}テキストのタイプ速度をゆっくりにします。{/cps}"

# game/indepth_text.rpy:59
translate japanese after_a_label_b102941f:

    # e "The cps tag can also be relative to the default speed, {cps=*2}doubling{/cps} or {cps=*0.5}halving{/cps} it."
    e "{cps=*2}倍{/cps}や{cps=*0.5}半分{/cps}のようにcpsタグデフォルトの早さに対して相対的にも指定できます。"

# game/indepth_text.rpy:64
translate japanese after_a_label_22c4339a:

    # e "The font tag changes the font, for example to {font=DejaVuSans-Bold.ttf}DejaVuSans-Bold.ttf{/font}."
    e "fontテキストタグは{font=DejaVuSans-Bold.ttf}DejaVuSans-Bold.ttf{/font}のようにフォントを変更できます。"

# game/indepth_text.rpy:66
translate japanese after_a_label_d43417d7:

    # e "Sometimes, changing to a bold font looks better than using the {{b} tag."
    e "{{b}タグを使用するよりもフォントを変更した方が見目よくなることもあります。"

# game/indepth_text.rpy:71
translate japanese after_a_label_f24052f9:

    # e "The k tag changes kerning. It can space the letters of a word {k=-.5}closer together{/k} or {k=.5}farther apart{/k}."
    e "kタグを使うと、カーニングを変更できます。これで文字同士の間隔を調整できます。{k=-.5}文字同士の間隔が狭くなりました。{/k}{k=.5}文字同士の間隔が広くなりました。{/k}"

# game/indepth_text.rpy:76
translate japanese after_a_label_2310b922:

    # e "The size tag changes the size of text. It can make text {size=+10}bigger{/size} or {size=-10}smaller{/size}, or set it to a {size=30}fixed size{/size}."
    e "sizeタグは文字のサイズを変更します。テキストを{size=+10}大きくしたり{/size}、{size=-10}小さくしたり{/size}、{size=30}固定のサイズにしたり{/size}できます。"

# game/indepth_text.rpy:81
translate japanese after_a_label_f566abf2:

    # e "The space tag {space=30} adds horizontal space in text.{vspace=30}The vspace tag adds vertical space between lines."
    e "spaceタグは{space=30}テキストの水平方向のスペースを、{vspace=30}vspaceタグは垂直方向のスペースを追加します。"

# game/indepth_text.rpy:85
translate japanese after_a_label_054b9ffa:

    # e "There are a few text tags that only makes sense in dialogue."
    e "台詞でのみ有効なテキストタグもあります。"

# game/indepth_text.rpy:89
translate japanese after_a_label_86efc45b:

    # e "The p tag breaks a paragraph,{p}and waits for the player to click."
    e "pタグは改行し、{p}プレイヤーのクリックを待ちます。"

# game/indepth_text.rpy:91
translate japanese after_a_label_3ece2387:

    # e "If it is given a number as an argument,{p=1.5}it waits that many seconds."
    e "引数に数字を指定されると、{p=1.5}その秒数分待機します。"

# game/indepth_text.rpy:95
translate japanese after_a_label_3881f72d:

    # e "The w tag also waits for a click,{w} except it doesn't break lines,{w=.5} the way p does."
    e "wタグもクリックを待ちます。{w}こちらは改行しない他は、{w=.5}pと同じように使えます。"

# game/indepth_text.rpy:100
translate japanese after_a_label_e5321e79:

    # eslow "The nw tag causes Ren'Py to continue past slow text,{nw}"
    eslow "nwタグはRen'Pyに{nw}"

# game/indepth_text.rpy:102
translate japanese after_a_label_1f2697ba:

    # extend " to the next statement."
    extend "次のステートメントまで進ませます。"

# game/indepth_text.rpy:106
translate japanese after_a_label_dbfca166:

    # e "To break a line without pausing,\none can write \\n. \\' and \\\" include quotes in the text."
    e "ポーズせずに改行したいならば、\n\\nが使えます。\\'と\\\"はテキストに引用符を含めます。"

# game/indepth_text.rpy:111
translate japanese after_a_label_ffdf7e76:

    # e "The interpolation feature takes a variable name in square brackets, and inserts it into text."
    e "補完機能は角括弧に変数名をとってテキストに挿入します。"

# game/indepth_text.rpy:117
translate japanese after_a_label_fc99fcbf:

    # e "For example, this displays the [variable!t]."
    e "例えば、これは[variable!t]を表示します。"

# game/indepth_text.rpy:121
translate japanese after_a_label_c84d9087:

    # e "When the variable name is followed by !q, special characters are quoted. This displays the raw [variable!q!t], including the italics tags."
    e "変数名に!qが続くと、特別な文字は引用符がつきます。これはイタリックを含む[variable!q!t]をそのまま表示します。"

# game/indepth_text.rpy:126
translate japanese after_a_label_c90f24a8:

    # e "When the variable name is followed by !t, it is translated to [variable!t]. It could be something else in a different language."
    e "変数名に!tが続くと、[variable!t]に翻訳されます。これで言語ごとに分けられます。"

# game/indepth_text.rpy:129
translate japanese after_a_label_fb106a95:

    # e "Finally, certain characters are special. [[, {{, and \\ need to be doubled if included in text. The %% character should be doubled if used in dialogue."
    e "さいごに、ある特定の特別な文字があります。[[, {{, \\はテキストに含めるときは二重でなければなりません。%%は台詞中では二重であるべきです。"

translate japanese strings:

    # game/indepth_text.rpy:115
    old "{i}variable value{/i}"
    new "{i}variable value{/i}"

    # game/indepth_text.rpy:124
    old "translatable text"
    new "翻訳可能なテキスト"

