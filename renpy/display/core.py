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

from typing import Optional, Tuple

import sys
import os
import time
import io
import threading
import copy
import gc
import atexit

import pygame_sdl2 as pygame
import renpy

from renpy.atl import position
from renpy.display.displayable import Displayable, DisplayableArguments, place
from renpy.display.scenelists import SceneListEntry, SceneLists

import_time = time.time()

try:
    import android # @UnresolvedImport
    android.init # Check to see if we have the right module.
except Exception:
    android = None

if renpy.emscripten:
    import emscripten

TIMEEVENT = pygame.event.register("TIMEEVENT")
PERIODIC = pygame.event.register("PERIODIC")
REDRAW = pygame.event.register("REDRAW")
EVENTNAME = pygame.event.register("EVENTNAME")

# All events except for TIMEEVENT and REDRAW
ALL_EVENTS = set(pygame.event.get_standard_events()) # @UndefinedVariable
ALL_EVENTS.add(PERIODIC)
ALL_EVENTS.add(EVENTNAME)

enabled_events = {
    pygame.QUIT,

    pygame.APP_TERMINATING,
    pygame.APP_LOWMEMORY,
    pygame.APP_WILLENTERBACKGROUND,
    pygame.APP_DIDENTERBACKGROUND,
    pygame.APP_WILLENTERFOREGROUND,
    pygame.APP_DIDENTERFOREGROUND,

    pygame.WINDOWEVENT,
    pygame.SYSWMEVENT,

    pygame.KEYDOWN,
    pygame.KEYUP,

    pygame.TEXTEDITING,
    pygame.TEXTINPUT,
    pygame.KEYMAPCHANGED,

    pygame.MOUSEMOTION,
    pygame.MOUSEBUTTONDOWN,
    pygame.MOUSEBUTTONUP,
    pygame.MOUSEWHEEL,

    pygame.JOYAXISMOTION,
    pygame.JOYHATMOTION,
    pygame.JOYBALLMOTION,
    pygame.JOYBUTTONDOWN,
    pygame.JOYBUTTONUP,
    pygame.JOYDEVICEADDED,
    pygame.JOYDEVICEREMOVED,

    pygame.CONTROLLERAXISMOTION,
    pygame.CONTROLLERBUTTONDOWN,
    pygame.CONTROLLERBUTTONUP,
    pygame.CONTROLLERDEVICEADDED,
    pygame.CONTROLLERDEVICEREMOVED,

    pygame.RENDER_TARGETS_RESET,

    TIMEEVENT,
    PERIODIC,
    REDRAW,
    EVENTNAME,
    }

# The number of msec between periodic events.
PERIODIC_INTERVAL = 50

null = None

# Time management.
time_base = 0.0
time_mult = 1.0

# Mouse management.
relx = 0
rely = 0


def init_time():
    warp = os.environ.get("RENPY_TIMEWARP", "1.0")

    global time_base
    global time_mult

    time_base = time.time()
    time_mult = float(warp)


def get_time():
    t = time.time()
    return time_base + (t - time_base) * time_mult


def get_size():
    """
    Returns the screen size. Always returns at least (256, 256), to make sure
    that we don't divide by zero.
    """

    size = pygame.display.get_size()

    if not size:
        return size

    if size[0] >= 256 and size[1] >= 256:
        return size

    return (max(size[0], 256), max(size[1], 256))


def displayable_by_tag(layer, tag):
    """
    Get the displayable on the given layer with the given tag.
    """

    return renpy.game.context().scene_lists.get_displayable_by_tag(layer, tag)


class IgnoreEvent(Exception):
    """
    Exception that is raised when we want to ignore an event, but
    also don't want to return anything.
    """


class EndInteraction(Exception):
    """
    Exception that can be raised (for example, during the render method of
    a displayable) to end the current interaction immediately.
    """

    def __init__(self, value):
        self.value = value


def absolute_wrap(func):
    """
    Wraps func into a method of absolute. The wrapped method
    converts a float result back to absolute.
    """

    def wrapper(*args):
        rv = func(*args)

        if type(rv) is float:
            return absolute(rv)
        else:
            return rv

    return wrapper

class absolute(float):
    """
    This represents an absolute float coordinate.
    """

    __slots__ = ()

    def __repr__(self):
        return "absolute({})".format(float.__repr__(self))

    def __divmod__(self, value):
        return self//value, self%value

    def __rdivmod__(self, value):
        return value//self, value%self

    @staticmethod
    def compute_raw(value, room):
        """
        Converts a position from one of the many supported position types
        into an absolute number of pixels, without regard for the return type.
        """
        if isinstance(value, position):
            return value.relative * room + value.absolute
        elif isinstance(value, (absolute, int)):
            return value
        elif isinstance(value, float):
            return value * room
        raise TypeError("Value {} of type {} not recognized as a position.".format(value, type(value)))

    @staticmethod
    def compute(value, room):
        """
        Does the same, but converts the result to the absolute type.
        """
        return absolute(absolute.compute_raw(value, room))

for fn in (
    '__coerce__', # PY2
    '__div__', # PY2
    '__long__', # PY2
    '__nonzero__', # PY2
    '__rdiv__', # PY2

    '__abs__',
    '__add__',
    # '__bool__', # non-float
    '__ceil__',
    # '__divmod__', # special-cased above, tuple of floats
    # '__eq__', # non-float
    '__floordiv__',
    # '__format__', # non-float
    # '__ge__', # non-float
    # '__gt__', # non-float
    # '__hash__', # non-float
    # '__int__', # non-float
    # '__le__', # non-float
    # '__lt__', # non-float
    '__mod__',
    '__mul__',
    # '__ne__', # non-float
    '__neg__',
    '__pos__',
    '__pow__',
    '__radd__',
    # '__rdivmod__', # special-cased above, tuple of floats
    '__rfloordiv__',
    '__rmod__',
    '__rmul__',
    '__round__',
    '__rpow__',
    '__rsub__',
    '__rtruediv__',
    # '__str__', # non-float
    '__sub__',
    '__truediv__',
    # '__trunc__', # non-float

    # 'as_integer_ratio', # tuple of non-floats
    'conjugate',
    'fromhex',
    # 'hex', # non-float
    # 'is_integer', # non-float
):
    f = getattr(float, fn, None)
    if f is not None: # for PY2-only and PY3-only methods
        setattr(absolute, fn, absolute_wrap(f))

del absolute_wrap, fn, f # type: ignore




class MouseMove(object):
    """
    This contains information about the current mouse move.
    """

    def __init__(self, x, y, duration):
        self.start = get_time()

        if duration is not None:
            self.duration = duration
            self.start_x, self.start_y = renpy.display.draw.get_mouse_pos()
        else:
            self.duration = 4/60.0
            self.start_x, self.start_y = x, y

        self.end_x = x
        self.end_y = y

    def perform(self):
        """
        Performs the mouse move. Returns True if this should be called
        again, or False if the move has finished.
        """

        elapsed = get_time() - self.start

        if elapsed >= self.duration:
            renpy.display.draw.set_mouse_pos(self.end_x, self.end_y)
            return False

        done = 1.0 * elapsed / self.duration

        x = int(self.start_x + done * (self.end_x - self.start_x))
        y = int(self.start_y + done * (self.end_y - self.start_y))

        renpy.display.draw.set_mouse_pos(x, y)
        return True


def get_safe_mode():
    """
    Returns true if we should go into safe mode.
    """

    if renpy.safe_mode_checked:
        return False

    if getattr(renpy.game.args, "safe_mode", False):
        return True

    try:
        if renpy.windows:
            import ctypes

            VK_SHIFT = 0x10

            ctypes.windll.user32.GetKeyState.restype = ctypes.c_ushort # type: ignore
            if ctypes.windll.user32.GetKeyState(VK_SHIFT) & 0x8000: # type: ignore
                return True
            else:
                return False

        # Safe mode doesn't work on other platforms.
        return False

    except Exception:
        return False


