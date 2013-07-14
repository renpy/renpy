# Copyright 2004-2013 Tom Rothamel <pytom@bishoujo.us>
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

# NOTE:
# Transitions need to be able to work even when old_widget and new_widget
# are None, at least to the point of making it through __init__. This is
# so that prediction of images works.

import renpy.display
from renpy.display.render import render


class Transition(renpy.display.core.Displayable):
    """
    This is the base class of most transitions. It takes care of event
    dispatching.
    """

    def __init__(self, delay, **properties):
        super(Transition, self).__init__(**properties)
        self.delay = delay
        self.events = True

    def event(self, ev, x, y, st):

        if self.events or ev.type == renpy.display.core.TIMEEVENT:
            return self.new_widget.event(ev, x, y, st) # E1101
        else:
            return None

    def visit(self):
        return [ self.new_widget, self.old_widget ] # E1101


def null_render(d, width, height, st, at):

    d.events = True
    surf = renpy.display.render.render(d.new_widget,
                                       width,
                                       height,
                                       st, at)

    rv = renpy.display.render.Render(surf.width, surf.height)
    rv.blit(surf, (0, 0))

    return rv

class NoTransition(Transition):
    """
    :doc: transition function
    :args: (delay)

    Returns a transition that only displays the new screen for `delay` seconds.
    It can be useful as part of a MultipleTransition.
    """

    def __init__(self, delay, old_widget=None, new_widget=None, **properties):
        super(NoTransition, self).__init__(delay, **properties)

        self.old_widget = old_widget
        self.new_widget = new_widget
        self.events = True

    def render(self, width, height, st, at):
        return null_render(self, width, height, st, at)


class MultipleTransition(Transition):
    """
    :doc: transition function
    :args: (args)

    Returns a transition that allows multiple transitions to be displayed, one
    after the other.

    `args`
        A list containing an odd number of items. The first, third, and
        other odd-numbered items must be scenes, and the even items
        must be transitions. A scene can be one of:

        * A displayable.
        * False, to use the old scene.
        * True, to use the new scene.

        Almost always, the first argument will be False and the last True.

    The transitions in `args` are applied in order. For each transition,
    the old scene is the screen preceding it, and the new scene is the
    scene following it. For example::

        define logodissolve = MultipleTransition(
            False, Dissolve(0.5)
            "logo.jpg", NoTransition(1.0),
            "logo.jpg", dissolve,
            True)

    This example will dissolve to logo.jpg, wait 1 second, and then
    dissolve to the new scene.
    """

    def __init__(self, args, old_widget=None, new_widget=None, **properties):

        if len(args) % 2 != 1 or len(args) < 3:
            raise Exception("MultipleTransition requires an odd number of arguments, and at least 3 arguments.")

        self.transitions = [ ]

        # The screens that we use for the transition.
        self.screens = [ renpy.easy.displayable(i) for i in args[0::2] ]

        def oldnew(w):
            if w is False:
                return old_widget
            if w is True:
                return new_widget

            return w

        for old, trans, new in zip(self.screens[0:], args[1::2], self.screens[1:]):
            old = oldnew(old)
            new = oldnew(new)

            self.transitions.append(trans(old_widget=old, new_widget=new))

        super(MultipleTransition, self).__init__(sum([i.delay for i in self.transitions]), **properties)

        self.new_widget = self.transitions[-1]
        self.events = False

    def visit(self):
        return [ i for i in self.screens if isinstance(i, renpy.display.core.Displayable)] + self.transitions

    def event(self, ev, x, y, st):

        if self.events or ev.type == renpy.display.core.TIMEEVENT:
            return self.transitions[-1].event(ev, x, y, st)
        else:
            return None

    def render(self, width, height, st, at):

        if renpy.game.less_updates:
            return null_render(self, width, height, st, at)

        for trans in self.transitions[:-1]:

            if trans.delay > st:
                break

            st -= trans.delay

        else:

            trans = self.transitions[-1]
            self.events = True

        if trans is not self.transitions[-1]:
            renpy.display.render.render(self.transitions[-1], width, height, 0, 0)

        surf = renpy.display.render.render(trans, width, height, st, at)
        width, height = surf.get_size()
        rv = renpy.display.render.Render(width, height)
        rv.blit(surf, (0, 0))

        if st < trans.delay:
            renpy.display.render.redraw(self, trans.delay - st)

        return rv


