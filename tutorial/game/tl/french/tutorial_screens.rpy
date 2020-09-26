
# game/tutorial_screens.rpy:165
translate french tutorial_screens_2faa22e5:

    # e "Screens are the most powerful part of Ren'Py. Screens let you customize the out-of-game interface, and create new in-game interface components."
    e "Les écrans (screens) sont la partie la plus puissante de Ren’Py. Ils vous laissent configurer les interfaces « hors du jeu » et créer des composants pour le jeu."

# game/tutorial_screens.rpy:171
translate french screens_menu_7f31d730:

    # e "What would you like to know about screens?" nointeract
    e "Que souhaitez-vous savoir sur les écrans ?" nointeract

# game/tutorial_screens.rpy:201
translate french screens_demo_115a4b8f:

    # e "Screens are how we create the user interface in Ren'Py. With the exception of images and transitions, everything you see comes from a screen."
    e "Les écrans sont ce que nous avons créé pour réaliser l’interface dans Ren’Py. À l’exception des images et des transitions, tout ce que vous voyez vient d’un écran."

# game/tutorial_screens.rpy:203
translate french screens_demo_ce100e07:

    # e "When I'm speaking to you, I'm using the 'say' screen. It's responsible for taking dialogue and presenting it to the player."
    e "Quand je vous parle, j’utilise l’écran 'say'. Il est responsable de l’affichage et de la présentation des dialogues."

# game/tutorial_screens.rpy:205
translate french screens_demo_1bdfb4bd:

    # e "And when the menu statement displays an in-game choice, the 'choice' screen is used. Got it?" nointeract
    e "Et via la déclaration 'menu' présente un choix au joueur, c’est l’écran 'choice' qui est utilisé. Compris ?" nointeract

# game/tutorial_screens.rpy:215
translate french screens_demo_31a20e24:

    # e "Text input uses the 'input' screen, NVL mode uses the 'nvl' screen, and so on."
    e "Le texte de saisie utilise l’écran 'input', le mode NVL utilise l’écran 'nvl', etc.."

# game/tutorial_screens.rpy:217
translate french screens_demo_5a5aa2d5:

    # e "More than one screen can be displayed at once. For example, the buttons at the bottom - Back, History, Skip, and so on - are all displayed by a quick_menu screen that's shown all of the time."
    e "Plusieurs écrans peuvent être affichés à la fois. Par exemple, les boutons du bas (Retour arrière, historique, …) sont tous affichés dans l’écran 'quick_menu'. Cet écran est constamment affiché durant la partie."

# game/tutorial_screens.rpy:219
translate french screens_demo_58d48fde:

    # e "There are a lot of special screens, like 'main_menu', 'load', 'save', and 'preferences'. Rather than list them all here, I'll {a=https://www.renpy.org/doc/html/screen_special.html}send you to the documentation{/a}."
    e "Il y a beaucoup d’écrans spéciaux, comme 'main_menu', 'load', 'save' et 'preferences'. Plutôt que de les lister tous ici, je {a=https://www.renpy.org/doc/html/screen_special.html}vous renvoie à la documentation{/a}."

# game/tutorial_screens.rpy:221
translate french screens_demo_27476d11:

    # e "In a newly created project, all these screens live in screens.rpy. You can edit that file in order to change them."
    e "Dans un projet nouvellement créé, tous ces écrans sont définis dans le fichier screens.rpy. Vous pouvez éditer ce fichier pour les modifier."

# game/tutorial_screens.rpy:223
translate french screens_demo_a699b1cb:

    # e "You aren't limited to these screens either. In Ren'Py, you can make your own screens, and use them for your game's interface."
    e "Vous n’êtes pas limité à ces écrans, par ailleurs. Dans Ren’Py, vous pouvez créer vos propres écrans et les utiliser pour votre interface de jeu."

# game/tutorial_screens.rpy:230
translate french screens_demo_a136e191:

    # e "For example, in an RPG like visual novel, a screen can display the player's statistics."
    e "Par exemple, dans un jeu RPG, un écran peut afficher les caractéristiques du joueur."

