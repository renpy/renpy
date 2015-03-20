## This file contains some of the options that can be changed to customize
## your Ren'Py game. It only contains the most common options... there
## is quite a bit more customization you can do.
##
## Lines beginning with two '#' marks are comments, and you shouldn't
## uncomment them. Lines beginning with a single '#' mark are
## commented-out code, and you may want to uncomment them when
## appropriate.
##
## - Este archivo contiene algunas de las opciones que pueden cambiarse para
##   personalizar el juego Ren'Py. Solo figuran las opciones más comunes.
##   Es posible añadir muchas más personalizaciones.
##
## - Las líneas que empiezan con dos marcas '#' son comentarios, no debes
##   eliminar las marcas. Las líneas que comienzan con una sola marca '#'
##   contienen código no activo. La marca '#' puede eliminarse si se quiere
##   utilizar esa característica.

init -1 python hide:

    ## Should we enable the use of developer tools? This should be
    ## set to False before the game is released, so the user can't
    ## cheat using developer tools.
    ## - Esta variable habilita las herramientas de desarrollo. Debe ser
    ##   ajustada a False antes del lanzamiento del juego, así el usuario
    ##   no puede hacer trampas usando las herramientas de desarrollo.

    config.developer = True

    ## These control the width and height of the screen.
    ## - Control de la anchura y altura de la pantalla.

    config.screen_width = 800
    config.screen_height = 600

    ## This controls the title of the window, when Ren'Py is
    ## running in a window.
    ## - Título de la ventana, cuando Ren'Py se ejecuta en modo ventana.

    config.window_title = u"PROJECT_NAME"

    ## These control the name and version of the game, that are reported
    ## with tracebacks and other debugging logs.
    ## - Control del nombre y versión del juego; se utilizan en los
    ##   rastreos y otras funciones de depuración.
    config.name = "PROJECT_NAME"
    config.version = "0.0"

    #########################################
    ## Themes
    ## - Temas

    ## We then want to call a theme function. theme.roundrect is
    ## a theme that features the use of rounded rectangles.
    ##
    ## The theme function takes a number of parameters that can
    ## customize the color scheme.

    ## - Para utilizar una función de tema, utilizamos themes.roundrect.
    ##   Este tema configura el uso de rectángulos redondeados.
    ##
    ## - La función de tema acepta una serie de parámetros que pueden
    ##   personalizar la paleta de colores.

    theme.roundrect(

        ## The color of an idle widget face.
        ## - Color base de un elemento (widget).
        widget = "#003c78",

        ## The color of a focused widget face.
        ## - Color de un elemento con foco.
        widget_hover = "#0050a0",

        ## The color of the text in a widget.
        ## - Color del texto en un elemento.
        widget_text = "#c8ffff",

        ## The color of the text in a selected widget. (For
        ## example, the current value of a preference.)
        ## - Color del texto en un elemento seleccionado (por ejemplo,
        ##   el valor actual de una preferencia).
        widget_selected = "#ffffc8",

        ## The color of a disabled widget face.
        ## - Color de un elemento deshabilitado.
        disabled = "#404040",

        ## The color of disabled widget text.
        ## - Color del texto de un elemento deshabilitado.
        disabled_text = "#c8c8c8",

        ## The color of informational labels.
        ## - Color de las etiquetas de información.
        label = "#ffffff",

        ## The color of a frame containing widgets.
        ## - Color del marco que contiene los elementos.
        frame = "#6496c8",

        ## If this is True, the in-game window is rounded. If False,
        ## the in-game window is square.
        ## - Si es 'True', la ventana interna del juego tendrà las
        ##   esquinas redondeadas. Si es 'False', serà rectangular.
        rounded_window = False,

        ## The background of the main menu. This can be a color
        ## beginning with '#', or an image filename. The latter
        ## should take up the full height and width of the screen.
        ## - Fondo del menú principal. Puede ser un color que
        ##   comience con '#' o bien el nombre de un archivo de imagen.
        ##   En ese caso, debe ocupar el ancho y alto de la pantalla.
        mm_root = "#dcebff",

        ## The background of the game menu. This can be a color
        ## beginning with '#', or an image filename. The latter
        ## should take up the full height and width of the screen.
        ## - Fondo del menú del juego. Puede ser un color que
        ##   comience con '#' o bien el nombre de un archivo de imagen.
        ##   En ese caso, debe ocupar el ancho y alto de la pantalla.
        gm_root = "#dcebff",

        ## And we're done with the theme. The theme will customize
        ## various styles, so if we want to change them, we should
        ## do so below.
        ## - Hemos terminado con el tema. El tema personalizará varios
        ##   estilos, que pueden ser cambiados más abajo.
        )


    #########################################
    ## These settings let you customize the window containing the
    ## dialogue and narration, by replacing it with an image.
    ## - Estos ajustes permiten personalizar la ventana que contiene
    ##   el diálogo y la narración, reemplazándola con una imagen.

    ## The background of the window. In a Frame, the two numbers
    ## are the size of the left/right and top/bottom borders,
    ## respectively.
    ## - Fondo de la ventana. Usando un marco ('Frame'), los dos números
    ##   indican la dimensión de los bordes izquierdo/derecho y
    ##   superior/inferior, respectivamente.

    # style.window.background = Frame("frame.png", 12, 12)

    ## Margin is space surrounding the window, where the background
    ## is not drawn.
    ## - El margen es el espacio alrededor de la ventana, en el cual el
    ##   fondo no aparece.

    # style.window.left_margin = 6
    # style.window.right_margin = 6
    # style.window.top_margin = 6
    # style.window.bottom_margin = 6

    ## Padding is space inside the window, where the background is
    ## drawn.
    ## - El 'relleno' ('padding') es el margen interior a la ventana,
    ##   en el cual el fondo sí se dibuja, pero no el texto.

    # style.window.left_padding = 6
    # style.window.right_padding = 6
    # style.window.top_padding = 6
    # style.window.bottom_padding = 6

    ## This is the minimum height of the window, including the margins
    ## and padding.
    ## - Altura mínima de la ventana, incluyendo margen y 'relleno'.

    # style.window.yminimum = 250


    #########################################
    ## This lets you change the placement of the main menu.
    ## - Esta sección permite cambiar la disposición del menú principal.

    ## The way placement works is that we find an anchor point
    ## inside a displayable, and a position (pos) point on the
    ## screen. We then place the displayable so the two points are
    ## at the same place.
    ## - La colocación funciona de la siguiente manera: Primero se
    ##   establece un punto de anclaje (anchor) dentro de un elemento
    ##   gràfico (displayable), a continuación un punto de posición (pos)
    ##   en la pantalla. Finalmente se coloca el elemento gràfico de forma
    ##   que ambos puntos coincidan.

    ## An anchor/pos can be given as an integer or a floating point
    ## number. If an integer, the number is interpreted as a number
    ## of pixels from the upper-left corner. If a floating point,
    ## the number is interpreted as a fraction of the size of the
    ## displayable or screen.
    ## - Los puntos de anclaje y de posición (anchor/pos) pueden indicarse
    ##   con un número entero o decimal. Un entero indica los píxeles desde
    ##   la esquina superior izquierda. Un decimal, en cambio, se interpreta
    ##   como fracción de las dimensiones del elemento gráfico o la
    ##   pantalla.

    # style.mm_menu_frame.xpos = 0.5
    # style.mm_menu_frame.xanchor = 0.5
    # style.mm_menu_frame.ypos = 0.75
    # style.mm_menu_frame.yanchor = 0.5


    #########################################
    ## These let you customize the default font used for text in Ren'Py.
    ## - Personalización del tipo de letra utilizado por defecto.

    ## The file containing the default font.
    ## - Archivo del tipo de letra.

    # style.default.font = "DejaVuSans.ttf"

    ## The default size of text.
    ## - Tamaño de letra por defecto.

    # style.default.size = 22

    ## Note that these only change the size of some of the text. Other
    ## buttons have their own styles.
    ## - Nota: Solo cambia el tamaño de parte del texto. Otros botones
    ##   tienen sus propios estilos.


    #########################################
    ## These settings let you change some of the sounds that are used by
    ## Ren'Py.
    ## - Ajuste de algunos de los sonidos utilizados por Ren'Py.

    ## Set this to False if the game does not have any sound effects.
    ## - Ajustar a 'False' si el juego no tiene efectos de sonido.

    config.has_sound = True

    ## Set this to False if the game does not have any music.
    ## - Ajustar a 'False' si el juego no tiene música.

    config.has_music = True

    ## Set this to True if the game has voicing.
    ## - Ajustar a 'True' si el juego contiene voces.

    config.has_voice = False

    ## Sounds that are used when button and imagemaps are clicked.
    ## - Sonidos utilizados cuando se hace clic en un botón.

    # style.button.activate_sound = "click.wav"
    # style.imagemap.activate_sound = "click.wav"

    ## Sounds that are used when entering and exiting the game menu.
    ## - Sonidos utilizados cuando se entra o sale del menú del juego.

    # config.enter_sound = "click.wav"
    # config.exit_sound = "click.wav"

    ## A sample sound that can be played to check the sound volume.
    ## - Sonido de ejemplo utilizado para comprobar el volumen.

    # config.sample_sound = "click.wav"

    ## Music that is played while the user is at the main menu.
    ## - Música del menú principal.

    # config.main_menu_music = "main_menu_theme.ogg"


    #########################################
    ## Help.
    ## - Ayuda.

    ## This lets you configure the help option on the Ren'Py menus.
    ## It may be:
    ## - A label in the script, in which case that label is called to
    ##   show help to the user.
    ## - A file name relative to the base directory, which is opened in a
    ##   web browser.
    ## - None, to disable help.

    ## - Configuración de la opción de ayuda de los menús de Ren'Py.
    ##   Puede ser:
    ##   - Una etiqueta (label) en el 'script', en cuyo caso se llama esa
    ##     etiqueta para mostrar la ayuda al usuario.
    ##   - El nombre de un archivo relativo al directorio base, que se abre
    ##     en un navegador web.
    ##   - 'None', para deshabilitar la ayuda (se debe eliminar el botón
    ##     de ayuda en las pantallas 'screens').
    config.help = "README.html"


    #########################################
    ## Transitions.
    ## - Transiciones.

    ## Used when entering the game menu from the game.
    ## - Desde el juego al menú del juego.
    config.enter_transition = None

    ## Used when exiting the game menu to the game.
    ## - Desde el menú del juego al juego.
    config.exit_transition = None

    ## Used between screens of the game menu.
    ## - Entre pantallas del menú del juego.
    config.intra_transition = None

    ## Used when entering the game menu from the main menu.
    ## - Desde el menú principal al menú del juego.
    config.main_game_transition = None

    ## Used when returning to the main menu from the game.
    ## - Desde el juego al menú principal.
    config.game_main_transition = None

    ## Used when entering the main menu from the splashscreen.
    ## - Desde la pantalla splash al menú principal.
    config.end_splash_transition = None

    ## Used when entering the main menu after the game has ended.
    ## - Al menú principal cuando el juego ha terminado.
    config.end_game_transition = None

    ## Used when a game is loaded.
    ## - Cuando se carga una partida.
    config.after_load_transition = None

    ## Used when the window is shown.
    ## - Cuando se muestra una ventana.
    config.window_show_transition = None

    ## Used when the window is hidden.
    ## - Cuando se oculta una ventana.
    config.window_hide_transition = None

    ## Used when showing NVL-mode text directly after ADV-mode text.
    ## - Cuando se usa texto en modo NVL inmediatamente después de
    ##   texto en modo ADV.
    config.adv_nvl_transition = dissolve

    ## Used when showing ADV-mode text directly after NVL-mode text.
    ## - Cuando se usa texto en modo ADV inmediatamente después de
    ##   texto en modo NVL.
    config.nvl_adv_transition = dissolve

    ## Used when yesno is shown.
    ## - Cuando se muestra la pantalla Sí/No
    config.enter_yesno_transition = None

    ## Used when the yesno is hidden.
    ## - Cuando se oculta la pantalla Sí/No
    config.exit_yesno_transition = None

    ## Used when entering a replay.
    ## - Cuando se entra a una repetición.
    config.enter_replay_transition = None

    ## Used when exiting a replay.
    ## - Cuando se sale de una repetición.
    config.exit_replay_transition = None

    ## Used when the image is changed by a say statement with image attributes.
    ## - Cuando la imagen cambia por una sentencia 'say' con atributos de
    ##   imagen.
    config.say_attribute_transition = None

    #########################################
    ## This is the name of the directory where the game's data is
    ## stored. (It needs to be set early, before any other init code
    ## is run, so the persistent information can be found by the init code.)
    ## - Nombre del directorio en el cual se almacenan los datos del juego.
    ##   (Debe ajustarse al inicio, antes de los otros bloques 'init', para
    ##   que la información persistente pueda ser encontrada por el código
    ##   'init'.)
python early:
    config.save_directory = "PROJECT_NAME-UNIQUE"

init -1 python hide:
    #########################################
    ## Default values of Preferences.
    ## - Valores por defecto de las Opciones

    ## Note: These options are only evaluated the first time a
    ## game is run. To have them run a second time, delete
    ## game/saves/persistent
    ## - Nota: Estas opciones tan solo son evaluadas la primera vez que
    ##   se ejecuta un juego. Para que sean evaluadas una segunda vez,
    ##   bórrese games/saves/persistent

    ## Should we start in fullscreen mode?
    ## - Ajusta a 'True' para comenzar en pantalla completa

    config.default_fullscreen = False

    ## The default text speed in characters per second. 0 is infinite.
    ## - Velocidad del texto por defecto en caracteres por segundo.
    ##   0 es infinito.

    config.default_text_cps = 0

    ## The default auto-forward time setting.
    ## - El ajuste de auto-avance por defecto.

    config.default_afm_time = 10

    #########################################
    ## More customizations can go here.
    ## - Más personalizaciones pueden ir aquí.
