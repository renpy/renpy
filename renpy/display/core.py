# This file contains code for initializing and managing the display
# window.

import renpy

import pygame
from pygame.constants import *
import sys
import os
import time
import cStringIO

TIMEEVENT = USEREVENT + 1
PERIODIC = USEREVENT + 2
JOYEVENT = USEREVENT + 3
REDRAW = USEREVENT + 4

# The number of msec between periodic events.
PERIODIC_INTERVAL = 50

class IgnoreEvent(Exception):
    """
    Exception that is raised when we want to ignore an event, but
    also don't want to return anything.
    """

    pass

class Displayable(renpy.object.Object):
    """
    The base class for every object in Ren'Py that can be
    displayed to the screen.

    Drawables will be serialized to a savegame file. Therefore, they
    shouldn't store non-serializable things (like pygame surfaces) in
    their fields.
    """

    focusable = False
    role = ''

    def __init__(self, focus=None, default=False, style='default', **properties):
        self.style = renpy.style.Style(style, properties)
        self.style_prefix = 'insensitive_'
        self.focus_name = focus
        self.default = default

    def find_focusable(self, callback, focus_name):

        def finder(d):
            if d.focusable:
                callback(d, d.focus_name or focus_name)
            
        self.visit_all(finder)


    def focus(self, default=False):
        """
        Called to indicate that this widget has the focus.
        """

        self.set_style_prefix(self.role + "hover_")
        
        if not default:
            renpy.audio.sound.play(self.style.sound)

    def unfocus(self):
        """
        Called to indicate that this widget has become unfocused.
        """

        self.set_style_prefix(self.role + "idle_")



    def is_focused(self):
        return renpy.game.context().scene_lists.focused is self

    def set_style_prefix(self, prefix):
        """
        Called to set the style prefix of this widget and its child
        widgets, if any.
        """

        if prefix == self.style_prefix:
            return

        self.style.set_prefix(prefix)
        self.style_prefix = prefix
        renpy.display.render.redraw(self, 0)

    def parameterize(self, name, parameters):
        """
        Called to parameterize this. By default, we don't take any
        parameters.
        """

        if parameters:
            raise Exception("Image '%s' can't take parameters '%s'. (Perhaps you got the name wrong?)" %
                            (' '.join(name), ' '.join(parameters)))

        return self

    def render(self, width, height, st, at):
        """
        Called to display this displayable. This is called with width
        and height parameters, which give the largest width and height
        that this drawable can be drawn to without overflowing some
        bounding box. It's also given two times. It returns a Surface
        that is the current image of this drawable. 

        @param st: The time since this widget was first shown, in seconds.
        @param at: The time since a similarly named widget was first shown,
        in seconds.        
        """

        assert False, "Draw not implemented."

    def event(self, ev, x, y, st):
        """
        Called to report than an event has occured. Ev is the raw
        pygame event object representing that event. If the event
        involves the mouse, x and y are the translation of the event
        into the coordinates of this displayable. st is the time this
        widget has been shown for.

        @returns A value that should be returned from Interact, or None if
        no value is appropriate.
        """

        return None

    def get_placement(self):
        """
        Returns a style object containing placement information for
        this Displayable. Children are expected to overload this
        to return something more sensible.
        """

        return self.style.xpos, self.style.ypos, self.style.xanchor, self.style.yanchor

    def visit_all(self, callback):
        """
        Calls the callback on this displayable and all children of this
        displayable.
        """

        worklist = [ self ]

        while worklist:
            d = worklist.pop(0)

            if d is None:
                continue

            callback(d)
            worklist.extend(d.visit())
        

    def visit(self):
        """
        Called to ask the displayable to return a list of its children
        (including children taken from styles). For convenience, this
        list may also include None values.
        """

        return [ ]

    def per_interact(self):
        """
        Called once per widget per interaction.
        """

        return None

    def predict(self, callback):
        """
        Called to ask this displayable to call the callback with all
        the images it, and its children, may want to load.
        """
        
        self.visit_all(lambda i : i.predict_one(callback))
        
    def predict_one(self, callback):
        """
        Called to ask this displayable to call the callback with all
        the images it may want to load.
        """

        return

    def place(self, dest, x, y, width, height, surf, xoff=None, yoff=None):
        """
        This draws this Displayable onto a destination surface, using
        the placement style information returned by this object's
        get_placement() method.

        @param dest: The surface that this displayable will be drawn
        on.

        @param x: The minimum x coordinate on this surface that this
        Displayable will be drawn to.

        @param y: The minimum y coordinate on this surface that this
        displayable will be drawn to.

        @param width: The width of the area allocated to this
        Displayable.

        @param height: The height of the area allocated to this
        Displayable.

        @param surf: The surface returned by a previous call to
        self.render().
        """

        xpos, ypos, xanchor, yanchor = self.get_placement()

        if xpos is None:
            xpos = 0
        if ypos is None:
            ypos = 0
        if xanchor is None:
            xanchor = 0
        if yanchor is None:
            yanchor = 0


        sw, sh = surf.get_size()

        # x
        if xoff is None:
            xoff = xpos


        if isinstance(xoff, float):
            xoff = int(xoff * width)

        if xanchor == 'left':
            xanchor = 0.0
        elif xanchor == 'center':
            xanchor = 0.5
        elif xanchor == 'right':
            xanchor = 1.0
        elif not isinstance(xanchor, (float, int)):
            raise Exception("xanchor %r is not known." % xanchor)

        if isinstance(xanchor, int):
            xoff -= xanchor
        else:
            xoff -= int(sw * xanchor)

        xoff += x
        

        # y

        if yoff is None:
            yoff = ypos

        if isinstance(yoff, float):
            yoff = int(yoff * height)

        if yanchor == 'top':
            yanchor = 0.0
        elif yanchor == 'center':
            yanchor = 0.5
        elif yanchor == 'bottom':
            yanchor = 1.0
        elif not isinstance(yanchor, (float, int)):
            raise Exception("yanchor %r is not known." % yanchor)

        if isinstance(yanchor, int):
            yoff -= yanchor
        else:
            yoff -= int(sh * yanchor)

        yoff += y

        # print self, xoff, yoff

        dest.blit(surf, (xoff, yoff))

        return xoff, yoff


