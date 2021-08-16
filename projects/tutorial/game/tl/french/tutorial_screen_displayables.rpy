
# game/tutorial_screen_displayables.rpy:3
translate french screen_displayables_7c897a6d:

    # e "There are quite a few screen displayables. Here, I'll tell you about some of the most important ones."
    e "Il y a quelques affichages d’écran différents. Ici, je vais vous parler des plus importants."

# game/tutorial_screen_displayables.rpy:9
translate french screen_displayables_menu_fef7b441:

    # e "What would you like to know about?" nointeract
    e "Que voulez-vous découvrir ?" nointeract

# game/tutorial_screen_displayables.rpy:49
translate french screen_displayable_properties_76c5639a:

    # e "There are a few properties that every screen language displayable shares. Here, I'll demonstrate them for you."
    e "Il y a quelques propriétés qui sont partagées par toutes les codes d’instruction des écrans. Ici nous allons vous les présenter."

# game/tutorial_screen_displayables.rpy:57
translate french screen_displayable_properties_527d4b4e:

    # e "First off, every screen language displayable supports the position properties. When the container a displayable is in supports it, you can use properties like align, anchor, pos, and so so on."
    e "Tout d’abord, chaque code d’instruction des écrans supporte les propriétés de position. Quand un conteneur dans lequel se trouve un élément affichable le supporte, vous pouvez utiliser les propriétés telles que 'align', 'anchor', 'pos', etc.."

# game/tutorial_screen_displayables.rpy:69
translate french screen_displayable_properties_8aff26dd:

    # e "The at property applies a transform to the displayable, the same way the at clause in the show statement does."
    e "La propriété 'at' applique une transformation à l’élément affichable de la même façon que la clause 'at' le fait pour les déclarations 'show'."

# game/tutorial_screen_displayables.rpy:106
translate french screen_displayable_properties_2ed40a70:

    # e "The id property is mostly used with the say screen, which is used to show dialogue. Outside of the say screen, it isn't used much."
    e "La propriété 'id' est particulièrement utilisée avec l’écran 'say' qui affiche les dialogues. Hors de l’écran 'say', cette instruction n’est pas beaucoup utilisée."

# game/tutorial_screen_displayables.rpy:108
translate french screen_displayable_properties_da5733d1:

    # e "It tells Ren'Py which displayables are the background window, 'who' is speaking, and 'what' is being said. This used to apply per-Character styles, and help with auto-forward mode."
    e "Elle indique à Ren’Py quel élément d'affichage utiliser pour la fenêtre, 'who' correspond à qui est en train de parler et 'what' correspond à ce qui est dit. C’est utilisé pour appliquer des styles par personnage et cela aide avec le mode 'avance rapide'."

# game/tutorial_screen_displayables.rpy:123
translate french screen_displayable_properties_cc09fade:

    # e "The style property lets you specify the style of a single displayable."
    e "La propriété 'style' vous laisse spécifier le style de ce seul élément affichable."

# game/tutorial_screen_displayables.rpy:144
translate french screen_displayable_properties_a7f4e25c:

    # e "The style_prefix property sets the prefix of the style that's used for a displayable and its children."
    e "La propriété 'style_prefixe' définit le préfixe du style qui est utilisé pour l’élément affichable et ses enfants."

# game/tutorial_screen_displayables.rpy:146
translate french screen_displayable_properties_6bdb0723:

    # e "For example, when the style_prefix property is 'green', the vbox has the 'green_vbox' style, and the text in it has the 'green_text' style."
    e "Par exemple, quand la propriété 'style_prefixe' vaut 'green', la 'vbox' a le style 'green_vbox' et le texte inclus a le style 'green_text'."

# game/tutorial_screen_displayables.rpy:150
translate french screen_displayable_properties_8a3a8635:

    # e "There are a few more properties than these, and you can find the rest in the documentation. But these are the ones you can expect to see in your game, in the default screens."
    e "Il y a d’autres propriétés que celles-ci et vous pourrez trouver leur description dans la documentation, mais celles-ci sont celles que vous risquez de voir dans votre jeu, dans les écrans par défaut."

# game/tutorial_screen_displayables.rpy:156
translate french add_displayable_ec121c5c:

    # e "Sometimes you'll have a displayable, like an image, that you want to add to a screen."
    e "Parfois, vous aurez un élément affichable, comme une image que vous voudrez ajouter à l’écran."

# game/tutorial_screen_displayables.rpy:165
translate french add_displayable_7ec3e2b0:

    # e "This can be done using the add statement, which adds an image or other displayable to the screen."
    e "Cela peut être fait en utilisant la déclaration 'add' qui ajoute une image ou n’importe quel autre élément à l’écran."

# game/tutorial_screen_displayables.rpy:167
translate french add_displayable_7112a377:

    # e "There are a few ways to refer to the image. If it's in the images directory or defined with the image statement, you can just put the name inside a quoted string."
    e "Il y a plusieurs façons de faire référence à une image. S’il s’agit d’une image du répertoire 'images' ou d’une image définie avec la déclaration 'image', alors vous avez juste à placer son nom dans une chaîne de caractères."

# game/tutorial_screen_displayables.rpy:176
translate french add_displayable_8ba81c26:

    # e "An image can also be referred to by it's filename, relative to the game directory."
    e "Une image peut aussi être référencée par son nom de fichier, relativement au répertoire du jeu."

