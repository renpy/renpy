# Copyright 2014 Patrick Dawson <pat@dw.is>
# Copyright 2014 Tom Rothamel <tom@rothamel.us>
#
# This software is provided 'as-is', without any express or implied
# warranty.  In no event will the authors be held liable for any damages
# arising from the use of this software.
#
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely, subject to the following restrictions:
#
# 1. The origin of this software must not be misrepresented; you must not
#    claim that you wrote the original software. If you use this software
#    in a product, an acknowledgment in the product documentation would be
#    appreciated but is not required.
# 2. Altered source versions must be plainly marked as such, and must not be
#    misrepresented as being the original software.
# 3. This notice may not be removed or altered from any source distribution.

from sdl2 cimport *
from renpy.pygame.surface cimport *
from renpy.pygame.rect cimport to_sdl_rect

from libc.stdlib cimport calloc, free
from renpy.pygame import register_init, register_quit
from renpy.pygame.locals import SRCALPHA, GL_SWAP_CONTROL
from renpy.pygame.error import error
import renpy.pygame

import warnings
import os

# True if we are on ios.
ios = ("PYGAME_IOS" in os.environ)

# This inits SDL proper, and should be called by the other init methods.

# A map from a renpy.pygame hint to what it was set to.
_pygame_hints = { }

def hint(hint, value, priority=1):

    if str(hint).startswith("renpy.pygame"):
        _pygame_hints[str(hint)] = str(value)
        return

    if not isinstance(hint, bytes):
        hint = hint.encode("utf-8")

    if not isinstance(value, bytes):
        value = value.encode("utf-8")

    SDL_SetHintWithPriority(hint, value, priority)

def _get_hint(hint, default):
    hint = str(hint)

    if hint in _pygame_hints:
        return _pygame_hints[hint]

    if hint in os.environ:
        return os.environ[hint]

    return default


main_done = False

def sdl_main_init():
    global main_done

    if main_done:
        return

    SDL_SetMainReady()

    if SDL_Init(0):
        raise error()

    main_done = True

# True if init has been called without quit being called.
init_done = False

@register_init
def init():

    if init_done:
        return

    sdl_main_init()

    if SDL_InitSubSystem(SDL_INIT_VIDEO):
        raise error()

    renpy.pygame.event.init()

    global init_done
    init_done = True



@register_quit
def quit(): # @ReservedAssignment

    global init_done
    global main_window

    if main_window:
        main_window.destroy()
        main_window = None


    SDL_QuitSubSystem(SDL_INIT_VIDEO)

    init_done = False

def get_init():
    return init_done


# The window that is used by the various module globals.
main_window = None

try:
    import androidembed
except ImportError:
    androidembed = None


