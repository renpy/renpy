# Copyright 2004-2010 PyTom <pytom@bishoujo.us>
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

# This file contains classes that handle layout of displayables on
# the screen.

import renpy
from renpy.display.render import render, Render


def scale(num, base):
    """
    If num is a float, multiplies it by base and returns that. Otherwise,
    returns num unchanged.
    """

    if isinstance(num, float):
        return num * base
    else:
        return num

class Null(renpy.display.core.Displayable):
    """
    This is a displayable that doesn't actually display anything. It's
    useful, I guess, when you need to wrap something with a behavior,
    but don't want to actually have anything there.
    """

    def __init__(self, width=0, height=0, style='default', **properties):
        super(Null, self).__init__(style=style, **properties)
        self.width = width
        self.height = height

    def render(self, width, height, st, at):
        rv = renpy.display.render.Render(self.width, self.height)

        if self.focusable:
            rv.add_focus(self, None, None, None, None, None)

        return rv


class Container(renpy.display.core.Displayable):
    """
    This is the base class for containers that can have one or more
    children.

    @ivar children: A list giving the children that have been added to
    this container, in the order that they were added in.

    @ivar child: The last child added to this container. This is also
    used to access the sole child in containers that can only hold
    one child.

    @ivar offsets: A list giving offsets for each of our children.
    It's expected that render will set this up each time it is called.

    @ivar sizes: A list giving sizes for each of our children. It's
    also expected that render will set this each time it is called.

    """

    # We indirect all list creation through this, so that we can
    # use RevertableLists if we want.
    _list_type = list

    def __init__(self, *args, **properties):

        self.children = self._list_type()
        self.child = None
        self.offsets = self._list_type()

        for i in args:
            self.add(i)

        super(Container, self).__init__(**properties)

    def set_style_prefix(self, prefix, root):
        super(Container, self).set_style_prefix(prefix, root)

        for i in self.children:
            i.set_style_prefix(prefix, False)
            
    def add(self, d):
        """
        Adds a child to this container.
        """

        child = renpy.easy.displayable(d)
        
        self.children.append(child)
        self.child = child
        self.offsets = self._list_type()

    def remove(self, d):
        """
        Removes the first instance of child from this container. May
        not work with all containers.
        """

        for i, c in enumerate(self.children):
            if c is d:
                break
        else:
            return

        self.children.pop(i) # W0631
        self.offsets = self._list_type()

        if self.children:
            self.child = self.children[-1]
        else:
            self.child = None
        
        
    def update(self):
        """
        This should be called if a child is added to this
        displayable outside of the render function.
        """

        renpy.display.render.invalidate(self)

        
    def render(self, width, height, st, at):

        rv = Render(width, height)
        self.offsets = self._list_type()
        
        for c in self.children:
            cr = render(c, width, height, st, at)
            offset = c.place(rv, 0, 0, width, height, cr)
            self.offsets.append(offset)

        return rv

    
    def event(self, ev, x, y, st):

        children = self.children
        offsets = self.offsets
        
        for i in xrange(len(offsets) - 1, -1, -1):

            d = children[i]
            xo, yo = offsets[i]

            rv = d.event(ev, x - xo, y - yo, st)    
            if rv is not None:
                return rv
                
        return None

    
    def visit(self):
        return self.children
    
    # These interact with the ui functions to allow use as a context
    # manager.

    def __enter__(self):

        if renpy.ui.current is self and not renpy.ui.current_once:
            return self

        raise Exception("%r cannot be used as a context manager.", type(self).__name__)


    def __exit__(self, exc_type, exc_val, exc_tb):

        if exc_type:
            return False

        if renpy.ui.current is not self:
            raise Exception("Widget %r left open at end of block.")

        renpy.ui.close()
        return False

        
    