class SceneLists(object):
    """
    This stores the current scene lists that are being used to display
    things to the user. 

    @ivar focused: The widget that is currently focused.
    """

    def __init__(self, oldsl=None):

        # A map from layer name -> list of
        # (key, show time, animation time, displayable) 
        self.layers = { }
         
        if oldsl:

            for i in renpy.config.layers + renpy.config.top_layers:
                self.layers[i] = oldsl.layers[i][:]

            for i in renpy.config.overlay_layers:
                self.clear(i)

            self.replace_transient()

            self.sticky_positions = oldsl.sticky_positions.copy()
            self.movie = oldsl.movie
            self.focused = None
            
        else:
            for i in renpy.config.layers + renpy.config.top_layers:
                self.layers[i] = [ ]

            self.music = None
            self.movie = None
            self.sticky_positions = { }
            self.focused = None

    def rollback_copy(self):
        """
        Makes a shallow copy of all the lists, except for the stack,
        which is a 2-level copy.
        """

        rv = SceneLists(self)
        rv.focused = None

#         rv.master = self.master[:]
#         rv.transient = self.transient[:]

#         rv.music = self.music
#         rv.movie = self.movie

        return rv
         

    def replace_transient(self):
        """
        Replaces the contents of the transient display list with
        a copy of the master display list. This is used after a
        scene is displayed to get rid of transitions and interface
        elements.
        """

        for i in renpy.config.transient_layers:
            self.layers[i] = [ ]

    def transient_is_empty(self):
        """
        This returns True if all transient layers are empty. This is
        used by the rollback code, as we can't start a new rollback
        if there is something in a transient layer (as things in the
        transient layer may contain objects that cannot be pickled,
        like lambdas.)
        """

        for i in renpy.config.transient_layers:
            if self.layers[i]:
                return False

        return True

    def add(self, layer, thing, key=None):
        """
        This is called to add something to a layer. Layer is
        the name of the layer that we need to add the thing to,
        one of 'master' or 'transient'. Key is an optional key.

        If key is provided, and there exists something in the selected
        layer with the given key, that entry from the layer
        is replaced with the supplied displayable.

        Otherwise, the displayable is added to the end of the layer, and
        the time it was first displayed is set to the current time.
        """

        if layer not in self.layers:
            raise Exception("Trying to add something to non-existent layer '%s'." % layer)

        l = self.layers[layer]

        if key is not None:
            for index, (k, st, at, d) in enumerate(l):
                if k == key:
                    break
            else:
                index = None

            st = None

            if index is not None:
                l[index] = (key, st, at, thing)
                return

        l.append((key, None, None, thing))

    def remove(self, layer, thing):
        """
        This is either a key or a displayable. This iterates through the
        named layer, searching for entries matching the thing.
        When they are found, they are removed from the displaylist.

        It's not an error to remove something that isn't in the layer in
        the first place.
        """

        if layer not in self.layers:
            raise Exception("Trying to remove something from non-existent layer '%s'." % layer)

        l = self.layers[layer]
        l = [ (k, st, at, d) for k, st, at, d in l if k != thing if d is not thing ]

        self.layers[layer] = l

    def clear(self, layer):
        """
        Clears the named layer, making it empty.
        """

        if layer not in self.layers is None:
            raise Exception("Trying to clear non-existent layer '%s'." % layer)
        
        self.layers[layer] = [ ]

    def set_times(self, time):
        """
        This finds entries with a time of None, and replaces that
        time with the given time.
        """

        for l in self.layers.values():
            ll = [ ]

            for i in range(0, len(l)):
                k, st, at, d = l[i]
                ll.append((k, st or time, at or time, d))

            l[:] = ll
            

    def showing(self, layer, key):
        """
        Returns true of tan entry with the given key is found in the
        given layer. Returns False otherwise. Key should be a string.
        """

        for k, st, at, d in self.layers[layer]:
            if k == key:
                return True

        return False
    

