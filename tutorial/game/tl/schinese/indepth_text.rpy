
# game/indepth_text.rpy:22
translate schinese a_label_8d79d234:

    # e "You just clicked to jump to a label."
    e "你刚才点击了跳转到一个标签。"

# game/indepth_text.rpy:28
translate schinese text_578c4060:

    # e "Sometimes, when showing text, we'll want to change the way some of the text is displayed."
    e "有时显示文本时，我们会想改变其中一部分的显示方式。"

# game/indepth_text.rpy:31
translate schinese text_60750345:

    # e "For example, we might want to have text that is {b}bold{/b}, {i}italic{/i}, {s}struckthrough{/s}, or {u}underlined{/u}."
    e "例如，我们可能希望文本显示为{b}粗体{/b}、{i}斜体{/i}、{s}删除线{/s}或{u}下划线{/u}。"

# game/indepth_text.rpy:33
translate schinese text_5e1a6ee8:

    # e "That's what text tags are for."
    e "这就是文本标签的作用。"

# game/indepth_text.rpy:37
translate schinese text_38c63ec8:

    # e "Text tags are contained in braces, like the {{b} tag above. When a text tag takes a closing tag, the closing tag begins with a slash, like {{/b} does."
    e "文本标签写在大括号中，例如上面的{{b}标签。需要结束标签时，结束标签会以斜线开头，例如{{/b}。"

# game/indepth_text.rpy:39
translate schinese text_1760f9c8:

    # e "We've already seen the b, i, s, and u tags, but there are lot more than those. I'll show you the rest of them."
    e "我们已经见过 b、i、s 和 u 标签，但标签远不止这些。下面介绍其余标签。"

# game/indepth_text.rpy:43
translate schinese text_a620251f:

    # e "The a text tag can {a=https://www.renpy.org}link to a website{/a} or {a=jump:a_label}jump to a label{/a}."
    e "a 文本标签可以{a=https://www.renpy.org}链接到网站{/a}，也可以{a=jump:a_label}跳转到标签{/a}。"

# game/indepth_text.rpy:49
translate schinese after_a_label_d22d5f4a:

    # e "The alpha text tag makes text {alpha=.5}translucent{/alpha}."
    e "alpha 文本标签可以让文本{alpha=.5}变为半透明{/alpha}。"

# game/indepth_text.rpy:53
translate schinese after_a_label_7c2c3cd2:

    # e "The color text tag changes the {color=#0080c0}color{/color} of the text."
    e "color 文本标签可以改变文本的{color=#0080c0}颜色{/color}。"

# game/indepth_text.rpy:57
translate schinese after_a_label_3f81fe7b:

    # e "The cps text tag {cps=25}makes text type itself out slowly{/cps}, even if slow text is off."
    e "即使关闭慢速文本，cps 文本标签也能让文本{cps=25}缓慢显示{/cps}。"

# game/indepth_text.rpy:59
translate schinese after_a_label_b102941f:

    # e "The cps tag can also be relative to the default speed, {cps=*2}doubling{/cps} or {cps=*0.5}halving{/cps} it."
    e "cps 标签还可以相对于默认速度设置，让速度{cps=*2}加倍{/cps}或{cps=*0.5}减半{/cps}。"

# game/indepth_text.rpy:64
translate schinese after_a_label_22c4339a:

    # e "The font tag changes the font, for example to {font=DejaVuSans-Bold.ttf}DejaVuSans-Bold.ttf{/font}."
    e "font 标签可以更换字体，例如{font=DejaVuSans-Bold.ttf}DejaVuSans-Bold.ttf{/font}。"

# game/indepth_text.rpy:66
translate schinese after_a_label_d43417d7:

    # e "Sometimes, changing to a bold font looks better than using the {{b} tag."
    e "有时，换用粗体字体的效果比使用{{b}标签更好。"

