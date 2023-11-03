translate french strings:

    # screens.rpy:9
    old "## Styles"
    new "## Styles"

    # screens.rpy:87
    old "## In-game screens"
    new "## Écrans de jeu"

    # screens.rpy:91
    old "## Say screen"
    new "## Écran des dialogues"

    # screens.rpy:93
    old "## The say screen is used to display dialogue to the player. It takes two parameters, who and what, which are the name of the speaking character and the text to be displayed, respectively. (The who parameter can be None if no name is given.)"
    new "## L’écran des dialogues est utilisé pour afficher les dialogues du joueur. Il prend deux paramètres, who(qui) et what(quoi) qui sont respectivement le nom du personnage en train de parler et le texte à afficher. (Le paramètre who(qui) peut être None si aucun nom n’est donné.)"

    # screens.rpy:98
    old "## This screen must create a text displayable with id \"what\", as Ren'Py uses this to manage text display. It can also create displayables with id \"who\" and id \"window\" to apply style properties."
    new "## Cet écran affiche le texte correspondant à what. Il peut également créer un texte avec le paramètre who et l’identifiant « window » est utilisé pour déterminer les styles à appliquer."

    # screens.rpy:102
    old "## https://www.renpy.org/doc/html/screen_special.html#say"
    new "## https://www.renpy.org/doc/html/screen_special.html#say"

    # screens.rpy:169
    old "## Input screen"
    new "## Écran de saisie"

    # screens.rpy:171
    old "## This screen is used to display renpy.input. The prompt parameter is used to pass a text prompt in."
    new "## Cet écran est utilisé pour afficher renpy.input. Le paramètre prompt est utilisé pour passer le texte par défaut."

    # screens.rpy:174
    old "## This screen must create an input displayable with id \"input\" to accept the various input parameters."
    new "## Cet écran doit créer une entrée affichable avec l'id \"input\" pour accepter les différents paramètres."

    # screens.rpy:177
    old "## http://www.renpy.org/doc/html/screen_special.html#input"
    new "## http://www.renpy.org/doc/html/screen_special.html#input"

    # screens.rpy:205
    old "## Choice screen"
    new "## Écran des choix"

    # screens.rpy:207
    old "## This screen is used to display the in-game choices presented by the menu statement. The one parameter, items, is a list of objects, each with caption and action fields."
    new "## Cet écran est utilisé pour afficher les choix qui seront fait par le joueur dans le jeu. Le premier paramètre, items, est une liste d'objets contenant chacun des champs de texte et d'action."

    # screens.rpy:211
    old "## http://www.renpy.org/doc/html/screen_special.html#choice"
    new "## http://www.renpy.org/doc/html/screen_special.html#choice"

    # screens.rpy:221
    old "## When this is true, menu captions will be spoken by the narrator. When false, menu captions will be displayed as empty buttons."
    new "## Lorsque cette option est activée, les sous-titres du menu sont dits par \"narrator\". Si cette valeur est fausse, les légendes du menu seront affichées sous forme de boutons vides."

    # screens.rpy:244
    old "## Quick Menu screen"
    new "## Écran des menus rapides"

    # screens.rpy:246
    old "## The quick menu is displayed in-game to provide easy access to the out-of-game menus."
    new "## Les menus rapides sont affichés dans le jeu pour permettre un accès rapide à certaines fonctions."

    # screens.rpy:261
    old "Back"
    new "Retour"

    # screens.rpy:262
    old "History"
    new "Historique"

    # screens.rpy:263
    old "Skip"
    new "Avance rapide"

    # screens.rpy:264
    old "Auto"
    new "Auto"

    # screens.rpy:265
    old "Save"
    new "Sauvegarde"

    # screens.rpy:266
    old "Q.Save"
    new "Sauvegarde R."

    # screens.rpy:267
    old "Q.Load"
    new "Chargement R."

    # screens.rpy:268
    old "Prefs"
    new "Préf."

    # screens.rpy:271
    old "## This code ensures that the quick_menu screen is displayed in-game, whenever the player has not explicitly hidden the interface."
    new "## Ce code garantit que le menu d’accès rapide sera affiché dans le jeu, tant que le joueur n’aura pas explicitement demandé à cacher l’interface."

    # screens.rpy:291
    old "## Navigation screen"
    new "## Écran de navigation"

    # screens.rpy:293
    old "## This screen is included in the main and game menus, and provides navigation to other menus, and to start the game."
    new "## Cet écran est disponible dans le menu principal et dans le menu de jeu. Il fournit l’accès aux autres menus et permet le démarrage du jeu."

    # screens.rpy:308
    old "Start"
    new "Nouvelle partie"

    # screens.rpy:316
    old "Load"
    new "Charger"

    # screens.rpy:318
    old "Preferences"
    new "Préférences"

    # screens.rpy:322
    old "End Replay"
    new "Fin de la rediffusion"

    # screens.rpy:326
    old "Main Menu"
    new "Menu principal"

    # screens.rpy:328
    old "About"
    new "À propos"

    # screens.rpy:332
    old "## Help isn't necessary or relevant to mobile devices."
    new "## L'aide n’est ni nécessaire ni pertinente sur les appareils mobiles."

    # screens.rpy:333
    old "Help"
    new "Aide"

    # screens.rpy:335
    old "## The quit button is banned on iOS and unnecessary on Android."
    new "## Le bouton pour quitter est banni sur iOs et n'est pas nécessaire sur Android."

    # screens.rpy:336
    old "Quit"
    new "Quitter"

    # screens.rpy:350
    old "## Main Menu screen"
    new "## Écran du menu principal"

    # screens.rpy:352
    old "## Used to display the main menu when Ren'Py starts."
    new "## Utilisé pour afficher le menu principal quand Ren'Py démarre."

    # screens.rpy:354
    old "## http://www.renpy.org/doc/html/screen_special.html#main-menu"
    new "## http://www.renpy.org/doc/html/screen_special.html#main-menu"

    # screens.rpy:369
    old "## The use statement includes another screen inside this one. The actual contents of the main menu are in the navigation screen."
    new "## L'instruction use inclut un autre écran à l'intérieur de celui-ci. Le vrai contenu du menu principal se trouve dans l'écran \"navigation\"."

    # screens.rpy:413
    old "## Game Menu screen"
    new "## Écran du menu de jeu"

    # screens.rpy:415
    old "## This lays out the basic common structure of a game menu screen. It's called with the screen title, and displays the background, title, and navigation."
    new "## Ceci présente la structure commune de base d'un écran du menu de jeu. Il est appelé en lui passant le titre de l'écran, et il affiche l'arrière-plan, le titre et la navigation."

    # screens.rpy:418
    old "## The scroll parameter can be None, or one of \"viewport\" or \"vpgrid\". This screen is intended to be used with one or more children, which are transcluded (placed) inside it."
    new "## Le paramètre de défilement peut être None, ou \"viewport\" ou \"vpgrid\". Cet écran est destiné à être utilisé avec un ou plusieurs enfants, qui sont transclus (placés) à l'intérieur de l'écran."

    # screens.rpy:476
    old "Return"
    new "Retour"

    # screens.rpy:539
    old "## About screen"
    new "## Écran « À propos... »"

    # screens.rpy:541
    old "## This screen gives credit and copyright information about the game and Ren'Py."
    new "## Cet écran présente le générique, les crédits et les informations de copyright relatives au jeu et à Ren’Py."

    # screens.rpy:544
    old "## There's nothing special about this screen, and hence it also serves as an example of how to make a custom screen."
    new "## Il n’y a rien de spécial sur cet écran. Par conséquent, il sert aussi d’exemple pour créer un écran personnalisé."

    # screens.rpy:551
    old "## This use statement includes the game_menu screen inside this one. The vbox child is then included inside the viewport inside the game_menu screen."
    new "## Cette déclaration concerne l’écran game_menu. L’élément vbox est ensuite inclus dans la fenêtre de l'écran game_menu."

    # screens.rpy:561
    old "Version [config.version!t]\n"
    new "Version [config.version!t]\n"

    # screens.rpy:563
    old "## gui.about is usually set in options.rpy."
    new "## gui.about est généralement initialisé dans le fichier options.rpy."

    # screens.rpy:567
    old "Made with {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only].\n\n[renpy.license!t]"
    new "Conçu avec {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only].\n\n[renpy.license!t]"

    # screens.rpy:570
    old "## This is redefined in options.rpy to add text to the about screen."
    new "## Ceci est généralement redéfini dans le fichier options.rpy  pour ajouter le texte dans l’écran « À propos »."

    # screens.rpy:582
    old "## Load and Save screens"
    new "## Écran de chargement et de sauvegarde"

    # screens.rpy:584
    old "## These screens are responsible for letting the player save the game and load it again. Since they share nearly everything in common, both are implemented in terms of a third screen, file_slots."
    new "## Ces écrans permettent au joueur d’enregistrer le jeu et de le charger à nouveau. Comme ils partagent beaucoup d’éléments communs, ils sont tous les deux implémentés dans un troisième écran, appelé fichiers_slots (emplacement_de_fichier)."

    # screens.rpy:588
    old "## https://www.renpy.org/doc/html/screen_special.html#save https://www.renpy.org/doc/html/screen_special.html#load"
    new "## https://www.renpy.org/doc/html/screen_special.html#save https://www.renpy.org/doc/html/screen_special.html#load"

    # screens.rpy:607
    old "Page {}"
    new "Page {}"

    # screens.rpy:607
    old "Automatic saves"
    new "Sauvegardes automatiques"

    # screens.rpy:607
    old "Quick saves"
    new "Sauvegardes rapides"

    # screens.rpy:613
    old "## This ensures the input will get the enter event before any of the buttons do."
    new "## Cette instruction s’assure que l’évènement enter aura lieu avant que l’un des boutons ne fonctionne."

    # screens.rpy:629
    old "## The grid of file slots."
    new "## La grille des emplacements de fichiers."

    # screens.rpy:649
    old "{#file_time}%A, %B %d %Y, %H:%M"
    new "{#file_time}%A %d %B %Y, %H:%M"

    # screens.rpy:649
    old "empty slot"
    new "emplacement vide"

    # screens.rpy:657
    old "## Buttons to access other pages."
    new "## Boutons pour accéder aux autres pages."

    # screens.rpy:666
    old "<"
    new "<"

    # screens.rpy:668
    old "{#auto_page}A"
    new "{#auto_page}A"

    # screens.rpy:670
    old "{#quick_page}Q"
    new "{#quick_page}Q"

    # screens.rpy:676
    old ">"
    new ">"

    # screens.rpy:711
    old "## Preferences screen"
    new "## Écran des préférences"

    # screens.rpy:713
    old "## The preferences screen allows the player to configure the game to better suit themselves."
    new "## L’écran de préférences permet au joueur de configurer le jeu pour mieux correspondre à ses attentes."

    # screens.rpy:716
    old "## https://www.renpy.org/doc/html/screen_special.html#preferences"
    new "## https://www.renpy.org/doc/html/screen_special.html#preferences"

    # screens.rpy:738
    old "Display"
    new "Affichage"

    # screens.rpy:739
    old "Window"
    new "Fenêtre"

    # screens.rpy:740
    old "Fullscreen"
    new "Plein écran"

    # screens.rpy:744
    old "Rollback Side"
    new "Rembobinage côté"

    # screens.rpy:745
    old "Disable"
    new "Désactivé"

    # screens.rpy:746
    old "Left"
    new "Gauche"

    # screens.rpy:747
    old "Right"
    new "Droite"

    # screens.rpy:752
    old "Unseen Text"
    new "Texte non lu"

    # screens.rpy:753
    old "After Choices"
    new "Après les choix"

    # screens.rpy:754
    old "Transitions"
    new "Transitions"

    # screens.rpy:756
    old "## Additional vboxes of type \"radio_pref\" or \"check_pref\" can be added here, to add additional creator-defined preferences."
    new "## Des boites vbox additionnelles de type \"radio_pref\" ou \"check_pref\" peuvent être ajoutées ici pour ajouter des préférences définies par le créateur du jeu."

    # screens.rpy:767
    old "Text Speed"
    new "Vitesse du texte"

    # screens.rpy:771
    old "Auto-Forward Time"
    new "Avance automatique"

    # screens.rpy:778
    old "Music Volume"
    new "Volume de la musique"

    # screens.rpy:785
    old "Sound Volume"
    new "Volume des sons"

    # screens.rpy:791
    old "Test"
    new "Test"

    # screens.rpy:795
    old "Voice Volume"
    new "Volume des voix"

    # screens.rpy:806
    old "Mute All"
    new "Couper tous les sons"

    # screens.rpy:882
    old "## History screen"
    new "## Écran de l'historique"

    # screens.rpy:884
    old "## This is a screen that displays the dialogue history to the player. While there isn't anything special about this screen, it does have to access the dialogue history stored in _history_list."
    new "## Il s’agit d’un écran qui affiche l’historique des dialogues au joueur. Bien qu’il n'y ait rien de spécial sur cet écran, il doit accéder à l’historique de dialogue stocké dans _history_list."

    # screens.rpy:888
    old "## https://www.renpy.org/doc/html/history.html"
    new "## https://www.renpy.org/doc/html/history.html"

    # screens.rpy:894
    old "## Avoid predicting this screen, as it can be very large."
    new "## Cette instruction permet d’éviter de prédire cet écran, car il peut être très large"

    # screens.rpy:905
    old "## This lays things out properly if history_height is None."
    new "## Cela positionne correctement l'écran si history_height est initialisé à None."

    # screens.rpy:914
    old "## Take the color of the who text from the Character, if set."
    new "## Utilise pour la couleur du texte, la couleur par défaut des dialogues du personnage si elle a été initialisée."

    # screens.rpy:921
    old "The dialogue history is empty."
    new "L'historique des dialogues est vide."

    # screens.rpy:965
    old "## Help screen"
    new "## Écran d'aide"

    # screens.rpy:967
    old "## A screen that gives information about key and mouse bindings. It uses other screens (keyboard_help, mouse_help, and gamepad_help) to display the actual help."
    new "## Cet écran fournit des informations sur les touches et les boutons de souris. En interne, il utilise d’autres écrans (keyboard_help, mouse_help et gamepad_help) pour afficher une aide dédiée."

    # screens.rpy:986
    old "Keyboard"
    new "Clavier"

    # screens.rpy:987
    old "Mouse"
    new "Souris"

    # screens.rpy:990
    old "Gamepad"
    new "Manette"

    # screens.rpy:1003
    old "Enter"
    new "Entrée"

    # screens.rpy:1004
    old "Advances dialogue and activates the interface."
    new "Avance dans les dialogues et active l’interface (effectue un choix)."

    # screens.rpy:1007
    old "Space"
    new "Espace"

    # screens.rpy:1008
    old "Advances dialogue without selecting choices."
    new "Avance dans les dialogues sans effectuer de choix."

    # screens.rpy:1011
    old "Arrow Keys"
    new "Flèches directionnelles"

    # screens.rpy:1012
    old "Navigate the interface."
    new "Permet de se déplacer dans l’interface."

    # screens.rpy:1015
    old "Escape"
    new "Echap."

    # screens.rpy:1016
    old "Accesses the game menu."
    new "Ouvre le menu du jeu."

    # screens.rpy:1019
    old "Ctrl"
    new "Ctrl"

    # screens.rpy:1020
    old "Skips dialogue while held down."
    new "Fait défiler les dialogues tant que la touche est pressée."

    # screens.rpy:1023
    old "Tab"
    new "Tab"

    # screens.rpy:1024
    old "Toggles dialogue skipping."
    new "Active ou désactive les «sauts des dialogues»."

    # screens.rpy:1027
    old "Page Up"
    new "Page Haut"

    # screens.rpy:1028
    old "Rolls back to earlier dialogue."
    new "Retourne au précédent dialogue."

    # screens.rpy:1031
    old "Page Down"
    new "Page Bas"

    # screens.rpy:1032
    old "Rolls forward to later dialogue."
    new "Avance jusqu'au prochain dialogue."

    # screens.rpy:1036
    old "Hides the user interface."
    new "Cache l’interface utilisateur."

    # screens.rpy:1040
    old "Takes a screenshot."
    new "Prend une capture d’écran."

    # screens.rpy:1044
    old "Toggles assistive {a=https://www.renpy.org/l/voicing}self-voicing{/a}."
    new "Active la {a=https://www.renpy.org/l/voicing}{size=24}vocalisation automatique{/size}{/a}."

    # screens.rpy:1050
    old "Left Click"
    new "Bouton gauche"

    # screens.rpy:1054
    old "Middle Click"
    new "Bouton central"

    # screens.rpy:1058
    old "Right Click"
    new "Bouton droit"

    # screens.rpy:1062
    old "Molette vers le haut\nBouton de retour en arrière"
    new "Mouse Wheel Up\nClic du côté rembobinage"

    # screens.rpy:1066
    old "Mouse Wheel Down"
    new "Molette vers le bas"

    # screens.rpy:1073
    old "Right Trigger\nA/Bottom Button"
    new "Bouton R1\nA/Bouton du bas"

    # screens.rpy:1074
    old "Advance dialogue and activates the interface."
    new "Avance dans les dialogues et active les choix dans l'interface."

    # screens.rpy:1078
    old "Roll back to earlier dialogue."
    new "Retourne au précédent dialogue."

    # screens.rpy:1081
    old "Right Shoulder"
    new "Bouton R1"

    # screens.rpy:1082
    old "Roll forward to later dialogue."
    new "Avance jusqu'au prochain dialogue."

    # screens.rpy:1085
    old "D-Pad, Sticks"
    new "Boutons directionnels, stick gauche"

    # screens.rpy:1089
    old "Start, Guide"
    new "Start, Guide"

    # screens.rpy:1090
    old "Access the game menu."
    new "Ouvre le menu du jeu."

    # screens.rpy:1093
    old "Y/Top Button"
    new "Y/Bouton du haut"

    # screens.rpy:1096
    old "Calibrate"
    new "Calibrage"

    # screens.rpy:1124
    old "## Additional screens"
    new "## Écrans additionnels"

    # screens.rpy:1128
    old "## Confirm screen"
    new "## Écran de confirmation"

    # screens.rpy:1130
    old "## The confirm screen is called when Ren'Py wants to ask the player a yes or no question."
    new "## Cet écran est appelé quand Ren'Py souhaite poser une question au joueur dont la réponse est oui ou non."

    # screens.rpy:1133
    old "## http://www.renpy.org/doc/html/screen_special.html#confirm"
    new "## http://www.renpy.org/doc/html/screen_special.html#confirm"

    # screens.rpy:1137
    old "## Ensure other screens do not get input while this screen is displayed."
    new "## Cette instruction s’assure que les autres écrans resteront en arrière plan tant que cet écran sera affiché."

    # screens.rpy:1161
    old "Yes"
    new "Oui"

    # screens.rpy:1162
    old "No"
    new "Non"

    # screens.rpy:1164
    old "## Right-click and escape answer \"no\"."
    new "## Le clic bouton droit et la touche Echap. correspondent à la réponse \"non\"."

    # screens.rpy:1191
    old "## Skip indicator screen"
    new "## Écran de l’indicateur d'avance rapide"

    # screens.rpy:1193
    old "## The skip_indicator screen is displayed to indicate that skipping is in progress."
    new "## L’écran skip_indicator est affiché pour indiquer qu’une avance rapide est en cours."

    # screens.rpy:1196
    old "## https://www.renpy.org/doc/html/screen_special.html#skip-indicator"
    new "## https://www.renpy.org/doc/html/screen_special.html#skip-indicator"

    # screens.rpy:1208
    old "Skipping"
    new "Avance rapide"

    # screens.rpy:1215
    old "## This transform is used to blink the arrows one after another."
    new "## Cette transformation est utilisé pour faire clignoter les flèches l’une après l’autre."

    # screens.rpy:1247
    old "## Notify screen"
    new "## Écran de notification"

    # screens.rpy:1249
    old "## The notify screen is used to show the player a message. (For example, when the game is quicksaved or a screenshot has been taken.)"
    new "## Cet écran est utilisé pour affiché un message au joueur. (Par exemple, quand une sauvegarde rapide a eu lieu ou quand une capture d’écran vient d’être réalisée.)"

    # screens.rpy:1252
    old "## https://www.renpy.org/doc/html/screen_special.html#notify-screen"
    new "## https://www.renpy.org/doc/html/screen_special.html#notify-screen"

    # screens.rpy:1286
    old "## NVL screen"
    new "## Écran NVL"

    # screens.rpy:1288
    old "## This screen is used for NVL-mode dialogue and menus."
    new "## Cet écran est utilisé pour les dialogues et les menus en mode NVL."

    # screens.rpy:1290
    old "## http://www.renpy.org/doc/html/screen_special.html#nvl"
    new "## http://www.renpy.org/doc/html/screen_special.html#nvl"

    # screens.rpy:1301
    old "## Displays dialogue in either a vpgrid or the vbox."
    new "## Les dialogues sont affichés soit dans une vpgrid soit dans une vbox."

    # screens.rpy:1314
    old "## Displays the menu, if given. The menu may be displayed incorrectly if config.narrator_menu is set to True."
    new "## Si fourni, affiche le menu. Le menu peut s’afficher de manière incorrecte si config.narrator_menu est initialisé à True."

    # screens.rpy:1344
    old "## This controls the maximum number of NVL-mode entries that can be displayed at once."
    new "## Ce paramètre contrôle le maximum d’entrée dans le mode NVL qui peuvent être affichée simultanément."

    # screens.rpy:1406
    old "## Mobile Variants"
    new "## Variantes pour les mobiles"

    # screens.rpy:1413
    old "## Since a mouse may not be present, we replace the quick menu with a version that uses fewer and bigger buttons that are easier to touch."
    new "## Comme la souris peut ne pas être présente, nous remplaçons le menu rapide avec une version qui utilise des boutons plus gros et qui sont plus faciles à toucher du doigt."

    # screens.rpy:1429
    old "Menu"
    new "Menu"

    # gui/game/screens.rpy:114
    old "## If there's a side image, display it above the text. Do not display on the phone variant - there's no room."
    new "## Si il y a une side image, l'afficher au-dessus du texte. Ne pas l'afficher sur la version téléphone - pas assez de place."

    # gui/game/screens.rpy:120
    old "## Make the namebox available for styling through the Character object."
    new "## Rendre la boîte du nom personnalisable à travers l'objet Character."

    # gui/game/screens.rpy:172
    old "## https://www.renpy.org/doc/html/screen_special.html#input"
    new "## https://www.renpy.org/doc/html/screen_special.html#input"

    # gui/game/screens.rpy:205
    old "## https://www.renpy.org/doc/html/screen_special.html#choice"
    new "## https://www.renpy.org/doc/html/screen_special.html#choice"

    # gui/game/screens.rpy:245
    old "## Ensure this appears on top of other screens."
    new "## Assure qu'il apparaît au-dessus des autres screens."

    # gui/game/screens.rpy:284
    old "## Main and Game Menu Screens"
    new "## Screens du menu principal et du menu de jeu"

    # gui/game/screens.rpy:333
    old "## The quit button is banned on iOS and unnecessary on Android and Web."
    new "## Le bouton pour quitter est banni sur iOS et inutile sur Android et sur le Web."

    # gui/game/screens.rpy:352
    old "## https://www.renpy.org/doc/html/screen_special.html#main-menu"
    new "## https://www.renpy.org/doc/html/screen_special.html#main-menu"

    # gui/game/screens.rpy:356
    old "## This ensures that any other menu screen is replaced."
    new "## Ceci assure que tout autre screen de menu est remplacé."

    # gui/game/screens.rpy:361
    old "## This empty frame darkens the main menu."
    new "## Cette frame vide obscurcit le menu principal."

    # gui/game/screens.rpy:433
    old "## Reserve space for the navigation section."
    new "## Réserve de l'expace pour la section de navigation."

    # gui/game/screens.rpy:612
    old "## The page name, which can be edited by clicking on a button."
    new "## Le nom de la page, qui peut être modifié en cliquant sur un bouton."

    # gui/game/screens.rpy:669
    old "## range(1, 10) gives the numbers from 1 to 9."
    new "## range(1, 10) donne les nombres de 1 à 9."

    # gui/game/screens.rpy:919
    old "## This determines what tags are allowed to be displayed on the history screen."
    new "## Ceci détermine quels tags peuvent être affichés sur le screen de l'historique."

    # gui/game/screens.rpy:1063
    old "Mouse Wheel Up\nClick Rollback Side"
    new "Molette vers le haut\nClic sur le côté du Rollback"

    # gui/game/screens.rpy:1078
    old "Left Trigger\nLeft Shoulder"
    new "Gâchettes gauche"

    # gui/game/screens.rpy:1135
    old "## https://www.renpy.org/doc/html/screen_special.html#confirm"
    new "## https://www.renpy.org/doc/html/screen_special.html#confirm"

    # gui/game/screens.rpy:1244
    old "## We have to use a font that has the BLACK RIGHT-POINTING SMALL TRIANGLE glyph in it."
    new "## Nous devons utiliser une police qui a le glyphe BLACK RIGHT-POINTING SMALL TRIANGLE."

    # gui/game/screens.rpy:1292
    old "## https://www.renpy.org/doc/html/screen_special.html#nvl"
    new "## https://www.renpy.org/doc/html/screen_special.html#nvl"

    # gui/game/screens.rpy:1049
    old "Opens the accessibility menu."
    new "Ouvre le menu d'accessibilité."

    # gui/game/screens.rpy:1397
    old "## Bubble screen"
    new "## Screen des bulles"

    # gui/game/screens.rpy:1412
    old "## The bubble screen is used to display dialogue to the player when using speech bubbles. The bubble screen takes the same parameters as the say screen, must create a displayable with the id of \"what\", and can create displayables with the \"namebox\", \"who\", and \"window\" ids."
    new "## Le screen des bulles est utilisé pour afficher des dialogues en utilisant des bulles de dialogue. Ce screen prend les mêmes paramètres que le screen say, doit prévoir un displayable avec l'id \"what\", et peut créer des displayables avec les ids \"namebox\", \"who\", et \"window\"."

    # gui/game/screens.rpy:1417
    old "## https://www.renpy.org/doc/html/bubble.html#bubble-screen"
    new "## https://www.renpy.org/doc/html/bubble.html#bubble-screen"

    # gui/game/screens.rpy:676
    old "Upload Sync"
    new "Uploader Sync"

    # gui/game/screens.rpy:680
    old "Download Sync"
    new "Télécharger Sync"
