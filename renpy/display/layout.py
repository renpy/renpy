# Copyright 2004-2018 Tom Rothamel <pytom@bishoujo.us>
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

from __future__ import print_function

from renpy.display.render import render, Render
import renpy.display


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
    :doc: disp_imagelike
    :name: Null

    A displayable that creates an empty box on the screen. The size
    of the box is controlled by `width` and `height`. This can be used
    when a displayable requires a child, but no child is suitable, or
    as a spacer inside a box.

    ::

        image logo spaced = HBox("logo.png", Null(width=100), "logo.png")

    """

    def __init__(self, width=0, height=0, **properties):
        super(Null, self).__init__(**properties)
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

    def _handles_event(self, event):
        for i in self.children:
            if i._handles_event(event):
                return True

        return False

    def set_style_prefix(self, prefix, root):
        super(Container, self).set_style_prefix(prefix, root)

        for i in self.children:
            i.set_style_prefix(prefix, False)

    def _duplicate(self, args):

        if not self._duplicatable:
            return self

        rv = self._copy(args)
        rv.children = [ i._duplicate(args) for i in self.children ]

        if rv.children:
            rv.child = rv.children[-1]

        rv._duplicatable = False

        for i in rv.children:
            i._unique()

            if i._duplicatable:
                rv._duplicatable = True

        return rv

    def _in_current_store(self):

        children = [ ]

        changed = False

        for old in self.children:
            new = old._in_current_store()
            changed |= (old is not new)
            children.append(new)

        if not changed:
            return self

        rv = self._copy()
        rv.children = children

        if rv.children:
            rv.child = rv.children[-1]

        return rv

    def add(self, d):
        """
        Adds a child to this container.
        """

        child = renpy.easy.displayable(d)

        self.children.append(child)

        self.child = child
        self.offsets = self._list_type()

        if child._duplicatable:
            self._duplicatable = True

    def _clear(self):
        self.child = None
        self.children = self._list_type()
        self.offsets = self._list_type()

        renpy.display.render.redraw(self, 0)

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

        self.children.pop(i)  # W0631
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

        # In #641, these went out of sync. Since they should resync on a
        # render, ignore the event for a short while rather than crashing.
        if len(offsets) != len(children):
            return None

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

        renpy.ui.context_enter(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        renpy.ui.context_exit(self)
        return False


def Composite(size, *args, **properties):
    """
    :name: Composite
    :doc: disp_imagelike

    This creates a new displayable of `size`, by compositing other
    displayables. `size` is a (width, height) tuple.

    The remaining positional arguments are used to place images inside
    the LiveComposite. The remaining positional arguments should come
    in groups of two, with the first member of each group an (x, y)
    tuple, and the second member of a group is a displayable that
    is composited at that position.

    Displayables are composited from back to front.

    ::

       image eileen composite = Composite(
           (300, 600),
           (0, 0), "body.png",
           (0, 0), "clothes.png",
           (50, 50), "expression.png")
    """

    properties.setdefault('style', 'image_placement')

    width, height = size

    rv = Fixed(xmaximum=width, ymaximum=height, xminimum=width, yminimum=height, **properties)

    if len(args) % 2 != 0:
        raise Exception("LiveComposite requires an odd number of arguments.")

    for pos, widget in zip(args[0::2], args[1::2]):
        xpos, ypos = pos
        rv.add(Position(widget, xpos=xpos, xanchor=0, ypos=ypos, yanchor=0))

    return rv


LiveComposite = Composite


class Position(Container):
    """
    :undocumented:

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

        self.offsets = [ (0, 0) ]

        rv = renpy.display.render.Render(surf.width, surf.height)
        rv.blit(surf, (0, 0))

        return rv

    def get_placement(self):

        xpos, ypos, xanchor, yanchor, xoffset, yoffset, subpixel = self.child.get_placement()

        if xoffset is None:
            xoffset = 0
        if yoffset is None:
            yoffset = 0

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
            xoffset += v

        v = self.style.yoffset
        if v is not None:
            yoffset += v

        v = self.style.subpixel
        if (not subpixel) and (v is not None):
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
                 style='grid', **properties):
        """
        @param cols: The number of columns in this widget.

        @params rows: The number of rows in this widget.

        @params transpose: True if the grid should be transposed.
        """

        if padding is not None:
            properties.setdefault('spacing', padding)

        super(Grid, self).__init__(style=style, **properties)

        cols = int(cols)
        rows = int(rows)

        self.cols = cols
        self.rows = rows

        self.transpose = transpose

    def render(self, width, height, st, at):

        xspacing = self.style.xspacing
        yspacing = self.style.yspacing

        if xspacing is None:
            xspacing = self.style.spacing
        if yspacing is None:
            yspacing = self.style.spacing

        # For convenience and speed.
        cols = self.cols
        rows = self.rows

        if len(self.children) != cols * rows:
            if len(self.children) < cols * rows:
                raise Exception("Grid not completely full.")
            else:
                raise Exception("Grid overfull.")

        if self.transpose:
            children = [ ]
            for y in range(rows):
                for x in range(cols):
                    children.append(self.children[y + x * rows])

        else:
            children = self.children

        # Now, start the actual rendering.

        renwidth = width
        renheight = height

        if self.style.xfill:
            renwidth = (width - (cols - 1) * xspacing) / cols
        if self.style.yfill:
            renheight = (height - (rows - 1) * yspacing) / rows

        renders = [ render(i, renwidth, renheight, st, at) for i in children ]
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

        width = cwidth * cols + xspacing * (cols - 1)
        height = cheight * rows + yspacing * (rows - 1)

        rv = renpy.display.render.Render(width, height)

        offsets = [ ]

        for y in range(0, rows):
            for x in range(0, cols):

                child = children[ x + y * cols ]
                surf = renders[x + y * cols]

                xpos = x * (cwidth + xspacing)
                ypos = y * (cheight + yspacing)

                offset = child.place(rv, xpos, ypos, cwidth, cheight, surf)
                offsets.append(offset)

        if self.transpose:
            self.offsets = [ ]
            for x in range(cols):
                for y in range(rows):
                    self.offsets.append(offsets[y * cols + x])
        else:
            self.offsets = offsets

        return rv