# game/tutorial_screen_displayables.rpy:185
translate french add_displayable_1f5571e3:

    # e "Other displayables can also be added using the add statement. Here, we add the Solid displayable, showing a solid block of color."
    e "Les autres éléments affichables peuvent aussi être ajoutés en utilisant la déclaration 'add'. Ici, nous avons ajouté un élément Solid montrant un bloc de couleur."

# game/tutorial_screen_displayables.rpy:195
translate french add_displayable_0213ffa2:

    # e "In addition to the displayable, the add statement can be given transform properties. These can place or otherwise transform the displayable being added."
    e "En plus des éléments affichables, la déclaration 'add' peut être utilisée pour donner des propriétés de transformation. Celles-ci peuvent placer ou transformer l’élément affichable qui vient d’être ajouté."

# game/tutorial_screen_displayables.rpy:207
translate french add_displayable_3a56a464:

    # e "Of course, the add statement can also take the at property, letting you give it a more complex transform."
    e "Bien sûr, la déclaration 'add' peut aussi prendre la propriété 'at' pour vous permettre des transformations plus complexes."

# game/tutorial_screen_displayables.rpy:222
translate french text_displayable_96f88225:

    # e "The screen language text statement adds a text displayable to the screen. It takes one argument, the text to be displayed."
    e "L’instruction 'text' des déclarations 'screen' ajoute un texte à l’écran. Il prend un argument, le texte à afficher."

# game/tutorial_screen_displayables.rpy:224
translate french text_displayable_1ed1a8c2:

    # e "In addition to the common properties that all displayables take, text takes the text style properties. For example, size sets the size of the text."
    e "En plus des propriétés communes que les éléments affichables peuvent prendre, 'text' peut recevoir des propriétés de style dédiées aux éléments de texte. Par exemple, 'size' définit la taille du texte."

# game/tutorial_screen_displayables.rpy:234
translate french text_displayable_9351d9dd:

    # e "The text displayable can also interpolate values enclosed in square brackets."
    e "L’élément de texte peut aussi interpoler des variables encadrées par des crochets."

# game/tutorial_screen_displayables.rpy:236
translate french text_displayable_32d76ccb:

    # e "When text is displayed in a screen using the text statement variables defined in the screen take precedence over those defined outside it."
    e "Quand le texte est affiché à l’écran en utilisant une déclaration 'text', les variables définies à l’intérieur de ce bloc de code prennent l’ascendant sur celles définies en dehors."

# game/tutorial_screen_displayables.rpy:238
translate french text_displayable_7e84a5d1:

    # e "Those variables may be parameters given to the screen, defined with the default or python statements, or set using the SetScreenVariable action."
    e "Ces variables peuvent être des paramètres transmis à l’écran, définis avec les déclaration 'default' ou 'python' ou encore initialisés en utilisant l’action 'SetScreenVariable'."

# game/tutorial_screen_displayables.rpy:247
translate french text_displayable_8bc866c4:

    # e "There's not much more to say about text in screens, as it works the same way as all other text in Ren'Py."
    e "Il n’y a pas beaucoup plus à dire à propos des textes dans les écrans, car ils fonctionnent de la même façon que les textes dans Ren’Py."

# game/tutorial_screen_displayables.rpy:255
translate french layout_displayables_d75efbae:

    # e "The layout displayables take other displayables and lay them out on the screen."
    e "Les canvas affichables peuvent prendre d’autres éléments affichables et les placer à l’écran."

# game/tutorial_screen_displayables.rpy:269
translate french layout_displayables_9a15144d:

    # e "For example, the hbox displayable takes its children and lays them out horizontally."
    e "Par exemple, l’élément hbox (boite horizontale) prend tous ses enfants (les éléments qu’il contient) et les dispose horizontalement."

# game/tutorial_screen_displayables.rpy:284
translate french layout_displayables_48eff197:

    # e "The vbox displayable is similar, except it takes its children and arranges them vertically."
    e "L’élément 'vbox' est similaire, si ce n’est qu’il dispose les éléments qu’il contient et les arrange verticalement."

# game/tutorial_screen_displayables.rpy:286
translate french layout_displayables_74de8a66:

    # e "Both of the boxes take the box style properties, the most useful of which is spacing, the amount of space to leave between children."
    e "Ces deux boîtes peuvent recevoir des propriétés de style, la plus utile est 'spacing', la quantité d’espace qui sépare les éléments contenus."

# game/tutorial_screen_displayables.rpy:301
translate french layout_displayables_a156591f:

    # e "The grid displayable displays its children in a grid of equally-sized cells. It takes two arguments, the number of columns and the number of rows."
    e "L’élément 'grid' affiche ses éléments dans une grille de cellules de même taille. Il reçoit deux arguments, le nombre de colonnes et le nombre de lignes."

# game/tutorial_screen_displayables.rpy:303
translate french layout_displayables_126f5816:

    # e "The grid has to be full, or Ren'Py will produce an error. Notice how in this example, the empty cell is filled with a null."
    e "La grille doit être remplie ou Ren’Py va produire une erreur. Notez comme dans cet exemple, les cellules vides sont remplies avec un 'null'."

# game/tutorial_screen_displayables.rpy:305
translate french layout_displayables_bfaaaf9b:

    # e "Like the boxes, grid uses the spacing property to specify the space between cells."
    e "Comme les boites, les grilles utilisent la propriété 'spacing' pour définir l’espacement entre les cellules."