def Fade(out_time,
         hold_time,
         in_time,
         old_widget=None,
         new_widget=None,
         color=None,
         widget=None,
         alpha=False,
         ):

    """
    :doc: transition function
    :args: (out_time, hold_time, in_time, color="#000")
    :name: Fade

    Returns a transition that takes `out_time` seconds to fade to
    a screen filled with `color`, holds at that screen for `hold_time`
    seconds, and then takes `in_time` to fade to then new screen.

    ::

        # Fade to black and back.
        define fade = Fade(0.5, 0.0, 0.5)

        # Hold at black for a bit.
        define fadehold = Fade(0.5, 1.0, 0.5)

        # Camera flash - quickly fades to white, then back to the scene.
        define flash = Fade(0.1, 0.0, 0.5, color="#fff")
    """

    dissolve = renpy.curry.curry(Dissolve)
    notrans = renpy.curry.curry(NoTransition)

    widget = renpy.easy.displayable_or_none(widget)

    if color:
        widget = renpy.display.image.Solid(color)

    if not widget:
        widget = renpy.display.image.Solid((0, 0, 0, 255))

    args = [ False, dissolve(out_time, alpha=alpha), widget ]

    if hold_time:
        args.extend([ notrans(hold_time), widget, ])

    args.extend([dissolve(in_time, alpha=alpha), True ])

    return MultipleTransition(args, old_widget=old_widget, new_widget=new_widget)


class Pixellate(Transition):
    """
    :doc: transition function
    :args: (time, steps)
    :name: Pixellate

    Returns a transition that pixellates out the old screen, and then
    pixellates in the new screen.

    `time`
        The total time the transition will take, in seconds.

    `steps`
        The number of steps that will occur, in each direction. Each step
        creates pixels about twice the size of those in the previous step,
        so a 5-step pixellation will create 32x32 pixels.
    """

    def __init__(self, time, steps, old_widget=None, new_widget=None, **properties):

        time = float(time)

        super(Pixellate, self).__init__(time, **properties)

        self.time = time
        self.steps = steps

        self.old_widget = old_widget
        self.new_widget = new_widget

        self.events = False

        self.quantum = time / (2 * steps)

    def render(self, width, height, st, at):

        if renpy.game.less_updates:
            return null_render(self, width, height, st, at)

        if st >= self.time:
            self.events = True
            return render(self.new_widget, width, height, st, at)

        step = st // self.quantum + 1
        visible = self.old_widget

        if step > self.steps:
            step = (self.steps * 2) - step + 1
            visible = self.new_widget
            self.events = True


        rdr = render(visible, width, height, st, at)
        rv = renpy.display.render.Render(rdr.width, rdr.height)

        rv.blit(rdr, (0, 0))

        rv.operation = renpy.display.render.PIXELLATE
        rv.operation_parameter = 2 ** step

        renpy.display.render.redraw(self, 0)

        return rv


class Dissolve(Transition):
    """
    :doc: transition function
    :args: (time, alpha=False, time_warp=None)
    :name: Dissolve

    Returns a transition that dissolves from the old scene to the new scene.

    `time`
        The time the dissolve will take.

    `alpha`
        If true, the dissolve will alpha-composite the the result of the
        transition with the screen. If false, the result of the transition
        will replace the screen, which is more efficient.

    `time_warp`
        A function that adjusts the timeline. If not None, this should be a
        function that takes a fractional time between 0.0 and 1.0, and returns
        a number in the same range.
    """

    __version__ = 1

    def after_upgrade(self, version):
        if version < 1:
            self.alpha = False

    time_warp = None

    def __init__(self, time, old_widget=None, new_widget=None, alpha=False, time_warp=None, **properties):
        super(Dissolve, self).__init__(time, **properties)

        self.time = time
        self.old_widget = old_widget
        self.new_widget = new_widget
        self.events = False
        self.alpha = alpha
        self.time_warp = time_warp


    def render(self, width, height, st, at):

        if renpy.game.less_updates:
            return null_render(self, width, height, st, at)

        if st >= self.time:
            self.events = True
            return render(self.new_widget, width, height, st, at)

        complete = min(1.0, st / self.time)

        if self.time_warp is not None:
            complete = self.time_warp(complete)

        bottom = render(self.old_widget, width, height, st, at)
        top = render(self.new_widget, width, height, st, at)

        width = min(top.width, bottom.width)
        height = min(top.height, bottom.height)

        rv = renpy.display.render.Render(width, height, opaque=not self.alpha)

        rv.operation = renpy.display.render.DISSOLVE
        rv.operation_alpha = self.alpha
        rv.operation_complete = complete

        rv.blit(bottom, (0, 0), focus=False, main=False)
        rv.blit(top, (0, 0), focus=True, main=True)

        renpy.display.render.redraw(self, 0)

        return rv


