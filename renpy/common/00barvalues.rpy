# Copyright 2004-2013 Tom Rothamel <pytom@bishoujo.us>
# See LICENSE.txt for license details.

init -1500 python:

    class StaticValue(BarValue):
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

    class AnimatedValue(BarValue):
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

    class FieldValue(BarValue):
        """
         :doc: value

         A value that allows the user to adjust the value of a field
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
         """

        offset = 0

        def __init__(self, object, field, range, max_is_zero=False, style="bar", offset=0, step=None):
            self.object = object
            self.field = field
            self.range = range
            self.max_is_zero = max_is_zero
            self.style = style
            self.offset = offset

            if step is None:
                if isinstance(range, float):
                    step = range / 10.0
                else:
                    step = max(range / 10, 1)

            self.step = step

        def changed(self, value):

            if self.max_is_zero:
                if value == self.range:
                    value = 0
                else:
                    value = value + 1

            value += self.offset

            setattr(self.object, self.field, value)
            renpy.restart_interaction()

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
                step=self.step)

        def get_style(self):
            return self.style, "v" + self.style

    def VariableValue(variable, range, max_is_zero=False, style="bar", offset=0, step=None):
        """
         :doc: value

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
        """

        return FieldValue(store, variable, range, max_is_zero=max_is_zero, style=style, offset=offset, step=step)

    class MixerValue(BarValue):
        """
         :doc: value

         The value of an audio mixer.

         `mixer`
             The name of the mixer to adjust. This is usually one of
             "music", "sfx", or "voice", but user code can create new
             mixers.
         """

        def __init__(self, mixer):
            self.mixer = mixer

        def set_mixer(self, value):
            _preferences.set_volume(self.mixer, value)

        def get_adjustment(self):
            return ui.adjustment(
                range=1.0,
                value=_preferences.get_volume(self.mixer),
                changed=self.set_mixer)

        def get_style(self):
            return "slider", "vslider"

    class XScrollValue(BarValue):
        """
         :doc: value

         The value of an adjustment that horizontally scrolls the the viewport with the
         given id, on the current screen. The viewport must be defined
         before a bar with this value is.
         """

        def __init__(self, viewport):
            self.viewport = viewport

        def get_adjustment(self):
            w = renpy.get_widget(None, self.viewport)
            if not isinstance(w, Viewport):
                raise Exception("The displayable with id %r is not declared, or not a viewport." % self.viewport)

            return w.xadjustment

        def get_style(self):
            return "scrollbar", "vscrollbar"

    class YScrollValue(BarValue):
        """
         :doc: value

         The value of an adjustment that vertically scrolls the the viewport with the
         given id, on the current screen. The viewport must be defined
         before a bar with this value is.
         """

        def __init__(self, viewport):
            self.viewport = viewport

        def get_adjustment(self):
            w = renpy.get_widget(None, self.viewport)
            if not isinstance(w, Viewport):
                raise Exception("The displayable with id %r is not declared, or not a viewport." % self.viewport)

            return w.yadjustment

        def get_style(self):
            return "scrollbar", "vscrollbar"
