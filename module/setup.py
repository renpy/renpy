#!/usr/bin/env python

# Set this to false to disable the use of sdl-config to automatically
# figure out the compile arguments.
auto_configure = True

# The following are only respected if auto_configure is False.
include_dirs = [ "." ]
libraries = [ "SDL" ]
extra_compile_args = [ ]
extra_link_args = [ ]

import distutils.core

def common():

    renpy_extension = distutils.core.Extension(
        "_renpy",
        [ "core.c", "_renpy.c" ],
        extra_compile_args=extra_compile_args,
        extra_link_args=extra_link_args,
        include_dirs=include_dirs,
        libraries=libraries,
        )
#                            include_dirs=[ "." ],
#                            libraries=[ "SDL" ],
    
    distutils.core.setup(
        name = "renpy_module",
        version = "4.8.2",
        ext_modules = [ renpy_extension ],
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
