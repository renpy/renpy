#!/bin/bash

set -e

pip install -e .
python3 -m pytest
