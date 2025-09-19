#!/bin/bash
# ==============================================================================
# RESUMEN DE FUNCIONALIDAD:
# Este es un script de limpieza. Su propósito es eliminar todos los archivos
# que se generaron durante el proceso de compilación del motor (los archivos .so)
# y otras carpetas temporales.
#
# RELEVANCIA PARA L-CODE: Es una herramienta de mantenimiento para los
# desarrolladores del motor. La ejecutamos cuando queremos asegurarnos de que
# la siguiente compilación sea completamente nueva, sin restos de archivos
# antiguos que puedan causar problemas.
# ==============================================================================

# Limpia y arregla la estructura de directorios del proyecto

# Se posiciona en el directorio donde se encuentra este script.
cd $(dirname "$0")

# Habilita el "globstar", una opción de bash que permite usar `**` para
# buscar archivos en subdirectorios de forma recursiva.
shopt -s globstar

# --- COMANDOS DE LIMPIEZA ---

# Borra todos los archivos .so (bibliotecas compiladas de C/Cython) que se
# encuentren en el directorio raíz y en cualquier subdirectorio de 'renpy'.
rm *.so renpy/**/*.so

# Borra de forma recursiva y forzada el directorio 'renpy/pygame'.
# Esto se hace probablemente para eliminar una versión antigua o temporal de
# los módulos de pygame que Ren'Py utiliza.
rm -Rf renpy/pygame
