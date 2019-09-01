
# game/tutorial_atl.rpy:205
translate spanish tutorial_positions_a09a3fd1:

    # e "In this tutorial, I'll teach you how Ren'Py positions things on the screen. But before that, let's learn a little bit about how Python handles numbers."
    e "En este tutorial, te enseñaré cómo Ren'Py coloca las cosas en la pantalla. Pero antes de eso, aprendamos un poco sobre cómo Python maneja los números."

# game/tutorial_atl.rpy:207
translate spanish tutorial_positions_ba39aabc:

    # e "There are two main kinds of numbers in Python: integers and floating point numbers. An integer consists entirely of digits, while a floating point number has a decimal point."
    e "Hay dos tipos principales de números en Python: enteros y números de punto flotante. Un entero consta de dígitos, mientras que un número de punto flotante tiene un punto decimal."

# game/tutorial_atl.rpy:209
translate spanish tutorial_positions_a60b775d:

    # e "For example, 100 is an integer, while 0.5 is a floating point number, or float for short. In this system, there are two zeros: 0 is an integer, and 0.0 is a float."
    e "Por ejemplo, 100 es un número entero, mientras que 0.5 es un número de punto flotante, o flotante para abreviar. En este sistema, hay dos ceros: 0 es un número entero y 0.0 es un flotante."

# game/tutorial_atl.rpy:211
translate spanish tutorial_positions_7f1a560c:

    # e "Ren'Py uses integers to represent absolute coordinates, and floats to represent fractions of an area with known size."
    e "Ren'Py usa números enteros para representar coordenadas absolutas y flotantes para representar fracciones de un área con un tamaño conocido."

# game/tutorial_atl.rpy:213
translate spanish tutorial_positions_8e7d3e52:

    # e "When we're positioning something, the area is usually the entire screen."
    e "Cuando estamos posicionando algo, el área es usualmente la pantalla completa."

# game/tutorial_atl.rpy:215
translate spanish tutorial_positions_fdcf9d8b:

    # e "Let me get out of the way, and I'll show you where some positions are."
    e "Déjame salir del camino y te mostraré dónde están algunas posiciones."

# game/tutorial_atl.rpy:229
translate spanish tutorial_positions_76d7a5bf:

    # e "The origin is the upper-left corner of the screen. That's where the x position (xpos) and the y position (ypos) are both zero."
    e "El origen es la esquina superior izquierda de la pantalla. Ahí es donde la posición x (xpos) y la posición y (ypos) son ambas cero."

# game/tutorial_atl.rpy:235
translate spanish tutorial_positions_be14c7c3:

    # e "When we increase xpos, we move to the right. So here's an xpos of .5, meaning half the width across the screen."
    e "Cuando aumentamos xpos, nos movemos a la derecha. Así que aquí hay un xpos de .5, que significa la mitad del ancho en la pantalla."

# game/tutorial_atl.rpy:240
translate spanish tutorial_positions_9b91be6c:

    # e "Increasing xpos to 1.0 moves us to the right-hand border of the screen."
    e "Al aumentar xpos a 1.0, nos movemos al borde derecho de la pantalla."

# game/tutorial_atl.rpy:246
translate spanish tutorial_positions_2b293304:

    # e "We can also use an absolute xpos, which is given in an absolute number of pixels from the left side of the screen. For example, since this window is 1280 pixels across, using an xpos of 640 will return the target to the center of the top row."
    e "También podemos usar un xpos absoluto, que se da en un número absoluto de píxeles desde el lado izquierdo de la pantalla. Por ejemplo, dado que esta ventana tiene 1280 píxeles de ancho, usar un xpos de 640 devolverá el objetivo al centro de la fila superior."

# game/tutorial_atl.rpy:248
translate spanish tutorial_positions_c4d18c0a:

    # e "The y-axis position, or ypos works the same way. Right now, we have a ypos of 0.0."
    e "La posición del eje y, o ypos, funciona de la misma manera. En este momento, tenemos un ypos de 0.0."

# game/tutorial_atl.rpy:254
translate spanish tutorial_positions_16933a61:

    # e "Here's a ypos of 0.5."
    e "Aquí hay un ypos de 0.5."

# game/tutorial_atl.rpy:259
translate spanish tutorial_positions_6eb36777:

    # e "A ypos of 1.0 specifies a position at the bottom of the screen. If you look carefully, you can see the position indicator spinning below the text window."
    e "Un ypos de 1.0 especifica una posición en la parte inferior de la pantalla. Si observa detenidamente, puede ver el indicador de posición girando debajo de la ventana de texto."

