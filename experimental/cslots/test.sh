#!/bin/bash

set -e

cython -a cslots.pyx
pip install -e .
python3 -m pytest
