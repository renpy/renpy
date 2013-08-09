# This file sets up the normal python modules. It's used to help eclipse
# do type detection, by providing an importable version of the cython code.

from distutils.core import setup

setup(
    packages=['renpy', 'renpy.gl', 'renpy.angle', 'renpy.display', 'renpy.audio', 'renpy.text', 'pysdlsound'],
    package_dir={ 'pysdlsound' : 'module' },
    )

