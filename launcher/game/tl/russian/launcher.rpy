translate russian strings:
    # game/new_project.rpy:77
    old "{#language name and font}"
    new "{font=fonts/Roboto-Light.ttf}Русский{/font}"

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

    # add_file.rpy:37
    old "The file name may not be empty."
    new "Имя файла не может быть пустым."

    # add_file.rpy:39
    old "The file already exists."
    new "Файл уже существует."

    # add_file.rpy:42
    old "# Ren'Py automatically loads all script files ending with .rpy. To use this\n# file, define a label and jump to it from another file.\n"
    new "# Ren'Py автоматически загружает все файлы сценариев, заканчивающиеся на .rpy\n#Чтобы использовать этот файл, определите метку и перейдите (jump) к ней из другого файла.\n"

    # android.rpy:30
    old "To build Android packages, please download RAPT, unzip it, and place it into the Ren'Py directory. Then restart the Ren'Py launcher."
    new "Чтобы построить Android-пакет, пожалуйста, загрузите RAPT, разархивируйте его, и поместите в директорию Ren'Py. Затем перезагрузите лаунчер Ren'Py."

    # android.rpy:31
    old "A 64-bit/x64 Java [JDK_REQUIREMENT] Development Kit is required to build Android packages on Windows. The JDK is different from the JRE, so it's possible you have Java without having the JDK.\n\nPlease {a=https://www.renpy.org/jdk/[JDK_REQUIREMENT]}download and install the JDK{/a}, then restart the Ren'Py launcher."
    new "Чтобы построить Android-пакеты на Windows требуется 64-битный инструментарий разработки Java 8. JDK отличен от JRE, и возможно, у вас есть Java без JDK.\n\nПожалуйста, {a=https://www.renpy.org/jdk/[JDK_REQUIREMENT]}загрузите и установите JDK{/a}, и перезапустите лаунчер Ren'Py."

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
    old "Retrieves the log from the Android device and writes it to a file."
    new "Берёт лог с Андроид-устройства и пишет его в файл."

    # android.rpy:50
    old "Selects the Debug build, which can be accessed through Android Studio. Changing between debug and release builds requires an uninstall from your device."
    new "Выбор сборки Отладки, доступной для Android Studio. Смена режимов между отладкой и релизом требует предварительного удаления приложения с вашего устройства."

    # android.rpy:51
    old "Selects the Release build, which can be uploaded to stores. Changing between debug and release builds requires an uninstall from your device."
    new "Выбор сборки Релиза, которую можно загружать в магазины приложений. Смена режимов между отладкой и релизом требует предварительного удаления приложения с вашего устройства."

    # android.rpy:245
    old "Copying Android files to distributions directory."
    new "Копирую файлы Android в директорию дистрибутивов."

    # android.rpy:313
    old "Android: [project.current.display_name!q]"
    new "Android: [project.current.display_name!q]"

    # android.rpy:333
    old "Emulation:"
    new "Эмуляция:"

    # android.rpy:342
    old "Phone"
    new "Телефон"

    # android.rpy:346
    old "Tablet"
    new "Планшет"

    # android.rpy:350
    old "Television"
    new "Телевизор"

    # android.rpy:362
    old "Build:"
    new "Собрать:"

    # android.rpy:373
    old "Debug"
    new "Отладку"

    # android.rpy:377
    old "Release"
    new "Релиз"

    # android.rpy:384
    old "Install SDK & Create Keys"
    new "Установить SDK и создать ключи"

    # android.rpy:388
    old "Configure"
    new "Настроить"

    # android.rpy:392
    old "Build Package"
    new "Собрать Пакет"

    # android.rpy:396
    old "Build & Install"
    new "Собрать и Установить"

    # android.rpy:400
    old "Build, Install & Launch"
    new "Собрать, Установить и Запустить"

    # android.rpy:411
    old "Other:"
    new "Другое:"

    # android.rpy:419
    old "Logcat"
    new "Logcat"

    # android.rpy:452
    old "Before packaging Android apps, you'll need to download RAPT, the Ren'Py Android Packaging Tool. Would you like to download RAPT now?"
    new "Перед упаковкой приложений Android вам нужно загрузить RAPT, инструмент упаковки Ren'Py Android. Желаете загрузить RAPT сейчас?"

    # android.rpy:505
    old "Retrieving logcat information from device."
    new "Извлекаю информацию logcat с устройства."

    # androidstrings.rpy:7
    old "{} is not a directory."
    new "{} - не папка."

    # androidstrings.rpy:8
    old "{} does not contain a Ren'Py game."
    new "{} не содержит игру Ren'Py."

    # androidstrings.rpy:9
    old "Run configure before attempting to build the app."
    new "Запуск настройки перед попыткой постройки приложения."

    # androidstrings.rpy:10
    old "Google Play support is enabled, but build.google_play_key is not defined."
    new "Поддержка Google Play включена, однако переменная build.google_play_key не определена."

    # androidstrings.rpy:11
    old "Updating project."
    new "Обновляю проект"

    # androidstrings.rpy:12
    old "Creating assets directory."
    new "Создаю директорию ресурсов"

    # androidstrings.rpy:13
    old "Creating expansion file."
    new "Создаю файл-расширение"

    # androidstrings.rpy:14
    old "Packaging internal data."
    new "Пакую внутренние данные"

    # androidstrings.rpy:15
    old "I'm using Gradle to build the package."
    new "Использую Gradle для сборки пакета"

    # androidstrings.rpy:16
    old "Uploading expansion file."
    new "Загружаю файл-расширение"

    # androidstrings.rpy:17
    old "The build seems to have failed."
    new "Похоже, сборка провалилась."

    # androidstrings.rpy:18
    old "Launching app."
    new "Запускаю приложение"

    # androidstrings.rpy:19
    old "The build seems to have succeeded."
    new "Кажется, сборка прошла успешно!"

    # androidstrings.rpy:20
    old "The armeabi-v7a version works on most phones or tablets, while the x86_64 version works on the simulator and chromebooks."
    new "Версия armeabi-v7a работает на большинстве смартфонов и планшетов, а версия x86_64 требуется для симуляторов и хромбуков."

    # androidstrings.rpy:20
    old "What is the full name of your application? This name will appear in the list of installed applications."
    new "Каким будет полное имя вашего приложения? Это имя будет представлено в списке установленных приложений."

    # androidstrings.rpy:21
    old "What is the short name of your application? This name will be used in the launcher, and for application shortcuts."
    new "Каким будет короткое имя вашего приложения? Это имя будет использоваться в лаунчере, а также ярлыках приложения."

    # androidstrings.rpy:22
    old "What is the name of the package?\n\nThis is usually of the form com.domain.program or com.domain.email.program. It may only contain ASCII letters and dots. It must contain at least one dot."
    new "Каким будет имя собранного пакета?\n\nОбычно оно имеет форму com.domain.program или com.domain.email.program. Имя может содержать только символы ASCII и точки. Также оно должно содержать хотя бы одну точку."

    # androidstrings.rpy:23
    old "The package name may not be empty."
    new "Имя пакета не может быть пустым."

    # androidstrings.rpy:24
    old "The package name may not contain spaces."
    new "В имени пакета не должно быть пробелов."

    # androidstrings.rpy:25
    old "The package name must contain at least one dot."
    new "Имя пакета должно содержать как минимум одну точку."

    # androidstrings.rpy:26
    old "The package name may not contain two dots in a row, or begin or end with a dot."
    new "Имя пакета не должно содержать две и более точек подряд, или начинаться и заканчиваться с точки."

    # androidstrings.rpy:27
    old "Each part of the package name must start with a letter, and contain only letters, numbers, and underscores."
    new "Каждая часть имя пакета должна начинаться с буквы и содержать только английские буквы, цифры и подчёркивания."

    # androidstrings.rpy:28
    old "{} is a Java keyword, and can't be used as part of a package name."
    new "{} - оператор Java, его нельзя использовать в имени пакета."

    # androidstrings.rpy:29
    old "What is the application's version?\n\nThis should be the human-readable version that you would present to a person. It must contain only numbers and dots."
    new "Какой будет версия приложения?\n\nВерсия приложения представлена для человека и независима от config.version. Она может содержать только цифры и точки."

    # androidstrings.rpy:30
    old "The version number must contain only numbers and dots."
    new "Номер версии должен содержать только цифры и точки."

    # androidstrings.rpy:31
    old "What is the version code?\n\nThis must be a positive integer number, and the value should increase between versions."
    new "Каким будет код версии?\n\nЭто должно быть положительное целое число, и его значение должно увеличиваться с каждой версией."

    # androidstrings.rpy:32
    old "The numeric version must contain only numbers."
    new "Целое версии должно содержать только цифры."

    # androidstrings.rpy:33
    old "How would you like your application to be displayed?"
    new "В какой ориентации экрана вы хотите отображать ваше приложение?"

    # androidstrings.rpy:34
    old "In landscape orientation."
    new "В альбомном виде."

    # androidstrings.rpy:35
    old "In portrait orientation."
    new "В портретном виде."

    # androidstrings.rpy:36
    old "In the user's preferred orientation."
    new "По желанию пользователя."

    # androidstrings.rpy:37
    old "Which app store would you like to support in-app purchasing through?"
    new "Через какой магазин приложений вы желаете поддерживать микротранзакции внутри приложения?"

    # androidstrings.rpy:38
    old "Google Play."
    new "Google Play."

    # androidstrings.rpy:39
    old "Amazon App Store."
    new "Магазин приложений Amazon."

    # androidstrings.rpy:40
    old "Both, in one app."
    new "Оба, в одном приложении."

    # androidstrings.rpy:41
    old "Neither."
    new "Отключить."

    # androidstrings.rpy:42
    old "Would you like to create an expansion APK?"
    new "Желаете создать пакет в формате APK+кэш?"

    # androidstrings.rpy:43
    old "No. Size limit of 100 MB on Google Play, but can be distributed through other stores and sideloaded."
    new "Нет. Ограничение по размеру в Google Play - 100 МБ, но может распространяться через другие магазины или локально."

    # androidstrings.rpy:44
    old "Yes. 2 GB size limit, but won't work outside of Google Play. (Read the documentation to get this to work.)"
    new "Да. Ограничение в 2 ГБ, но не будет работать вне среды Google Play. (Ознакомьтесь с {a=https://renpy.org/doc/html/android.html?highlight=apk#google-play-expansion-apks}документацией{/a})"

    # androidstrings.rpy:45
    old "Do you want to allow the app to access the Internet?"
    new "Желаете разрешить вашему приложению доступ в Интернет?"

    # androidstrings.rpy:46
    old "Do you want to automatically update the generated project?"
    new "Желаете автоматически обновлять сгенерированный проект?"

    # androidstrings.rpy:47
    old "Yes. This is the best choice for most projects."
    new "Да. Это лучшее решение для большинства проектов."

    # androidstrings.rpy:48
    old "No. This may require manual updates when Ren'Py or the project configuration changes."
    new "Нет. Это решение может потребовать ручных обновлений при изменении Ren'Py или конфигурации проекта."

    # androidstrings.rpy:49
    old "Unknown configuration variable: {}"
    new "Неизвестная конфигурационная переменная: {}"

    # androidstrings.rpy:50
    old "I'm compiling a short test program, to see if you have a working JDK on your system."
    new "Сейчас я компилирую небольшую тестовую программу, чтобы убедиться, что в вашей системе есть работающий JDK."

    # androidstrings.rpy:51
    old "I was unable to use javac to compile a test file. If you haven't installed the Java Development Kit yet, please download it from:\n\nhttp://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html\n\nThe JDK is different from the JRE, so it's possible you have Java without having the JDK. Without a working JDK, I can't continue."
    new "Я не смогла воспользоваться javac для компиляции тестового файла. Если у вас не установлен Инструментарий Разработки Java, пожалуйста, загрузите его с:\n\nhttp://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html\n\nJDK отличается от JRE, так что есть вероятность, что у вас установлена Java без JDK. Без функционирующего JDK я не могу продолжить."

    # androidstrings.rpy:52
    old "The version of Java on your computer does not appear to be JDK 8, which is the only version supported by the Android SDK. If you need to install JDK 8, you can download it from:\n\nhttp://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html\n\nYou can also set the JAVA_HOME environment variable to use a different version of Java."
    new "Судя по всему, версия Java на вашем компьютере - не JDK 8, единственная версия, поддерживаемая Android SDK. Если вам нужно установить JDK 8, вы можете скачать его с:\n\nhttp://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html\n\nТакже вы можете изменить переменную окружения JAVA_HOME, чтобы воспользоваться другой версией Java."

    # androidstrings.rpy:53
    old "The JDK is present and working. Good!"
    new "JDK найден и работает. Отлично!"

    # androidstrings.rpy:54
    old "The Android SDK has already been unpacked."
    new "Android SDK уже распакован."

    # androidstrings.rpy:55
    old "Do you accept the Android SDK Terms and Conditions?"
    new "Вы принимаете условия и положения пользования Android SDK?"

    # androidstrings.rpy:56
    old "I'm downloading the Android SDK. This might take a while."
    new "Загружаю Android SDK. Это может занять некоторое время."

    # androidstrings.rpy:57
    old "I'm extracting the Android SDK."
    new "Извлекаю Android SDK."

    # androidstrings.rpy:58
    old "I've finished unpacking the Android SDK."
    new "Извлечение Android SDK завершено."

    # androidstrings.rpy:59
    old "I'm about to download and install the required Android packages. This might take a while."
    new "Начинаю загрузку и установку необходимых пакетов Android. Это может занять время."

    # androidstrings.rpy:60
    old "I was unable to accept the Android licenses."
    new "Внимание, не удалось принять соглашения Android!"

    # androidstrings.rpy:61
    old "I was unable to install the required Android packages."
    new "Установка необходимых пакетов Android не удалась!"

    # androidstrings.rpy:62
    old "I've finished installing the required Android packages."
    new "Заканчиваю установку необходимых пакетов Android."

    # androidstrings.rpy:63
    old "You set the keystore yourself, so I'll assume it's how you want it."
    new "Вы сами установили хранилище ключей, так что посмею предположить, что оно настроено так, как вы хотите."

    # androidstrings.rpy:64
    old "You've already created an Android keystore, so I won't create a new one for you."
    new "Вы уже создали хранилище ключей Android, так что я не буду создавать для вас новое."

    # androidstrings.rpy:65
    old "I can create an application signing key for you. Signing an application with this key allows it to be placed in the Android Market and other app stores.\n\nDo you want to create a key?"
    new "Я могу создать для вас ключ для подписи приложения. Подпись приложения этим ключом позволит разместить его в Android Market и других магазинах приложений.\n\nХотите создать ключ?"

    # androidstrings.rpy:66
    old "I will create the key in the android.keystore file.\n\nYou need to back this file up. If you lose it, you will not be able to upgrade your application.\n\nYou also need to keep the key safe. If evil people get this file, they could make fake versions of your application, and potentially steal your users' data.\n\nWill you make a backup of android.keystore, and keep it in a safe place?"
    new "Я создам ключ в файле android.keystore.\n\nВам нужно сохранить этот файл. Если вы его потеряете, то не сможете обновлять ваше приложение.\n\nТакже вам нужно держать ваш ключ в безопасность. Если злоумышленникам удастся получить его, они потенциально могут создать вредоносную версию приложения и красть данные ваших пользователей.\n\nБудете ли вы хранить android.keystore и держать его в надёжном месте?"

    # androidstrings.rpy:67
    old "Please enter your name or the name of your organization."
    new "Пожалуйста, введите ваше имя или имя вашей организации."

    # androidstrings.rpy:68
    old "Could not create android.keystore. Is keytool in your path?"
    new "Не могу создать android.keystore. Хранилище ключей расположено в вашем пути файлов?"

    # androidstrings.rpy:69
    old "I've finished creating android.keystore. Please back it up, and keep it in a safe place."
    new "Создание android.keystore завершено. Пожалуйста, сохраните его и держите в надёжном месте."

    # androidstrings.rpy:70
    old "It looks like you're ready to start packaging games."
    new "Похоже, вы готовы собирать игры!"

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

    # editor.rpy:152
    old "(Recommended) A modern and approachable text editor."
    new "(Рекомендуется) Современный, доступный текстовый редактор."

    # editor.rpy:164
    old "Up to 150 MB download required."
    new "Требуется скачать 150 МБ."

    # editor.rpy:178
    old "A mature editor. Editra lacks the IME support required for Chinese, Japanese, and Korean text input."
    new "Старый, проверенный бета-редактор. Editra на данный момент не поддерживает IME, необходимые для ввода Китайского, Японского и Корейского текстов."

    # editor.rpy:179
    old "A mature editor. Editra lacks the IME support required for Chinese, Japanese, and Korean text input. On Linux, Editra requires wxPython."
    new "Старый, проверенный бета-редактор. Editra на данный момент не поддерживает IME, необходимые для ввода Китайского, Японского и Корейского текстов. На Linux, Editra требует wxPython."

    # editor.rpy:195
    old "This may have occured because wxPython is not installed on this system."
    new "Это могло случиться из-за того, что wxPython не установлен на этой системе."

    # editor.rpy:197
    old "Up to 22 MB download required."
    new "Требуется скачать 22 МБ."

    # editor.rpy:210
    old "A mature editor that requires Java."
    new "Проверенный временем редактор. Требует Java."

    # editor.rpy:210
    old "1.8 MB download required."
    new "Требуется скачать 1.8 МБ."

    # editor.rpy:210
    old "This may have occured because Java is not installed on this system."
    new "Это могло случиться из-за того, что Java не установлена в данной системе."

    # editor.rpy:219
    old "System Editor"
    new "Системный"

    # editor.rpy:219
    old "Invokes the editor your operating system has associated with .rpy files."
    new "Включает текстовый редактор, ассоциированный в вашей системе с файлами .rpy."

    # editor.rpy:235
    old "None"
    new "Нет"

    # editor.rpy:235
    old "Prevents Ren'Py from opening a text editor."
    new "Не позволяет Ren'Py запускать текстовый редактор."

    # editor.rpy:338
    old "Edit [text]."
    new "Редактировать [text]"

    # editor.rpy:387
    old "An exception occured while launching the text editor:\n[exception!q]"
    new "Возникла ошибка при запуске текстового редактора:\n[exception!q]"

    # editor.rpy:519
    old "Select Editor"
    new "Выберите редактор"

    # editor.rpy:534
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

    # front_page.rpy:215
    old "Open project"
    new "Открыть проект"

    # front_page.rpy:217
    old "All script files"
    new "все файлы сценария"

    # front_page.rpy:221
    old "Actions"
    new "Действия с Проектом"

    # front_page.rpy:230
    old "Navigate Script"
    new "Навигация по cценарию"

    # front_page.rpy:231
    old "Check Script (Lint)"
    new "Проверить скрипт (Lint)"

    # front_page.rpy:234
    old "Change/Update GUI"
    new "Изменить/Обновить GUI"

    # front_page.rpy:236
    old "Change Theme"
    new "Сменить тему"

    # front_page.rpy:239
    old "Delete Persistent"
    new "Очистить постоянные"

    # front_page.rpy:248
    old "Build Distributions"
    new "Построить дистрибутивы"

    # front_page.rpy:250
    old "Android"
    new "Android"

    # front_page.rpy:251
    old "iOS"
    new "iOS"

    # front_page.rpy:252
    old "Generate Translations"
    new "Создать переводы"

    # front_page.rpy:253
    old "Extract Dialogue"
    new "Извлечь диалог"

    # front_page.rpy:270
    old "Checking script for potential problems..."
    new "Проверка потенциальных проблем сценария..."

    # front_page.rpy:285
    old "Deleting persistent data..."
    new "Удаление постоянных данных..."

    # front_page.rpy:293
    old "Recompiling all rpy files into rpyc files..."
    new "Перекомпиляция всех файлов rpy в файлы rpyc..."

    # gui7.rpy:252
    old "Select Accent and Background Colors"
    new "Выберите Акцентный и Фоновый Цвета"

    # gui7.rpy:266
    old "Please click on the color scheme you wish to use, then click Continue. These colors can be changed and customized later."
    new "Пожалуйста, кликните на цветовую схему, которую вы хотите использовать, а затем кликните Продолжить. Эти цвета можно изменить позже."

    # gui7.rpy:311
    old "{b}Warning{/b}\nContinuing will overwrite customized bar, button, save slot, scrollbar, and slider images.\n\nWhat would you like to do?"
    new "{b}Внимание{/b}\nПродолжив, вы перепишете настроенные полосы, кнопки, слоты сохранения, полосы прокрутки и ползунки.\n\nЧто вы хотите сделать?"

    # gui7.rpy:311
    old "Choose new colors, then regenerate image files."
    new "Выбрать новые цвета, затем воссоздать файлы изображений."

    # gui7.rpy:311
    old "Regenerate the image files using the colors in gui.rpy."
    new "Воссоздать файлы изображений используя цвета из gui.rpy."

    # gui7.rpy:331
    old "PROJECT NAME"
    new "ИМЯ ПРОЕКТА"

    # gui7.rpy:331
    old "Please enter the name of your project:"
    new "Пожалуйста, введите имя проекта:"

    # gui7.rpy:339
    old "The project name may not be empty."
    new "Имя проекта не должно быть пустым."

    # gui7.rpy:344
    old "[project_name!q] already exists. Please choose a different project name."
    new "[project_name!q] уже существует. Выберите другое имя проекта."

    # gui7.rpy:347
    old "[project_dir!q] already exists. Please choose a different project name."
    new "[project_dir!q] уже существует. Выберите другое имя проекта."

    # gui7.rpy:358
    old "What resolution should the project use? Although Ren'Py can scale the window up and down, this is the initial size of the window, the size at which assets should be drawn, and the size at which the assets will be at their sharpest.\n\nThe default of [default_size[0]]x[default_size[1]] is a reasonable compromise."
    new "Какое разрешение будет использовать ваш проект? Хотя Ren'Py может масштабировать окно, это будет целевой размер окна, по отношению к которому будут вырисовываться ресурсы, и на котором они будут наиболее чёткие.\n\nСтандартный [default_size[0]]x[default_size[1]] — резонный компромисс."

    # gui7.rpy:358
    old "Custom. The GUI is optimized for a 16:9 aspect ratio."
    new "Своё. GUI оптимизирован под соотношение сторон 16:9."

    # gui7.rpy:373
    old "WIDTH"
    new "ШИРИНА"

    # gui7.rpy:373
    old "Please enter the width of your game, in pixels."
    new "Пожалуйста, введите ширину вашей игры в пикселях."

    # gui7.rpy:378
    old "The width must be a number."
    new "Ширина должна быть цифрой."

    # gui7.rpy:380
    old "HEIGHT"
    new "ВЫСОТА"

    # gui7.rpy:380
    old "Please enter the height of your game, in pixels."
    new "Пожалуйста, введите высоту вашей игры в пикселях."

    # gui7.rpy:385
    old "The height must be a number."
    new "Высота должна быть цифрой."

    # gui7.rpy:427
    old "Creating the new project..."
    new "Создаю новый проект..."

    # gui7.rpy:429
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
    # Automatic translation.
    new "Открыть каталог проектов Xcode"

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

    # mobilebuild.rpy:110
    old "{a=%s}%s{/a}"
    new "{a=%s}%s{/a}"

    # navigation.rpy:168
    old "Navigate: [project.current.display_name!q]"
    new "Навигация: [project.current.display_name!q]"

    # navigation.rpy:178
    old "Order: "
    new "Порядок: "

    # navigation.rpy:179
    old "alphabetical"
    new "алфавитный"

    # navigation.rpy:181
    old "by-file"
    new "по файлу"

    # navigation.rpy:183
    old "natural"
    new "натуральный"

    # navigation.rpy:195
    old "Category:"
    new "Категория:"

    # navigation.rpy:198
    old "files"
    new "файлы"

    # navigation.rpy:199
    old "labels"
    new "метки"

    # navigation.rpy:200
    old "defines"
    new "определения"

    # navigation.rpy:201
    old "transforms"
    new "трансформации"

    # navigation.rpy:202
    old "screens"
    new "экраны"

    # navigation.rpy:203
    old "callables"
    new "вызываемые"

    # navigation.rpy:204
    old "TODOs"
    new "TODO"

    # navigation.rpy:243
    old "+ Add script file"
    new "+ Добавить файл сценария"

    # navigation.rpy:251
    old "No TODO comments found.\n\nTo create one, include \"# TODO\" in your script."
    new "Не найдено комментариев TODO.\n\nЧтобы создать такой, включите \"#TODO\" в ваш сценарий"

    # navigation.rpy:258
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
    old "You will be creating an [new_project_language]{#this substitution may be localized} language project. Change the launcher language in preferences to create a project in another language."
    new "Вы создаёте проект на русском языке. Чтобы создать проект на другом языке, измените язык лаунчера."

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

    # preferences.rpy:73
    old "Launcher Preferences"
    new "Настройки лаунчера"

    # preferences.rpy:94
    old "Projects Directory:"
    new "Папка проектов:"

    # preferences.rpy:101
    old "[persistent.projects_directory!q]"
    new "[persistent.projects_directory!q]"

    # preferences.rpy:103
    old "Projects directory: [text]"
    new "Папка проектов: [text]"

    # preferences.rpy:105
    old "Not Set"
    new "Не задано"

    # preferences.rpy:120
    old "Text Editor:"
    new "Текстовый редактор:"

    # preferences.rpy:126
    old "Text editor: [text]"
    new "Текстовый редактор: [text]"

    # preferences.rpy:145
    old "Navigation Options:"
    new "Опции навигации:"

    # preferences.rpy:149
    old "Include private names"
    new "Включать приватные имена"

    # preferences.rpy:150
    old "Include library names"
    new "Включать имена библиотек"

    # preferences.rpy:160
    old "Launcher Options:"
    new "Опции лаунчера:"

    # preferences.rpy:164
    old "Hardware rendering"
    new "Аппаратный рендеринг"

    # preferences.rpy:165
    old "Show edit file section"
    new "Показывать секцию редактирования"

    # preferences.rpy:166
    old "Large fonts"
    new "Большие шрифты"

    # preferences.rpy:169
    old "Console output"
    new "Вывод на консоль"

    # preferences.rpy:173
    old "Force new tutorial"
    new "Новое обучение"

    # preferences.rpy:177
    old "Legacy options"
    new "Включить старые темы"

    # preferences.rpy:180
    old "Show templates"
    new "Показывать образцы"

    # preferences.rpy:182
    old "Sponsor message"
    new "Сообщение спонсорам"

    # preferences.rpy:202
    old "Open launcher project"
    new "Открыть проект лаунчера"

    # preferences.rpy:216
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

    # project.rpy:281
    old "Launching the project failed."
    new "Запуск проекта провален."

    # project.rpy:281
    old "Please ensure that your project launches normally before running this command."
    new "Пожалуйста, убедитесь, что ваш проект нормально запускается перед использованием этой команды."

    # project.rpy:297
    old "Ren'Py is scanning the project..."
    new "Ren'Py сканирует проект..."

    # project.rpy:729
    old "Launching"
    new "Запускаю"

    # project.rpy:763
    old "PROJECTS DIRECTORY"
    new "ДИРЕКТОРИЯ ПРОЕКТОВ"

    # project.rpy:763
    old "Please choose the projects directory using the directory chooser.\n{b}The directory chooser may have opened behind this window.{/b}"
    new "Пожалуйста, выберите директорию проектов, используя выборщик директорий.\n{b}Он мог появиться позади этого окна.{/b}"

    # project.rpy:763
    old "This launcher will scan for projects in this directory, will create new projects in this directory, and will place built projects into this directory."
    new "Лаунчер будет искать проекты в этой директории, создавать новые проекты в этой директории, и размещать построенные проекты в этой директории."

    # project.rpy:768
    old "Ren'Py has set the projects directory to:"
    new "Ren'Py установила директорию проектов на:"

    # translations.rpy:91
    old "Translations: [project.current.display_name!q]"
    new "Переводы: [project.current.display_name!q]"

    # translations.rpy:132
    old "The language to work with. This should only contain lower-case ASCII characters and underscores."
    new "Язык работы. Он должен содержать только не-заглавные символы ASCII и подчёркивания."

    # translations.rpy:158
    old "Generate empty strings for translations"
    new "Генерировать пустые строки для переводов"

    # translations.rpy:176
    old "Generates or updates translation files. The files will be placed in game/tl/[persistent.translate_language!q]."
    new "Генерирует или обновляет файлы переводов. Файлы будут помещены в game/tl/[persistent.translate_language!q]."

    # translations.rpy:196
    old "Extract String Translations"
    new "Извлечь Строки Для Перевода"

    # translations.rpy:198
    old "Merge String Translations"
    new "Объединить Строки Перевода"

    # translations.rpy:203
    old "Replace existing translations"
    new "Заменить существующие переводы"

    # translations.rpy:204
    old "Reverse languages"
    new "Обратить языки"

    # translations.rpy:208
    old "Update Default Interface Translations"
    new "Обновить Базовый Перевод Интерфейса"

    # translations.rpy:228
    old "The extract command allows you to extract string translations from an existing project into a temporary file.\n\nThe merge command merges extracted translations into another project."
    new "{size=-1}Команда извлечения позволяет вам извлечь переводимые строки из существующего проекта во временный файл.\n\nКоманда объединения объединяет извлечённые переводы в другой перевод.{/size}"

    # translations.rpy:252
    old "Ren'Py is generating translations...."
    new "Ren'Py создаёт переводы..."

    # translations.rpy:263
    old "Ren'Py has finished generating [language] translations."
    new "Ren'Py закончила создавать перевод для [language]."

    # translations.rpy:276
    old "Ren'Py is extracting string translations..."
    new "Ren'Py извлекает переводимые строки..."

    # translations.rpy:279
    old "Ren'Py has finished extracting [language] string translations."
    new "Ren'Py завершила извлечение [language] строк перевода."

    # translations.rpy:299
    old "Ren'Py is merging string translations..."
    new "Ren'Py объединяет строки перевода..."

    # translations.rpy:302
    old "Ren'Py has finished merging [language] string translations."
    new "Ren'Py завершила объединение [language] строк перевода."

    # translations.rpy:313
    old "Updating default interface translations..."
    new "Обновляю базовый перевод интерфейса..."

    # translations.rpy:342
    old "Extract Dialogue: [project.current.display_name!q]"
    new "Извлечь диалог: [project.current.display_name!q]"

    # translations.rpy:358
    old "Format:"
    new "Формат:"

    # translations.rpy:366
    old "Tab-delimited Spreadsheet (dialogue.tab)"
    new "Табулированная таблица (dialogue.tab)"

    # translations.rpy:367
    old "Dialogue Text Only (dialogue.txt)"
    new "Только текст диалога (dialogue.txt)"

    # translations.rpy:380
    old "Strip text tags from the dialogue."
    new "Убрать текстовые теги из диалога."

    # translations.rpy:381
    old "Escape quotes and other special characters."
    new "Включать кавычки и регулярные выражения."

    # translations.rpy:382
    old "Extract all translatable strings, not just dialogue."
    new "Извлечь все переводимые строки, не только диалог."

    # translations.rpy:410
    old "Ren'Py is extracting dialogue...."
    new "Ren'Py извлекает диалог..."

    # translations.rpy:414
    old "Ren'Py has finished extracting dialogue. The extracted dialogue can be found in dialogue.[persistent.dialogue_format] in the base directory."
    new "Ren'Py завершила извлечение диалога. Извлечённый диалог можно найти в файле dialogue.[persistent.dialogue_format] в директории проекта."

    # updater.rpy:63
    old "{b}Recommended.{/b} The version of Ren'Py that should be used in all newly-released games."
    new "{b}Рекомендуется.{/b} Эта версия Ren'Py должна использоваться для всех новых игр."

    # updater.rpy:65
    old "Prerelease"
    new "Пререлиз"

    # updater.rpy:66
    old "A preview of the next version of Ren'Py that can be used for testing and taking advantage of new features, but not for final releases of games."
    new "Публичный анонс следующей версии Ren'Py, который можно использовать для тестирования, в том числе новых возможностей Ren'Py, но не для финальных релизов игр."

    # updater.rpy:68
    old "Experimental"
    new "Экспериментальный"

    # updater.rpy:69
    old "Experimental versions of Ren'Py. You shouldn't select this channel unless asked by a Ren'Py developer."
    new "Экспериментальные версии Ren'Py. Не выбирайте этот канал, если вас не просил об этом разработчик Ren'Py."

    # updater.rpy:71
    old "Nightly"
    new "Ночной"

    # updater.rpy:72
    old "The bleeding edge of Ren'Py development. This may have the latest features, or might not run at all."
    new "Развитие Ren'Py на краю горизонта событий. Здесь можно найти новейшие возможности Ren'Py или всё может просто не запуститься."

    # updater.rpy:90
    old "Select Update Channel"
    new "Выберите канал обновлений"

    # updater.rpy:101
    old "The update channel controls the version of Ren'Py the updater will download."
    new "Канал обновлений отвечает за версию Ren'Py, скачиваемую через обновление."

    # updater.rpy:110
    old "• This version is installed and up-to-date."
    new "• На данный момент установлена эта версия."

    # updater.rpy:118
    old "%B %d, %Y"
    new "%d %B %Y года"

    # updater.rpy:140
    old "An error has occured:"
    new "Возникла ошибка:"

    # updater.rpy:142
    old "Checking for updates."
    new "Проверка обновлений."

    # updater.rpy:144
    old "Ren'Py is up to date."
    new "Ren'Py обновлена."

    # updater.rpy:146
    old "[u.version] is now available. Do you want to install it?"
    new "[u.version] доступна. Вы хотите её установить?"

    # updater.rpy:148
    old "Preparing to download the update."
    new "Подготовка к обновлению."

    # updater.rpy:150
    old "Downloading the update."
    new "Загрузка обновления."

    # updater.rpy:152
    old "Unpacking the update."
    new "Распаковка обновления."

    # updater.rpy:154
    old "Finishing up."
    new "Завершаю..."

    # updater.rpy:156
    old "The update has been installed. Ren'Py will restart."
    new "Обновление было установлено. Ren'Py будет перезапущена."

    # updater.rpy:158
    old "The update has been installed."
    new "Обновление было установлено."

    # updater.rpy:160
    old "The update was cancelled."
    new "Обновление было отменено."

    # updater.rpy:177
    old "Ren'Py Update"
    new "Обновление Ren'Py"

    # updater.rpy:183
    old "Proceed"
    new "Продолжить"

    # updater.rpy:188
    old "Fetching the list of update channels"
    new "Запрашиваю список каналов обновления"

    # androidstrings.rpy:20
    old "The arm64-v8a version works on newer Android devices, the armeabi-v7a version works on older devices, and the x86_64 version works on the simulator and chromebooks."
    new "Версия arm64-v8a работает на новых Android устройствах, версия armeabi-v7a требуется для старых устройств, а версия x86_64 требуется для симуляторов и хромбуков."

    # front_page.rpy:252
    old "Web"
    new "Веб-инструменты"

    # game/front_page.rpy:252
    old "(Beta)"
    new "(Бета)"

    # interface.rpy:394
    old "While [what!qt], an error occured:"
    new "В процессе выполнения \"[what!qt]\" произошла ошибка:"

    # interface.rpy:394
    old "[exception!q]"
    new "[exception!q]"

    # itch.rpy:43
    old "Downloading the itch.io butler."
    new "Загрузка itch.io помошника"

    # web.rpy:118
    old "Web: [project.current.display_name!q]"
    new "Web: [project.current.display_name!q]"

    # web.rpy:148
    old "Build Web Application"
    new "Построить приложение для сети"

    # web.rpy:149
    old "Build and Open in Browser"
    new "Построить и открыть в браузере"

    # web.rpy:150
    old "Open without Build"
    new "Открыть без постройки"

    # web.rpy:154
    old "Support:"
    new "Поддержка:"

    # web.rpy:162
    old "RenPyWeb Home"
    new "RenPyWeb главная страница"

    # web.rpy:163
    old "Beuc's Patreon"
    new "Патреон Beuc"

    # web.rpy:181
    old "Ren'Py web applications require the entire game to be downloaded to the player's computer before it can start."
    new "Веб-приложения Ren'Py требуют, чтобы вся игра была загружена на компьютер игрока, прежде чем она запуститься."

    # web.rpy:185
    old "Current limitations in the web platform mean that loading large images, audio files, or movies may cause audio or framerate glitches, and lower performance in general."
    new "Текущие ограничения веб-платформы означают, что загрузка больших изображений, аудиофайлов или фильмов может привести к сбоям звука или частоты смены кадров, а также к снижению производительности в целом."

    # web.rpy:194
    old "Before packaging web apps, you'll need to download RenPyWeb, Ren'Py's web support. Would you like to download RenPyWeb now?"
    new "Перед упаковкой веб-приложений вам необходимо загрузить RenPyWeb, веб-поддержку Ren'Py. Вы хотите загрузить RenPyWeb прямо сейчас?"

    # choose_theme.rpy:507
    old "changing the theme"
    new "смена темы"

    # gui7.rpy:429
    old "creating a new project"
    new "создание нового проекта"

    # gui7.rpy:433
    old "activating the new project"
    new "активация нового проекта"

    # interface.rpy:372
    old "opening the log file"
    new "открытие лог-файла"

    # updater.rpy:194
    old "downloading the list of update channels"
    new "загрузка списка каналов обновления"

    # updater.rpy:198
    old "parsing the list of update channels"
    new "разбор списка каналов обновления"

    # game/web.rpy:150
    old "Open in Browser"
    new "Открыть в браузере"

    # game/web.rpy:151
    old "Open build directory"
    new "Открыть папку сборки"

    # game/androidstrings.rpy:47
    old "Do you want to automatically update the Java source code?"
    new "Вы хотите автоматически обновлять исходный код Java?"

    # game/choose_directory.rpy:93
    old "Ren'Py was unable to run python with tkinter to choose the directory. Please install the python3-tk or tkinter package."
    new "Ren'Py не смог запустить python с tkinter для выбора каталога. Пожалуйста, установите модуль python3-tk или tkinter."

    # game/front_page.rpy:198
    old "audio"
    new "звук"

    # game/install.rpy:33
    old "Could not install [name!t], as a file matching [zipglob] was not found in the Ren'Py SDK directory."
    new "Установка [name!t] провалилась, так как файл, соответствующий [zipglob] не был найден в папке Ren'Py SDK."

    # game/install.rpy:76
    old "Successfully installed [name!t]."
    new "Успешно установлен [name!t]."

    # game/install.rpy:104
    old "Install Libraries"
    new "Установка библиотек"

    # game/install.rpy:119
    old "This screen allows you to install libraries that can't be distributed with Ren'Py. Some of these libraries may require you to agree to a third-party license before being used or distributed."
    new "Этот экран позволяет установить библиотеки, которые не могут распространяться вместе с Ren'Py. Некоторые из этих библиотек могут потребовать от вас принятия сторонней лицензии для использования или распространения."

    # game/install.rpy:131
    old "Install Live2D Cubism SDK for Native"
    new "Установить Live2D Cubism SDK for Native"

    # game/install.rpy:134
    old "The {a=https://www.live2d.com/en/download/cubism-sdk/download-native/}Cubism SDK for Native{/a} adds support for displaying Live2D models. Place CubismSdkForNative-4-{i}version{/i}.zip in the Ren'Py SDK directory, and then click Install. Distributing a game with Live2D requires you to accept a license from Live2D, Inc."
    new "{a=https://www.live2d.com/en/download/cubism-sdk/download-native/}Cubism SDK for Native{/a} добавляет поддержку отображения моделей Live2D. Поместите CubismSdkForNative-4-{i}версия{/i}.zip в папку Ren'Py SDK, а затем нажмите кнопку Установить. Для распространения игры с Live2D необходимо принять лицензию от Live2D, Inc."

    # game/install.rpy:138
    old "Open Ren'Py SDK Directory"
    new "Открыть папку Ren'Py SDK"

    # game/preferences.rpy:138
    old "Install libraries"
    new "Установить библиотеки"

    # game/preferences.rpy:140
    old "Reset window size"
    new "Сбросить размер окна"

    # game/install.rpy:144
    old "Live2D in Ren'Py doesn't support the Web, Android x86_64 (including emulators and Chrome OS), and must be added to iOS projects manually. Live2D must be reinstalled after upgrading Ren'Py or installing Android support."
    new "Live2D в Ren'Py не поддерживается на Web, Android x86_64 (включая эмуляторы и Chrome OS), а также должен добавлятся в iOS проекты вручную. Live2D должен быть установлен заново после обновления Ren'Py и/или установки пакета поддержки Android."

    # game/install.rpy:151
    old "Install Steam Support"
    new "Установить поддержку Steam"

    # game/install.rpy:160
    old "Before installing Steam support, please make sure you are a {a=https://partner.steamgames.com/}Steam partner{/a}."
    new "Перед установкой поддержки Steam убедитесь что вы являетесь {a=https://partner.steamgames.com/}партнёром Steam{/a}."

    # game/install.rpy:172
    old "Steam support has already been installed."
    new "Поддержка Steam уже установлена."

    # game/web.rpy:242
    old "Preparing progressive download"
    new "Подготовка прогрессивной загрузки"

    # game/web.rpy:341
    old "Images and musics can be downloaded while playing. A 'progressive_download.txt' file will be created so you can configure this behavior."
    new "Изображения и музыка могут загружаться во время игры. Будет создан файл 'progressive_download.txt', чтобы вы могли настроить такое поведение."

    # game/androidstrings.rpy:21
    old "The universal version works everywhere but is larger."
    new "Универсальная версия работает на всех устройствах но занимает больше места."

    # game/androidstrings.rpy:45
    old "Automatically installing expansion APKs {a=https://issuetracker.google.com/issues/160942333}may not work on Android 11{/a}."
    new "Автоматическая установка APK-расширения {a=https://issuetracker.google.com/issues/160942333}может не работать на Android 11{/a}."

    # game/android.rpy:35
    old "A 64-bit/x64 Java 8 Development Kit is required to build Android packages on Windows. The JDK is different from the JRE, so it's possible you have Java without having the JDK.\n\nPlease {a=https://adoptopenjdk.net/?variant=openjdk8&jvmVariant=hotspot}download and install the JDK{/a}, then restart the Ren'Py launcher."
    new "Для сборки пакетов Android под Windows требуется 64-bit/x64 Java 8 Development Kit. JDK отличается от JRE, поэтому возможно, что у вас есть Java без JDK.\n\n{a=https://adoptopenjdk.net/?variant=openjdk8&jvmVariant=hotspot}Cкачайте и установите JDK{/a}, затем перезапустите лаунчер Ren'Py."

    # game/android.rpy:38
    old "RAPT has been installed, but a bundle key hasn't been configured. Please create a new key, or restore bundle.keystore."
    new "RAPT был установлен, но ключ Bundle не был настроен. Пожалуйста, создайте новый ключ или восстановите bundle.keystore."

    # game/android.rpy:40
    old "Please select if you want a Play Bundle (for Google Play), or a Universal APK (for sideloading and other app stores)."
    new "Пожалуйста, выберите, хотите ли вы создать Play Bundle (для Google Play) или универсальный APK (для других магазинов приложений и распространения локально)."

    # game/android.rpy:55
    old "Lists the connected devices."
    new "Список подключенных устройств."

    # game/android.rpy:56
    old "Pairs with a device over Wi-Fi, on Android 11+."
    new "Сопряжение с устройством по Wi-Fi, на Android 11+"

    # game/android.rpy:57
    old "Connects to a device over Wi-Fi, on Android 11+."
    new "Подключение к устройству по Wi-Fi, на Android 11+"

    # game/android.rpy:58
    old "Disconnects a device connected over Wi-Fi."
    new "Отключение от устройства по Wi-Fi, на Android 11+"

    # game/android.rpy:60
    old "Builds an Android App Bundle (ABB), intended to be uploaded to Google Play. This can include up to 2GB of data."
    new "Создает пакет приложений для Android (ABB), предназначенный для загрузки в Google Play. Он может включать до 2 ГБ данных."

    # game/android.rpy:61
    old "Builds a Universal APK package, intended for sideloading and stores other than Google Play. This can include up to 2GB of data."
    new "Создает универсальный APK, предназначенный для магазинов, отличных от Google Play и локального распространения. Он может включать до 2 ГБ данных."

    # game/android.rpy:396
    old "Play Bundle"
    new "Play Bundle"

    # game/android.rpy:401
    old "Universal APK"
    new "Универсальный APK"

    # game/android.rpy:451
    old "List Devices"
    new "Список устройств"

    # game/android.rpy:455
    old "Wi-Fi Debugging Pair"
    new "Отладка сопряжения по Wi-Fi"

    # game/android.rpy:459
    old "Wi-Fi Debugging Connect"
    new "Отладка подключения по Wi-Fi"

    # game/android.rpy:463
    old "Wi-Fi Debugging Disconnect"
    new "Отладка отключения от Wi-Fi"

    # game/android.rpy:562
    old "Wi-Fi Pairing Code"
    new "Код сопряжения по Wi-Fi"

    # game/android.rpy:562
    old "If supported, this can be found in 'Developer options', 'Wireless debugging', 'Pair device with pairing code'."
    new "Если поддерживается, это можно найти в 'Настройки разработчика', 'Отладка беспроводной сети', 'Сопряжение устройства кодом сопряжения'."

    # game/android.rpy:569
    old "Pairing Host & Port"
    new "Сопряжение через хост и порт"

    # game/android.rpy:585
    old "IP Address & Port"
    new "IP-адрес и порт"

    # game/android.rpy:585
    old "If supported, this can be found in 'Developer options', 'Wireless debugging'."
    new "Если поддерживается, это можно найти в 'Настройки разработчика', 'Отладка беспроводной сети'."

    # game/android.rpy:601
    old "This can be found in 'List Devices'."
    new "Это можно найти в 'Список устройств'."

    # game/androidstrings.rpy:16
    old "I'm installing the bundle."
    new "Установка Bundle."

    # game/androidstrings.rpy:17
    old "Installing the bundle appears to have failed."
    new "Установка Bundle, похоже, не удалась."

    # game/androidstrings.rpy:19
    old "Launching the app appears to have failed."
    new "Запуск приложения, похоже, не удался."

    # game/androidstrings.rpy:32
    old "How much RAM do you want to allocate to Gradle?\n\nThis must be a positive integer number."
    new "Сколько оперативной памяти вы хотите выделить Gradle?\n\nЭто должно быть целое положительное число."

    # game/androidstrings.rpy:33
    old "The RAM size must contain only numbers."
    new "Размер оперативной памяти должен содержать только числа."

    # game/androidstrings.rpy:43
    old "I was unable to use javac to compile a test file. If you haven't installed the Java Development Kit yet, please download it from:\n\nhttps://adoptopenjdk.net/?variant=openjdk8&jvmVariant=hotspot\n\nThe JDK is different from the JRE, so it's possible you have Java without having the JDK. Without a working JDK, I can't continue."
    new "Не удалось использовать javac для компиляции тестового файла. Если вы еще не установили Java Development Kit, пожалуйста, скачайте его с:\n\nhttps://adoptopenjdk.net/?variant=openjdk8&jvmVariant=hotspot\n\nJDK отличается от JRE, поэтому возможно, что у вас есть Java без JDK. Без работающего JDK невозможно продолжить."

    # game/androidstrings.rpy:44
    old "The version of Java on your computer does not appear to be JDK 8, which is the only version supported by the Android SDK. If you need to install JDK 8, you can download it from:\n\n{a=https://adoptium.net/?variant=openjdk8}https://adoptium.net/?variant=openjdk8{/a}\n\nYou can also set the JAVA_HOME environment variable to use a different version of Java."
    new "Версия Java на вашем компьютере, похоже, не JDK 8, которая является единственной версией, поддерживаемой Android SDK. Если вам нужно установить JDK 8, вы можете загрузить его с:\n\n{a=https://adoptium.net/?variant=openjdk8}https://adoptium.net/?variant=openjdk8{/a}\n\nВы также можете установить переменную среды JAVA_HOME, чтобы использовать другую версию Java."

    # game/androidstrings.rpy:57
    old "I can create an application signing key for you. This key is required to create Universal APK for sideloading and stores other than Google Play.\n\nDo you want to create a key?"
    new "Я могу создать для вас ключ подписи приложения. Этот ключ необходим для создания универсального APK для магазинов, отличных от Google Play и для локального распространения.\n\nХотите создать ключ?"

    # game/androidstrings.rpy:61
    old "I can create a bundle signing key for you. This key is required to build an Android App Bundle (AAB) for upload to Google Play.\n\nDo you want to create a key?"
    new "Я могу создать для вас ключ подписи пакета. Этот ключ необходим для создания пакета приложения Android (AAB) для загрузки в Google Play.\n\n\nХотите создать ключ?"

    # game/androidstrings.rpy:62
    old "I will create the key in the bundle.keystore file.\n\nYou need to back this file up. If you lose it, you will not be able to upgrade your application.\n\nYou also need to keep the key safe. If evil people get this file, they could make fake versions of your application, and potentially steal your users' data.\n\nWill you make a backup of bundle.keystore, and keep it in a safe place?"
    new "Я создам ключ в файле bundle.keystore.\n\nВам нужно создать резервную копию этого файла. Если вы потеряете его, вы не сможете обновить ваше приложение.\n\nВы также должны хранить ключ в безопасности. Если злоумышленники получат этот файл, они могут создать поддельную версию вашего приложения и, возможно, украсть данные ваших пользователей.\n\nСделаете ли вы резервную копию bundle.keystore и сохраните ее в безопасном месте?"

    # game/androidstrings.rpy:63
    old "Could not create bundle.keystore. Is keytool in your path?"
    new "Не удалось создать bundle.keystore. Проверьте, есть ли keytool в path?"

    # game/gui7.rpy:311
    old "{size=-4}\n\nThis will not overwrite gui/main_menu.png, gui/game_menu.png, and gui/window_icon.png, but will create files that do not exist.{/size}"
    new "{size=-4}\n\nЭто не перезапишет gui/main_menu.png, gui/game_menu.png, и gui/window_icon.png, но создаст несуществующие файлы.{/size}"

    # game/ios.rpy:339
    old "There are known issues with the iOS simulator on Apple Silicon. Please test on x86_64 or iOS devices."
    new "Существуют проблемы с симулятором iOS на Apple Silicon. Пожалуйста, протестируйте на x86_64 или iOS-устройствах."

    # game/preferences.rpy:206
    old "Daily check for update"
    new "Ежедневная проверка обновлений"

    # game/preferences.rpy:210
    old "Default theme"
    new "Тема по умолчанию"

    # game/preferences.rpy:212
    old "Dark theme"
    new "Тёмная тема"

    # game/preferences.rpy:213
    old "Custom theme"
    new "Пользовательская тема"

    # game/web.rpy:330
    old "Images and music can be downloaded while playing. A 'progressive_download.txt' file will be created so you can configure this behavior."
    new "Изображения и музыка могут быть загружаемы во время игры. В созданном файле 'progressive_download.txt', вы можете настроить это поведение."

    # game/web.rpy:334
    old "Current limitations in the web platform mean that loading large images may cause audio or framerate glitches, and lower performance in general. Movies aren't supported."
    new "Текущие ограничения веб-платформы означают, что загрузка больших изображений может привести к сбоям звука или частоты кадров, а также к снижению производительности в целом. Видео-файлы не поддерживаются."

    # game/web.rpy:338
    old "There are known issues with Safari and other Webkit-based browsers that may prevent games from running."
    new "Существуют проблемы с Safari и другими браузерами на базе Webkit, которые могут не позволить запустить игру."

    # game/updater.rpy:109
    old "• {a=https://www.renpy.org/doc/html/changelog.html}View change log{/a}"
    new "• {a=https://www.renpy.org/doc/html/changelog.html}Посмотреть журнал изменений{/a}"

    # game/updater.rpy:111
    old "• {a=https://www.renpy.org/dev-doc/html/changelog.html}View change log{/a}"
    new "• {a=https://www.renpy.org/dev-doc/html/changelog.html}Посмотреть журнал изменений{/a}"

    # game/android.rpy:60
    old "Removes Android temporary files."
    new "Очистить временные файлы Android"

    # game/android.rpy:472
    old "Clean"
    new "Очистить"

    # game/android.rpy:628
    old "Cleaning up Android project."
    new "Очистка временных файлов Android"

    # game/androidstrings.rpy:43
    old "I was unable to use javac to compile a test file. If you haven't installed the Java Development Kit yet, please download it from:\n\n{a=https://adoptium.net/?variant=openjdk8}https://adoptium.net/?variant=openjdk8{/a}\n\nThe JDK is different from the JRE, so it's possible you have Java without having the JDK. Please make sure you installed the 'JavaSoft (Oracle) registry keys'.\n\nWithout a working JDK, I can't continue."
    new "Не удалось использовать javac для компиляции тестового файла. Если вы еще не установили Java Development Kit, загрузите его с:\n\n{a=https://adoptium.net/?variant=openjdk8}https://adoptium.net/?variant=openjdk8{/a}\n\JDK отличается от JRE, поэтому возможно, что у вас есть Java без JDK. Пожалуйста, убедитесь, что вы установили 'переменные окружения JavaSoft (Oracle)'.\n\nБез работающего JDK я не могу продолжать."

    # game/androidstrings.rpy:64
    old "I've opened the directory containing android.keystore and bundle.keystore. Please back them up, and keep them in a safe place."
    new "Открыт каталог, содержащий android.keystore и bundle.keystore. Пожалуйста, сделайте их резервную копию и храните в безопасном месте."

    # game/choose_directory.rpy:67
    old "Select Projects Directory"
    new "Выбрать папку с проектами"

    # game/distribute.rpy:1674
    old "Copying files..."
    new "Копирование файлов..."

    # game/distribute_gui.rpy:195
    old "Update old-game"
    new "Обновить old-game"

    # game/editor.rpy:152
    old "A modern editor with many extensions including advanced Ren'Py integration."
    new "Современный текстовый редактор с множеством расширений, включая расширенную интеграцию Ren'Py."

    # game/editor.rpy:153
    old "A modern editor with many extensions including advanced Ren'Py integration.\n{a=jump:reinstall_vscode}Upgrade Visual Studio Code to the latest version.{/a}"
    new "Современный текстовый редактор с множеством расширений, включая расширенную интеграцию Ren'Py.\n{a=jump:reinstall_vscode}Обновить Visual Studio Code до последней версии.{/a}"

    # game/editor.rpy:162
    old "Visual Studio Code"
    new "Visual Studio Code"

    # game/editor.rpy:162
    old "Up to 110 MB download required."
    new "Требуется скачать 110 МБ."

    # game/editor.rpy:175
    old "A modern and approachable text editor."
    new "Современный и удобный текстовый редактор."

    # game/editor.rpy:187
    old "Atom"
    new "Atom"

    # game/editor.rpy:200
    old "jEdit"
    new "jEdit"

    # game/editor.rpy:209
    old "Visual Studio Code (System)"
    new "Visual Studio Code (установленный)"

    # game/editor.rpy:209
    old "Uses a copy of Visual Studio Code that you have installed outside of Ren'Py. It's recommended you install the language-renpy extension to add support for Ren'Py files."
    new "Используется версия Visual Studio Code, установленная вне Ren'Py. Рекомендуется установить расширение language-renpy, чтобы добавить поддержку файлов Ren'Py."

    # game/installer.rpy:10
    old "Downloading [extension.download_file]."
    new "Загрузка [extension.download_file]."

    # game/installer.rpy:11
    old "Could not download [extension.download_file] from [extension.download_url]:\n{b}[extension.download_error]"
    new "Не удалось загрузить [extension.download_file] из [extension.download_url]:\n{b}[extension.download_error]"

    # game/installer.rpy:12
    old "The downloaded file [extension.download_file] from [extension.download_url] is not correct."
    new "Загруженный файл [extension.download_file] из [extension.download_url] некорректен."

    # game/interface.rpy:124
    old "[interface.version]"
    new "[interface.version]"

    # game/preferences.rpy:153
    old "Clean temporary files"
    new "Очистить временные файлы"

    # game/preferences.rpy:255
    old "Cleaning temporary files..."
    new "Очистка временных файлов..."

    # game/project.rpy:280
    old "This may be because the project is not writeable."
    new "Это может быть связано с тем, что папка проекта недоступна для записи."

    # game/translations.rpy:391
    old "Language (or None for the default language):"
    new "Язык (или None для языка по умолчанию):"

    # game/web.rpy:344
    old "This feature is not supported in Ren'Py 8."
    new "Этот функционал недоступен в Ren'Py 8."

    # game/web.rpy:344
    old "We will restore support in a future release of Ren'Py 8. Until then, please use Ren'Py 7 for web support."
    new "Мы восстановим поддержку в будущем релизе Ren'Py 8. Пока что, пожалуйста используйте Ren'Py 7 для веб-сборки."

    # game/preferences.rpy:104
    old "General"
    new "Общие"

    # game/preferences.rpy:105
    old "Options"
    new "Опции"

    # game/preferences.rpy:244
    old "Launcher Theme:"
    new "Тема лаунчера:"

    # game/preferences.rpy:254
    old "Information about creating a custom theme can be found {a=[skins_url]}in the Ren'Py Documentation{/a}."
    new "Информацию о создании пользовательских тем можно найти {a=[skins_url]}в документации Ren'Py{/a}."

    # game/preferences.rpy:271
    old "Install Libraries:"
    new "Установить библиотеки:"

    # game/preferences.rpy:338
    old "{#in language font}Welcome! Please choose a language"
    new "Добро пожаловать!\nВыберите язык"

    # game/preferences.rpy:373
    old "{#in language font}Start using Ren'Py in [lang_name]"
    new "Начать использовать Ren'Py на русском"

    # game/updater.rpy:64
    old "Release (Ren'Py 8, Python 3)"
    new "Релиз (Ren'Py 8, Python 3)"

    # game/updater.rpy:65
    old "Release (Ren'Py 7, Python 2)"
    new "Релиз (Ren'Py 7, Python 2)"

    # game/updater.rpy:69
    old "Prerelease (Ren'Py 8, Python 3)"
    new "Пререлиз (Ren'Py 8, Python 3)"

    # game/updater.rpy:70
    old "Prerelease (Ren'Py 7, Python 2)"
    new "Пререлиз (Ren'Py 7, Python 2)"

    # game/updater.rpy:77
    old "Nightly (Ren'Py 8, Python 3)"
    new "Ночной (Ren'Py 8, Python 3)"

    # game/updater.rpy:78
    old "Nightly (Ren'Py 7, Python 2)"
    new "Ночной (Ren'Py 7, Python 2)"

