==============================
The Ren'Py Visual Novel Engine
==============================

http://www.renpy.org

Ren'Py development takes place on the ``master`` branch, and occasionally
on feature branches.


Getting Started
===============

Ren'Py depends on a number of python modules written in Cython and C. For
changes to Ren'Py that only involve python modules, you can use the modules
found in the latest nightly build. Otherwise, you'll have to compile the
modules yourself.

The development scripts assume a POSIX-like platform. The scripts should run
on Linux or Mac OS X, and can be made to run on Windows using an environment
like Msys.

Nightly Build
-------------

Nightly builds can be downloaded from:

   http://nightly.renpy.org

Note that the latest nightly build is at the bottom of the list. Once you've
unpacked the nightly, change into this repository, and run::

    ./after_checkout.sh <path-to-nightly>

Once this script completes, you should be able to run Ren'Py using renpy.sh,
renpy.app, or renpy.exe, as appropriate for your platform.

If the current nightly build doesn't work, please wait 24 hours for a new
build to occur. If that build still doesn't work, contact Tom (`pytom at bishoujo.us`,
or @renpytom on twitter) to find out what's wrong.

The ``doc`` symlink will dangle until documentation is built, as described
below.

Compiling the Modules
----------------------

Building the modules requires you have the many dependencies installed on
your system. On Ubuntu and Debian, these dependencies can be installed with
the command::

    apt-get install python-dev python-pygame libavcodec-dev libavformat-dev \
        libavresample-dev libfreetype6-dev libglew1.6-dev libsdl1.2-dev \
        libsdl-image1.2-dev libfribidi-dev libswscale-dev libesd0-dev libpulse-dev

Other platforms may have an equivalent command. Otherwise, you'll need to
build `renpy-deps <https://github.com/renpy/renpy-deps>`_.

We strongly suggest installing the Ren'Py modules into a Python
virtualenv. `This page <http://dabapps.com/blog/introduction-to-pip-and-virtualenv-python/>`_
describes how to install pip and the virtualenv tool, and set up a new virtualenv.

After activating the virtualenv, install cython::

    pip install -U cython

Next, set RENPY_DEPS_INSTALL To a \::-separated list of paths containing the
dependencies, and RENPY_CYTHON to the name of the cython command::

    export RENPY_DEPS_INSTALL=/usr::/usr/lib/x86_64-linux-gnu/
    export RENPY_CYTHON=cython

Finally, change into the `modules` directory, and run::

    python setup.py install

Ren'Py will be installed into the activated virtualenv. It can then be run
using the command::

    python -O renpy.py


Documentation
=============

Building
--------

Building the documentation requires Ren'Py to work. You'll either need to
link in a nightly build, or compile the modules as described above. You'll
also need the `Sphinx <http://sphinx-doc.org/>`_ documentation generator.
If you have pip working, install Sphinx using::

    pip install -U sphinx

Once Sphinx is installed, change into the ``sphinx`` directory inside the
Ren'Py checkout and run::

    ./build.sh

Format
------

Ren'Py's documentation consists of reStructuredText files found in sphinx/source, and
generated documentation found in function docstrings scattered throughout the code. Do
not edit the files in sphinx/source/inc directly, as they will be overwritten.

Docstrings may include tags on the first few lines:

\:doc: `section` `kind`
    Indicates that this functions should be documented. `section` gives
    the name of the include file the function will be documented in, while
    `kind` indicates the kind of object to be documented (one of ``function``,
    ``method`` or ``class``. If omitted, `kind` will be auto-detected.
\:name: `name`
    The name of the function to be documented. Function names are usually
    detected, so this is only necessary when a function has multiple aliases.
\:args: `args`
    This overrides the detected argument list. It can be used if some arguments
    to the function are deprecated.

For example::

    def warp_speed(factor, transwarp=False):
        """
        :doc: warp
        :name: renpy.warp_speed
        :args: (factor)

        Exceeds the speed of light.
        """

        renpy.engine.warp_drive.engage(factor)


Translating
===========

For best practices when it comes to translating the launcher and template
game, please read:

http://lemmasoft.renai.us/forums/viewtopic.php?p=321603#p321603


Contributing
============

For bug fixes, documentation improvements, and simple changes, just
make a pull request. For more complex changes, it might make sense
to file an issue first so we can discuss the design.