class ImageDissolve(Transition):
    """
    :doc: transition function
    :args: (image, time, ramplen=8, reverse=False, alpha=True, time_warp=None)
    :name: ImageDissolve

    Returns a transition that dissolves the old scene into the new scene, using
    an image to control the dissolve process. This means that white pixels will
    dissolve in first, and black pixels will dissolve in last.

    `image`
        A control image to use. This must be either an image file or
        image manipulator. The control image should be the size of
        the scenes being dissolved.

    `time`
        The time the dissolve will take.

    `ramplen`
        The length of the ramp to use. This must be an integer power
        of 2. When this is the default value of 8, when a white pixel
        is fully dissolved, a pixel 8 shades of gray darker will have
        completed one step of dissolving in.

    `reverse`
        If true, black pixels will dissolve in before white pixels.

    `alpha`
        If true, the dissolve will alpha-composite the the result of the
        transition with the screen. If false, the result of the transition
        will replace the screen, which is more efficient.

    `time_warp`
        A function that adjusts the timeline. If not None, this should be a
        function that takes a fractional time between 0.0 and 1.0, and returns
        a number in the same range.

    ::

        define circirisout = ImageDissolve("circiris.png", 1.0)
        define circirisin = ImageDissolve("circiris.png", 1.0, reverse=True)
        define circiristbigramp = ImageDissolve("circiris.png", 1.0, ramplen=256)
    """

    __version__ = 1

    def after_upgrade(self, version):
        if version < 1:
            self.alpha = False

    time_warp = None

    def __init__(
        self,
        image,
        time,
        ramplen=8,
        ramptype='linear',
        ramp=None,
        reverse=False,
        alpha=False,
        old_widget=None,
        new_widget=None,
        time_warp=None,
        **properties):

        # ramptype and ramp are now unused, but are kept for compatbility with
        # older code.

        super(ImageDissolve, self).__init__(time, **properties)

        self.old_widget = old_widget
        self.new_widget = new_widget
        self.events = False
        self.alpha = alpha
        self.time_warp = time_warp

        if not reverse:

            # Copies red -> alpha
            matrix = renpy.display.im.matrix(
                0, 0, 0, 0, 1,
                0, 0, 0, 0, 1,
                0, 0, 0, 0, 1,
                1, 0, 0, 0, 0)

        else:

            # Copies 1-red -> alpha
            matrix = renpy.display.im.matrix(
                0, 0, 0, 0, 1,
                0, 0, 0, 0, 1,
                0, 0, 0, 0, 1,
                - 1, 0, 0, 0, 1)

        self.image = renpy.display.im.MatrixColor(image, matrix)

        if ramp is not None:
            ramplen = len(ramp)

        # The length of the ramp.
        self.ramplen = max(ramplen, 1)


    def visit(self):
        return super(ImageDissolve, self).visit() + [ self.image ]


    def render(self, width, height, st, at):

        if renpy.game.less_updates or renpy.display.less_imagedissolve:
            return null_render(self, width, height, st, at)

        if st >= self.delay:
            self.events = True
            return render(self.new_widget, width, height, st, at)

        image = render(self.image, width, height, st, at)
        bottom = render(self.old_widget, width, height, st, at)
        top = render(self.new_widget, width, height, st, at)

        width = min(bottom.width, top.width, image.width)
        height = min(bottom.height, top.height, image.height)

        rv = renpy.display.render.Render(width, height, opaque=not self.alpha)

        complete = st / self.delay

        if self.time_warp is not None:
            complete = self.time_warp(complete)

        rv.operation = renpy.display.render.IMAGEDISSOLVE
        rv.operation_alpha = self.alpha
        rv.operation_complete = complete
        rv.operation_parameter = self.ramplen

        rv.blit(image, (0, 0), focus=False, main=False)
        rv.blit(bottom, (0, 0), focus=False, main=False)
        rv.blit(top, (0, 0), focus=True, main=True)

        renpy.display.render.redraw(self, 0)

        return rv


