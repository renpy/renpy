#!/bin/bash

set -e

cython cslots.pyx
pip install -e .
python3 -m pytest
