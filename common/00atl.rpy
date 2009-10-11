# This file contains warpers that are used by ATL. They need to be defined
# early, so Ren'Py knows about them when parsing other files.

python early hide:

    # Interpolators.
    
    @renpy.atl_warper
    def linear(t):
        return t

