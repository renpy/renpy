# Copyright 2004-2024 Tom Rothamel <pytom@bishoujo.us>
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

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode # *



import math
import time
import os

import pygame_sdl2 as pygame
import renpy
from renpy.display.render import blit_lock, IDENTITY, BLIT, DISSOLVE, IMAGEDISSOLVE, PIXELLATE, FLATTEN


class Clipper(object):
    """
    This is used to calculate the clipping rectangle and update rectangles
    used for a particular draw of the screen.
    """

    def __init__(self):

        # Lists of (x0, y0, x1, y1, clip, surface, transform) tuples,
        # representing how a displayable is drawn to the screen.
        self.blits = [ ]
        self.old_blits = [ ]

        # Sets of (x0, y0, x1, y1) tuples, representing areas that
        # aren't part of any displayable.
        self.forced = set()
        self.old_forced = set()

        # The set of surfaces that have been mutated recently.
        self.mutated = set()

    def compute(self, full_redraw):
        """
        This returns a clipping rectangle, and a list of update rectangles
        that cover the changes between the old and new frames.
        """

        # First, get things out of the fields, and update them. This
        # allows us to just return without having to do any cleanup
        # code.
        bl0 = self.old_blits
        bl1 = self.blits
        old_forced = self.old_forced
        forced = self.forced
        mutated = self.mutated

        self.old_blits = bl1
        self.blits = [ ]
        self.old_forced = forced
        self.forced = set()
        self.mutated = set()

        sw = renpy.config.screen_width
        sh = renpy.config.screen_height
        sa = sw * sh

        # A tuple representing the size of the fullscreen.
        fullscreen = (0, 0, sw, sh)

        # Check to see if a full redraw has been forced, and return
        # early.
        if full_redraw:
            return fullscreen, [ fullscreen ]

        # Quick checks to see if a dissolve is happening, or something like
        # that.
        changes = forced | old_forced

        if fullscreen in changes:
            return fullscreen, [ fullscreen ]

        # Compute the differences between the two sets, and add those
        # to changes.
        i0 = 0
        i1 = 0
        bl1set = set(bl1)

        while True:
            if i0 >= len(bl0) or i1 >= len(bl1):
                break

            b0 = bl0[i0]
            b1 = bl1[i1]

            if b0 == b1:
                if id(b0[5]) in mutated:
                    changes.add(b0[:5])

                i0 += 1
                i1 += 1

            elif b0 not in bl1set:
                changes.add(b0[:5])
                i0 += 1

            else:
                changes.add(b1[:5])
                i1 += 1

        changes.update(i[:5] for i in bl0[i0:])
        changes.update(i[:5] for i in bl1[i1:])

        # No changes? Quit.
        if not changes:
            return None, [ ]

        # Compute the sizes of the updated rectangles.
        sized = [ ]

        for x0, y0, x1, y1, (sx0, sy0, sx1, sy1) in changes:

            # Round up by a pixel, to prevent visual artifacts when scaled down.
            x1 += 1
            y1 += 1

            if x0 < sx0:
                x0 = sx0
            if y0 < sy0:
                y0 = sy0
            if x1 > sx1:
                x1 = sx1
            if y1 > sy1:
                y1 = sy1

            w = x1 - x0
            h = y1 - y0

            if w <= 0 or h <= 0:
                continue

            area = w * h

            if area >= sa:
                return fullscreen, [ fullscreen ]

            sized.append((area, x0, y0, x1, y1))

        sized.sort()

        # The list of non-contiguous updates.
        noncont = [ ]

        # The total area of noncont.
        nca = 0

        # Pick the largest area, merge with all overlapping smaller areas, repeat
        # until no merge possible.
        while sized:
            area, x0, y0, x1, y1 = sized.pop()

            merged = False

            if nca + area >= sa:
                return (0, 0, sw, sh), [ (0, 0, sw, sh) ]

            i = 0

            while i < len(sized):
                _iarea, ix0, iy0, ix1, iy1 = sized[i]

                if (x0 <= ix0 <= x1 or x0 <= ix1 <= x1) and \
                   (y0 <= iy0 <= y1 or y0 <= iy1 <= y1):

                    merged = True
                    x0 = min(x0, ix0)
                    x1 = max(x1, ix1)
                    y0 = min(y0, iy0)
                    y1 = max(y1, iy1)

                    area = (x1 - x0) * (y1 - y0)

                    sized.pop(i)

                else:
                    i += 1

            if merged:
                sized.append((area, x0, y0, x1, y1))
            else:
                noncont.append((x0, y0, x1, y1))
                nca += area

        if not noncont:
            return None, [ ]

        x0, y0, x1, y1 = noncont.pop()
        x0 = int(x0)
        y0 = int(y0)
        x1 = int(math.ceil(x1))
        y1 = int(math.ceil(y1))

        # A list of (x, y, w, h) tuples for each update.
        updates = [ (x0, y0, x1 - x0, y1 - y0) ]

        for ix0, iy0, ix1, iy1 in noncont:

            ix0 = int(ix0)
            iy0 = int(iy0)
            ix1 = int(math.ceil(ix1))
            iy1 = int(math.ceil(iy1))

            x0 = min(x0, ix0)
            y0 = min(y0, iy0)
            x1 = max(x1, ix1)
            y1 = max(y1, iy1)

            updates.append((ix0, iy0, ix1 - ix0, iy1 - iy0))

        return (x0, y0, x1 - x0, y1 - y0), updates


