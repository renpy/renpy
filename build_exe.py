#!/usr/bin/env python

import modulefinder
import shutil
from distutils.core import setup
import py2exe #@UnresolvedImport @UnusedImport
import sys
import zipfile
import traceback
import os

# The pythonpath on my system.
sys.path.insert(0, 'c:\\msys\\1.0\\newbuild\\install\\bin')
sys.path.insert(0, 'c:\\msys\\1.0\\newbuild\\install\\python')

def move_from_dist(fn):
    """
    Moves the file `fn` from the dist directory to the main
    directory. (This means we don't need symlinks on windows.)
    """

    if os.path.isdir(fn):
        shutil.rmtree(fn)
    elif os.path.exists(fn):
        os.unlink(fn)

    os.rename("dist/" + fn, fn)

import renpy
renpy.setup_modulefinder(modulefinder) #@UndefinedVariable

def main():

    sys.argv[1:] = [ 'py2exe', '-a', '--dll-excludes', 'w9xpopen.exe', ]

    setup(name="Ren'Py",
          windows=[ dict(script="renpy.py",
                         dest_base="renpy",
                         icon_resources=[ (1, "newicon.ico") ],
                         ),
                    ],

          console=[ dict(script="renpy.py", dest_base="console") ],

          zipfile='lib/windows-x86/renpy.code',

          options={ 'py2exe' : { 'excludes' : [ 'doctest',
                                                'pygame.macosx',
                                                'pygame.surfarray',
                                                'pygame.mixer',
                                                'pygame.mixer_music',
                                                '_ssl',
                                                '_hashlib',
                                                'win32con',
                                                'win32api',
                                                'Numeric',
                                                'locale',
                                                'gettext',
                                                'os2emxpath',
                                                'macpath',
                                                'posixpath',
                                                ],
                                 'optimize' : 2,
                                 } },
          )


    zfold = zipfile.ZipFile("dist/lib/windows-x86/renpy.code")
    zfnew = zipfile.ZipFile("dist/lib/windows-x86/renpy.code.new", "w", zipfile.ZIP_STORED)

    seen = { }

    for fn in zfold.namelist():
        if fn.startswith("renpy/"):

            # Keep around .pyo files that load pyd files.
            pydfn = fn.replace("/", ".").replace(".pyo", ".pyd")
            if not os.path.exists("dist/lib/windows-x86/" + pydfn):
                continue

        if fn in seen:
            continue

        if fn == "SDL_mixer.dll":
            continue
        
        seen[fn] = True

        zfnew.writestr(fn, zfold.read(fn))

    zfold.close()
    zfnew.close()

    os.unlink("dist/lib/windows-x86/renpy.code")
    os.rename("dist/lib/windows-x86/renpy.code.new", "dist/lib/windows-x86/renpy.code")

    shutil.copy("c:/Python26/Microsoft.VC90.CRT.manifest", "Microsoft.VC90.CRT.manifest")
    shutil.copy("c:/Python26/msvcr90.dll", "msvcr90.dll")

    move_from_dist("lib/windows-x86")
    move_from_dist("console.exe")
    move_from_dist("python26.dll")
    move_from_dist("renpy.exe")
    
    
try:
    main()
except:
    traceback.print_exc()

    