# game/tutorial_screen_displayables.rpy:321
translate french layout_displayables_3e931106:

    # e "Grid also takes the transpose property, to make it fill top-to-bottom before it fills left-to-right."
    e "'grid' prend aussi la propriété 'transpose', pour qu’elle se remplisse d’abord du haut vers le bas avant de se remplir de gauche à droite."

# game/tutorial_screen_displayables.rpy:338
translate french layout_displayables_afdc1b11:

    # e "And just to demonstrate that all cells are equally-sized, here's what happens when once child is bigger than the others."
    e "Et juste pour démontrer que les cellules sont toutes de même taille, voici ce qui se passe quand un des contenus est plus grand que les autres."

# game/tutorial_screen_displayables.rpy:353
translate french layout_displayables_a23e2826:

    # e "The fixed displayable displays the children using Ren'Py's normal placement algorithm. This lets you place displayables anywhere in the screen."
    e "L’élément 'fixed' affiche ses enfants en utilisant l’algorithme standard de placement de Ren’Py. Cela vous permet d’afficher les éléments n’importe où à l’écran."

# game/tutorial_screen_displayables.rpy:355
translate french layout_displayables_fd3926ca:

    # e "By default, the layout expands to fill all the space available to it. To prevent that, we use the xsize and ysize properties to set its size in advance."
    e "Par défaut, le canvas 'layout' s’étend pour remplir tout l’espace disponible. Pour prévenir cela, vous pouvez définir les propriétés 'xsize' et 'ysize' à l’avance."

# game/tutorial_screen_displayables.rpy:369
translate french layout_displayables_eff42786:

    # e "When a non-layout displayable is given two or more children, it's not necessary to create a fixed. A fixed is automatically added, and the children are added to it."
    e "Quand un élément qui n’est pas un canvas a un ou deux enfants, alors il n’est pas nécessaire de créer un élément 'fixed'. Un élément 'fixed' est en effet automatiquement créé et les enfants sont ajoutés en son sein."

# game/tutorial_screen_displayables.rpy:384
translate french layout_displayables_c32324a7:

    # e "Finally, there's one convenience to save space. When many displayables are nested, adding a layout to each could cause crazy indent levels."
    e "Finalement, il y a une astuce pour préserver l’indentation dans le code. Quand de nombreux éléments affichables sont imbriqués, ajouter un canvas à chacun peut entraîner des indentations importantes voire illisibles."

# game/tutorial_screen_displayables.rpy:386
translate french layout_displayables_d7fa0f28:

    # e "The has statement creates a layout, and then adds all further children of its parent to that layout. It's just a convenience to make screens more readable."
    e "La déclaration 'has' crée un canvas et ajoute ensuite tous les enfants de son parent au canvas. C’est juste une astuce pour rendre les écrans plus lisible."

# game/tutorial_screen_displayables.rpy:395
translate french window_displayables_14beb786:

    # e "In the default GUI that Ren'Py creates for a game, most user interface elements expect some sort of background."
    e "Dans l’interface par défaut que Ren’Py crée pour le jeu, la plupart des éléments de l’interface attendent une sorte d’arrière-plan."

# game/tutorial_screen_displayables.rpy:405
translate french window_displayables_495d332b:

    # e "Without the background, text can be hard to read. While a frame isn't strictly required, many screens have one or more of them."
    e "Sans cet arrière-plan, le texte peut être difficile à lire. Comme la 'frame' n’est pas strictement requise, de nombreux écrans en ont un ou plusieurs."

# game/tutorial_screen_displayables.rpy:417
translate french window_displayables_2c0565ab:

    # e "But when I add a background, it's much easier. That's why there are two displayables that are intended to give backgrounds to user interface elements."
    e "Mais quand j’ajoute un arrière plan, c’est beaucoup plus facile. C’est pourquoi deux éléments affichables sont destinés pour fournir des arrière-plans aux éléments de l’interface utilisateur."

# game/tutorial_screen_displayables.rpy:419
translate french window_displayables_c7d0968c:

    # e "The two displayables are frame and window. Frame is the one we use above, and it's designed to provide a background for arbitrary parts of the user interface."
    e "Ces deux éléments sont 'frame' et 'window'. 'Frame' est celle que nous utilisons ci-dessus et elle est conçue pour fournir un arrière-plan pour les parties arbitraires de l’interface utilisateur."

# game/tutorial_screen_displayables.rpy:423
translate french window_displayables_7d843f62:

    # e "On the other hand, the window displayable is very specific. It's used to provide the text window. If you're reading what I'm saying, you're looking at the text window right now."
    e "De l’autre côté, l’élément 'window' est très spécifique. Il est utilisé pour fournir une fenêtre de texte. Si vous lisez ce que je dis, vous être en train de regarder le texte d’une fenêtre en ce moment-même."

# game/tutorial_screen_displayables.rpy:425
translate french window_displayables_de5963e4:

    # e "Both frames and windows can be given window style properties, allowing you to change things like the background, margins, and padding around the window."
    e "'window' et 'frame' acceptent les propriétés de style, ce qui vous autorise à changer l’arrière-plan, les marges, les espacements internes."

# game/tutorial_screen_displayables.rpy:433
translate french button_displayables_ea626553:

    # e "One of the most flexible displayables is the button displayable, and its textbutton and imagebutton variants."
    e "L’un des éléments affichables les plus flexibles est l’élément 'button' et ses variantes 'textbutton' et 'imagebutton'."

