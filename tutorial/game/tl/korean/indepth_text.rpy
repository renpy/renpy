# TODO: Translation updated at 2019-01-15 15:31

# game/indepth_text.rpy:22
translate korean a_label_8d79d234:

    # e "You just clicked to jump to a label."
    e ""

# game/indepth_text.rpy:28
translate korean text_578c4060:

    # e "Sometimes, when showing text, we'll want to change the way some of the text is displayed."
    e ""

# game/indepth_text.rpy:31
translate korean text_60750345:

    # e "For example, we might want to have text that is {b}bold{/b}, {i}italic{/i}, {s}struckthrough{/s}, or {u}underlined{/u}."
    e ""

# game/indepth_text.rpy:33
translate korean text_5e1a6ee8:

    # e "That's what text tags are for."
    e ""

# game/indepth_text.rpy:37
translate korean text_38c63ec8:

    # e "Text tags are contained in braces, like the {{b} tag above. When a text tag takes a closing tag, the closing tag begins with a slash, like {{/b} does."
    e ""

# game/indepth_text.rpy:39
translate korean text_1760f9c8:

    # e "We've already seen the b, i, s, and u tags, but there are lot more than those. I'll show you the rest of them."
    e ""

# game/indepth_text.rpy:43
translate korean text_a620251f:

    # e "The a text tag can {a=https://www.renpy.org}link to a website{/a} or {a=jump:a_label}jump to a label{/a}."
    e ""

# game/indepth_text.rpy:49
translate korean after_a_label_d22d5f4a:

    # e "The alpha text tag makes text {alpha=.5}translucent{/alpha}."
    e ""

# game/indepth_text.rpy:53
translate korean after_a_label_7c2c3cd2:

    # e "The color text tag changes the {color=#0080c0}color{/color} of the text."
    e ""

# game/indepth_text.rpy:57
translate korean after_a_label_3f81fe7b:

    # e "The cps text tag {cps=25}makes text type itself out slowly{/cps}, even if slow text is off."
    e ""

# game/indepth_text.rpy:59
translate korean after_a_label_b102941f:

    # e "The cps tag can also be relative to the default speed, {cps=*2}doubling{/cps} or {cps=*0.5}halving{/cps} it."
    e ""

# game/indepth_text.rpy:64
translate korean after_a_label_22c4339a:

    # e "The font tag changes the font, for example to {font=DejaVuSans-Bold.ttf}DejaVuSans-Bold.ttf{/font}."
    e ""

# game/indepth_text.rpy:66
translate korean after_a_label_d43417d7:

    # e "Sometimes, changing to a bold font looks better than using the {{b} tag."
    e ""

# game/indepth_text.rpy:71
translate korean after_a_label_f24052f9:

    # e "The k tag changes kerning. It can space the letters of a word {k=-.5}closer together{/k} or {k=.5}farther apart{/k}."
    e ""

# game/indepth_text.rpy:76
translate korean after_a_label_2310b922:

    # e "The size tag changes the size of text. It can make text {size=+10}bigger{/size} or {size=-10}smaller{/size}, or set it to a {size=30}fixed size{/size}."
    e ""

# game/indepth_text.rpy:81
translate korean after_a_label_f566abf2:

    # e "The space tag {space=30} adds horizontal space in text.{vspace=30}The vspace tag adds vertical space between lines."
    e ""

# game/indepth_text.rpy:85
translate korean after_a_label_054b9ffa:

    # e "There are a few text tags that only makes sense in dialogue."
    e ""

# game/indepth_text.rpy:89
translate korean after_a_label_86efc45b:

    # e "The p tag breaks a paragraph,{p}and waits for the player to click."
    e ""

# game/indepth_text.rpy:91
translate korean after_a_label_3ece2387:

    # e "If it is given a number as an argument,{p=1.5}it waits that many seconds."
    e ""

# game/indepth_text.rpy:95
translate korean after_a_label_3881f72d:

    # e "The w tag also waits for a click,{w} except it doesn't break lines,{w=.5} the way p does."
    e ""

# game/indepth_text.rpy:100
translate korean after_a_label_e5321e79:

    # eslow "The nw tag causes Ren'Py to continue past slow text,{nw}"
    eslow ""

# game/indepth_text.rpy:102
translate korean after_a_label_1f2697ba:

    # extend " to the next statement."
    extend ""

# game/indepth_text.rpy:106
translate korean after_a_label_dbfca166:

    # e "To break a line without pausing,\none can write \\n. \\' and \\\" include quotes in the text."
    e ""

# game/indepth_text.rpy:111
translate korean after_a_label_ffdf7e76:

    # e "The interpolation feature takes a variable name in square brackets, and inserts it into text."
    e ""

# game/indepth_text.rpy:117
translate korean after_a_label_fc99fcbf:

    # e "For example, this displays the [variable!t]."
    e ""

# game/indepth_text.rpy:121
translate korean after_a_label_c84d9087:

    # e "When the variable name is followed by !q, special characters are quoted. This displays the raw [variable!q!t], including the italics tags."
    e ""

# game/indepth_text.rpy:126
translate korean after_a_label_c90f24a8:

    # e "When the variable name is followed by !t, it is translated to [variable!t]. It could be something else in a different language."
    e ""

# game/indepth_text.rpy:129
translate korean after_a_label_fb106a95:

    # e "Finally, certain characters are special. [[, {{, and \\ need to be doubled if included in text. The %% character should be doubled if used in dialogue."
    e ""

translate korean strings:

    # indepth_text.rpy:115
    old "{i}variable value{/i}"
    new ""

    # indepth_text.rpy:124
    old "translatable text"
    new ""

