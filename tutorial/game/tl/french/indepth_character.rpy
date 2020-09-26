
# game/indepth_character.rpy:11
translate french demo_character_e7e1b1bb:

    # e "We've already seen how to define a Character in Ren'Py. But I want to go into a bit more detail as to what a Character is."
    e "Nous avons déjà vu comment définir un personnage (Character) dans Ren’Py, mais je veux détailler un peu plus ce qu’est un Character."

# game/indepth_character.rpy:17
translate french demo_character_d7908a94:

    # e "Here are couple of additional characters."
    e "Voici quelques caractères additionnels."

# game/indepth_character.rpy:19
translate french demo_character_275ef8b9:

    # e "Each statement creates a Character object, and gives it a single argument, a name. If the name is None, no name is displayed."
    e "Chaque déclaration crée un objet Character et lui donne un nom comme argument. Si le nom est None, aucun nom n’est affiché."

# game/indepth_character.rpy:21
translate french demo_character_a63aea0c:

    # e "This can be followed by named arguments that set properties of the character. A named argument is a property name, an equals sign, and a value."
    e "Des arguments nommés peuvent suivre pour définir certaines propriétés du personnage. Un argument nommé est le nom de la propriété suivi d’un signe égal et de la valeur."

# game/indepth_character.rpy:23
translate french demo_character_636a502e:

    # e "Multiple arguments should be separated with commas, like they are here. Let's see those characters in action."
    e "Les arguments sont séparés par des virgules. Voyons ces personnages en action !"

# game/indepth_character.rpy:27
translate french demo_character_44b54e1d:

    # e_shout "I can shout!"
    e_shout "Je peux crier !"

# game/indepth_character.rpy:29
translate french demo_character_a9646dd8:

    # e_whisper "And I can speak in a whisper."
    e_whisper "Et je peux murmurer."

# game/indepth_character.rpy:31
translate french demo_character_79793208:

    # e "This example shows how the name Character is a bit of a misnomer. Here, we have multiple Characters in use, but you see it as me speaking."
    e "Cet exemple montre que les noms de personnages ne sont pas très appropriés. Ici, nous utilisons de multiples déclarations de personnages, mais vous voyez que c’est toujours moi qui parle."

# game/indepth_character.rpy:33
translate french demo_character_5d5d7482:

    # e "It's best to think of a Character as repesenting a name and style, rather than a single person."
    e "Il est préférable de penser qu’un 'Character' représente un nom et un style, plutôt qu’un seul personnage."

# game/indepth_character.rpy:37
translate french demo_character_66d08d98:

    # e "There are a lot of properties that can be given to Characters, most of them prefixed styles."
    e "Il y a beaucoup de propriétés qui peuvent être données aux personnages, la plupart sont préfixées."

# game/indepth_character.rpy:39
translate french demo_character_7e0d75aa:

    # e "Properties beginning with window apply to the textbox, those with what apply to the the dialogue, and those with who to the name of Character speaking."
    e "Les propriétés préfixées par 'window' concernent la zone de texte, celle avec 'what' concerne les dialogues et celles avec 'who' concerne l’affichage du nom du personnage."

# game/indepth_character.rpy:41
translate french demo_character_56703784:

    # e "If you leave a prefix out, the style customizes the name of the speaker."
    e "Si vous laissez un préfixe de côté, le style principal personnalise le nom de l’orateur."

# game/indepth_character.rpy:43
translate french demo_character_b456f0a9:

    # e "There are quite a few different properties that can be set this way. Here are some of the most useful."
    e "Il y a de nombreuses propriétés qui peuvent être initialisée de cette façon. Voici quelques unes des plus utiles."

translate french demo_character_31ace18e:

    # e1 "The window_background property sets the image that's used for the background of the textbox, which should be the same size as the default in gui/textbox.png."
    e1 "La propriété 'window_background' définit l’image qui sera utilisée en arrière plan de la zone de texte. Cette image doit avoir la même taille que celle par défaut (gui/textbox.png)."

# game/indepth_character.rpy:54
translate french demo_character_18ba073d:

    # e1a "If it's set to None, the textbox has no background window."
    e1a "Si vous la laissez à None, la zone de texte n’a pas d’arrière-plan."

# game/indepth_character.rpy:59
translate french demo_character_5a26445c:

    # e2 "The who_color and what_color properties set the color of the character's name and dialogue text, respectively."
    e2 "Les propriétés 'who_color' et 'what_color' définissent respectivement la couleur du nom du personnage et la couleur des dialogues."

# game/indepth_character.rpy:61
translate french demo_character_88a18c32:

    # e2 "The colors are strings containing rgb hex codes, the same sort of colors understood by a web browser."
    e2 "Les couleurs sont des chaînes de caractères contenant un code hexadécimal, c’est le même type de couleurs que celles comprises par un navigateur web."

# game/indepth_character.rpy:67
translate french demo_character_ed690751:

    # e3 "Similarly, the who_font and what_font properties set the font used by the different kinds of text."
    e3 "De la même façon, les propriétés 'who_font' et 'what_font' définissent la police des différents textes."