def LiveComposite(size, *args, **properties):
    """
    This is similar to im.Composite, but can be used with displayables
    instead of images. This allows it to be used to composite, for
    example, an animation on top of the image.

    This is less efficient then im.Composite, as it needs to draw all
    of the displayables on the screen. On the other hand, it allows
    displayables to change while they are on the screen, which is
    necessary for animation.
    
    This takes a variable number of arguments. The first argument is
    size, which must be a tuple giving the width and height of the
    composited widgets, for layout purposes.

    It then takes an even number of further arguments. (For an odd
    number of total arguments.) The second and other even numbered
    arguments contain position tuples, while the third and further
    odd-numbered arguments give displayables. A position argument
    gives the position of the displayable immediately following it,
    with the position expressed as a tuple giving an offset from the
    upper-left corner of the LiveComposite.  The displayables are
    drawn in bottom-to-top order, with the last being closest to the
    user.
    """

    properties.setdefault('style', 'image_placement')

    width, height = size

    rv = Fixed(xmaximum=width, ymaximum=height, xminimum=width, yminimum=height, **properties)

    if len(args) % 2 != 0:
        raise Exception("LiveComposite requires an odd number of arguments.")

    for pos, widget in zip(args[0::2], args[1::2]):
        xpos, ypos = pos
        rv.add(Position(renpy.easy.displayable(widget),
                        xpos=xpos, xanchor=0, ypos=ypos, yanchor=0))

    return rv

class Position(Container):
    """
    Controls the placement of a displayable on the screen, using
    supplied position properties. This is the non-curried form of
    Position, which should be used when the user has directly created
    the displayable that will be shown on the screen.
    """

    def __init__(self, child, style='image_placement', **properties):
        """
        @param child: The child that is being laid out.

        @param style: The base style of this position.

        @param properties: Position properties that control where the
        child of this widget is placed.
        """

        super(Position, self).__init__(style=style, **properties)
        self.add(child)

    def render(self, width, height, st, at):

        surf = render(self.child, width, height, st, at)
        cw, ch = surf.get_size()

        self.offsets = [ (0, 0) ]

        rv = renpy.display.render.Render(surf.width, surf.height)
        rv.blit(surf, (0, 0))
        
        return rv

    def get_placement(self):
    
        xpos, ypos, xanchor, yanchor, xoffset, yoffset, subpixel = self.child.get_placement()

        v = self.style.xpos
        if v is not None:
            xpos = v

        v = self.style.ypos
        if v is not None:
            ypos = v

        v = self.style.xanchor
        if v is not None:
            xanchor = v

        v = self.style.yanchor
        if v is not None:
            yanchor = v

        v = self.style.xoffset
        if v is not None:
            xoffset = v

        v = self.style.yoffset
        if v is not None:
            yoffset = v

        v = self.style.subpixel
        if v is not None:
            subpixel = v

        return xpos, ypos, xanchor, yanchor, xoffset, yoffset, subpixel

    
class Grid(Container):
    """
    A grid is a widget that evenly allocates space to its children.
    The child widgets should not be greedy, but should instead be
    widgets that only use part of the space available to them.
    """

    def __init__(self, cols, rows, padding=None,
                 transpose=False,
                 style='default', **properties):
        """
        @param cols: The number of columns in this widget.

        @params rows: The number of rows in this widget.

        @params transpose: True if the grid should be transposed.
        """

        if padding is not None:
            properties.setdefault('spacing', padding)
        
        super(Grid, self).__init__(style=style, **properties)

        self.cols = cols
        self.rows = rows

        self.transpose = transpose

    def render(self, width, height, st, at):

        # For convenience and speed.
        padding = self.style.spacing
        cols = self.cols
        rows = self.rows

        if len(self.children) != cols * rows:
            raise Exception("Grid not completely full.")

        # If necessary, transpose the grid (kinda hacky, but it works here.)
        if self.transpose:
            self.transpose = False

            old_children = self.children[:]
            
            for y in range(0, rows):
                for x in range(0, cols):
                    self.children[x + y * cols] = old_children[ y + x * rows ]

            
        # Now, start the actual rendering.

        renwidth = width
        renheight = height

        if self.style.xfill:
            renwidth = (width - (cols - 1) * padding) / cols
        if self.style.yfill:
            renheight = (height - (rows - 1) * padding) / rows
        
        renders = [ render(i, renwidth, renheight, st, at) for i in self.children ]
        sizes = [ i.get_size() for i in renders ]

        cwidth = 0
        cheight = 0

        for w, h in sizes:
            cwidth = max(cwidth, w)
            cheight = max(cheight, h)

        if self.style.xfill:
            cwidth = renwidth

        if self.style.yfill:
            cheight = renheight

        width = cwidth * cols + padding * (cols - 1)
        height = cheight * rows + padding * (rows - 1)

        rv = renpy.display.render.Render(width, height)

        self.offsets = [ ]
            
        for y in range(0, rows):
            for x in range(0, cols):

                child = self.children[ x + y * cols ]
                surf = renders[x + y * cols]

                xpos = x * (cwidth + padding)
                ypos = y * (cheight + padding)

                offset = child.place(rv, xpos, ypos, cwidth, cheight, surf)
                self.offsets.append(offset)

        return rv

