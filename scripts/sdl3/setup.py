from setuptools import setup, Extension
from Cython.Build import cythonize


extensions: list[Extension] = [ ]

def cython(module: str, source: list[str] = [ ]) -> None:
    extensions.append(
        Extension(
            module,
            sources=[module.replace(".", "/") + ".pyx"] + source,
            libraries=["SDL3"],
        )
    )


cython("pygame.sdl")
cython("pygame.color")

# cython("pygame.surface")

setup(
    name="sdl",
    ext_modules=cythonize(extensions),
)
