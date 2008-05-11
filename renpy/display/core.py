# Copyright 2004-2008 PyTom <pytom@bishoujo.us>
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

# This file contains code for initializing and managing the display
# window.

import renpy

import pygame
from pygame.constants import *
import sys
import os
import time
import cStringIO
import threading

# Is the cpu idle enough to do other things?
cpu_idle = threading.Event()
cpu_idle.clear()



TIMEEVENT = USEREVENT + 1
PERIODIC = USEREVENT + 2
JOYEVENT = USEREVENT + 3
REDRAW = USEREVENT + 4

# The number of msec between periodic events.
PERIODIC_INTERVAL = 50

# Time management.
time_base = None

def init_time():
    global time_base
    time_base = time.time() - pygame.time.get_ticks() / 1000.0

def get_time():
    return time_base + pygame.time.get_ticks() / 1000.0

class IgnoreEvent(Exception):
    """
    Exception that is raised when we want to ignore an event, but
    also don't want to return anything.
    """

    pass


# Names for anchors.
anchors = dict(
    left=0.0,
    right=1.0,
    center=0.5,
    top=0.0,
    bottom=1.0,
    )

class Displayable(renpy.object.Object):
    """
    The base class for every object in Ren'Py that can be
    displayed to the screen.

    Drawables will be serialized to a savegame file. Therefore, they
    shouldn't store non-serializable things (like pygame surfaces) in
    their fields.
    """

    activated = False
    focusable = False
    full_focus_name = None
    role = ''
    
    def __init__(self, focus=None, default=False, style='default', **properties):
        self.style = renpy.style.Style(style, properties, heavy=True)
        self.focus_name = focus
        self.default = default

    def find_focusable(self, callback, focus_name):

        focus_name = self.focus_name or focus_name
        
        if self.focusable:
            callback(self, focus_name)

        for i in self.visit():
            if i is None:
                continue

            i.find_focusable(callback, focus_name)
            


    def focus(self, default=False):
        """
        Called to indicate that this widget has the focus.
        """

        if not self.activated:
            self.set_style_prefix(self.role + "hover_")
        
        if not default and not self.activated:
            renpy.audio.sound.play(self.style.sound)

    def unfocus(self):
        """
        Called to indicate that this widget has become unfocused.
        """

        if not self.activated:
            self.set_style_prefix(self.role + "idle_")



    def is_focused(self):
        return renpy.game.context().scene_lists.focused is self

    def set_style_prefix(self, prefix):
        """
        Called to set the style prefix of this widget and its child
        widgets, if any.
        """

        if prefix == self.style.prefix:
            return
        
        # if prefix == self.style_prefix:
        #    return

        self.style.set_prefix(prefix)
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

        return self.style.get_placement()
    
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

    def place(self, dest, x, y, width, height, surf, xoff=None, yoff=None, main=True):
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
        
        xpos, ypos, xanchor, yanchor, xoffset, yoffset = self.get_placement()

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

        if isinstance(xanchor, int):
            xoff -= xanchor
        else:            
            xanchor = anchors.get(xanchor, xanchor)
            xoff -= int(sw * xanchor)

        xoff += x

        # y

        if yoff is None:
            yoff = ypos

        if isinstance(yoff, float):
            yoff = int(yoff * height)

        if isinstance(yanchor, int):
            yoff -= yanchor
        else:            
            yanchor = anchors.get(yanchor, yanchor)
            yoff -= int(sh * yanchor)

        yoff += y

        # Add in offsets.
        xoff += xoffset
        yoff += yoffset
        
        dest.blit(surf, (xoff, yoff), main=main)

        return xoff, yoff