class MultiBox(Container):

    layer_name = None
    first = True
    
    def __init__(self, spacing=None, layout=None, style='default', **properties):

        if spacing is not None:
            properties['spacing'] = spacing

        super(MultiBox, self).__init__(style=style, **properties)

        self.default_layout = layout

        # The start and animation times for children of this
        # box.
        self.start_times = [ ]
        self.anim_times = [ ]

        # A map from layer name to the widget corresponding to
        # that layer.
        self.layers = None

        # The scene list for this widget.
        self.scene_list = None

    def add(self, widget, start_time=None, anim_time=None): # W0221
        super(MultiBox, self).add(widget)
        self.start_times.append(start_time)
        self.anim_times.append(anim_time)
        
    def append_scene_list(self, l):
        for tag, zo, start, anim, d in l:
            self.add(d, start, anim)

        if self.scene_list is None:
            self.scene_list = [ ]
            
        self.scene_list.extend(l)
        
    def render(self, width, height, st, at):

        # Do we need to adjust the child times due to our being a layer?
        if self.layer_name or (self.layers is not None):
            adjust_times = True
        else:
            adjust_times = False

        xminimum = self.style.xminimum
        if xminimum is not None:
            width = max(width, scale(xminimum, width))

        yminimum = self.style.yminimum
        if yminimum is not None:
            height = max(height, scale(yminimum, height))
            
        if self.first:

            self.first = False

            if adjust_times:
            
                it = renpy.game.interface.interact_time
                
                self.start_times = [ i or it for i in self.start_times ]
                self.anim_times = [ i or it for i in self.anim_times ]
                            
            layout = self.style.box_layout

            if layout is None:
                layout = self.default_layout

            self.layout = layout # W0201

        else:
            layout = self.layout


        # Handle time adjustment, store the results in csts and cats.
        if adjust_times:            
            t = renpy.game.interface.frame_time

            csts = [ t - start for start in self.start_times ]
            cats = [ t - anim for anim in self.anim_times ]

        else:
            csts = [ st ] * len(self.children)
            cats = [ at ] * len(self.children)
            
        if layout == "fixed":

            self.offsets = [ ]
            
            rv = renpy.display.render.Render(width, height, layer_name=self.layer_name)

            for child, cst, cat in zip(self.children, csts, cats):
                
                surf = render(child, width, height, cst, cat)

                if surf:
                    offset = child.place(rv, 0, 0, width, height, surf)
                    self.offsets.append(offset)
                else:
                    self.offsets.append((0, 0))
                    
            return rv
                    
        if layout == "horizontal":

            spacing = self.style.spacing
            first_spacing = self.style.first_spacing

            if first_spacing is None:
                first_spacing = spacing

            spacings = [ first_spacing ] + [ spacing ] * (len(self.children) - 1)

            self.offsets = [ ]

            surfaces = [ ]
            xoffsets = [ ]

            remwidth = width
            xo = 0

            myheight = 0

            padding = 0

            for i, padding, cst, cat in zip(self.children, spacings, csts, cats):
                
                xoffsets.append(xo)
                surf = render(i, remwidth, height, cst, cat)

                sw, sh = surf.get_size()

                remwidth -= sw
                remwidth -= padding

                xo += sw + padding

                myheight = max(sh, myheight)

                surfaces.append(surf)


            if self.style.yfill:
                myheight = height

            if not self.style.xfill:
                width = xo - padding
                bonus = 0
            else:
                bonus = (remwidth + padding) / len(xoffsets)
                xoffsets = [ xo + i * bonus for i, xo in enumerate(xoffsets) ]
                
                
            rv = renpy.display.render.Render(width, myheight)

            for surf, child, xo in zip(surfaces, self.children, xoffsets):
                sw, sh = surf.get_size()

                offset = child.place(rv, xo, 0, sw + bonus, myheight, surf)
                self.offsets.append(offset)

            return rv
        
        elif layout == "vertical":

            spacing = self.style.spacing
            first_spacing = self.style.first_spacing

            if first_spacing is None:
                first_spacing = spacing

            spacings = [ first_spacing ] + [ spacing ] * (len(self.children) - 1)
    
            self.offsets = [ ]

            surfaces = [ ]
            yoffsets = [ ]

            remheight = height
            yo = 0

            mywidth = 0

            padding = 0

            for i, padding, cst, cat in zip(self.children, spacings, csts, cats):

                yoffsets.append(yo)

                surf = render(i, width, remheight, cst, cat)

                sw, sh = surf.get_size()

                remheight -= sh
                remheight -= padding

                yo += sh + padding

                mywidth = max(sw, mywidth)

                surfaces.append(surf)

            if self.style.xfill:
                mywidth = width

            if not self.style.yfill:
                height = yo - padding
                bonus = 0
            else:
                bonus = (remheight + padding) / len(yoffsets)
                yoffsets = [ yo + i * bonus for i, yo in enumerate(yoffsets) ]
                
            rv = renpy.display.render.Render(mywidth, height)

            for surf, child, yo in zip(surfaces, self.children, yoffsets):

                sw, sh = surf.get_size()

                offset = child.place(rv, 0, yo, mywidth, sh + bonus, surf)

                self.offsets.append(offset)

            return rv

        
    def event(self, ev, x, y, st):
        children_offsets = zip(self.children, self.offsets, self.start_times)
        children_offsets.reverse()

        for i, (xo, yo), t in children_offsets: 

            if t is None:
                cst = st
            else:
                cst = renpy.game.interface.event_time - t

            rv = i.event(ev, x - xo, y - yo, cst)    
            if rv is not None:
                return rv
                
        return None

