
# game/indepth_text.rpy:22
translate schinese a_label_8d79d234:

    # e "You just clicked to jump to a label."
    e "你刚刚点击了跳转到一个label。"

# game/indepth_text.rpy:28
translate schinese text_578c4060:

    # e "Sometimes, when showing text, we'll want to change the way some of the text is displayed."
    e "有时，在显示文本时，我们会希望更改某些文本的显示方式。"

# game/indepth_text.rpy:31
translate schinese text_60750345:

    # e "For example, we might want to have text that is {b}bold{/b}, {i}italic{/i}, {s}struckthrough{/s}, or {u}underlined{/u}."
    e "例如，我们可能希望文本是{b}粗体{/b}、{i}斜体{/i}、{s}删除线{/s}，或者{u}下划线{/u}。"

# game/indepth_text.rpy:33
translate schinese text_5e1a6ee8:

    # e "That's what text tags are for."
    e "这就是文本标签的用途。"

# game/indepth_text.rpy:37
translate schinese text_38c63ec8:

    # e "Text tags are contained in braces, like the {{b} tag above. When a text tag takes a closing tag, the closing tag begins with a slash, like {{/b} does."
    e "文本标签包含在大括号中，如上面的{{b}标记。当文本标记接受结束标记时，结束标记以斜线开头，就像{{/b}那样。"

# game/indepth_text.rpy:39
translate schinese text_1760f9c8:

    # e "We've already seen the b, i, s, and u tags, but there are lot more than those. I'll show you the rest of them."
    e "我们已经看到了b、i、s和u等标签，但还有很多其他标签。接下来我将展示给你。"

# game/indepth_text.rpy:43
translate schinese text_a620251f:

    # e "The a text tag can {a=https://www.renpy.org}link to a website{/a} or {a=jump:a_label}jump to a label{/a}."
    e "a文本标签可以{a=https://www.renpy.org}链接网址{/a}或{a=jump:a_label}跳转到一个标签{/a}。"

# game/indepth_text.rpy:49
translate schinese after_a_label_d22d5f4a:

    # e "The alpha text tag makes text {alpha=.5}translucent{/alpha}."
    e "alpha文本标签使文本{alpha=.5}半透明{/alpha}。"

# game/indepth_text.rpy:53
translate schinese after_a_label_7c2c3cd2:

    # e "The color text tag changes the {color=#0080c0}color{/color} of the text."
    e "color文本标签更改文本的{color=#0080c0}颜色{/color}。"

# game/indepth_text.rpy:57
translate schinese after_a_label_3f81fe7b:

    # e "The cps text tag {cps=25}makes text type itself out slowly{/cps}, even if slow text is off."
    e "cps文本标签{cps=25}使文本缓慢地打出{/cps}，即使慢速文本处于关闭状态。"

# game/indepth_text.rpy:59
translate schinese after_a_label_b102941f:

    # e "The cps tag can also be relative to the default speed, {cps=*2}doubling{/cps} or {cps=*0.5}halving{/cps} it."
    e "cps还可以相对于默认速度{cps=*2}加倍{/cps}或{cps=*0.5}减半{/cps}。"

# game/indepth_text.rpy:64
translate schinese after_a_label_22c4339a:

    # e "The font tag changes the font, for example to {font=DejaVuSans-Bold.ttf}DejaVuSans-Bold.ttf{/font}."
    e "font更改字体，例如{font=DejaVuSans-Bold.ttf}DejaVuSans-Bold.ttf{/font}。"

# game/indepth_text.rpy:66
translate schinese after_a_label_d43417d7:

    # e "Sometimes, changing to a bold font looks better than using the {{b} tag."
    e "有时，更改为粗体字体比使用{{b}更好。"

# game/indepth_text.rpy:71
translate schinese after_a_label_f24052f9:

    # e "The k tag changes kerning. It can space the letters of a word {k=-.5}closer together{/k} or {k=.5}farther apart{/k}."
    e "k改变了字体间距。它可以使单词的字母间距{k=-.5}更近{/k}或{k=.5}更远{/k}。（译者注：看上去对中文字体不起作用）"

