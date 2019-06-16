
# game/tutorial_screen_displayables.rpy:3
translate spanish screen_displayables_7c897a6d:

    # e "There are quite a few screen displayables. Here, I'll tell you about some of the most important ones."
    e "Hay bastantes visualizables screen. Aquí les contaré algunas de las más importantes."

# game/tutorial_screen_displayables.rpy:9
translate spanish screen_displayables_menu_fef7b441:

    # e "What would you like to know about?" nointeract
    e "¿Qué te gustaría saber?" nointeract

# game/tutorial_screen_displayables.rpy:49
translate spanish screen_displayable_properties_76c5639a:

    # e "There are a few properties that every screen language displayable shares. Here, I'll demonstrate them for you."
    e "Hay algunas propiedades que todos visualizables del lenguaje de pantalla comparten. Aquí, te las demostraré."

# game/tutorial_screen_displayables.rpy:57
translate spanish screen_displayable_properties_527d4b4e:

    # e "First off, every screen language displayable supports the position properties. When the container a displayable is in supports it, you can use properties like align, anchor, pos, and so so on."
    e "En primer lugar, todos los lenguajes de visualizables screen admiten las propiedades de posición. Cuando el contenedor en el que se puede exhibir lo admite, puedes usar propiedades como align, anchor, pos, etc."

# game/tutorial_screen_displayables.rpy:69
translate spanish screen_displayable_properties_8aff26dd:

    # e "The at property applies a transform to the displayable, the same way the at clause in the show statement does."
    e "La propiedad at aplica una transformación al visualizable, de la misma forma que lo hace la cláusula at en la sentencia show."

# game/tutorial_screen_displayables.rpy:106
translate spanish screen_displayable_properties_2ed40a70:

    # e "The id property is mostly used with the say screen, which is used to show dialogue. Outside of the say screen, it isn't used much."
    e "La propiedad id se usa principalmente con la pantalla say, que se usa para mostrar el diálogo. Fuera de la pantalla de say, no se usa mucho."

# game/tutorial_screen_displayables.rpy:108
translate spanish screen_displayable_properties_da5733d1:

    # e "It tells Ren'Py which displayables are the background window, 'who' is speaking, and 'what' is being said. This used to apply per-Character styles, and help with auto-forward mode."
    e "Le dice a Ren'Py qué visualizables son la ventana de fondo, 'who' quién hablan y 'what' que se dice. Se usa para aplicar estilos por Character, y ayuda con el modo de avance automático."

# game/tutorial_screen_displayables.rpy:123
translate spanish screen_displayable_properties_cc09fade:

    # e "The style property lets you specify the style of a single displayable."
    e "La propiedad de estilo te permiten especificar el estilo de un solo visualizable."

# game/tutorial_screen_displayables.rpy:144
translate spanish screen_displayable_properties_a7f4e25c:

    # e "The style_prefix property sets the prefix of the style that's used for a displayable and its children."
    e "La propiedad style_prefix establece el prefijo del estilo que se usa para un visualizable y sus hijos."

# game/tutorial_screen_displayables.rpy:146
translate spanish screen_displayable_properties_6bdb0723:

    # e "For example, when the style_prefix property is 'green', the vbox has the 'green_vbox' style, and the text in it has the 'green_text' style."
    e "Por ejemplo, cuando la propiedad style_prefix es 'green', vbox tiene el estilo 'green_vbox' y el texto tiene el estilo 'green_text'."

# game/tutorial_screen_displayables.rpy:150
translate spanish screen_displayable_properties_8a3a8635:

    # e "There are a few more properties than these, and you can find the rest in the documentation. But these are the ones you can expect to see in your game, in the default screens."
    e "Hay algunas propiedades más que éstas, y puede encontrar el resto en la documentación. Pero estos son los que puedes esperar ver en tu juego, en las pantallas predeterminadas."

# game/tutorial_screen_displayables.rpy:156
translate spanish add_displayable_ec121c5c:

    # e "Sometimes you'll have a displayable, like an image, that you want to add to a screen."
    e "A veces, tendrás un visualizable, como una imagen, que deseas agregar a una pantalla."

# game/tutorial_screen_displayables.rpy:165
translate spanish add_displayable_7ec3e2b0:

    # e "This can be done using the add statement, which adds an image or other displayable to the screen."
    e "Esto se puede hacer usando la sentencia add, que agrega una imagen u otro visualizable en la pantalla."

# game/tutorial_screen_displayables.rpy:167
translate spanish add_displayable_7112a377:

    # e "There are a few ways to refer to the image. If it's in the images directory or defined with the image statement, you can just put the name inside a quoted string."
    e "Hay algunas maneras de referirse a la imagen. Si está en el directorio de imágenes o definido con la sentencia image, solo pon el nombre dentro de una cadena entre comillas."

# game/tutorial_screen_displayables.rpy:176
translate spanish add_displayable_8ba81c26:

    # e "An image can also be referred to by it's filename, relative to the game directory."
    e "También se puede hacer referencia a una imagen por su nombre de archivo, en relación con el directorio del juego."

