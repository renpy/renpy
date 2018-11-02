# Copyright 2018 Shehriyar Qureshi <SShehriyar266@gmail.com>
import os
import sys

# add renpy directory to path else main module isn't found
current_directory = os.getcwd()
sys.path.insert(0, current_directory)

# thou shalt not move this artifact unless thou can without errors
import main


def test_renpy_path_to_renpy_base():

    # We're just doing what the function does and comparing the values.
    # This test should fail if the function is changed and returns
    # something else.

    # we change sys.argv to replicate normal renpy execution
    sys.argv.pop(1)
    sys.argv[0] = 'renpy.py'

    renpy_base = main.path_to_renpy_base()

    # we use sys.path[0] as it is the expected result of function
    assert renpy_base == sys.path[0]


def test_path_to_common():
    assert "{}/renpy/common".format(sys.path[0]) == main.path_to_common(
        sys.path[0])
