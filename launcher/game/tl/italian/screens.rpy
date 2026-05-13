translate italian strings:

    # screens.rpy:9
    old "## Styles"
    new "## Stili"

    # screens.rpy:87
    old "## In-game screens"
    new "## Schermate interne al gioco"

    # screens.rpy:91
    old "## Say screen"
    new "## Schermata dei dialoghi"

    # screens.rpy:93
    old "## The say screen is used to display dialogue to the player. It takes two parameters, who and what, which are the name of the speaking character and the text to be displayed, respectively. (The who parameter can be None if no name is given.)"
    new "## La schermata dei dialoghi (say) è usata per mostrare dialoghi al giocatore. Richiede due parametri, who e what, che sono il nome del personaggio che parla e il testo da mostrare. (Il parametro who può essere None se non si intende fornire un nome)"

    # screens.rpy:98
    old "## This screen must create a text displayable with id \"what\", as Ren'Py uses this to manage text display. It can also create displayables with id \"who\" and id \"window\" to apply style properties."
    new "## Questa schermata crea un displayable di testo con id \"what\", che Ren'Py usa per gestire la visualizzazione del testo. Può creare anche displayable con id \"who\" e id \"window\" per applicarvi proprietà di stile."

    # screens.rpy:102
    old "## https://www.renpy.org/doc/html/screen_special.html#say"
    new "## https://www.renpy.org/doc/html/screen_special.html#say"

    # screens.rpy:169
    old "## Input screen"
    new "## Schermata di inserimento"

    # screens.rpy:171
    old "## This screen is used to display renpy.input. The prompt parameter is used to pass a text prompt in."
    new "## Questa schermata si usa per mostrare renpy.input. Il parametro prompt è usato per fornire un prompt testuale."

    # screens.rpy:174
    old "## This screen must create an input displayable with id \"input\" to accept the various input parameters."
    new "## Questa schermata deve creare un displayable input con id \"input\" per accettare i vari parametri dell'input."

    # screens.rpy:177
    old "## http://www.renpy.org/doc/html/screen_special.html#input"
    new "## http://www.renpy.org/doc/html/screen_special.html#input"

    # screens.rpy:205
    old "## Choice screen"
    new "## Schermata di scelta"

    # screens.rpy:207
    old "## This screen is used to display the in-game choices presented by the menu statement. The one parameter, items, is a list of objects, each with caption and action fields."
    new "## Questa schermata è usata per mostrare le scelte nel gioco, offerte dal comando 'menu'. Il solo parametro, 'items', è una lista di oggetti, ciascuna coi campi 'caption' e 'action'."

    # screens.rpy:211
    old "## http://www.renpy.org/doc/html/screen_special.html#choice"
    new "## http://www.renpy.org/doc/html/screen_special.html#choice"

    # screens.rpy:221
    old "## When this is true, menu captions will be spoken by the narrator. When false, menu captions will be displayed as empty buttons."
    new "## Quando impostato su 'True', le didascalie del menu saranno dette dal narratore. Quando falso, le didascalie saranno mostrate come pulsanti inattivi."

    # screens.rpy:244
    old "## Quick Menu screen"
    new "## Schermata del Menu Rapido"

    # screens.rpy:246
    old "## The quick menu is displayed in-game to provide easy access to the out-of-game menus."
    new "## Il menu rapido è mostrato durante il gioco per fornire accesso facile ai menu esterni."

    # screens.rpy:261
    old "Back"
    new "Indietro"

    # screens.rpy:262
    old "History"
    new "Cronologia"

    # screens.rpy:263
    old "Skip"
    new "Salta"

    # screens.rpy:264
    old "Auto"
    new "Auto"

    # screens.rpy:265
    old "Save"
    new "Salva"

    # screens.rpy:266
    old "Q.Save"
    new "Salva R."

    # screens.rpy:267
    old "Q.Load"
    new "Carica R."

    # screens.rpy:268
    old "Prefs"
    new "Opzioni"

    # screens.rpy:271
    old "## This code ensures that the quick_menu screen is displayed in-game, whenever the player has not explicitly hidden the interface."
    new "## Questo codice assicura che il quick menu sia mostrato nel gioco, a meno che il giocatore non nasconda esplicitamente l'interfaccia."

    # screens.rpy:291
    old "## Navigation screen"
    new "## Schermata di navigazione"

    # screens.rpy:293
    old "## This screen is included in the main and game menus, and provides navigation to other menus, and to start the game."
    new "## Questa schermata è inclusa nei menu principale e di gioco, e consente di navigare verso altri menu o di iniziare il gioco."

    # screens.rpy:308
    old "Start"
    new "Inizia"

    # screens.rpy:316
    old "Load"
    new "Carica"

    # screens.rpy:318
    old "Preferences"
    new "Opzioni"

    # screens.rpy:322
    old "End Replay"
    new "Fine Replay"

    # screens.rpy:326
    old "Main Menu"
    new "Menu Principale"

    # screens.rpy:328
    old "About"
    new "Informazioni"

    # screens.rpy:332
    old "## Help isn't necessary or relevant to mobile devices."
    new "## L'Aiuto non è necessario o rilevante sui dispositivi mobili."

    # screens.rpy:333
    old "Help"
    new "Aiuto"

    # screens.rpy:335
    old "## The quit button is banned on iOS and unnecessary on Android."
    new "## Il pulsante esci è vietato su iOS e inutile su Android."

    # screens.rpy:336
    old "Quit"
    new "Esci"

    # screens.rpy:350
    old "## Main Menu screen"
    new "## Schermata del menu principale"

    # screens.rpy:352
    old "## Used to display the main menu when Ren'Py starts."
    new "## Usato per mostrare il menu principale quando si avvia Ren'Py."

    # screens.rpy:354
    old "## http://www.renpy.org/doc/html/screen_special.html#main-menu"
    new "## http://www.renpy.org/doc/html/screen_special.html#main-menu"

    # screens.rpy:369
    old "## The use statement includes another screen inside this one. The actual contents of the main menu are in the navigation screen."
    new "## Il comando 'use' include un'altra schermata all'interno della corrente. I contenuti effettivi del menu principale sono nella schermata di navigazione."

    # screens.rpy:413
    old "## Game Menu screen"
    new "## Schermata del Menu di Gioco"

    # screens.rpy:415
    old "## This lays out the basic common structure of a game menu screen. It's called with the screen title, and displays the background, title, and navigation."
    new "## Costituisce la struttura comune di qualunque schermata del menu di gioco. Viene avviato nella schermata del titolo, e mostra lo sfondo, il titolo e la navigazione."

    # screens.rpy:418
    old "## The scroll parameter can be None, or one of \"viewport\" or \"vpgrid\". This screen is intended to be used with one or more children, which are transcluded (placed) inside it."
    new "## Il parametro 'scroll' può essere None, oppure uno fra \"viewport\" o \"vpgrid\". Questa schermata è progettata per essere usata con uno o più figli, che sono trasclusi (piazzati) dentro di esso."

    # screens.rpy:476
    old "Return"
    new "Indietro"

    # screens.rpy:539
    old "## About screen"
    new "## Schermata delle informazioni"

    # screens.rpy:541
    old "## This screen gives credit and copyright information about the game and Ren'Py."
    new "## Questa schermata visualizza i crediti e le informazioni di copyright sul gioco e su Ren'Py."

    # screens.rpy:544
    old "## There's nothing special about this screen, and hence it also serves as an example of how to make a custom screen."
    new "## Non c'è niente di speciale in questa schermata, pertanto può servire come esempio su come si crea una schermata personalizzata."

    # screens.rpy:551
    old "## This use statement includes the game_menu screen inside this one. The vbox child is then included inside the viewport inside the game_menu screen."
    new "## Questo comando 'use' include la schermata game_menu all'interno della corrente. Il figlio di vbox è quindi incluso nel viewport all'interno dello screen game_menu. \n## ===PER NEOFITI===: in pratica viene prima chiamato il game menu che stabilisce spaziature, sfondo, titoli e una viewport. Questo screen chiama e mostra il navigation screen a sinistra, che a sua volta determina quale screen (opzioni, slot, aiuto...) mostrare nella viewport a destra."

    # screens.rpy:561
    old "Version [config.version!t]\n"
    new "Versione [config.version!t]\n"

    # screens.rpy:563
    old "## gui.about is usually set in options.rpy."
    new "## gui.about viene di solito impostato in options.rpy."

    # screens.rpy:567
    old "Made with {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only].\n\n[renpy.license!t]"
    new "Creato con {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only].\n\n[renpy.license!t]"

    # screens.rpy:570
    old "## This is redefined in options.rpy to add text to the about screen."
    new "## Viene ridefinito in options.rpy per aggiungere testo a questo screen."

    # screens.rpy:582
    old "## Load and Save screens"
    new "## Schermate di Caricamento e Salvataggio"

    # screens.rpy:584
    old "## These screens are responsible for letting the player save the game and load it again. Since they share nearly everything in common, both are implemented in terms of a third screen, file_slots."
    new "## Questi screen sono responsabili per la possibilità di salvare il gioco e caricarlo di nuovo. Dato che condividono praticamente tutto, entrambi sono implementati in relazione a un terzo screen, file_slot."

    # screens.rpy:588
    old "## https://www.renpy.org/doc/html/screen_special.html#save https://www.renpy.org/doc/html/screen_special.html#load"
    new "## https://www.renpy.org/doc/html/screen_special.html#save https://www.renpy.org/doc/html/screen_special.html#load"

    # screens.rpy:607
    old "Page {}"
    new "Pagina {}"

    # screens.rpy:607
    old "Automatic saves"
    new "Salvataggi automatici"

    # screens.rpy:607
    old "Quick saves"
    new "Salvataggi rapidi"

    # screens.rpy:613
    old "## This ensures the input will get the enter event before any of the buttons do."
    new "## Questo garantisce che l'input riceva un'eventuale pressione di Invio prima che accada ad altri pulsanti."

    # screens.rpy:629
    old "## The grid of file slots."
    new "## La griglia di slot."

    # screens.rpy:649
    old "{#file_time}%A, %B %d %Y, %H:%M"
    new "{#file_time}%A, %B %d %Y, %H:%M"

    # screens.rpy:649
    old "empty slot"
    new "Spazio Vuoto"

    # screens.rpy:657
    old "## Buttons to access other pages."
    new "## Pulsanti per accedere ad altre pagine."

    # screens.rpy:666
    old "<"
    new "<"

    # screens.rpy:668
    old "{#auto_page}A"
    new "{#auto_page}A"

    # screens.rpy:670
    old "{#quick_page}Q"
    new "{#quick_page}R"

    # screens.rpy:676
    old ">"
    new ">"

    # screens.rpy:711
    old "## Preferences screen"
    new "## Schermata delle preferenze"

    # screens.rpy:713
    old "## The preferences screen allows the player to configure the game to better suit themselves."
    new "## Lo screen preferences (Opzioni) consente al giocatore di configurare il gioco per un'esperienza più affine ai suoi gusti."

    # screens.rpy:716
    old "## https://www.renpy.org/doc/html/screen_special.html#preferences"
    new "## https://www.renpy.org/doc/html/screen_special.html#preferences"

    # screens.rpy:738
    old "Display"
    new "Schermo"

    # screens.rpy:739
    old "Window"
    new "Finestra"

    # screens.rpy:740
    old "Fullscreen"
    new "Schermo intero"

    # screens.rpy:744
    old "Rollback Side"
    new "Lato Riavvolgimento"

    # screens.rpy:745
    old "Disable"
    new "Disattiva"

    # screens.rpy:746
    old "Left"
    new "Sinistra"

    # screens.rpy:747
    old "Right"
    new "Destra"

    # screens.rpy:752
    old "Unseen Text"
    new "Testo non letto"

    # screens.rpy:753
    old "After Choices"
    new "Dopo le Scelte"

    # screens.rpy:754
    old "Transitions"
    new "Transizioni"

    # screens.rpy:756
    old "## Additional vboxes of type \"radio_pref\" or \"check_pref\" can be added here, to add additional creator-defined preferences."
    new "## Vbox addizionali del tipo \"radio_pref\" o \"check_pref\" possono venire aggiunti qui, per offrire ulteriori opzioni al giocatore."

    # screens.rpy:767
    old "Text Speed"
    new "Velocità del Testo"

    # screens.rpy:771
    old "Auto-Forward Time"
    new "Ritmo di Avanzamento Automatico"

    # screens.rpy:778
    old "Music Volume"
    new "Volume della Musica"

    # screens.rpy:785
    old "Sound Volume"
    new "Volume dei Suoni"

    # screens.rpy:791
    old "Test"
    new "Prova"

    # screens.rpy:795
    old "Voice Volume"
    new "Volume della Voce"

    # screens.rpy:806
    old "Mute All"
    new "Silenzia Tutto"

    # screens.rpy:882
    old "## History screen"
    new "## Schermata della cronologia"

    # screens.rpy:884
    old "## This is a screen that displays the dialogue history to the player. While there isn't anything special about this screen, it does have to access the dialogue history stored in _history_list."
    new "## Questo è uno screen che mostra una cronologia dei dialoghi al giocatore. Benché non vi sia niente di speciale in questo screen, deve accedere alla cronologia contenuta in _history_list."

    # screens.rpy:888
    old "## https://www.renpy.org/doc/html/history.html"
    new "## https://www.renpy.org/doc/html/history.html"

    # screens.rpy:894
    old "## Avoid predicting this screen, as it can be very large."
    new "## Evita di predirre questo screen, perché può essere molto grande."

    # screens.rpy:905
    old "## This lays things out properly if history_height is None."
    new "## Questo dispone le cose appropriatamente, se history_height è None."

    # screens.rpy:914
    old "## Take the color of the who text from the Character, if set."
    new "## Prende il colore dal nome del personaggio, se impostato."

    # screens.rpy:921
    old "The dialogue history is empty."
    new "Nessun dialogo da mostrare."

    # screens.rpy:965
    old "## Help screen"
    new "## Schermata di aiuto"

    # screens.rpy:967
    old "## A screen that gives information about key and mouse bindings. It uses other screens (keyboard_help, mouse_help, and gamepad_help) to display the actual help."
    new "## Uno screen che offre informazioni sulle impostazioni di tastiera e mouse. Usa altri screen (keyboard_help, mouse_help, e gamepad_help) per mostrare l'effettivo contenuto."

    # screens.rpy:986
    old "Keyboard"
    new "Tastiera"

    # screens.rpy:987
    old "Mouse"
    new "Mouse"

    # screens.rpy:990
    old "Gamepad"
    new "Gamepad"

    # screens.rpy:1003
    old "Enter"
    new "Invio"

    # screens.rpy:1004
    old "Advances dialogue and activates the interface."
    new "Avanza nei dialoghi e conferma opzioni."

    # screens.rpy:1007
    old "Space"
    new "Spazio"

    # screens.rpy:1008
    old "Advances dialogue without selecting choices."
    new "Avanza nei dialoghi senza eseguire scelte."

    # screens.rpy:1011
    old "Arrow Keys"
    new "Tasti Freccia"

    # screens.rpy:1012
    old "Navigate the interface."
    new "Naviga nell'interfaccia."

    # screens.rpy:1015
    old "Escape"
    new "Esc"

    # screens.rpy:1016
    old "Accesses the game menu."
    new "Accedi al menu di gioco."

    # screens.rpy:1019
    old "Ctrl"
    new "Ctrl"

    # screens.rpy:1020
    old "Skips dialogue while held down."
    new "Tieni premuto per saltare i dialoghi."

    # screens.rpy:1023
    old "Tab"
    new "Tab"

    # screens.rpy:1024
    old "Toggles dialogue skipping."
    new "Attiva/Disattiva salto dei dialoghi."

    # screens.rpy:1027
    old "Page Up"
    new "Pagina Su"

    # screens.rpy:1028
    old "Rolls back to earlier dialogue."
    new "Torna indietro al dialogo precedente."

    # screens.rpy:1031
    old "Page Down"
    new "Pagina Giù"

    # screens.rpy:1032
    old "Rolls forward to later dialogue."
    new "Procedi fino all'ultimo dialogo letto."

    # screens.rpy:1036
    old "Hides the user interface."
    new "Nascondi l'interfaccia utente."

    # screens.rpy:1040
    old "Takes a screenshot."
    new "Cattura la schermata."

    # screens.rpy:1044
    old "Toggles assistive {a=https://www.renpy.org/l/voicing}self-voicing{/a}."
    new "Attiva l'{a=https://www.renpy.org/l/voicing}Assistente Vocale{/a}."

    # screens.rpy:1050
    old "Left Click"
    new "Click Sinistro"

    # screens.rpy:1054
    old "Middle Click"
    new "Click Centrale"

    # screens.rpy:1058
    old "Right Click"
    new "Click Destro"

    # screens.rpy:1062
    old "Mouse Wheel Up"
    new "Rotella Su"

    # screens.rpy:1066
    old "Mouse Wheel Down"
    new "Rotella Giù"

    # screens.rpy:1073
    old "Right Trigger\nA/Bottom Button"
    new "Grilletto Destro\nPulsante A/Inferiore"

    # screens.rpy:1074
    old "Advance dialogue and activates the interface."
    new "Avanza nei dialoghi e conferma opzioni."

    # screens.rpy:1078
    old "Roll back to earlier dialogue."
    new "Torna al dialogo precedente."

    # screens.rpy:1081
    old "Right Shoulder"
    new "Dorsale Destro"

    # screens.rpy:1082
    old "Roll forward to later dialogue."
    new "Torna all'ultimo dialogo letto."

    # screens.rpy:1085
    old "D-Pad, Sticks"
    new "Croce direzionale, Joystick"

    # screens.rpy:1089
    old "Start, Guide"
    new "Start, Guida"

    # screens.rpy:1090
    old "Access the game menu."
    new "Accedi al menu di gioco."

    # screens.rpy:1093
    old "Y/Top Button"
    new "Pulsante Y/Superiore"

    # screens.rpy:1096
    old "Calibrate"
    new "Calibra"

    # screens.rpy:1124
    old "## Additional screens"
    new "## Schermate addizionali"

    # screens.rpy:1128
    old "## Confirm screen"
    new "## Schermata di conferma"

    # screens.rpy:1130
    old "## The confirm screen is called when Ren'Py wants to ask the player a yes or no question."
    new "## La schermata di conferma (confirm) è usata quando Ren'Py vuole porre una domanda 'sì o no?' al giocatore."

    # screens.rpy:1133
    old "## http://www.renpy.org/doc/html/screen_special.html#confirm"
    new "## http://www.renpy.org/doc/html/screen_special.html#confirm"

    # screens.rpy:1137
    old "## Ensure other screens do not get input while this screen is displayed."
    new "## Garantisce che gli altri screen non ricevano input fino a che questo screen è attivo."

    # screens.rpy:1161
    old "Yes"
    new "Sì"

    # screens.rpy:1162
    old "No"
    new "No"

    # screens.rpy:1164
    old "## Right-click and escape answer \"no\"."
    new "## Click destro ed ESC rispondono \"no\"."

    # screens.rpy:1191
    old "## Skip indicator screen"
    new "## Schermata dell'indicatore di salto"

    # screens.rpy:1193
    old "## The skip_indicator screen is displayed to indicate that skipping is in progress."
    new "## La schermata skip_indicator è visualizzata per indicare che è in corso la modalità salto."

    # screens.rpy:1196
    old "## https://www.renpy.org/doc/html/screen_special.html#skip-indicator"
    new "## https://www.renpy.org/doc/html/screen_special.html#skip-indicator"

    # screens.rpy:1208
    old "Skipping"
    new "Salto"

    # screens.rpy:1215
    old "## This transform is used to blink the arrows one after another."
    new "## Questa transform è usata per far lampeggiare le freccie una dopo l'altra."

    # screens.rpy:1247
    old "## Notify screen"
    new "## Schermata di notifica"

    # screens.rpy:1249
    old "## The notify screen is used to show the player a message. (For example, when the game is quicksaved or a screenshot has been taken.)"
    new "## La schermata di notifica (notify) è usata per mostrare una notifica al giocatore (per esempio, quando si salva rapidamente o si cattura una schermata)."

    # screens.rpy:1252
    old "## https://www.renpy.org/doc/html/screen_special.html#notify-screen"
    new "## https://www.renpy.org/doc/html/screen_special.html#notify-screen"

    # screens.rpy:1286
    old "## NVL screen"
    new "## Schermata NVL"

    # screens.rpy:1288
    old "## This screen is used for NVL-mode dialogue and menus."
    new "## Questa schermata è usata per dialoghi e menu in modalità NVL."

    # screens.rpy:1290
    old "## http://www.renpy.org/doc/html/screen_special.html#nvl"
    new "## http://www.renpy.org/doc/html/screen_special.html#nvl"

    # screens.rpy:1301
    old "## Displays dialogue in either a vpgrid or the vbox."
    new "## Mostra il dialogo in una vpgrid o in una vbox."

    # screens.rpy:1314
    old "## Displays the menu, if given. The menu may be displayed incorrectly if config.narrator_menu is set to True."
    new "## Mostra il menu, se fornito. Il menu può apparire distorto se config.narrator_menu è impostato a True."

    # screens.rpy:1344
    old "## This controls the maximum number of NVL-mode entries that can be displayed at once."
    new "## Questo controlla il numero massimo di elementi NVL che possono venire mostrati all'unisono."

    # screens.rpy:1406
    old "## Mobile Variants"
    new "## Varianti Mobili"

    # screens.rpy:1413
    old "## Since a mouse may not be present, we replace the quick menu with a version that uses fewer and bigger buttons that are easier to touch."
    new "## Dato che un mouse non è presente, rimpiazziamo il quick menu con una versione che usa meno pulsanti e più grandi, più facili da toccare."

    # screens.rpy:1429
    old "Menu"
    new "Menu"

    # screens.rpy:120
    old "## If there's a side image, display it above the text. Do not display on the phone variant - there's no room."
    new "## Se c'è una side image, mostrala sopra al testo. Non mostrarla nella variante 'phone' - non c'è posto."

    # screens.rpy:252
    old "## Ensure this appears on top of other screens."
    new "## Assicura che compaia in cima ad altri screen."

    # screens.rpy:291
    old "## Main and Game Menu Screens"
    new "## Main Menu e Game Menu"

    # screens.rpy:361
    old "## This ensures that any other menu screen is replaced."
    new "## Questo assicura che ogni altro menu sia rimpiazzato."

    # screens.rpy:368
    old "## This empty frame darkens the main menu."
    new "## Questo frame vuoto oscura il main menu."

    # screens.rpy:439
    old "## Reserve space for the navigation section."
    new "## Riserva spazio per la sezione di navigazione."

    # screens.rpy:619
    old "## The page name, which can be edited by clicking on a button."
    new "## Il nome della pagina, che può essere cambiato cliccando su un pulsante."

    # screens.rpy:674
    old "## range(1, 10) gives the numbers from 1 to 9."
    new "## range(1, 10) fornisce i numeri da 1 a 9."

    # screens.rpy:1079
    old "Left Trigger\nLeft Shoulder"
    new "Grilletto Sinistro\nDorsale Sinistro"

    # gui/game/screens.rpy:120
    old "## Make the namebox available for styling through the Character object."
    new "## Rendi la casella dei nomi disponibile per lo styling attraverso l'oggetto Character."

    # gui/game/screens.rpy:173
    old "## https://www.renpy.org/doc/html/screen_special.html#input"
    new "## https://www.renpy.org/doc/html/screen_special.html#input"

    # gui/game/screens.rpy:206
    old "## https://www.renpy.org/doc/html/screen_special.html#choice"
    new "## https://www.renpy.org/doc/html/screen_special.html#choice"

    # gui/game/screens.rpy:329
    old "## The quit button is banned on iOS and unnecessary on Android and Web."
    new "## Il pulsante esci è vietato su iOS e inutile su Android e sul Web."

    # gui/game/screens.rpy:348
    old "## https://www.renpy.org/doc/html/screen_special.html#main-menu"
    new "## https://www.renpy.org/doc/html/screen_special.html#main-menu"

    # gui/game/screens.rpy:676
    old "Upload Sync"
    new "Carica dati per la Sincronizzazione"

    # gui/game/screens.rpy:680
    old "Download Sync"
    new "Scarica dati Sincronizzati"

    # gui/game/screens.rpy:921
    old "## This determines what tags are allowed to be displayed on the history screen."
    new "## Determina quali tag possono essere visualizzati nella schermata della cronologia."

    # gui/game/screens.rpy:1049
    old "Opens the accessibility menu."
    new "Apri il menu di accessibilità."

    # gui/game/screens.rpy:1139
    old "## https://www.renpy.org/doc/html/screen_special.html#confirm"
    new "## https://www.renpy.org/doc/html/screen_special.html#confirm"

    # gui/game/screens.rpy:1248
    old "## We have to use a font that has the BLACK RIGHT-POINTING SMALL TRIANGLE glyph in it."
    new "## Bisogna usare un carattere che contenga il glifo BLACK RIGHT-POINTING SMALL TRIANGLE."

    # gui/game/screens.rpy:1296
    old "## https://www.renpy.org/doc/html/screen_special.html#nvl"
    new "## https://www.renpy.org/doc/html/screen_special.html#nvl"

    # gui/game/screens.rpy:1410
    old "## Bubble screen"
    new "## Schermata a bolle"

    # gui/game/screens.rpy:1412
    old "## The bubble screen is used to display dialogue to the player when using speech bubbles. The bubble screen takes the same parameters as the say screen, must create a displayable with the id of \"what\", and can create displayables with the \"namebox\", \"who\", and \"window\" ids."
    new "## La schermata a bolle (bubble) è usata per visualizzare il dialogo al giocatore quando si usano le bolle di dialogo. La schermata a bolle prende gli stessi parametri della schermata say, deve creare un visualizzabile con l'id \"what\" e può creare visualizzabili con gli id \"namebox\", \"who\" e \"window\"."

    # gui/game/screens.rpy:1417
    old "## https://www.renpy.org/doc/html/bubble.html#bubble-screen"
    new "## https://www.renpy.org/doc/html/bubble.html#bubble-screen"
