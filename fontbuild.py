from distutils.core import setup
from distutils.extension import Extension
from distutils.command.build_ext import build_ext

try:
    from Cython.Distutils import build_ext
except ImportError:
    pass


ext_modules = [Extension("ftfont", [ "ftfont.pyx", "ftsupport.c" ],
    include_dirs=[ '/usr/include/freetype2' ],
    libraries=[ 'freetype' ],    
    extra_compile_args=['-O0', '-ggdb'],
    extra_link_args=['-O0', '-ggdb'],
    )]

setup(
    name = 'font',
    cmdclass = {'build_ext': build_ext},
    ext_modules = ext_modules    
)
