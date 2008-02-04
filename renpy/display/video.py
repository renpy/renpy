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

import renpy
from renpy.display.render import render
import pygame
import sys # for maxint

class MovieInfo(object):

    def __init__(self, filename, loops, fullscreen, size=None):
        self.filename = filename
        self.loops = loops + 1
        self.fullscreen = fullscreen
        self.size = size

# The movie that is currently playing, if any.
movie = None

# If the movie is running in a widget, this is the surface corresponding
# to that widget.
surface = None

# The current movie info.
current_info = None

# The number of loops the current movie has made.
loops = 0

def movie_stop(clear=True):
    """
    This stops the currently playing movie.
    """

    global movie
    global loops

    if movie:
        movie.stop()
        movie = None
        surface = None
        loops = 0
        
        renpy.audio.audio.init()

    if clear:
        renpy.game.context().scene_lists.movie = None


def movie_start_fullscreen(filename, loops=0):
    """
    This starts a MPEG-1 movie playing in fullscreen mode. While the movie is
    playing (that is, until the next call to movie_stop), interactions will
    not display anything on the screen.

    @param filename: The filename of the MPEG-1 move that we're playing.

    @param loops: The number of additional times the movie should be looped. -1 to loop it forever.
    """

    movie_stop()
    renpy.game.context().scene_lists.movie = MovieInfo(filename, loops, True)

def movie_start_displayable(filename, size, loops=0):
    """
    This starts a MPEG-1 movie playing in displayable mode. One or more Movie()
    widgets must be displayed if the movie is to be shown to the user.

    @param filename: The filename of the MPEG-1 move that we're playing.

    @param size: A tuple containing the size of the movie on the screen. For example, (640, 480).

    @param loops: The number of additional times the movie should be looped. -1 to loop it forever.
    """

    movie_stop()
    renpy.game.context().scene_lists.movie = MovieInfo(filename, loops, False, size)
    
def movie_length(filename):
    m = pygame.movie.Movie(renpy.loader.load(filename))
    return m.get_length()
    
def interact():
    """
    This is called at the start of an interaction. It starts the required
    movie playing, if it's necessary. It returns True if the movie is fullscreen
    and therefore nothing else should be drawn on the screen, or False
    otherwise.
    """

    try:

        global movie
        global surface
        global current_info
        global loops
    
        info = renpy.game.context().scene_lists.movie

        # Has the info changed? If so, stop the movie.
        if info is not current_info:
            movie_stop(False)
            current_info = info

        # No movie to play.
        if not info:
            return False

        # Movie not playing, start it up.
        if not movie:            

            # Needed so we get movie sound.
            renpy.audio.audio.quit()

            m = pygame.movie.Movie(renpy.loader.load(info.filename))

            if info.fullscreen:
                s = None

                m.set_display(pygame.display.get_surface(),
                              (renpy.game.interface.display.screen_xoffset, 0,
                               renpy.config.screen_width,
                               renpy.config.screen_height))

            else:
                s = pygame.Surface(info.size, 0, renpy.game.interface.display.window)
                m.set_display(s, (0, 0) + info.size)

            movie = m
            surface = s

            renpy.display.render.redraw(None, 1.0/48)
            
        if not movie.get_busy():
            if not info.loops or loops < info.loops:
                movie.rewind()
                movie.play()
                loops += 1
                renpy.display.render.redraw(None, 1.0/48)
            else:
                movie_stop()
        else:
            renpy.display.render.redraw(None, 1.0/48)
                

        # Movie is playing (by now).
        return info.fullscreen

    except:
        movie_stop()
        
        if renpy.config.debug_sound:
            raise
        else:
            renpy.audio.audio.init()
            return False


class Movie(renpy.display.layout.Null):
    """
    This is a displayable that displays the current movie. In general,
    a movie should be playing whenever this is on the screen.
    That movie should have been started using movie_start_displayable
    before this is shown on the screen, and hidden before this is
    removed.
    """

    def __init__(self, fps=24, style='default', **properties):
        """
        @param fps: The framerate that the movie should be shown at.
        """

        self.frame_time = 1.0 / fps
        super(Movie, self).__init__(style=style, **properties)

    def render(self, width, height, st, at):
        renpy.display.render.redraw(self, self.frame_time - st % self.frame_time)

        if surface:
            renpy.display.render.mutated_surface(surface)
            
            w, h = surface.get_size()
            rv = renpy.display.render.Render(w, h)
            rv.blit(surface, (0, 0))
            return rv
        else:
            return super(Movie, self).render(width, height, st, at)
        