def Fixed(**properties):
    return MultiBox(layout='fixed', **properties)

class SizeGroup(renpy.object.Object):

    def __init__(self):

        super(SizeGroup, self).__init__()
        
        self.members = [ ]
        self._width = None
        self.computing_width = False
        
    def width(self, width, height, st, at):
        if self._width is not None:
            return self._width

        if self.computing_width:
            return 0

        self.computing_width = True
        
        maxwidth = 0

        for i in self.members:
            rend = renpy.display.render.render(i, width, height, st, at)
            maxwidth = max(rend.width, maxwidth)
            rend.kill()
            
        self._width = maxwidth
        self.computing_width = False

        return maxwidth
        

size_groups = dict()
    
class Window(Container):
    """
    A window is a container that holds a single Displayable in it. A window
    is responsable for displaying the displayable on top of a background.

    Margin is space that is left empty by the window, and does not
    have the background displayed in it. Padding is space that is
    filled with the background, but does not contain the widget in it.

    If fill in a dimension is True, then the window expands to the
    maximum size possible in that dimension, and the child is place at
    the left or top of the space. Otherwise, the window will shrink to
    fit the child, but on no account will the size of child area +
    2*padding shrink below the minimum.    
    """
    
    def __init__(self, child, style='window', **properties):

        super(Window, self).__init__(style=style, **properties)
        if child is not None:
            self.add(child)

    def visit(self):
        return [ self.style.background ] + self.children

    def get_child(self):
        return self.style.child or self.child

    def per_interact(self):
        size_group = self.style.size_group

        if size_group:
            group = size_groups.get(size_group, None)
            if group is None:
                group = size_groups[size_group] = SizeGroup()

            group.members.append(self)

                
    def render(self, width, height, st, at):

        # save some typing.
        style = self.style

        xminimum = scale(style.xminimum, width)
        yminimum = scale(style.yminimum, height)

        size_group = self.style.size_group
        if size_group:
            xminimum = max(xminimum, size_groups[size_group].width(width, height, st, at))
        
        left_margin = scale(style.left_margin, width)
        left_padding = scale(style.left_padding, width)

        right_margin = scale(style.right_margin, width)
        right_padding = scale(style.right_padding, width)

        top_margin = scale(style.top_margin, height)
        top_padding = scale(style.top_padding, height)

        bottom_margin = scale(style.bottom_margin, height)
        bottom_padding = scale(style.bottom_padding, height)

        # c for combined.
        cxmargin = left_margin + right_margin
        cymargin = top_margin + bottom_margin

        cxpadding = left_padding + right_padding
        cypadding = top_padding + bottom_padding

        child = self.get_child()

        # Render the child.
        surf = render(child,
                      width  - cxmargin - cxpadding,
                      height - cymargin - cypadding,
                      st, at)

        sw, sh = surf.get_size()

        # If we don't fill, shrink our size to fit.

        if not style.xfill:
            width = max(cxmargin + cxpadding + sw, xminimum)

        if not style.yfill:
            height = max(cymargin + cypadding + sh, yminimum)

        rv = renpy.display.render.Render(width, height)

        # Draw the background. The background should render at exactly the
        # requested size. (That is, be a Frame or a Solid).
        if style.background:
            bw = width - cxmargin
            bh = height - cymargin

            back = render(style.background, bw, bh, st, at)

            style.background.place(rv, left_margin, top_margin, bw, bh, back, main=False)

        offsets = child.place(rv,
                              left_margin + left_padding, 
                              top_margin + top_padding,
                              width  - cxmargin - cxpadding,
                              height - cymargin - cypadding,
                              surf)

        # Draw the foreground. The background should render at exactly the
        # requested size. (That is, be a Frame or a Solid).
        if style.foreground:
            bw = width  - cxmargin
            bh = height - cymargin

            back = render(style.foreground, bw, bh, st, at)

            style.foreground.place(rv, left_margin, top_margin, bw, bh, back, main=False)

        self.offsets = [ offsets ]

        self.window_size = width, height # W0201

        return rv