# game/tutorial_screen_displayables.rpy:185
translate spanish add_displayable_1f5571e3:

    # e "Other displayables can also be added using the add statement. Here, we add the Solid displayable, showing a solid block of color."
    e "También se pueden agregar otros visualizables utilizando la instrucción add. Aquí, agregamos el visualizable Solid, mostrando un bloque sólido de color."

# game/tutorial_screen_displayables.rpy:195
translate spanish add_displayable_0213ffa2:

    # e "In addition to the displayable, the add statement can be given transform properties. These can place or otherwise transform the displayable being added."
    e "Además de visualizables, a la instrucción add se le pueden dar propiedades de transformación. Estos pueden colocar o transformar el visualizable agregando."

# game/tutorial_screen_displayables.rpy:207
translate spanish add_displayable_3a56a464:

    # e "Of course, the add statement can also take the at property, letting you give it a more complex transform."
    e "Por supuesto, la instrucción add también puede tomar la propiedad at, permitiéndole darle una transformación más compleja."

# game/tutorial_screen_displayables.rpy:222
translate spanish text_displayable_96f88225:

    # e "The screen language text statement adds a text displayable to the screen. It takes one argument, the text to be displayed."
    e "La sentencia text del lenguaje de pantalla agrega un visualizable text a la pantalla. Toma un argumento, el texto que se mostrará."

# game/tutorial_screen_displayables.rpy:224
translate spanish text_displayable_1ed1a8c2:

    # e "In addition to the common properties that all displayables take, text takes the text style properties. For example, size sets the size of the text."
    e "Además de las propiedades comunes que toman todos los visualizables, el texto toma las propiedades de estilo text. Por ejemplo, tamaño establece el tamaño del texto."

# game/tutorial_screen_displayables.rpy:234
translate spanish text_displayable_9351d9dd:

    # e "The text displayable can also interpolate values enclosed in square brackets."
    e "El visualizable text también puede interpolar valores encerrados entre corchetes."

# game/tutorial_screen_displayables.rpy:236
translate spanish text_displayable_32d76ccb:

    # e "When text is displayed in a screen using the text statement variables defined in the screen take precedence over those defined outside it."
    e "Cuando el texto se muestra en una pantalla, las variables de sentencia text definidas en la pantalla tienen prioridad sobre las definidas fuera de ella."

# game/tutorial_screen_displayables.rpy:238
translate spanish text_displayable_7e84a5d1:

    # e "Those variables may be parameters given to the screen, defined with the default or python statements, or set using the SetScreenVariable action."
    e "Esas variables pueden ser parámetros dados a la pantalla, definidos con las sentencias predeterminadas o de Python, o configurados mediante la acción SetScreenVariable."

# game/tutorial_screen_displayables.rpy:247
translate spanish text_displayable_8bc866c4:

    # e "There's not much more to say about text in screens, as it works the same way as all other text in Ren'Py."
    e "No hay mucho más que decir sobre el texto en las pantallas, ya que funciona de la misma manera que el resto del texto en Ren'Py."

# game/tutorial_screen_displayables.rpy:255
translate spanish layout_displayables_d75efbae:

    # e "The layout displayables take other displayables and lay them out on the screen."
    e "El visualizable layout toma otros visualizables y los coloca en la pantalla."

# game/tutorial_screen_displayables.rpy:269
translate spanish layout_displayables_9a15144d:

    # e "For example, the hbox displayable takes its children and lays them out horizontally."
    e "Por ejemplo, el visualizable hbox toma a sus hijos y los coloca horizontalmente."

# game/tutorial_screen_displayables.rpy:284
translate spanish layout_displayables_48eff197:

    # e "The vbox displayable is similar, except it takes its children and arranges them vertically."
    e "El visualizable vbox es similar, excepto que toma a sus hijos y los organiza verticalmente."

# game/tutorial_screen_displayables.rpy:286
translate spanish layout_displayables_74de8a66:

    # e "Both of the boxes take the box style properties, the most useful of which is spacing, the amount of space to leave between children."
    e "Ambas cajas toman las propiedades de estilo de box, la más útil de las cuales es el spacing, la cantidad de espacio para dejar entre los hijos."

# game/tutorial_screen_displayables.rpy:301
translate spanish layout_displayables_a156591f:

    # e "The grid displayable displays its children in a grid of equally-sized cells. It takes two arguments, the number of columns and the number of rows."
    e "El visualizable grid  muestra a sus hijos en una malla de celdas de igual tamaño. Toma dos argumentos, el número de columnas y el número de filas."

# game/tutorial_screen_displayables.rpy:303
translate spanish layout_displayables_126f5816:

    # e "The grid has to be full, or Ren'Py will produce an error. Notice how in this example, the empty cell is filled with a null."
    e "La malla tiene que estar llena, o Ren'Py producirá un error. Observe cómo en este ejemplo, la celda vacía se rellena con un valor null."

# game/tutorial_screen_displayables.rpy:305
translate spanish layout_displayables_bfaaaf9b:

    # e "Like the boxes, grid uses the spacing property to specify the space between cells."
    e "Al igual que las boxes, grid utiliza la propiedad de espaciado para especificar el espacio entre las celdas."

# game/tutorial_screen_displayables.rpy:321
translate spanish layout_displayables_3e931106:

    # e "Grid also takes the transpose property, to make it fill top-to-bottom before it fills left-to-right."
    e "Grid también toma la propiedad de transposición, para que se llene de arriba a abajo antes de que se llene de izquierda a derecha."

