
translate russian strings:

    # screens.rpy:9
    old "## Styles"
    new "## Стили"

    # screens.rpy:81
    old "## In-game screens"
    new "## Внутриигровые экраны"

    # screens.rpy:85
    old "## Say screen"
    new "## Экран разговора"

    # screens.rpy:87
    old "## The say screen is used to display dialogue to the player. It takes two parameters, who and what, which are the name of the speaking character and the text to be displayed, respectively. (The who parameter can be None if no name is given.)"
    new "## Экран разговора используется для показа диалога игроку. Он использует два параметра — who и what — что, соответственно, имя говорящего персонажа и показываемый текст. (Параметр who может быть None, если имя не задано.)"

    # screens.rpy:92
    old "## This screen must create a text displayable with id \"what\", as Ren'Py uses this to manage text display. It can also create displayables with id \"who\" and id \"window\" to apply style properties."
    new "## Этот экран должен создать текст с id \"what\", чтобы Ren'Py могла показать текст. Здесь также можно создать наложения с id \"who\" и id \"window\", чтобы применить к ним настройки стиля."

    # screens.rpy:96
    old "## https://www.renpy.org/doc/html/screen_special.html#say"
    new "## https://www.renpy.org/doc/html/screen_special.html#say"

    # screens.rpy:114
    old "## If there's a side image, display it above the text. Do not display on the phone variant - there's no room."
    new "## Если есть боковое изображение (\"голова\"), показывает её поверх текста. По стандарту не показывается на варианте для мобильных устройств — мало места."

    # screens.rpy:120
    old "## Make the namebox available for styling through the Character object."
    new "## Делает namebox доступным для стилизации через объект Character."

    # screens.rpy:164
    old "## Input screen"
    new "## Экран ввода"

    # screens.rpy:166
    old "## This screen is used to display renpy.input. The prompt parameter is used to pass a text prompt in."
    new "## Этот экран используется, чтобы показывать renpy.input. Это параметр запроса, используемый для того, чтобы дать игроку ввести в него текст."

    # screens.rpy:169
    old "## This screen must create an input displayable with id \"input\" to accept the various input parameters."
    new "## Этот экран должен создать наложение ввода с id \"input\", чтобы принять различные вводимые параметры."

    # screens.rpy:172
    old "## https://www.renpy.org/doc/html/screen_special.html#input"
    new "## https://www.renpy.org/doc/html/screen_special.html#input"

    # screens.rpy:199
    old "## Choice screen"
    new "## Экран выбора"

    # screens.rpy:201
    old "## This screen is used to display the in-game choices presented by the menu statement. The one parameter, items, is a list of objects, each with caption and action fields."
    new "## Этот экран используется, чтобы показывать внутриигровые выборы, представленные оператором menu. Один параметр, вложения, список объектов, каждый с заголовком и полями действия."

    # screens.rpy:205
    old "## https://www.renpy.org/doc/html/screen_special.html#choice"
    new "## https://www.renpy.org/doc/html/screen_special.html#choice"

    # screens.rpy:215
    old "## When this is true, menu captions will be spoken by the narrator. When false, menu captions will be displayed as empty buttons."
    new "## Когда этот параметр True, заголовки меню будут проговариваться рассказчиком. Когда False, заголовки меню будут показаны как пустые кнопки."

    # screens.rpy:238
    old "## Quick Menu screen"
    new "## Экран быстрого меню"

    # screens.rpy:240
    old "## The quick menu is displayed in-game to provide easy access to the out-of-game menus."
    new "## Быстрое меню показывается внутри игры, чтобы обеспечить лёгкий доступ к внеигровым меню."

    # screens.rpy:245
    old "## Ensure this appears on top of other screens."
    new "## Гарантирует, что оно появляется поверх других экранов."

    # screens.rpy:256
    old "Back"
    new "Назад"

    # screens.rpy:257
    old "History"
    new "История"

    # screens.rpy:258
    old "Skip"
    new "Пропуск"

    # screens.rpy:259
    old "Auto"
    new "Авто"

    # screens.rpy:260
    old "Save"
    new "Сохранить"

    # screens.rpy:261
    old "Q.Save"
    new "Б.Сохр"

    # screens.rpy:262
    old "Q.Load"
    new "Б.Загр"

    # screens.rpy:263
    old "Prefs"
    new "Опции"

    # screens.rpy:266
    old "## This code ensures that the quick_menu screen is displayed in-game, whenever the player has not explicitly hidden the interface."
    new "## Данный код гарантирует, что экран быстрого меню будет показан в игре в любое время, если только игрок не скроет интерфейс."

    # screens.rpy:284
    old "## Main and Game Menu Screens"
    new "## Экраны Главного и Игрового меню"

    # screens.rpy:287
    old "## Navigation screen"
    new "## Экран навигации"

    # screens.rpy:289
    old "## This screen is included in the main and game menus, and provides navigation to other menus, and to start the game."
    new "## Этот экран включает в себя главное и игровое меню, и обеспечивает навигацию к другим меню и к началу игры."

    # screens.rpy:304
    old "Start"
    new "Начать"

    # screens.rpy:312
    old "Load"
    new "Загрузить"

    # screens.rpy:314
    old "Preferences"
    new "Настройки"

    # screens.rpy:318
    old "End Replay"
    new "Завершить повтор"

    # screens.rpy:322
    old "Main Menu"
    new "Главное меню"

    # screens.rpy:324
    old "About"
    new "Об игре"

    # screens.rpy:328
    old "## Help isn't necessary or relevant to mobile devices."
    new "## Помощь не необходима и не относится к мобильным устройствам."

    # screens.rpy:329
    old "Help"
    new "Помощь"

    # screens.rpy:331
    old "## The quit button is banned on iOS and unnecessary on Android and Web."
    new "## Кнопка выхода блокирована в iOS и не нужна на Android и в веб-версии."

    # screens.rpy:332
    old "Quit"
    new "Выход"

    # screens.rpy:346
    old "## Main Menu screen"
    new "## Экран главного меню"

    # screens.rpy:348
    old "## Used to display the main menu when Ren'Py starts."
    new "## Используется, чтобы показать главное меню после запуска игры."

    # screens.rpy:350
    old "## https://www.renpy.org/doc/html/screen_special.html#main-menu"
    new "## https://www.renpy.org/doc/html/screen_special.html#main-menu"

    # screens.rpy:354
    old "## This ensures that any other menu screen is replaced."
    new "## Этот тег гарантирует, что любой другой экран с тем же тегом будет заменять этот."

    # screens.rpy:361
    old "## This empty frame darkens the main menu."
    new "## Эта пустая рамка затеняет главное меню."

    # screens.rpy:365
    old "## The use statement includes another screen inside this one. The actual contents of the main menu are in the navigation screen."
    new "## Оператор use включает отображение другого экрана в данном. Актуальное содержание главного меню находится на экране навигации."

    # screens.rpy:408
    old "## Game Menu screen"
    new "## Экран игрового меню"

    # screens.rpy:410
    old "## This lays out the basic common structure of a game menu screen. It's called with the screen title, and displays the background, title, and navigation."
    new "## Всё это показывает основную, обобщённую структуру экрана игрового меню. Он вызывается с экраном заголовка и показывает фон, заголовок и навигацию."

    # screens.rpy:413
    old "## The scroll parameter can be None, or one of \"viewport\" or \"vpgrid\". When this screen is intended to be used with one or more children, which are transcluded (placed) inside it."
    new "## Параметр scroll может быть None, или \"viewport\", или \"vpgrid\", когда этот экран предназначается для использования с более чем одним дочерним экраном, включённым в него."

    # screens.rpy:431
    old "## Reserve space for the navigation section."
    new "## Резервирует пространство для навигации."

    # screens.rpy:473
    old "Return"
    new "Вернуться"

    # screens.rpy:536
    old "## About screen"
    new "## Экран Об игре"

    # screens.rpy:538
    old "## This screen gives credit and copyright information about the game and Ren'Py."
    new "## Этот экран показывает авторскую информацию об игре и Ren'Py."

    # screens.rpy:541
    old "## There's nothing special about this screen, and hence it also serves as an example of how to make a custom screen."
    new "## В этом экране нет ничего особенного, и он служит только примером того, каким можно сделать свой экран."

    # screens.rpy:548
    old "## This use statement includes the game_menu screen inside this one. The vbox child is then included inside the viewport inside the game_menu screen."
    new "## Этот оператор включает игровое меню внутрь этого экрана. Дочерний vbox включён в порт просмотра внутри экрана игрового меню."

    # screens.rpy:558
    old "Version [config.version!t]\n"
    new "Версия [config.version!t]\n"

    # screens.rpy:560
    old "## gui.about is usually set in options.rpy."
    new "## gui.about обычно установлено в options.rpy."

    # screens.rpy:564
    old "Made with {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only].\n\n[renpy.license!t]"
    new "Сделано с помощью {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only].\n\n[renpy.license!t]"

    # screens.rpy:567
    old "## This is redefined in options.rpy to add text to the about screen."
    new "## Это переустанавливается в options.rpy для добавления текста на экран Об игре."

    # screens.rpy:579
    old "## Load and Save screens"
    new "## Экраны загрузки и сохранения"

    # screens.rpy:581
    old "## These screens are responsible for letting the player save the game and load it again. Since they share nearly everything in common, both are implemented in terms of a third screen, file_slots."
    new "## Эти экраны ответственны за возможность сохранять и загружать игру. Так как они почти одинаковые, оба реализованы по правилам третьего экрана — file_slots."

    # screens.rpy:585
    old "## https://www.renpy.org/doc/html/screen_special.html#save https://www.renpy.org/doc/html/screen_special.html#load"
    new "## https://www.renpy.org/doc/html/screen_special.html#save \n https://www.renpy.org/doc/html/screen_special.html#load"

    # screens.rpy:604
    old "Page {}"
    new "{} страница"

    # screens.rpy:604
    old "Automatic saves"
    new "Автосохранения"

    # screens.rpy:604
    old "Quick saves"
    new "Быстрые сохранения"

    # screens.rpy:610
    old "## This ensures the input will get the enter event before any of the buttons do."
    new "## Это гарантирует, что ввод будет принимать enter перед остальными кнопками."

    # screens.rpy:614
    old "## The page name, which can be edited by clicking on a button."
    new "## Номер страницы, который может быть изменён посредством клика на кнопку."

    # screens.rpy:626
    old "## The grid of file slots."
    new "## Таблица слотов."

    # screens.rpy:646
    old "{#file_time}%A, %B %d %Y, %H:%M"
    new "{#file_time}%A, %d %B %Y, %H:%M"

    # screens.rpy:646
    old "empty slot"
    new "Пустой слот"

    # screens.rpy:654
    old "## Buttons to access other pages."
    new "## Кнопки для доступа к другим страницам."

    # screens.rpy:663
    old "<"
    new "<"

    # screens.rpy:666
    old "{#auto_page}A"
    new "{#auto_page}А"

    # screens.rpy:669
    old "{#quick_page}Q"
    new "{#quick_page}Б"

    # screens.rpy:671
    old "## range(1, 10) gives the numbers from 1 to 9."
    new "## range(1, 10) задаёт диапазон значений от 1 до 9."

    # screens.rpy:675
    old ">"
    new ">"

    # screens.rpy:710
    old "## Preferences screen"
    new "## Экран настроек"

    # screens.rpy:712
    old "## The preferences screen allows the player to configure the game to better suit themselves."
    new "## Экран настроек позволяет игроку настраивать игру под себя."

    # screens.rpy:715
    old "## https://www.renpy.org/doc/html/screen_special.html#preferences"
    new "## https://www.renpy.org/doc/html/screen_special.html#preferences"

    # screens.rpy:732
    old "Display"
    new "Режим экрана"

    # screens.rpy:733
    old "Window"
    new "Оконный"

    # screens.rpy:734
    old "Fullscreen"
    new "Полный"

    # screens.rpy:738
    old "Rollback Side"
    new "Сторона отката"

    # screens.rpy:739
    old "Disable"
    new "Отключено"

    # screens.rpy:740
    old "Left"
    new "Левая"

    # screens.rpy:741
    old "Right"
    new "Правая"

    # screens.rpy:746
    old "Unseen Text"
    new "Всего текста"

    # screens.rpy:747
    old "After Choices"
    new "После выборов"

    # screens.rpy:748
    old "Transitions"
    new "Переходов"

    # screens.rpy:750
    old "## Additional vboxes of type \"radio_pref\" or \"check_pref\" can be added here, to add additional creator-defined preferences."
    new "## Дополнительные vbox'ы типа \"radio_pref\" или \"check_pref\" могут быть добавлены сюда для добавления новых настроек."

    # screens.rpy:761
    old "Text Speed"
    new "Скорость текста"

    # screens.rpy:765
    old "Auto-Forward Time"
    new "Скорость авточтения"

    # screens.rpy:772
    old "Music Volume"
    new "Громкость музыки"

    # screens.rpy:779
    old "Sound Volume"
    new "Громкость звуков"

    # screens.rpy:785
    old "Test"
    new "Тест"

    # screens.rpy:789
    old "Voice Volume"
    new "Громкость голоса"

    # screens.rpy:800
    old "Mute All"
    new "Без звука"

    # screens.rpy:876
    old "## History screen"
    new "## Экран истории"

    # screens.rpy:878
    old "## This is a screen that displays the dialogue history to the player. While there isn't anything special about this screen, it does have to access the dialogue history stored in _history_list."
    new "## Этот экран показывает игроку историю диалогов. Хотя в этом экране нет ничего особенного, он имеет доступ к истории диалогов, хранимом в _history_list."

    # screens.rpy:882
    old "## https://www.renpy.org/doc/html/history.html"
    new "## https://www.renpy.org/doc/html/history.html"

    # screens.rpy:888
    old "## Avoid predicting this screen, as it can be very large."
    new "## Избегайте предсказывания этого экрана, так как он может быть очень массивным."

    # screens.rpy:899
    old "## This lays things out properly if history_height is None."
    new "## Это всё правильно уравняет, если history_height будет установлен на None."

    # screens.rpy:908
    old "## Take the color of the who text from the Character, if set."
    new "## Берёт цвет из who параметра персонажа, если он установлен."

    # screens.rpy:916
    old "The dialogue history is empty."
    new "История диалогов пуста."

    # screens.rpy:919
    old "## This determines what tags are allowed to be displayed on the history screen."
    new "## Это определяет, какие теги могут отображаться на экране истории."

    # screens.rpy:966
    old "## Help screen"
    new "## Экран помощи"

    # screens.rpy:968
    old "## A screen that gives information about key and mouse bindings. It uses other screens (keyboard_help, mouse_help, and gamepad_help) to display the actual help."
    new "## Экран, дающий информацию о клавишах управления. Он использует другие экраны (keyboard_help, mouse_help, и gamepad_help), чтобы показывать актуальную помощь."

    # screens.rpy:987
    old "Keyboard"
    new "Клавиатура"

    # screens.rpy:988
    old "Mouse"
    new "Мышь"

    # screens.rpy:991
    old "Gamepad"
    new "Геймпад"

    # screens.rpy:1004
    old "Enter"
    new "Enter"

    # screens.rpy:1005
    old "Advances dialogue and activates the interface."
    new "Прохождение диалогов, активация интерфейса."

    # screens.rpy:1008
    old "Space"
    new "Пробел"

    # screens.rpy:1009
    old "Advances dialogue without selecting choices."
    new "Прохождение диалогов без возможности делать выбор."

    # screens.rpy:1012
    old "Arrow Keys"
    new "Стрелки"

    # screens.rpy:1013
    old "Navigate the interface."
    new "Навигация по интерфейсу."

    # screens.rpy:1016
    old "Escape"
    new "Esc"

    # screens.rpy:1017
    old "Accesses the game menu."
    new "Вход в игровое меню."

    # screens.rpy:1020
    old "Ctrl"
    new "Ctrl"

    # screens.rpy:1021
    old "Skips dialogue while held down."
    new "Пропускает диалоги, пока зажат."

    # screens.rpy:1024
    old "Tab"
    new "Tab"

    # screens.rpy:1025
    old "Toggles dialogue skipping."
    new "Включает режим пропуска."

    # screens.rpy:1028
    old "Page Up"
    new "Page Up"

    # screens.rpy:1029
    old "Rolls back to earlier dialogue."
    new "Откат назад по сюжету игры."

    # screens.rpy:1032
    old "Page Down"
    new "Page Down"

    # screens.rpy:1033
    old "Rolls forward to later dialogue."
    new "Откатывает предыдущее действие вперёд."

    # screens.rpy:1037
    old "Hides the user interface."
    new "Скрывает интерфейс пользователя."

    # screens.rpy:1041
    old "Takes a screenshot."
    new "Делает снимок экрана."

    # screens.rpy:1045
    old "Toggles assistive {a=https://www.renpy.org/l/voicing}self-voicing{/a}."
    new "Включает поддерживаемый {a=https://www.renpy.org/l/voicing}синтезатор речи{/a}."

    # screens.rpy:1051
    old "Left Click"
    new "Левый клик"

    # screens.rpy:1055
    old "Middle Click"
    new "Клик колёсиком"

    # screens.rpy:1059
    old "Right Click"
    new "Правый клик"

    # screens.rpy:1063
    old "Mouse Wheel Up\nClick Rollback Side"
    new "Колёсико вверх\nКлик на сторону отката"

    # screens.rpy:1067
    old "Mouse Wheel Down"
    new "Колёсико вниз"

    # screens.rpy:1074
    old "Right Trigger\nA/Bottom Button"
    new "Правый триггер\nA/Нижняя кнопка"

    # screens.rpy:1078
    old "Left Trigger\nLeft Shoulder"
    new "Левый Триггер\nЛевый Бампер"

    # screens.rpy:1082
    old "Right Shoulder"
    new "Правый бампер"

    # screens.rpy:1087
    old "D-Pad, Sticks"
    new "Крестовина, Стики"

    # screens.rpy:1091
    old "Start, Guide"
    new "Start, Guide"

    # screens.rpy:1095
    old "Y/Top Button"
    new "Y/Верхняя кнопка"

    # screens.rpy:1098
    old "Calibrate"
    new "Калибровка"

    # screens.rpy:1126
    old "## Additional screens"
    new "## Дополнительные экраны"

    # screens.rpy:1130
    old "## Confirm screen"
    new "## Экран подтверждения"

    # screens.rpy:1132
    old "## The confirm screen is called when Ren'Py wants to ask the player a yes or no question."
    new "## Экран подтверждения вызывается, когда Ren'Py хочет спросить у игрока вопрос Да или Нет."

    # screens.rpy:1135
    old "## https://www.renpy.org/doc/html/screen_special.html#confirm"
    new "## https://www.renpy.org/doc/html/screen_special.html#confirm"

    # screens.rpy:1139
    old "## Ensure other screens do not get input while this screen is displayed."
    new "## Гарантирует, что другие экраны будут недоступны, пока показан этот экран."

    # screens.rpy:1163
    old "Yes"
    new "Да"

    # screens.rpy:1164
    old "No"
    new "Нет"

    # screens.rpy:1166
    old "## Right-click and escape answer \"no\"."
    new "## Правый клик и esc, как ответ \"Нет\"."

    # screens.rpy:1193
    old "## Skip indicator screen"
    new "## Экран индикатора пропуска"

    # screens.rpy:1195
    old "## The skip_indicator screen is displayed to indicate that skipping is in progress."
    new "## Экран индикатора пропуска появляется для того, чтобы показать, что идёт пропуск."

    # screens.rpy:1198
    old "## https://www.renpy.org/doc/html/screen_special.html#skip-indicator"
    new "## https://www.renpy.org/doc/html/screen_special.html#skip-indicator"

    # screens.rpy:1210
    old "Skipping"
    new "Пропускаю"

    # screens.rpy:1217
    old "## This transform is used to blink the arrows one after another."
    new "## Эта трансформация используется, чтобы мигать стрелками одна за другой."

    # screens.rpy:1244
    old "## We have to use a font that has the BLACK RIGHT-POINTING SMALL TRIANGLE glyph in it."
    new "## Нам надо использовать шрифт, имеющий в себе символ U+25B8 (стрелку выше)."

    # screens.rpy:1249
    old "## Notify screen"
    new "## Экран уведомлений"

    # screens.rpy:1251
    old "## The notify screen is used to show the player a message. (For example, when the game is quicksaved or a screenshot has been taken.)"
    new "## Экран уведомлений используется, чтобы показать игроку оповещение. (Например, когда игра автосохранилась, или был сделан скриншот)"

    # screens.rpy:1254
    old "## https://www.renpy.org/doc/html/screen_special.html#notify-screen"
    new "## https://www.renpy.org/doc/html/screen_special.html#notify-screen"

    # screens.rpy:1288
    old "## NVL screen"
    new "## Экран NVL"

    # screens.rpy:1290
    old "## This screen is used for NVL-mode dialogue and menus."
    new "## Этот экран используется в диалогах и меню режима NVL."

    # screens.rpy:1292
    old "## https://www.renpy.org/doc/html/screen_special.html#nvl"
    new "## https://www.renpy.org/doc/html/screen_special.html#nvl"

    # screens.rpy:1303
    old "## Displays dialogue in either a vpgrid or the vbox."
    new "## Показывает диалог или в vpgrid, или в vbox."

    # screens.rpy:1316
    old "## Displays the menu, if given. The menu may be displayed incorrectly if config.narrator_menu is set to True, as it is above."
    new "## Показывает меню, если есть. Меню может показываться некорректно, если config.narrator_menu установлено на True."

    # screens.rpy:1346
    old "## This controls the maximum number of NVL-mode entries that can be displayed at once."
    new "## Это контролирует максимальное число строк NVL, могущих показываться за раз."

    # screens.rpy:1408
    old "## Mobile Variants"
    new "## Мобильные варианты"

    # screens.rpy:1415
    old "## Since a mouse may not be present, we replace the quick menu with a version that uses fewer and bigger buttons that are easier to touch."
    new "## Раз мышь может не использоваться, мы заменили быстрое меню версией, использующей меньше кнопок, но больших по размеру, чтобы их было легче касаться."

    # screens.rpy:1431
    old "Menu"
    new "Меню"
