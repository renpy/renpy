# Rules for renders: Every widget creates its own Render, even if all
# it does is blit that render somewhere else.

import time
import renpy
import pygame
from pygame.constants import *

# We only cache a single solid... but that should be enough to handle
# some important cases, like button and window backgrounds.
class SolidCache(object):

    def __init__(self):
        self.size = None
        self.color = None
        self.cached = None
    
    def create(self, size, color):
        if size == self.size and color == self.color:
            return self.cached

        self.size = size
        self.color = color

        if color[3] == 255:
            surf = pygame.Surface(size, 0, renpy.game.interface.display.window)
        else:
            surf = pygame.Surface(size, 0,
                                  renpy.game.interface.display.sample_surface)

        surf.fill(color)
        
        self.cached = surf
        return surf

solid_cache = SolidCache()

## One thing to realize when considering the safety of this is that
## if any widget producing a render is redrawn, all instances of that
## render are killed, and so the entire thing is redrawn.

# Renders of a given widget.
widget_renders = { }

# Renders that have been used during the current rendering pass.
new_renders = { }

# Renders that were used on the old rendering pass.
old_renders = { }

# The set of surfaces that are mutable (that is, can change their
# contents.)
mutable_surfaces = { }

def render(widget, width, height, st):
    """
    Renders a widget on the screen.
    """

    if (widget, width, height) in old_renders:
        rv = old_renders[widget, width, height]

        assert widget in rv.widgets

        rv.add_to_new_renders()

        return rv

    rv = widget.render(width, height, st)

    rv.req_width = width
    rv.req_height = height

    rv.widgets.append(widget)
    new_renders[widget, width, height] = rv
    widget_renders.setdefault(widget, []).append(rv)

    return rv

# A list of (when, widget) for redraws.
redraw_queue = [ ]

def process_redraws():
    """
    Processes pending redraws. Returns True if a redraw is needed.
    """

    global redraw_queue
    redraw_queue.sort()

    i = 0
    now = time.time()

    for when, widget in redraw_queue:

        if when > now:
            break

        i += 1

        if widget in widget_renders:
            for r in widget_renders[widget]:
                r.remove_from_old_renders()

    if i == 0:
        return False

    redraw_queue = redraw_queue[i:]
    return True

def redraw(widget, when):
    """
    Call this to queue the redraw of the supplied widget in the
    supplied number of seconds.
    """

    redraw_queue.append((when + time.time(), widget))
    
def render_screen(widget, width, height, st):

    global widget_renders
    global redraw_queue
    global old_renders
    global new_renders
    global mutable_surfaces

    new_renders = { }
    widget_renders = { }
    redraw_queue = [ ]
    mutable_surfaces = { }

    rv = render(widget, width, height, st)

    old_renders = new_renders

    return rv

old_blits = [ ]


def compute_clip(source):
    """
    This computes and returns the clipping rectangle of the source render.
    """

    global old_blits

    new_blits = [ ]
    source.clip_to(pygame.display.get_surface(), 0, 0, new_blits)

    bl0 = old_blits[:]
    bl1 = new_blits[:]

    # Backup blits.
    old_blits = new_blits

    # Changes between the two lists.
    changes = [ ]


    # Set of things in bl1.
    bl1set = { }
    for i in bl1:
        bl1set[i] = True

    # indices.
    i0 = 0
    i1 = 0

    while True:
        # If we're done with either of the lists, break.
        if i0 >= len(bl0) or i1 >= len(bl1):
            break

        # blits
        b0 = bl0[i0]
        b1 = bl1[i1]

        # If the two are the same.
        if b0 == b1:

            # Only add if the surface is mutable.
            if b0[0] in mutable_surfaces:
                changes.append(b0)

            i0 += 1
            i1 += 1
            continue

        # If the surface is only in bl0.
        if b0 not in bl1set:
            changes.append(b0)
            i0 += 1

        # The surface is only in bl1.
        else:
            changes.append(b1)
            i1 += 1
    
    changes.extend(bl0[i0:])
    changes.extend(bl1[i1:])

    if not changes:
        return None

    surf, x0, y0, w, h = changes[0]
    x1 = x0 + w
    y1 = y0 + h

    for surf, x, y, w, h in changes:
        x0 = min(x0, x)
        y0 = min(y0, y)

        x1 = max(x1, x + w)
        y1 = max(y1, y + h)

    return x0, y0, x1 - x0, y1 - y0
    

def screen_blit(source):
    """
    Blits the given render to the screen. Computes the difference
    between the current blit list and old_blits.
    """

    cliprect = compute_clip(source)

    if not cliprect:
        return None

    screen = pygame.display.get_surface()
    screen.set_clip(cliprect)

    source.blit_to(screen, 0, 0)

    screen.set_clip()
    
    return cliprect
    


def mutable_surface(surf):
    """
    Called to indicate that a pygame surface is mutable.
    """

    mutable_surfaces[id(surf)] = True

