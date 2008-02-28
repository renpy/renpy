# Copyright 2004-2008 PyTom <pytom@bishoujo.us>
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

# Render lifespan.

# A render is alive when it is first created. It stays alive on subsequent
# styles if it is not killed and it is used. It can be killed either
# due to lack of use by the end of a cycle or because it was killed between
# cycles due to a timeout.

try:
    set()
except:
    from sets import Set as set

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
            surf = pygame.Surface(size, 0,
                                  renpy.game.interface.display.window)
        else:
            surf = pygame.Surface(size, 0,
                                  renpy.game.interface.display.sample_surface)

        mutated_surface(surf)

        surf.fill(color)
        
        self.cached = surf
        return surf

solid_cache = SolidCache()

## One thing to realize when considering the safety of this is that
## if any widget producing a render is redrawn, all instances of that
## render are killed, and so the entire thing is redrawn.

# Renders that have been used during the current rendering pass.
new_renders = { }

# Renders that were used on the old rendering pass.
old_renders = { }

# The set of surfaces that are mutated (that is, can change their
# contents.)
mutated_surfaces = { }

def free_memory():
    """
    Frees up some memory.
    """

    global new_renders
    global old_renders
    global mutated_surfaces
    global old_blits
    global old_forced
    
    new_renders = { }
    old_renders = { }
    mutated_surfaces = { }
    old_blits = [ ]
    old_forced = [ ]
    
    
def render(d, width, height, st, at):
    """
    Renders a widget on the screen.
    """

    style = d.style
    xmaximum = style.xmaximum
    ymaximum = style.ymaximum
    
    if xmaximum is not None:
        if isinstance(xmaximum, float):
            width = int(width * xmaximum)
        else:
            width = min(xmaximum, width)

    if ymaximum is not None:
        if isinstance(ymaximum, float):
            width = int(height * ymaximum)
        else:
            height = min(ymaximum, height)

    if (d, width, height) in old_renders:
        rv = old_renders[d, width, height]

        # assert (widget, width, height) in rv.render_of
        # assert not rv.dead

        rv.keep_alive()

        return rv

    rv = d.render(width, height, st, at)

    if style.clipping:
        rv = rv.subsurface((0, 0, width, height), focus=True)
        
    # rv.clipped = widget.style.clipping

    rv.render_of.append((d, width, height))

    old_renders[d, width, height] = rv
    new_renders[d, width, height] = rv

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
    dead_widgets = set()
    now = renpy.display.core.get_time()

    for when, widget in redraw_queue:

        if when > now:
            break

        i += 1

        dead_widgets.add(widget)

    if not dead_widgets:
        return False

    redraw_queue = redraw_queue[i:]

    for (widget, width, height), render in old_renders.items():
        if widget in dead_widgets:
            render.kill()
    
    return True

def redraw_time():
    """
    Returns the time at which a redraw is scheduled. This
    should be called only after process_redraws, so that
    the list is sorted.
    """

    if redraw_queue:
        return redraw_queue[0][0]
    else:
        return None
        

def redraw(widget, when):
    """
    Call this to queue the redraw of the supplied widget in the
    supplied number of seconds.
    """

    if not renpy.game.interface:
        return
    
    redraw_queue.append((when + renpy.game.interface.frame_time, widget))
    
def render_screen(widget, width, height, st):

    global redraw_queue
    global old_renders
    global new_renders
    global mutated_surfaces

    mutated_surfaces = { }

    rv = render(widget, width, height, st, st)

    # Renders that are in the old set but not the new one die here.
    old_render_set = set(old_renders.itervalues())
    new_render_set = set(new_renders.itervalues())

    dead_render_set = old_render_set - new_render_set

    for r in dead_render_set:
        render_of = r.render_of
        r.kill()
        assert not rv.dead, render_of

    old_renders.update(new_renders)
    new_renders.clear()

    # Figure out which widgets are still alive.
    live_widgets = set()
    for widget, height, width in old_renders:
        live_widgets.add(widget)

    # Filter dead widgets from the redraw queue.
    redraw_queue = [ (when, widget) for when, widget in redraw_queue if
                     widget in live_widgets or widget is None]
    
    return rv

old_blits = [ ]
old_forced = [ ]

