#!/bin/bash

cd $(dirname $(dirname $(readlink -f $0)))

lib/py3-linux-x86_64/python add.py --real "$@"
