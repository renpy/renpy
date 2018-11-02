# Copyright 2018 Shehriyar Qureshi <SShehriyar266@gmail.com>
import os
import sys

# add renpy directory to path else main module isn't found
current_directory = os.getcwd()
sys.path.insert(0, current_directory)

# thou shalt not move this artifact unless thou can without errors
import main


class TestRenpyPath:
    def test_renpy_path_to_common(self):

        # We're just doing what the function does and comparing the values.
        # This test should fail if the function is changed and returns
        # something else.

        # The reason we're doing the same thing as the function is because
        # the function uses os.path which, when running the program does the
        # right thing i.e return path in which renpy directory resides but
        # when this test is run using pytest, the sys.argv values are changed
        # from pointing towards directory in which renpy resides to pointing
        # towards the directory inside which pytest resides.

        renpy_base = main.path_to_renpy_base()
        check_value = os.path.abspath(
            os.path.dirname(os.path.realpath(sys.argv[0])))

        assert renpy_base == check_value