# game/tutorial_screen_displayables.rpy:338
translate spanish layout_displayables_afdc1b11:

    # e "And just to demonstrate that all cells are equally-sized, here's what happens when once child is bigger than the others."
    e "Y solo para demostrar que todas las celdas tienen el mismo tamaño, esto es lo que sucede cuando un hijo es más grande que los demás."

# game/tutorial_screen_displayables.rpy:353
translate spanish layout_displayables_a23e2826:

    # e "The fixed displayable displays the children using Ren'Py's normal placement algorithm. This lets you place displayables anywhere in the screen."
    e "El visualizable fixed muestra a los hijos utilizando el algoritmo de colocación normal de Ren'Py. Esto le permite colocar visualizables en cualquier lugar de la pantalla."

# game/tutorial_screen_displayables.rpy:355
translate spanish layout_displayables_fd3926ca:

    # e "By default, the layout expands to fill all the space available to it. To prevent that, we use the xsize and ysize properties to set its size in advance."
    e "De forma predeterminada, el layout se expande para llenar todo el espacio disponible. Para evitar eso, usamos las propiedades xsize y ysize para establecer su tamaño por adelantado."

# game/tutorial_screen_displayables.rpy:369
translate spanish layout_displayables_eff42786:

    # e "When a non-layout displayable is given two or more children, it's not necessary to create a fixed. A fixed is automatically added, and the children are added to it."
    e "Cuando a un visualizable que no sea layout da dos o más hijos, no es necesario crear un fixed. Se agrega automáticamente fixed, y se agregan los hijos."

# game/tutorial_screen_displayables.rpy:384
translate spanish layout_displayables_c32324a7:

    # e "Finally, there's one convenience to save space. When many displayables are nested, adding a layout to each could cause crazy indent levels."
    e "Por último, hay una conveniencia para ahorrar espacio. Cuando se anidan muchos visualizables, agregar un diseño a cada uno podría causar niveles de sangría locos."

# game/tutorial_screen_displayables.rpy:386
translate spanish layout_displayables_d7fa0f28:

    # e "The has statement creates a layout, and then adds all further children of its parent to that layout. It's just a convenience to make screens more readable."
    e "La sentencia has crea un diseño y luego agrega todos los demás hijos de su padre a ese diseño. Es solo una conveniencia para hacer las pantallas más legibles."

# game/tutorial_screen_displayables.rpy:395
translate spanish window_displayables_14beb786:

    # e "In the default GUI that Ren'Py creates for a game, most user interface elements expect some sort of background."
    e "En la GUI predeterminada que Ren'Py crea para un juego, la mayoría de los elementos de la interfaz de usuario esperan algún tipo de fondo."

# game/tutorial_screen_displayables.rpy:405
translate spanish window_displayables_495d332b:

    # e "Without the background, text can be hard to read. While a frame isn't strictly required, many screens have one or more of them."
    e "Sin el fondo, el texto puede ser difícil de leer. Mientras que un marco no es estrictamente requerido, muchas pantallas tienen uno o más."

# game/tutorial_screen_displayables.rpy:417
translate spanish window_displayables_2c0565ab:

    # e "But when I add a background, it's much easier. That's why there are two displayables that are intended to give backgrounds to user interface elements."
    e "Pero cuando agrego un fondo, es mucho más fácil. Es por eso que hay dos visualizables destinados a proporcionar fondos a los elementos de la interfaz de usuario."

# game/tutorial_screen_displayables.rpy:419
translate spanish window_displayables_c7d0968c:

    # e "The two displayables are frame and window. Frame is the one we use above, and it's designed to provide a background for arbitrary parts of the user interface."
    e "Los dos visualizables son frame y window. El que usamos anteriormente es frame, y está diseñado para proporcionar un fondo para partes arbitrarias de la interfaz de usuario."

# game/tutorial_screen_displayables.rpy:423
translate spanish window_displayables_7d843f62:

    # e "On the other hand, the window displayable is very specific. It's used to provide the text window. If you're reading what I'm saying, you're looking at the text window right now."
    e "Por otro lado, el visualizable window es muy específico. Se utiliza para proporcionar la ventana de texto. Si estás leyendo lo que estoy diciendo, estás mirando la ventana de texto ahora mismo."

# game/tutorial_screen_displayables.rpy:425
translate spanish window_displayables_de5963e4:

    # e "Both frames and windows can be given window style properties, allowing you to change things like the background, margins, and padding around the window."
    e "Tanto frames como windows pueden recibir propiedades de estilo window, lo que le permite cambiar elementos como el fondo, los márgenes y el relleno alrededor de la ventana."

# game/tutorial_screen_displayables.rpy:433
translate spanish button_displayables_ea626553:

    # e "One of the most flexible displayables is the button displayable, and its textbutton and imagebutton variants."
    e "Uno de los indicadores más flexibles es el visualizable button, y sus variantes textbutton y imagebutton."