def compute_clip(source):
    """
    This computes and returns the clipping rectangle of the source render.
    """

    global old_blits
    global old_forced

    new_blits = [ ]
    forced = [ ]

    # source.clip_to(0, 0, new_blits, forced)
    clipsurf = ClipSurface((0, 0, renpy.config.screen_width, renpy.config.screen_height),
                           new_blits, forced)

    source.blit_to(clipsurf, 0, 0)

    bl0 = old_blits
    bl1 = new_blits

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

            # Only add if the surface is mutated.
            if b0[0] in mutated_surfaces:
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

    if not changes and not forced and not old_forced:
        return None

    sw = renpy.config.screen_width
    sh = renpy.config.screen_height
    sa = sw * sh # screen area

    # (size, x0, y0, x1, y1) tuples.
    sized = [ ]

    old_old_forced = old_forced
    old_forced = forced

    for surf, srcx, srcy, x0, y0, w, h in changes:

        if x0 < 0:
            x0 = 0
        if y0 < 0:
            y0 = 0
        if w > sw - x0:
            w = sw - x0
        if h > sh - y0:
            h = sh - y0

        if w * h >= sa:
            return (0, 0, sw, sh), [ (0, 0, sw, sh) ]
            
        sized.append((w * h, x0, y0, x0 + w, y0 + h))

    for x0, y0, w, h in forced + old_old_forced:

        if x0 < 0:
            x0 = 0
        if y0 < 0:
            y0 = 0
        if w > sw - x0:
            w = sw - x0
        if h > sh - y0:
            h = sh - y0

        if w * h >= sa:
            return (0, 0, sw, sh), [ (0, 0, sw, sh) ]
            
        sized.append((w * h, x0, y0, x0 + w, y0 + h))

        
    sized.sort()

    # The set of non-contained updates. (x0, y0, x1, y1) tuples. 
    noncont = [ ]

    # The sum of areas in noncont.
    nca = 0

    # Pick the largest area, merge with all overlapping smaller areas, repeat
    # until no merge possible.
    while sized:
        area, x0, y0, x1, y1 = sized.pop()
        
        merged = False
            
        if nca + area >= sa:
            return (0, 0, sw, sh), [ (0, 0, sw, sh) ]

        newsized = [ ]
            
        for t in sized:
            iarea, ix0, iy0, ix1, iy1 = t 

            if (x0 <= ix0 <= x1 or x0 <= ix1 <= x1) and \
               (y0 <= iy0 <= y1 or y0 <= iy1 <= y1):

                merged = True
                x0 = min(x0, ix0)
                x1 = max(x1, ix1)
                y0 = min(y0, iy0)
                y1 = max(y1, iy1)

                area = (x1 - x0) * (y1 - y0)

                continue

            newsized.append(t)

        sized = newsized
        
        if not merged:
            noncont.append((x0, y0, x1, y1))
            nca += area
            continue

        sized.append((area, x0, y0, x1, y1))

    x0, y0, x1, y1 = noncont[0]

    # A list of (x, y, w, h) tuples for each update.
    updates = [ ]

    for ix0, iy0, ix1, iy1 in noncont:
        x0 = min(x0, ix0)
        y0 = min(y0, iy0)
        x1 = max(x1, ix1)
        y1 = max(y1, iy1)

        updates.append((ix0, iy0, ix1 - ix0, iy1 - iy0))

    return (x0, y0, x1 - x0, y1 - y0), updates
    

# This is used to compute clipping, and also to see if rgwew ua =
class ClipSurface(object):

    def __init__(self, (x, y, w, h), blits, forced, surfid=id):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.blits = blits
        self.forced = forced

        # Function that transforms the surface.
        self.surfid = surfid
        
    def set_clip(self, rect):
        return 

    def get_clip(self):
        return (0, 0, self.w, self.h)

    def get_size(self):
        return (self.w, self.h)

    def blit(self, surf, (xo, yo)):

        if xo < 0:
            srcx = -xo
            xo = 0
        else:
            srcx = 0

        if yo < 0:
            srcy = -yo
            yo = 0
        else:
            srcy = 0

        sw, sh = surf.get_size()

        bw = min(self.w - xo, sw - srcx)
        bh = min(self.h - yo, sh - srcy)

        if bw <= 0 or bh <= 0:
            return

        self.blits.append((self.surfid(surf), srcx, srcy, xo + self.x, yo + self.y, bw, bh))

    def force(self):
        self.forced.append((self.x, self.y, self.w, self.h))

    def subsurface(self, (x, y, w, h)):
        return ClipSurface((self.x + x, self.y + y, w, h),
                           self.blits, self.forced, self.surfid)


