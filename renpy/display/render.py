# Copyright 2004-2010 PyTom <pytom@bishoujo.us>
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

import collections
import pygame
import threading
import renpy


# We grab the blit lock each time it is necessary to blit
# something. This allows call to the pygame.transform functions to
# disable blitting, should it prove necessary.
blit_lock = threading.Condition()

# The number of living renders. (That is, the number that have been
# constructed, but not had kill() called.
render_count = 0

# This is a dictionary containing all the renders that we know of. It's a
# map from displayable to dictionaries containing the render of that
# displayable.
render_cache = collections.defaultdict(dict)

# The queue of redraws. A list of (time, displayable) pairs.
redraw_queue = [ ]

# The render returned from render_screen.
screen_render = None

# The previous render returned from render_screen. We keep this around
# so that we can kill it when we render the next screen.
old_screen_render = None

# Two sets of renders that have no parents, for the new and old frames.
# Renders get added to these sets, and then removed when added to something.
# If they're in old_parentless at the end of a render, they get killed. 
new_parentless = set()
old_parentless = set()

def free_memory():
    """
    Frees memory used by the render system.
    """

    global screen_render
    global old_parentless
    global new_parentless

    if screen_render:
        screen_render.refcount -= 1
        screen_render.kill()
        screen_render = None

    for i in new_parentless:
        i.kill()

    for i in old_parentless:
        i.kill()

    old_parentless = set()
    new_parentless = set()
        
    render_cache.clear()


def check_at_shutdown():
    """
    This is called at shutdown time to check that everything went okay.
    The big thing it checks for is memory leaks.
    """
    
    if not renpy.config.developer:
        return

    free_memory()

    if render_count != 0:
        raise Exception("Render count is %d at shutdown. This probably indicates a memory leak bug in Ren'Py." % render_count)

    
def render(d, width, height, st, at):
    """
    Causes the displayable `d` to be rendered in an area of size
    width, height.  st and at are the times of this render, but once
    rendered the Render will remain cached until the displayable needs
    to be redrawn.
    """

    ft = renpy.game.interface.frame_time 
    
    orig_wh = (width, height, ft-st, ft-at)
    rv = render_cache[d].get(orig_wh, None)
    if rv is not None:
        return rv

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

    if width < 0:
        width = 0
    if height < 0:
        height = 0
            
    wh = (width, height, ft-st, ft-at)
            
    rv = render_cache[d].get(wh, None)
    if rv is not None:
        return rv
    
    rv = d.render(width, height, st, at)
    rv.render_of.append(d)

    if style.clipping:
        rv = rv.subsurface((0, 0, rv.width, rv.height), focus=True)
        rv.render_of.append(d)

    render_cache[d][wh] = rv
    render_cache[d][orig_wh] = rv

    old_parentless.discard(rv)
    new_parentless.add(rv)

    return rv


# This is true if something has been invalidated, and a redraw needs
# to occur. It's automatically cleared to False at the end of each
# redraw.
invalidated = False

def invalidate(d):
    """
    Removes d from the render cache. If we're not in a redraw, triggers
    a redraw to start.
    """

    global invalidated
    
    if d in render_cache:
        for v in render_cache[d].values():
            v.kill_cache()

        invalidated = True

        
def process_redraws():
    """
    Called to determine if any redraws are pending. Returns true if we
    need to redraw the screen now, false otherwise.
    """

    global redraw_queue
    
    redraw_queue.sort()

    now = renpy.display.core.get_time()
    rv = invalidated

    new_redraw_queue = [ ]
    seen = set()

    for t in redraw_queue:
        when, d = t

        if d in seen:
            continue

        seen.add(d)

        if d not in render_cache:
            continue
        
        if when <= now:
            # Remove this displayable and all its parents from the
            # render cache. But don't kill them yet, as that will kill the
            # children that we want to reuse.

            for v in render_cache[d].values():
                v.kill_cache()

            rv = True

        else:
            new_redraw_queue.append(t)

        redraw_queue = new_redraw_queue

        
    return rv