# game/indepth_text.rpy:71
translate schinese after_a_label_f24052f9:

    # e "The k tag changes kerning. It can space the letters of a word {k=-.5}closer together{/k} or {k=.5}farther apart{/k}."
    e "k 标签改变字距。它可以让单词中的字母{k=-.5}靠得更近{/k}，或{k=.5}分得更开{/k}。"

# game/indepth_text.rpy:76
translate schinese after_a_label_2310b922:

    # e "The size tag changes the size of text. It can make text {size=+10}bigger{/size} or {size=-10}smaller{/size}, or set it to a {size=30}fixed size{/size}."
    e "size 标签改变文本大小，可以让文本{size=+10}变大{/size}、{size=-10}变小{/size}，或设为{size=30}固定大小{/size}。"

# game/indepth_text.rpy:81
translate schinese after_a_label_f566abf2:

    # e "The space tag {space=30} adds horizontal space in text.{vspace=30}The vspace tag adds vertical space between lines."
    e "space 标签{space=30}在文本中加入水平空格。{vspace=30}vspace 标签在行间加入垂直空格。"

# game/indepth_text.rpy:85
translate schinese after_a_label_054b9ffa:

    # e "There are a few text tags that only makes sense in dialogue."
    e "有些文本标签只有在对话中才有意义。"

# game/indepth_text.rpy:89
translate schinese after_a_label_86efc45b:

    # e "The p tag breaks a paragraph,{p}and waits for the player to click."
    e "p 标签会结束一段文字，{p}并等待玩家点击。"

# game/indepth_text.rpy:91
translate schinese after_a_label_3ece2387:

    # e "If it is given a number as an argument,{p=1.5}it waits that many seconds."
    e "如果为它提供数字参数，{p=1.5}它就会等待相应的秒数。"

# game/indepth_text.rpy:95
translate schinese after_a_label_3881f72d:

    # e "The w tag also waits for a click,{w} except it doesn't break lines,{w=.5} the way p does."
    e "w 标签也会等待点击，{w}但不会像 p 标签那样换行；{w=.5}它只会等待半秒。"

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
    e "要在不暂停的情况下换行，\n可以在文本中写入\\n。\\'和\\\"在文本中加入引号。"

# game/indepth_text.rpy:111
translate schinese after_a_label_ffdf7e76:

    # e "The interpolation feature takes a variable name in square brackets, and inserts it into text."
    e "插值功能会接收方括号中的变量名，并将变量值插入文本。"

# game/indepth_text.rpy:117
translate schinese after_a_label_fc99fcbf:

    # e "For example, this displays the [variable!t]."
    e "例如，这里显示的是 [variable!t]。"

# game/indepth_text.rpy:121
translate schinese after_a_label_c84d9087:

    # e "When the variable name is followed by !q, special characters are quoted. This displays the raw [variable!q!t], including the italics tags."
    e "变量名后跟 !q 时，特殊字符会被引用。这里显示原始的 [variable!q!t]，包括斜体标签。"

# game/indepth_text.rpy:126
translate schinese after_a_label_c90f24a8:

    # e "When the variable name is followed by !t, it is translated to [variable!t]. It could be something else in a different language."
    e "变量名后跟 !t 时，会将其翻译为 [variable!t]。在其他语言中，它可能会变成不同的内容。"

# game/indepth_text.rpy:129
translate schinese after_a_label_fb106a95:

    # e "Finally, certain characters are special. [[, {{, and \\ need to be doubled if included in text. The %% character should be doubled if used in dialogue."
    e "最后，某些字符具有特殊含义。要在文本中使用 [[、{{ 或 \\，必须把它们各写两次。在对话中使用 %% 时，也必须写成两个。"

translate schinese strings:

    # game/indepth_text.rpy:115
    old "{i}variable value{/i}"
    new "{i}变量值{/i}"

    # game/indepth_text.rpy:124
    old "translatable text"
    new "可翻译文本"
