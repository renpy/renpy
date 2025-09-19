#!/bin/bash
# ==============================================================================
# RESUMEN DE FUNCIONALIDAD:
# Este script es una herramienta de atajo para los desarrolladores. Su propósito
# es vincular un motor de Ren'Py ya compilado (una "nightly build") con el
# directorio de código fuente actual.
#
# En lugar de compilar todo el código de C/Cython, un desarrollador puede
# descargar la última versión, ejecutar este script, y empezar a modificar los
# archivos .py inmediatamente, usando el motor pre-compilado.
#
# RELEVANCIA PARA L-CODE: Aunque nosotros SÍ vamos a compilar nuestro propio
# motor y, por lo tanto, no usaremos este script, este nos muestra un
# excelente ejemplo de cómo el "motor" (los ejecutables y librerías) puede
# ser un componente separado que se "conecta" al código fuente del juego.
# Es una validación de nuestra propia estrategia de empaquetado.
# ==============================================================================

# Encuentra la ruta raíz del proyecto de una manera robusta.
ROOT="$(dirname $(python -c "import os;print(os.path.realpath('$0'))"))"

# --- CREACIÓN DE ENLACES SIMBÓLICOS (ATAJOS) ---
# EXPLICACIÓN: `ln -s` crea un "enlace simbólico", que es como un acceso directo
# avanzado. Estos comandos hacen que ciertos archivos apunten a otros,
# evitando la necesidad de duplicar contenido.

# Enlaza el archivo de ayuda principal a los directorios de los juegos de ejemplo.
ln -s "$ROOT/help.html" "$ROOT/tutorial/README.html"
ln -s "$ROOT/help.html" "$ROOT/the_question/README.html"
ln -s "$ROOT/help.html" "$ROOT/templates/english/README.html"

# Enlaza el archivo fuente de la licencia al archivo LICENSE.txt en la raíz
# para que sea fácilmente accesible.
ln -s "$ROOT/sphinx/source/license.rst" "$ROOT/LICENSE.txt"


# --- VINCULACIÓN DEL MOTOR PRE-COMPILADO ---
# EXPLICACIÓN: Este bloque es el corazón del script. Se ejecuta solo si se le
# pasa un argumento al script (la ruta a la compilación de Ren'Py descargada).
if [ "$1" != "" ]; then

    # Enlaza el directorio 'lib' de la compilación descargada al directorio 'lib'
    # de nuestro código fuente. Este directorio contiene todos los módulos
    # compilados de C/Cython.
    ln -s "$1/lib" "$ROOT/lib"

    # Enlaza el ejecutable de macOS.
    ln -s "$1/renpy.app" "$ROOT"

    # Enlaza el ejecutable de Windows.
    ln -s "$1/renpy.exe" "$ROOT"

    # Enlaza el script de ejecución de Linux/macOS.
    ln -s "$1/renpy.sh" "$ROOT"
fi
