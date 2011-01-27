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

import renpy
import pygame
import math
import weakref
import time

from renpy.display.render import blit_lock, IDENTITY, BLIT, DISSOLVE, IMAGEDISSOLVE, PIXELLATE

# A map from cached surface to rle version of cached surface.
rle_cache = weakref.WeakKeyDictionary()



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
            target = renpy.display.pgrender.surface((w, h), True)
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
            target = renpy.display.pgrender.surface((w, h), True)
        else:
            target = dest.subsurface((0, 0, w, h))

        ramplen = what.operation_parameter
            
        ramp = "\x00" * 256

        for i in xrange(0, ramplen):
            ramp += chr(255 * i / ramplen)

        ramp += "\xff" * 256

        step = int( what.operation_complete * (256 + ramplen) )
        ramp = ramp[step:step+256]
            
        renpy.display.module.imageblend(
            bottom.subsurface((-x, -y, w, h)),
            top.subsurface((-x, -y, w, h)),
            target,
            image.subsurface((-x, -y, w, h)),
            ramp)

        if what.operation_alpha:
            dest.blit(target, (0, 0))

    elif what.operation == PIXELLATE:

        surf = what.children[0][0].render_to_texture(False)

        px = what.operation_parameter

        renpy.display.module.pixellate(
            surf.subsurface((-x, -y, w, h)),
            dest.subsurface((0, 0, w, h)),
            px, px, px, px)
    
    else:
        raise Exception("Unknown operation: %d" % what.operation)


def draw(dest, what, xo, yo, screen):
    """
    This is the simple draw routine, which only works when alpha is 1.0
    and the matrices are None. If those aren't the case, draw_complex
    is used instead.

    `dest` - The desitnation surface.
    `what` - The Render or Surface we're drawing to.
    `xo` - The X offset.
    `yo` - The Y offset.
    `screen` - True if this is a blit to the screen, False otherwise.    
    """

    if not isinstance(what, renpy.display.render.Render):

        # Pixel-Aligned blit.
        if isinstance(xo, int) and isinstance(yo, int):
            if screen:
                what = rle_cache.get(what, what)

            try:
                blit_lock.acquire()
                dest.blit(what, (xo, yo))
            finally:
                blit_lock.release()
            
        # Subpixel blit.
        else:
            renpy.display.module.subpixel(what, dest, xo, yo)

        return

    # Deal with draw functions.
    if what.operation != BLIT:

        xo = int(xo)
        yo = int(yo)

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

        newdest = dest.subsurface((subx, suby, subw, subh))
        # what.draw_func(newdest, newx, newy)
        draw_special(what, newdest, newx, newy)
            
        return

    # Deal with clipping, if necessary.
    if what.clipping:
        
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
    if what.alpha != 1 or what.forward:
        for child, cxo, cyo, focus, main in what.visible_children:
            draw_transformed(dest, child, xo + cxo, yo + cyo,
                             what.alpha, what.forward, what.reverse)
        return
        
    for child, cxo, cyo, focus, main in what.visible_children:
        draw(dest, child, xo + cxo, yo + cyo, screen)

def draw_transformed(dest, what, xo, yo, alpha, forward, reverse):

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

        if minx > dw or miny > dh:
            return
            
        cx, cy = forward.transform(minx - xo, miny - yo)

        dest = dest.subsurface((minx, miny, maxx - minx, maxy - miny))

        renpy.display.module.transform(
            what, dest,
            cx, cy,
            forward.xdx, forward.ydx,
            forward.xdy, forward.ydy,
            alpha, True)

        return

    if what.clipping and False:

        if reverse.xdy or reverse.ydx:        
            draw_transformed(dest, what.pygame_surface(True), xo, yo, alpha, forward, reverse)
            return
            

            # raise Exception("Non-axis-aligned clipping is not supported.")


        
        width = what.width * reverse.xdx
        height = what.height * reverse.ydy

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
        
        
    if what.draw_func:
        child = what.pygame_surface(True)
        draw_transformed(dest, child, xo, yo, alpha, forward, reverse)
        
        # raise Exception("Using a draw_func on a transformed surface is not supported.")

    for child, cxo, cyo, focus, main in what.visible_children:

        cxo, cyo = reverse.transform(cxo, cyo)

        if what.forward:
            child_forward = forward * what.forward
            child_reverse = what.reverse * reverse
        else:
            child_forward = forward
            child_reverse = reverse
            
        draw_transformed(dest, child, xo + cxo, yo + cyo, alpha * what.alpha, child_forward, child_reverse)