class AlphaDissolve(Transition):
    """
    :doc: transition function
    :args: (control, delay=0.0, alpha=False, reverse=False)

    Returns a transition that uses a control displayable (almost always some
    sort of animated transform) to transition from one screen to another. The
    transform is evaluated. The new screen is used where the transform is
    opaque, and the old image is used when it is transparent.

    `control`
        The control transform.

    `delay`
        The time the transition takes, before ending.

    `alpha`
        If true, the image is composited with what's behind it. If false,
        the default, the image is opaque and overwrites what's behind it.

    `reverse`
        If true, the alpha channel is reversed. Opaque areas are taken
        from the old image, while transparent areas are taken from the
        new image.
     """

    def __init__(
        self,
        control,
        delay=0.0,
        old_widget=None,
        new_widget=None,
        alpha=False,
        reverse=False,
        **properties):

        super(AlphaDissolve, self).__init__(delay, **properties)

        self.control = renpy.display.layout.Fixed()
        self.control.add(control)

        self.old_widget = renpy.easy.displayable(old_widget)
        self.new_widget = renpy.easy.displayable(new_widget)
        self.events = False

        self.alpha = alpha
        self.reverse = reverse

    def visit(self):
        return super(AlphaDissolve, self).visit() + [ self.control ]

    def render(self, width, height, st, at):

        if renpy.game.less_updates or renpy.display.less_imagedissolve:
            return null_render(self, width, height, st, at)

        if st >= self.delay:
            self.events = True

        bottom = render(self.old_widget, width, height, st, at)
        top = render(self.new_widget, width, height, st, at)

        width = min(bottom.width, top.width)
        height = min(bottom.height, top.height)

        control = render(self.control, width, height, st, at)

        rv = renpy.display.render.Render(width, height, opaque=not self.alpha)

        rv.operation = renpy.display.render.IMAGEDISSOLVE
        rv.operation_alpha = self.alpha
        rv.operation_complete = 256.0 / (256.0 + 256.0)
        rv.operation_parameter = 256

        rv.blit(control, (0, 0), focus=False, main=False)

        if not self.reverse:
            rv.blit(bottom, (0, 0), focus=False, main=False)
            rv.blit(top, (0, 0), focus=True, main=True)
        else:
            rv.blit(top, (0, 0), focus=True, main=True)
            rv.blit(bottom, (0, 0), focus=False, main=False)

        return rv


