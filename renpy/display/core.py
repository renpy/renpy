# This file contains code for initializing and managing the display
# window.

import renpy

import pygame
from pygame.constants import *
import time

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

    def render(self, width, height, shown_time, transition_time):
        """
        Called to display this displayable. This is called with width
        and height parameters, which give the largest width and height
        that this drawable can be drawn to without overflowing some
        bounding box. It's also given two times. It returns a Surface
        that is the current image of this drawable. If the image will
        be need to be redrawn at some time in the future, call
        game.interface.redraw with the time with the delay until the
        next redraw.

        @param shown_time: The time since we first started showing this
        drawable, a float in seconds.

        @param transition_time: The time elapsed since we started the
        current round of showing things to the user, in float seconds.
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
            
        else:
            self.master = [ ]            
            self.transient = [ ]
            self.overlay = [ ]
            self.music = None

    def rollback_copy(self):
        """
        Makes a shallow copy of all the lists, except for the stack,
        which is a 2-level copy.
        """

        rv = SceneLists()
        rv.master = self.master[:]
        rv.transient = self.transient[:]
        rv.overlay = self.overlay[:]

        rv.music = self.music

        return rv
         

    def replace_transient(self):
        """
        Replaces the contents of the transient display list with
        a copy of the master display list. This is used after a
        scene is displayed to get rid of transitions and interface
        elements.
        """

        self.transient = self.master[:]

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
    
    def replace_lists(self, list):
        """
        Clears the master and transient lists, and replaces their
        contents with the contents of the provided list.
        """
        
        self.clear('master')
        self.clear('transient')

        for i in list:
            self.add('master', i, key=None)
            self.add('transient', i, key=None)

    def set_overlay(self, new_overlay):
        """
        This replaces the overlay scene list with the provided overlay
        scene list.
        """

        self.overlay = [ (None, time.time(), i) for i in new_overlay ]


class Display(object):
    """
    This is responsible for managing the display window.

    @ivar window: The window that is being presented to the user.

    @ivar sample_surface: A sample surface that is optimized for
    fast blitting to thew window. Used to create other surfaces from.

    @ivar fullscreen: Is the window in fullscreen mode?
    """


    def __init__(self):

        # It shouldn't matter if pygame is already initialized.
        pygame.init()

        self.fullscreen = renpy.config.fullscreen
        fsflag = 0

        if renpy.config.fullscreen:
            fsflag = FULLSCREEN


        self.window = pygame.display.set_mode((renpy.config.screen_width,
                                               renpy.config.screen_height),
                                              fsflag | DOUBLEBUF)

        pygame.display.set_caption(renpy.config.window_title)

        self.sample_surface = self.window.convert_alpha()

    def screenshot(self, filename):
        """
        Saves a screenshot of the current window into the given filename.
        """

        pygame.image.save(self.window, filename)
                
    def show(self, transient, start_time):
        """
        Draws the current transient screen list to the screen.
        
        @returns A list of offsets corresponding to each widget,
        relative to the screen.
        """

        rv = [ ]
        t = time.time()

        self.window.fill((0, 0, 0, 255))

        for key, base_start_time, d in transient:

            surf = d.render(renpy.config.screen_width,
                            renpy.config.screen_height,
                            t - base_start_time,
                            t - start_time)

            if not surf:
                rv.append((0, 0))
                continue
            
            # Fix the location. If the width of the surface is less
            # than the width of the window, center the surface. If the
            # height is less, then align the surface to the bottom of
            # the screen.

            width, height = surf.get_size()

            xo = (renpy.config.screen_width - width) / 2
            if xo < 0:
                xo = 0

            yo = (renpy.config.screen_height - height)
            if yo < 0:
                yo = 0

            # Draw the image to the screen.

            self.window.blit(surf, (xo, yo))
            rv.append((xo, yo))


        pygame.display.flip()
        return rv


class Interface(object):
    """
    This represents the user interface that interacts with the user.
    It manages the Display objects that display things to the user, and
    also handles accepting and responding to user input.

    @ivar display: The display that we used to display the screen.

    @ivar needs_reraw: True if we need a redraw now.
    
    @ivar profile_time: The time of the last profiling.
    """

    def __init__(self):
        self.display = Display()
        self.needs_redraw = False
        self.profile_time = time.time()

    def redraw(self, delay=0.0):
        """
        Called to indicate that the screen has changed in some way, and
        needs to be redrawn.

        @param delay: The time from now at which the redraw needs to
        be performed, in fractional seconds.
        """

        self.needs_redraw = True

        # TODO: Queue up a redraw, when needed. Do this by either
        # (re)scheduling a timer, or posting an event.
    
    def interact(self):
        """
        This handles one cycle of displaying an image to the user,
        and then responding to user input.
        """

        scene_lists = renpy.game.context().scene_lists

        underlay = [ ( None, 0, i) for i in renpy.config.underlay ]
        overlay = [ ( None, 0, i ) for i in renpy.config.overlay ] 

        transient = underlay + scene_lists.transient + scene_lists.overlay + overlay

        # Compute the reversed list, which is in the right order
        # for handling events on.
        rev_transient = transient[:]
        rev_transient.reverse()

        start_time = time.time()

        # Redraw the screen during every interaction.
        self.needs_redraw = True

        # This list of offsets will be filled in before we need
        # it. It's kept in reverse order of the transient list
        # (The same order as rev_transient.)
        offsets = [ ]

        rv = None
        
        while rv is None:

            if self.display.fullscreen != renpy.config.fullscreen:
                self.display = Display()
                self.needs_redraw = True

            if self.needs_redraw:
                self.needs_redraw = False

                draw_start = time.time()

                offsets = self.display.show(transient, start_time)
                offsets.reverse()

                # If profiling is enabled, report the profile time.
                if renpy.config.profile:
                    new_time = time.time()
                    print "Profile: Redraw took %f seconds." % (new_time - draw_start)
                    print "Profile: %f seconds between event and display." % (new_time - self.profile_time)

            # Update the playing music, if necessary.
            renpy.music.restore()

            try:
                ev = pygame.event.wait()
                self.profile_time = time.time()

                # Handle quit specially for now.
                if ev.type == QUIT:
                    raise renpy.game.QuitException()

                # Merge mousemotion events.
                if ev.type == MOUSEMOTION:
                    evs = pygame.event.get([MOUSEMOTION])

                    if len(evs):
                        ev = evs[-1]

                x, y = getattr(ev, 'pos', (0, 0))

                for (k, t, d), (xo, yo) in zip(rev_transient, offsets):
                    rv = d.event(ev, x - xo, y - yo)

                    if rv is not None:
                        break

            except IgnoreEvent:
                pass
                
        scene_lists.replace_transient()
        return rv
