translate spanish strings:
    # game/new_project.rpy:77
    old "{#language name and font}"
    new "{font=fonts/Roboto-Light.ttf}Español{/font}"

    # about.rpy:39
    old "[version!q]"
    new "[version!q]"

    # about.rpy:43
    old "View license"
    new "Ver licencia"

    # add_file.rpy:28
    old "FILENAME"
    new "ARCHIVO"

    # add_file.rpy:28
    old "Enter the name of the script file to create."
    new "Introduce el nombre del archivo de script para crearlo."

    # add_file.rpy:31
    old "The filename must have the .rpy extension."
    new "El nombre del archivo debe tener la extensión .rpy."

    # add_file.rpy:39
    old "The file already exists."
    new "El archivo ya existe."

    # add_file.rpy:42
    old "# Ren'Py automatically loads all script files ending with .rpy. To use this\n# file, define a label and jump to it from another file.\n"
    new "# Ren'Py carga automáticamente todos los archivos que terminan en .rpy. Para usar este\n# archivo, defina una etiqueta y salte a el desde otro archivo\n"

    # android.rpy:30
    old "To build Android packages, please download RAPT, unzip it, and place it into the Ren'Py directory. Then restart the Ren'Py launcher."
    new "Para construir un paquete para Android, por favor descarga RAPT, descomprímelo y colócalo dentro de la carpeta de Ren'Py. Después reinicia el lanzador de Ren'Py."

    # game/android.rpy:31
    old "A 64-bit/x64 Java [JDK_REQUIREMENT] Development Kit is required to build Android packages on Windows. The JDK is different from the JRE, so it's possible you have Java without having the JDK.\n\nPlease {a=https://www.renpy.org/jdk/[JDK_REQUIREMENT]}download and install the JDK{/a}, then restart the Ren'Py launcher."
    new "Se requiere un kit de desarrollo Java 8 de 64 bits/x64 para construir paquetes de Android en Windows. El JDK es diferente del JRE, por lo que es posible que tengas Java sin el JDK.\n\nPor favor, {a=https://www.renpy.org/jdk/[JDK_REQUIREMENT]}descarga e instala el JDK{/a}, luego reinicia el lanzador de Ren'Py."

    # android.rpy:32
    old "RAPT has been installed, but you'll need to install the Android SDK before you can build Android packages. Choose Install SDK to do this."
    new "RAPT está instalado, pero tendrás que instalar el SDK de Android para poder construir paquetes de Android. Selecciona instalar SDK para instalarlo."

    # android.rpy:33
    old "RAPT has been installed, but a key hasn't been configured. Please create a new key, or restore android.keystore."
    new "RAPT está instalado, pero la clave aún no se ha configurado. Por favor crea una nueva clave, o restaura android.keystore."

    # android.rpy:34
    old "The current project has not been configured. Use \"Configure\" to configure it before building."
    new "El proyecto actual no se ha configurado. Usa \"Configurar\" para configurarlo antes de construirlo."

    # android.rpy:35
    old "Choose \"Build\" to build the current project, or attach an Android device and choose \"Build & Install\" to build and install it on the device."
    new "Selecciona \"Construir\" para construir el proyecto actual, o conecta un dispositivo Android y selecciona \"Construir & instalar\" para construirlo e instalarlo en el dispositivo."

    # android.rpy:37
    old "Attempts to emulate an Android phone.\n\nTouch input is emulated through the mouse, but only when the button is held down. Escape is mapped to the menu button, and PageUp is mapped to the back button."
    new "Intenta emular un teléfono Android. \n\nLa entrada táctil se emula mediante el ratón, pero solo cuando el botón se mantiene pulsado. Escape está asignado al botón de menú, y Av.Pág está asignado al botón Atrás."

    # android.rpy:38
    old "Attempts to emulate an Android tablet.\n\nTouch input is emulated through the mouse, but only when the button is held down. Escape is mapped to the menu button, and PageUp is mapped to the back button."
    new "Intenta emular una tablet Android. \n\nLa entrada táctil se emula mediante el ratón, pero solo cuando el botón se mantiene pulsado. Escape está asignado al botón de menú, y Av.Pág está asignado al botón Atrás."

    # android.rpy:39
    old "Attempts to emulate a televison-based Android console, like the OUYA or Fire TV.\n\nController input is mapped to the arrow keys, Enter is mapped to the select button, Escape is mapped to the menu button, and PageUp is mapped to the back button."
    new "Intenta emular una consola Android basada en televisión, como OUYA o Fire TV.\n\nPara el control se usan las flechas, Intro está asignado al botón select. Escape está asignado al botón de menú, y Av.Pág está asignado al botón Atrás."

    # android.rpy:41
    old "Downloads and installs the Android SDK and supporting packages. Optionally, generates the keys required to sign the package."
    new "Descarga e instala el SDK de android y los paquetes de soporte. Opcionalmente, genera la clave necesaria para firmar el paquete."

    # android.rpy:42
    old "Configures the package name, version, and other information about this project."
    new "Configura el nombre del paquete, la versión, y otra información de este proyecto."

    # android.rpy:43
    old "Opens the file containing the Google Play keys in the editor.\n\nThis is only needed if the application is using an expansion APK. Read the documentation for more details."
    new "Abre el archivo que contiene las claves de Google Play en el editor. \n\nEsto sólo es necesario si la aplicación usa una expansión APK. Para más información lee la documentación."

    # android.rpy:44
    old "Builds the Android package."
    new "Construye el paquete de Android."

    # android.rpy:45
    old "Builds the Android package, and installs it on an Android device connected to your computer."
    new "Construye el paquete de Android y lo instala en un dispositivo Android conectado al ordenador."

    # android.rpy:46
    old "Builds the Android package, installs it on an Android device connected to your computer, then launches the app on your device."
    new "Construye un paquete para Android, lo instala en un dispositivo conectado al ordenador y luego ejecuta la aplicación en el dispositivo."

    # android.rpy:48
    old "Connects to an Android device running ADB in TCP/IP mode."
    new "Conecta a un dispositivo Android ejecutando ADB en modo TCP/IP."

    # android.rpy:49
    old "Disconnects from an Android device running ADB in TCP/IP mode."
    new "Desconecta de un dispositivo Android ejecutando ADB en modo TCP/IP."

    # android.rpy:50
    old "Retrieves the log from the Android device and writes it to a file."
    new "Recupera el registro del dispositivo Android y lo escribe en un archivo."

    # android.rpy:244
    old "Copying Android files to distributions directory."
    new "Copiando archivos Android al directorio de distribuciones."

    # android.rpy:308
    old "Android: [project.current.display_name!q]"
    new "Android: [project.current.display_name!q]"

    # android.rpy:328
    old "Emulation:"
    new "Emulación:"

    # android.rpy:337
    old "Phone"
    new "Teléfono"

    # android.rpy:341
    old "Tablet"
    new "Tablet"

    # android.rpy:345
    old "Television"
    new "Televisión"

    # android.rpy:357
    old "Build:"
    new "Construir:"

    # android.rpy:365
    old "Install SDK & Create Keys"
    new "Instalar SDK y Crear claves"

    # android.rpy:369
    old "Configure"
    new "Configurar"

    # android.rpy:373
    old "Build Package"
    new "Construir paquete"

    # android.rpy:377
    old "Build & Install"
    new "Construir e Instalar"

    # android.rpy:381
    old "Build, Install & Launch"
    new "Construir, instalar y ejecutar"

    # android.rpy:392
    old "Other:"
    new "Otros:"

    # android.rpy:400
    old "Remote ADB Connect"
    new "Conexión remota ADB"

    # android.rpy:404
    old "Remote ADB Disconnect"
    new "Desconexión remota ADB"

    # android.rpy:408
    old "Logcat"
    new "Logcat"

    # android.rpy:441
    old "Before packaging Android apps, you'll need to download RAPT, the Ren'Py Android Packaging Tool. Would you like to download RAPT now?"
    new "Antes de empaquetar apps para Android, vas a necesitar descargar RAPT (Ren'Py Android Packaging Tool). ¿Quieres descargar RAPT ahora?"

    # android.rpy:500
    old "Remote ADB Address"
    new "Dirección remota ADB"

    # android.rpy:500
    old "Please enter the IP address and port number to connect to, in the form \"192.168.1.143:5555\". Consult your device's documentation to determine if it supports remote ADB, and if so, the address and port to use."
    new "Por favor introduce la dirección IP y el número de puerto para conectarte, con el formato \"192.168.1.143:5555\". Consulta la documentación de tu dispositivo para averiguar si es compatible con ADB remoto, y si es así, la dirección y el puerto a utilizar."

    # android.rpy:512
    old "Invalid remote ADB address"
    new "Dirección remota ADB no válida"

    # android.rpy:512
    old "The address must contain one exactly one ':'."
    new "La dirección debe contener exactamente un ':'."

    # android.rpy:516
    old "The host may not contain whitespace."
    new "El host no puede contener espacios en blanco."

    # android.rpy:522
    old "The port must be a number."
    new "El puerto debe ser un número."

    # android.rpy:548
    old "Retrieving logcat information from device."
    new "Recuperando la información 'logcat' del dispositivo."

    # choose_directory.rpy:87
    old "Ren'Py was unable to run python with tkinter to choose the directory. Please install the python-tk or tkinter package."
    new "Ren'Py fue incapaz de ejecutar python con tkinter para elegir el directorio. Por favor instala el paquete python-tk o tkinter."

    # choose_directory.rpy:104
    old "The selected projects directory is not writable."
    new "El directorio de proyectos seleccionado no puede ser escrito"

    # choose_theme.rpy:303
    old "Could not change the theme. Perhaps options.rpy was changed too much."
    new "No se puede cambiar el tema. Quizás options.rpy ha sufrido muchos cambios."

    # choose_theme.rpy:370
    old "Planetarium"
    new "Planetarium"

    # choose_theme.rpy:425
    old "Choose Theme"
    new "Elegir tema"

    # choose_theme.rpy:438
    old "Theme"
    new "Tema"

    # choose_theme.rpy:463
    old "Color Scheme"
    new "Combinación de colores"

    # choose_theme.rpy:495
    old "Continue"
    new "Continuar"

    # consolecommand.rpy:84
    old "INFORMATION"
    new "INFORMACIÓN"

    # consolecommand.rpy:84
    old "The command is being run in a new operating system console window."
    new "El comando se está ejecutando en una nueva ventana de la consola del sistema operativo."

    # distribute.rpy:444
    old "Scanning project files..."
    new "Escaneando archivos del proyecto..."

    # distribute.rpy:460
    old "Building distributions failed:\n\nThe build.directory_name variable may not include the space, colon, or semicolon characters."
    new "Ha fallado la construcción de distribuciones:\n\nLa variable build.directory_name no puede incluir espacios, dos puntos, ni punto y coma."

    # distribute.rpy:505
    old "No packages are selected, so there's nothing to do."
    new "Ningún paquete seleccionado. No hay nada que hacer."

    # distribute.rpy:517
    old "Scanning Ren'Py files..."
    new "Escaneando los archivos de Ren'Py..."

    # distribute.rpy:572
    old "All packages have been built.\n\nDue to the presence of permission information, unpacking and repacking the Linux and Macintosh distributions on Windows is not supported."
    new "Se han construido todos los paquetes.\n\nDebido a la presencia de información de permisos, desempaquetar y reempaquetar las distribuciones para Linux y Macintosh no es compatible en Windows."

    # distribute.rpy:755
    old "Archiving files..."
    new "Archivando archivos..."

    # distribute.rpy:1068
    old "Unpacking the Macintosh application for signing..."
    new "Desempaquetando la aplicación Macintosh para firmar..."

    # distribute.rpy:1078
    old "Signing the Macintosh application...\n(This may take a long time.)"
    new "Firmando la aplicación para Macintosh...\n(Esto puede tardar mucho tiempo)"

    # distribute.rpy:1100
    old "Creating the Macintosh DMG..."
    new "Creando el DMG Macintosh..."

    # distribute.rpy:1109
    old "Signing the Macintosh DMG..."
    new "Firmando el DMG Macintosh..."

    # distribute.rpy:1304
    old "Writing the [variant] [format] package."
    new "Escribiendo el paquete [format] para [variant]."

    # distribute.rpy:1317
    old "Making the [variant] update zsync file."
    new "Creando el archivo de actualización zsync para [variant]."

    # distribute.rpy:1427
    old "Processed {b}[complete]{/b} of {b}[total]{/b} files."
    new "Procesados {b}[complete]{/b} de {b}[total]{/b} archivos."

    # distribute_gui.rpy:157
    old "Build Distributions: [project.current.display_name!q]"
    new "Construir distribuciones: [project.current.display_name!q]"

    # distribute_gui.rpy:171
    old "Directory Name:"
    new "Nombre de la carpeta:"

    # distribute_gui.rpy:175
    old "Executable Name:"
    new "Nombre del ejecutable:"

    # distribute_gui.rpy:185
    old "Actions:"
    new "Acciones:"

    # distribute_gui.rpy:193
    old "Edit options.rpy"
    new "Editar options.rpy"

    # distribute_gui.rpy:194
    old "Add from clauses to calls, once"
    new "Añadir cláusulas 'from' a 'calls', una vez"

    # distribute_gui.rpy:195
    old "Refresh"
    new "Recargar"

    # distribute_gui.rpy:199
    old "Upload to itch.io"
    new "Cargar a itch.io"

    # distribute_gui.rpy:215
    old "Build Packages:"
    new "Construir Paquetes:"

    # distribute_gui.rpy:234
    old "Options:"
    new "Opciones:"

    # distribute_gui.rpy:239
    old "Build Updates"
    new "Construir actualizaciones"

    # distribute_gui.rpy:241
    old "Add from clauses to calls"
    new "Añadir cláusulas 'from' a 'calls'"

    # distribute_gui.rpy:242
    old "Force Recompile"
    new "Forzar Recompilación"

    # distribute_gui.rpy:246
    old "Build"
    new "Construir"

    # distribute_gui.rpy:250
    old "Adding from clauses to call statements that do not have them."
    new "Añadiendo cláusulas 'from' a las sentencias 'call' que no las tienen."

    # distribute_gui.rpy:271
    old "Errors were detected when running the project. Please ensure the project runs without errors before building distributions."
    new "Se detectaron errores al ejecutar el proyecto. Por favor asegúrate de que el proyecto se ejecuta sin errores antes de construir distibuciones."

    # distribute_gui.rpy:288
    old "Your project does not contain build information. Would you like to add build information to the end of options.rpy?"
    new "Tu proyecto no tiene información de construcción. ¿Te gustaría añadir la información de construcción al final del archivo options.rpy?"

    # dmgcheck.rpy:50
    old "Ren'Py is running from a read only folder. Some functionality will not work."
    new "Ren'Py se ejecuta en una carpeta de solo lectura. Algunas funciones no disponibles."

    # dmgcheck.rpy:50
    old "This is probably because Ren'Py is running directly from a Macintosh drive image. To fix this, quit this launcher, copy the entire %s folder somewhere else on your computer, and run Ren'Py again."
    new "Esto sucede probablemente porque Ren'Py se ejecuta directamente desde una imagen de disco Macintosh. Cierra este lanzador, copia toda la carpeta %s en otro lugar del ordenador y ejecuta Ren'Py de nuevo."

    # editor.rpy:152
    old "(Recommended) A modern and approachable text editor."
    new "(Recomendado) Editor de texto moderno y accesible."

    # editor.rpy:164
    old "Up to 150 MB download required."
    new "Requiere descargar hasta 150 MB."

    # editor.rpy:178
    old "A mature editor. Editra lacks the IME support required for Chinese, Japanese, and Korean text input."
    new "Un editor maduro. Editra carece de soporte IME, necesario para el texto en chino, japonés y coreano."

    # editor.rpy:179
    old "A mature editor. Editra lacks the IME support required for Chinese, Japanese, and Korean text input. On Linux, Editra requires wxPython."
    new "Un editor maduro. Editra carece de soporte IME, necesario para el texto en chino, japonés y coreano. En Linux, Editra necesita wxPython."

    # editor.rpy:195
    old "This may have occured because wxPython is not installed on this system."
    new "Esto puede haber ocurrido porque wxPython no está instalado en este sistema."

    # editor.rpy:197
    old "Up to 22 MB download required."
    new "Requiere descargar hasta 22 MB."

    # editor.rpy:210
    old "A mature editor that requires Java."
    new "Un editor muy maduro que requiere Java."

    # editor.rpy:210
    old "1.8 MB download required."
    new "Requiere descargar 1.8 MB."

    # editor.rpy:210
    old "This may have occured because Java is not installed on this system."
    new "Esto puede haber ocurrido porque Java no está instalado en este sistema"

    # editor.rpy:219
    old "System Editor"
    new "Editor del sistema"

    # editor.rpy:219
    old "Invokes the editor your operating system has associated with .rpy files."
    new "Usar el editor de su sistema operativo para que se asocie con los archivos .rpy."

    # editor.rpy:235
    old "None"
    new "Ninguno"

    # editor.rpy:235
    old "Prevents Ren'Py from opening a text editor."
    new "Evita que Ren'Py abra un editor de texto."

    # editor.rpy:338
    old "Edit [text]."
    new "Editar [text]."

    # editor.rpy:387
    old "An exception occured while launching the text editor:\n[exception!q]"
    new "Ha ocurrido una excepción mientras se ejecutaba el editor de texto:\\[exception!q]"

    # editor.rpy:519
    old "Select Editor"
    new "Seleccionar Editor"

    # editor.rpy:534
    old "A text editor is the program you'll use to edit Ren'Py script files. Here, you can select the editor Ren'Py will use. If not already present, the editor will be automatically downloaded and installed."
    new "Un editor de texto es el programa que vas a utilizar para editar los scripts de Ren'Py. Aquí, puedes seleccionar el editor que Ren'Py usará. Si no está disponible, el editor se descargará e instalará automáticamente."

    # front_page.rpy:35
    old "Open [text] directory."
    new "Abrir directorio [text]."

    # front_page.rpy:91
    old "PROJECTS:"
    new "PROYECTOS:"

    # front_page.rpy:93
    old "refresh"
    new "recargar"

    # front_page.rpy:120
    old "+ Create New Project"
    new "+ Crear un proyecto nuevo"

    # front_page.rpy:130
    old "Launch Project"
    new "Ejecutar proyecto"

    # front_page.rpy:147
    old "[p.name!q] (template)"
    new "[p.name!q] (plantilla)"

    # front_page.rpy:149
    old "Select project [text]."
    new "Seleccionar proyecto [text]."

    # front_page.rpy:165
    old "Tutorial"
    new "Tutorial"

    # front_page.rpy:166
    old "The Question"
    new "The Question"

    # front_page.rpy:182
    old "Active Project"
    new "Proyecto activo"

    # front_page.rpy:190
    old "Open Directory"
    new "Abrir carpeta"

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
    new "Editar archivo"

    # front_page.rpy:215
    old "Open project"
    new "Abrir proyecto"

    # front_page.rpy:217
    old "All script files"
    new "Todos los scripts"

    # front_page.rpy:221
    old "Actions"
    new "Acciones"

    # front_page.rpy:230
    old "Navigate Script"
    new "Navegar por los scripts"

    # front_page.rpy:231
    old "Check Script (Lint)"
    new "Comprobar script (Lint)"

    # front_page.rpy:234
    old "Change/Update GUI"
    new "Cambiar/Actualizar GUI"

    # front_page.rpy:236
    old "Change Theme"
    new "Cambiar tema"

    # front_page.rpy:239
    old "Delete Persistent"
    new "Eliminar datos persistentes"

    # front_page.rpy:248
    old "Build Distributions"
    new "Construir distribuciones"

    # front_page.rpy:250
    old "Android"
    new "Android"

    # front_page.rpy:251
    old "iOS"
    new "iOS"

    # front_page.rpy:252
    old "Generate Translations"
    new "Generar traducciones"

    # front_page.rpy:253
    old "Extract Dialogue"
    new "Extraer diálogos"

    # front_page.rpy:270
    old "Checking script for potential problems..."
    new "Comprobando potenciales problemas en el script..."

    # front_page.rpy:285
    old "Deleting persistent data..."
    new "Eliminando datos persistentes..."

    # front_page.rpy:293
    old "Recompiling all rpy files into rpyc files..."
    new "Recompilando todos los archivos rpy en archivos rpyc..."

    # gui7.rpy:252
    old "Select Accent and Background Colors"
    new "Selecciona colores de fondo y énfasis"

    # gui7.rpy:266
    old "Please click on the color scheme you wish to use, then click Continue. These colors can be changed and customized later."
    new "Haz clic en el esquema de color que quieres usar y haz clic en Continuar. Estos colores pueden ser cambiados y personalizados más tarde."

    # gui7.rpy:311
    old "{b}Warning{/b}\nContinuing will overwrite customized bar, button, save slot, scrollbar, and slider images.\n\nWhat would you like to do?"
    new "{b}Aviso{/b}\nSi continúas se sobreescribirán las barras, botones, huecos de partida grabada, barras de desplazamiento y controles deslizantes personalizados.\n\n¿Qué deseas hacer?"

    # gui7.rpy:311
    old "Choose new colors, then regenerate image files."
    new "Escoge los nuevos colores y luego regenera las imágenes."

    # gui7.rpy:311
    old "Regenerate the image files using the colors in gui.rpy."
    new "Regenera las imágenes usando los colores de gui.rpy."

    # gui7.rpy:331
    old "PROJECT NAME"
    new "NOMBRE DEL PROYECTO"

    # gui7.rpy:331
    old "Please enter the name of your project:"
    new "Por favor introduce el nombre de tu proyecto:"

    # gui7.rpy:339
    old "The project name may not be empty."
    new "El nombre del proyecto no puede estar vacío."

    # gui7.rpy:344
    old "[project_name!q] already exists. Please choose a different project name."
    new "[project_name!q] ya existe. Por favor elige un nombre diferente para el proyecto."

    # gui7.rpy:347
    old "[project_dir!q] already exists. Please choose a different project name."
    new "[project_dir!q] ya existe. Por favor elige un nombre diferente para el proyecto."

    # gui7.rpy:358
    old "What resolution should the project use? Although Ren'Py can scale the window up and down, this is the initial size of the window, the size at which assets should be drawn, and the size at which the assets will be at their sharpest.\n\nThe default of [default_size[0]]x[default_size[1]] is a reasonable compromise."
    new "¿Qué resolución debería usar el proyecto? Aunque Ren'Py puede escalar la ventana más grande o más pequeña, este es el tamaño inicial de la ventana, el tamaño en el que se deben dibujar las imágenes y el tamaño en el que serán más nítidas.\n\nEl valor predeterminado de [default_size[0]]x[default_size[1]] es un compromiso razonable."

    # gui7.rpy:358
    old "Custom. The GUI is optimized for a 16:9 aspect ratio."
    new "Personalizado. La GUI está optimizada para una proporción 16:9."

    # gui7.rpy:373
    old "WIDTH"
    new "ANCHURA"

    # gui7.rpy:373
    old "Please enter the width of your game, in pixels."
    new "Introduce la anchura de tu juego en píxeles."

    # gui7.rpy:378
    old "The width must be a number."
    new "La anchura debe ser un número."

    # gui7.rpy:380
    old "HEIGHT"
    new "ALTURA"

    # gui7.rpy:380
    old "Please enter the height of your game, in pixels."
    new "Introduce la altura de tu juego en píxeles."

    # gui7.rpy:385
    old "The height must be a number."
    new "La altura debe ser un número."

    # gui7.rpy:427
    old "Creating the new project..."
    new "Creando el nuevo proyecto..."

    # gui7.rpy:429
    old "Updating the project..."
    new "Actualizando el proyecto..."

    # interface.rpy:119
    old "Documentation"
    new "Documentación"

    # interface.rpy:120
    old "Ren'Py Website"
    new "Web de Ren'Py"

    # interface.rpy:121
    old "Ren'Py Games List"
    new "Lista de juegos Ren'Py"

    # interface.rpy:129
    old "update"
    new "actualizar"

    # interface.rpy:131
    old "preferences"
    new "preferencias"

    # interface.rpy:132
    old "quit"
    new "salir"

    # interface.rpy:136
    old "Ren'Py Sponsor Information"
    new "Información de patrocinadores de Ren'Py"

    # interface.rpy:258
    old "Due to package format limitations, non-ASCII file and directory names are not allowed."
    new "Debido a las limitaciones del formato de paquete, no se permite el uso de nombres de archivos y carpetas que no sean ASCII"

    # interface.rpy:354
    old "ERROR"
    new "ERROR"

    # interface.rpy:400
    old "Text input may not contain the {{ or [[ characters."
    new "La entrada de texto no puede contener los caracteres {{ o [[."

    # interface.rpy:405
    old "File and directory names may not contain / or \\."
    new "Los nombres de archivos y carpetas no pueden contener / o \\."

    # interface.rpy:411
    old "File and directory names must consist of ASCII characters."
    new "Los nombres de archivos y carpetas deben ser caracteres ASCII."

    # interface.rpy:479
    old "PROCESSING"
    new "PROCESANDO"

    # interface.rpy:496
    old "QUESTION"
    new "PREGUNTA"

    # interface.rpy:509
    old "CHOICE"
    new "SELECCIONA"

    # ios.rpy:28
    old "To build iOS packages, please download renios, unzip it, and place it into the Ren'Py directory. Then restart the Ren'Py launcher."
    new "Para construir paquetes para iOS, por favor descarga renios, descomprímelo, y colócalo dentro de la carpeta de Ren'Py. Después reinicia el launcher de Ren'Py."

    # ios.rpy:29
    old "The directory in where Xcode projects will be placed has not been selected. Choose 'Select Directory' to select it."
    new "El directorio donde se colocarán los proyectos de Xcode no se ha seleccionado. Elige 'Seleccionar directorio' para seleccionarlo."

    # ios.rpy:30
    old "There is no Xcode project corresponding to the current Ren'Py project. Choose 'Create Xcode Project' to create one."
    new "No hay proyecto de Xcode correspondiente al proyecto de Ren'Py actual. Elige 'Crear proyecto de Xcode' para crear uno."

    # ios.rpy:31
    old "An Xcode project exists. Choose 'Update Xcode Project' to update it with the latest game files, or use Xcode to build and install it."
    new "Existe un proyecto de Xcode. Elige 'Actualizar proyecto de Xcode' para actualizarlo con los últimos archivos del juego, o usa Xcode para construirlo e instalarlo."

    # ios.rpy:33
    old "Attempts to emulate an iPhone.\n\nTouch input is emulated through the mouse, but only when the button is held down."
    new "Intenta emular un iPhone.\n\nLa entrada táctil se emula a través del ratón, pero solo cuando se mantiene pulsado el botón."

    # ios.rpy:34
    old "Attempts to emulate an iPad.\n\nTouch input is emulated through the mouse, but only when the button is held down."
    new "Intenta emular un iPad.\n\nLa entrada táctil se emula a través del ratón, pero solo cuando se mantiene pulsado el botón."

    # ios.rpy:36
    old "Selects the directory where Xcode projects will be placed."
    new "Selecciona el directorio donde se colocarán los proyectos de Xcode."

    # ios.rpy:37
    old "Creates an Xcode project corresponding to the current Ren'Py project."
    new "Crea un proyecto de Xcode correspondiente al proyecto de Ren'Py actual."

    # ios.rpy:38
    old "Updates the Xcode project with the latest game files. This must be done each time the Ren'Py project changes."
    new "Actualiza el proyecto de Xcode con los últimos archivos del juego. Esto debe hacerse cada vez que el proyecto de Ren'Py cambie."

    # ios.rpy:39
    old "Opens the Xcode project in Xcode."
    new "Abre el proyecto de Xcode en Xcode."

    # ios.rpy:41
    old "Opens the directory containing Xcode projects."
    new "Abre el directorio que contiene los proyectos de Xcode."

    # ios.rpy:126
    old "The Xcode project already exists. Would you like to rename the old project, and replace it with a new one?"
    new "El proyecto de Xcode ya existe. ¿Quieres cambiar el nombre del antiguo proyecto, y sustituirlo por uno nuevo?"

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
    new "Selecciona directorio para los proyectos de Xcode"

    # ios.rpy:268
    old "Create Xcode Project"
    new "Crea Proyecto de Xcode"

    # ios.rpy:272
    old "Update Xcode Project"
    new "Actualiza Proyecto de Xcode"

    # ios.rpy:277
    old "Launch Xcode"
    new "Ejecuta Xcode"

    # ios.rpy:312
    old "Open Xcode Projects Directory"
    new "Abre directorio de proyectos de Xcode"

    # ios.rpy:345
    old "Before packaging iOS apps, you'll need to download renios, Ren'Py's iOS support. Would you like to download renios now?"
    new "Antes de empaquetar aplicaciones de iOS, tendrás que descargar renios, el soporte de iOS para Ren'Py. ¿Quieres descargar renios ahora?"

    # ios.rpy:354
    old "XCODE PROJECTS DIRECTORY"
    new "DIRECTORIO DE PROYECTOS DE XCODE"

    # ios.rpy:354
    old "Please choose the Xcode Projects Directory using the directory chooser.\n{b}The directory chooser may have opened behind this window.{/b}"
    new "Por favor elige el directorio de proyectos de Xcode usando el selector de directorio.\n{b}El selector de directorio puede haberse abierto detrás de esta ventana.{/b}"

    # ios.rpy:359
    old "Ren'Py has set the Xcode Projects Directory to:"
    new "Ren'Py ha establecido el directorio de proyectos de Xcode en:"

    # itch.rpy:60
    old "The built distributions could not be found. Please choose 'Build' and try again."
    new "Las distribuciones compiladas no se pudieron encontrar. Elige 'Construir' y vuelve a intentarlo."

    # itch.rpy:98
    old "No uploadable files were found. Please choose 'Build' and try again."
    new "No se encontraron archivos para cargar. Elige 'Construir' y vuelve a intentarlo."

    # itch.rpy:106
    old "The butler program was not found."
    new "No se encontró el programa 'butler'."

    # itch.rpy:106
    old "Please install the itch.io app, which includes butler, and try again."
    new "Instala la aplicación itch.io, que incluye 'butler', y vuelve a intentarlo."

    # itch.rpy:115
    old "The name of the itch project has not been set."
    new "El nombre del proyecto de itch no ha sido establecido."

    # itch.rpy:115
    old "Please {a=https://itch.io/game/new}create your project{/a}, then add a line like \n{vspace=5}define build.itch_project = \"user-name/game-name\"\n{vspace=5} to options.rpy."
    new "{a=https://itch.io/game/new}Crea tu proyecto{/a} y luego añade una línea como \n{vspace=5}define build.itch_project = \"nombre-de-usuario/nombre-del-juego\"\n{vspace=5} en 'options.rpy'."

    # mobilebuild.rpy:109
    old "{a=%s}%s{/a}"
    new "{a=%s}%s{/a}"

    # navigation.rpy:168
    old "Navigate: [project.current.display_name!q]"
    new "Navegar: [project.current.display_name!q]"

    # navigation.rpy:178
    old "Order: "
    new "Orden: "

    # navigation.rpy:179
    old "alphabetical"
    new "alfabético"

    # navigation.rpy:181
    old "by-file"
    new "por archivo"

    # navigation.rpy:183
    old "natural"
    new "natural"

    # navigation.rpy:195
    old "Category:"
    new "Categoría:"

    # navigation.rpy:198
    old "files"
    new "archivos"

    # navigation.rpy:199
    old "labels"
    new "labels"

    # navigation.rpy:200
    old "defines"
    new "defines"

    # navigation.rpy:201
    old "transforms"
    new "transforms"

    # navigation.rpy:202
    old "screens"
    new "pantallas"

    # navigation.rpy:203
    old "callables"
    new "callables"

    # navigation.rpy:204
    old "TODOs"
    new "TODOs"

    # navigation.rpy:243
    old "+ Add script file"
    new "+ Añadir archivo de script"

    # navigation.rpy:251
    old "No TODO comments found.\n\nTo create one, include \"# TODO\" in your script."
    new "No se han encontrado comentarios \"TODO\". Para crear uno, incluye \"# TODO\" en tu script."

    # navigation.rpy:258
    old "The list of names is empty."
    new "La lista de nombres está vacía."

    # new_project.rpy:38
    old "New GUI Interface"
    new "Nueva interfaz GUI"

    # new_project.rpy:48
    old "Both interfaces have been translated to your language."
    new "Ambas interfaces han sido traducidas a tu idioma."

    # new_project.rpy:50
    old "Only the new GUI has been translated to your language."
    new "Solo la nueva GUI ha sido traducida a tu idioma."

    # new_project.rpy:52
    old "Only the legacy theme interface has been translated to your language."
    new "Solo la interfaz del tema antiguo ha sido traducida a tu idioma.."

    # new_project.rpy:54
    old "Neither interface has been translated to your language."
    new "Ninguna interfaz ha sido traducida a tu idioma."

    # new_project.rpy:63
    old "The projects directory could not be set. Giving up."
    new "No se puede establecer el directorio de proyectos. Abandonando."

    # new_project.rpy:71
    old "You will be creating an [new_project_language]{#this substitution may be localized} language project. Change the launcher language in preferences to create a project in another language."
    new "Vas a crear un proyecto en idioma [new_project_language]. Cambia el idioma del lanzador en preferencias para crear un proyecto en otro idioma."

    # new_project.rpy:79
    old "Which interface would you like to use? The new GUI has a modern look, supports wide screens and mobile devices, and is easier to customize. Legacy themes might be necessary to work with older example code.\n\n[language_support!t]\n\nIf in doubt, choose the new GUI, then click Continue on the bottom-right."
    new "¿Qué interfaz te gustaría usar? La nueva GUI tiene un aspecto moderno, admite pantallas anchas y dispositivos móviles, y es más fácil de personalizar. Es posible que los temas antiguos sean necesarios para trabajar con código anterior.\n\n[language_support!t]\n\nSi tienes dudas, elige la nueva GUI, luego haz clic en Continuar en la parte inferior derecha."

    # new_project.rpy:79
    old "Legacy Theme Interface"
    new "Interfaz de temas antiguos"

    # new_project.rpy:100
    old "Choose Project Template"
    new "Elige una plantilla para el proyecto"

    # new_project.rpy:118
    old "Please select a template to use for your new project. The template sets the default font and the user interface language. If your language is not supported, choose 'english'."
    new "Por favor selecciona una plantilla para usar en tu nuevo proyecto. La plantilla establece la fuente predeterminada y el idioma de la interfaz de usuario, Si tu idioma no está soportado, elige \"English\"."

    # preferences.rpy:73
    old "Launcher Preferences"
    new "Preferencias del lanzador"

    # preferences.rpy:94
    old "Projects Directory:"
    new "Carpeta de proyectos:"

    # preferences.rpy:101
    old "[persistent.projects_directory!q]"
    new "[persistent.projects_directory!q]"

    # preferences.rpy:103
    old "Projects directory: [text]"
    new "Directorio de proyectos: [text]"

    # preferences.rpy:105
    old "Not Set"
    new "No establecido"

    # preferences.rpy:120
    old "Text Editor:"
    new "Editor de texto:"

    # preferences.rpy:126
    old "Text editor: [text]"
    new "Editor de texto: [text]"

    # preferences.rpy:142
    old "Update Channel:"
    new "Canal de actualización"

    # preferences.rpy:162
    old "Navigation Options:"
    new "Opciones de navegación:"

    # preferences.rpy:166
    old "Include private names"
    new "Incluir nombres privados"

    # preferences.rpy:167
    old "Include library names"
    new "Incluir nombres de bibliotecas"

    # preferences.rpy:177
    old "Launcher Options:"
    new "Opciones del lanzador:"

    # preferences.rpy:181
    old "Hardware rendering"
    new "Renderización por hardware"

    # preferences.rpy:182
    old "Show edit file section"
    new "Mostrar la sección 'Editar archivo'"

    # preferences.rpy:183
    old "Large fonts"
    new "Fuentes grandes"

    # preferences.rpy:186
    old "Console output"
    new "Salida de la consola"

    # preferences.rpy:190
    old "Force new tutorial"
    new "Fuerza el nuevo tutorial"

    # preferences.rpy:194
    old "Legacy options"
    new "Opciones antiguas"

    # preferences.rpy:197
    old "Show templates"
    new "Mostrar plantillas"

    # preferences.rpy:199
    old "Sponsor message"
    new "Mensaje de patrocinadores"

    # preferences.rpy:219
    old "Open launcher project"
    new "Abrir el lanzador"

    # preferences.rpy:233
    old "Language:"
    new "Idioma:"

    # project.rpy:49
    old "After making changes to the script, press shift+R to reload your game."
    new "Después de hacer cambios a un script, presiona Mayús+R para recargar tu juego."

    # project.rpy:49
    old "Press shift+O (the letter) to access the console."
    new "Presiona Mayús+O (la letra) para acceder a la consola."

    # project.rpy:49
    old "Press shift+D to access the developer menu."
    new "Presiona Mayús+D para acceder al menú de desarrollador."

    # project.rpy:49
    old "Have you backed up your projects recently?"
    new "¿Has respaldado tus proyectos recientemente?"

    # project.rpy:280
    old "Launching the project failed."
    new "La ejecución del proyecto ha fallado."

    # project.rpy:280
    old "Please ensure that your project launches normally before running this command."
    new "Por favor, asegúrate de que tu proyecto se ejecuta normalmente antes de ejecutar este comando."

    # project.rpy:296
    old "Ren'Py is scanning the project..."
    new "Ren'Py está escaneando el proyecto..."

    # project.rpy:728
    old "Launching"
    new "Ejecutando"

    # project.rpy:762
    old "PROJECTS DIRECTORY"
    new "CARPETA DEL PROYECTO"

    # project.rpy:762
    old "Please choose the projects directory using the directory chooser.\n{b}The directory chooser may have opened behind this window.{/b}"
    new "Por favor elige la carpeta del proyecto usando el selector de proyecto. \n{b}El selector de carpetas puede haberse abierto detrás de esta ventana."

    # project.rpy:762
    old "This launcher will scan for projects in this directory, will create new projects in this directory, and will place built projects into this directory."
    new "El lanzador buscará proyectos en esta carpeta, creará nuevos proyectos en esta carpeta, y colocará los proyectos en este directorio."

    # project.rpy:767
    old "Ren'Py has set the projects directory to:"
    new "Ren'Py ha establecido el directorio de proyectos:"

    # translations.rpy:91
    old "Translations: [project.current.display_name!q]"
    new "Traducciones: [project.current.display_name!q]"

    # translations.rpy:132
    old "The language to work with. This should only contain lower-case ASCII characters and underscores."
    new "El idioma en que trabajar. Debe contener solo caracteres ASCII minúsculos y guiones bajos."

    # translations.rpy:158
    old "Generate empty strings for translations"
    new "Generar cadenas vacías para las traducciones"

    # translations.rpy:176
    old "Generates or updates translation files. The files will be placed in game/tl/[persistent.translate_language!q]."
    new "Genera o actualiza los archivos de traducción. Los archivos se colocarán en game/tl/[persistent.translate_language!q]."

    # translations.rpy:196
    old "Extract String Translations"
    new "Extraer cadenas traducidas"

    # translations.rpy:198
    old "Merge String Translations"
    new "Fusionar cadenas traducidas"

    # translations.rpy:203
    old "Replace existing translations"
    new "Reemplazar traducciones existentes"

    # translations.rpy:204
    old "Reverse languages"
    new "Invertir idiomas"

    # translations.rpy:208
    old "Update Default Interface Translations"
    new "Actualizar traducciones de la interfaz por defecto"

    # translations.rpy:228
    old "The extract command allows you to extract string translations from an existing project into a temporary file.\n\nThe merge command merges extracted translations into another project."
    new "El comando 'extrae' permite extraer las cadenas traducidas de un proyecto existente en un archivo temporal.\n\nEl comando 'fusiona' introduce las traducciones extraídas en otro proyecto."

    # translations.rpy:252
    old "Ren'Py is generating translations...."
    new "Ren'Py está generando las traducciones..."

    # translations.rpy:263
    old "Ren'Py has finished generating [language] translations."
    new "Ren'Py ha terminado de generar las traducciones en [language]"

    # translations.rpy:276
    old "Ren'Py is extracting string translations..."
    new "Ren'Py está extrayendo las cadenas traducidas..."

    # translations.rpy:279
    old "Ren'Py has finished extracting [language] string translations."
    new "Ren'Py ha terminado de extrar las cadenas traducidas en [language]."

    # translations.rpy:299
    old "Ren'Py is merging string translations..."
    new "Ren'Py está fusionando las cadenas traducidas..."

    # translations.rpy:302
    old "Ren'Py has finished merging [language] string translations."
    new "Ren'Py ha terminado de fusionar las cadenas traducidas en [language]."

    # translations.rpy:313
    old "Updating default interface translations..."
    new "Actualizando las traducciones por defecto de la interfaz..."

    # translations.rpy:342
    old "Extract Dialogue: [project.current.display_name!q]"
    new "Extraer diálogos de: [project.current.display_name!q]"

    # translations.rpy:358
    old "Format:"
    new "Formato:"

    # translations.rpy:366
    old "Tab-delimited Spreadsheet (dialogue.tab)"
    new "Hoja delimitada por tabuladores (dialogue.tab)"

    # translations.rpy:367
    old "Dialogue Text Only (dialogue.txt)"
    new "Diálogo en solo texto (dialogue.txt)"

    # translations.rpy:380
    old "Strip text tags from the dialogue."
    new "Elimina etiquetas de texto del diálogo."

    # translations.rpy:381
    old "Escape quotes and other special characters."
    new "Escapa las comillas y otros caracteres especiales."

    # translations.rpy:382
    old "Extract all translatable strings, not just dialogue."
    new "Extraer todas las cadenas traducibles, no solo el diálogo."

    # translations.rpy:410
    old "Ren'Py is extracting dialogue...."
    new "Ren'Py está extrayendo los diálogos..."

    # translations.rpy:414
    old "Ren'Py has finished extracting dialogue. The extracted dialogue can be found in dialogue.[persistent.dialogue_format] in the base directory."
    new "Ren'Py ha terminado de extraer el diálogo. El texto se encuentra en dialogue.[persistent.dialogue_format] en el directorio base."

    # updater.rpy:75
    old "Select Update Channel"
    new "Selecciona el Canal de Actualización"

    # updater.rpy:86
    old "The update channel controls the version of Ren'Py the updater will download. Please select an update channel:"
    new "El canal de actualización controla la versión de Ren'Py que el actualizador descargará. Selecciona un canal de actualización:"

    # updater.rpy:91
    old "Release"
    new "Estable"

    # updater.rpy:97
    old "{b}Recommended.{/b} The version of Ren'Py that should be used in all newly-released games."
    new "{b}Recomendado.{/b} La versión the Ren'Py que se recomienda usar en todos los juegos recién liberados."

    # updater.rpy:102
    old "Prerelease"
    new "Preliminar"

    # updater.rpy:108
    old "A preview of the next version of Ren'Py that can be used for testing and taking advantage of new features, but not for final releases of games."
    new "Una vista previa de la próxima versión de Ren'Py que puede ser utilizada para probar y aprovechar las nuevas características, pero no para las versiones finales de los juegos."

    # updater.rpy:114
    old "Experimental"
    new "Experimental"

    # updater.rpy:120
    old "Experimental versions of Ren'Py. You shouldn't select this channel unless asked by a Ren'Py developer."
    new "Versiones experimentales de Ren'Py. No debes seleccionar el canal a menos que te lo pida un desarrollador de Ren'Py."

    # updater.rpy:126
    old "Nightly"
    new "Nocturna"

    # updater.rpy:132
    old "The bleeding edge of Ren'Py development. This may have the latest features, or might not run at all."
    new "Versión de desarrollo de Ren'Py. Puede tener las últimas características o puede no funcionar."

    # updater.rpy:152
    old "An error has occured:"
    new "Ha sucedido un error:"

    # updater.rpy:154
    old "Checking for updates."
    new "Buscando actualizaciones."

    # updater.rpy:156
    old "Ren'Py is up to date."
    new "Ren'Py está actualizado."

    # updater.rpy:158
    old "[u.version] is now available. Do you want to install it?"
    new "[u.version] está disponible. ¿Quieres instalarla?"

    # updater.rpy:160
    old "Preparing to download the update."
    new "Preparando para descargar la actualización."

    # updater.rpy:162
    old "Downloading the update."
    new "Descargando la actualización."

    # updater.rpy:164
    old "Unpacking the update."
    new "Descomprimiendo la actualización."

    # updater.rpy:166
    old "Finishing up."
    new "Finalizando."

    # updater.rpy:168
    old "The update has been installed. Ren'Py will restart."
    new "La actualización se ha instalado. Ren'Py se reiniciará."

    # updater.rpy:170
    old "The update has been installed."
    new "La actualización se ha instalado."

    # updater.rpy:172
    old "The update was cancelled."
    new "Se ha cancelado la actualización."

    # updater.rpy:189
    old "Ren'Py Update"
    new "Actualizar Ren'Py"

    # updater.rpy:195
    old "Proceed"
    new "Continuar"

    # game/add_file.rpy:37
    old "The file name may not be empty."
    new "El nombre del archivo no puede estar vacío."

    # game/android.rpy:31
    old "A 64-bit/x64 Java 8 Development Kit is required to build Android packages on Windows. The JDK is different from the JRE, so it's possible you have Java without having the JDK.\n\nPlease {a=http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html}download and install the JDK{/a}, then restart the Ren'Py launcher."
    new "Se requiere un kit de desarrollo Java 8 de 64 bits/x64 para construir paquetes de Android en Windows. El JDK es diferente del JRE, por lo que es posible que tengas Java sin el JDK.\n\nPor favor, {a=http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html}descarga e instala el JDK{/a}, luego reinicie el launcher de Ren'Py."

    # game/android.rpy:50
    old "Selects the Debug build, which can be accessed through Android Studio. Changing between debug and release builds requires an uninstall from your device."
    new "Selecciona la versión de depuración, a la que se puedes acceder a través de Android Studio. Cambiar entre las compilaciones de depuración y estable requiere una desinstalación de su dispositivo."

    # game/android.rpy:51
    old "Selects the Release build, which can be uploaded to stores. Changing between debug and release builds requires an uninstall from your device."
    new "Selecciona la versión estable, que se puede cargar en las tiendas. Cambiar entre las compilaciones de depuración y estable requiere una desinstalación de su dispositivo."

    # game/androidstrings.rpy:7
    old "{} is not a directory."
    new "{} no es un directorio"

    # game/androidstrings.rpy:8
    old "{} does not contain a Ren'Py game."
    new "{} no contiene un juego de Ren'Py."

    # game/androidstrings.rpy:9
    old "Run configure before attempting to build the app."
    new "Ejecutar 'Configurar' antes de intentar construir la aplicación."

    # game/androidstrings.rpy:10
    old "Google Play support is enabled, but build.google_play_key is not defined."
    new "El soporte de Google Play está habilitado, pero build.google_play_key no está definido."

    # game/androidstrings.rpy:11
    old "Updating project."
    new "Actualizando proyecto"

    # game/androidstrings.rpy:12
    old "Creating assets directory."
    new "Creando directorio de recursos."

    # game/androidstrings.rpy:13
    old "Creating expansion file."
    new "Creando archivo de expansión."

    # game/androidstrings.rpy:14
    old "Packaging internal data."
    new "Empaquetando datos internos."

    # game/androidstrings.rpy:15
    old "I'm using Gradle to build the package."
    new "Estoy usando Gradle para construir el paquete."

    # game/androidstrings.rpy:16
    old "Uploading expansion file."
    new "Subiendo archivo de expansión."

    # game/androidstrings.rpy:17
    old "The build seems to have failed."
    new "La construcción parece haber fallado."

    # game/androidstrings.rpy:18
    old "Launching app."
    new "Lanzando app."

    # game/androidstrings.rpy:19
    old "The build seems to have succeeded."
    new "La construcción parece haber tenido éxito."

    # game/androidstrings.rpy:20
    old "The arm64-v8a version works on newer Android devices, the armeabi-v7a version works on older devices, and the x86_64 version works on the simulator and chromebooks."
    new "La versión de arm64-v8a funciona en dispositivos Android más nuevos, la versión de armeabi-v7a funciona en dispositivos más antiguos y la versión x86_64 funciona en el simulador y chromebooks."

    # game/androidstrings.rpy:21
    old "What is the full name of your application? This name will appear in the list of installed applications."
    new "¿Cuál es el nombre completo de tu aplicación? Este nombre aparecerá en la lista de aplicaciones instaladas."

    # game/androidstrings.rpy:22
    old "What is the short name of your application? This name will be used in the launcher, and for application shortcuts."
    new "¿Cuál es el nombre corto de tu aplicación? Este nombre se utilizará en el launcher y para los accesos directos de aplicaciones."

    # game/androidstrings.rpy:23
    old "What is the name of the package?\n\nThis is usually of the form com.domain.program or com.domain.email.program. It may only contain ASCII letters and dots. It must contain at least one dot."
    new "¿Cuál es el nombre del paquete?\n\nEsto suele tener la forma com.dominio.programa o com.dominio.correo.programa. Solo puede contener letras y puntos ASCII. Debe contener al menos un punto."

    # game/androidstrings.rpy:24
    old "The package name may not be empty."
    new "El nombre del paquete no puede estar vacío."

    # game/androidstrings.rpy:25
    old "The package name may not contain spaces."
    new "El nombre del paquete no puede contener espacios."

    # game/androidstrings.rpy:26
    old "The package name must contain at least one dot."
    new "El nombre del paquete debe contener al menos un punto."

    # game/androidstrings.rpy:27
    old "The package name may not contain two dots in a row, or begin or end with a dot."
    new "El nombre del paquete no puede contener dos puntos en una fila, o comenzar o terminar con un punto."

    # game/androidstrings.rpy:28
    old "Each part of the package name must start with a letter, and contain only letters, numbers, and underscores."
    new "Cada parte del nombre del paquete debe comenzar con una letra y contener solo letras, números y guiones bajos."

    # game/androidstrings.rpy:29
    old "{} is a Java keyword, and can't be used as part of a package name."
    new "{} es una palabra clave de Java y no se puede utilizar como parte de un nombre de paquete."

    # game/androidstrings.rpy:30
    old "What is the application's version?\n\nThis should be the human-readable version that you would present to a person. It must contain only numbers and dots."
    new "¿Cuál es la versión de la aplicación?\n\nEsta debe ser la versión legible para el ser humano que presentarías a una persona. Debe contener solo números y puntos."

    # game/androidstrings.rpy:31
    old "The version number must contain only numbers and dots."
    new "El número de versión debe contener solo números y puntos."

    # game/androidstrings.rpy:32
    old "What is the version code?\n\nThis must be a positive integer number, and the value should increase between versions."
    new "¿Cuál es el código de la versión?\n\nEste debe ser un número entero positivo, y el valor debe aumentar entre las versiones."

    # game/androidstrings.rpy:33
    old "The numeric version must contain only numbers."
    new "La versión numérica debe contener solo números."

    # game/androidstrings.rpy:34
    old "How would you like your application to be displayed?"
    new "¿Cómo desea que se muestre su aplicación?"

    # game/androidstrings.rpy:35
    old "In landscape orientation."
    new "En orientación horizontal."

    # game/androidstrings.rpy:36
    old "In portrait orientation."
    new "En orientación vertical."

    # game/androidstrings.rpy:37
    old "In the user's preferred orientation."
    new "En la orientación preferida del usuario."

    # game/androidstrings.rpy:38
    old "Which app store would you like to support in-app purchasing through?"
    new "¿En qué tienda de aplicaciones te gustaría incluir soporte para compras desde la aplicación?"

    # game/androidstrings.rpy:39
    old "Google Play."
    new "Google Play."

    # game/androidstrings.rpy:40
    old "Amazon App Store."
    new "Amazon App Store."

    # game/androidstrings.rpy:41
    old "Both, in one app."
    new "Ambos, en una sola aplicación."

    # game/androidstrings.rpy:42
    old "Neither."
    new "Ninguna."

    # game/androidstrings.rpy:43
    old "Would you like to create an expansion APK?"
    new "¿Te gustaría crear un APK de expansión?"

    # game/androidstrings.rpy:44
    old "No. Size limit of 100 MB on Google Play, but can be distributed through other stores and sideloaded."
    new "No. El límite de tamaño de 100 MB en Google Play, pero se puede distribuir a través de otras tiendas y se puede descargar de forma simultánea."

    # game/androidstrings.rpy:45
    old "Yes. 2 GB size limit, but won't work outside of Google Play. (Read the documentation to get this to work.)"
    new "Sí. Límite de tamaño de 2 GB, pero no funcionará fuera de Google Play. (Lee la documentación para que esto funcione.)"

    # game/androidstrings.rpy:46
    old "Do you want to allow the app to access the Internet?"
    new "¿Quieres permitir que la aplicación acceda a internet?"

    # game/androidstrings.rpy:47
    old "Do you want to automatically update the generated project?"
    new "¿Quieres actualizar automáticamente el proyecto generado?"

    # game/androidstrings.rpy:48
    old "Yes. This is the best choice for most projects."
    new "Sí. Esta es la mejor opción para la mayoría de los proyectos."

    # game/androidstrings.rpy:49
    old "No. This may require manual updates when Ren'Py or the project configuration changes."
    new "No. Esto puede requerir actualizaciones manuales cuando Ren'Py o la configuración del proyecto cambien."

    # game/androidstrings.rpy:50
    old "Unknown configuration variable: {}"
    new "Variable de configuración desconocida: {}."

    # game/androidstrings.rpy:51
    old "I'm compiling a short test program, to see if you have a working JDK on your system."
    new "Estoy compilando un programa de prueba corto, para ver si tienes un JDK en funcionamiento en tu sistema."

    # game/androidstrings.rpy:54
    old "I was unable to use javac to compile a test file. If you haven't installed the Java Development Kit yet, please download it from:\n\nhttps://adoptopenjdk.net/?variant=openjdk8&jvmVariant=hotspot\n\nThe JDK is different from the JRE, so it's possible you have Java without having the JDK. Without a working JDK, I can't continue."
    new "No pude usar javac para compilar un archivo de prueba. Si aún no has instalado el Kit de desarrollo de Java, descárgalo de:\n\nhttps://adoptopenjdk.net/?variant=openjdk8&jvmVariant=hotspot\n\nEl JDK es diferente del JRE, por lo que es posible que tengas Java sin tener el JDK. Sin un JDK en funcionamiento, no puedo continuar."

    # game/androidstrings.rpy:55
    old "The version of Java on your computer does not appear to be JDK 8, which is the only version supported by the Android SDK. If you need to install JDK 8, you can download it from:\n\nhttps://adoptopenjdk.net/?variant=openjdk8&jvmVariant=hotspot\n\nYou can also set the JAVA_HOME environment variable to use a different version of Java."
    new "La versión de Java en su computadora no parece ser JDK 8, que es la única versión compatible con el SDK de Android. Si necesitas instalar JDK 8, puedes descargarlo de:\n\nhttps://adoptopenjdk.net/?variant=openjdk8&jvmVariant=hotspot\n\nTambién puedes configurar la Variable de entorno JAVA_HOME para usar una versión diferente de Java."

    # game/androidstrings.rpy:54
    old "The JDK is present and working. Good!"
    new "El JDK está presente y funcionando. ¡Bien!"

    # game/androidstrings.rpy:55
    old "The Android SDK has already been unpacked."
    new "El SDK de Android ya ha sido desempaquetado."

    # game/androidstrings.rpy:56
    old "Do you accept the Android SDK Terms and Conditions?"
    new "¿Aceptas los términos y condiciones del SDK de Android?"

    # game/androidstrings.rpy:57
    old "I'm downloading the Android SDK. This might take a while."
    new "Estoy descargando el SDK de Android. Esto podría tomar un tiempo."

    # game/androidstrings.rpy:58
    old "I'm extracting the Android SDK."
    new "Estoy extrayendo el SDK de Android."

    # game/androidstrings.rpy:59
    old "I've finished unpacking the Android SDK."
    new "He terminado de desempacar el SDK de Android."

    # game/androidstrings.rpy:60
    old "I'm about to download and install the required Android packages. This might take a while."
    new "Estoy a punto de descargar e instalar los paquetes de Android necesarios. Esto podría tomar un tiempo."

    # game/androidstrings.rpy:61
    old "I was unable to accept the Android licenses."
    new "No pude aceptar las licencias de Android."

    # game/androidstrings.rpy:62
    old "I was unable to install the required Android packages."
    new "No pude instalar los paquetes de Android necesarios."

    # game/androidstrings.rpy:63
    old "I've finished installing the required Android packages."
    new "He terminado de instalar los paquetes de Android requeridos."

    # game/androidstrings.rpy:64
    old "You set the keystore yourself, so I'll assume it's how you want it."
    new "Tú mismo configuras el keystore, así que asumiré que es como lo quieres."

    # game/androidstrings.rpy:65
    old "You've already created an Android keystore, so I won't create a new one for you."
    new "Ya has creado un keystore de Android, así que no crearé uno nuevo para ti."

    # game/androidstrings.rpy:66
    old "I can create an application signing key for you. Signing an application with this key allows it to be placed in the Android Market and other app stores.\n\nDo you want to create a key?"
    new "Puedo crear una clave de firma de la aplicación para ti. Firmar una aplicación con esta clave le permite ubicarla en Android Market y otras tiendas de aplicaciones.\n\n¿Desea crear una clave?"

    # game/androidstrings.rpy:67
    old "I will create the key in the android.keystore file.\n\nYou need to back this file up. If you lose it, you will not be able to upgrade your application.\n\nYou also need to keep the key safe. If evil people get this file, they could make fake versions of your application, and potentially steal your users' data.\n\nWill you make a backup of android.keystore, and keep it in a safe place?"
    new "Crearé la clave en el archivo android.keystore.\n\nTienes que hacer una copia de seguridad de este archivo. Si lo pierdes, no podrás actualizar tu aplicación.\n\nTambién debes mantener la clave segura. Si la gente malvada obtiene este archivo, podrían crear versiones falsas de su aplicación y, posiblemente, robar los datos de sus usuarios.\n\n¿Harás una copia de seguridad de android.keystore y la mantendrás en un lugar seguro?"

    # game/androidstrings.rpy:68
    old "Please enter your name or the name of your organization."
    new "Por favor ingresa tu nombre o el nombre de tu organización."

    # game/androidstrings.rpy:69
    old "Could not create android.keystore. Is keytool in your path?"
    new "No se pudo crear android.keystore. ¿Está keytool en tu ruta?"

    # game/androidstrings.rpy:70
    old "I've finished creating android.keystore. Please back it up, and keep it in a safe place."
    new "He terminado de crear android.keystore. Por favor haga una copia de seguridad y guárdelo en un lugar seguro."

    # game/androidstrings.rpy:71
    old "It looks like you're ready to start packaging games."
    new "Parece que estás listo para comenzar a empaquetar juegos."

    # game/choose_theme.rpy:507
    old "changing the theme"
    new "cambiando el tema"

    # game/front_page.rpy:252
    old "Web"
    new "Web"

    # game/front_page.rpy:252
    old "(Beta)"
    new "(Beta)"

    # game/gui7.rpy:429
    old "creating a new project"
    new "creando un nuevo proyecto"

    # game/gui7.rpy:433
    old "activating the new project"
    new "activando el nuevo proyecto"

    # game/interface.rpy:372
    old "opening the log file"
    new "abriendo el archivo de registro"

    # game/interface.rpy:394
    old "While [what!qt], an error occured:"
    new "Mientras que [what!qt], ocurrió un error:"

    # game/interface.rpy:394
    old "[exception!q]"
    new "[exception!q]"

    # game/itch.rpy:43
    old "Downloading the itch.io butler."
    new "Descargando el butler de itch.io"

    # game/updater.rpy:101
    old "The update channel controls the version of Ren'Py the updater will download."
    new "El canal de actualización controla la versión de Ren'Py que el actualizador descargará."

    # game/updater.rpy:110
    old "• This version is installed and up-to-date."
    new "• Esta versión está instalada y actualizada."

    # game/updater.rpy:118
    old "%B %d, %Y"
    new "%d de %B, %Y"

    # game/updater.rpy:188
    old "Fetching the list of update channels"
    new "Obteniendo la lista de canales de actualización."

    # game/updater.rpy:194
    old "downloading the list of update channels"
    new "descargando la lista de canales de actualización"

    # game/updater.rpy:198
    old "parsing the list of update channels"
    new "analizar la lista de canales de actualización"

    # game/web.rpy:118
    old "Web: [project.current.display_name!q]"
    new "Web: [project.current.display_name!q]"

    # game/web.rpy:148
    old "Build Web Application"
    new "Construir una aplicación web"

    # game/web.rpy:149
    old "Build and Open in Browser"
    new "Construir y abrir en el navegador"

    # game/web.rpy:150
    old "Open without Build"
    new "Abrir sin construir"

    # game/web.rpy:154
    old "Support:"
    new "Soporte:"

    # game/web.rpy:162
    old "RenPyWeb Home"
    new "Página de inicio de RenpyWeb"

    # game/web.rpy:163
    old "Beuc's Patreon"
    new "Patreon de Beuc"

    # game/web.rpy:181
    old "Ren'Py web applications require the entire game to be downloaded to the player's computer before it can start."
    new "Las aplicaciones web de Ren'Py requieren que todo el juego se descargue en la computadora del jugador antes de que pueda comenzar."

    # game/web.rpy:185
    old "Current limitations in the web platform mean that loading large images, audio files, or movies may cause audio or framerate glitches, and lower performance in general."
    new "Las limitaciones actuales en la plataforma web significan que la carga de imágenes grandes, archivos de audio o películas pueden ocasionar problemas de audio o de frecuencia de cuadros, y un rendimiento más bajo en general."

    # game/web.rpy:194
    old "Before packaging web apps, you'll need to download RenPyWeb, Ren'Py's web support. Would you like to download RenPyWeb now?"
    new "Antes de empaquetar aplicaciones web, deberá descargar RenPyWeb, el soporte web de Ren'Py. ¿Te gustaría descargar RenPyWeb ahora?"

    # game/web.rpy:150
    old "Open in Browser"
    new "Abrir en el navegador"

    # game/web.rpy:151
    old "Open build directory"
    new "Abrir directorio de construcción"

    # game/front_page.rpy:198
    old "audio"
    new "audio"

    # game/androidstrings.rpy:47
    old "Do you want to automatically update the Java source code?"
    new "¿Quieres actualizar automáticamente el código fuente de Java?"

    # game/choose_directory.rpy:93
    old "Ren'Py was unable to run python with tkinter to choose the directory. Please install the python3-tk or tkinter package."
    new "Ren'Py no pudo ejecutar Python con tkinter para elegir el directorio. Instale el paquete python3-tk o tkinter."

    # game/install.rpy:33
    old "Could not install [name!t], as a file matching [zipglob] was not found in the Ren'Py SDK directory."
    new "No se pudo instalar [name!t], ya que no se encontró un archivo que coincida con [zipglob] en el directorio del SDK de Ren'Py."

    # game/install.rpy:76
    old "Successfully installed [name!t]."
    new "[name!t] se instaló correctamente."

    # game/install.rpy:104
    old "Install Libraries"
    new "Instalar bibliotecas"

    # game/install.rpy:119
    old "This screen allows you to install libraries that can't be distributed with Ren'Py. Some of these libraries may require you to agree to a third-party license before being used or distributed."
    new "Esta pantalla le permite instalar bibliotecas que no se pueden distribuir con Ren'Py. Algunas de estas bibliotecas pueden requerir que aceptes una licencia de terceros antes de ser utilizadas o distribuidas."

    # game/install.rpy:134
    old "The {a=https://www.live2d.com/en/download/cubism-sdk/download-native/}Cubism SDK for Native{/a} adds support for displaying Live2D models. Place CubismSdkForNative-4-{i}version{/i}.zip in the Ren'Py SDK directory, and then click Install. Distributing a game with Live2D requires you to accept a license from Live2D, Inc."
    new "{a=https://www.live2d.com/en/download/cubism-sdk/download-native/}Cubism SDK for Native{/a} agrega soporte para mostrar modelos Live2D. Coloca CubismSdkForNative-4-{i}version{/i}.zip en el directorio Ren'Py SDK y luego haz clic en Instalar. La distribución de un juego con Live2D requiere que aceptes una licencia de Live2D, Inc."

    # game/install.rpy:138
    old "Open Ren'Py SDK Directory"
    new "Abrir el directorio del SDK de Ren'Py"

    # game/preferences.rpy:138
    old "Install libraries"
    new "Instalar bibliotecas"

    # game/preferences.rpy:140
    old "Reset window size"
    new "Restablecer el tamaño de la ventana"

    # game/web.rpy:242
    old "Preparing progressive download"
    new "Preparando descarga progresiva"

    # game/web.rpy:341
    old "Images and musics can be downloaded while playing. A 'progressive_download.txt' file will be created so you can configure this behavior."
    new "Las imágenes y las músicas se pueden descargar mientras juegas. Se creará un archivo 'progress_download.txt' para que puedas configurar este comportamiento."

    # game/install.rpy:144
    old "Live2D in Ren'Py doesn't support the Web, Android x86_64 (including emulators and Chrome OS), and must be added to iOS projects manually. Live2D must be reinstalled after upgrading Ren'Py or installing Android support."
    new "Live2D en Ren'Py no tiene soporte en Web, Android x86_64 (incluidos emuladores y Chrome OS) y debe agregarse a los proyectos de iOS manualmente. Live2D debe reinstalarse después de actualizar Ren'Py o instalar el soporte de Android."

    # game/install.rpy:131
    old "Install Live2D Cubism SDK for Native"
    new "Instalar Live2D Cubism SDK for Native"

    # game/install.rpy:151
    old "Install Steam Support"
    new "Instalar el soporte de Steam"

    # game/install.rpy:160
    old "Before installing Steam support, please make sure you are a {a=https://partner.steamgames.com/}Steam partner{/a}."
    new "Antes de instalar el soporte de Steam, asegúrate de ser un {a=https://partner.steamgames.com/}socio de Steam{/a}.."

    # game/install.rpy:172
    old "Steam support has already been installed."
    new "El soporte de Steam ya está instalado."

    # game/androidstrings.rpy:21
    old "The universal version works everywhere but is larger."
    new "La versión universal funciona en todas partes pero es más grande."

    # game/androidstrings.rpy:45
    old "Automatically installing expansion APKs {a=https://issuetracker.google.com/issues/160942333}may not work on Android 11{/a}."
    new "Es posible que la instalación automática de APK de expansión {a=https://issuetracker.google.com/issues/160942333} no funcione en Android 11 {/a}."

    # game/preferences.rpy:199
    old "Default theme"
    new "Tema predeterminado"

    # game/preferences.rpy:201
    old "Clear theme"
    new "Tema claro"

    # game/preferences.rpy:203
    old "Dark theme"
    new "Tema oscuro"

    # game/preferences.rpy:209
    old "Custom theme"
    new "Tema personalizado"

    # game/android.rpy:38
    old "RAPT has been installed, but a bundle key hasn't been configured. Please create a new key, or restore bundle.keystore."
    new "Se ha instalado RAPT, pero no se ha configurado una clave de paquete. Cree una nueva clave o restaure bundle.keystore."

    # game/android.rpy:40
    old "Please select if you want a Play Bundle (for Google Play), or a Universal APK (for sideloading and other app stores)."
    new "Selecciona si quieres un Play Bundle (para Google Play) o un APK Universal (para descarga lateral y otras tiendas de aplicaciones)."

    # game/android.rpy:55
    old "Pairs with a device over Wi-Fi, on Android 11+."
    new "Empareja con un dispositivo a través de Wi-Fi, en Android 11+."

    # game/android.rpy:56
    old "Connects to a device over Wi-Fi, on Android 11+."
    new "Conecta a un dispositivo a través de Wi-Fi, en Android 11+."

    # game/android.rpy:58
    old "Builds an Android App Bundle (ABB), intended to be uploaded to Google Play. This can include up to 2GB of data."
    new "Crea un paquete de aplicaciones de Android (ABB), destinado a cargarse en Google Play. Esto puede incluir hasta 2 GB de datos."

    # game/android.rpy:59
    old "Builds a Universal APK package, intended for sideloading and stores other than Google Play. This can include up to 2GB of data."
    new "Crea un paquete de APK universal, destinado a la descarga lateral y a tiendas distintas de Google Play. Esto puede incluir hasta 2 GB de datos."

    # game/android.rpy:388
    old "Play Bundle"
    new "Play Bundle"

    # game/android.rpy:392
    old "Universal APK"
    new "APK Universal"

    # game/android.rpy:449
    old "Wi-Fi Debugging Pair"
    new "Depuración de par de Wi-Fi "

    # game/android.rpy:453
    old "Wi-Fi Debugging Connect"
    new "Depuración de conexión de Wi-Fi "

    # game/android.rpy:541
    old "Wi-Fi Pairing Code"
    new "Código de emparejamiento de Wi-Fi"

    # game/android.rpy:541
    old "If supported, this can be found in 'Developer options', 'Wireless debugging', 'Pair device with pairing code'."
    new "Si es compatible, puedes encontrarlo en 'Opciones de desarrollador', 'Depuración inalámbrica', 'Emparejar dispositivo con código de emparejamiento'."

    # game/android.rpy:548
    old "Pairing Host & Port"
    new "Emparejamiento de host y puerto"

    # game/android.rpy:564
    old "IP Address & Port"
    new "Dirección IP y puerto"

    # game/android.rpy:564
    old "If supported, this can be found in 'Developer options', 'Wireless debugging'."
    new "Si es compatible, puedes encontrarlo en 'Opciones de desarrollador', 'Depuración inalámbrica'."

    # game/gui7.rpy:311
    old "{size=-4}\n\nThis will not overwrite gui/main_menu.png, gui/game_menu.png, and gui/window_icon.png, but will create files that do not exist.{/size}"
    new "{size=-4}\n\nEsto no sobrescribirá gui/main_menu.png, gui/game_menu.png y gui/window_icon.png, pero creará archivos que no existen.{/size}"

    # game/ios.rpy:339
    old "There are known issues with the iOS simulator on Apple Silicon. Please test on x86_64 or iOS devices."
    new "Hay problemas conocidos con el simulador de iOS en Apple Silicon. Pruebe en dispositivos x86_64 o iOS."

    # game/preferences.rpy:213
    old "Daily check for update"
    new "Comprobación diaria de actualizaciones"

    # game/web.rpy:330
    old "Images and music can be downloaded while playing. A 'progressive_download.txt' file will be created so you can configure this behavior."
    new "Las imágenes y la música se pueden descargar mientras se reproduce. Se creará un archivo 'progress_download.txt' para que pueda configurar este comportamiento."

    # game/web.rpy:334
    old "Current limitations in the web platform mean that loading large images may cause audio or framerate glitches, and lower performance in general. Movies aren't supported."
    new "Las limitaciones actuales en la plataforma web significan que la carga de imágenes grandes puede causar problemas de audio o de velocidad de fotogramas, y un rendimiento más bajo en general. No se admiten películas."

    # game/web.rpy:338
    old "There are known issues with Safari and other Webkit-based browsers that may prevent games from running."
    new "Existen problemas conocidos con Safari y otros navegadores basados en Webkit que pueden impedir que los juegos se ejecuten."

    # game/androidstrings.rpy:16
    old "I'm installing the bundle."
    new "Estoy instalando el paquete."

    # game/androidstrings.rpy:30
    old "How much RAM do you want to allocate to Gradle?\n\nThis must be a positive integer number."
    new "¿Cuánta RAM deseas asignar a Gradle?\n\nDebe ser un número entero positivo."

    # game/androidstrings.rpy:31
    old "The RAM size must contain only numbers."
    new "El tamaño de la RAM debe contener solo números."

    # game/androidstrings.rpy:61
    old "Could not create bundle.keystore. Is keytool in your path?"
    new "No se pudo crear bundle.keystore. ¿Está keytool en tu ruta?"

    # game/androidstrings.rpy:55
    old "I can create an application signing key for you. This key is required to create Universal APK for sideloading and stores other than Google Play.\n\nDo you want to create a key?"
    new "Puedo crear una clave de firma de la aplicación para ti. Esta clave es necesaria para crear un APK universal para la descarga y las tiendas que no sean Google Play.\n\n¿Deseas crear una clave?"

    # game/androidstrings.rpy:59
    old "I can create a bundle signing key for you. This key is required to build an Android App Bundle (AAB) for upload to Google Play.\n\nDo you want to create a key?"
    new "Puedo crearte una clave de firma de paquete. Esta clave es necesaria para crear un paquete de aplicaciones de Android (AAB) para cargarlo en Google Play.\n\n¿Deseas crear una clave?"

    # game/androidstrings.rpy:60
    old "I will create the key in the bundle.keystore file.\n\nYou need to back this file up. If you lose it, you will not be able to upgrade your application.\n\nYou also need to keep the key safe. If evil people get this file, they could make fake versions of your application, and potentially steal your users' data.\n\nWill you make a backup of bundle.keystore, and keep it in a safe place?"
    new "Crearé la clave en el archivo bundle.keystore.\n\nNecesitas hacer una copia de seguridad de este archivo. Si la pierdes, no podrás actualizar tu aplicación.\n\nTambién necesitas mantener la clave segura. Si personas malvadas obtienen este archivo, podrían crear versiones falsas de tu aplicación y potencialmente robar los datos de tus usuarios.\n\n¿Harás una copia de seguridad de bundle.keystore y la guardarás en un lugar seguro?"

    # game/android.rpy:55
    old "Lists the connected devices."
    new "Enlista los dispositivos conectados."

    # game/android.rpy:58
    old "Disconnects a device connected over Wi-Fi."
    new "Desconecta un dispositivo conectado a través de Wi-Fi."

    # game/android.rpy:453
    old "List Devices"
    new "Lista de dispositivos"

    # game/android.rpy:465
    old "Wi-Fi Debugging Disconnect"
    new "Desconexión de depuración de Wi-Fi"

    # game/android.rpy:603
    old "This can be found in 'List Devices'."
    new "Esto se puede encontrar en 'Lista de dispositivos'."

    # game/androidstrings.rpy:17
    old "Installing the bundle appears to have failed."
    new "La instalación del paquete parece haber fallado."

    # game/androidstrings.rpy:19
    old "Launching the app appears to have failed."
    new "El lanzamiento de la aplicación parece haber fallado."

    # game/androidstrings.rpy:44
    old "The version of Java on your computer does not appear to be JDK 8, which is the only version supported by the Android SDK. If you need to install JDK 8, you can download it from:\n\n{a=https://adoptium.net/?variant=openjdk8}https://adoptium.net/?variant=openjdk8{/a}\n\nYou can also set the JAVA_HOME environment variable to use a different version of Java."
    new "La versión de Java en su computadora no parece ser JDK 8, que es la única versión compatible con el SDK de Android. Si necesita instalar JDK 8, puede descargarlo desde:\n\n{a=https://adoptium.net/?variant=openjdk8}https://adoptium.net/?variant=openjdk8{/a}\n\nTambién puede configurar la variable de entorno JAVA_HOME para usar una versión diferente de Java."

    # game/updater.rpy:109
    old "• {a=https://www.renpy.org/doc/html/changelog.html}View change log{/a}"
    new "• {a=https://www.renpy.org/doc/html/changelog.html}Ver el registro de cambios{/a}"

    # game/updater.rpy:111
    old "• {a=https://www.renpy.org/dev-doc/html/changelog.html}View change log{/a}"
    new "• {a=https://www.renpy.org/dev-doc/html/changelog.html}Ver el registro de cambios{/a}"

    # game/installer.rpy:10
    old "Downloading [extension.download_file]."
    new "Descargando [extension.download_file]."

    # game/installer.rpy:11
    old "Could not download [extension.download_file] from [extension.download_url]:\n{b}[extension.download_error]"
    new "No se pudo descargar [extension.download_file] desde [extension.download_url]:\n{b}[extension.download_error]"

    # game/installer.rpy:12
    old "The downloaded file [extension.download_file] from [extension.download_url] is not correct."
    new "El archivo descargado [extension.download_file] desde [extension.download_url] no es correcto."

    # game/android.rpy:60
    old "Removes Android temporary files."
    new "Elimina los archivos temporales de Android."

    # game/android.rpy:472
    old "Clean"
    new "Limpiar"

    # game/android.rpy:628
    old "Cleaning up Android project."
    new "Limpieando el proyecto de Android."

    # game/androidstrings.rpy:43
    old "I was unable to use javac to compile a test file. If you haven't installed the Java Development Kit yet, please download it from:\n\n{a=https://adoptium.net/?variant=openjdk8}https://adoptium.net/?variant=openjdk8{/a}\n\nThe JDK is different from the JRE, so it's possible you have Java without having the JDK. Please make sure you installed the 'JavaSoft (Oracle) registry keys'.\n\nWithout a working JDK, I can't continue."
    new "No pude usar javac para compilar un archivo de prueba. Si aún no has instalado el kit de desarrollo de Java, descárgalo de:\n\n{a=https://adoptium.net/?variant=openjdk8}https://adoptium.net/?variant=openjdk8{/a}\n\nEl JDK es diferente del JRE, por lo que es posible que tenga Java sin tener el JDK. Asegúrese de haber instalado las 'claves de registro de JavaSoft (Oracle)'.\n\nSin un JDK que funcione, no puedo continuar."

    # game/androidstrings.rpy:64
    old "I've opened the directory containing android.keystore and bundle.keystore. Please back them up, and keep them in a safe place."
    new "Abrí el directorio que contiene android.keystore y bundle.keystore. Por favor, haz una copia de seguridad y guárdalos en un lugar seguro."

    # game/choose_directory.rpy:67
    old "Select Projects Directory"
    new "Seleccionar directorio de proyectos"

    # game/distribute.rpy:1674
    old "Copying files..."
    new "Copiando archivos..."

    # game/distribute_gui.rpy:195
    old "Update old-game"
    new "Actualizar juego antiguo"

    # game/editor.rpy:152
    old "A modern editor with many extensions including advanced Ren'Py integration."
    new "Un editor moderno con muchas extensiones, incluida la integración avanzada de Ren'Py."

    # game/editor.rpy:153
    old "A modern editor with many extensions including advanced Ren'Py integration.\n{a=jump:reinstall_vscode}Upgrade Visual Studio Code to the latest version.{/a}"
    new "Un editor moderno con muchas extensiones, incluida la integración avanzada de Ren'Py.\n{a=jump:reinstall_vscode}Actualice Visual Studio Code a la última versión.{/a}"

    # game/editor.rpy:162
    old "Visual Studio Code"
    new "Visual Studio Code"

    # game/editor.rpy:162
    old "Up to 110 MB download required."
    new "Requiere descargar hasta 110 MB."

    # game/editor.rpy:175
    old "A modern and approachable text editor."
    new "Un editor de texto moderno y accesible."

    # game/editor.rpy:187
    old "Atom"
    new "Atom"

    # game/editor.rpy:200
    old "jEdit"
    new "jEdit"

    # game/editor.rpy:209
    old "Visual Studio Code (System)"
    new "Visual Studio Code (Sistema)"

    # game/editor.rpy:209
    old "Uses a copy of Visual Studio Code that you have installed outside of Ren'Py. It's recommended you install the language-renpy extension to add support for Ren'Py files."
    new "Utiliza una copia de Visual Studio Code que ha instalado fuera de Ren'Py. Se recomienda que instale la extensión language-renpy para agregar soporte para archivos Ren'Py."

    # game/interface.rpy:124
    old "[interface.version]"
    new "[interface.version]"

    # game/preferences.rpy:161
    old "Clean temporary files"
    new "Limpiar archivos temporales"

    # game/preferences.rpy:263
    old "Cleaning temporary files..."
    new "Limpiando archivos temporales..."

    # game/project.rpy:280
    old "This may be because the project is not writeable."
    new "Esto puede deberse a que el proyecto no se puede escribir."

    # game/translations.rpy:391
    old "Language (or None for the default language):"
    new "Idioma (o Ninguno para el idioma predeterminado):"

    # game/web.rpy:344
    old "This feature is not supported in Ren'Py 8."
    new "Esta característica no es compatible con Ren'Py 8."

    # game/web.rpy:344
    old "We will restore support in a future release of Ren'Py 8. Until then, please use Ren'Py 7 for web support."
    new "Restauraremos el soporte en una versión estable futura de Ren'Py 8. Hasta entonces, use Ren'Py 7 para soporte web."

    # game/preferences.rpy:104
    old "General"
    new "General"

    # game/preferences.rpy:105
    old "Options"
    new "Opciones"

    # game/preferences.rpy:244
    old "Launcher Theme:"
    new "Tema del lanzdor"

    # game/preferences.rpy:254
    old "Information about creating a custom theme can be found {a=https://www.renpy.org/doc/html/skins.html}in the Ren'Py Documentation{/a}."
    new "Puedes encontrar información sobre cómo crear un tema personalizado {a=https://www.renpy.org/doc/html/skins.html}en la documentación de Ren'Py{/a}."

    # game/preferences.rpy:271
    old "Install Libraries:"
    new "Instalar bibliotecas:"

    # game/updater.rpy:64
    old "Release (Ren'Py 8, Python 3)"
    new "Estable (Ren'Py 8, Python 3)"

    # game/updater.rpy:65
    old "Release (Ren'Py 7, Python 2)"
    new "Estable (Ren'Py 7, Python 2)"

    # game/updater.rpy:69
    old "Prerelease (Ren'Py 8, Python 3)"
    new "Preliminar (Ren'Py 8, Python 3)"

    # game/updater.rpy:70
    old "Prerelease (Ren'Py 7, Python 2)"
    new "Preliminar (Ren'Py 7, Python 2)"

    # game/updater.rpy:77
    old "Nightly (Ren'Py 8, Python 3)"
    new "Nocturna (Ren'Py 8, Python 3)"

    # game/updater.rpy:78
    old "Nightly (Ren'Py 7, Python 2)"
    new "Nocturna (Ren'Py 7, Python 2)"

    # game/preferences.rpy:327
    old "{#in language font}Welcome! Please choose a language"
    new "{font=fonts/Roboto-Light.ttf}¡Bienvenido! Por favor elige un idioma{/font}"

    # game/preferences.rpy:327
    old "{#in language font}Start using Ren'Py in [lang_name]"
    new "{font=fonts/Roboto-Light.ttf}Empieza a usar Ren'Py en [lang_name]{/font}"

    # game/distribute_gui.rpy:231
    old "(DLC)"
    new "(DLC)"

    # game/project.rpy:46
    old "Lint checks your game for potential mistakes, and gives you statistics."
    new "Lint comprueba tu juego en busca de posibles errores y te ofrece estadísticas."

    # game/web.rpy:484
    old "Creating package..."
    new "Creando paquete..."

    # game/android.rpy:39
    old "RAPT has been installed, but a key hasn't been configured. Please generate new keys, or copy android.keystore and bundle.keystore to the base directory."
    new "RAPT ha sido instalado, pero no se ha configurado una clave. Por favor, genera nuevas claves, o copia android.keystore y bundle.keystore al directorio base."

    # game/android.rpy:46
    old "Attempts to emulate a televison-based Android console.\n\nController input is mapped to the arrow keys, Enter is mapped to the select button, Escape is mapped to the menu button, and PageUp is mapped to the back button."
    new "Intenta emular una consola Android basada en televisión.\n\nLa entrada del controlador se asigna a las teclas de flecha, Enter se asigna al botón de selección, Escape se asigna al botón de menú y PageUp se asigna al botón de retroceso."

    # game/android.rpy:48
    old "Downloads and installs the Android SDK and supporting packages."
    new "Descarga e instala el SDK de Android y los paquetes de soporte."

    # game/android.rpy:49
    old "Generates the keys required to sign the package."
    new "Genera las claves necesarias para firmar el paquete."

    # game/android.rpy:383
    old "Install SDK"
    new "Instalar SDK"

    # game/android.rpy:387
    old "Generate Keys"
    new "Generar claves"

    # game/androidstrings.rpy:32
    old "How much RAM (in GB) do you want to allocate to Gradle?\nThis must be a positive integer number."
    new "¿Cuánta RAM (en GB) quiere asignar a Gradle?\nDebe ser un número entero positivo."

    # game/androidstrings.rpy:33
    old "The RAM size must contain only numbers and be positive."
    new "El tamaño de la RAM debe contener sólo números y ser positivo."

    # game/androidstrings.rpy:63
    old "I found an android.keystore file in the rapt directory. Do you want to use this file?"
    new "He encontrado un archivo android.keystore en el directorio rapt. ¿Quieres usar este archivo?"

    # game/androidstrings.rpy:66
    old "\n\nSaying 'No' will prevent key creation."
    new "\n\nDecir 'No' impedirá la creación de claves."

    # game/androidstrings.rpy:69
    old "I found a bundle.keystore file in the rapt directory. Do you want to use this file?"
    new "He encontrado un archivo bundle.keystore en el directorio rapt. ¿Quieres usar este archivo?"
    
    # game/updater.rpy:79
    old "A nightly build of fixes to the release version of Ren'Py."
    new "Compilación nocturna de correcciones para la versión estable de Ren'Py."

    # game/updater.rpy:76
    old "Nightly Fix"
    new "Correciones nocturnas"

    # game/updater.rpy:77
    old "Nightly Fix (Ren'Py 8, Python 3)"
    new "Correciones nocturnas (Ren'Py 8, Python 3)"

    # game/updater.rpy:78
    old "Nightly Fix (Ren'Py 7, Python 2)"
    new "Correciones nocturnas (Ren'Py 7, Python 2)"