class CropMove(Transition):
    """
    :doc: transition function
    :args: (time, mode="slideright", startcrop=(0.0, 0.0, 0.0, 1.0), startpos=(0.0, 0.0), endcrop=(0.0, 0.0, 1.0, 1.0), endpos=(0.0, 0.0), topnew=True)
    :name: CropMove

    Returns a transition that works by cropping a scene and positioning it on the
    screen. This can be used to implement a variety of effects, all of which
    involved changing rectangular slices of scenes.

    `time`
        The time the transition takes.

    `mode`
        The name of the mode of the transition. There are three groups
        of modes: wipes, slides, and other. This can also be "custom",
        to allow a custom mode to be defined.

        In a wipe, the image stays fixed, and more of it is revealed as
        the transition progresses. For example, in "wiperight", a wipe from left to right, first the left edge of the image is
        revealed at the left edge of the screen, then the center of the image,
        and finally the right side of the image at the right of the screen.
        Other supported wipes are "wipeleft", "wipedown", and "wipeup".

        In a slide, the image moves. So in a "slideright", the right edge of the
        image starts at the left edge of the screen, and moves to the right
        as the transition progresses. Other slides are "slideleft", "slidedown",
        and "slideup".

        There are also slideaways, in which the old image moves on top of
        the new image. Slideaways include "slideawayright", "slideawayleft",
        "slideawayup", and "slideawaydown".

        We also support a rectangular iris in with "irisin" and a
        rectangular iris out with "irisout".

    The following parameters are only respected if the mode is "custom". Positions
    are relative to the size of the screen, while the crops are relative to the
    size of the image. So a crop of (0.25, 0.0, 0.5, 1.0) takes the middle
    half of an image.

    `startcrop`
        The starting rectangle that is cropped out of the
        top image. A 4-element tuple containing x, y, width, and height.

    `startpos`
        The starting place that the top image is drawn
        to the screen at, a 2-element tuple containing x and y.

    `endcrop`
        The ending rectangle that is cropped out of the
        top image. A 4-element tuple containing x, y, width, and height.

    `endpos`
        The ending place that the top image is drawn
        to the screen at, a 2-element tuple containing x and y.

    `topnew`
        If true, the scene that is cropped and moved (and is on top of
        the other scene) is the new scene. If false, it is the old scene.

    ::

        define wiperight = CropMove(1.0, "wiperight")
        define wipeleft = CropMove(1.0, "wipeleft")
        define wipeup = CropMove(1.0, "wipeup")
        define wipedown = CropMove(1.0, "wipedown")

        define slideright = CropMove(1.0, "slideright")
        define slideleft = CropMove(1.0, "slideleft")
        define slideup = CropMove(1.0, "slideup")
        define slidedown = CropMove(1.0, "slidedown")

        define slideawayright = CropMove(1.0, "slideawayright")
        define slideawayleft = CropMove(1.0, "slideawayleft")
        define slideawayup = CropMove(1.0, "slideawayup")
        define slideawaydown = CropMove(1.0, "slideawaydown")

        define irisout = CropMove(1.0, "irisout")
        define irisin = CropMove(1.0, "irisin")
    """

    def __init__(self, time,
                 mode="slideright",
                 startcrop=(0.0, 0.0, 0.0, 1.0),
                 startpos=(0.0, 0.0),
                 endcrop=(0.0, 0.0, 1.0, 1.0),
                 endpos=(0.0, 0.0),
                 topnew=True,
                 old_widget=None,
                 new_widget=None,
                 **properties):

        super(CropMove, self).__init__(time, **properties)
        self.time = time

        if mode == "wiperight":
            startpos = (0.0, 0.0)
            startcrop = (0.0, 0.0, 0.0, 1.0)
            endpos = (0.0, 0.0)
            endcrop = (0.0, 0.0, 1.0, 1.0)
            topnew = True

        elif mode == "wipeleft":
            startpos = (1.0, 0.0)
            startcrop = (1.0, 0.0, 0.0, 1.0)
            endpos = (0.0, 0.0)
            endcrop = (0.0, 0.0, 1.0, 1.0)
            topnew = True

        elif mode == "wipedown":
            startpos = (0.0, 0.0)
            startcrop = (0.0, 0.0, 1.0, 0.0)
            endpos = (0.0, 0.0)
            endcrop = (0.0, 0.0, 1.0, 1.0)
            topnew = True

        elif mode == "wipeup":
            startpos = (0.0, 1.0)
            startcrop = (0.0, 1.0, 1.0, 0.0)
            endpos = (0.0, 0.0)
            endcrop = (0.0, 0.0, 1.0, 1.0)
            topnew = True

        elif mode == "slideright":
            startpos = (0.0, 0.0)
            startcrop = (1.0, 0.0, 0.0, 1.0)
            endpos = (0.0, 0.0)
            endcrop = (0.0, 0.0, 1.0, 1.0)
            topnew = True

        elif mode == "slideleft":
            startpos = (1.0, 0.0)
            startcrop = (0.0, 0.0, 0.0, 1.0)
            endpos = (0.0, 0.0)
            endcrop = (0.0, 0.0, 1.0, 1.0)
            topnew = True

        elif mode == "slideup":
            startpos = (0.0, 1.0)
            startcrop = (0.0, 0.0, 1.0, 0.0)
            endpos = (0.0, 0.0)
            endcrop = (0.0, 0.0, 1.0, 1.0)
            topnew = True

        elif mode == "slidedown":
            startpos = (0.0, 0.0)
            startcrop = (0.0, 1.0, 1.0, 0.0)
            endpos = (0.0, 0.0)
            endcrop = (0.0, 0.0, 1.0, 1.0)
            topnew = True

        elif mode == "slideawayleft":
            endpos = (0.0, 0.0)
            endcrop = (1.0, 0.0, 0.0, 1.0)
            startpos = (0.0, 0.0)
            startcrop = (0.0, 0.0, 1.0, 1.0)
            topnew = False

        elif mode == "slideawayright":
            endpos = (1.0, 0.0)
            endcrop = (0.0, 0.0, 0.0, 1.0)
            startpos = (0.0, 0.0)
            startcrop = (0.0, 0.0, 1.0, 1.0)
            topnew = False

        elif mode == "slideawaydown":
            endpos = (0.0, 1.0)
            endcrop = (0.0, 0.0, 1.0, 0.0)
            startpos = (0.0, 0.0)
            startcrop = (0.0, 0.0, 1.0, 1.0)
            topnew = False

        elif mode == "slideawayup":
            endpos = (0.0, 0.0)
            endcrop = (0.0, 1.0, 1.0, 0.0)
            startpos = (0.0, 0.0)
            startcrop = (0.0, 0.0, 1.0, 1.0)
            topnew = False

        elif mode == "irisout":
            startpos = (0.5, 0.5)
            startcrop = (0.5, 0.5, 0.0, 0.0)
            endpos = (0.0, 0.0)
            endcrop = (0.0, 0.0, 1.0, 1.0)
            topnew = True

        elif mode == "irisin":
            startpos = (0.0, 0.0)
            startcrop = (0.0, 0.0, 1.0, 1.0)
            endpos = (0.5, 0.5)
            endcrop = (0.5, 0.5, 0.0, 0.0)
            topnew = False


        elif mode == "custom":
            pass
        else:
            raise Exception("Invalid mode %s passed into CropMove." % mode)

        self.delay = time
        self.time = time

        self.startpos = startpos
        self.endpos = endpos

        self.startcrop = startcrop
        self.endcrop = endcrop

        self.topnew = topnew

        self.old_widget = old_widget
        self.new_widget = new_widget

        self.events = False

        if topnew:
            self.bottom = old_widget
            self.top = new_widget
        else:
            self.bottom = new_widget
            self.top = old_widget

    def render(self, width, height, st, at):

        if renpy.game.less_updates:
            return null_render(self, width, height, st, at)

        time = 1.0 * st / self.time

        # Done rendering.
        if time >= 1.0:
            self.events = True
            return render(self.new_widget, width, height, st, at)

        # How we scale each element of a tuple.
        scales = (width, height, width, height)

        def interpolate_tuple(t0, t1):
            return tuple([ int(s * (a * (1.0 - time) + b * time))
                           for a, b, s in zip(t0, t1, scales) ])

        crop = interpolate_tuple(self.startcrop, self.endcrop)
        pos = interpolate_tuple(self.startpos, self.endpos)


        top = render(self.top, width, height, st, at)
        bottom = render(self.bottom, width, height, st, at)

        width = min(bottom.width, width)
        height = min(bottom.height, height)
        rv = renpy.display.render.Render(width, height)

        rv.blit(bottom, (0, 0), focus=not self.topnew)

        ss = top.subsurface(crop, focus=self.topnew)
        rv.blit(ss, pos, focus=self.topnew)

        renpy.display.render.redraw(self, 0)
        return rv


