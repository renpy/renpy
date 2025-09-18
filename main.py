#!/usr/bin/env python
# ==============================================================================
# RESUMEN DE FUNCIONALIDAD:
# Este es el punto de entrada más básico del motor. Piensa en él como la
# "llave de encendido" del coche. Su única y exclusiva responsabilidad es
# llamar al archivo principal `renpy.py` (el "motor de arranque") para que
# todo el sistema se ponga en marcha.
#
# En nuestro "Motor L-Code Runtime", este archivo se mantendrá prácticamente
# igual, asegurando un inicio limpio de la ejecución del juego.
# ==============================================================================

# Un script de arranque para el lanzador de Ren'Py.

# Importa la función principal, llamada 'main', desde nuestro archivo renpy.py.
from renpy import main

# Ejecuta la función principal que acabamos de importar.
# Esta simple llamada pone en movimiento toda la cadena de arranque que
# analizamos en el archivo renpy.py.
main()
