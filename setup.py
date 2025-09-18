#!/usr/bin/env python

# ==============================================================================
# RESUMEN DE FUNCIONALIDAD:
# Este archivo es el "maestro de obras" del proceso de compilación del motor.
# Su función es orquestar la compilación de todos los módulos de bajo nivel
# escritos en Cython y C. Cython es un lenguaje que mezcla Python y C para
# obtener un rendimiento muy alto en tareas críticas.
#
# Este script se encarga de:
#   1. Encontrar todas las librerías externas necesarias (SDL2, FFMpeg, Freetype, etc.).
#   2. Tomar todos los archivos de código fuente ".pyx" (Cython).
#   3. Convertirlos en archivos ".c".
#   4. Compilar esos archivos ".c" para crear los módulos binarios (.pyd en Windows,
#      .so en Linux) que forman el núcleo rápido del motor.
#
# RELEVANCIA PARA L-CODE:
# Este archivo es nuestro "panel de control" para modificar el motor.
# - Para añadir nuevas librerías (como Protocol Buffers), las declararemos aquí.
# - Para reemplazar un módulo de Ren'Py con nuestra propia versión optimizada,
#   modificaremos su entrada en este archivo.
# - Es la pieza central que nos permitirá construir nuestro "Motor L-Code Runtime".
# ==============================================================================


# Copyright 2004-2025 Tom Rothamel <pytom@bishoujo.us>
#
# ... (Licencia MIT - Permite la modificación y redistribución) ...
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import sys
import os

# CONFIGURACIÓN INICIAL DEL ENTORNO
# ---------------------------------
# EXPLICACIÓN: Se asegura de que el script se ejecute desde el directorio correcto
# y añade la carpeta 'scripts' al path de Python para poder importar las
# herramientas de compilación personalizadas.
BASE = os.path.abspath(os.path.dirname(sys.argv[0]))
os.chdir(BASE)

SCRIPTS = os.path.join(BASE, 'scripts')
sys.path.insert(0, SCRIPTS)

# IMPORTACIÓN DE LA LIBRERÍA DE CONSTRUCCIÓN PERSONALIZADA
# -----------------------------------------------------
# EXPLICACIÓN: En lugar de usar directamente las herramientas de Python (distutils/setuptools),
# Ren'Py utiliza su propia librería de ayuda llamada 'setuplib' para simplificar
# el proceso. La mayor parte de la lógica compleja está dentro de esa librería.
import setuplib
from setuplib import windows, library, cython, find_unnecessary_gen, generate_all_cython, env

import generate_styles