def redraw_time():
    """
    Returns the time at which the next redraw is scheduled.
    """

    if redraw_queue:
        return redraw_queue[0][0]

    return None
    

def redraw(d, when):
    """
    Called to cause `d` to be redrawn in `when` seconds.
    """

    if not renpy.game.interface:
        return

    redraw_queue.append((when + renpy.game.interface.frame_time, d))
    

class Matrix2D(object):
    """
    This represents a 2d matrix that can be used to transform
    points and things like that.
    """

    def __init__(self, xdx, xdy, ydx, ydy):
        self.xdx = xdx
        self.xdy = xdy
        self.ydx = ydx
        self.ydy = ydy

    def transform(self, x, y):
        return (x * self.xdx + y * self.xdy), (x * self.ydx + y * self.ydy)

    def __mul__(self, other):
        return Matrix2D(
            other.xdx * self.xdx + other.xdy * self.ydx,
            other.xdx * self.xdy + other.xdy * self.ydy,
            other.ydx * self.xdx + other.ydy * self.ydx,
            other.ydx * self.xdy + other.ydy * self.ydy)

IDENTITY = Matrix2D(1, 0, 0, 1)

def kill_old_screen():
    """
    Kills the old screen if it's different from the current screen.
    """

    global old_parentless
    global new_parentless
    global old_screen_render
    
    if old_screen_render is None:
        return

    old_screen_render.refcount -= 1
    
    if old_screen_render is screen_render:
        return
        
    old_screen_render.kill()
    old_screen_render = None

    for i in old_parentless:
        i.kill()

    old_parentless = new_parentless
    new_parentless = set()

    
def take_focuses(focuses):
    """
    Adds a list of rectangular focus regions to the focuses list.
    """

    screen_render.take_focuses(
        0, 0, screen_render.width, screen_render.height,
        IDENTITY, 0, 0, focuses)
    
def focus_at_point(x, y):
    """
    Returns a focus object corresponding to the uppermost displayable
    at point, or None if nothing focusable is at point.
    """
        
    cf = screen_render.focus_at_point(x, y)
    if cf is None:
        return None
    else:
        d, arg = cf
        return renpy.display.focus.Focus(d, arg, None, None, None, None)

    
def mutated_surface(surf):
    """
    Called to indicate that the given surface has changed. 
    """

    renpy.display.draw.mutated_surface(surf)


def render_screen(root, width, height):
    """
    Renders `root` (a displayable) as the root of a screen with the given
    `width` and `height`.
    """

    global old_screen_render
    global screen_render
    global invalidated
    
    old_screen_render = screen_render
    
    rv = render(root, width, height, 0, 0)
    screen_render = rv
    screen_render.refcount += 1
    
    invalidated = False

    rv.is_opaque()
    
    return rv

# Possible operations that can be done as part of a render.
BLIT = 0
DISSOLVE = 1
IMAGEDISSOLVE = 2
PIXELLATE = 3

