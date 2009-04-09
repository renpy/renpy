# Copyright 2004-2009 PyTom <pytom@bishoujo.us>
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

    
PygameSurface = pygame.Surface

try:
    import _renpy_font as font_module
except ImportError:
    import pygame.font as font_module

# This needs to be done before we mess too hard with pygame.
try:
    import _renpy
except ImportError:
    _renpy = None
    
factor = 1.0

if ('RENPY_SCALE_FACTOR' in os.environ) or ('RENPY_SCALE_WIDTH' in os.environ):
    enable_scaling = True
else:
    enable_scaling = False

##############################################################################
# The scaling API that's used if we don't enable scaling.
    

def init():
    return

# Gets the real pygame surface.
def real(s):
    return s

# Scales the number, n.
def scale(n):
    return n

def real_bilinear(src, size):
    rv = pygame.Surface(size, 0, src)
    renpy.display.module.bilinear_scale(src, rv)
    return rv

# Does pygame.transform.scale.
def real_transform_scale(surf, size):
    global real_transform_scale
    real_transform_scale = pygame.transform.scale

    return real_transform_scale(surf, size)

# Loads an image, without scaling it.
def image_load_unscaled(f, hint, convert=True):
    rv = pygame.image.load(f, hint)

    if convert:
        rv = rv.convert_alpha()

    return rv

# Scales down a surface.
def surface_scale(full):
    return full

# Saves an image without rescaling.
def image_save_unscaled(surf, dest):
    pygame.image.save(surf, dest)


    
def init():    
    global factor

    if 'RENPY_SCALE_FACTOR' in os.environ:
        factor = float(os.environ['RENPY_SCALE_FACTOR'])
    elif 'RENPY_SCALE_WIDTH' in os.environ:
        width = float(os.environ['RENPY_SCALE_WIDTH'])
        if width < renpy.config.screen_width:            
            factor = float(os.environ['RENPY_SCALE_WIDTH']) / renpy.config.screen_width
        else:
            factor = 1.0

    else:

        factor = 1.0
        
        # Automatically scale to screen if too small.
        
#         info = pygame.display.Info()

#         factor = min(1.0,
#                      1.0 * info.current_w / renpy.config.screen_width,
#                      1.0 * info.current_h / renpy.config.screen_height)