# game/tutorial_screen_displayables.rpy:443
translate spanish button_displayables_372dcc0f:

    # e "A button is a displayable that when selected runs an action. Buttons can be selected by clicking with the mouse, by touch, or with the keyboard and controller."
    e "Un botón es un botón visualizable que, cuando se selecciona, ejecuta una acción. Los botones se pueden seleccionar haciendo clic con el mouse, por touch o con el teclado y mando."

# game/tutorial_screen_displayables.rpy:445
translate spanish button_displayables_a6b270ff:

    # e "Actions can do many things, like setting variables, showing screens, jumping to a label, or returning a value. There are many {a=https://www.renpy.org/doc/html/screen_actions.html}actions in the Ren'Py documentation{/a}, and you can also write your own."
    e "Las acciones(action) pueden hacer muchas cosas, como establecer variables, mostrar pantallas, saltar a una etiqueta o devolver un valor. Hay muchas acciones {a=https://www.renpy.org/doc/html/screen_actions.html}en la documentación de Ren'Py{/a}, y también puede escribir las tuyas propias."

# game/tutorial_screen_displayables.rpy:458
translate spanish button_displayables_4c600d20:

    # e "It's also possible to run actions when a button gains and loses focus."
    e "También es posible ejecutar acciones cuando un botón gana y pierde el foco."

# game/tutorial_screen_displayables.rpy:473
translate spanish button_displayables_47af4bb9:

    # e "A button takes another displayable as children. Since that child can be a layout, it can takes as many children as you want."
    e "Un button toma otro visualizables como hijos. Dado que ese hijo puede ser un layout, puede tomar tantos hijos como quierass."

# game/tutorial_screen_displayables.rpy:483
translate spanish button_displayables_d01adde3:

    # e "In many cases, buttons will be given text. To make that easier, there's the textbutton displayable that takes the text as an argument."
    e "En muchos casos, los botones recibirán texto. Para hacerlo más fácil, está el visualizable textbutton que toma el texto como un argumento."

# game/tutorial_screen_displayables.rpy:485
translate spanish button_displayables_01c551b3:

    # e "Since the textbutton displayable manages the style of the button text for you, it's the kind of button that's used most often in the default GUI."
    e "Dado que el visualizable textbutton administra el estilo del texto del botón por ti, es el tipo de botón que se usa con más frecuencia en la GUI predeterminada."

# game/tutorial_screen_displayables.rpy:498
translate spanish button_displayables_6911fb9b:

    # e "There's also the imagebutton, which takes displayables, one for each state the button can be in, and displays them as the button."
    e "También está el imagebutton, que toma visualizables, uno para cada estado en el que puede estar el botón, y los muestra como el botón."

# game/tutorial_screen_displayables.rpy:500
translate spanish button_displayables_49720fa6:

    # e "An imagebutton gives you the most control over what a button looks like, but is harder to translate and won't look as good if the game window is resized."
    e "Un imagebutton te da el mayor control sobre el aspecto de un botón, pero es más difícil de traducir y no se verá tan bien si se cambia el tamaño de la ventana del juego."

# game/tutorial_screen_displayables.rpy:522
translate spanish button_displayables_e8d40fc8:

    # e "Buttons take Window style properties, that are used to specify the background, margins, and padding. They also take Button-specific properties, like a sound to play on hover."
    e "Los botones toman las propiedades de estilo Window, que se utilizan para especificar el fondo, los márgenes y el relleno. También tienen propiedades específicas de los botones, como un sonido para reproducir cuando se enfocan."

# game/tutorial_screen_displayables.rpy:524
translate spanish button_displayables_1e40e311:

    # e "When used with a button, style properties can be given prefixes like idle and hover to make the property change with the button state."
    e "Cuando se usa con un botón, las propiedades de estilo pueden tener prefijos como idle y hover para hacer que la propiedad cambie con el estado del botón."

# game/tutorial_screen_displayables.rpy:526
translate spanish button_displayables_220b020d:

    # e "A text button also takes Text style properties, prefixed with text. These are applied to the text displayable it creates internally."
    e "Un botón de texto también toma las propiedades de estilo de texto, prefijadas con text. Estos se aplican al texto desplegable que crea internamente."

# game/tutorial_screen_displayables.rpy:558
translate spanish button_displayables_b89d12aa:

    # e "Of course, it's prety rare we'd ever customize a button in a screen like that. Instead, we'd create custom styles and tell Ren'Py to use them."
    e "Por supuesto, es muy raro que personalicemos un botón en una pantalla como esa. En su lugar, crearíamos estilos personalizados y le diríamos a Ren'Py que los use."

# game/tutorial_screen_displayables.rpy:577
translate spanish bar_displayables_946746c2:

    # e "The bar and vbar displayables are flexible displayables that show bars representing a value. The value can be static, animated, or adjustable by the player."
    e "Los visualizables bar y vbar son visualizables flexibles que muestran barras que representan un valor. El valor puede ser estático, animado o ajustable por el jugador."

# game/tutorial_screen_displayables.rpy:579
translate spanish bar_displayables_af3a51b8:

    # e "The value property gives a BarValue, which is an object that determines the bar's value and range. Here, a StaticValue sets the range to 100 and the value to 66, making a bar that's two thirds full."
    e "La propiedad value proporciona un BarValue, que es un objeto que determina el valor y el rango de la barra. Aquí, un StaticValue establece el rango en 100 y el valor en 66, haciendo que una barra esté dos tercios llena."

