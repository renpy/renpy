from setuptools import setup, Extension
from Cython.Build import cythonize


extensions: list[Extension] = [ ]

def cython(module: str, source: list[str] = [ ]) -> None:
    extensions.append(
        Extension(
            module,
            sources=[module.replace(".", "/") + ".pyx"] + source,
            include_dirs=[ "src/" ],
            libraries=["SDL3"],
        )
    )


cython("pygame.sdl")
cython("pygame.color")
cython("pygame.rect")
cython("pygame.error")
cython("pygame.surface")
cython("pygame.draw")
cython("pygame.gfxdraw", source=[ "c/SDL3_gfxPrimitives.c" ])
cython("pygame.joystick")
cython("pygame.display")

setup(
    name="sdl",
    ext_modules=cythonize(extensions),
    packages=["pygame"],
)
