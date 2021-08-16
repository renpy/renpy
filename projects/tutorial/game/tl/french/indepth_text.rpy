
# game/indepth_text.rpy:22
translate french a_label_8d79d234:

    # e "You just clicked to jump to a label."
    e "Vous venez juste de cliquer pour sauter vers un 'label'."

# game/indepth_text.rpy:28
translate french text_578c4060:

    # e "Sometimes, when showing text, we'll want to change the way some of the text is displayed."
    e "Parfois, quand vous affichez du texte, vous voudriez changer la façon dont celui-ci est affiché."

# game/indepth_text.rpy:31
translate french text_60750345:

    # e "For example, we might want to have text that is {b}bold{/b}, {i}italic{/i}, {s}struckthrough{/s}, or {u}underlined{/u}."
    e "Par exemple, vous pourriez vouloir afficher ce texte {b}en gras{/b}, {i}en italique{/i}, le {s}barrer{/s} ou le {u}souligner{/u}."

# game/indepth_text.rpy:33
translate french text_5e1a6ee8:

    # e "That's what text tags are for."
    e "C’est ce à quoi servent les étiquettes de texte (tag en anglais)."

# game/indepth_text.rpy:37
translate french text_38c63ec8:

    # e "Text tags are contained in braces, like the {{b} tag above. When a text tag takes a closing tag, the closing tag begins with a slash, like {{/b} does."
    e "Les étiquettes de texte sont contenues entre des accolades, comme l’étiquette {{b}. Quand une étiquette de texte nécessite une marque de fin, celle-ci commence par un slash comme ceci : {{/b}."

# game/indepth_text.rpy:39
translate french text_1760f9c8:

    # e "We've already seen the b, i, s, and u tags, but there are lot more than those. I'll show you the rest of them."
    e "Nous avons déjà vu les étiquettes 'b', 'i', 's' et 'u', mais nous allons en voir beaucoup d’autres."

# game/indepth_text.rpy:43
translate french text_a620251f:

    # e "The a text tag can {a=https://www.renpy.org}link to a website{/a} or {a=jump:a_label}jump to a label{/a}."
    e "L’étiquette 'a' permet de {a=https://www.renpy.org}faire un lien vers un site{/a} ou de {a=jump:a_label}sauter vers un label{/a}."

# game/indepth_text.rpy:49
translate french after_a_label_d22d5f4a:

    # e "The alpha text tag makes text {alpha=.5}translucent{/alpha}."
    e "L’étiquette 'alpha' permet de rendre du texte {alpha=.5}transparent{/alpha}."

# game/indepth_text.rpy:53
translate french after_a_label_7c2c3cd2:

    # e "The color text tag changes the {color=#0080c0}color{/color} of the text."
    e "L’étiquette 'color' permet de changer la {color=#0080c0}couleur{/color} du texte."

# game/indepth_text.rpy:57
translate french after_a_label_3f81fe7b:

    # e "The cps text tag {cps=25}makes text type itself out slowly{/cps}, even if slow text is off."
    e "L’étiquette 'cps' permet de {cps=25}saisir du texte lentement{/cps}, quelque soit les préférences d’affichage choisies par le joueur."

# game/indepth_text.rpy:59
translate french after_a_label_b102941f:

    # e "The cps tag can also be relative to the default speed, {cps=*2}doubling{/cps} or {cps=*0.5}halving{/cps} it."
    e "L’étiquette 'cps' peut être relative à la vitesse par défaut, on peut la {cps=*2}doubler{/cps} ou la {cps=*0.5}diviser{/cps}."

# game/indepth_text.rpy:64
translate french after_a_label_22c4339a:

    # e "The font tag changes the font, for example to {font=DejaVuSans-Bold.ttf}DejaVuSans-Bold.ttf{/font}."
    e "L’étiquette 'font' permet de changer la police, par exemple {font=DejaVuSans-Bold.ttf}DejaVuSans-Bold.ttf{/font}."

# game/indepth_text.rpy:66
translate french after_a_label_d43417d7:

    # e "Sometimes, changing to a bold font looks better than using the {{b} tag."
    e "Parfois, changer pour une police grasse est préférable à l’utilisation de l’étiquette {{b}."

# game/indepth_text.rpy:71
translate french after_a_label_f24052f9:

    # e "The k tag changes kerning. It can space the letters of a word {k=-.5}closer together{/k} or {k=.5}farther apart{/k}."
    e "L’étiquette 'k' change l’espacement pour que les lettres d’un mot apparaissent {k=-.5}plus condensées{/k} ou {k=.5}plus espacées{/k}."