class Render(object):
    
    def __init__(self, width, height, draw_func=None, layer_name=None, opaque=None):
        """
        Creates a new render corresponding to the given widget with
        the specified width and height.

        If `layer_name` is given, then this render corresponds to a
        layer.
        """

        global render_count
        render_count += 1

        self.width = width
        self.height = height

        self.layer_name = layer_name

        # A list of (surface/render, xoffset, yoffset, focus, main) tuples, ordered from
        # back to front.
        self.children = [ ]

        # A list of Renders that are the parents of this Render. (We need
        # to kill these when this Render is redrawn.)
        self.parents = set()

        # A list of additional surfaces that we depend on. (Like children)
        self.depends_on_set = set()
        
        # A list of surfaces that depend on us.
        self.depends_on_us = set()

        # len(self.parents) + len(self.depends_on_us)
        self.refcount = 0

        # The operation we're performing. (BLIT, DISSOLVE, OR IMAGE_DISSOLVE)
        self.operation = BLIT

        # The fraction of the operation that is complete.
        self.operation_complete = 0.0

        # Should the dissolve operations preserve alpha?
        self.operation_alpha = False
        
        # The parameter to the operation. 
        self.operation_parameter = 0
        

        # Forward is used to transform from screen coordinates to child
        # coordinates.
        # Reverse is used to transform from child coordinates to screen
        # coordinates.
        # 
        # For performance reasons, these aren't used to transform the
        # x and y offsets found in self.children. Those offsets should
        # be of the (0, 0) point in the child coordinate space.
        self.forward = None
        self.reverse = None

        # This is used to adjust the alpha of children of this render.
        self.alpha = 1
        
        # A list of focus regions in this displayable.
        self.focuses = [ ]

        # Other renders that we should pass focus onto.
        self.pass_focuses = [ ]
        
        # The displayable(s) that this is a render of. (Set by render)
        self.render_of = [ ]

        # Is has this render been removed from the cache?
        self.cache_killed = False
        
        # Is this render dead?
        self.dead = False

        # If set, this is a function that's called to draw this render
        # instead of the default.
        self.draw_func = draw_func

        # Is this displayable opaque? (May be set on init, or later on
        # if we have opaque children.) This may be True, False, or None
        # to indicate we don't know yet.
        self.opaque = opaque

        # A list of our visible children. (That is, children above and
        # including our uppermost opaque child.) If nothing is opaque,
        # includes all children.
        self.visible_children = self.children
        
        # Should children be clipped to a rectangle?
        self.clipping = False

        # Caches of this render, rendered as a surface.
        self.surface = None
        self.alpha_surface = None

        
    def __repr__(self):

        if self.dead:
            dead = "dead"
        else:
            dead = "live"
        
        return "<Render %x %s of %r>" % (id(self), dead, self.render_of)

        
    def blit(self, source, (xo, yo), focus=True, main=True, index=None):
        """
        Blits `source` (a Render or Surface) to this Render, offset by
        xo and yo.

        If `focus` is true, then focuses are added from the child to the
        parent.

        This will only blit on integer pixel boundaries.
        """

        if source is self:
            raise Exception("Blitting to self.")
        
        xo = int(xo)
        yo = int(yo)

        if index is None:
            self.children.append((source, xo, yo, focus, main))
        else:
            self.children.insert(index, (source, xo, yo, focus, main))
            
            
        if isinstance(source, Render):
            source.parents.add(self)
            source.refcount += 1

        new_parentless.discard(source)

        
    def subpixel_blit(self, source, (xo, yo), focus=True, main=True, index=None):
        """
        Blits `source` (a Render or Surface) to this Render, offset by
        xo and yo.

        If `focus` is true, then focuses are added from the child to the
        parent.

        This blits at fractional pixel boundaries.
        """

        xo = float(xo)
        yo = float(yo)
        
        if index is None:
            self.children.append((source, xo, yo, focus, main))
        else:
            self.children.insert(index, (source, xo, yo, focus, main))
                        
        if isinstance(source, Render):
            source.parents.add(self)
            source.refcount += 1

        new_parentless.discard(source)

        
    def get_size(self):
        """
        Returns the size of this Render, a mostly ficticious value
        that's taken from the inputs to the constructor. (As in, we
        don't clip to this size.)
        """

        return self.width, self.height

    
    def render_to_texture(self, alpha=True):
        """
        Returns a texture constructed from this render. This may return
        a cached textue, if one has already been rendered.

        `alpha` is a hint that controls if the surface should have
        alpha or not.
        """

        if alpha:
            if self.alpha_surface is not None:
                return self.alpha_surface
        else:
            if self.surface is not None:
                return self.surface
            
        rv = None

        # If we can, reuse a child's texture.
        if not self.forward and len(self.children) == 1:
            child, x, y, focus, main = self.children[0]
            cw, ch = child.get_size()
            if x <= 0 and y <= 0 and cw + x >= self.width and ch + y >= self.height:
                # Our single child overlaps us.
                if isinstance(child, Render):
                    child = child.render_to_texture(alpha)

                if x != 0 or y != 0 or cw != self.width or ch != self.height:
                    rv = child.subsurface((-x, -y, self.width, self.height))
                else:
                    rv = child

        # Otherwise, render to a texture.
        if rv is None:

            # Compute opacity information, as necessary.
            self.is_opaque()

            rv = renpy.display.draw.render_to_texture(self, alpha)


        # Stash and return the surface.
        if alpha:
            self.alpha_surface = rv
        else:
            self.surface = rv
            
        return rv

    
    pygame_surface = render_to_texture

    
    def subsurface(self, rect, focus=False):
        """
        Returns a subsurface of this render. If `focus` is true, then
        the focuses are copied from this render to the child.
        """

        x, y, w, h = rect
        rv = Render(w, h)
        rv.clipping = True
        rv.blit(self, (-x, -y), focus=focus)

        return rv
        
    def depends_on(self, source, focus=False):
        """
        Used to indicate that this render depends on another
        render. Useful, for example, if we use pygame_surface to make
        a surface, and then blit that surface into another render.
        """

        if source is self:
            raise Exception("Render depends on itself.")
        
        if source not in self.depends_on_set:
            self.depends_on_set.add(source)
            source.depends_on_us.add(self)
            source.refcount += 1

        if focus:
            self.pass_focuses.append(source)

        new_parentless.discard(source)

        
    def kill_cache(self):
        """
        Removes this render and its transitive parents from the cache.
        """

        if self.cache_killed:
            return

        self.cache_killed = True

        for i in self.parents:
            i.kill_cache()
                
        for i in self.depends_on_us:
            i.kill_cache()

        for ro in self.render_of:
            cache = render_cache[ro]
            for k, v in cache.items():
                if v is self:
                    del cache[k]
                    
            if not cache:
                del render_cache[ro]
            
    def kill(self):
        """
        Removes this Render from its children, and kills those children if
        doing so causes their refcount to fall to 0.
        """

        if self.dead:
            return

        if self.refcount > 0:
            return
        
        self.dead = True
            
        global render_count
        render_count -= 1

        for c, xo, yo, focus, main in self.children:

            if not isinstance(c, Render):
                continue
            
            # We could be added to c.parents twice, but we'll only show
            # up once. (But twice in the refcount.) 
            c.parents.discard(self)
            c.refcount -= 1
            
            if c.refcount == 0:
                c.kill()
                
        for c in self.depends_on_set:
            c.depends_on_us.remove(self)
            c.refcount -= 1

            if c.refcount == 0:
                c.kill()

        self.kill_cache()
                
    def add_focus(self, d, arg=None, x=0, y=0, w=None, h=None, mx=None, my=None, mask=None):
        """
        This is called to indicate a region of the screen that can be
        focused.

        `d` - the displayable that is being focused.
        `arg` - an argument.

        The rest of the parameters are a rectangle giving the portion of
        this region corresponding to the focus. If they are all None, than
        this focus is assumed to be the singular full-screen focus.
        """

        if mask is not None and mask is not self:
            self.depends_on(mask)
            
        self.focuses.append((d, arg, x, y, w, h, mx, my, mask))

    def take_focuses(self, cminx, cminy, cmaxx, cmaxy, reverse, x, y, focuses):
        """
        This adds to focuses Focus objects corresponding to the focuses
        added to this object and its children, transformed into screen
        coordinates.

        `cminx`, `cminy`, `cmaxx`, `cmaxy` - The clipping rectangle.
        `reverse` - The transform from render to screen coordinates.
        `x`, `y` - The offset of the upper-left corner of the render.
        `focuses` - The list of focuses to add to.
        """
        
        if self.reverse:
            reverse = reverse * self.reverse

        for (d, arg, xo, yo, w, h, mx, my, mask) in self.focuses:

            if xo is None:
                focuses.append(renpy.display.focus.Focus(d, arg, None, None, None, None)) 
                continue
                
            x1, y1 = reverse.transform(xo, yo)
            x2, y2 = reverse.transform(xo + w, yo + h)

            minx = min(x1, x2) + x
            miny = min(y1, y2) + y
            maxx = max(x1, x2) + x
            maxy = max(y1, y2) + y

            minx = max(minx, cminx)
            miny = max(miny, cminy)
            maxx = min(maxx, cmaxx)
            maxy = min(maxy, cmaxy)

            if minx >= maxx or miny >= maxy:
                continue
            
            focuses.append(renpy.display.focus.Focus(d, arg, minx, miny, maxx - minx, maxy - miny)) 

        if self.clipping:
            cminx = max(cminx, x)
            cminy = max(cminy, y)
            cmaxx = min(cmaxx, x + self.width)
            cmaxy = min(cmaxx, x + self.height)

        for child, xo, yo, focus, main in self.children:
            if not focus or not isinstance(child, Render):
                continue

            xo, yo = reverse.transform(xo, yo)
            child.take_focuses(cminx, cminy, cmaxx, cmaxy, reverse, x + xo, y + yo, focuses)

        for child in self.pass_focuses:
            child.take_focuses(cminx, cminy, cmaxx, cmaxy, reverse, x, y, focuses)
        
    def focus_at_point(self, x, y):
        """
        This returns the focus of this object at the given point.
        """

        if self.clipping:
            if x < 0 or x >= self.width or y < 0 or y >= self.height:
                return None
        
        rv = None
        
        for (d, arg, xo, yo, w, h, mx, my, mask) in self.focuses:

            if xo is None:
                continue
            
            elif mx is not None:
                cx = x - mx
                cy = y - my

                if self.forward:
                    cx, cy = self.forward.transform(cx, cy)

                if mask.is_pixel_opaque(cx, cy):
                    rv = d, arg
                    
            elif xo <= x < xo + w and yo <= y < yo + h:
                rv = d, arg
            
        for child, xo, yo, focus, main in self.children:

            if not focus or not isinstance(child, Render):
                continue
            
            cx = x - xo
            cy = y - yo

            if self.forward:
                cx, cy = self.forward.transform(cx, cy)

            cf = child.focus_at_point(cx, cy)
            if cf is not None:
                rv = cf

        for child in self.pass_focuses:
            cf = child.focus_at_point(x, y)
            if cf is not None:
                rv = cf

        return rv
        
            
    def main_displayables_at_point(self, x, y, layers, depth=None):
        """
        Returns the displayable at `x`, `y` on one of the layers in
        the set or list `layers`.
        """

        rv = [ ]

        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return rv

        if depth is not None:
            for d in self.render_of:
                rv.append((depth, self.width, self.height, d))
                depth += 1
        elif self.layer_name in layers:
            depth = 0

        for (child, xo, yo, focus, main) in self.children:
            if not main or not isinstance(child, Render):
                continue

            cx = x - xo
            cy = y - yo

            if self.forward:
                cx, cy = self.forward.transform(cx, cy)

            cf = child.main_displayables_at_point(cx, cy, layers, depth)
            rv.extend(cf)            

        return rv
        

    def is_opaque(self):
        """
        Returns true if this displayable is opaque, or False otherwise.
        Also sets self.visible_children.
        """

        if self.opaque is not None:
            return self.opaque

        # A rotated image is never opaque. (This isn't actually true, but it
        # saves us from the expensive calculations require to prove it is.)
        if self.forward:
            self.opaque = False
            return False
        
        rv = False
        vc = [ ]
        
        for i in self.children:
            child, xo, yo, focus, main = i

            if xo <= 0 and yo <= 0:
                cw, ch = child.get_size()
                if cw + xo < self.width or ch + yo < self.height:
                    if child.is_opaque():
                        vc = [ ]
                        rv = True
              
            vc.append(i)

        self.visible_children = vc
        self.opaque = rv
        return rv

    
    def is_pixel_opaque(self, x, y):
        """
        Determine if the pixel at x and y is opaque or not.
        """

        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return False

        for (child, xo, yo, focus, main) in self.children:
            cx = x - xo
            cy = y - yo

            if self.forward:
                cx, cy = self.forward.transform(cx, cy)

            if isinstance(child, Render):
                if child.is_pixel_opaque(cx, cy):
                    return True
            else:
                cw, ch = child.get_size()
                if cx >= cw or cy >= ch:
                    return False

                if not child.get_masks()[3] or child.get_at((cx, cy))[3]:
                    return True

        return False

    
    def fill(self, color):
        """
        Fills this Render with the given color.
        """

        color = renpy.easy.color(color)
        solid = renpy.display.im.SolidImage(color, self.width, self.height)
        surf = render(solid, self.width, self.height, 0, 0)
        self.blit(surf, (0, 0), focus=False, main=False)

        
    def canvas(self):
        """
        Returns a canvas object that draws to this Render.
        """

        surf = renpy.display.pgrender.surface((self.width, self.height), True)
        mutated_surface(surf)

        self.blit(surf, (0, 0))

        return Canvas(surf)

        
