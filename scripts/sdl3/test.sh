#!/bin/bash

set -ex

SDL=/home/tom/sdl/install
export CFLAGS="-I$SDL/include"
export LDFLAGS="-L$SDL/lib"

uv run main.py $SDL/include/SDL3/SDL.h $SDL/include/SDL3/SDL_main.h
uv run main.py $SDL/include/SDL3_image/SDL_image.h  --early $SDL/include/SDL3/SDL.h
uv run python setup.py build_ext --inplace
