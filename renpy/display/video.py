import renpy
import pygame

# The filename of the movie that is being set up to be played.
filename = None

# The position of the movie that is being set up to be played.
position = None

# The number of additional loops the movie will make.
loops = None

# The currently-prepared movie.
movie = None


def prepare():
    global filename
    global position
    global loops
    global movie

    if movie:
        movie.stop()
        movie = None

    if not filename:
        renpy.display.audio.enable_mixer()
        return

    renpy.display.audio.disable_mixer()
    
    movie = pygame.movie.Movie(filename)    
    movie.set_display(pygame.display.get_surface(), position)

    filename = None

def start():

    if movie and not movie.get_busy():
        movie.play(loops)

def movie_start(filename, rect=None, loops=0):
    """
    This sets up an MPEG1 movie to be played during the next
    interaction. Starting at the next call to ui.interact, the
    supplied movie will begin playing. The movie will play until
    the next interaction begins, at which time it will stop.

    @param filename: A file containing a MPEG-1 movie. This has to be
    a real file.

    @param rect: A rectangle (tuple containing four elements)
    containing the position on screen at which the movie will be
    displayed. The movie will be stretched to fit in this
    rectangle. If not supplied, defaults to having the movie fill the
    screen.

    @param loops: The number of additional loops the movie should play for,
    or -1 to have it play forever. (Well, till the end of the interaction.)    
    """

    if rect is None:
        rect = (0, 0, renpy.config.screen_width, renpy.config.screen_height)

    renpy.display.video.filename = filename
    renpy.display.video.position = rect
    renpy.display.video.loops = loops

def abort():
    global movie

    if movie:
        movie.stop()
        movie = None

        renpy.display.audio.enable_mixer()
