from distutils.core import setup, Extension
from Cython.Distutils import build_ext


setup(name="stuff",
      version="1.0",
      cmdclass = {'build_ext': build_ext},
      ext_modules=[
        Extension(
            "tegl",
            ["tegl.c"],
            extra_compile_args=['-Wall'],
            libraries=['GLEW']),
        
        Extension(
            "pysdlgl",
            ["pysdlgl.pyx"],
            extra_compile_args=['-Wall'],
            include_dirs=['/usr/include/SDL'],
            libraries=['GLEW']),
        ])

      
