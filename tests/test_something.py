# Copyright 2018 Shehriyar Qureshi <SShehriyar266@gmail.com>
from __future__ import print_function

import os
import sys

# add renpy directory to path else main module isn't found
pwd_result = os.getcwd()
sys.path.insert(0, pwd_result)

# thou shalt not move this artifact unless thou can without errors
import main


class TestRenpyPath:
    def test_renpy_path_to_common(self):

        # We're just doing what the function does and comparing the values.
        # This test should fail if the function is changed and returns
        # something else.

        # The reason we're doing the same thing as the function is because
        # the function uses os.path which, when running the program does the
        # right thing i.e return path to renpy directory but when this test
        # is run using pytest, the sys.argv values are changed from pointing
        # towards renpy folder to pointing towards the directory inside which
        # pytest resides.

        # Long comment para because most of the time output value is known
        # but in this case it changes to something else. Value is similar
        # but not consistent. Thank you for reading this big abomination.
        renpy_base = main.path_to_renpy_base()
        check_value = os.path.abspath(
            os.path.dirname(os.path.realpath(sys.argv[0])))

        assert renpy_base == check_value