# game/tutorial_screen_displayables.rpy:581
translate spanish bar_displayables_62f8b0ab:

    # e "A list of all the BarValues that can be used is found {a=https://www.renpy.org/doc/html/screen_actions.html#bar-values}in the Ren'Py documentation{/a}."
    e "Una lista de todos los BarValues que se pueden usar se encuentra {a=https://www.renpy.org/doc/html/screen_actions.html#bar-values}en la documentación de Ren'Py{/a}."

# game/tutorial_screen_displayables.rpy:583
translate spanish bar_displayables_5212eb0a:

    # e "In this example, we give the frame the xsize property. If we didn't do that, the bar would expand to fill all available horizontal space."
    e "En este ejemplo, le damos a frame la propiedad xsize. Si no hiciéramos eso, la barra se expandiría para llenar todo el espacio horizontal disponible."

# game/tutorial_screen_displayables.rpy:600
translate spanish bar_displayables_67295018:

    # e "There are a few different bar styles that are defined in the default GUI. The styles are selected by the style property, with the default selected by the value."
    e "Hay algunos estilos de barras diferentes que se definen en la GUI predeterminada. Los estilos son seleccionados por la propiedad de estilo, con el valor predeterminado seleccionado por el valor."

# game/tutorial_screen_displayables.rpy:602
translate spanish bar_displayables_1b037b21:

    # e "The top style is the 'bar' style. It's used to display values that the player can't adjust, like a life or progress bar."
    e "El estilo superior es el estilo 'bar'. Se utiliza para mostrar valores que el jugador no puede ajustar, como una barra de vida o de progreso."

# game/tutorial_screen_displayables.rpy:604
translate spanish bar_displayables_c2aa4725:

    # e "The middle stye is the 'slider' value. It's used for values the player is expected to adjust, like a volume preference."
    e "El estilo de en medio es el valor 'slider'. Se usa para los valores que se espera que el jugador ajuste, como una preferencia de volumen."

# game/tutorial_screen_displayables.rpy:606
translate spanish bar_displayables_2fc44226:

    # e "Finally, the bottom style is the 'scrollbar' style, which is used for horizontal scrollbars. When used as a scrollbar, the thumb in the center changes size to reflect the visible area of a viewport."
    e "Finalmente, el estilo inferior es el estilo 'scrollbar', que se usa para las barras de desplazamiento horizontal. Cuando se utiliza como una barra de desplazamiento, el thumb en el centro cambia de tamaño para reflejar el área visible de una ventana gráfica."

# game/tutorial_screen_displayables.rpy:623
translate spanish bar_displayables_26eb88bf:

    # e "The vbar displayable is similar to the bar displayable, except it uses vertical styles - 'vbar', 'vslider', and 'vscrollbar' - by default."
    e "El visualizable vbar es similar al visualizable bar, excepto que usa estilos verticales: 'vbar', 'vslider' y 'vscrollbar' - de forma predeterminada."

# game/tutorial_screen_displayables.rpy:626
translate spanish bar_displayables_11cf8af2:

    # e "Bars take the Bar style properties, which can customize the look and feel greatly. Just look at the difference between the bar, slider, and scrollbar styles."
    e "Las baras toman las propiedades de estilo Bar, que pueden personalizar la apariencia enormemente. Solo mira la diferencia entre los estilos de bar, slider y scrollbar."

# game/tutorial_screen_displayables.rpy:635
translate spanish imagemap_displayables_d62fad02:

    # e "Imagemaps use two or more images to show buttons and bars. Let me start by showing you an example of an imagemap in action."
    e "Los Imagemaps utilizan dos o más imágenes para mostrar botones y barras. Permítame comenzar mostrándote un ejemplo de un Imagemap en acción."

# game/tutorial_screen_displayables.rpy:657
translate spanish swimming_405542a5:

    # e "You chose swimming."
    e "Elegiste swimming."

# game/tutorial_screen_displayables.rpy:659
translate spanish swimming_264b5873:

    # e "Swimming seems like a lot of fun, but I didn't bring my bathing suit with me."
    e "La natación parece muy divertida, pero no traje mi traje de baño."

# game/tutorial_screen_displayables.rpy:665
translate spanish science_83e5c0cc:

    # e "You chose science."
    e "Elegiste science."

# game/tutorial_screen_displayables.rpy:667
translate spanish science_319cdf4b:

    # e "I've heard that some schools have a competitive science team, but to me research is something that can't be rushed."
    e "He oído que algunas escuelas tienen un equipo científico competitivo, pero para mí la investigación es algo que no se puede apresurar."

# game/tutorial_screen_displayables.rpy:672
translate spanish art_d2a94440:

    # e "You chose art."
    e "Elegiste art."

# game/tutorial_screen_displayables.rpy:674
translate spanish art_e6af6f1d:

    # e "Really good background art is hard to make, which is why so many games use filtered photographs. Maybe you can change that."
    e "Realmente es difícil hacer una buena imagen de fondo, razón por la cual muchos juegos usan fotografías filtradas. Tal vez puedas cambiar eso."

# game/tutorial_screen_displayables.rpy:680
translate spanish home_373ea9a5:

    # e "You chose to go home."
    e "Elegiste go home."