# game/indepth_text.rpy:76
translate french after_a_label_2310b922:

    # e "The size tag changes the size of text. It can make text {size=+10}bigger{/size} or {size=-10}smaller{/size}, or set it to a {size=30}fixed size{/size}."
    e "L’étiquette 'size' permet de changer la taille du texte pour le rendre plus {size=+10}large{/size} or plus {size=-10}petit{/size}. Vous pouvez également {size=30}fixer sa taille{/size}."

# game/indepth_text.rpy:81
translate french after_a_label_f566abf2:

    # e "The space tag {space=30} adds horizontal space in text.{vspace=30}The vspace tag adds vertical space between lines."
    e "L’étiquette 'space' {space=30} ajoute un espace horizontal dans le texte. L’étiquette 'vspace'{vspace=30} ajoute un espace vertical entre les lignes."

# game/indepth_text.rpy:85
translate french after_a_label_054b9ffa:

    # e "There are a few text tags that only makes sense in dialogue."
    e "Il y a des étiquettes qui ne prennent sens que dans les dialogues."

# game/indepth_text.rpy:89
translate french after_a_label_86efc45b:

    # e "The p tag breaks a paragraph,{p}and waits for the player to click."
    e "L’étiquette 'p' interrompt un paragraphe,{p}et attend que l’utilisateur clique pour afficher la suite."

# game/indepth_text.rpy:91
translate french after_a_label_3ece2387:

    # e "If it is given a number as an argument,{p=1.5}it waits that many seconds."
    e "Si un nombre est donné en argument,{p=1.5}il attendra le nombre de seconde correspondant."

# game/indepth_text.rpy:95
translate french after_a_label_3881f72d:

    # e "The w tag also waits for a click,{w} except it doesn't break lines,{w=.5} the way p does."
    e "L’étiquette w attend également un clic,{w} mais elle ne provoque pas de saut de ligne{w=.5} comme le fait l’étiquette p."

# game/indepth_text.rpy:100
translate french after_a_label_e5321e79:

    # eslow "The nw tag causes Ren'Py to continue past slow text,{nw}"
    eslow "L’étiquette 'nw' oblige Ren’Py a saisir le texte lentement{nw}"

# game/indepth_text.rpy:102
translate french after_a_label_1f2697ba:

    # extend " to the next statement."
    extend " jusqu’à la prochaine déclaration."

# game/indepth_text.rpy:106
translate french after_a_label_dbfca166:

    # e "To break a line without pausing,\none can write \\n. \\' and \\\" include quotes in the text."
    e "Pour effectuer un saut de ligne sans pause, \non peut écrire \\n. \\' et \\\" permettent d’écrire des guillemets dans le texte. (NDLT : En français, pour éviter tout soucis, vous pouvez utiliser la véritable apostrophe ’.)"

# game/indepth_text.rpy:111
translate french after_a_label_ffdf7e76:

    # e "The interpolation feature takes a variable name in square brackets, and inserts it into text."
    e "La fonctionnalité d’interpolation reçoit une variable entre crochets et insère sa valeur dans le texte."

# game/indepth_text.rpy:117
translate french after_a_label_fc99fcbf:

    # e "For example, this displays the [variable!t]."
    e "Par exemple, ceci affiche la [variable!t]."

# game/indepth_text.rpy:121
translate french after_a_label_c84d9087:

    # e "When the variable name is followed by !q, special characters are quoted. This displays the raw [variable!q!t], including the italics tags."
    e "Quand le nom de la variable est suivi de !q, les caractères spéciaux sont protégés. Ceci affiche le contenu [variable!q!t], incluant les étiquettes 'italique'."

# game/indepth_text.rpy:126
translate french after_a_label_c90f24a8:

    # e "When the variable name is followed by !t, it is translated to [variable!t]. It could be something else in a different language."
    e "Quand le nom de variable est suivi par !t, la valeur est traduite à [variable!t]. Sa valeur peut donc être différente dans d’autres langages."

# game/indepth_text.rpy:129
translate french after_a_label_fb106a95:

    # e "Finally, certain characters are special. [[, {{, and \\ need to be doubled if included in text. The %% character should be doubled if used in dialogue."
    e "Enfin, certains caractères sont spéciaux. [[, {{ et \\ doivent être doublés pour être affiché dans le texte. Le caractère %% doit également être doublé s’il est utilisé dans un dialogue."

translate french strings:

    # indepth_text.rpy:115
    old "{i}variable value{/i}"
    new "{i}valeur de la variable{/i}"

    # indepth_text.rpy:124
    old "translatable text"
    new "texte traduit en français"
