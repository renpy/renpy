
translate russian strings:

    # about.rpy:39
    old "[version!q]"
    new "[version!q]"

    # about.rpy:43
    old "View license"
    new "Посмотреть лицензию"

    # add_file.rpy:28
    old "FILENAME"
    new "ИМЯ ФАЙЛА"

    # add_file.rpy:28
    old "Enter the name of the script file to create."
    new "Введите имя файла сценария, который вы хотите создать."

    # add_file.rpy:31
    old "The filename must have the .rpy extension."
    new "Имя должно иметь расширение .rpy."

    # add_file.rpy:39
    old "The file already exists."
    new "Файл уже существует."

    # add_file.rpy:42
    old "# Ren'Py automatically loads all script files ending with .rpy. To use this\n# file, define a label and jump to it from another file.\n"
    new "# Ren'Py автоматически загружает все файлы сценариев, заканчивающиеся на .rpy\n#Чтобы использовать этот файл, определите метку и перейдите (jump) к ней из другого файла.\n"

    # android.rpy:30
    old "To build Android packages, please download RAPT, unzip it, and place it into the Ren'Py directory. Then restart the Ren'Py launcher."
    new "Чтобы построить Android-пакет, пожалуйста, загрузите RAPT, разархивируйте его и поместить в директорию Ren'Py. Затем перезагрузите лаунчер Ren'Py."

    # android.rpy:31
    old "A 32-bit Java Development Kit is required to build Android packages on Windows. The JDK is different from the JRE, so it's possible you have Java without having the JDK.\n\nPlease {a=http://www.oracle.com/technetwork/java/javase/downloads/index.html}download and install the JDK{/a}, then restart the Ren'Py launcher."
    new "Чтобы построить Android-пакеты на Windows требуется 32-разрядный инструментарий разработки Java. JDK отличен от JRE, и возможно, у вас есть Java без JDK.\n\nПожалуйста, {a=httpу://www.oracle.com/technetwork/java/javase/downloads/index.html}загрузите и установите JDK{/a}, и перезапустите лаунчер Ren'Py."

    # android.rpy:32
    old "RAPT has been installed, but you'll need to install the Android SDK before you can build Android packages. Choose Install SDK to do this."
    new "RAPT установлен, но вам понадобится установить Android SDK до того, как вы сможете создать Android-пакеты. Выберите \"Установить SDK\", чтобы сделать это."

    # android.rpy:33
    old "RAPT has been installed, but a key hasn't been configured. Please create a new key, or restore android.keystore."
    new "RAPT установлен, но отсутствует ключ. Пожалуйста, создайте новый ключ, или восстановите android.keystore."

    # android.rpy:34
    old "The current project has not been configured. Use \"Configure\" to configure it before building."
    new "Текущий проект не настроен. Используйте \"Настроить\", чтобы настроить его перед сборкой."

    # android.rpy:35
    old "Choose \"Build\" to build the current project, or attach an Android device and choose \"Build & Install\" to build and install it on the device."
    new "Выберите \"Построить\", чтобы собрать текущий проект, или присоедините Android-устройство и выберите \"Построить и Установить\", чтобы собрать и установить его на устройстве."

    # android.rpy:37
    old "Attempts to emulate an Android phone.\n\nTouch input is emulated through the mouse, but only when the button is held down. Escape is mapped to the menu button, and PageUp is mapped to the back button."
    new "Пытается эмулировать Android-телефон.\n\nПрикосновения имитируются мышью при зажатой кнопке. Escape назначен на кнопку меню, а PageUp - на кнопку назад."

    # android.rpy:38
    old "Attempts to emulate an Android tablet.\n\nTouch input is emulated through the mouse, but only when the button is held down. Escape is mapped to the menu button, and PageUp is mapped to the back button."
    new "Пытается эмулировать Android-планшет.\n\nПрикосновения имитируются мышью при зажатой кнопке. Escape назначен на кнопку меню, а PageUp - на кнопку назад."

    # android.rpy:39
    old "Attempts to emulate a televison-based Android console, like the OUYA or Fire TV.\n\nController input is mapped to the arrow keys, Enter is mapped to the select button, Escape is mapped to the menu button, and PageUp is mapped to the back button."
    new "Пытается эмулировать ориентированную на телевизор консоль Android, такую как OUYA или Fire TV.\n\nКонтроллер назначен стрелки, Enter назначен на кнопку выбора, Escape назначен на кнопку меню, а PageUp — на кнопку назад."

    # android.rpy:41
    old "Downloads and installs the Android SDK and supporting packages. Optionally, generates the keys required to sign the package."
    new "Скачивает и устанавливает Android SDK и поддерживающие пакеты. При желании, создаёт ключи для подписи пакета."

    # android.rpy:42
    old "Configures the package name, version, and other information about this project."
    new "Настраивает имя пакета, версию, и другую информацию о проекте."

    # android.rpy:43
    old "Opens the file containing the Google Play keys in the editor.\n\nThis is only needed if the application is using an expansion APK. Read the documentation for more details."
    new "Открывает файл, содержащий ключи Google Play в редакторе.\n\nЭто необходимо лишь для случаев, если приложение использует расширяющий APK. Прочтите документацию для больших деталей."

    # android.rpy:44
    old "Builds the Android package."
    new "Собирает Android-пакет."

    # android.rpy:45
    old "Builds the Android package, and installs it on an Android device connected to your computer."
    new "Собирает Android-пакет и устанавливает его на Android-устройстве, подключённом к компьютеру."

    # android.rpy:46
    old "Builds the Android package, installs it on an Android device connected to your computer, then launches the app on your device."
    new "Собирает Android-пакет, устанавливает его на Android-устройстве, подключённом к компьютеру, а затем запускает приложение на устройстве."

    # android.rpy:48
    old "Connects to an Android device running ADB in TCP/IP mode."
    new "Присоединение к Android-устройству с запущенным Android Debug Bridge в режиме TCP/IP."

    # android.rpy:49
    old "Disconnects from an Android device running ADB in TCP/IP mode."
    new "Отсоединение от Android-устройства с запущенным Android Debug Bridge в режиме TCP/IP."

    # android.rpy:50
    old "Retrieves the log from the Android device and writes it to a file."
    new "Берёт лог с Android-устройства и пишет его в файл."

    # android.rpy:240
    old "Copying Android files to distributions directory."
    new "Копирую файлы Android в директорию дистрибутивов."

    # android.rpy:304
    old "Android: [project.current.display_name!q]"
    new "Android: [project.current.display_name!q]"

    # android.rpy:324
    old "Emulation:"
    new "Эмуляция:"

    # android.rpy:333
    old "Phone"
    new "Телефон"

    # android.rpy:337
    old "Tablet"
    new "Планшет"

    # android.rpy:341
    old "Television"
    new "Телевизор"

    # android.rpy:353
    old "Build:"
    new "Собрать:"

    # android.rpy:361
    old "Install SDK & Create Keys"
    new "Установить SDK и создать ключи"

    # android.rpy:365
    old "Configure"
    new "Настроить"

    # android.rpy:369
    old "Build Package"
    new "Собрать Пакет"

    # android.rpy:373
    old "Build & Install"
    new "Собрать и Установить"

    # android.rpy:377
    old "Build, Install & Launch"
    new "Собрать, Установить и Запустить"

    # android.rpy:388
    old "Other:"
    new "Другое:"

    # android.rpy:396
    old "Remote ADB Connect"
    new "Удалённое Соединение с ADB"

    # android.rpy:400
    old "Remote ADB Disconnect"
    new "Удалённое Отсоединение от ADB"

    # android.rpy:404
    old "Logcat"
    new "Logcat"

    # android.rpy:437
    old "Before packaging Android apps, you'll need to download RAPT, the Ren'Py Android Packaging Tool. Would you like to download RAPT now?"
    new "Перед тем как собирать приложения Android, вам нужно загрузить RAPT, инструмент Ren'Py для сбора пакетов Android. Хотите загрузить RAPT сейчас?"

    # android.rpy:496
    old "Remote ADB Address"
    new "Удалённый адрес ADB"

    # android.rpy:496
    old "Please enter the IP address and port number to connect to, in the form \"192.168.1.143:5555\". Consult your device's documentation to determine if it supports remote ADB, and if so, the address and port to use."
    new "Пожалуйста, введите IP-адрес и номер порта, чтобы соединиться с устройством, по форме \"192.168.1.143:5555\". Ознакомьтесь с документацией своего устройства, чтобы определить поддерживает ли оно удалённый ADB, и если так, адрес и порт для использования."

    # android.rpy:508
    old "Invalid remote ADB address"
    new "Неверный адрес удалённого ADB"

    # android.rpy:508
    old "The address must contain one exactly one ':'."
    new "Адрес должен содержать один, только один ':'."

    # android.rpy:512
    old "The host may not contain whitespace."
    new "Хост не может содержать пробелы."

    # android.rpy:518
    old "The port must be a number."
    new "Порт должен содержать только цифры."

    # android.rpy:544
    old "Retrieving logcat information from device."
    new "Извлекаю информацию logcat из устройства."

    # choose_directory.rpy:87
    old "Ren'Py was unable to run python with tkinter to choose the directory. Please install the python-tk or tkinter package."
    new "Ren'Py не удалось запустить python с tkinter, чтобы выбрать директорию. Пожалуйста, установите python-tk или пакет tkinter."

    # choose_directory.rpy:104
    old "The selected projects directory is not writable."
    new "Выбранная директория проектов недоступна для записи."

    # choose_theme.rpy:303
    old "Could not change the theme. Perhaps options.rpy was changed too much."
    new "Невозможно изменить тему. Возможно, options.rpy был сильно изменён."

    # choose_theme.rpy:370
    old "Planetarium"
    new "Планетарий"

    # choose_theme.rpy:425
    old "Choose Theme"
    new "Выберите тему"

    # choose_theme.rpy:438
    old "Theme"
    new "Тема"

    # choose_theme.rpy:463
    old "Color Scheme"
    new "Цветовая схема"

    # choose_theme.rpy:495
    old "Continue"
    new "Продолжить"

    # consolecommand.rpy:84
    old "INFORMATION"
    new "ИНФОРМАЦИЯ"

    # consolecommand.rpy:84
    old "The command is being run in a new operating system console window."
    new "Команда будет запущена в новом окне консоли операционной системы."

    # distribute.rpy:444
    old "Scanning project files..."
    new "Сканирую файлы проекта..."

    # distribute.rpy:460
    old "Building distributions failed:\n\nThe build.directory_name variable may not include the space, colon, or semicolon characters."
    new "Постройка дистрибутивов провалилась:\n\nПеременная build.directory_name (или её производная build.name) не должна содержать пробелов, двоеточий и точек с запятой."

    # distribute.rpy:505
    old "No packages are selected, so there's nothing to do."
    new "Пакеты не выбраны. Нечего делать."

    # distribute.rpy:517
    old "Scanning Ren'Py files..."
    new "Сканирую файлы Ren'Py..."

    # distribute.rpy:572
    old "All packages have been built.\n\nDue to the presence of permission information, unpacking and repacking the Linux and Macintosh distributions on Windows is not supported."
    new "Все пакеты были построены.\n\nВ связи с наличием информации о правах доступа, не распаковывайте дистрибутивы для Linux и Macintosh на Windows."

    # distribute.rpy:755
    old "Archiving files..."
    new "Архивирую файлы..."

    # distribute.rpy:1068
    old "Unpacking the Macintosh application for signing..."
    new "Распаковываю приложение Macintosh для подписи..."

    # distribute.rpy:1078
    old "Signing the Macintosh application...\n(This may take a long time.)"
    new "Подписываю приложение Macintosh...\n(Это может занять время.)"

    # distribute.rpy:1100
    old "Creating the Macintosh DMG..."
    new "Создаю Macintosh DMG..."

    # distribute.rpy:1109
    old "Signing the Macintosh DMG..."
    new "Подписываю Macintosh DMG..."

    # distribute.rpy:1304
    old "Writing the [variant] [format] package."
    new "Пишу пакет [variant] [format]"

    # distribute.rpy:1317
    old "Making the [variant] update zsync file."
    new "Создаю файл zsync для обновления [variant]"

    # distribute.rpy:1427
    old "Processed {b}[complete]{/b} of {b}[total]{/b} files."
    new "Обработано {b}[complete]{/b} из {b}[total]{/b} файлов."

    # distribute_gui.rpy:157
    old "Build Distributions: [project.current.display_name!q]"
    new "Сборка дистрибутивов: [project.current.display_name!q]"

    # distribute_gui.rpy:171
    old "Directory Name:"
    new "Имя Папки:"

    # distribute_gui.rpy:175
    old "Executable Name:"
    new "Имя исполняемого файла:"

    # distribute_gui.rpy:185
    old "Actions:"
    new "Действия"

    # distribute_gui.rpy:193
    old "Edit options.rpy"
    new "Редактировать options.rpy"

    # distribute_gui.rpy:194
    old "Add from clauses to calls, once"
    new "Один раз добавить функции from к calls"

    # distribute_gui.rpy:195
    old "Refresh"
    new "Обновить"

    # distribute_gui.rpy:199
    old "Upload to itch.io"
    new "Загрузить на itch.io"

    # distribute_gui.rpy:215
    old "Build Packages:"
    new "Построить пакеты:"

    # distribute_gui.rpy:234
    old "Options:"
    new "Опции:"

    # distribute_gui.rpy:239
    old "Build Updates"
    new "Обновить сборку"

    # distribute_gui.rpy:241
    old "Add from clauses to calls"
    new "Добавить функции from к calls"

    # distribute_gui.rpy:242
    old "Force Recompile"
    new "Перекомпилировать проект"

    # distribute_gui.rpy:246
    old "Build"
    new "Построить"

    # distribute_gui.rpy:250
    old "Adding from clauses to call statements that do not have them."
    new "Добавляю функции from к операторам call, если они их не имеют."

    # distribute_gui.rpy:271
    old "Errors were detected when running the project. Please ensure the project runs without errors before building distributions."
    new "При запуске проекта произошли ошибки. Пожалуйста, убедитесь в том, что проект успешно запускается, перед созданием дистрибутивов."

    # distribute_gui.rpy:288
    old "Your project does not contain build information. Would you like to add build information to the end of options.rpy?"
    new "Ваш проект не содержит информации, необходимой для сборки. Добавить её к концу options.rpy?"

    # dmgcheck.rpy:50
    old "Ren'Py is running from a read only folder. Some functionality will not work."
    new "Ren'Py запущена из директории только для чтения. Часть функционала может не работать."

    # dmgcheck.rpy:50
    old "This is probably because Ren'Py is running directly from a Macintosh drive image. To fix this, quit this launcher, copy the entire %s folder somewhere else on your computer, and run Ren'Py again."
    new "Вероятно, это из-за того, что Ren'Py запущена напрямую из образа диска Mac. Чтобы исправить это, выйдите из лаунчера и скопируйте всю папку %s куда-нибудь ещё на компьютер и снова запустите Ren'Py."

    # editor.rpy:150
    old "{b}Recommended.{/b} A beta editor with an easy to use interface and features that aid in development, such as spell-checking. Editra currently lacks the IME support required for Chinese, Japanese, and Korean text input."
    new "{b}Рекомендуется.{/b} Бета-редактор с простым интерфейсом и возможностями, помогающими в разработке, такими, как проверка орфографии. Editra на данный момент не поддерживает IME, необходимые для ввода Китайского, Японского и Корейского текстов."

    # editor.rpy:151
    old "{b}Recommended.{/b} A beta editor with an easy to use interface and features that aid in development, such as spell-checking. Editra currently lacks the IME support required for Chinese, Japanese, and Korean text input. On Linux, Editra requires wxPython."
    new "{b}Рекомендуется.{/b} Бета-редактор с простым интерфейсом и возможностями, помогающими в разработке, такими, как проверка орфографии. Editra на данный момент не поддерживает IME, необходимые для ввода Китайского, Японского и Корейского текстов. На Linux, Editra требует wxPython."

    # editor.rpy:167
    old "This may have occured because wxPython is not installed on this system."
    new "Это могло случиться из-за того, что wxPython не установлен на этой системе."

    # editor.rpy:169
    old "Up to 22 MB download required."
    new "Требуется скачать 22 МБ."

    # editor.rpy:182
    old "A mature editor that requires Java."
    new "Проверенный временем редактор. Требует Java."

    # editor.rpy:182
    old "1.8 MB download required."
    new "Требуется скачать 1.8 МБ."

    # editor.rpy:182
    old "This may have occured because Java is not installed on this system."
    new "Это могло случиться из-за того, что Java не установлена в данной системе."

    # editor.rpy:191
    old "Invokes the editor your operating system has associated with .rpy files."
    new "Включает текстовый редактор, ассоциированный в вашей системе с файлами .rpy."

    # editor.rpy:207
    old "Prevents Ren'Py from opening a text editor."
    new "Не позволяет Ren'Py запускать текстовый редактор."

    # editor.rpy:359
    old "An exception occured while launching the text editor:\n[exception!q]"
    new "Возникла ошибка при запуске текстового редактора:\n[exception!q]"

    # editor.rpy:457
    old "Select Editor"
    new "Выберите редактор"

    # editor.rpy:472
    old "A text editor is the program you'll use to edit Ren'Py script files. Here, you can select the editor Ren'Py will use. If not already present, the editor will be automatically downloaded and installed."
    new "Текстовый редактор — программа, необходимая для редактирования сценариев Ren'Py. Здесь, вы можете выбрать редактор, который будет использовать Ren'Py. Если такового нет, редактор будет автоматически загружен и установлен."

    # front_page.rpy:35
    old "Open [text] directory."
    new "Открыть папку [text]."

    # front_page.rpy:91
    old "PROJECTS:"
    new "ПРОЕКТЫ:"

    # front_page.rpy:93
    old "refresh"
    new "обновить"

    # front_page.rpy:120
    old "+ Create New Project"
    new "+ Добавить новый проект"

    # front_page.rpy:130
    old "Launch Project"
    new "Запустить проект"

    # front_page.rpy:147
    old "[p.name!q] (template)"
    new "[p.name!q] (образец)"

    # front_page.rpy:149
    old "Select project [text]."
    new "Выбрать проект [text]."

    # front_page.rpy:165
    old "Tutorial"
    new "Обучение"

    # front_page.rpy:166
    old "The Question"
    new "Вопрос"

    # front_page.rpy:182
    old "Active Project"
    new "Активный проект"

    # front_page.rpy:190
    old "Open Directory"
    new "Открыть Папку"

    # front_page.rpy:195
    old "game"
    new "game"

    # front_page.rpy:196
    old "base"
    new "base"

    # front_page.rpy:197
    old "images"
    new "images"

    # front_page.rpy:198
    old "gui"
    new "gui"

    # front_page.rpy:204
    old "Edit File"
    new "Редактировать Файл"

    # front_page.rpy:214
    old "All script files"
    new "Все файлы сценариев"

    # front_page.rpy:223
    old "Navigate Script"
    new "Навигация по Сценарию"

    # front_page.rpy:234
    old "Check Script (Lint)"
    new "Проверить сценарий (Lint)"

    # front_page.rpy:237
    old "Change/Update GUI"
    new "Изменить/Обновить GUI"

    # front_page.rpy:239
    old "Change Theme"
    new "Сменить тему"

    # front_page.rpy:242
    old "Delete Persistent"
    new "Очистить постоянные"

    # front_page.rpy:251
    old "Build Distributions"
    new "Построить дистрибутивы"

    # front_page.rpy:253
    old "Android"
    new "Android"

    # front_page.rpy:254
    old "iOS"
    new "iOS"

    # front_page.rpy:255
    old "Generate Translations"
    new "Создать переводы"

    # front_page.rpy:256
    old "Extract Dialogue"
    new "Извлечь диалог"

    # front_page.rpy:273
    old "Checking script for potential problems..."
    new "Проверка потенциальных проблем сценария..."

    # front_page.rpy:288
    old "Deleting persistent data..."
    new "Удаление постоянных данных..."

    # front_page.rpy:296
    old "Recompiling all rpy files into rpyc files..."
    new "Перекомпиляция всех файлов rpy в файлы rpyc..."

    # gui7.rpy:252
    old "Select Accent and Background Colors"
    new "Выберите Акцентный и Фоновый Цвета"

    # gui7.rpy:266
    old "Please click on the color scheme you wish to use, then click Continue. These colors can be changed and customized later."
    new "Пожалуйста, кликните на цветовую схему, которую вы хотите использовать, а затем кликните Продолжить. Эти цвета можно изменить позже."

    # gui7.rpy:310
    old "{b}Warning{/b}\nContinuing will overwrite customized bar, button, save slot, scrollbar, and slider images.\n\nWhat would you like to do?"
    new "{b}Внимание{/b}\nПродолжив, вы перепишете настроенные полосы, кнопки, слоты сохранения, полосы прокрутки и ползунки.\n\nЧто вы хотите сделать?"

    # gui7.rpy:310
    old "Choose new colors, then regenerate image files."
    new "Выбрать новые цвета, затем воссоздать файлы изображений."

    # gui7.rpy:310
    old "Regenerate the image files using the colors in gui.rpy."
    new "Воссоздать файлы изображений используя цвета из gui.rpy."

    # gui7.rpy:330
    old "PROJECT NAME"
    new "ИМЯ ПРОЕКТА"

    # gui7.rpy:330
    old "Please enter the name of your project:"
    new "Пожалуйста, введите имя проекта:"

    # gui7.rpy:338
    old "The project name may not be empty."
    new "Имя проекта не должно быть пустым."

    # gui7.rpy:343
    old "[project_name!q] already exists. Please choose a different project name."
    new "[project_name!q] уже существует. Выберите другое имя проекта."

    # gui7.rpy:346
    old "[project_dir!q] already exists. Please choose a different project name."
    new "[project_dir!q] уже существует. Выберите другое имя проекта."

    # gui7.rpy:357
    old "What resolution should the project use? Although Ren'Py can scale the window up and down, this is the initial size of the window, the size at which assets should be drawn, and the size at which the assets will be at their sharpest.\n\nThe default of 1280x720 is a reasonable compromise."
    new "Какое разрешение будет использовать ваш проект? Хотя Ren'Py может масштабировать окно, это будет целевой размер окна, по отношению к которому будут вырисовываться ресурсы, и на котором они будут наиболее чёткие.\n\nСтандартный 1280x720 — резонный компромисс."

    # gui7.rpy:357
    old "Custom. The GUI is optimized for a 16:9 aspect ratio."
    new "Своё. GUI оптимизирован под соотношение сторон 16:9."

    # gui7.rpy:372
    old "WIDTH"
    new "ШИРИНА"

    # gui7.rpy:372
    old "Please enter the width of your game, in pixels."
    new "Пожалуйста, введите ширину вашей игры в пикселях."

    # gui7.rpy:377
    old "The width must be a number."
    new "Ширина должна быть цифрой."

    # gui7.rpy:379
    old "HEIGHT"
    new "ВЫСОТА"

    # gui7.rpy:379
    old "Please enter the height of your game, in pixels."
    new "Пожалуйста, введите высоту вашей игры в пикселях."

    # gui7.rpy:384
    old "The height must be a number."
    new "Высота должна быть цифрой."

    # gui7.rpy:426
    old "Creating the new project..."
    new "Создаю новый проект..."

    # gui7.rpy:428
    old "Updating the project..."
    new "Обновляю проект..."

    # interface.rpy:119
    old "Documentation"
    new "Документация"

    # interface.rpy:120
    old "Ren'Py Website"
    new "Сайт Ren'Py"

    # interface.rpy:121
    old "Ren'Py Games List"
    new "Список игр Ren'Py"

    # interface.rpy:129
    old "update"
    new "обновить"

    # interface.rpy:131
    old "preferences"
    new "настройки"

    # interface.rpy:132
    old "quit"
    new "выйти"

    # interface.rpy:136
    old "Ren'Py Sponsor Information"
    new "Спонсоры Ren'Py"

    # interface.rpy:258
    old "Due to package format limitations, non-ASCII file and directory names are not allowed."
    new "В связи с ограничениями на форматы пакетов, не-ASCII имена файлов и папок недопустимы."

    # interface.rpy:354
    old "ERROR"
    new "ОШИБКА"

    # interface.rpy:400
    old "Text input may not contain the {{ or [[ characters."
    new "Текст не должен содержать знаки {{ или [[."

    # interface.rpy:405
    old "File and directory names may not contain / or \\."
    new "Имена файлов и папок не должны содержать / или \\."

    # interface.rpy:411
    old "File and directory names must consist of ASCII characters."
    new "Имена файлов и папок должны состоять из знаков ASCII."

    # interface.rpy:479
    old "PROCESSING"
    new "ОБРАБОТКА"

    # interface.rpy:496
    old "QUESTION"
    new "ВОПРОС"

    # interface.rpy:509
    old "CHOICE"
    new "ВЫБОР"

    # ios.rpy:28
    old "To build iOS packages, please download renios, unzip it, and place it into the Ren'Py directory. Then restart the Ren'Py launcher."
    new "Чтобы построить iOS-пакеты, пожалуйста, загрузите renios, разархивируйте его и положите в директорию Ren'Py. Затем перезагрузите лаунчер Ren'Py."

    # ios.rpy:29
    old "The directory in where Xcode projects will be placed has not been selected. Choose 'Select Directory' to select it."
    new "Директория, куда должны складываться проекты Xcode не выбрана. Выберите 'Указать Директорию', чтобы её выбрать."

    # ios.rpy:30
    old "There is no Xcode project corresponding to the current Ren'Py project. Choose 'Create Xcode Project' to create one."
    new "Нет проекта Xcode, соответствующего текущему проекту Ren'Py. Выберите 'Создать Проект Xcode', чтобы создать его."

    # ios.rpy:31
    old "An Xcode project exists. Choose 'Update Xcode Project' to update it with the latest game files, or use Xcode to build and install it."
    new "Проект Xcode уже существует. Выберите 'Обновить Проект Xcode', чтобы обновить его последними файлами игры или используйте Xcode, чтобы построить и установить её."

    # ios.rpy:33
    old "Attempts to emulate an iPhone.\n\nTouch input is emulated through the mouse, but only when the button is held down."
    new "Пытается эмулировать iPhone.\n\nПрикосновения эмулируются мышью, но только когда кнопка зажата."

    # ios.rpy:34
    old "Attempts to emulate an iPad.\n\nTouch input is emulated through the mouse, but only when the button is held down."
    new "Пытается эмулировать iPad.\n\nПрикосновения эмулируются мышью, но только когда кнопка зажата."

    # ios.rpy:36
    old "Selects the directory where Xcode projects will be placed."
    new "Выбрать директорию, куда будут складываться проекты Xcode."

    # ios.rpy:37
    old "Creates an Xcode project corresponding to the current Ren'Py project."
    new "Создаёт проект Xcode, соответствующий текущему проекту Ren'Py."

    # ios.rpy:38
    old "Updates the Xcode project with the latest game files. This must be done each time the Ren'Py project changes."
    new "Обновляет проект Xcode последними файлами игры. Это должно выполняться каждый раз, когда проект Ren'Py изменяется."

    # ios.rpy:39
    old "Opens the Xcode project in Xcode."
    new "Открывает проект Xcode в Xcode."

    # ios.rpy:41
    old "Opens the directory containing Xcode projects."
    new "Открывает директорию, содержащую проекты Xcode."

    # ios.rpy:126
    old "The Xcode project already exists. Would you like to rename the old project, and replace it with a new one?"
    new "Проект Xcode уже существует. Хотите переименовать старый проект или заменить его новым?"

    # ios.rpy:211
    old "iOS: [project.current.display_name!q]"
    new "iOS: [project.current.display_name!q]"

    # ios.rpy:240
    old "iPhone"
    new "iPhone"

    # ios.rpy:244
    old "iPad"
    new "iPad"

    # ios.rpy:264
    old "Select Xcode Projects Directory"
    new "Выбрать Директорию Проектов Xcode"

    # ios.rpy:268
    old "Create Xcode Project"
    new "Создать Проект Xcode"

    # ios.rpy:272
    old "Update Xcode Project"
    new "Обновить Проект Xcode"

    # ios.rpy:277
    old "Launch Xcode"
    new "Запустить Xcode"

    # ios.rpy:312
    old "Open Xcode Projects Directory"
    new "Open Xcode Projects Directory"

    # ios.rpy:345
    old "Before packaging iOS apps, you'll need to download renios, Ren'Py's iOS support. Would you like to download renios now?"
    new "Перед упаковкой приложений iOS, вам требуется загрузить renios, поддержка iOS для Ren'Py. Хотите загрузить renios прямо сейчас?"

    # ios.rpy:354
    old "XCODE PROJECTS DIRECTORY"
    new "ДИРЕКТОРИЯ ПРОЕКТОВ XCODE"

    # ios.rpy:354
    old "Please choose the Xcode Projects Directory using the directory chooser.\n{b}The directory chooser may have opened behind this window.{/b}"
    new "Пожалуйста, выберите Директорию Проектов Xcode, используя выборщик папок.\n{b}Выборщик папок может быть открыт за этим окном.{/b}"

    # ios.rpy:359
    old "Ren'Py has set the Xcode Projects Directory to:"
    new "Ren'Py установила Директорию Проектов Xcode в:"

    # itch.rpy:60
    old "The built distributions could not be found. Please choose 'Build' and try again."
    new "Собранный дистрибутив не найден. Пожалуйста, выберите 'Построить' и попытайтесь снова."

    # itch.rpy:98
    old "No uploadable files were found. Please choose 'Build' and try again."
    new "Загружаемые файлы не были найдены. Пожалуйста, выберите 'Построить' и попытайтесь снова."

    # itch.rpy:106
    old "The butler program was not found."
    new "Программа butler не найдена."

    # itch.rpy:106
    old "Please install the itch.io app, which includes butler, and try again."
    new "Пожалуйста, установите приложение itch.io, которое содержит butler, и попытайтесь снова."

    # itch.rpy:115
    old "The name of the itch project has not been set."
    new "Имя itch.io проекта не установлено."

    # itch.rpy:115
    old "Please {a=https://itch.io/game/new}create your project{/a}, then add a line like \n{vspace=5}define build.itch_project = \"user-name/game-name\"\n{vspace=5} to options.rpy."
    new "Пожалуйста, {a=https://itch.io/game/new}создайте ваш проект{/a}, затем добавьте строку типа\n{vspace=5}define build.itch_project = \"user-name/game-name\"\n{vspace=5} в options.rpy."

    # mobilebuild.rpy:109
    old "{a=%s}%s{/a}"
    new "{a=%s}%s{/a}"

    # navigation.rpy:168
    old "Navigate: [project.current.display_name!q]"
    new "Навигация: [project.current.display_name!q]"

    # navigation.rpy:177
    old "Order: "
    new "Порядок: "

    # navigation.rpy:178
    old "alphabetical"
    new "алфавитный"

    # navigation.rpy:180
    old "by-file"
    new "по-файлу"

    # navigation.rpy:182
    old "natural"
    new "натуральный"

    # navigation.rpy:194
    old "Category:"
    new "Категория:"

    # navigation.rpy:196
    old "files"
    new "файлы"

    # navigation.rpy:197
    old "labels"
    new "метки"

    # navigation.rpy:198
    old "defines"
    new "определения"

    # navigation.rpy:199
    old "transforms"
    new "трансформации"

    # navigation.rpy:200
    old "screens"
    new "экраны"

    # navigation.rpy:201
    old "callables"
    new "вызываемые"

    # navigation.rpy:202
    old "TODOs"
    new "TODO"

    # navigation.rpy:241
    old "+ Add script file"
    new "+ Добавить файл сценария"

    # navigation.rpy:249
    old "No TODO comments found.\n\nTo create one, include \"# TODO\" in your script."
    new "Не найдено комментариев TODO.\n\nЧтобы создать такой, включите \"#TODO\" в ваш сценарий"

    # navigation.rpy:256
    old "The list of names is empty."
    new "Список имён пуст."

    # new_project.rpy:38
    old "New GUI Interface"
    new "Новый Интерфейс GUI"

    # new_project.rpy:48
    old "Both interfaces have been translated to your language."
    new "Все интерфейсы переведены на ваш язык."

    # new_project.rpy:50
    old "Only the new GUI has been translated to your language."
    new "Только новый GUI переведён на ваш язык."

    # new_project.rpy:52
    old "Only the legacy theme interface has been translated to your language."
    new "Только старые темы интерфейса переведены на ваш язык."

    # new_project.rpy:54
    old "Neither interface has been translated to your language."
    new "Ни один из интерфейсов не переведён на ваш язык."

    # new_project.rpy:63
    old "The projects directory could not be set. Giving up."
    new "Директория проектов не может быть установлена. Сдаюсь."

    # new_project.rpy:71
    old "You will be creating an [new_project_language] language project. Change the launcher language in preferences to create a project in another language."
    new "Вы создаёте проект на языке [new_project_language]. Чтобы создать проект на другом языке, измените язык лаунчера."

    # new_project.rpy:79
    old "Which interface would you like to use? The new GUI has a modern look, supports wide screens and mobile devices, and is easier to customize. Legacy themes might be necessary to work with older example code.\n\n[language_support!t]\n\nIf in doubt, choose the new GUI, then click Continue on the bottom-right."
    new "Какой интерфейс вы хотите использовать? У нового GUI современный вид, поддержка широких экранов и мобильных устройств, и его легче изменять. Старые темы могут быть необходимы для работы со старым кодом.\n\n[language_support!t]\n\nЕсли сомневаетесь, выберите новый GUI, затем кликните на кнопку Продолжить."

    # new_project.rpy:79
    old "Legacy Theme Interface"
    new "Старые Темы Интерфейса"

    # new_project.rpy:100
    old "Choose Project Template"
    new "Выберите Образец Проекта"

    # new_project.rpy:118
    old "Please select a template to use for your new project. The template sets the default font and the user interface language. If your language is not supported, choose 'english'."
    new "Пожалуйста, выберите образец, на котором основывать ваш проект. Образец задаёт шрифт и язык по умолчанию для интерфейса. Если ваш язык не поддерживается, выберите 'english'."

    # preferences.rpy:72
    old "Launcher Preferences"
    new "Настройки лаунчера"

    # preferences.rpy:93
    old "Projects Directory:"
    new "Папка проектов:"

    # preferences.rpy:100
    old "[persistent.projects_directory!q]"
    new "[persistent.projects_directory!q]"

    # preferences.rpy:102
    old "Projects directory: [text]"
    new "Папка проектов: [text]"

    # preferences.rpy:104
    old "Not Set"
    new "Не задано"

    # preferences.rpy:119
    old "Text Editor:"
    new "Текстовый редактор:"

    # preferences.rpy:125
    old "Text editor: [text]"
    new "Текстовый редактор: [text]"

    # preferences.rpy:141
    old "Update Channel:"
    new "Канал обновлений:"

    # preferences.rpy:161
    old "Navigation Options:"
    new "Опции навигации:"

    # preferences.rpy:165
    old "Include private names"
    new "Включать приватные имена"

    # preferences.rpy:166
    old "Include library names"
    new "Включать имена библиотек"

    # preferences.rpy:176
    old "Launcher Options:"
    new "Опции лаунчера:"

    # preferences.rpy:180
    old "Hardware rendering"
    new "Аппаратный рендеринг"

    # preferences.rpy:181
    old "Show edit file section"
    new "Показать секцию редактирования"

    # preferences.rpy:182
    old "Large fonts"
    new "Большие шрифты"

    # preferences.rpy:185
    old "Console output"
    new "Вывод на консоль"

    # preferences.rpy:187
    old "Force new tutorial"
    new "Новое обучение"

    # preferences.rpy:189
    old "Legacy options"
    new "Включить старые темы"

    # preferences.rpy:192
    old "Show templates"
    new "Показывать образцы"

    # preferences.rpy:194
    old "Sponsor message"
    new "Сообщение спонсорам"

    # preferences.rpy:214
    old "Open launcher project"
    new "Открыть проект лаунчера"

    # preferences.rpy:228
    old "Language:"
    new "Язык:"

    # project.rpy:49
    old "After making changes to the script, press shift+R to reload your game."
    new "После применения изменений в скрипте, нажмите shift+R, чтобы перезагрузить вашу игру."

    # project.rpy:49
    old "Press shift+O (the letter) to access the console."
    new "Нажмите shift+O (букву), чтобы войти в консоль."

    # project.rpy:49
    old "Press shift+D to access the developer menu."
    new "Нажмите shift+D, чтобы получить доступ к меню разработчика."

    # project.rpy:49
    old "Have you backed up your projects recently?"
    new "Давно сохраняли свои проекты?"

    # project.rpy:276
    old "Launching the project failed."
    new "Запуск проекта провален."

    # project.rpy:276
    old "Please ensure that your project launches normally before running this command."
    new "Пожалуйста, убедитесь, что ваш проект нормально запускается перед использованием этой команды."

    # project.rpy:292
    old "Ren'Py is scanning the project..."
    new "Ren'Py сканирует проект..."

    # project.rpy:721
    old "Launching"
    new "Запускаю"

    # project.rpy:755
    old "PROJECTS DIRECTORY"
    new "ДИРЕКТОРИЯ ПРОЕКТОВ"

    # project.rpy:755
    old "Please choose the projects directory using the directory chooser.\n{b}The directory chooser may have opened behind this window.{/b}"
    new "Пожалуйста, выберите директорию проектов, используя выборщик директорий.\n{b}Он мог появиться позади этого окна.{/b}"

    # project.rpy:755
    old "This launcher will scan for projects in this directory, will create new projects in this directory, and will place built projects into this directory."
    new "Лаунчер будет искать проекты в этой директории, создавать новые проекты в этой директории, и размещать построенные проекты в этой директории."

    # project.rpy:760
    old "Ren'Py has set the projects directory to:"
    new "Ren'Py установила директорию проектов на:"

    # translations.rpy:92
    old "Translations: [project.current.display_name!q]"
    new "Переводы: [project.current.display_name!q]"

    # translations.rpy:133
    old "The language to work with. This should only contain lower-case ASCII characters and underscores."
    new "Язык работы. Он должен содержать только не-заглавные символы ASCII и подчёркивания."

    # translations.rpy:159
    old "Generate empty strings for translations"
    new "Генерировать пустые строки для переводов"

    # translations.rpy:177
    old "Generates or updates translation files. The files will be placed in game/tl/[persistent.translate_language!q]."
    new "Генерирует или обновляет файлы переводов. Файлы будут помещены в game/tl/[persistent.translate_language!q]."

    # translations.rpy:197
    old "Extract String Translations"
    new "Извлечь Строки Для Перевода"

    # translations.rpy:199
    old "Merge String Translations"
    new "Объединить Строки Перевода"

    # translations.rpy:204
    old "Replace existing translations"
    new "Заменить существующие переводы"

    # translations.rpy:205
    old "Reverse languages"
    new "Обратить языки"

    # translations.rpy:209
    old "Update Default Interface Translations"
    new "Обновить Базовый Перевод Интерфейса"

    # translations.rpy:229
    old "The extract command allows you to extract string translations from an existing project into a temporary file.\n\nThe merge command merges extracted translations into another project."
    new "Команда извлечения позволяет вам извлечь переводимые строки из существующего проекта во временный файл.\n\nКоманда объединения объединяет извлечённые переводы в другой перевод."

    # translations.rpy:253
    old "Ren'Py is generating translations...."
    new "Ren'Py создаёт переводы..."

    # translations.rpy:264
    old "Ren'Py has finished generating [language] translations."
    new "Ren'Py закончила создавать перевод для [language]."

    # translations.rpy:277
    old "Ren'Py is extracting string translations..."
    new "Ren'Py извлекает переводимые строки..."

    # translations.rpy:280
    old "Ren'Py has finished extracting [language] string translations."
    new "Ren'Py завершила извлечение [language] строк перевода."

    # translations.rpy:300
    old "Ren'Py is merging string translations..."
    new "Ren'Py объединяет строки перевода..."

    # translations.rpy:303
    old "Ren'Py has finished merging [language] string translations."
    new "Ren'Py завершила объединение [language] строк перевода."

    # translations.rpy:314
    old "Updating default interface translations..."
    new "Обновляю базовый перевод интерфейса..."

    # translations.rpy:343
    old "Extract Dialogue: [project.current.display_name!q]"
    new "Извлечь диалог: [project.current.display_name!q]"

    # translations.rpy:359
    old "Format:"
    new "Формат:"

    # translations.rpy:367
    old "Tab-delimited Spreadsheet (dialogue.tab)"
    new "Табулированная таблица (dialogue.tab)"

    # translations.rpy:368
    old "Dialogue Text Only (dialogue.txt)"
    new "Только текст диалога (dialogue.txt)"

    # translations.rpy:381
    old "Strip text tags from the dialogue."
    new "Убрать текстовые теги из диалога."

    # translations.rpy:382
    old "Escape quotes and other special characters."
    new "Включать кавычки и регулярные выражения."

    # translations.rpy:383
    old "Extract all translatable strings, not just dialogue."
    new "Извлечь все переводимые строки, не только диалог."

    # translations.rpy:411
    old "Ren'Py is extracting dialogue...."
    new "Ren'Py извлекает диалог..."

    # translations.rpy:415
    old "Ren'Py has finished extracting dialogue. The extracted dialogue can be found in dialogue.[persistent.dialogue_format] in the base directory."
    new "Ren'Py завершила извлечение диалога. Извлечённый диалог можно найти в файле dialogue.[persistent.dialogue_format] в директории base."

    # updater.rpy:75
    old "Select Update Channel"
    new "Выберите канал обновлений"

    # updater.rpy:86
    old "The update channel controls the version of Ren'Py the updater will download. Please select an update channel:"
    new "Канал обновлений выбирает, какую версию Ren'Py скачает программа для обновления. Выберите канал:"

    # updater.rpy:91
    old "Release"
    new "Релиз"

    # updater.rpy:97
    old "{b}Recommended.{/b} The version of Ren'Py that should be used in all newly-released games."
    new "{b}Рекомендуется.{/b} Эта версия Ren'Py должна использоваться для всех новых игр."

    # updater.rpy:102
    old "Prerelease"
    new "Пререлиз"

    # updater.rpy:108
    old "A preview of the next version of Ren'Py that can be used for testing and taking advantage of new features, but not for final releases of games."
    new "Публичный анонс следующей версии Ren'Py, который можно использовать для тестирования, в том числе новых возможностей Ren'Py, но не для финальных релизов игр."

    # updater.rpy:114
    old "Experimental"
    new "Экспериментальный"

    # updater.rpy:120
    old "Experimental versions of Ren'Py. You shouldn't select this channel unless asked by a Ren'Py developer."
    new "Экспериментальные версии Ren'Py. Не выбирайте этот канал, если вас не просил об этом разработчик Ren'Py."

    # updater.rpy:126
    old "Nightly"
    new "Ночной"

    # updater.rpy:132
    old "The bleeding edge of Ren'Py development. This may have the latest features, or might not run at all."
    new "Развитие Ren'Py на краю горизонта событий. Здесь можно найти новейшие возможности Ren'Py или всё может просто не запуститься."

    # updater.rpy:152
    old "An error has occured:"
    new "Возникла ошибка:"

    # updater.rpy:154
    old "Checking for updates."
    new "Проверка обновлений."

    # updater.rpy:156
    old "Ren'Py is up to date."
    new "Ren'Py обновлена."

    # updater.rpy:158
    old "[u.version] is now available. Do you want to install it?"
    new "[u.version] доступна. Вы хотите её установить?"

    # updater.rpy:160
    old "Preparing to download the update."
    new "Подготовка к обновлению."

    # updater.rpy:162
    old "Downloading the update."
    new "Загрузка обновления."

    # updater.rpy:164
    old "Unpacking the update."
    new "Распаковка обновления."

    # updater.rpy:166
    old "Finishing up."
    new "Завершаю..."

    # updater.rpy:168
    old "The update has been installed. Ren'Py will restart."
    new "Обновление было установлено. Ren'Py будет перезапущена."

    # updater.rpy:170
    old "The update has been installed."
    new "Обновление было установлено."

    # updater.rpy:172
    old "The update was cancelled."
    new "Обновление было отменено."

    # updater.rpy:189
    old "Ren'Py Update"
    new "Обновление Ren'Py"

    # updater.rpy:195
    old "Proceed"
    new "Продолжить"