def ComposeTransition(trans, before=None, after=None, new_widget=None, old_widget=None):
    """
    :doc: transition function
    :args: (trans, before, after)

    Returns a transition that composes up to three transitions. If not None,
    the `before` and `after` transitions are applied to the old and new
    scenes, respectively. These updated old and new scenes are then supplied
    to the `trans` transition.

    ::

        # Move the images in and out while dissolving. (This is a fairly expensive transition.)
        define moveinoutdissolve = ComposeTransition(dissolve, before=moveoutleft, after=moveinright)
    """

    if before is not None:
        old = before(new_widget=new_widget, old_widget=old_widget)
    else:
        old = old_widget

    if after is not None:
        new = after(new_widget=new_widget, old_widget=old_widget)
    else:
        new = new_widget

    return trans(new_widget=new, old_widget=old)


def SubTransition(rect, trans, old_widget=None, new_widget=None, **properties):
    """
    Applies a transition to a subset of the screen. Not documented.
    """

    x, y, _w, _h = rect

    old = renpy.display.layout.LiveCrop(rect, old_widget)
    new = renpy.display.layout.LiveCrop(rect, new_widget)

    inner = trans(old_widget=old, new_widget=new)
    delay = inner.delay
    inner = renpy.display.layout.Position(inner, xpos=x, ypos=y, xanchor=0, yanchor=0)

    f = renpy.display.layout.MultiBox(layout='fixed')
    f.add(new_widget)
    f.add(inner)

    return NoTransition(delay, old_widget=f, new_widget=f)

