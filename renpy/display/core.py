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
MUSICEND = USEREVENT + 3

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

    focusable = False

    def __init__(self, focus=None, default=False, style='default', **properties):
        self.style = renpy.style.Style(style, properties)
        self.style_prefix = None
        self.focus_name = focus
        self.default = default

    def find_focusable(self, callback, focus_name):
        if self.focusable:
            callback(self, self.focus_name or focus_name)
            

    def focus(self, default=False):
        """
        Called to indicate that this widget has the focus.
        """

        if self.style.enable_hover:
            if not default:
                renpy.display.audio.play(self.style.hover_sound)
            self.set_style_prefix("hover_")

    def unfocus(self):
        """
        Called to indicate that this widget has become unfocused.
        """

        if self.style.enable_hover:
            self.set_style_prefix("idle_")

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

        if self.style and self.style.background:
            self.style.background.predict(callback)

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

    @ivar focused: The widget that is currently focused.
    """

    def __init__(self, oldsl=None):

        self.layers = { }
         
        if oldsl:

            for i in renpy.config.layers:
                self.layers[i] = oldsl.layers[i][:]

            self.replace_transient()

            self.music = oldsl.music
            self.sticky_positions = oldsl.sticky_positions.copy()
            self.movie = oldsl.movie
            self.focused = oldsl.focused
            
        else:
            for i in renpy.config.layers:
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

        for i in renpy.config.overlay_layers:
            rv.layers[i] = [ ]

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

    def add(self, layer, thing, key=None):
        """
        This is called to add something to a layer. Layer is
        the name of the layer that we need to add the thing to,
        one of 'master' or 'transient'. Key is an optional key.

        If key is provided, and there exists something in the selected
        layer with the given key, that entry from the layer
        is replaced with the supplied displayable, preserving the
        time it was first displayed.

        Otherwise, the displayable is added to the end of the layer, and
        the time it was first displayed is set to the current time.
        """

        if layer not in self.layers:
            raise Exception("Trying to add something to non-existent layer '%s'." % layer)

        l = self.layers[layer]

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
        l = [ (k, t, d) for k, t, d in l if k != thing if d is not thing ]

        self.layers[layer] = l

    def clear(self, layer):
        """
        Clears the named layer, making it empty.
        """

        if layer not in self.layers is None:
            raise Exception("Trying to clear non-existent layer '%s'." % layer)
        
        self.layers[layer] = [ ]
    

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

    @ivar full_redraw: Force a full redraw.
    """


    def __init__(self):


        # Ensure that we kill off the movie when changing screen res.
        renpy.display.video.movie_stop(clear=False)

        renpy.display.audio.pre_init()
        pygame.init()
        renpy.display.audio.init()
        
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
            pygame.display.set_icon(renpy.display.im.load_image(renpy.config.window_icon))
            

        # Load the mouse image, if any.
        if renpy.config.mouse:
            self.mouse = renpy.display.im.load_image(renpy.config.mouse)
            pygame.mouse.set_visible(False)
        else:
            self.mouse = None
            pygame.mouse.set_visible(True)

        self.mouse_location = None
        self.suppress_mouse = False

        self.full_redraw = True

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

            damage = renpy.display.render.screen_blit(surftree, self.full_redraw)
            self.full_redraw = False

            if self.mouse:
                if damage:
                    self.buffer.blit(self.window, damage, damage)
                self.draw_mouse(True)

            if damage:
                pygame.display.update(damage)

        else:
            self.full_redraw = True
            
        self.suppress_mouse = suppress_blit

        renpy.display.focus.take_focuses(surftree.focuses)
        
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

    """

    def __init__(self):
        self.display = Display()
        self.profile_time = time.time()
        self.screenshot = None
        self.old_scene = None
        self.transition = { }
        self.suppress_transition = False
        self.quick_quit = False
        self.force_redraw = False
        self.restart_interaction = False
        self.pushed_event = None

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

        # We don't want the overlay to be clear here.

        if not renpy.config.overlay_during_wait:
            for i in renpy.config.overlay_layers:
                scene_lists.clear(i)

        self.old_scene = self.compute_scene(scene_lists)


        # self.old_scene.append_scene_list(scene_lists.master)

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

        return pygame.event.wait()


    def compute_scene(self, scene_lists):
        """
        This converts scene lists into a dictionary mapping layer
        name to a Fixed containing that layer. None is mapped
        to a fixed containing all of the layers.
        """

        rv = { }

        root = renpy.display.layout.Fixed()

        for layer in renpy.config.layers:
            f = renpy.display.layout.Fixed(focus=layer)
            f.append_scene_list(scene_lists.layers[layer])

            rv[layer] = f
            root.add(f)

        rv[None] = root

        return rv
            

    def interact(self, **kwargs):
        """
        This handles an interaction, restarting it if necessary. All of the
        keyword arguments are passed off to interact_core.
        """

        # These things can be done once per interaction.

        try:

            repeat = True

            while repeat:
                repeat, rv = self.interact_core(**kwargs)
            
            return rv

        finally:

            # Clean out transient stuff at the end of an interaction.
            scene_lists = renpy.game.context().scene_lists
            scene_lists.replace_transient()

        

    def interact_core(self,
                 show_mouse=True,
                 trans_pause=False,
                 suppress_overlay=False,
                 suppress_underlay=False,
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

        self.suppress_transition |= renpy.config.skipping

        ## Safety condition, prevents deadlocks.
        if trans_pause:
            if not self.transition:
                return False, None
            if self.suppress_transition:
                return False, None

        # We just restarted.
        self.restart_interaction = False

        # frames = 0

        # Update the music, if necessary.
        for i in pygame.event.get([ MUSICEND ]):
            renpy.display.audio.music_end_event()

        renpy.display.audio.music_interact()

        # Tick time forward.
        renpy.display.im.cache.tick()

        # Set up key repeats.
        # pygame.time.set_timer(KEYREPEATEVENT, renpy.config.skip_delay)

        # Set up display time event.
        pygame.time.set_timer(DISPLAYTIME, DISPLAYTIME_INTERVAL)

        # Clear some events.
        pygame.event.clear((MOUSEMOTION, DISPLAYTIME,
                            MOUSEBUTTONUP, MOUSEBUTTONDOWN))
        
        # Figure out the scene list we want to show.        
        scene_lists = renpy.game.context().scene_lists
        
        # Figure out what the overlay layer should look like.
        for i in renpy.config.overlay_layers:
            scene_lists.clear(i)

        renpy.ui.layer("overlay")

        if not suppress_overlay:
            for i in renpy.config.overlay_functions:
                i()

        renpy.ui.close()

        # Figure out the underlay layer.
        if not suppress_underlay:
            underlay = [ ( None, 0, i) for i in renpy.config.underlay ]
        else:
            underlay = [ ]

        # The root widget of everything that is displayed on the screen.
        root_widget = renpy.display.layout.Fixed() 
        root_widget.append_scene_list(underlay)

        # Figure out the scene. (All of the layers, and the root.)
        scene = self.compute_scene(scene_lists)

        # If necessary, load all images here.
        if renpy.config.load_before_transition:
            for w in scene.itervalues():
                w.predict(renpy.display.im.cache.get)

        # The start time of transitions.
        start_time = time.time()

        # The root widget of all of the layers.
        layers_root = renpy.display.layout.Fixed()

        # Add layers (perhaps with transitions) to the layers root.
        for layer in renpy.config.layers:
            if layer in self.transition and self.old_scene and not self.suppress_transition:

                trans = self.transition[layer](old_widget=self.old_scene[layer],
                                               new_widget=scene[layer])
                layers_root.add(trans, start_time)
            else:
                layers_root.add(scene[layer], start_time)
                
        # Add layers_root to root_widget, perhaps through a transition.
        if None in self.transition and self.old_scene and not self.suppress_transition:
            trans = self.transition[None](old_widget=self.old_scene[None],
                                          new_widget=layers_root)
            
            root_widget.add(trans, start_time)

            if trans_pause:
                sb = renpy.display.behavior.SayBehavior()
                root_widget.add(sb, start_time)

                pb = renpy.display.behavior.PauseBehavior(trans.delay)
                root_widget.add(pb, start_time)
                
        else:
            root_widget.add(layers_root, start_time)


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

        # Post an event that moves us to the current mouse position.
        # pygame.event.post(pygame.event.Event(MOUSEMOTION,
        #                                     pos=pygame.mouse.get_pos()))
        
        # We only want to do prediction once, but we will defer it as
        # long as possible.
        did_prediction = False
        
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
                    
                    renpy.config.frames += 1

                    # If profiling is enabled, report the profile time.
                    if renpy.config.profile:
                        new_time = time.time()
                        print "Profile: Redraw took %f seconds." % (new_time - draw_start)
                        print "Profile: %f seconds to complete event." % (new_time - self.profile_time)

                # Draw the mouse, if it needs drawing.
                if show_mouse:
                    self.display.draw_mouse()
                    
                # Determine if we need a redraw.
                needs_redraw = renpy.display.render.process_redraws()

                # If we need to redraw again, do it if we don't have an
                # event going on.
                if needs_redraw and not self.event_peek():
                    continue

                # Predict images, if we haven't done so already.
                if not did_prediction and not self.event_peek():
                    root_widget.predict(renpy.display.im.cache.preload_image)
                    renpy.game.context().predict(renpy.display.im.cache.preload_image)
                    did_prediction = True

                try:
                    ev = self.event_wait()
                    self.profile_time = time.time()

                    # A song just ended.
                    if ev.type == MUSICEND:
                        renpy.display.audio.music_end_event()

                    if ev.type == DISPLAYTIME:

                        events = 1 + len(pygame.event.get([DISPLAYTIME]))

                        renpy.game.context().runtime += events * DISPLAYTIME_INTERVAL

                        ev = pygame.event.Event(DISPLAYTIME, {},
                                                duration=(time.time() - start_time))

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

                    renpy.display.focus.event_handler(ev)

                    # x, y = getattr(ev, 'pos', (0, 0))
                    x, y = pygame.mouse.get_pos()

                    rv = root_widget.event(ev, x, y)

                    if rv is not None:
                        break

                except IgnoreEvent:
                    pass

                # Check again after handling the event.
                needs_redraw |= renpy.display.render.process_redraws()

                if self.restart_interaction:
                    return True, None
                    
            # But wait, there's more! The finally block runs some cleanup
            # after this.
            return False, rv

        finally:

            # pygame.time.set_timer(KEYREPEATEVENT, 0)
            pygame.time.set_timer(DISPLAYTIME, 0)

            # Restart the old interaction, which also causes a
            # redraw if needed.
            self.restart_interaction = True

            # print "It took", frames, "frames."

