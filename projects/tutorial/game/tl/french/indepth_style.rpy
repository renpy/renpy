
# game/indepth_style.rpy:40
translate french new_gui_17a0326e:

    # e "When you create a new project, Ren'Py will automatically create a GUI - a Graphical User Interface - for it."
    e "Quand vous créez un nouveau projet, Ren’Py va automatiquement créer une interface graphique pour l’utilisateur, une GUI (Graphical User Interface)."

# game/indepth_style.rpy:42
translate french new_gui_12c814ed:

    # e "It defines the look of both in-game interface, like this text box, and out-of-game interface like the main and game menus."
    e "Elle définit le look de l’interface de jeu, comme cette zone de texte mais aussi le look hors de l’interface de jeu comme le menu principal et les menus du jeu."

# game/indepth_style.rpy:44
translate french new_gui_0a2a73bb:

    # e "The default GUI is meant to be nice enough for a simple project. With a few small changes, it's what you're seeing in this game."
    e "La GUI par défaut est pensée pour être suffisante pour un simple projet. Avec quelques petits changements, cela peut donner ce que vous voyez actuellement dans ce jeu."

# game/indepth_style.rpy:46
translate french new_gui_22adf68e:

    # e "The GUI is also meant to be easy for an intermediate creator to customize. Customizing the GUI consists of changing the image files in the gui directory, and changing variables in gui.rpy."
    e "La GUI est aussi pensée pour qu’un créateur de niveau intermédiaire puisse facilement la personnaliser. Personnaliser la GUI consiste à changer les fichiers images et modifier quelques variables dans le fichier gui.rpy."

# game/indepth_style.rpy:48
translate french new_gui_da21de30:

    # e "At the same time, even when customized, the default GUI might be too recognizable for an extremely polished game. That's why we've made it easy to totally replace."
    e "En même temps et même si elle est personnalisée, l’interface graphique par défaut peut être trop reconnaissable pour un jeu extrêmement soigné. C’est pourquoi nous l'avons rendu facile à remplacer totalement."

# game/indepth_style.rpy:50
translate french new_gui_45765574:

    # e "We've put an extensive guide to customizing the GUI on the Ren'Py website. So if you want to learn more, visit the {a=https://www.renpy.org/doc/html/gui.html}GUI customization guide{/a}."
    e "Nous avons écrit un guide complet pour personnaliser la GUI sur le site Ren’Py. Alors, si vous souhaitez en apprendre plus, consultez le {a=https://www.renpy.org/doc/html/gui.html}guide de personnalisation de la GUI{/a}."

# game/indepth_style.rpy:58
translate french styles_fa345a38:

    # e "Ren'Py has a powerful style system that controls what displayables look like."
    e "Ren’Py intègre un puissant système pour contrôler le styles des différents éléments affichables."

# game/indepth_style.rpy:60
translate french styles_6189ee12:

    # e "While the default GUI uses variables to provide styles with sensible defaults, if you're replacing the GUI or creating your own screens, you'll need to learn about styles yourself."
    e "Par défaut, les variables définissant l’interface graphique sont initialisées avec des valeurs raisonnables, si vous remplacez l’interface graphique ou créez vos propres écrans, vous allez devoir en apprendre plus sur les styles."

# game/indepth_style.rpy:66
translate french styles_menu_a4a6913e:

    # e "What would you like to know about styles?" nointeract
    e "Qu’est-ce que vous souhaitez apprendre au sujet des styles ?" nointeract

# game/indepth_style.rpy:98
translate french style_basics_9a79ef89:

    # e "Styles let a displayable look different from game to game, or even inside the same game."
    e "Les styles peuvent adopter un look différent d’un jeu à l’autre et même au sein du même jeu."

# game/indepth_style.rpy:103
translate french style_basics_48777f2c:

    # e "Both of these buttons use the same displayables. But since different styles have been applied, the buttons look different from each other."
    e "Ces deux boutons utilisent les mêmes éléments affichables, mais différents styles y sont appliqués. Les boutons semblent donc différents."

# game/indepth_style.rpy:108
translate french style_basics_57704d8c:

    # e "Styles are a combination of information from four different places."
    e "Les styles sont une combinaison d’informations venant de plusieurs sources."

# game/indepth_style.rpy:121
translate french style_basics_144731f6:

    # e "The first place Ren'Py can get style information from is part of a screen. Each displayable created by a screen can take a style name and style properties."
    e "La déclaration 'screen' est le premier endroit où Ren’Py peut trouver l’information stylistique. Chaque élément affichable de l’écran peut recevoir un nom de style et des propriétés de styles."

# game/indepth_style.rpy:138
translate french style_basics_67e48162:

    # e "When a screen displayable contains text, style properties prefixed with text_ apply to that text."
    e "Quand un élément affichable contient du texte, les propriétés de style préfixées par text_ s’appliquent à chaque texte."

# game/indepth_style.rpy:151
translate french style_basics_03516b4a:

    # e "The next is as part of a displayable created in an image statement. Style properties are just arguments to the displayable."
    e "L’autre façon d’appliquer un style est de créer l’élément affichable via une déclaration image. Les propriétés de style sont simplement des arguments de l’élément créé."

# game/indepth_style.rpy:160
translate french style_basics_ccc0d1ca:

    # egreen "Style properties can also be given as arguments when defining a character."
    egreen "Les propriétés de styles peuvent également être fournies en argument quand elles définissent un personnage."

