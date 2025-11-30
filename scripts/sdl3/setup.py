from setuptools import setup, Extension

ext_modules = [
    Extension(
        "pygame.sdl",
        sources=["pygame/sdl.c"],
        libraries=["SDL3"],
    )
]

setup(
    name="sdl",
    ext_modules=ext_modules,
)