# game/tutorial_atl.rpy:261
translate spanish tutorial_positions_a423050f:

    # e "Like xpos, ypos can also be an integer. In this case, ypos would give the total number of pixels from the top of the screen."
    e "Como xpos, ypos también puede ser un número entero. En este caso, ypos daría el número total de píxeles desde la parte superior de la pantalla."

# game/tutorial_atl.rpy:267
translate spanish tutorial_positions_bc7a809a:

    # e "Can you guess where this position is, relative to the screen?" nointeract
    e "¿Puedes adivinar dónde está esta posición, relativa a la pantalla?" nointeract

# game/tutorial_atl.rpy:273
translate spanish tutorial_positions_6f926e18:

    # e "Sorry, that's wrong. The xpos is .75, and the ypos is .25."
    e "Lo siento, eso está mal. El xpos es .75, y el ypos es .25."

# game/tutorial_atl.rpy:275
translate spanish tutorial_positions_5d5feb98:

    # e "In other words, it's 75%% of the way from the left side, and 25%% of the way from the top."
    e "En otras palabras, es 75%% del lado izquierdo, y 25%% del camino desde la parte superior."

# game/tutorial_atl.rpy:279
translate spanish tutorial_positions_77b45218:

    # e "Good job! You got that position right."
    e "¡Buen trabajo! Tienes la posición correcta."

# game/tutorial_atl.rpy:283
translate spanish tutorial_positions_6f926e18_1:

    # e "Sorry, that's wrong. The xpos is .75, and the ypos is .25."
    e "Lo siento, está mal. El xpos es .75, y el ypos es .25."

# game/tutorial_atl.rpy:285
translate spanish tutorial_positions_5d5feb98_1:

    # e "In other words, it's 75%% of the way from the left side, and 25%% of the way from the top."
    e "En otras palabras, es 75%% del lado izquierdo, y 25%% del camino desde la parte superior."

# game/tutorial_atl.rpy:299
translate spanish tutorial_positions_e4380a83:

    # e "The second position we care about is the anchor. The anchor is a spot on the thing being positioned."
    e "La segunda posición que nos importa es el anchor. El anchor es un punto en la imagen que se coloca."

# game/tutorial_atl.rpy:301
translate spanish tutorial_positions_d1db1246:

    # e "For example, here we have an xanchor of 0.0 and a yanchor of 0.0. It's in the upper-left corner of the logo image."
    e "Por ejemplo, aquí tenemos un xanchor de 0.0 y un yanchor de 0.0. Está en la esquina superior izquierda de la imagen del logotipo."

# game/tutorial_atl.rpy:306
translate spanish tutorial_positions_6056873f:

    # e "When we increase the xanchor to 1.0, the anchor moves to the right corner of the image."
    e "Cuando aumentamos el xanchor a 1.0, el anchor se mueve a la esquina derecha de la imagen."

# game/tutorial_atl.rpy:311
translate spanish tutorial_positions_7cdb8dcc:

    # e "Similarly, when both xanchor and yanchor are 1.0, the anchor is the bottom-right corner."
    e "De manera similar, cuando tanto xanchor como yanchor son 1.0, el anchor es la esquina inferior derecha."

# game/tutorial_atl.rpy:318
translate spanish tutorial_positions_03a07da8:

    # e "To place an image on the screen, we need both the position and the anchor."
    e "Para colocar una imagen en la pantalla, necesitamos tanto la posición como el anchor."

# game/tutorial_atl.rpy:326
translate spanish tutorial_positions_8945054f:

    # e "We then line them up, so that both the position and anchor are at the same point on the screen."
    e "Luego los alineamos, de modo que tanto la posición como el anchor estén en el mismo punto de la pantalla."

# game/tutorial_atl.rpy:336
translate spanish tutorial_positions_2b184a93:

    # e "When we place both in the upper-left corner, the image moves to the upper-left corner of the screen."
    e "Cuando colocamos ambos en la esquina superior izquierda, la imagen se mueve a la esquina superior izquierda de la pantalla."

# game/tutorial_atl.rpy:345
translate spanish tutorial_positions_5aac4f3f:

    # e "With the right combination of position and anchor, any place on the screen can be specified, without even knowing the size of the image."
    e "Con la combinación correcta de posición y anchor, se puede especificar cualquier lugar en la pantalla, sin siquiera saber el tamaño de la imagen."

