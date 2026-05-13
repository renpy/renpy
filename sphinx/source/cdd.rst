.. _udd:
.. _cdd:

============================
Creator-Defined Displayables
============================

The most complex, but most powerful, way of customizing Ren'Py's
behavior is to use a creator-defined displayable. A creator-defined
displayable is allowed to take arbitrary pygame events. It can
also render other displayables, and place them at arbitrary locations
on the screen. This makes it suitable for creating 2D mini-games that
cannot be expressed with the tools Ren'Py gives you. (But see also the
section :doc:`sprites <sprites>`, which describes a higher-level way
of accomplishing many of the same things.)

Creator-defined displayables are programmed entirely in Python, and we
encourage you to have a reasonable degree of skill at object-oriented
Python programming before you begin creating one.

Example
=======

Here's an example of a creator-defined displayable. This displayable
changes renders its child with an alpha that is determined by the
distance of the mouse pointer from the center of the child. ::

    init python:

        import math

        class Appearing(renpy.Displayable):

            def __init__(self, child, opaque_distance, transparent_distance, **kwargs):

                # Pass additional properties on to the renpy.Displayable
                # constructor.
                super(Appearing, self).__init__(**kwargs)

                # The child.
                self.child = renpy.displayable(child)

                # The distance at which the child will become fully opaque, and
                # where it will become fully transparent. The former must be less
                # than the latter.
                self.opaque_distance = opaque_distance
                self.transparent_distance = transparent_distance

                # The alpha channel of the child.
                self.alpha = 0.0

                # The width and height of us, and our child.
                self.width = 0
                self.height = 0

            def render(self, width, height, st, at):

                # Create a transform, that can adjust the alpha channel of the
                # child.
                t = Transform(child=self.child, alpha=self.alpha)

                # Create a render from the child.
                child_render = renpy.render(t, width, height, st, at)

                # Get the size of the child.
                self.width, self.height = child_render.get_size()

                # Create the render we will return.
                render = renpy.Render(self.width, self.height)

                # Blit (draw) the child's render to our render.
                render.blit(child_render, (0, 0))

                # Return the render.
                return render

            def event(self, ev, x, y, st):

                # Compute the distance between the center of this displayable and
                # the mouse pointer. The mouse pointer is supplied in x and y,
                # relative to the upper-left corner of the displayable.
                distance = math.hypot(x - (self.width / 2), y - (self.height / 2))

                # Base on the distance, figure out an alpha.
                if distance <= self.opaque_distance:
                    alpha = 1.0
                elif distance >= self.transparent_distance:
                    alpha = 0.0
                else:
                    alpha = 1.0 - 1.0 * (distance - self.opaque_distance) / (self.transparent_distance - self.opaque_distance)

                # If the alpha has changed, trigger a redraw event.
                if alpha != self.alpha:
                    self.alpha = alpha
                    renpy.redraw(self, 0)

                # Pass the event to our child.
                return self.child.event(ev, x, y, st)

            def visit(self):
                return [ self.child ]

To use the creator-defined displayable, we can create an instance of it,
and add that instance to the screen. ::

    screen alpha_magic:
        add Appearing("logo.png", 100, 200):
            xalign 0.5
            yalign 0.5

    label start:
        show screen alpha_magic

        "Can you find the logo?"

        return


renpy.Displayable
=================

A creator-defined displayable is created by subclassing the
renpy.Displayable class. A creator-defined displayable must override
the render method, and may override other methods as well.

A displayable object must be pickleable, which means it may not
contain references to objects that cannot be pickled. Most notably,
Render objects cannot be stored in a creator-defined displayable.

Since we expect you to override the methods of the displayable
class, we'll present them with the `self` parameter.

.. class:: renpy.Displayable

    Base class for creator-defined displayables.

    .. method:: __init__(**properties)

        A subclass may override the constructor, perhaps adding new
        parameters. If it does, it should pass all unknown keyword
        arguments to the renpy.Displayable constructor, with the
        call::

            super(MyDisplayable, self).__init__(**properties)

    .. method:: render(self, width, height, st, at)

        Subclasses must override this, to return a :class:`renpy.Render`
        object. The render object determines what, if anything, is
        shown on the screen.

        `width`, `height`
            The amount of space available to this displayable, in
            pixels.

        `st`
            A float, the shown timebase, in seconds. The shown
            timebase begins when this displayable is first shown
            on the screen.

        `at`
            A float, the animation timebase, in seconds. The animation
            timebase begins when an image with the same tag was shown,
            without being hidden. (When the displayable is shown
            without a tag, this is the same as the shown timebase.)

        The render method is called when the displayable is first
        shown. It can be called again if :func:`renpy.redraw`
        is called on this object.

    .. method:: event(self, ev, x, y, st)

        The event method is called to pass a pygame event to
        the creator-defined displayable. If the event method returns
        a value other than None, that value is returned as the result
        of the interaction. If the event method returns None, the event
        is passed on to other displayables.

        To ignore the event without returning None, raise :exc:`renpy.IgnoreEvent`.

        The event method exists on other displayables, allowing the
        creator-defined displayable to pass on the event.

        `ev`
            An `event object <http://www.pygame.org/docs/ref/event.html>`_

        `x`, `y`
            The x and y coordinates of the event, relative to the
            upper-left corner of the displayable. These should
            be used in preference to position information
            found in the pygame event objects.

        `st`
            A float, the shown timebase, in seconds.

        An event is generated at the start of each interaction, and
        :func:`renpy.timeout` can be used to cause another event to
        occur.

    .. method:: per_interact(self)

        This method is called at the start of each interaction. It
        can be used to trigger a redraw, and probably should be used
        to trigger a redraw if the object participates in rollback.

    .. method:: visit(self)

        If the displayable has child displayables, this method should
        be overridden to return a list of those displayables. This
        ensures that the per_interact methods of those displayables
        are called, and also allows images used by those displayables
        to be predicted.

    .. method:: place(self, dest, x, y, width, height, surf, main=True)

        This places a render (which must be of this displayable)
        within a bounding area. Returns an (x, y) tuple giving the location
        the displayable was placed at.

        `dest`
            If not None, the `surf` will be blitted to `dest` at the
            computed coordinates.

        `x`, `y`, `width`, `height`
            The bounding area.

        `surf`
            The render to place.

        `main`
            This is passed to Render.blit().