# game/tutorial_screen_displayables.rpy:686
translate spanish imagemap_done_48eca0a4:

    # e "Anyway..."
    e "Como sea"

# game/tutorial_screen_displayables.rpy:691
translate spanish imagemap_done_a60635a1:

    # e "To demonstrate how imagemaps are put together, I'll show you the five images that make up a smaller imagemap."
    e "Para demostrar cómo se combinan los imagemaps, te mostraré las cinco imágenes que conforman un imagemaps más pequeño."

# game/tutorial_screen_displayables.rpy:697
translate spanish imagemap_done_ac9631ef:

    # e "The idle image is used for the background of the imagemap, for hotspot buttons that aren't focused or selected, and for the empty part of an unfocused bar."
    e "La imagen idle se usa para el fondo del mapa de imágenes, para los botones hotspot que no están enfocados o seleccionados, y para la parte vacía de una barra desenfocada."

# game/tutorial_screen_displayables.rpy:703
translate spanish imagemap_done_123b5924:

    # e "The hover image is used for hotspots that are focused but not selected, and for the empty part of a focused bar."
    e "La imagen hover se usa para zonas activas que están enfocadas pero no seleccionadas, y para la parte vacía de una barra enfocada."

# game/tutorial_screen_displayables.rpy:705
translate spanish imagemap_done_37f538dc:

    # e "Notice how both the bar and button are highlighted in this image. When we display them as part of a screen, only one of them will show up as focused."
    e "Observa cómo se resaltan tanto la barra como el botón en esta imagen. Cuando los mostramos como parte de una pantalla, solo uno de ellos aparecerá como enfocado."

# game/tutorial_screen_displayables.rpy:711
translate spanish imagemap_done_c76b072d:

    # e "Selected images like this selected_idle image are used for parts of the bar that are filled, and for selected buttons, like the current screen and a checked checkbox."
    e "Las imágenes seleccionadas como esta imagen selected_idle se utilizan para partes de la barra que se rellenan, y para los botones seleccionados, como la pantalla actual y una casilla de verificación marcada."

# game/tutorial_screen_displayables.rpy:717
translate spanish imagemap_done_241a4112:

    # e "Here's the selected_hover image. The button here will never be shown, since it will never be marked as selected."
    e "Aquí está la imagen selected_hover. El botón aquí nunca se mostrará, ya que nunca se marcará como seleccionado."

# game/tutorial_screen_displayables.rpy:723
translate spanish imagemap_done_3d8f454c:

    # e "Finally, an insensitive image can be given, which is used when a hotspot can't be interacted with."
    e "Finalmente, se puede dar una imagen insensitive, que se usa cuando no se puede interactuar con un hotspot."

# game/tutorial_screen_displayables.rpy:728
translate spanish imagemap_done_ca286729:

    # e "Imagemaps aren't limited to just images. Any displayable can be used where an image is expected."
    e "Los imagemap no se limitan solo a imágenes. Se puede usar cualquier visualizable donde se espera una imagen."

# game/tutorial_screen_displayables.rpy:743
translate spanish imagemap_done_6060b17f:

    # e "Here's an imagemap built using those five images. Now that it's an imagemap, you can interact with it if you want to."
    e "Aquí hay un imagemap construido usando esas cinco imágenes. Ahora que es un imagemap, puedes interactuar con él si lo deseas."

# game/tutorial_screen_displayables.rpy:755
translate spanish imagemap_done_c817794d:

    # e "To make this a little more concise, we can replace the five images with the auto property, which replaces '%%s' with 'idle', 'hover', 'selected_idle', 'selected_hover', or 'insensitive' as appropriate."
    e "Para hacer esto un poco más conciso, podemos reemplazar las cinco imágenes con la propiedad automática, que reemplaza '%%s' con 'idle', 'hover', 'selected_idle', 'selected_hover', o 'insensitive' según corresponda."

# game/tutorial_screen_displayables.rpy:757
translate spanish imagemap_done_c1ed91b8:

    # e "Feel free to omit the selected and insensitive images if your game doesn't need them. Ren'Py will use the idle or hover images to replace them."
    e "Siéntete libre de omitir las imágenes selected e insensitive si tu juego no las necesita. Ren'Py utilizará las imágenes idle o hover para reemplazarlos."

# game/tutorial_screen_displayables.rpy:759
translate spanish imagemap_done_166f75db:

    # e "The hotspot and hotbar statements describe areas of the imagemap that should act as buttons or bars, respectively."
    e "Las sentencias hotspot y hotbar describen áreas del imagemap que deben actuar como botones o barras, respectivamente."

# game/tutorial_screen_displayables.rpy:761
translate spanish imagemap_done_becb9688:

    # e "Both take the coordinates of the area, in (x, y, width, height) format."
    e "Ambas toman las coordenadas del área, en formato (x, y, ancho, alto)."

# game/tutorial_screen_displayables.rpy:763
translate spanish imagemap_done_fd56baa2:

    # e "A hotspot takes an action that is run when the hotspot is activated. It can also take actions that are run when it's hovered and unhovered, just like a button can."
    e "Un hotspot toma una acción que se ejecuta cuando el hotspot está activado. También puede tomar acciones que se ejecutan cuando está enfocado y no enfocado, al igual que un botón."

