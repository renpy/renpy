# This file was automatically generated from renpy/gl/glblacklist.py
# Modifications will be automatically overwritten.

# Copyright 2004-2018 Tom Rothamel <pytom@bishoujo.us>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


# The blacklist of OpenGL cards. Fields are:
# - A substring of the Renderer.
# - A substring of the Version.
# - True to allow shader rendering.
# - True to allow fixed-function rendering.

# If both of the last two entries are false, GL refuses to
# start.

BLACKLIST = [

    # Crashes for Mugenjohncel.
    ("S3 Graphics DeltaChrome", "1.4 20.00", False, False),

    # A bug in Mesa 7.9 and 7.10 (before 7.10.3) causes the system to
    # fail to initialize the GLSL compiler.
    # https://bugs.freedesktop.org/show_bug.cgi?id=35603
    ("Mesa", "Mesa 7.9", False, True),
    ("Mesa", "Mesa 7.10.3", True, True),
    ("Mesa", "Mesa 7.10", False, True),

    # Default to allowing everything.
    ("", "", True, True),
    ]
