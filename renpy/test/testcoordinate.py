# import unittest
# not included in the shipped-in python, would be easier

from renpy.display.core import absolute, coordinate, px

def check():
    create_check()
    value_check()
    error_check()

def create_check():
    """
    Building coordinate instances, testing for internal errors.
    """
    coordinate(offset=1.) # constructed offset
    coordinate(offset=1., relative=.5) # constructed mixed
    10*px     # px-built positive offset
    -10*px    # px-built negative offset
    10*px+.7  # px-built mixed, positive offset, positive relative
    .7+10*px  # px-built mixed, positive relative, positive offset
    -10*px+.5 # px-built mixed, negative offset, positive relative
    .5-10*px  # px-built mixed, positive relative, negative offset
    10*px-.7  # px-built mixed, positive offset, negative relative
    -.7+10*px # px-built mixed, negative relative, positive offset
    -10*px-.5 # px-built mixed, negative offset, negative relative
    -.5-10*px # px-built mixed, negative relative, negative offset

def value_check():
    """
    Checking the correctness of absolute.compute's calculations.
    """
    if not (absolute.compute(10, 500) == 10.):
        raise ValueError("absolute.compute failing for integer value")
    if not (absolute.compute(.25, 500) == 125.):
        raise ValueError("absolute.compute failing for float value")
    if not (absolute.compute(absolute(6.25), 500) == 6.25):
        raise ValueError("absolute.compute failing for absolute value")

    # disabled because the offset argument is not optional
    # if not (absolute.compute(coordinate(relative=.25), 500) == 125.):
    #     raise ValueError("absolute.compute failing for relative coordinate")
    if not (absolute.compute(coordinate(offset=6.25), 500) == 6.25):
        raise ValueError("absolute.compute failing for offset coordinate")
    if not (absolute.compute(coordinate(offset=4.25, relative=.5), 500) == 254.25):
        raise ValueError("absolute.compute failing for relative+offset coordinate")
    if not (absolute.compute(coordinate(offset=4.25)+coordinate(offset=-50), 500) == -45.75):
        raise ValueError("absolute.compute failing for sum of offset coordinates")

    if not (absolute.compute(10*px, 500) == 10.):
        raise ValueError("absolute.compute failing for px-built offset coordinate")
    if not (absolute.compute(-10*px, 500) == -10.):
        raise ValueError("absolute.compute failing for px-built negative offset coordinate")
    if not (absolute.compute(10*px+.5, 500) == 260.):
        raise ValueError("absolute.compute failing for px-built mixed coordinate")
    if not (absolute.compute(-10*px+.5, 500) == 240.):
        raise ValueError("absolute.compute failing for px-built coordinate with negative offset followed with relative value")
    if not (absolute.compute(.5-10*px, 500) == 240.):
        raise ValueError("absolute.compute failing for px-built coordinate with relative value followed with negative offset")
    if not (absolute.compute(10*px+absolute(20)*px, 500) == 30.):
        raise ValueError("absolute.compute failing for sum of px-built offset coordinates")
    if not (absolute.compute(10*px+absolute(20)*px+.5, 500) == 280.):
        raise ValueError("absolute.compute failing for sum of px-built offset coordinates with a relative value")
    # disabled because summing coordinates with relative values is disabled
    # if not (absolute.compute(10*px+.5+absolute(20)*px, 500) == 280.):
    #     raise ValueError("absolute.compute failing for sum of px-built coordinates")

def error_check():
    """
    Testing for errors which should be there
    """
    try:
        1.*px
    except TypeError: pass
    else:
        raise Exception("Pure-float multiplication with coordinates should be disabled")

    try:
        (10*px+.5)*10
    except TypeError: pass
    else:
        raise Exception("Multiplication on coordinates with relative values should be disabled")

    try:
        10*px+10
    except TypeError: pass
    else:
        raise Exception("Adding integers to coordinates should be disabled")

    try:
        10*px+absolute(10)
    except TypeError: pass
    else:
        raise Exception("Adding absolutes to coordinates should be disabled")

    try:
        absolute.compute("left")
    except TypeError: pass
    else:
        raise Exception("Computing random values with absolute.compute should raise exceptions")
