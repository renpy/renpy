# TODO: Translation updated at 2019-05-11 23:37

translate turkish strings:

    # screens.rpy:9
    old "## Styles"
    new ""

    # screens.rpy:81
    old "## In-game screens"
    new ""

    # screens.rpy:85
    old "## Say screen"
    new ""

    # screens.rpy:87
    old "## The say screen is used to display dialogue to the player. It takes two parameters, who and what, which are the name of the speaking character and the text to be displayed, respectively. (The who parameter can be None if no name is given.)"
    new ""

    # screens.rpy:92
    old "## This screen must create a text displayable with id \"what\", as Ren'Py uses this to manage text display. It can also create displayables with id \"who\" and id \"window\" to apply style properties."
    new ""

    # screens.rpy:96
    old "## https://www.renpy.org/doc/html/screen_special.html#say"
    new ""

    # screens.rpy:114
    old "## If there's a side image, display it above the text. Do not display on the phone variant - there's no room."
    new ""

    # screens.rpy:120
    old "## Make the namebox available for styling through the Character object."
    new ""

    # screens.rpy:164
    old "## Input screen"
    new ""

    # screens.rpy:166
    old "## This screen is used to display renpy.input. The prompt parameter is used to pass a text prompt in."
    new ""

    # screens.rpy:169
    old "## This screen must create an input displayable with id \"input\" to accept the various input parameters."
    new ""

    # screens.rpy:172
    old "## https://www.renpy.org/doc/html/screen_special.html#input"
    new ""

    # screens.rpy:199
    old "## Choice screen"
    new ""

    # screens.rpy:201
    old "## This screen is used to display the in-game choices presented by the menu statement. The one parameter, items, is a list of objects, each with caption and action fields."
    new ""

    # screens.rpy:205
    old "## https://www.renpy.org/doc/html/screen_special.html#choice"
    new ""

    # screens.rpy:215
    old "## When this is true, menu captions will be spoken by the narrator. When false, menu captions will be displayed as empty buttons."
    new ""

    # screens.rpy:238
    old "## Quick Menu screen"
    new ""

    # screens.rpy:240
    old "## The quick menu is displayed in-game to provide easy access to the out-of-game menus."
    new ""

    # screens.rpy:245
    old "## Ensure this appears on top of other screens."
    new ""

    # screens.rpy:256
    old "Back"
    new ""

    # screens.rpy:257
    old "History"
    new ""

    # screens.rpy:258
    old "Skip"
    new ""

    # screens.rpy:259
    old "Auto"
    new ""

    # screens.rpy:260
    old "Save"
    new ""

    # screens.rpy:261
    old "Q.Save"
    new ""

    # screens.rpy:262
    old "Q.Load"
    new ""

    # screens.rpy:263
    old "Prefs"
    new ""

    # screens.rpy:266
    old "## This code ensures that the quick_menu screen is displayed in-game, whenever the player has not explicitly hidden the interface."
    new ""

    # screens.rpy:284
    old "## Main and Game Menu Screens"
    new ""

    # screens.rpy:287
    old "## Navigation screen"
    new ""

    # screens.rpy:289
    old "## This screen is included in the main and game menus, and provides navigation to other menus, and to start the game."
    new ""

    # screens.rpy:304
    old "Start"
    new ""

    # screens.rpy:312
    old "Load"
    new ""

    # screens.rpy:314
    old "Preferences"
    new ""

    # screens.rpy:318
    old "End Replay"
    new ""

    # screens.rpy:322
    old "Main Menu"
    new ""

    # screens.rpy:324
    old "About"
    new ""

    # screens.rpy:328
    old "## Help isn't necessary or relevant to mobile devices."
    new ""

    # screens.rpy:329
    old "Help"
    new ""

    # screens.rpy:331
    old "## The quit button is banned on iOS and unnecessary on Android."
    new ""

    # screens.rpy:332
    old "Quit"
    new ""

    # screens.rpy:346
    old "## Main Menu screen"
    new ""

    # screens.rpy:348
    old "## Used to display the main menu when Ren'Py starts."
    new ""

    # screens.rpy:350
    old "## https://www.renpy.org/doc/html/screen_special.html#main-menu"
    new ""

    # screens.rpy:354
    old "## This ensures that any other menu screen is replaced."
    new ""

    # screens.rpy:361
    old "## This empty frame darkens the main menu."
    new ""

    # screens.rpy:365
    old "## The use statement includes another screen inside this one. The actual contents of the main menu are in the navigation screen."
    new ""

    # screens.rpy:408
    old "## Game Menu screen"
    new ""

    # screens.rpy:410
    old "## This lays out the basic common structure of a game menu screen. It's called with the screen title, and displays the background, title, and navigation."
    new ""

    # screens.rpy:413
    old "## The scroll parameter can be None, or one of \"viewport\" or \"vpgrid\". When this screen is intended to be used with one or more children, which are transcluded (placed) inside it."
    new ""

    # screens.rpy:431
    old "## Reserve space for the navigation section."
    new ""

    # screens.rpy:473
    old "Return"
    new ""

    # screens.rpy:536
    old "## About screen"
    new ""

    # screens.rpy:538
    old "## This screen gives credit and copyright information about the game and Ren'Py."
    new ""

    # screens.rpy:541
    old "## There's nothing special about this screen, and hence it also serves as an example of how to make a custom screen."
    new ""

    # screens.rpy:548
    old "## This use statement includes the game_menu screen inside this one. The vbox child is then included inside the viewport inside the game_menu screen."
    new ""

    # screens.rpy:558
    old "Version [config.version!t]\n"
    new ""

    # screens.rpy:560
    old "## gui.about is usually set in options.rpy."
    new ""

    # screens.rpy:564
    old "Made with {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only].\n\n[renpy.license!t]"
    new ""

    # screens.rpy:567
    old "## This is redefined in options.rpy to add text to the about screen."
    new ""

    # screens.rpy:579
    old "## Load and Save screens"
    new ""

    # screens.rpy:581
    old "## These screens are responsible for letting the player save the game and load it again. Since they share nearly everything in common, both are implemented in terms of a third screen, file_slots."
    new ""

    # screens.rpy:585
    old "## https://www.renpy.org/doc/html/screen_special.html#save https://www.renpy.org/doc/html/screen_special.html#load"
    new ""

    # screens.rpy:604
    old "Page {}"
    new ""

    # screens.rpy:604
    old "Automatic saves"
    new ""

    # screens.rpy:604
    old "Quick saves"
    new ""

    # screens.rpy:610
    old "## This ensures the input will get the enter event before any of the buttons do."
    new ""

    # screens.rpy:614
    old "## The page name, which can be edited by clicking on a button."
    new ""

    # screens.rpy:626
    old "## The grid of file slots."
    new ""

    # screens.rpy:646
    old "{#file_time}%A, %B %d %Y, %H:%M"
    new ""

    # screens.rpy:646
    old "empty slot"
    new ""

    # screens.rpy:654
    old "## Buttons to access other pages."
    new ""

    # screens.rpy:663
    old "<"
    new ""

    # screens.rpy:666
    old "{#auto_page}A"
    new ""

    # screens.rpy:669
    old "{#quick_page}Q"
    new ""

    # screens.rpy:671
    old "## range(1, 10) gives the numbers from 1 to 9."
    new ""

    # screens.rpy:675
    old ">"
    new ""

    # screens.rpy:710
    old "## Preferences screen"
    new ""

    # screens.rpy:712
    old "## The preferences screen allows the player to configure the game to better suit themselves."
    new ""

    # screens.rpy:715
    old "## https://www.renpy.org/doc/html/screen_special.html#preferences"
    new ""

    # screens.rpy:732
    old "Display"
    new ""

    # screens.rpy:733
    old "Window"
    new ""

    # screens.rpy:734
    old "Fullscreen"
    new ""

    # screens.rpy:738
    old "Rollback Side"
    new ""

    # screens.rpy:739
    old "Disable"
    new ""

    # screens.rpy:740
    old "Left"
    new ""

    # screens.rpy:741
    old "Right"
    new ""

    # screens.rpy:746
    old "Unseen Text"
    new ""

    # screens.rpy:747
    old "After Choices"
    new ""

    # screens.rpy:748
    old "Transitions"
    new ""

    # screens.rpy:750
    old "## Additional vboxes of type \"radio_pref\" or \"check_pref\" can be added here, to add additional creator-defined preferences."
    new ""

    # screens.rpy:761
    old "Text Speed"
    new ""

    # screens.rpy:765
    old "Auto-Forward Time"
    new ""

    # screens.rpy:772
    old "Music Volume"
    new ""

    # screens.rpy:779
    old "Sound Volume"
    new ""

    # screens.rpy:785
    old "Test"
    new ""

    # screens.rpy:789
    old "Voice Volume"
    new ""

    # screens.rpy:800
    old "Mute All"
    new ""

    # screens.rpy:876
    old "## History screen"
    new ""

    # screens.rpy:878
    old "## This is a screen that displays the dialogue history to the player. While there isn't anything special about this screen, it does have to access the dialogue history stored in _history_list."
    new ""

    # screens.rpy:882
    old "## https://www.renpy.org/doc/html/history.html"
    new ""

    # screens.rpy:888
    old "## Avoid predicting this screen, as it can be very large."
    new ""

    # screens.rpy:899
    old "## This lays things out properly if history_height is None."
    new ""

    # screens.rpy:909
    old "## Take the color of the who text from the Character, if set."
    new ""

    # screens.rpy:918
    old "The dialogue history is empty."
    new ""

    # screens.rpy:921
    old "## This determines what tags are allowed to be displayed on the history screen."
    new ""

    # screens.rpy:968
    old "## Help screen"
    new ""

    # screens.rpy:970
    old "## A screen that gives information about key and mouse bindings. It uses other screens (keyboard_help, mouse_help, and gamepad_help) to display the actual help."
    new ""

    # screens.rpy:989
    old "Keyboard"
    new ""

    # screens.rpy:990
    old "Mouse"
    new ""

    # screens.rpy:993
    old "Gamepad"
    new ""

    # screens.rpy:1006
    old "Enter"
    new ""

    # screens.rpy:1007
    old "Advances dialogue and activates the interface."
    new ""

    # screens.rpy:1010
    old "Space"
    new ""

    # screens.rpy:1011
    old "Advances dialogue without selecting choices."
    new ""

    # screens.rpy:1014
    old "Arrow Keys"
    new ""

    # screens.rpy:1015
    old "Navigate the interface."
    new ""

    # screens.rpy:1018
    old "Escape"
    new ""

    # screens.rpy:1019
    old "Accesses the game menu."
    new ""

    # screens.rpy:1022
    old "Ctrl"
    new ""

    # screens.rpy:1023
    old "Skips dialogue while held down."
    new ""

    # screens.rpy:1026
    old "Tab"
    new ""

    # screens.rpy:1027
    old "Toggles dialogue skipping."
    new ""

    # screens.rpy:1030
    old "Page Up"
    new ""

    # screens.rpy:1031
    old "Rolls back to earlier dialogue."
    new ""

    # screens.rpy:1034
    old "Page Down"
    new ""

    # screens.rpy:1035
    old "Rolls forward to later dialogue."
    new ""

    # screens.rpy:1039
    old "Hides the user interface."
    new ""

    # screens.rpy:1043
    old "Takes a screenshot."
    new ""

    # screens.rpy:1047
    old "Toggles assistive {a=https://www.renpy.org/l/voicing}self-voicing{/a}."
    new ""

    # screens.rpy:1053
    old "Left Click"
    new ""

    # screens.rpy:1057
    old "Middle Click"
    new ""

    # screens.rpy:1061
    old "Right Click"
    new ""

    # screens.rpy:1065
    old "Mouse Wheel Up\nClick Rollback Side"
    new ""

    # screens.rpy:1069
    old "Mouse Wheel Down"
    new ""

    # screens.rpy:1076
    old "Right Trigger\nA/Bottom Button"
    new ""

    # screens.rpy:1080
    old "Left Trigger\nLeft Shoulder"
    new ""

    # screens.rpy:1084
    old "Right Shoulder"
    new ""

    # screens.rpy:1089
    old "D-Pad, Sticks"
    new ""

    # screens.rpy:1093
    old "Start, Guide"
    new ""

    # screens.rpy:1097
    old "Y/Top Button"
    new ""

    # screens.rpy:1100
    old "Calibrate"
    new ""

    # screens.rpy:1128
    old "## Additional screens"
    new ""

    # screens.rpy:1132
    old "## Confirm screen"
    new ""

    # screens.rpy:1134
    old "## The confirm screen is called when Ren'Py wants to ask the player a yes or no question."
    new ""

    # screens.rpy:1137
    old "## https://www.renpy.org/doc/html/screen_special.html#confirm"
    new ""

    # screens.rpy:1141
    old "## Ensure other screens do not get input while this screen is displayed."
    new ""

    # screens.rpy:1165
    old "Yes"
    new ""

    # screens.rpy:1166
    old "No"
    new ""

    # screens.rpy:1168
    old "## Right-click and escape answer \"no\"."
    new ""

    # screens.rpy:1195
    old "## Skip indicator screen"
    new ""

    # screens.rpy:1197
    old "## The skip_indicator screen is displayed to indicate that skipping is in progress."
    new ""

    # screens.rpy:1200
    old "## https://www.renpy.org/doc/html/screen_special.html#skip-indicator"
    new ""

    # screens.rpy:1212
    old "Skipping"
    new ""

    # screens.rpy:1219
    old "## This transform is used to blink the arrows one after another."
    new ""

    # screens.rpy:1246
    old "## We have to use a font that has the BLACK RIGHT-POINTING SMALL TRIANGLE glyph in it."
    new ""

    # screens.rpy:1251
    old "## Notify screen"
    new ""

    # screens.rpy:1253
    old "## The notify screen is used to show the player a message. (For example, when the game is quicksaved or a screenshot has been taken.)"
    new ""

    # screens.rpy:1256
    old "## https://www.renpy.org/doc/html/screen_special.html#notify-screen"
    new ""

    # screens.rpy:1290
    old "## NVL screen"
    new ""

    # screens.rpy:1292
    old "## This screen is used for NVL-mode dialogue and menus."
    new ""

    # screens.rpy:1294
    old "## https://www.renpy.org/doc/html/screen_special.html#nvl"
    new ""

    # screens.rpy:1305
    old "## Displays dialogue in either a vpgrid or the vbox."
    new ""

    # screens.rpy:1318
    old "## Displays the menu, if given. The menu may be displayed incorrectly if config.narrator_menu is set to True, as it is above."
    new ""

    # screens.rpy:1348
    old "## This controls the maximum number of NVL-mode entries that can be displayed at once."
    new ""

    # screens.rpy:1410
    old "## Mobile Variants"
    new ""

    # screens.rpy:1417
    old "## Since a mouse may not be present, we replace the quick menu with a version that uses fewer and bigger buttons that are easier to touch."
    new ""

    # screens.rpy:1435
    old "Menu"
    new ""