class ImagePredictInfo(renpy.object.Object):
    """
    This stores information involved in image prediction.
    """

    def after_setstate(self):
        for i in renpy.config.layers + renpy.config.top_layers:
            self.images.setdefault(i, {})
    
    def __init__(self, ipi=None):

        # layer -> (tag -> image name)
        self.images = { }

        if ipi is None:
            for i in renpy.config.layers + renpy.config.top_layers:
                self.images[i] = { }
        else:
            for i in renpy.config.layers + renpy.config.top_layers:
                self.images[i] = ipi.images[i].copy()
            
                
    def showing(self, layer, name):

        shown = self.images[layer].get(name[0], None)
        
        if shown is None or len(shown) < len(name):
            return False

        for a, b in zip(name, shown):
            if a != b:
                return False

        return True

    def predict_scene(self, layer):
        self.images[layer].clear()

    def predict_show(self, name, layer):
        self.images[layer][name[0]] = name
        
    def predict_hide(self, tag, layer):
        self.images[layer].pop(tag, None)
    

class SceneLists(renpy.object.Object):
    """
    This stores the current scene lists that are being used to display
    things to the user. 
    """

    __version__ = 1
    
    def after_setstate(self):
        for i in renpy.config.layers + renpy.config.top_layers:
            if i not in self.layers:
                self.layers[i] = [ ]
                self.at_list[i] = { }

    def after_upgrade(self, version):

        if version < 1:

            self.at_list = { }
            self.layer_at_list = { }

            for i in renpy.config.layers + renpy.config.top_layers:
                self.at_list[i] = { }
                self.layer_at_list[i] = (None, [ ])
                

    def __init__(self, oldsl, ipi):

        # A map from layer name -> list of
        # (key, zorder, show time, animation time, displayable) 
        self.layers = { }
        self.at_list = { }
        self.layer_at_list = { }
        
        self.image_predict_info = ipi
        
        if oldsl:

            for i in renpy.config.layers + renpy.config.top_layers:
                try:
                    self.layers[i] = oldsl.layers[i][:]
                except KeyError:
                    self.layers[i] = [ ]

                self.at_list[i] = oldsl.at_list[i].copy()
                self.layer_at_list[i] = oldsl.layer_at_list[i]
                
            for i in renpy.config.overlay_layers:
                self.clear(i)

            self.replace_transient()

            self.movie = oldsl.movie
            self.focused = None
            
        else:
            for i in renpy.config.layers + renpy.config.top_layers:
                self.layers[i] = [ ]
                self.at_list[i] = { }
                self.layer_at_list[i] = (None, [ ])
                
            self.music = None
            self.movie = None
            self.focused = None

    def replace_transient(self):
        """
        Replaces the contents of the transient display list with
        a copy of the master display list. This is used after a
        scene is displayed to get rid of transitions and interface
        elements.
        """

        for i in renpy.config.transient_layers:
            self.layers[i] = [ ]
            self.at_list[i].clear()
            self.image_predict_info.images[i].clear()
            self.layer_at_list[i] = (None, [ ])
            
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

    def add(self, layer, thing, key=None, zorder=0, behind=[ ], at_list=[ ], name=None):
        """
        This is called to add something to a layer. Layer is
        the name of the layer that we need to add the thing to,
        one of 'master' or 'transient'. Key is an optional key. Zorder
        is a place in the zorder to add the thing. Behind is a list of keys
        this thing must be placed below, within the zorder.

        If key is provided, and there exists something in the selected
        layer with the given key, and the same zorder, that entry from
        the layer is replaced with the supplied displayable. If the
        same key exists, but a different zorder, the thing with the
        old key is removed.

        Otherwise, the displayable is placed in the given zorder, behind all
        keys listed in behind. If no keys are listed in behind, the
        displayable is placed at the end of the zorder.
        """

        if not isinstance(thing, Displayable):
            raise Exception("Attempting to show something that isn't a displayable:" + repr(thing))
        
        if layer not in self.layers:
            raise Exception("Trying to add something to non-existent layer '%s'." % layer)

        if key:
            self.at_list[layer][key] = at_list

        if key and name:
            self.image_predict_info.images[layer][key] = name
                
        l = self.layers[layer]

        at = None
        st = None

        if key is not None:
            for index, (k, zo, st, at, d) in enumerate(l):
                if k == key:
                    break
            else:
                index = None
                at = None

            st = None

            if index is not None:
                if zorder == zo:                
                    l[index] = (key, zorder, st, at, thing)
                    return
                else:
                    l.pop(index)

        index = 0
        for index, (behind_key, zo, ignore_st, ignore_at, ignore_thing) in enumerate(l):
            if zo == zorder and behind_key in behind:
                break

            if zo > zorder:
                break
        else:
            index = len(l)

        l.insert(index, (key, zorder, st, at, thing))

    def remove(self, layer, thing):
        """
        Thing is either a key or a displayable. This iterates through the
        named layer, searching for entries matching the thing.
        When they are found, they are removed from the displaylist.

        It's not an error to remove something that isn't in the layer in
        the first place.
        """

        if layer not in self.layers:
            raise Exception("Trying to remove something from non-existent layer '%s'." % layer)
        
        l = self.layers[layer]
        l = [ (k, zo, st, at, d) for k, zo, st, at, d in l if k != thing if d is not thing ]
        self.layers[layer] = l

        self.at_list[layer].pop(thing, None)
        self.image_predict_info.images[layer].pop(thing, None)
            

    def clear(self, layer):
        """
        Clears the named layer, making it empty.
        """

        if layer not in self.layers is None:
            raise Exception("Trying to clear non-existent layer '%s'." % layer)

        self.layers[layer] = [ ]
        self.at_list[layer].clear()
        self.image_predict_info.images[layer].clear()
        self.layer_at_list[layer] = (None, [ ])

    def set_layer_at_list(self, layer, at_list):
        self.layer_at_list[layer] = (None, list(at_list))
        
    def set_times(self, time):
        """
        This finds entries with a time of None, and replaces that
        time with the given time.
        """

        for l, (t, list) in self.layer_at_list.items():
            self.layer_at_list[l] = (t or time, list)
        
        for l in self.layers.values():
            ll = [ ]

            for i in range(0, len(l)):
                k, zo, st, at, d = l[i]
                ll.append((k, zo, st or time, at or time, d))

            l[:] = ll
            

    def showing(self, layer, name):
        """
        Returns true if something with the prefix of the given name
        is found in the scene list.
        """

        return self.image_predict_info.showing(layer, name)

    def make_layer(self, layer, properties):
        """
        Creates a Fixed with the given layer name and scene_list.
        """

        rv = renpy.display.layout.MultiBox(layout='fixed', focus=layer, **properties)
        rv.append_scene_list(self.layers[layer])

        time, at_list = self.layer_at_list[layer]

        if at_list:
            for a in at_list:
                rv = a(rv)

                f = renpy.display.layout.MultiBox(layout='fixed')
                f.add(rv, time, time)
                rv = f

        rv.layer_name = layer
        return rv
    

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

        init_time()
        
        # Setup screen.
        fullscreen = renpy.game.preferences.fullscreen

        # If we're in fullscreen mode, and changing to another mode, go to
        # windowed mode first.
        s = pygame.display.get_surface()
        if s and (s.get_flags() & FULLSCREEN):
            fullscreen = False
            
        self.fullscreen = fullscreen

        if os.environ.get('RENPY_DISABLE_FULLSCREEN', False):
            fullscreen = False
            self.fullscreen = renpy.game.preferences.fullscreen