# game/tutorial_screens.rpy:234
translate french screens_demo_1f50f3d3:

    # e "Which reminds me, I should probably heal you."
    e "Cela me rappelle que je dois probablement vous soigner."

# game/tutorial_screens.rpy:241
translate french screens_demo_8a54de7a:

    # e "Complex screens can be the basis of whole game mechanics. A stats screen like this can be the basis of dating and life-sims."
    e "Les écrans complexes peuvent être à la base de toute une mécanique de jeu. Un écran de statistique peut être la base d’un jeu de rencontre (simdate) ou d’un simulateur de vie (life-sims)."

# game/tutorial_screens.rpy:246
translate french screens_demo_62c184f8:

    # e "While screens might be complex, they're really just the result of a lot of simple parts working together to make something larger than all of them."
    e "Comme les écrans peuvent être complexes, ils sont le résultat d’une composition d’éléments simples travaillant ensemble pour rendre quelque chose qui les dépasse."

# game/tutorial_screens.rpy:265
translate french screens_showing_1b51e9a4:

    # e "Here's an example of a very simple screen. The screen statement is used to tell Ren'Py this is a screen, and it's name is simple_screen."
    e "Voici un exemple d’un écran très simple. La déclaration 'screen' est utilisée pour dire à Ren’Py que c’est un écran et que son nom est 'simple_screen'."

# game/tutorial_screens.rpy:267
translate french screens_showing_5a6bbad0:

    # e "Inside the screen statement, lines introduces displayables such as frame, vbox, text, and textbutton; or properties like action, xalign, and ypos."
    e "Au sein de la déclaration 'screen', quelques lignes introduisent des éléments affichables tels que des cadres (frame), des boîtes verticales (vbox), des textes (text) et des boutons textuels (textbutton) ainsi que des propriétés comme 'action', 'xalign' et 'ypos'."

# game/tutorial_screens.rpy:272
translate french screens_showing_ae40755c:

    # e "I'll work from the inside out to describe the statements. But first, I'll show the screen so you can see it in action."
    e "Je vais vous décrire les déclarations en partant du cœur. Mais avant cela, je vais vous montrer l’écran en action."

# game/tutorial_screens.rpy:274
translate french screens_showing_bc320819:

    # e "The text statement is used to display the text provided."
    e "La déclaration 'text' est utilisé pour afficher le texte."

# game/tutorial_screens.rpy:276
translate french screens_showing_64f23380:

    # e "The textbutton statement introduces a button that can be clicked. When the button is clicked, the provided action is run."
    e "La déclaration 'textbutton' place un bouton cliquable. Quand le bouton est cliqué, l’action mentionnée est exécutée."

# game/tutorial_screens.rpy:278
translate french screens_showing_e8f68c08:

    # e "Both are inside a vbox, which means vertical box, statement - that places the text on top of the button."
    e "Les deux sont à l’intérieur d’une 'vbox', une boîte verticale qui va donc placer le texte au-dessus du bouton."

# game/tutorial_screens.rpy:280
translate french screens_showing_7e48fc22:

    # e "And that is inside a frame that provides the background and borders. The frame has an at property that takes a transform giving its position."
    e "Et tout cela se trouve dans un cadre (frame) qui fournit les bordures et l’arrière-plan. Le cadre a une propriété 'at' qui reçoit une transformation pour préciser sa position."

# game/tutorial_screens.rpy:286
translate french screens_showing_80425bf3:

    # e "There are a trio of statements that are used to display screens."
    e "Il y a un trio de déclarations qui sont utilisées pour afficher les écrans."

# game/tutorial_screens.rpy:291
translate french screens_showing_7d2deb37:

    # e "The first is the show screen statement, which displays a screen and lets Ren'Py keep going."
    e "La première est la déclaration 'show screen' qui affiche un écran et laisse Ren’Py poursuivre."