class IgnoreLayers(Exception):
    """
    Raise this to have the event ignored by layers, but reach the
    underlay.
    """

    pass


class MultiBox(Container):

    layer_name = None
    first = True
    order_reverse = False
    layout = None

    def __init__(self, spacing=None, layout=None, style='default', **properties):

        if spacing is not None:
            properties['spacing'] = spacing

        super(MultiBox, self).__init__(style=style, **properties)

        self._clipping = self.style.clipping

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

    def _clear(self):
        super(MultiBox, self)._clear()

        self.start_times = [ ]
        self.anim_times = [ ]
        self.layers = None
        self.scene_list = None

    def _in_current_store(self):

        if self.layer_name is not None:

            if self.scene_list is None:
                return self

            scene_list = [ ]

            changed = False

            for old_sle in self.scene_list:
                new_sle = old_sle.copy()

                d = new_sle.displayable._in_current_store()

                if d is not new_sle.displayable:
                    new_sle.displayable = d
                    changed = True

                scene_list.append(new_sle)

            if not changed:
                return self

            rv = MultiBox(layout=self.default_layout)
            rv.layer_name = self.layer_name
            rv.append_scene_list(scene_list)

        elif self.layers:
            rv = MultiBox(layout=self.default_layout)
            rv.layers = { }

            changed = False

            for layer in renpy.config.layers:
                old_d = self.layers[layer]
                new_d = old_d._in_current_store()

                if new_d is not old_d:
                    changed = True

                rv.add(new_d)
                rv.layers[layer] = new_d

            if not changed:
                return self

        else:
            return super(MultiBox, self)._in_current_store()

        if self.offsets:
            rv.offsets = list(self.offsets)
        if self.start_times:
            rv.start_times = list(self.start_times)
        if self.anim_times:
            rv.anim_times = list(self.anim_times)

        return rv

    def __unicode__(self):
        layout = self.style.box_layout

        if layout is None:
            layout = self.default_layout

        if layout == "fixed":
            return "Fixed"
        elif layout == "horizontal":
            return "HBox"
        elif layout == "vertical":
            return "VBox"
        else:
            return "MultiBox"

    def add(self, widget, start_time=None, anim_time=None):  # W0221
        super(MultiBox, self).add(widget)
        self.start_times.append(start_time)
        self.anim_times.append(anim_time)

    def append_scene_list(self, l):

        for sle in l:
            self.add(sle.displayable, sle.show_time, sle.animation_time)

        if self.scene_list is None:
            self.scene_list = [ ]

        self.scene_list.extend(l)

    def update_times(self):

        it = renpy.game.interface.interact_time

        self.start_times = [ i or it for i in self.start_times ]
        self.anim_times = [ i or it for i in self.anim_times ]

        if it is None:
            self.first = True

    def render(self, width, height, st, at):

        # Do we need to adjust the child times due to our being a layer?
        if self.layer_name or (self.layers is not None):
            adjust_times = True
        else:
            adjust_times = False

        minx = self.style.xminimum
        if minx is not None:
            width = max(width, scale(minx, width))

        miny = self.style.yminimum
        if miny is not None:
            height = max(height, scale(miny, height))

        if self.first:

            self.first = False

            if adjust_times:
                self.update_times()

        layout = self.style.box_layout

        if layout is None:
            layout = self.default_layout

        # Handle time adjustment, store the results in csts and cats.
        if adjust_times:
            t = renpy.game.interface.frame_time

            csts = [ 0 if (start is None) else (t - start) for start in self.start_times ]
            cats = [ 0 if (anim is None) else (t - anim) for anim in self.anim_times ]

        else:
            csts = [ st ] * len(self.children)
            cats = [ at ] * len(self.children)

        offsets = [ ]

        if layout == "fixed":

            rv = None

            if self.style.order_reverse:
                iterator = zip(reversed(self.children), reversed(csts), reversed(cats))
            else:
                iterator = zip(self.children, csts, cats)

            rv = renpy.display.render.Render(width, height, layer_name=self.layer_name)

            xfit = self.style.xfit
            yfit = self.style.yfit

            fit_first = self.style.fit_first

            if fit_first == "width":
                first_fit_width = True
                first_fit_height = False
            elif fit_first == "height":
                first_fit_width = False
                first_fit_height = True
            elif fit_first:
                first_fit_width = True
                first_fit_height = True
            else:
                first_fit_width = False
                first_fit_height = False

            sizes = [ ]

            for child, cst, cat in iterator:

                surf = render(child, width, height, cst, cat)
                size = surf.get_size()
                sizes.append(size)

                if first_fit_width:
                    width = rv.width = size[0]
                    first_fit_width = False

                if first_fit_height:
                    height = rv.height = size[1]
                    first_fit_height = False

                if surf:
                    offset = child.place(rv, 0, 0, width, height, surf)
                    offsets.append(offset)
                else:
                    offsets.append((0, 0))

            if xfit:
                width = 0

                for o, s in zip(offsets, sizes):
                    width = max(o[0] + s[0], width)

                    if fit_first:
                        break

                rv.width = width

                if width > renpy.config.max_fit_size:
                    raise Exception("Fixed fit width ({}) is too large.".format(width))

            if yfit:
                height = 0

                for o, s in zip(offsets, sizes):
                    height = max(o[1] + s[1], height)

                    if fit_first:
                        break

                rv.height = height

                if height > renpy.config.max_fit_size:
                    raise Exception("Fixed fit width ({}) is too large.".format(height))

            if self.style.order_reverse:
                offsets.reverse()

            self.offsets = offsets

            return rv

        # If we're here, we have a box, either horizontal or vertical. Which is good,
        # as we can share some code between boxes.

        spacing = self.style.spacing
        first_spacing = self.style.first_spacing

        if first_spacing is None:
            first_spacing = spacing

        spacings = [ first_spacing ] + [ spacing ] * (len(self.children) - 1)

        box_wrap = self.style.box_wrap
        box_wrap_spacing = self.style.box_wrap_spacing
        xfill = self.style.xfill
        yfill = self.style.yfill
        xminimum = self.style.xminimum
        yminimum = self.style.yminimum

        # The shared height and width of the current line. The line_height must
        # be 0 for a vertical box, and the line_width must be 0 for a horizontal
        # box.
        line_width = 0
        line_height = 0

        # The children to layout.
        children = list(self.children)
        if self.style.box_reverse:
            children.reverse()
            spacings.reverse()

        # a list of (child, x, y, w, h, surf) tuples that are turned into
        # calls to child.place().
        placements = [ ]

        # The maximum x and y.
        maxx = 0
        maxy = 0

        # The minimum size of x and y.
        minx = 0
        miny = 0

        def layout_line(line, xfill, yfill):
            """
            Lays out a single line.

            `line` a list of (child, x, y, surf) tuples.
            `xfill` the amount of space to add in the x direction.
            `yfill` the amount of space to add in the y direction.
            """

            xfill = max(0, xfill)
            yfill = max(0, yfill)

            if line:
                xperchild = xfill / len(line)
                yperchild = yfill / len(line)
            else:
                xperchild = 0
                yperchild = 0

            maxxout = maxx
            maxyout = maxy

            for i, (child, x, y, surf) in enumerate(line):
                sw, sh = surf.get_size()
                sw = max(line_width, sw)
                sh = max(line_height, sh)

                x += i * xperchild
                y += i * yperchild

                sw += xperchild
                sh += yperchild

                placements.append((child, x, y, sw, sh, surf))

                maxxout = max(maxxout, x + sw)
                maxyout = max(maxyout, y + sh)

            return maxxout, maxyout

        x = 0
        y = 0

        if layout == "horizontal":

            if yfill:
                miny = height
            else:
                miny = yminimum

            line_height = 0
            line = [ ]
            remwidth = width

            if xfill:
                target_width = width
            else:
                target_width = xminimum

            for d, padding, cst, cat in zip(children, spacings, csts, cats):

                if box_wrap:
                    rw = width
                else:
                    rw = remwidth

                surf = render(d, rw, height - y, cst, cat)
                sw, sh = surf.get_size()

                if box_wrap and remwidth - sw - padding < 0 and line:
                    maxx, maxy = layout_line(line, target_width - x, 0)

                    y += line_height + box_wrap_spacing
                    x = 0
                    line_height = 0
                    remwidth = width
                    line = [ ]

                line.append((d, x, y, surf))
                line_height = max(line_height, sh)
                x += sw + padding
                remwidth -= (sw + padding)

            maxx, maxy = layout_line(line, target_width - x, 0)

        elif layout == "vertical":

            if xfill:
                minx = width
            else:
                minx = xminimum

            line_width = 0
            line = [ ]
            remheight = height

            if yfill:
                target_height = height
            else:
                target_height = yminimum

            for d, padding, cst, cat in zip(children, spacings, csts, cats):

                if box_wrap:
                    rh = height
                else:
                    rh = remheight

                surf = render(d, width - x, rh, cst, cat)
                sw, sh = surf.get_size()

                if box_wrap and remheight - sh - padding < 0:
                    maxx, maxy = layout_line(line, 0, target_height - y)

                    x += line_width + box_wrap_spacing
                    y = 0
                    line_width = 0
                    remheight = height
                    line = [ ]

                line.append((d, x, y, surf))
                line_width = max(line_width, sw)
                y += sh + padding
                remheight -= (sh + padding)

            maxx, maxy = layout_line(line, 0, target_height - y)

        else:
            raise Exception("Unknown box layout: %r" % layout)

        # Back to the common for vertical and horizontal.

        if not xfill:
            width = max(xminimum, maxx)

        if not yfill:
            height = max(yminimum, maxy)

        rv = renpy.display.render.Render(width, height)

        if self.style.box_reverse ^ self.style.order_reverse:
            placements.reverse()

        for child, x, y, w, h, surf in placements:
            w = max(minx, w)
            h = max(miny, h)

            offset = child.place(rv, x, y, w, h, surf)
            offsets.append(offset)

        if self.style.order_reverse:
            offsets.reverse()

        self.offsets = offsets

        return rv

    def event(self, ev, x, y, st):

        # Do we need to adjust the child times due to our being a layer?
        if self.first:

            self.first = False

            if self.layer_name or (self.layers is not None):
                self.update_times()

        children_offsets = zip(self.children, self.offsets, self.start_times)

        if not self.style.order_reverse:
            children_offsets.reverse()

        try:

            for i, (xo, yo), t in children_offsets:

                if t is None:
                    cst = st
                else:
                    cst = renpy.game.interface.event_time - t

                rv = i.event(ev, x - xo, y - yo, cst)
                if rv is not None:
                    return rv

        except IgnoreLayers:
            if self.layers:

                if ev.type != renpy.display.core.TIMEEVENT:
                    renpy.display.interface.post_time_event()

                return None
            else:
                raise

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
            rend = i.render(width, height, st, at)
            maxwidth = max(rend.width, maxwidth)

        self._width = maxwidth
        self.computing_width = False

        return maxwidth