# game/tutorial_atl.rpy:357
translate spanish tutorial_positions_3b59b797:

    # e "It's often useful to set xpos and xanchor to the same value. We call that xalign, and it gives a fractional position on the screen."
    e "A menudo es útil establecer xpos y xanchor en el mismo valor. Llamamos a eso xalign, y le da una posición fraccionaria en la pantalla."

# game/tutorial_atl.rpy:362
translate spanish tutorial_positions_b8ebf9fe:

    # e "For example, when we set xalign to 0.0, things are aligned to the left side of the screen."
    e "Por ejemplo, cuando configuramos xalign en 0.0, las cosas se alinean al lado izquierdo de la pantalla."

# game/tutorial_atl.rpy:367
translate spanish tutorial_positions_8ce35d52:

    # e "When we set it to 1.0, then we're aligned to the right side of the screen."
    e "Cuando lo configuramos a 1.0, entonces estamos alineados al lado derecho de la pantalla."

# game/tutorial_atl.rpy:372
translate spanish tutorial_positions_6745825f:

    # e "And when we set it to 0.5, we're back to the center of the screen."
    e "Y cuando lo configuramos a 0.5, volvemos al centro de la pantalla."

# game/tutorial_atl.rpy:374
translate spanish tutorial_positions_64428a07:

    # e "Setting yalign is similar, except along the y-axis."
    e "La configuración de yalign es similar, excepto que es a lo largo del eje y."

# game/tutorial_atl.rpy:376
translate spanish tutorial_positions_cfb77d42:

    # e "Remember that xalign is just setting xpos and xanchor to the same value, and yalign is just setting ypos and yanchor to the same value."
    e "Recuerde que xalign solo establece xpos y xanchor en el mismo valor, y yalign solo establece ypos y yanchor en el mismo valor."

# game/tutorial_atl.rpy:381
translate spanish tutorial_positions_cfc1723e:

    # e "The xcenter and ycenter properties position the center of the image. Here, with xcenter set to .75, the center of the image is three-quarters of the way to the right side of the screen."
    e "Las propiedades xcenter y ycenter colocan el centro de la imagen. Aquí, con xcenter establecido en .75, el centro de la imagen está a tres cuartos del lado derecho de la pantalla."

# game/tutorial_atl.rpy:386
translate spanish tutorial_positions_7728dbf9:

    # e "The difference between xalign and xcenter is more obvious when xcenter is 1.0, and the image is halfway off the right side of the screen."
    e "La diferencia entre xalign y xcenter es más obvia cuando xcenter es 1.0, y la imagen está a mitad de camino del lado derecho de la pantalla."

# game/tutorial_atl.rpy:394
translate spanish tutorial_positions_1b1cedc6:

    # e "There are the xoffset and yoffset properties, which are applied after everything else, and offset things to the right or bottom, respectively."
    e "Existen las propiedades xoffset y yoffset, que se aplican después de todo lo demás, y compensan las cosas a la derecha o abajo, respectivamente."

# game/tutorial_atl.rpy:399
translate spanish tutorial_positions_e6da2798:

    # e "Of course, you can use negative numbers to offset things to the left and top."
    e "Por supuesto, puedes usar números negativos para compensar cosas a la izquierda y arriba."

# game/tutorial_atl.rpy:404
translate spanish tutorial_positions_e0fe2d81:

    # e "Lastly, I'll mention that there are combined properties like align, pos, anchor, and center. Align takes a pair of numbers, and sets xalign to the first and yalign to the second. The others are similar."
    e "Por último, mencionaré que hay propiedades combinadas como align, pos, anchor y center. Align toma un par de números y establece xalign para el primero y yalign para el segundo. Los otros son similares."

# game/tutorial_atl.rpy:411
translate spanish tutorial_positions_0f4ca2b6:

    # e "Once you understand positions, you can use transformations to move things around the Ren'Py screen."
    e "Una vez que entiendas las posiciones, puedes usar transformaciones para mover cosas por toda la pantalla de Ren'Py."

# game/tutorial_atl.rpy:418
translate spanish tutorial_atl_d5d6b62a:

    # e "Ren'Py uses transforms to animate, manipulate, and place images. We've already seen the very simplest of transforms in use:"
    e "Una vez que entiendas las posiciones, puedes usar transformaciones para mover cosas toda la pantalla de Ren'Py."

# game/tutorial_atl.rpy:425
translate spanish tutorial_atl_7e853c9d:

    # e "Transforms can be very simple affairs that place the image somewhere on the screen, like the right transform."
    e "Las transformaciones pueden ser asuntos muy simples que colocan la imagen en algún lugar de la pantalla, como la transformación right."

