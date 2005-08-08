# This makefile should work on Linux, and might work on other unix-like
# platforms as well. It probably won't work on Mac OS X, however.

build::
	pyrexc _renpy.pyx
	pyrexc pysdlsound.pyx
	pyrexc nativemidi.pyx
	pyrexc winmixer.pyx
	python setup.py build_ext -i

clean:
	-rm *.so
	-rm -Rf build