class Display(object):
    """
    This is responsible for managing the display window.

    @ivar interface: The interface corresponding to this display.

    @ivar window: The window that is being presented to the user.

    @ivar sample_surface: A sample surface that is optimized for fast
    blitting to the window, with alpha. Used to create other surfaces
    from.

    @ivar fullscreen: Is the window in fullscreen mode?

    @ivar mouse: The mouse image, if we have one, or None if
    we do not have one.    

    @ivar mouse_location: The mouse location the last time it was
    drawn, or None if it wasn't drawn the last time around.

    @ivar mouse_backing: A backing store image holding the background
    that goes behind the mouse.

    @ivar mouse_backing_pos: The position of the upper-left hand
    corner of the backing pos, relative to the window.

    @ivar full_redraw: Force a full redraw.

    @ivar next_frame: The time when the next frame should be drawn. In
    ms returned from pygame.time.get_ticks().
    """


    def __init__(self, interface):

        self.interface = interface

        # Ensure that we kill off the presplash.
        renpy.display.presplash.end()

        # Ensure that we kill off the movie when changing screen res.
        renpy.display.video.movie_stop(clear=False)

        try:
            pygame.macosx.init()
        except:
            pass

        pygame.display.init()
        pygame.font.init()
        renpy.audio.audio.init()
        renpy.display.joystick.init()
        
        self.fullscreen = renpy.game.preferences.fullscreen
        fsflag = 0

        fullscreen = self.fullscreen

        if os.environ.get('RENPY_DISABLE_FULLSCREEN', False):
            fullscreen = False

        if fullscreen:
            fsflag = FULLSCREEN

        width = renpy.config.screen_width
        height = renpy.config.screen_height
        self.screen_xoffset = 0

        # Try out the widescreen mode.
        if os.environ.get('RENPY_FULLSCREEN_WIDE', False):
            wide_width = max(int(1.6 * height), width)

            try:
                pygame.display.set_mode((wide_width, height), fsflag, 32)
                self.screen_xoffset = (wide_width - width) // 2 
                width = wide_width
            except:
                pass

                
        # Pick an appropriate display mode. Prefer 32, but accept 24
        # before letting SDL do conversions.
        if 24 == pygame.display.mode_ok((width, height), fsflag, 32):
            depth = 24
        else:
            depth = 32

        # The window we display things in.
        self.window = pygame.display.set_mode((width, height), fsflag, depth)
        
        # Sample surface that all surfaces are created based on.
        self.sample_surface = self.window.convert_alpha()

        pygame.event.set_grab(False)

        # Window title and icon.
        pygame.display.set_caption(renpy.config.window_title.encode("utf-8"))

        if renpy.config.window_icon:
            pygame.display.set_icon(renpy.display.im.load_image(renpy.config.window_icon))
            

        # Load the mouse image, if any.
        if renpy.config.mouse:
            self.mouse = True
            pygame.mouse.set_visible(False)
        else:
            self.mouse = None
            pygame.mouse.set_visible(True)

        self.mouse_location = None
        self.mouse_backing = None
        self.mouse_backing_pos = None
        self.mouse_info = None

        self.suppress_mouse = False
        self.full_redraw = True

        self.next_frame = 0

    def can_redraw(self, first_pass):
        """
        Uses the framerate to determine if we can and should redraw.
        """
        
        framerate = renpy.config.framerate

        if framerate is None:
            return True
        
        next_frame = self.next_frame
        now = pygame.time.get_ticks()

        frametime = 1000 / framerate

        # Handle timer rollover.
        if next_frame > now + frametime:
            next_frame = now

        # It's not yet time for the next frame.
        if now < next_frame and not first_pass:            
            return False
            
        # Otherwise, it is. Schedule the next frame.
        if next_frame + frametime < now:
            next_frame = now + frametime
        else:
            next_frame += frametime

        self.next_frame = next_frame

        return True

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
        self.mouse_backing = pygame.Surface((mw, mh), self.window.get_flags(), self.window)
        self.mouse_backing.blit(self.window, (0, 0), (bx, by, mw, mh))

        self.window.blit(mouse, (bx, by))

        return bx, by, mw, mh

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

    def draw_mouse(self, show_mouse=True):
        """
        This draws the mouse to the screen, if necessary. It uses the
        buffer to minimize the amount of the screen that needs to be
        drawn, and only redraws if the mouse has actually been moved.
        """

        if not self.mouse:
            return [ ]

        if self.suppress_mouse:
            return [ ]

        # Figure out the mouse animation.
        if self.interface.mouse in renpy.config.mouse:
            anim = renpy.config.mouse[self.interface.mouse]
        else:
            anim = renpy.config.mouse['default']

        info = anim[self.interface.ticks % len(anim)]

        pos = pygame.mouse.get_pos()

        if pos == self.mouse_location and show_mouse and info == self.mouse_info:
            return [ ]

        if not pos and not show_mouse:
            return [ ]

        updates = [ ]

        if self.mouse_location:
            updates.append(self.hide_mouse())

        if show_mouse:
            updates.append(self.show_mouse(pos, info))
            
        return updates

    def update_mouse(self):
        """
        Draws the mouse, and then updates the screen.
        """

        updates = self.draw_mouse()

        if updates:
            pygame.display.update(updates)
        
        
    def show(self, root_widget, suppress_blit):
        """
        Draws the current transient screen list to the screen.
        
        @returns A list of offsets corresponding to each widget,
        relative to the screen.
        """