# game/tutorial_screen_displayables.rpy:765
translate spanish imagemap_done_5660a6a2:

    # e "A hotbar takes a BarValue object that describes how full the bar is, and the range of values the bar should display, just like a bar and vbar does."
    e "Una hotbar toma un objeto BarValue que describe qué tan llena está la barra y el rango de valores que debe mostrar la barra, tal como lo hace una barra y una barra vbar."

# game/tutorial_screen_displayables.rpy:772
translate spanish imagemap_done_10496a29:

    # e "A useful pattern is to define a screen with an imagemap that has hotspots that jump to labels, and call that using the call screen statement."
    e "Un patrón útil es definir una pantalla con un imagemap que tiene hotspots que saltan a las etiquetas y llamarla usando la sentencia screen."

# game/tutorial_screen_displayables.rpy:774
translate spanish imagemap_done_dcb45224:

    # e "That's what we did in the school example I showed before. Here's the script for it. It's long, but the imagemap itself is fairly simple."
    e "Eso es lo que hicimos en el ejemplo de la escuela que mostré antes. Aquí está el guión para ello. Es largo, pero el imagemap en sí es bastante simple."

# game/tutorial_screen_displayables.rpy:778
translate spanish imagemap_done_5b5bc5e5:

    # e "Imagemaps have pluses and minuses. On one hand, they are easy for a designer to create, and can look very good. At the same time, they can be hard to translate, and text baked into images may be blurry when the window is scaled."
    e "Imagemaps tienen ventajas y desventajas. Por un lado, son fáciles de crear para un diseñador y pueden verse muy bien. Al mismo tiempo, pueden ser difíciles de traducir, y el texto incrustado en las imágenes puede aparecer borroso cuando se escala la ventana."

# game/tutorial_screen_displayables.rpy:780
translate spanish imagemap_done_b6cebf2b:

    # e "It's up to you and your team to decide if imagemaps are right for your project."
    e "Depende de ti y tu equipo decidir si los imagemaps son adecuados para su proyecto."

# game/tutorial_screen_displayables.rpy:787
translate spanish viewport_displayables_e509d50d:

    # e "Sometimes, you'll want to display something bigger than the screen. That's what the viewport displayable is for."
    e "A veces, querrás mostrar algo más grande que la pantalla. Para eso está el visualizable viewport."

# game/tutorial_screen_displayables.rpy:803
translate spanish viewport_displayables_9853b0e3:

    # e "Here's an example of a simple viewport, used to display a single image that's far bigger than the screen. Since the viewport will expand to the size of the screen, we use the xysize property to make it smaller."
    e "Este es un ejemplo de un viewport simple, que se usa para mostrar una imagen única que es mucho más grande que la pantalla. Dado que el viewport ampliará al tamaño de la pantalla, usamos la propiedad xysize para hacerla más pequeña."

# game/tutorial_screen_displayables.rpy:805
translate spanish viewport_displayables_778668c8:

    # e "By default the viewport can't be moved, so we give the draggable, mousewheel, and arrowkeys properties to allow it to be moved in multiple ways."
    e "Por defecto, el viewport no se puede mover, por lo que le damos a las propiedades draggable, mousewheel y arrowkeys para permitir que se mueva de varias maneras."

# game/tutorial_screen_displayables.rpy:820
translate spanish viewport_displayables_bbd63377:

    # e "When I give the viewport the edgescroll property, the viewport automatically scrolls when the mouse is near its edges. The two numbers are the size of the edges, and the speed in pixels per second."
    e "Cuando le doy al viewport la propiedad edgescroll, la ventana se desplaza automáticamente cuando el mouse está cerca de sus bordes. Los dos números son el tamaño de los bordes y la velocidad en píxeles por segundo."

# game/tutorial_screen_displayables.rpy:839
translate spanish viewport_displayables_7c4678ee:

    # e "Giving the viewport the scrollbars property surrounds it with scrollbars. The scrollbars property can take 'both', 'horizontal', and 'vertical' as values."
    e "Al darle al viewport la propiedad de scrollbars la rodea con barras de desplazamiento. La propiedad scrollbars puede tomar 'ambos', 'horizontal' y 'vertical' como valores."

# game/tutorial_screen_displayables.rpy:841
translate spanish viewport_displayables_197953b5:

    # e "The spacing property controls the space between the viewport and its scrollbars, in pixels."
    e "La propiedad spacing controla el espacio entre la ventana gráfica y sus barras de desplazamiento, en píxeles."

# game/tutorial_screen_displayables.rpy:864
translate spanish viewport_displayables_54dd6e7b:

    # e "The xinitial and yinitial properties set the initial amount of scrolling, as a fraction of the amount that can be scrolled."
    e "Las propiedades xinitial y yinitial establecen la cantidad inicial de desplazamiento, como una fracción de la cantidad que se puede desplazar."

# game/tutorial_screen_displayables.rpy:885
translate spanish viewport_displayables_c047efb5:

    # e "Finally, there's the child_size property. To explain what it does, I first have to show you what happens when we don't have it."
    e "Finalmente, está la propiedad child_size. Para explicar lo que hace, primero tengo que mostrarte lo que sucede cuando no lo tenemos."