cdef class Window:
    def __init__(self, title, resolution=(0, 0), flags=0, depth=0, pos=(SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED), Surface shape=None):
        cdef SDL_WindowShapeMode shape_mode

        if not isinstance(title, bytes):
            title = title.encode("utf-8")

        self.create_flags = flags

        # If we do not get the AVOID_GL hint, we always create a GL-compatible
        # window. This lets us change the OPENGL flag later on.
        if int(_get_hint("renpy.pygame_AVOID_GL", "0")) or os.environ.get("SDL_VIDEODRIVER") == "dummy":
            gl_flag = 0
        else:
            gl_flag = SDL_WINDOW_OPENGL

        self.window = NULL

        if androidembed is not None:
            self.window = SDL_GL_GetCurrentWindow()

            if self.window:

                # Android bug - a RGB_565 format is likely to mean the window
                # wasn't created properly, so re-make it.
                if SDL_GetWindowPixelFormat(self.window) == SDL_PIXELFORMAT_RGB565:
                    SDL_DestroyWindow(self.window)
                    self.window = NULL
                else:
                    SDL_SetWindowTitle(self.window, title)

        if not self.window:

            flags |= SDL_WINDOW_HIDDEN

            if shape is not None:

                shape_mode.mode = ShapeModeDefault

                self.window = SDL_CreateShapedWindow(
                    title,
                    pos[0], pos[1],
                    resolution[0], resolution[1], flags | gl_flag)

                if not self.window:
                    raise error()

                SDL_SetWindowShape(self.window, shape.surface, &shape_mode)

            else:

                self.window = SDL_CreateWindow(
                    title,
                    pos[0], pos[1],
                    resolution[0], resolution[1], flags | gl_flag)

                if not self.window:
                    raise error()

            if pos != (SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED):
                SDL_SetWindowPosition(self.window, pos[0], pos[1])

            SDL_ShowWindow(self.window)

        if not self.window:
            raise error()

        # From here on, the window exists. So we have to call self.destroy if
        # an exception occurs.

        try:

            if flags & SDL_WINDOW_OPENGL:

                self.gl_context = SDL_GL_CreateContext(self.window)

                if self.gl_context == NULL:
                    raise error()

                SDL_GL_MakeCurrent(self.window, self.gl_context)

                if not ios:
                    # Try setting the swap interval - first positive, then negated
                    # to deal with the case where the negative interval isn't
                    # supported. Then give up and carry on.
                    if SDL_GL_SetSwapInterval(default_swap_control):
                        if default_swap_control < 0:
                            SDL_GL_SetSwapInterval(-default_swap_control)

            self.create_surface()

        except:
            self.destroy()
            raise

    def create_surface(self):
        """
        Creates the surface associated with this window.
        """

        cdef int w, h
        SDL_GetWindowSize(self.window, &w, &h)

        if self.gl_context:

            # For now, make this the size of the window so get_size() works.
            # TODO: Make this a bit less wasteful of memory, even if it means
            # we lie about the actual size of the pixel array.
            self.surface = Surface((w, h), SRCALPHA, 32)

        else:

            self.window_surface = SDL_GetWindowSurface(self.window)

            # If the surface is 32-bit, we can use it directly. Otherwise,
            # we need to create a 32-bit proxy surface.
            if self.window_surface.format.BitsPerPixel == 32:

                self.surface = Surface(())
                self.surface.surface = self.window_surface
                self.surface.owns_surface = False
                self.surface.window_surface = True

            else:
                self.surface = Surface((w, h), 0, 32)

        self.surface.get_window_flags = self.get_window_flags


    def destroy(self):
        """
        This should be called before the window is deleted.
        """

        if self.gl_context != NULL:
            SDL_GL_DeleteContext(self.gl_context)

        if self.surface:

            # Break the cycle that prevents refcounting from collecting this
            # object.
            self.surface.get_window_flags = None

            # Necessary to collect the GL surface, doesn't hurt the window surface.
            self.surface = None

        SDL_DestroyWindow(self.window)

    def resize(self, size, opengl=False, fullscreen=None, maximized=None):
        """
        Resizes the window to `size`, which must be a width, height tuple. If opengl
        is true, adds an OpenGL context, if it's missing. Otherwise, removes the
        opengl context if present.
        """

        flags = SDL_GetWindowFlags(self.window)

        if fullscreen is None:
            fullscreen = flags & SDL_WINDOW_FULLSCREEN_DESKTOP

        if maximized is None:
            maximized = flags & SDL_WINDOW_MAXIMIZED

        if fullscreen:
            maximized = False

        # Prevents a loop between the surface and this object.
        self.surface.get_window_flags = None

        if self.gl_context and not opengl:
            SDL_GL_DeleteContext(self.gl_context)
            self.gl_context = NULL

        cdef int cur_width = 0
        cdef int cur_height = 0

        if (not fullscreen) and (not maximized) and (flags & SDL_WINDOW_MAXIMIZED):
            SDL_RestoreWindow(self.window)

        if fullscreen:

            if SDL_SetWindowFullscreen(self.window, SDL_WINDOW_FULLSCREEN_DESKTOP):
                fullscreen = False

        if not fullscreen:
            SDL_SetWindowFullscreen(self.window, 0)

        if (not fullscreen) and (not maximized):

            width, height = size

            SDL_GetWindowSize(self.window, &cur_width, &cur_height)

            if (cur_width != width) or (cur_height != height):
                SDL_SetWindowSize(self.window, width, height)

        if maximized:
            SDL_MaximizeWindow(self.window)

        # Create a missing GL context.
        if opengl and not self.gl_context:
            self.gl_context = SDL_GL_CreateContext(self.window)

            if self.gl_context == NULL:
                raise error()

        self.create_surface()

    def recreate_gl_context(self, always=False):
        """
        Check to see if the GL context was lost, and re-create it if it was.
        """

        if not always:
            if <unsigned long> SDL_GL_GetCurrentContext():
                return False

        self.gl_context = SDL_GL_CreateContext(self.window)

        if self.gl_context == NULL:
            raise error()

        SDL_GL_MakeCurrent(self.window, self.gl_context)

        return True

    def get_window_flags(self):
        rv = SDL_GetWindowFlags(self.window)

        if self.gl_context:
            rv |= SDL_WINDOW_OPENGL
        else:
            rv &= ~SDL_WINDOW_OPENGL

        return rv

    def proxy_window_surface(self):
        SDL_UpperBlit(self.surface.surface, NULL, self.window_surface, NULL)

    def flip(self):
        cdef const char *err

        if self.gl_context != NULL:
            with nogil:
                SDL_ClearError();

                SDL_GL_SwapWindow(self.window)

                err = SDL_GetError()

            if err[0]:
                raise error(err)

        else:

            if self.surface.surface != self.window_surface:
                self.proxy_window_surface()

            with nogil:
                SDL_UpdateWindowSurface(self.window)

    def get_surface(self):
        return self.surface

    def update(self, rectangles=None):

        cdef SDL_Rect *rects
        cdef int count = 0

        if rectangles is None:
            self.flip()
            return

        if self.surface.surface != self.window_surface:
            self.proxy_window_surface()

        if not isinstance(rectangles, list):
            rectangles = [ rectangles ]

        rects = <SDL_Rect *> calloc(len(rectangles), sizeof(SDL_Rect))
        if rects == NULL:
            raise MemoryError("Couldn't allocate rectangles.")

        try:

            for i in rectangles:
                if i is None:
                    continue

                to_sdl_rect(i, &rects[count])
                count += 1

            SDL_UpdateWindowSurfaceRects(self.window, rects, count)

        finally:
            free(rects)

    def get_wm_info(self):
        return { }

    def get_active(self):
        if SDL_GetWindowFlags(self.window) & (SDL_WINDOW_HIDDEN | SDL_WINDOW_MINIMIZED):
            return False
        else:
            return True

    def iconify(self):
        SDL_MinimizeWindow(self.window)
        return True

    def toggle_fullscreen(self):
        if SDL_GetWindowFlags(self.window) & (SDL_WINDOW_FULLSCREEN_DESKTOP):
            if SDL_SetWindowFullscreen(self.window, 0):
                raise error()
        else:
            if SDL_SetWindowFullscreen(self.window, SDL_WINDOW_FULLSCREEN_DESKTOP):
                raise error()

        return True

    def set_gamma(self, red, green=None, blue=None):
        if green is None:
            green = red
        if blue is None:
            blue = red

        cdef Uint16 red_gamma[256]
        cdef Uint16 green_gamma[256]
        cdef Uint16 blue_gamma[256]

        SDL_CalculateGammaRamp(red, red_gamma)
        SDL_CalculateGammaRamp(green, green_gamma)
        SDL_CalculateGammaRamp(blue, blue_gamma)

        if SDL_SetWindowGammaRamp(self.window, red_gamma, green_gamma, blue_gamma):
            return False

        return True

    def set_gamma_ramp(self, red, green, blue):

        cdef Uint16 red_gamma[256]
        cdef Uint16 green_gamma[256]
        cdef Uint16 blue_gamma[256]

        for i in range(256):
            red_gamma[i] = red[i]
            green_gamma[i] = green[i]
            blue_gamma[i] = blue[i]

        if SDL_SetWindowGammaRamp(self.window, red_gamma, green_gamma, blue_gamma):
            return False

        return True

    def set_icon(self, Surface surface):
        SDL_SetWindowIcon(self.window, surface.surface)

    def set_caption(self, title):

        if not isinstance(title, bytes):
            title = title.encode("utf-8")

        SDL_SetWindowTitle(self.window, title)

    def get_drawable_size(self):
        cdef int w, h

        SDL_GL_GetDrawableSize(self.window, &w, &h)
        return w, h


    def get_size(self):
        cdef int w, h

        SDL_GetWindowSize(self.window, &w, &h)
        return w, h

    def restore(self):
        SDL_RestoreWindow(self.window)

    def maximize(self):
        SDL_MaximizeWindow(self.window)

    def minimize(self):
        SDL_MinimizeWindow(self.window)

    def get_sdl_window_pointer(self):
        """
        Returns the pointer to the SDL_Window corresponding to this window.
        """

        import ctypes
        return ctypes.c_void_p(<unsigned long> self.window)

    def get_position(self):
        cdef int x, y

        SDL_GetWindowPosition(self.window, &x, &y)
        return x, y

    def set_position(self, pos):
        SDL_SetWindowPosition(self.window, pos[0], pos[1])



