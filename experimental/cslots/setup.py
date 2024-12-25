from setuptools import setup, Extension

setup(
    name="cslots",
    version="1.0.0",
    ext_modules=[
        Extension("cslots", [ "cslots.pyx" ]),
    ])
