#!/usr/bin/env python


import distutils.core
import os
import os.path
import platform
import sys

try:
    import bdist_mpkg
except:
    pass

# This environment variable should have the full path to the installed
# Ren'Py dependencies.
install = os.environ.get("RENPY_DEPS_INSTALL", "/does/not/exist")

# Check to see if that's the case.
if not os.path.isdir(install):
    print "The Ren'Py dependencies install directory:"
    print
    print install
    print
    print "does not exist. Please set RENPY_DEPS_INSTALL to the correct"
    print "location of the Ren'Py dependencies install directory, and "
    print "re-run this script."
    sys.exit(-1)

ffmpeg = os.environ.get("FFMPEG_BUILD_PATH", "/does/not/exist")

if not os.path.isdir(install):
    print "The FFMPEG build path:"
    print
    print ffmpeg
    print
    print "does not exist. Please set FFMPEG_BUILD_PATH to the correct"
    print "location and re-run this script."
    sys.exit(-1)

    
# Default compile arguements for everybody.
include_dirs = [ install + "/include",
                 install + "/include/SDL",
                 install + "/include/freetype2",
                 install + "/include/pygame",
                 ffmpeg]

library_dirs = [ install + "/lib" ]

# Fast math breaks on windows. :-(
extra_compile_args = [ "-O3", "-funroll-loops" ] # , "-ffast-math" ]
# extra_compile_args = [ "-O0", "-ggdb" ]

extra_link_args = [ ]

sdl_libraries = [ 'SDL' ]
sound_libraries = [ "avformat", "avcodec", "avutil", "z" ]


# The following turn on optional modules.
winmixer = None
linmixer = None

# Detect win32.
if platform.win32_ver()[0]:
    extra_compile_args.append("-fno-strict-aliasing")
    winmixer = True

# Detect mac.
if platform.mac_ver()[0]:
    nativemidi_libs = [ 'SDL' ]

# Detect OSS.
try:
    import ossaudiodev
    linmixer = True
except:
    pass

extensions = [ ]
py_modules = [ 'pysdlsound.__init__' ]

rpe = distutils.core.Extension(
    "_renpy",
    [ "core.c", "rwobject.c", "_renpy.c", "subpixel.c" ],
    include_dirs=include_dirs,
    library_dirs=library_dirs,
    extra_compile_args=extra_compile_args,
    extra_link_args=extra_link_args,
    libraries=sdl_libraries,
    )

extensions.append(rpe)

renpy_font = distutils.core.Extension(
    "_renpy_font",
    [ "renpy_ttf.c", "renpy_font.c"],
    include_dirs=include_dirs,
    library_dirs=library_dirs,
    extra_compile_args=extra_compile_args,
    extra_link_args=extra_link_args,
    libraries=sdl_libraries + [ 'freetype' ],
    )

extensions.append(renpy_font)

psse = distutils.core.Extension(
    "pysdlsound.sound",
    [ "pss.c", "rwobject.c", "sound.c", "ffdecode.c" ],
    include_dirs=include_dirs,
    library_dirs=library_dirs,
    extra_compile_args=extra_compile_args,
    extra_link_args=extra_link_args,
    libraries=sound_libraries + sdl_libraries,
    )

extensions.append(psse)

if winmixer:
    wme = distutils.core.Extension(
        "pysdlsound.winmixer",
        [ 'winmixer.c' ],
        libraries=['winmm'],
        )

    extensions.append(wme)

if linmixer:
    py_modules.append('pysdlsound.linmixer')

distutils.core.setup(
    name = "renpy_module",
    version = "6.9.1",
    ext_modules = extensions,
    py_modules = py_modules,
    package_dir = { '' : 'lib' },
    )