# The icon that's used for new windows.
default_icon = None

# The title that's used for new windows.
default_title = "pygame window"

# The default gl_swap_control
default_swap_control = 1

def set_mode(resolution=(0, 0), flags=0, depth=0, pos=(SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED)):
    global main_window

    RESIZE_FLAGS = SDL_WINDOW_OPENGL | SDL_WINDOW_FULLSCREEN_DESKTOP

    if main_window:

        if (flags & ~RESIZE_FLAGS) == (main_window.create_flags & ~RESIZE_FLAGS):
            main_window.resize(resolution, flags & SDL_WINDOW_OPENGL, flags & SDL_WINDOW_FULLSCREEN_DESKTOP)
            return main_window.surface

        else:
            main_window.destroy()

    main_window = Window(default_title, resolution, flags, depth, pos=pos)

    if default_icon is not None:
        main_window.set_icon(default_icon)

    return main_window.surface

def destroy():
    global main_window

    if main_window is not None:
        main_window.destroy()
        main_window = None

def get_surface():
    if main_window is None:
        return None

    return main_window.get_surface()

def get_window():
    """
    Returns the Window created by set_mode, or None if no such window
    exists.
    """

    return main_window

def flip():
    if main_window:
        main_window.flip()

def update(rectangles=None):
    if main_window:
        main_window.update(rectangles)

