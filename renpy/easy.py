# Functions that make the user's life easier.

import renpy

def color(c):
    if isinstance(c, tuple) and len(c) == 4:
        return c

    if c is None:
        return c

    if isinstance(c, basestring):
        return renpy.display.text.color(c)

    raise Exception("Not a color: %r" % c)

def displayable(d):

    if isinstance(d, renpy.display.core.Displayable):
        return d

    if d is None:
        return d

    if isinstance(d, basestring):
        if d[0] == '#':
            return renpy.store.Solid(d)
        else:
            return renpy.store.Image(d)

    # We assume the user knows what he's doing in this case.
    if hasattr(d, 'parameterize'):
        return d
    
    raise Exception("Not a displayable: %r" % d)