def main():
    """
    Función principal que orquesta todo el proceso de compilación.
    """

    setuplib.init()
    setuplib.check_imports(SCRIPTS, "setuplib.py", "generate_styles.py")

    # Genera código relacionado con los estilos de la interfaz.
    generate_styles.generate()

    # Opciones para el compilador de C.
    setuplib.extra_compile_args = [ "-Wno-unused-function" ]
    setuplib.extra_link_args = [ ]

    # LISTA DE "INGREDIENTES" (DEPENDENCIAS DE C)
    # ------------------------------------------
    # EXPLICACIÓN: Esta es la lista de todas las librerías de C externas que
    # el motor Ren'Py necesita para funcionar. 'pkg-config' es una herramienta
    # que ayuda a encontrar estas librerías en el sistema.
    pkgconfig_packages = """
    libavformat
    libavcodec
    libavutil
    libswresample
    libswscale
    harfbuzz
    freetype2
    fribidi
    sdl2
    """

    # DECLARACIÓN DE LIBRERÍAS
    # ------------------------
    # EXPLICACIÓN: Cada llamada a `library("nombre")` le dice al sistema de
    # compilación que busque y se enlace con una librería específica.
    # Por ejemplo, 'avformat' es para video, 'freetype' para fuentes, 'SDL2' para gráficos.
    library("avformat")
    library("avcodec")
    library("avutil")
    library("swresample")
    library("swscale")
    library("harfbuzz")
    library("freetype")
    library("fribidi")
    library("SDL2_image")
    library("SDL2")
    library("png")
    library("jpeg")
    library("z")

    # Dependencias específicas para Windows.
    if windows:
        setuplib.extra_compile_args.append("-fno-strict-aliasing")
        library("comdlg32")
        library("ole32")

    # Soporte opcional para Live2D Cubism.
    cubism = os.environ.get("CUBISM", None)
    if cubism:
        setuplib.include_dirs.append("{}/Core/include".format(cubism))

    pkgconfig_packages = "assimp\n" + pkgconfig_packages
    library("assimp") # Librería para importar modelos 3D.

    # COMPILACIÓN DE MÓDULOS DE CYTHON
    # ==================================
    # EXPLICACIÓN: Esta es la sección más importante. Cada llamada a `cython(...)`
    # define un módulo del motor que será compilado desde Cython/C a un binario.
    # Esto nos da un mapa completo de la arquitectura de bajo nivel del motor.

    # Módulos del núcleo en la carpeta 'src/'.
    cython("_renpy", [ "src/IMG_savepng.c", "src/core.c" ])
    cython("_renpybidi", [ "src/renpybidicore.c" ])
    cython("_renpytfd", [ "src/tinyfiledialogs/tinyfiledialogs.c" ])

    # Módulos del paquete 'renpy'.
    cython("renpy.astsupport")      # Soporte para el Árbol de Sintaxis Abstracta (AST).
    cython("renpy.cslots")         # Optimización para slots de clases.
    cython("renpy.lexersupport")   # Soporte para el analizador léxico (parser).
    cython("renpy.pydict")         # Implementación de diccionarios optimizada.
    cython("renpy.style")          # Núcleo del sistema de estilos.
    cython("renpy.encryption")     # Módulo de encriptación.

    # Módulos de audio.
    # NOTA: Aquí se compila el núcleo de sonido y la integración con FFMpeg para
    # reproducir múltiples formatos de audio y video.
    cython("renpy.audio.renpysound", [ "src/renpysound_core.c", "src/ffmedia.c" ],
        compile_args=[ "-Wno-deprecated-declarations" ] if ("RENPY_FFMPEG_NO_DEPRECATED_DECLARATIONS" in os.environ) else [ ])

    cython("renpy.audio.filter")   # Filtros de audio.

    # Módulos para datos de estilos.
    cython("renpy.styledata.styleclass")
    cython("renpy.styledata.stylesets")

    for p in generate_styles.prefixes:
        cython("renpy.styledata.style_{}functions".format(p), pyx=setuplib.gen + "/style_{}functions.pyx".format(p))

    # Módulos de display (renderizado).
    cython("renpy.display.matrix")
    cython("renpy.display.render")      # El renderizador principal.
    cython("renpy.display.accelerator")  # Aceleración de renderizado.
    cython("renpy.display.quaternion") # Para rotaciones 3D.

    # Módulos de renderizado por GPU (basado en OpenGL).
    cython("renpy.uguu.gl")
    cython("renpy.uguu.uguu")

    # Módulos del renderizador OpenGL 2.
    cython("renpy.gl2.gl2mesh")
    cython("renpy.gl2.gl2mesh2")
    cython("renpy.gl2.gl2mesh3")
    cython("renpy.gl2.gl2polygon")
    cython("renpy.gl2.gl2model")
    cython("renpy.gl2.gl2draw")
    cython("renpy.gl2.gl2texture")  # Manejo de texturas en la GPU.
    cython("renpy.gl2.gl2uniform")
    cython("renpy.gl2.gl2shader")   # Manejo de shaders.

    if cubism:
        cython("renpy.gl2.live2dmodel", [ "src/live2dcsm.c" ],)

    cython("renpy.gl2.assimp", [ "src/assimpio.cc" ], language="c++")

    # Módulos de texto.
    cython("renpy.text.textsupport") # Soporte base de texto.
    cython("renpy.text.texwrap")    # Lógica para el ajuste de línea (word wrap).
    cython("renpy.text.ftfont", [ "src/ftsupport.c", "src/ttgsubtable.c" ]) # Renderizado con Freetype.
    cython("renpy.text.hbfont", [ "src/ftsupport.c" ])

    # Módulos que replican la API de Pygame (una dependencia histórica de Ren'Py).
    cython("renpy.pygame.error")
    cython("renpy.pygame.color")
    cython("renpy.pygame.controller")
    cython("renpy.pygame.rect")
    cython("renpy.pygame.rwobject")
    cython("renpy.pygame.surface", source=[ "src/pygame/alphablit.c" ])
    cython("renpy.pygame.display")
    cython("renpy.pygame.event")
    cython("renpy.pygame.locals")
    cython("renpy.pygame.key")
    cython("renpy.pygame.mouse")
    cython("renpy.pygame.joystick")
    cython("renpy.pygame.power")
    cython("renpy.pygame.pygame_time")
    cython("renpy.pygame.image", source=[ "src/pygame/write_jpeg.c", "src/pygame/write_png.c" ])
    cython("renpy.pygame.transform", source=[ "src/pygame/SDL2_rotozoom.c" ])
    cython("renpy.pygame.gfxdraw", source=[ "src/pygame/SDL_gfxPrimitives.c" ])
    cython("renpy.pygame.draw")
    cython("renpy.pygame.scrap")

    # PASOS FINALES DE LA CONSTRUCCIÓN
    # --------------------------------
    generate_all_cython()
    find_unnecessary_gen()

    pkgconfig_packages = pkgconfig_packages.replace("\n", " ").strip()

    # Configura las variables de entorno para los compiladores.
    env("CC")
    env("LD")
    env("CXX")
    env("CFLAGS", f"pkg-config --cflags {pkgconfig_packages}")
    env("LDFLAGS", f"pkg-config --libs {pkgconfig_packages}")

    # INICIO DE LA COMPILACIÓN
    # ------------------------
    # EXPLICACIÓN: Esta es la llamada final. Pasa toda la configuración
    # que hemos definido a la librería `setuplib`, que se encarga de invocar
    # a los compiladores de Cython y C para construir todos los módulos.
    setuplib.setup("renpy", "8.99.99")


if __name__ == "__main__":
    main()
