# Copyright 2004-2021 Tom Rothamel <pytom@bishoujo.us>
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

init -1500 python:

    @renpy.pure
    class StaticValue(BarValue, DictEquality):
        """
         :doc: value

         This allows a value to be specified statically.

         `value`
              The value itself, a number.

         `range`
              The range of the value.
         """

        def __init__(self, value=0.0, range=1.0):
            self.value = value
            self.range = range

        def get_adjustment(self):
            return ui.adjustment(value=self.value, range=self.range, adjustable=False)

    @renpy.pure
    class AnimatedValue(BarValue, DictEquality):
        """
         :doc: value

         This animates a value, taking `delay` seconds to vary the value from
         `old_value` to `value`.

         `value`
             The value itself, a number.

         `range`
             The range of the value, a number.

         `delay`
             The time it takes to animate the value, in seconds. Defaults
             to 1.0.

         `old_value`
             The old value. If this is None, then the value is taken from the
             AnimatedValue we replaced, if any. Otherwise, it is initialized
             to `value`.
         """

        def __init__(self, value=0.0, range=1.0, delay=1.0, old_value=None):
            if old_value == None:
                old_value = value

            self.value = value
            self.range = range
            self.delay = delay
            self.old_value = old_value
            self.start_time = None

            self.adjustment = None

        def get_adjustment(self):
            self.adjustment = ui.adjustment(value=self.value, range=self.range, adjustable=False)
            return self.adjustment

        def periodic(self, st):

            if self.start_time is None:
                self.start_time = st

            if self.value == self.old_value:
                return

            fraction = (st - self.start_time) / self.delay
            fraction = min(1.0, fraction)

            value = self.old_value + fraction * (self.value - self.old_value)

            self.adjustment.change(value)

            if fraction != 1.0:
                return 0

        def replaces(self, other):

            if not isinstance(other, AnimatedValue):
                return

            if self.value == other.value:
                self.start_time = other.start_time
                self.old_value = other.old_value
            else:
                self.old_value = other.value
                self.start_time = None

    @renpy.pure
    class DictValue(BarValue, FieldEquality):
        """
         :doc: value

         A value that allows the user to adjust the value of a key
         in a dict.

         `dict`
             The dict.
         `key`
             The key.
         `range`
             The range to adjust over.
         `max_is_zero`
             If True, then when the value of a key is zero, the value of the
             bar will be range, and all other values will be shifted down by 1.
             This works both ways - when the bar is set to the maximum, the
             value of a key is set to 0.

         `style`
             The styles of the bar created.
         `offset`
             An offset to add to the value.
         `step`
             The amount to change the bar by. If None, defaults to 1/10th of
             the bar.
         `action`
             If not None, an action to call when the field has changed.
         """

        offset = 0
        action = None
        force_step = False

        identity_fields = [ 'dict' ]
        equality_fields = [ 'key', 'range', 'max_is_zero', 'style', 'offset', 'step', 'action', 'force_step' ]

        def __init__(self, dict, key, range, max_is_zero=False, style="bar", offset=0, step=None, action=None, force_step=False):
            self.dict = dict
            self.key = key
            self.range = range
            self.max_is_zero = max_is_zero
            self.style = style
            self.offset = offset
            self.force_step = force_step

            if step is None:
                if isinstance(range, float):
                    step = range / 10.0
                else:
                    step = max(range / 10, 1)

            self.step = step
            self.action = action

        def changed(self, value):

            if self.max_is_zero:
                if value == self.range:
                    value = 0
                else:
                    value = value + 1

            value += self.offset

            self.dict[self.key] = value
            renpy.restart_interaction()

            renpy.run(self.action)

        def get_adjustment(self):

            value = self.dict[self.key]

            value -= self.offset

            if self.max_is_zero:
                if value == 0:
                    value = self.range
                else:
                    value = value - 1

            return ui.adjustment(
                range=self.range,
                value=value,
                changed=self.changed,
                step=self.step,
                force_step=self.force_step,
            )

        def get_style(self):
            return self.style, "v" + self.style

    @renpy.pure
    class FieldValue(BarValue, FieldEquality):
        """
         :doc: value

         A bar value that allows the user to adjust the value of a field
         on an object.

         `object`
             The object.
         `field`
             The field, a string.
         `range`
             The range to adjust over.
         `max_is_zero`
             If True, then when the field is zero, the value of the
             bar will be range, and all other values will be shifted
             down by 1. This works both ways - when the bar is set to
             the maximum, the field is set to 0.

             This is used internally, for some preferences.
         `style`
             The styles of the bar created.
         `offset`
             An offset to add to the value.
         `step`
             The amount to change the bar by. If None, defaults to 1/10th of
             the bar.
         `action`
             If not None, an action to call when the field has changed.
         """

        offset = 0
        action = None
        force_step = False

        identity_fields = [ 'object', ]
        equality_fields = [ 'range', 'max_is_zero', 'style', 'offset', 'step', 'action', 'force_step' ]

        def __init__(self, object, field, range, max_is_zero=False, style="bar", offset=0, step=None, action=None, force_step=False):
            self.object = object
            self.field = field
            self.range = range
            self.max_is_zero = max_is_zero
            self.style = style
            self.offset = offset
            self.force_step = force_step

            if step is None:
                if isinstance(range, float):
                    step = range / 10.0
                else:
                    step = max(range / 10, 1)

            self.step = step
            self.action = action

        def changed(self, value):

            if self.max_is_zero:
                if value == self.range:
                    value = 0
                else:
                    value = value + 1

            value += self.offset

            setattr(self.object, self.field, value)
            renpy.restart_interaction()

            renpy.run(self.action)

        def get_adjustment(self):

            value = getattr(self.object, self.field)

            value -= self.offset

            if self.max_is_zero:
                if value == 0:
                    value = self.range
                else:
                    value = value - 1

            return ui.adjustment(
                range=self.range,
                value=value,
                changed=self.changed,
                step=self.step,
                force_step=self.force_step,
            )

        def get_style(self):
            return self.style, "v" + self.style

    @renpy.pure
    def VariableValue(variable, range, max_is_zero=False, style="bar", offset=0, step=None, action=None, force_step=False):
        """
         :doc: value

         A bar value that allows the user to adjust the value of a variable
         in the default store.

         `variable`
             A string giving the name of the variable to adjust.
         `range`
             The range to adjust over.
         `max_is_zero`
             If True, then when the field is zero, the value of the
             bar will be range, and all other values will be shifted
             down by 1. This works both ways - when the bar is set to
             the maximum, the field is set to 0.

             This is used internally, for some preferences.
         `style`
             The styles of the bar created.
         `offset`
             An offset to add to the value.
         `step`
             The amount to change the bar by. If None, defaults to 1/10th of
             the bar.
         `action`
             If not None, an action to call when the field has changed.
        """

        return FieldValue(store, variable, range, max_is_zero=max_is_zero, style=style, offset=offset, step=step, action=action, force_step=force_step)

    @renpy.pure
    class ScreenVariableValue(BarValue, FieldEquality):
        """
        :doc: value

        A bar value that adjusts the value of a variable in a screen.

        `variable`
            A string giving the name of the variable to adjust.
        `range`
            The range to adjust over.
        `max_is_zero`
            If True, then when the field is zero, the value of the
            bar will be range, and all other values will be shifted
            down by 1. This works both ways - when the bar is set to
            the maximum, the field is set to 0.

            This is used internally, for some preferences.
        `style`
            The styles of the bar created.
        `offset`
            An offset to add to the value.
        `step`
            The amount to change the bar by. If None, defaults to 1/10th of
            the bar.
        `action`
            If not None, an action to call when the field has changed.
         """

        action = None
        offset = 0
        force_step = False

        identity_fields = [  ]
        equality_fields = [ 'variable', 'max_is_zero', 'style', 'offset', 'step', 'action', 'force_step' ]

        def __init__(self, variable, range, max_is_zero=False, style="bar", offset=0, step=None, action=None, force_step=False):
            self.variable = variable
            self.range = range
            self.max_is_zero = max_is_zero
            self.style = style
            self.offset = offset
            self.force_step = force_step

            if step is None:
                if isinstance(range, float):
                    step = range / 10.0
                else:
                    step = max(range / 10, 1)

            self.step = step
            self.action = action

        def changed(self, value):

            cs = renpy.current_screen()

            if self.max_is_zero:
                if value == self.range:
                    value = 0
                else:
                    value = value + 1

            value += self.offset

            cs.scope[self.variable] = value
            renpy.restart_interaction()

            renpy.run(self.action)

        def get_adjustment(self):

            cs = renpy.current_screen()

            if (cs is None) or (self.variable not in cs.scope):
                raise Exception("{} is not defined in the {} screen.".format(self.variable, cs.screen_name))

            value = cs.scope[self.variable]

            value -= self.offset

            if self.max_is_zero:
                if value == 0:
                    value = self.range
                else:
                    value = value - 1

            return ui.adjustment(
                range=self.range,
                value=value,
                changed=self.changed,
                step=self.step,
                force_step=self.force_step,
            )

        def get_style(self):
            return self.style, "v" + self.style



    @renpy.pure
    class MixerValue(BarValue, DictEquality):
        """
         :doc: value

         The value of an audio mixer.

         `mixer`
             The name of the mixer to adjust. This is usually one of
             "music", "sfx", or "voice", but creators can create new
             mixers.
         """

        def __init__(self, mixer):
            self.mixer = mixer

        def set_mixer(self, value):
            _preferences.set_volume(self.mixer, value)
            renpy.restart_interaction()

        def get_adjustment(self):
            return ui.adjustment(
                range=1.0,
                value=_preferences.get_volume(self.mixer),
                changed=self.set_mixer)

        def get_style(self):
            return "slider", "vslider"

    class XScrollValue(BarValue, FieldEquality):
        """
         :doc: value

         The value of an adjustment that horizontally scrolls the viewport with the
         given id, on the current screen. The viewport must be defined before a bar
         with this value is.
         """

        equality_fields = [ 'viewport' ]

        def __init__(self, viewport):
            self.viewport = viewport

        def get_adjustment(self):
            w = renpy.get_widget(None, self.viewport)
            if not isinstance(w, Viewport):
                raise Exception("The displayable with id %r is not declared, or not a viewport." % self.viewport)

            return w.xadjustment

        def get_style(self):
            return "scrollbar", "vscrollbar"

    class YScrollValue(BarValue, FieldEquality):
        """
         :doc: value

         The value of an adjustment that vertically scrolls the viewport with the
         given id, on the current screen. The viewport must be defined before a bar
         with this value is.
         """

        equality_fields = [ 'viewport' ]

        def __init__(self, viewport):
            self.viewport = viewport

        def get_adjustment(self):

            w = renpy.get_widget(None, self.viewport)
            if not isinstance(w, Viewport):
                raise Exception("The displayable with id %r is not declared, or not a viewport." % self.viewport)

            return w.yadjustment

        def get_style(self):
            return "scrollbar", "vscrollbar"


    @renpy.pure
    class AudioPositionValue(BarValue, DictEquality):
        """
        :doc: value

        A value that shows the playback position of the audio file playing
        in `channel`.

        `update_interval`
            How often the value updates, in seconds.
        """

        def __init__(self, channel='music', update_interval=0.1):
            self.channel = channel
            self.update_interval = update_interval

            self.adjustment = None

        def get_pos_duration(self):
            pos = renpy.music.get_pos(self.channel) or 0.0
            duration = renpy.music.get_duration(self.channel) or 1.0

            return pos, duration

        def get_adjustment(self):
            pos, duration = self.get_pos_duration()
            self.adjustment = ui.adjustment(value=pos, range=duration, adjustable=False)
            return self.adjustment

        def periodic(self, st):

            pos, duration = self.get_pos_duration()
            self.adjustment.set_range(duration)
            self.adjustment.change(pos)

            return self.update_interval
