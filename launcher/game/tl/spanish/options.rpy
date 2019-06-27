translate spanish strings:

    # options.rpy:1
    old "## This file contains options that can be changed to customize your game."
    new "## Este archivo contiene opciones que pueden cambiarse para personalizar el juego."

    # options.rpy:4
    old "## Lines beginning with two '#' marks are comments, and you shouldn't uncomment them. Lines beginning with a single '#' mark are commented-out code, and you may want to uncomment them when appropriate."
    new "## Las líneas que empiezan con doble '#' son comentarios, no deben ser descomentadas. Las líneas que empiezan con simple '#' son código comentado, puedes descomentarlas si es apropiado."

    # options.rpy:10
    old "## Basics"
    new "## Básico"

    # options.rpy:12
    old "## A human-readable name of the game. This is used to set the default window title, and shows up in the interface and error reports."
    new "## Nombre del juego en forma legible. Usado en el título de la ventana del juego, en la interfaz y en los informes de error."

    # options.rpy:15
    old "## The _() surrounding the string marks it as eligible for translation."
    new "## El _() que rodea la cadena de texto la señala como traducible."

    # options.rpy:17
    old "Ren'Py 7 Default GUI"
    new "Ren'Py 7 Default GUI"

    # options.rpy:20
    old "## Determines if the title given above is shown on the main menu screen. Set this to False to hide the title."
    new "## Determina si el título dado más arriba se muestra en el menú principal. Ajústalo a 'False' para esconder el título."

    # options.rpy:26
    old "## The version of the game."
    new "## Versión del juego."

    # options.rpy:31
    old "## Text that is placed on the game's about screen. Place the text between the triple-quotes, and leave a blank line between paragraphs."
    new "## Texto situado en la pantalla 'Acerca de' del juego. Sitúa el texto entre comillas triples y deja una línea en blanco entre párrafos."

    # options.rpy:38
    old "## A short name for the game used for executables and directories in the built distribution. This must be ASCII-only, and must not contain spaces, colons, or semicolons."
    new "## Nombre breve del juego para ejecutables y directorios en la distribución. Debe contener solo carácteres ASCII, sin espacios, comas o puntos y coma."

    # options.rpy:45
    old "## Sounds and music"
    new "## Sonidos y música"

    # options.rpy:47
    old "## These three variables control which mixers are shown to the player by default. Setting one of these to False will hide the appropriate mixer."
    new "## Estas tres variables controlan los mezcladores mostrados por defecto al jugador. Ajustar alguno a 'False' para esconderlo."

    # options.rpy:56
    old "## To allow the user to play a test sound on the sound or voice channel, uncomment a line below and use it to set a sample sound to play."
    new "## Para permitir al usuario probar el volumen de los canales de sonido o voz, descomenta la línea más abajo y ajústala a un sonido de ejemplo."

    # options.rpy:63
    old "## Uncomment the following line to set an audio file that will be played while the player is at the main menu. This file will continue playing into the game, until it is stopped or another file is played."
    new "## Descomenta la línea siguiente para ajustar un archivo de audio que sonará en el menú principal. Este archivo seguirá sonando en el juego hasta que sea detenido o se reproduzca otro archivo."

    # options.rpy:70
    old "## Transitions"
    new "## Transiciones"

    # options.rpy:72
    old "## These variables set transitions that are used when certain events occur. Each variable should be set to a transition, or None to indicate that no transition should be used."
    new "## Estas variables ajustan transiciones usadas ante ciertos eventos. Cada variable debe indicar una transición o bien 'None', cuando no se desea usar ninguna transición."

    # options.rpy:76
    old "## Entering or exiting the game menu."
    new "## Entrar o salir del manú del juego."

    # options.rpy:82
    old "## Between screens of the game menu."
    new "## Entre pantallas del menú del juego."

    # options.rpy:87
    old "## A transition that is used after a game has been loaded."
    new "## Transición tras la carga de una partida."

    # options.rpy:92
    old "## Used when entering the main menu after the game has ended."
    new "## Transición de acceso al menú principal tras finalizar el juego."

    # options.rpy:97
    old "## A variable to set the transition used when the game starts does not exist. Instead, use a with statement after showing the initial scene."
    new "## No existe la variable que ajusta la transición cuando el juego comienza. Para ello se usa la sentencia 'with' al mostrar la escena inicial."

    # options.rpy:102
    old "## Window management"
    new "## Gestión de ventanas"

    # options.rpy:104
    old "## This controls when the dialogue window is displayed. If \"show\", it is always displayed. If \"hide\", it is only displayed when dialogue is present. If \"auto\", the window is hidden before scene statements and shown again once dialogue is displayed."
    new "## Esto controla cuándo se muestra la ventana de diálogo. Si es \"show\", es siempre visible. Si es \"hide\", solo se muestra cuando hay diálogo presente. Si es \"auto\", la ventana se esconde antes de las sentencias 'scene' y se muestra de nuevo cuando hay diálogo que presentar."

    # options.rpy:109
    old "## After the game has started, this can be changed with the \"window show\", \"window hide\", and \"window auto\" statements."
    new "## Una vez comenzado el juego, esto se puede ajustar con las sentencias \"window show\", \"window hide\", y \"window auto\"."

    # options.rpy:115
    old "## Transitions used to show and hide the dialogue window"
    new "## Transiciones usadas para mostrar o esconder la ventana de diálogo"

    # options.rpy:121
    old "## Preference defaults"
    new "## Preferencias por defecto"

    # options.rpy:123
    old "## Controls the default text speed. The default, 0, is infinite, while any other number is the number of characters per second to type out."
    new "## Controla la velocidad del texto por defecto. El valor por defecto 0 indica infinito; cualquier otro número indica el número de caracteres por segundo que se mostrarán."

    # options.rpy:129
    old "## The default auto-forward delay. Larger numbers lead to longer waits, with 0 to 30 being the valid range."
    new "## El retraso por defecto del auto-avance. Números más grandes indican esperas mayores. El rango válido es 0-30."

    # options.rpy:135
    old "## Save directory"
    new "## Directorio de guardado"

    # options.rpy:137
    old "## Controls the platform-specific place Ren'Py will place the save files for this game. The save files will be placed in:"
    new "## Controla el lugar en el que Ren'Py colocará los archivos de guardado, dependiendo de la plataforma."

    # options.rpy:140
    old "## Windows: %APPDATA\\RenPy\\<config.save_directory>"
    new "## Windows: %APPDATA\\RenPy\\<config.save_directory>"

    # options.rpy:142
    old "## Macintosh: $HOME/Library/RenPy/<config.save_directory>"
    new "## Macintosh: $HOME/Library/RenPy/<config.save_directory>"

    # options.rpy:144
    old "## Linux: $HOME/.renpy/<config.save_directory>"
    new "## Linux: $HOME/.renpy/<config.save_directory>"

    # options.rpy:146
    old "## This generally should not be changed, and if it is, should always be a literal string, not an expression."
    new "## Normalmente, este valor no debe ser modificado. Si lo es, debe ser siempre una cadena literal y no una expresión."

    # options.rpy:152
    old "## Icon"
    new "## Ícono"

    # options.rpy:154
    old "## The icon displayed on the taskbar or dock."
    new "## El ícono mostrado en la barra de tareas."

    # options.rpy:159
    old "## Build configuration"
    new "## Configuración de 'Build'"

    # options.rpy:161
    old "## This section controls how Ren'Py turns your project into distribution files."
    new "## Esta sección contrla cómo Ren'Py convierte el proyecto en archivos para la distribución."

    # options.rpy:166
    old "## The following functions take file patterns. File patterns are case- insensitive, and matched against the path relative to the base directory, with and without a leading /. If multiple patterns match, the first is used."
    new "## Las funciones siguientes toman patrones de archivos. No son relevantes las mayúsculas o minúsculas. Son relativos al directorio base, con o sin una / inicial. Si corresponden más de un patrón, se usa el primero."

    # options.rpy:171
    old "## In a pattern:"
    new "## En un patrón:"

    # options.rpy:173
    old "## / is the directory separator."
    new "## / es el separador de directorios."

    # options.rpy:175
    old "## * matches all characters, except the directory separator."
    new "## * corresponde a todos los carácteres, excepto el separador de directorios."

    # options.rpy:177
    old "## ** matches all characters, including the directory separator."
    new "## ** corresponde a todos los carácteres, incluynedo el separador de directorios."

    # options.rpy:179
    old "## For example, \"*.txt\" matches txt files in the base directory, \"game/**.ogg\" matches ogg files in the game directory or any of its subdirectories, and \"**.psd\" matches psd files anywhere in the project."
    new "## Por ejemplo, \"*.txt\" corresponde a los archivos .txt en el directorio de base, \"game/**.ogg\" corresponde a los archivos .ogg del directorio 'game' y sus subdirectorios y \"**.psd\" corresponde a los archivos .psd en cualquier parte del proyecto."

    # options.rpy:183
    old "## Classify files as None to exclude them from the built distributions."
    new "## Clasifica archivos como 'None' para excluirlos de la distribución."

    # options.rpy:191
    old "## To archive files, classify them as 'archive'."
    new "## Para archivar, se clasifican como 'archive'."

    # options.rpy:196
    old "## Files matching documentation patterns are duplicated in a mac app build, so they appear in both the app and the zip file."
    new "## Los archivos que corresponden a patrones de documentation se duplican en la distribución de mac; aparecerán en los archivos app y zip."

    # options.rpy:202
    old "## Set this to a string containing your Apple Developer ID Application to enable codesigning on the Mac. Be sure to change it to your own Apple-issued ID."
    new "## Ajusta la cadena que contiene tu 'Apple Developer ID Application' para permitir el firmado en Mac. Asegúrate de cambiarlo a tu propia ID facilitada por Apple."

    # options.rpy:209
    old "## A Google Play license key is required to download expansion files and perform in-app purchases. It can be found on the \"Services & APIs\" page of the Google Play developer console."
    new "## Es necesaria una clave de licencia Google Play para descargar archivos de expansión y realizar compras en la aplicación. Se puede encontrar en la página \"Services & APIs\" de la consola de desarrollador de Google Play."

    # options.rpy:216
    old "## The username and project name associated with an itch.io project, separated by a slash."
    new "## Los nombres de usuario y de proyecto asociados con un proyecto itch.io, separados por una barra."