def do_draw_screen(screen_render, full_redraw):
    """
    Draws the render produced by render_screen to the screen.
    """

    screen_render.is_opaque()

    screen = pygame.display.get_surface()
    w, h = screen.get_size()
    
    draw(screen, screen_render, 0, 0, True)

    return [ (0, 0, w, h) ]


class SWDraw(object):
    """
    This uses the software renderer to draw to the screen.
    """

    def __init__(self):
        
        # Should we draw the screen?
        self.suppressed_blit = False

        # The earliest time at which the next frame can be redrawn.
        self.next_frame = 0

        # Mouse re-drawing.
        self.mouse_location = None
        self.mouse_backing = None
        self.mouse_backing_pos = None
        self.mouse_info = None
        
        
        # Is the mouse currently visible?
        self.mouse_old_visible = None

        # This is used to cache the surface->texture operation.
        self.texture_cache = weakref.WeakKeyDictionary()

        # This is used to display video to the screen.
        self.fullscreen_surface = None

        # Info.
        self.info = { "renderer" : "sw" }

        pygame.display.init()
        renpy.display.interface.post_init()
        
        # Scaling?
        renpy.display.scale.init()
        
        
    def set_mode(self, virtual_size, physical_size, fullscreen):

        width, height = virtual_size
        fsflag = 0

        if fullscreen:
            fsflag = pygame.FULLSCREEN
              
        # If a window exists of the right size and flags, use it. Otherwise,
        # make our own window.
        old_window = pygame.display.get_surface()

        if ((old_window is not None) and 
            (old_window.get_size() == (width, height)) and
            (old_window.get_flags() & pygame.FULLSCREEN == fsflag)):
            
            self.window = old_window
                    
        else:
            self.window = renpy.display.pgrender.set_mode(
                (width, height),
                fsflag,
                32)
            
        # Should we redraw the screen from scratch?
        self.full_redraw = True

        # The surface used to display fullscreen video.
        self.fullscreen_surface = renpy.display.scale.real(self.window)

        # Reset this on a mode change.
        self.mouse_location = None
        self.mouse_backing = None
        self.mouse_backing_pos = None
        self.mouse_info = None

        return True
        

    # private
    def show_mouse(self, pos, info):
        """
        Actually shows the mouse.
        """

        self.mouse_location = pos
        self.mouse_info = info

        mxo, myo, tex = info
        
        mx, my = pos
        mw, mh = tex.get_size()

        bx = mx - mxo
        by = my - myo

        self.mouse_backing_pos = (bx, by)
        self.mouse_backing = renpy.display.pgrender.surface((mw, mh), False)
        self.mouse_backing.blit(self.window, (0, 0), (bx, by, mw, mh))

        self.window.blit(tex, (bx, by))

        return bx, by, mw, mh

    # private
    def hide_mouse(self):
        """
        Actually hides the mouse.
        """
        
        size = self.mouse_backing.get_size()
        self.window.blit(self.mouse_backing, self.mouse_backing_pos)

        rv = self.mouse_backing_pos + size

        self.mouse_backing = None
        self.mouse_backing_pos = None
        self.mouse_location = None 

        return rv

    # private
    def draw_mouse(self, show_mouse):
        """
        This draws the mouse to the screen, if necessary. It uses the
        buffer to minimize the amount of the screen that needs to be
        drawn, and only redraws if the mouse has actually been moved.
        """

        hardware, x, y, tex = renpy.game.interface.get_mouse_info()
        
        if self.mouse_old_visible != hardware:
            pygame.mouse.set_visible(hardware)
            self.mouse_old_visible = hardware

        # The rest of this is for the software mouse.
        
        if self.suppressed_blit:
            return [ ]

        if not show_mouse:
            tex = None

        info = (x, y, tex)
        pos = pygame.mouse.get_pos()
            
        if (pos == self.mouse_location and tex and info == self.mouse_info):
            return [ ]

        updates = [ ]

        if self.mouse_location:
            updates.append(self.hide_mouse())
            
        if tex and pos and renpy.game.interface.focused:
            updates.append(self.show_mouse(pos, info))
            
        return updates

    def update_mouse(self):
        """
        Draws the mouse, and then updates the screen.
        """
        
        updates = self.draw_mouse(True)

        if updates:
            pygame.display.update(updates)
            
    def mouse_event(self, ev):        
        x, y = getattr(ev, 'pos', pygame.mouse.get_pos())
        return x, y
        
    def get_mouse_pos(self):
        return pygame.mouse.get_pos()
    
    def screenshot(self):
        """
        Returns a pygame surface containing a screenshot.
        """

        return self.window
    
    def should_redraw(self, needs_redraw, first_pass):
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


    def draw_screen(self, surftree, fullscreen_video):
        """
        Draws the screen. 
        """
        
        if not fullscreen_video:

            updates = [ ]

            updates.extend(self.draw_mouse(False))

            damage = do_draw_screen(surftree, self.full_redraw)

            if damage:
                updates.extend(damage)

            self.full_redraw = False

            updates.extend(self.draw_mouse(True))
            pygame.display.update(updates)
            
        else:
            pygame.display.flip()
            self.full_redraw = True

        self.suppressed_blit = fullscreen_video

        
    def render_to_texture(self, render, alpha):
        rv = renpy.display.pgrender.surface((render.width, render.height), alpha)
        draw(rv, render, 0, 0, False)

        return rv

    def is_pixel_opaque(self, what, x, y):

        if x < 0 or y < 0 or x >= what.width or y >= what.height:
            return 0

        for (child, xo, yo, focus, main) in what.visible_children:
            cx = x - xo
            cy = y - yo

            if what.forward:
                cx, cy = what.forward.transform(cx, cy)


            if isinstance(child, renpy.display.render.Render):
                if self.is_pixel_opaque(child, x, y):
                    return True

            else:
                cw, ch = child.get_size()
                if cx >= cw or cy >= ch:
                    return False

                if not child.get_masks()[3] or child.get_at((cx, cy))[3]:
                    return True

        return False

    
    def mutated_surface(self, surf):
        """
        Called to indicate that the given surface has changed.
        """

        if surf in rle_cache:
            del rle_cache[surf]
            
            
    def load_texture(self, surf, transient=False):
        """
        Creates a texture from the surface. In the software implementation,
        the only difference between a texture and a surface is that a texture
        is in the RLE cache.
        """

        if transient:
            return surf

        if renpy.game.less_memory:
            return surf

        if surf not in rle_cache:
            rle_surf = renpy.display.pgrender.copy_surface(surf)
            rle_surf.set_alpha(255, pygame.RLEACCEL)
            self.mutated_surface(rle_surf)

            rle_cache[surf] = rle_surf
        
        return surf

        
    def free_memory(self):
        """
        Frees up memory.
        """

        rle_cache.clear()
        
    def deinit(self):
        """
        Called when we're restarted.
        """

        renpy.display.render.free_memory()
        
        return
        
    def quit(self):
        """
        Shuts down the drawing system.
        """

        pygame.display.quit()
        
        return
            
    def event_peek_sleep(self):
        """
        Wait a little bit so the CPU doesn't speed up.
        """

        time.sleep(.0001)
        