# game/indepth_style.rpy:162
translate french style_basics_013ab314:

    # egreen "Arguments beginning with who_ are style properties applied to the character's name, while those beginning with what_ are applied to the character's dialogue."
    egreen "Les arguments qui commencent par 'who_' sont des propriétés de style qui s’appliquent au nom du personnage, alors que celles qui commencent par 'what_' s’appliquent aux dialogues."

# game/indepth_style.rpy:164
translate french style_basics_dbe80939:

    # egreen "Style properties that don't have a prefix are also applied to the character's name."
    egreen "Les propriétés de style qui n’ont pas de préfixe s’appliquent au nom du personnage."

# game/indepth_style.rpy:174
translate french style_basics_ac6a8414:

    # e "Finally, there is the the style statement, which creates or changes a named style. By giving Text the style argument, we tell it to use the blue_text style."
    e "Enfin, il y a des déclarations de style qui créent ou changent un style nommé. En fournissant l’argument de style à Text, nous lui disons d’utiliser le style 'blue_text'."

# game/indepth_style.rpy:180
translate french style_basics_3d9bdff7:

    # e "A style property can inherit from a parent. If a style property is not given in a style, it comes from the parent of that style."
    e "Une propriété de style peut hériter des informations d’un parent. Si une propriété de style n’est pas donnée à un style, alors il prendra la valeur de la classe parente."

# game/indepth_style.rpy:182
translate french style_basics_49c5fbfe:

    # e "By default the parent of the style has the same name, with the prefix up to the the first underscore removed. If the style does not have an underscore in its name, 'default' is used."
    e "Par défaut, le parent d’un style a le même nom sans le préfixe. Si le style n’a pas de préfixe, alors il hérite des valeurs du style 'default'."

# game/indepth_style.rpy:184
translate french style_basics_6ab170a3:

    # e "For example, blue_text inherits from text, which in turn inherits from default. The default style defines all properties, so it doesn't inherit from anything."
    e "Par exemple, 'blue_text' hérite de 'text', qui lui-même hérite de 'default'. Le style par défaut définit toutes les propriétés, donc il n’a pas à hériter de valeur de qui que ce soit d’autre."

# game/indepth_style.rpy:190
translate french style_basics_f78117a7:

    # e "The parent can be explicitly changed by giving the style statement an 'is' clause. In this case, we're explictly setting the style to the parent of text."
    e "Le parent peut explicitement être changé en indiquant la déclaration de style la clause 'is'. Dans ce cas, on initialise le style explicitement avec les valeurs du parent déclaré."

# game/indepth_style.rpy:194
translate french style_basics_6007040b:

    # e "Each displayable has a default style name. By default, it's usually the lower-case displayable name, like 'text' for Text, or 'button' for buttons."
    e "Chaque élément affichable a un nom de style par défaut. Par défaut, ce nom est correspond à son nom de classe en minuscule, comme 'text' pour un 'Text' et 'button' pour les boutons."

# game/indepth_style.rpy:196
translate french style_basics_35db9a05:

    # e "In a screen, a displayable can be given the style_prefix property to give a prefix for that displayable and it's children."
    e "À l’écran, on peut renseigner la propriété 'style_prefix' pour chaque élément affichable. Ce préfixe servira à identifier le style de l’élément et de tous ses enfants."

# game/indepth_style.rpy:198
translate french style_basics_422a87f7:

    # e "For example, a text displayable with a style_prefix of 'help' will be given the style 'help_text'."
    e "Par exemple, un texte affichable avec la propriété 'style_prefix' déclarée à 'help' sera configuré avec les éléments de style déclarés dans 'help_text'."

# game/indepth_style.rpy:200
translate french style_basics_bad2e207:

    # e "Lastly, when a displayable is a button, or inside a button, it can take style prefixes."
    e "Enfin, quand un élément affichable est un bouton ou un élément d’un bouton, il peut également recevoir un préfixe de style en fonction de son état."

# game/indepth_style.rpy:202
translate french style_basics_22ed20a1:

    # e "The prefixes idle_, hover_, and insensitive_ are used when the button is unfocused, focused, and unfocusable."
    e "Les préfixes 'idle_', 'hover_' et 'insensitive_' sont appliqués en fonction des états du bouton, respectivement 'non survolé', 'survolé' et 'non cliquable'."

# game/indepth_style.rpy:204
translate french style_basics_7a58037e:

    # e "These can be preceded by selected_ to change how the button looks when it represents a selected value or screen."
    e "Ceux-ci peuvent également être précédés par 'selected_' pour changer son apparence quand il représente une valeur sélectionnée."

# game/indepth_style.rpy:233
translate french style_basics_0cdcb8c3:

    # e "This screen shows the style prefixes in action. You can click on a button to select it, or click outside to advance."
    e "Cet écran vous montre les préfixes de style en action. Vous pouvez cliquer sur un bouton pour le sélectionner, ou cliquer à l’extérieur pour avancer dans le tutoriel."

# game/indepth_style.rpy:240
translate french style_basics_aed05094:

    # e "Those are the basics of styles. If GUI customization isn't enough for you, styles let you customize just about everything in Ren'Py."
    e "Nous venons de découvrir les bases des styles. Si cette personnalisation de la GUI n’est pas suffisante pour vous, sachez que Ren’Py vous laisse tout personnaliser."

# game/indepth_style.rpy:253
translate french style_general_81f3c8ff:

    # e "The first group of style properties that we'll go over are the general style properties. These work with every displayable, or at least many different ones."
    e "Le premier groupe des propriétés de style que nous allons découvrir concerne les propriétés générales. Elles fonctionnent avec tous les éléments affichables ou du moins avec l’essentiel d’entre eux."

