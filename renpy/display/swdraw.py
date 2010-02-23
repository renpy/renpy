import renpy
import pygame
import cStringIO

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

            damage = renpy.display.render.draw_screen(0, 0, self.full_redraw)

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
