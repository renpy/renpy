#!/bin/bash
# ==============================================================================
# RESUMEN DE FUNCIONALIDAD:
# Este script es la herramienta principal para el desarrollador del motor. Su
# propósito es compilar cualquier módulo de Cython/C que haya sido modificado
# y, acto seguido, ejecutar la versión recién compilada de Ren'Py.
#
# Es el script que nosotros usaremos cada vez que queramos probar los cambios
# que hagamos en nuestro "Motor L-Code Runtime".
#
# El flujo es el siguiente:
#   1. Asegurarse de que estamos en un entorno de Python virtual.
#   2. Invocar a nuestro "maestro de obras" (el archivo setup.py) para que
#      compile las piezas necesarias.
#   3. Ejecutar el script principal de Ren'Py (renpy.py) para iniciar el motor.
# ==============================================================================

# Este comando asegura que si cualquier paso falla, el script se detendrá
# inmediatamente. Es una medida de seguridad para evitar errores en cascada.
set -e

# Establece la variable de entorno para especificar el comando de Cython.
export RENPY_CYTHON=cython

# Encuentra la ruta raíz del proyecto.
ROOT="$(dirname $(realpath $0))"
# Permite silenciar la salida de la compilación si se desea.
QUIET=${RENPY_QUIET- --quiet}

# Permite seleccionar una variante de compilación (para ejecución normal o para
# análisis de cobertura de código durante las pruebas).
if [ -n "$RENPY_COVERAGE" ]; then
    variant="renpy-coverage"
else
    variant="renpy-run"
fi

# VERIFICACIÓN DEL ENTORNO VIRTUAL DE PYTHON
# -------------------------------------------
# EXPLICACIÓN: Es una buena práctica de desarrollo en Python aislar las
# dependencias de un proyecto en un "entorno virtual". Este bloque de código
# se asegura de que uno de estos entornos esté activado antes de continuar.
if [ -n "$RENPY_VIRTUAL_ENV" ] ; then
    . "$RENPY_VIRTUAL_ENV/bin/activate"
fi

if [ -z "$VIRTUAL_ENV" ] ; then
    if [ -d "$ROOT/.venv" ] ; then
        . "$ROOT/.venv/bin/activate"
    else
        echo "Por favor, crea un entorno virtual primero (consulta el README)."
        exit 1
    fi
fi

# Configura la compilación para usar todos los núcleos de CPU disponibles,
# acelerando significativamente el proceso.
BUILD_J="-j $(nproc)"

# FUNCIÓN DE COMPILACIÓN
# ----------------------
# EXPLICACIÓN: Esta es la función que invoca a nuestro setup.py.
setup () {
    # Entra en el directorio del proyecto.
    pushd $1 >/dev/null

    # ¡EL COMANDO CLAVE DE COMPILACIÓN!
    # Llama a setup.py con los argumentos para construir las extensiones de C/Cython.
    # `-b` y `-t` especifican directorios de salida temporales.
    # `--inplace` asegura que los módulos compilados se coloquen junto a los
    # archivos fuente de Python, permitiendo que el motor los encuentre y los use.
    python setup.py $QUIET \
        build_ext -b tmp/build/lib.$variant -t tmp/build/tmp.$variant --inplace $BUILD_J \

    # Vuelve al directorio original.
    popd >/dev/null
}

# CONFIGURACIÓN OPCIONAL PARA LIVE2D CUBISM
# -----------------------------------------
if [ -e "$ROOT/cubism" ]; then
    export CUBISM="$ROOT/cubism"
    export CUBISM_PLATFORM=${CUBISM_PLATFORM:-linux/x86_64}
    export LD_LIBRARY_PATH="$CUBISM/Core/dll/$CUBISM_PLATFORM"
fi

# EJECUCIÓN DE LA COMPILACIÓN
# ---------------------------
# Llama a la función 'setup' que definimos arriba para compilar el motor.
setup "$ROOT/"

# PREPARACIÓN DE LA DISTRIBUCIÓN
# ------------------------------
# Después de compilar, este script vincula los directorios para que el motor
# pueda encontrar todos sus archivos como si fuera una instalación normal.
python "$ROOT/distribute.py" --link-directories

# EJECUCIÓN DEL MOTOR
# -------------------
# EXPLICACIÓN: Este bloque final decide qué hacer después de compilar.
if [ "$1" = "--build" ] ; then
    # Si el usuario solo quería compilar (ejecutando `./run.sh --build`),
    # muestra un mensaje y termina.
    echo "Compilación de Ren'Py completada."
else
    # Si no, usa 'exec' para reemplazar este script por el proceso del motor.
    # Esto inicia Ren'Py usando la versión que acabamos de compilar.
    # "$@" pasa cualquier argumento adicional directamente a Ren'Py.
    exec $RENPY_GDB python $ROOT/renpy.py "$@"
fi