# game/tutorial_screens.rpy:293
translate french screens_showing_7626dc8b:

    # e "The screen will stay shown until it is hidden."
    e "L’écran restera affiché jusqu’à ce qu’il soit caché."

# game/tutorial_screens.rpy:297
translate french screens_showing_c79038a4:

    # e "Hiding a screen is done with the hide screen statement."
    e "Cacher un écran se fait en utilisant la déclaration 'hide screen'."

# game/tutorial_screens.rpy:301
translate french screens_showing_8f78a97d:

    # e "The call screen statement stops Ren'Py from executing script until the screen either returns a value, or jumps the script somewhere else."
    e "La déclaration 'call screen' stoppe tout script Ren’Py en cours d’exécution jusqu’à ce que l’écran retourne une valeur ou saute ailleurs dans le script."

# game/tutorial_screens.rpy:303
translate french screens_showing_b52e420c:

    # e "Since we can't display dialogue at the same time, you'll have to click 'Okay' to continue."
    e "Comme nous ne pouvons pas afficher de dialogue en même temps, vous devrez cliquer sur 'OK' pour poursuivre."

# game/tutorial_screens.rpy:310
translate french screens_showing_c5ca730f:

    # e "When a call screen statement ends, the screen is automatically hidden."
    e "Quand une déclaration 'call screen' se termine, l’écran est automatiquement caché."

# game/tutorial_screens.rpy:312
translate french screens_showing_a38d1702:

    # e "Generally, you use show screen to show overlays that are up all the time, and call screen to show screens the player interacts with for a little while."
    e "Généralement, vous utilisez 'show screen' pour montrer ce qui est tout le temps affiché et 'call screen' pour montrer les écrans qui interagissent durant un instant avec le joueur."

# game/tutorial_screens.rpy:335
translate french screens_parameters_0666043d:

    # e "Here's an example of a screen that takes three parameters. The message parameter is a message to show, while the okay and cancel actions are run when the appropriate button is chosen."
    e "Voici un exemple qui prend trois paramètres. Le paramètre 'message' est le message à afficher, tandis que les actions 'okay' et 'cancel' sont exécutées quand vous pressez sur le bouton correspondant."

# game/tutorial_screens.rpy:337
translate french screens_parameters_cf95b914:

    # e "While the message parameter always has to be supplied, the okay and cancel parameters have default values that are used if no argument is given."
    e "Le paramètre 'message' doit toujours être fourni, les paramètres 'okay' et 'cancel' ont des valeurs par défaut. Du coup, vous n’êtes pas obligé de fournir ces paramètres."

# game/tutorial_screens.rpy:339
translate french screens_parameters_4ce03111:

    # e "Each parameter is a variable that is defined inside the screen. Inside the screen, these variables take priority over those used in the rest of Ren'Py."
    e "Chaque paramètre est une variable qui est définie au sein de l’écran. Ces variables sont prioritaires sur celles qui sont utilisées dans le reste du code Ren’Py."

# game/tutorial_screens.rpy:343
translate french screens_parameters_106c2a04:

    # e "When a screen is shown, arguments can be supplied for each of the parameters. Arguments can be given by position or by name."
    e "Quand un écran est affiché, les arguments peuvent être fournis pour chaque paramètre. Les arguments peuvent être donnés par position ou par nom."

# game/tutorial_screens.rpy:350
translate french screens_parameters_12ac92d4:

    # e "Parameters let us change what a screen displays, simply by re-showing it with different arguments."
    e "Les paramètres nous permettent de changer ce que l’écran affiche, simplement en les réaffichant avec des arguments différents."

# game/tutorial_screens.rpy:357
translate french screens_parameters_d143a994:

    # e "The call screen statement can also take arguments, much like show screen does."
    e "La déclaration 'call screen' peut aussi recevoir des arguments, exactement comme le fait la déclaration 'show screen'."

# game/tutorial_screens.rpy:369
translate french screens_properties_423246a2:

    # e "There are a few properties that can be applied to a screen itself."
    e "Il y a quelques propriétés qui peuvent s’appliquer sur les écrans eux-mêmes."

