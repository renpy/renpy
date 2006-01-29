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

            m = pygame.movie.Movie(renpy.loader.transfn(info.filename))

            if info.fullscreen:
                s = None

                m.set_display(pygame.display.get_surface(),
                              (0, 0,
                               renpy.config.screen_width,
                               renpy.config.screen_height))
            else:
                s = pygame.Surface(info.size, 0, renpy.game.interface.display.window)
                m.set_display(s, (0, 0) + info.size)

            movie = m
            surface = s

        if not movie.get_busy():
            if not info.loops or loops < info.loops:
                movie.rewind()
                movie.play()
                loops += 1
            else:
                movie_stop()
    

        # Movie is playing (by now).
        return info.fullscreen

    except:
        movie_stop()
        
        if renpy.config.debug_sound:
            raise
        else:
            renpy.audio.audio.enable_mixer()
            return False


class Movie(renpy.display.layout.Null):
    """
    This is a displayable that displays the current movie. In general,
    a movie should be playing whenever this is on the screen.
    That movie should have been started using movie_start_displayable
    before this is shown on the screen, and hidden before this is
    removed.
    """


    def __init__(self, style='image_placement', **properties):
        super(Movie, self).__init__(style=style, **properties)

    def render(self, width, height, st, at):
        renpy.display.render.redraw(self, 0)

        if surface:
            renpy.display.render.mutated_surface(surface)
            
            w, h = surface.get_size()
            rv = renpy.display.render.Render(w, h)
            rv.blit(surface, (0, 0))
            return rv
        else:
            return super(Movie, self).render(width, height, st, at)
        