size_groups = dict()


class Window(Container):
    """
    A window that has padding and margins, and can place a background
    behind its child. `child` is the child added to this
    displayable. All other properties are as for the :ref:`Window`
    screen language statement.
    """

    def __init__(self, child=None, style='window', **properties):
        super(Window, self).__init__(style=style, **properties)
        if child is not None:
            self.add(child)

    def visit(self):
        rv = [ ]
        self.style._visit_window(rv.append)
        return rv + self.children

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

        xmaximum = scale(style.xmaximum, width)
        ymaximum = scale(style.ymaximum, height)

        size_group = self.style.size_group
        if size_group and size_group in size_groups:
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

        if renpy.config.enforce_window_max_size:

            if xmaximum is not None:
                width = min(width, xmaximum)

            if ymaximum is not None:
                height = min(height, ymaximum)

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

        if self.child:
            self.offsets = [ offsets ]

        self.window_size = width, height  # W0201

        return rv


def dynamic_displayable_compat(st, at, expr):
    child = renpy.python.py_eval(expr)
    return child, None


class DynamicDisplayable(renpy.display.core.Displayable):
    """
    :doc: disp_dynamic

    A displayable that can change its child based on a Python
    function, over the course of an interaction.

    `function`
        A function that is called with the arguments:

        * The amount of time the displayable has been shown for.
        * The amount of time any displayable with the same tag has been shown for.
        * Any positional or keyword arguments supplied to DynamicDisplayable.

        and should return a (d, redraw) tuple, where:

        * `d` is a displayable to show.
        * `redraw` is the amount of time to wait before calling the
          function again, or None to not call the function again
          before the start of the next interaction.

        `function` is called at the start of every interaction.

    As a special case, `function` may also be a python string that evaluates
    to a displayable. In that case, function is run once per interaction.

    ::

        # Shows a countdown from 5 to 0, updating it every tenth of
        # a second until the time expires.
        init python:

            def show_countdown(st, at):
                if st > 5.0:
                    return Text("0.0"), None
                else:
                    d = Text("{:.1f}".format(5.0 - st))
                    return d, 0.1

        image countdown = DynamicDisplayable(show_countdown)
    """

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

    def update(self, st, at):
        child, redraw = self.function(st, at, *self.args, **self.kwargs)
        child = renpy.easy.displayable(child)
        child.visit_all(lambda c : c.per_interact())

        self.child = child

        if redraw is not None:
            renpy.display.render.redraw(self, redraw)

    def per_interact(self):
        renpy.display.render.redraw(self, 0)

    def render(self, w, h, st, at):
        self.update(st, at)

        return renpy.display.render.render(self.child, w, h, st, at)

    def predict_one(self):
        try:
            if self.predict_function:
                child = self.predict_function(*self.args, **self.kwargs)
            else:
                child, _ = self.function(0, 0, *self.args, **self.kwargs)

            if isinstance(child, list):

                for i in child:
                    renpy.display.predict.displayable(i)
            else:
                renpy.display.predict.displayable(child)

        except:
            pass

    def get_placement(self):
        if not self.child:
            self.update(0, 0)

        return self.child.get_placement()

    def event(self, ev, x, y, st):
        if self.child:
            return self.child.event(ev, x, y, st)


