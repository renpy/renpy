#!/usr/bin/env python
# ==============================================================================
# RESUMEN DE FUNCIONALIDAD:
# Este script es la herramienta de lanzamiento (release) del desarrollador
# principal de Ren'Py. Automatiza todo el proceso de tomar una versión ya
# compilada, etiquetarla oficialmente en el control de versiones (Git),
# crear una "Release" en GitHub y subir todos los archivos descargables.
#
# RELEVANCIA PARA L-CODE: Este script es nuestro manual de "cómo publicar
# software profesionalmente". Aunque las rutas a los archivos son específicas
# del desarrollador original, la lógica de cómo usar Git, la herramienta de
# GitHub (gh), y cómo manejar diferentes tipos de lanzamientos (estable,
# pre-lanzamiento, experimental) es exactamente lo que implementaremos para
# gestionar las versiones de nuestro "Motor L-Code Runtime".
# ==============================================================================

from __future__ import print_function

import argparse
import os
import subprocess
import sys

from renpy import version_tuple # @UnresolvedImport

# Obtiene la rama actual de Git para determinar qué repositorios usar.
branch = os.popen("git branch --show-current").read().strip()

# --- CONFIGURACIÓN DE RUTAS ---
# EXPLICACIÓN: Estas son las rutas a los diferentes repositorios de código en
# la computadora del desarrollador original. Muestra cómo el proyecto está
# dividido en varios componentes.
SOURCE = [
    "/home/tom/ab/renpy",
    "/home/tom/ab/renpy-build-" + branch,
    "/home/tom/ab/pygame_sdl2",
    ]


from renpy.versions import generate_vc_version

# Genera el número de versión actual.
version = generate_vc_version()["version"]
short_version = version.rpartition(".")[0]
major = version.partition(".")[0]
print("Version", version)

# Lógica para incluir componentes adicionales dependiendo de la versión mayor.
if major == '7':
    SOURCE.append("/home/tom/ab/renpy-build-fix/renpyweb")

# --- ANÁLISIS DE ARGUMENTOS DE LÍNEA DE COMANDOS ---
# EXPLICACIÓN: Define las opciones que controlan el tipo de lanzamiento.
ap = argparse.ArgumentParser()

ap.add_argument("--release", action="store_true") # Marca como un lanzamiento estable oficial.
ap.add_argument("--prerelease", action="store_true") # Marca como un pre-lanzamiento.
ap.add_argument("--experimental", action="store_true") # Marca como un lanzamiento experimental.
ap.add_argument("--no-tag", "-n", action="store_true") # Realiza el proceso sin crear una etiqueta de Git.
ap.add_argument("--push-tags", action="store_true") # Sube las etiquetas de Git al servidor remoto.
ap.add_argument("--delete-tag") # Borra una etiqueta existente.
ap.add_argument("--github", action="store_true") # Sube los archivos a una "Release" de GitHub.
ap.add_argument("--real", action="store_true") # Un seguro para evitar ejecuciones accidentales.

args = ap.parse_args()

# --- SEGURO DE EJECUCIÓN ---
# EXPLICACIÓN: Una excelente medida de seguridad. El script no hará nada
# peligroso a menos que se le pase explícitamente la bandera "--real".
if not args.real:
    print("¿Querías usar scripts/add_all.sh? Si no, proporciona --real.")
    sys.exit(1)

# --- LÓGICA DE PUBLICACIÓN EN GITHUB ---
if args.github:
    # Sube las etiquetas de Git.
    subprocess.call([ "git", "push", "--tags" ])
    # Usa la herramienta de línea de comandos de GitHub (`gh`) para crear una nueva "Release".
    subprocess.call([ "gh", "release", "create", version, "--notes", "See https://www.renpy.org/release/" + short_version, "-t", "Ren'Py {}".format(short_version) ])

    # Define el directorio donde están los archivos finales listos para subir.
    dn = "/home/tom/ab/renpy/dl/" + short_version

    # Itera sobre todos los archivos en el directorio de descargas...
    for fn in os.listdir(dn):

        # ...y sube cada archivo relevante como un "asset" a la Release de GitHub.
        if fn == ".build_cache":
            continue
        # (Se omiten varios filtros de archivos que no deben subirse)
        # ...
        subprocess.call([ "gh", "release", "upload", version, os.path.join(dn, fn) ])


    sys.exit(0)


# --- LÓGICA DE GESTIÓN DE ETIQUETAS (TAGS) ---
# EXPLICACIÓN: Un "tag" en Git es una marca permanente que señala una versión
# específica del código. Es la forma correcta de marcar un lanzamiento.
if args.release:
    # Calcula los checksums (firmas de archivo) para la versión.
    subprocess.check_call([ "/home/tom/ab/renpy/scripts/checksums.py", "/home/tom/ab/renpy/dl/" + short_version ])

if args.delete_tag:
    # Lógica para borrar una etiqueta en todos los repositorios.
    for i in SOURCE:
        os.chdir(i)
        tag = "renpy-" + args.delete_tag if i != SOURCE[0] else args.delete_tag
        subprocess.call([ "git", "tag", "-d", tag, ])
    sys.exit(0)

if args.push_tags:
    # Lógica para subir todas las etiquetas a los servidores remotos.
    for i in SOURCE:
        os.chdir(i)
        if subprocess.call([ "git", "push", "--tags" ]):
            print("Tags not pushed: {}".format(os.getcwd()))
            sys.exit(1)
    print("Pushed tags.")
    sys.exit(0)

# --- LÓGICA DE CREACIÓN DE ETIQUETAS Y ENLACES ---
if args.release:
    links = [ "release", "prerelease", "experimental" ]
    tag = True
elif args.prerelease:
    links = [ "prerelease", "experimental" ]
    tag = True
elif args.experimental:
    links = [ "experimental" ]
    tag = False
else:
    links = [ ]
    tag = False

if args.no_tag:
    tag = False

links = [ i + "-" + major for i in links ]

if tag:
    # Antes de crear una etiqueta, verifica que no haya cambios sin guardar.
    for i in SOURCE:
        os.chdir(i)
        if subprocess.call([ "git", "diff", "--quiet", "HEAD" ]):
            print("Directory not checked in: {}".format(os.getcwd()))
            sys.exit(1)

    # Crea la etiqueta de Git en todos los repositorios.
    for i in SOURCE:
        os.chdir(i)
        tag_name = version if i == SOURCE[0] else "renpy-" + version
        subprocess.check_call([ "git", "tag", "-a", tag_name, "-m", "Tagging Ren'Py + " + version + " release." ])

# --- ACTUALIZACIÓN DEL SITIO WEB ---
# EXPLICACIÓN: Finalmente, el script actualiza los enlaces simbólicos en el
# servidor web para que "latest-release" apunte a esta nueva versión y luego
# ejecuta scripts para subir los cambios al sitio web y la documentación.
os.chdir("/home/tom/ab/renpy/dl")
for i in links:
    if os.path.exists(i):
        os.unlink(i)
    os.symlink(short_version, i)

os.chdir("/home/tom/ab/website")
subprocess.check_call("./upload.sh")

os.chdir("/home/tom/ab/renpy/sphinx")
if args.release:
    subprocess.check_call("./upload.sh")
elif args.prerelease:
    subprocess.check_call("./upload_dev.sh")

print("Version", version)