class Renderer(object):
    """
    A Renderer (also known as a draw object) is responsible for drawing a
    tree of displayables to the window. It also provides other services that
    involved drawing and the SDL main window, as documented here.

    A Renderer is responsible for updating the renpy.game.preferences.fullscreen
    and renpy.game.preferences.physical_size preferences, when these are
    changed from outside the game.

    A renderer has an info dict, that contains the keys from pygame_sdl2.display.Info(),
    and then:
    - "renderer", the name of the Renderer.
    - "resizable", true if the window can be resized.
    - "additive", true if additive blendering is supported.
    - "models", true if model-based rendering is being used.
    """

    texture_cache = { }

    def get_texture_size(self):
        """
        This returns a pair contining the total amount of memory consumed by
        textures, and a count of the number of textures that exist.
        """

    def update(self, force=False):
        """
        This is called before a draw operation to check to see if the state of
        the draw objects needs to be updated after an external event has occured.
        Things that require draw updates might be:

        * The window has changed its size.
        * The window has changed full-screen status.
        * `force` is given, which generally means that it's likely the GL
          context has become invalid.

        After this has been called, the system should be in a good state for
        rendering.

        Returns True if a redraw is required, False otherwise.
        """

    def init(self, virtual_size):
        """
        This creates a renderer with the given `virtual_size`. It returns
        True of the renderer initialized correctly, False otherwise.
        """

    def quit(self):
        """
        This shuts down the renderer until the next call to ``init``.
        """

    def resize(self):
        """
        This is called to implement resizing and changing the fullscreen
        mode. It is expected to determine the size to use using
        renpy.game.preferences.physical_size, and the fullscreen mode
        using renpy.game.preferences.fullscreen.
        """

    def can_block(self):
        """
        Returns True if we can block to wait for input, False if the screen
        needs to be immediately redrawn.
        """

    def should_redraw(self, needs_redraw, first_pass, can_block):
        """
        Determines if the screen needs to be redrawn. Returns True if it
        does.

        `needs_redraw`
            True if the needs_redraw flag is set.

        `first_pass`
            True if this is the first pass through the interact loop.

        `can_block`
            The value of self.can_block, from above.
        """

    def mutated_surface(self, surf):
        """
        Called to indicated that `surf` has changed and textures based on
        it should not be used.
        """

        if surf in self.texture_cache:
            del self.texture_cache[surf]

    def load_texture(self, surf, transient=False):
        """
        Loads a surface into a texture.

        `surf`
            The pygame.Surface to load.

        `transient`
            True if the texture is unlikely to be used for more than a single
            frame.
        """

    def ready_one_texture(self):
        """
        This is called in the main thread to indicate that one texture
        should be loaded into the GPU.
        """

    def kill_textures(self):
        """
        Removes all cached textures, to free memory.
        """

    def solid_texture(self, w, h, color):
        """
        This is called to create a (`w` x `h`) texture of a single
        color.

        Returns the texture.
        """

    def draw_screen(self, surftree, flip=True):
        """
        This draw the screen.

        `surftree`
            A Render object (the root of a tree of Render objects) that
            will be drawn to the screen.

        `flip`
            If True, the drawing will be presented to the user.
        """

    def render_to_texture(self, what, alpha):
        """
        Converts `what`, a tree of Renders, to a texture of the same size.

        `alpha`
            A hint as to if the texture should have an alpha channel.
        """

    def is_pixel_opaque(self, what, x, y):
        """
        Returns true if the pixel is not 100% transparent.

        `what`
            A tree of renders.

        `x`, `y`
            The coordinates of the pixels to check.
        """

    def get_half(self, what):
        """
        Gets a texture that is half the size of `what`, which may be
        a texture or a tree of Renders.
        """

    def translate_point(self, x, y):
        """
        Translates (`x`, `y`) from physical to virtual coordinates.
        """

        return (0, 0) # type

    def untranslate_point(self, x, y):
        """
        Untranslates (`x`, `y`) from virtual to physical coordinates.
        """

        return (0, 0) # type

    def mouse_event(self, ev):
        """
        This translates the .pos field of `ev` from physical coordinates to
        virtual coordinates. Returns an (x, y) pait of virtual coordinates.
        """

        return ev

    def get_mouse_pos(self):
        """
        Returns the x and y coordinates of the mouse, in virtual coordinates.
        """

        return (0, 0) # type

    def set_mouse_pos(self, x, y):
        """
        Moves the mouse to the virtual coordinates `x` and `y`.
        """

        x, y = self.untranslate_point(x, y)
        pygame.mouse.set_pos([x, y])

    def screenshot(self, surftree):
        """
        This returns a pygame.Surface that is the result of rendering
        `surftree`, a tree of Renders.
        """

    def event_peek_sleep(self):
        """
        On platforms where CPU usage is gated by the need to redraw, sleeps
        a short amount of time to keep the CPU idle.
        """

    def get_physical_size(self):
        """
        Returns the physical size of the window, in physical pixels.
        """