# A cache of compiled conditions used by ConditionSwitch.
cond_cache = { }

# This chooses the first member of switch that's being shown on the
# given layer.


def condition_switch_pick(switch):
    for cond, d in switch:

        if cond is None:
            return d

        if cond in cond_cache:
            code = cond_cache[cond]
        else:
            code = renpy.python.py_compile(cond, 'eval')
            cond_cache[cond] = code

        if renpy.python.py_eval_bytecode(code):
            return d

    raise Exception("Switch could not choose a displayable.")


def condition_switch_show(st, at, switch, predict_all=None):
    return condition_switch_pick(switch), None


def condition_switch_predict(switch, predict_all=None):

    if predict_all is None:
        predict_all = renpy.config.conditionswitch_predict_all

    if renpy.game.lint or (predict_all and renpy.display.predict.predicting):
        return [ d for _cond, d in switch ]

    return [ condition_switch_pick(switch) ]


def ConditionSwitch(*args, **kwargs):
    """
    :doc: disp_dynamic
    :args: (*args, predict_all=None, **properties)

    This is a displayable that changes what it is showing based on
    Python conditions. The positional arguments should be given in
    groups of two, where each group consists of:

    * A string containing a Python condition.
    * A displayable to use if the condition is true.

    The first true condition has its displayable shown, at least
    one condition should always be true.

    The conditions uses here should not have externally-visible side-effects.

    `predict_all`
        If True, all of the possible displayables will be predicted when
        the displayable is shown. If False, only the current condition is
        predicted. If None, :var:`config.conditionswitch_predict_all` is
        used.

    ::

        image jill = ConditionSwitch(
            "jill_beers > 4", "jill_drunk.png",
            "True", "jill_sober.png")
    """

    predict_all = kwargs.pop("predict_all", None)
    kwargs.setdefault('style', 'default')

    switch = [ ]

    if len(args) % 2 != 0:
        raise Exception('ConditionSwitch takes an even number of arguments')

    for cond, d in zip(args[0::2], args[1::2]):

        if cond not in cond_cache:
            code = renpy.python.py_compile(cond, 'eval')
            cond_cache[cond] = code

        d = renpy.easy.displayable(d)
        switch.append((cond, d))

    rv = DynamicDisplayable(condition_switch_show,
                            switch,
                            predict_all,
                            _predict_function=condition_switch_predict)

    return Position(rv, **kwargs)


