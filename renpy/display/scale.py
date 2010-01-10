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

# This hacks pygame to support resolution-scaling.

import os
import math
import pygame
import renpy
import renpy.display.pgrender as pgrender

# These need to be here before we mess with Pygame.
import _renpy_font
import _renpy

# Store this before we change it.
PygameSurface = pygame.Surface


# The factor we're scaling by.
factor = 1.0

# Should we scale fast or scale good-looking?
scale_fast = False


##############################################################################
# The scaling API that's used if we don't enable scaling.
    
# Gets the real pygame surface.
def real(s):
    return s

# Scales the number, n.
def scale(n):
    return n

def real_bilinear(src, size):
    rv = pgrender.surface_unscaled(size, src)
    renpy.display.module.bilinear_scale(src, rv)
    return rv

# Does pygame.transform.scale.
def real_transform_scale(surf, size):
    return pgrender.transform_scale_unscaled(surf, size)

# Loads an image, without scaling it.
def image_load_unscaled(f, hint, convert=True):
    rv = pgrender.load_image_unscaled(f, hint)
    return rv

# Saves an image without rescaling.
def image_save_unscaled(surf, dest):
    pygame.image.save(surf, dest)

# Scales down a surface.
def surface_scale(full):
    return full

real_renpy_pixellate = _renpy.pixellate
real_renpy_transform = _renpy.transform

def real_smoothscale(src, size, dest=None):
    """
    This scales src up or down to size. This uses both the pixellate
    and the transform operations to handle the scaling.
    """

    width, height = size
    srcwidth, srcheight = src.get_size()
    iwidth, iheight = srcwidth, srcheight

    if dest is None:
        dest = pgrender.surface_unscaled(size, src)

    if width == 0 or height == 0:
        return dest

    xshrink = 1
    yshrink = 1

    while iwidth >= width * 2:
        xshrink *= 2
        iwidth /= 2

    while iheight >= height * 2:
        yshrink *= 2
        iheight /= 2

    if iwidth != srcwidth or iheight != srcheight:
        inter = pgrender.surface_unscaled((iwidth, iheight), src)
        real_renpy_pixellate(src, inter, xshrink, yshrink, 1, 1)
        src = inter

    real_renpy_transform(src, dest,
                         0, 0,
                         1.0 * iwidth / width , 0,                             
                         0, 1.0 * iheight / height,
                         precise=1,
                         )

    return dest
    
smoothscale = real_smoothscale
    
    
def init():    
    global factor
    global scale_fast
    
    if 'RENPY_SCALE_FACTOR' in os.environ:
        factor = float(os.environ['RENPY_SCALE_FACTOR'])
    elif 'RENPY_SCALE_WIDTH' in os.environ:
        width = float(os.environ['RENPY_SCALE_WIDTH'])
        if width < renpy.config.screen_width:            
            factor = float(os.environ['RENPY_SCALE_WIDTH']) / renpy.config.screen_width
        else:
            factor = 1.0

    else:

        # Automatically scale to screen if too small.
        
        info = pygame.display.Info()

        factor = min(1.0,
                     1.0 * info.current_w / renpy.config.screen_width,
                     1.0 * info.current_h / renpy.config.screen_height)

        if factor <= 0:
            factor = 1.0
        
    if factor != 1.0:
        print "Using scale factor of %f." % factor
        load_scaling()

    if 'RENPY_SCALE_FAST' in os.environ:
        scale_fast = True
    else:
        scale_fast = False
        

scaling_loaded = False
    
# The virtual screen scaling creates.
screen = None