# game/tutorial_screens.rpy:380
translate french screens_properties_4fde164e:

    # e "When the modal property is true, you can't interact with things beneath the screen. You'll have to click 'Close This Screen' before you can continue."
    e "Quand la propriété 'modal' est à True, vous ne pouvez plus interagir avec les éléments hors de cet écran. Vous devrez cliquez sur 'Fermer cet écran' pour pouvoir poursuivre."

# game/tutorial_screens.rpy:398
translate french screens_properties_550c0bea:

    # e "When a screen has the tag property, it's treated like the tag part of an image name. Here, I'm showing a_tag_screen."
    e "Quand un écran a la propriété 'tag', il est traité comme la partie étiquetée d’une image nommée. Ici, j’affiche 'a_tag_screen'."

# game/tutorial_screens.rpy:402
translate french screens_properties_4fcf8af8:

    # e "When I show b_tag_screen, it replaces a_tag_screen."
    e "Quand j’affiche 'b_tag_screen', il remplace 'a_tag_screen'."

# game/tutorial_screens.rpy:404
translate french screens_properties_7ed5a791:

    # e "This is useful in the game and main menus, where you want the load screen to replace the preferences screen. By default, all those screens have tag menu."
    e "Ceci est très pratique dans le jeu et dans les menus principaux, quand vous voulez que l’écran de chargement remplace l’écran de préférences. Par défaut, tous ces menus ont un tag."

# game/tutorial_screens.rpy:408
translate french screens_properties_5d51bd1e:

    # e "For some reason, tag takes a name, and not an expression. It's too late to change it."
    e "Pour certaines raisons, la déclaration 'tag' prend un nom, pas une expression. C’est trop tard pour le changer."

# game/tutorial_screens.rpy:432
translate french screens_properties_6706e266:

    # e "The zorder property controls the order in which screens overlap each other. The larger the zorder number, the closer the screen is to the player."
    e "La propriété 'zorder' contrôle l’ordre dans lequel les écrans s’entrelacent les uns les autres. Plus le nombre 'zorder' est élévé, plus l’écran est proche du joueur."

# game/tutorial_screens.rpy:434
translate french screens_properties_f7a2c73d:

    # e "By default, a screen has a zorder of 0. When two screens have the same zorder number, the screen that is shown second is closer to the player."
    e "Par défaut, un écran a un 'zorder' à zéro. Quand deux écrans ont la même valeur 'zorder', l’écran qui a été affiché en second apparait par-dessus l’autre."

# game/tutorial_screens.rpy:454
translate french screens_properties_78433eb8:

    # e "The variant property selects a screen based on the properties of the device it's running on."
    e "La propriété 'variant' sélectionne un écran basé sur les propriétés de l’équipement qui fait tourner le jeu."

# game/tutorial_screens.rpy:456
translate french screens_properties_e6db6d02:

    # e "In this example, the first screen will be used for small devices like telephones, and the other screen will be used for tablets and computers."
    e "Dans cet exemple, le premier écran a été utilisé pour les petits équipements comme les téléphones et cet autre écran est utilisé pour les tablettes et les ordinateurs."

# game/tutorial_screens.rpy:475
translate french screens_properties_d21b5500:

    # e "Finally, the style_prefix property specifies a prefix that's applied to the styles in the screen."
    e "Enfin, la propriété 'style_prefix' spécifie le préfixe qui sera appliqué à tous les styles de cet écran."

# game/tutorial_screens.rpy:477
translate french screens_properties_560ca08a:

    # e "When the 'red' prefix is given, the frame gets the 'red_frame' style, and the text gets the 'red_text' style."
    e "Quand le préfixe 'red' est donné, le cadre (frame) hérite du style 'red_frame' et le texte obtient le style 'red_text'."

# game/tutorial_screens.rpy:479
translate french screens_properties_c7ad3a8e:

    # e "This can save a lot of typing when styling screens with many displayables in them."
    e "Cela permet d’éviter beaucoup de saisie quand on conçoit un écran qui contient beaucoup d’éléments affichables en son sein."