def ShowingSwitch(*args, **kwargs):
    """
    :doc: disp_dynamic
    :args: (*args, predict_all=None, **properties)

    This is a displayable that changes what it is showing based on the
    images are showing on the screen. The positional argument should
    be given in groups of two, where each group consists of:

    * A string giving an image name, or None to indicate the default.
    * A displayable to use if the condition is true.

    A default image should be specified.

    `predict_all`
        If True, all of the possible displayables will be predicted when
        the displayable is shown. If False, only the current condition is
        predicted. If None, :var:`config.conditionswitch_predict_all` is
        used.

    One use of ShowingSwitch is to have side images change depending on
    the current emotion of a character. For example::

       define e = Character("Eileen",
           show_side_image=ShowingSwitch(
               "eileen happy", Image("eileen_happy_side.png", xalign=1.0, yalign=1.0),
               "eileen vhappy", Image("eileen_vhappy_side.png", xalign=1.0, yalign=1.0),
               None, Image("eileen_happy_default.png", xalign=1.0, yalign=1.0),
               )
           )
    """

    layer = kwargs.pop('layer', 'master')

    if len(args) % 2 != 0:
        raise Exception('ShowingSwitch takes an even number of positional arguments')

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

    def __init__(self, child, **properties):
        super(IgnoresEvents, self).__init__(**properties)
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