# game/tutorial_atl.rpy:429
translate spanish tutorial_atl_87a6ecbd:

    # e "But transforms can also be far more complicated affairs, that introduce animation and effects into the mix. To demonstrate, let's have a Gratuitous Rock Concert!"
    e "Pero las transformaciones también pueden ser asuntos mucho más complicados, que introducen animación y efectos a la mezcla. Para demostrarlo, ¡tengamos un Concierto de Rock Gratuito!"

# game/tutorial_atl.rpy:437
translate spanish tutorial_atl_65badef3:

    # e "But first, let's have... a Gratuitous Rock Concert!"
    e "Pero primero, tengamos ... ¡un Concierto de Rock Gratuito!"

# game/tutorial_atl.rpy:445
translate spanish tutorial_atl_e0d3c5ec:

    # e "That was a lot of work, but it was built out of small parts."
    e "Eso fue mucho trabajo, pero fue construido con pequeñas partes."

# game/tutorial_atl.rpy:447
translate spanish tutorial_atl_f2407514:

    # e "Most transforms in Ren'Py are built using the Animation and Transform Language, or ATL for short."
    e "La mayoría de las transformaciones en Ren'Py se crean utilizando el lenguaje de animación y transformación, o ATL, para abreviar."

# game/tutorial_atl.rpy:449
translate spanish tutorial_atl_1f22f875:

    # e "There are currently three places where ATL can be used in Ren'Py."
    e "Actualmente hay tres lugares donde se puede usar ATL en Ren'Py."

# game/tutorial_atl.rpy:454
translate spanish tutorial_atl_fd036bdf:

    # e "The first place ATL can be used is as part of an image statement. Instead of a displayable, an image may be defined as a block of ATL code."
    e "El primer lugar donde se puede usar ATL es como parte de una sentencia image. En lugar de mostrarse, una imagen puede definirse como un bloque de código ATL."

# game/tutorial_atl.rpy:456
translate spanish tutorial_atl_7cad2ab9:

    # e "When used in this way, we have to be sure that ATL includes one or more displayables to actually show."
    e "Cuando se usa de esta manera, tenemos que asegurarnos de que ATL incluya uno o más elementos visualizables para mostrar realmente."

# game/tutorial_atl.rpy:461
translate spanish tutorial_atl_c78b2a1e:

    # e "The second way is through the use of the transform statement. This assigns the ATL block to a python variable, allowing it to be used in at clauses and inside other transforms."
    e "La segunda forma es a través del uso de la sentencia transform. Esto asigna el bloque ATL a una variable de python, lo que permite que se use en cláusulas at y dentro de otras transformaciones."

# game/tutorial_atl.rpy:473
translate spanish tutorial_atl_da7a7759:

    # e "Finally, an ATL block can be used as part of a show statement, instead of the at clause."
    e "Finalmente, un bloque ATL se puede usar como parte de una sentencia show, en lugar de la cláusula at."

# game/tutorial_atl.rpy:480
translate spanish tutorial_atl_1dd345c6:

    # e "When ATL is used as part of a show statement, values of properties exist even when the transform is changed. So even though a click your click stopped the motion, the image remains in the same place."
    e "Cuando se usa ATL como parte de una sentencia show, los valores de las propiedades existen incluso cuando se cambia la transformación. Así que aunque des clic y se detenga el movimiento, la imagen permanece en el mismo lugar."

# game/tutorial_atl.rpy:488
translate spanish tutorial_atl_98047789:

    # e "The key to ATL is what we call composability. ATL is made up of relatively simple commands, which can be combined together to create complicated transforms."
    e "La clave para ATL es lo que llamamos composabilidad. ATL se compone de comandos relativamente simples, que se pueden combinar para crear transformaciones complicadas."

# game/tutorial_atl.rpy:490
translate spanish tutorial_atl_ed82983f:

    # e "Before I explain how ATL works, let me explain what animation and transformation are."
    e "Antes de explicar cómo funciona ATL, permítanme explicar qué son las animaciones y las transformaciones."

# game/tutorial_atl.rpy:495
translate spanish tutorial_atl_2807adff:

    # e "Animation is when the displayable being shown changes. For example, right now I am changing my expression."
    e "La animación es cuando el visualizable que se muestra cambia. Por ejemplo, ahora mismo estoy cambiando mi expresión."

# game/tutorial_atl.rpy:522
translate spanish tutorial_atl_3eec202b:

    # e "Transformation involves moving or distorting an image. This includes placing it on the screen, zooming it in and out, rotating it, and changing its opacity."
    e "Transformación implica mover o distorsionar una imagen. Esto incluye colocarlo en la pantalla, acercarlo y alejarlo, girarlo y cambiar su opacidad."