# game/tutorial_screen_displayables.rpy:443
translate french button_displayables_372dcc0f:

    # e "A button is a displayable that when selected runs an action. Buttons can be selected by clicking with the mouse, by touch, or with the keyboard and controller."
    e "Un bouton est un élément affichable qui exécute des actions quand il est sélectionné. Un bouton peut être sélectionné en cliquant avec la souris, en le touchant ou via les touches du clavier ou de la manette."

# game/tutorial_screen_displayables.rpy:445
translate french button_displayables_a6b270ff:

    # e "Actions can do many things, like setting variables, showing screens, jumping to a label, or returning a value. There are many {a=https://www.renpy.org/doc/html/screen_actions.html}actions in the Ren'Py documentation{/a}, and you can also write your own."
    e "Les actions peuvent faire beaucoup de choses, comme initialiser des variables, afficher des écrans, sauter à un label ou retourner une valeur. Il y a beaucoup {a=https://www.renpy.org/doc/html/screen_actions.html}d’actions dans la documentation Ren’Py{/a} et nous vous laissons écrire les vôtres."

# game/tutorial_screen_displayables.rpy:458
translate french button_displayables_4c600d20:

    # e "It's also possible to run actions when a button gains and loses focus."
    e "Il est également possible d’exécuter des actions quand un bouton gagne ou perd le focus."

# game/tutorial_screen_displayables.rpy:473
translate french button_displayables_47af4bb9:

    # e "A button takes another displayable as children. Since that child can be a layout, it can takes as many children as you want."
    e "Un bouton peut prendre un autre élément affichable comme enfant. Comme cet enfant peut être un canvas (layout), il peut donc prendre autant d’enfants que vous le souhaitez."

# game/tutorial_screen_displayables.rpy:483
translate french button_displayables_d01adde3:

    # e "In many cases, buttons will be given text. To make that easier, there's the textbutton displayable that takes the text as an argument."
    e "Dans beaucoup de cas, les boutons contiendront un élément 'text', pour rendre cela plus facile, il y a l’élément 'textbutton' qui prend un texte en argument."

# game/tutorial_screen_displayables.rpy:485
translate french button_displayables_01c551b3:

    # e "Since the textbutton displayable manages the style of the button text for you, it's the kind of button that's used most often in the default GUI."
    e "Comme l’élément 'textbutton' gère le style du bouton pour vous, c’est le type de bouton le plus souvent utilisé dans la GUI par défaut."

# game/tutorial_screen_displayables.rpy:498
translate french button_displayables_6911fb9b:

    # e "There's also the imagebutton, which takes displayables, one for each state the button can be in, and displays them as the button."
    e "Il y a également l’élément 'imagebutton' qui prend plusieurs éléments affichables, un pour chacun des états possibles du bouton et il les affiche comme un bouton."

# game/tutorial_screen_displayables.rpy:500
translate french button_displayables_49720fa6:

    # e "An imagebutton gives you the most control over what a button looks like, but is harder to translate and won't look as good if the game window is resized."
    e "Un 'imagebutton' vous donne le plus de contrôle sur le look que peut avoir un bouton, mais il est plus compliqué à traduire et il ne donnera pas un aussi bon rendu si la fenêtre du jeu est redimensionnée."

# game/tutorial_screen_displayables.rpy:522
translate french button_displayables_e8d40fc8:

    # e "Buttons take Window style properties, that are used to specify the background, margins, and padding. They also take Button-specific properties, like a sound to play on hover."
    e "Les boutons prennent les propriétés de style de 'window', celles qui sont utilisées pour définir l’arrière-plan, les marges et les espacements. "

# game/tutorial_screen_displayables.rpy:524
translate french button_displayables_1e40e311:

    # e "When used with a button, style properties can be given prefixes like idle and hover to make the property change with the button state."
    e "Quand elles sont utilisées avec un bouton, les propriétés de styles peuvent avoir des préfixes comme 'idle' et 'hover' qui change la propriété en fonction de l’état du bouton."

# game/tutorial_screen_displayables.rpy:526
translate french button_displayables_220b020d:

    # e "A text button also takes Text style properties, prefixed with text. These are applied to the text displayable it creates internally."
    e "Un bouton de texte peut également recevoir les propriétés de style de Text, styles préfixés par 'text'. Elles sont appliquées à l’élément 'text' qui est créé en interne."

# game/tutorial_screen_displayables.rpy:558
translate french button_displayables_b89d12aa:

    # e "Of course, it's prety rare we'd ever customize a button in a screen like that. Instead, we'd create custom styles and tell Ren'Py to use them."
    e "Bien sûr, il est particulièrement rare de personnaliser un bouton de cette façon là. À la place, on va plutôt créer un style personnalisé et dire à Ren’Py de l’utiliser."

# game/tutorial_screen_displayables.rpy:577
translate french bar_displayables_946746c2:

    # e "The bar and vbar displayables are flexible displayables that show bars representing a value. The value can be static, animated, or adjustable by the player."
    e "Les éléments 'bar' et 'vbar' sont des éléments affichables flexibles qui affichent des barres représentant une valeur. La valeur peut être statique, animée ou ajustée par le joueur."

# game/tutorial_screen_displayables.rpy:579
translate french bar_displayables_af3a51b8:

    # e "The value property gives a BarValue, which is an object that determines the bar's value and range. Here, a StaticValue sets the range to 100 and the value to 66, making a bar that's two thirds full."
    e "La propriété 'value' fournit à 'BarValue' un objet qui détermine la valeur de la barre et sa portée. Ici, une 'StaticValue' définit la portée à 100 et la valeur à 66, faisant que la barre est remplie au deux tiers."

