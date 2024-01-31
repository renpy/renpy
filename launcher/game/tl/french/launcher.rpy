translate french strings:
    # game/new_project.rpy:77
    old "{#language name and font}"
    new "{font=fonts/Roboto-Light.ttf}Français{/font}"

    # about.rpy:39
    old "[version!q]"
    new "[version!q]"

    # about.rpy:43
    old "View license"
    new "Consulter la licence"

    # add_file.rpy:28
    old "FILENAME"
    new "NOM DU FICHIER"

    # add_file.rpy:28
    old "Enter the name of the script file to create."
    new "Entrez le nom du fichier du script à créer."

    # add_file.rpy:31
    old "The filename must have the .rpy extension."
    new "Le fichier doit avoir l’extension .rpy."

    # add_file.rpy:39
    old "The file already exists."
    new "Le fichier existe déjà."

    # add_file.rpy:42
    old "# Ren'Py automatically loads all script files ending with .rpy. To use this\n# file, define a label and jump to it from another file.\n"
    new "# Ren’Py charge automatiquement tous les fichiers de script finissant par .rpy. Pour utiliser ce ficher\n#, définissez un label et faites un « jump » vers lui depuis un autre fichier.\n"

    # android.rpy:30
    old "To build Android packages, please download RAPT, unzip it, and place it into the Ren'Py directory. Then restart the Ren'Py launcher."
    new "Pour compiler les paquets Android, veuillez télécharger RAPT, le décompresser et le placer dans le répertoire de Ren’Py. Ensuite, redémarrez le lanceur Ren’Py."

    # android.rpy:31
    old "An x86 Java Development Kit is required to build Android packages on Windows. The JDK is different from the JRE, so it's possible you have Java without having the JDK.\n\nPlease {a=http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html}download and install the JDK{/a}, then restart the Ren'Py launcher."
    new "Un Kit de Développement Java (JDK) 32 bits est nécessaire pour compiler les paquets Android depuis Windows. Le JDK n’est pas la même chose que le JRE, il est possible que Java soit installé sur votre machine sans le JDK.\n\n{a=http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html}Téléchargez et installez le JDK{/a}, puis relancez le lanceur Ren’Py."

    # android.rpy:32
    old "RAPT has been installed, but you'll need to install the Android SDK before you can build Android packages. Choose Install SDK to do this."
    new "RAPT a été installé, mais vous devez installer le kit de développement Android pour pouvoir compiler les paquets Android, avec « Installer le SDK »."

    # android.rpy:33
    old "RAPT has been installed, but a key hasn't been configured. Please create a new key, or restore android.keystore."
    new "RAPT a été installé, mais aucune clé n’a été configurée. Veuillez créer une nouvelle clé ou restaurer android.keystore."

    # android.rpy:34
    old "The current project has not been configured. Use \"Configure\" to configure it before building."
    new "Le projet actuel n’a pas été configuré. Choisissez « Configurer » pour effectuer la configuration."

    # android.rpy:35
    old "Choose \"Build\" to build the current project, or attach an Android device and choose \"Build & Install\" to build and install it on the device."
    new "Choisissez « Compiler » (build) pour compiler le projet actuel ou connectez un appareil Android et choisissez « Compiler et installer » (Build & Install) pour l’installer sur l’appareil."

    # android.rpy:37
    old "Attempts to emulate an Android phone.\n\nTouch input is emulated through the mouse, but only when the button is held down. Escape is mapped to the menu button, and PageUp is mapped to the back button."
    new "Tentative d'émulation d’un téléphone Android.\n\nLe contact est émulé par la souris, mais uniquement lorsque le bouton est pressé. La barre d’espace correspond au bouton menu et la touche PageUp correspond au bouton retour."

    # android.rpy:38
    old "Attempts to emulate an Android tablet.\n\nTouch input is emulated through the mouse, but only when the button is held down. Escape is mapped to the menu button, and PageUp is mapped to the back button."
    new "Tentative d’émulation d'une tablette Android.\n\nLe contact est émulé par la souris, mais uniquement lorsque le bouton est pressé. La barre d’espace correspond au bouton menu et la touche PageUp correspond au bouton retour."

    # android.rpy:39
    old "Attempts to emulate a televison-based Android console, like the OUYA or Fire TV.\n\nController input is mapped to the arrow keys, Enter is mapped to the select button, Escape is mapped to the menu button, and PageUp is mapped to the back button."
    new "Tentative d’émulation d'une console télé basée sur Android, comme OUYA ou Fire TV.\n\nLa manette est émulée par les touches fléchées, le bouton select par la touche Entrée, le bouton menu par la touche Echap, et le bouton retour par la touche PageUp."

    # android.rpy:41
    old "Downloads and installs the Android SDK and supporting packages. Optionally, generates the keys required to sign the package."
    new "Télécharge et installe le kit de développement Android et les paquets requis. Optionnellement, génère les clés requises pour signer le paquet."

    # android.rpy:42
    old "Configures the package name, version, and other information about this project."
    new "Configure le nom du paquet, sa version et d’autres informations à propos de ce projet."

    # android.rpy:43
    old "Opens the file containing the Google Play keys in the editor.\n\nThis is only needed if the application is using an expansion APK. Read the documentation for more details."
    new "Ouvre le fichier contenant les clés Google Play dans l’éditeur.\n\nCela est nécessaire uniquement si l’application utilise une expansion APK. Référez-vous à la documentation pour plus d’informations."

    # android.rpy:44
    old "Builds the Android package."
    new "Compiler le paquet Android."

    # android.rpy:45
    old "Builds the Android package, and installs it on an Android device connected to your computer."
    new "Compile le paquet Android et l’installe sur l’appareil Android connecté à votre ordinateur."

    # android.rpy:46
    old "Builds the Android package, installs it on an Android device connected to your computer, then launches the app on your device."
    new "Compile le paquet Android, l’installe sur l’appareil Android connecté à votre ordinateur et lance l’application sur l’appareil."

    # android.rpy:48
    old "Connects to an Android device running ADB in TCP/IP mode."
    new "Se connecte en mode TCP/IP à l’appareil Android sur lequel tourne ADB."

    # android.rpy:49
    old "Disconnects from an Android device running ADB in TCP/IP mode."
    new "Se déconnecte de l’appareil Android sur lequel tourne ADB en mode TCP/IP."

    # android.rpy:50
    old "Retrieves the log from the Android device and writes it to a file."
    new "Récupère les journaux depuis l’appareil Android les retranscrit dans un fichier."

    # android.rpy:240
    old "Copying Android files to distributions directory."
    new "Copie en cours des fichiers vers le répertoire de distribution."

    # android.rpy:304
    old "Android: [project.current.name!q]"
    new "Android : [project.current.name!q]"

    # android.rpy:324
    old "Emulation:"
    new "Émulateur :"

    # android.rpy:333
    old "Phone"
    new "Téléphone"

    # android.rpy:337
    old "Tablet"
    new "Tablette"

    # android.rpy:341
    old "Television"
    new "Télévision"

    # android.rpy:353
    old "Build:"
    new "Compiler :"

    # android.rpy:361
    old "Install SDK & Create Keys"
    new "Installer le kit de développement et créer les clés"

    # android.rpy:365
    old "Configure"
    new "Configurer"

    # android.rpy:369
    old "Build Package"
    new "Compiler le paquet"

    # android.rpy:373
    old "Build & Install"
    new "Compiler et installer"

    # android.rpy:377
    old "Build, Install & Launch"
    new "Compile, installe et exécute"

    # android.rpy:388
    old "Other:"
    new "Autre :"

    # android.rpy:396
    old "Remote ADB Connect"
    new "Connexion ADB distante"

    # android.rpy:400
    old "Remote ADB Disconnect"
    new "Déconnexion distante ADB"

    # android.rpy:404
    old "Logcat"
    new "Logcat"

    # android.rpy:437
    old "Before packaging Android apps, you'll need to download RAPT, the Ren'Py Android Packaging Tool. Would you like to download RAPT now?"
    new "Avant de paquager les applications Android, vous devez télécharger RAPT, le « Ren'Py Android Packaging Tool ». Voulez-vous télécharger RAPT maintenant ?"

    # android.rpy:496
    old "Remote ADB Address"
    new "Adresse ADB distante"

    # android.rpy:496
    old "Please enter the IP address and port number to connect to, in the form \"192.168.1.143:5555\". Consult your device's documentation to determine if it supports remote ADB, and if so, the address and port to use."
    new "Veuillez entre l’adresse IP et le port selon le format « 192.168.1.143:5555 » pour vous connecter. Consultez la documentation de votre appareil pour déterminer s’il supporte l’ADB et, si tel est le cas, l’adresse et le port à utiliser."

    # android.rpy:508
    old "Invalid remote ADB address"
    new "Adresse ADB distante invalide"

    # android.rpy:508
    old "The address must contain one exactly one ':'."
    new "L’adresse doit contenir exactement un ':'."

    # android.rpy:512
    old "The host may not contain whitespace."
    new "L’hôte ne doit pas contenir d’espace."

    # android.rpy:518
    old "The port must be a number."
    new "Le port doit être un nombre entier."

    # android.rpy:544
    old "Retrieving logcat information from device."
    new "Récupération en cours des logcat depuis l’appareil."

    # choose_directory.rpy:73
    old "Ren'Py was unable to run python with tkinter to choose the directory. Please install the python-tk or tkinter package."
    new "Ren’Py n’a pas réussi à exécuter python avec le tkinter pour choisir le répertoire. Veuillez installer le paquet python-tk ou tkinter."

    # choose_theme.rpy:303
    old "Could not change the theme. Perhaps options.rpy was changed too much."
    new "Impossible de changer le thème. Peut être que options.rpy a été trop modifié."

    # choose_theme.rpy:370
    old "Planetarium"
    # Automatic translation.
    new "Planétarium"

    # choose_theme.rpy:425
    old "Choose Theme"
    new "Choisir un thème"

    # choose_theme.rpy:438
    old "Theme"
    new "Thème"

    # choose_theme.rpy:463
    old "Color Scheme"
    new "Agencement des couleurs"

    # choose_theme.rpy:495
    old "Continue"
    new "Continuer"

    # consolecommand.rpy:84
    old "INFORMATION"
    new "INFORMATION"

    # consolecommand.rpy:84
    old "The command is being run in a new operating system console window."
    new "La commande est en cours d’exécution dans une nouvelle console du système d’exploitation."

    # distribute.rpy:443
    old "Scanning project files..."
    new "Analyse des fichiers du projet en cours..."

    # distribute.rpy:459
    old "Building distributions failed:\n\nThe build.directory_name variable may not include the space, colon, or semicolon characters."
    new "La compilation de la distribution a échoué :\n\nLa variable « build.directory_name » ne doit pas contenir d’espace, ni de virgule, ni de point-virgule."

    # distribute.rpy:504
    old "No packages are selected, so there's nothing to do."
    new "Aucun paquet n’a été sélectionné, il n’y a donc rien à faire."

    # distribute.rpy:516
    old "Scanning Ren'Py files..."
    new "Analyse des fichiers Ren’Py en cours..."

    # distribute.rpy:569
    old "All packages have been built.\n\nDue to the presence of permission information, unpacking and repacking the Linux and Macintosh distributions on Windows is not supported."
    new "Tous les paquets ont été construits.\n\nDu fait de l’absence de systèmes de permissions sur Windows, il n’est pas possible de reconstruire les paquets construits sur GNU-Linux ou Mac OS sur Windows."

    # distribute.rpy:752
    old "Archiving files..."
    new "Archivage des fichiers..."

    # distribute.rpy:1050
    old "Unpacking the Macintosh application for signing..."
    new "Décompression de l’application Macintosh pour calcul de la signature..."

    # distribute.rpy:1060
    old "Signing the Macintosh application..."
    new "Signature de l’application Macintosh en cours..."

    # distribute.rpy:1082
    old "Creating the Macintosh DMG..."
    new "Création en cours du DMG Macintosh..."

    # distribute.rpy:1091
    old "Signing the Macintosh DMG..."
    new "Signature en cours du DMG Macintosh..."

    # distribute.rpy:1248
    old "Writing the [variant] [format] package."
    new "Écriture du paquet [variant] [format]."

    # distribute.rpy:1261
    old "Making the [variant] update zsync file."
    new "Création du fichier de mise à jour zsync [variant]."

    # distribute.rpy:1404
    old "Processed {b}[complete]{/b} of {b}[total]{/b} files."
    new "Traitement du fichier {b}[complete]{/b} sur {b}[total]{/b}."

    # distribute_gui.rpy:157
    old "Build Distributions: [project.current.name!q]"
    new "Construction des paquets : [project.current.name!q]"

    # distribute_gui.rpy:171
    old "Directory Name:"
    new "Nom du répertoire :"

    # distribute_gui.rpy:175
    old "Executable Name:"
    new "Nom de l’exécutable :"

    # distribute_gui.rpy:185
    old "Actions:"
    new "Actions :"

    # distribute_gui.rpy:193
    old "Edit options.rpy"
    new "Éditer options.rpy"

    # distribute_gui.rpy:194
    old "Add from clauses to calls, once"
    new "Ajouter des \"from\" aux \"call\""

    # distribute_gui.rpy:195
    old "Refresh"
    new "Rafraichir"

    # distribute_gui.rpy:199
    old "Upload to itch.io"
    new "Uploader sur itch.io"

    # distribute_gui.rpy:215
    old "Build Packages:"
    new "Compiler les paquets :"

    # distribute_gui.rpy:234
    old "Options:"
    new "Options :"

    # distribute_gui.rpy:239
    old "Build Updates"
    new "Compiler les mises à jour"

    # distribute_gui.rpy:241
    old "Add from clauses to calls"
    new "Ajouter des \"from\" aux \"call\""

    # distribute_gui.rpy:242
    old "Force Recompile"
    new "Forcer la recompilation"

    # distribute_gui.rpy:246
    old "Build"
    new "Compiler"

    # distribute_gui.rpy:250
    old "Adding from clauses to call statements that do not have them."
    new "Ajout de \"from\" aux \"call\" qui n'en ont pas."

    # distribute_gui.rpy:271
    old "Errors were detected when running the project. Please ensure the project runs without errors before building distributions."
    new "Des erreurs ont été détectées lors de l’exécution du projet. Assurez-vous qu’il n'y ait plus d’erreurs avant de compiler les paquets."

    # distribute_gui.rpy:288
    old "Your project does not contain build information. Would you like to add build information to the end of options.rpy?"
    new "Votre projet ne contient pas d’informations de compilation. Voulez-vous ajouter ces informations à la fin du fichier options.rpy ?"

    # editor.rpy:150
    old "{b}Recommended.{/b} A beta editor with an easy to use interface and features that aid in development, such as spell-checking. Editra currently lacks the IME support required for Chinese, Japanese, and Korean text input."
    new "{b}Recommandé.{/b} Un éditeur en version beta avec une interface simple et des fonctionnalités d’assistance au développement. Editra manque pour le moment du support pour les textes en chinois, japonais et coréen."

    # editor.rpy:151
    old "{b}Recommended.{/b} A beta editor with an easy to use interface and features that aid in development, such as spell-checking. Editra currently lacks the IME support required for Chinese, Japanese, and Korean text input. On Linux, Editra requires wxPython."
    new "{b}Recommandé.{/b} Un éditeur en version beta avec une interface simple et des fonctionnalités d’assistance au développement. Editra manque pour le moment du support pour les textes en chinois, japonais et coréen. Sur GNU-Linux, Editra nécessite wxPython."

    # editor.rpy:167
    old "This may have occured because wxPython is not installed on this system."
    new "Cela est sans doute dû au fait que wxPython n’est pas installé sur votre système."

    # editor.rpy:169
    old "Up to 22 MB download required."
    new "Jusqu’à 22 Mo de téléchargement requis."

    # editor.rpy:182
    old "A mature editor that requires Java."
    new "Un éditeur éprouvé nécessitant Java."

    # editor.rpy:182
    old "1.8 MB download required."
    new "1.8 Mo de téléchargement requis."

    # editor.rpy:182
    old "This may have occured because Java is not installed on this system."
    new "Cela est sans doute produit parce que Java n’est pas installé sur ce système."

    # editor.rpy:191
    old "Invokes the editor your operating system has associated with .rpy files."
    new "Lance l’éditeur associé par défaut aux fichiers d’extension .rpy."

    # editor.rpy:207
    old "Prevents Ren'Py from opening a text editor."
    new "Empêcher Ren’Py d’ouvrir un éditeur de texte."

    # editor.rpy:359
    old "An exception occured while launching the text editor:\n[exception!q]"
    new "Une exception est survenue lors du lancement de l’éditeur de texte :\n[exception!q]"

    # editor.rpy:457
    old "Select Editor"
    new "Sélectionnez un éditeur"

    # editor.rpy:472
    old "A text editor is the program you'll use to edit Ren'Py script files. Here, you can select the editor Ren'Py will use. If not already present, the editor will be automatically downloaded and installed."
    new "Un éditeur de texte est un logiciel que vous utilisez pour éditer les fichiers de script Ren’Py. Vous pouvez choisir l’éditeur que Ren’Py utilise. S’il n’est pas déjà installé, l’éditeur sera automatiquement téléchargé et installé."

    # editor.rpy:494
    old "Cancel"
    new "Annuler"

    # front_page.rpy:35
    old "Open [text] directory."
    new "Ouvrir le répertoire [text]."

    # front_page.rpy:93
    old "refresh"
    new "rafraîchir"

    # front_page.rpy:120
    old "+ Create New Project"
    new "+ Créer un nouveau projet"

    # front_page.rpy:130
    old "Launch Project"
    new "Lancer le projet"

    # front_page.rpy:147
    old "[p.name!q] (template)"
    new "[p.name!q] (gabarit)"

    # front_page.rpy:149
    old "Select project [text]."
    new "Selectionner le projet [text]."

    # front_page.rpy:165
    old "Tutorial"
    new "Tutoriel"

    # front_page.rpy:166
    old "The Question"
    new "La Question"

    # front_page.rpy:182
    old "Active Project"
    new "Projet actif"

    # front_page.rpy:190
    old "Open Directory"
    new "Ouvrir le répertoire"

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
    new "Éditer le fichier"

    # front_page.rpy:214
    old "All script files"
    new "Tous les fichiers de script"

    # front_page.rpy:223
    old "Navigate Script"
    new "Parcourir le script"

    # front_page.rpy:234
    old "Check Script (Lint)"
    new "Vérifier le script (Lint)"

    # front_page.rpy:237
    old "Change/Update GUI"
    new "Mettre à jour l’interface GUI"

    # front_page.rpy:239
    old "Change Theme"
    new "Changer de thème"

    # front_page.rpy:242
    old "Delete Persistent"
    new "Supprimer les données persistantes"

    # front_page.rpy:251
    old "Build Distributions"
    new "Compiler les paquets"

    # front_page.rpy:253
    old "Android"
    new "Android"

    # front_page.rpy:254
    old "iOS"
    new "iOS"

    # front_page.rpy:255
    old "Generate Translations"
    new "Générer les fichiers de traduction"

    # front_page.rpy:256
    old "Extract Dialogue"
    new "Extraire les dialogues"

    # front_page.rpy:272
    old "Checking script for potential problems..."
    new "Vérifier le script vis-à-vis des problèmes potentiels..."

    # front_page.rpy:287
    old "Deleting persistent data..."
    new "Suppression des données persistantes en cours..."

    # front_page.rpy:295
    old "Recompiling all rpy files into rpyc files..."
    new "Recompiler tous les fichiers rpy files en rpyc..."

    # gui7.rpy:236
    old "Select Accent and Background Colors"
    new "Sélectionner les couleurs des surbrillances et des arrière-plans"

    # gui7.rpy:250
    old "Please click on the color scheme you wish to use, then click Continue. These colors can be changed and customized later."
    new "Veuillez cliquer sur le schéma de couleur que vous souhaitez utiliser. Ensuite, cliquez sur « continuer ». Les couleurs pourront être personnalisées et modifiées plus tard."

    # gui7.rpy:294
    old "{b}Warning{/b}\nContinuing will overwrite customized bar, button, save slot, scrollbar, and slider images.\n\nWhat would you like to do?"
    new "{b}Attention{/b}\nSi vous continuez, vous allez écraser la personnalisation des barres, des boutons, des emplacements de sauvegarde, des ascenseurs et des curseurs.\n\nQue souhaitez-vous faire ?"

    # gui7.rpy:294
    old "Choose new colors, then regenerate image files."
    new "Choisissez les nouvelles couleurs, ensuite régénérez les fichiers d’images."

    # gui7.rpy:294
    old "Regenerate the image files using the colors in gui.rpy."
    new "Régénérer les images en utilisant les couleurs dans gui.rpy."

    # gui7.rpy:314
    old "PROJECT NAME"
    new "NOM DU PROJET"

    # gui7.rpy:314
    old "Please enter the name of your project:"
    new "Entrez le nom de votre projet :"

    # gui7.rpy:322
    old "The project name may not be empty."
    new "Le nom du projet ne doit pas être vide."

    # gui7.rpy:327
    old "[project_name!q] already exists. Please choose a different project name."
    new "Le projet [project_name!q] existe déjà. Choisissez un nom de projet différent."

    # gui7.rpy:330
    old "[project_dir!q] already exists. Please choose a different project name."
    new "Le projet [project_name!q] existe déjà. Choisissez un nom de projet différent."

    # gui7.rpy:341
    old "What resolution should the project use? Although Ren'Py can scale the window up and down, this is the initial size of the window, the size at which assets should be drawn, and the size at which the assets will be at their sharpest.\n\nThe default of [default_size[0]]x[default_size[1]] is a reasonable compromise."
    new "Quelle résolution souhaitez-vous utiliser pour votre projet ? Même si Ren’Py peut agrandir ou diminuer les fenêtres et leurs images à l’échelle, il s’agit là de l’échelle initiale, la taille à laquelle les composants doivent être dessinés et la taille de fenêtre pour lesquelles ils seront le plus précis.\n\nThe La valeur par défaut ([default_size[0]]x[default_size[1]]) semble être un compromis raisonnable."

    # gui7.rpy:389
    old "Creating the new project..."
    new "Création en cours du nouveau projet..."

    # gui7.rpy:391
    old "Updating the project..."
    new "Mise à jour en cours du projet..."

    # interface.rpy:107
    old "Documentation"
    new "Documentation"

    # interface.rpy:108
    old "Ren'Py Website"
    new "Site Web de Ren’Py"

    # interface.rpy:109
    old "Ren'Py Games List"
    new "Liste des jeux Ren’Py"

    # interface.rpy:117
    old "update"
    new "mise à jour"

    # interface.rpy:119
    old "preferences"
    new "préférences"

    # interface.rpy:120
    old "quit"
    new "quitter"

    # interface.rpy:232
    old "Due to package format limitations, non-ASCII file and directory names are not allowed."
    new "Les caractères non-ASCII ne sont pas autorisés pour les noms de fichiers et les répertoires."

    # interface.rpy:327
    old "ERROR"
    new "ERREUR"

    # interface.rpy:356
    old "While [what!qt], an error occured:"
    new "Pendant que [what!qt], une erreur est survenue :"

    # interface.rpy:356
    old "[exception!q]"
    new "[exception!q]"

    # interface.rpy:375
    old "Text input may not contain the {{ or [[ characters."
    new "Le texte ne doit pas contenir les caractères {{ ou [[."

    # interface.rpy:380
    old "File and directory names may not contain / or \\."
    new "Les noms de fichiers et répertoires ne doivent pas contenir / ou \\."

    # interface.rpy:386
    old "File and directory names must consist of ASCII characters."
    new "Les noms de fichiers et de répertoires doivent contenir uniquement des caractères ASCII."

    # interface.rpy:454
    old "PROCESSING"
    new "TRAITEMENT"

    # interface.rpy:471
    old "QUESTION"
    new "QUESTION"

    # interface.rpy:484
    old "CHOICE"
    new "CHOIX"

    # ios.rpy:28
    old "To build iOS packages, please download renios, unzip it, and place it into the Ren'Py directory. Then restart the Ren'Py launcher."
    new "Pour compiler un paquet iOS, veuillez télécharger renios, le décompresser et le placer dans le répertoire de Ren’Py. Ensuite redémarrer le lanceur Ren’Py."

    # ios.rpy:29
    old "The directory in where Xcode projects will be placed has not been selected. Choose 'Select Directory' to select it."
    new "Le répertoire dans lequel les projets Xcode vont être placés n'a pas été sélectionné. Veuillez choisir « Sélectionner un répertoire » pour le renseigner."

    # ios.rpy:30
    old "There is no Xcode project corresponding to the current Ren'Py project. Choose 'Create Xcode Project' to create one."
    new "Il n’y a pas de projet Xcode correspondant au projet Ren’Py actuel. Veuillez choisir « Créer un projet Xcode » pour en créer un."

    # ios.rpy:31
    old "An Xcode project exists. Choose 'Update Xcode Project' to update it with the latest game files, or use Xcode to build and install it."
    new "Un projet Xcode existe. Choisissez « Mettre à jour le Projet XCode » pour le mettre à jour avec les dernier fichier du jeu ou utilisez Xcode pour le compiler et l'installer."

    # ios.rpy:33
    old "Attempts to emulate an iPhone.\n\nTouch input is emulated through the mouse, but only when the button is held down."
    new "Tentative d'émuler un iPhone.\n\nLe contact tactile est émulé via la souris, mais seulement si le bouton est maintenu pressé."

    # ios.rpy:34
    old "Attempts to emulate an iPad.\n\nTouch input is emulated through the mouse, but only when the button is held down."
    new "Tentative d'émuler un iPad.\n\nLe contact tactile est émulé via la souris, mais seulement si le bouton est maintenu pressé."

    # ios.rpy:36
    old "Selects the directory where Xcode projects will be placed."
    new "Sélectionnez le répertoire où les projets Xcode doivent être placés."

    # ios.rpy:37
    old "Creates an Xcode project corresponding to the current Ren'Py project."
    new "Créez un projet Xcode correspondant à projet Ren’Py actuel."

    # ios.rpy:38
    old "Updates the Xcode project with the latest game files. This must be done each time the Ren'Py project changes."
    new "Mettez à jour le projet Xcode avec les derniers fichiers de jeu. Cela doit être fait chaque fois que le projet Ren’Py est modifié."

    # ios.rpy:39
    old "Opens the Xcode project in Xcode."
    new "Ouvrez le projet Xcode dans Xcode."

    # ios.rpy:41
    old "Opens the directory containing Xcode projects."
    new "Ouvrez le répertoire contenant les projets Xcode."

    # ios.rpy:126
    old "The Xcode project already exists. Would you like to rename the old project, and replace it with a new one?"
    new "Le projet Xcode existe déjà. Voulez-vous renommer l’ancien projet et le remplacer par un nouveau ?"

    # ios.rpy:211
    old "iOS: [project.current.name!q]"
    new "iOS : [project.current.name!q]"

    # ios.rpy:240
    old "iPhone"
    new "iPhone"

    # ios.rpy:244
    old "iPad"
    new "iPad"

    # ios.rpy:264
    old "Select Xcode Projects Directory"
    new "Sélectionner le répertoire de projet Xcode"

    # ios.rpy:268
    old "Create Xcode Project"
    new "Créer le projet Xcode"

    # ios.rpy:272
    old "Update Xcode Project"
    new "Mettre à jour le projet Xcode"

    # ios.rpy:277
    old "Launch Xcode"
    new "Exécuter Xcode"

    # ios.rpy:312
    old "Open Xcode Projects Directory"
    new "Ouvrir le répertoire de projet Xcode"

    # ios.rpy:345
    old "Before packaging iOS apps, you'll need to download renios, Ren'Py's iOS support. Would you like to download renios now?"
    new "Avant de paquager les applications iOS, vous devez télécharger renios, le support iOS pour Ren'Py. Voulez-vous télécharger renios maintenant ?"

    # ios.rpy:354
    old "XCODE PROJECTS DIRECTORY"
    new "REPERTOIRE DES PROJETS XCODE"

    # ios.rpy:354
    old "Please choose the Xcode Projects Directory using the directory chooser.\n{b}The directory chooser may have opened behind this window.{/b}"
    new "Veuillez choisir le répertoire de projets Xcode en utilisant le sélectionneur de répertoire.\n{b}Le sélectionneur de répertoire s’est peut-être ouvert en arrière-plan de cette fenêtre.{/b}"

    # ios.rpy:359
    old "Ren'Py has set the Xcode Projects Directory to:"
    new "Ren’Py a configuré comme répertoire de projet Xcode le répertoire :"

    # itch.rpy:60
    old "The built distributions could not be found. Please choose 'Build' and try again."
    new "Le compileur de distribution n'a pas été trouvé. Veuillez choisir « Compiler » et réessayez."

    # itch.rpy:91
    old "No uploadable files were found. Please choose 'Build' and try again."
    new "Aucun fichier à télécharger(upload) n'a été trouvé. Veuillez choisir « Compiler » et réessayer."

    # itch.rpy:99
    old "The butler program was not found."
    new "Le programme butler n'a pas été trouvé."

    # itch.rpy:99
    old "Please install the itch.io app, which includes butler, and try again."
    new "Veuillez installer l’application itch.io qui inclut le coordonnateur et réessayer."

    # itch.rpy:108
    old "The name of the itch project has not been set."
    new "Le nom du projet itch n'a pas été configuré."

    # itch.rpy:108
    old "Please {a=https://itch.io/game/new}create your project{/a}, then add a line like \n{vspace=5}define build.itch_project = \"user-name/game-name\"\n{vspace=5} to options.rpy."
    new "Veuillez {a=https://itch.io/game/new}créer votre projet{/a}, ensuite ajouter une ligne comme \n{vspace=5}define build.itch_project = \"user-name/game-name\"\n{vspace=5} dans le fichier options.rpy."

    # mobilebuild.rpy:109
    old "{a=%s}%s{/a}"
    new "{a=%s}%s{/a}"

    # navigation.rpy:168
    old "Navigate: [project.current.name]"
    new "Navigation : [project.current.name]"

    # navigation.rpy:177
    old "Order: "
    new "Ordre :"

    # navigation.rpy:178
    old "alphabetical"
    new "alphabétique"

    # navigation.rpy:180
    old "by-file"
    new "par fichier"

    # navigation.rpy:182
    old "natural"
    new "naturel"

    # navigation.rpy:194
    old "Category:"
    new "Catégorie :"

    # navigation.rpy:196
    old "files"
    new "fichiers"

    # navigation.rpy:197
    old "labels"
    new "labels"

    # navigation.rpy:198
    old "defines"
    new "définitions"

    # navigation.rpy:199
    old "transforms"
    new "transformations"

    # navigation.rpy:200
    old "screens"
    new "écrans"

    # navigation.rpy:201
    old "callables"
    new "appelables"

    # navigation.rpy:202
    old "TODOs"
    new "TODOs"

    # navigation.rpy:241
    old "+ Add script file"
    new "+ Ajouter un fichier de script"

    # navigation.rpy:249
    old "No TODO comments found.\n\nTo create one, include \"# TODO\" in your script."
    new "Aucun commentaire « TODO » trouvé.\n\nPour en créer un, écrivez \"# TODO\" dans le script."

    # navigation.rpy:256
    old "The list of names is empty."
    new "La liste des noms est vide."

    # new_project.rpy:38
    old "New GUI Interface"
    new "Nouvelle interface GUI"

    # new_project.rpy:48
    old "Both interfaces have been translated to your language."
    new "Les deux interfaces ont été traduites dans votre langue."

    # new_project.rpy:50
    old "Only the new GUI has been translated to your language."
    new "Seule la nouvelle GUI a été traduite dans votre langue."

    # new_project.rpy:52
    old "Only the legacy theme interface has been translated to your language."
    new "Seule l'interface de thème initiale a été traduite dans votre langue."

    # new_project.rpy:54
    old "Neither interface has been translated to your language."
    new "Aucune interface n’a été traduite dans votre langue."

    # new_project.rpy:63
    old "The projects directory could not be set. Giving up."
    new "Le répertoire de projet ne peut pas être initialisé. Abandon."

    # new_project.rpy:69
    old "Which interface would you like to use? The new GUI has a modern look, supports wide screens and mobile devices, and is easier to customize. Legacy themes might be necessary to work with older example code.\n\n[language_support!t]\n\nIf in doubt, choose the new GUI, then click Continue on the bottom-right."
    new "Quelle interface souhaitez-vous utiliser ? La nouvelle interface possède un look moderne et supporte les écrans larges ainsi que les appareils mobiles. De plus, elle est simple à personnaliser. Les thèmes hérités peuvent être nécessaires pour fonctionner avec d'anciens codes.\n\n[language_support!t]\n\nEn cas de doute, choisissez la nouvelle interface GUI, ensuite cliquez sur « Continuer » en bas à droite."

    # new_project.rpy:69
    old "Legacy Theme Interface"
    new "Interface des thèmes originale"

    # new_project.rpy:90
    old "Choose Project Template"
    new "Choisissez un modèle de projet"

    # new_project.rpy:108
    old "Please select a template to use for your new project. The template sets the default font and the user interface language. If your language is not supported, choose 'english'."
    new "Sélectionnez un modèle pour votre nouveau projet. Le modèle définit la police par défaut, ainsi que la langue de l'interface. Si votre langue n'est pas supportée, sélectionnez 'english'."

    # preferences.rpy:64
    old "Launcher Preferences"
    new "Préférence du lanceur"

    # preferences.rpy:85
    old "Projects Directory:"
    new "Répertoire des projets :"

    # preferences.rpy:92
    old "[persistent.projects_directory!q]"
    new "[persistent.projects_directory!q]"

    # preferences.rpy:94
    old "Projects directory: [text]"
    new "Répertoire des projets : [text]"

    # preferences.rpy:96
    old "Not Set"
    new "Non configuré"

    # preferences.rpy:111
    old "Text Editor:"
    new "Éditeur de texte :"

    # preferences.rpy:117
    old "Text editor: [text]"
    new "Éditeur de texte : [text]"

    # preferences.rpy:133
    old "Update Channel:"
    new "Type de version :"

    # preferences.rpy:153
    old "Navigation Options:"
    new "Options de navigation :"

    # preferences.rpy:157
    old "Include private names"
    new "Inclure les noms privés"

    # preferences.rpy:158
    old "Include library names"
    new "Inclure les noms des bibliothèques"

    # preferences.rpy:168
    old "Launcher Options:"
    new "Options du lanceur :"

    # preferences.rpy:172
    old "Hardware rendering"
    new "Rendu matériel"

    # preferences.rpy:173
    old "Show templates"
    new "Afficher les modèles"

    # preferences.rpy:174
    old "Show edit file section"
    new "Afficher la section d’édition de fichiers"

    # preferences.rpy:175
    old "Large fonts"
    new "Grandes polices"

    # preferences.rpy:178
    old "Console output"
    new "Console de sortie"

    # preferences.rpy:199
    old "Open launcher project"
    new "Ouvrir le projet du lanceur"

    # preferences.rpy:213
    old "Language:"
    new "Langue :"

    # project.rpy:47
    old "After making changes to the script, press shift+R to reload your game."
    new "Après avoir effectué des changements dans le script, pressez « Maj+R » pour recharger le jeu."

    # project.rpy:47
    old "Press shift+O (the letter) to access the console."
    new "Pressez « Maj+O » (la lettre O) pour accéder à la console."

    # project.rpy:47
    old "Press shift+D to access the developer menu."
    new "Pressez « Maj+D » pour accéder au menu du développeur."

    # project.rpy:47
    old "Have you backed up your projects recently?"
    new "Avez-vous sauvegardé vos projets récemment ?"

    # project.rpy:229
    old "Launching the project failed."
    new "L’exécution du projet a échoué."

    # project.rpy:229
    old "Please ensure that your project launches normally before running this command."
    new "Veuillez vous assurer que votre projet s’exécute normalement avant d’exécuter cette commande."

    # project.rpy:242
    old "Ren'Py is scanning the project..."
    new "Ren’Py est en train de parcourir le projet..."

    # project.rpy:568
    old "Launching"
    new "Exécution en cours"

    # project.rpy:597
    old "PROJECTS DIRECTORY"
    new "RÉPERTOIRE DES PROJETS"

    # project.rpy:597
    old "Please choose the projects directory using the directory chooser.\n{b}The directory chooser may have opened behind this window.{/b}"
    new "Choisissez le répertoire de projets avec le sélectionneur de fichier.\n{b}Il se peut que le sélectionneur de fichier s’ouvre derrière cette fenêtre.{/b}"

    # project.rpy:597
    old "This launcher will scan for projects in this directory, will create new projects in this directory, and will place built projects into this directory."
    new "Ce lanceur va parcourir ce répertoire pour trouver les projets existants, il créera les nouveaux projets dans ce répertoire et placera les projets compilés dans ce répertoire."

    # project.rpy:602
    old "Ren'Py has set the projects directory to:"
    new "Le répertoire des projets vient d’être configuré à l’emplacement :"

    # translations.rpy:63
    old "Translations: [project.current.name!q]"
    new "Traductions : [project.current.name!q]"

    # translations.rpy:104
    old "The language to work with. This should only contain lower-case ASCII characters and underscores."
    new "Le langage avec lequel travailler. Cette valeur ne doit contenir que des caractères ASCII en minuscules et des underscores."

    # translations.rpy:130
    old "Generate empty strings for translations"
    new "Génère des chaînes de caractères vides pour les traductions"

    # translations.rpy:148
    old "Generates or updates translation files. The files will be placed in game/tl/[persistent.translate_language!q]."
    new "Génère ou met à jour les fichiers de traduction. Les fichiers seront placés dans le jeu/tl/[persistent.translate_language!q]."

    # translations.rpy:168
    old "Extract String Translations"
    new "Extrait les traductions"

    # translations.rpy:170
    old "Merge String Translations"
    new "Fusionne les traductions"

    # translations.rpy:175
    old "Replace existing translations"
    new "Remplace les traductions existantes"

    # translations.rpy:176
    old "Reverse languages"
    new "Inverse les langages"

    # translations.rpy:180
    old "Update Default Interface Translations"
    new "Mise à jour de la traduction par défaut de l'interface"

    # translations.rpy:200
    old "The extract command allows you to extract string translations from an existing project into a temporary file.\n\nThe merge command merges extracted translations into another project."
    new "La commande d'extraction vous permet d'extraire les traductions depuis un projet existant vers un fichier temporaire.\n\nLa commande de fusion fusionne les traductions dans un autre projet."

    # translations.rpy:224
    old "Ren'Py is generating translations...."
    new "Ren’Py est en train de générer les traductions..."

    # translations.rpy:235
    old "Ren'Py has finished generating [language] translations."
    new "Ren’Py a fini de générer les fichiers de traductions pour [language]."

    # translations.rpy:248
    old "Ren'Py is extracting string translations..."
    new "Ren’Py est en train d'extraire les traductions..."

    # translations.rpy:251
    old "Ren'Py has finished extracting [language] string translations."
    new "Ren’Py a fini l’extraction des traductions de la langue [language]."

    # translations.rpy:271
    old "Ren'Py is merging string translations..."
    new "Ren’Py est en train de fusionner les traductions..."

    # translations.rpy:274
    old "Ren'Py has finished merging [language] string translations."
    new "Ren’Py a fini de fusionner les traductions de la langue [language]."

    # translations.rpy:282
    old "Updating default interface translations..."
    new "Mise à jour de la traduction par défaut de l’interface en cours..."

    # translations.rpy:306
    old "Extract Dialogue: [project.current.name!q]"
    new "Extraire les dialogues : [project.current.name!q]"

    # translations.rpy:322
    old "Format:"
    new "Format :"

    # translations.rpy:330
    old "Tab-delimited Spreadsheet (dialogue.tab)"
    new "Feuille de calcul avec des tabulations comme séparateur (dialogue.tab)"

    # translations.rpy:331
    old "Dialogue Text Only (dialogue.txt)"
    new "Texte des dialogues uniquement (dialogue.txt)"

    # translations.rpy:344
    old "Strip text tags from the dialogue."
    new "Retire les text tags (balises) des dialogues."

    # translations.rpy:345
    old "Escape quotes and other special characters."
    new "Protège (échappe) les apostrophes et les autres caractères spéciaux."

    # translations.rpy:346
    old "Extract all translatable strings, not just dialogue."
    new "Extrait les chaînes traduisibles, pas seulement les dialogues."

    # translations.rpy:374
    old "Ren'Py is extracting dialogue...."
    new "Ren’Py est en train d’extraire les dialogues...."

    # translations.rpy:378
    old "Ren'Py has finished extracting dialogue. The extracted dialogue can be found in dialogue.[persistent.dialogue_format] in the base directory."
    new "Ren’Py a fini d’extraire les dialogues. Les dialogues extraits peuvent-être trouvés dans dialogue.[persistent.dialogue_format] dans le répertoire de base."

    # updater.rpy:75
    old "Select Update Channel"
    new "Choisissez une version."

    # updater.rpy:86
    old "The update channel controls the version of Ren'Py the updater will download. Please select an update channel:"
    new "Le canal de mise à jour détermine la version de Ren’Py qui sera téléchargée. Sélectionnez un canal de mise à jour :"

    # updater.rpy:91
    old "Release"
    new "Stable"

    # game/updater.rpy:64
    old "Release (Ren'Py 8, Python 3)"
    new "Stable (Ren'Py 8, Python 3)"

    # game/updater.rpy:65
    old "Release (Ren'Py 7, Python 2)"
    new "Stable (Ren'Py 7, Python 2)"

    # updater.rpy:97
    old "{b}Recommended.{/b} The version of Ren'Py that should be used in all newly-released games."
    new "{b}Recommandé.{/b} La version de Ren’Py qui devrait être utilisée pour tous les jeux récemment sortis."

    # updater.rpy:102
    old "Prerelease"
    new "Pré-stable"

    # game/updater.rpy:69
    old "Prerelease (Ren'Py 8, Python 3)"
    new "Pré-stable (Ren'Py 8, Python 3)"

    # game/updater.rpy:70
    old "Prerelease (Ren'Py 7, Python 2)"
    new "Pré-stable (Ren'Py 7, Python 2)"

    # updater.rpy:108
    old "A preview of the next version of Ren'Py that can be used for testing and taking advantage of new features, but not for final releases of games."
    new "Un aperçu de la prochaine version de Ren’Py qui peut être utilisée pour faire des tests et profiter de toutes nouvelles fonctionnalités, mais pas pour créer de nouveaux jeux."

    # updater.rpy:114
    old "Experimental"
    new "Expérimental"

    # updater.rpy:120
    old "Experimental versions of Ren'Py. You shouldn't select this channel unless asked by a Ren'Py developer."
    new "Version expérimentale de Ren’Py. Vous ne devriez pas choisir cette version, à moins qu’un développeur de Ren’Py ne vous y invite."

    # updater.rpy:126
    old "Nightly"
    new "Journalière"

    # game/updater.rpy:77
    old "Nightly (Ren'Py 8, Python 3)"
    new "Journalière (Ren'Py 8, Python 3)"

    # game/updater.rpy:78
    old "Nightly (Ren'Py 7, Python 2)"
    new "Journalière (Ren'Py 7, Python 2)"

    # updater.rpy:132
    old "The bleeding edge of Ren'Py development. This may have the latest features, or might not run at all."
    new "La toute dernière version de Ren’Py, encore en développement. Elle peut contenir les toutes dernières fonctionnalités, ou alors ne pas marcher du tout."

    # game/updater.rpy:76
    old "Nightly Fix"
    new "Journalière Corrective"

    # game/updater.rpy:77
    old "Nightly Fix (Ren'Py 8, Python 3)"
    new "Journalière Corrective (Ren'Py 8, Python 3)"

    # game/updater.rpy:78
    old "Nightly Fix (Ren'Py 7, Python 2)"
    new "Journalière Corrective (Ren'Py 7, Python 2)"

    # game/updater.rpy:79
    old "A nightly build of fixes to the release version of Ren'Py."
    new "Une version journalière qui corrige les bugs de la dernière version stable."

    # updater.rpy:152
    old "An error has occured:"
    new "Une erreur est survenue :"

    # updater.rpy:154
    old "Checking for updates."
    new "Vérification des mises à jour."

    # updater.rpy:156
    old "Ren'Py is up to date."
    new "Ren’Py est à jour."

    # updater.rpy:158
    old "[u.version] is now available. Do you want to install it?"
    new "La version [u.version] est disponible. Voulez-vous l’installer ?"

    # updater.rpy:160
    old "Preparing to download the update."
    new "Préparation du téléchargement de la mise à jour."

    # updater.rpy:162
    old "Downloading the update."
    new "Téléchargement de la mise à jour en cours."

    # updater.rpy:164
    old "Unpacking the update."
    new "Décompression de la mise à jour en cours."

    # updater.rpy:166
    old "Finishing up."
    new "Finalisation en cours."

    # updater.rpy:168
    old "The update has been installed. Ren'Py will restart."
    new "La mise à jour a bien été effectuée. Ren'Py va redémarrer."

    # updater.rpy:170
    old "The update has been installed."
    new "La mise à jour a bien été effectuée."

    # updater.rpy:172
    old "The update was cancelled."
    new "La mise à jour a été annulée."

    # updater.rpy:189
    old "Ren'Py Update"
    new "Mise à jour de Ren’Py"

    # updater.rpy:195
    old "Proceed"
    new "Continuer"

    # game/add_file.rpy:37
    old "The file name may not be empty."
    new "Le nom de fichier ne peut pas être vide."

    # game/android.rpy:31
    old "A 64-bit/x64 Java [JDK_REQUIREMENT] Development Kit is required to build Android packages on Windows. The JDK is different from the JRE, so it's possible you have Java without having the JDK.\n\nPlease {a=https://www.renpy.org/jdk/[JDK_REQUIREMENT]}download and install the JDK{/a}, then restart the Ren'Py launcher."
    new "Un kit de développement Java [JDK_REQUIREMENT] 64-bit/x64 est requis pour construire des paquets Android depuis Windows. Le JDK est différent du JRE, donc il est possible d'avoir Java sans avoir le JDK.\n\n{a=https://www.renpy.org/jdk/[JDK_REQUIREMENT]}Téléchargez et installez le JDK{/a}, puis redémarrez Ren'Py."

    # game/android.rpy:50
    old "Selects the Debug build, which can be accessed through Android Studio. Changing between debug and release builds requires an uninstall from your device."
    new "Selectionne le build de Debug, qui peut être atteint depuis Android Studio. Passer d'un build debug à un build stable nécessitera une désinstallation sur votre appareil."

    # game/android.rpy:51
    old "Selects the Release build, which can be uploaded to stores. Changing between debug and release builds requires an uninstall from your device."
    new "Sélectionne le build Stable, qui peut être posté sur des magasins d'applications. Passer d'un build debug à un build stable nécessitera une désinstallation sur votre appareil."

    # game/android.rpy:313
    old "Android: [project.current.display_name!q]"
    new "Android : [project.current.display_name!q]"

    # game/androidstrings.rpy:7
    old "{} is not a directory."
    new "{} n'est pas un répertoire."

    # game/androidstrings.rpy:8
    old "{} does not contain a Ren'Py game."
    new "{} ne contient pas un jeu Ren'Py."

    # game/androidstrings.rpy:9
    old "Run configure before attempting to build the app."
    new "Lancez la configuration avant d'essayer de construire l'app."

    # game/androidstrings.rpy:10
    old "Google Play support is enabled, but build.google_play_key is not defined."
    new "Le support Google Play est activé, mais build.google_play_key n'est pas défini."

    # game/androidstrings.rpy:11
    old "Updating project."
    new "Mise à jour du projet."

    # game/androidstrings.rpy:12
    old "Creating assets directory."
    new "Création du répertoire d'assets."

    # game/androidstrings.rpy:13
    old "Creating expansion file."
    new "Création du fihier d'expansion."

    # game/androidstrings.rpy:14
    old "Packaging internal data."
    new "Paquetage des données internes."

    # game/androidstrings.rpy:15
    old "I'm using Gradle to build the package."
    new "J'utilise Gradle pour construire le package."

    # game/androidstrings.rpy:16
    old "Uploading expansion file."
    new "Téléversement du fichier d'expansion."

    # game/androidstrings.rpy:17
    old "The build seems to have failed."
    new "Le build semble avoir échoué."

    # game/androidstrings.rpy:18
    old "Launching app."
    new "Lancement de l'app."

    # game/androidstrings.rpy:19
    old "The build seems to have succeeded."
    new "Le build semble avoir réussi."

    # game/androidstrings.rpy:20
    old "The arm64-v8a version works on newer Android devices, the armeabi-v7a version works on older devices, and the x86_64 version works on the simulator and chromebooks."
    new "La version arm64-v8a fonctionne sur les appareils Android les plus récents, la version armeabi-v7a fonctionne sur les plus anciens, et la version x86_64 version fonctionne sur les simulateurs et chromebooks."

    # game/androidstrings.rpy:21
    old "The universal version works everywhere but is larger."
    new "La version universelle fonctionne partout mais pèse plus lourd."

    # game/androidstrings.rpy:22
    old "What is the full name of your application? This name will appear in the list of installed applications."
    new "quel est le nom complet de votre application ? Ce nom apparaîtra dans la liste des applications installées."

    # game/androidstrings.rpy:23
    old "What is the short name of your application? This name will be used in the launcher, and for application shortcuts."
    new "Quel est le nom court de votre application ? Ce nom sera utilisé dans le launcher, et pour les raccourcis d'application."

    # game/androidstrings.rpy:24
    old "What is the name of the package?\n\nThis is usually of the form com.domain.program or com.domain.email.program. It may only contain ASCII letters and dots. It must contain at least one dot."
    new "Quel est le nom du package ?\n\nIl est généralement de la forme com.domain.program ou com.domain.email.program. Il doit uniquement contenir des lettres ASCII et des points. Il doit contenir au moins un point."

    # game/androidstrings.rpy:25
    old "The package name may not be empty."
    new "Le nom du package ne peut pas être vide."

    # game/androidstrings.rpy:26
    old "The package name may not contain spaces."
    new "Le nom de package ne peut pas contenir d'espaces."

    # game/androidstrings.rpy:27
    old "The package name must contain at least one dot."
    new "Le nom du package doit contenir au moins un point."

    # game/androidstrings.rpy:28
    old "The package name may not contain two dots in a row, or begin or end with a dot."
    new "Le nom du package ne peut pas contenir deux points de suite, ni commencer ni finir par un point."

    # game/androidstrings.rpy:29
    old "Each part of the package name must start with a letter, and contain only letters, numbers, and underscores."
    new "Chaque partie du nom de package doit commencer par une lettre, et ne contenir que des lettres, chiffres, et tirets de soulignement."

    # game/androidstrings.rpy:30
    old "{} is a Java keyword, and can't be used as part of a package name."
    new "{} est un mot-clé Java, et ne peut pas faire partie d'un nom de package."

    # game/androidstrings.rpy:31
    old "What is the application's version?\n\nThis should be the human-readable version that you would present to a person. It must contain only numbers and dots."
    new "Quelle est la version de l'application ?\n\nCe devrait être la version lisible par un humain que vous présentez à une personne. Il doit contenir uniquement des chiffres et des points."

    # game/androidstrings.rpy:32
    old "The version number must contain only numbers and dots."
    new "Le numéro de version ne peut contenir que des nombres et des points."

    # game/androidstrings.rpy:33
    old "What is the version code?\n\nThis must be a positive integer number, and the value should increase between versions."
    new "Quel est le code de version ?\n\nCe doit être un nombre entier positif, et la valeur devrait augmenter entre les versions."

    # game/androidstrings.rpy:34
    old "The numeric version must contain only numbers."
    new "Le numéro de version ne peut contenir que des chiffres."

    # game/androidstrings.rpy:35
    old "How would you like your application to be displayed?"
    new "Comment voulez-vous que l'application soit affichée ?"

    # game/androidstrings.rpy:36
    old "In landscape orientation."
    new "En orientation paysage."

    # game/androidstrings.rpy:37
    old "In portrait orientation."
    new "En orientation portrait."

    # game/androidstrings.rpy:38
    old "In the user's preferred orientation."
    new "Dans l'orientation préférée de l'utilisateur."

    # game/androidstrings.rpy:39
    old "Which app store would you like to support in-app purchasing through?"
    new "Sur quel magasin d'applications voulez-vous vous baser pour les achats dans l'application ?"

    # game/androidstrings.rpy:40
    old "Google Play."
    new "Google Play."

    # game/androidstrings.rpy:41
    old "Amazon App Store."
    new "Amazon App Store."

    # game/androidstrings.rpy:42
    old "Both, in one app."
    new "Les deux, en une seule app."

    # game/androidstrings.rpy:43
    old "Neither."
    new "Aucun."

    # game/androidstrings.rpy:44
    old "Would you like to create an expansion APK?"
    new "Voulez-vous créer un APK d'expansion ?"

    # game/androidstrings.rpy:45
    old "Automatically installing expansion APKs {a=https://issuetracker.google.com/issues/160942333}may not work on Android 11{/a}."
    new "Les APK d'expansion s'installant automatiquement {a=https://issuetracker.google.com/issues/160942333}peuvent ne pas fonctionner sur Android 11{/a}."

    # game/androidstrings.rpy:46
    old "No. Size limit of 100 MB on Google Play, but can be distributed through other stores and sideloaded."
    new "Non. Limite de taille de 100 MB sur Google Play, mais il peut être distribué sur d'autres magasins et installé directement."

    # game/androidstrings.rpy:47
    old "Yes. 2 GB size limit, but won't work outside of Google Play. (Read the documentation to get this to work.)"
    new "Oui. Limite de taille de 2 GB, mais ne marchera pas en-dehors de Google Play. (Lisez la documentation pour le faire marcher.)"

    # game/androidstrings.rpy:48
    old "Do you want to allow the app to access the Internet?"
    new "Voulez-vous autoriser l'app à accéder à Internet ?"

    # game/androidstrings.rpy:49
    old "Do you want to automatically update the Java source code?"
    new "Voulez-vous mettre à jour le code source de Java automatiquement ?"

    # game/androidstrings.rpy:50
    old "Yes. This is the best choice for most projects."
    new "Oui. C'est le meilleur choix pour la plupart des projets."

    # game/androidstrings.rpy:51
    old "No. This may require manual updates when Ren'Py or the project configuration changes."
    new "Non. Cela pourra nécessiter des mises à jour manuelles quand Ren'Py ou la configuration du projet changeront."

    # game/androidstrings.rpy:52
    old "Unknown configuration variable: {}"
    new "Variable de configuration inconnue : {}"

    # game/androidstrings.rpy:53
    old "I'm compiling a short test program, to see if you have a working JDK on your system."
    new "Je compile un petit programme de test, pour voir si un JDK fonctionnel est installé sur votre système."

    # game/androidstrings.rpy:54
    old "I was unable to use javac to compile a test file. If you haven't installed the Java Development Kit yet, please download it from:\n\nhttps://adoptopenjdk.net/?variant=openjdk8&jvmVariant=hotspot\n\nThe JDK is different from the JRE, so it's possible you have Java without having the JDK. Without a working JDK, I can't continue."
    new "L'usage de javac pour compiler un programme de test a échoué. Si vous n'avez pas encore installé le JDK, téléchargez-le :\n\nhttps://adoptopenjdk.net/?variant=openjdk8&jvmVariant=hotspot\n\nLe JDK est différent du JRE, il est donc possible que vous ayiez Java sans avoir le JDK. Sans un JDK en état de marche, je ne peux pas continuer."

    # game/androidstrings.rpy:55
    old "The version of Java on your computer does not appear to be JDK 8, which is the only version supported by the Android SDK. If you need to install JDK 8, you can download it from:\n\nhttps://adoptopenjdk.net/?variant=openjdk8&jvmVariant=hotspot\n\nYou can also set the JAVA_HOME environment variable to use a different version of Java."
    new "La version de Java sur votre ordinateur n'a pas l'air d'être JDK 8, qui est la seule version supportée par le SDK Android. Si vous avez besoin d'installer JDK 8, vous pouvez le télécharger depuis :\n\nhttps://adoptopenjdk.net/?variant=openjdk8&jvmVariant=hotspot\n\nVous pouvez aussi aussi modifier la variable d'environnement JAVA_HOME pour utiliiser une différente version de Java."

    # game/androidstrings.rpy:56
    old "The JDK is present and working. Good!"
    new "Le JDK est présent et il marche. Super !"

    # game/androidstrings.rpy:57
    old "The Android SDK has already been unpacked."
    new "Le SDK Android a été dépaqueté."

    # game/androidstrings.rpy:58
    old "Do you accept the Android SDK Terms and Conditions?"
    new "Acceptez-vous les termes et conditions du SDK Android ?"

    # game/androidstrings.rpy:59
    old "I'm downloading the Android SDK. This might take a while."
    new "Je télécharge le SDK Android, ce qui peut prendre un moment."

    # game/androidstrings.rpy:60
    old "I'm extracting the Android SDK."
    new "J'extrais le SDK Android."

    # game/androidstrings.rpy:61
    old "I've finished unpacking the Android SDK."
    new "J'ai terminé d'extraire le SDK Android."

    # game/androidstrings.rpy:62
    old "I'm about to download and install the required Android packages. This might take a while."
    new "Je suis sur le point de télécharger et d'installer les paquets Android requis, ce qui peut prendre un moment."

    # game/androidstrings.rpy:63
    old "I was unable to accept the Android licenses."
    new "L'acceptation des licences Android."

    # game/androidstrings.rpy:65
    old "I was unable to install the required Android packages."
    new "L'installation des paquets Android requis a échoué."

    # game/androidstrings.rpy:66
    old "I've finished installing the required Android packages."
    new "L'installation des paquets Android requis est terminée."

    # game/androidstrings.rpy:67
    old "You set the keystore yourself, so I'll assume it's how you want it."
    new "Vous avez vous-même spécifié un keystore, donc je vais supposer que vous le voulez."

    # game/androidstrings.rpy:68
    old "You've already created an Android keystore, so I won't create a new one for you."
    new "Vous avez déjà créé un keystore Android, donc je ne vais pas en créer un pour vous."

    # game/androidstrings.rpy:69
    old "I can create an application signing key for you. Signing an application with this key allows it to be placed in the Android Market and other app stores.\n\nDo you want to create a key?"
    new "Je peux créer une clé de signature d'application pour vous. Signer une application avec cette clé lui permet d'être placée sur l'Android Market et d'autres magasins d'applications.\n\nVoulez-vous crer une clé ?"

    # game/androidstrings.rpy:70
    old "I will create the key in the android.keystore file.\n\nYou need to back this file up. If you lose it, you will not be able to upgrade your application.\n\nYou also need to keep the key safe. If evil people get this file, they could make fake versions of your application, and potentially steal your users' data.\n\nWill you make a backup of android.keystore, and keep it in a safe place?"
    new "Je vais créer une clé dans le fichier android.keystore.\n\nVous devez créer une sauvegarde de ce fichier. Si vous le perdez, vous ne pourrez plus mettre à jour votre application.\n\nVous devez aussi garder cette clé secrète. Si de mauvaises personnes y ont accès, ils pourraient faire de fausses versions de votre application, et potentiellement voler les données de vos utilisateurs.\n\nAllez-vous faire une sauvegarde de android.keystore, et le arder dans un endroit sûr ?"

    # game/androidstrings.rpy:71
    old "Please enter your name or the name of your organization."
    new "Entrez votre nom ou celui de votre organisation."

    # game/androidstrings.rpy:72
    old "Could not create android.keystore. Is keytool in your path?"
    new "Impossible de créer android.keystore. Est-ce que le keytool est dans votre PATH ?"

    # game/androidstrings.rpy:73
    old "I've finished creating android.keystore. Please back it up, and keep it in a safe place."
    new "J'ai terminé la création de android.keystore. Faites-en une sauvegarde, et gardez-le secret."

    # game/androidstrings.rpy:74
    old "It looks like you're ready to start packaging games."
    new "Il semblerait que vous êtes prêt à commencer à empaqueter des jeux."

    # game/choose_directory.rpy:140
    old "Ren'Py was unable to run python with tkinter to choose the directory. Please install the python3-tk or tkinter package."
    new "Ren'Py n'a pas été capable de lancer python avec tkinter pour choisir le répertoire. Installer le package python3-tk ou tkinter."

    # game/choose_directory.rpy:158
    old "The selected projects directory is not writable."
    new "Le répertoire de projets sélectionné n'est pas ouvert en écriture."

    # game/choose_theme.rpy:508
    old "changing the theme"
    new "changer le thème"

    # game/distribute.rpy:1126
    old "Signing the Macintosh application...\n(This may take a long time.)"
    new "Signature de l'application Macintosh...\n(Ceci peut prendre longtemps.)"

    # game/distribute_gui.rpy:157
    old "Build Distributions: [project.current.display_name!q]"
    new "Construire les Distributions : [project.current.display_name!q]"

    # game/dmgcheck.rpy:50
    old "Ren'Py is running from a read only folder. Some functionality will not work."
    new "Ren'Py est lancé depuis un dossier en lecture seule. Certaines fonctionnalités ne fonctionneront pas."

    # game/dmgcheck.rpy:50
    old "This is probably because Ren'Py is running directly from a Macintosh drive image. To fix this, quit this launcher, copy the entire %s folder somewhere else on your computer, and run Ren'Py again."
    new "C'est probablement parce que Ren'Py est lancé directement depuis une image disque Macintosh. Quittez le lanceur, copier le dossier %s entier quelque part d'autre sur votre ordinateur et relancez Ren'Py."

    # game/editor.rpy:152
    old "(Recommended) A modern and approachable text editor."
    new "(Recommandé) Un éditeur de texte moderne et ergonomique."

    # game/editor.rpy:164
    old "Up to 150 MB download required."
    new "Jusqu'à 150 MB requis pour le téléchargement."

    # game/editor.rpy:186
    old "System Editor"
    new "Éditeur de texte du système"

    # game/editor.rpy:202
    old "None"
    new "Aucun"

    # game/editor.rpy:305
    old "Edit [text]."
    new "Modifier [text]."

    # game/front_page.rpy:91
    old "PROJECTS:"
    new "PROJETS :"

    # game/front_page.rpy:198
    old "audio"
    new "audio"

    # game/front_page.rpy:215
    old "Open project"
    new "Ouvrir le projet"

    # game/front_page.rpy:221
    old "Actions"
    new "Actions"

    # game/front_page.rpy:252
    old "Web"
    new "Web"

    # game/front_page.rpy:252
    old "(Beta)"
    new "(Béta)"

    # game/gui7.rpy:339
    old "Custom. The GUI is optimized for a 16:9 aspect ratio."
    new "Personnalisé. Le GUI est optimisé pour un ratio de cadre 16:9."

    # game/gui7.rpy:355
    old "WIDTH"
    new "LARGEUR"

    # game/gui7.rpy:355
    old "Please enter the width of your game, in pixels."
    new "Entrez la largeur de votre jeu, en pixels."

    # game/gui7.rpy:365
    old "The width must be a number."
    new "La largeur doit être un nombre."

    # game/gui7.rpy:371
    old "HEIGHT"
    new "HAUTEUR"

    # game/gui7.rpy:371
    old "Please enter the height of your game, in pixels."
    new "Entrez la hauteur de votre jeu, en pixels."

    # game/gui7.rpy:381
    old "The height must be a number."
    new "La hauteur doit être un nombre."

    # game/gui7.rpy:429
    old "creating a new project"
    new "création d'un nouveau projet"

    # game/gui7.rpy:433
    old "activating the new project"
    new "activation du nouevau projet"

    # game/install.rpy:33
    old "Could not install [name!t], as a file matching [zipglob] was not found in the Ren'Py SDK directory."
    new "Impossible d'installer [name!t], car aucunun fichier correspondant à [zipglob] n'a été trouvé dans le répertoire de Ren'Py."

    # game/install.rpy:76
    old "Successfully installed [name!t]."
    new "Installé [name!t] avec succès."

    # game/install.rpy:110
    old "Install Libraries"
    new "Installer des bibliothèques"

    # game/install.rpy:125
    old "This screen allows you to install libraries that can't be distributed with Ren'Py. Some of these libraries may require you to agree to a third-party license before being used or distributed."
    new "Ce menu vous permet d'installer des bibliothèques qui ne peuvent pas être distribuées avec Ren'Py. Certaines peuvent requérir d'accepter une licence tierce avant d'être utilisées ou distribuées."

    # game/install.rpy:131
    old "Install Live2D Cubism SDK for Native"
    new "Installer le SDK Live2D Cubism for Native"

    # game/install.rpy:140
    old "The {a=https://www.live2d.com/en/download/cubism-sdk/download-native/}Cubism SDK for Native{/a} adds support for displaying Live2D models. Place CubismSdkForNative-4-{i}version{/i}.zip in the Ren'Py SDK directory, and then click Install. Distributing a game with Live2D requires you to accept a license from Live2D, Inc."
    new "Le {a=https://www.live2d.com/en/download/cubism-sdk/download-native/}SDK Cubism for Native{/a} ajoute le support pour l'affichage de modèles Live2D. Placez CubismSdkForNative-4-{i}version{/i}.zip dans le répertoire de Ren'Py, puis cliquez sur Installer. Publier un jeu avec Live2D nécessite d'accepter une licence de Live2D, Inc."

    # game/install.rpy:144
    old "Live2D in Ren'Py doesn't support the Web, Android x86_64 (including emulators and Chrome OS), and must be added to iOS projects manually. Live2D must be reinstalled after upgrading Ren'Py or installing Android support."
    new "Live2D dans Ren'Py ne supporte pas le Web, Android x86_64 (y compris les émulateurs et Chrome OS), et doit être ajouté aux projets iOS manuellement. Live2D doit être réinstallé après avoir mis à jour Ren'Py ou installé le support Android."

    # game/install.rpy:151
    old "Install Steam Support"
    new "Installer le support Steam"

    # game/install.rpy:160
    old "Before installing Steam support, please make sure you are a {a=https://partner.steamgames.com/}Steam partner{/a}."
    new "Avant d'installer le support Steam, vérifiez que vous êtes bien un {a=https://partner.steamgames.com/}partenaire Steam{/a}."

    # game/install.rpy:172
    old "Steam support has already been installed."
    new "Le support Steam a déjà été installé."

    # game/install.rpy:176
    old "Open Ren'Py SDK Directory"
    new "Ouvrir le répertoire de Ren'Py"

    # game/interface.rpy:136
    old "Ren'Py Sponsor Information"
    new "Informations sur les sponsors de Ren'Py"

    # game/interface.rpy:372
    old "opening the log file"
    new "ouverture du fichier log"

    # game/ios.rpy:233
    old "iOS: [project.current.display_name!q]"
    new "iOS : [project.current.display_name!q]"

    # game/itch.rpy:43
    old "Downloading the itch.io butler."
    new "Téléchargement du butler itch.io."

    # game/navigation.rpy:168
    old "Navigate: [project.current.display_name!q]"
    new "Explorer : [project.current.display_name!q]"

    # game/new_project.rpy:81
    old "You will be creating an [new_project_language]{#this substitution may be localized} language project. Change the launcher language in preferences to create a project in another language."
    new "Vous allez créer un projet en [new_project_language]{#this substitution may be localized}. Changez la langue du launcher dans les préférences pour créer un projet dans une autre langue."

    # game/preferences.rpy:143
    old "Install libraries"
    new "Installer les bibliothèques"

    # game/preferences.rpy:145
    old "Reset window size"
    new "Réinitialiser la taille de la fenêtre"

    # game/preferences.rpy:188
    old "Force new tutorial"
    new "Forcer le nouveau tutoriel"

    # game/preferences.rpy:192
    old "Legacy options"
    new "Options de compatibilité"

    # game/preferences.rpy:197
    old "Sponsor message"
    new "Message des sponsors"

    # game/preferences.rpy:199
    old "Dark theme"
    new "Thème sombre"

    # game/translations.rpy:91
    old "Translations: [project.current.display_name!q]"
    new "Traductions : [project.current.display_name!q]"

    # game/translations.rpy:342
    old "Extract Dialogue: [project.current.display_name!q]"
    new "Extraire les dialogues : [project.current.display_name!q]"

    # game/updater.rpy:101
    old "The update channel controls the version of Ren'Py the updater will download."
    new "Les canaux de mise à jour contrôlent la version de Ren'Py qui sera téléchargée."

    # game/updater.rpy:110
    old "• This version is installed and up-to-date."
    new "• Cette version est installée et à jour."

    # game/updater.rpy:118
    old "%B %d, %Y"
    new "%d %B %Y"

    # game/updater.rpy:188
    old "Fetching the list of update channels"
    new "Vérification de la liste des canaux de mise à jour"

    # game/updater.rpy:193
    old "downloading the list of update channels"
    new "téléchargement de la liste des canaux de mise à jour"

    # game/updater.rpy:196
    old "parsing the list of update channels"
    new "compulsion de la liste des canaux de mise à jour"

    # game/web.rpy:242
    old "Preparing progressive download"
    new "Préparation du téléchargement progressif"

    # game/web.rpy:277
    old "Web: [project.current.display_name!q]"
    new "Web : [project.current.display_name!q]"

    # game/web.rpy:307
    old "Build Web Application"
    new "Construire l'application Web"

    # game/web.rpy:308
    old "Build and Open in Browser"
    new "Construire et ouvrir dans le navigateur"

    # game/web.rpy:309
    old "Open in Browser"
    new "Ouvrir dans le navigateur"

    # game/web.rpy:310
    old "Open build directory"
    new "Ouvrir le répertoire des distributions"

    # game/web.rpy:314
    old "Support:"
    new "Support :"

    # game/web.rpy:322
    old "RenPyWeb Home"
    new "Accueil RenPyWeb"

    # game/web.rpy:323
    old "Beuc's Patreon"
    new "Patreon de Beuc"

    # game/web.rpy:341
    old "Images and musics can be downloaded while playing. A 'progressive_download.txt' file will be created so you can configure this behavior."
    new "Les images et musiques peuvent être téléchargées pendant le jeu. Un fichier 'progressive_download.txt' sera créé pour contrôler cette fonctionnalité."

    # game/web.rpy:345
    old "Current limitations in the web platform mean that loading large images, audio files, or movies may cause audio or framerate glitches, and lower performance in general."
    new "Les limitations actuelles de la platforme web implique que changer de gros images, fichiers audio ou films peuvent causer des bugs audio ou des pertes de fps, et une baisse de performance en général."

    # game/web.rpy:354
    old "Before packaging web apps, you'll need to download RenPyWeb, Ren'Py's web support. Would you like to download RenPyWeb now?"
    new "Avant l'empaquetage des apps web, vous devrez télécharger RenPyWeb, le support web de Ren'Py. Voulez-vous télécharger RenPyWeb maintenant ?"

    # game/preferences.rpy:206
    old "Default theme"
    new "Thème par défaut"

    # game/preferences.rpy:209
    old "Custom theme"
    new "Thème personnalisé"

    # game/web.rpy:330
    old "Images and music can be downloaded while playing. A 'progressive_download.txt' file will be created so you can configure this behavior."
    new "Les images et la musique peuvent être téléchargées pendant le jeu. Un fichier 'progressive_download.txt' sera créé pour configurer cette fonction."

    # game/web.rpy:334
    old "Current limitations in the web platform mean that loading large images may cause audio or framerate glitches, and lower performance in general. Movies aren't supported."
    new "Les limitations actuelles de la platforme web signifient que le chargement de grandes images peuvent causer des bugs audio ou des saccades. Les objets 'Movies' ne sont pas supportés."

    # game/web.rpy:338
    old "There are known issues with Safari and other Webkit-based browsers that may prevent games from running."
    new "Des bugs connus avec Safari et d'autres navigateurs basés sur Webkit peuvent empêcher des jeux de fonctionner."

    # game/android.rpy:38
    old "Please select if you want a Play Bundle (for Google Play), or a Universal APK (for sideloading and other app stores)."
    new "Faites le choix entre un Play Bundle (pour Google Play), ou un Universal APK (pour d'autres librairies d'applications)."

    # game/android.rpy:53
    old "Pairs with a device over Wi-Fi, on Android 11+."
    new "Appaire un autre appareil par Wi-Fi, sur Android 11+."

    # game/android.rpy:54
    old "Connects to a device over Wi-Fi, on Android 11+."
    new "Se connecte à un appareil par Wi-Fi, sur Android 11+."

    # game/android.rpy:56
    old "Builds an Android App Bundle (ABB), intended to be uploaded to Google Play. This can include up to 2GB of data."
    new "Construit un Android App Bundle (ABB), fait pour être uploadé sur Google Play. Peut inclure jusqu'à 2GB de données."

    # game/android.rpy:57
    old "Builds a Universal APK package, intended for sideloading and stores other than Google Play. This can include up to 2GB of data."
    new "Construit un paquet Universal APK, fait pour d'autres librairies que Google Play. Peut inclure jusqu'à 2GB de données."

    # game/android.rpy:384
    old "Play Bundle"
    new "Play Bundle"

    # game/android.rpy:388
    old "Universal APK"
    new "Universal APK"

    # game/android.rpy:445
    old "Wi-Fi Debugging Pair"
    new "Debug d'appairage Wi-Fi"

    # game/android.rpy:449
    old "Wi-Fi Debugging Connect"
    new "Debug de connexion Wi-Fi"

    # game/android.rpy:537
    old "Wi-Fi Pairing Code"
    new "Code d'appairage Wi-Fi"

    # game/android.rpy:537
    old "If supported, this can be found in 'Developer options', 'Wireless debugging', 'Pair device with pairing code'."
    new "Si supporté, peut être trouvé dans 'Options de développement', 'Débogage sans fil', 'Appairer appareil avec un code'."

    # game/android.rpy:544
    old "Pairing Host & Port"
    new "Hôte d'appairage & Port"

    # game/android.rpy:560
    old "IP Address & Port"
    new "Addresse IP & Port"

    # game/android.rpy:560
    old "If supported, this can be found in 'Developer options', 'Wireless debugging'."
    new "Si supporté, peut être trouvé dans 'Options de développement', 'Débogage sans fil'."

    # game/gui7.rpy:311
    old "{size=-4}\n\nThis will not overwrite gui/main_menu.png, gui/game_menu.png, and gui/window_icon.png, but will create files that do not exist.{/size}"
    new "{size=-4}\n\nCeci ne remplacera pas gui/main_menu.png, gui/game_menu.png, ou gui/window_icon.png, mais créera des fichiers s'ils n'existent pas.{/size}"

    # game/ios.rpy:339
    old "There are known issues with the iOS simulator on Apple Silicon. Please test on x86_64 or iOS devices."
    new "Des erreurs sont rapportées sur le simulateur d'iOS sur Apple Silicon. Préférez des appareils x86_64 ou iOS."

    # game/android.rpy:38
    old "RAPT has been installed, but a bundle key hasn't been configured. Please create a new key, or restore bundle.keystore."
    new "RAPT a été installé, mais aucune clé de paquet n'a été configurée. Créez une nouvelle clé, ou restaurez bundle.keystore."

    # game/androidstrings.rpy:16
    old "I'm installing the bundle."
    new "J'installe le paquet."

    # game/androidstrings.rpy:30
    old "How much RAM do you want to allocate to Gradle?\n\nThis must be a positive integer number."
    new "Combien de RAM voulez-vous allouer à Gradle ?\n\nEntrez un nombre entier positif."

    # game/androidstrings.rpy:31
    old "The RAM size must contain only numbers."
    new "La taille de RAM ne doit contenir que des chiffres."

    # game/androidstrings.rpy:55
    old "I can create an application signing key for you. This key is required to create Universal APK for sideloading and stores other than Google Play.\n\nDo you want to create a key?"
    new "Je paux vous créer une clé de signature d'application. Cette clé est nécessaire pour créer des Universal APK pour des autres stores que Google Play.\n\nVoulez-vous créer une clé ?"

    # game/androidstrings.rpy:59
    old "I can create a bundle signing key for you. This key is required to build an Android App Bundle (AAB) for upload to Google Play.\n\nDo you want to create a key?"
    new "Je peux vous créer une clé de signature de paquets. Cette clé est nécessaire pour construire un Android App Bundle (AAB) pour uploader sur Google Play.\n\nVoulez-vous créer une clé ?"

    # game/androidstrings.rpy:60
    old "I will create the key in the bundle.keystore file.\n\nYou need to back this file up. If you lose it, you will not be able to upgrade your application.\n\nYou also need to keep the key safe. If evil people get this file, they could make fake versions of your application, and potentially steal your users' data.\n\nWill you make a backup of bundle.keystore, and keep it in a safe place?"
    new "Je vais créer la clé dans le fichier bundle.keystore.\n\nVous devez conserver ce fichier. Sans lui, vous ne pourrez plus mettre à jour votre application.\n\nVous devez aussi la garder cachée. Si des malotrus accèdent à ce fichier, ils pourront faire des faussez versions de votre application, et potentiellement voler les données des utilisateurs.\n\nAllez-vous faire une sauvegarde de bundle.keystore, et le garder bien caché ?"

    # game/androidstrings.rpy:61
    old "Could not create bundle.keystore. Is keytool in your path?"
    new "Impossible de créer bundle.keystore. Est-ce que le keytool est dans votre path ?"

    # game/preferences.rpy:206
    old "Daily check for update"
    new "Vérification quotidienne des mises à jour"

    # game/android.rpy:55
    old "Lists the connected devices."
    new "Liste les appareils connectés."

    # game/android.rpy:58
    old "Disconnects a device connected over Wi-Fi."
    new "Déconnecte un appareil connecté via Wi-Fi."

    # game/android.rpy:453
    old "List Devices"
    new "Lister les appareils"

    # game/android.rpy:465
    old "Wi-Fi Debugging Disconnect"
    new "Debug : déconnexion Wi-Fi"

    # game/android.rpy:603
    old "This can be found in 'List Devices'."
    new "Introuvable dans 'Lister les appareils'."

    # game/androidstrings.rpy:17
    old "Installing the bundle appears to have failed."
    new "L'installation du bundle semble avoir échoué."

    # game/androidstrings.rpy:19
    old "Launching the app appears to have failed."
    new "Le lancement de l'app semble avoir échoué."

    # game/androidstrings.rpy:44
    old "The version of Java on your computer does not appear to be JDK 8, which is the only version supported by the Android SDK. If you need to install JDK 8, you can download it from:\n\n{a=https://adoptium.net/?variant=openjdk8}https://adoptium.net/?variant=openjdk8{/a}\n\nYou can also set the JAVA_HOME environment variable to use a different version of Java."
    new "La version de Java présente sur votre ordinateur ne semble pas être JDK 8, qui est la seule version supportée par le SDK Android. Si vous devez installer JDK 8, vous pouvez le télécharger ici :\n\n{a=https://adoptium.net/?variant=openjdk8}https://adoptium.net/?variant=openjdk8{/a}\n\nVous pouvez aussi régler la variable d'environnement JAVA_HOME sur une autre version de Java."

    # game/updater.rpy:109
    old "• {a=https://www.renpy.org/doc/html/changelog.html}View change log{/a}"
    new "• {a=https://www.renpy.org/doc/html/changelog.html}Regarder le changelog{/a}"

    # game/updater.rpy:111
    old "• {a=https://www.renpy.org/dev-doc/html/changelog.html}View change log{/a}"
    new "• {a=https://www.renpy.org/dev-doc/html/changelog.html}Regarder le changelog{/a}"

    # game/android.rpy:60
    old "Removes Android temporary files."
    new "Retirer les fichiers temporaires Android."

    # game/android.rpy:472
    old "Clean"
    new "Nettoyer"

    # game/android.rpy:628
    old "Cleaning up Android project."
    new "Nettoyage du projet Android."

    # game/androidstrings.rpy:43
    old "I was unable to use javac to compile a test file. If you haven't installed the Java Development Kit yet, please download it from:\n\n{a=https://adoptium.net/?variant=openjdk8}https://adoptium.net/?variant=openjdk8{/a}\n\nThe JDK is different from the JRE, so it's possible you have Java without having the JDK. Please make sure you installed the 'JavaSoft (Oracle) registry keys'.\n\nWithout a working JDK, I can't continue."
    new "Impossible d'utiliser javac pour compiler un fichier de test. Si vous n'avez pas installé Java Development Kit, téléchargez-le ici :\n\n{a=https://adoptium.net/?variant=openjdk8}https://adoptium.net/?variant=openjdk8{/a}\n\nLe JDK est différent du JRE, donc il est possible d'avoir Java sans avoir le JDK. Vérifiez que vous avez installé les 'JavaSoft (Oracle) registry keys'.\n\nSans un JDK fonctionnel, je ne peux pas continuer."

    # game/androidstrings.rpy:64
    old "I've opened the directory containing android.keystore and bundle.keystore. Please back them up, and keep them in a safe place."
    new "J'ai ouvert le répertoire contenant android.keystore et bundle.keystore. Sauvegardez-les, et gardez-les dans un endroit sûr."

    # game/choose_directory.rpy:67
    old "Select Projects Directory"
    new "Sélectionner le répertoire des Projets"

    # game/distribute.rpy:1674
    old "Copying files..."
    new "Copie des fichiers..."

    # game/distribute_gui.rpy:195
    old "Update old-game"
    new "Mettre à jour old-game"

    # game/editor.rpy:152
    old "A modern editor with many extensions including advanced Ren'Py integration."
    new "Un éditeur moderne avec beaucoup d'extensions, y compris des intégrations Ren'Py avancées."

    # game/editor.rpy:153
    old "A modern editor with many extensions including advanced Ren'Py integration.\n{a=jump:reinstall_vscode}Upgrade Visual Studio Code to the latest version.{/a}"
    new "Un éditeur moderne avec beaucoup d'extensions, y compris des intégrations Ren'Py avancées.\n{a=jump:reinstall_vscode}Mettez Visual Studio Code à jour.{/a}"

    # game/editor.rpy:162
    old "Visual Studio Code"
    new "Visual Studio Code"

    # game/editor.rpy:162
    old "Up to 110 MB download required."
    new "Jusqu'à 110 Mo nécessaires pour le téléchargement."

    # game/editor.rpy:175
    old "A modern and approachable text editor."
    new "Un éditeur de texte moderne et accessible."

    # game/editor.rpy:187
    old "Atom"
    new "Atom"

    # game/editor.rpy:200
    old "jEdit"
    new "jEdit"

    # game/editor.rpy:209
    old "Visual Studio Code (System)"
    new "Visual Studio Code (Système)"

    # game/editor.rpy:209
    old "Uses a copy of Visual Studio Code that you have installed outside of Ren'Py. It's recommended you install the language-renpy extension to add support for Ren'Py files."
    new "Utilise une copie de Visual Studio Code que vous avez installé en-dehors de Ren'Py. Il est recommandé d'installer l'extension language-renpy pour ajouter la gestion des fichiers Ren'Py."

    # game/installer.rpy:10
    old "Downloading [extension.download_file]."
    new "Téléchargement de [extension.download_file]."

    # game/installer.rpy:11
    old "Could not download [extension.download_file] from [extension.download_url]:\n{b}[extension.download_error]"
    new "Impossible de télécharger [extension.download_file] depuis [extension.download_url] :\n{b}[extension.download_error]"

    # game/installer.rpy:12
    old "The downloaded file [extension.download_file] from [extension.download_url] is not correct."
    new "le fichier [extension.download_file] téléchargé depuis [extension.download_url] est incorrect."

    # game/interface.rpy:124
    old "[interface.version]"
    new "[interface.version]"

    # game/preferences.rpy:154
    old "Clean temporary files"
    new "Nettoyer les fichiers temporaires"

    # game/preferences.rpy:256
    old "Cleaning temporary files..."
    new "Nettoyage des fichiers temporaires..."

    # game/project.rpy:280
    old "This may be because the project is not writeable."
    new "Il est possible que le projet ne soit pas accessible en écriture."

    # game/translations.rpy:391
    old "Language (or None for the default language):"
    new "Langue (or None pour la langue par défaut) :"

    # game/web.rpy:344
    old "This feature is not supported in Ren'Py 8."
    new "Cette fonctionnalité n'est pas supportée dans Ren'Py 8."

    # game/web.rpy:344
    old "We will restore support in a future release of Ren'Py 8. Until then, please use Ren'Py 7 for web support."
    new "La version web sera supportée à nouveau dans une future version de Ren'Py 8. En attendant, utilisez Ren'Py 7 pour des distributions web."

    # game/preferences.rpy:104
    old "General"
    new "Général"

    # game/preferences.rpy:105
    old "Options"
    new "Options"

    # game/preferences.rpy:244
    old "Launcher Theme:"
    new "Thème du lanceur :"

    # game/preferences.rpy:254
    old "Information about creating a custom theme can be found {a=[skins_url]}in the Ren'Py Documentation{/a}."
    new "Plus d'informations sur comment créer un thème personnalisé se trouvent {a=[skins_url]}dans la documentation de Ren'Py{/a}."

    # game/preferences.rpy:271
    old "Install Libraries:"
    new "Installer des bibliothèques :"

    # game/preferences.rpy:327
    old "{#in language font}Welcome! Please choose a language"
    new "{font=fonts/Roboto-Light.ttf}Bienvenue ! Choisissez une langue{/font}"

    # game/preferences.rpy:327
    old "{#in language font}Start using Ren'Py in [lang_name]"
    new "{font=fonts/Roboto-Light.ttf}Commencez à utiliser Ren'Py en [lang_name]{/font}"

    # game/distribute_gui.rpy:231
    old "(DLC)"
    new "(DLC)"

    # game/project.rpy:46
    old "Lint checks your game for potential mistakes, and gives you statistics."
    new "Lint vérifie votre jeu pour des erreurs communes, et génère des statistiques."

    # game/web.rpy:484
    old "Creating package..."
    new "Création du package..."

    # game/android.rpy:37
    old "RAPT has been installed, but a key hasn't been configured. Please generate new keys, or copy android.keystore and bundle.keystore to the base directory."
    new "RAPT a été installé, mais aucune clé n’a été configurée. Veuillez générer de nouvelles clés, ou copier android.keystore and bundle.keystore dans le dossier racine du projet."

    # game/android.rpy:44
    old "Attempts to emulate a televison-based Android console.\n\nController input is mapped to the arrow keys, Enter is mapped to the select button, Escape is mapped to the menu button, and PageUp is mapped to the back button."
    new "Tentative d’émulation d'une console télé basée sur Android.\n\nLa manette est émulée par les touches fléchées, le bouton select par la touche Entrée, le bouton menu par la touche Echap, et le bouton retour par la touche PageUp."

    # game/android.rpy:46
    old "Downloads and installs the Android SDK and supporting packages."
    new "Télécharge et installe le kit de développement Android et les paquets requis."

    # game/android.rpy:47
    old "Generates the keys required to sign the package."
    new "Génère les clés requises pour signer le package."

    # game/android.rpy:381
    old "Install SDK"
    new "Installer le SDK"

    # game/android.rpy:385
    old "Generate Keys"
    new "Générer les clés"

    # game/androidstrings.rpy:32
    old "How much RAM (in GB) do you want to allocate to Gradle?\nThis must be a positive integer number."
    new "Combien de RAM (in GB) voulez-vous allouer à Gradle ?\nEntrez un nombre entier positif."

    # game/androidstrings.rpy:33
    old "The RAM size must contain only numbers and be positive."
    new "La taille de RAM ne doit contenir que des chiffres et être positive."

    # game/androidstrings.rpy:63
    old "I found an android.keystore file in the rapt directory. Do you want to use this file?"
    new "J'ai trouvé un fichier android.keystore dans le dossier \"rapt\". Voulez-vous l'utiliser ?"

    # game/androidstrings.rpy:66
    old "\n\nSaying 'No' will prevent key creation."
    new "\n\nRépondre \"Non\" empêchera la création de clés."

    # game/androidstrings.rpy:69
    old "I found a bundle.keystore file in the rapt directory. Do you want to use this file?"
    new "J'ai trouvé un fichier bundle.keystore dans le dossier \"rapt\". Voulez-vous l'utiliser ?"

    # game/choose_directory.rpy:72
    old "No directory was selected, but one is required."
    new "Un chemin d'accès est nécessaire, mais aucun n'a été fourni."

    # game/choose_directory.rpy:80
    old "The selected directory does not exist."
    new "Le dossier sélectionné n'existe pas."

    # game/choose_directory.rpy:82
    old "The selected directory is not writable."
    new "Le dossier sélectionné n'est pas ouvert en écriture."

    # game/distribute.rpy:554
    old "This may be derived from build.name and config.version or build.version."
    new "Cette variable peut être dérivée de build.name, et de config.version ou build.version."

    # game/new_project.rpy:66
    old "Warning : you are using Ren'Py 7. It is recommended to start new projects using Ren'Py 8 instead."
    new "Attention : vous utilisez Ren'Py 7. Il est recommandé d'utiliser Ren'Py 8 pour de nouveaux projets."