def get_driver():
    cdef const char *driver = SDL_GetCurrentVideoDriver()

    if driver == NULL:
        raise error()

    return driver

class Info(object):

    def __init__(self):
        cdef SDL_DisplayMode dm
        cdef SDL_PixelFormat *format

        if SDL_GetCurrentDisplayMode(0, &dm):
            raise error()

        format = SDL_AllocFormat(dm.format)
        if format == NULL:
            raise error()

        self.bitsize = format.BitsPerPixel
        self.bytesize = format.BytesPerPixel

        self.masks = (
            format.Rmask,
            format.Gmask,
            format.Bmask,
            format.Amask,
            )

        self.shifts = (
            format.Rshift,
            format.Gshift,
            format.Bshift,
            format.Ashift,
            )

        self.losses = (
            format.Rloss,
            format.Gloss,
            format.Bloss,
            format.Aloss,
            )

        SDL_FreeFormat(format)

        if main_window:
            self.current_w, self.current_h = main_window.surface.get_size()
        else:

            self.current_w = dm.w
            self.current_h = dm.h

        self.refresh_rate = dm.refresh_rate

        # The rest of these are just guesses.
        self.hw = False
        self.wm = True
        self.video_mem = 256 * 1024 * 1024

        self.blit_hw = False
        self.blit_hw_CC = False
        self.blit_hw_A = False

        self.blit_sw = False
        self.blit_sw_CC = False
        self.blit_sw_A = False

    def __repr__(self):
        return "<Info({!r})>".format(self.__dict__)


