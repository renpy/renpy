
translate ukrainian strings:

    # gui/game/options.rpy:1
    old "## This file contains options that can be changed to customize your game."
    new "## Цей файл містить параметри, які можна змінити, щоб налаштувати гру."

    # gui/game/options.rpy:4
    old "## Lines beginning with two '#' marks are comments, and you shouldn't uncomment them. Lines beginning with a single '#' mark are commented-out code, and you may want to uncomment them when appropriate."
    new "## Рядки, що починаються з двох позначок «#», є коментарями, і ви не повинні розкоментувати їх. Рядки, що починаються з одного знака «#», є закоментованим кодом, і ви можете за потреби розкоментувати їх."

    # gui/game/options.rpy:10
    old "## Basics"
    new "## Основи"

    # gui/game/options.rpy:12
    old "## A human-readable name of the game. This is used to set the default window title, and shows up in the interface and error reports."
    new "## Зрозуміла назва гри. Це використовується для встановлення заголовка вікна за замовчуванням і відображається в інтерфейсі та звітах про помилки."

    # gui/game/options.rpy:15
    old "## The _() surrounding the string marks it as eligible for translation."
    new "## _() навколо рядка позначає його як придатний для перекладу."

    # gui/game/options.rpy:17
    old "Ren'Py 7 Default GUI"
    new "Графічний інтерфейс Ren'Py 7 за замовчуванням"

    # gui/game/options.rpy:20
    old "## Determines if the title given above is shown on the main menu screen. Set this to False to hide the title."
    new "## Визначає, чи заголовок, наведений вище, відображається на екрані головного меню. Встановіть значення False, щоб приховати назву."

    # gui/game/options.rpy:26
    old "## The version of the game."
    new "## Версія гри."

    # gui/game/options.rpy:31
    old "## Text that is placed on the game's about screen. Place the text between the triple-quotes, and leave a blank line between paragraphs."
    new "## Текст, який розміщується на екрані інформації про гру. Поставте текст між потрійними лапками, а між абзацами залиште порожній рядок."

    # gui/game/options.rpy:38
    old "## A short name for the game used for executables and directories in the built distribution. This must be ASCII-only, and must not contain spaces, colons, or semicolons."
    new "## Коротка назва гри, яка використовується для виконуваних файлів і каталогів у вбудованому дистрибутиві. Це має бути лише ASCII і не повинно містити пробілів, двокрапки чи крапки з комою."

    # gui/game/options.rpy:45
    old "## Sounds and music"
    new "## Звуки і музика"

    # gui/game/options.rpy:47
    old "## These three variables control, among other things, which mixers are shown to the player by default. Setting one of these to False will hide the appropriate mixer."
    new "## Ці три змінні керують, серед іншого, тим, які міксери відображаються гравцеві за замовчуванням. Встановлення для одного з них значення False приховає відповідний мікшер."

    # gui/game/options.rpy:56
    old "## To allow the user to play a test sound on the sound or voice channel, uncomment a line below and use it to set a sample sound to play."
    new "## Щоб дозволити користувачеві відтворювати тестовий звук на звуковому або голосовому каналі, розкоментуйте рядок нижче та використовуйте його, щоб встановити зразок звуку для відтворення."

    # gui/game/options.rpy:63
    old "## Uncomment the following line to set an audio file that will be played while the player is at the main menu. This file will continue playing into the game, until it is stopped or another file is played."
    new "## Розкоментуйте наступний рядок, щоб налаштувати аудіофайл, який відтворюватиметься, коли плеєр перебуває в головному меню. Цей файл продовжуватиме відтворюватися в грі, доки його не буде зупинено або не буде відтворено інший файл."

    # gui/game/options.rpy:70
    old "## Transitions"
    new "## Переходи"

    # gui/game/options.rpy:72
    old "## These variables set transitions that are used when certain events occur. Each variable should be set to a transition, or None to indicate that no transition should be used."
    new "## Ці змінні встановлюють переходи, які використовуються, коли відбуваються певні події. Кожна змінна має бути встановлена на перехід або None, щоб вказати, що перехід не слід використовувати."

    # gui/game/options.rpy:76
    old "## Entering or exiting the game menu."
    new "## Вхід або вихід з меню гри."

    # gui/game/options.rpy:82
    old "## Between screens of the game menu."
    new "## Між екранами меню гри"

    # gui/game/options.rpy:87
    old "## A transition that is used after a game has been loaded."
    new "## Перехід, що використовується після завантаження гри."

    # gui/game/options.rpy:92
    old "## Used when entering the main menu after the game has ended."
    new "## Використовується під час входу в головне меню після завершення гри."

    # gui/game/options.rpy:97
    old "## A variable to set the transition used when the game starts does not exist. Instead, use a with statement after showing the initial scene."
    new "## Змінна для встановлення переходу, який використовується під час запуску гри, не існує. Замість цього використовуйте оператор with після показу початкової сцени."

    # gui/game/options.rpy:102
    old "## Window management"
    new "## Керування вікнами"

    # gui/game/options.rpy:104
    old "## This controls when the dialogue window is displayed. If \"show\", it is always displayed. If \"hide\", it is only displayed when dialogue is present. If \"auto\", the window is hidden before scene statements and shown again once dialogue is displayed."
    new "## Цей параметр визначає час відображення діалогового вікна. Якщо \"show\", він завжди відображається. Якщо \"hide\", воно відображається лише за наявності діалогу. Якщо \"auto\", вікно буде приховано перед операторами сцени та показано знову, коли відобразиться діалог."

    # gui/game/options.rpy:109
    old "## After the game has started, this can be changed with the \"window show\", \"window hide\", and \"window auto\" statements."
    new "## Після початку гри це можна змінити за допомогою операторів \"window show\", \"window hide\" і \"window auto\"."

    # gui/game/options.rpy:115
    old "## Transitions used to show and hide the dialogue window"
    new "## Переходи, які використовуються для показу та приховування діалогового вікна"

    # gui/game/options.rpy:121
    old "## Preference defaults"
    new "## Параметри за замовчуванням"

    # gui/game/options.rpy:123
    old "## Controls the default text speed. The default, 0, is infinite, while any other number is the number of characters per second to type out."
    new "## Керує швидкістю тексту за замовчуванням. За замовчуванням, 0, є нескінченним, тоді як будь-яке інше число означає кількість символів за секунду, які потрібно ввести."

    # gui/game/options.rpy:129
    old "## The default auto-forward delay. Larger numbers lead to longer waits, with 0 to 30 being the valid range."
    new "## Затримка автоматичного пересилання за замовчуванням. Більші числа призводять до довшого очікування, при цьому допустимим діапазоном є від 0 до 30."

    # gui/game/options.rpy:135
    old "## Save directory"
    new "## Зберегти каталог"

    # gui/game/options.rpy:137
    old "## Controls the platform-specific place Ren'Py will place the save files for this game. The save files will be placed in:"
    new "## Контролює місце, де Ren'Py буде розміщувати файли збереження для цієї гри. Файли збереження будуть розміщені в:"

    # gui/game/options.rpy:140
    old "## Windows: %APPDATA\\RenPy\\<config.save_directory>"
    new "## Windows: %APPDATA\\RenPy\\<config.save_directory>"

    # gui/game/options.rpy:142
    old "## Macintosh: $HOME/Library/RenPy/<config.save_directory>"
    new "## Macintosh: $HOME/Library/RenPy/<config.save_directory>"

    # gui/game/options.rpy:144
    old "## Linux: $HOME/.renpy/<config.save_directory>"
    new "## Linux: $HOME/.renpy/<config.save_directory>"

    # gui/game/options.rpy:146
    old "## This generally should not be changed, and if it is, should always be a literal string, not an expression."
    new "## Як правило, це не слід змінювати, і якщо це так, завжди має бути літеральний рядок, а не вираз."

    # gui/game/options.rpy:152
    old "## Icon"
    new "## Значок"

    # gui/game/options.rpy:154
    old "## The icon displayed on the taskbar or dock."
    new "## Значок, що відображається на панелі завдань або док-станції."

    # gui/game/options.rpy:159
    old "## Build configuration"
    new "## Створити конфігурацію"

    # gui/game/options.rpy:161
    old "## This section controls how Ren'Py turns your project into distribution files."
    new "## Цей розділ керує тим, як Ren'Py перетворює ваш проєкт у файли розповсюдження."

    # gui/game/options.rpy:166
    old "## The following functions take file patterns. File patterns are case- insensitive, and matched against the path relative to the base directory, with and without a leading /. If multiple patterns match, the first is used."
    new "## Наступні функції приймають шаблони файлів. Шаблони файлів не чутливі до регістру та зіставляються зі шляхом відносно основного каталогу, з / без нього на початку. Якщо збігається декілька шаблонів, використовується перший."

    # gui/game/options.rpy:171
    old "## In a pattern:"
    new "## У шаблоні:"

    # gui/game/options.rpy:173
    old "## / is the directory separator."
    new "## / є роздільником каталогу."

    # gui/game/options.rpy:175
    old "## * matches all characters, except the directory separator."
    new "## * відповідає всім символам, крім роздільника каталогу."

    # gui/game/options.rpy:177
    old "## ** matches all characters, including the directory separator."
    new "## ** відповідає всім символам, включаючи роздільник каталогу."

    # gui/game/options.rpy:179
    old "## For example, \"*.txt\" matches txt files in the base directory, \"game/**.ogg\" matches ogg files in the game directory or any of its subdirectories, and \"**.psd\" matches psd files anywhere in the project."
    new "## Наприклад, \"*.txt\" відповідає файлам txt у базовому каталозі, \"game/**.ogg\" відповідає файлам ogg у каталозі гри або будь-якому з його підкаталогів, а \"**.psd \" відповідає файлам psd будь-де в проєкті."

    # gui/game/options.rpy:183
    old "## Classify files as None to exclude them from the built distributions."
    new "## Класифікуйте файли як None, щоб виключити їх із вбудованих дистрибутивів."

    # gui/game/options.rpy:191
    old "## To archive files, classify them as 'archive'."
    new "## Щоб архівувати файли, класифікуйте їх як 'archive'."

    # gui/game/options.rpy:196
    old "## Files matching documentation patterns are duplicated in a mac app build, so they appear in both the app and the zip file."
    new "## Файли, що відповідають шаблонам документації, дублюються у створенні програми Mac, тому вони з’являються як у програмі, так і в zip-файлі."

    # gui/game/options.rpy:203
    old "## A Google Play license key is required to download expansion files and perform in-app purchases. It can be found on the \"Services & APIs\" page of the Google Play developer console."
    new "## Для завантаження файлів розширення та здійснення покупок у програмі потрібен ліцензійний ключ Google Play. Його можна знайти на сторінці \"Services & APIs\" консолі розробника Google Play."

    # gui/game/options.rpy:210
    old "## The username and project name associated with an itch.io project, separated by a slash."
    new "## Ім’я користувача та назва проєкту, пов’язані з проєктом itch.io, розділені скісною рискою."


translate ukrainian strings:

    # gui/game/options.rpy:203
    old "## A Google Play license key is required to perform in-app purchases. It can be found in the Google Play developer console, under \"Monetize\" > \"Monetization Setup\" > \"Licensing\"."
    # Automatic translation.
    new "## Для здійснення покупок у додатку потрібен ліцензійний ключ Google Play. Його можна знайти в консолі розробника Google Play у розділі \"Монетизація\" > \"Налаштування монетизації\" > \"Ліцензування\"."

