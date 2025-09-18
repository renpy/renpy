#!/bin/sh

# ==============================================================================
# RESUMEN DE FUNCIONALIDAD:
# Este script es una prueba de "ciclo completo". Su propósito es automatizar
# el proceso de:
#   1. Construir una nueva versión de distribución de Ren'Py (el SDK).
#   2. Descomprimir esa nueva versión en una carpeta temporal.
#   3. Ejecutar el lanzador de Ren'Py desde esa nueva versión para confirmar
#      que la construcción fue exitosa y que el programa se inicia.
#
# RELEVANCIA PARA L-CODE:
# Este script nos confirma que el archivo "distribute.py" es el verdadero
# "maestro de ceremonias" del empaquetado final en el Ren'Py original.
# Nuestro `compiler.py` se inspirará en la lógica de `distribute.py`, pero
# lo adaptará para empaquetar nuestro "Motor L-Code Runtime" y los archivos .lspmt.
# ==============================================================================

# PASO 1: CONSTRUIR LA DISTRIBUCIÓN
# ---------------------------------
# EXPLICACIÓN:
# - `lib/py3-linux-x86_64/python`: Forza el uso de una versión específica de Python
#   incluida con el código fuente, para asegurar que no haya conflictos con la
#   versión de Python instalada en el sistema.
# - `./distribute.py`: Este es el comando clave. Ejecuta el script principal de
#   distribución de Ren'Py.
# - `--nosign --fast`: Opciones para acelerar la prueba. `--nosign` evita la firma
#   criptográfica del paquete y `--fast` probablemente omite algunos pasos de
#   optimización para una compilación más rápida.
# - `$1`: Es el primer argumento que se le pasa al script. Por ejemplo, si se
#   ejecuta `./test_dlc.sh 7.4.11`, `$1` será "7.4.11". Esto se usa para nombrar
#   los archivos de salida.
lib/py3-linux-x86_64/python ./distribute.py --nosign --fast $1

# PASO 2: LIMPIEZA
# ----------------
# EXPLICACIÓN:
# - `rm -Rf`: Elimina de forma forzada y recursiva la carpeta de una prueba anterior.
#   Esto asegura que la prueba se realice con archivos completamente nuevos.
# - `/tmp/renpy-$1-sdk`: La carpeta temporal que se va a eliminar.
rm -Rf /tmp/renpy-$1-sdk

# PASO 3: DESCOMPRESIÓN
# ---------------------
# EXPLICACIÓN:
# - `unzip -d /tmp`: Descomprime el archivo resultante en la carpeta temporal del sistema.
# - `dl/$1/renpy-$1-sdk.zip`: La ruta al archivo que generó `distribute.py`.
#   Normalmente, Ren'Py guarda las distribuciones compiladas en una carpeta `dl/`.
unzip -d /tmp dl/$1/renpy-$1-sdk.zip

# PASO 4: EJECUTAR LA PRUEBA
# --------------------------
# EXPLICACIÓN:
# - `/tmp/renpy-$1-sdk/renpy.sh`: Este es el paso final. Ejecuta el script de
#   lanzamiento `renpy.sh` desde dentro de la carpeta recién descomprimida.
#   Si el lanzador de Ren'Py aparece en pantalla, la prueba ha sido un éxito.
/tmp/renpy-$1-sdk/renpy.sh