#         if fullscreen == "16:9":
#             fsratio = 16.0 / 9.0
#         elif fullscreen == "16:10":
#             fsratio = 16.0 / 10.0
#         elif fullscreen: # 4:3 mode.
#             fsratio = 4.0 / 3.0
#         else:
#             fsratio = None

        if fullscreen:
            fsflag = FULLSCREEN
#             width = int(max(renpy.config.screen_width, renpy.config.screen_height * fsratio))
#             height = int(max(renpy.config.screen_height, renpy.config.screen_width / fsratio))
#             self.screen_xoffset = (width - renpy.config.screen_width) / 2
#             self.screen_yoffset = (height - renpy.config.screen_height) / 2            
        else:
            fsflag = 0

        width = renpy.config.screen_width
        height = renpy.config.screen_height
        self.screen_xoffset = 0
        self.screen_yoffset = 0
            
        # Window icon.
        if renpy.config.window_icon:
            pygame.display.set_icon(
                renpy.display.scale.image_load_unscaled(
                    renpy.loader.load(renpy.config.window_icon),
                    renpy.config.window_icon))
            
        # The window we display things in.
        self.window = pygame.display.set_mode((width, height), fsflag, 32)

        # Window title.
        pygame.display.set_caption(renpy.config.window_title.encode("utf-8"))


        # Sample surface that all surfaces are created based on.
        sample = pygame.Surface((10, 10))
        self.sample_surface = sample.convert_alpha()

        pygame.event.set_grab(False)

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

        self.mouse_event_time = get_time()
        
        # Used for HW mouse.
        self.mouse_old_visible = None
        
        self.suppressed_blit = False
        self.full_redraw = True

        self.next_frame = 0

        # A tree of surfaces from the last time the screen was rendered.
        self.surftree = None
        
        # Setup periodic event.
        pygame.time.set_timer(PERIODIC, PERIODIC_INTERVAL)

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

    def mouse_event(self, ev):

        if ev.type == pygame.MOUSEMOTION or pygame.MOUSEBUTTONDOWN or pygame.MOUSEBUTTONUP:
            self.mouse_event_time = get_time()
         
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

        # Figure out if the mouse visibility algorithm is hiding the mouse.
        if self.mouse_event_time + renpy.config.mouse_hide_time < get_time():
            visible = False
        else:
            visible = renpy.store.mouse_visible

        # Deal with a hardware mouse, the easy way.
        if not self.mouse:

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

        if (pos == self.mouse_location and
            show_mouse and
            info == self.mouse_info):
            
            return [ ]

        updates = [ ]

        if self.mouse_location:
            updates.append(self.hide_mouse())

        if visible and pos:
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

            damage = renpy.display.render.screen_blit(surftree, self.full_redraw, self.screen_xoffset, self.screen_yoffset)

            if damage:
                updates.extend(damage)

            self.full_redraw = False

            updates.extend(self.draw_mouse(True))
            pygame.display.update(updates)

        else:
            self.full_redraw = True
            
        self.suppressed_blit = suppress_blit

        renpy.display.focus.take_focuses(surftree.focuses)

        self.surftree = surftree
        
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

    @ivar old_scene: The last thing that was displayed to the screen.

    @ivar transition: A map from layer name to the transition that will
    be applied the next time interact restarts.

    @ivar transition_time: A map from layer name to the time the transition
    involving that layer started.

    @ivar transition_from: A map from layer name to the scene that we're
    transitioning from on that layer.
    
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
        self.profile_time = get_time()
        self.screenshot = None
        self.old_scene = { }
        self.transition = { }
        self.ongoing_transition = { }
        self.transition_time = { }
        self.transition_from = { }
        self.suppress_transition = False
        self.quick_quit = False
        self.force_redraw = False
        self.restart_interaction = False
        self.pushed_event = None
        self.ticks = 0
        self.mouse = 'default'
        self.timeout_time = None
        self.last_event = None
        self.current_context = None
        
        # Should we reset the display?
        self.display_reset = False
        
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
                

        # A stack giving the values of self.transition and self.transition_time
        # for contexts outside the current one. This is used to restore those
        # in the case where nothing has changed in the new context.
        self.transition_info_stack = [ ]
                
                
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


    def do_with(self, trans, paired, clear=False):
        
        if renpy.config.with_callback:
            trans = renpy.config.with_callback(trans, paired)

        if (not trans) or self.suppress_transition:
            self.with_none()
            return False
        else:
            self.set_transition(trans)
            return self.interact(trans_pause=True,
                                 suppress_overlay=not renpy.config.overlay_during_with,
                                 mouse='with',
                                 clear=clear)

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

    def set_transition(self, transition, layer=None, force=False):
        """
        Sets the transition that will be performed as part of the next
        interaction.
        """

        if self.suppress_transition and not force:
            return

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
        else:
            rv = pygame.event.poll()

        self.last_event = rv
        return rv
            

    def event_wait(self):
        """
        This is in its own function so that we can track in the
        profiler how much time is spent in interact.
        """

        if self.pushed_event:
            rv = self.pushed_event
            self.pushed_event = None
            self.last_event = rv
            return rv

        while renpy.display.im.cache.needs_preload():
            ev = pygame.event.poll()
            if ev.type != NOEVENT:
                self.last_event = ev
                return ev

            renpy.display.im.cache.preload()
            
        try:
            cpu_idle.set()            
            ev = pygame.event.wait()
        finally:
            cpu_idle.clear()

        self.last_event = ev
        return ev


    def compute_scene(self, scene_lists):
        """
        This converts scene lists into a dictionary mapping layer
        name to a Fixed containing that layer.
        """

        rv = { }

        for layer in renpy.config.layers + renpy.config.top_layers:
            rv[layer] = scene_lists.make_layer(layer, self.layer_properties[layer])

        root = renpy.display.layout.MultiBox(layout='fixed')
        root.layers = { }

        for layer in renpy.config.layers:
            root.layers[layer] = rv[layer]
            root.add(rv[layer])
        rv[None] = root
             
        return rv
            

    def interact(self, clear=True, **kwargs):
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
            if clear:
                scene_lists = renpy.game.context().scene_lists
                scene_lists.replace_transient()

            self.ongoing_transition = { }
            self.transition_time = { }
            self.transition_from = { }
                
            self.restart_interaction = True
        
    def interact_core(self,
                      show_mouse=True,
                      trans_pause=False,
                      suppress_overlay=False,
                      suppress_underlay=False,
                      mouse='default',
                      preloads=[],
                      roll_forward=None,
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
        
        suppress_overlay = suppress_overlay or renpy.store.suppress_overlay        
        suppress_transition = renpy.config.skipping

        # The global one.
        self.suppress_transition = False

        # Figure out transitions.
        for k in self.transition:
            if k not in self.old_scene:
                continue
            
            self.ongoing_transition[k] = self.transition[k]            
            self.transition_from[k] = self.old_scene[k]
            self.transition_time[k] = None

        self.transition.clear()
                
        ## Safety condition, prevents deadlocks.
        if trans_pause:
            if not self.ongoing_transition:
                return False, None
            if None not in self.ongoing_transition:
                return False, None
            if suppress_transition:
                return False, None
            if not self.old_scene:
                return False, None
            
        # We just restarted.
        self.restart_interaction = False

        # Setup the mouse.
        self.mouse = mouse

        # The start and end times of this interaction.
        start_time = get_time()
        end_time = start_time

        # frames = 0

        for i in renpy.config.interact_callbacks:
            i()

        # Tick time forward.
        renpy.display.im.cache.tick()

        # Cleare the size groups.
        renpy.display.layout.size_groups.clear()
        
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

        # The root widget of everything that is displayed on the screen.
        root_widget = renpy.display.layout.MultiBox(layout='fixed') 
        root_widget.layers = { }

        # A list of widgets that are roots of trees of widgets that are
        # considered for focusing.
        focus_roots = [ ]

        # Add the underlay to the root widget.
        if not suppress_underlay:
            for i in renpy.config.underlay:
                root_widget.add(i)
                focus_roots.append(i)

            if roll_forward is not None:
                rfw = renpy.display.behavior.RollForward(roll_forward)
                root_widget.add(rfw)
                focus_roots.append(rfw)
                
                
        # Figure out the scene. (All of the layers, and the root.)
        scene = self.compute_scene(scene_lists)

        # If necessary, load all images here.
        if renpy.config.load_before_transition:
            for w in scene.itervalues():
                w.predict(renpy.display.im.cache.get)

        # The root widget of all of the layers.
        layers_root = renpy.display.layout.MultiBox(layout='fixed')
        layers_root.layers = { }

        def add_layer(where, layer):

            scene_layer = scene[layer]
            focus_roots.append(scene_layer)

            if (self.ongoing_transition.get(layer, None) and
                 not suppress_transition):

                trans = self.ongoing_transition[layer](
                    old_widget=self.transition_from[layer],
                    new_widget=scene_layer)
                                               
                if not isinstance(trans, Displayable):
                    raise Exception("Expected transition to be a displayable, not a %r" % trans)

                transition_time = self.transition_time.get(layer, None)
                
                where.add(trans, transition_time, transition_time)
                where.layers[layer] = trans
                
            else:
                where.layers[layer] = scene_layer
                where.add(scene_layer)

        # Add layers (perhaps with transitions) to the layers root.
        for layer in renpy.config.layers:
            add_layer(layers_root, layer)
                
        # Add layers_root to root_widget, perhaps through a transition.
        if (None in self.ongoing_transition and
            not suppress_transition):

            trans = self.ongoing_transition[None](
                old_widget=self.transition_from[None],
                new_widget=layers_root)

            if not isinstance(trans, Displayable):
                raise Exception("Expected transition to be a displayable, not a %r" % trans)
            
            transition_time = self.transition_time.get(None, None)

            root_widget.add(trans, transition_time, transition_time)

            if trans_pause:
                sb = renpy.display.behavior.SayBehavior()
                root_widget.add(sb)
                focus_roots.append(sb)

                pb = renpy.display.behavior.PauseBehavior(trans.delay)
                root_widget.add(pb, transition_time, transition_time)
                focus_roots.append(pb)
                
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

        # Okay, from here on we now have a single root widget (root_widget),
        # which we will try to show to the user.

        # Figure out what should be focused.
        renpy.display.focus.before_interact(focus_roots)

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

        # We only want to do autosave once.
        did_autosave = False
        
        old_timeout_time = None
        old_redraw_time = None

        rv = None

        # Start sound.
        renpy.audio.audio.interact()

        # This try block is used to force cleanup even on termination
        # caused by an exception propigating through this function.
        try: 

            while rv is None:

                # Check for a change in fullscreen preference, or a triggered display reset.
                if self.display.fullscreen != renpy.game.preferences.fullscreen or self.display_reset:
                    self.display = Display(self)
                    needs_redraw = True
                    self.display_reset = False

                # Check for a forced redraw.
                if self.force_redraw:
                    needs_redraw = True
                    self.force_redraw = False

                # Redraw the screen.
                if needs_redraw and self.display.can_redraw(first_pass):
                    
                    # If we have a movie, start showing it.
                    suppress_blit = renpy.display.video.interact()

                    # Draw the screen.
                    self.frame_time = get_time()

                    if not self.interact_time:
                        self.interact_time = self.frame_time

                    self.display.show(root_widget, suppress_blit)
                    
                    if first_pass:
                        scene_lists.set_times(self.interact_time)
                        for k, v in self.transition_time.iteritems():
                            if v is None:
                                self.transition_time[k] = self.interact_time

                    renpy.config.frames += 1

                    # If profiling is enabled, report the profile time.
                    if renpy.config.profile :
                        new_time = get_time()
                        print "Profile: Redraw took %f seconds." % (new_time - self.frame_time)
                        print "Profile: %f seconds to complete event." % (new_time - self.profile_time)

                        
                    if first_pass and self.last_event:
                        x, y = pygame.mouse.get_pos()
                        x -= self.display.screen_xoffset
                        y -= self.display.screen_yoffset
                        renpy.display.focus.mouse_handler(self.last_event, x, y, default=False)

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
                        self.profile_time = get_time()
                    continue

                # Predict images, if we haven't done so already.
                if not did_prediction and not self.event_peek():
                    root_widget.predict(renpy.display.im.cache.preload_image)

                    for w in preloads:
                        w.predict(renpy.display.im.cache.preload_image)

                    renpy.game.context().predict(renpy.display.im.cache.preload_image)
                    did_prediction = True


                try:

                    # Times until events occur.
                    # We use large values to approximate infinity.
                    redraw_in = 3600
                    timeout_in = 3600
                    
                    # Handle the redraw timer.
                    redraw_time = renpy.display.render.redraw_time()

                    if redraw_time and not needs_redraw:

                        if redraw_time != old_redraw_time:
                            time_left = redraw_time - get_time()
                            time_left = min(time_left, 3600)
                            redraw_in = time_left
                            pygame.time.set_timer(REDRAW, max(int(time_left * 1000), 1))
                            old_redraw_time = redraw_time
                    else:
                        pygame.time.set_timer(REDRAW, 0)

                    # Handle the timeout timer.
                    if not self.timeout_time:
                        pygame.time.set_timer(TIMEEVENT, 0)
                        ev = None
                    else:
                        time_left = self.timeout_time - get_time() 
                        time_left = min(time_left, 3600)
                        redraw_in = time_left
                        
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

                    # Handle autosaving, as necessary.
                    if not did_autosave and not needs_redraw and not self.event_peek() and redraw_in > .25 and timeout_in > .25:
                        renpy.loadsave.autosave()
                        did_autosave = True
                        
                    # Get the event, if we don't have one already.
                    if ev is None:
                        if needs_redraw:
                            ev = self.event_poll()
                        else:
                            ev = self.event_wait()

                    if ev.type == NOEVENT:
                        continue

                    if renpy.config.profile:
                        self.profile_time = get_time()

                    
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

                    
                    # This checks the event to see if it's a mouse event,
                    # and updates the mouse event timer as appropriate.
                    self.display.mouse_event(ev)
                    
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
                    y -= self.display.screen_yoffset

                    self.event_time = end_time = get_time()


                    # Handle the event normally.
                    rv = renpy.display.focus.mouse_handler(ev, x, y)

                    if rv is None:
                        rv = root_widget.event(ev, x, y, 0)

                    if rv is None:
                        rv = renpy.display.focus.key_handler(ev)

                    if rv is not None:
                        break

                    # Handle displayable inspector.
                    if renpy.config.inspector and renpy.display.behavior.inspector(ev):
                        l = self.display.surftree.main_displayables_at_point(x, y, renpy.config.transient_layers + renpy.config.overlay_layers)
                        renpy.game.invoke_in_new_context(renpy.config.inspector, l)
                        
            
                except IgnoreEvent:
                    # An ignored event can change the timeout. So we want to
                    # process an TIMEEVENT to ensure that the timeout is
                    # set correctly.
                    pygame.event.post(self.time_event)
                    

                # Check again after handling the event.
                needs_redraw |= renpy.display.render.process_redraws()

                if self.restart_interaction:
                    return True, None

            # If we were trans-paused and rv is true, suppress
            # transitions up to the next interaction.
            if trans_pause and rv:
                self.suppress_transition = True

                
            # But wait, there's more! The finally block runs some cleanup
            # after this.
            return False, rv

        finally:

            # Clean out the overlay layers.
            for i in renpy.config.overlay_layers:
                scene_lists.clear(i)

            # We no longer disable periodic between interactions.
            # pygame.time.set_timer(PERIODIC, 0)

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