# game/tutorial_screens.rpy:491
translate french screens_control_4a1d8d7c:

    # e "The screen language has a few statements that do things other than show displayables. If you haven't seen the section on {a=jump:warp_screen_displayables}Screen Displayables{/a} yet, you might want to check it out, then come back here."
    e "L’écran 'language' dispose de quelques déclarations qui gère d’autres choses que son affichage. Si vous n’avez pas encore lu la section sur {a=jump:warp_screen_displayables}les écrans affichables{/a}, vous devriez la consulter avant de revenir ici."

# game/tutorial_screens.rpy:503
translate french screens_control_0e939050:

    # e "The python statement works just about the same way it does in the script. A single line of Python is introduced with a dollar sign. This line is run each time the screen updates."
    e "La déclaration python fonctionne de la même façon que dans un script. Une ligne Python est introduite par le signe dollar. Cette ligne est exécutée à chaque mise à jour de l’écran."

# game/tutorial_screens.rpy:518
translate french screens_control_6334650a:

    # e "Similarly, the python statement introduces an indented block of python statements. But there is one big difference in Python in screens and Python in scripts."
    e "De façon similaire, la déclaration 'python' est introduite par un code indenté de déclarations python. Mais il y a une grande différence entre Python dans les écrans et Python dans les scripts."

# game/tutorial_screens.rpy:520
translate french screens_control_ba8f5f13:

    # e "The Python you use in screens isn't allowed to have side effects. That means that it can't do things like change the value of a variable."
    e "Le code Python que vous utilisez dans les écrans ne vous autorisent pas les effets de bord. Cela signifie que vous ne pouvez pas faire certaines choses comme changer la valeur d’une variable."

# game/tutorial_screens.rpy:522
translate french screens_control_f75fa254:

    # e "The reason for this is that Ren'Py will run a screen, and the Python in it, during screen prediction."
    e "La raison à cela est que Ren’Py va exécuter un 'screen' et que le Python intégré n’existera que durant cette exécution."

# game/tutorial_screens.rpy:536
translate french screens_control_40c12afa:

    # e "The default statement lets you set the value of a screen variable the first time the screen runs. This value can be changed with the SetScreenVariable and ToggleScreenVariable actions."
    e "La déclaration 'default' vous permet de définir la valeur par défaut d’une variable de l’écran durant sa première exécution. Cette valeur peut être modifiée avec les actions 'SetScreenVariable' et 'ToggleScreenVariable'."

# game/tutorial_screens.rpy:538
translate french screens_control_39e0f7e6:

    # e "The default statement differs from the Python statement in that it is only run once. Python runs each time the screen updates, and hence the variable would never change value."
    e "La déclaration 'default' diffère des déclarations Python dans le sens où elle n’est exécutée qu’une seule fois. Python s’exécute chaque fois que l’écran se met à jour et du coup la variable ne changerait jamais de valeur."

# game/tutorial_screens.rpy:557
translate french screens_control_87a75fe7:

    # e "The if statement works like it does in script, running one block if the condition is true and another if the condition is false."
    e "La déclaration 'if' fonctionne comme dans les scripts, exécutant le premier bloc si la condition vaut True et l’autre si la condition vaut False."

# game/tutorial_screens.rpy:572
translate french screens_control_6a8c07f6:

    # e "The for statement takes a list of values, and iterates through them, running the block inside the for loop with the variable bound to each list item."
    e "La déclaration 'for' prend une liste de valeur et itère dessus, exécutant le bloc à l’intérieur de la boucle 'for' avec la variable liée à chaque élément de la liste."

# game/tutorial_screens.rpy:588
translate french screens_control_f7b755fa:

    # e "The on and key statements probably only make sense at the top level of the screen."
    e "Les déclarations 'on' et 'key' ne prennent du sens que pour le plus haut niveau des écrans."