# game/indepth_style.rpy:264
translate french style_general_a8d99699:

    # e "Every displayable takes the position properties, which control where it can be placed on screen. Since I've already mentioned them, I won't repeat them here."
    e "Chaque élément affichable peut recevoir des propriétés de position qui vont donc contrôler la position à l’écran. Comme je les ai déjà présentées auparavant, je ne vais pas me répéter ici."

# game/indepth_style.rpy:275
translate french style_general_58d4a18f:

    # e "The xmaximum and ymaximum properties set the maximum width and height of the displayable, respectively. This will cause Ren'Py to shrink things, if possible."
    e "Les propriétés 'xmaximum' et 'ymaximum' définissent respectivement la largeur et la hauteur maximales de l’élément. Ren’Py va alors rétrécir les éléments, si c’est possible."

# game/indepth_style.rpy:277
translate french style_general_cae9a39f:

    # e "Sometimes, the shrunken size will be smaller than the size given by xmaximum and ymaximum."
    e "Parfois, la taille rétrécie va être plus petite que les valeurs mentionnées par 'xmaximum' et 'ymaximum'."

# game/indepth_style.rpy:279
translate french style_general_5928c24e:

    # e "Similarly, the xminimum and yminimum properties set the minimum width and height. If the displayable is smaller, Ren'Py will try to make it bigger."
    e "Par analogie, les propriétés 'xminimum' et 'yminimum' définissent la largeur et la hauteur minimale. Si l’élément affichable est plus petit, Ren’Py tentera de l’agrandir."

# game/indepth_style.rpy:289
translate french style_general_35a8ee5e:

    # e "The xsize and ysize properties set the minimum and maximum size to the same value, fixing the size."
    e "Les propriétés 'xsize' et 'ysize' définissent la taille minimale et maximale à la même valeur. Par conséquent, ces propriétés fixent la taille. "

# game/indepth_style.rpy:291
translate french style_general_fcfb0640:

    # e "These only works for displayables than can be resized. Some displayables, like images, can't be made bigger or smaller."
    e "Tout cela ne fonctionne évidemment que pour les éléments qui peuvent être redimensionnés. Certains éléments, comme les images, ne peuvent pas être agrandies ou rétrécies."

# game/indepth_style.rpy:299
translate french style_general_cd5cc97c:

    # e "The area property takes a tuple - a parenthesis bounded list of four items. The first two give the position, and the second two the size."
    e "La propriété 'aera' doit être initialisée par un tuple, une liste de quatre éléments entre parenthèses. Le premier couple donne la position, le second couple la taille."

# game/indepth_style.rpy:308
translate french style_general_e5a58f0b:

    # e "Finally, the alt property changes the text used by self-voicing for the hearing impaired."
    e "Enfin, la propriété 'alt' change le texte utilisé par la synthèse vocale pour aider les joueurs sourds ou malentendants."

# game/indepth_style.rpy:335
translate french style_text_fe457b8f:

    # e "The text style properties apply to text and input displayables."
    e "La propriété de style 'text' s’applique uniquement aux éléments de texte et de saisie."

# game/indepth_style.rpy:337
translate french style_text_7ab53f03:

    # e "Text displayables can be created implicitly or explicitly. For example, a textbutton creates a text displayable with a style ending in button_text."
    e "Les éléments de texte peuvent être créés de façon implicite ou explicite. Par exemple, un bouton textuel crée un élément de texte avec un nom de style se terminant par 'button_text'."

# game/indepth_style.rpy:339
translate french style_text_6dd42a57:

    # e "These can also be set in gui.rpy by changing or defining variables with names like gui.button_text_size."
    e "Ces styles peuvent donc être initialisés dans le fichier gui.rpy en changeant ou en définissant des variables avec des noms tels que gui.button_text_size."

# game/indepth_style.rpy:347
translate french style_text_c689130e:

    # e "The bold style property makes the text bold. This can be done using an algorithm, rather than a different version of the font."
    e "La propriété de style 'bold' rend le texte en gras. "

# game/indepth_style.rpy:355
translate french style_text_3420bfe4:

    # e "The color property changes the color of the text. It takes hex color codes, just like everything else in Ren'Py."
    e "La propriété 'color' change la couleur du texte. Elle doit être composée de codes couleur hexadécimaux, comme n’importe quelle autre couleur dans Ren’Py."

# game/indepth_style.rpy:363
translate french style_text_14bd6327:

    # e "The first_indent style property determines how far the first line is indented."
    e "La propriété de style 'first_indent' détermine comment la première ligne de texte sera indentée."

# game/indepth_style.rpy:371
translate french style_text_779ac517:

    # e "The font style property changes the font the text uses. Ren'Py takes TrueType and OpenType fonts, and you'll have to include the font file as part of your visual novel."
    e "La propriété de style 'font' change la police. Ren’Py accepte les polices TrueType et OpenType. Vous aurez à inclure les polices dans votre projet."

# game/indepth_style.rpy:379
translate french style_text_917e2bca:

    # e "The size property changes the size of the text."
    e "La propriété 'size' change la taille du texte."

# game/indepth_style.rpy:388
translate french style_text_1a46cd43:

    # e "The italic property makes the text italic. Again, this is better done with a font, but for short amounts of text Ren'Py can do it for you."
    e "La propriété 'italic' rend le texte en italique. Encore une fois, il est souvent préférable de changer pour une police intrasèquement en italique, mais pour de petites zones de texte, cela peut suffire."

