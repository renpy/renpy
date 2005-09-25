# This file will really only work on my mac. But hopefully it will give you
# an idea of how to do things on the mac platform.

import setup
import bdist_mpkg

setup.extra_compile_args = [ "-framework", "SDL",
                             "-I/Library/Frameworks/SDL.framework/Headers",
                             "-I/Users/tom/install/include/",
			     "-DMACOSX" ]
setup.extra_link_args = [ "-framework", "QuickTime",
                          "-framework", "SDL",
                          "-framework", "Cocoa",
                          "-L/Users/tom/install/lib",
                          "-framework", "smpeg" ]
setup.includes = [ ]
setup.libraries = [ ]

setup.nativemidi = [ 'nativemidi.c', 'native_midi_mac.c', 'native_midi_common.c', 'rwobject.c' ]
setup.nativemidi_libs = [ ]

setup.common()
