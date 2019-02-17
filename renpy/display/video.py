# Copyright 2004-2019 Tom Rothamel <pytom@bishoujo.us>
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

from __future__ import print_function

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

# A map from a channel to the topmost Movie being displayed on
# that channel. (Or None if no such movie exists.)
channel_movie = { }

# Is there a video being displayed fullscreen?
fullscreen = False

# Movie channels that had a hide operation since the last interaction took
# place.
reset_channels = set()


def early_interact():
    """
    Called early in the interact process, to clear out the fullscreen
    flag.
    """

    displayable_channels.clear()
    channel_movie.clear()


def interact():
    """
    This is called each time the screen is drawn, and should return True
    if the movie should display fullscreen.
    """

    global fullscreen

    for i in list(texture.keys()):
        if not renpy.audio.music.get_playing(i):
            del texture[i]

    if renpy.audio.music.get_playing("movie"):

        for i in displayable_channels.keys():
            if i[0] == "movie":
                fullscreen = False
                break
        else:
            fullscreen = True

    else:
        fullscreen = False

    return fullscreen


def get_movie_texture(channel, mask_channel=None, side_mask=False):

    if not renpy.audio.music.get_playing(channel):
        return None, False

    c = renpy.audio.music.get_channel(channel)
    surf = c.read_video()

    if side_mask:

        if surf is not None:

            w, h = surf.get_size()
            w //= 2

            mask_surf = surf.subsurface((w, 0, w, h))
            surf = surf.subsurface((0, 0, w, h))

        else:
            mask_surf = None

    elif mask_channel:
        mc = renpy.audio.music.get_channel(mask_channel)
        mask_surf = mc.read_video()
    else:
        mask_surf = None

    if mask_surf is not None:

        # Something went wrong with the mask video.
        if surf:
            renpy.display.module.alpha_munge(mask_surf, surf, renpy.display.im.identity)
        else:
            surf = None

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


