# Copyright 2004-2014 Tom Rothamel <pytom@bishoujo.us>
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

# This file contains warpers that are used by ATL. They need to be defined
# early, so Ren'Py knows about them when parsing other files.

python early hide:

    # pause is defined internally, but would look like:
    #
    # @renpy.atl_warper
    # def pause(t):
    #     if t >= 1.0:
    #         return 1.0
    #     else:
    #         return 0.0

    @renpy.atl_warper
    def linear(t):
        return t

    @renpy.atl_warper
    def easeout(x):
        import math
        return 1.0 - math.cos(x * math.pi / 2.0)

    @renpy.atl_warper
    def easein(x):
        import math
        return math.cos((1.0 - x) * math.pi / 2.0)

    @renpy.atl_warper
    def ease(x):
        import math
        return .5 - math.cos(math.pi * x) / 2.0