# game/indepth_style.rpy:397
translate french style_text_472f382d:

    # e "The justify property makes the text justified, lining all but the last line up on the left and the right side."
    e "La propriété 'justify' rend le texte en justifié, alignant tout à gauche et à droite, sauf la dernière ligne."

# game/indepth_style.rpy:405
translate french style_text_87b075f8:

    # e "The kerning property kerns the text. When it's negative, characters are closer together. When positive, characters are farther apart."
    e "La propriété 'kerning' définit l’espacement entre les caractères. Quand la valeur est négative, les caractères sont condensés. Quand la valeur est positive, les caractères sont plus espacés."

# game/indepth_style.rpy:415
translate french style_text_fe7dec14:

    # e "The line_leading and line_spacing properties put spacing before each line, and between lines, respectively."
    e "Les propriétés 'line_leading' et 'line_spacing' placent respectivement des espaces avant chaque ligne et entre les lignes."

# game/indepth_style.rpy:424
translate french style_text_aee9277a:

    # e "The outlines property puts outlines around text. This takes a list of tuples, which is a bit complicated."
    e "La propriété 'outlines' place une bordure autour du texte, autour des caractères. Elle doit être renseignée par un tuple, ce qui est un peu compliqué."

# game/indepth_style.rpy:426
translate french style_text_b4c5190f:

    # e "But if you ignore the brackets and parenthesis, you have the width of the outline, the color, and then horizontal and vertical offsets."
    e "Si vous ignorez les crochets et les parenthèses, vous verrez l’épaisseur de la bordure, la couleur et les décalages horizontal et vertical."

# game/indepth_style.rpy:434
translate french style_text_5a0c2c02:

    # e "The rest_indent property controls the indentation of lines after the first one."
    e "La propriété 'rest_indent' contrôle l’indentation des lignes après la première."

# game/indepth_style.rpy:443
translate french style_text_430c1959:

    # e "The text_align property controls the positioning of multiple lines of text inside the text displayable. For example, 0.5 means centered."
    e "La propriété 'text_align' contrôle l’alignement d’un texte de plusieurs lignes. Par exemple, 0.5 centre le texte."

# game/indepth_style.rpy:445
translate french style_text_19aa0833:

    # e "It doesn't change the position of the text displayable itself. For that, you'll often want to set the text_align and xalign to the same value."
    e "Cela ne change pas directement la position du texte. Pour cela, vous allez souvent initialiser les propriétés 'text_align' et 'xalign' avec la même valeur."

# game/indepth_style.rpy:455
translate french style_text_efc3c392:

    # e "When both text_align and xalign are set to 1.0, the text is properly right-justified."
    e "Ainsi, quand 'text_align' et 'xalign' sont initialisées à 1, alors le texte est aligné à droite."

# game/indepth_style.rpy:464
translate french style_text_43be63b9:

    # e "The underline property underlines the text."
    e "La propritété 'underline' souligne le texte."

# game/indepth_style.rpy:471
translate french style_text_343f6d34:

    # e "Those are the most common text style properties, but not the only ones. Here are a few more that you might need in special circumstances."
    e "C’étaient les principales propriétés de style s’appliquant aux textes, mais ce ne sont pas les seules. En voici d’autres que vous pourrez utiliser dans des circonstances plus particulières."

# game/indepth_style.rpy:479
translate french style_text_e7204a95:

    # e "By default, text in Ren'Py is antialiased, to smooth the edges. The antialias property can turn that off, and make the text a little more jagged."
    e "Par défaut, les textes dans Ren’Py sont antialiasés, pour arrondir les angles. La propriété 'antialias' peut être désactivée rendant le texte un peu plus irrégulier."

# game/indepth_style.rpy:487
translate french style_text_a5316e4c:

    # e "The adjust_spacing property is a very subtle one, that only matters when a player resizes the window. When True, characters will be shifted a bit so the Text has the same relative spacing."
    e "La propriété 'adjust_spacing' est très subtile. Elle n’a d’importance que lorsque les joueurs redimensionnent la fenêtre. À True, les caractères seront légèrement décalés pour que le texte conserve le même espacement."

# game/indepth_style.rpy:496
translate french style_text_605d4e4a:

    # e "When False, the text won't jump around as much. But it can be a little wider or narrower based on screen size."
    e "À False, le texte ne sera pas décalé, mais il pourra être un peu plus étroit ou plus large à l’écran."

# game/indepth_style.rpy:505
translate french style_text_acf8a0e1:

    # e "The layout property has a few special values that control where lines are broken. The 'nobreak' value disables line breaks entirely, making the text wider."
    e "La propriété 'layout' peut prendre différentes valeurs qui contrôle les retours à la ligne. La valeur 'nobreak' bloquera tout retour à la ligne."

# game/indepth_style.rpy:516
translate french style_text_785729cf:

    # e "When the layout property is set to 'subtitle', the line breaking algorithm is changed to try to make all lines even in length, as subtitles usually are."
    e "Quand la propriété 'layout' vaut 'subtitle', l’algorithme de retour à la ligne est modifié pour essayer que chaque ligne fasse la même longueur, comme dans les sous-titrages."

# game/indepth_style.rpy:524
translate french style_text_9c26f218:

    # e "The strikethrough property draws a line through the text. It seems pretty unlikely you'd want to use this one."
    e "La propriété 'strikethrough' dessine une ligne en travers du texte. Il semble assez improbable que vous vouliez l’utiliser."

