#!/bin/sh
python setup.py clean
python setup.py build --compiler=mingw32 install_lib -d $PYTHONPATH