# game/tutorial_atl.rpy:530
translate spanish tutorial_atl_fbc9bf83:

    # e "To introduce ATL, let's start by looking at at a simple animation. Here's one that consists of five lines of ATL code, contained within an image statement."
    e "Para presentar ATL, comencemos observando una animación simple. Aquí hay una que consta de cinco líneas de código ATL, contenidas dentro de una sentencia image."

# game/tutorial_atl.rpy:532
translate spanish tutorial_atl_bf92d973:

    # e "To change a displayable, simply mention it on a line of ATL. Here, we're switching back and forth between two images."
    e "Para cambiar un visualizable, simplemente mencionelo en una línea de ATL. Aquí, estamos alternando entre dos imágenes."

# game/tutorial_atl.rpy:534
translate spanish tutorial_atl_51a41db4:

    # e "Since we're defining an image, the first line of ATL must give a displayable. Otherwise, there would be nothing to show."
    e "Ya que estamos definiendo una imagen, la primera línea de ATL debe dar un visualizable. De lo contrario, no habría nada que mostrar."

# game/tutorial_atl.rpy:536
translate spanish tutorial_atl_3d065074:

    # e "The second and fourth lines are pause statements, which cause ATL to wait half a second each before continuing. That's how we give the delay between images."
    e "Las líneas segunda y cuarta son sentencias pause, lo que hace que ATL espere medio segundo cada una antes de continuar. Así es como damos la demora entre las imágenes."

# game/tutorial_atl.rpy:538
translate spanish tutorial_atl_60f2a5e8:

    # e "The final line is a repeat statement. This causes the current block of ATL to be restarted. You can only have one repeat statement per block."
    e "La línea final es una sentencia repeat. Esto hace que el bloque actual de ATL se reinicie. Sólo puede tener una sentencia repeat por bloque."

# game/tutorial_atl.rpy:543
translate spanish tutorial_atl_146cf4c4:

    # e "If we were to write repeat 2 instead, the animation would loop twice, then stop."
    e "Si en su lugar escribieramos repeat 2, la animación se repetirá dos veces y luego se detendrá."

# game/tutorial_atl.rpy:548
translate spanish tutorial_atl_d90b1838:

    # e "Omitting the repeat statement means that the animation stops once we reach the end of the block of ATL code."
    e "Omitir la sentencia repeat significa que la animación se detiene una vez que llegamos al final del bloque del código ATL."

# game/tutorial_atl.rpy:554
translate spanish tutorial_atl_e5872360:

    # e "By default, displayables are replaced instantaneously. We can also use a with clause to give a transition between displayables."
    e "De forma predeterminada, los visualizables se reemplazan instantáneamente. También podemos usar una cláusula with para dar una transición entre visualizables."

# game/tutorial_atl.rpy:561
translate spanish tutorial_atl_2e9d63ea:

    # e "With animation done, we'll see how we can use ATL to transform images, starting with positioning an image on the screen."
    e "Teminamos con la animación, veremos cómo podemos usar ATL para transformar imágenes, comenzando con el posicionamiento de una imagen en la pantalla."

# game/tutorial_atl.rpy:570
translate spanish tutorial_atl_ddc55039:

    # e "The simplest thing we can to is to statically position an image. This is done by giving the names of the position properties, followed by the property values."
    e "Lo más simple que podemos hacer es posicionar estáticamente una imagen. Esto se hace dando los nombres de las propiedades de posición, seguidos de los valores de propiedad."

# game/tutorial_atl.rpy:575
translate spanish tutorial_atl_43516492:

    # e "With a few more statements, we can move things around on the screen."
    e "Con unas cuantas sentencia más, podemos mover las cosas en la pantalla."

# game/tutorial_atl.rpy:577
translate spanish tutorial_atl_fb979287:

    # e "This example starts the image off at the top-right of the screen, and waits a second. It then moves it to the left side, waits another second, and repeats."
    e "Este ejemplo inicia la imagen en la esquina superior derecha de la pantalla y espera un segundo. Luego lo mueve hacia el lado izquierdo, espera otro segundo y se repite."

# game/tutorial_atl.rpy:579
translate spanish tutorial_atl_7650ec09:

    # e "The pause and repeat statements are the same statements we used in our animations. They work throughout ATL code."
    e "Las sentencia pause y repeat son las mismas sentencias que usamos en nuestras animaciones. Funcionan a lo largo del código ATL."

