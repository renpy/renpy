from setuptools import setup, Extension
from Cython.Build import cythonize


extensions: list[Extension] = [ ]

def cython(module: str, source: list[str] = [ ], libraries: list[str] = [ ]) -> None:
    extensions.append(
        Extension(
            module,
            sources=[module.replace(".", "/") + ".pyx"] + source,
            include_dirs=[ "c" ],
            libraries=libraries + ["SDL3"],
        )
    )
cython("pygame.iostream")
cython("pygame.locals")
cython("pygame.image", source=[ "c/write_png.c", "c/write_jpeg.c" ], libraries=[ "SDL3_image", "jpeg", "png", "z"])
cython("pygame.sdl_image")
cython("pygame.controller")
cython("pygame.joystick")
cython("pygame.pygame_time")
cython("pygame.power")
cython("pygame.transform", source=[ "c/SDL3_rotozoom.c" ])
cython("pygame.scrap")
cython("pygame.key")
cython("pygame.mouse")
cython("pygame.event")
cython("pygame.display")
cython("pygame.sdl")
cython("pygame.color")
cython("pygame.rect")
cython("pygame.error")
cython("pygame.surface")
cython("pygame.draw")
cython("pygame.gfxdraw", source=[ "c/SDL3_gfxPrimitives.c",  "c/SDL3_rotozoom.c" ])

setup(
    name="sdl",
    ext_modules=cythonize(extensions),
    packages=["pygame"],
)
