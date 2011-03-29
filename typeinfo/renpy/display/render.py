# Version of renpy.display.render for use in python-only type inferencing.
raise NotImplemented()

import threading
import renpy.display

blit_lock = threading.Condition()

def free_memory():
    """
    Frees memory used by the render system.
    """
    

def check_at_shutdown():
    """
    This is called at shutdown time to check that everything went okay.
    The big thing it checks for is memory leaks.
    """
    
def render(d, widtho, heighto,  st, at):
    """
    Causes the displayable `d` to be rendered in an area of size
    width, height.  st and at are the times of this render, but once
    rendered the Render will remain cached until the displayable needs
    to be redrawn.
    """

    return Render(0, 0)


def invalidate(d):
    """
    Removes d from the render cache. If we're not in a redraw, triggers
    a redraw to start.
    """

        
def process_redraws():
    """
    Called to determine if any redraws are pending. Returns true if we
    need to redraw the screen now, false otherwise.
    """
    
    return True


def redraw_time():
    """
    Returns the time at which the next redraw is scheduled.
    """

    return 0.0

    

def redraw(d, when):
    """
    Called to cause `d` to be redrawn in `when` seconds.
    """
    

class Matrix2D:
    """
    This represents a 2d matrix that can be used to transform
    points and things like that.
    """

        
    def __init__(self, xdx, xdy, ydx, ydy):
        self.xdx = xdx
        self.xdy = xdy
        self.ydx = ydx
        self.ydy = ydy

    def transform(self, x, y):
        return (x * self.xdx + y * self.xdy), (x * self.ydx + y * self.ydy)

    def __mul__(self, other):
        return Matrix2D(
            other.xdx * self.xdx + other.xdy * self.ydx,
            other.xdx * self.xdy + other.xdy * self.ydy,
            other.ydx * self.xdx + other.ydy * self.ydx,
            other.ydx * self.xdy + other.ydy * self.ydy)

    def __repr__(self):
        return "Matrix2D(xdx=%f, xdy=%f, ydx=%f, ydy=%f)" % (self.xdx, self.xdy, self.ydx, self.ydy)
    
IDENTITY = Matrix2D(1, 0, 0, 1)

def take_focuses(focuses):
    """
    Adds a list of rectangular focus regions to the focuses list.
    """

# The result of focus_at_point for a modal render. This overrides any
# specific focus from below us.
Modal = object()
    
def focus_at_point(x, y):
    """
    Returns a focus object corresponding to the uppermost displayable
    at point, or None if nothing focusable is at point.
    """

    return renpy.display.focus.Focus(None, None, None, None, None, None)

    
def mutated_surface(surf):
    """
    Called to indicate that the given surface has changed. 
    """


def render_screen(root, width, height):
    """
    Renders `root` (a displayable) as the root of a screen with the given
    `width` and `height`.
    """

    return Render(0, 0)

def mark_sweep():
    """
    This performs mark-and-sweep garbage collection on the live_renders
    list.
    """

def compute_subline(sx0, sw, cx0, cw):
    """
    Given a source line (start sx0, width sw) and a crop line (cx0, cw),
    return three things:

    * The offset of the portion of the source line that overlaps with
      the crop line, relative to the crop line.
    * The offset of the portion of the source line that overlaps with the
      the crop line, relative to the source line.
    * The length of the overlap in pixels. (can be <= 0) 
    """


# Possible operations that can be done as part of a render.
BLIT = 0
DISSOLVE = 1
IMAGEDISSOLVE = 2
PIXELLATE = 3