# game/tutorial_screen_displayables.rpy:581
translate french bar_displayables_62f8b0ab:

    # e "A list of all the BarValues that can be used is found {a=https://www.renpy.org/doc/html/screen_actions.html#bar-values}in the Ren'Py documentation{/a}."
    e "Une liste de toutes les 'BarValue' utilisables est décrite {a=https://www.renpy.org/doc/html/screen_actions.html#bar-values}dans la documentation Ren’Py{/a}."

# game/tutorial_screen_displayables.rpy:583
translate french bar_displayables_5212eb0a:

    # e "In this example, we give the frame the xsize property. If we didn't do that, the bar would expand to fill all available horizontal space."
    e "Dans cet exemple, nous donnons au cadre la propriété 'xsize'. Si nous ne le faisions pas, la barre s’étendrait pour occuper tout l’espace horizontal disponible."

# game/tutorial_screen_displayables.rpy:600
translate french bar_displayables_67295018:

    # e "There are a few different bar styles that are defined in the default GUI. The styles are selected by the style property, with the default selected by the value."
    e "Dans l’interface graphique par défaut, il y a déjà quelques styles de barres différents. Elles sont sélectionnées en fonction de la propriété 'style'."

# game/tutorial_screen_displayables.rpy:602
translate french bar_displayables_1b037b21:

    # e "The top style is the 'bar' style. It's used to display values that the player can't adjust, like a life or progress bar."
    e "Le style utilisé en haut est le style 'bar'. Il est utilisé pour afficher des valeurs que le joueur ne peut pas ajuster, comme ses points de vie ou une barre de progression."

# game/tutorial_screen_displayables.rpy:604
translate french bar_displayables_c2aa4725:

    # e "The middle stye is the 'slider' value. It's used for values the player is expected to adjust, like a volume preference."
    e "Au milieu, la propriété 'style' est à 'slider' (curseur en français). Elle est utilisée pour les valeurs que le joueur est censé ajuster, comme ses préférences de volume."

# game/tutorial_screen_displayables.rpy:606
translate french bar_displayables_2fc44226:

    # e "Finally, the bottom style is the 'scrollbar' style, which is used for horizontal scrollbars. When used as a scrollbar, the thumb in the center changes size to reflect the visible area of a viewport."
    e "Enfin, en bas, la propriété 'style' vaut 'scrollbar', elle est utilisée pour les ascenseurs horizontaux. Quand la barre est utilisée comme ascenseur, le centre de l’image change de taille pour refléter la partie visible par rapport à la taille réelle."

# game/tutorial_screen_displayables.rpy:623
translate french bar_displayables_26eb88bf:

    # e "The vbar displayable is similar to the bar displayable, except it uses vertical styles - 'vbar', 'vslider', and 'vscrollbar' - by default."
    e "L’élément 'vbar' est similaire à l’élément 'bar', si ce n’est que, par défaut, il utilise des styles verticaux — 'vbar', 'vslider' et 'vscrollbar'."

# game/tutorial_screen_displayables.rpy:626
translate french bar_displayables_11cf8af2:

    # e "Bars take the Bar style properties, which can customize the look and feel greatly. Just look at the difference between the bar, slider, and scrollbar styles."
    e "Les barres prennent les propriétés de style 'Bar' qui permettent de bien personnaliser le look et le rendu. Regardez la différence de style avec ces barres, curseurs et ascenseurs."

# game/tutorial_screen_displayables.rpy:635
translate french imagemap_displayables_d62fad02:

    # e "Imagemaps use two or more images to show buttons and bars. Let me start by showing you an example of an imagemap in action."
    e "Les 'Imagemaps' (qu’on pourrait traduire par cartes d’images ou des images servant de carte en français) utilise une ou plusieurs images pour montrer des boutons et des barres. Laissez-moi commencer en vous montrant une 'imagemap' en action."

# game/tutorial_screen_displayables.rpy:657
translate french swimming_405542a5:

    # e "You chose swimming."
    e "Vous avez choisi 'swimming' (nager)."

# game/tutorial_screen_displayables.rpy:659
translate french swimming_264b5873:

    # e "Swimming seems like a lot of fun, but I didn't bring my bathing suit with me."
    e "La natation semble être amusante, mais je n’ai pas pris mon maillot de bain avec moi."

# game/tutorial_screen_displayables.rpy:665
translate french science_83e5c0cc:

    # e "You chose science."
    e "Vous avez choisi 'science'."

# game/tutorial_screen_displayables.rpy:667
translate french science_319cdf4b:

    # e "I've heard that some schools have a competitive science team, but to me research is something that can't be rushed."
    e "J’ai entendu dire que certaines écoles ont des équipes scientifiques de compétition, mais, pour moi, rechercher ne peut pas être quelque chose qu’on précipite."

# game/tutorial_screen_displayables.rpy:672
translate french art_d2a94440:

    # e "You chose art."
    e "Vous avez choisi 'art'."

# game/tutorial_screen_displayables.rpy:674
translate french art_e6af6f1d:

    # e "Really good background art is hard to make, which is why so many games use filtered photographs. Maybe you can change that."
    e "Un très bon arrière-plan est très difficile à faire, c’est pourquoi beaucoup de jeux utilisent des photographies filtrées, mais peut-être que vous pouvez changer cela."

