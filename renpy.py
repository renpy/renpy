#!/usr/bin/env python

# ==============================================================================
# RESUMEN DE FUNCIONALIDAD:
# Este es el script principal y el punto de entrada para ejecutar Ren'Py.
# Cuando un jugador hace doble clic en el .exe de un juego, este es el código
# que se ejecuta primero.
#
# Sus responsabilidades principales son:
#   1. Configurar el entorno de Python inicial.
#   2. Determinar las rutas de carpetas importantes (dónde está el juego,
#      dónde está el motor, y crucialmente, dónde se guardarán las partidas).
#   3. Iniciar el proceso de "bootstrap" (arranque), que carga el resto del motor.
#
# RELEVANCIA PARA L-CODE:
# Este archivo es el corazón de varias de nuestras modificaciones planeadas.
# - La función `path_to_saves` será COMPLETAMENTE REESCRITA en nuestro
#   "Motor L-Code Runtime" para implementar la lógica de guardado en la carpeta
#   "PROGRESOS JUEGOS" y para manejar la migración de guardados antiguos.
# - Modificaremos la lógica de `path_to_gamedir` para que siempre cargue los
#   datos desde nuestro paquete encriptado `.lspmt`.
# ==============================================================================


# This file is part of Ren'Py. The license below applies to Ren'Py only.
# Games and other projects that use Ren'Py may use a different license.

# Copyright 2004-2025 Tom Rothamel <pytom@bishoujo.us>
#
# ... (Licencia) ...
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from __future__ aimport print_function, absolute_import

import os
import sys
import warnings

# Funciones a ser personalizadas por los distribuidores. ################################
# EXPLICACIÓN: Estas funciones están diseñadas para que alguien que empaqueta
# Ren'Py pueda cambiar su comportamiento sin tocar el núcleo del motor.
# Nosotros las modificaremos directamente en nuestro fork.

def path_to_gamedir(basedir, name):
    """
    # EXPLICACIÓN: Devuelve la ruta absoluta a la carpeta que contiene los
    # scripts y assets del juego (esto se convierte en config.gamedir).
    #
    # MODIFICACIÓN L-CODE: En nuestro motor, esta función será modificada.
    # En lugar de buscar una carpeta 'game/', apuntará a la lógica que
    # descomprime y lee nuestro archivo de paquete `.lspmt`.
    """

    # Una lista de nombres candidatos para la carpeta del juego.
    candidates = [ name ]

    # Añade nombres candidatos basados en el nombre del ejecutable.
    game_name = name

    while game_name:
        prefix = game_name[0]
        game_name = game_name[1:]

        if prefix == ' ' or prefix == '_':
            candidates.append(game_name)

    # Añade candidatos por defecto.
    candidates.extend([ 'game', 'data', 'launcher/game' ])

    # Toma el primer candidato que exista.
    for i in candidates:

        if i == "renpy":
            continue

        gamedir = os.path.join(basedir, i)

        if os.path.isdir(gamedir):
            break

    else:
        gamedir = basedir

    return gamedir


def path_to_common(renpy_base):
    """
    # EXPLICACIÓN: Devuelve la ruta al directorio 'common' de Ren'Py, que
    # contiene los assets y scripts compartidos por el motor y el lanzador.
    """
    path = renpy_base + "/renpy/common"

    if os.path.isdir(path):
        return path
    return None


