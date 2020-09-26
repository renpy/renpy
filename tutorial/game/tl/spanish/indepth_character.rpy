
# game/indepth_character.rpy:11
translate spanish demo_character_e7e1b1bb:

    # e "We've already seen how to define a Character in Ren'Py. But I want to go into a bit more detail as to what a Character is."
    e "Ya hemos visto cómo definir 'Character' en Ren'Py, pero quiero entrar en más detalles sobre qué es un 'Character'."

# game/indepth_character.rpy:17
translate spanish demo_character_d7908a94:

    # e "Here are couple of additional characters."
    e "Aquí hay un par de personajes adicionales."

# game/indepth_character.rpy:19
translate spanish demo_character_275ef8b9:

    # e "Each statement creates a Character object, and gives it a single argument, a name. If the name is 'None', no name is displayed."
    e "Cada sentencia crea un objeto 'Character' y le da un solo argumento, un nombre. Si el nombre es None, no se muestra ningún nombre."

# game/indepth_character.rpy:21
translate spanish demo_character_a63aea0c:

    # e "This can be followed by named arguments that set properties of the character. A named argument is a property name, an equals sign, and a value."
    e "Esto puede ser seguido por argumentos con nombre que establecen las propiedades del personaje. Un argumento con nombre es el nombre de propiedad, un signo igual y un valor."

# game/indepth_character.rpy:23
translate spanish demo_character_636a502e:

    # e "Multiple arguments should be separated with commas, like they are here. Let's see those characters in action."
    e "Los argumentos múltiples se deben separar con comas, como están aquí. Veamos esos personajes en acción."

# game/indepth_character.rpy:27
translate spanish demo_character_44b54e1d:

    # e_shout "I can shout!"
    e_shout "Puedo gritar"

# game/indepth_character.rpy:29
translate spanish demo_character_a9646dd8:

    # e_whisper "And I can speak in a whisper."
    e_whisper "Y puedo hablar susurrando."

# game/indepth_character.rpy:31
translate spanish demo_character_79793208:

    # e "This example shows how the name Character is a bit of a misnomer. Here, we have multiple Characters in use, but you see it as me speaking."
    e "Este ejemplo muestra cómo el nombre 'Character' es un poco inapropiado. Aquí, tenemos varios 'Characters' en uso, pero los ves como mi hablar."

# game/indepth_character.rpy:33
translate spanish demo_character_5d5d7482:

    # e "It's best to think of a Character as repesenting a name and style, rather than a single person."
    e "Es mejor pensar que un 'Character' representa un nombre y un estilo, en lugar de una sola persona."

# game/indepth_character.rpy:37
translate spanish demo_character_66d08d98:

    # e "There are a lot of properties that can be given to Characters, most of them prefixed styles."
    e "Hay muchas propiedades que se pueden asignar a los 'Characters', la mayoría de ellos con estilos prefijados."

# game/indepth_character.rpy:39
translate spanish demo_character_7e0d75aa:

    # e "Properties beginning with window apply to the textbox, those with what apply to the the dialogue, and those with who to the name of Character speaking."
    e "Las propiedades que comienzan con 'window' se aplican al cuadro de texto, aquellas con 'what' se aplican al diálogo y aquellas con 'who' al nombre del Character que habla."

# game/indepth_character.rpy:41
translate spanish demo_character_56703784:

    # e "If you leave a prefix out, the style customizes the name of the speaker."
    e "Si dejas un prefijo, el estilo personaliza el nombre del orador."

# game/indepth_character.rpy:43
translate spanish demo_character_b456f0a9:

    # e "There are quite a few different properties that can be set this way. Here are some of the most useful."
    e "Hay bastantes propiedades diferentes que se pueden establecer de esta manera. Éstos son algunos de los más útiles."

# game/indepth_character.rpy:48
translate spanish demo_character_31ace18e:

    # e1 "The window_background property sets the image that's used for the background of the textbox, which should be the same size as the default in gui/textbox.png."
    e1 "La propiedad 'window_background' establece la imagen que se utiliza para el fondo del cuadro de texto, que debe tener el mismo tamaño que el predeterminado en gui/textbox.png."

# game/indepth_character.rpy:54
translate spanish demo_character_18ba073d:

    # e1a "If it's set to None, the textbox has no background window."
    e1a "Si está configurado como 'None', el cuadro de texto no tiene ventana de fondo."

# game/indepth_character.rpy:59
translate spanish demo_character_5a26445c:

    # e2 "The who_color and what_color properties set the color of the character's name and dialogue text, respectively."
    e2 "Las propiedades 'who_color' y 'what_color' establecen el color del texto del nombre y diálogo del personaje, respectivamente."

# game/indepth_character.rpy:61
translate spanish demo_character_88a18c32:

    # e2 "The colors are strings containing rgb hex codes, the same sort of colors understood by a web browser."
    e2 "Los colores son cadenas que contienen códigos hexadecimales rgb, el mismo tipo de colores que entiende un navegador web."

# game/indepth_character.rpy:67
translate spanish demo_character_ed690751:

    # e3 "Similarly, the who_font and what_font properties set the font used by the different kinds of text."
    e3 "De manera similar, las propiedades 'who_font' y 'what_font' establecen la fuente utilizada por los diferentes tipos de texto."

