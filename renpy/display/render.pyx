#cython: profile=False
# Copyright 2004-2015 Tom Rothamel <pytom@bishoujo.us>
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
import pygame_sdl2 as pygame
import threading
import renpy
import gc
import math

# We grab the blit lock each time it is necessary to blit
# something. This allows call to the pygame.transform functions to
# disable blitting, should it prove necessary.
blit_lock = threading.Condition()

# This is a dictionary containing all the renders that we know of. It's a
# map from displayable to dictionaries containing the render of that
# displayable.
render_cache = collections.defaultdict(dict)

# The queue of redraws. A list of (time, displayable) pairs.
redraw_queue = [ ]

# The render returned from render_screen.
screen_render = None

# A list of renders the system knows about, and thinks are still alive.
cdef list live_renders
live_renders = [ ]

# A copy of renpy.display.interface.frame_time, for speed reasons.
cdef double frame_time
frame_time = 0

def free_memory():
    """
    Frees memory used by the render system.
    """

    global screen_render
    screen_render = None

    mark_sweep()

    render_cache.clear()

    # This can hang onto a render.
    renpy.display.interface.surftree = None


def check_at_shutdown():
    """
    This is called at shutdown time to check that everything went okay.
    The big thing it checks for is memory leaks.
    """

    if not renpy.config.developer:
        return

    free_memory()

    gc.collect()
    l = gc.get_objects()

    count = 0
    objects = gc.get_objects()

    for i in objects:
        if isinstance(i, Render):
            count += 1

    if count:
        raise Exception("%d Renders are alive at shutdown. This is probably a memory leak bug in Ren'Py." % count)


# The number of things being rendered at the moment.
cdef int rendering
rendering = 0

# The st and at of the current call to render.
render_st = 0.0
render_at = 0.0

cpdef render(d, object widtho, object heighto, double st, double at):
    """
    :doc: udd_utility
    :args: (d, width, height, st, at)

    Causes a displayable to be rendered, and a renpy.Render object to
    be returned.

    `d`
        The displayable to render.

    `width`, `height`
        The width and height available for the displayable to render into.

    `st`, `at`
        The shown and animation timebases.

    Renders returned by this object may be cached, and should not be modified
    once they have been retrieved.
    """

    global rendering
    global render_st
    global render_at

    cdef float width, height
    cdef float orig_width, orig_height
    cdef tuple orig_wh, wh
    cdef dict render_cache_d
    cdef Render rv

    orig_wh = (widtho, heighto, frame_time-st, frame_time-at)

    id_d = id(d)
    render_cache_d = render_cache[id_d]
    rv = render_cache_d.get(orig_wh, None)

    if rv is not None:
        return rv

    orig_width = width = widtho
    orig_height = height = heighto

    style = d.style
    xmaximum = style.xmaximum
    ymaximum = style.ymaximum

    if xmaximum is not None:
        if isinstance(xmaximum, float):
            width = width * xmaximum
        else:
            width = min(xmaximum, width)

    if ymaximum is not None:
        if isinstance(ymaximum, float):
            height = height * ymaximum
        else:
            height = min(ymaximum, height)

    if width < 0:
        width = 0
    if height < 0:
        height = 0

    if orig_width != width or orig_height != height:
        widtho = width
        heighto = height
        wh = (widtho, heighto, frame_time-st, frame_time-at)
        rv = render_cache_d.get(wh, None)

        if rv is not None:
            return rv

    else:
        wh = orig_wh

    try:
        rendering += 1
        old_st = render_st
        old_at = render_at
        render_st = st
        render_at = at
        rv = d.render(widtho, heighto, st, at)
    finally:
        rendering -= 1
        render_st = old_st
        render_at = old_at

    rv.render_of.append(d)

    if style.clipping:
        rv = rv.subsurface((0, 0, rv.width, rv.height), focus=True)
        rv.render_of.append(d)

    render_cache_d[wh] = rv

    if wh is not orig_wh:
        render_cache_d[orig_wh] = rv

    return rv

def invalidate(d):
    """
    Removes d from the render cache. If we're not in a redraw, triggers
    a redraw to start.
    """

    if not rendering:
        redraw(d, 0)


