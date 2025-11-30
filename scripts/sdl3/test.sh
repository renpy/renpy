#!/bin/bash

set -e

uv run main.py /usr/include/SDL3/SDL.h
uv run cython -3 pygame/sdl.pyx 2>&1
uv run python setup.py build_ext --inplace