def load_scaling():

    global scaling_loaded

    if scaling_loaded:
        return

    scaling_loaded = True

    def real(s):
        return s.surface

    
    def same_size(*args):
        """
        If all the surfaces in args are the same size, return them all
        unchanged. Otherwise, compute smallest width and height, and
        take subsurfaces of anything bigger.
        """

        w = min(i.get_width() for i in args)
        h = min(i.get_height() for i in args)

        size = (w, h)
        
        rv = [ ]
        
        for i in args:
            if i.get_size() != size:
                i = i.subsurface((0, 0) + size)

            rv.append(i)
        
        return rv

    
    def scale(n):
        if n is None:
            return n

        return int(n * factor)

    
    def surface_scale(full):

        if scale_fast:
            scaled = real_transform_scale(full, v2p(full.get_size()))
        else:
            scaled = real_smoothscale(full, v2p(full.get_size()))

            return ScaledSurface(scaled, wh=full.get_size())

        
    # Project a tuple from virtual to physical coordinates.
    def v2p(n):
        if n is None:
            return None
        
        return tuple([ int(i * factor) for i in n ])

    
    # Similar, but include an extra pixel to deal with rounding.
    def v2pplus(n):

        if n is None:
            return None

        return tuple([ int(i * factor) + k for i, k in zip(n, (0, 0, 1, 1)) ])

    
    # Project a tuple from physical to virtual coordinates.
    def p2v(n):
        if n is None:
            return None

        return tuple([ int(i / factor) for i in n ])

    
    def set_mode((w, h), flags, bpp):

        global screen

        width = int(w * factor)
        height = int(h * factor)

        real_screen = pgrender.set_mode_unscaled((width, height), flags, bpp)
        screen = ScaledSurface(real_screen, wh=(w, h))

        return screen

    pgrender.set_mode = set_mode
    pygame.display.set_mode = set_mode
    

    # Proxies a function call from a Surface to a pygame surface.
    def proxy(name):
        func = getattr(PygameSurface, name)
        def rv(self, *args, **kwargs):
            return func(self.surface, *args, **kwargs)

        return rv


    # When scaling is enabled, objects of this class are returned from
    # pgrender.surface instead of pygame surfaces.
    class ScaledSurface(object):

        def __init__(self, what, alpha=True, wh=None):

            if isinstance(what, PygameSurface):
                self.surface = what

                if wh is not None:
                    self.width = int(wh[0])
                    self.height = int(wh[1])
                else:
                    self.width = int(math.ceil(self.surface.get_width() / factor))
                    self.height = int(math.ceil(self.surface.get_height() / factor))

            else:

                w, h = what
                w = int(w)
                h = int(h)
                self.width = w
                self.height = h

                w = int(w * factor)
                h = int(h * factor)

                if isinstance(alpha, ScaledSurface):
                    alpha = alpha.surface # E1103
                
                self.surface = pgrender.surface_unscaled((w, h), alpha)
                              
            self.virtx = 0
            self.virty = 0
            self.physx = 0
            self.physy = 0

        
        def transform_pos(self, (x, y)):
            """
            Converts a virtual position into a physical one.
            """

            x0 = x + self.virtx
            y0 = y + self.virty

            x0 *= factor
            y0 *= factor

            x0 = int(x0)            
            y0 = int(y0)            
            
            return (x0 - self.physx, y0 - self.physy)

        
        def transform_rect(self, (x, y, w, h)):
            """
            Converts a virtual rectangle into a physical one.
            """

            x0 = x + self.virtx
            y0 = y + self.virty
            x1 = x0 + w
            y1 = y0 + h

            x0 *= factor
            y0 *= factor
            x1 *= factor
            y1 *= factor

            x0 = int(x0)            
            y0 = int(y0)            
            x1 = int(x1)
            y1 = int(y1)
            
            rv = (x0 - self.physx, y0 - self.physy, x1 - x0, y1 - y0)

            return rv
            
            
        def __repr__(self):
            return "<ScaledSurface %r %r>" % (self.get_size(), self.surface)

        
        def blit(self, s, destpos, sourcerect=None):

            if sourcerect is None:
                self.surface.blit(
                    s.surface,
                    self.transform_pos(destpos))
            else:
                self.surface.blit(
                    s.surface,
                    self.transform_pos(destpos),
                    self.transform_rect(sourcerect))


        def copy(self):
            return ScaledSurface(self.surface.copy(), wh=self.get_size())

        
        def fill(self, color):
            self.surface.fill(color)

            
        def get_alpha(self):
            return self.surface.get_alpha()

        
        def get_at(self, pos):
            x, y = self.transform_pos(pos)
            w, h = self.surface.get_size()
            
            return self.surface.get_at((min(x, w - 1), min(y, h - 1)))


        set_colorkey = proxy("set_colorkey")
        get_alpha = proxy("get_alpha")
        get_locks = proxy("get_locks")
        map_rgb = proxy("map_rgb")
        unmap_rgb = proxy("unmap_rgb")
        get_pitch = proxy("get_pitch")
        set_masks = proxy("set_masks")
        get_shifts = proxy("get_shifts")
        set_shifts = proxy("set_shifts")
        get_losses = proxy("get_losses")
        
        
        def get_bytesize(self):
            return self.surface.get_bytesize()

        def get_bitsize(self):
            return self.surface.get_bitsize()
        
        def get_colorkey(self):
            return self.surface.get_colorkey()

        def get_flags(self):
            return self.surface.get_flags()

        def get_masks(self):
            return self.surface.get_masks()

        def get_size(self):
            return (self.width, self.height)
        
        def set_alpha(self, alpha, flags):
            self.surface.set_alpha(alpha, flags)

        def subsurface(self, rect):

            prect = self.transform_rect(rect)
            surf = self.surface.subsurface(prect)
            
            rv = ScaledSurface(surf, wh=rect[2:])

            vx, vy, vw, vh = rect
            px, py, pw, ph = prect

            rv.virtx = vx + self.virtx
            rv.virty = vy + self.virty
            rv.physx = px + self.physx
            rv.physy = py + self.physy

            return rv
            
        def mustlock(self):
            return False
        
        def lock(self):
            pass

        def unlock(self):
            pass

        def get_locked(self):
            return False

        def get_rect(self, **kwargs):
            rv = self.surface.get_rect()
            rv.size = p2v(rv.size)
            rv.topleft = p2v(rv.topleft)
            for k, v in kwargs.iteritems():
                setattr(rv, k, v)

            return rv
        
    pgrender.surface = ScaledSurface


    def copy_surface(surf, alpha=True):
        # We don't need to unbox alpha, since all relevant methods
        # are proxied.

        new_surf = pgrender.copy_surface_unscaled(surf.surface, alpha)
        return ScaledSurface(new_surf, wh=(surf.width, surf.height))

    pgrender.copy_surface = copy_surface
    
    

    def pygame_surface(size, flags, sample):
        return ScaledSurface(size, sample)

    pygame.Surface = pygame_surface
    
    
    
    old_update = pygame.display.update

    def update(rects=None):
        if rects is None:
            old_update()
            return

        if not isinstance(rects, list):
            rects = [ rects ]

        old_update([ v2pplus(i) for i in rects])

    pygame.display.update = update

    
    def get_surface():
        return screen

    pygame.display.get_surface = get_surface

    
    def load_image(f, filename):
        full = pgrender.load_image_unscaled(f, filename)
        return surface_scale(full)

    pgrender.load_image = load_image
    pygame.image.load = load_image
    

    def transform_scale(surf, size):

        rv = pgrender.transform_scale_unscaled(surf.surface, v2p(size))
        rv = ScaledSurface(rv, wh=size)

        return rv

    pgrender.transform_scale = transform_scale
    pygame.transform.scale = transform_scale
    
    
    def transform_flip(surf, xbool, ybool):
        new_surf = pgrender.flip_unscaled(surf.surface, xbool, ybool) 
        return ScaledSurface(new_surf, wh=surf.get_size())

    pgrender.flip = transform_flip
    pygame.transform.flip = transform_flip
    

    
    def transform_rotate(surf, angle):
        new_surf = pgrender.transform_rotate_unscaled(surf.surface, angle)
        return ScaledSurface(new_surf)

    pgrender.transform_rotate = transform_rotate
    pygame.transform.rotate = transform_rotate
    

    
    def rotozoom(surf, angle, scale):
        new_surf = pgrender.rotozoom(surf.surface, angle, scale)
        return ScaledSurface(new_surf)

    pgrender.rotozoom = rotozoom
    pygame.transform.rotozoom = rotozoom

    
    # Ignoring scale2x and chop. The former due to a pending api change,
    # the latter due to general uselessness.
    
    PygameFont = _renpy_font.Font

    class Font(object):

        def __init__(self, o, size, index):
            self.font = PygameFont(o, int(size * factor), index)

        def render(self, *args):
            return ScaledSurface(self.font.render(*args))

        def size(self, text):
            return p2v(self.font.size(text))

        def set_underline(self, b):
            self.font.set_underline(b)

        def get_underline(self,):
            return self.font.get_underline()

        def set_bold(self, b):
            self.font.set_bold(b)

        def get_bold(self):
            return self.font.get_bold()

        def set_italic(self, b):
            self.font.set_italic(b)

        def get_italic(self):
            return self.font.get_italic()

        def get_linesize(self):
            return int(self.font.get_linesize() / factor)

        def get_height(self):
            return int(self.font.get_height() / factor)

        def get_ascent(self):
            return int(self.font.get_ascent() / factor)

        def get_descent(self):
            return int(self.font.get_descent() / factor)

        def set_expand(self, value):
            self.font.set_expand(value * factor)
        
    _renpy_font.Font = Font

    
    old_image_save = pygame.image.save

    def image_save(surf, dest):
        surf = pgrender.transform_scale_unscaled(surf.surface, surf.get_size())
        old_image_save(surf, dest)

    pygame.image.save = image_save

    
    def image_save_unscaled(surf, dest):
        old_image_save(surf.surface, dest)

    
    old_mouse_get_pos = pygame.mouse.get_pos

    def mouse_get_pos():
        return p2v(old_mouse_get_pos())

    pygame.mouse.get_pos = mouse_get_pos

    
    def scale_event(ev):
        if ev.type == pygame.MOUSEMOTION:
            return pygame.event.Event(ev.type, pos=p2v(ev.pos), rel=p2v(ev.rel), buttons=ev.buttons)
        elif ev.type == pygame.MOUSEBUTTONUP or ev.type == pygame.MOUSEBUTTONDOWN:
            return pygame.event.Event(ev.type, pos=p2v(ev.pos), button=ev.button)
        else:
            return ev


    old_event_poll = pygame.event.poll
    
    def event_poll():
        ev = old_event_poll()
        return scale_event(ev)

    pygame.event.poll = event_poll


    old_event_wait = pygame.event.wait

    def event_wait():
        ev = old_event_wait()
        return scale_event(ev)

    pygame.event.wait = event_wait


    old_event_get = pygame.event.get

    def event_get(*args):
        rv = old_event_get(*args)

        if rv:
            rv[-1] = scale_event(rv[-1])

        return rv

    pygame.event.get = event_get


        
    old_save_png = _renpy.save_png

    def save_png(surf, dest, compress=-1):
        surf = pgrender.transform_scale_unscaled(surf.surface, surf.get_size())
        old_save_png(surf, dest, compress=compress)

    _renpy.save_png = save_png


    old_pixellate = _renpy.pixellate

    def pixellate(pysrc, pydst, avgwidth, avgheight, outwidth, outheight):
        ow = max(int(outwidth * factor), 1)
        oh = max(int(outheight * factor), 1)

        owf = 1.0 * ow / outwidth
        ohf = 1.0 * oh / outheight

        old_pixellate(pysrc.surface, pydst.surface,
                      max(avgwidth * owf, 1),
                      max(avgheight * ohf, 1),
                      ow, oh)

    _renpy.pixellate = pixellate


    old_map = _renpy.map

    def map(pysrc, pydst, r, g, b, a):
        pysrc, pydst = same_size(pysrc.surface, pydst.surface)
        old_map(pysrc, pydst, r, g, b, a)

    _renpy.map = map


    old_linmap = _renpy.linmap

    def linmap(pysrc, pydst, r, g, b, a):
        pysrc, pydst = same_size(pysrc.surface, pydst.surface)
        old_linmap(pysrc, pydst, r, g, b, a)

    _renpy.linmap = linmap


    old_bilinear = _renpy.bilinear
    
    def bilinear(pysrc, pydst, source_xoff=0.0, source_yoff=0.0,
                 source_width=None, source_height=None,
                 dest_xoff=0.0, dest_yoff=0.0, dest_width=None,
                 dest_height=None, precise=0):

        def f(n):
            if n is None:
                return n
            return n * factor

        source_xoff = f(source_xoff)
        source_yoff = f(source_yoff)
        source_width = f(source_width)
        source_height = f(source_height)

        dest_xoff = f(dest_xoff)
        dest_yoff = f(dest_yoff)
        dest_width = f(dest_width)
        dest_height = f(dest_height)

        old_bilinear(pysrc.surface, pydst.surface,
                     source_xoff=source_xoff,
                     source_yoff=source_yoff,
                     source_width=source_width,
                     source_height=source_height,
                     dest_xoff=dest_xoff,
                     dest_yoff=dest_yoff,
                     dest_width=dest_width,
                     dest_height=dest_height,
                     precise=precise)

    _renpy.bilinear = bilinear


    old_alpha_munge = _renpy.alpha_munge

    def alpha_munge(pysrc, pydst, srcchan, dstchan, amap):
        pysrc, pydst = same_size(pysrc.surface, pydst.surface)
        old_alpha_munge(pysrc, pydst, srcchan, dstchan, amap)

    _renpy.alpha_munge = alpha_munge


    old_transform = _renpy.transform

    def transform(pysrc, pydst, corner_x, corner_y,
                  xdx, ydx, xdy, ydy, a=1.0, precise=0):

        old_transform(pysrc.surface, pydst.surface,
                      corner_x * factor, corner_y * factor,
                      xdx, ydx, xdy, ydy, a, precise)

    _renpy.transform = transform


    old_subpixel = _renpy.subpixel

    def subpixel(pysrc, pydst, x, y, shift):
        return old_subpixel(pysrc.surface, pydst.surface, x * factor, y * factor, shift)

    _renpy.subpixel = subpixel


    old_blend = _renpy.blend

    def blend(pysrca, pysrcb, pydst, alpha):
        pysrca, pysrcb, pydst = same_size(pysrca.surface, pysrcb.surface, pydst.surface)
        old_blend(pysrca, pysrcb, pydst, alpha)

    _renpy.blend = blend

    
    old_imageblend = _renpy.imageblend

    def imageblend(pysrca, pysrcb, pydst, pyimg, aoff, amap):
        pysrca, pysrcb, pydst, pyimg = same_size(pysrca.surface, pysrcb.surface, pydst.surface, pyimg.surface)
        old_imageblend(pysrca, pysrcb, pydst, pyimg, aoff, amap)

    _renpy.imageblend = imageblend

    
    old_colormatrix = _renpy.colormatrix

    def colormatrix(src, dst, *args):
        src, dst = same_size(src.surface, dst.surface)
        old_colormatrix(src, dst, *args)

    _renpy.colormatrix = colormatrix
        

    def draw_scale(o):
        if isinstance(o, int):
            return int(math.ceil(o * factor))
        elif isinstance(o, float):
            return o * factor        
        elif isinstance(o, tuple):
            return tuple(draw_scale(i) for i in o)
        elif isinstance(o, list):
            return tuple(draw_scale(i) for i in o)
        elif isinstance(o, dict):
            return dict((k, draw_scale(v)) for k, v in o.iteritems())
        else:
            return None

        
    def draw_wrap(f):
        def newf(surf, color, *args, **kwargs):
            f(surf.surface, color, *draw_scale(args), **draw_scale(kwargs))
        return newf

    
    def arc_wrap(f):
        def newf(surf, color, Rect, start_angle, stop_angle, width=1):
            f(surf.surface, color, draw_scale(Rect), start_angle, stop_angle, draw_scale(width))
        return newf

    
    pygame.draw.rect = draw_wrap(pygame.draw.rect)
    pygame.draw.polygon = draw_wrap(pygame.draw.polygon)
    pygame.draw.circle = draw_wrap(pygame.draw.circle)
    pygame.draw.ellipse = draw_wrap(pygame.draw.ellipse)
    pygame.draw.arc = arc_wrap(pygame.draw.arc)
    pygame.draw.line = draw_wrap(pygame.draw.line)
    pygame.draw.lines = draw_wrap(pygame.draw.lines)
    pygame.draw.aaline = draw_wrap(pygame.draw.aaline)
    pygame.draw.aalines = draw_wrap(pygame.draw.aalines)

    # Smoothscale:

    def smoothscale(surf, size, dest=None):
        if dest is not None:
            dest = dest.surface

        rv = real_smoothscale(surf.surface, v2p(size), dest)

        if rv is None:
            return rv
        else:
            return ScaledSurface(rv, wh=size)
    
    # Now, put everything from this function's namespace into the
    # module namespace.

    globals().update(locals())
    reload(renpy.display.module)