class Render:

    def __init__(self, width, height, draw_func=None, layer_name=None, opaque=None):
        """
        Creates a new render corresponding to the given widget with
        the specified width and height.

        If `layer_name` is given, then this render corresponds to a
        layer.
        """
        

    def blit(self, source, pos, focus=True, main=True, index=None):
        """
        Blits `source` (a Render or Surface) to this Render, offset by
        xo and yo.

        If `focus` is true, then focuses are added from the child to the
        parent.

        This will only blit on integer pixel boundaries.
        """

        
    def subpixel_blit(self, source, pos, focus=True, main=True, index=None):
        """
        Blits `source` (a Render or Surface) to this Render, offset by
        xo and yo.

        If `focus` is true, then focuses are added from the child to the
        parent.

        This blits at fractional pixel boundaries.
        """
            
    def get_size(self):
        """
        Returns the size of this Render, a mostly ficticious value
        that's taken from the inputs to the constructor. (As in, we
        don't clip to this size.)
        """

        return 0, 0

    
    def render_to_texture(self, alpha=True):
        """
        Returns a texture constructed from this render. This may return
        a cached textue, if one has already been rendered.

        `alpha` is a hint that controls if the surface should have
        alpha or not.
        """        
    
    pygame_surface = render_to_texture

    
    def subsurface(self, rect, focus=False):
        """
        Returns a subsurface of this render. If `focus` is true, then
        the focuses are copied from this render to the child.
        """

        return Render(0, 0)

    
        
    def depends_on(self, source, focus=False):
        """
        Used to indicate that this render depends on another
        render. Useful, for example, if we use pygame_surface to make
        a surface, and then blit that surface into another render.
        """

        
    def kill_cache(self):
        """
        Removes this render and its transitive parents from the cache.
        """

    def kill(self):
        """
        Retained for compatibility.
        """
                
    def add_focus(self, d, arg=None, x=0, y=0, w=None, h=None, mx=None, my=None, mask=None):
        """
        This is called to indicate a region of the screen that can be
        focused.

        `d` - the displayable that is being focused.
        `arg` - an argument.

        The rest of the parameters are a rectangle giving the portion of
        this region corresponding to the focus. If they are all None, than
        this focus is assumed to be the singular full-screen focus.
        """

    def take_focuses(self, cminx, cminy, cmaxx, cmaxy, reverse, x, y, focuses):
        """
        This adds to focuses Focus objects corresponding to the focuses
        added to this object and its children, transformed into screen
        coordinates.

        `cminx`, `cminy`, `cmaxx`, `cmaxy` - The clipping rectangle.
        `reverse` - The transform from render to screen coordinates.
        `x`, `y` - The offset of the upper-left corner of the render.
        `focuses` - The list of focuses to add to.
        """
        
        
    def focus_at_point(self, x, y):
        """
        This returns the focus of this object at the given point.
        """

        return renpy.display.layout.Null()
    
            
    def main_displayables_at_point(self, x, y, layers, depth=None):
        """
        Returns the displayable at `x`, `y` on one of the layers in
        the set or list `layers`.
        """
        
        return [ ]
        
    def is_opaque(self):
        """
        Returns true if this displayable is opaque, or False otherwise.
        Also sets self.visible_children.
        """

        return True

    
    def is_pixel_opaque(self, x, y):
        """
        Determine if the pixel at x and y is opaque or not.
        """

        return True

    
    def fill(self, color):
        """
        Fills this Render with the given color.
        """
        
    def canvas(self):
        """
        Returns a canvas object that draws to this Render.
        """

        return Canvas(None)

        
class Canvas(object):

    def __init__(self, surf):
        self.surf = surf
        
    def rect(self, color, rect, width=0):
        return

    def polygon(self, color, pointlist, width=0):
        return
    
    def circle(self, color, pos, radius, width=0):
        return

    def ellipse(self, color, rect, width=0):
        return

    def arc(self, color, rect, start_angle, stop_angle, width=1):
        return

    def line(self, color, start_pos, end_pos, width=1):
        return

    def lines(self, color, closed, pointlist, width=1):
        return
    
    def aaline(self, color, startpos, endpos, blend=1):
        return

    def aalines(self, color, closed, pointlist, blend=1):
        return