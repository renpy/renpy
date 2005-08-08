# This file will really only work on my Win32 system, as it uses
# sdl-config directly.

import setup

setup.extra_compile_args = [ "-O3", "-Ic:\\msys\\1.0\\local\\include" ]
setup.extra_link_args = [ "-Lc:\\msys\\1.0\\local\\lib", "-lSDL" ]
setup.includes = [ ]
setup.libraries = [ ]

setup.nativemidi = [ 'nativemidi.c', 'native_midi_win32.c', 'native_midi_common.c', 'rwobject.c' ]
setup.nativemidi_libs = [ 'winmm', 'SDL' ]

setup.winmixer = True

setup.common()