clippers = [ Clipper() ]


def surface(w, h, alpha):
    """
    Creates a surface that shares a pixel format with the screen. The created
    surface will
    """

    if alpha:
        rv = pygame.Surface((w + 4, h + 4), pygame.SRCALPHA)
    else:
        rv = pygame.Surface((w + 4, h + 4), 0)

    return rv.subsurface((2, 2, w, h))


def copy_surface(surf):
    w, h = surf.get_size()
    rv = surface(w, h, True)

    renpy.display.accelerator.nogil_copy(surf, rv) # @UndefinedVariable
    return rv


def draw_special(what, dest, x, y):
    """
    This handles the special drawing operations, such as dissolve and
    image dissolve. `x` and `y` are the offsets of the thing to be drawn
    relative to the destination rectangle, and are always negative.
    """

    dw, dh = dest.get_size()

    w = min(dw, what.width + x)
    h = min(dh, what.height + y)

    if w <= 0 or h <= 0:
        return

    if what.operation == DISSOLVE:

        bottom = what.children[0][0].render_to_texture(True)
        top = what.children[1][0].render_to_texture(True)

        if what.operation_alpha:
            target = surface(w, h, True)
        else:
            target = dest.subsurface((0, 0, w, h))

        renpy.display.module.blend(
            bottom.subsurface((-x, -y, w, h)),
            top.subsurface((-x, -y, w, h)),
            target,
            int(what.operation_complete * 255))

        if what.operation_alpha:
            dest.blit(target, (0, 0))

    elif what.operation == IMAGEDISSOLVE:

        image = what.children[0][0].render_to_texture(True)
        bottom = what.children[1][0].render_to_texture(True)
        top = what.children[2][0].render_to_texture(True)

        if what.operation_alpha:
            target = surface(w, h, True)
        else:
            target = dest.subsurface((0, 0, w, h))

        ramplen = what.operation_parameter

        ramp = b"\x00" * 256

        for i in range(0, ramplen):
            ramp += bchr(255 * i // ramplen)

        ramp += b"\xff" * 256

        step = int(what.operation_complete * (256 + ramplen))
        ramp = ramp[step:step + 256]

        renpy.display.module.imageblend(
            bottom.subsurface((-x, -y, w, h)),
            top.subsurface((-x, -y, w, h)),
            target,
            image.subsurface((-x, -y, w, h)),
            ramp)

        if what.operation_alpha:
            dest.blit(target, (0, 0))

    elif what.operation == PIXELLATE:

        surf = what.children[0][0].render_to_texture(dest.get_masks()[3])

        px = what.operation_parameter

        renpy.display.module.pixellate(
            surf.subsurface((-x, -y, w, h)),
            dest.subsurface((0, 0, w, h)),
            px, px, px, px)

    elif what.operation == FLATTEN:
        surf = what.children[0][0].render_to_texture(dest.get_masks()[3])
        dest.subsurface((0, 0, w, h)).blit(surf, (0, 0))

    else:
        raise Exception("Unknown operation: %d" % what.operation)


def draw(dest, clip, what, xo, yo, screen):
    """
    This is the simple draw routine, which only works when alpha is 1.0
    and the matrices are None. If those aren't the case, draw_complex
    is used instead.

    `dest` - Either a destination surface, or a clipper.
    `clip` - If None, we should draw. Otherwise we should clip, and this is
    the rectangle to clip to.
    `what` - The Render or Surface we're drawing to.
    `xo` - The X offset.
    `yo` - The Y offset.
    `screen` - True if this is a blit to the screen, False otherwise.
    """

    if not isinstance(what, renpy.display.render.Render):

        # Pixel-Aligned blit.
        if isinstance(xo, int) and isinstance(yo, int):

            if clip:
                w, h = what.get_size()
                dest.blits.append((xo, yo, xo + w, yo + h, clip, what, None))
            else:
                try:
                    blit_lock.acquire()
                    dest.blit(what, (xo, yo))
                finally:
                    blit_lock.release()

        # Subpixel blit.
        else:
            if clip:
                w, h = what.get_size()
                dest.blits.append((xo, yo, xo + w, yo + h, clip, what, None))
            else:
                renpy.display.module.subpixel(what, dest, xo, yo)

        return

    if what.text_input:
        renpy.display.interface.text_rect = what.screen_rect(xo, yo, None)

    # Deal with draw functions.
    if what.operation != BLIT:

        xo = int(xo)
        yo = int(yo)

        if clip:
            dx0, dy0, dx1, dy1 = clip
            dw = dx1 - dx0
            dh = dy1 - dy0
        else:
            dw, dh = dest.get_size()

        if xo >= 0:
            newx = 0
            subx = xo
        else:
            newx = xo
            subx = 0

        if yo >= 0:
            newy = 0
            suby = yo
        else:
            newy = yo
            suby = 0

        if subx >= dw or suby >= dh:
            return

        # newx and newy are the offset of this render relative to the
        # subsurface. They can only be negative or 0, as otherwise we
        # would make a smaller subsurface.

        subw = min(dw - subx, what.width + newx)
        subh = min(dh - suby, what.height + newy)

        if subw <= 0 or subh <= 0:
            return

        if clip:
            dest.forced.add((subx, suby, subx + subw, suby + subh, clip))
        else:
            newdest = dest.subsurface((subx, suby, subw, subh))
            draw_special(what, newdest, newx, newy)

        return

    # Deal with clipping, if necessary.
    if what.xclipping or what.yclipping:

        if clip:
            cx0, cy0, cx1, cy1 = clip

            cx0 = max(cx0, xo)
            cy0 = max(cy0, yo)
            cx1 = min(cx1, xo + what.width)
            cy1 = min(cy1, yo + what.height)

            if cx0 > cx1 or cy0 > cy1:
                return

            clip = (cx0, cy0, cx1, cy1)

            dest.forced.add(clip + (clip,))
            return

        else:

            # After this code, x and y are the coordinates of the subsurface
            # relative to the destination. xo and yo are the offset of the
            # upper-left corner relative to the subsurface.

            if xo >= 0:
                x = xo
                xo = 0
            else:
                x = 0
                # xo = xo

            if yo >= 0:
                y = yo
                yo = 0
            else:
                y = 0
                # yo = yo

            dw, dh = dest.get_size()

            width = min(dw - x, what.width + xo)
            height = min(dh - y, what.height + yo)

            if width < 0 or height < 0:
                return

            dest = dest.subsurface((x, y, width, height))

    # Deal with alpha and transforms by passing them off to draw_transformed.
    if what.alpha != 1 or what.over != 1.0 or (what.forward is not None and what.forward is not IDENTITY):
        for child, cxo, cyo, _focus, _main in what.children:
            draw_transformed(dest, clip, child, xo + cxo, yo + cyo,
                             what.alpha * what.over, what.forward, what.reverse)
        return

    for child, cxo, cyo, _focus, _main in what.children:
        draw(dest, clip, child, xo + cxo, yo + cyo, screen)


def draw_transformed(dest, clip, what, xo, yo, alpha, forward, reverse):

    # If our alpha has hit 0, don't do anything.
    if alpha <= 0.003: # (1 / 256)
        return

    if forward is None:
        forward = IDENTITY
        reverse = IDENTITY

    if not isinstance(what, renpy.display.render.Render):

        # Figure out where the other corner of the transformed surface
        # is on the screen.
        sw, sh = what.get_size()
        if clip:

            dx0, dy0, dx1, dy1 = clip
            dw = dx1 - dx0
            dh = dy1 - dy0

        else:
            dw, dh = dest.get_size()

        x0, y0 = 0.0, 0.0
        x1, y1 = reverse.transform(sw, 0.0)
        x2, y2 = reverse.transform(sw, sh)
        x3, y3 = reverse.transform(0.0, sh)

        minx = math.floor(min(x0, x1, x2, x3) + xo)
        maxx = math.ceil(max(x0, x1, x2, x3) + xo)
        miny = math.floor(min(y0, y1, y2, y3) + yo)
        maxy = math.ceil(max(y0, y1, y2, y3) + yo)

        if minx < 0:
            minx = 0
        if miny < 0:
            miny = 0

        if maxx > dw:
            maxx = dw
        if maxy > dh:
            maxy = dh

        if minx > dw or miny > dh or maxx < 0 or maxy < 0:
            return

        cx, cy = forward.transform(minx - xo, miny - yo)

        if clip:

            dest.blits.append(
                (minx, miny, maxx + dx0, maxy + dy0, clip, what, # type: ignore
                 (cx, cy,
                  forward.xdx, forward.ydx,
                  forward.xdy, forward.ydy,
                  alpha)))

        else:

            dest = dest.subsurface((minx, miny, maxx - minx, maxy - miny))

            renpy.display.module.self(
                what, dest,
                cx, cy,
                forward.xdx, forward.ydx,
                forward.xdy, forward.ydy,
                alpha, True)

        return

    if what.text_input:
        renpy.display.interface.text_rect = what.screen_rect(xo, yo, reverse)

    if what.xclipping or what.yclipping:

        if reverse.xdy or reverse.ydx:
            draw_transformed(dest, clip, what.pygame_surface(True), xo, yo, alpha, forward, reverse)
            return

        width = what.width * reverse.xdx
        height = what.height * reverse.ydy

        if clip:
            cx0, cy0, cx1, cy1 = clip

            cx0 = max(cx0, xo)
            cy0 = max(cy0, yo)
            cx1 = min(cx1, xo + width)
            cy1 = min(cy1, yo + height)

            if cx0 > cx1 or cy0 > cy1:
                return

            clip = (cx0, cy0, cx1, cy1)

            dest.forced.add(clip + (clip,))
            return

        else:

            # After this code, x and y are the coordinates of the subsurface
            # relative to the destination. xo and yo are the offset of the
            # upper-left corner relative to the subsurface.

            if xo >= 0:
                x = xo
                xo = 0
            else:
                x = 0
                # xo = xo

            if yo >= 0:
                y = yo
                yo = 0
            else:
                y = 0
                # yo = yo

            dw, dh = dest.get_size()

            width = min(dw - x, width + xo)
            height = min(dh - y, height + yo)

            if width < 0 or height < 0:
                return

            dest = dest.subsurface((x, y, width, height))

    if what.operation != BLIT:
        child = what.pygame_surface(True)
        draw_transformed(dest, clip, child, xo, yo, alpha, forward, reverse)
        return

    for child, cxo, cyo, _focus, _main in what.children:

        cxo, cyo = reverse.transform(cxo, cyo)

        if what.forward:
            child_forward = what.forward * forward
            child_reverse = reverse * what.reverse
        else:
            child_forward = forward
            child_reverse = reverse

        draw_transformed(dest, clip, child, xo + cxo, yo + cyo, alpha * what.alpha * what.over, child_forward, child_reverse)


def do_draw_screen(screen_render, full_redraw, swdraw):
    """
    Draws the render produced by render_screen to the screen.
    """

    yoffset = xoffset = 0

    clip = (xoffset, yoffset, xoffset + screen_render.width, yoffset + screen_render.height)
    clipper = clippers[0]

    draw(clipper, clip, screen_render, xoffset, yoffset, True)

    cliprect, updates = clipper.compute(full_redraw)

    if cliprect is None:
        return [ ]

    x, y, _w, _h = cliprect

    dest = swdraw.window.subsurface(cliprect)
    draw(dest, None, screen_render, -x, -y, True)

    return updates


class SWDraw(object):
    """
    This uses the software renderer to draw to the screen.
    """

    def __init__(self):
        self.display_info = None

        self.reset()

    def reset(self):

        # Should we draw the screen?
        self.suppressed_blit = False

        # The earliest time at which the next frame can be redrawn.
        self.next_frame = 0

        # Info.
        self.info = { "renderer" : "sw", "resizable" : False, "additive" : False }

        if self.display_info is None:
            self.display_info = renpy.display.get_info()

        # The scale factor we use for this display.
        self.scale_factor = 1.0

        # The screen returned to us from pygame.
        self.screen = None

        # The window that we render into, if not the screen. This has a
        # 1px border around it iff we're scaling.
        self.window = None

    def get_texture_size(self):
        return 0, 0

    def init(self, virtual_size):

        # These disable a failed load of ANGLE.
        pygame.display.gl_reset_attributes()
        pygame.display.hint("SDL_OPENGL_ES_DRIVER", "0")

        # Reset before resize.
        self.reset()

        width, height = virtual_size

        # Set up scaling, if necessary.
        screen_width = self.display_info.current_w # type: ignore
        screen_height = self.display_info.current_h # type: ignore

        scale_factor = min(1.0 * screen_width / width, 1.0 * screen_height / height, 1.0)
        if "RENPY_SCALE_FACTOR" in os.environ:
            scale_factor = float(os.environ["RENPY_SCALE_FACTOR"])
        self.scale_factor = scale_factor

        # Don't reuse the old screen, because doing so fails to update
        # properly on Xorg.

        scaled_width = int(width * scale_factor)
        scaled_height = int(height * scale_factor)

        self.screen = pygame.display.set_mode((scaled_width, scaled_height), 0, 32)

        if scale_factor != 1.0:
            self.window = surface(width, height, True)
        else:
            self.window = self.screen

        renpy.display.pgrender.set_rgba_masks()

        # Scale from the rtt size to the virtual size.
        self.draw_per_virt = 1.0
        self.virt_to_draw = renpy.display.render.Matrix2D(self.draw_per_virt, 0, 0, self.draw_per_virt)
        self.draw_to_virt = renpy.display.render.Matrix2D(1.0 / self.draw_per_virt, 0, 0, 1.0 / self.draw_per_virt)

        # Should we redraw the screen from scratch?
        self.full_redraw = True

        # The surface used to display fullscreen video.
        self.fullscreen_surface = self.screen

        return True

    def update(self, force=True):
        renpy.game.preferences.fullscreen = False

    def resize(self):
        return

    def quit(self): # @ReservedAssignment
        return

    def translate_point(self, x, y):
        x /= self.scale_factor
        y /= self.scale_factor
        return (x, y)

    def untranslate_point(self, x, y):
        x *= self.scale_factor
        y *= self.scale_factor
        return (x, y)

    def mouse_event(self, ev):
        x, y = getattr(ev, 'pos', pygame.mouse.get_pos()) # type: ignore

        x /= self.scale_factor
        y /= self.scale_factor

        return x, y

    def get_mouse_pos(self):
        x, y = pygame.mouse.get_pos()

        x /= self.scale_factor
        y /= self.scale_factor

        return x, y

    def set_mouse_pos(self, x, y):

        x *= self.scale_factor
        y *= self.scale_factor

        return pygame.mouse.set_pos([x, y])

    def screenshot(self, surftree):
        """
        Returns a pygame surface containing a screenshot.
        """

        return self.window

    def can_block(self):
        return True

    def should_redraw(self, needs_redraw, first_pass, can_block):
        """
        Uses the framerate to determine if we can and should redraw.
        """

        if not needs_redraw:
            return False

        framerate = renpy.config.framerate

        if framerate is None:
            return True

        next_frame = self.next_frame
        now = pygame.time.get_ticks()

        frametime = 1000.0 / framerate

        # Handle timer rollover.
        if next_frame > now + frametime:
            next_frame = now

        # It's not yet time for the next frame.
        if now < next_frame and not first_pass:
            return False

        # Otherwise, it is. Schedule the next frame.
        # if next_frame + frametime < now:
        next_frame = now + frametime
        # else:
        #    next_frame += frametime

        self.next_frame = next_frame

        return True

    def draw_screen(self, surftree):
        """
        Draws the screen.
        """

        updates = [ ]

        damage = do_draw_screen(surftree, self.full_redraw, self)

        if damage:
            updates.extend(damage)

        self.full_redraw = False

        if self.window is self.screen:

            pygame.display.update(updates)

        else:
            renpy.display.scale.smoothscale(self.window, self.screen.get_size(), self.screen)

            pygame.display.flip()

    def render_to_texture(self, render, alpha):

        rv = surface(render.width, render.height, alpha)
        draw(rv, None, render, 0, 0, False)

        return rv

    def is_pixel_opaque(self, what):
        """
        Not implemented for swdraw - always return True.
        """

        return True

    def mutated_surface(self, surf):
        """
        Called to indicate that the given surface has changed.
        """

        for i in clippers:
            i.mutated.add(id(surf))

    def load_texture(self, surf, transient=False, properties={}):
        """
        Creates a texture from the surface. In the software implementation,
        the only difference between a texture and a surface is that a texture
        is in the RLE cache.
        """

        return surf.convert_alpha(self.screen)

    def ready_one_texture(self):
        return False

    def solid_texture(self, w, h, color):
        """
        Creates a texture filled to the edges with color.
        """

        surf = surface(w + 4, h + 4, True)
        surf.fill(color)
        self.mutated_surface(surf)

        surf = surf.subsurface((2, 2, w, h))

        self.mutated_surface(surf)
        return surf

    def kill_textures(self):
        """
        Kills all textures and caches of textures.
        """

    def event_peek_sleep(self):
        """
        Wait a little bit so the CPU doesn't speed up.
        """

        time.sleep(.0001)

    def get_physical_size(self):
        """
        Return the physical width and height of the screen.
        """
        return renpy.config.screen_width, renpy.config.screen_height
