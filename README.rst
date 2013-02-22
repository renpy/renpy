==============================
The Ren'Py Visual Novel Engine
==============================

http://www.renpy.org


Branches
========

Ren'Py development takes place on two branches, ``master`` and
``devel``, as well as the occasional feature branch.

Master
-----

The master branch contains code that can be run using the libraries in
the latest (release or pre-release) version of Ren'Py. It's used for
bugfixes and features that do not require C or Cython code to
implement.

After checking out master, run::

    ./after_checkout.sh <path-to-renpy>

to link in the libraries from the most recent Ren'Py. (On Windows, you
will need to run this under msys or cygwin.)

Ren'Py can then be run by running renpy.exe, renpy.sh, or renpy.app as
appropriate.

Devel
-----

The devel branch contains code that requires a recompile of modules
implemented in C or Cython. Building devel requires you to have the
prerequisite libraries installed. Then set RENPY_DEPS_INSTALLED to
a \::-separated list of paths containing dependencies. For example::

  export RENPY_DEPS_INSTALL=/usr::/usr/lib/x86_64-linux-gnu/

Finally, change into the modules directory, and run::

  python setup.py install

Ren'Py can then be run by using python to run renpy.py.


Contributing
============

For bug fixes, documentation improvements, and simple changes, just
make a pull request. For more complex changes, it might make sense
to file an issue so we can discuss the design.

