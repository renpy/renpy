#!/bin/bash

# Clean and fix the project directory structure

cd $(dirname "$0")

shopt -s globstar

rm *.so renpy/**/*.so
rm -Rf renpy/pygame