renpy.Render
============

Creator-defined displayables work with renpy.Render objects. Render
objects are returned by calling the :func:`renpy.render` function on a
displayable. A creator-defined displayable should create a Render object
by calling :class:`renpy.Render` from its render method.

Since the render object isn't intended to be subclassed, we will omit
the implicit `self` parameter.

.. class:: renpy.Render(width, height)

    Creates a new Render object.

    `width`, `height`
        The width and height of the render object, in pixels.


    .. method:: blit(source, pos, main=True)

        Draws another render object into this render object.

        `source`
            The render object to draw.

        `pos`
            The location to draw into. This is an (x, y) tuple
            with the coordinates being pixels relative to the
            upper-left corner of the target render.

        `main`
            A keyword-only parameter. If true, `source` will be displayed
            in the style inspector.

    .. method:: place(d, x=0, y=0, width=None, height=None, st=None, at=None, render=None, main=True)

        Renders `d`, a displayable, and places it into the rectangle defined by the `x`, `y`,
        `width`, and `height`, using Ren'Py's standard placement algorithm.
        Returns an (x, y) tuple giving the location
        the displayable was placed at. Location is computed
        by calling Displayable.place() method.

        `x`, `y`, `width`, `height`
            The rectangle to place in. If `width` or `height`, when None,
            are the width and height of this render, respectively.

        `st`, `at`
            The times passed to Render. If None, defaults to the times
            passed to the render method calling this method.

        `render`
            If not None, this is used instead of rendering `d`.

        `main`
            As for .blit().

    .. method:: canvas()

       Returns a canvas object. A canvas object has methods
       corresponding to the
       `pygame.draw <http://www.pygame.org/docs/ref/draw.html>`_
       functions, with the first parameter (the surface) omitted.

       In Ren'Py, the arc and ellipse functions aren't implemented.

       Canvas objects also have a get_surface() method that returns the
       pygame Surface underlying the canvas.

    .. method:: get_size()

        Returns a (width, height) tuple giving the size of
        this render.

    .. method:: subsurface(rect)

        Returns a render consisting of a rectangle cut out of this
        render.

        `rect`
            A (x, y, width, height) tuple.

    .. method:: zoom(xzoom, yzoom)

        Sets the zoom level of the children of this displayable in the
        horizontal and vertical axes. Only the children of the displayable
        are zoomed – the width, height, and blit coordinates are not zoomed.

    The following attributes and methods are only used when model-based rendering
    is enabled:

    .. attribute:: mesh

        This field enables model-based rendering for this Render. If true:

        If set to True:

        * All of the children of this displayable are rendered to textures.
        * A mesh the size of the first child is associated with this displayable.
        * A model is created with the mesh, shaders, uniforms, and properties
          associated with this Render.

        The model will then be drawn in a single operation.

    .. method:: add_shader(shader)

        This causes the shader part `shader` to be used when this Render
        or its children are drawn. The part should be a string, or can be a
        string beginning with "-" to prevent a shader from being drawn.

    .. method:: add_uniform(name, value)

        Causes the uniform `name` to have `value` when this Render or
        its children are drawn.

    .. method:: add_property(name, value)

        Causes the GL property `name` to have `value` when this Render or
        one of its children are drawn.



Utility Functions and Classes
=============================

.. include:: inc/udd_utility

.. function:: renpy.redraw(d, when)

    Causes the displayable `d` to be redrawn (the render method called)
    when `when` seconds have elapsed. The displayable may be redrawn before
    that time (for example, when a child is redrawn), in which case a pending
    redraw is forgotten.

.. exception:: renpy.IgnoreEvent

    This is an exception that, if raised, causes Ren'Py to ignore the
    event. To raise this inside the event method, write::

        raise renpy.IgnoreEvent()
