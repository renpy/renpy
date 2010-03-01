import renpy
import pygame
import cStringIO
import math

from renpy.display.render import blit_lock, IDENTITY, BLIT, DISSOLVE, IMAGEDISSOLVE, PIXELLATE

# A map from id(cached surface) to rle version of cached surface.
rle_cache = { }

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
                iarea, ix0, iy0, ix1, iy1 = sized[i] 

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

        bottom = what.children[0][0].render_to_texture(what.operation_alpha)
        top = what.children[1][0].render_to_texture(what.operation_alpha)

        if what.operation_alpha:
            target = renpy.display.pgrender.surface((w, h), True)
        else:
            target = dest.subsurface((0, 0, w, h))
        
        renpy.display.module.blend(
            bottom.subsurface((-x, -y, w, h)),
            top.subsurface((-x, -y, w, h)),
            target,
            what.operation_complete)

        if what.operation_alpha:
            dest.blit(target, (0, 0))

    elif what.operation == IMAGEDISSOLVE:

        image = what.children[0][0].render_to_texture(what.operation_alpha)
        bottom = what.children[1][0].render_to_texture(what.operation_alpha)
        top = what.children[2][0].render_to_texture(what.operation_alpha)

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
            if screen:
                what = rle_cache.get(id(what), what)

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
            # what.draw_func(newdest, newx, newy)
            draw_special(what, newdest, newx, newy)

            
        return

    # Deal with clipping, if necessary.
    if what.clipping:
        
        if clip:
            cx0, cy0, cx1, cy1 = clip

            cx0 = max(cx0, xo)
            cy0 = max(cy0, yo)
            cx1 = min(cx1, xo + what.width)
            cy1 = min(cy1, yo + what.height)

            if cx0 > cx1 or cy0 > cy1:
                return
            
            clip = (cx0, cy0, cx1, cy1)

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
    if what.alpha != 1 or what.forward:
        for child, cxo, cyo, focus, main in what.visible_children:
            draw_transformed(dest, clip, child, xo + cxo, yo + cyo,
                             what.alpha, what.forward, what.reverse)
        return
        
    for child, cxo, cyo, focus, main in what.visible_children:
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

        if minx > dw or miny > dh:
            return
            
        cx, cy = forward.transform(minx - xo, miny - yo)

        if clip:

            dest.blits.append(
                (minx, miny, maxx + dx0, maxy + dy0, clip, what,
                 (cx, cy,
                  forward.xdx, forward.ydx,
                  forward.xdy, forward.ydy,
                  alpha)))

        else:
            dest = dest.subsurface((minx, miny, maxx - minx, maxy - miny))
            
            renpy.display.module.transform(
                what, dest,
                cx, cy,
                forward.xdx, forward.ydx,
                forward.xdy, forward.ydy,
                alpha, True)

        return

    if what.clipping:

        if reverse.xdy or reverse.ydx:        
            draw_transformed(dest, clip, what.pygame_surface(True), xo, yo, alpha, forward, reverse)
            return
            

            # raise Exception("Non-axis-aligned clipping is not supported.")


        
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
        
        
    if what.draw_func:
        child = what.pygame_surface(True)
        draw_transformed(dest, clip, child, xo, yo, alpha, forward, reverse)
        
        # raise Exception("Using a draw_func on a transformed surface is not supported.")

    for child, cxo, cyo, focus, main in what.visible_children:

        cxo, cyo = reverse.transform(cxo, cyo)

        if what.forward:
            child_forward = forward * what.forward
            child_reverse = what.reverse * reverse
        else:
            child_forward = forward
            child_reverse = reverse
            
        draw_transformed(dest, clip, child, xo + cxo, yo + cyo, alpha * what.alpha, child_forward, child_reverse)



