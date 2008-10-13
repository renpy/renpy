import sys
import os

try:
    import Image
except ImportError:
    print "Could not import the Image module. Please ensure that the Python Imaging"
    print "Library (PIL) is properly installed."

    sys.exit(-1)


