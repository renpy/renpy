# This file will really only work on my Win32 system, as it uses
# sdl-config directly.

import setup
import bdist_mpkg

setup.extra_compile_args = [ "-framework", "SDL", "-I/Library/Frameworks/SDL.framework/Headers" ]
setup.extra_link_args = [ "-framework", "SDL" ]
setup.includes = [ ]
setup.libraries = [ ]

setup.common()