# game/tutorial_screen_displayables.rpy:887
translate spanish viewport_displayables_c563019f:

    # e "As you can see, the text wraps. That's because Ren'Py is offering it space that isn't big enough."
    e "Como puedes ver, el texto se envuelve. Eso es porque Ren'Py le está ofreciendo un espacio que no es lo suficientemente grande."

# game/tutorial_screen_displayables.rpy:909
translate spanish viewport_displayables_4bcf0ad0:

    # e "When we give the screen a child_size, it offers more space to its children, allowing scrolling. It takes a horizontal and vertical size. If one component is None, it takes the size of the viewport."
    e "Cuando le damos a la pantalla un child_size, ofrece más espacio para sus hijos, lo que permite el desplazamiento. Toma un tamaño horizontal y vertical. Si un componente es None, toma el tamaño del viewport."

# game/tutorial_screen_displayables.rpy:936
translate spanish viewport_displayables_ae4ff821:

    # e "Finally, there's the vpgrid displayable. It combines a viewport and a grid into a single displayable, except it's more efficient than either, since it doesn't have to draw every child."
    e "Finalmente, está el visualizable vpgrid. Combina un viewport y una malla en una única pantalla, excepto que es más eficiente que cualquiera de los dos, ya que no tiene que dibujar a todos los hijos."

# game/tutorial_screen_displayables.rpy:938
translate spanish viewport_displayables_71fa0b8f:

    # e "It takes the cols and rows properties, which give the number of rows and columns of children. If one is omitted, Ren'Py figures it out from the other and the number of children."
    e "Toma las propiedades cols y rows, que dan el número de filas y columnas de hijos. Si se omite uno, Ren'Py lo calcula a partir del otro y el número de hijos."

translate spanish strings:

    # tutorial_screen_displayables.rpy:9
    old "Common properties all displayables share."
    new "Todas las propiedades comunes que comparten los visualizables."

    # tutorial_screen_displayables.rpy:9
    old "Adding images and other displayables."
    new "Añadir imágenes y otros visualizables."

    # tutorial_screen_displayables.rpy:9
    old "Text."
    new "Text."

    # tutorial_screen_displayables.rpy:9
    old "Boxes and other layouts."
    new "Boxes y otros layouts."

    # tutorial_screen_displayables.rpy:9
    old "Windows and frames."
    new "Windows y frames."

    # tutorial_screen_displayables.rpy:9
    old "Buttons."
    new "Buttons."

    # tutorial_screen_displayables.rpy:9
    old "Bars."
    new "Bars."

    # tutorial_screen_displayables.rpy:9
    old "Viewports."
    new "Viewports."

    # tutorial_screen_displayables.rpy:9
    old "Imagemaps."
    new "Imagemaps."

    # tutorial_screen_displayables.rpy:9
    old "That's all for now."
    new "Eso es todo por ahora."

    # tutorial_screen_displayables.rpy:55
    old "This uses position properties."
    new "Esto utiliza propiedades de posición."

    # tutorial_screen_displayables.rpy:63
    old "And the world turned upside down..."
    new "Y el mundo se puso al revés..."

    # tutorial_screen_displayables.rpy:115
    old "Flight pressure in tanks."
    new "Presión de vuelo en tanques."

    # tutorial_screen_displayables.rpy:116
    old "On internal power."
    new "Energía interna encendida"

    # tutorial_screen_displayables.rpy:117
    old "Launch enabled."
    new "Lanzamiento habilitado."

    # tutorial_screen_displayables.rpy:118
    old "Liftoff!"
    new "¡Despegar!"

    # tutorial_screen_displayables.rpy:232
    old "The answer is [answer]."
    new "La respuesta es [answer]."

    # tutorial_screen_displayables.rpy:244
    old "Text tags {color=#c8ffc8}work{/color} in screens."
    new "Las etiquetas de texto {color=#c8ffc8}funcionan{/color} en las pantallas."

    # tutorial_screen_displayables.rpy:336
    old "Bigger"
    new "Más grande"

    # tutorial_screen_displayables.rpy:401
    old "This is a screen."
    new "Esta es una pantalla."

    # tutorial_screen_displayables.rpy:402
    old "Okay"
    new "Aceptar"

    # tutorial_screen_displayables.rpy:440
    old "You clicked the button."
    new "Hiciste clic en el botón."

    # tutorial_screen_displayables.rpy:441
    old "Click me."
    new "Haz click en mí"

    # tutorial_screen_displayables.rpy:453
    old "You hovered the button."
    new "En focaste el botón"

    # tutorial_screen_displayables.rpy:454
    old "You unhovered the button."
    new "Desenfocaste el botón"

    # tutorial_screen_displayables.rpy:470
    old "Heal"
    new "Curar"

    # tutorial_screen_displayables.rpy:479
    old "This is a textbutton."
    new "Este es un textbutton."

    # tutorial_screen_displayables.rpy:539
    old "Or me."
    new "O en mí."

    # tutorial_screen_displayables.rpy:541
    old "You clicked the other button."
    new "Hiciste clic en el otro botón."

    # tutorial_screen_displayables.rpy:880
    old "This text is wider than the viewport."
    new "Este texto es más ancho que el viewport."