def dynamic_displayable_compat(st, at, expr):
    child = renpy.python.py_eval(expr)
    return child, None

class DynamicDisplayable(renpy.display.core.Displayable):

    nosave = [ 'child' ]

    def after_setstate(self):
        self.child = None

    def __init__(self, function, *args, **kwargs):
        super(DynamicDisplayable, self).__init__()
        self.child = None

        if isinstance(function, basestring):
            args = ( function, )
            kwargs = { }
            function = dynamic_displayable_compat

        self.predict_function = kwargs.pop("_predict_function", None)            
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def visit(self):
        return [ ]

    def per_interact(self):
        renpy.display.render.redraw(self, 0)
        
    def render(self, w, h, st, at):

        child, redraw = self.function(st, at, *self.args, **self.kwargs)
        child = renpy.easy.displayable(child)

        self.child = child
        child.visit_all(lambda c : c.per_interact())

        if redraw is not None:
            renpy.display.render.redraw(self, redraw)
        
        return renpy.display.render.render(self.child, w, h, st, at)

    def predict_one(self, callback):

        if not self.predict_function:
            return
        
        for i in self.predict_function(*self.args, **self.kwargs):
            if i is not None:
                i.predict(callback)
        
    def get_placement(self):
        return self.child.get_placement()

    def event(self, ev, x, y, st):
        if self.child:
            return self.child.event(ev, x, y, st)

# This chooses the first member of switch that's being shown on the
# given layer.
def condition_switch_pick(switch):
    for cond, d in switch:
        if cond is None or renpy.python.py_eval(cond):
            return d

    raise Exception("Switch could not choose a displayable.")

def condition_switch_show(st, at, switch):
    return condition_switch_pick(switch), None

def condition_switch_predict(switch):

    if renpy.game.lint:
        return [ d for cond, d in switch ]

    return [ condition_switch_pick(switch) ]

