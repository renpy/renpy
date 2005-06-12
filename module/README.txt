This directory contains the source code for the _renpy module. This
module contains a number of image processing functions that aren't
present in pygame. If it's not present, then some of Ren'Py's
functionality will be missing. Games should still be playable, but
some effects may not be present, or may be present in a degraded form.

How does this affect you? Well, it depends on the platform you're
running on. So please read the appropriate selection below.


Windows
-------

If you're running an exe file under Windows, this doesn't affect you
one iota. Run it and be happy.

If you're running a python script under windows, you can download a
precompiled version of the module from the Ren'Py homepage, 
http://www.bishoujo.us/renpy/.


Macintosh
---------

You'll need to download a mpkg containing the precompiled version of
the _renpy module. You can grab it from http://www.bishoujo.us/renpy/.


Linux/Unix
----------

You'll need to compile the module yourself. Ensure that you have the
SDL development headers and libraries installed, and that you can run
the sdl-config program. Then, in this directory, type:

  python setup.py build_ext -i

It should autodetect SDL, and build the module in the current
directory. If successful, a file named _renpy.so will come into
existence. You can then run Ren'Py.


If you have question or problems, please contact us via the Ren'Py web
page, http://www.bishoujo.us/renpy/.