# game/tutorial_screen_displayables.rpy:680
translate french home_373ea9a5:

    # e "You chose to go home."
    e "Vous avez choisi de rentrer à la maison 'home'."

# game/tutorial_screen_displayables.rpy:686
translate french imagemap_done_48eca0a4:

    # e "Anyway..."
    e "Enfin, bref…"

# game/tutorial_screen_displayables.rpy:691
translate french imagemap_done_a60635a1:

    # e "To demonstrate how imagemaps are put together, I'll show you the five images that make up a smaller imagemap."
    e "Pour montrer comment les cartes sont assemblées, je vais vous montrer les cinq images qui ont permis de construire cette carte."

# game/tutorial_screen_displayables.rpy:697
translate french imagemap_done_ac9631ef:

    # e "The idle image is used for the background of the imagemap, for hotspot buttons that aren't focused or selected, and for the empty part of an unfocused bar."
    e "L’image 'idle' est utilisée pour l’arrière plan de la carte 'imagemap' quand les boutons et la zone vide de la barre ne sont ni sélectionnés ou survolés."

# game/tutorial_screen_displayables.rpy:703
translate french imagemap_done_123b5924:

    # e "The hover image is used for hotspots that are focused but not selected, and for the empty part of a focused bar."
    e "L’image 'hover' est utilisée dès que ces zones sensibles sont survolées, mais pas sélectionnées."

# game/tutorial_screen_displayables.rpy:705
translate french imagemap_done_37f538dc:

    # e "Notice how both the bar and button are highlighted in this image. When we display them as part of a screen, only one of them will show up as focused."
    e "Remarquez comment la barre et le bouton sont tous les deux illuminés dans cette image. Comme nous affichons que leur partie propre à l’écran, seule la zone survolée changera de couleur."

# game/tutorial_screen_displayables.rpy:711
translate french imagemap_done_c76b072d:

    # e "Selected images like this selected_idle image are used for parts of the bar that are filled, and for selected buttons, like the current screen and a checked checkbox."
    e "Pour les images sélectionnées cette fois, c’est l’image déclarée dans 'selected_idle' qui est utilisée pour montrer la partie remplie de la barre et quand le bouton est sélectionné, comme pour l’écran actuel et la case à cocher."

# game/tutorial_screen_displayables.rpy:717
translate french imagemap_done_241a4112:

    # e "Here's the selected_hover image. The button here will never be shown, since it will never be marked as selected."
    e "Ici nous avons l’image 'selected_hover'. Le bouton ici ne sera jamais montré, car il ne sera jamais marqué comme sélectionné."

# game/tutorial_screen_displayables.rpy:723
translate french imagemap_done_3d8f454c:

    # e "Finally, an insensitive image can be given, which is used when a hotspot can't be interacted with."
    e "Enfin, une image 'insensitive' peut être donnée, elle est utilisée quand une zone habituellement sensible ne peut pas interagir."

# game/tutorial_screen_displayables.rpy:728
translate french imagemap_done_ca286729:

    # e "Imagemaps aren't limited to just images. Any displayable can be used where an image is expected."
    e "Les cartes ne se limitent pas à des images. N’importe quel élément affichable peut être utilisé là où une image est habituellement attendue."

# game/tutorial_screen_displayables.rpy:743
translate french imagemap_done_6060b17f:

    # e "Here's an imagemap built using those five images. Now that it's an imagemap, you can interact with it if you want to."
    e "Voici une carte qui a été construite à partie de ces cinq images. Maintenant que c’est une 'imagemap', vous pouvez interagir avec elle si vous voulez."

# game/tutorial_screen_displayables.rpy:755
translate french imagemap_done_c817794d:

    # e "To make this a little more concise, we can replace the five images with the auto property, which replaces '%%s' with 'idle', 'hover', 'selected_idle', 'selected_hover', or 'insensitive' as appropriate."
    e "Pour rendre ce code un peu plus concis, nous pouvons remplacer les cinq images avec la propriété 'auto' qui remplace '%%s' par 'idle', 'hover', 'selected_idle', 'selected_hover' ou 'insensitive' en fonction de l’état courant."

# game/tutorial_screen_displayables.rpy:757
translate french imagemap_done_c1ed91b8:

    # e "Feel free to omit the selected and insensitive images if your game doesn't need them. Ren'Py will use the idle or hover images to replace them."
    e "N’hésitez pas à omettre les images 'selected' et 'insensitive' si vous jeu n’en a pas besoin. Ren’Py utilise les images 'idle' ou 'hover' pour les remplacer."

# game/tutorial_screen_displayables.rpy:759
translate french imagemap_done_166f75db:

    # e "The hotspot and hotbar statements describe areas of the imagemap that should act as buttons or bars, respectively."
    e "Les déclarations 'hotspot' et 'hotbar' décrivent des aires des 'imagemaps' qui peuvent interagir respectivement comme des boutons ou des barres."

# game/tutorial_screen_displayables.rpy:761
translate french imagemap_done_becb9688:

    # e "Both take the coordinates of the area, in (x, y, width, height) format."
    e "Les deux prennent en argument les coordonnées des aires, au format (x, y, hauteur, largeur)."

# game/tutorial_screen_displayables.rpy:763
translate french imagemap_done_fd56baa2:

    # e "A hotspot takes an action that is run when the hotspot is activated. It can also take actions that are run when it's hovered and unhovered, just like a button can."
    e "Un 'hotspot' prend aussi une 'action' qui est exécutée quand la zone sensible est activée. Il peut également recevoir des actions qui sont utilisées quand la zone est survolée ou n’est plus survolée, exactement comme un bouton peut l’être."