def ConditionSwitch(*args, **kwargs):

    kwargs.setdefault('style', 'default')
    
    switch = [ ]
    
    if len(args) % 2 != 0:
        raise Exception('ConditionSwitch takes an even number of arguments')

    for cond, d in zip(args[0::2], args[1::2]):

        d = renpy.easy.displayable(d)
        switch.append((cond, d))

    rv = DynamicDisplayable(condition_switch_show,
                            switch,
                            _predict_function=condition_switch_predict)
                              
    return Position(rv, **kwargs)

    
def ShowingSwitch(*args, **kwargs):

    layer = kwargs.pop('layer', 'master')

    
    if len(args) % 2 != 0:
        raise Exception('ConditionSwitch takes an even number of arguments')

    condargs = [ ]

    
    for name, d in zip(args[0::2], args[1::2]):
        if name is not None:
            if not isinstance(name, tuple):        
                name = tuple(name.split())
            cond = "renpy.showing(%r, layer=%r)" % (name, layer)
        else:
            cond = None 
            
 
        condargs.append(cond)
        condargs.append(d)

    return ConditionSwitch(*condargs, **kwargs)


class IgnoresEvents(Container):

    def __init__(self, child):
        super(IgnoresEvents, self).__init__(style='default')
        self.add(child)
    
    def render(self, w, h, st, at):
        cr = renpy.display.render.render(self.child, w, h, st, at)
        cw, ch = cr.get_size()
        rv = renpy.display.render.Render(cw, ch)
        rv.blit(cr, (0, 0), focus=False)

        return rv

    def get_placement(self):
        return self.child.get_placement()

    # Ignores events.
    def event(self, ev, x, y, st):
        return None
    

        

class Viewport(Container):

    __version__ = 1

    def after_upgrade(self, version):
        if version < 1:
            self.xadjustment = renpy.display.behavior.Adjustment(1, 0)
            self.yadjustment = renpy.display.behavior.Adjustment(1, 0)
            self.set_adjustments = False
            self.mousewheel = False
            self.draggable = False
            self.width = 0
            self.height = 0
            
    def __init__(self,
                 child=None,
                 child_size=(None, None),
                 offsets=(None, None),
                 xadjustment=None,
                 yadjustment=None,
                 set_adjustments=True,
                 mousewheel=False,
                 draggable=False,
                 style='viewport',
                 **properties):

        super(Viewport, self).__init__(style=style, **properties)
        if child is not None:
            self.add(child)

        if xadjustment is None:
            self.xadjustment = renpy.display.behavior.Adjustment(1, 0)
        else:
            self.xadjustment = xadjustment
            
        if yadjustment is None:
            self.yadjustment = renpy.display.behavior.Adjustment(1, 0)
        else:
            self.yadjustment = yadjustment
            
        self.set_adjustments = set_adjustments
        
        self.child_width, self.child_height = child_size
        self.xoffset, self.yoffset = offsets
        self.mousewheel = mousewheel
        self.draggable = draggable

        self.width = 0
        self.height = 0

    def per_interact(self):
        self.xadjustment.register(self)
        self.yadjustment.register(self)
        
    def render(self, width, height, st, at):

        self.width = width
        self.height = height
        
        child_width = self.child_width or width
        child_height = self.child_height or height

        surf = render(self.child, child_width, child_height, st, at)

        cw, ch = surf.get_size()

        # width = min(cw, width)
        # height = min(ch, height)

        if self.set_adjustments:
            self.xadjustment.range = max(cw - width, 0)
            self.xadjustment.page = width
            self.yadjustment.range = max(ch - height, 0)
            self.yadjustment.page = height

        if self.xoffset is not None:
            if isinstance(self.xoffset, int):
                value = self.xoffset
            else:
                value = max(cw - width, 0) * self.xoffset
                
            self.xadjustment.value = value
            self.xoffset = None
            
        if self.yoffset is not None:
            if isinstance(self.yoffset, int):
                value = self.yoffset
            else:
                value = max(ch - height, 0) * self.yoffset 

            self.yadjustment.value = value
            self.yoffset = None
                
        cxo = -int(self.xadjustment.value)
        cyo = -int(self.yadjustment.value)

        self.offsets = [ (cxo, cyo) ]

        rv = renpy.display.render.Render(width, height)
        rv.blit(surf, (cxo, cyo))

        return rv

    def event(self, ev, x, y, st):

        rv = super(Viewport, self).event(ev, x, y, st)
        if rv is not None:
            return rv

        if self.draggable and renpy.display.focus.get_grab() == self:

            oldx, oldy = self.drag_position
            dx = x - oldx
            dy = y - oldy

            self.xadjustment.change(self.xadjustment.value - dx)
            self.yadjustment.change(self.yadjustment.value - dy)

            self.drag_position = (x, y) # W0201
            
            if renpy.display.behavior.map_event(ev, 'viewport_drag_end'):
                renpy.display.focus.set_grab(None)
                raise renpy.display.core.IgnoreEvent()
                
        if not ((0 <= x < self.width) and (0 <= y <= self.height)):
            return
                
        if self.mousewheel:

            if renpy.display.behavior.map_event(ev, 'viewport_up'):
                rv = self.yadjustment.change(self.yadjustment.value - self.yadjustment.step)
                if rv is not None:
                    return rv
                else:
                    raise renpy.display.core.IgnoreEvent()

            if renpy.display.behavior.map_event(ev, 'viewport_down'):
                rv = self.yadjustment.change(self.yadjustment.value + self.yadjustment.step)
                if rv is not None:
                    return rv
                else:
                    raise renpy.display.core.IgnoreEvent()

        if self.draggable:

            if renpy.display.behavior.map_event(ev, 'viewport_drag_start'):
                self.drag_position = (x, y)
                renpy.display.focus.set_grab(self)
                raise renpy.display.core.IgnoreEvent()
                
        return None
    
    def set_xoffset(self, offset):
        self.xoffset = offset
        renpy.display.render.redraw(self, 0)
        
    def set_yoffset(self, offset):
        self.yoffset = offset
        renpy.display.render.redraw(self, 0)
        