# game/indepth_style.rpy:534
translate french style_text_c7229243:

    # e "The vertical style property places text in a vertical layout. It's meant for Asian languages with special fonts."
    e "La propriété de style 'vertical' place le texte dans un canvas vertical. C’est utilisé pour les langages asiatiques avec des polices spécifiques."

# game/indepth_style.rpy:540
translate french style_text_724bd5e0:

    # e "And those are the text style properties. There might be a lot of them, but we want to give you a lot of control over how you present text to your players."
    e "Et voilà pour les propriétés de style applicables aux textes. Il y en a peut-être beaucoup, mais nous voulons vous donner le maximum de contrôle sur la façon de présenter le texte à vos joueurs."

# game/indepth_style.rpy:580
translate french style_button_300b6af5:

    # e "Next up, we have the window and button style properties. These apply to windows like the text window at the bottom of this screen and frames like the ones we show examples in."
    e "Nous allons voir les propriétés de style pour les fenêtres et les boutons. Ces propriétés s’appliquent à toute fenêtre comme la fenêtre de texte en bas de cet écran et les cadres comme ceux qui contiennent les exemples."

# game/indepth_style.rpy:582
translate french style_button_255a18e4:

    # e "These properties also apply to buttons, in-game and out-of-game. To Ren'Py, a button is a window you can click."
    e "Ces propriétés s’appliquent également aux boutons, qu’ils soient dans le jeu ou hors du jeu. Pour Ren’Py un bouton n’est qu’une fenêtre sur laquelle vous pouvez cliquer."

# game/indepth_style.rpy:593
translate french style_button_9b53ce93:

    # e "I'll start off with this style, which everything will inherit from. To make our lives easier, it inherits from the default style, rather than the customizes buttons in this game's GUI."
    e "Je vais commencer par ce style dont tous les éléments affichables des exemples hériteront. Pour nous simplifier la vie, il hérite du style par défaut plutôt que des éléments déjà personnalisés par l’interface de ce tutoriel."

# game/indepth_style.rpy:595
translate french style_button_aece4a8c:

    # e "The first style property is the background property. It adds a background to the a button or window. Since this is a button, idle and hover variants choose different backgrounds when focused."
    e "La première propriété de style est 'background'. Elle ajoute un arrière plan au bouton ou à la fenêtre. Comme il s’agit d’un bouton, les variantes 'idle' et 'hover' prennent un autre arrière-plan quand le focus lui est donné."

# game/indepth_style.rpy:597
translate french style_button_b969f04a:

    # e "We also center the two buttons, using the xalign position property."
    e "Nous pouvons aussi centrer deux boutons en utilisant la propriété 'xalign'."

# game/indepth_style.rpy:601
translate french style_button_269ae069:

    # e "We've also customized the style of the button's text, using this style. It centers the text and makes it change color when hovered."
    e "Nous pouvons aussi personnaliser le style du texte du bouton en utilisant ce style. Il centre le texte et change la couleur quand il est survolé."

# game/indepth_style.rpy:612
translate french style_button_1009f3e1:

    # e "Without any padding around the text, the button looks odd. Ren'Py has padding properties that add space inside the button's background."
    e "Sans aucun espacement autour du texte, le bouton rend mal. Ren’Py possèdent des propriétés 'padding' qui ajoute de l’espace à l’intérieur du bouton."

# game/indepth_style.rpy:621
translate french style_button_5bdfa45a:

    # e "More commonly used are the xpadding and ypadding style properties, which add the same padding to the left and right, or the top and bottom, respectively."
    e "Les propriétés de style 'xpadding' et 'ypadding' sont plus communément utilisées, elles ajoutent le même espacement respectivement à gauche et à droite, ou en haut et en bas."

# game/indepth_style.rpy:629
translate french style_button_81283d42:

    # e "The margin style properties work the same way, except they add space outside the background. The full set exists: left_margin, right_margin, top_margin, bottom_margin, xmargin, and ymargin."
    e "Les propriétés de style 'margin' fonctionnent de la même façon, si ce n’est qu’elles ajoutent de l’espace autour du bouton. L’ensemble complet existe : 'left_margin', 'right_margin', 'top_margin', 'bottom_margin', 'xmargin' et 'ymargin'."

# game/indepth_style.rpy:638
translate french style_button_0b7aca6b:

    # e "The size_group style property takes a string. Ren'Py will make sure that all the windows or buttons with the same size_group string are the same size."
    e "La propriété de style 'size_group' reçoit une chaîne de caractères. Ren’Py va s’assurer que toutes les fenêtres ou les boutons avec la même valeur 'size_group' aient tous la même taille."

# game/indepth_style.rpy:647
translate french style_button_4c6da7d9:

    # e "Alternatively, the xfill and yfill style properties make a button take up all available space in the horizontal or vertical directions."
    e "Alternativement, les propriétés de style 'xfill' et 'yfill' modifieront un bouton pour qu’il occupe respectivement tout l’espace horizontal ou vertical."

# game/indepth_style.rpy:657
translate french style_button_fd5338b2:

    # e "The foreground property gives a displayable that is placed on top of the contents and background of the window or button."
    e "La propriété 'foreground' fournit un élément affichable qui sera placé devant le contenu et l’arrière-plan d’une fenêtre ou d’un bouton."

# game/indepth_style.rpy:659
translate french style_button_b8af697c:

    # e "One way to use it is to provide extra decorations to a button that's serving as a checkbox. Another would be to use it with a Frame to provide a glossy shine that overlays the button's contents."
    e "L’un des moyens de l’utiliser est de fournir des décorations à un bouton pour qu’il serve de case à cocher. Un autre moyen serait de l’utiliser pour qu’une fenêtre ait des reflets."

