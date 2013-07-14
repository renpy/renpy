# Copyright 2004-2013 Tom Rothamel <pytom@bishoujo.us>
# See LICENSE.txt for license details.

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