# game/indepth_character.rpy:74
translate french demo_character_8dfa6426:

    # e4 "Setting the who_bold, what_italic, and what_size properties makes the name bold, and the dialogue text italic at a size of 20 pixels."
    e4 "En personnalisant les propriétés 'who_bold', 'what_italic' et 'what_size' vous pouvez rendre le dialogue en gras, en italic avec une taille de 20 pixels, par exemple."

# game/indepth_character.rpy:76
translate french demo_character_20e83c32:

    # e4 "Of course, the what_bold, who_italic and who_size properties also exist, even if they're not used here."
    e4 "Bien sûr, les propriétés 'what_bold', 'who_italic' et 'who_size' existent également, même si elles ne sont pas utilisées ici."

# game/indepth_character.rpy:83
translate french demo_character_e4cbb1f2:

    # e5 "The what_outlines property puts an outline around the text."
    e5 "La propriété 'what_outlines' dessine une ligne autour des caractères du texte."

# game/indepth_character.rpy:85
translate french demo_character_71535ecf:

    # e5 "It's a little complicated since it takes a list with a tuple in it, with the tuple being four things in parenthesis, and the list the square brackets around them."
    e5 "Cette propriété est un peu plus compliquée à initialiser, car elle est constituée de tuple (une liste de quatre valeurs entre parenthèses) et est encadrée par des crochets."

# game/indepth_character.rpy:87
translate french demo_character_e9ac7482:

    # e5 "The first number is the size of the outline, in pixels. That's followed by a string giving the hex-code of the color of the outline, and the x and y offsets."
    e5 "Le premier nombre définit la taille de la bordure en pixel. Il est suivi par le code hexadécimal de la couleur de la bordure puis des décalages x et y (offsets en anglais)."

# game/indepth_character.rpy:93
translate french demo_character_ea72d988:

    # e6 "When the outline size is 0 and the offsets are given, what_outlines can also act as a drop-shadow behind the text."
    e6 "En initialisant la taille de la bordure à zéro et avec des décalages de quelques pixels, 'what_outlines' peut être utilisé pour projeter une ombre derrière le texte."

# game/indepth_character.rpy:99
translate french demo_character_8d35ebcd:

    # e7 "The what_xalign and what_textalign properties control the alignment of text, with 0.0 being left, 0.5 being center, and 1.0 being right."
    e7 "Les propriétés 'what_xalign' et 'what_textalign' contrôlent l’alignement du texte, avec 0.0 pour aligner à gauche, 0.5 pour centrer et 1.0 pour aligner à droite."

# game/indepth_character.rpy:101
translate french demo_character_7c75906c:

    # e7 "The what_xalign property controls where all the text itself is placed within the textbox, while what_textalign controls where rows of text are placed relative to each other."
    e7 "La propriété 'what_xalign' contrôle la position du texte en lui-même, tandis que la propriété 'what_textalign' contrôle l'alignement des lignes de textes les unes par rapport aux autres."

# game/indepth_character.rpy:103
translate french demo_character_e2811c1c:

    # e7 "Generally you'll want to to set them both what_xalign and what_textalign to the same value."
    e7 "Généralement, vous voudrez définir les deux propriétés 'what_xalign' et 'what_textalign' avec la même valeur."

# game/indepth_character.rpy:105
translate french demo_character_baa52234:

    # e7 "Setting what_layout to 'subtitle' puts Ren'Py in subtitle mode, which tries to even out the length of every line of text in a block."
    e7 "Initialiser 'what_layout' à 'subtitle' place Ren’Py en mode sous-titre, il tente alors de scinder le texte pour que chaque ligne ait la même longueur."

# game/indepth_character.rpy:110
translate french demo_character_41190f01:

    # e8 "These properties can be combined to achieve many different effects."
    e8 "Ces propriétés peuvent être combinées pour fournir différents effets."

# game/indepth_character.rpy:124
translate french demo_character_aa12d9ca:

    # e8 "This example hides the background and shows dialogue centered and outlined, as if the game is being subtitled."
    e8 "Cet exemple cache l’arrière-plan et affiche des dialogues centrés, entourés, comme si le jeu était sous-titré."

# game/indepth_character.rpy:133
translate french demo_character_a7f243e5:

    # e9 "There are two interesting non-style properties, what_prefix and what_suffix. These can put text at the start and end of a line of dialogue."
    e9 "Il y a également deux propriétés non stylistiques, 'what_prefix' et 'what_suffix'. Celles-ci permettent d’ajouter du texte au début ou à la fin du dialogue."

# game/indepth_character.rpy:139
translate french demo_character_f9b0052f:

    # e "By using kind, you can copy properties from one character to another, changing only what you need to."
    e "En utilisant 'kind', vous pouvez copier des propriétés d’un personnage à un autre, en changeant seulement ce qui est nécessaire."

# game/indepth_character.rpy:148
translate french demo_character_6dfce4b7:

    # l8 "Like this! Finally I get some more dialogue around here."
    l8 "Comme ceci! Finalement, j’obtiens un peu plus de dialogue par ici."

# game/indepth_character.rpy:157
translate french demo_character_68d9e46c:

    # e "The last thing you have to know is that there's a special character, narrator, that speaks narration. Got it?"
    e "La dernière chose à savoir, c’est qu’il existe des personnages spéciaux, comme le narrateur. Compris ?"

# game/indepth_character.rpy:159
translate french demo_character_0c8f314a:

    # "I think I do."
    "Je crois, oui."