# This takes two rectangles: A "source" rectangle and a "clipping" 
# rectangle. It returns two tuples: the (xo, yo) of the source rectangle
# relative to the upper left of the clipping rectangle. And the (x, y, w, h)
# of the part of the source rectangle that is shown within the clipping
# rectangle.
def compute_subrect(source, clipping):
    sx, sy, sw, sh = source
    cx, cy, cw, ch = clipping

    # The coordinates of the upper-left corner of the source
    # rectangle inside the clipping rectange.
    ulx = sx - cx
    uly = sy - cy

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

    if ox > cw or oy > ch:
        return (0, 0), (0, 0, 0, 0)

    sw = min(sw - sx, cw - ox)
    sh = min(sh - sy, ch - oy)

    return (ox, oy), (sx, sy, sw, sh)
    
def screen_blit(source, full=False, xoffset=0, yoffset=0):
    """
    Blits the given render to the screen. Computes the difference
    between the current blit list and old_blits.
    """

    screen = pygame.display.get_surface()

    clip = compute_clip(source)

    if full:
        clip = (0, 0) + screen.get_size(), [ (0, 0) + screen.get_size() ]

    if not clip:
        return [ ]

    cliprect, updates = clip

    screen = pygame.display.get_surface()

    if xoffset:
        sw = renpy.config.screen_width
        sh = renpy.config.screen_height
        
        x, y, w, h = cliprect
        cliprect = (x + xoffset, y + yoffset, min(w, sw - x), h)
        updates = [ (x + xoffset, y + yoffset, min(w, sw - x), h) for x, y, w, h in updates ]

    old_clip = screen.get_clip()
    screen.set_clip(cliprect)
    source.blit_to(screen, xoffset, yoffset)
    screen.set_clip(old_clip)

    return updates
    


def mutated_surface(surf):
    """
    Called to indicate that a pygame surface has been mutated. This also
    should be called each time a new pygame surface is created.
    """

    mutated_surfaces[id(surf)] = True