# game/tutorial_atl.rpy:584
translate spanish tutorial_atl_d3416d4f:

    # e "Having the image jump around on the screen isn't all that useful. That's why ATL has the interpolation statement."
    e "Hacer que la imagen salte por la pantalla no es tan útil. Es por eso que ATL tiene la sentencia de interpolación."

# game/tutorial_atl.rpy:586
translate spanish tutorial_atl_4e7512ec:

    # e "The interpolation statement allows you to smoothly vary the value of a transform property, from an old to a new value."
    e "La sentencia de interpolación te permite variar suavemente el valor de una propiedad de transformación, de un valor antiguo a uno nuevo."

# game/tutorial_atl.rpy:588
translate spanish tutorial_atl_685eeeaa:

    # e "Here, we have an interpolation statement on the second ATL line. It starts off with the name of a time function, in this case linear."
    e "Aquí, tenemos una sentencia de interpolación en la segunda línea ATL. Comienza con el nombre de una función de tiempo, en este caso linear."

# game/tutorial_atl.rpy:590
translate spanish tutorial_atl_c5cb49de:

    # e "That's followed by an amount of time, in this case three seconds. It ends with a list of properties, each followed by its new value."
    e "A eso le sigue una cantidad de tiempo, en este caso tres segundos. Termina con una lista de propiedades, cada una seguida por su nuevo valor."

# game/tutorial_atl.rpy:592
translate spanish tutorial_atl_04b8bc1d:

    # e "The value of each property is interpolated from its value when the statement starts to the value at the end of the statement. This is done once per frame, allowing smooth animation."
    e "El valor de cada propiedad se interpola a partir de su valor cuando la sentencia comienza al valor al final de la sentencia. Esto se hace una vez por fotograma, permitiendo una animación suave."

# game/tutorial_atl.rpy:603
translate spanish tutorial_atl_2958f397:

    # e "ATL supports more complicated move types, like circle and spline motion. But I won't be showing those here."
    e "ATL admite tipos de movimiento más complicados, como el movimiento de círculo y spline. Pero no los mostraré aquí."

# game/tutorial_atl.rpy:607
translate spanish tutorial_atl_d08fe8d9:

    # e "Apart from displayables, pause, interpolation, and repeat, there are a few other statements we can use as part of ATL."
    e "Además de visualizables, pausas, interploaciones y repeticiones, hay algunas otras sentencias que podemos usar como parte de ATL."

# game/tutorial_atl.rpy:619
translate spanish tutorial_atl_84b22ac0:

    # e "ATL transforms created using the statement become ATL statements themselves. Since the default positions are also transforms, this means that we can use left, right, and center inside of an ATL block."
    e "Las transformaciones ATL creadas usando la sentencia se convierten en sentencias ATL. Dado que las posiciones predeterminadas también son transformaciones, esto significa que podemos usar left, derecha y centro dentro de un bloque ATL."

# game/tutorial_atl.rpy:635
translate spanish tutorial_atl_331126c1:

    # e "Here, we have two new statements. The block statement allows you to include a block of ATL code. Since the repeat statement applies to blocks, this lets you repeat only part of an ATL transform."
    e "Aquí tenemos dos nuevas sentencias. La sentencia block te permite incluir un bloque de código ATL. Como la sentencia repeat se aplica a los bloques, esto le permite repetir solo una parte de una transformación ATL."

# game/tutorial_atl.rpy:637
translate spanish tutorial_atl_24f67b67:

    # e "We also have the time statement, which runs after the given number of seconds have elapsed from the start of the block. It will run even if another statement is running, stopping the other statement."
    e "También tenemos la sentencia time, que se ejecuta después de que hayan transcurrido los segundos dados desde el inicio del bloque. Se ejecutará incluso si se está ejecutando otra sentencia, deteniendo la otra sentencia."

# game/tutorial_atl.rpy:639
translate spanish tutorial_atl_b7709507:

    # e "So this example bounces the image back and forth for eleven and a half seconds, and then moves it to the right side of the screen."
    e "Entonces, este ejemplo rebota la imagen de un lado a otro durante once segundos y medio, y luego la mueve hacia el lado derecho de la pantalla."

# game/tutorial_atl.rpy:653
translate spanish tutorial_atl_f903bc3b:

    # e "The parallel statement lets us run two blocks of ATL code at the same time."
    e "La sentencia parallel nos permite ejecutar dos bloques de código ATL al mismo tiempo."