def process_redraws():
    """
    Called to determine if any redraws are pending. Returns true if we
    need to redraw the screen now, false otherwise.
    """

    global redraw_queue

    redraw_queue.sort()

    now = renpy.display.core.get_time()
    rv = False

    new_redraw_queue = [ ]
    seen = set()

    for t in redraw_queue:
        when, d = t

        id_d = id(d)

        if id_d in seen:
            continue

        seen.add(id_d)

        if id_d not in render_cache:
            continue

        if when <= now:
            # Remove this displayable and all its parents from the
            # render cache. But don't kill them yet, as that will kill the
            # children that we want to reuse.

            for v in render_cache[id_d].values():
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
    :doc: udd_utility

    Causes the displayable `d` to be redrawn after `when` seconds have
    elapsed.
    """

    if not renpy.game.interface:
        return

    redraw_queue.append((when + renpy.game.interface.frame_time, d))


cdef class Matrix2D:
    """
    This represents a 2d matrix that can be used to transform
    points and things like that.
    """

    def __getstate__(self):
        return dict(
            xdx = self.xdx,
            xdy = self.xdy,
            ydx = self.ydx,
            ydy = self.ydy)

    def __setstate__(self, state):
        self.xdx = state['xdx']
        self.xdy = state['xdy']
        self.ydx = state['ydx']
        self.ydy = state['ydy']

    def __init__(Matrix2D self, double xdx, double xdy, double ydx, double ydy):
        self.xdx = xdx
        self.xdy = xdy
        self.ydx = ydx
        self.ydy = ydy

    cpdef tuple transform(Matrix2D self, double x, double y):
        return (x * self.xdx + y * self.xdy), (x * self.ydx + y * self.ydy)

    def __mul__(Matrix2D self, Matrix2D other):
        return Matrix2D(
            other.xdx * self.xdx + other.xdy * self.ydx,
            other.xdx * self.xdy + other.xdy * self.ydy,
            other.ydx * self.xdx + other.ydy * self.ydx,
            other.ydx * self.xdy + other.ydy * self.ydy)

    def __repr__(self):
        return "Matrix2D(xdx=%f, xdy=%f, ydx=%f, ydy=%f)" % (self.xdx, self.xdy, self.ydx, self.ydy)

    def __richcmp__(self, other, op):

        if op != 2:
            return NotImplemented

        if self is other:
            return True

        return (
            abs(self.xdx - other.xdx) +
            abs(self.xdy - other.xdy) +
            abs(self.ydx - other.ydx) +
            abs(self.ydy - other.ydy)) < .00001


IDENTITY = Matrix2D(1, 0, 0, 1)

def take_focuses(focuses):
    """
    Adds a list of rectangular focus regions to the focuses list.
    """

    screen_render.take_focuses(
        0, 0, screen_render.width, screen_render.height,
        IDENTITY,
        0, 0,
        None,
        focuses)

# The result of focus_at_point for a modal render. This overrides any
# specific focus from below us.
Modal = renpy.object.Sentinel("Modal")

def focus_at_point(x, y):
    """
    Returns a focus object corresponding to the uppermost displayable
    at point, or None if nothing focusable is at point.
    """

    if screen_render is None:
        return None

    cf = screen_render.focus_at_point(x, y, None)
    if cf is None or cf is Modal:
        return None
    else:
        d, arg, screen = cf
        return renpy.display.focus.Focus(d, arg, None, None, None, None, screen)


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

    global screen_render
    global invalidated
    global frame_time

    frame_time = renpy.display.interface.frame_time

    rv = render(root, width, height, 0, 0)
    screen_render = rv

    invalidated = False

    rv.is_opaque()

    return rv

def mark_sweep():
    """
    This performs mark-and-sweep garbage collection on the live_renders
    list.
    """

    global live_renders

    cdef list worklist
    cdef int i
    cdef Render r, j

    worklist = [ ]

    if screen_render is not None:
        worklist.append(screen_render)

    i = 0

    while i < len(worklist):
        r = worklist[i]

        for j in r.depends_on_list:
            if not j.mark:
                j.mark = True
                worklist.append(j)

        i += 1

    for r in live_renders:
        if not r.mark:
            r.kill_cache()
        else:
            r.mark = False

    live_renders = worklist

def compute_subline(sx0, sw, cx0, cw):
    """
    Given a source line (start sx0, width sw) and a crop line (cx0, cw),
    return three things:

    * The offset of the portion of the source line that overlaps with
      the crop line, relative to the crop line.
    * The offset of the portion of the source line that overlaps with the
      the crop line, relative to the source line.
    * The length of the overlap in pixels. (can be <= 0)
    """

    sx1 = sx0 + sw
    cx1 = cx0 + cw

    if sx0 > cx0:
        start = sx0
    else:
        start = cx0

    offset = start - cx0
    crop = start - sx0

    if sx1 < cx1:
        width = sx1 - start
    else:
        width = cx1 - start


    return offset, crop, width




# Possible operations that can be done as part of a render.
BLIT = 0
DISSOLVE = 1
IMAGEDISSOLVE = 2
PIXELLATE = 3

cdef class Render:

    def __init__(Render self, float width, float height, draw_func=None, layer_name=None, bint opaque=None): #@DuplicatedSignature
        """
        Creates a new render corresponding to the given widget with
        the specified width and height.

        If `layer_name` is given, then this render corresponds to a
        layer.
        """

        # The mark bit, used for mark/sweep-style garbage collection of
        # renders.
        self.mark = False

        # Is has this render been removed from the cache?
        self.cache_killed = False


        self.width = width
        self.height = height

        self.layer_name = layer_name

        # A list of (surface/render, xoffset, yoffset, focus, main) tuples, ordered from
        # back to front.
        self.children = [ ]

        # The set of renders that either have us as children, or depend on
        # us.
        self.parents = set()

        # The renders we depend on, including our children.
        self.depends_on_list = [ ]

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

        # The over blending factor. When this is 1.0, blends only use the
        # over operation. When set to 0.0, we get additive blending.
        self.over = 1.0

        # If true, children of this render use nearest-neighbor texture
        # lookup. If false, bilinear, if None, from the parent.
        self.nearest = None

        # A list of focus regions in this displayable.
        self.focuses = None

        # Other renders that we should pass focus onto.
        self.pass_focuses = None

        # The ScreenDisplayable this is a render of.
        self.focus_screen = None

        # The displayable(s) that this is a render of. (Set by render)
        self.render_of = [ ]

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

        # Caches of the texture created by rendering this surface.
        self.surface = None
        self.alpha_surface = None

        # Cache of the texture created by rendering this surface at half size.
        # (This is set in gldraw.)
        self.half_cache = None

        # Are we modal?
        self.modal = False

        # Are we a text input?
        self.text_input = False

        live_renders.append(self)

    def __repr__(self): #@DuplicatedSignature
        return "<Render %x of %r>" % (id(self), self.render_of)

    def __getstate__(self): #@DuplicatedSignature
        if renpy.config.developer:
            raise Exception("Can't pickle a Render.")
        else:
            return { }

    def __setstate__(self, state): #@DuplicatedSignature
        return

    cpdef int blit(Render self, source, tuple pos, object focus=True, object main=True, object index=None):
        """
        Blits `source` (a Render or Surface) to this Render, offset by
        xo and yo.

        If `focus` is true, then focuses are added from the child to the
        parent.

        This will only blit on integer pixel boundaries.
        """

        (xo, yo) = pos

        if source is self:
            raise Exception("Blitting to self.")

        xo = int(xo)
        yo = int(yo)

        if index is None:
            self.children.append((source, xo, yo, focus, main))
        else:
            self.children.insert(index, (source, xo, yo, focus, main))

        if isinstance(source, Render):
            self.depends_on_list.append(source)
            source.parents.add(self)

        return 0

    cpdef int subpixel_blit(Render self, source, tuple pos, object focus=True, object main=True, object index=None):
        """
        Blits `source` (a Render or Surface) to this Render, offset by
        xo and yo.

        If `focus` is true, then focuses are added from the child to the
        parent.

        This blits at fractional pixel boundaries.
        """

        (xo, yo) = pos

        xo = float(xo)
        yo = float(yo)

        if index is None:
            self.children.append((source, xo, yo, focus, main))
        else:
            self.children.insert(index, (source, xo, yo, focus, main))

        if isinstance(source, Render):
            self.depends_on_list.append(source)
            source.parents.add(self)

        return 0

    cpdef int absolute_blit(Render self, source, tuple pos, object focus=True, object main=True, object index=None):
        """
        Blits `source` (a Render or Surface) to this Render, offset by
        xo and yo.

        If `focus` is true, then focuses are added from the child to the
        parent.

        This blits at fractional pixel boundaries.
        """

        (xo, yo) = pos

        xo = renpy.display.core.absolute(xo)
        yo = renpy.display.core.absolute(yo)

        if index is None:
            self.children.append((source, xo, yo, focus, main))
        else:
            self.children.insert(index, (source, xo, yo, focus, main))

        if isinstance(source, Render):
            self.depends_on_list.append(source)
            source.parents.add(self)

        return 0


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

        This returns a texture that's at the drawable resolultion, which
        may be bigger than the virtual resolution. Use renpy.display.draw.draw_to_virt
        and draw.virt_to_draw to convert between the two resolutions. (For example,
        multiply reverse by draw_to_virt to scale this down for blitting.)
        """

        if alpha:
            if self.alpha_surface is not None:
                return self.alpha_surface
        else:
            if self.surface is not None:
                return self.surface

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

        (x, y, w, h) = rect
        rv = Render(w, h)

        reverse = self.reverse

        # This doesn't actually make a subsurface, as we can't easily do
        # so for non-rectangle-aligned renders.
        if (reverse is not None) and (
            reverse.xdx != 1.0 or
            reverse.xdy != 0.0 or
            reverse.ydx != 0.0 or
            reverse.ydy != 1.0):

            rv.clipping = True
            rv.blit(self, (-x, -y), focus=focus, main=True)
            return rv

        # This is the path that executes for rectangle-aligned surfaces,
        # making an actual subsurface.

        for child, cx, cy, cfocus, cmain in self.children:

            childw, childh = child.get_size()
            xo, cx, cw = compute_subline(cx, childw, x, w)
            yo, cy, ch = compute_subline(cy, childh, y, h)

            if cw <= 0 or ch <= 0 or w - xo <= 0 or h - yo <= 0:
                continue

            if cx < 0 or cx >= childw or cy < 0 or cy >= childh:
                continue

            offset = (xo, yo)
            crop = None

            try:
                if isinstance(child, Render) and not child.clipping:
                    crop = (cx, cy, w - xo, h - yo)
                    newchild = child.subsurface(crop, focus=focus)
                    newchild.render_of = child.render_of[:]
                else:
                    crop = (cx, cy, cw, ch)
                    newchild = child.subsurface(crop)
                    renpy.display.draw.mutated_surface(newchild)
            except:
                raise Exception("Creating subsurface failed. child size = ({}, {}), crop = {!r}".format(childw, childh, crop))

            rv.blit(newchild, offset, focus=cfocus, main=cmain)

        if focus and self.focuses:

            for (d, arg, xo, yo, fw, fh, mx, my, mask) in self.focuses:

                if xo is None:
                    rv.add_focus(d, arg, xo, yo, fw, fh, mx, my, mask)
                    continue

                xo, cx, fw = compute_subline(xo, fw, x, w)
                yo, cy, fh = compute_subline(yo, fh, y, h)

                if cw <= 0 or ch <= 0:
                    continue

                if mx is not None:

                    mw, mh = mask.get_size()

                    mx, mcx, mw = compute_subline(mx, mw, x, w)
                    my, mcy, mh = compute_subline(my, mh, y, h)

                    if mw <= 0 or mh <= 0:
                        mx = None
                        my = None
                        mask = None
                    else:
                        mask = mask.subsurface((mcx, mcy, mw, mh))

                rv.add_focus(d, arg, xo, yo, fw, fh, mx, my, mask)

        rv.depends_on(self)
        rv.alpha = self.alpha
        rv.operation = self.operation
        rv.operation_alpha = self.operation_alpha
        rv.operation_complete = self.operation_complete
        rv.nearest = self.nearest

        return rv


    def depends_on(self, source, focus=False):
        """
        Used to indicate that this render depends on another
        render. Useful, for example, if we use pygame_surface to make
        a surface, and then blit that surface into another render.
        """

        if source is self:
            raise Exception("Render depends on itself.")

        self.depends_on_list.append(source)
        source.parents.add(self)

        if focus:
            if self.pass_focuses is None:
                self.pass_focuses = [ source ]
            else:
                self.pass_focuses.append(source)


    def kill_cache(self):
        """
        Removes this render and its transitive parents from the cache.
        """

        if self.cache_killed:
            return

        self.cache_killed = True

        for i in self.parents:
            i.kill_cache()

        self.parents.clear()

        for i in self.depends_on_list:
            if not i.cache_killed:
                i.parents.discard(self)

        for ro in self.render_of:
            id_ro = id(ro)

            cache = render_cache[id_ro]
            for k, v in cache.items():
                if v is self:
                    del cache[k]

            if not cache:
                del render_cache[id_ro]

    def kill(self):
        """
        Retained for compatibility, but does not need to be called.
        """

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

        if isinstance(mask, Render) and mask is not self:
            self.depends_on(mask)

        t = (d, arg, x, y, w, h, mx, my, mask)

        if self.focuses is None:
            self.focuses = [ t ]
        else:
            self.focuses.append(t)

    def take_focuses(self, cminx, cminy, cmaxx, cmaxy, reverse, x, y, screen, focuses): #@DuplicatedSignature
        """
        This adds to focuses Focus objects corresponding to the focuses
        added to this object and its children, transformed into screen
        coordinates.

        `cminx`, `cminy`, `cmaxx`, `cmaxy`
            The clipping rectangle.

        `reverse`
            The transform from render to screen coordinates.

        `x`, `y`
            The offset of the upper-left corner of the render.

        `screen`
            The screen this is a render of, or None if this is not part of
            a screen.

        `focuses`
            The list of focuses to add to.

        """

        if self.focus_screen is not None:
            screen = self.focus_screen

        if self.modal:
            focuses[:] = [ ]

        if self.reverse:
            reverse = reverse * self.reverse

        if self.focuses:

            for (d, arg, xo, yo, w, h, mx, my, mask) in self.focuses:

                if xo is None:
                    focuses.append(renpy.display.focus.Focus(d, arg, None, None, None, None, screen))
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

                focuses.append(renpy.display.focus.Focus(d, arg, minx, miny, maxx - minx, maxy - miny, screen))

        if self.clipping:
            cminx = max(cminx, x)
            cminy = max(cminy, y)
            cmaxx = min(cmaxx, x + self.width)
            cmaxy = min(cmaxx, x + self.height)

        for child, xo, yo, focus, main in self.children:
            if not focus or not isinstance(child, Render):
                continue

            xo, yo = reverse.transform(xo, yo)
            child.take_focuses(cminx, cminy, cmaxx, cmaxy, reverse, x + xo, y + yo, screen, focuses)

        if self.pass_focuses:
            for child in self.pass_focuses:
                child.take_focuses(cminx, cminy, cmaxx, cmaxy, reverse, x, y, screen, focuses)

    def focus_at_point(self, x, y, screen): #@DuplicatedSignature
        """
        This returns the focus of this object at the given point.
        """

        if self.focus_screen is not None:
            screen = self.focus_screen

        if self.clipping:
            if x < 0 or x >= self.width or y < 0 or y >= self.height:
                return None

        if self.operation == IMAGEDISSOLVE:
            if not self.children[0][0].is_pixel_opaque(x, y):
                return None

        rv = None

        if self.focuses:
            for (d, arg, xo, yo, w, h, mx, my, mask) in self.focuses:

                if xo is None:
                    continue

                elif mx is not None:
                    cx = x - mx
                    cy = y - my

                    if self.forward:
                        cx, cy = self.forward.transform(cx, cy)

                    if isinstance(mask, Render):
                        if mask.is_pixel_opaque(cx, cy):
                            rv = d, arg, screen
                    else:
                        if mask(cx, cy):
                            rv = d, arg, screen

                elif xo <= x < xo + w and yo <= y < yo + h:
                    rv = d, arg, screen

        for child, xo, yo, focus, main in self.children:

            if not focus or not isinstance(child, Render):
                continue

            cx = x - xo
            cy = y - yo

            if self.forward:
                cx, cy = self.forward.transform(cx, cy)

            cf = child.focus_at_point(cx, cy, screen)
            if cf is not None:
                rv = cf

        if self.pass_focuses:
            for child in self.pass_focuses:
                cf = child.focus_at_point(x, y, screen)
                if cf is not None:
                    rv = cf

        if rv is None and self.modal:
            rv = Modal

        return rv


    def main_displayables_at_point(self, x, y, layers, depth=None):
        """
        Returns the displayable at `x`, `y` on one of the layers in
        the set or list `layers`.
        """

        rv = [ ]

        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return rv

        is_screen = False

        if depth is not None:
            for d in self.render_of:
                rv.append((depth, self.width, self.height, d))
                depth += 1

                if isinstance(d, renpy.display.screen.ScreenDisplayable):
                    is_screen = True

        elif self.layer_name in layers:
            depth = 0

        for (child, xo, yo, focus, main) in self.children:
            if not main or not isinstance(child, Render):
                continue

            cx = x - xo
            cy = y - yo

            if self.forward:
                cx, cy = self.forward.transform(cx, cy)

            if is_screen:
                # Ignore the fixed at the root of every screen.
                cf = child.main_displayables_at_point(cx, cy, layers, depth - 1)
                rv.extend(cf[1:])
            else:
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

        if self.is_opaque():
            return True

        return renpy.display.draw.is_pixel_opaque(self, x, y)


    def fill(self, color):
        """
        Fills this Render with the given color.
        """

        color = renpy.easy.color(color)
        solid = renpy.display.imagelike.Solid(color)
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

    def screen_rect(self, double sx, double sy, Matrix2D transform):
        """
        Returns the rectangle, in screen-space coordinates, that will be covered
        by this render when it's drawn to the screen at sx, sy, with the transform
        `transform`.
        """

        if transform is None:
            transform = IDENTITY

        cdef double w = self.width
        cdef double h = self.height

        cdef double xdx = transform.xdx
        cdef double xdy = transform.xdy
        cdef double ydx = transform.ydx
        cdef double ydy = transform.ydy

        # Transform the vertex coordinates to screen-space.
        cdef double x0 = sx
        cdef double y0 = sy

        cdef double x1 = w * xdx + sx
        cdef double y1 = w * ydx + sy

        cdef double x2 = h * xdy + sx
        cdef double y2 = h * ydy + sy

        cdef double x3 = w * xdx + h * xdy + sx
        cdef double y3 = w * ydx + h * ydy + sy

        cdef double minx = min(x0, x1, x2, x3)
        cdef double maxx = max(x0, x1, x2, x3)
        cdef double miny = min(y0, y1, y2, y3)
        cdef double maxy = max(y0, y1, y2, y3)

        return (
            int(minx),
            int(miny),
            int(math.ceil(maxx - minx)),
            int(math.ceil(maxy - miny)),
            )

    def place(self, d, x=0, y=0, width=None, height=None, st=None, at=None, render=None, main=True):
        """
        Documented in udd.rst.
        """

        if width is None:
            width = self.width
        if height is None:
            height = self.height

        if render is None:
            if st is None:
                st = render_st
            if at is None:
                at = render_at

            render = renpy.display.render.render(d, width, height, st, at)

        d.place(self, x, y, width, height, render, main=main)

    def zoom(self, xzoom, yzoom):
        """
        Sets the zoom factor applied to this displayable's children.
        """
        if self.reverse is None:
            self.reverse = IDENTITY
            self.forward = IDENTITY

        self.reverse *= Matrix2D(xzoom, 0, 0, yzoom)

        if xzoom and yzoom:
            self.forward *= Matrix2D(1.0 / xzoom, 0, 0, 1.0 / yzoom)
        else:
            self.forward *= Matrix2D(0, 0, 0, 0)

class Canvas(object):

    def __init__(self, surf): #@DuplicatedSignature
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

    def get_surface(self):
        return self.surf

