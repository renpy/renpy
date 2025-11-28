#!/bin/bash

set -e

uv run main.py /usr/include/SDL3/SDL.h
uv run cython -3 sdl.pyx 2>&1