# game/tutorial_screen_displayables.rpy:765
translate french imagemap_done_5660a6a2:

    # e "A hotbar takes a BarValue object that describes how full the bar is, and the range of values the bar should display, just like a bar and vbar does."
    e "Une 'hotbar' prend en argument un objet 'BarValue' qui décrit de combien la jauge est remplie et la portée des valeurs qui peuvent apparaitre, un peu comme une 'bar' ou une 'vbar' le font."

# game/tutorial_screen_displayables.rpy:772
translate french imagemap_done_10496a29:

    # e "A useful pattern is to define a screen with an imagemap that has hotspots that jump to labels, and call that using the call screen statement."
    e "Voici un modèle utile : définir un écran qu’on affiche avec la déclaration 'call screen' et y placer une 'imagemap' dont les 'hotspots' sautent vers des labels."

# game/tutorial_screen_displayables.rpy:774
translate french imagemap_done_dcb45224:

    # e "That's what we did in the school example I showed before. Here's the script for it. It's long, but the imagemap itself is fairly simple."
    e "C’est exactement ce que nous avions fait tout à l’heure grâce à cet exemple avec l’école. Voici le script utilisé. C’est long, mais la déclaration de la carte est particulièrement simple."

# game/tutorial_screen_displayables.rpy:778
translate french imagemap_done_5b5bc5e5:

    # e "Imagemaps have pluses and minuses. On one hand, they are easy for a designer to create, and can look very good. At the same time, they can be hard to translate, and text baked into images may be blurry when the window is scaled."
    e "Les cartes d’images ont des avantages et des inconvénients. Pour le designer, elles sont très simple à créer et peuvent avoir un très beau look, mais d’un autre côté, elles sont complexes à traduire et le texte dans les images peut être flou quand elles sont réduites."

# game/tutorial_screen_displayables.rpy:780
translate french imagemap_done_b6cebf2b:

    # e "It's up to you and your team to decide if imagemaps are right for your project."
    e "C’est à vous et à votre équipe de décider si les 'imagemap' sont intéressantes ou non pour votre projet."

# game/tutorial_screen_displayables.rpy:787
translate french viewport_displayables_e509d50d:

    # e "Sometimes, you'll want to display something bigger than the screen. That's what the viewport displayable is for."
    e "Parfois, vous souhaitez afficher quelque chose de plus grand que l’écran. C’est à cela que l’élément 'viewport' est destiné. (NDLT : Il est difficile de traduire 'viewport', c’est un hublot par lequel on regarde en quelque sorte)."

# game/tutorial_screen_displayables.rpy:803
translate french viewport_displayables_9853b0e3:

    # e "Here's an example of a simple viewport, used to display a single image that's far bigger than the screen. Since the viewport will expand to the size of the screen, we use the xysize property to make it smaller."
    e "Voici un exemple simple de 'viewport', utilisé pour afficher une simple image qui est bien plus grande que notre écran. Comme le 'viewport' va s’étendre à la taille de l’écran, nous utilisons ici la propriété 'xysize' pour rétrécir le hublot."

# game/tutorial_screen_displayables.rpy:805
translate french viewport_displayables_778668c8:

    # e "By default the viewport can't be moved, so we give the draggable, mousewheel, and arrowkeys properties to allow it to be moved in multiple ways."
    e "Par défaut, le 'viewport' ne peut pas être déplacé, alors nous allons renseigner les propriétés 'draggable', 'mousewheel' et 'arrowkeys' pour autoriser son déplacement dans de nombreuses directions."

# game/tutorial_screen_displayables.rpy:820
translate french viewport_displayables_bbd63377:

    # e "When I give the viewport the edgescroll property, the viewport automatically scrolls when the mouse is near its edges. The two numbers are the size of the edges, and the speed in pixels per second."
    e "Quand je renseigne la propriété 'edgescroll' du 'viewport', le 'viewport' va automatiquement défiler quand la souris sera proche des angles. Les deux nombres indiquent la taille des angles et la vitesse de déplacement en pixels par seconde."

# game/tutorial_screen_displayables.rpy:839
translate french viewport_displayables_7c4678ee:

    # e "Giving the viewport the scrollbars property surrounds it with scrollbars. The scrollbars property can take 'both', 'horizontal', and 'vertical' as values."
    e "Quand je renseigne la propriété 'scrollbars', des ascenseurs apparaissent. La propriété 'scrollbars' peut prendre comme valeur 'both', 'horizontal' et 'vertical'."

# game/tutorial_screen_displayables.rpy:841
translate french viewport_displayables_197953b5:

    # e "The spacing property controls the space between the viewport and its scrollbars, in pixels."
    e "La propriété 'spacing' gère l’espacement en pixels entre le hublot et les ascenseurs."

# game/tutorial_screen_displayables.rpy:864
translate french viewport_displayables_54dd6e7b:

    # e "The xinitial and yinitial properties set the initial amount of scrolling, as a fraction of the amount that can be scrolled."
    e "Les propriétés 'xinitial' et 'yinitial' indique le décalage initial, comme une fraction de ce qui peut être déplacé."

# game/tutorial_screen_displayables.rpy:885
translate french viewport_displayables_c047efb5:

    # e "Finally, there's the child_size property. To explain what it does, I first have to show you what happens when we don't have it."
    e "Finalement, il y a la propriété 'child_size'. Pour vous expliquez ce qu’elle fait, je vais commencer par vous montrer ce qui se passe quand elle n’est pas présente."