# game/indepth_style.rpy:668
translate french style_button_c0b1b62e:

    # e "There are also a few style properties that only apply to buttons. The hover_sound and activate_sound properties play sound files when a button is focused and activated, respectively."
    e "Il y a également quelques propriétés de styles qui ne s’appliquent qu’aux boutons. Les propriétés 'hover_sound' et 'activate_sound' permettent de définir des sons à jouer quand un bouton reçoit le focus ou quand il est activé."

# game/indepth_style.rpy:677
translate french style_button_02fa647e:

    # e "Finally, the focus_mask property applies to partially transparent buttons. When it's set to True, only areas of the button that aren't transparent cause a button to focus."
    e "Finalement, la propriété 'focus_mask' applique une transparence partielle au bouton. Quand sa valeur est à True, seules les zones du bouton qui ne sont pas transparentes peuvent permettre le focus lors du survol de la souris notamment."

# game/indepth_style.rpy:759
translate french style_bar_414d454a:

    # e "To demonstrate styles, let me first show two of the images we'll be using. This is the image we're using for parts of the bar that are empty."
    e "Pour vous présenter les styles, laissez-moi vous montrer les deux images que nous allons utiliser. Voici l’image qui servira pour les parties vides de la barre."

# game/indepth_style.rpy:763
translate french style_bar_9422b7b0:

    # e "And here's what we use for parts of the bar that are full."
    e "Et voici celle qui sera utilisée pour les parties remplies de la barre."

# game/indepth_style.rpy:775
translate french style_bar_8ae6a14b:

    # e "The left_bar and right_bar style properties, and their hover variants, give displayables for the left and right side of the bar. By default, the value is shown on the left."
    e "Les propriétés de style 'left_bar' et 'right_bar' et leurs variantes 'hover' fournissent les éléments affichables pour les côtés gauche et droit de la barre. Par défaut, la jauge se remplit par la gauche."

# game/indepth_style.rpy:777
translate french style_bar_7f0f50e5:

    # e "Also by default, both the left and right displayables are rendered at the full width of the bar, and then cropped to the appropriate size."
    e "De même par défaut, les éléments affichables à droite et à gauche sont rendus avec la pleine largeur de la barre et ils sont coupés à la taille appropriée."

# game/indepth_style.rpy:779
translate french style_bar_9ef4f62f:

    # e "We give the bar the ysize property to set how tall it is. We could also give it xsize to choose how wide, but here it's limited by the width of the frame it's in."
    e "Nous indiquons à la barre la propriété 'ysize' pour préciser sa hauteur. Nous pourrions aussi lui donner 'xsize' pour choisir sa largeur, mais ici nous sommes limités par la largeur du cadre."

# game/indepth_style.rpy:792
translate french style_bar_d4c29710:

    # e "When the bar_invert style property is True, the bar value is displayed on the right side of the bar. The left_bar and right_bar displayables might also need to be swapped."
    e "Quand la propriété de style 'bar_invert' est à True, la jauge de la barre est affichée à droite. Les éléments de 'left_bar' et 'right_bar' ont également besoin d’être intervertis."

# game/indepth_style.rpy:806
translate french style_bar_cca67222:

    # e "The bar_resizing style property causes the bar images to be resized to represent the value, rather than being rendered at full size and cropped."
    e "La propriété de style 'bar_resizing' provoque le redimensionnement de l’image pour représenter la valeur, plutôt que d’être rendue sur toute la taille puis coupée."

# game/indepth_style.rpy:819
translate french style_bar_7d361bac:

    # e "The thumb style property gives a thumb image, that's placed based on the bars value. In the case of a scrollbar, it's resized if possible."
    e "La propriété de style 'thumb' précise la vignette de l’image qui sera placée sur la barre en fonction de la valeur. Dans le cas d’un ascenseur, son redimensionnement est possible."

# game/indepth_style.rpy:821
translate french style_bar_b6dfb61b:

    # e "Here, we use it with the base_bar style property, which sets both bar images to the same displayable."
    e "Ici, nous l’utilisons avec la propriété de style 'base_bar' qui définit les deux images de la barre pour le même élément affichable."

# game/indepth_style.rpy:836
translate french style_bar_996466ad:

    # e "The left_gutter and right_gutter properties set a gutter on the left or right size of the bar. The gutter is space the bar can't be dragged into, that can be used for borders."
    e "Les propriété 'left_gutter' et 'right_gutter' définissent une gouttière sur la gauche ou la droite de la barre. Cette gouttière ne peut pas être déplacée. Elle peut être utilisée pour les bordures."

# game/indepth_style.rpy:851
translate french style_bar_fa41a83c:

    # e "The bar_vertical style property displays a vertically oriented bar. All of the other properties change names - left_bar becomes top_bar, while right_bar becomes bottom_bar."
    e "La propriété de style 'bar_vertical' affiche une barre orientée verticalement. Toutes les propriétés changent alors de nom. 'left_bar' devient 'top_bar', tandis que 'right_bar' devient 'bottom_bar'."

# game/indepth_style.rpy:856
translate french style_bar_5d33c5dc:

    # e "Finally, there's one style we can't show here, and it's unscrollable. It controls what happens when a scrollbar can't be moved at all."
    e "Finalement, il y a un style que nous ne pouvons pas voir ici, c’est 'unscrollable'. Il contrôle ce qu’il se passe quand un ascenseur ne peut pas être déplacé du tout."

