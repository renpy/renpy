from setuptools import setup, Extension

ext_modules = [
    Extension(
        "sdl",
        sources=["sdl.c"],
        libraries=["SDL3"],
    )
]

setup(
    name="sdl",
    ext_modules=ext_modules,
)