def default_play_callback(old, new):  # @UnusedVariable

    renpy.audio.music.play(new._play, channel=new.channel, loop=new.loop, synchro_start=True)

    if new.mask:
        renpy.audio.music.play(new.mask, channel=new.mask_channel, loop=new.loop, synchro_start=True)


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
        The audio channel associated with this movie. When a movie file
        is played on that channel, it will be displayed in this Movie
        displayable. If this is not given, and the `play` is provided,
        a channel name is automatically selected.

    `play`
        If given, this should be the path to a movie file. The movie
        file will be automatically played on `channel` when the Movie is
        shown, and automatically stopped when the movie is hidden.

    `side_mask`
        If true, this tells Ren'Py to use the side-by-side mask mode for
        the Movie. In this case, the movie is divided in half. The left
        half is used for color information, while the right half is used
        for alpha information. The width of the displayable is half the
        width of the movie file.

        Where possible, `side_mask` should be used over `mask` as it has
        no chance of frames going out of sync.

    `mask`
        If given, this should be the path to a movie file that is used as
        the alpha channel of this displayable. The movie file will be
        automatically played on `movie_channel` when the Movie is shown,
        and automatically stopped when the movie is hidden.

    `mask_channel`
        The channel the alpha mask video is played on. If not given,
        defaults to `channel`\ _mask. (For example, if `channel` is "sprite",
        `mask_channel` defaults to "sprite_mask".)

    `start_image`
        An image that is displayed when playback has started, but the
        first frame has not yet been decoded.

    `image`
        An image that is displayed when `play` has been given, but the
        file it refers to does not exist. (For example, this can be used
        to create a slimmed-down mobile version that does not use movie
        sprites.) Users can also choose to fall back to this image as a
        preference if video is too taxing for their system. The image will
        also be used if the video plays, and then the movie ends.

    ``play_callback``
        If not None, a function that's used to start the movies playing.
        (This may do things like queue a transition between sprites, if
        desired.) It's called with the following arguments:

        `old`
            The old Movie object, or None if the movie is not playing.
        `new`
            The new Movie object.

        A movie object has the `play` parameter available as ``_play``,
        while the ``channel``, ``loop``, ``mask``, and ``mask_channel`` fields
        correspond to the given parameters.

        Generally, this will want to use :func:`renpy.music.play` to start
        the movie playing on the given channel, with synchro_start=True.
        A minimal implementation is::

            def play_callback(old, new):

                renpy.music.play(new._play, channel=new.channel, loop=new.loop, synchro_start=True)

                if new.mask:
                    renpy.music.play(new.mask, channel=new.mask_channel, loop=new.loop, synchro_start=True)

        `loop`
            If False, the movie will not loop. If `image` is defined, the image
            will be displayed when the movie ends. Otherwise, the movie will
            become transparent.



    This displayable will be transparent when the movie is not playing.
    """

    fullscreen = False
    channel = "movie"
    _play = None

    mask = None
    mask_channel = None
    side_mask = False

    image = None
    start_image = None

    play_callback = None

    loop = True

    def ensure_channel(self, name):

        if name is None:
            return

        if renpy.audio.music.channel_defined(name):
            return

        if self.mask:
            framedrop = True
        else:
            framedrop = False

        renpy.audio.music.register_channel(name, renpy.config.movie_mixer, loop=True, stop_on_mute=False, movie=True, framedrop=framedrop)

    def __init__(self, fps=24, size=None, channel="movie", play=None, mask=None, mask_channel=None, image=None, play_callback=None, side_mask=False, loop=True, start_image=None, **properties):
        super(Movie, self).__init__(**properties)

        global auto_channel_serial

        if channel == "movie" and play and renpy.config.auto_movie_channel:
            channel = "movie_{}_{}".format(play, mask)

        self.size = size
        self.channel = channel
        self._play = play
        self.loop = loop

        if side_mask:
            mask = None

        self.mask = mask

        if mask is None:
            self.mask_channel = None
        elif mask_channel is None:
            self.mask_channel = channel + "_mask"
        else:
            self.mask_channel = mask_channel

        self.side_mask = side_mask

        self.ensure_channel(self.channel)
        self.ensure_channel(self.mask_channel)

        self.image = renpy.easy.displayable_or_none(image)
        self.start_image = renpy.easy.displayable_or_none(start_image)

        self.play_callback = play_callback

        if (self.channel == "movie") and (renpy.config.hw_video) and renpy.mobile:
            raise Exception("Movie(channel='movie') doesn't work on mobile when config.hw_video is true. (Use a different channel argument.)")

    def render(self, width, height, st, at):

        if self._play and not (renpy.game.preferences.video_image_fallback is True):
            channel_movie[self.channel] = self

            if st == 0:
                reset_channels.add(self.channel)

        playing = renpy.audio.music.get_playing(self.channel)

        not_playing = not playing

        if self.channel in reset_channels:
            not_playing = False

        if (self.image is not None) and not_playing:
            surf = renpy.display.render.render(self.image, width, height, st, at)
            w, h = surf.get_size()
            rv = renpy.display.render.Render(w, h)
            rv.blit(surf, (0, 0))

            return rv

        if self.size is None:

            tex, _ = get_movie_texture(self.channel, self.mask_channel, self.side_mask)

            if (not not_playing) and (tex is not None):
                width, height = tex.get_size()

                rv = renpy.display.render.Render(width, height)
                rv.blit(tex, (0, 0))

            elif (not not_playing) and (self.start_image is not None):
                surf = renpy.display.render.render(self.start_image, width, height, st, at)
                w, h = surf.get_size()
                rv = renpy.display.render.Render(w, h)
                rv.blit(surf, (0, 0))

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

    def play(self, old):
        if old is None:
            old_play = None
        else:
            old_play = old._play

        if (self._play != old_play) or renpy.config.replay_movie_sprites:
            if self._play:

                if self.play_callback is not None:
                    self.play_callback(old, self)
                else:
                    default_play_callback(old, self)

            else:
                renpy.audio.music.stop(channel=self.channel)

                if self.mask:
                    renpy.audio.music.stop(channel=self.mask_channel)

    def stop(self):
        if self._play:
            renpy.audio.music.stop(channel=self.channel)

            if self.mask:
                renpy.audio.music.stop(channel=self.mask_channel)

    def per_interact(self):
        displayable_channels[(self.channel, self.mask_channel)].append(self)
        renpy.display.render.redraw(self, 0)

    def visit(self):
        return [ self.image, self.start_image ]


def playing():
    if renpy.audio.music.get_playing("movie"):
        return True

    for i in displayable_channels:
        channel, _mask_channel = i

        if renpy.audio.music.get_playing(channel):
            return True

    return


def update_playing():
    """
    Calls play/stop on Movie displayables.
    """

    old_channel_movie = renpy.game.context().movie

    for c, m in channel_movie.items():

        old = old_channel_movie.get(c, None)

        if (c in reset_channels) and renpy.config.replay_movie_sprites:
            m.play(old)
        elif old is not m:
            m.play(old)

    for c, m in old_channel_movie.items():
        if c not in channel_movie:
            m.stop()

    renpy.game.context().movie = dict(channel_movie)
    reset_channels.clear()


def frequent():
    """
    Called to update the video playback. Returns true if a video refresh is
    needed, false otherwise.
    """

    update_playing()

    renpy.audio.audio.advance_time()

    if displayable_channels:

        update = True

        for i in displayable_channels:
            channel, mask_channel = i

            c = renpy.audio.audio.get_channel(channel)
            if not c.video_ready():
                update = False
                break

            if mask_channel:
                c = renpy.audio.audio.get_channel(mask_channel)
                if not c.video_ready():
                    update = False
                    break

        if update:
            for v in displayable_channels.values():
                for j in v:
                    renpy.display.render.redraw(j, 0.0)

        return False

    elif fullscreen and not ((renpy.android or renpy.ios) and renpy.config.hw_video):

        c = renpy.audio.audio.get_channel("movie")

        if c.video_ready():
            return True
        else:
            return False

    return False