# game/indepth_style.rpy:858
translate french style_bar_e8e32280:

    # e "By default, it's shown. But if unscrollable is 'insensitive', the bar becomes insensitive. If it's 'hide', the bar is hidden, but still takes up space."
    e "Par défaut, il est affiché. Mais si 'unscrollable' est initialisé à 'insensitive', alors la barre devient non sensible. Si la valeur est à 'hide', alors la barre est cachée, mais elle occupe toujours l’espace."

# game/indepth_style.rpy:862
translate french style_bar_f1292000:

    # e "That's it for the bar properties. By using them, a creator can customize bars, scrollbars, and sliders."
    e "Voilà pour les propriétés des barres. En les utilisant, le créateur peut personnaliser les barres, les ascenseurs et les curseurs."

# game/indepth_style.rpy:961
translate french style_box_5fd535f4:

    # e "The hbox displayable is used to lay its children out horizontally. By default, there's no spacing between children, so they run together."
    e "L’élément affichable 'hbox' est utilisé pour disposer ses enfants (son contenu) horizontalement. Par défaut, il n’y a pas d’espace entre les éléments enfants, alors ils se suivent les uns les autres."

# game/indepth_style.rpy:967
translate french style_box_0111e5dc:

    # e "Similarly, the vbox displayable is used to lay its children out vertically. Both support style properties that control placement."
    e "De façon similaire, l’élément 'vbox' est utilisé pour les disposer verticalement. Les deux supportent les propriétés de style qui contrôlent le positionnement."

# game/indepth_style.rpy:972
translate french style_box_5a44717b:

    # e "To make the size of the box displayable obvious, I'll add a highlight to the box itself, and not the frame containing it."
    e "Pour rendre la taille de l’élément affiché visible, je vais illuminer la boîte elle-même et non le cadre qui la contient."

# game/indepth_style.rpy:980
translate french style_box_239e7a8f:

    # e "Boxes support the xfill and yfill style properties. These properties make a box expand to fill the available space, rather than the space of the largest child."
    e "Les boîtes supportent les propriétés de style 'xfill' et 'yfill'. Ces propriétés étendent la boîte pour qu’elle occupe tout l’espace disponible plutôt que l’espace du plus large des éléments qu’elle contient."

# game/indepth_style.rpy:990
translate french style_box_e513c946:

    # e "The spacing style property takes a value in pixels, and adds that much spacing between each child of the box."
    e "La propriété de style 'spacing' reçoit une valeur entière exprimée en pixels. Elle ajoute cet espacement entre chaque élément de la boîte."

# game/indepth_style.rpy:1000
translate french style_box_6ae4f94d:

    # e "The first_spacing style property is similar, but it only adds space between the first and second children. This is useful when the first child is a title that needs different spacing."
    e "La propriété de style 'first_spacing' est similaire, mais elle ajoute uniquement de l’espace entre le premier et le second élément. C’est pratique quand le premier élément est un titre qui nécessite un espacement différent."

# game/indepth_style.rpy:1010
translate french style_box_0c518d9f:

    # e "The box_reverse style property reverses the order of entries in the box."
    e "La propriété de style 'box_revese' inverse l’ordre des entrées dans la boîte."

# game/indepth_style.rpy:1023
translate french style_box_f73c1422:

    # e "We'll switch back to a horizontal box for our next example."
    e "Nous revenons sur une boîte horizontale pour notre prochain exemple."

# game/indepth_style.rpy:1033
translate french style_box_285592bb:

    # e "The box_wrap style property fills the box with children until it's full, then starts again on the next line."
    e "La propriété de style 'box_wrap' remplit la boîte avec ses enfants, ses éléments de contenu, jusqu’à ce qu'elle soit remplie, puis elle passe à la ligne suivante."

# game/indepth_style.rpy:1046
translate french style_box_a7637552:

    # e "Grids bring with them two more style properties. The xspacing and yspacing properties control spacing in the horizontal and vertical directions, respectively."
    e "Les grilles peuvent recevoir deux propriétés de style supplémentaires. Les propriétés 'xspacing' et 'yspacing' contrôle respectivement l’espacement horizontal et vertical."

# game/indepth_style.rpy:1053
translate french style_box_4006f74b:

    # e "Lastly, we have the fixed layout. The fixed layout usually expands to fill all space, and shows its children from back to front."
    e "Enfin, nous avons les cadres fixés (fixed layout). Par usage, les cadres fixés s’étendent pour remplir tout l’espace pour montrer les éléments de contenu de l’arrière vers l’avant."

# game/indepth_style.rpy:1055
translate french style_box_4a2866f0:

    # e "But of course, we have some style properties that can change that."
    e "Mais, bien sûr, nous avons quelques propriétés de style pour changer cela."

# game/indepth_style.rpy:1064
translate french style_box_66e042c4:

    # e "When the xfit style property is True, the fixed lays out all its children as if it was full size, and then shrinks in width to fit them. The yfit style works the same way, but in height."
    e "Quand la propriété de style 'xfit' est à True, alors le canvas affiche chaque élément de contenu à sa taille d’origine et les réduit ensuite en largeur pour les afficher correctement dans la largeur. La propriété de style 'yfit' fonctionne de la même façon, mais en hauteur."

# game/indepth_style.rpy:1072
translate french style_box_6a593b10:

    # e "The order_reverse style property changes the order in which the children are shown. Instead of back-to-front, they're displayed front-to-back."
    e "La propriété de style 'order_reverse' change l’ordre dans lequel les éléments contenus sont affichés. Au lieu d’être affiché de l’arrière-plan vers l’avant-plan, ils sont affichés de l’avant vers l’arrière."