translate russian strings:

    # game/android.rpy:39
    old "RAPT has been installed, but a key hasn't been configured. Please generate new keys, or copy android.keystore and bundle.keystore to the base directory."
    # Automatic translation.
    new "RAPT был установлен, но ключ не был настроен. Пожалуйста, сгенерируйте новые ключи или скопируйте android.keystore и bundle.keystore в базовый каталог."

    # game/android.rpy:46
    old "Attempts to emulate a televison-based Android console.\n\nController input is mapped to the arrow keys, Enter is mapped to the select button, Escape is mapped to the menu button, and PageUp is mapped to the back button."
    # Automatic translation.
    new "Попытка эмуляции телевизионной консоли Android.\n\nВвод контроллера отображается на клавиши со стрелками, Enter отображается на кнопку выбора, Escape отображается на кнопку меню, а PageUp отображается на кнопку назад."

    # game/android.rpy:48
    old "Downloads and installs the Android SDK and supporting packages."
    # Automatic translation.
    new "Загружает и устанавливает Android SDK и вспомогательные пакеты."

    # game/android.rpy:49
    old "Generates the keys required to sign the package."
    # Automatic translation.
    new "Генерирует ключи, необходимые для подписания пакета."

    # game/android.rpy:383
    old "Install SDK"
    # Automatic translation.
    new "Установите SDK"

    # game/android.rpy:387
    old "Generate Keys"
    # Automatic translation.
    new "Генерировать ключи"

    # game/androidstrings.rpy:32
    old "How much RAM (in GB) do you want to allocate to Gradle?\nThis must be a positive integer number."
    # Automatic translation.
    new "Сколько оперативной памяти (в ГБ) вы хотите выделить для Gradle?\nЭто должно быть целое положительное число."

    # game/androidstrings.rpy:33
    old "The RAM size must contain only numbers and be positive."
    # Automatic translation.
    new "Размер оперативной памяти должен содержать только числа и быть положительным."

    # game/androidstrings.rpy:63
    old "I found an android.keystore file in the rapt directory. Do you want to use this file?"
    # Automatic translation.
    new "Я нашел файл android.keystore в каталоге rapt. Вы хотите использовать этот файл?"

    # game/androidstrings.rpy:66
    old "\n\nSaying 'No' will prevent key creation."
    # Automatic translation.
    new "\n\nОтвет \"Нет\" не позволит создать ключ."

    # game/androidstrings.rpy:69
    old "I found a bundle.keystore file in the rapt directory. Do you want to use this file?"
    # Automatic translation.
    new "Я нашел файл bundle.keystore в каталоге rapt. Вы хотите использовать этот файл?"

    # game/distribute_gui.rpy:231
    old "(DLC)"
    new "(DLC)"

    # game/project.rpy:46
    old "Lint checks your game for potential mistakes, and gives you statistics."
    # Automatic translation.
    new "Lint проверяет вашу игру на наличие потенциальных ошибок и выдает статистику."

    # game/web.rpy:485
    old "Creating package..."
    # Automatic translation.
    new "Создание пакета..."

    # game/updater.rpy:79
    old "A nightly build of fixes to the release version of Ren'Py."
    # Automatic translation.
    new "Ночная сборка исправлений к релизной версии Ren'Py."

    # game/androidstrings.rpy:46
    old "I was unable to use javac to compile a test file. If you haven't installed the Java Development Kit yet, please download it from:\n\n{a=https://adoptium.net}https://adoptium.net/{/a}\n\nThe JDK is different from the JRE, so it's possible you have Java without having the JDK. Please install JDK [JDK_REQUIREMENT], and add it to your PATH.\n\nWithout a working JDK, I can't continue."
    new "Я не смог скомпилировать тестовый файл с помощью javac. Если вы еще не установили Java Development Kit, загрузите его с сайта:\n\n{a=https://adoptium.net}https://adoptium.net/{/a}\n\nJDK отличается от JRE, поэтому возможно, что у вас есть Java без JDK. Пожалуйста, установите JDK [JDK_REQUIREMENT] и добавьте его в PATH.\n\nБез работающего JDK я не могу продолжить."

    # game/androidstrings.rpy:47
    old "The version of Java on your computer does not appear to be JDK [JDK_REQUIREMENT], which is required to build Android apps. If you need to install a newer JDK, you can download it from:\n\n{a=https://adoptium.net/}https://adoptium.net/{/a}, and add it to your PATH.\n\nYou can also set the JAVA_HOME environment variable to use a different version of Java."
    new "Похоже, что версия Java на вашем компьютере не соответствует JDK [JDK_REQUIREMENT], который требуется для создания приложений для Android. Если вам нужно установить более новый JDK, вы можете загрузить его с:\n\n{a=https://adoptium.net/}https://adoptium.net/{/a} и добавить в PATH.\n\nВы также можете изменить переменную окружения JAVA_HOME, чтобы использовать другую версию Java."

    # game/choose_directory.rpy:72
    old "No directory was selected, but one is required."
    new "Не выбрана ни одна папка."

    # game/choose_directory.rpy:80
    old "The selected directory does not exist."
    new "Выбранная папка не существует."

    # game/choose_directory.rpy:82
    old "The selected directory is not writable."
    new "Выбранная папка недоступна для записи."

    # game/distribute.rpy:535
    old "Building distributions failed:\n\nThe project is the Ren'Py Tutorial, which can't be distributed outside of Ren'Py. Consider using The Question as a test project."
    new "Сборка дистрибутивов не удалась:\n\nПроект является туториалом Ren'Py, который не может быть собран за пределами Ren'Py. Используйте The Question в качестве тестового проекта."

    # game/distribute.rpy:562
    old "This may be derived from build.name and config.version or build.version."
    new "Это может быть связано с build.name и config.version или build.version."

    # game/distribute.rpy:1620
    old "Finishing the [variant] [format] package."
    new "Завершение работы над пакетом [variant] [format]."

    # game/editor.rpy:185
    old "Atom is deprecated and its bugs are known for corrupting games, using another editor is recommended."
    new "Atom устарел, и его баги известны тем, что повреждают игры, поэтому рекомендуется использовать другой редактор."

    # game/editor.rpy:214
    old "JEdit is deprecated, using another editor is recommended."
    new "JEdit устарел, рекомендуется использовать другой редактор."

    # game/editor.rpy:607
    old "The Atom text editor is no longer supported by its developers. We suggest switching to Visual Studio Code or another editor."
    new "Текстовый редактор Atom больше не поддерживается его разработчиками. Мы рекомендуем перейти на Visual Studio Code или другой редактор."

    # game/editor.rpy:607
    old "Select editor now."
    new "Выберите редактор."

    # game/editor.rpy:607
    old "Ignore until next launch."
    new "Игнорировать до следующего запуска."

    # game/editor.rpy:607
    old "Do not ask again."
    new "Больше не спрашивать."

    # game/new_project.rpy:38
    old "Warning : you are using Ren'Py 7. It is recommended to start new projects using Ren'Py 8 instead."
    new "Предупреждение: вы используете Ren'Py 7. Рекомендуется начинать новые проекты, используя Ren'Py 8."

    # game/new_project.rpy:49
    old "Please select a template project to use."
    new "Пожалуйста, выберите проект используемый как шаблон."

    # game/new_project.rpy:49
    old "Do not use a template project."
    new "Не использовать шаблон проекта."

    # game/preferences.rpy:94
    old "Lint"
    new "Проверка скрипта (lint)"

    # game/preferences.rpy:233
    old "Game Options:"
    new "Опции игры:"

    # game/preferences.rpy:240
    old "Skip splashscreen"
    new "Пропустить заставку"

    # game/preferences.rpy:258
    old "Restore window position"
    new "Восстановить положение окна"

    # game/preferences.rpy:262
    old "Prefer RPU updates"
    new "Предпочитать обновления RPU"

    # game/preferences.rpy:332
    old "Open projects.txt"
    new "Открыть файл projects.txt"

    # game/preferences.rpy:356
    old "Lint toggles:"
    new "Опции проверки скрипта:"

    # game/preferences.rpy:360
    old "Check for orphan/obsolete translations"
    new "Проверка на наличие ненужных/устаревших переводов"

    # game/preferences.rpy:363
    old "Check parameters shadowing reserved names"
    new "Проверка параметров, переписывающие зарезервированные имена"

    # game/preferences.rpy:366
    old "Print block, word, and character counts by speaking character."
    new "Печать количества блоков, слов и символов используемых каждым персонажем."

    # game/preferences.rpy:369
    old "Unclosed text tags"
    new "Незакрытые текстовые теги"

    # game/preferences.rpy:372
    old "Show all unreachable blocks and orphaned translations."
    new "Показать все недостижимые блоки и неиспользуемые переводы."

    # game/project.rpy:776
    old "Splashscreen skipped in launcher preferences."
    new "Заставка пропущена в настройках лаунчера."

    # game/updater.rpy:76
    old "Nightly Fix"
    new "Ежедневные исправления"

    # game/updater.rpy:77
    old "Nightly Fix (Ren'Py 8, Python 3)"
    new "Ежедневные исправления (Ren'Py 8, Python 3)"

    # game/updater.rpy:78
    old "Nightly Fix (Ren'Py 7, Python 2)"
    new "Ежедневные исправления (Ren'Py 7, Python 2)"