#         if self.next_draw < pygame.time.get_ticks():
#             self.next_draw = pygame.time.get_ticks()

#         pygame.time.delay(self.next_draw - pygame.time.get_ticks())

#         self.next_draw += 1000 / 30

        surftree = renpy.display.render.render_screen(
            root_widget,
            renpy.config.screen_width,
            renpy.config.screen_height,
            0)

        if not suppress_blit:

            updates = [ ]

            updates.extend(self.draw_mouse(False))

            damage = renpy.display.render.screen_blit(surftree, self.full_redraw, self.screen_xoffset)

            if damage:
                updates.extend(damage)

            self.full_redraw = False

            updates.extend(self.draw_mouse(True))
            pygame.display.update(updates)

        else:
            self.full_redraw = True
            
        self.suppress_mouse = suppress_blit

        renpy.display.focus.take_focuses(surftree.focuses)
        
    def save_screenshot(self, filename):
        """
        Saves a full-size screenshot in the given filename.
        """

        if filename.endswith(".png"):
            f = file(filename, "wb")
            renpy.display.module.save_png(self.window, f)
            f.close()
        else:
            pygame.image.save(self.window, filename)

    def screenshot(self, scale):
        """
        Returns a pygame Surface that is a screenshot of the current
        contents of the window.
        """

        surf = renpy.display.module.scale(self.window, scale)
        
        sio = cStringIO.StringIO()
        pygame.image.save(surf, sio)
        rv = sio.getvalue()
        sio.close()
        
        return rv
    
