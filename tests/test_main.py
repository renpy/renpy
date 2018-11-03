# Copyright 2018 Shehriyar Qureshi <SShehriyar266@gmail.com>
import os
import sys

# add renpy directory to path else main module isn't found
current_directory = os.getcwd()
sys.path.insert(0, current_directory)

# thou shalt not move this artifact unless thou can without errors
import main


def test_renpy_path_to_renpy_base():

    renpy_base = main.path_to_renpy_base()

    # os.path.dirname removes the script name, which
    # in these test cases, is path to pytest executable.
    # So we're testing these functions using path to pytest
    # which should give us constant results and known output
    # value.
    assert renpy_base == os.path.dirname(sys.argv[0])


def test_path_to_common():
    # This test just checks that the function didn't get changed for some
    # reason
    assert "{}/renpy/common".format(os.path.dirname(
        sys.argv[0])) == main.path_to_common(os.path.dirname(sys.argv[0]))