def do_draw_screen(screen_render, full_redraw):
    """
    Draws the render produced by render_screen to the screen.
    """

    yoffset = xoffset = 0    
    
    screen_render.is_opaque()

    clip = (xoffset, yoffset, xoffset + screen_render.width, yoffset + screen_render.height)
    clipper = clippers[0]

    draw(clipper, clip, screen_render, xoffset, yoffset, True)

    cliprect, updates = clipper.compute(full_redraw)

    if cliprect is None:
        return [ ]

    x, y, w, h = cliprect

    dest = pygame.display.get_surface().subsurface(cliprect)
    draw(dest, None, screen_render, -x, -y, True)

    return updates


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
        self.mouse_old_visible = True

        # The time of the last mouse event.
        self.mouse_event_time = renpy.display.core.get_time()

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

        return True
        

    # private
    def show_mouse(self, pos, info):
        """
        Actually shows the mouse.
        """

        self.mouse_location = pos
        self.mouse_info = info

        img, mxo, myo = info
        
        mouse = renpy.display.im.load_image(img)

        mx, my = pos
        mw, mh = mouse.get_size()

        bx = mx - mxo
        by = my - myo

        self.mouse_backing_pos = (bx, by)
        self.mouse_backing = renpy.display.pgrender.surface((mw, mh), False)
        self.mouse_backing.blit(self.window, (0, 0), (bx, by, mw, mh))

        self.window.blit(mouse, (bx, by))

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
    def draw_mouse(self, show_mouse=True):
        """
        This draws the mouse to the screen, if necessary. It uses the
        buffer to minimize the amount of the screen that needs to be
        drawn, and only redraws if the mouse has actually been moved.
        """

        # Figure out if the mouse visibility algorithm is hiding the mouse.
        if self.mouse_event_time + renpy.config.mouse_hide_time < renpy.display.core.get_time():
            visible = False
        else:
            visible = renpy.store.mouse_visible and (not renpy.game.less_mouse)
            
        # Deal with a hardware mouse, the easy way.
        if not renpy.config.mouse:

            if self.mouse_old_visible != visible:
                pygame.mouse.set_visible(visible)
                self.mouse_old_visible = visible
            
            return [ ]

        # The rest of this is for the software mouse.
        
        if self.suppressed_blit:
            return [ ]

        visible = show_mouse and visible
        
        mouse_kind = renpy.display.focus.get_mouse() or self.interface.mouse 
        
        # Figure out the mouse animation.
        if mouse_kind in renpy.config.mouse:
            anim = renpy.config.mouse[mouse_kind]
        else:
            anim = renpy.config.mouse[getattr(renpy.store, 'default_mouse', 'default')]

        info = anim[self.interface.ticks % len(anim)]

        pos = pygame.mouse.get_pos()

        if not renpy.game.interface.focused:
            pos = None
            
        if (pos == self.mouse_location and
            show_mouse and
            info == self.mouse_info):
            
            return [ ]

        updates = [ ]

        if self.mouse_location:
            updates.append(self.hide_mouse())
            
        if visible and pos and renpy.game.interface.focused:
            updates.append(self.show_mouse(pos, info))
            
        return updates


    def update_mouse(self):
        """
        Draws the mouse, and then updates the screen.
        """
        
        updates = self.draw_mouse()

        if updates:
            pygame.display.update(updates)

    
    def mouse_event(self, ev):

        if ev.type == pygame.MOUSEMOTION or \
                ev.type == pygame.MOUSEBUTTONDOWN or \
                ev.type == pygame.MOUSEBUTTONUP:
            
            self.mouse_event_time = renpy.display.core.get_time()
            
        
    def save_screenshot(self, filename):
        """
        Saves a full-size screenshot in the given filename.
        """

        try:
            renpy.display.scale.image_save_unscaled(self.window, filename)
        except:
            if renpy.config.debug:
                raise
            pass
        
    def screenshot(self, scale):
        """
        Returns a string containing the contents of the window, as a PNG.
        """

        surf = renpy.display.pgrender.copy_surface(self.window, True)
        surf = renpy.display.scale.smoothscale(surf, scale)
        surf = renpy.display.pgrender.copy_surface(surf, False)
        
        sio = cStringIO.StringIO()
        renpy.display.module.save_png(surf, sio, 0)
        rv = sio.getvalue()
        sio.close()
        
        return rv
    
    def can_redraw(self, first_pass):
        """
        Uses the framerate to determine if we can and should redraw.
        """
        
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
            self.full_redraw = True

        renpy.display.render.kill_old_screen()
        renpy.display.focus.take_focuses()
        
        self.suppressed_blit = fullscreen_video

        
    def render_to_texture(self, render, alpha):
        rv = renpy.display.pgrender.surface((render.width, render.height), alpha)
        draw(rv, None, render, 0, 0, False)

        return rv
        

    def mutated_surface(self, surf):
        """
        Called to indicate that the given surface has changed.
        """

        for i in clippers:
            i.mutated.add(id(surf))

            
    def load_texture(self, surf):
        """
        Creates a texture from the surface. In the software implementation,
        the only difference between a texture and a surface is that a texture
        is in the RLE cache.
        """

        if renpy.game.less_memory:
            return surf
        
        idsurf = id(surf)
        
        rle_surf = renpy.display.pgrender.copy_surface(surf)
        rle_surf.set_alpha(255, pygame.RLEACCEL)
        self.mutated_surface(rle_surf)

        rle_cache[idsurf] = rle_surf
        
        return surf
        
        
    def unload_texture(self, surf):
        """
        Unloads a texture.
        """

        idsurf = id(surf)
        if idsurf in rle_cache:
            del rle_cache[idsurf]
            

    def free_memory(self):
        """
        Frees up memory.
        """

        rle_cache.clear()
        
        
        
            
