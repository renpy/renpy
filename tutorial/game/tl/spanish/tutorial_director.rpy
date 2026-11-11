
# game/tutorial_director.rpy:5
translate spanish director_e4543d9b:

    # e "There are a few tools you can access by pressing the right commands on the keyboard."
    e "Hay algunas herramientas a las que puedes acceder presionando las combinaciones de teclas correctas."

# game/tutorial_director.rpy:7
translate spanish director_ebf40500:

    # e "Typing Shift+R turns on autoreload mode. When it's enabled, your game will automatically reload when you edit a script file."
    e "Escribir Shift+R activa el modo de recarga automática. Cuando está habilitado, tu juego se recargará automáticamente cuando edites un archivo de {i}script{/i}."

# game/tutorial_director.rpy:9
translate spanish director_6f3d1bea:

    # e "Shift+O brings you to the console, which lets you enter Ren'Py and Python commands to try them out."
    e "Shift+O te lleva a la consola, que te permite ingresar comandos de Ren'Py y de Python para probarlos."

# game/tutorial_director.rpy:11
translate spanish director_70a61c1c:

    # e "Shift+D pops up a developer menu with access to these and other functions."
    e "Shift+D muestra un menú de desarrollador con acceso a estas y otras funciones."

# game/tutorial_director.rpy:13
translate spanish director_43504744:

    # e "The most powerful tool is the interactive director that lets you add images, music, and voice lines to your game from inside Ren'Py."
    e "La herramienta más poderosa es el director interactivo, que te permite agregar imágenes, música y líneas de voz a tu juego desde dentro de Ren'Py."

# game/tutorial_director.rpy:15
translate spanish director_32f8695e:

    # e "The idea is that you can use an editor to write the script and logic of your visual novel, and then interactively add images in the right places."
    e "La idea es que puedas usar un editor para escribir el {i}script{/i} y la lógica de tu novela visual, y luego agregar imágenes de forma interactiva en los lugares correctos."

# game/tutorial_director.rpy:21
translate spanish director_62734181:

    # e "It looks like Ren'Py is installed read-only on your system, so you won't be able to try out the interactive director now."
    e "Parece que Ren'Py está instalado en modo de solo lectura en tu sistema, por lo que no podrás probar el director interactivo ahora."

# game/tutorial_director.rpy:23
translate spanish director_aec4c7d4:

    # e "You'll need to make your own project, and try it out there. But I can tell you how to use it."
    e "Tendrás que crear tu propio proyecto y probarlo allí. Pero puedo explicarte cómo usarlo."

# game/tutorial_director.rpy:29
translate spanish director_453d4d67:

    # e "You can try the interactive director out right now, by using it to change this tutorial game."
    e "Puedes probar el director interactivo ahora mismo, usándolo para modificar este juego tutorial."

# game/tutorial_director.rpy:31
translate spanish director_c35284d1:

    # e "Be sure to click my dialogue at the bottom of the screen to advance the tutorial."
    e "Asegúrate de hacer clic en mi diálogo en la parte inferior de la pantalla para avanzar en el tutorial."

# game/tutorial_director.rpy:33
translate spanish director_e253e03b:

    # e "If something goes wrong, don't worry. Quitting and restarting this tutorial will remove your changes and bring everything back to normal."
    e "Si algo sale mal, no te preocupes. Salir y reiniciar este tutorial eliminará tus cambios y hará que todo vuelva a la normalidad."

# game/tutorial_director.rpy:42
translate spanish director_1cd735bc:

    # e "To get started, let's go back to a blank slate, with no images on the screen."
    e "Para comenzar, volvamos a un estado inicial, sin imágenes en la pantalla."

# game/tutorial_director.rpy:44
translate spanish director_c7a18979:

    # e "You can show the director at any time by pressing the 'D' key on your keyboard. Ren'Py will reload, and you'll come back here. Try it now."
    e "Puedes mostrar el director en cualquier momento presionando la tecla 'D' de tu teclado. Ren'Py se recargará y volverás aquí. Pruébalo ahora."

# game/tutorial_director.rpy:46
translate spanish director_3dcc4362:

    # e "Let's add a background. Click the '+' to pick where to add it, then the 'scene' statement and 'washington' for the image. Finally, click 'Add' to add it."
    scene bg panorama

    e "Vamos a añadir un fondo. Haz clic en '+' para elegir dónde agregarlo, luego en la sentencia 'scene' y en 'washington' para la imagen. Finalmente, haz clic en 'Añadir' para agregarlo."

# game/tutorial_director.rpy:48
translate spanish director_292d58b5:

    # e "Next, add a sprite. Click '+', then 'show', 'eileen', 'happy', and 'Add'. Once you've added it, dissolve it in by clicking the second '+', then 'with', 'dissolve', and 'Add'."
    show eileen happy
    e "A continuación, agrega un {i}sprite{/i}. Haz clic en '+', luego en 'show', 'eileen', 'happy' y 'Añadir'. Una vez que lo hayas agregado, disuélvelo haciendo clic en el segundo '+', luego en 'with', 'dissolve' y 'Añadir'."

# game/tutorial_director.rpy:52
translate spanish director_c875c1a7:

    # e "You can edit or remove statements with the pencil icon. You can move me to the right by editing the show statement, then clicking '(transform)', 'right', and 'Change'."
    e "Puedes editar o eliminar sentencias con el icono de lápiz. Puedes moverme a la derecha editando la sentencia 'show', luego haciendo clic en '(transform)', 'right' y 'Cambiar'."

# game/tutorial_director.rpy:54
translate spanish director_4e04a74e:

    # e "Finally, you can use the play, queue, stop, and voice statements to manage audio. Try adding 'play', 'music', 'sunflower-slow-drag.ogg'."
    play music 'sunflower-slow-drag.ogg'
    e "Finalmente, puedes usar las sentencias 'play', 'queue', 'stop' y 'voice' para administrar el audio. Intenta agregar 'play', 'music', 'sunflower-slow-drag.ogg'."

# game/tutorial_director.rpy:61
translate spanish director_1364b336:

    # l "Finally, I get some more screen time!"
    l "¡Finalmente, tengo un poco más de tiempo en pantalla!"

# game/tutorial_director.rpy:69
translate spanish director_c6dd0c81:

    # e "The changes you make with the director are permanent. They're saved to the script, and you can rollback or repeat this section to see them."
    e "Los cambios que hagas con el director son permanentes. Se guardan en el {i}script{/i}, y puedes retroceder o repetir esta sección para verlos."

# game/tutorial_director.rpy:71
translate spanish director_9d03b14b:

    # e "However, we reset this tutorial when the game restarts, so you can try again from a clean slate. That won't happen with your own visual novel."
    e "Sin embargo, restablecemos este tutorial cuando se reinicia el juego, para que puedas volver a intentarlo desde cero. Eso no sucederá con tu propia novela visual."

# game/tutorial_director.rpy:73
translate spanish director_dbfa07b2:

    # e "I hope these tools make developing your visual novel that much easier."
    e "Espero que estas herramientas hagan que desarrollar tu novela visual sea mucho más fácil."