def get_wm_info():
    if main_window:
        return main_window.get_wm_info()

    return {}


def get_num_video_displays():
    """
    Returns the number of video displays connected to the system.
    """

    rv = SDL_GetNumVideoDisplays()

    if rv < 0:
        raise error()

    return rv


def list_modes(depth=0, flags=0, display=0):
    """
    Returns a list of possible display modes for the display `display`.

    `depth` and `flags` are ignored.
    """

    cdef int num_modes, i
    cdef SDL_DisplayMode mode

    rv = [ ]

    num_modes = SDL_GetNumDisplayModes(display)
    if num_modes < 0:
        raise error()

    for 0 <= i < num_modes:
        if SDL_GetDisplayMode(display, i, &mode) == 0:
            t = (mode.w, mode.h)
            if t not in rv:
                rv.append(t)

    return rv


def mode_ok(size, flags=0, depth=0):
    """
    Returns true if size is in the result of list_modes().
    """

    return tuple(size) in list_modes()

def gl_reset_attributes():
    SDL_GL_ResetAttributes()

def gl_set_attribute(flag, value):

    if flag == GL_SWAP_CONTROL:
        if ios:
            return

        global default_swap_control

        # Try setting the swap interval - first positive, then negated
        # to deal with the case where the negative interval isn't
        # supported. Then give up and carry on.
        if SDL_GL_SetSwapInterval(value):
            SDL_GL_SetSwapInterval(-value)

        default_swap_control = value
        return

    if SDL_GL_SetAttribute(flag, value):
        raise error()

def gl_get_attribute(flag):
    cdef int rv

    if flag == GL_SWAP_CONTROL:
        return SDL_GL_GetSwapInterval()

    if SDL_GL_GetAttribute(flag, &rv):
        raise error()

    return rv

def gl_load_library(path):
    if path is None:
        if SDL_GL_LoadLibrary(NULL):
            raise error()
    else:
        if SDL_GL_LoadLibrary(path):
            raise error()

def gl_unload_library():
    SDL_GL_UnloadLibrary()

def get_active():
    if main_window:
        return main_window.get_active()
    return False

def iconify():
    if main_window:
        return main_window.iconify()

    return False

def toggle_fullscreen():
    if main_window:
        return main_window.toggle_fullscreen()

    return True

def set_gamma(red, green=None, blue=None):
    if main_window:
        return main_window.set_gamma(red, green, blue)
    return False

def set_gamma_ramp(red, green, blue):
    if main_window:
        return main_window.set_gamma_ramp(red, green, blue)
    return False

def set_icon(surface):
    global default_icon

    default_icon = surface.copy()

    if main_window is not None:
        main_window.set_icon(default_icon)

def set_caption(title, icontitle = None):
    global default_title

    default_title = title

    if main_window:
        main_window.set_caption(default_title)

def get_caption():
    return default_title

def get_drawable_size():
    if main_window:
        return main_window.get_drawable_size()
    return None

def get_size():
    if main_window:
        return main_window.get_size()
    return None

def get_position():
    if main_window:
        return main_window.get_position()
    return None

def set_position(pos):
    if main_window:
        return main_window.set_position(pos)
    return False


def get_num_video_displays():
    rv = SDL_GetNumVideoDisplays()
    if rv < 0:
        raise error()

    return rv

def get_display_bounds(index):
    cdef SDL_Rect rect
    rv = SDL_GetDisplayBounds(index, &rect)

    return (rect.x, rect.y, rect.w, rect.h)

def set_screensaver(state):
    """
    Sets the screenslaver to `state`.
    """

    if state:
        SDL_EnableScreenSaver()
    else:
        SDL_DisableScreenSaver()

def get_platform():
    return SDL_GetPlatform().decode("utf-8")

cdef api SDL_Window *PyWindow_AsWindow(window):
    """
    Returns a pointer to the SDL_Window corresponding to `window`. If `window`
    is None, a pointer to the main window is returned. NULL is returned if
    there is no main window.
    """

    if window is None:
        window = main_window

    if window is None:
        return NULL

    return (<Window> window).window
