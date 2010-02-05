from distutils.core import setup, Extension

setup(name="stuff",
      version="1.0",
      ext_modules=[
        Extension("tegl", ["tegl.c"], extra_compile_args=['-Wall'],
            libraries=['GLEW']),
      ])
