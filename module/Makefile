# This makefile should work on Linux, and might work on other unix-like
# platforms as well. It probably won't work on Mac OS X, however.

build:: _renpy.c pysdlsound.c nativemidi.c winmixer.c 
	python setup.py build_ext -i

clean:
	-rm *.so
	-rm -Rf build

%.c : %.pyx
	pyrexc $+