# game/tutorial_screens.rpy:590
translate french screens_control_328b0676:

    # e "The on statement makes the screen run an action when an event occurs. The 'show' event happens when the screen is first shown, and the 'hide' event happens when it is hidden."
    e "La déclaration 'on' fait que l’écran exécute une action quand un évènement survient. L’évènement 'show' est déclenché au premier affichage et l’évènement 'hide' survient quand l’écran est caché."

# game/tutorial_screens.rpy:592
translate french screens_control_6768768b:

    # e "The key event runs an event when a key is pressed."
    e "L’évènement 'key' s’exécute quand une touche est pressée."

# game/tutorial_screens.rpy:600
translate french screen_use_c6a20a16:

    # e "The screen language use statement lets you include a screen inside another. This can be useful to prevent duplication inside screens."
    e "La déclaration 'use' de l’écran 'language' vous permet d’inclure un écran dans un autre. C’est utile pour prévenir la duplication au sein des écrans."

# game/tutorial_screens.rpy:616
translate french screen_use_95a34d3a:

    # e "Take for example this screen, which shows two stat entries. There's already a lot of duplication there, and if we had more stats, there would be more."
    e "Prenons par exemple cet écran qui présente deux statistiques. Il y a déjà beaucoup de duplication ici. Si vous ajoutez des statistiques, il y en aura encore plus."

# game/tutorial_screens.rpy:633
translate french screen_use_e2c673d9:

    # e "Here, we moved the statements that show the text and bar into a second screen, and the use statement includes that screen in the first one."
    e "Ici, nous avons déplacé les déclarations qui affichent le texte les barres dans un second écran et nous avons utilisé la déclaration 'use' dans le premier écran."

# game/tutorial_screens.rpy:635
translate french screen_use_2efdd2ff:

    # e "The name and amount of the stat are passed in as arguments to the screen, just as is done in the call screen statement."
    e "Le nom et la valeur de la statistique sont passés comme argument à l’écran, comme nous l’aurions fait pour une déclaration 'call screen'."

# game/tutorial_screens.rpy:637
translate french screen_use_f8d1bf9d:

    # e "By doing it this way, we control the amount of duplication, and can change the stat in one place."
    e "En faisant cela, nous limitons la duplication et nous pouvons changer la statistique à un seul endroit."

# game/tutorial_screens.rpy:653
translate french screen_use_4e22c25e:

    # e "The transclude statement goes one step further, by letting the use statement take a block of screen language statements."
    e "La déclaration 'transclude' va encore plus loin en laissant la déclaration 'use' recevoir un bloc de déclaration de langage pour les écrans."

# game/tutorial_screens.rpy:655
translate french screen_use_c83b97e3:

    # e "When the included screen reaches the transclude statement it is replaced with the block from the use statement."
    e "Quand l’écran inclus atteint la déclaration 'transclude', il la remplace par le bloc provenant de la déclaration 'use'."

# game/tutorial_screens.rpy:657
translate french screen_use_1ad1f358:

    # e "The boilerplate screen is included in the first one, and the text from the first screen is transcluded into the boilerplate screen."
    e "L’écran 'boilerplate' est inclus en premier et le texte de cet écran est retranscrit dans l’écran 'boilerplate'."

# game/tutorial_screens.rpy:659
translate french screen_use_f74fab6e:

    # e "Use and transclude are complex, but very powerful. If you think about it, 'use boilerplate' is only one step removed from writing your own Screen Language statement."
    e "'use' et 'transclude' sont complexes, mais très puissantes. Si vous y réfléchissez, 'use boilerplate' supprime une étape de rédaction dans votre code."