def LiveCrop(rect, child, **properties):
    x, y, w, h = rect

    return Viewport(child, offsets=(x, y), xmaximum=w, ymaximum=h, **properties)

class Side(Container):

    possible_positions = set([ 'tl', 't', 'tr', 'r', 'br', 'b', 'bl', 'l', 'c'])

    def after_setstate(self):
        self.sized = False
    
    def __init__(self, positions, style='default', **properties):

        super(Side, self).__init__(style=style, **properties)

        if isinstance(positions, basestring):
            positions = positions.split()
        
        for i in positions:
            if not i in Side.possible_positions:
                raise Exception("Side used with impossible position '%s'." % (i,))

        self.positions = tuple(positions)
        self.sized = False
        
    def render(self, width, height, st, at):

        pos_d = { }
        pos_i = { }
        
        for i, (pos, d) in enumerate(zip(self.positions, self.children)):
            pos_d[pos] = d
            pos_i[pos] = i

        # Figure out the size of each widget (and hence where the
        # widget needs to be placed).

        if not self.sized:
            self.sized = True
            
            # Deal with various spacings.
            spacing = self.style.spacing
            
            def spacer(a, b, c, axis):
                if (a in pos_d) or (b in pos_d) or (c in pos_d):
                    return spacing, axis - spacing
                else:
                    return 0, axis
                
            self.left_space, width = spacer('tl', 'l', 'bl', width) # W0201
            self.right_space, width = spacer('tr', 'r', 'br', width) # W0201
            self.top_space, height = spacer('tl', 't', 'tr', height) # W0201
            self.bottom_space, height = spacer('bl', 'b', 'br', height) # W0201
            
            # The sizes of the various borders.
            left = 0
            right = 0
            top = 0
            bottom = 0
            cwidth = 0
            cheight = 0
            
            def sizeit(pos, width, height, owidth, oheight):
                if pos not in pos_d:
                    return owidth, oheight
                
                rend = render(pos_d[pos], width, height, st, at)
                rv = max(owidth, rend.width), max(oheight, rend.height)
                rend.kill()
                return rv
                
            cwidth, cheight = sizeit('c', width, height, 0, 0)
            cwidth, top = sizeit('t', cwidth, height, cwidth, top)
            cwidth, bottom = sizeit('b', cwidth, height, cwidth, bottom)
            left, cheight = sizeit('l', width, cheight, left, cheight) 
            right, cheight = sizeit('r', width, cheight, right, cheight) 

            left, top = sizeit('tl', left, top, left, top)
            left, bottom = sizeit('bl', left, bottom, left, bottom)
            right, top = sizeit('tr', right, top, right, top)
            right, bottom = sizeit('br', right, bottom, right, bottom)
            
            self.cwidth = cwidth # W0201
            self.cheight = cheight # W0201

            self.top = top # W0201
            self.bottom = bottom # W0201
            self.left = left # W0201
            self.right = right # W0201

        else:
            cwidth = self.cwidth
            cheight = self.cheight
            top = self.top
            bottom = self.bottom
            left = self.left
            right = self.right
        
        # Now, place everything onto the render.
        
        self.offsets = [ None ] * len(self.children)

        lefts = self.left_space
        rights = self.right_space
        tops = self.top_space
        bottoms = self.bottom_space


        cwidth = min(cwidth, width - left - lefts - right - rights)
        cheight = min(cheight, height - top - tops - bottom - bottoms)
        
        rv = renpy.display.render.Render(left + lefts + cwidth + rights + right,
                                         top + tops + cheight + bottoms + bottom)

        def place(pos, x, y, w, h):

            if pos not in pos_d:
                return

            d = pos_d[pos]
            i = pos_i[pos]
            rend = render(d, w, h, st, at)
            self.offsets[i] = pos_d[pos].place(rv, x, y, w, h, rend)
            
        col1 = 0
        col2 = left + lefts
        col3 = left + lefts + cwidth + rights

        row1 = 0
        row2 = top + tops
        row3 = top + tops + cheight + bottoms

        place('c', col2, row2, cwidth, cheight)

        place('t', col2, row1, cwidth, top)
        place('r', col3, row2, right, cheight)
        place('b', col2, row3, cwidth, bottom)
        place('l', col1, row2, left, cheight)

        place('tl', col1, row1, left, top)
        place('tr', col3, row1, right, top)
        place('br', col3, row3, right, bottom)
        place('bl', col1, row3, left, bottom)

        return rv
        
