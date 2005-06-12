#!/bin/sh

pyrexc _renpy.pyx && python setup.py build_ext -i
