# This file contains code for initializing and managing the display
# window.

import renpy
from renpy.display.render import render

import pygame
from pygame.constants import *
import time
import cStringIO

# KEYREPEATEVENT = USEREVENT + 1
DISPLAYTIME = USEREVENT + 2

# The number of msec 
DISPLAYTIME_INTERVAL = 50

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

    def __init__(self):
        self.style = None
        self.style_prefix = None

    def set_style_prefix(self, prefix):
        """
        Called to set the style prefix of this widget and its child
        widgets, if any.
        """

        if prefix == self.style_prefix:
            return

        if self.style:
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

    def render(self, width, height, shown_time):
        """
        Called to display this displayable. This is called with width
        and height parameters, which give the largest width and height
        that this drawable can be drawn to without overflowing some
        bounding box. It's also given two times. It returns a Surface
        that is the current image of this drawable. 

        @param shown_time: The time since we first started showing this
        drawable, a float in seconds.
        """

        assert False, "Draw not implemented."

    def event(self, ev, x, y):
        """
        Called to report than an event has occured. Ev is the raw
        pygame event object representing that event. If the event
        involves the mouse, x and y are the translation of the event
        into the coordinates of this displayable.

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

        return renpy.game.style.default

    def predict(self, callback):
        """
        Called to ask this displayable to call the callback with all
        the images it may want to load.
        """

        return


    def place(self, dest, x, y, width, height, surf):
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

        style = self.get_placement()
        sw, sh = surf.get_size()

        # x
        xoff = style.xpos

        if isinstance(xoff, float):
            xoff = int(xoff * width)

        if style.xanchor == 'left':
            xoff -= 0
        elif style.xanchor == 'center':
            xoff -= sw / 2
        elif style.xanchor == 'right':
            xoff -= sw
        else:
            raise Exception("xanchor '%s' is not known." % style.xanchor)
            
        xoff += x

        # y
        yoff = style.ypos

        if isinstance(yoff, float):
            yoff = int(yoff * height)

        if style.yanchor == 'top':
            yoff -= 0
        elif style.yanchor == 'center':
            yoff -= sh / 2
        elif style.yanchor == 'bottom':
            yoff -= sh
        else:
            raise Exception("yanchor '%s' is not known." % style.yanchor)

        yoff += y

        # print self, xoff, yoff

        dest.blit(surf, (xoff, yoff))

        return xoff, yoff


class SceneLists(object):
    """
    This stores the current scene lists that are being used to display
    things to the user. 

    Scene lists are lists of triples. The elements of the triple are
    (key, time, displayable), where key is a key that can be used to
    remove things from the list, time is the time that this entry was
    first added to a list, and drawable is the thing that is being
    drawn.

    @ivar master: The current master display list.
    @ivar transient: The current transient display list.
    @ivar overlay: The current overlay display list.

    @ivar music: Opaque information about the music that is being played.

    """

    def __init__(self, oldsl=None):
        
        if oldsl:
            self.master = oldsl.master[:]
            self.replace_transient()
            self.overlay = oldsl.overlay[:]
            self.music = oldsl.music
            self.sticky_positions = oldsl.sticky_positions.copy()
            self.movie = oldsl.movie
            
        else:
            self.master = [ ]            
            self.transient = [ ]
            self.overlay = [ ]
            self.music = None
            self.movie = None
            self.sticky_positions = { }

    def rollback_copy(self):
        """
        Makes a shallow copy of all the lists, except for the stack,
        which is a 2-level copy.
        """

        rv = SceneLists()
        rv.master = self.master[:]
        rv.transient = self.transient[:]

        rv.music = self.music
        rv.movie = self.movie

        return rv
         

    def replace_transient(self):
        """
        Replaces the contents of the transient display list with
        a copy of the master display list. This is used after a
        scene is displayed to get rid of transitions and interface
        elements.
        """

        self.transient = [ ]

    def add(self, listname, thing, key=None):
        """
        This is called to add something to a display list. Listname is
        the name of the displaylist that we need to add the thing to,
        one of 'master' or 'transient'. Key is an optional key.

        If key is provided, and there exists something in the selected
        displaylist with the given key, that entry from the displaylist
        is replaced with the supplied displayable, preserving the
        time it was first displayed.

        Otherwise, the displayable is added to the end of the list, and
        the time it was first displayed is set to the current time.
        """

        l = getattr(self, listname, None)

        if l is None:
            raise Exception("Trying to add something to non-existent display list '%s'." % listname)

        if key is not None:
            for index, (k, t, d) in enumerate(l):
                if k == key:
                    break
            else:
                index = None

            if index is not None:
                l[index] = (key, t, thing)
                return

        l.append((key, time.time(), thing))

    def remove(self, listname, thing):
        """
        This is either a key or a displayable. This iterates through the
        named display list, searching for entries matching the thing.
        When they are found, they are removed from the displaylist.

        It's not an error to remove something that isn't in the list in
        the first place.
        """

        l = getattr(self, listname)

        l = [ (k, t, d) for k, t, d in l if k != thing if d is not thing ]

        setattr(self, listname, l)

    def clear(self, listname):
        """
        Resets the given listname to either the empty list, or to the
        contents of the empty scenelist if reset_to_empty is True.

        @param: The name of the list to clear. One of the strings
        'master' or 'transient'.
        """

        l = getattr(self, listname, None)

        if l is None:
            raise Exception("Trying to clear non-existent display list '%s'." % listname)
        
        nl = [ ]

        setattr(self, listname, nl)
    

class Display(object):
    """
    This is responsible for managing the display window.

    @ivar window: The window that is being presented to the user.

    @ivar buffer: A surface that buffers the window.

    @ivar sample_surface: A sample surface that is optimized for fast
    blitting to the window, with alpha. Used to create other surfaces
    from.

    @ivar fullscreen: Is the window in fullscreen mode?

    @ivar mouse: The mouse image, if we have one, or None if
    we do not have one.    

    @ivar mouse_location: The mouse location the last time it was
    drawn, or None if it wasn't drawn the last time around.
    """


    def __init__(self):


        # Ensure that we kill off the movie when changing screen res.
        renpy.display.video.movie_stop(clear=False)

        renpy.display.audio.pre_init()
        pygame.init()
        
        self.fullscreen = renpy.game.preferences.fullscreen
        fsflag = 0

        if self.fullscreen:
            fsflag = FULLSCREEN

        # The window we display things in.
        self.window = pygame.display.set_mode((renpy.config.screen_width,
                                               renpy.config.screen_height),
                                              fsflag)

        # The mouse buffer.
        if renpy.config.mouse:
            self.buffer = pygame.Surface((renpy.config.screen_width,
                                          renpy.config.screen_height))

        # Sample surface that all surfaces are created based on.
        self.sample_surface = self.window.convert_alpha()

        pygame.event.set_grab(False)

        # Window title and icon.
        pygame.display.set_caption(renpy.config.window_title)

        if renpy.config.window_icon:
            pygame.display.set_icon(renpy.display.image.cache.load_image(renpy.config.window_icon))
            

        # Load the mouse image, if any.
        if renpy.config.mouse:
            self.mouse = renpy.display.image.cache.load_image(renpy.config.mouse)
            pygame.mouse.set_visible(False)
        else:
            self.mouse = None
            pygame.mouse.set_visible(True)

        self.mouse_location = None
        self.suppress_mouse = False

    def draw_mouse(self, show_mouse=True):
        """
        This draws the mouse to the screen, if necessary. It uses the
        buffer to minimize the amount of the screen that needs to be
        drawn, and only redraws if the mouse has actually been moved.
        """
        
        if not self.mouse:
            return

        if self.suppress_mouse:
            return

        mw, mh = self.mouse.get_size()
        pos = pygame.mouse.get_pos()

        if not pygame.mouse.get_focused():
            pos = None

        if not show_mouse:
            pos = None

        updates = [ ]

        if self.mouse_location and self.mouse_location != pos:
            ox, oy = self.mouse_location
            self.window.blit(self.buffer, (ox, oy), (ox, oy, mw, mh))
            updates.append((ox, oy, mw, mh))

        if pos and (pos != self.mouse_location):
            self.window.blit(self.mouse, pos)
            updates.append(pos + (mw, mh))

        self.mouse_location = pos

        pygame.display.update(updates)
            
        
    def show(self, root_widget, suppress_blit):
        """
        Draws the current transient screen list to the screen.
        
        @returns A list of offsets corresponding to each widget,
        relative to the screen.
        """

        surftree = renpy.display.render.render_screen(
            root_widget,
            renpy.config.screen_width,
            renpy.config.screen_height,
            0)

        if not suppress_blit:        

            if self.mouse:
                self.draw_mouse(False)

            damage = renpy.display.render.screen_blit(surftree)

            if self.mouse:
                if damage:
                    self.buffer.blit(self.window, damage, damage)
                self.draw_mouse(True)

            if damage:
                pygame.display.update(damage)

        self.suppress_mouse = suppress_blit

        
    def save_screenshot(self, filename):
        """
        Saves a full-size screenshot in the given filename.
        """

        pygame.image.save(self.window, filename)

    def screenshot(self, scale):
        """
        Returns a pygame Surface that is a screenshot of the current
        contents of the window.
        """

        surf = pygame.transform.scale(self.window, scale)

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
    counting underlays and things like that.

    @ivar transition: If not None, the transition to be applied for the
    next interaction.

    @ivar suppress_transition: If True, then the next transition will not
    happen.

    @ivar quick_quit: If true, a click on the delete button will
    cause an immediate quit.

    @ivar force_redraw: If True, a redraw is forced.

    """

    def __init__(self):
        self.display = Display()
        self.profile_time = time.time()
        self.screenshot = None
        self.old_scene = None
        self.transition = None
        self.supress_transition = False
        self.quick_quit = False
        self.force_redraw = False

    def take_screenshot(self, scale):
        """
        This takes a screenshot of the current screen, and stores it so
        that it can gotten using get_screenshot()
        """

        self.screenshot = self.display.screenshot(scale)

    def get_screenshot(self):
        """
        Gets the current screenshot, as a string containing a TGA file.
        """

        if not self.screenshot:
            raise Exception("Trying to write a screenshot that hasn't been taken.")

        return self.screenshot

    def lose_screenshot(self):
        """
        This deallocates the saved screenshot.
        """

        self.screenshot = None
        
    def with_none(self):
        """
        Implements the with None command, which sets the scene we will
        be transitioning from.
        """

        scene_lists = renpy.game.context().scene_lists
        self.old_scene = renpy.display.layout.Fixed()
        self.old_scene.append_scene_list(scene_lists.master)

    def set_transition(self, transition):
        """
        Sets the transition that will be performed as part of the next
        interaction.
        """

        self.transition = transition

    def event_wait(self):
        """
        This is in its own function so that we can track in the
        profiler how much time is spent in interact.
        """

        return pygame.event.wait()


    def interact(self, transient=None, show_mouse=True,
                 trans_pause=False,
                 suppress_overlay=False,
                 suppress_underlay=False,
                 ):
        """
        This handles one cycle of displaying an image to the user,
        and then responding to user input.

        @param transient: If given, a replacement list of transient
        things to show.

        @param show_mouse: Should the mouse be shown during this
        interaction? Only advisory.

        @param trans_pause: If given, we must have a transition. Should we
        add a pause behavior during the transition?

        @param suppress_overlay: This suppresses the display of the overlay.
        @param suppress_underlay: This suppresses the display of the underlay.
        """

        ## Safety condition, prevents deadlocks.
        if trans_pause:
            if not self.transition:
                return None
            if self.supress_transition:
                return None


        # frames = 0

        ## Expensive things we want to do before we pick the start_time.

        # Tick time forward.
        renpy.display.image.cache.tick()

        # Predict images.
        renpy.game.context().predict(renpy.display.image.cache.preload_image)

        # Set up key repeats.
        # pygame.time.set_timer(KEYREPEATEVENT, renpy.config.skip_delay)

        # Set up display time event.
        pygame.time.set_timer(DISPLAYTIME, DISPLAYTIME_INTERVAL)

        # Clear some events.
        pygame.event.clear((MOUSEMOTION, DISPLAYTIME,
                            MOUSEBUTTONUP, MOUSEBUTTONDOWN))

        
        # Figure out the scene list we want to show.
        start_time = time.time()
        scene_lists = renpy.game.context().scene_lists

        # Compute the overlay, by calling the overlay functions.
        overlay = [ ]
        
        if not suppress_overlay:
            for i in renpy.config.overlay_functions:

                overlaid = i()

                if overlaid:
                    for j in overlaid:
                        overlay.append((None, 0, j))

        if not suppress_underlay:
            underlay = [ ( None, 0, i) for i in renpy.config.underlay ]
        else:
            underlay = [ ]

        # Set up the transient scene list.
        if transient:
            transient = scene_lists.transient + [ (None, start_time, i) for i in transient ] 
        else:
            transient = scene_lists.transient 


        # The root widget of everything that is displayed on the screen.
        root_widget = renpy.display.layout.Fixed() 
        root_widget.append_scene_list(underlay)

        # The root widget of the normal stuff.
        current_scene = renpy.display.layout.Fixed()
        current_scene.append_scene_list(scene_lists.master + transient + overlay)
        
        if self.transition and self.old_scene and not self.supress_transition:

            trans = self.transition(old_widget=self.old_scene,
                                    new_widget=current_scene)

            root_widget.add(trans, start_time)

            if trans_pause:
                sb = renpy.display.behavior.SayBehavior()
                root_widget.add(sb, start_time)

                pb = renpy.display.behavior.PauseBehavior(trans.delay)
                root_widget.add(pb, start_time)
        else:
            root_widget.add(current_scene, start_time)

        # Reset this for next time.
        self.transition = None
        self.supress_transition = False

        # Redraw the screen during every interaction.
        needs_redraw = True

        # Post an event that moves us to the current mouse position.
        pygame.event.post(pygame.event.Event(MOUSEMOTION,
                                             pos=pygame.mouse.get_pos()))
        
        rv = None

        # This try block is used to force cleanup even on termination
        # caused by an exception propigating through this function.
        try: 

            while rv is None:

                # Check for a change in fullscreen preference.
                if self.display.fullscreen != renpy.game.preferences.fullscreen:
                    self.display = Display()
                    needs_redraw = True

                # Check for a forced redraw.
                if self.force_redraw:
                    needs_redraw = True
                    self.force_redraw = False

                # Redraw the screen.
                if needs_redraw:
                    needs_redraw = False

                    # If we have a movie, start showing it.
                    suppress_blit = renpy.display.video.interact()

                    # Draw the screen.
                    draw_start = time.time()

                    self.display.show(root_widget, suppress_blit)
                    
                    # frames = frames + 1

                    # If profiling is enabled, report the profile time.
                    if renpy.config.profile:
                        new_time = time.time()
                        print "Profile: Redraw took %f seconds." % (new_time - draw_start)
                        print "Profile: %f seconds between event and display." % (new_time - self.profile_time)

                # Draw the mouse, if it needs drawing.
                if show_mouse:
                    self.display.draw_mouse()
                    
                # Determine if we need a redraw.
                needs_redraw = renpy.display.render.process_redraws()

                # If we need to redraw again, do it if we don't have an
                # event going on.
                if needs_redraw and not pygame.event.peek():
                    continue

                # While we have nothing to do, preload images.
                while renpy.display.image.cache.needs_preload() and \
                          not pygame.event.peek():
                    renpy.display.image.cache.preload()

                try:
                    # ev = pygame.event.wait()
                    ev = self.event_wait()
                    self.profile_time = time.time()

                    if ev.type == DISPLAYTIME:

                        events = 1 + len(pygame.event.get([DISPLAYTIME]))

                        renpy.game.context().runtime += events * DISPLAYTIME_INTERVAL

                        ev = pygame.event.Event(DISPLAYTIME, {},
                                                duration=(time.time() - start_time))

                        # Update the playing music, if necessary.

                        # This needs to be here so that we eventually start a
                        # new song at the end of a fadeout.
                        renpy.display.audio.restore_music()

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

                    rv = root_widget.event(ev, x, y)

                    if rv is not None:
                        break

                except IgnoreEvent:
                    pass

            # But wait, there's more! The finally block runs some cleanup
            # after this.
            return rv

        finally:

            # pygame.time.set_timer(KEYREPEATEVENT, 0)
            pygame.time.set_timer(DISPLAYTIME, 0)
            scene_lists.replace_transient()

            # Clear up the transitions. 
            self.old_scene = current_scene
            self.transition = None
            self.supress_transition = False

            # Redraw the old scene, if any.
            self.force_redraw = True

            # print "It took", frames, "frames."