class Canvas(object):

    def __init__(self, surf):
        self.surf = surf
        
    def rect(self, color, rect, width=0):

        try:
            blit_lock.acquire()
            pygame.draw.rect(self.surf,
                             renpy.easy.color(color),
                             rect,
                             width)
        finally:
            blit_lock.release()

    def polygon(self, color, pointlist, width=0):
        try:
            blit_lock.acquire()
            pygame.draw.polygon(self.surf,
                                renpy.easy.color(color),
                                pointlist,
                                width)
        finally:
            blit_lock.release()

    def circle(self, color, pos, radius, width=0):

        try:
            blit_lock.acquire()
            pygame.draw.circle(self.surf,
                               renpy.easy.color(color),
                               pos,
                               radius,
                               width)

        finally:
            blit_lock.release()

    def ellipse(self, color, rect, width=0):
        try:
            blit_lock.acquire()
            pygame.draw.ellipse(self.surf,
                                renpy.easy.color(color),
                                rect,
                                width)
        finally:
            blit_lock.release()


    def arc(self, color, rect, start_angle, stop_angle, width=1):
        try:
            blit_lock.acquire()
            pygame.draw.arc(self.surf,
                            renpy.easy.color(color),
                            rect,
                            start_angle,
                            stop_angle,
                            width)
        finally:
            blit_lock.release()


    def line(self, color, start_pos, end_pos, width=1):
        try:
            blit_lock.acquire()
            pygame.draw.line(self.surf,
                             renpy.easy.color(color),
                             start_pos,
                             end_pos,
                             width)
        finally:
            blit_lock.release()

    def lines(self, color, closed, pointlist, width=1):
        try:
            blit_lock.acquire()
            pygame.draw.lines(self.surf,
                              renpy.easy.color(color),
                              closed,
                              pointlist,
                              width)
        finally:
            blit_lock.release()
    
    def aaline(self, color, startpos, endpos, blend=1):
        try:
            blit_lock.acquire()
            pygame.draw.aaline(self.surf,
                               renpy.easy.color(color),
                               startpos,
                               endpos,
                               blend)
        finally:
            blit_lock.release()

    def aalines(self, color, closed, pointlist, blend=1):
        try:
            blit_lock.acquire()
            pygame.draw.aalines(self.surf,
                                renpy.easy.color(color),
                                closed,
                                pointlist,
                                blend)
        finally:
            blit_lock.release()
