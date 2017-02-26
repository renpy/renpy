
translate italian strings:

    # options.rpy:1
    old "## This file contains options that can be changed to customize your game."
    new "## Questo file contiene opzioni che possono venire cambiate per personalizzare il gioco."

    # options.rpy:4
    old "## Lines beginning with two '#' marks are comments, and you shouldn't uncomment them. Lines beginning with a single '#' mark are commented-out code, and you may want to uncomment them when appropriate."
    new "## Le linee che cominciano con due '#' sono commenti e non dovresti modificarle. Le linee con un solo '#' sono linee di codice opzionali, e potresti volerle modificare se appropriato."

    # options.rpy:10
    old "## Basics"
    new "## Fondamentali"

    # options.rpy:12
    old "## A human-readable name of the game. This is used to set the default window title, and shows up in the interface and error reports."
    new "## Il nome del gioco in forma leggibile. E' usato per il titolo nella finestra e viene impiegato per i resoconti di errore e nell'interfaccia."

    # options.rpy:15
    old "## The _() surrounding the string marks it as eligible for translation."
    new "## La notazione _() che racchiude la stringa la segna come testo traducibile."

    # options.rpy:17
    old "Ren'Py 7 Default GUI"
    new "Ren'Py 7 Default GUI"

    # options.rpy:20
    old "## Determines if the title given above is shown on the main menu screen. Set this to False to hide the title."
    new "## Determina se il titolo fornito più sopra è mostrato nel main menu. Imposta su 'False' per nascondere il titolo."

    # options.rpy:26
    old "## The version of the game."
    new "## La versione del gioco."

    # options.rpy:31
    old "## Text that is placed on the game's about screen. To insert a blank line between paragraphs, write \\n\\n."
    new "## Il testo che compare nello screen About. Per inserire linee vuote fra i paragrafi, scrivi \\n\\n."

    # options.rpy:37
    old "## A short name for the game used for executables and directories in the built distribution. This must be ASCII-only, and must not contain spaces, colons, or semicolons."
    new "## Un nome abbreviato impiegato dagli eseguibili e dalle cartelle nelle distribuzioni compilate. Deve contenere solo caratteri ASCII e non può contenere spazi, due punti, o punti e virgole."

    # options.rpy:44
    old "## Sounds and music"
    new "## Suoni e musica"

    # options.rpy:46
    old "## These three variables control which mixers are shown to the player by default. Setting one of these to False will hide the appropriate mixer."
    new "## Queste tre variabili controllano quali mixer audio sono mostrati al giocatore. Impostare una di esse su 'False' nasconderà il mixer audio relativo."

    # options.rpy:55
    old "## To allow the user to play a test sound on the sound or voice channel, uncomment a line below and use it to set a sample sound to play."
    new "## Per consentire al giocatore di eseguire un test sonoro sui canali Suono o Voce, togli # dalla linea e usala per impostare un suono di esempio."

    # options.rpy:62
    old "## Uncomment the following line to set an audio file that will be played while the player is at the main menu. This file will continue playing into the game, until it is stopped or another file is played."
    new "## Togli # dalla linea seguente per impostare un file audio che sarà riprodotto durante il main menu. Continuerà a suonare fino a che non verrà interrotto o un altro file audio verrà suonato."

    # options.rpy:69
    old "## Transitions"
    new "## Transizioni"

    # options.rpy:71
    old "## These variables set transitions that are used when certain events occur. Each variable should be set to a transition, or None to indicate that no transition should be used."
    new "## Queste variabili impostano le transizioni che sono usate quando avvengono certi eventi. Ogni variabile deve essere impostata su una transizione, o su None per indicare che nessuna transizione deve venire usata."

    # options.rpy:75
    old "## Entering or exiting the game menu."
    new "## Entrare o uscire dal game menu."

    # options.rpy:81
    old "## A transition that is used after a game has been loaded."
    new "## Transizione usata dopo che una partita viene caricata."

    # options.rpy:86
    old "## Used when entering the main menu after the game has ended."
    new "## Usata quando si torna al main menu dopo che è finita una partita."

    # options.rpy:91
    old "## A variable to set the transition used when the game starts does not exist. Instead, use a with statement after showing the initial scene."
    new "## Non esiste una variabile per impostare la transizione da usare quando inizia il gioco. Usa un comando 'with' subito dopo aver mostrato la prima 'scene'."

    # options.rpy:96
    old "## Window management"
    new "## Gestione finestra"

    # options.rpy:98
    old "## This controls when the dialogue window is displayed. If \"show\", it is always displayed. If \"hide\", it is only displayed when dialogue is present. If \"auto\", the window is hidden before scene statements and shown again once dialogue is displayed."
    new "## Controlla come viene mostrata la finestra dei dialoghi. Con \"show\", viene mostrata sempre. Con \"hide\", è mostrata solo quando ci sono linee di dialogo. Con \"auto\", la finestra è nascosta prima di un comando 'scene' e mostrata di nuovo al successivo dialogo."

    # options.rpy:103
    old "## After the game has started, this can be changed with the \"window show\", \"window hide\", and \"window auto\" statements."
    new "## Dopo che il gioco ha avuto inizio, questo può essere cambiato coi comandi \"window show\", \"window hide\", and \"window auto\"."

    # options.rpy:109
    old "## Transitions used to show and hide the dialogue window"
    new "## Transizioni usate per mostrare e nascondere la finestra dei dialoghi"

    # options.rpy:115
    old "## Preference defaults"
    new "## Opzioni predefinite"

    # options.rpy:117
    old "## Controls the default text speed. The default, 0, is infinite, while any other number is the number of characters per second to type out."
    new "## Controlla la velocità del testo predefinita. Lo standard, 0, è infinito, mentre qualunque altro numero indica il numero di caratteri al secondo da mostrare."

    # options.rpy:123
    old "## The default auto-forward delay. Larger numbers lead to longer waits, with 0 to 30 being the valid range."
    new "## Il ritardo predefinito dell'avanzamento automatico. Numeri alti portano ad attese più lunghe, con un intervallo valido da 0 a 30."

    # options.rpy:129
    old "## Save directory"
    new "## Percorso Salvataggi"

    # options.rpy:131
    old "## Controls the platform-specific place Ren'Py will place the save files for this game. The save files will be placed in:"
    new "## Controlla dove ren'Py pone i file di salvataggio, secondo la piattaforma. I file possono essere posti in:"

    # options.rpy:134
    old "## Windows: %APPDATA\\RenPy\\<config.save_directory>"
    new "## Windows: %APPDATA\\RenPy\\<config.save_directory>"

    # options.rpy:136
    old "## Macintosh: $HOME/Library/RenPy/<config.save_directory>"
    new "## Macintosh: $HOME/Library/RenPy/<config.save_directory>"

    # options.rpy:138
    old "## Linux: $HOME/.renpy/<config.save_directory>"
    new "## Linux: $HOME/.renpy/<config.save_directory>"

    # options.rpy:140
    old "## This generally should not be changed, and if it is, should always be a literal string, not an expression."
    new "## Di solito questo non dovrebbe venire cambiato, ma se lo fosse deve sempre essere una stringa diretta e non un'espressione."

    # options.rpy:146
    old "## Icon ########################################################################'"
    new "## Icona #######################################################################'"

    # options.rpy:148
    old "## The icon displayed on the taskbar or dock."
    new "## L'icona mostrata sulla dock o sulla barra applicazioni."

    # options.rpy:153
    old "## Build configuration"
    new "## Configura Compilazione"

    # options.rpy:155
    old "## This section controls how Ren'Py turns your project into distribution files."
    new "## Questa sezione controlla come Ren'Py trasforma il tuo progetto in file di distribuzione."

    # options.rpy:160
    old "## The following functions take file patterns. File patterns are case- insensitive, and matched against the path relative to the base directory, with and without a leading /. If multiple patterns match, the first is used."
    new "## Le funzioni seguenti richiedono schemi di nome. Questi schemi non differenziano maiuscole e minuscole, e corrispondono al percorso relativo alla cartella base, con e senza un segno / preposto. Se più schemi corrispondono, viene usato il primo."

    # options.rpy:165
    old "## In a pattern:"
    new "## In uno schema:"

    # options.rpy:167
    old "## / is the directory separator."
    new "## / è il separatore fra cartelle."

    # options.rpy:169
    old "## * matches all characters, except the directory separator."
    new "## * equivale a qualunque carattere tranne il separatore fra cartelle."

    # options.rpy:171
    old "## ** matches all characters, including the directory separator."
    new "## ** equivale a qualunque carattere inclusi i separatori fra cartelle."

    # options.rpy:173
    old "## For example, \"*.txt\" matches txt files in the base directory, \"game/**.ogg\" matches ogg files in the game directory or any of its subdirectories, and \"**.psd\" matches psd files anywhere in the project."
    new "## Per esempio, \"*.txt\" indica file .txt nella cartella base, \"game/**.ogg\" indica file .ogg nella cartella base o qualunque sua sottocartella, e \"**.psd\" indica file .psd ovunque nel progetto."

    # options.rpy:177
    old "## Classify files as None to exclude them from the built distributions."
    new "## Classifica file come 'None' per escluderli dalla compilazione."

    # options.rpy:185
    old "## To archive files, classify them as 'archive'."
    new "## Per archiviare i file, classificali come 'archive'."

    # options.rpy:190
    old "## Files matching documentation patterns are duplicated in a mac app build, so they appear in both the app and the zip file."
    new "## I file che corrispondono a schemi di documentazione sono duplicati nella compilazione di app Macintosh, quindi appariranno sia nella app che nel file zip."

    # options.rpy:196
    old "## A Google Play license key is required to download expansion files and perform in-app purchases. It can be found on the \"Services & APIs\" page of the Google Play developer console."
    new "## Una licenza Google Play è richiesta per scaricare file di espansione ed eseguire acquisti in-app. La Chiave Licenza può essere trovata alla pagina \"Services & APIs\" della console sviluppatori di Google Play."

    # options.rpy:203
    old "## The username and project name associated with an itch.io project, separated by a slash."
    new "## L'username e project name associati a un progetto itch.io, separati da una slash."

    # options.rpy:146
    old "## Icon"
    new "## Icona"