# How long should we be in maximum framerate mode at the start of the game?
initial_maximum_framerate = 0.0


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

        # PNG data and the surface for the current file screenshot.
        self.screenshot = None
        self.screenshot_surface = None

        self.old_scene = { }
        self.transition = { }
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
        self.roll_forward = None

        # Are we in fullscreen mode?
        self.fullscreen = False

        # Things to be preloaded.
        self.preloads = [ ]

        # The time at which this object was initialized.
        self.init_time = get_time()

        # The time at which this draw occurs.
        self.frame_time = 0

        # The time when this interaction occured.
        self.interact_time = None

        # The time we last tried to quit.
        self.quit_time = 0

        # Are we currently processing the quit event?
        self.in_quit_event = False

        self.time_event = pygame.event.Event(TIMEEVENT, { "modal" : False })
        self.redraw_event = pygame.event.Event(REDRAW)

        # Are we focused?
        self.mouse_focused = True
        self.keyboard_focused = True

        # Properties for each layer.
        self.layer_properties = { }

        # Have we shown the window this interaction?
        self.shown_window = False

        # Should we ignore the rest of the current touch? Used to ignore the
        # rest of a mousepress after a longpress occurs.
        self.ignore_touch = False

        # Should we clear the screenshot at the start of the next interaction?
        self.clear_screenshot = False

        # Is our audio paused?
        self.audio_paused = False

        # Transition-related:

        # A map from layer (or None for the root) to the uninstantiate
        # transition object that's on that layer.
        self.ongoing_transition = { }

        # The same, but for the transition after it's been called with the
        # old and new displayables.
        self.instantiated_transition = { }

        # The time an ongoing transition started.
        self.transition_time = { }

        # The displayable that an ongoing transition is transitioning from.
        self.transition_from = { }

        # The previous root transform.
        self.old_root_transform = None

        # Init layers.
        renpy.display.scenelists.init_layers()

        global null
        null = renpy.display.layout.Null()

        for layer in renpy.display.scenelists.layers:
            if layer in renpy.config.layer_clipping:
                x, y, w, h = renpy.config.layer_clipping[layer]
                self.layer_properties[layer] = dict(
                    xpos=x,
                    xanchor=0,
                    ypos=y,
                    yanchor=0,
                    xmaximum=w,
                    ymaximum=h,
                    xminimum=w,
                    yminimum=h,
                    clipping=True,
                    )

            else:
                self.layer_properties[layer] = {}

        # A stack giving the values of self.transition and self.transition_time
        # for contexts outside the current one. This is used to restore those
        # in the case where nothing has changed in the new context.
        self.transition_info_stack = [ ]

        # The time when the event was dispatched.
        self.event_time = 0

        # The time we saw the last mouse event.
        self.mouse_event_time = None

        # Should we show the mouse?
        self.show_mouse = True

        # Should we reset the display?
        self.display_reset = False

        # Should we profile the next frame?
        self.profile_once = False

        # The thread that can do display operations.
        self.thread = threading.current_thread()

        # Init timing.
        init_time()
        self.mouse_event_time = get_time()

        # The current window caption.
        self.window_caption = None

        renpy.game.interface = self
        renpy.display.interface = self

        # Are we in safe mode, from holding down shift at start?
        self.safe_mode = False

        # Do we need a background screenshot?
        self.bgscreenshot_needed = False

        # Event used to signal background screenshot taken.
        self.bgscreenshot_event = threading.Event()

        # The background screenshot surface.
        self.bgscreenshot_surface = None

        # Mouse move. If not None, information about the current mouse
        # move.
        self.mouse_move = None

        # If in text editing mode, the current text editing event.
        self.text_editing = None

        # The text rectangle after the current draw.
        self.text_rect = None

        # The text rectangle after the previous draw.
        self.old_text_rect = None

        # Are we a touchscreen?
        self.touch = renpy.exports.variant("touch")

        # Should we use the touch keyboard?
        self.touch_keyboard = (self.touch and renpy.emscripten) or renpy.config.touch_keyboard

        # Should we restart the interaction?
        self.restart_interaction = True

        # For compatibility with older code.
        if renpy.config.periodic_callback:
            renpy.config.periodic_callbacks.append(renpy.config.periodic_callback)

        # Has start been called?
        self.started = False

        # Are we in fullscreen video mode?
        self.fullscreen_video = False

        self.safe_mode = get_safe_mode()
        renpy.safe_mode_checked = True

        # A scale factor used to compensate for the system DPI.
        self.dpi_scale = self.setup_dpi_scaling()

        renpy.display.log.write("DPI scale factor: %f", self.dpi_scale)

        # A time until which we should draw at maximum framerate.
        self.maximum_framerate_time = 0.0
        self.maximum_framerate(initial_maximum_framerate)

        # True if this is the first interact.
        self.start_interact = True

        # The time of each frame.
        self.frame_times = [ ]

        # The duration of each frame, in seconds.
        self.frame_duration = 1.0 / 60.0

        # The cursor cache.
        self.cursor_cache = None # type: dict|None

        # The old mouse.
        self.old_mouse = None

        # A map from a layer to the duration of the current transition on that
        # layer.
        self.transition_delay = { }

        # Is this the first frame?
        self.first_frame = True

        # Should prediction be forced? This causes the prediction coroutine to
        # be prioritized, and is set to False when it's done, when preloading
        # is done, or at the end of the interaction.
        self.force_prediction = False

        # The number of interactions that have happened without processing an event.
        self.interaction_counter = 0

        # This caches the mod field of the last event that has one, allowing keyboard
        # modifiers to be used with mouse and other events.
        self.mod = 0

        # A queue of functions to invoke at the start of the next interaction.
        # Set by renpy.exports.invoke_in_main_thread.
        self.invoke_queue = [ ]

        try:
            self.setup_nvdrs()
        except Exception:
            pass

    def setup_nvdrs(self):
        from ctypes import cdll, c_char_p
        nvdrs = cdll.nvdrs

        disable_thread_optimization = nvdrs.disable_thread_optimization
        restore_thread_optimization = nvdrs.restore_thread_optimization
        get_nvdrs_error = nvdrs.get_nvdrs_error
        get_nvdrs_error.restype = c_char_p

        renpy.display.log.write("nvdrs: Loaded, about to disable thread optimizations.")

        disable_thread_optimization()
        error = get_nvdrs_error()
        if error:
            renpy.display.log.write("nvdrs: %r (can be ignored)", error)
        else:
            renpy.display.log.write("nvdrs: Disabled thread optimizations.")

        atexit.register(restore_thread_optimization)

    def setup_dpi_scaling(self):

        if "RENPY_HIGHDPI" in os.environ:
            return float(os.environ["RENPY_HIGHDPI"])

        if not renpy.windows:
            return 1.0

        try:
            import ctypes
            from ctypes import c_void_p, c_int

            ctypes.windll.user32.SetProcessDPIAware() # type: ignore

            GetDC = ctypes.windll.user32.GetDC # type: ignore
            GetDC.restype = c_void_p
            GetDC.argtypes = [ c_void_p ]

            ReleaseDC = ctypes.windll.user32.ReleaseDC # type: ignore
            ReleaseDC.argtypes = [ c_void_p, c_void_p ]

            GetDeviceCaps = ctypes.windll.gdi32.GetDeviceCaps # type: ignore
            GetDeviceCaps.restype = c_int
            GetDeviceCaps.argtypes = [ c_void_p, c_int ]

            LOGPIXELSX = 88

            dc = GetDC(None)
            rv = GetDeviceCaps(dc, LOGPIXELSX) / 96.0
            ReleaseDC(None, dc)

            if rv < renpy.config.de_minimus_dpi_scale:
                renpy.display.log.write("De minimus DPI scale, was %r", rv)
                rv = 1.0

            return rv

        except Exception:
            renpy.display.log.write("Could not determine DPI scale factor:")
            renpy.display.log.exception()
            return 1.0

    def get_display_layout(self):
        """
        Get the display layout. A list of rectangles that have monitors in them.
        """

        rv = [ ]
        for i in range(pygame.display.get_num_video_displays()):
            rv.append(pygame.display.get_display_bounds(i))

        return tuple(rv)

    def on_move(self, pos):
        """
        Called when the player moves the window.
        """

        if not (renpy.windows or renpy.macintosh or renpy.linux):
            return

        if renpy.game.preferences.fullscreen or renpy.game.preferences.maximized:
            return

        renpy.game.preferences.window_position = pos
        renpy.game.preferences.window_position_layout = self.get_display_layout()

    def start(self):
        """
        Starts the interface, by opening a window and setting the mode.
        """

        import traceback

        if self.started:
            return

        # Avoid starting on Android if we don't have focus.
        if renpy.android:
            self.check_android_start()

        # Initialize audio.
        pygame.display.hint("SDL_APP_NAME", (renpy.config.name or "Ren'Py Game").encode("utf-8"))
        pygame.display.hint("SDL_AUDIO_DEVICE_APP_NAME", (renpy.config.name or "Ren'Py Game").encode("utf-8"))

        renpy.audio.audio.init()

        # Initialize pygame.
        try:
            pygame.display.init()
            pygame.mouse.init()
        except Exception:
            pass

        self.post_init()

        renpy.display.emulator.init_emulator()

        gc.collect()

        if gc.garbage:
            del gc.garbage[:]

        renpy.display.render.render_ready()

        # Kill off the presplash.
        renpy.display.presplash.end()

        # If we are on the web browser, start preloading the browser cache.
        if renpy.emscripten and renpy.game.preferences.web_cache_preload:
            emscripten.run_script("loadCache()")

        renpy.main.log_clock("Interface start")

        self.started = True

        self.set_mode()

        # Load the image fonts.
        renpy.text.font.load_fonts()

        # Setup periodic event.
        pygame.time.set_timer(PERIODIC, PERIODIC_INTERVAL)

        # Don't grab the screen.
        pygame.event.set_grab(False)

        if not self.safe_mode:
            renpy.display.controller.init()

        pygame.event.get([ pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP ])

        # Create a cache of the the mouse information.
        if renpy.config.mouse:

            self.cursor_cache = { }

            cursors = { }

            for key, cursor_list in renpy.config.mouse.items():

                l = [ ]

                for i in cursor_list:

                    if i not in cursors:
                        fn, x, y = i
                        surf = renpy.display.im.load_surface(fn)
                        cursors[i] = pygame.mouse.ColorCursor(surf, x, y)

                    l.append(cursors[i])

                self.cursor_cache[key] = l

            if ("default" not in self.cursor_cache) and (None in self.cursor_cache):
                self.cursor_cache["default"] = self.cursor_cache[None]

        s = "Total time until interface ready: {}s.".format(time.time() - import_time)

        if renpy.android and not renpy.config.log_to_stdout:
            print(s)

        # Clear out any pending events.
        pygame.event.get()

        for i in renpy.config.display_start_callbacks:
            i()


    def post_init(self):
        """
        This is called after display init, but before the window is created.
        """

        pygame.display.hint("SDL_VIDEO_X11_NET_WM_BYPASS_COMPOSITOR", "0")
        pygame.display.hint("SDL_VIDEO_MINIMIZE_ON_FOCUS_LOSS", "0")
        pygame.display.hint("SDL_TOUCH_MOUSE_EVENTS", "1")
        pygame.display.hint("SDL_MOUSE_TOUCH_EVENTS", "0")
        pygame.display.hint("SDL_EMSCRIPTEN_ASYNCIFY", "0")
        pygame.display.hint("SDL_IME_SHOW_UI", "1")

        if renpy.config.mouse_focus_clickthrough:
            pygame.display.hint("SDL_MOUSE_FOCUS_CLICKTHROUGH", "1")

        pygame.display.set_screensaver(renpy.config.allow_screensaver)

        # Needed for Ubuntu Unity.
        wmclass = renpy.config.save_directory or os.path.basename(sys.argv[0])
        os.environ['SDL_VIDEO_X11_WMCLASS'] = wmclass

        self.set_window_caption(force=True)
        self.set_icon()

        if renpy.android:
            android.wakelock(True)

        # Block events we don't use.
        for i in pygame.event.get_standard_events():

            if i in enabled_events:
                continue

            if i in renpy.config.pygame_events:
                continue

            pygame.event.set_blocked(i)

        # Fix a problem with fullscreen and maximized.
        if renpy.game.preferences.fullscreen:
            renpy.game.preferences.maximized = False

    def after_first_frame(self):
        """
        Called after the first frame has been drawn.
        """

        if renpy.android:
            from jnius import autoclass
            PythonSDLActivity = autoclass("org.renpy.android.PythonSDLActivity")
            PythonSDLActivity.hidePresplash()

            print("Hid presplash.")

    def set_icon(self):
        """
        This is called to set up the window icon.
        """

        # Window icon.
        icon = renpy.config.window_icon

        if icon:

            try:
                with renpy.loader.load(icon, directory="images") as f:
                    im = renpy.display.scale.image_load_unscaled(
                        f,
                        icon,
                        )

                # Convert the aspect ratio to be square.
                iw, ih = im.get_size()
                imax = max(iw, ih)
                square_im = renpy.display.pgrender.surface_unscaled((imax, imax), True)
                square_im.blit(im, ((imax - iw) // 2, (imax - ih) // 2))
                im = square_im

                if im.get_size()[0] > 1024:
                    im = renpy.display.scale.smoothscale(im, (1024, 1024))

                pygame.display.set_icon(im)
            except renpy.webloader.DownloadNeeded:
                pass

    def set_window_caption(self, force=False):

        window_title = renpy.config.window_title

        if window_title is None:
            window_title = "A Ren'Py Game"

        caption = renpy.translation.translate_string(window_title) + renpy.store._window_subtitle

        if renpy.exports.get_autoreload():
            caption += " - autoreload"

        if not force and caption == self.window_caption:
            return

        self.window_caption = caption
        pygame.display.set_caption(caption.encode("utf-8"))

    def iconify(self):
        pygame.display.iconify()

    def get_draw_constructors(self):
        """
        Figures out the list of draw constructors to try.
        """

        renderer = renpy.game.preferences.renderer
        renderer = os.environ.get("RENPY_RENDERER", renderer)
        renderer = renpy.session.get("renderer", renderer)

        renpy.config.renderer = renderer

        if renpy.android or renpy.ios or renpy.emscripten:
            renderers = [ "gles" ]
        elif renpy.windows:
            renderers = [ "gl", "angle", "gles" ]
        else:
            renderers = [ "gl", "gles" ]

        gl2_renderers = [ ]

        for i in [ "gl", "angle", "gles" ]:

            if i in renderers:
                gl2_renderers.append(i + "2")

        renderers = gl2_renderers + renderers

        # Prevent a performance warning if the renderer
        # is taken from old persistent data.
        if renderer not in gl2_renderers and (renpy.macintosh or renpy.android or renpy.config.gl2):
            renderer = "auto"

        # Software renderer is the last hope for PC .
        if not (renpy.android or renpy.ios or renpy.emscripten):
            renderers = renderers + [ "sw" ]

        if renderer in renderers:
            renderers = [ renderer, "sw" ]

        if renderer == "sw":
            renderers = [ "sw" ]

        if self.safe_mode:
            renderers = [ "sw" ]

        draw_objects = { }

        def make_draw(name, mod, cls, *args):

            if name not in renderers:
                return False

            try:
                __import__(mod)
                module = sys.modules[mod]
                draw_class = getattr(module, cls)
                draw_objects[name] = draw_class(*args)
                return True

            except Exception:
                renpy.display.log.write("Couldn't import {0} renderer:".format(name))
                renpy.display.log.exception()

                return False

        make_draw("gl", "renpy.gl.gldraw", "GLDraw", "gl")
        make_draw("angle", "renpy.gl.gldraw", "GLDraw", "angle")
        make_draw("gles", "renpy.gl.gldraw", "GLDraw", "gles")

        make_draw("gl2", "renpy.gl2.gl2draw", "GL2Draw", "gl2")
        make_draw("angle2", "renpy.gl2.gl2draw", "GL2Draw", "angle2")
        make_draw("gles2", "renpy.gl2.gl2draw", "GL2Draw", "gles2")

        make_draw("sw", "renpy.display.swdraw", "SWDraw")

        rv = [ ]

        def append_draw(name):
            if name in draw_objects:
                rv.append((name, draw_objects[name]))
            else:
                renpy.display.log.write("Unknown renderer: {0}".format(name))

        for i in renderers:
            append_draw(i)

        return rv

    def kill_textures(self):
        """
        Kills all textures that have been loaded.
        """

        if renpy.display.draw is not None:
            renpy.display.draw.kill_textures()

        renpy.display.im.cache.clear()
        renpy.display.render.free_memory()
        renpy.text.text.layout_cache_clear()
        renpy.display.video.texture.clear()

    def kill_surfaces(self):
        """
        Kills all surfaces that have been loaded.
        """

        renpy.display.im.cache.clear()
        renpy.display.module.bo_cache = None

    def before_resize(self):
        """
        This is called when the window has been resized.
        """

        self.kill_textures()

        # Stop the resizing.
        pygame.key.stop_text_input() # @UndefinedVariable
        pygame.key.set_text_input_rect(None) # @UndefinedVariable
        self.text_rect = None
        self.old_text_rect = None
        self.display_reset = False

        self.force_redraw = True

        # Assume we have focus until told otherwise.
        self.mouse_focused = True
        self.keyboard_focused = True

        # Assume we're not minimized.
        self.minimized = False

        # Force an interaction restart.
        self.restart_interaction = True

        # True if we're doing a one-time profile.
        self.profile_once = False

        # Clear the frame times.
        self.frame_times = [ ]

    def set_mode(self):
        """
        This constructs the draw object and sets the initial size of the
        window.
        """

        if renpy.session.get("_keep_renderer", False):
            renpy.display.render.models = renpy.display.draw.info.get("models", False)
            return

        virtual_size = (renpy.config.screen_width, renpy.config.screen_height)

        if renpy.display.draw:
            draws = [ renpy.display.draw ]
        else:
            draws = self.get_draw_constructors()

        for name, draw in draws: #type: ignore
            renpy.display.log.write("")
            renpy.display.log.write("Initializing {0} renderer:".format(name))
            if draw.init(virtual_size):
                renpy.display.draw = draw
                renpy.display.render.models = draw.info.get("models", False)
                break
            else:
                pygame.display.destroy()

        else:
            # Ensure we don't get stuck in fullscreen.
            renpy.game.preferences.fullscreen = False
            raise Exception("Could not set video mode.")

        renpy.session["renderer"] = draw.info["renderer"]
        renpy.game.persistent._gl2 = renpy.config.gl2

        if renpy.android:
            android.init()
            pygame.event.get()

    def draw_screen(self, root_widget, fullscreen_video, draw):

        try:
            renpy.display.render.per_frame = True
            renpy.display.screen.per_frame()
        finally:
            renpy.display.render.per_frame = False

        surftree = renpy.display.render.render_screen(
            root_widget,
            renpy.config.screen_width,
            renpy.config.screen_height,
            )

        if draw:
            renpy.display.draw.draw_screen(surftree)

        if renpy.emscripten:
            emscripten.sleep(0)

        now = time.time()

        self.frame_times.append(now)

        while (now - self.frame_times[0]) > renpy.config.performance_window:
            self.frame_times.pop(0)

        renpy.display.render.mark_sweep()
        renpy.display.focus.take_focuses()

        self.surftree = surftree
        self.fullscreen_video = fullscreen_video

        if self.first_frame:
            self.after_first_frame()
            self.first_frame = False

    def take_screenshot(self, scale, background=False):
        """
        This takes a screenshot of the current screen, and stores it so
        that it can gotten using get_screenshot()

        `background`
           If true, we're in a background thread. So queue the request
           until it can be handled by the main thread.
        """

        self.clear_screenshot = False

        # Do nothing before the first interaction.
        if not self.started:
            return

        if background and not renpy.emscripten:
            self.bgscreenshot_event.clear()
            self.bgscreenshot_needed = True

            if not self.bgscreenshot_event.wait(1.0):
                raise Exception("Screenshot timed out.")

            surf = self.bgscreenshot_surface
            self.bgscreenshot_surface = None

        else:

            surf = renpy.display.draw.screenshot(self.surftree)

        surf = renpy.display.scale.smoothscale(surf, scale)

        renpy.display.render.mutated_surface(surf)

        self.screenshot_surface = surf

        with io.BytesIO() as sio:
            renpy.display.module.save_png(surf, sio, 0)
            self.screenshot = sio.getvalue()

    def check_background_screenshot(self):
        """
        Handles requests for a background screenshot.
        """

        if self.bgscreenshot_needed:
            self.bgscreenshot_needed = False
            self.bgscreenshot_surface = renpy.display.draw.screenshot(self.surftree)
            self.bgscreenshot_event.set()

    def get_screenshot(self):
        """
        Gets the current screenshot, as a string. Returns None if there isn't
        a current screenshot.
        """

        if not self.started:
            return None

        rv = self.screenshot

        if not rv:
            self.take_screenshot(
                (renpy.config.thumbnail_width, renpy.config.thumbnail_height),
                background=(threading.current_thread() is not self.thread),
                )
            rv = self.screenshot
            self.lose_screenshot()

        return rv

    def lose_screenshot(self):
        """
        This deallocates the saved screenshot.
        """

        self.screenshot = None
        self.screenshot_surface = None

    def save_screenshot(self, filename):
        """
        Saves a full-size screenshot in the given filename.
        """

        window = renpy.display.draw.screenshot(self.surftree)

        if renpy.config.screenshot_crop:
            window = window.subsurface(renpy.config.screenshot_crop)

        try:
            renpy.display.scale.image_save_unscaled(window, filename)
            if renpy.emscripten:
                emscripten.run_script(r'''FSDownload('%s');''' % filename)
            return True
        except Exception:
            if renpy.config.debug:
                raise

            return False

    def screenshot_to_bytes(self, size=None):
        """
        This takes a screenshot of the last thing drawn, and returns it.
        """

        self.clear_screenshot = False

        # Do nothing before the first interaction.
        if not self.started:
            return

        surf = renpy.display.draw.screenshot(self.surftree)

        if size is not None:
            surf = renpy.display.scale.smoothscale(surf, size)

        renpy.display.render.mutated_surface(surf)

        self.screenshot_surface = surf

        with io.BytesIO() as sio:
            renpy.display.module.save_png(surf, sio, 0)
            return sio.getvalue()

    def show_window(self):

        if not renpy.store._window:
            return

        if not renpy.game.preferences.show_empty_window:
            return

        if renpy.game.context().scene_lists.shown_window:
            return

        if renpy.config.empty_window:

            old_history = renpy.store._history # @UndefinedVariable
            renpy.store._history = False

            PPP("empty window") # type: ignore

            old_say_attributes = renpy.game.context().say_attributes
            old_temporary_attributes = renpy.game.context().temporary_attributes

            try:
                renpy.game.context().say_attributes = None
                renpy.game.context().temporary_attributes = None

                renpy.config.empty_window()

            finally:
                renpy.store._history = old_history

                renpy.game.context().say_attributes = old_say_attributes
                renpy.game.context().temporary_attributes = old_temporary_attributes

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

    def with_none(self, overlay=True):
        """
        Implements the with None command, which sets the scene we will
        be transitioning from.
        """

        PPP("start of with none") # type: ignore

        # Show the window, if that's necessary.
        self.show_window()

        # Compute the overlay.
        if overlay:
            self.compute_overlay()

        scene_lists = renpy.game.context().scene_lists

        # Compute the scene.
        for layer, d in self.compute_scene(scene_lists).items():
            if layer is None:
                if not self.transition:
                    self.old_scene[layer] = d
            elif layer not in self.transition:
                self.old_scene[layer] = d

        # Get rid of transient things.
        for i in renpy.config.overlay_layers:
            scene_lists.clear(i)

        scene_lists.replace_transient()
        scene_lists.shown_window = False

        if renpy.store._side_image_attributes_reset:
            renpy.store._side_image_attributes = None
            renpy.store._side_image_attributes_reset = False

    def end_transitions(self):
        """
        This runs at the end of each interaction to remove the transitions
        that have run their course.
        """

        layers = list(self.ongoing_transition)

        for l in layers:
            if l is None:
                self.ongoing_transition.pop(None, None)
                self.instantiated_transition.pop(None, None)
                self.transition_time.pop(None, None)
                self.transition_from.pop(None, None)
                continue

            start = self.transition_time.get(l, self.frame_time) or 0
            delay = self.transition_delay.get(l, None) or 0

            if (self.frame_time - start) >= delay:
                self.ongoing_transition.pop(l, None)
                self.instantiated_transition.pop(l, None)
                self.transition_time.pop(l, None)
                self.transition_from.pop(l, None)

    def set_transition(self, transition, layer=None, force=False):
        """
        Sets the transition that will be performed as part of the next
        interaction.
        """

        if self.suppress_transition and not force:
            return

        if transition is None:
            self.transition.pop(layer, None)
        else:
            self.transition[layer] = transition

    def event_peek(self):
        """
        This peeks the next event. It returns None if no event exists.
        """

        if renpy.emscripten:
            emscripten.sleep(0)

        if self.pushed_event:
            return self.pushed_event

        ev = pygame.event.poll()

        if ev.type == pygame.NOEVENT:
            self.check_background_screenshot()
            # Seems to prevent the CPU from speeding up.
            renpy.display.draw.event_peek_sleep()
            return None

        self.pushed_event = ev

        return ev

    def event_poll(self):
        """
        Called to busy-wait for an event while we're waiting to
        redraw a frame.
        """

        if renpy.emscripten:
            emscripten.sleep(0)

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

        self.check_background_screenshot()

        if renpy.emscripten:

            emscripten.sleep(0)

            while True:
                ev = pygame.event.poll()
                if ev.type != pygame.NOEVENT:
                    break

                emscripten.sleep(1)

        else:
            ev = pygame.event.wait()

        self.last_event = ev

        return ev

    def compute_overlay(self):

        if renpy.store.suppress_overlay:
            return

        # Figure out what the overlay layer should look like.
        renpy.ui.layer("overlay")

        for i in renpy.config.overlay_functions:
            i()

        if renpy.game.context().scene_lists.shown_window:
            for i in renpy.config.window_overlay_functions:
                i()

        renpy.ui.close()

    def compute_scene(self, scene_lists):
        """
        This converts scene lists into a dictionary mapping layer
        name to a Fixed containing that layer.
        """

        rv = { }

        for layer in renpy.display.scenelists.layers:
            d = scene_lists.make_layer(layer, self.layer_properties[layer])
            rv[layer] = scene_lists.transform_layer(layer, d)

        root = renpy.display.layout.MultiBox(layout='fixed')
        root.layers = { }

        for layer in renpy.config.layers:
            root.layers[layer] = rv[layer]
            root.add(rv[layer])

        rv[None] = root

        return rv

    def quit_event(self):
        """
        This is called to handle the user invoking a quit.
        """

        if self.screenshot is None:
            renpy.exports.take_screenshot()

        if self.quit_time > (time.time() - .75):
            renpy.exports.quit(save=True)

        if self.in_quit_event:
            renpy.exports.quit(save=True)

        if renpy.config.quit_action is not None:
            self.quit_time = time.time()

            # Make the screen more suitable for interactions.
            renpy.exports.movie_stop(only_fullscreen=True)
            renpy.store.mouse_visible = True

            try:
                self.in_quit_event = True
                renpy.display.behavior.run(renpy.config.quit_action)
            finally:
                self.in_quit_event = False

        else:
            renpy.exports.quit(save=True)

    def set_mouse(self, cursor):
        """
        Sets the current mouse cursor.

        True sets a visible system cursor. False hides the cursor. A ColorCursor
        object sets a cursor image.
        """

        if cursor is self.old_mouse:
            return

        self.old_mouse = cursor

        if cursor is True:
            pygame.mouse.reset()
            pygame.mouse.set_visible(True)
        elif cursor is False:
            pygame.mouse.reset()
            pygame.mouse.set_visible(False)
        else:
            pygame.mouse.set_visible(True)
            cursor.activate()

    def hide_mouse(self):
        """
        Called from the controller to hide the mouse when a controller
        event happens.
        """

        self.mouse_event_time = 0

    def is_mouse_visible(self):
        # Figure out if the mouse visibility algorithm is hiding the mouse.
        if (renpy.config.mouse_hide_time is not None) and (self.mouse_event_time + renpy.config.mouse_hide_time < renpy.display.core.get_time()):
            visible = False
        else:
            visible = renpy.store.mouse_visible and (not renpy.game.less_mouse)

        visible = visible and self.show_mouse and not (renpy.display.video.fullscreen)

        return visible

    def get_mouse_name(self, cache_only=False, interaction=True):

        mouse_kind = renpy.display.focus.get_mouse() # str|None

        if interaction and (mouse_kind is None):
            mouse_kind = self.mouse

        if mouse_kind is None:
            mouse_kind = "default"

        if pygame.mouse.get_pressed()[0]:
            mouse_kind = "pressed_" + mouse_kind # type: ignore

        if cache_only and (mouse_kind not in self.cursor_cache): # type: ignore
            # if the mouse_kind cursor is not in cache, use a replacement
            # if pressed_ is in the cursor name, we'll try to use pressed_default
            # or the non-pressed cursor if we have it in cache
            # otherwise we'll use the default cursor
            if mouse_kind.startswith("pressed_") and ("pressed_default" in self.cursor_cache): # type: ignore
                # if a generic pressed_default cursor is defined, use it
                mouse_kind = "pressed_default"
            elif mouse_kind.startswith("pressed_") and (mouse_kind[8:] in self.cursor_cache): # type: ignore
                # otherwise use the non-pressed cursor if we have it in cache
                mouse_kind = mouse_kind[8:]
            else:
                mouse_kind = 'default'

        if mouse_kind == 'default':
            mouse_kind = getattr(renpy.store, 'default_mouse', 'default')

        return mouse_kind

    def update_mouse(self, mouse_displayable):

        visible = self.is_mouse_visible()

        if mouse_displayable is not None:
            x, y = renpy.exports.get_mouse_pos()

            if (0 <= x < renpy.config.screen_width) and (0 <= y < renpy.config.screen_height):
                visible = False

        # If not visible, hide the mouse.
        if not visible:
            self.set_mouse(False)
            return

        # Deal with a hardware mouse, the easy way.
        if self.cursor_cache is None:
            self.set_mouse(True)
            return

        # Use hardware mouse if the preferences force.
        if renpy.game.preferences.system_cursor:
            if isinstance(self.old_mouse, pygame.mouse.ColorCursor):
                pygame.mouse.reset()
            self.set_mouse(True)
            return

        mouse_kind = self.get_mouse_name(True)

        if mouse_kind in self.cursor_cache:
            anim = self.cursor_cache[mouse_kind]
            cursor = anim[self.ticks % len(anim)]
        else:
            cursor = True

        self.set_mouse(cursor)

    def set_mouse_pos(self, x, y, duration):
        """
        Sets the mouse position. Duration can be a number of seconds or
        None.
        """

        self.mouse_move = MouseMove(x, y, duration)
        self.force_redraw = True

    def drawn_since(self, seconds_ago):
        """
        Returns true if the screen has been drawn in the last `seconds_ago`,
        and false otherwise.
        """

        return (get_time() - self.frame_time) <= seconds_ago

    def mobile_save(self):
        """
        Create a mobile reload file.
        """

        should_skip_save = renpy.store.main_menu or renpy.store._in_replay
        if renpy.config.save_on_mobile_background and not should_skip_save:
            renpy.loadsave.save("_reload-1", include_screenshot=False)

        renpy.persistent.update(True)
        renpy.persistent.save_on_quit_MP()

    def mobile_unlink(self):
        """
        Delete an unused mobile reload file.
        """

        # Since we came back to life, we can get rid of the
        # auto-reload.
        renpy.loadsave.unlink_save("_reload-1")

    def check_android_start(self):
        """
        Delays until the android screen is visible, to ensure the
        GL context is created properly.
        """

        from jnius import autoclass
        SDLActivity = autoclass("org.libsdl.app.SDLActivity")

        if SDLActivity.mHasFocus:
            return

        renpy.display.log.write("App not focused at interface start, shutting down early.")

        self.mobile_save()

        os._exit(1)

    def check_suspend(self, ev):
        """
        Handles the SDL2 suspend process.
        """

        if ev.type != pygame.APP_WILLENTERBACKGROUND:
            return False

        print("Pausing audio.")

        renpy.audio.audio.pause_all()

        print("Disabling periodic events.")

        pygame.time.set_timer(PERIODIC, 0)
        pygame.time.set_timer(REDRAW, 0)
        pygame.time.set_timer(TIMEEVENT, 0)

        print("Saving.")

        try:
            self.mobile_save()
        except Exception as e:
            import traceback
            traceback.print_exc()

        if renpy.config.quit_on_mobile_background:

            if renpy.android:
                try:
                    android.activity.finishAndRemoveTask()
                except Exception:
                    pass

                from jnius import autoclass
                System = autoclass("java.lang.System")
                System.exit(0)

            sys.exit(0)

        print("Freeing memory.")

        renpy.exports.free_memory()

        print("Releasing wakelock.")

        if renpy.android:
            android.wakelock(False)

            # Tell Android to end the onPause method.
            android.activity.finishOnPause()

        print("Entered background. --------------------------------------------")

        while True:
            ev = pygame.event.wait()

            if ev.type == pygame.APP_TERMINATING:

                sys.exit(0)

            if ev.type == pygame.APP_DIDENTERFOREGROUND:
                break

        print("Entering foreground. -------------------------------------------")

        self.mobile_unlink()

        pygame.time.set_timer(PERIODIC, PERIODIC_INTERVAL)

        renpy.audio.audio.unpause_all()

        if renpy.android:
            android.wakelock(True)

        # Reset the display so we get the GL context back.
        self.display_reset = True
        self.restart_interaction = True

        return True

    def enter_context(self):
        """
        Called when we enter a new context.
        """

        # Stop ongoing transitions.
        self.ongoing_transition.clear()
        self.instantiated_transition.clear()
        self.transition_from.clear()
        self.transition_time.clear()

    def post_time_event(self):
        """
        Posts a time_event object to the queue.
        """

        try:
            pygame.event.post(self.time_event)
        except Exception:
            pass

    def after_longpress(self):
        """
        Called after a longpress, to ignore the mouse button release.
        """

        self.ignore_touch = True
        renpy.display.focus.mouse_handler(None, -1, -1, default=False)

    def text_event_in_queue(self):
        """
        Returns true if the next event in the queue is a text editing event.
        """

        ev = self.event_peek()
        if ev is None:
            return False
        else:
            return ev.type in (pygame.TEXTINPUT, pygame.TEXTEDITING)

    def update_text_rect(self):
        """
        Updates the text input state and text rectangle.
        """

        if renpy.store._text_rect is not None: # @UndefinedVariable
            self.text_rect = renpy.store._text_rect # @UndefinedVariable

        if self.text_rect is not None:

            not_shown = pygame.key.has_screen_keyboard_support() and not pygame.key.is_screen_keyboard_shown() # @UndefinedVariable
            if self.touch_keyboard:
                not_shown = renpy.exports.get_screen('_touch_keyboard', layer='screens') is None

            if self.old_text_rect != self.text_rect:
                x, y, w, h = self.text_rect
                x0, y0 = renpy.display.draw.untranslate_point(x, y)
                x1, y1 = renpy.display.draw.untranslate_point(x + w, y + h)
                rect = (x0, y0, x1 - x0, y1 - y0)

                pygame.key.set_text_input_rect(rect) # @UndefinedVariable

            if not self.old_text_rect or not_shown:
                pygame.key.start_text_input() # @UndefinedVariable

                if self.touch_keyboard:
                    renpy.exports.restart_interaction() # required in mobile mode
                    renpy.exports.show_screen('_touch_keyboard',
                        _layer='screens', # not 'transient' so as to be above other screens
                                          # not 'overlay' as it conflicts with console
                        _transient=True,
                    )

        else:
            if self.old_text_rect:
                pygame.key.stop_text_input() # @UndefinedVariable
                pygame.key.set_text_input_rect(None) # @UndefinedVariable

                if self.touch_keyboard:
                    renpy.exports.hide_screen('_touch_keyboard', layer='screens')

        self.old_text_rect = self.text_rect

    def maximum_framerate(self, t):
        """
        Forces Ren'Py to draw the screen at the maximum framerate for `t` seconds.
        """

        if t is None:
            self.maximum_framerate_time = 0
        else:
            self.maximum_framerate_time = max(self.maximum_framerate_time, get_time() + t)

    def interact(self, clear=True, suppress_window=False, trans_pause=False, pause=None, pause_modal=False, **kwargs):
        """
        This handles an interaction, restarting it if necessary. All of the
        keyword arguments are passed off to interact_core.
        """

        renpy.plog(1, "start of new interaction")

        if not self.started:
            self.start()

        if self.clear_screenshot:
            self.lose_screenshot()

        self.clear_screenshot = False

        self.trans_pause = trans_pause

        context = renpy.game.context()

        if context.interacting:
            raise Exception("Cannot start an interaction in the middle of an interaction, without creating a new context.")

        context.interacting = True

        # Show a missing window.
        if not suppress_window:
            self.show_window()

        # These things can be done once per interaction.

        preloads = self.preloads
        self.preloads = [ ]

        try:
            self.start_interact = True

            for i in renpy.config.start_interact_callbacks:
                i()

            self.interaction_counter = 0

            repeat = True

            pause_start = get_time()

            while repeat:
                self.interaction_counter += 1

                if self.interaction_counter == 100 and renpy.config.developer:
                    raise Exception("renpy.restart_interaction() was called 100 times without processing any input.")

                repeat, rv = self.interact_core(preloads=preloads, trans_pause=trans_pause, pause=pause, pause_start=pause_start, pause_modal=pause_modal, **kwargs) # type: ignore

                self.start_interact = False

            return rv # type: ignore

        finally:
            renpy.game.context().deferred_translate_identifier = None

            self.force_prediction = False

            context.interacting = False

            # Clean out transient stuff at the end of an interaction.
            if clear:
                scene_lists = renpy.game.context().scene_lists
                scene_lists.replace_transient()

            self.end_transitions()

            self.restart_interaction = True

            renpy.game.context().mark_seen()
            renpy.game.context().scene_lists.shown_window = False

            if renpy.game.log is not None:
                renpy.game.log.did_interaction = True

            if renpy.store._side_image_attributes_reset:
                renpy.store._side_image_attributes = None
                renpy.store._side_image_attributes_reset = False

    def consider_gc(self):
        """
        Considers if we should peform a garbage collection.
        """

        if not renpy.config.manage_gc:
            return

        count = gc.get_count()

        if count[0] >= renpy.config.idle_gc_count:
            renpy.plog(2, "before gc")

            if count[2] >= renpy.config.gc_thresholds[2]:
                gen = 2
            elif count[1] >= renpy.config.gc_thresholds[1]:
                gen = 1
            else:
                gen = 0

            gc.collect(gen)

            if gc.garbage:
                renpy.memory.print_garbage(gen)
                del gc.garbage[:]

            renpy.plog(2, "after gc")

    def idle_frame(self, can_block, expensive):
        """
        Tasks that are run during "idle" frames.
        """

        if expensive:
            renpy.plog(1, "start idle_frame (expensive)")
        else:
            renpy.plog(1, "start idle_frame (inexpensive)")

        # We want this to include the GC time, so we don't predict on
        # frames where we GC.
        start = get_time()

        step = 1

        while True:

            if self.event_peek() and not self.force_prediction:
                break

            if not (can_block and expensive):
                if get_time() > (start + .0005):
                    break

            # Step 1: Run gc.
            if step == 1:
                self.consider_gc()
                step += 1

            # Step 2: Push textures to GPU.
            elif step == 2:
                renpy.display.draw.ready_one_texture()
                step += 1

            # Step 3: Predict more images.
            elif step == 3:

                if not self.prediction_coroutine:
                    step += 1
                    continue

                try:
                    result = self.prediction_coroutine.send(expensive)
                except ValueError:
                    # Saw this happen once during a quit, giving a
                    # ValueError: generator already executing
                    result = None

                if result is None:
                    self.prediction_coroutine = None
                    step += 1

                elif result is False:
                    if not expensive:
                        step += 1

            # Step 4: Preload images (on emscripten)
            elif step == 4:

                if expensive and renpy.emscripten:
                    renpy.display.im.cache.preload_thread_pass()

                step += 1

            # Step 5: Autosave.
            elif step == 5:

                if not self.did_autosave:
                    renpy.loadsave.autosave()
                    renpy.persistent.check_update()
                    self.did_autosave = True

                step += 1

            else:

                # Check to see if preloading has finished
                if renpy.display.im.cache.done():
                    self.force_prediction = False

                break

        if expensive:
            renpy.plog(1, "end idle_frame (expensive)")
        else:
            renpy.plog(1, "end idle_frame (inexpensive)")

    # This gets assigned below.
    take_layer_displayable = None

    def interact_core(self,
                      show_mouse=True,
                      trans_pause=False,
                      suppress_overlay=False,
                      suppress_underlay=False,
                      mouse='default',
                      preloads=[],
                      roll_forward=None,
                      pause=None,
                      pause_start=0.0,
                      pause_modal=None,
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

        `pause`
            If not None, the amount of time before the interaction ends with
            False being returned.

        `pause_modal`
            If true, the pause will respect modal windows. If false, it will
            not.
        """

        renpy.plog(1, "start interact_core")

        # Process the invoke queue.
        while self.invoke_queue:
            fn, args, kwargs = self.invoke_queue.pop(0)
            rv = fn(*args, **kwargs)
            if rv is not None:
                return False, rv

        # Check to see if the language has changed.
        renpy.translation.check_language()

        suppress_overlay = suppress_overlay or renpy.store.suppress_overlay

        # Store the various parameters.
        self.suppress_overlay = suppress_overlay
        self.suppress_underlay = suppress_underlay
        self.trans_pause = trans_pause

        # Show default screens.
        renpy.display.screen.show_overlay_screens(suppress_overlay)

        # Prepare screens, if need be.
        renpy.display.screen.prepare_screens()

        self.roll_forward = roll_forward
        self.show_mouse = show_mouse

        suppress_transition = renpy.config.skipping or renpy.game.less_updates

        # The global one.
        self.suppress_transition = False

        # Figure out transitions.
        if suppress_transition or renpy.game.after_rollback:
            self.ongoing_transition.clear()
            self.instantiated_transition.clear()
            self.transition_from.clear()
            self.transition_time.clear()

        if not suppress_transition:

            for k, t in self.transition.items():
                if k not in self.old_scene:
                    continue

                self.ongoing_transition[k] = t
                self.transition_from[k] = self.old_scene[k]._in_current_store()
                self.transition_time[k] = None

        self.transition.clear()

        # Safety condition, prevents deadlocks.
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

        self.frame_time = start_time

        for i in renpy.config.interact_callbacks:
            i()

        # Set the window caption.
        self.set_window_caption()

        # Tick time forward.
        renpy.display.im.cache.tick()
        renpy.text.text.text_tick()
        renpy.display.predict.reset()

        # Clear the size groups.
        renpy.display.layout.size_groups.clear()

        # Clear the set of updated screens.
        renpy.display.screen.updated_screens.clear()

        # Clear some events.
        pygame.event.clear((PERIODIC,
                            TIMEEVENT,
                            REDRAW))

        # Accumulate relative mouse movement from otherwise obsolete events.
        global relx, rely
        for ev in pygame.event.get(pygame.MOUSEMOTION):
            xr, yr = ev.rel
            relx += xr
            rely += yr

        # Add a single TIMEEVENT to the queue.
        self.post_time_event()

        # Figure out the scene list we want to show.
        scene_lists = renpy.game.context().scene_lists

        # Remove the now-hidden things.
        scene_lists.remove_hidden()

        # Compute the overlay.
        if not suppress_overlay:
            self.compute_overlay()

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
        renpy.display.tts.set_root(scene[None])

        renpy.plog(1, "computed scene")

        # If necessary, load all images here.
        for w in scene.values():
            try:
                renpy.display.predict.displayable(w)
            except Exception:
                pass

        renpy.plog(1, "final predict")

        if pause is not None:
            pb = renpy.display.behavior.PauseBehavior(pause, modal=pause_modal)
            root_widget.add(pb, pause_start, pause_start)
            focus_roots.append(pb)

        # The root widget of all of the layers.
        layers_root = renpy.display.layout.MultiBox(layout='fixed')
        layers_root.layers = { }

        def instantiate_transition(layer, old_d, new_d):
            """
            Create a transition that will be used to transition `layer` (which
            can be None) to `d`.
            """

            old_trans = self.instantiated_transition.get(layer, None)

            trans = self.ongoing_transition[layer](
                old_widget=old_d,
                new_widget=new_d)

            if not isinstance(trans, Displayable):
                raise Exception("Expected transition to return a displayable, not a {!r}".format(trans))

            if isinstance(trans, renpy.display.transform.Transform) and isinstance(old_trans, renpy.display.transform.Transform):
                trans.take_state(old_trans)
                trans.take_execution_state(old_trans)

            self.instantiated_transition[layer] = trans

            return trans

        def add_layer(where, layer):

            scene_layer = scene[layer]
            focus_roots.append(scene_layer)

            if (self.ongoing_transition.get(layer, None) and
                    not suppress_transition):

                trans = instantiate_transition(layer, self.transition_from[layer], scene_layer)

                transition_time = self.transition_time.get(layer, None)

                where.add(trans, transition_time, transition_time)
                where.layers[layer] = trans

            else:
                where.add(scene_layer)
                where.layers[layer] = scene_layer

        # Add the bottom layers to root_widget.
        for layer in renpy.config.bottom_layers:
            add_layer(root_widget, layer)

        # Add layers (perhaps with transitions) to the layers root.
        for layer in renpy.config.layers:
            add_layer(layers_root, layer)

        def add_layers_to_root(d, st=None, at=None):
            """
            This adds layers_root to root_widget, perhaps transforming it
            with config.layer_transforms[None]
            """

            at_list = renpy.config.layer_transforms.get(None, [ ])

            if not at_list:
                root_widget.add(d, st, at)
                return

            rv = renpy.display.layout.MultiBox(layout='fixed')
            rv.adjust_times = True
            rv.add(d, st, at)

            new_transform = None

            for a in at_list:

                if isinstance(a, renpy.display.motion.Transform):
                    rv = a(child=rv)
                else:
                    rv = a(rv)

                rv._unique()

                if isinstance(rv, renpy.display.transform.Transform):
                    new_transform = rv

            if (new_transform is not None):
                scene_lists.transform_state(self.old_root_transform, new_transform, execution=True)

            self.old_root_transform = new_transform
            root_widget.add(rv, 0, 0)

        # Add layers_root to root_widget, perhaps through a transition.
        if (self.ongoing_transition.get(None, None) and
                not suppress_transition):

            old_root = renpy.display.layout.MultiBox(layout='fixed')
            old_root.layers = { }

            for layer in renpy.config.layers:
                d = self.transition_from[None].layers[layer]
                old_root.layers[layer] = d
                old_root.add(d)

            trans = instantiate_transition(None, old_root, layers_root)

            if not isinstance(trans, Displayable):
                raise Exception("Expected transition to return a displayable, not a {!r}".format(trans))

            transition_time = self.transition_time.get(None, None)
            add_layers_to_root(trans, transition_time, transition_time)

            if (transition_time is None) and isinstance(trans, renpy.display.transform.Transform):
                trans.update_state()

            if trans_pause:

                if renpy.store._dismiss_pause:
                    sb = renpy.display.behavior.SayBehavior(dismiss=[], dismiss_unfocused='dismiss')
                else:
                    sb = renpy.display.behavior.SayBehavior(dismiss=[], dismiss_unfocused='dismiss_hard_pause')

                root_widget.add(sb)
                focus_roots.append(sb)

                pb = renpy.display.behavior.PauseBehavior(trans.delay) # type: ignore
                root_widget.add(pb, transition_time, transition_time)
                focus_roots.append(pb)

        else:
            add_layers_to_root(layers_root)

        # Add top_layers to the root_widget.
        for layer in renpy.config.top_layers:
            add_layer(root_widget, layer)

        for i in renpy.display.emulator.overlay:
            root_widget.add(i)

        if renpy.game.preferences.system_cursor:
            mouse_displayable = None
        else:
            mouse_displayable = renpy.config.mouse_displayable
            if mouse_displayable is not None:
                if not isinstance(mouse_displayable, Displayable):
                    mouse_displayable = mouse_displayable()

                if mouse_displayable is not None:
                    root_widget.add(mouse_displayable, 0, 0)

        self.prediction_coroutine = renpy.display.predict.prediction_coroutine(root_widget)
        self.prediction_coroutine.send(None)

        # Clean out the registered adjustments.
        renpy.display.behavior.adj_registered.clear()

        # Clean up some movie-related things.
        renpy.display.video.early_interact()

        # A dict of any active layer transitions.
        layer_transitions = { }

        # This try block is used to force cleanup even on termination
        # caused by an exception propagating through this function.
        try:

            # Call per-interaction code for all displayables.
            def take_layer_displayable(ld):
                """
                This is called by a layer displayable to add the layer's
                contents to the layer displayable.
                """

                if ld.layer in scene:
                    ld.layers = layer_transitions
                    add_layer(ld, ld.layer)
                    del ld.layers
                else:
                    ld.add(null)

            self.take_layer_displayable = take_layer_displayable

            renpy.display.behavior.input_pre_per_interact()
            root_widget.visit_all(lambda d : d.per_interact())
            renpy.display.behavior.input_post_per_interact()

            self.take_layer_displayable = None


            # Consolidate static and layer transitions for later processing.
            if layer_transitions:
                layer_transitions.update(layers_root.layers)
            else:
                layer_transitions = layers_root.layers

            # Now, update various things regarding scenes and transitions,
            # so we are ready for a new interaction or a restart.
            self.old_scene = scene

            # Okay, from here on we now have a single root widget (root_widget),
            # which we will try to show to the user.

            # Figure out what should be focused.
            renpy.display.behavior.WebInput.pre_find_focusable()
            renpy.display.focus.before_interact(focus_roots)
            renpy.display.behavior.WebInput.post_find_focusable()

            # Something updated the screens. Deal with it now, so the player doesn't
            # see it.
            if self.restart_interaction:
                return True, None

            # Redraw the screen.
            needs_redraw = True

            # First pass through the while loop?
            first_pass = True

            # We don't yet know when the interaction began.
            self.interact_time = None

            # We only want to do autosave once.
            self.did_autosave = False

            old_timeout_time = None
            old_redraw_time = None

            rv = None

            # Start sound.
            renpy.audio.audio.interact()

            # How long until we redraw.
            _redraw_in = 3600

            # Have we drawn a frame yet?
            video_frame_drawn = False

            # We're no longer after rollback.
            renpy.game.after_rollback = False

            # How many frames have we shown so far?
            frame = 0

            can_block = False

            while rv is None:

                renpy.plog(1, "start of interact while loop")

                renpy.execution.not_infinite_loop(10)

                # Check for autoreload.
                renpy.loader.check_autoreload()

                if renpy.emscripten or os.environ.get('RENPY_SIMULATE_DOWNLOAD', False):
                    renpy.webloader.process_downloaded_resources()

                avoid_draw = False

                if renpy.emscripten:
                    avoid_draw = emscripten.run_script_int("webglContextLost")

                    if emscripten.run_script_int("webglContextRestored"):
                        self.display_reset = True
                        emscripten.run_script("webglContextRestored = false;")

                if not avoid_draw:

                    for i in renpy.config.needs_redraw_callbacks:
                        if i():
                            needs_redraw = True

                    # Check for a fullscreen change.

                    if not renpy.display.can_fullscreen:
                        renpy.game.preferences.fullscreen = False

                    if renpy.game.preferences.fullscreen != self.fullscreen:
                        if (not PY2) and renpy.emscripten:
                            if renpy.game.preferences.fullscreen:
                                emscripten.run_script("setFullscreen(true);")
                            else:
                                emscripten.run_script("setFullscreen(false);")

                        else:
                            renpy.display.draw.resize()

                    # Ask if the game has changed size.
                    if renpy.display.draw.update(force=self.display_reset):
                        needs_redraw = True

                    # Redraw the screen.
                    if (self.force_redraw or
                        ((first_pass or not pygame.event.peek(ALL_EVENTS)) and
                        renpy.display.draw.should_redraw(needs_redraw, first_pass, can_block))):

                        self.force_redraw = False

                        renpy.display.render.process_redraws()

                        # If we have a movie, start showing it.
                        fullscreen_video = renpy.display.video.interact()

                        # Clean out the redraws, if we have to.
                        # renpy.display.render.kill_redraws()

                        self.text_rect = None

                        # Draw the screen.
                        self.frame_time = get_time()

                        renpy.audio.audio.advance_time() # Sets the time of all video frames.

                        self.draw_screen(root_widget, fullscreen_video, (not fullscreen_video) or video_frame_drawn)

                        if first_pass:
                            if not self.interact_time:
                                self.interact_time = max(self.frame_time, get_time() - self.frame_duration)

                            scene_lists.set_times(self.interact_time)

                            for k, v in self.transition_time.items():
                                if v is None:
                                    self.transition_time[k] = self.interact_time

                            renpy.display.render.adjust_render_cache_times(self.frame_time, self.interact_time)

                        frame += 1
                        renpy.config.frames += 1

                        # If profiling is enabled, report the profile time.
                        if renpy.config.profile or self.profile_once:

                            renpy.plog(0, "end frame")
                            renpy.performance.analyze()
                            renpy.performance.clear()
                            renpy.plog(0, "start frame")

                            self.profile_once = False

                        if first_pass and self.last_event and self.last_event.type in [ pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION ]:

                            x, y = renpy.display.draw.get_mouse_pos()
                            ev, x, y = renpy.display.emulator.emulator(self.last_event, x, y)

                            if self.ignore_touch:
                                x = -1
                                y = -1

                            if renpy.android and self.last_event.type == pygame.MOUSEBUTTONUP:
                                x = -1
                                y = -1

                            renpy.display.focus.mouse_handler(None, x, y, default=False)

                        needs_redraw = False
                        first_pass = False

                        pygame.time.set_timer(REDRAW, 0)
                        pygame.event.clear([REDRAW])
                        old_redraw_time = None

                        self.update_text_rect()

                        renpy.test.testexecution.execute()

                # Move the mouse, if necessary.
                if self.mouse_move is not None:
                    if not self.mouse_move.perform():
                        self.mouse_move = None

                # Check the autosave callback.
                if renpy.loadsave.did_autosave:
                    renpy.loadsave.did_autosave = False
                    renpy.exports.run(renpy.config.autosave_callback)

                # See if we want to restart the interaction entirely.
                if self.restart_interaction and not self.display_reset:
                    return True, None

                # Determine if we need a redraw. (We want to run these
                # functions, so we put them first to prevent short-circuiting.)

                if renpy.display.video.frequent():
                    needs_redraw = True
                    video_frame_drawn = True

                if renpy.display.render.check_redraws():
                    needs_redraw = True

                # How many seconds until we timeout.
                _timeout_in = 3600

                # Handle the redraw timer.
                redraw_time = renpy.display.render.redraw_time()

                # We only need to set the REDRAW timer if we can block.
                can_block = renpy.display.draw.can_block()

                if self.maximum_framerate_time > get_time():
                    can_block = False

                if (redraw_time is not None) and (not needs_redraw) and can_block:
                    if redraw_time != old_redraw_time:
                        time_left = redraw_time - get_time()
                        time_left = min(time_left, 3600)
                        _redraw_in = time_left

                        if time_left <= 0:
                            try:
                                pygame.event.post(self.redraw_event)
                            except Exception:
                                pass
                            pygame.time.set_timer(REDRAW, 0)
                        else:
                            pygame.time.set_timer(REDRAW, max(int(time_left * 1000), 1))

                        old_redraw_time = redraw_time
                else:
                    _redraw_in = 3600
                    pygame.time.set_timer(REDRAW, 0)

                # Handle the timeout timer.
                if not self.timeout_time:
                    pygame.time.set_timer(TIMEEVENT, 0)
                else:
                    time_left = self.timeout_time - get_time()
                    time_left = min(time_left, 3600)
                    _timeout_in = time_left

                    if time_left <= 0:
                        self.timeout_time = None
                        pygame.time.set_timer(TIMEEVENT, 0)
                        self.post_time_event()
                    elif self.timeout_time != old_timeout_time:
                        # Always set to at least 1ms.
                        pygame.time.set_timer(TIMEEVENT, int(time_left * 1000 + 1))
                        old_timeout_time = self.timeout_time

                if can_block or (frame >= renpy.config.idle_frame) or (self.force_prediction):
                    expensive = not (needs_redraw or (_redraw_in < .2) or (_timeout_in < .2) or renpy.display.video.playing())

                    if self.force_prediction:
                        expensive = True
                        can_block = True

                    self.idle_frame(can_block, expensive)

                if needs_redraw or (not can_block) or self.mouse_move or renpy.display.video.playing():
                    renpy.plog(1, "pre peek")
                    ev = self.event_poll()
                    renpy.plog(1, "post peek {!r}", ev)
                else:
                    renpy.plog(1, "pre wait")
                    ev = self.event_wait()
                    renpy.plog(1, "post wait {!r}", ev)

                self.interaction_counter = 0

                if ev.type == pygame.NOEVENT:

                    if can_block and (not needs_redraw) and (not self.prediction_coroutine) and (not self.mouse_move):
                        pygame.time.wait(1)

                    continue

                # Add the current keyboard modifiers to all events.
                if ev.type in (pygame.KEYDOWN, pygame.KEYUP):
                    self.mod = ev.mod

                ev.mod = self.mod

                # Recognize and ignore AltGr on Windows.
                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_LCTRL:

                        ev2 = self.event_peek()

                        if (ev2 is not None) and (ev2.type == pygame.KEYDOWN):
                            if ev2.key == pygame.K_RALT:
                                continue

                # Check to see if the OS is asking us to suspend (on Android
                # and iOS.)
                if self.check_suspend(ev):
                    continue

                # Try to merge an TIMEEVENT with other timeevents.
                if ev.type == TIMEEVENT:
                    old_timeout_time = None
                    pygame.event.clear([TIMEEVENT])

                    # Set the modal flag to False.
                    ev.modal = False

                # On Android, where we have multiple mouse buttons, we can
                # merge a mouse down and mouse up event with its successor. This
                # prevents us from getting overwhelmed with too many events on
                # a multitouch screen.
                if renpy.android and (ev.type == pygame.MOUSEBUTTONDOWN or ev.type == pygame.MOUSEBUTTONUP):
                    pygame.event.clear(ev.type)

                # Handle redraw timeouts.
                if ev.type == REDRAW:
                    pygame.event.clear([REDRAW])
                    old_redraw_time = None
                    continue

                # Handle periodic events. This includes updating the mouse timers (and through the loop,
                # the mouse itself), and the audio system periodic calls.
                if ev.type == PERIODIC:
                    events = 1 + len(pygame.event.get([PERIODIC]))
                    self.ticks += events

                    for i in renpy.config.periodic_callbacks:
                        i()

                    renpy.audio.audio.periodic()
                    renpy.display.tts.periodic()
                    renpy.display.controller.periodic()

                    self.update_mouse(mouse_displayable)

                    if renpy.emscripten:
                        self.exec_js_cmd()

                    continue

                # Handle quit specially for now.
                if ev.type == pygame.QUIT:
                    self.quit_event()
                    continue

                # Ignore KEY-events while text is being edited (usually with an IME).
                if ev.type == pygame.TEXTEDITING:
                    if ev.text:
                        self.text_editing = ev
                    else:
                        self.text_editing = None
                elif ev.type == pygame.TEXTINPUT:
                    self.text_editing = None

                elif ev.type == pygame.KEYMAPCHANGED:

                    # Clear the mods when the keymap is changed, such as when
                    # an IME is selected. This fixes a problem on Windows 10 where
                    # super+space won't unset super.

                    # This only happens when the GUI key is down, as shift can
                    # also change the keymap.

                    if pygame.key.get_mods() & pygame.KMOD_GUI:
                        pygame.key.set_mods(pygame.key.get_mods() & (pygame.KMOD_NUM | pygame.KMOD_CAPS))

                    continue

                elif self.text_editing and ev.type in [ pygame.KEYDOWN, pygame.KEYUP ]:
                    continue

                if ev.type == pygame.VIDEOEXPOSE:
                    # Needed to force the display to redraw after expose in
                    # the software renderer.

                    if isinstance(renpy.display.draw, renpy.display.swdraw.SWDraw):
                        renpy.display.draw.full_redraw = True
                        renpy.game.interface.force_redraw = True

                    continue

                # Handle videoresize.
                if ev.type == pygame.VIDEORESIZE:

                    if isinstance(renpy.display.draw, renpy.display.swdraw.SWDraw):
                        renpy.display.draw.full_redraw = True

                    renpy.game.interface.force_redraw = True

                    continue

                # Handle window moves.
                if ev.type == pygame.WINDOWMOVED:
                    self.on_move(ev.pos)
                    continue

                # If we're ignoring touch events, and get a mouse up, stop
                # ignoring those events.
                if self.ignore_touch and \
                        ev.type == pygame.MOUSEBUTTONUP and \
                        ev.button == 1:

                    self.ignore_touch = False
                    continue

                # Merge mousemotion events.
                if ev.type == pygame.MOUSEMOTION:
                    xr, yr = ev.rel
                    relx += xr
                    rely += yr

                    for ev in pygame.event.get(pygame.MOUSEMOTION):
                        xr, yr = ev.rel
                        relx += xr
                        rely += yr

                    # Event is now the most recent mouse move due to loop.
                    ev.rel = relx, rely
                    relx = 0
                    rely = 0

                    if renpy.windows:
                        self.mouse_focused = True

                # Handle mouse event time, and ignoring touch.
                if ev.type == pygame.MOUSEMOTION or \
                        ev.type == pygame.MOUSEBUTTONDOWN or \
                        ev.type == pygame.MOUSEBUTTONUP:

                    self.mouse_event_time = renpy.display.core.get_time()

                    if self.ignore_touch:
                        renpy.display.focus.mouse_handler(None, -1, -1, default=False)

                    if mouse_displayable:
                        renpy.display.render.redraw(mouse_displayable, 0)

                # Handle focus notifications.
                if ev.type == pygame.ACTIVEEVENT:

                    if ev.state & 1:
                        if not ev.gain:
                            renpy.display.focus.clear_focus()

                        self.mouse_focused = ev.gain

                        if mouse_displayable:
                            renpy.display.render.redraw(mouse_displayable, 0)

                    if ev.state & 2:
                        self.keyboard_focused = ev.gain

                        if not renpy.game.preferences.audio_when_unfocused and not renpy.emscripten:
                            if not ev.gain:
                                renpy.audio.audio.pause_all()
                            else:
                                renpy.audio.audio.unpause_all()

                    # If the window becomes inactive as a result of this event
                    # pause the audio according to preference
                    if not renpy.game.preferences.audio_when_minimized and not renpy.emscripten:
                        if not pygame.display.get_active() and not self.audio_paused:
                            renpy.audio.audio.pause_all()
                            self.audio_paused = True
                        # If the window had not gone inactive or has regained activity
                        # unpause the audio
                        elif pygame.display.get_active() and self.audio_paused:
                            renpy.audio.audio.unpause_all()
                            self.audio_paused = False

                    pygame.key.set_mods(pygame.key.get_mods() & (pygame.KMOD_NUM | pygame.KMOD_CAPS))

                # This returns the event location. It also updates the
                # mouse state as necessary.
                x, y = renpy.display.draw.mouse_event(ev)
                x, y = renpy.test.testmouse.get_mouse_pos(x, y)

                ev, x, y = renpy.display.emulator.emulator(ev, x, y)
                if ev is None:
                    continue

                if not self.mouse_focused or self.ignore_touch:
                    x = -1
                    y = -1

                # This can set the event to None, to ignore it.
                ev = renpy.display.controller.event(ev)
                if not ev:
                    continue

                # Handle skipping.
                renpy.display.behavior.skipping(ev)

                self.event_time = end_time = get_time()

                try:

                    if self.touch:
                        renpy.display.gesture.recognizer.event(ev, x, y) # @UndefinedVariable

                    renpy.plog(1, "start mouse focus handling")

                    # Handle the event normally.
                    rv = renpy.display.focus.mouse_handler(ev, x, y)

                    renpy.plog(1, "start event handling")

                    if rv is None:
                        rv = root_widget.event(ev, x, y, 0)

                    if rv is None:
                        rv = renpy.display.focus.key_handler(ev)

                    renpy.plog(1, "finish event handling")

                    if rv is not None:
                        break

                    # Handle displayable inspector.
                    if renpy.config.inspector:
                        if renpy.display.behavior.map_event(ev, "inspector"):
                            l = self.surftree.main_displayables_at_point(x, y, renpy.config.transient_layers + renpy.config.context_clear_layers + renpy.config.overlay_layers)
                            renpy.game.invoke_in_new_context(renpy.config.inspector, l)
                        elif renpy.display.behavior.map_event(ev, "full_inspector"):
                            l = self.surftree.main_displayables_at_point(x, y, renpy.config.layers)
                            renpy.game.invoke_in_new_context(renpy.config.inspector, l)

                    # Handle the dismissing of non trans_pause transitions.
                    if self.ongoing_transition.get(None, None) and (not suppress_transition) and (not trans_pause) and (renpy.config.dismiss_blocking_transitions):

                        if renpy.store._dismiss_pause:
                            dismiss = "dismiss"
                        else:
                            dismiss = "dismiss_hard_pause"

                        if renpy.display.behavior.map_event(ev, dismiss):
                            self.transition.pop(None, None)
                            self.ongoing_transition.pop(None, None)
                            self.transition_time.pop(None, None)
                            self.transition_from.pop(None, None)
                            self.restart_interaction = True
                            raise IgnoreEvent()

                except IgnoreEvent:
                    # An ignored event can change the timeout. So we want to
                    # process an TIMEEVENT to ensure that the timeout is
                    # set correctly

                    if ev.type != TIMEEVENT:
                        self.post_time_event()

                    # On mobile, if an event originates from the touch mouse, unfocus.
                    if renpy.mobile and (ev.type == pygame.MOUSEBUTTONUP) and getattr(ev, "which", 0) == 4294967295:
                        if not self.restart_interaction:
                            renpy.display.focus.mouse_handler(None, -1, -1, default=False)

                # Check again after handling the event.
                needs_redraw |= renpy.display.render.check_redraws()

                if self.restart_interaction:
                    return True, None

            # If we were trans-paused and rv is true, suppress
            # transitions up to the next interaction.
            if trans_pause and rv:
                self.suppress_transition = True

            # But wait, there's more! The finally block runs some cleanup
            # after this.
            return False, rv

        except EndInteraction as e:
            return False, e.value

        finally:

            # Determine the transition delay for each layer.
            self.transition_delay = { k : getattr(v, "delay", 0) for k, v in layer_transitions.items() }

            # Clean out the overlay layers.
            for i in renpy.config.overlay_layers:
                scene_lists.clear(i)

            # Stop ongoing preloading.
            renpy.display.im.cache.end_tick()

            # We no longer disable periodic between interactions.
            # pygame.time.set_timer(PERIODIC, 0)

            pygame.time.set_timer(TIMEEVENT, 0)
            pygame.time.set_timer(REDRAW, 0)

            self.consider_gc()

            renpy.game.context().runtime += end_time - start_time

            # Restart the old interaction, which also causes a
            # redraw if needed.
            self.restart_interaction = True

            renpy.plog(1, "end interact_core")

            # print("It took", frames, "frames.")

    def timeout(self, offset):
        if offset < 0:
            return

        if self.timeout_time:
            self.timeout_time = min(self.event_time + offset, self.timeout_time)
        else:
            self.timeout_time = self.event_time + offset

    def finish_pending(self):
        """
        Called before a quit or restart to finish any pending work that might
        block other threads.
        """

        self.check_background_screenshot()

    def exec_js_cmd(self):
        """
        Execute a command from JS if required (emscripten only).
        """

        if not renpy.emscripten:
            return

        # Retrieve the command to be executed from a global JS variable
        # (an empty string is returned if the variable is not defined)

        cmd = emscripten.run_script_string("window._renpy_cmd")

        if len(cmd) == 0:
            return

        # Delete command variable to prevent executing the command again
        emscripten.run_script("delete window._renpy_cmd")

        # Execute the command
        try:
            renpy.python.py_exec(cmd, hide=True)
        except Exception as e:
            renpy.display.log.write(cmd)
            renpy.display.log.write('Error while executing JS command: %s' % (e,))