class Interface(object):
    """
    This represents the user interface that interacts with the user.
    It manages the Display objects that display things to the user, and
    also handles accepting and responding to user input.

    @ivar display: The display that we used to display the screen.

    @ivar profile_time: The time of the last profiling.

    @ivar screenshot: A screenshot, or None if no screenshot has been
    taken.

    @ivar old_scene: The last thing that was displayed to the screen, not
    counting underlays.

    @ivar transition: A map from layer name to the transition that will
    be applied the next time interact restarts.

    @ivar suppress_transition: If True, then the next transition will not
    happen.

    @ivar quick_quit: If true, a click on the delete button will
    cause an immediate quit.

    @ivar force_redraw: If True, a redraw is forced.

    @ivar restart_interaction: If True, the current interaction will
    be restarted.

    @ivar pushed_event: If not None, an event that was pushed back
    onto the stack.

    @ivar mouse: The name of the mouse cursor to use during the current
    interaction.

    @ivar ticks: The number of 20hz ticks.

    @ivar frame_time: The time at which we began drawing this frame.

    @ivar interact_time: The time of the start of the first frame of the current interact_core.

    @ivar time_event: A singleton ignored event.

    @ivar event_time: The time of the current event.

    @ivar timeout_time: The time at which the timeout will occur.

    """

    def __init__(self):
        self.display = Display(self)
        self.profile_time = time.time()
        self.screenshot = None
        self.old_scene = None
        self.transition = { }
        self.suppress_transition = False
        self.quick_quit = False
        self.force_redraw = False
        self.restart_interaction = False
        self.pushed_event = None
        self.ticks = 0
        self.mouse = 'default'
        self.timeout_time = None

        # Things to be preloaded.
        self.preloads = [ ]

        # The time at which this draw occurs.
        self.frame_time = 0

        self.interact_time = None

        self.time_event = pygame.event.Event(TIMEEVENT)

        # Properties for each layer.
        self.layer_properties = { }

        for layer in renpy.config.layers + renpy.config.top_layers:
            if layer in renpy.config.layer_clipping:
                x, y, w, h = renpy.config.layer_clipping[layer]
                self.layer_properties[layer] = dict(
                    xpos = x,
                    xanchor = 0,
                    ypos = y,
                    yanchor = 0,
                    xmaximum = w,
                    ymaximum = h,
                    clipping = True,
                    )

            else:
                self.layer_properties[layer] = dict()
                


    def take_screenshot(self, scale):
        """
        This takes a screenshot of the current screen, and stores it so
        that it can gotten using get_screenshot()
        """

        self.screenshot = self.display.screenshot(scale)

    def get_screenshot(self):
        """
        Gets the current screenshot, as a string. Returns None if there isn't
        a current screenshot.
        """

        if not self.screenshot:
            raise Exception("Trying to write a screenshot that hasn't been taken.")

        return self.screenshot

    def lose_screenshot(self):
        """
        This deallocates the saved screenshot.
        """

        self.screenshot = None


    def with(self, trans, paired):

        
        if renpy.config.with_callback:
            trans = renpy.config.with_callback(trans, paired)

        if not trans:
            self.with_none()
            return False
        else:
            self.set_transition(trans)
            return self.interact(show_mouse=False, trans_pause=True,
                                 suppress_overlay=not renpy.config.overlay_during_with,
                                 mouse='with')

    def with_none(self):
        """
        Implements the with None command, which sets the scene we will
        be transitioning from.
        """
        
        scene_lists = renpy.game.context().scene_lists

        old_old_scene = self.old_scene

        self.old_scene = self.compute_scene(scene_lists)        

        if renpy.config.overlay_during_with and old_old_scene:
            for i in renpy.config.overlay_layers:
                self.old_scene[i] = old_old_scene[i]

        scene_lists = renpy.game.context().scene_lists
        scene_lists.replace_transient()

    def set_transition(self, transition, layer=None):
        """
        Sets the transition that will be performed as part of the next
        interaction.
        """

        self.transition[layer] = transition


    def event_peek(self):
        """
        This peeks the next event. It returns None if no event exists.
        """

        if self.pushed_event:
            return self.pushed_event

        ev = pygame.event.poll()

        if ev.type == NOEVENT:
            return None

        self.pushed_event = ev
        return ev

    def event_poll(self):
        """
        Called to busy-wait for an event while we're waiting to
        redraw a frame.
        """
        
        if self.pushed_event:
            rv = self.pushed_event
            self.pushed_event = None
            return rv

        else:
            return pygame.event.poll()
        

    def event_wait(self):
        """
        This is in its own function so that we can track in the
        profiler how much time is spent in interact.
        """

        if self.pushed_event:
            rv = self.pushed_event
            self.pushed_event = None
            return rv

        # We load at most one image per wait.
        if renpy.display.im.cache.needs_preload():
            ev = pygame.event.poll()
            if ev.type != NOEVENT:
                return ev


            renpy.display.im.cache.preload()

        ev = pygame.event.wait()
        return ev

    def compute_scene(self, scene_lists):
        """
        This converts scene lists into a dictionary mapping layer
        name to a Fixed containing that layer.
        """

        rv = { }

        for layer in renpy.config.layers + renpy.config.top_layers:

            f = renpy.display.layout.Fixed(focus=layer, **self.layer_properties[layer])

            f.append_scene_list(scene_lists.layers[layer])

            rv[layer] = f

        return rv
            

    def interact(self, **kwargs):
        """
        This handles an interaction, restarting it if necessary. All of the
        keyword arguments are passed off to interact_core.
        """

        # These things can be done once per interaction.

        preloads = self.preloads
        self.preloads = [ ]

        try:
            renpy.game.after_rollback = False
            
            for i in renpy.config.start_interact_callbacks:
                i()

            repeat = True

            while repeat:
                repeat, rv = self.interact_core(preloads=preloads, **kwargs)
            
            return rv
        
        finally:

            # Clean out transient stuff at the end of an interaction.
            scene_lists = renpy.game.context().scene_lists
            scene_lists.replace_transient()
            if renpy.config.implicit_with_none:
                self.with(None, None)

            self.restart_interaction = True
        

    def interact_core(self,
                      show_mouse=True,
                      trans_pause=False,
                      suppress_overlay=False,
                      suppress_underlay=False,
                      mouse='default',
                      preloads=[],
                      ):

        """
        This handles one cycle of displaying an image to the user,
        and then responding to user input.

        @param show_mouse: Should the mouse be shown during this
        interaction? Only advisory, and usually doesn't work.

        @param trans_pause: If given, we must have a transition. Should we
        add a pause behavior during the transition?

        @param suppress_overlay: This suppresses the display of the overlay.
        @param suppress_underlay: This suppresses the display of the underlay.
        """

        self.suppress_transition = self.suppress_transition or renpy.config.skipping

        ## Safety condition, prevents deadlocks.
        if trans_pause:
            if not self.transition:
                return False, None
            if self.suppress_transition:
                return False, None

        # We just restarted.
        self.restart_interaction = False

        # Setup the mouse.
        self.mouse = mouse

        # The start and end times of this interaction.
        start_time = time.time()
        end_time = start_time

        # frames = 0

        for i in renpy.config.interact_callbacks:
            i()

        renpy.audio.audio.interact()

        # Tick time forward.
        renpy.display.im.cache.tick()

        # Setup periodic event.
        pygame.time.set_timer(PERIODIC, PERIODIC_INTERVAL)

        # Clear some events.
        pygame.event.clear((MOUSEMOTION, PERIODIC,
                            MOUSEBUTTONUP, MOUSEBUTTONDOWN,
                            TIMEEVENT, REDRAW))

        # Add a single TIMEEVENT to the queue.
        pygame.event.post(self.time_event)
        
        # Figure out the scene list we want to show.        
        scene_lists = renpy.game.context().scene_lists
        
        # Figure out what the overlay layer should look like.
        renpy.ui.layer("overlay")

        if not suppress_overlay:
            for i in renpy.config.overlay_functions:
                i()

        renpy.ui.close()

        # Figure out the underlay layer.
        if not suppress_underlay:
            underlay = [ ( None, 0, 0, i) for i in renpy.config.underlay ]
        else:
            underlay = [ ]

        # The root widget of everything that is displayed on the screen.
        root_widget = renpy.display.layout.Fixed() 
        root_widget.append_scene_list(underlay)
        root_widget.layers = { }

        # Figure out the scene. (All of the layers, and the root.)
        scene = self.compute_scene(scene_lists)

        # If necessary, load all images here.
        if renpy.config.load_before_transition:
            for w in scene.itervalues():
                w.predict(renpy.display.im.cache.get)

        # The root widget of all of the layers.
        layers_root = renpy.display.layout.Fixed()
        layers_root.layers = { }


        def add_layer(where, layer):
            if self.transition.get(layer, None) and self.old_scene and not self.suppress_transition:

                trans = self.transition[layer](old_widget=self.old_scene[layer],
                                               new_widget=scene[layer])
                where.add(trans)
                where.layers[layer] = trans
                
            else:
                where.layers[layer] = scene[layer]
                where.add(scene[layer])

        # Add layers (perhaps with transitions) to the layers root.
        for layer in renpy.config.layers:
            add_layer(layers_root, layer)
                
        # Add layers_root to root_widget, perhaps through a transition.
        if None in self.transition and self.old_scene and not self.suppress_transition:

            # Compute what the old root should be.
            old_root = renpy.display.layout.Fixed()
            old_root.layers = { }

            for layer in renpy.config.layers:
                old_root.layers[layer] = self.old_scene[layer]
                old_root.add(self.old_scene[layer])
            
            trans = self.transition[None](old_widget=old_root,
                                          new_widget=layers_root)
            
            root_widget.add(trans)

            if trans_pause:
                sb = renpy.display.behavior.SayBehavior()
                root_widget.add(sb)

                pb = renpy.display.behavior.PauseBehavior(trans.delay)
                root_widget.add(pb)
                
        else:
            root_widget.add(layers_root)


        # Add top_layers to the root_widget.
        for layer in renpy.config.top_layers:
            add_layer(root_widget, layer)

        # Call per-interaction code for all widgets.
        root_widget.visit_all(lambda i : i.per_interact())

        # Now, update various things regarding scenes and transitions,
        # so we are ready for a new interaction or a restart.
        self.old_scene = scene
        self.transition = { }
        self.suppress_transition = False
            

        # Okay, from here on we now have a single root widget (root_widget),
        # which we will try to show to the user.

        # Figure out what should be focused.
        renpy.display.focus.before_interact(root_widget)

        # Redraw the screen.
        renpy.display.render.process_redraws()
        needs_redraw = True

        # First pass through the while loop?
        first_pass = True

        # We don't yet know when the interaction began.
        self.interact_time = None
        
        # We only want to do prediction once, but we will defer it as
        # long as possible.
        did_prediction = False

        old_timeout_time = None
        old_redraw_time = None

        rv = None

        # This try block is used to force cleanup even on termination
        # caused by an exception propigating through this function.
        try: 

            while rv is None:

                # Check for a change in fullscreen preference.
                if self.display.fullscreen != renpy.game.preferences.fullscreen:
                    self.display = Display(self)
                    needs_redraw = True

                # Check for a forced redraw.
                if self.force_redraw:
                    needs_redraw = True
                    self.force_redraw = False

                # Redraw the screen.
                if needs_redraw and self.display.can_redraw(first_pass):


                    # If we have a movie, start showing it.
                    suppress_blit = renpy.display.video.interact()

                    # Draw the screen.
                    self.frame_time = time.time()

                    if not self.interact_time:
                        self.interact_time = self.frame_time

                    self.display.show(root_widget, suppress_blit)
                    
                    renpy.config.frames += 1

                    # If profiling is enabled, report the profile time.
                    if renpy.config.profile :
                        new_time = time.time()
                        print "Profile: Redraw took %f seconds." % (new_time - self.frame_time)
                        print "Profile: %f seconds to complete event." % (new_time - self.profile_time)

                    if first_pass:
                        scene_lists.set_times(self.interact_time)

                    needs_redraw = False
                    first_pass = False

                    pygame.time.set_timer(REDRAW, 0)
                    pygame.event.clear([REDRAW])
                    old_redraw_time = None


                # Draw the mouse, if it needs drawing.
                if show_mouse:
                    self.display.update_mouse()
                    
                # See if we want to restart the interaction entirely.
                if self.restart_interaction:                    
                    return True, None

                # Determine if we need a redraw.
                needs_redraw = needs_redraw or renpy.display.render.process_redraws()

                # If we need to redraw again, do it if we don't have an
                # event going on.
                if needs_redraw and not self.event_peek():
                    if renpy.config.profile:
                        self.profile_time = time.time()
                    continue

                # Predict images, if we haven't done so already.
                if not did_prediction and not self.event_peek():
                    root_widget.predict(renpy.display.im.cache.preload_image)

                    for w in preloads:
                        w.predict(renpy.display.im.cache.preload_image)

                    renpy.game.context().predict(renpy.display.im.cache.preload_image)
                    did_prediction = True


                try:

                    # Handle the redraw timer.
                    redraw_time = renpy.display.render.redraw_time()
                    if redraw_time and not needs_redraw:

                        if redraw_time != old_redraw_time:
                            time_left = redraw_time - time.time()
                            time_left = min(time_left, 3600)
                            pygame.time.set_timer(REDRAW, max(int(time_left * 1000), 1))
                            old_redraw_time = redraw_time
                    else:
                        pygame.time.set_timer(REDRAW, 0)

                    # Handle the timeout timer.
                    if not self.timeout_time:
                        pygame.time.set_timer(TIMEEVENT, 0)
                        ev = None
                    else:
                        time_left = self.timeout_time - time.time() 
                        time_left = min(time_left, 3600)

                        if time_left < 0:
                            self.timeout_time = None
                            ev = self.time_event
                            pygame.time.set_timer(TIMEEVENT, 0)
                        else:
                            ev = None

                            if self.timeout_time != old_timeout_time:
                                # Always set to at least 1ms.
                                pygame.time.set_timer(TIMEEVENT, int(time_left * 1000 + 1))

                                old_timeout_time = self.timeout_time


                    # Get the event, if we don't have one already.
                    if ev is None:
                        if needs_redraw:
                            ev = self.event_poll()
                        else:
                            ev = self.event_wait()

                    if ev.type == NOEVENT:
                        continue

                    if renpy.config.profile:
                        self.profile_time = time.time()

                    
                    # Try to merge an TIMEEVENT with the next event.
                    if ev.type == TIMEEVENT:
                        old_timeout_time = None

                        pygame.event.clear([TIMEEVENT])

                        ev2 = self.event_peek()

                        if ev2 and ev2.type not in (NOEVENT, PERIODIC, REDRAW, QUIT):
                            ev = self.event_poll()

                    # Handle redraw timeouts.
                    if ev.type == REDRAW:
                        old_redraw_time = None
                        continue

                    # Handle periodic events. This includes updating the mouse timers (and through the loop,
                    # the mouse itself), and the audio system periodic calls.
                    if ev.type == PERIODIC:
                        events = 1 + len(pygame.event.get([PERIODIC]))
                        self.ticks += events

                        if renpy.config.periodic_callback:
                            renpy.config.periodic_callback()

                        renpy.audio.audio.periodic()
                        continue
                            
                    # This can set the event to None, to ignore it.
                    ev = renpy.display.joystick.event(ev)
                    if not ev:
                        continue

                    # Handle skipping.
                    renpy.display.behavior.skipping(ev)

                    # Handle quit specially for now.
                    if ev.type == QUIT:
                        if renpy.game.script.has_label("_confirm_quit") and not self.quick_quit:
                            self.quick_quit = True
                            renpy.game.call_in_new_context("_confirm_quit")
                            self.quick_quit = False
                        else:                
                            raise renpy.game.QuitException()

                    # Merge mousemotion events.
                    if ev.type == MOUSEMOTION:
                        evs = pygame.event.get([MOUSEMOTION])

                        if len(evs):
                            ev = evs[-1]


                    # x, y = getattr(ev, 'pos', (0, 0))
                    x, y = pygame.mouse.get_pos()
                    x -= self.display.screen_xoffset

                    renpy.display.focus.event_handler(ev, x, y)

                    self.event_time = end_time = time.time()

                    rv = root_widget.event(ev, x, y, 0)

                    if rv is not None:
                        break
            
                except IgnoreEvent:
                    # An ignored event can change the timeout. So we want to
                    # process an TIMEEVENT to ensure that the timeout is
                    # set correctly.
                    pygame.event.post(self.time_event)
                    

                # Check again after handling the event.
                needs_redraw |= renpy.display.render.process_redraws()

                if self.restart_interaction:
                    return True, None
                    
            # But wait, there's more! The finally block runs some cleanup
            # after this.
            return False, rv

        finally:

            # Clean out the overlay layers.
            for i in renpy.config.overlay_layers:
                scene_lists.clear(i)

            # pygame.time.set_timer(KEYREPEATEVENT, 0)
            pygame.time.set_timer(PERIODIC, 0)
            pygame.time.set_timer(TIMEEVENT, 0)
            pygame.time.set_timer(REDRAW, 0)

            renpy.game.context().runtime += end_time - start_time

            # Restart the old interaction, which also causes a
            # redraw if needed.
            self.restart_interaction = True

            # print "It took", frames, "frames."

    def timeout(self, offset):
        if offset < 0:
            return

        if self.timeout_time:
            self.timeout_time = min(self.event_time + offset, self.timeout_time)
        else:
            self.timeout_time = self.event_time + offset