class Alpha(renpy.display.core.Displayable):
    def __init__(self, start, end, time, child=None, repeat=False, bounce=False,
                 anim_timebase=False, time_warp=None, **properties):

        super(Alpha, self).__init__(**properties)

        self.start = start
        self.end = end
        self.time = time
        self.child = renpy.easy.displayable(child)
        self.repeat = repeat
        self.anim_timebase = anim_timebase
        self.time_warp = time_warp
        
    def visit(self):
        return [ self.child ]

    def render(self, height, width, st, at):
        if self.anim_timebase:
            t = at
        else:
            t = st
        
        if self.time:
            done = min(t / self.time, 1.0)
        else:
            done = 1.0

        if renpy.game.less_updates:
            done = 1.0
        elif self.repeat:
            done = done % 1.0
            renpy.display.render.redraw(self, 0)
        elif done != 1.0:
            renpy.display.render.redraw(self, 0)
            
        if self.time_warp:
            done = self.time_warp(done)

        alpha = self.start + done * (self.end - self.start)
            
        rend = renpy.display.render.render(self.child, height, width, st, at)

        w, h = rend.get_size()
        rv = renpy.display.render.Render(w, h)
        rv.blit(rend, (0, 0))
        rv.alpha = alpha

        return rv
        
        
class AdjustTimes(Container):

    def __init__(self, child, start_time, anim_time):
        super(AdjustTimes, self).__init__(style='default')

        self.start_time = start_time
        self.anim_time = anim_time

        self.add(child)
    
    def render(self, w, h, st, at):

        if self.start_time is None:
            self.start_time = renpy.game.interface.frame_time

        if self.anim_time is None:
            self.anim_time = renpy.game.interface.frame_time

        st = renpy.game.interface.frame_time - self.start_time
        at = renpy.game.interface.frame_time - self.anim_time       
            
        cr = renpy.display.render.render(self.child, w, h, st, at)
        cw, ch = cr.get_size()
        rv = renpy.display.render.Render(cw, ch)
        rv.blit(cr, (0, 0))

        self.offsets = [ (0, 0) ]
        
        return rv

    def get_placement(self):
        return self.child.get_placement()