# game/tutorial_screen_displayables.rpy:887
translate french viewport_displayables_c563019f:

    # e "As you can see, the text wraps. That's because Ren'Py is offering it space that isn't big enough."
    e "Comme vous pouvez le voir, le texte est coupé. C’est parce que Ren’Py ne lui offre pas un espace suffisant."

# game/tutorial_screen_displayables.rpy:909
translate french viewport_displayables_4bcf0ad0:

    # e "When we give the screen a child_size, it offers more space to its children, allowing scrolling. It takes a horizontal and vertical size. If one component is None, it takes the size of the viewport."
    e "Quand nous donnons à l’écran une 'child_size', cela permet d’obtenir plus d’espace pour le contenu, nous autorisant le déplacement. Il prend une taille horizontale et une taille verticale. Si l’un des composants vaut None, alors il prend la taille du 'viewport'."

# game/tutorial_screen_displayables.rpy:936
translate french viewport_displayables_ae4ff821:

    # e "Finally, there's the vpgrid displayable. It combines a viewport and a grid into a single displayable, except it's more efficient than either, since it doesn't have to draw every child."
    e "Enfin, il y a l’élément 'vpgrid'. Il combine un 'viewport' et une 'grid' (un hublot et une grille)"

# game/tutorial_screen_displayables.rpy:938
translate french viewport_displayables_71fa0b8f:

    # e "It takes the cols and rows properties, which give the number of rows and columns of children. If one is omitted, Ren'Py figures it out from the other and the number of children."
    e "Elle reçoit donc les propriétés 'cols' et 'rows' qui donnent le nombre de colonnes et de lignes pour les enfants. Si l’un est omis, Ren’Py le calcule grâce à la première valeur et au nombre d’enfants."

translate french strings:

    # tutorial_screen_displayables.rpy:9
    old "Common properties all displayables share."
    new "Les propriétés communes que tous les éléments affichables partagent."

    # tutorial_screen_displayables.rpy:9
    old "Adding images and other displayables."
    new "Ajouter des images et d’autres éléments affichables."

    # tutorial_screen_displayables.rpy:9
    old "Text."
    new "Texte."

    # tutorial_screen_displayables.rpy:9
    old "Boxes and other layouts."
    new "Boîtes et autres canvas."

    # tutorial_screen_displayables.rpy:9
    old "Windows and frames."
    new "Fenêtre et cadres."

    # tutorial_screen_displayables.rpy:9
    old "Buttons."
    new "Boutons"

    # tutorial_screen_displayables.rpy:9
    old "Bars."
    new "Barres."

    # tutorial_screen_displayables.rpy:9
    old "Viewports."
    new "Viewports (hublots)."

    # tutorial_screen_displayables.rpy:9
    old "Imagemaps."
    new "Cartes."

    # tutorial_screen_displayables.rpy:9
    old "That's all for now."
    new "C’est tout pour le moment."

    # tutorial_screen_displayables.rpy:55
    old "This uses position properties."
    new "Ceci utilise des propriétés de position."

    # tutorial_screen_displayables.rpy:63
    old "And the world turned upside down..."
    new "Et le monde fut renversé."

    # tutorial_screen_displayables.rpy:115
    old "Flight pressure in tanks."
    new "Pression de vol dans les tanks."

    # tutorial_screen_displayables.rpy:116
    old "On internal power."
    new "Sur le générateur interne."

    # tutorial_screen_displayables.rpy:117
    old "Launch enabled."
    new "Lancement activé."

    # tutorial_screen_displayables.rpy:118
    old "Liftoff!"
    new "Décollage !"

    # tutorial_screen_displayables.rpy:232
    old "The answer is [answer]."
    new "La réponse est [answer]."

    # tutorial_screen_displayables.rpy:244
    old "Text tags {color=#c8ffc8}work{/color} in screens."
    new "Les étiquettes de texte {color=#c8ffc8}fonctionnent{/color} dans les écrans."

    # tutorial_screen_displayables.rpy:336
    old "Bigger"
    new "Plus grand."

    # tutorial_screen_displayables.rpy:401
    old "This is a screen."
    new "Ceci est un écran."

    # tutorial_screen_displayables.rpy:402
    old "Okay"
    new "OK."

    # tutorial_screen_displayables.rpy:440
    old "You clicked the button."
    new "Vous avez cliqué sur le bouton."

    # tutorial_screen_displayables.rpy:441
    old "Click me."
    new "Cliquez sur moi !"

    # tutorial_screen_displayables.rpy:453
    old "You hovered the button."
    new "Vous survolez le bouton."

    # tutorial_screen_displayables.rpy:454
    old "You unhovered the button."
    new "Vous ne survolez pas le bouton."

    # tutorial_screen_displayables.rpy:470
    old "Heal"
    new "Soigner"

    # tutorial_screen_displayables.rpy:479
    old "This is a textbutton."
    new "Ceci est un bouton de texte."

    # tutorial_screen_displayables.rpy:539
    old "Or me."
    new "Ou moi."

    # tutorial_screen_displayables.rpy:541
    old "You clicked the other button."
    new "Vous avez cliqué sur l’autre bouton."

    # tutorial_screen_displayables.rpy:880
    old "This text is wider than the viewport."
    new "Le texte est plus large que le hublot."