class Render(object):
    """
    A render represents a static picture of a single widget (perhaps
    including the images of all of the children of that widget). It
    is able to draw that widget to the screen, and contains
    information about when it becomes invalid (and therefore the
    widget can be withdrawn).
    """

    def __init__(self, width, height, draw_func=None, opaque=False, layer_name=None):
        """
        Creates a new render corresponding to the given widget with
        the specified width and height.
        """

        # Just for safety's sake.
        self.dead = False

        # A list of widget, width, height, corresponding to the
        # entries in old_renders that this render is in.
        self.render_of = [ ]

        # The width and height of this render.
        self.width = width
        self.height = height

        # The parents of this render.
        self.parents = [ ]

        self.blittables = [ ]
        self.children = [ ]
        self.depends = [ ]

        # A list of child renders that were marked important when we
        # blitted them.
        self.main_child_renders = [ ]
        
        # A pygame surface holding this Render, if one exists.
        self.surface = None
        self.surface_alpha = None
        
        self.subsurfaces = { }

        # The list of focusable widgets collected from this render
        # and the children of this render. A list of (widget, arg, x, y, w, h,)
        self.focuses = [ ]

        self.draw_func = draw_func

        # Is this render fullscreen? 
        self.fullscreen = { }

        # Is this render clipped?
        self.clipped = False

        # Is this render opaque? (Only needs to be set for surfaces with draw_func.)
        self.opaque = opaque

        # The name of this layer, if this render corresponds to a layer.
        self.layer_name = layer_name
        
    
    # def __del__(self):
    #     Render.renders -= 1
    #     print "Render del", Render.renders, Render.liverenders, self

    def keep_alive(self):

        new = False

        if self.render_of and self.render_of[0] in new_renders:
            return

        # wwh == widget, width, height
        for wwh in self.render_of:
            new_renders[wwh] = self
            
        for i in self.children:
            i.keep_alive()

        for i in self.depends:
            i.keep_alive()
                

    def kill(self):
        """
        Calling this marks the render and all of its parents dead. It also
        unlinks it from the tree, readying it for reclamation.
        """

        if self.dead:
            return 

        self.dead = True

        for widget, width, height in self.render_of:

            if (widget, width, height) in old_renders:
                del old_renders[widget, width, height]

            if (widget, width, height) in new_renders:
                del new_renders[widget, width, height]

        parents = self.parents[:]
        children = self.children[:]
        depends = self.depends[:]

        for p in parents:
            p.kill()

        for c in children:
            while self in c.parents:
                c.parents.remove(self)

        for c in depends:
            while self in c.parents:
                c.parents.remove(self)

        # assert not self.parents

        # for p in parents:
        #     # assert p.dead

        self.main_child_renders = [ ]
        self.children = [ ]
        self.depends = [ ]

        # Removes cycles.
        self.render_of = [ ]
        self.focuses = [ ]

    def blit(self, source, (xo, yo), focus=True, main=True):
        """
        Adds the source to the list of things that need to be blitted
        to the screen. The source should be either a pygame.Surface,
        or a Render.
        """


        if isinstance(source, Render):
            # assert not source.dead

            source.parents.append(self)
            self.children.append(source)

            if main:
                self.main_child_renders.append((xo, yo, source))

            if focus and xo == 0 and yo == 0:
                self.focuses.extend(source.focuses)
            elif focus:

                for f in source.focuses:
                    nf = f.copy()
                    
                    if nf.x is not None:
                        nf.x += xo
                        nf.y += yo

                    if nf.mx is not None:
                        nf.mx += xo
                        nf.my += yo

                    self.focuses.append(nf)
                                      
        self.blittables.append((xo, yo, source))

    def blit_to(self, dest, x, y):
        """
        This blits the children of this Render to dest, which must be
        a pygame.Surface. The x and y parameters are the location of
        the upper-left hand corner of this surface, relative to the
        destination surface.
        """

        worklist = [ (self, x, y) ]

        destw, desth = dest_size = dest.get_size()
        
        winblit = dest is renpy.game.interface.display.window
        cacheget = renpy.display.im.rle_cache.get # bound method.

        while worklist:

            what, x, y = worklist.pop()

            if what.__class__ is pygame.Surface:

                if winblit:
                    what = cacheget(id(what), what)

                dest.blit(what, (x, y))
                continue

            
            if what.draw_func:

                if x >= 0:
                    newx = 0
                    subx = x
                else:
                    newx = x
                    subx = 0

                if y >= 0:
                    newy = 0
                    suby = y
                else:
                    newy = y
                    suby = 0

                if subx >= destw or suby >= desth:
                    return

                # newx and newy are the offset of this render relative to the
                # subsurface. They can only be negative or 0, as otherwise we
                # would make a smaller subsurface.

                subw = min(destw - subx, what.width + newx) 
                subh = min(desth - suby, what.height + newy)

                if subw <= 0 or subh <= 0:
                    return

                newdest = dest.subsurface((subx, suby, subw, subh))
                
                if newdest.__class__ is ClipSurface:
                    newdest.force()
                else:
                    what.draw_func(newdest, newx, newy)

                continue

            fullscreen = 0
            i = 0

            if x <= 0 and y <= 0:
            
                for xo, yo, source in what.blittables:
                    if is_fullscreen(source, x + xo, y + yo, dest_size):
                       fullscreen = i
                    i += 1
                    
            wll = len(worklist)
            
            for xo, yo, source in what.blittables[fullscreen:]:
                worklist.insert(wll, (source, x + xo, y + yo))

                
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

        # Check to see if we have a single surface, bigger then the render.
        forced = [ ]
        blits = [ ]

        clipsurf = ClipSurface((0, 0, self.width, self.height),
                               blits, forced, lambda x : x)

        self.blit_to(clipsurf, 0, 0)
        
        if len(blits) == 1 and not forced:
            surf, sx, sy, x, y, w, h = blits[0]
            if x <= 0 and y <= 0 and w + x >= self.width and h + y >= self.height:
                if surf.get_masks()[3]:
                    self.surface = surf.subsurface((sx - x, sy - y, self.width, self.height))
                    return self.surface
                    
        # Otherwise, do things the hard way.

        if alpha:
            sample = renpy.game.interface.display.sample_surface
        else:
            sample = renpy.game.interface.display.window

        rv = pygame.Surface((self.width, self.height), 0, sample)

        self.blit_to(rv, 0, 0)

        self.surface = rv
        self.surface_alpha = rv
        
        mutated_surface(rv)

        return rv

    def subsurface(self, pos, focus=False):
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

        rv.children.append(self)

        if focus:

            for f in self.focuses:

                nf = f.copy()

                if nf.x is not None:
                    (nf.x, nf.y), (ignored1, ignored2, nf.w, nf.h) = compute_subrect(
                        (nf.x, nf.y, nf.w, nf.h),
                        (x, y, width, height))

                    if nf.w <= 0 or nf.h <= 0:
                        continue

                if nf.mx is not None:
                    
                    (nf.mx, nf.my), (mcx, mcy, mcw, mch) = compute_subrect(
                        (nf.mx, nf.my) + nf.mask.get_size(),
                        (x, y, width, height))

                    if mcw <= 0 or mch <= 0:
                        continue

                    nf.mask = nf.mask.subsurface((mcx, mcy, mcw, mch))
                    
                rv.focuses.append(nf)
                
        for xo, yo, source in self.blittables:

            (xo, yo), (sx, sy, sw, sh) = compute_subrect(
                (xo, yo) + source.get_size(),
                (x, y, width, height))
            
            if sw <= 0 or sh <= 0:
                continue

            subsurf = source.subsurface((sx, sy, sw, sh))

            if isinstance(subsurf, pygame.Surface):
                mutated_surface(subsurf) 
            
            rv.blit(subsurf, (xo, yo))


        self.subsurfaces[pos] = rv
        rv.depends_on(self)
        
        return rv

    def depends_on(self, child):
        """
        Used to indicate that this render depends on another
        render. Useful, for example, if we use pygame_surface to make
        a surface, and then blit that surface into another render.
        """

        # assert not child.dead

        self.depends.append(child)
        child.parents.append(self)

    def add_focus(self, widget, arg=None, x=0, y=0, w=None, h=None, mx=None, my=None, mask=None):
        """
        This is called to indicate a region of the screen that can be
        focused.

        @param widget: The widget that will be focused.
        @param arg: A focus argument, which can be checked by the widget.

        The rest of the parameters are a rectangle giving the portion of
        this region corresponding to the focus. If they are all None, than
        this focus is assumed to be the singular full-screen focus.
        """

        if x is not None:
            if w is None:
                w = self.width

            if h is None:
                h = self.height

        if mask is not None and mask is not self:
            self.depends_on(mask)
                
        self.focuses.append(renpy.display.focus.Focus(widget, arg, x, y, w, h, mx, my, mask))

    # Determines if the pixel at x, y is opaque or not.
    def is_opaque(self, x, y):
        if x >= self.width or y >= self.height:
            return False
        
        for xo, yo, source in self.blittables:
            xx = x - xo
            yy = y - yo

            if xx < 0 or yy < 0:
                continue

            if isinstance(source, pygame.Surface):
                ww, hh = source.get_size()
                if xx >= ww or yy >= hh:
                    continue

                if not source.get_masks()[3] or source.get_at((xx, yy))[3]:
                    return True
            else:
                if source.is_opaque(xx, yy):
                    return True

        return False
                
    def main_displayables_at_point(self, x, y, layers, depth=None):
        
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return [ ]

        rv = [ ]
        
        if depth is not None:
            for w, width, height in self.render_of:
                rv.append((depth, self.width, self.height, w))

            depth += 1
            
        elif self.layer_name in layers:
            depth = 0

        for xo, yo, child in self.main_child_renders:
            rv.extend(child.main_displayables_at_point(x - xo, y - yo, layers, depth))

        return rv
            
        
# Determine if a surface is fullscreen or not.
def is_fullscreen(surf, x, y, wh):

    w, h = wh
    sw, sh = surf.get_size()

    # Check that this surface is on the screen.
    if (x > 0) or (y > 0) or (sw + x < w) or (sh + y < h):
        return False
        
    if surf.__class__ is pygame.Surface:

        if (surf.get_masks()[3] == 0 and
            (surf.get_alpha() == None or surf.get_alpha() == 255)):
            return True
        else:
            return False

    xywh = (x, y, w, h)

    rv = surf.fullscreen.get(xywh, None)
    if rv is not None:
        return rv

    # Clipping can stop its children from being fullscreen.

    if surf.opaque:
        surf.fullscreen[xywh] = True
        return True

    for xo, yo, source in surf.blittables:
        if is_fullscreen(source, x + xo, y + yo, wh):
            surf.fullscreen[xywh] = True
            return True

    surf.fullscreen[xywh] = False
    return False