# game/indepth_text.rpy:76
translate schinese after_a_label_2310b922:

    # e "The size tag changes the size of text. It can make text {size=+10}bigger{/size} or {size=-10}smaller{/size}, or set it to a {size=30}fixed size{/size}."
    e "size更改文本的大小。它可以使文本{size=+10}变大{/size}或{size=-10}变小{/size}，或者将其设置为{size=30}固定大小{/size}。"

# game/indepth_text.rpy:81
translate schinese after_a_label_f566abf2:

    # e "The space tag {space=30} adds horizontal space in text.{vspace=30}The vspace tag adds vertical space between lines."
    e "space{space=30}在文本中添加水平空格。{vspace=30}vspace在行之间添加垂直空格。"

# game/indepth_text.rpy:85
translate schinese after_a_label_054b9ffa:

    # e "There are a few text tags that only makes sense in dialogue."
    e "有一些文本标签只有在对话中才有意义。"

# game/indepth_text.rpy:89
translate schinese after_a_label_86efc45b:

    # e "The p tag breaks a paragraph,{p}and waits for the player to click."
    e "p会打断一个段落，{p}并等待玩家单击。"

# game/indepth_text.rpy:91
translate schinese after_a_label_3ece2387:

    # e "If it is given a number as an argument,{p=1.5}it waits that many seconds."
    e "如果给它一个数字作为参数，{p=1.5}它会等待那么多秒。"

# game/indepth_text.rpy:95
translate schinese after_a_label_3881f72d:

    # e "The w tag also waits for a click,{w} except it doesn't break lines,{w=.5} the way p does."
    e "w也会等待一次点击，{w}除了不换行，{w=.5}不像p那样。"

# game/indepth_text.rpy:100
translate schinese after_a_label_e5321e79:

    # eslow "The nw tag causes Ren'Py to continue past slow text,{nw}"
    eslow "nw使Ren'Py慢速显示文本，{nw}"

# game/indepth_text.rpy:102
translate schinese after_a_label_1f2697ba:

    # extend " to the next statement."
    extend "到下一个语句。"

# game/indepth_text.rpy:106
translate schinese after_a_label_dbfca166:

    # e "To break a line without pausing,\none can write \\n. \\' and \\\" include quotes in the text."
    e "若要在不暂停的情况下换行，\n可以在文本中写入\\n。\\'和\\\"在文本中加入引号。"

# game/indepth_text.rpy:111
translate schinese after_a_label_ffdf7e76:

    # e "The interpolation feature takes a variable name in square brackets, and inserts it into text."
    e "插值功能采用方括号中的变量名，并将其插入到文本中。"

# game/indepth_text.rpy:117
translate schinese after_a_label_fc99fcbf:

    # e "For example, this displays the [variable!t]."
    e "例如，这里显示[variable]。"

# game/indepth_text.rpy:121
translate schinese after_a_label_c84d9087:

    # e "When the variable name is followed by !q, special characters are quoted. This displays the raw [variable!q!t], including the italics tags."
    e "当变量名后面跟着!q，特殊字符会被引用。这里显示原始的[variable!q]，包括斜体标签。"

# game/indepth_text.rpy:126
translate schinese after_a_label_c90f24a8:

    # e "When the variable name is followed by !t, it is translated to [variable!t]. It could be something else in a different language."
    e "当变量名后面跟着!t，它被转换成[variable!t]。这可能是另一种语言。"

# game/indepth_text.rpy:129
translate schinese after_a_label_fb106a95:

    # e "Finally, certain characters are special. [[, {{, and \\ need to be doubled if included in text. The %% character should be doubled if used in dialogue."
    e "最后，某些字符是特殊的。如果包含在文本中， [[ 、 {{ 和 \\ 需要两个。如果在对话中使用， %% 字符也要两个。"

translate schinese strings:

    # game/indepth_text.rpy:115
    old "{i}variable value{/i}"
    new "{i}变量值{/i}"

    # game/indepth_text.rpy:124
    old "translatable text"
    new "可翻译文本"
