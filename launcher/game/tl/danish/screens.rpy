translate danish strings:

    # gui/game/screens.rpy:9
    old "## Styles"
    new "## Stile"

    # gui/game/screens.rpy:81
    old "## In-game screens"
    new "## Skærme i spillet"

    # gui/game/screens.rpy:85
    old "## Say screen"
    new "## Dialogskærmen"

    # gui/game/screens.rpy:87
    old "## The say screen is used to display dialogue to the player. It takes two parameters, who and what, which are the name of the speaking character and the text to be displayed, respectively. (The who parameter can be None if no name is given.)"
    new "## Dialogskærmen bruges til at vise dialog til spilleren. Den tager to parametre, who (hvem) og what (hvad), som henholdsvis er navnet på den talende figur og teksten, der skal vises. (Parametren who kan være None, hvis intet navn angives.)"

    # gui/game/screens.rpy:92
    old "## This screen must create a text displayable with id \"what\", as Ren'Py uses this to manage text display. It can also create displayables with id \"who\" and id \"window\" to apply style properties."
    new "## Denne skærm skal oprette et visbart tekstelement med id'et \"what\", da Ren'Py bruger denne til at styre tekstvisning. Den kan også oprette visbare elementer med id'et \"who\" og id'et \"window\" for at anvende stilegenskaber."

    # gui/game/screens.rpy:96
    old "## https://www.renpy.org/doc/html/screen_special.html#say"
    new "## https://www.renpy.org/doc/html/screen_special.html#say"

    # gui/game/screens.rpy:114
    old "## If there's a side image, display it above the text. Do not display on the phone variant - there's no room."
    new "## Hvis der er et sidebillede, så vis det over teksten. Vis ikke på mobilvarianten - der er ikke plads."

    # gui/game/screens.rpy:120
    old "## Make the namebox available for styling through the Character object."
    new "## Gør navneboksen tilgængelig for stilisering gennem Character-objektet."

    # gui/game/screens.rpy:165
    old "## Input screen"
    new "## Inputskærmen"

    # gui/game/screens.rpy:167
    old "## This screen is used to display renpy.input. The prompt parameter is used to pass a text prompt in."
    new "## Denne skærm bruges til at vise renpy.input. Promptparameteren bruges til at føre en tekstprompt ind."

    # gui/game/screens.rpy:170
    old "## This screen must create an input displayable with id \"input\" to accept the various input parameters."
    new "## Denne skærm skal oprette et visbart inputelement med id'et \"input\" for at acceptere de forskellige inputparametre."

    # gui/game/screens.rpy:173
    old "## https://www.renpy.org/doc/html/screen_special.html#input"
    new "## https://www.renpy.org/doc/html/screen_special.html#input"

    # gui/game/screens.rpy:200
    old "## Choice screen"
    new "## Valgmulighedsskærmen"

    # gui/game/screens.rpy:202
    old "## This screen is used to display the in-game choices presented by the menu statement. The one parameter, items, is a list of objects, each with caption and action fields."
    new "## Denne skærm bruges til at vise valg i spillet præsenteret af menu-sætningen. Den ene parameter, items, er en liste af objekter, hver med caption- og action-felter."

    # gui/game/screens.rpy:206
    old "## https://www.renpy.org/doc/html/screen_special.html#choice"
    new "## https://www.renpy.org/doc/html/screen_special.html#choice"

    # gui/game/screens.rpy:234
    old "## Quick Menu screen"
    new "## Hurtigmenuskærmen"

    # gui/game/screens.rpy:236
    old "## The quick menu is displayed in-game to provide easy access to the out-of-game menus."
    new "## Hurtigmenuen vises i spillet for at give let adgang til menuerne uden for spillet."

    # gui/game/screens.rpy:241
    old "## Ensure this appears on top of other screens."
    new "## Sørg for at denne vises oven på andre skærme."

    # gui/game/screens.rpy:252
    old "Back"
    new "Tilbage"

    # gui/game/screens.rpy:253
    old "History"
    new "Historik"

    # gui/game/screens.rpy:254
    old "Skip"
    new "Spring over"

    # gui/game/screens.rpy:255
    old "Auto"
    new "Auto"

    # gui/game/screens.rpy:256
    old "Save"
    new "Gem"

    # gui/game/screens.rpy:257
    old "Q.Save"
    new "H.gem"

    # gui/game/screens.rpy:258
    old "Q.Load"
    new "H.indlæs"

    # gui/game/screens.rpy:259
    old "Prefs"
    new "Præf."

    # gui/game/screens.rpy:262
    old "## This code ensures that the quick_menu screen is displayed in-game, whenever the player has not explicitly hidden the interface."
    new "## Denne kode sørger for at quick_menu-skærmen vises i spillet, når end spilleren ikke eksplicit har skjult grænsefladen."

    # gui/game/screens.rpy:280
    old "## Main and Game Menu Screens"
    new "## Hoved- og spilmenuskærme"

    # gui/game/screens.rpy:283
    old "## Navigation screen"
    new "## Navigationsskærmen"

    # gui/game/screens.rpy:285
    old "## This screen is included in the main and game menus, and provides navigation to other menus, and to start the game."
    new "## Denne skærm er inkluderet i hoved- og spilmenuerne og giver navigation til andre menuer og til at starte spillet."

    # gui/game/screens.rpy:300
    old "Start"
    new "Start"

    # gui/game/screens.rpy:308
    old "Load"
    new "Indlæs"

    # gui/game/screens.rpy:310
    old "Preferences"
    new "Præferencer"

    # gui/game/screens.rpy:314
    old "End Replay"
    new "Slut genafspilning"

    # gui/game/screens.rpy:318
    old "Main Menu"
    new "Hovedmenu"

    # gui/game/screens.rpy:320
    old "About"
    new "Om"

    # gui/game/screens.rpy:324
    old "## Help isn't necessary or relevant to mobile devices."
    new "## Hjælp er ikke nødvendig eller relevant for mobilenheder."

    # gui/game/screens.rpy:325
    old "Help"
    new "Hjælp"

    # gui/game/screens.rpy:329
    old "## The quit button is banned on iOS and unnecessary on Android and Web."
    new "## Afslut-knappen er forbudt på iOS og unødvendig på Android og web."

    # gui/game/screens.rpy:330
    old "Quit"
    new "Afslut"

    # gui/game/screens.rpy:344
    old "## Main Menu screen"
    new "## Hovedmenuskærmen"

    # gui/game/screens.rpy:346
    old "## Used to display the main menu when Ren'Py starts."
    new "## Bruges til at vise hovedmenuen, når Ren'Py starter."

    # gui/game/screens.rpy:348
    old "## https://www.renpy.org/doc/html/screen_special.html#main-menu"
    new "## https://www.renpy.org/doc/html/screen_special.html#main-menu"

    # gui/game/screens.rpy:352
    old "## This ensures that any other menu screen is replaced."
    new "## Dette sikrer, at andre eventuelle menuskærme erstattes."

    # gui/game/screens.rpy:357
    old "## This empty frame darkens the main menu."
    new "## Denne tomme ramme mørkner hovedmenuen."

    # gui/game/screens.rpy:361
    old "## The use statement includes another screen inside this one. The actual contents of the main menu are in the navigation screen."
    new "## Sætningen use inkluderer en anden skærm inde i denne. Det faktiske indhold af hovedmenuen er i navigationsskærmen."

    # gui/game/screens.rpy:406
    old "## Game Menu screen"
    new "## Spilmenuskærmen"

    # gui/game/screens.rpy:408
    old "## This lays out the basic common structure of a game menu screen. It's called with the screen title, and displays the background, title, and navigation."
    new "## Denne udlægger de grundlæggende fællesstrukturer for en spilmenuskærm. Den kaldes med screen-titlen og viser baggrunden, titlen og navigationen."

    # gui/game/screens.rpy:411
    old "## The scroll parameter can be None, or one of \"viewport\" or \"vpgrid\". This screen is intended to be used with one or more children, which are transcluded (placed) inside it."
    new "## Parameteren scroll kan være None eller en af \"viewport\" eller \"vpgrid\". Denne skærm er tiltænkt at blive brugt med et eller flere børn, som transkluderes (placeres) inde i den."

    # gui/game/screens.rpy:429
    old "## Reserve space for the navigation section."
    new "## Reserver plads til navigationssektionen"

    # gui/game/screens.rpy:471
    old "Return"
    new "Tilbage"

    # gui/game/screens.rpy:534
    old "## About screen"
    new "## Om-skærmen"

    # gui/game/screens.rpy:536
    old "## This screen gives credit and copyright information about the game and Ren'Py."
    new "## Denne skærm giver kreditering og ophavsretsinformation om spillet og Ren'Py."

    # gui/game/screens.rpy:539
    old "## There's nothing special about this screen, and hence it also serves as an example of how to make a custom screen."
    new "## Der er intet specielt ved denne skærm, og derfor fungerer den også som et eksempel, på hvordan man laver en skræddersyet skærm."

    # gui/game/screens.rpy:546
    old "## This use statement includes the game_menu screen inside this one. The vbox child is then included inside the viewport inside the game_menu screen."
    new "## Denne use-sætning inkluderer game_menu-skærmen inde i denne. Barnet vbox inkluderes derefter inde i visningsporten inde i game_menu-skærmen."

    # gui/game/screens.rpy:556
    old "Version [config.version!t]\n"
    new "Version [config.version!t]\n"

    # gui/game/screens.rpy:558
    old "## gui.about is usually set in options.rpy."
    new "## gui.about indstilles sædvanligvis i options.rpy."

    # gui/game/screens.rpy:562
    old "Made with {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only].\n\n[renpy.license!t]"
    new "Lavet med {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only].\n\n[renpy.license!t]"

    # gui/game/screens.rpy:573
    old "## Load and Save screens"
    new "## Indlæsnings- og gemmeskærmene"

    # gui/game/screens.rpy:575
    old "## These screens are responsible for letting the player save the game and load it again. Since they share nearly everything in common, both are implemented in terms of a third screen, file_slots."
    new "## Disse skærme er ansvarlige for at lade spilleren gemme spillet og indlæse det igen. Siden de har næsten alting tilfælles, implementeres begge i form af en tredje skærm, file_slots."

    # gui/game/screens.rpy:579
    old "## https://www.renpy.org/doc/html/screen_special.html#save https://www.renpy.org/doc/html/screen_special.html#load"
    new "## https://www.renpy.org/doc/html/screen_special.html#save https://www.renpy.org/doc/html/screen_special.html#load"

    # gui/game/screens.rpy:598
    old "Page {}"
    new "Side {}"

    # gui/game/screens.rpy:598
    old "Automatic saves"
    new "Autogemmefiler"

    # gui/game/screens.rpy:598
    old "Quick saves"
    new "Hurtiggemmefiler"

    # gui/game/screens.rpy:604
    old "## This ensures the input will get the enter event before any of the buttons do."
    new "## Dette sikrer, at inputtet får enter-begivenheden før nogen af knapperne gør."

    # gui/game/screens.rpy:608
    old "## The page name, which can be edited by clicking on a button."
    new "## Sidenavnet, som kan redigeres ved at klikke på en knap."

    # gui/game/screens.rpy:620
    old "## The grid of file slots."
    new "## Filpladsgitteret."

    # gui/game/screens.rpy:640
    old "{#file_time}%A, %B %d %Y, %H:%M"
    new "{#file_time}%A, %d %B %Y, %H:%M"

    # gui/game/screens.rpy:640
    old "empty slot"
    new "tom plads"

    # gui/game/screens.rpy:648
    old "## Buttons to access other pages."
    new "## Knapper til at tilgå andre sider."

    # gui/game/screens.rpy:660
    old "<"
    new "<"

    # gui/game/screens.rpy:663
    old "{#auto_page}A"
    new "{#auto_page}A"

    # gui/game/screens.rpy:666
    old "{#quick_page}Q"
    new "{#quick_page}H"

    # gui/game/screens.rpy:668
    old "## range(1, 10) gives the numbers from 1 to 9."
    new "## range(1, 10) giver numrene fra 1 til 9."

    # gui/game/screens.rpy:672
    old ">"
    new ">"

    # gui/game/screens.rpy:676
    old "Upload Sync"
    new "Send synkronisering"

    # gui/game/screens.rpy:680
    old "Download Sync"
    new "Hent synkronisering"

    # gui/game/screens.rpy:717
    old "## Preferences screen"
    new "## Præferenceskærmen"

    # gui/game/screens.rpy:719
    old "## The preferences screen allows the player to configure the game to better suit themselves."
    new "## Præferenceskærmen gør det muligt for spilleren at konfigurere spillet til bedre at passe vedkommende."

    # gui/game/screens.rpy:722
    old "## https://www.renpy.org/doc/html/screen_special.html#preferences"
    new "## https://www.renpy.org/doc/html/screen_special.html#preferences"

    # gui/game/screens.rpy:739
    old "Display"
    new "Skærmvisning"

    # gui/game/screens.rpy:740
    old "Window"
    new "Vindue"

    # gui/game/screens.rpy:741
    old "Fullscreen"
    new "Fuldskærm"

    # gui/game/screens.rpy:746
    old "Unseen Text"
    new "Uset tekst"

    # gui/game/screens.rpy:747
    old "After Choices"
    new "Efter valg"

    # gui/game/screens.rpy:748
    old "Transitions"
    new "Overgange"

    # gui/game/screens.rpy:750
    old "## Additional vboxes of type \"radio_pref\" or \"check_pref\" can be added here, to add additional creator-defined preferences."
    new "## Yderligere vboxe af typen \"radio_pref\" eller \"check_pref\" kan tilføjes her for at tilføje yderligere udviklerdefinerede præferencer."

    # gui/game/screens.rpy:761
    old "Text Speed"
    new "Teksthastighed"

    # gui/game/screens.rpy:765
    old "Auto-Forward Time"
    new "Tid for auto-fremad"

    # gui/game/screens.rpy:772
    old "Music Volume"
    new "Musiklydstyrke"

    # gui/game/screens.rpy:779
    old "Sound Volume"
    new "Lydeffektlydstyrke"

    # gui/game/screens.rpy:785
    old "Test"
    new "Test"

    # gui/game/screens.rpy:789
    old "Voice Volume"
    new "Stemmelydstyrke"

    # gui/game/screens.rpy:800
    old "Mute All"
    new "Slå alle fra"

    # gui/game/screens.rpy:876
    old "## History screen"
    new "## Historikskærmen"

    # gui/game/screens.rpy:878
    old "## This is a screen that displays the dialogue history to the player. While there isn't anything special about this screen, it does have to access the dialogue history stored in _history_list."
    new "## Dette er en skærm, der viser dialoghistorikken til spilleren. Mens der ikke er noget særligt ved denne skærm, har den dog adgang til dialoghistorikken opbevaret i _history_list."

    # gui/game/screens.rpy:882
    old "## https://www.renpy.org/doc/html/history.html"
    new "## https://www.renpy.org/doc/html/history.html"

    # gui/game/screens.rpy:888
    old "## Avoid predicting this screen, as it can be very large."
    new "## Undgå at forudsige denne skærm, da den kan være meget stor."

    # gui/game/screens.rpy:899
    old "## This lays things out properly if history_height is None."
    new "## Dette udlægger tingene korrekt, hvis history_height er None."

    # gui/game/screens.rpy:909
    old "## Take the color of the who text from the Character, if set."
    new "## Tag farven fra who-teksten fra en Character, hvis den er angivet."

    # gui/game/screens.rpy:918
    old "The dialogue history is empty."
    new "Dialoghistorikken er tom."

    # gui/game/screens.rpy:921
    old "## This determines what tags are allowed to be displayed on the history screen."
    new "## Dette bestemmer, hvilke mærker der tillades at blive vist på historikskærmen."

    # gui/game/screens.rpy:966
    old "## Help screen"
    new "## Hjælpeskærmen"

    # gui/game/screens.rpy:968
    old "## A screen that gives information about key and mouse bindings. It uses other screens (keyboard_help, mouse_help, and gamepad_help) to display the actual help."
    new "## En skærm, der giver information om tastatur- og musetildelinger. Den bruger andre skærme (keyboard_help, mouse_help og gamepad_help) til at vise den faktiske hjælp."

    # gui/game/screens.rpy:987
    old "Keyboard"
    new "Tastatur"

    # gui/game/screens.rpy:988
    old "Mouse"
    new "Mus"

    # gui/game/screens.rpy:991
    old "Gamepad"
    new "Spillekontrol"

    # gui/game/screens.rpy:1004
    old "Enter"
    new "Retur"

    # gui/game/screens.rpy:1005
    old "Advances dialogue and activates the interface."
    new "Går videre i dialog og aktiverer grænsefladen."

    # gui/game/screens.rpy:1008
    old "Space"
    new "Mellemrum"

    # gui/game/screens.rpy:1009
    old "Advances dialogue without selecting choices."
    new "Går videre i dialog uden at træffe valg."

    # gui/game/screens.rpy:1012
    old "Arrow Keys"
    new "Piltaster"

    # gui/game/screens.rpy:1013
    old "Navigate the interface."
    new "Navigerer i grænsefladen."

    # gui/game/screens.rpy:1016
    old "Escape"
    new "Escape"

    # gui/game/screens.rpy:1017
    old "Accesses the game menu."
    new "Tilgår spilmenuen."

    # gui/game/screens.rpy:1020
    old "Ctrl"
    new "Ctrl"

    # gui/game/screens.rpy:1021
    old "Skips dialogue while held down."
    new "Springer over dialog ved nedholdning."

    # gui/game/screens.rpy:1024
    old "Tab"
    new "Tab"

    # gui/game/screens.rpy:1025
    old "Toggles dialogue skipping."
    new "Slår dialogoverspringning til/fra."

    # gui/game/screens.rpy:1028
    old "Page Up"
    new "Page Up"

    # gui/game/screens.rpy:1029
    old "Rolls back to earlier dialogue."
    new "Ruller tilbage til tidligere dialog."

    # gui/game/screens.rpy:1032
    old "Page Down"
    new "Page Down"

    # gui/game/screens.rpy:1033
    old "Rolls forward to later dialogue."
    new "Ruller fremad til senere dialog."

    # gui/game/screens.rpy:1037
    old "Hides the user interface."
    new "Skjuler brugerfladen."

    # gui/game/screens.rpy:1041
    old "Takes a screenshot."
    new "Tager et skærmbillede."

    # gui/game/screens.rpy:1045
    old "Toggles assistive {a=https://www.renpy.org/l/voicing}self-voicing{/a}."
    new "Slår assisterende {a=https://www.renpy.org/l/voicing}automatisk oplæsning{/a} til/fra."

    # gui/game/screens.rpy:1049
    old "Opens the accessibility menu."
    new "Åbner tilgængelighedsmenuen."

    # gui/game/screens.rpy:1055
    old "Left Click"
    new "Venstreklik"

    # gui/game/screens.rpy:1059
    old "Middle Click"
    new "Midterklik"

    # gui/game/screens.rpy:1063
    old "Right Click"
    new "Højreklik"

    # gui/game/screens.rpy:1067
    old "Mouse Wheel Up\nClick Rollback Side"
    new "Musehjul op\nKlik på tilbagerulningsside"

    # gui/game/screens.rpy:1071
    old "Mouse Wheel Down"
    new "Musehjul ned"

    # gui/game/screens.rpy:1078
    old "Right Trigger\nA/Bottom Button"
    new "Højre aftrækker\nA/Nederste knap"

    # gui/game/screens.rpy:1082
    old "Left Trigger\nLeft Shoulder"
    new "Venstre aftrækker\nVenstre skulderknap"

    # gui/game/screens.rpy:1086
    old "Right Shoulder"
    new "Højre skulderknap"

    # gui/game/screens.rpy:1091
    old "D-Pad, Sticks"
    new "Retningsknapper, Pinde"

    # gui/game/screens.rpy:1095
    old "Start, Guide"
    new "Start, Guide"

    # gui/game/screens.rpy:1098
    old "Start, Guide, B/Right Button"
    new "Start, Guide, B/Højre knap"

    # gui/game/screens.rpy:1099
    old "Y/Top Button"
    new "Y/Øverste knap"

    # gui/game/screens.rpy:1102
    old "Calibrate"
    new "Kalibrér"

    # gui/game/screens.rpy:1130
    old "## Additional screens"
    new "## Yderligere skærme"

    # gui/game/screens.rpy:1134
    old "## Confirm screen"
    new "## Bekræftelsesskærmen"

    # gui/game/screens.rpy:1136
    old "## The confirm screen is called when Ren'Py wants to ask the player a yes or no question."
    new "## Bekræftelsesskærmen kaldes, når Ren'Py vil stille spilleren et ja-nej-spørgsmål."

    # gui/game/screens.rpy:1139
    old "## https://www.renpy.org/doc/html/screen_special.html#confirm"
    new "## https://www.renpy.org/doc/html/screen_special.html#confirm"

    # gui/game/screens.rpy:1143
    old "## Ensure other screens do not get input while this screen is displayed."
    new "## Sørg for, at andre skærme ikke får input, mens denne skærm vises."

    # gui/game/screens.rpy:1167
    old "Yes"
    new "Ja"

    # gui/game/screens.rpy:1168
    old "No"
    new "Nej"

    # gui/game/screens.rpy:1170
    old "## Right-click and escape answer \"no\"."
    new "## Højreklik og undgå svaret \"no\"."

    # gui/game/screens.rpy:1197
    old "## Skip indicator screen"
    new "## Overspringningsindikatorskærmen"

    # gui/game/screens.rpy:1199
    old "## The skip_indicator screen is displayed to indicate that skipping is in progress."
    new "## Skærmen skip_indicator vises for at indikere, at overspringning er i gang."

    # gui/game/screens.rpy:1202
    old "## https://www.renpy.org/doc/html/screen_special.html#skip-indicator"
    new "## https://www.renpy.org/doc/html/screen_special.html#skip-indicator"

    # gui/game/screens.rpy:1214
    old "Skipping"
    new "Springer over"

    # gui/game/screens.rpy:1221
    old "## This transform is used to blink the arrows one after another."
    new "## Denne transformation bruges til at blinke med pilene en efter hinanden."

    # gui/game/screens.rpy:1248
    old "## We have to use a font that has the BLACK RIGHT-POINTING SMALL TRIANGLE glyph in it."
    new "## Vi skal bruge en skrifttype, der har tegnet BLACK RIGHT-POINTING SMALL TRIANGLE i sig."

    # gui/game/screens.rpy:1253
    old "## Notify screen"
    new "## Notifikationsskærmen"

    # gui/game/screens.rpy:1255
    old "## The notify screen is used to show the player a message. (For example, when the game is quicksaved or a screenshot has been taken.)"
    new "## Notifikationsskærmen bruges til at vise spilleren en besked. (For eksempel når spillet hurtiggemmes, eller når et skærmbillede er blevet taget.)"

    # gui/game/screens.rpy:1258
    old "## https://www.renpy.org/doc/html/screen_special.html#notify-screen"
    new "## https://www.renpy.org/doc/html/screen_special.html#notify-screen"

    # gui/game/screens.rpy:1292
    old "## NVL screen"
    new "## NVL-skærmen"

    # gui/game/screens.rpy:1294
    old "## This screen is used for NVL-mode dialogue and menus."
    new "## Denne skærm bruges til dialog og menuer i NVL-tilstand."

    # gui/game/screens.rpy:1296
    old "## https://www.renpy.org/doc/html/screen_special.html#nvl"
    new "## https://www.renpy.org/doc/html/screen_special.html#nvl"

    # gui/game/screens.rpy:1307
    old "## Displays dialogue in either a vpgrid or the vbox."
    new "## Viser dialog i enten et vpgrid eller vboxen."

    # gui/game/screens.rpy:1320
    old "## Displays the menu, if given. The menu may be displayed incorrectly if config.narrator_menu is set to True."
    new "## Viser menuen, hvis angivet. Menuen kan muligvis vises ukorrekt, hvis config.narrator_menu er sat til True."

    # gui/game/screens.rpy:1350
    old "## This controls the maximum number of NVL-mode entries that can be displayed at once."
    new "## Dette kontrollerer det maksimale antal af NVL-tilstandsindlæg, der kan vises på én gang."

    # gui/game/screens.rpy:1410
    old "## Bubble screen"
    new "## Talebobleskærmen"

    # gui/game/screens.rpy:1412
    old "## The bubble screen is used to display dialogue to the player when using speech bubbles. The bubble screen takes the same parameters as the say screen, must create a displayable with the id of \"what\", and can create displayables with the \"namebox\", \"who\", and \"window\" ids."
    new "## Talebobleskærmen bruges til at vise dialog til spilleren ved brug af talebobler. Talebobleskærmen tager imod de samme parametre som dialogskærmen. Den skal oprette et visbart element med id'et \"what\", og den kan oprette visbare elementer med id'erne \"namebox\", \"who\" og \"window\"."

    # gui/game/screens.rpy:1417
    old "## https://www.renpy.org/doc/html/bubble.html#bubble-screen"
    new "## https://www.renpy.org/doc/html/bubble.html#bubble-screen"

    # gui/game/screens.rpy:1501
    old "## Mobile Variants"
    new "## Mobilvarianter"

    # gui/game/screens.rpy:1508
    old "## Since a mouse may not be present, we replace the quick menu with a version that uses fewer and bigger buttons that are easier to touch."
    new "## Siden en mus muligvis ikke er til stede, erstatter vi hurtigmenuen med en version, der bruger færre og større knapper, der er lettere at ramme."

    # gui/game/screens.rpy:1526
    old "Menu"
    new "Menu"

