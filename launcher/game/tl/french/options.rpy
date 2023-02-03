translate french strings:

    # options.rpy:1
    old "## This file contains options that can be changed to customize your game."
    new "## Ce fichier contient les options qui peuvent être modifiées pour personnaliser votre jeu."

    # options.rpy:4
    old "## Lines beginning with two '#' marks are comments, and you shouldn't uncomment them. Lines beginning with a single '#' mark are commented-out code, and you may want to uncomment them when appropriate."
    new "## Les lignes qui commencent avec deux dièses '#' sont des commentaires et vous ne devriez pas les décommenter. Les lignes qui commencent avec un seul dièse sont du code commenté et vous pouvez les décommentez quand c’est approprié (pour votre projet)."

    # options.rpy:10
    old "## Basics"
    new "## Bases"

    # options.rpy:12
    old "## A human-readable name of the game. This is used to set the default window title, and shows up in the interface and error reports."
    new "## Un nom de jeu intelligible. Il est utilisé pour personnaliser le titre de la fenêtre par défaut et s’affiche dans l’interface ainsi que dans les rapports d’erreur."

    # options.rpy:15
    old "## The _() surrounding the string marks it as eligible for translation."
    new "## La chaîne de caractère contenu dans _() est éligible à la traduction."

    # options.rpy:17
    old "Ren'Py 7 Default GUI"
    new "GUI Ren’Py 7 par défaut"

    # options.rpy:20
    old "## Determines if the title given above is shown on the main menu screen. Set this to False to hide the title."
    new "## Détermine si le titre renseigné plus haut est affiché sur l'écran du menu principal Configurez-le à False (Faux) pour cacher le titre."

    # options.rpy:26
    old "## The version of the game."
    new "## La version du jeu."

    # options.rpy:31
    old "## Text that is placed on the game's about screen. To insert a blank line between paragraphs, write \\n\\n."
    new "## Texte qui est placé dans l’écran « À propos ». Pour insérer une ligne vide entre deux paragraphes écrivez \\n\\n."

    # options.rpy:37
    old "## A short name for the game used for executables and directories in the built distribution. This must be ASCII-only, and must not contain spaces, colons, or semicolons."
    new "## Un nom court pour le jeu qui sera utilisé pour les répertoires et le nom de l’exécutable. Il ne doit contenir que des caractères ASCII et ne doit pas contenir d’espace, de virgules ou de points-virgules."

    # options.rpy:44
    old "## Sounds and music"
    new "## Sons et musiques"

    # gui/game/options.rpy:47
    old "## These three variables control, among other things, which mixers are shown to the player by default. Setting one of these to False will hide the appropriate mixer."
    new "## Ces trois variables contrôlent, entre autres, quels mixeurs sont affichés au joueur par défaut. Configurer l’un de ceux-ci à False (Faux) cachera le mixeur concerné."

    # options.rpy:55
    old "## To allow the user to play a test sound on the sound or voice channel, uncomment a line below and use it to set a sample sound to play."
    new "## Pour autoriser le joueur à réaliser un test de volume, décommenter la ligne ci-dessous et utilisez-la pour configurer un son d’exemple."

    # options.rpy:62
    old "## Uncomment the following line to set an audio file that will be played while the player is at the main menu. This file will continue playing into the game, until it is stopped or another file is played."
    new "## Décommentez la ligne suivante pour configurer un fichier audio qui sera diffusé quand le joueur sera sur le menu principal. Ce son se poursuivra dans le jeu, jusqu’à ce qu'il soit stoppé ou qu’un autre fichier soit joué."

    # options.rpy:69
    old "## Transitions"
    new "## Transitions"

    # options.rpy:71
    old "## These variables set transitions that are used when certain events occur. Each variable should be set to a transition, or None to indicate that no transition should be used."
    new "## Ces variables configurent les transitions qui sont utilisées quand certains événements surviennent. Chaque variable peuvent être configurée pour une transition. La valeur None indique qu’aucune transition ne doit être utilisée."

    # options.rpy:75
    old "## Entering or exiting the game menu."
    new "## À l’entrée ou à la sortie du menu du jeu."

    # options.rpy:81
    old "## A transition that is used after a game has been loaded."
    new "## La transition qui sera utilisée après le chargement d’une partie."

    # options.rpy:86
    old "## Used when entering the main menu after the game has ended."
    new "## La transition qui sera utilisé après la fin du jeu."

    # options.rpy:91
    old "## A variable to set the transition used when the game starts does not exist. Instead, use a with statement after showing the initial scene."
    new "## Il n’y a pas de variable pour configurer la transition en début de partie. À la place, utilisez un état de transition juste après l’affichage de la toute première scène."

    # options.rpy:96
    old "## Window management"
    new "## Gestion des fenêtres"

    # options.rpy:98
    old "## This controls when the dialogue window is displayed. If \"show\", it is always displayed. If \"hide\", it is only displayed when dialogue is present. If \"auto\", the window is hidden before scene statements and shown again once dialogue is displayed."
    new "## Cela contrôle l’affichage de la fenêtre de dialogue. Si « show », elle est toujours affichée. Si « hide », elle ne s’affiche que lorsque du dialogue est présent. Si « auto », La fenêtre est cachée avant chaque changement de scène et réapparait une fois le dialogue affiché."

    # options.rpy:103
    old "## After the game has started, this can be changed with the \"window show\", \"window hide\", and \"window auto\" statements."
    new "## Après le début de la partie, cela peut-être changé avec les instructions « window show », « window hide » et « window auto »."

    # options.rpy:109
    old "## Transitions used to show and hide the dialogue window"
    new "## Transitions utilisées pour afficher ou cacher la fenêtre de dialogue"

    # options.rpy:115
    old "## Preference defaults"
    new "## Préférences par défaut"

    # options.rpy:117
    old "## Controls the default text speed. The default, 0, is infinite, while any other number is the number of characters per second to type out."
    new "## Contrôle la vitesse du texte. La valeur par défaut, 0, est infinie. Toute autre valeur est le nombre de caractères tapés par seconde."

    # options.rpy:123
    old "## The default auto-forward delay. Larger numbers lead to longer waits, with 0 to 30 being the valid range."
    new "## Le délai d’avancée automatique. Des nombres importants entraînent une longue attente. Des valeurs réputées correctes sont comprises dans une plage allant de 0 à 30."

    # options.rpy:129
    old "## Save directory"
    new "## Répertoire de sauvegarde"

    # options.rpy:131
    old "## Controls the platform-specific place Ren'Py will place the save files for this game. The save files will be placed in:"
    new "## Ces valeurs, dépendant de la plateforme, déterminent l’emplacement où Ren’Py stockera les fichiers de sauvegarde. Les fichiers de sauvegardes seront stockés dans :"

    # options.rpy:134
    old "## Windows: %APPDATA\\RenPy\\<config.save_directory>"
    new "## Windows : %APPDATA\\RenPy\\<config.save_directory>"

    # options.rpy:136
    old "## Macintosh: $HOME/Library/RenPy/<config.save_directory>"
    new "## Macintosh : $HOME/Library/RenPy/<config.save_directory>"

    # options.rpy:138
    old "## Linux: $HOME/.renpy/<config.save_directory>"
    new "## Linux : $HOME/.renpy/<config.save_directory>"

    # options.rpy:140
    old "## This generally should not be changed, and if it is, should always be a literal string, not an expression."
    new "## Cela ne devrait généralement pas changer. Si vous le faîtes, choisissez toujours une chaîne de caractères littéraux, pas une expression."

    # options.rpy:146
    old "## Icon ########################################################################'"
    new "## Icone #######################################################################'"

    # options.rpy:148
    old "## The icon displayed on the taskbar or dock."
    new "## L'icone affichée dans la barre des tâches ou sur le dock."

    # options.rpy:153
    old "## Build configuration"
    new "## Configuration de la compilation"

    # options.rpy:155
    old "## This section controls how Ren'Py turns your project into distribution files."
    new "## Cette section paramètre la façon dont Ren’Py transforme votre projet en fichier à distribuer."

    # options.rpy:160
    old "## The following functions take file patterns. File patterns are case- insensitive, and matched against the path relative to the base directory, with and without a leading /. If multiple patterns match, the first is used."
    new "## Les fonctions suivantes prennent en paramètres un format de fichier. Les formats de fichiers ne sont pas sensibles à la casse et correspondent au répertoire relatif au répertoire de base. Il n’y a pas de / à la fin. Si plusieurs formats correspondent, le premier est utilisé."

    # options.rpy:165
    old "## In a pattern:"
    new "## Dans le format :"

    # options.rpy:167
    old "## / is the directory separator."
    new "## / est le séparateur de répertoire."

    # options.rpy:169
    old "## * matches all characters, except the directory separator."
    new "## * correspond à tous les caractères à l’exception du séparateur de répertoire."

    # options.rpy:171
    old "## ** matches all characters, including the directory separator."
    new "## ** correspond à tous les caractères, y compris le séparateur de répertoire."

    # options.rpy:173
    old "## For example, \"*.txt\" matches txt files in the base directory, \"game/**.ogg\" matches ogg files in the game directory or any of its subdirectories, and \"**.psd\" matches psd files anywhere in the project."
    new "## Par exemple, \"*.txt\" correspond à tous les fichiers txt dans le répertoire de base, \"game/**.ogg\" correspond à tous les fichiers ogg dans le répertoire game, mais aussi à tous ses répertoires. \"**.psd\" correspond à tous les fichiers psd quelque soit leur emplacement dans l’arborescence du fichier."

    # options.rpy:177
    old "## Classify files as None to exclude them from the built distributions."
    new "## Choisissez la valeur « None » pour les exclure de la distribution."

    # options.rpy:185
    old "## To archive files, classify them as 'archive'."
    new "## Pour archiver les fichiers, choisissez la valeur « archive »."

    # options.rpy:190
    old "## Files matching documentation patterns are duplicated in a mac app build, so they appear in both the app and the zip file."
    new "## Les fichiers correspondant au format de documentation sont dupliqués pour les compilation sur Mac, c'est pourquoi ils apparaissent deux fois dans l’archive zip."

    # options.rpy:196
    old "## A Google Play license key is required to perform in-app purchases. It can be found in the Google Play developer console, under \"Monetize\" > \"Monetization Setup\" > \"Licensing\"."
    new "## Une clé de licence Google Play est requise pour permettre les achats depuis l'application. Vous pourrez la trouver dans la console de développement Google Play, sous \"Monétiser\" > \"Configuration de la monétisation\" > \"Licences\"."

    # options.rpy:203
    old "## The username and project name associated with an itch.io project, separated by a slash."
    new "## Le nom d’utilisateur et du projet associé au projet itch.io, séparé par un slash."

    # gui/game/options.rpy:31
    old "## Text that is placed on the game's about screen. Place the text between the triple-quotes, and leave a blank line between paragraphs."
    new "## Texte placé sur l'écran \"À propos\" du jeu. Placez le texte entre triples guillemets, et laissez une ligne entre les paragraphes."

    # gui/game/options.rpy:82
    old "## Between screens of the game menu."
    new "## Entre les écrans du menu du jeu."

    # gui/game/options.rpy:152
    old "## Icon"
    new "## Icône"
