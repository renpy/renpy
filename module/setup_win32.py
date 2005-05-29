# This file will really only work on my Win32 system, as it uses
# sdl-config directly.

import setup

setup.extra_compile_args = [ "-O3", "-Ic:\\msys\\1.0\\local\\include\\SDL" ]
setup.extra_link_args = [ "-Lc:\\msys\\1.0\\local\\lib", "-lSDL" ]
setup.includes = [ ]
setup.libraries = [ ]

setup.common()
