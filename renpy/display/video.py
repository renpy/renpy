# Copyright 2004-2016 Tom Rothamel <pytom@bishoujo.us>
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
import collections

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


# A map from a channel name to the movie texture that is being displayed
# on that channel.
texture = { }

# The set of channels that are being displayed in Movie objects.
displayable_channels = collections.defaultdict(list)

# Is there a video being displayed fullscreen?
fullscreen = False

def early_interact():
    """
    Called early in the interact process, to clear out the fullscreen
    flag.
    """

    displayable_channels.clear()


def interact():
    """
    This is called each time the screen is drawn, and should return True
    if the movie should display fulscreen.
    """

    global fullscreen

    for i in list(texture.keys()):
        if not renpy.audio.music.get_playing(i):
            del texture[i]

    if renpy.audio.music.get_playing("movie"):
        fullscreen = ("movie" not in displayable_channels)
    else:
        fullscreen = False

    return fullscreen


def get_movie_texture(channel):

    if not renpy.audio.music.get_playing(channel):
        return None, False

    c = renpy.audio.music.get_channel(channel)
    surf = c.read_video()

    if surf is not None:
        renpy.display.render.mutated_surface(surf)
        tex = renpy.display.draw.load_texture(surf, True)
        texture[channel] = tex
        new = True
    else:
        tex = texture.get(channel, None)
        new = False

    return tex, new

def render_movie(channel, width, height):
    tex, _new = get_movie_texture(channel)

    if tex is None:
        return None

    sw, sh = tex.get_size()

    scale = min(1.0 * width / sw, 1.0 * height / sh)

    dw = scale * sw
    dh = scale * sh

    rv = renpy.display.render.Render(width, height)
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
        This should be specified as either a tuple giving the width and
        height of the movie, or None to automatically adjust to the size
        of the playing movie. (If None, the displayable will be (0, 0)
        when the movie is not playing.)

    `channel`
        The channel the movie should be played on.

    The contents of this displayable when a movie is not playing are undefined.
    (And may change when a rollback occurs.)
    """

    fullscreen = False
    channel = "movie"

    def __init__(self, fps=24, size=None, channel="movie", **properties):
        super(Movie, self).__init__(**properties)
        self.size = size
        self.channel = channel

    def render(self, width, height, st, at):

        playing = renpy.audio.music.get_playing(self.channel)

        if self.size is None:

            tex, _ = get_movie_texture(self.channel)

            if playing and (tex is not None):
                width, height = tex.get_size()

                rv = renpy.display.render.Render(width, height)
                # rv.blit(tex, (0, 0))

            else:

                rv = renpy.display.render.Render(0, 0)

        else:

            w, h = self.size

            if not playing:
                rv = None
            else:
                rv = render_movie(self.channel, w, h)

            if rv is None:
                rv = renpy.display.render.Render(w, h)

        # Usually we get redrawn when the frame is ready - but we want
        # the movie to disappear if it's ended, or if it hasn't started
        # yet.
        renpy.display.render.redraw(self, 0.1)

        return rv


    def per_interact(self):
        displayable_channels[self.channel].append(self)


def playing():
    return renpy.audio.music.get_playing("movie")

def frequent():
    """
    Called to update the video playback. Returns true if a video refresh is
    needed, false otherwise.
    """

    if renpy.mobile:
        return False

    rv = False

    for i, v in displayable_channels.items():
        _, new = get_movie_texture(i)
        if new:
            for j in v:
                renpy.display.render.redraw(j, 0.0)

            rv = True

    if fullscreen:
        _, new = get_movie_texture("movie")

        rv = rv or new

    return rv
