# This makefile should work on Linux, and might work on other unix-like
# platforms as well. It probably won't work on Mac OS X, however.

all: _renpy.so

_renpy.c: _renpy.pyx
	pyrexc _renpy.pyx

_renpy.so: _renpy.c core.c
	python setup.py build_ext -i

clean:
	-rm _renpy.so
	-rm -Rf build
