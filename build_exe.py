#!/usr/bin/env python

from distutils.core import setup
import py2exe
import sys
import zipfile
import traceback

# The pythonpath on my system.
sys.path.insert(0, 'c:\\msys\\1.0\\newbuild25\\install\\bin')
sys.path.insert(0, 'c:\\msys\\1.0\\newbuild25\\install\\python')

def main():

    sys.argv[1:] = [ 'py2exe', '--bundle', '2', '-a', '--dll-excludes', 'w9xpopen.exe', ]
    # sys.argv[1:] = [ 'py2exe', '-a', '--dll-excludes', 'w9xpopen.exe', ]

    setup(name="RenPy",
          windows=[ dict(script="renpy.py",
                         dest_base="renpy",
                         icon_resources=[ (1, "newicon.ico") ],
                         ),
                    ],

          console=[ dict(script="renpy.py", dest_base="console") ],

          zipfile='renpy.code',

          options={ 'py2exe' : { 'excludes' : [ 'doctest',
                                                'pygame.macosx',
                                                'pygame.surfarray',
                                                'pygame.mixer',
                                                'pygame.mixer_music',
                                                'pygame.font',
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


    zfold = zipfile.ZipFile("dist/renpy.code")
    zfnew = zipfile.ZipFile("renpy.code", "w", zipfile.ZIP_STORED)

    seen = { }

    for fn in zfold.namelist():
        if fn.startswith("renpy/"):
            continue

        if fn in seen:
            continue

        if fn == "SDL_mixer.dll":
            continue
        
        seen[fn] = True

        zfnew.writestr(fn, zfold.read(fn))

    zfold.close()
    zfnew.close()

try:
    main()
except:
    traceback.print_exc()

print
print "Press return to quit."
raw_input()