# game/indepth_style.rpy:1084
translate french style_inspector_21bc0709:

    # e "Sometimes it's hard to figure out what style is being used for a particular displayable. The displayable inspector can help with that."
    e "Parfois, il est difficile de savoir quel style est utilisé pour un élément en particulier. L’inspecteur d’élément affichable peut vous aider."

# game/indepth_style.rpy:1086
translate french style_inspector_243c50f0:

    # e "To use it, place the mouse over a portion of the Ren'Py user interface, and hit shift+I. That's I for inspector."
    e "Pour l’utiliser, placez votre souris sur l’élément affiché dont vous souhaitez obtenir les informations et pressez Maj+I. C’est I pour inspecteur."

# game/indepth_style.rpy:1088
translate french style_inspector_bcbdc396:

    # e "Ren'Py will pop up a list of displayables the mouse is over. Next to each is the name of the style that displayable uses."
    e "Ren’Py va vous présenter la liste d’éléments affichables qui se trouvaient sous la souris. Ensuite pour chacun des éléments, vous avez le nom du style qui s’applique."

# game/indepth_style.rpy:1090
translate french style_inspector_d981e5c8:

    # e "You can click on the name of the style to see where it gets its properties from."
    e "Vous pouvez cliquer sur un nom pour voir d’où il tient ses propriétés."

# game/indepth_style.rpy:1092
translate french style_inspector_ef46b86d:

    # e "By default, the inspector only shows interface elements like screens, and not images. Type shift+alt+I if you'd like to see images as well."
    e "Par défaut, l’inspecteur ne présente que les éléments d’interface comme les écrans, pas les images. Presser Maj+Alt+I si vous souhaitez aussi les styles des images."

# game/indepth_style.rpy:1094
translate french style_inspector_b59c6b69:

    # e "You can try the inspector right now, by hovering this text and hitting shift+I."
    e "Vous pouvez utiliser l’inspecteur dès maintenant, en laissant la souris au-dessus de ce texte et en pressant Maj+I."

translate french strings:

    # indepth_style.rpy:20
    old "Button 1"
    new "Bouton 1"

    # indepth_style.rpy:22
    old "Button 2"
    new "Bouton 2"

    # indepth_style.rpy:66
    old "Style basics."
    new "Style de base."

    # indepth_style.rpy:66
    old "General style properties."
    new "Propriétés générales des styles."

    # indepth_style.rpy:66
    old "Text style properties."
    new "Propriétés de style des textes."

    # indepth_style.rpy:66
    old "Window and Button style properties."
    new "Propriétés de style des fenêtres et des boutons."

    # indepth_style.rpy:66
    old "Bar style properties."
    new "Propriétés de style des barres."

    # indepth_style.rpy:66
    old "Box, Grid, and Fixed style properties."
    new "Propriétés de style des boîtes, des grilles et des éléments fixes."

    # indepth_style.rpy:66
    old "The Displayable Inspector."
    new "L’inspecteur d’affichage."

    # indepth_style.rpy:66
    old "That's all I want to know."
    new "C’est tout ce que je veux savoir."

    # indepth_style.rpy:112
    old "This text is colored green."
    new "Ce texte est coloré en vert."

    # indepth_style.rpy:126
    old "Danger"
    new "Danger"

    # indepth_style.rpy:142
    old "This text is colored red."
    new "Ce texte est coloré en rouge."

    # indepth_style.rpy:170
    old "This text is colored blue."
    new "Ce texte est coloré en bleu."

    # indepth_style.rpy:248
    old "Orbiting Earth in the spaceship, I saw how beautiful our planet is.\n–Yuri Gagarin"
    new "Dans mon vaisseau spatial en orbite autour de la Terre, j’ai vu combien notre planète est magnifique.\n-Yuri Gagarin"

    # indepth_style.rpy:303
    old "\"Orbiting Earth in the spaceship, I saw how beautiful our planet is.\" Said by Yuri Gagarin."
    new "\"Dans mon vaisseau spatial en orbite autour de la Terre, j’ai vu combien notre planète est magnifique.\" Prononcé par Yuri Gagarin."

    # indepth_style.rpy:326
    old "Vertical"
    new "Vertical"

    # indepth_style.rpy:329
    old "Far better it is to dare mighty things, to win glorious triumphs, even though checkered by failure, than to rank with those poor spirits who neither enjoy nor suffer much, because they live in the gray twilight that knows not victory nor defeat.\n\n–Theodore Roosevelt"
    new "Il vaut bien mieux oser des choses puissantes, remporter des triomphes glorieux, quoique damnés par l’échec, que de se ranger parmi ces pauvres esprits qui ne jouissent ni ne souffrent beaucoup, parce qu’ils vivent dans le crépuscule gris qui ne connaît ni victoire ni défaite.\n\n-Theodore Roosevelt"

    # indepth_style.rpy:561
    old "Top Choice"
    new "Choix du haut"

    # indepth_style.rpy:566
    old "Bottom Choice"
    new "Choix du bas"

    # indepth_style.rpy:879
    old "First Child"
    new "Premier enfant"

    # indepth_style.rpy:880
    old "Second Child"
    new "Deuxième enfant"

    # indepth_style.rpy:881
    old "Third Child"
    new "Troisième enfant"

    # indepth_style.rpy:884
    old "Fourth Child"
    new "Quatrième enfant"

    # indepth_style.rpy:885
    old "Fifth Child"
    new "Cinquième enfant"

    # indepth_style.rpy:886
    old "Sixth Child"
    new "Sixième enfant"