class Render(object):
    """
    A render represents a static picture of a single widget (perhaps
    including the images of all of the children of that widget). It
    is able to draw that widget to the screen, and contains
    information about when it becomes invalid (and therefore the
    widget can be withdrawn).
    """

    def __init__(self, width, height):
        """
        Creates a new render corresponding to the given widget with
        the specified width and height.

        @param widget: If this render corresponds directly to a
        widget, then this is the widget it corresponds to.
        """

        self.widgets = [ ]

        self.width = width
        self.height = height

        self.req_width = width
        self.req_height = height

        self.parents = [ ]

        self.blittables = [ ]
        self.children = [ ]

        # A pygame surface holding this Render, if one exists.
        self.surface = None
        self.surface_alpha = False

        self.subsurfaces = { }

    def add_to_new_renders(self):

        for w in self.widgets:
            widget_renders.setdefault(w, []).append(self)
            new_renders[w, self.req_width, self.req_height] = self

        for i in self.children:
            i.add_to_new_renders()

    def remove_from_old_renders(self):

        for w in self.widgets:
            # We need to check, since the same widget can appear twice.
            if (w, self.req_width, self.req_height) in old_renders:
                del old_renders[w, self.req_width, self.req_height]

        self.widgets = [ ]

        for p in self.parents:
            p.remove_from_old_renders()

        self.parents = [ ]

    def blit(self, source, (x, y)):
        """
        Adds the source to the list of things that need to be blitted
        to the screen. The source should be either a pygame.Surface,
        or a Render.
        """

        if isinstance(source, Render):
            source.parents.append(self)
            self.children.append(source)
                      
        self.blittables.append((x, y, source))


    def blit_to(self, dest, x, y):
        """
        This blits the children of this Render to dest, which must be
        a pygame.Surface. The x and y parameters are the location of
        the upper-left hand corner of this surface, relative to the
        destination surface.
        """

        for xo, yo, source in self.blittables:

            if isinstance(source, pygame.Surface):
                dest.blit(source, (x + xo, y + yo))
            else:
                source.blit_to(dest, x + xo, y + yo)

    def clip_to(self, dest, x, y, blits):
        """
        This fills in blits with (id(surf), x, y, w, h) tuples.
        """

        for xo, yo, source in self.blittables:

            if isinstance(source, pygame.Surface):
                blits.append((id(source), x + xo, y + yo) + source.get_size())
            else:
                source.clip_to(dest, x + xo, y + yo, blits)

    def fill(self, color):
        """
        Fake a pygame.Surface.fill()
        """

        surf = solid_cache.create((self.width, self.height), color)
        self.blit(surf, (0,0))

    def get_size(self):
        """
        Returns the size of this Render, a mostly ficticious value
        that's taken from the inputs to the constructor. (As in, we
        don't clip to this size.)
        """

        return self.width, self.height
                
    def pygame_surface(self, alpha=True):
        """
        Returns a pygame surface constructed from this Render. This
        may return a cached surface, if one already has been rendered
        (so you probably shouldn't change the output of this much).
        """

        if self.surface and self.surface_alpha == alpha:
            return self.surface

        if alpha:
            sample = renpy.game.interface.display.sample_surface
        else:
            sample = renpy.game.interface.display.window
        
        rv = pygame.Surface((self.width, self.height), 0, sample)

        self.blit_to(rv, 0, 0)

        self.surface = rv
        self.surface_alpha = alpha

        return rv

    def subsurface(self, pos):
        """
        Returns a subsurface of this render.
        """

        if pos in self.subsurfaces:
            return self.subsurfaces[pos]

        x, y, width, height = pos

        if x > self.width or y > self.height:
            return Render(0, 0)

        width = min(self.width - x, width)
        height = min(self.height - y, height)

        rv = Render(width, height)

        for xo, yo, source in self.blittables:

            # ulx, uly -- the coordinates of the upper-left hand corner of
            # the image, relative to the subsurface.

            ulx = xo - x
            uly = yo - y

            # ox, oy -- the offsets that the source will be blitted at.
            # sx, sy -- the offset within the subsurface at which we begin.

            if ulx < 0:
                ox = 0
                sx = -ulx
            else:
                ox = ulx
                sx = 0

            if uly < 0:
                oy = 0
                sy = -uly
            else:
                oy = uly
                sy = 0
            
            sw, sh = source.get_size()

            if sw - ox <= 0:
                continue
            if sh - oy <= 0:
                continue

            sw = min(sw - sx - ox, width)
            sh = min(sh - sy - oy, height)

            rv.blit(source.subsurface((sx, sy, sw, sh)),
                    (ox, oy))


        self.subsurfaces[pos] = rv
        return rv

    def depends_on(self, render):
        """
        Used to indicate that this render depends on another
        render. Useful, for example, if we use pygame_surface to make
        a surface, and then blit that surface into another render.
        """
        
        render.parents.append(self)
