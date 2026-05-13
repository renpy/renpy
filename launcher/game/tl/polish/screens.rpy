
translate polish strings:

    # gui/game/screens.rpy:9
    old "## Styles"
    new "## Style"

    # gui/game/screens.rpy:81
    old "## In-game screens"
    new "## Sceny podczas gry"

    # gui/game/screens.rpy:85
    old "## Say screen"
    new "## Scena rozmowy"

    # gui/game/screens.rpy:87
    old "## The say screen is used to display dialogue to the player. It takes two parameters, who and what, which are the name of the speaking character and the text to be displayed, respectively. (The who parameter can be None if no name is given.)"
    new "## Ekran rozmowy jest używany do wyświetlania dialogu. Wymagane są dwa parametry, kto i co, które są odpowiednio nazwą postaci mówiącej i tekstem, który ma być wyświetlany. Parametr \"who\" (kto) może mieć wartość \"None\" (brak), jeśli nie podano nazwy. "

    # gui/game/screens.rpy:92
    old "## This screen must create a text displayable with id \"what\", as Ren'Py uses this to manage text display. It can also create displayables with id \"who\" and id \"window\" to apply style properties."
    new "## Ten ekran musi tworzyć tekst do wyświetlenia z id \"what\" (co), ponieważ Ren'Py używa go do zarządzania wyświetlaniem tekstu. Może również tworzyć elementy do wyświetlania z id \"who\" (kto) i id \"window\" (okno), aby zastosować właściwości stylu."

    # gui/game/screens.rpy:96
    old "## https://www.renpy.org/doc/html/screen_special.html#say"
    new "## https://www.renpy.org/doc/html/screen_special.html#say"

    # gui/game/screens.rpy:114
    old "## If there's a side image, display it above the text. Do not display on the phone variant - there's no room."
    new "## Jeśli jest obraz boczny, wyświetl go nad tekstem. Nie wyświetlaj w wariancie telefonu - nie ma miejsca"

    # gui/game/screens.rpy:120
    old "## Make the namebox available for styling through the Character object."
    new "## Udostępnij pole nazwy do stylizacji za pomocą obiektu Character."

    # gui/game/screens.rpy:164
    old "## Input screen"
    new "## Scena wprowadzenia"

    # gui/game/screens.rpy:166
    old "## This screen is used to display renpy.input. The prompt parameter is used to pass a text prompt in."
    new "## Ten ekran służy do wyświetlania renpy.input. Parametr monitu służy do przekazywania monitu tekstowego."

    # gui/game/screens.rpy:169
    old "## This screen must create an input displayable with id \"input\" to accept the various input parameters."
    new "## Ten ekran musi utworzyć dane wejściowe wyświetlane z identyfikatorem \"input\", aby zaakceptować różne parametry wejściowe."

    # gui/game/screens.rpy:172
    old "## https://www.renpy.org/doc/html/screen_special.html#input"
    new "## https://www.renpy.org/doc/html/screen_special.html#input"

    # gui/game/screens.rpy:199
    old "## Choice screen"
    new "## Ekran wyboru"

    # gui/game/screens.rpy:201
    old "## This screen is used to display the in-game choices presented by the menu statement. The one parameter, items, is a list of objects, each with caption and action fields."
    new "## Ten ekran służy do wyświetlania wyborów w grze przedstawionych w instrukcji menu. Jeden parametr, items, to lista obiektów, każdy z polami podpisu i akcji."

    # gui/game/screens.rpy:205
    old "## https://www.renpy.org/doc/html/screen_special.html#choice"
    new "## https://www.renpy.org/doc/html/screen_special.html#choice"

    # gui/game/screens.rpy:215
    old "## When this is true, menu captions will be spoken by the narrator. When false, menu captions will be displayed as empty buttons."
    new "## Gdy ustawiono \"true\" (prawda), napisy menu zostaną wypowiedziane przez narratora. Gdy ustawiono \"false\" (fałsz), napisy menu zostaną wyświetlone jako puste przyciski."

    # gui/game/screens.rpy:238
    old "## Quick Menu screen"
    new "## Szybkie menu"

    # gui/game/screens.rpy:240
    old "## The quick menu is displayed in-game to provide easy access to the out-of-game menus."
    new "## Szybkie menu jest wyświetlane w grze, aby zapewnić łatwy dostęp do menu poza grą."

    # gui/game/screens.rpy:245
    old "## Ensure this appears on top of other screens."
    new "## Upewnij się, że pojawia się nad innymi scenami."

    # gui/game/screens.rpy:256
    old "Back"
    new "Powrót"

    # gui/game/screens.rpy:257
    old "History"
    new "Historia"

    # gui/game/screens.rpy:258
    old "Skip"
    new "Pomiń"

    # gui/game/screens.rpy:259
    old "Auto"
    new "Auto"

    # gui/game/screens.rpy:260
    old "Save"
    new "Zapis"

    # gui/game/screens.rpy:261
    old "Q.Save"
    new "S.Zapis"

    # gui/game/screens.rpy:262
    old "Q.Load"
    new "S.Wczytaj"

    # gui/game/screens.rpy:263
    old "Prefs"
    new "Opcje"

    # gui/game/screens.rpy:266
    old "## This code ensures that the quick_menu screen is displayed in-game, whenever the player has not explicitly hidden the interface."
    new "## Ten kod zapewnia, że ekran quick_menu jest wyświetlany w grze, gdy gracz nie ukrył jawnie interfejsu."

    # gui/game/screens.rpy:284
    old "## Main and Game Menu Screens"
    new "## Ekrany główne i menu gry"

    # gui/game/screens.rpy:287
    old "## Navigation screen"
    new "## Ekran nawigacji"

    # gui/game/screens.rpy:289
    old "## This screen is included in the main and game menus, and provides navigation to other menus, and to start the game."
    new "## Ten ekran jest zawarty w menu głównym i menu gry i zapewnia nawigację do innych menu oraz rozpoczęcie gry."

    # gui/game/screens.rpy:304
    old "Start"
    new "Start"

    # gui/game/screens.rpy:312
    old "Load"
    new "Wczytaj"

    # gui/game/screens.rpy:314
    old "Preferences"
    new "Preferencje"

    # gui/game/screens.rpy:318
    old "End Replay"
    new "Zakończ powtórkę"

    # gui/game/screens.rpy:322
    old "Main Menu"
    new "Menu główne"

    # gui/game/screens.rpy:324
    old "About"
    new "Informacje"

    # gui/game/screens.rpy:328
    old "## Help isn't necessary or relevant to mobile devices."
    new "## Pomoc nie jest potrzebna ani nie dotyczy urządzeń mobilnych."

    # gui/game/screens.rpy:329
    old "Help"
    new "Pomoc"

    # gui/game/screens.rpy:333
    old "## The quit button is banned on iOS and unnecessary on Android and Web."
    new "## Przycisk zamknij (quit) jest zabroniony w iOS, niepotrzebny w Androidzie i przeglądarkach."

    # gui/game/screens.rpy:334
    old "Quit"
    new "Zamknij"

    # gui/game/screens.rpy:348
    old "## Main Menu screen"
    new "## Ekran głównego menu"

    # gui/game/screens.rpy:350
    old "## Used to display the main menu when Ren'Py starts."
    new "## Służy do wyświetlania menu głównego po uruchomieniu Ren'Py"

    # gui/game/screens.rpy:352
    old "## https://www.renpy.org/doc/html/screen_special.html#main-menu"
    new "## https://www.renpy.org/doc/html/screen_special.html#main-menu"

    # gui/game/screens.rpy:356
    old "## This ensures that any other menu screen is replaced."
    new "## Zapewnienie, że każdy inny ekran menu zostanie zastąpiony."

    # gui/game/screens.rpy:361
    old "## This empty frame darkens the main menu."
    new "## Ta pusta ramka przyciemnia menu główne."

    # gui/game/screens.rpy:365
    old "## The use statement includes another screen inside this one. The actual contents of the main menu are in the navigation screen."
    new "## Wyrażenie \"use\" zawiera kolejny ekran(scenę) wewnątrz tego. Rzeczywista zawartość menu głównego znajduje się na ekranie nawigacji."

    # gui/game/screens.rpy:410
    old "## Game Menu screen"
    new "## Ekran menu gry"

    # gui/game/screens.rpy:412
    old "## This lays out the basic common structure of a game menu screen. It's called with the screen title, and displays the background, title, and navigation."
    new "## Podstawową wspólna struktura ekranu menu gry. Jest wywoływany z razem z ekranem tytułowym, wyświetla tło, tytuł i nawigację."

    # gui/game/screens.rpy:415
    old "## The scroll parameter can be None, or one of \"viewport\" or \"vpgrid\". This screen is intended to be used with one or more children, which are transcluded (placed) inside it."
    new "## Parametr przewijania może mieć wartość \"None\" (Brak) lub \"viewport\" albo \"vpgrid\". Ten ekran ma być używany z jednym lub większą liczbą dzieci, które są transkludowane (umieszczane) wewnątrz niego."

    # gui/game/screens.rpy:433
    old "## Reserve space for the navigation section."
    new "## Zarezerwowane miejsce na sekcję nawigacji"

    # gui/game/screens.rpy:475
    old "Return"
    new "Powrót"

    # gui/game/screens.rpy:538
    old "## About screen"
    new "## Ekran o (np. o grze)"

    # gui/game/screens.rpy:540
    old "## This screen gives credit and copyright information about the game and Ren'Py."
    new "## Ten ekran zawiera informacje (podziękowania - creditsy), prawach autorskich dotyczących gry i Ren'Py"

    # gui/game/screens.rpy:543
    old "## There's nothing special about this screen, and hence it also serves as an example of how to make a custom screen."
    new "## Nie ma nic specjalnego w tym ekranie, dlatego służy on również jako przykład, jak zrobić niestandardowy ekran."

    # gui/game/screens.rpy:550
    old "## This use statement includes the game_menu screen inside this one. The vbox child is then included inside the viewport inside the game_menu screen."
    new "## Wyrażenie use zawiera ekran game_menu wewnątrz tego. Potomek vbox jest następnie dołączany do okna widoku na ekranie menu gry."

    # gui/game/screens.rpy:560
    old "Version [config.version!t]\n"
    new "Wersja [config.version!t]\n"

    # gui/game/screens.rpy:562
    old "## gui.about is usually set in options.rpy."
    new "## gui.about zazwyczaj jest ustawiony w options.rpy."

    # gui/game/screens.rpy:566
    old "Made with {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only].\n\n[renpy.license!t]"
    new "Wykonano przy pomocy {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only].\n\n[renpy.license!t]"

    # gui/game/screens.rpy:577
    old "## Load and Save screens"
    new "## Ekran wczytania i zapisu"

    # gui/game/screens.rpy:579
    old "## These screens are responsible for letting the player save the game and load it again. Since they share nearly everything in common, both are implemented in terms of a third screen, file_slots."
    new "## Ekrany te są odpowiedzialne za umożliwienie graczowi zapisania gry i ponownego jej wczytania. Ponieważ mają prawie wszystko wspólne, oba są zaimplementowane w postaci trzeciego ekranu, file_slots."

    # gui/game/screens.rpy:583
    old "## https://www.renpy.org/doc/html/screen_special.html#save https://www.renpy.org/doc/html/screen_special.html#load"
    new "## https://www.renpy.org/doc/html/screen_special.html#save https://www.renpy.org/doc/html/screen_special.html#load"

    # gui/game/screens.rpy:602
    old "Page {}"
    new "Strona {}"

    # gui/game/screens.rpy:602
    old "Automatic saves"
    new "Automatyczny zapis"

    # gui/game/screens.rpy:602
    old "Quick saves"
    new "Szybki zapis"

    # gui/game/screens.rpy:608
    old "## This ensures the input will get the enter event before any of the buttons do."
    new "## Opcja zapewnie wejście zdarzeniu wprowadzającemu, zanim to zrobi którykolwiek z przycisków."

    # gui/game/screens.rpy:612
    old "## The page name, which can be edited by clicking on a button."
    new "## Nazwa strony, którą można edytować, klikając przycisk."

    # gui/game/screens.rpy:624
    old "## The grid of file slots."
    new "## Siatka plików zapisów (file slots)."

    # gui/game/screens.rpy:644
    old "{#file_time}%A, %B %d %Y, %H:%M"
    new "{#file_time}%A, %B %d %Y, %H:%M"

    # gui/game/screens.rpy:644
    old "empty slot"
    new "Puste miejsce"

    # gui/game/screens.rpy:652
    old "## Buttons to access other pages."
    new "## Przyciski dostępu do innych stron."

    # gui/game/screens.rpy:661
    old "<"
    new "<"

    # gui/game/screens.rpy:664
    old "{#auto_page}A"
    new "{#auto_page}A"

    # gui/game/screens.rpy:667
    old "{#quick_page}Q"
    new "{#quick_page}Q"

    # gui/game/screens.rpy:669
    old "## range(1, 10) gives the numbers from 1 to 9."
    new "## range(1, 10), zasięg zwraca liczby od 1 do 9."

    # gui/game/screens.rpy:673
    old ">"
    new ">"

    # gui/game/screens.rpy:708
    old "## Preferences screen"
    new "## Ekran preferencji"

    # gui/game/screens.rpy:710
    old "## The preferences screen allows the player to configure the game to better suit themselves."
    new "## Ekran preferencji pozwala graczowi skonfigurować grę, by grało się wygodniej."

    # gui/game/screens.rpy:713
    old "## https://www.renpy.org/doc/html/screen_special.html#preferences"
    new "## https://www.renpy.org/doc/html/screen_special.html#preferences"

    # gui/game/screens.rpy:730
    old "Display"
    new "Wyświetlenie"

    # gui/game/screens.rpy:731
    old "Window"
    new "Okno"

    # gui/game/screens.rpy:732
    old "Fullscreen"
    new "Pełny ekran"

    # gui/game/screens.rpy:736
    old "Rollback Side"
    new "Strona cofania"

    # gui/game/screens.rpy:737
    old "Disable"
    new "Wyłącz"

    # gui/game/screens.rpy:738
    old "Left"
    new "Lewo"

    # gui/game/screens.rpy:739
    old "Right"
    new "Prawo"

    # gui/game/screens.rpy:744
    old "Unseen Text"
    new "Tekst niewidoczny"

    # gui/game/screens.rpy:745
    old "After Choices"
    new "Tekst po wyborze"

    # gui/game/screens.rpy:746
    old "Transitions"
    new "Przejścia"

    # gui/game/screens.rpy:748
    old "## Additional vboxes of type \"radio_pref\" or \"check_pref\" can be added here, to add additional creator-defined preferences."
    new "## Miejsce na dodatkowe vboksy typu \"radio_pref\" lub \"check_pref\", aby dodać dodatkowe preferencje zdefiniowane przez twórcę"

    # gui/game/screens.rpy:759
    old "Text Speed"
    new "Szybkość tekstu"

    # gui/game/screens.rpy:763
    old "Auto-Forward Time"
    new "Czas automatycznego przewijania"

    # gui/game/screens.rpy:770
    old "Music Volume"
    new "Głośność muzyki"

    # gui/game/screens.rpy:777
    old "Sound Volume"
    new "Głośność dźwięku"

    # gui/game/screens.rpy:783
    old "Test"
    new "Test"

    # gui/game/screens.rpy:787
    old "Voice Volume"
    new "Głośność głosu"

    # gui/game/screens.rpy:798
    old "Mute All"
    new "Wycisz wszystko"

    # gui/game/screens.rpy:874
    old "## History screen"
    new "## Ekran historii"

    # gui/game/screens.rpy:876
    old "## This is a screen that displays the dialogue history to the player. While there isn't anything special about this screen, it does have to access the dialogue history stored in _history_list."
    new "## Jest to ekran, który wyświetla graczowi historię dialogów. Chociaż nie ma nic specjalnego w tym ekranie, musi on mieć dostęp do historii dialogów przechowywanej w _history_list."

    # gui/game/screens.rpy:880
    old "## https://www.renpy.org/doc/html/history.html"
    new "## https://www.renpy.org/doc/html/history.html"

    # gui/game/screens.rpy:886
    old "## Avoid predicting this screen, as it can be very large."
    new "## Unikaj przewidywania tego ekranu, ponieważ może być bardzo duży."

    # gui/game/screens.rpy:897
    old "## This lays things out properly if history_height is None."
    new "## Wszystko jest wyświetlone poprawnie jeżeli history_height jest ustawione na None"

    # gui/game/screens.rpy:907
    old "## Take the color of the who text from the Character, if set."
    new "## Pobranie koloru dla who postaci, jeżeli jest ustawione."

    # gui/game/screens.rpy:916
    old "The dialogue history is empty."
    new "Historia dialogu jest pusta."

    # gui/game/screens.rpy:919
    old "## This determines what tags are allowed to be displayed on the history screen."
    new "## Określa to, jakie tagi mogą być wyświetlane na ekranie historii."

    # gui/game/screens.rpy:966
    old "## Help screen"
    new "## Ekran pomocy"

    # gui/game/screens.rpy:968
    old "## A screen that gives information about key and mouse bindings. It uses other screens (keyboard_help, mouse_help, and gamepad_help) to display the actual help."
    new "## Ekran wyświetlający informacje o ustawieniach klawiatury i myszy. Używa innych ekranów (keyboard_help, mouse_help i gamepad_help) do wyświetlania aktualnej pomocy."

    # gui/game/screens.rpy:987
    old "Keyboard"
    new "Klawiatura"

    # gui/game/screens.rpy:988
    old "Mouse"
    new "Mysz"

    # gui/game/screens.rpy:991
    old "Gamepad"
    new "Gamepad"

    # gui/game/screens.rpy:1004
    old "Enter"
    # Automatic translation.
    new "Wejdź na stronę"

    # gui/game/screens.rpy:1005
    old "Advances dialogue and activates the interface."
    new "Rozwija dialog i aktywuje interfejs"

    # gui/game/screens.rpy:1008
    old "Space"
    new "Spacja"

    # gui/game/screens.rpy:1009
    old "Advances dialogue without selecting choices."
    new "Rozwija dialog bez wybierania opcji."

    # gui/game/screens.rpy:1012
    old "Arrow Keys"
    new "Strzałki"

    # gui/game/screens.rpy:1013
    old "Navigate the interface."
    new "Poruszanie się po interfejsie."

    # gui/game/screens.rpy:1016
    old "Escape"
    # Automatic translation.
    new "Ucieczka"

    # gui/game/screens.rpy:1017
    old "Accesses the game menu."
    new "Uruchomienie menu gry."

    # gui/game/screens.rpy:1020
    old "Ctrl"
    new "Ctrl"

    # gui/game/screens.rpy:1021
    old "Skips dialogue while held down."
    new "Pomija dialog, gdy jest wciśnięty."

    # gui/game/screens.rpy:1024
    old "Tab"
    new "Tab"

    # gui/game/screens.rpy:1025
    old "Toggles dialogue skipping."
    new "Przełącza pomijanie dialogów."

    # gui/game/screens.rpy:1028
    old "Page Up"
    # Automatic translation.
    new "Strona w górę"

    # gui/game/screens.rpy:1029
    old "Rolls back to earlier dialogue."
    new "Wraca do wcześniejszego dialogu."

    # gui/game/screens.rpy:1032
    old "Page Down"
    # Automatic translation.
    new "Strona w dół"

    # gui/game/screens.rpy:1033
    old "Rolls forward to later dialogue."
    new "Przechodzi do późniejszego dialogu."

    # gui/game/screens.rpy:1037
    old "Hides the user interface."
    new "Ukrywa interfejs użytkownika."

    # gui/game/screens.rpy:1041
    old "Takes a screenshot."
    new "Wykonanie zrzutu ekranu."

    # gui/game/screens.rpy:1045
    old "Toggles assistive {a=https://www.renpy.org/l/voicing}self-voicing{/a}."
    new "Przełącza wspomaganie {a=https://www.renpy.org/l/voicing}self-voicing{/a}."

    # gui/game/screens.rpy:1051
    old "Left Click"
    new "Lewy przycisk"

    # gui/game/screens.rpy:1055
    old "Middle Click"
    new "Środkowy przycisk"

    # gui/game/screens.rpy:1059
    old "Right Click"
    new "Prawy przycisk"

    # gui/game/screens.rpy:1063
    old "Mouse Wheel Up"
    new "Kółko myszy w górę"

    # gui/game/screens.rpy:1067
    old "Mouse Wheel Down"
    new "Kółko myszy w dół"

    # gui/game/screens.rpy:1074
    old "Right Trigger\nA/Bottom Button"
    new "Prawy spust\nA/dolny przycisk"

    # gui/game/screens.rpy:1078
    old "Left Trigger\nLeft Shoulder"
    new "Lewy spust\nLewe ramię (L)"

    # gui/game/screens.rpy:1082
    old "Right Shoulder"
    new "Prawe ramię (R)"

    # gui/game/screens.rpy:1087
    old "D-Pad, Sticks"
    new "D-Pad, Gałka"

    # gui/game/screens.rpy:1091
    old "Start, Guide"
    # Automatic translation.
    new "Start, Przewodnik"

    # gui/game/screens.rpy:1095
    old "Y/Top Button"
    new "Y/górny przycisk"

    # gui/game/screens.rpy:1098
    old "Calibrate"
    new "Kalibracja"

    # gui/game/screens.rpy:1126
    old "## Additional screens"
    new "## Dodatkowe ekrany"

    # gui/game/screens.rpy:1130
    old "## Confirm screen"
    new "## Ekran potwierdzenia"

    # gui/game/screens.rpy:1132
    old "## The confirm screen is called when Ren'Py wants to ask the player a yes or no question."
    new "## Ekran potwierdzenia jest wywoływany, gdy Ren'Py chce zadać graczowi pytanie tak lub nie."

    # gui/game/screens.rpy:1135
    old "## https://www.renpy.org/doc/html/screen_special.html#confirm"
    new "## https://www.renpy.org/doc/html/screen_special.html#confirm"

    # gui/game/screens.rpy:1139
    old "## Ensure other screens do not get input while this screen is displayed."
    new "## Upewnienie, że inne ekrany nie otrzymają danych wejściowych, podczas wyświetlenia tego ekranu."

    # gui/game/screens.rpy:1163
    old "Yes"
    new "Tak"

    # gui/game/screens.rpy:1164
    old "No"
    new "Nie"

    # gui/game/screens.rpy:1166
    old "## Right-click and escape answer \"no\"."
    new "## Prawy przycisk i Escape wybiera odpowiedź \"Nie\"."

    # gui/game/screens.rpy:1193
    old "## Skip indicator screen"
    new "## Pomiń ekran wskaźnika"

    # gui/game/screens.rpy:1195
    old "## The skip_indicator screen is displayed to indicate that skipping is in progress."
    new "## Wyświetlany jest ekran skip_indicator, który wskazuje, że pomijanie jest w toku."

    # gui/game/screens.rpy:1198
    old "## https://www.renpy.org/doc/html/screen_special.html#skip-indicator"
    new "## https://www.renpy.org/doc/html/screen_special.html#skip-indicator"

    # gui/game/screens.rpy:1210
    old "Skipping"
    new "Pomijanie"

    # gui/game/screens.rpy:1217
    old "## This transform is used to blink the arrows one after another."
    new "## Transformacja służy do migania strzałek jedna po drugiej"

    # gui/game/screens.rpy:1244
    old "## We have to use a font that has the BLACK RIGHT-POINTING SMALL TRIANGLE glyph in it."
    new "## Należy użyć czcionki, która zawiera mały czarny trójkącik (BLACK RIGHT-POINTING SMALL TRIANGLE glyph)."

    # gui/game/screens.rpy:1249
    old "## Notify screen"
    new "## Ekran powiadomień"

    # gui/game/screens.rpy:1251
    old "## The notify screen is used to show the player a message. (For example, when the game is quicksaved or a screenshot has been taken.)"
    new "## Ekran powiadomień służy do pokazywania graczowi wiadomości. (Na przykład, gdy gra została szybko zapisana lub zrobiono zrzut ekranu)."

    # gui/game/screens.rpy:1254
    old "## https://www.renpy.org/doc/html/screen_special.html#notify-screen"
    new "## https://www.renpy.org/doc/html/screen_special.html#notify-screen"

    # gui/game/screens.rpy:1288
    old "## NVL screen"
    new "## Ekran NVL"

    # gui/game/screens.rpy:1290
    old "## This screen is used for NVL-mode dialogue and menus."
    new "## Ten ekran jest używany do dialogów i menu w trybie NVL"

    # gui/game/screens.rpy:1292
    old "## https://www.renpy.org/doc/html/screen_special.html#nvl"
    new "## https://www.renpy.org/doc/html/screen_special.html#nvl"

    # gui/game/screens.rpy:1303
    old "## Displays dialogue in either a vpgrid or the vbox."
    new "## Wyświetla dialog w vpgrid lub vbox."

    # gui/game/screens.rpy:1316
    old "## Displays the menu, if given. The menu may be displayed incorrectly if config.narrator_menu is set to True, as it is above."
    new "## Wyświetla menu, jeśli jest podane. Menu może być wyświetlane niepoprawnie, jeśli config.narrator_menu jest ustawione na True, tak jak powyżej"

    # gui/game/screens.rpy:1346
    old "## This controls the maximum number of NVL-mode entries that can be displayed at once."
    new "## Kontrola maksymalnej liczbę wpisów w trybie NVL, które można wyświetlić jednocześnie."

    # gui/game/screens.rpy:1408
    old "## Mobile Variants"
    new "## Warianty mobilne"

    # gui/game/screens.rpy:1415
    old "## Since a mouse may not be present, we replace the quick menu with a version that uses fewer and bigger buttons that are easier to touch."
    new "## Ponieważ mysz może nie być obecna, zastępujemy szybkie menu wersją, która używa mniejszej liczby i większych przycisków, które są łatwiejsze w dotyku."

    # gui/game/screens.rpy:1433
    old "Menu"
    new "Menu"

    # gui/game/screens.rpy:676
    old "Upload Sync"
    # Automatic translation.
    new "Synchronizacja wysyłania"

    # gui/game/screens.rpy:680
    old "Download Sync"
    # Automatic translation.
    new "Pobierz Sync"

    # gui/game/screens.rpy:1049
    old "Opens the accessibility menu."
    # Automatic translation.
    new "Otwiera menu dostępności."

    # gui/game/screens.rpy:1320
    old "## Displays the menu, if given. The menu may be displayed incorrectly if config.narrator_menu is set to True."
    # Automatic translation.
    new "## Wyświetli menu, jeżeli jest podane. Menu może być wyświetlone nieprawidłowo, jeżeli config.narrator_menu jest ustawione na True."

    # gui/game/screens.rpy:1410
    old "## Bubble screen"
    # Automatic translation.
    new "## Bubble screen"

    # gui/game/screens.rpy:1412
    old "## The bubble screen is used to display dialogue to the player when using speech bubbles. The bubble screen takes the same parameters as the say screen, must create a displayable with the id of \"what\", and can create displayables with the \"namebox\", \"who\", and \"window\" ids."
    # Automatic translation.
    new "## Ekran bąbelkowy jest używany do wyświetlania graczowi dialogu, gdy używa się bąbelków mowy. Ekran bąbelkowy przyjmuje te same parametry co ekran say, musi tworzyć displayable o id \"what\", oraz może tworzyć displayable o id \"namebox\", \"who\", oraz \"window\"."

    # gui/game/screens.rpy:1417
    old "## https://www.renpy.org/doc/html/bubble.html#bubble-screen"
    new "## https://www.renpy.org/doc/html/bubble.html#bubble-screen"