def Crop(rect, child, **properties):
    """
    :doc: disp_imagelike
    :name: Crop

    This creates a displayable by cropping `child` to `rect`, where
    `rect` is an (x, y, width, height) tuple. ::

        image eileen cropped = Crop((0, 0, 300, 300), "eileen happy")
    """

    return renpy.display.motion.Transform(child, crop=rect, **properties)


LiveCrop = Crop


class Side(Container):

    possible_positions = set([ 'tl', 't', 'tr', 'r', 'br', 'b', 'bl', 'l', 'c'])

    def after_setstate(self):
        self.sized = False

    def __init__(self, positions, style='side', **properties):

        super(Side, self).__init__(style=style, **properties)

        if isinstance(positions, basestring):
            positions = positions.split()

        seen = set()

        for i in positions:
            if not i in Side.possible_positions:
                raise Exception("Side used with impossible position '%s'." % (i,))

            if i in seen:
                raise Exception("Side used with duplicate position '%s'." % (i,))

            seen.add(i)

        self.positions = tuple(positions)
        self.sized = False

    def add(self, d):
        if len(self.children) >= len(self.positions):
            raise Exception("Side has been given too many arguments.")

        super(Side, self).add(d)

    def _clear(self):
        super(Side, self)._clear()
        self.sized = False

    def render(self, width, height, st, at):

        pos_d = { }
        pos_i = { }

        for i, (pos, d) in enumerate(zip(self.positions, self.children)):
            pos_d[pos] = d
            pos_i[pos] = i

        # Figure out the size of each widget (and hence where the
        # widget needs to be placed).

        old_width = width
        old_height = height

        if not self.sized:
            self.sized = True

            # Deal with various spacings.
            spacing = self.style.spacing

            def spacer(a, b, c, axis):
                if (a in pos_d) or (b in pos_d) or (c in pos_d):
                    return spacing, axis - spacing
                else:
                    return 0, axis

            self.left_space, width = spacer('tl', 'l', 'bl', width)  # W0201
            self.right_space, width = spacer('tr', 'r', 'br', width)  # W0201
            self.top_space, height = spacer('tl', 't', 'tr', height)  # W0201
            self.bottom_space, height = spacer('bl', 'b', 'br', height)  # W0201

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

            self.cwidth = cwidth  # W0201
            self.cheight = cheight  # W0201

            self.top = top  # W0201
            self.bottom = bottom  # W0201
            self.left = left  # W0201
            self.right = right  # W0201

        else:
            cwidth = self.cwidth
            cheight = self.cheight
            top = self.top
            bottom = self.bottom
            left = self.left
            right = self.right

        # Now, place everything onto the render.

        width = old_width
        height = old_height

        self.offsets = [ None ] * len(self.children)

        lefts = self.left_space
        rights = self.right_space
        tops = self.top_space
        bottoms = self.bottom_space

        if self.style.xfill:
            cwidth = width

        if self.style.yfill:
            cheight = height

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

    def __init__(self, child, start_time, anim_time, **properties):
        super(AdjustTimes, self).__init__(**properties)

        self.start_time = start_time
        self.anim_time = anim_time

        self.add(child)

    def adjusted_times(self):

        interact_time = renpy.game.interface.interact_time

        if (self.start_time is None) and (interact_time is not None):
            self.start_time = interact_time

        if self.start_time is not None:
            st = renpy.game.interface.frame_time - self.start_time
        else:
            st = 0

        if (self.anim_time is None) and (interact_time is not None):
            self.anim_time = interact_time

        if self.anim_time is not None:
            at = renpy.game.interface.frame_time - self.anim_time
        else:
            at = 0

        return st, at

    def render(self, w, h, st, at):

        st, at = self.adjusted_times()

        cr = renpy.display.render.render(self.child, w, h, st, at)
        cw, ch = cr.get_size()
        rv = renpy.display.render.Render(cw, ch)
        rv.blit(cr, (0, 0))

        self.offsets = [ (0, 0) ]

        return rv

    def event(self, ev, x, y, st):
        st, _ = self.adjusted_times()
        Container.event(self, ev, x, y, st)

    def get_placement(self):
        return self.child.get_placement()


