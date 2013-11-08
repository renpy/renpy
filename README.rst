==============================
The Ren'Py Visual Novel Engine
==============================

http://www.renpy.org


Branches
========

Ren'Py development takes place on two branches, ``master`` and
``devel``, as well as the occasional feature branch.

Master
------

The master branch contains code that can be run using the precompiled libraries in
the latest (release or pre-release) version of Ren'Py. It is mainly used for
bugfixes and features that do not require C or Cython code to implement.

To start please check out from devel into the `master` branch::

    git checkout master

After checking out master, run::

    ./after_checkout.sh <path-to-built-renpysdk>

to link in the libraries from the most recent Ren'Py. (On Windows, you
will need to run this under msys or cygwin however the use of cygwin is
deprecated because it would mean that this working copy of Ren'Py would
have to be covered by the GNU GPL.)

Ren'Py can then be run by running renpy.exe, renpy.sh, or renpy.app as
appropriate.

*NB* After completion of these steps, there will be an error in the symlink 
of the folder `doc`, making this inaccessible. This is because the documentation
has not been built using the documentation generator `sphinx`.

To build this please install the sphinx documentation generator using the python
package installation tool `pip`, install sphinx::

    pip install sphinx

Change directory into renpy/sphinx and run this command to build the documentation::

    ./ build.sh
    
This will be helpful to those who wish to change documentation files, and want to 
see the end result by running this build script.

Devel
-----

The devel branch contains code that requires a recompile of modules
implemented in C or Cython. Building devel requires you to have the
prerequisite libraries installed in addition to cython and other tools 
such as sphinx mentioned above to get a complete package. The installation
of some of the libraries requires permission to install them globally
however if one does not wish to do so, this can be overcome by installing 
the libraries into a python `virtualenv` (more information to this below under "Without Global Permissions") 

**With Global Permissions**
The required software can be installed using `pip`::

    pip install sphinx cython
    
Or `apt` and `easy_install`::

    apt-get install cython && easy_install -U sphinx

Then install the necessary libraries::

    apt-get install python-dev python-pygame libavcodec-dev libavformat-dev \
        libfreetype6-dev libglew1.6-dev libsdl1.2-dev libsdl-image1.2-dev \
        libfribidi-dev libswscale-dev libesd0-dev libpulse-dev
    
RENPY_DEPS_INSTALLED to a \::-separated list of paths containing dependencies:: 

    export RENPY_DEPS_INSTALL=/usr::/usr/lib/x86_64-linux-gnu/
    export RENPY_CYTHON=cython
    
Finally, change into the modules directory, and run::

    python setup.py install

Ren'Py can then be run by using python to run renpy.py

**Without Global Permissions**

If one does not have global permissions (or does not wish to use them) one can use python 
`virtualenv`. `virtualenv` is essentially a smaller installation of python made in the $HOME
directory to which one can add modules without su rights.

The easiest way to do this is to install `virtualenvwrapper` which includes more features 
than the stock `virtualenv` using pip::

    pip install virtualenvwrapper
    
Once this is done, please restart the shell so that `virtualenv` is available for use. Then 
one can make wrappers for managing the virtual environments and work on Ren'Py after 
installing the required libraries and modules::

    mkvirtualenv renpy
    workon renpy
     
Now one can install software into this virtual environment using `pip` as in the section *With Global Permission*. 
More information on how to use this tool can be found here: (http://virtualenvwrapper.readthedocs.org/en/latest/) 

Finally one can run renpy using::

    python renpy.py

Contributing
============

For bug fixes, documentation improvements, and simple changes, just
make a pull request. For more complex changes, it might make sense
to file an issue so we can discuss the design.

