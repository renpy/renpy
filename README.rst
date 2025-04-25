==============================
The Ren'Py Visual Novel Engine
==============================

https://www.renpy.org


Branches
========

The following branches are the most interesting.

``fix``
    The fix branch is used for fixes to the current version of Ren'Py that do
    not require dangerous changes. The fix branch is also the source of the
    documentation on https://www.renpy.org/. This branch is automatically
    merged into master on a regular basis.

    Pull requests that contain fixes or documentation improvements should be
    made to the fix branch. When a release is made, the master branch is
    copied to the fix branch.

``master``
    The master branch is where the main focus of development is. This branch
    will eventually become the next release of Ren'Py.

    Pull requests that contain new features, that require incompatible changes,
    or major changes to Ren'Py's internals should be targeted at the master
    branch.


Getting Started
===============

Ren'Py depends on a number of Python modules written in Cython and C. For
changes to Ren'Py that only involve Python modules, you can use the modules
found in the latest nightly build. Otherwise, you'll have to compile the
modules yourself.

The development scripts assume a POSIX-like platform. The scripts should run
on Linux or macOS, and can be made to run on Windows using an environment
like MSYS.

Nightly Build
-------------

Nightly builds can be downloaded from:

   https://nightly.renpy.org

Note that the latest nightly build is at the bottom of the list. Once you've
unpacked the nightly, change into this repository, and run::

    ./after_checkout.sh <path-to-nightly>

Once this script completes, you should be able to run Ren'Py using renpy.sh,
renpy.app, or renpy.exe, as appropriate for your platform.

If the current nightly build doesn't work, please wait 24 hours for a new
build to occur. If that build still doesn't work, contact Tom (`pytom at bishoujo.us`,
or @renpytom on Twitter/X) to find out what's wrong.

The ``doc`` symlink will dangle until documentation is built, as described
below.

Compiling the Modules
----------------------

Building the modules requires you have the many dependencies installed on
your system. On Ubuntu and Debian, these dependencies can be installed with
the command::

    sudo apt install virtualenvwrapper python3-dev libassimp-dev libavcodec-dev libavformat-dev \
        libswresample-dev libswscale-dev libharfbuzz-dev libfreetype6-dev libfribidi-dev libsdl2-dev \
        libsdl2-image-dev libsdl2-gfx-dev libsdl2-mixer-dev libsdl2-ttf-dev libjpeg-dev pkg-config

Ren'Py requires SDL_image 2.6 or greater. If your distribution doesn't include
that version, you'll need to download it from:

    https://github.com/libsdl-org/SDL_image/tree/SDL2

We strongly suggest installing the Ren'Py modules into a Python
virtualenv. To create a new virtualenv, open a new terminal and run::

    . /usr/share/virtualenvwrapper/virtualenvwrapper.sh
    mkvirtualenv renpy

To return to this virtualenv later, run::

    . /usr/share/virtualenvwrapper/virtualenvwrapper.sh
    workon renpy

After activating the virtualenv, install additional dependencies::

    pip install -U setuptools cython future six typing pefile requests ecdsa

Then, install pygame_sdl2 by running the following commands::

    git clone https://www.github.com/renpy/pygame_sdl2
    pushd pygame_sdl2
    python setup.py install
    popd

Finally, use setup.py to compile extension modules that support Ren'Py::

    python setup.py install

Ren'Py will be installed into the activated virtualenv. It can then be run
using the command::

    python renpy.py


Other Platforms
---------------

Where supported, Ren'Py will attempt to find include directories and library paths
using pkg-config. If pkg-config is not present, include and library paths can be
specified using CFLAGS and LDFLAGS.

If RENPY_CFLAGS is present in the environment and CFLAGS is not, setup.py
will set CFLAGS to RENPY_CFLAGS. The same is true for RENPY_LDFLAGS,
RENPY_CC, RENPY_CXX, and RENPY_LD.

Setup.py does not support cross-compiling. See https://github.com/renpy/renpy-build
for software that cross-compiles Ren'Py for many platforms.


Documentation
=============

Building
--------

Building the documentation requires Ren'Py to work. You'll either need to
link in a nightly build, or compile the modules as described above. You'll
also need the `Sphinx <https://www.sphinx-doc.org>`_ documentation generator.
If you have pip working, install Sphinx using::

    pip install -U sphinx sphinx_rtd_theme sphinx_rtd_dark_mode

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
    Indicates that this function should be documented. `section` gives
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

https://lemmasoft.renai.us/forums/viewtopic.php?p=321603#p321603


Contributing
============

For bug fixes, documentation improvements, and simple changes, just
make a pull request. For more complex changes, it might make sense
to file an issue first so we can discuss the design.

License
=======

For the complete licensing terms, please read:

https://www.renpy.org/doc/html/license.html