class Tile(Container):
    """
    :doc: disp_imagelike
    :name: Tile

    Tiles `child` until it fills the area allocated to this displayable.

    ::

        image bg tile = Tile("bg.png")

    """

    def __init__(self, child, style='tile', **properties):
        super(LiveTile, self).__init__(style=style, **properties)

        self.add(child)

    def render(self, width, height, st, at):

        cr = renpy.display.render.render(self.child, width, height, st, at)
        cw, ch = cr.get_size()
        rv = renpy.display.render.Render(width, height)

        width = int(width)
        height = int(height)
        cw = int(cw)
        ch = int(ch)

        for y in range(0, height, ch):
            for x in range(0, width, cw):

                ccw = min(cw, width - x)
                cch = min(ch, height - y)

                if (ccw < cw) or (cch < ch):
                    ccr = cr.subsurface((0, 0, ccw, cch))
                else:
                    ccr = cr

                rv.blit(ccr, (x, y), focus=False)

        return rv


LiveTile = Tile


class Flatten(Container):
    """
    :doc: disp_imagelike

    This flattens `child`, which may be made up of multiple textures, into
    a single texture.

    Certain operations, like the alpha transform property, apply to every
    texture making up a displayable, which can yield incorrect results
    when the textures overlap on screen. Flatten creates a single texture
    from multiple textures, which can prevent this problem.

    Flatten is a relatively expensive operation, and so should only be used
    when absolutely required.
    """

    def __init__(self, child, **properties):
        super(Flatten, self).__init__(**properties)

        self.add(child)

    def render(self, width, height, st, at):
        cr = renpy.display.render.render(self.child, width, height, st, at)
        cw, ch = cr.get_size()

        tex = cr.render_to_texture(True)

        rv = renpy.display.render.Render(cw, ch)
        rv.blit(tex, (0, 0))
        rv.depends_on(cr, focus=True)

        rv.reverse = renpy.display.draw.draw_to_virt
        rv.forward = renpy.display.render.IDENTITY

        self.offsets = [ (0, 0) ]

        return rv


