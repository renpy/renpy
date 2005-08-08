#!/usr/bin/env python

# Set this to false to disable the use of sdl-config to automatically
# figure out the compile arguments.
auto_configure = True

# The following are only respected if auto_configure is False.
include_dirs = [ "." ]
libraries = [ "SDL" ]
extra_compile_args = [ ]
extra_link_args = [ ]

# The following turn on optional modules.
nativemidi = None
winmixer = None

import distutils.core

def common():

    extensions = [ ]

    rpe = distutils.core.Extension(
        "_renpy",
        [ "core.c", "_renpy.c" ],
        extra_compile_args=extra_compile_args,
        extra_link_args=extra_link_args,
        include_dirs=include_dirs,
        libraries=libraries,
        )

    extensions.append(rpe)

    psse = distutils.core.Extension(
        "pysdlsound",
        [ "pss.c", "rwobject.c", "pysdlsound.c" ],
        extra_compile_args=extra_compile_args,
        extra_link_args=extra_link_args,
        include_dirs=include_dirs,
        libraries=[ "SDL_sound" ] + libraries,
        )

    extensions.append(psse)

    if nativemidi:
        nme = distutils.core.Extension(
            "nativemidi",
            nativemidi,
            libraries=nativemidi_libs,
            include_dirs=include_dirs,
            extra_link_args=extra_link_args,
            )
        
        extensions.append(nme)

    if winmixer:
        wme = distutils.core.Extension(
            "winmixer",
            [ 'winmixer.c' ],
            libraries=['winmm'],
            )

        extensions.append(wme)
    
    distutils.core.setup(
        name = "renpy_module",
        version = "5.1.0",
        ext_modules = extensions,
        )

if __name__ == "__main__":

    if auto_configure:
        try:
            import os
            
            extra_compile_args = os.popen("sdl-config --cflags").read().split()
            extra_link_args = os.popen("sdl-config --libs").read().split()
            include_dirs = [ ]
            libraries = [ ]

        except:

            print "I was unable to automatically configure the Ren'Py module."
            print "Perhaps sdl-config was not found, or could not be run."
            print
            print "Hopefully, you can figure it out yourself from the traceback below."
            print "Otherwise, email pytom@bishoujo.us for help."
            print
            raise

    common()
