=======================================================
Motor L-Code Runtime (Basado en el Código Fuente de Ren'Py)
=======================================================
RESUMEN DE FUNCIONALIDAD:
Este documento es nuestra guía de construcción. Explica la estructura del
código fuente de Ren'Py (nuestros "cimientos") y, lo más importante, detalla
los pasos y las herramientas necesarias para compilarlo desde cero.
Seguiremos estas instrucciones para crear nuestra propia versión del motor.
Sitio web del proyecto original: https://www.renpy.org
Ramas (Branches)
========================
EXPLICACIÓN: El código fuente se organiza en "ramas" para separar las
correcciones urgentes del desarrollo de nuevas características.
NOTA PARA L-CODE: Nosotros trabajaremos sobre nuestra propia copia de la rama
'master', creando nuestras propias ramas para nuevas características como la
integración del sistema de guardado LUSS.
A continuación se describen las ramas más interesantes del proyecto Ren'Py original.

fix
La rama fix se utiliza para correcciones a la versión actual de Ren'Py que no
requieren cambios peligrosos. La rama fix es también la fuente de la
documentación en https://www.renpy.org/. Esta rama se fusiona automáticamente
con master de forma regular.

Las solicitudes de cambio (pull requests) que contengan correcciones o mejoras
de documentación deben hacerse a la rama `fix`. Cuando se hace una nueva versión,
la rama `master` se copia a la rama `fix`.

master
La rama master es donde se centra el desarrollo principal. Esta rama
se convertirá eventualmente en la próxima versión de Ren'Py.

Las solicitudes de cambio que contengan nuevas características, que requieran
cambios incompatibles o cambios importantes en las partes internas de Ren'Py
deben dirigirse a la rama `master`.

Primeros Pasos (Getting Started)
===============================
OBJETIVO PRINCIPAL PARA L-CODE: Esta sección es la más crucial para nosotros.
Detalla cómo compilar los módulos de C y Cython que forman el núcleo
de bajo nivel del motor.
Ren'Py depende de varios módulos de Python escritos en Cython y C. Para
cambios en Ren'Py que solo involucran módulos de Python, puedes usar los módulos
que se encuentran en la última compilación nocturna (nightly build). De lo contrario,
tendrás que compilar los módulos tú mismo.

Los scripts de desarrollo asumen una plataforma similar a POSIX. Los scripts deberían
funcionar en Linux o macOS, y pueden hacerse funcionar en Windows usando un
entorno como MSYS.

Compilación Nocturna (Nightly Build)
-----------------------------
NOTA: Este método es para desarrolladores del Ren'Py original que no quieren
compilar todo. Nosotros nos centraremos en el siguiente método: "Compilando los Módulos".
Las compilaciones nocturnas se pueden descargar desde:

https://nightly.renpy.org

Ten en cuenta que la última compilación nocturna está al final de la lista. Una vez que hayas
descomprimido la compilación nocturna, entra en este repositorio y ejecuta::

./after_checkout.sh <ruta-a-la-compilacion-nocturna>

Una vez que este script se complete, deberías poder ejecutar Ren'Py usando renpy.sh,
renpy.app, o renpy.exe, según corresponda a tu plataforma.

Si la compilación nocturna actual no funciona, por favor espera 24 horas para que
ocurra una nueva compilación. Si esa compilación todavía no funciona, contacta a Tom
(pytom at bishoujo.us, o @renpytom en Twitter/X) para averiguar qué pasa.

El enlace simbólico doc estará roto hasta que se construya la documentación,
como se describe más abajo.

Compilando los Módulos (NUESTRO MÉTODO PRINCIPAL)
----------------------------------------------------
¡ATENCIÓN! Este es el proceso que seguiremos para construir nuestro motor.
Construir los módulos requiere que tengas muchas dependencias instaladas en
tu sistema. En Ubuntu y Debian, estas dependencias se pueden instalar con
el comando::

# EXPLICACIÓN: Este comando instala todas las librerías de las que depende
# el motor para funcionar: manejo de imágenes, códecs de video, renderizado de
# texto, audio, interacción con el sistema operativo (SDL2), etc.
# Son los "ladrillos" de terceros que usa Ren'Py para construir su funcionalidad.
sudo apt install python3-dev libassimp-dev libavcodec-dev libavformat-dev \
    libswresample-dev libswscale-dev libharfbuzz-dev libfreetype6-dev libfribidi-dev libsdl2-dev \
    libsdl2-image-dev libsdl2-gfx-dev libsdl2-mixer-dev libsdl2-ttf-dev libjpeg-dev pkg-config

Ren'Py requiere SDL_image 2.6 o superior. Si tu distribución no incluye
esa versión, necesitarás descargarla desde:

https://github.com/libsdl-org/SDL_image/tree/SDL2

Sugerimos encarecidamente usar un gestor de paquetes para crear un entorno virtual y
gestionar las dependencias. Hemos probado con uv <https://docs.astral.sh/uv/>_ pero
otros gestores de paquetes deberían funcionar también. Para crear un entorno virtual e
instalar las dependencias, abre una nueva terminal y ejecuta::

# EXPLICACIÓN: Este comando utiliza la herramienta 'uv' para crear un entorno
# aislado de Python e instalar todas las dependencias de Python (como Cython y Sphinx)
# que se necesitan para el proceso de compilación.
uv sync

Después de eso, compila los módulos de extensión y ejecuta Ren'Py usando el comando::

# EXPLICACIÓN: Este es el comando final. Ejecuta el script 'run.sh' que
# orquesta todo el proceso: compila todo el código de Cython y C, y si tiene
# éxito, lanza la versión recién compilada del motor.
./run.sh

Otras Plataformas
-----------------
Donde sea compatible, Ren'Py intentará encontrar los directorios de inclusión y las rutas
de las librerías usando pkg-config. Si pkg-config no está presente, las rutas de inclusión
y de las librerías se pueden especificar usando CFLAGS y LDFLAGS.

Si RENPY_CFLAGS está presente en el entorno y CFLAGS no lo está, setup.py
establecerá CFLAGS en RENPY_CFLAGS. Lo mismo es cierto para RENPY_LDFLAGS,
RENPY_CC, RENPY_CXX y RENPY_LD.

Setup.py no admite la compilación cruzada (cross-compiling). Consulta
https://github.com/renpy/renpy-build para el software que realiza la
compilación cruzada de Ren'Py para muchas plataformas. El sistema renpy-build
también incluye algunos componentes de tiempo de ejecución para Android, iOS y la web.

Documentación
=================
NOTA: Esta sección explica cómo se construye la documentación oficial de Ren'Py.
Es útil si en el futuro queremos añadir documentación para las nuevas
funciones que incorporemos a nuestro Motor L-Code.
Construcción
---------
Construir la documentación requiere que Ren'Py funcione. Necesitarás
enlazar una compilación nocturna o compilar los módulos como se describió
anteriormente. También necesitarás el generador de documentación
Sphinx <https://www.sphinx-doc.org>. Si tienes pip funcionando, instala
Sphinx usando::

pip install -U sphinx sphinx_rtd_theme sphinx_rtd_dark_mode

Una vez que Sphinx esté instalado, entra en el directorio sphinx dentro del
código de Ren'Py y ejecuta::

./build.sh

Formato
-----
La documentación de Ren'Py consiste en archivos reStructuredText que se encuentran
en sphinx/source, y documentación generada que se encuentra en los docstrings de
las funciones esparcidos por todo el código. No edites los archivos en
sphinx/source/inc directamente, ya que serán sobrescritos.

Los docstrings pueden incluir etiquetas en las primeras líneas:

:doc: seccion tipo
Indica que esta función debe ser documentada. seccion da
el nombre del archivo de inclusión donde se documentará la función, mientras que
tipo indica el tipo de objeto a documentar (uno de function,
method o class). Si se omite, tipo se autodetectará.
:name: nombre
El nombre de la función a documentar. Los nombres de las funciones suelen
detectarse, por lo que solo es necesario cuando una función tiene múltiples alias.
:args: argumentos
Esto anula la lista de argumentos detectada. Se puede usar si algunos argumentos
de la función están obsoletos.

Por ejemplo::

def warp_speed(factor, transwarp=False):
    """
    :doc: warp
    :name: renpy.warp_speed
    :args: (factor)

    Exceeds the speed of light.

    `factor`
        The warp factor. See Sternbach (1991) for details.

    `transwarp`
        If True, use transwarp. This does not work on all platforms.
    """

    renpy.engine.warp_drive.engage(factor)

Traducción del Motor
======================
NOTA: Esto se refiere a traducir la interfaz del lanzador de Ren'Py y
el juego de plantilla, no los juegos creados por los usuarios.
Para las mejores prácticas a la hora de traducir el lanzador y el juego
de plantilla, por favor lee:

https://lemmasoft.renai.us/forums/viewtopic.php?p=321603#p321603

Contribuciones al Motor L-Code
==================================
NOTA PARA L-CODE: El texto original se refería a cómo contribuir al
proyecto Ren'Py. Lo hemos adaptado para nuestro proceso interno.
Para correcciones de errores, mejoras de documentación y cambios simples,
simplemente se realizarán los cambios en nuestra rama de desarrollo. Para
cambios más complejos, primero discutiremos el diseño y la arquitectura
antes de la implementación.

Licencia
========
¡IMPORTANTE! Nuestro Motor L-Code Runtime, al ser un trabajo derivado de
Ren'Py, está sujeto a los mismos términos de licenciamiento del proyecto
original (principalmente la licencia LGPL). Es fundamental entender y
respetar esta licencia en todo momento.
Para los términos completos de licenciamiento, por favor lee:

https://www.renpy.org/doc/html/license.html
