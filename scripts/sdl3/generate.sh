#!/bin/bash

set -ex

SDL=/home/tom/sdl/install

uv run main.py $SDL/include/SDL3/SDL.h $SDL/include/SDL3/SDL_main.h
uv run main.py $SDL/include/SDL3_image/SDL_image.h  --early $SDL/include/SDL3/SDL.h
