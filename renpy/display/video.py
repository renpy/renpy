# Copyright 2004-2014 Tom Rothamel <pytom@bishoujo.us>
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

import renpy.display
import renpy.audio

# The movie displayable that's currently being shown on the screen.
current_movie = None

# True if the movie that is currently displaying is in fullscreen mode,
# False if it's a smaller size.
fullscreen = False

# The size of a Movie object that hasn't had an explicit size set.
default_size = (400, 300)

# The file we allocated the surface for.
surface_file = None

# The surface to display the movie on, if not fullscreen.
surface = None

def movie_stop(clear=True, only_fullscreen=False):
    """
    Stops the currently playing movie.
    """

    if (not fullscreen) and only_fullscreen:
        return

    renpy.audio.music.stop(channel='movie')


def movie_start(filename, size=None, loops=0):
    """
    This starts a movie playing.
    """

    if renpy.game.less_updates:
        return

    global default_size

    if size is not None:
        default_size = size

    filename = [ filename ]

    if loops == -1:
        loop = True
    else:
        loop = False
        filename = filename * (loops + 1)

    renpy.audio.music.play(filename, channel='movie', loop=loop)

movie_start_fullscreen = movie_start
movie_start_displayable = movie_start

def early_interact():
    """
    Called early in the interact process, to clear out the fullscreen
    flag.
    """

    global fullscreen
    global current_movie

    fullscreen = True
    current_movie = None


def interact():
    """
    This is called each time the screen is redrawn. It helps us decide if
    the movie should be displayed fullscreen or not.
    """

    global surface
    global surface_file

    if not renpy.audio.music.get_playing("movie"):
        surface = None
        surface_file = None
        return False

    if fullscreen:
        return True
    else:
        return False

def get_movie_texture():
    """
    Gets a movie texture we can draw to the screen.
    """

    global surface
    global surface_file

    playing = renpy.audio.music.get_playing("movie")

    pss = renpy.audio.audio.pss

    if pss:
        size = pss.movie_size()
    else:
        size = (64, 64)

    if (surface is None) or (surface.get_size() != size) or (surface_file != playing):
        surface = renpy.display.pgrender.surface(size, False)
        surface_file = playing
        surface.fill((0, 0, 0, 255))

    tex = None

    if playing is not None:
        renpy.display.render.mutated_surface(surface)
        tex = renpy.display.draw.load_texture(surface, True)

    return tex


def render_movie(width, height):
    tex = get_movie_texture()

    if tex is None:
        return None

    sw, sh = tex.get_size()

    scale = min(1.0 * width / sw, 1.0 * height / sh)

    dw = scale * sw
    dh = scale * sh

    rv = renpy.display.render.Render(width, height, opaque=True)
    rv.forward = renpy.display.render.Matrix2D(1.0 / scale, 0.0, 0.0, 1.0 / scale)
    rv.reverse = renpy.display.render.Matrix2D(scale, 0.0, 0.0, scale)
    rv.blit(tex, (int((width - dw) / 2), int((height - dh) / 2)))

    return rv

class Movie(renpy.display.core.Displayable):
    """
    :doc: movie

    This is a displayable that shows the current movie.

    `fps`
        The framerate that the movie should be shown at. (This is currently
        ignored, but the parameter is kept for backwards compatibility.
        The framerate is auto-detected.)

    `size`
        This should always be specified. A tuple giving the width and height
        of the movie.

    The contents of this displayable when a movie is not playing are undefined.
    (And may change when a rollback occurs.) 
    """

    fullscreen = False

    def __init__(self, fps=24, size=None, **properties):
        super(Movie, self).__init__(**properties)
        self.size = size

    def render(self, width, height, st, at):

        size = self.size

        if size is None:
            size = default_size

        width, height = size

        rv = render_movie(width, height)

        if rv is None:
            rv = renpy.display.render.Render(0, 0)

        # Usually we get redrawn when the frame is ready - but we want
        # the movie to disappear if it's ended, or if it hasn't started
        # yet.
        renpy.display.render.redraw(self, 0.1)

        return rv


    def per_interact(self):
        global fullscreen
        fullscreen = False

        global current_movie
        current_movie = self


def playing():
    return renpy.audio.music.get_playing("movie")

def frequent():
    """
    Called to update the video playback. Returns true if a video refresh is
    needed, false otherwise.
    """

    if not playing():
        return 0

    pss = renpy.audio.audio.pss

    if pss.needs_alloc():

        if renpy.display.video.fullscreen and renpy.display.draw.fullscreen_surface:
            surf = renpy.display.draw.fullscreen_surface
        else:
            get_movie_texture()
            surf = renpy.display.scale.real(surface)

        pss.alloc_event(surf)

    rv = pss.refresh_event()

    if rv and current_movie is not None:
        renpy.display.render.redraw(current_movie, 0)

    return rv