#         if factor <= 0:
#             factor = 1.0

        
    if factor != 1.0:
        print "Using scale factor of %f." % factor
        load_scaling()
    

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

    def scale(n):
        if n is None:
            return n

        return int(n * factor)

    def real_bilinear(src, size):
        rv = PygameSurface(size, 0, src)
        old_bilinear(src, rv)
        return rv
        
    def real_transform_scale(surf, size):
        return old_transform_scale(surf, size)

    def image_load_unscaled(f, hint, convert=True):
        rv = old_image_load(f, hint)
        if convert:
            rv = rv.convert_alpha()
        return rv
        
    def surface_scale(full):
        return Surface(old_transform_scale(full, v2p(full.get_size())), wh=full.get_size())

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

    # Proxies a function call from a PygameSurface to a surface.
    def proxy(name):
        func = getattr(PygameSurface, name)
        def rv(self, *args, **kwargs):
            return func(self.surface, *args, **kwargs)
        
    class Surface(object):

        def __init__(self, what, flags=0, sample=None, wh=None):

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
                self.width, self.height = w, h

                w = int(w * factor)
                h = int(h * factor)
                
                if sample is None:
                    sample = screen

                if not isinstance(sample, PygameSurface):
                    sample = sample.surface
                    
                self.surface = PygameSurface((w, h), flags, sample)

        def __repr__(self):
            return "<scale.Surface %r %r>" % (self.get_size(), self.surface)

        def blit(self, s, destpos, sourcerect=None):

            if sourcerect is None:
                self.surface.blit(s.surface, v2p(destpos))
            else:
                self.surface.blit(s.surface, v2p(destpos), v2p(sourcerect))

        def convert(self, *args):
            if args:
                args = (args[0].surface,)            
            return Surface(self.surface.convert(*args), wh=self.get_size())

        def convert_alpha(self, *args):
            if args:
                args = (args[0].surface,)            
            return Surface(self.surface.convert_alpha(*args), wh=self.get_size())

        def copy(self):
            return Surface(self.surface.copy(), wh=self.get_size())

        def fill(self, color):
            self.surface.fill(color)

        def get_alpha(self):
            return self.surface.get_alpha()

        def get_at(self, pos):
            x, y = v2p(pos)
            w, h = self.surface.get_size()
            
            return self.surface.get_at((min(x, w - 1), min(y, h - 1)))


        get_colorkey = proxy("get_colorkey")
        set_colorkey = proxy("set_colorkey")
        get_alpha = proxy("get_alpha")
        set_alpha = proxy("set_alpha")
        get_locked = proxy("get_locked")
        get_locks = proxy("get_locks")
        map_rgb = proxy("map_rgb")
        unmap_rgb = proxy("unmap_rgb")
        get_bytesize = proxy("get_bytesize")
        get_bitsize = proxy("get_bitsize")
        get_flags = proxy("get_flags")
        get_pitch = proxy("get_pitch")
        get_masks = proxy("get_masks")
        set_masks = proxy("set_masks")
        get_shifts = proxy("get_shifts")
        set_shifts = proxy("set_shifts")
        get_losses = proxy("get_losses")
        
        
        def get_bytesize(self):
            return self.surface.get_bytesize()

        def get_bitsize(self):
            return self.surface.get_bitsize()
        
        def get_clip(self):
            return p2v(self.surface.get_clip())

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

        def set_clip(self, rect):
            self.surface.set_clip(v2pplus(rect))
            pass

        def subsurface(self, rect):
            return Surface(self.surface.subsurface(v2p(rect)), wh=rect[2:])

        def mustlock(self):
            return False
        
        def lock(self):
            pass

        def unlock(self):
            pass

        def mustlock(self):
            return False

        def get_locked(self):
            return False

        def get_rect(self, **kwargs):
            rv = self.surface.get_rect()
            rv.size = p2v(rv.size)
            rv.topleft = p2v(rv.topleft)
            for k, v in kwargs.iteritems():
                setattr(rv, k, v)

            return rv
        
    pygame.Surface = Surface

    old_set_mode = pygame.display.set_mode

    def set_mode((w, h), flags, bpp):

        global screen

        width = int(w * factor)
        height = int(h * factor)

        screen = Surface(old_set_mode((width, height), flags, bpp), wh=(w, h))

        return screen

    pygame.display.set_mode = set_mode

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

    old_image_load = pygame.image.load
    old_transform_scale = pygame.transform.scale

    def image_load(*args, **kwargs):

        full = old_image_load(*args, **kwargs)
        return surface_scale(full)

    pygame.image.load = image_load

    def transform_scale(surf, size):

        rv = old_transform_scale(surf.surface, v2p(size))
        rv = Surface(rv, wh=size)

        return rv

    pygame.transform.scale = transform_scale

    old_transform_flip = pygame.transform.flip

    def transform_flip(surf, xbool, ybool):
        return Surface(old_transform_flip(surf.surface, xbool, ybool),
                       wh=surf.get_size())

    pygame.transform.flip = transform_flip

    old_transform_rotate = pygame.transform.rotate

    def transform_rotate(surf, angle):
        return Surface(old_transform_flip(surf.surface, angle))

    pygame.transform.rotate = transform_rotate
    
    old_transform_rotozoom = pygame.transform.rotozoom

    def transform_rotozoom(surf, angle, scale):
        return Surface(old_transform_flip(surf.surface, angle, scale))

    pygame.transform.rotozoom = transform_rotozoom

    # Ignoring scale2x and chop. The former due to a pending api change,
    # the latter due to general uselessness.
        
    PygameFont = font_module.Font

    class Font(object):

        def __init__(self, o, size):
            self.font = PygameFont(o, int(size * factor))

        def render(self, *args):
            return Surface(self.font.render(*args))

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

        # Ignored:
        #
        # set_at
        # Anything involving palettes.
        # Anything involving the parents of subsurfaces.
        # get_pitch, get_shifts, get_losses
                
    font_module.Font = Font

    old_image_save = pygame.image.save

    def image_save(surf, dest):
        surf = old_transform_scale(surf.surface, surf.get_size())
        old_image_save(surf, dest)

    pygame.image.save = image_save

    def image_save_unscaled(surf, dest):
        old_image_save(surf.surface, dest)
    
    old_mouse_get_pos = pygame.mouse.get_pos

    def mouse_get_pos():
        return p2v(old_mouse_get_pos())

    pygame.mouse.get_pos = mouse_get_pos


    if _renpy is not None:
        
        old_save_png = _renpy.save_png
        
        def save_png(surf, dest, compress=-1):
            surf = old_transform_scale(surf.surface, surf.get_size())
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
            old_map(pysrc.surface, pydst.surface, r, g, b, a)

        _renpy.map = map


        old_linmap = _renpy.linmap

        def linmap(pysrc, pydst, r, g, b, a):
            old_linmap(pysrc.surface, pydst.surface, r, g, b, a)

        _renpy.linmap = linmap


        old_bilinear = _renpy.bilinear
        def bilinear(pysrc, pydst, source_xoff=0.0, source_yoff=0.0,
                     source_width=None, source_height=None,
                     dest_xoff=0.0, dest_yoff=0.0, dest_width=None, dest_height=None):

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
                         dest_height=dest_height)

        _renpy.bilinear = bilinear
            

        old_alpha_munge = _renpy.alpha_munge
        

        def alpha_munge(pysrc, pydst, srcchan, dstchan, amap):
            old_alpha_munge(pysrc.surface, pydst.surface,
                            srcchan, dstchan, amap)

        _renpy.alpha_munge = alpha_munge


        old_transform = _renpy.transform

        def transform(pysrc, pydst, corner_x, corner_y,
                      xdx, ydx, xdy, ydy, a=1.0):
            
            old_transform(pysrc.surface, pydst.surface,
                          corner_x * factor, corner_y * factor,
                          xdx, ydx, xdy, ydy, a)
            
        _renpy.transform = transform
            

        old_subpixel = _renpy.subpixel
        
        def subpixel(pysrc, pydst, x, y, shift):
            return old_subpixel(pysrc.surface, pydst.surface, x * factor, y * factor, shift)

        _renpy.subpixel = subpixel

        
        old_blend = _renpy.blend

        def blend(pysrca, pysrcb, pydst, alpha):
            old_blend(pysrca.surface, pysrcb.surface, pydst.surface, alpha)

        _renpy.blend = blend
        
        old_imageblend = _renpy.imageblend

        def imageblend(pysrca, pysrcb, pydst, pyimg, aoff, amap):
            old_imageblend(pysrca.surface, pysrcb.surface, pydst.surface,
                           pyimg.surface, aoff, amap)

        _renpy.imageblend = imageblend


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


    # Now, put everything from this function's namespace into the
    # module namespace.

    globals().update(locals())
    reload(renpy.display.module)
