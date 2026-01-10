#!/bin/bash

set -e

uv run main.py /usr/include/SDL3/SDL.h /usr/include/SDL3/SDL_main.h
uv run python setup.py build_ext --inplace