translate french strings:

    # tutorial_screens.rpy:26
    old " Lv. [lv]"
    new "Lvl. [lv]"

    # tutorial_screens.rpy:29
    old "HP"
    new "PV"

    # tutorial_screens.rpy:58
    old "Morning"
    new "Matin"

    # tutorial_screens.rpy:58
    old "Afternoon"
    new "Après-midi"

    # tutorial_screens.rpy:58
    old "Evening"
    new "Soir"

    # tutorial_screens.rpy:61
    old "Study"
    new "Étudier"

    # tutorial_screens.rpy:61
    old "Exercise"
    new "Exercice"

    # tutorial_screens.rpy:61
    old "Eat"
    new "Manger"

    # tutorial_screens.rpy:61
    old "Drink"
    new "Boire"

    # tutorial_screens.rpy:61
    old "Be Merry"
    new "Être joyeux"

    # tutorial_screens.rpy:107
    old "Strength"
    new "Force"

    # tutorial_screens.rpy:111
    old "Intelligence"
    new "Intelligence"

    # tutorial_screens.rpy:115
    old "Moxie"
    new "Moxie"

    # tutorial_screens.rpy:119
    old "Chutzpah"
    new "Chutzpah"

    # tutorial_screens.rpy:171
    old "What screens can do."
    new "Ce que les écrans peuvent faire."

    # tutorial_screens.rpy:171
    old "How to show screens."
    new "Comment afficher un écran."

    # tutorial_screens.rpy:171
    old "Passing parameters to screens."
    new "Passer des paramètres à un écran."

    # tutorial_screens.rpy:171
    old "Screen properties."
    new "Les propriétés des écrans."

    # tutorial_screens.rpy:171
    old "Special screen statements."
    new "Les déclarations spéciales des écrans."

    # tutorial_screens.rpy:171
    old "Using other screens."
    new "Utiliser d’autres écrans."

    # tutorial_screens.rpy:171
    old "That's it."
    new "C’est tout, pour le moment."

    # tutorial_screens.rpy:205
    old "I do."
    new "Oui"

    # tutorial_screens.rpy:331
    old "Hello, world."
    new "Bonjour le monde !"

    # tutorial_screens.rpy:331
    old "You can't cancel this."
    new "Vous ne pouvez pas annuler cela."

    # tutorial_screens.rpy:346
    old "Shiro was here."
    new "Shiro était ici."

    # tutorial_screens.rpy:362
    old "Click either button to continue."
    new "Cliquez sur n’importe quel bouton pour poursuivre."

    # tutorial_screens.rpy:377
    old "Close This Screen"
    new "Fermer cet écran"

    # tutorial_screens.rpy:388
    old "A Tag Screen"
    new "Écran taggé A"

    # tutorial_screens.rpy:395
    old "B Tag Screen"
    new "Écran taggé B"

    # tutorial_screens.rpy:447
    old "You're on a small device."
    new "Vous êtes sur un petit équipement."

    # tutorial_screens.rpy:452
    old "You're not on a small device."
    new "Vous n’êtes pas sur un petit équipement."

    # tutorial_screens.rpy:466
    old "This text is red."
    new "Ce texte est rouge."

    # tutorial_screens.rpy:496
    old "Hello, World."
    new "Bonjour, Monde."

    # tutorial_screens.rpy:510
    old "It's good to meet you."
    new "C’est bon de vous rencontrer."

    # tutorial_screens.rpy:534
    old "Increase"
    new "Augmenter"

    # tutorial_screens.rpy:563
    old "Earth"
    new "Terre"

    # tutorial_screens.rpy:563
    old "Moon"
    new "Lune"

    # tutorial_screens.rpy:563
    old "Mars"
    new "Mars"

    # tutorial_screens.rpy:581
    old "Now press 'a'."
    new "Maintenant pressez 'a'."

    # tutorial_screens.rpy:583
    old "The screen was just shown."
    new "Cet écran vient juste d’apparaître."

    # tutorial_screens.rpy:585
    old "You pressed the 'a' key."
    new "Vous avez pressé la touche 'a'."

    # tutorial_screens.rpy:608
    old "Health"
    new "Santé"

    # tutorial_screens.rpy:613
    old "Magic"
    new "Magie"

    # tutorial_screens.rpy:644
    old "There's not much left to see."
    new "Il n’y a plus grand chose à voir."