def path_to_saves(gamedir, save_directory=None): # type: (str, str|None) -> str
    """
    # ¡¡¡FUNCIÓN CRÍTICA PARA L-CODE!!!
    # EXPLICACIÓN: Esta función contiene toda la lógica para decidir dónde se
    # guardan los archivos de progreso del jugador. Tiene reglas diferentes para
    # Windows, macOS, Linux, Android e iOS.
    #
    # MODIFICACIÓN L-CODE (NUEVO PLAN): En nuestro "Motor L-Code Runtime", vamos a
    # ARRANCAR Y REEMPLAZAR toda esta función. Nuestra nueva implementación hará lo siguiente:
    #   1. Localizará la carpeta de "Documentos" del usuario de forma multiplataforma.
    #   2. Dentro de "Documentos", creará una carpeta llamada "PROGRESOS" si no existe.
    #   3. Dentro de "PROGRESOS", creará una carpeta con el nombre del juego
    #      (el `save_directory`, ej. 'MiNovelaIncreible') si no existe.
    #   4. Devolverá la ruta a la subcarpeta "saves" dentro de la carpeta del juego.
    #   5. La lógica de MIGRACIÓN de guardados antiguos NO será automática. En su lugar,
    #      las pantallas de la interfaz del juego (como la pantalla de carga) tendrán
    #      un botón "Importar Partidas Antiguas". Este botón abrirá un selector de
    #      archivos para que el usuario elija la carpeta con sus viejos .save, y el
    #      motor los convertirá a .luss al momento.
    """

    import renpy # @UnresolvedImport

    if save_directory is None:
        save_directory = renpy.config.save_directory
        save_directory = renpy.exports.fsencode(save_directory) # type: ignore

    # Se asegura de que se puede escribir en el directorio de guardado.
    def test_writable(d):
        try:
            fn = os.path.join(d, "test.txt")
            open(fn, "w").close()
            open(fn, "r").close()
            os.unlink(fn)
            return True
        except Exception:
            return False

    # Lógica para Android.
    if renpy.android:
        paths = [
            os.path.join(os.environ["ANDROID_OLD_PUBLIC"], "game/saves"),
            os.path.join(os.environ["ANDROID_PRIVATE"], "saves"),
            os.path.join(os.environ["ANDROID_PUBLIC"], "saves"),
            ]

        for rv in paths:
            if os.path.isdir(rv) and test_writable(rv):
                break
        else:
            rv = paths[-1]

        print("Saving to", rv)
        return rv

    # Lógica para iOS.
    if renpy.ios:
        from pyobjus import autoclass # type: ignore
        from pyobjus.objc_py_types import enum # type: ignore

        NSSearchPathDirectory = enum("NSSearchPathDirectory", NSDocumentDirectory=9)
        NSSearchPathDomainMask = enum("NSSearchPathDomainMask", NSUserDomainMask=1)

        NSFileManager = autoclass('NSFileManager')
        manager = NSFileManager.defaultManager()
        url = manager.URLsForDirectory_inDomains_(
            NSSearchPathDirectory.NSDocumentDirectory,
            NSSearchPathDomainMask.NSUserDomainMask,
            ).lastObject()

        try:
            rv = url.path().UTF8String()
        except Exception:
            rv = url.path.UTF8String()


        if isinstance(rv, bytes):
            rv = rv.decode("utf-8")

        print("Saving to", rv)
        return rv

    # Si no se da un directorio de guardado, lo pone en la carpeta del juego.
    if not save_directory:
        return os.path.join(gamedir, "saves")

    if "RENPY_PATH_TO_SAVES" in os.environ:
        return os.environ["RENPY_PATH_TO_SAVES"] + "/" + save_directory

    path = renpy.config.renpy_base

    while True:
        if os.path.isdir(path + "/Ren'Py Data"):
            return path + "/Ren'Py Data/" + save_directory

        newpath = os.path.dirname(path)
        if path == newpath:
            break
        path = newpath

    # Lógica para PC (Windows, macOS, Linux).
    if renpy.macintosh:
        rv = "~/Library/RenPy/" + save_directory
        return os.path.expanduser(rv)

    elif renpy.windows:
        if 'APPDATA' in os.environ:
            return os.environ['APPDATA'] + "/RenPy/" + save_directory
        else:
            rv = "~/RenPy/" + renpy.config.save_directory # type: ignore
            return os.path.expanduser(rv)

    else:
        rv = "~/.renpy/" + save_directory
        return os.path.expanduser(rv)


def path_to_renpy_base():
    """
    # EXPLICACIÓN: Devuelve la ruta a la carpeta base de Ren'Py.
    """

    renpy_base = os.path.dirname(os.path.abspath(__file__))
    renpy_base = os.path.abspath(renpy_base)

    return renpy_base

def path_to_logdir(basedir):
    """
    # EXPLICACIÓN: Devuelve la ruta a la carpeta de logs.
    """

    import renpy # @UnresolvedImport

    if renpy.android:
        return os.environ['ANDROID_PUBLIC']

    return basedir

def predefined_searchpath(commondir):
    # EXPLICACIÓN: Define las carpetas y el orden en que Ren'Py buscará los
    # archivos del juego (imágenes, scripts, etc.).
    import renpy # @UnresolvedImport

    searchpath = [ renpy.config.gamedir ]

    if renpy.android:
        if "ANDROID_PUBLIC" in os.environ:
            android_game = os.path.join(os.environ["ANDROID_PUBLIC"], "game")

            if os.path.exists(android_game):
                searchpath.insert(0, android_game)

        packs = [
            "ANDROID_PACK_FF1", "ANDROID_PACK_FF2",
            "ANDROID_PACK_FF3", "ANDROID_PACK_FF4",
        ]

        for i in packs:
            if i not in os.environ:
                continue

            assets = os.environ[i]

            for i in [ "renpy/common", "game" ]:
                dn = os.path.join(assets, i)
                if os.path.isdir(dn):
                    searchpath.append(dn)
    else:
        if "RENPY_SEARCHPATH" in os.environ:
            searchpath.extend(os.environ["RENPY_SEARCHPATH"].split("::"))

    if commondir and os.path.isdir(commondir):
        searchpath.append(commondir)

    if renpy.android or renpy.ios:
        print("Mobile search paths:" , " ".join(searchpath))

    return searchpath

##############################################################################


android = ("ANDROID_PRIVATE" in os.environ)

def main():
    # EXPLICACIÓN: Esta es la función principal que inicia todo.
    # Es el "botón de encendido" del motor.

    # Obtiene la ruta base del motor.
    renpy_base = path_to_renpy_base()

    # Añade la carpeta del motor al path de Python para que se puedan importar sus módulos.
    sys.path.append(renpy_base)

    # Ignora ciertos avisos de versiones antiguas.
    warnings.simplefilter("ignore", DeprecationWarning)

    # ¡INICIO DEL MOTOR!
    # ------------------
    # EXPLICACIÓN: Esta es la parte más importante. Llama al módulo 'bootstrap',
    # que es el responsable de cargar la configuración, inicializar los subsistemas
    # (video, audio, entrada) y finalmente, iniciar la ejecución del juego.
    try:
        import renpy.bootstrap
    except ImportError:
        print("No se pudo importar renpy.bootstrap. Asegúrate de haber descomprimido Ren'Py", file=sys.stderr)
        print("correctamente, preservando la estructura de directorios.", file=sys.stderr)
        raise

    renpy.__main__ = sys.modules[__name__] # type: ignore

    renpy.bootstrap.bootstrap(renpy_base)


if __name__ == "__main__":
    # EXPLICACIÓN: Esto asegura que la función `main()` se ejecute cuando se
    # llama a este archivo directamente desde la línea de comandos.
    main()