# game/tutorial_atl.rpy:655
translate spanish tutorial_atl_5d0f8f9d:

    # e "Here, the top block move the image in the horizontal direction, and the bottom block moves it in the vertical direction. Since they're moving at different speeds, it looks like the image is bouncing on the screen."
    e "Aquí, el bloque superior mueve la imagen en la dirección horizontal, y el bloque inferior la mueve en la dirección vertical. Ya que se están moviendo a diferentes velocidades, parece que la imagen rebota en la pantalla."

# game/tutorial_atl.rpy:669
translate spanish tutorial_atl_28a7d27e:

    # e "Finally, the choice statement makes Ren'Py randomly pick a block of ATL code. This allows you to add some variation as to what Ren'Py shows."
    e "Finalmente, la sentencia choice hace que Ren'Py elija aleatoriamente un bloque de código ATL. Esto le permite agregar alguna variación a lo que muestra Ren'Py."

# game/tutorial_atl.rpy:675
translate spanish tutorial_atl_2265254b:

    # e "This tutorial game has only scratched the surface of what you can do with ATL. For example, we haven't even covered the on and event statements. For more information, you might want to check out {a=https://renpy.org/doc/html/atl.html}the ATL chapter in the reference manual{/a}."
    e "Este juego tutorial solo ha arañado la superficie de lo que puedes hacer con ATL. Por ejemplo, ni siquiera hemos cubierto las sentencias on y event. Para más información, es posible que desee revisar {a=https://renpy.org/doc/html/atl.html}el capítulo ATL en el manual de referencias{/a}."

# game/tutorial_atl.rpy:684
translate spanish transform_properties_391169cf:

    # e "Ren'Py has quite a few transform properties that can be used with ATL, the Transform displayable, and the add Screen Language statement."
    e "Ren'Py tiene unas cuantas propiedades de transformación que se pueden usar con ATL, el visualizable Transform y la sentencia add Screen Language."

# game/tutorial_atl.rpy:685
translate spanish transform_properties_fc895a1f:

    # e "Here, we'll show them off so you can see them in action and get used to what each does."
    e "Aquí, los mostraremos para que puedas verlos en acción y acostumbrarte a lo que hace cada uno."

# game/tutorial_atl.rpy:701
translate spanish transform_properties_88daf990:

    # e "First off, all of the position properties are also transform properties. These include the pos, anchor, align, center, and offset properties."
    e "En primer lugar, todas las propiedades de posición también son propiedades de transformación. Estos incluyen las propiedades pos, anchor, align, center y offset."

# game/tutorial_atl.rpy:719
translate spanish transform_properties_d7a487f1:

    # e "The position properties can also be used to pan over a displayable larger than the screen, by giving xpos and ypos negative values."
    e "Las propiedades de posición también se pueden usar para desplazarse por una pantalla más grande que la pantalla, dando valores negativos a xpos y ypos."

# game/tutorial_atl.rpy:729
translate spanish transform_properties_89e0d7c2:

    # "The subpixel property controls how things are lined up with the screen. When False, images can be pixel-perfect, but there can be pixel jumping."
    "La propiedad de subpíxele controla cómo se alinean las cosas con la pantalla. Cuando es False, las imágenes pueden ser perfectas en píxeles, pero puede haber saltos de píxeles."

# game/tutorial_atl.rpy:736
translate spanish transform_properties_4194527e:

    # "When it's set to True, movement is smoother at the cost of blurring images a little."
    "Cuando se establece en True, el movimiento es más suave a costa de desenfocar un poco las imágenes."

# game/tutorial_atl.rpy:755
translate spanish transform_properties_35934e77:

    # e "Transforms also support polar coordinates. The around property sets the center of the coordinate system to coordinates given in pixels."
    e "Las transformaciones también soportan coordenadas polares. La propiedad around establece el centro del sistema de coordenadas en coordenadas dadas en píxeles."

# game/tutorial_atl.rpy:763
translate spanish transform_properties_605ebd0c:

    # e "The angle property gives the angle in degrees. Angles run clockwise, with the zero angle at the top of the screen."
    e "La propiedad de angle da el ángulo en grados. Los ángulos se ejecutan en el sentido de las agujas del reloj, con el ángulo cero en la parte superior de la pantalla."

# game/tutorial_atl.rpy:772
translate spanish transform_properties_6d4555ed:

    # e "The radius property gives the distance in pixels from the anchor of the displayable to the center of the coordinate system."
    e "La propiedad de radius proporciona la distancia en píxeles desde el anchor del visualizable hasta el centro del sistema de coordenadas."