# game/indepth_character.rpy:74
translate spanish demo_character_8dfa6426:

    # e4 "Setting the who_bold, what_italic, and what_size properties makes the name bold, and the dialogue text italic at a size of 20 pixels."
    e4 "La configuración de las propiedades 'who_bold', 'what_italic' y 'what_size' hace que el nombre aparezca en negrita y el texto del diálogo en cursiva a un tamaño de 20 píxeles."

# game/indepth_character.rpy:76
translate spanish demo_character_20e83c32:

    # e4 "Of course, the what_bold, who_italic and who_size properties also exist, even if they're not used here."
    e4 "Por supuesto, las propiedades 'what_bold', 'who_italic' y 'who_size' también existen, incluso si no se usan aquí."

# game/indepth_character.rpy:83
translate spanish demo_character_e4cbb1f2:

    # e5 "The what_outlines property puts an outline around the text."
    e5 "La propiedad 'what_outlines' coloca un contorno alrededor del texto."

# game/indepth_character.rpy:85
translate spanish demo_character_71535ecf:

    # e5 "It's a little complicated since it takes a list with a tuple in it, with the tuple being four things in parenthesis, and the list the square brackets around them."
    e5 "Es un poco complicado, ya que toma una lista con una tupla, con la tupla cuatro valores entre paréntesis, y los corchetes de la lista a su alrededor."

# game/indepth_character.rpy:87
translate spanish demo_character_e9ac7482:

    # e5 "The first number is the size of the outline, in pixels. That's followed by a string giving the hex-code of the color of the outline, and the x and y offsets."
    e5 "El primer número es el tamaño del contorno, en píxeles. A esto le sigue una cadena que proporciona el código hexadecimal del color del contorno y los desplazamientos de x e y."

# game/indepth_character.rpy:93
translate spanish demo_character_ea72d988:

    # e6 "When the outline size is 0 and the offsets are given, what_outlines can also act as a drop-shadow behind the text."
    e6 "Cuando el tamaño del contorno es 0 y se dan los desplazamientos, 'what_outlines' también puede actuar como una sombra detrás del texto."

# game/indepth_character.rpy:99
translate spanish demo_character_8d35ebcd:

    # e7 "The what_xalign and what_textalign properties control the alignment of text, with 0.0 being left, 0.5 being center, and 1.0 being right."
    e7 "Las propiedades 'what_xalign' y 'what_textalign' controlan la alineación del texto, con 0.0 a la izquierda, 0,5 al centro y 1.0 a la derecha."

# game/indepth_character.rpy:101
translate spanish demo_character_7c75906c:

    # e7 "The what_xalign property controls where all the text itself is placed within the textbox, while what_textalign controls where rows of text are placed relative to each other."
    e7 "La propiedad 'what_xalign' controla dónde se coloca todo el texto dentro del cuadro de texto, mientras que 'what_textalign' controla dónde se colocan las filas de texto relativas entre sí."

# game/indepth_character.rpy:103
translate spanish demo_character_e2811c1c:

    # e7 "Generally you'll want to to set them both what_xalign and what_textalign to the same value."
    e7 "Por lo general, querrás establecerlos 'what_xalign' y 'what_textalign' en el mismo valor."

# game/indepth_character.rpy:105
translate spanish demo_character_baa52234:

    # e7 "Setting what_layout to 'subtitle' puts Ren'Py in subtitle mode, which tries to even out the length of every line of text in a block."
    e7 "Al establecer 'what_layout' en 'subtitle' pones a Ren'Py en el modo de subtítulos, que intenta igualar la longitud de cada línea de texto en un bloque."

# game/indepth_character.rpy:110
translate spanish demo_character_41190f01:

    # e8 "These properties can be combined to achieve many different effects."
    e8 "Estas propiedades se pueden combinar para lograr muchos efectos diferentes."

# game/indepth_character.rpy:124
translate spanish demo_character_aa12d9ca:

    # e8 "This example hides the background and shows dialogue centered and outlined, as if the game is being subtitled."
    e8 "Este ejemplo oculta el fondo y muestra el diálogo centrado y delineado, como si el juego estuviera subtitulado."

# game/indepth_character.rpy:133
translate spanish demo_character_a7f243e5:

    # e9 "There are two interesting non-style properties, what_prefix and what_suffix. These can put text at the start and end of a line of dialogue."
    e9 "Hay dos propiedades interesantes que no son de estilo, 'what_prefix' y 'what_suffix'. Estos pueden poner texto al principio y al final de una línea de diálogo."

# game/indepth_character.rpy:139
translate spanish demo_character_f9b0052f:

    # e "By using kind, you can copy properties from one character to another, changing only what you need to."
    e "Al usar 'kind', puede copiar las propiedades de un personaje a otro, cambiando solo lo que necesitas."

# game/indepth_character.rpy:148
translate spanish demo_character_6dfce4b7:

    # l8 "Like this! Finally I get some more dialogue around here."
    l8 "¡Me gusta esto! Finalmente consigo un poco más de diálogo por aquí."

# game/indepth_character.rpy:157
translate spanish demo_character_68d9e46c:

    # e "The last thing you have to know is that there's a special character, narrator, that speaks narration. Got it?"
    e "Lo último que debes saber es que hay un personaje especial, 'narrator' (narrador), que habla narración. ¿Entendido?"

# game/indepth_character.rpy:159
translate spanish demo_character_0c8f314a:

    # "I think I do."
    "Eso creo."

