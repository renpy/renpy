#!/usr/bin/env python
import distutils.core
import os
import os.path
import platform
import sys
import subprocess

try:
    import bdist_mpkg
except:
    pass


# These control the level of optimization versus debugging.
# extra_compile_args = [ "-O3", "-funroll-loops" ]
extra_compile_args = [ "-O0", "-ggdb" ]
# extra_compile_args = [ "-O0", "-gstabs" ]

# This environment variable should have the full path to the installed
# Ren'Py dependencies.
install = os.environ.get("RENPY_DEPS_INSTALL", None)

if install is None:
    print """
The RENPY_DEPS_INSTALL environment variable has not been set. This
should be set to a double-colon-delimited list of places where the
Ren'Py dependencies can be found. (To use system libraries, this can
be set to a system directory, like /usr.)
"""
    sys.exit(-1)

install = install.split("::")

include_dirs = [ ]
library_dirs = [ ]

def add_include(prefix, file):
    """
    Search for prefix/file underneath <i> and <i>/include, for each of the
    directories <i> in install. When found, puts the directory it was found
    in into include_dirs.
    """

    checked = [ ]
    for i in install:

        dir = os.path.join(i, prefix)
        fn = os.path.join(dir, file)
        fn = os.path.normpath(fn)
        checked.append(fn)
        if os.path.exists(fn):
            break

        dir = os.path.join(i, "include", prefix)
        fn = os.path.join(dir, file)
        fn = os.path.normpath(fn)
        checked.append(fn)

        if os.path.exists(fn):
            break
        
    else:

        print "Could not find include %s." % file
        print "The paths searched were:"
        for i in checked:
            print "-", i
        sys.exit(-1)

    dir = os.path.normpath(dir)
        
    print "Found %s in %s." % (file, dir)
        
    if dir not in include_dirs:
        include_dirs.append(dir)

def add_library(name, optional=False):
    """
    This looks for a library named name in the <i> and <i>/lib, for all
    <i> in install. When found, it adds it to library_dirs.
    """

    checked = [ ]
    
    for i in install:
        for d in ('', 'lib'):
            for suffix in (".so", ".dylib", ".a"):

                dir = os.path.join(i, d)
                fn = os.path.join(dir, name + suffix)
                checked.append(fn)
                
                if os.path.exists(fn):
                    print "Found %s." % fn

                    if dir not in library_dirs:
                        library_dirs.append(dir)
                    return True

    if optional:
        return False
                
    print "Couldn't find library %s." % name
    print "The paths searched were:"
    for i in checked:
        print "-", i
    sys.exit(-1)

def cython(fn):
    """
    Use cython to generate `fn`.c from `fn`.pyx, if necessary.
    """

    c = fn + ".c"
    pyx = fn + ".pyx"

    if not os.path.exists(pyx):
        print pyx, "not in current directory, not running cython."
        return

    if os.path.exists(c) and os.path.getmtime(c) >= os.path.getmtime(pyx):
        print pyx, "is not newer than", c
        return

    subprocess.call(["cython", pyx])
    
    
add_include("", "zlib.h")
add_include("", "png.h")
add_include("SDL", "SDL.h")
add_include("", "ft2build.h")
add_include("freetype2", "freetype/freetype.h")
add_include("", "libavutil/avstring.h")
add_include("", "libavformat/avformat.h")
add_include("", "libavcodec/avcodec.h")
add_include("", "libswscale/swscale.h")
add_include("", "GL/glew.h")

add_library("libSDL")
add_library("libpng")
add_library("libavformat")
add_library("libavcodec")
add_library("libavutil")
has_swscale = add_library("libswscale", True)
add_library("libfreetype")
add_library("libfribidi")            
add_library("libz")
add_library("libGLEW")

cython("_renpy")
cython("_renpybidi")
cython("_renpy_pysdlgl")
cython("sound")
cython("winmixer")

extra_link_args = [ ]

sdl_libraries = [ 'SDL' ]
png_libraries = [ 'png', "z" ]

sound_libraries = [ "avformat", "avcodec", "avutil", "z" ]
if has_swscale:
    sound_libraries.insert(0, "swscale")

# The following turn on optional modules.
winmixer = None
linmixer = None

# Detect win32.
if platform.win32_ver()[0]:
    extra_compile_args.append("-fno-strict-aliasing")
    winmixer = True

# Detect OSS.
try:
    import ossaudiodev
    linmixer = True
except:
    pass

extensions = [ ]
py_modules = [ 'pysdlsound.__init__' ]

extensions.append(distutils.core.Extension(
    "_renpy",
    [ "IMG_savepng.c", "core.c", "rwobject.c", "_renpy.c", "subpixel.c" ],
    include_dirs=include_dirs,
    library_dirs=library_dirs,
    extra_compile_args=extra_compile_args,
    extra_link_args=extra_link_args,
    libraries=sdl_libraries + png_libraries,
    ))

extensions.append(distutils.core.Extension(
    "_renpy_font",
    [ "renpy_ttf.c", "renpy_font.c"],
    include_dirs=include_dirs,
    library_dirs=library_dirs,
    extra_compile_args=extra_compile_args,
    extra_link_args=extra_link_args,
    libraries=sdl_libraries + [ 'freetype', 'z' ],
    ))

extensions.append(distutils.core.Extension(
    "pysdlsound.sound",
    [ "pss.c", "rwobject.c", "sound.c", "ffdecode.c" ],
    include_dirs=include_dirs,
    library_dirs=library_dirs,
    extra_compile_args=extra_compile_args,
    extra_link_args=extra_link_args,
    libraries=sound_libraries + sdl_libraries,
    ))


if winmixer:
    extensions.append(distutils.core.Extension(
        "pysdlsound.winmixer",
        [ 'winmixer.c' ],
        libraries=['winmm'],
        ))

if linmixer:
    py_modules.append('pysdlsound.linmixer')

extensions.append(distutils.core.Extension(
    "_renpybidi",
    ["_renpybidi.c", "renpybidicore.c"],
    include_dirs=include_dirs,
    library_dirs=library_dirs,
    libraries=['fribidi'],
    ))

extensions.append(distutils.core.Extension(
    "_renpy_tegl",
    ["_renpy_tegl.c"],
    extra_compile_args=extra_compile_args,
    include_dirs=include_dirs,
    library_dirs=library_dirs,
    libraries=['GLEW']))
        
extensions.append(distutils.core.Extension(
    "_renpy_pysdlgl",
    ["_renpy_pysdlgl.c"],
    extra_compile_args=extra_compile_args,
    include_dirs=include_dirs,
    library_dirs=library_dirs,
    libraries=['GLEW']))

distutils.core.setup(
    name = "renpy_module",
    version = "6.11.0",
    ext_modules = extensions,
    py_modules = py_modules,
    package_dir = { '' : 'lib' },
    )

print "BIG FAT WARNING! DEBUGGGING IS STILL ENABLED!"