class AlphaMask(Container):
    """
    :doc: disp_imagelike

    This displayable takes its colors from `child`, and its alpha channel
    from the multiplication of the alpha channels of `child` and `mask`.
    The result is a displayable that has the same colors as `child`, is
    transparent where either `child` or `mask` is transparent, and is
    opaque where `child` and `mask` are both opaque.

    The `child` and `mask` parameters may be arbitrary displayables. The
    size of the AlphaMask is the size of `child`.
    """

    def __init__(self, child, mask, **properties):
        super(AlphaMask, self).__init__(**properties)

        self.add(child)
        self.mask = renpy.easy.displayable(mask)
        self.null = None

    def render(self, width, height, st, at):

        cr = renpy.display.render.render(self.child, width, height, st, at)
        w, h = cr.get_size()

        mr = renpy.display.render.Render(w, h)
        mr.place(self.mask, main=False)

        if self.null is None:
            self.null = Fixed()

        nr = renpy.display.render.render(self.null, w, h, st, at)

        rv = renpy.display.render.Render(w, h, opaque=False)

        rv.operation = renpy.display.render.IMAGEDISSOLVE
        rv.operation_alpha = 1.0
        rv.operation_complete = 256.0 / (256.0 + 256.0)
        rv.operation_parameter = 256

        rv.blit(mr, (0, 0), focus=False, main=False)
        rv.blit(nr, (0, 0), focus=False, main=False)
        rv.blit(cr, (0, 0))

        return rv