# game/tutorial_atl.rpy:786
translate spanish transform_properties_7af037a5:

    # e "There are several ways to resize a displayable. The zoom property lets us scale a displayable by a factor, making it bigger and smaller."
    e "Hay varias formas de cambiar el tamaño de un visuzlizable. La propiedad de zoom nos permite escalar un valor visualizable, haciéndolo más grande y más pequeño."

# game/tutorial_atl.rpy:799
translate spanish transform_properties_b6527546:

    # e "The xzoom and yzoom properties allow the displayable to be scaled in the X and Y directions independently."
    e "Las propiedades xzoom y yzoom permiten escalar lo visualizable en las direcciones X e Y de forma independiente."

# game/tutorial_atl.rpy:809
translate spanish transform_properties_b98b780b:

    # e "By making xzoom or yzoom a negative number, we can flip the image horizontally or vertically."
    e "Al hacer que xzoom o yzoom sean un número negativo, podemos voltear la imagen horizontal o verticalmente."

# game/tutorial_atl.rpy:819
translate spanish transform_properties_74d542ff:

    # e "Instead of zooming by a scale factor, the size transform property can be used to scale a displayable to a size in pixels."
    e "En lugar de hacer zoom en un factor de escala, la propiedad de transformación de tamaño se puede usar para escalar un tamaño que se pueda mostrar a un tamaño en píxeles."

# game/tutorial_atl.rpy:834
translate spanish transform_properties_438ed776:

    # e "The alpha property is used to change the opacity of a displayable. This can make it appear and disappear."
    e "La propiedad alpha se utiliza para cambiar la opacidad de un visualizable. Esto puede hacer que aparezca y desaparezca "

# game/tutorial_atl.rpy:847
translate spanish transform_properties_aee19f86:

    # e "The rotate property rotates a displayable."
    e "La propiedad rotate gira un visualizable."

# game/tutorial_atl.rpy:858
translate spanish transform_properties_57b3235a:

    # e "By default, when a displayable is rotated, Ren'Py will include extra space on all four sides, so the size doesn't change as it rotates. Here, you can see the extra space on the left and top, and it's also there on the right and bottom."
    e "Por defecto, cuando se gira un visualizable, Ren'Py incluirá espacio adicional en los cuatro lados, por lo que el tamaño no cambia a medida que gira. Aquí, puedes ver el espacio adicional a la izquierda y arriba, y también está a la derecha y abajo."

# game/tutorial_atl.rpy:870
translate spanish transform_properties_66d29ee8:

    # e "By setting rotate_pad to False, we can get rid of the space, at the cost of the size of the displayable changing as it rotates."
    e "Al establecer rotate_pad en False, podemos deshacernos del espacio, a costa del tamaño del cambio visualizable a medida que gira."

# game/tutorial_atl.rpy:881
translate spanish transform_properties_7f32e8ad:

    # e "The tile transform properties, xtile and ytile, repeat the displayable multiple times."
    e "Las propiedades de transformación tile, xtile y ytile, repiten multiples veces el visualizable."

# game/tutorial_atl.rpy:891
translate spanish transform_properties_207b7fc8:

    # e "The crop property crops a rectangle out of a displayable, showing only part of it."
    e "La propiedad crop recorta un rectángulo de un objeto visualizable, mostrando solo una parte de él."

# game/tutorial_atl.rpy:905
translate spanish transform_properties_e7e22d28:

    # e "When used together, crop and size can be used to focus in on specific parts of an image."
    e "Cuando se usan juntos, crop y size se pueden usar para enfocar en partes específicas de una imagen."

# game/tutorial_atl.rpy:917
translate spanish transform_properties_f34abd82:

    # e "The xpan and ypan properties can be used to pan over a displayable, given an angle in degrees, with 0 being the center."
    e "Las propiedades xpan e ypan se pueden usar para desplazarse sobre un visualizable, dado un ángulo en grados, siendo 0 el centro."

# game/tutorial_atl.rpy:924
translate spanish transform_properties_bfa3b139:

    # e "Those are all the transform properties we have to work with. By putting them together in the right order, you can create complex things."
    e "Esas son todas las propiedades de transformación con las que tenemos que trabajar. Al juntarlas en el orden correcto, puedes crear cosas complejas."

translate spanish strings:

    # tutorial_atl.rpy:267
    old "xpos 1.0 ypos .5"
    new "xpos 1.0 ypos .5"

    # tutorial_atl.rpy:267
    old "xpos .75 ypos .25"
    new "xpos .75 ypos .25"

    # tutorial_atl.rpy:267
    old "xpos .25 ypos .33"
    new "xpos .25 ypos .33"

