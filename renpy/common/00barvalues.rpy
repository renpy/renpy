# Copyright 2004-2024 Tom Rothamel <pytom@bishoujo.us>
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

    class __GenericValue(BarValue, FieldEquality):
        # pickle defaults
        offset = 0
        action = None
        force_step = False

        identity_fields = ()
        equality_fields = ('range', 'max_is_zero', 'style', 'offset', 'step', 'action', 'force_step')

        _max = max

        def __init__(self, range=None, max_is_zero=False, style="bar", offset=0, step=None, action=None, force_step=False, min=None, max=None):

            if max is not None and min is not None:
                range = max - min
                offset = min
            elif range is None:
                raise Exception("You must specify either range, or both max and min.")

            self.range = range
            self.max_is_zero = max_is_zero
            self.style = style
            self.offset = offset
            self.force_step = force_step
            if step is None:
                if isinstance(range, float):
                    step = range / 10.0
                else:
                    step = __GenericValue._max(range // 10, 1)
            self.step = step
            self.action = action

        def changed(self, value):

            if self.max_is_zero:
                if value == self.range:
                    value = 0
                else:
                    value = value + 1

            value += self.offset

            self.set_value(value)
            renpy.restart_interaction()

            return renpy.run(self.action)

        def get_adjustment(self):
            value = self.get_value()

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
    class DictValue(__GenericValue):
        """
        :doc: value
        :args: {args}

        A bar value that allows the user to adjust the value of a key in
        a dict, or of an element at a particular index in a list.

        `dict`
            The dict, or the list.
        `key`
            The key, or the index when using a list.
        """

        kind = "key or index"

        identity_fields = ('dict',)
        equality_fields = __GenericValue.equality_fields + ('key',)

        def __init__(self, dict, key, *args, **kwargs):
            self.dict = dict
            self.key = key
            super(DictValue, self).__init__(*args, **kwargs)

        def get_value(self):
            value = self.dict[self.key]

            return value

        def set_value(self, value):
            try:
                self.dict[self.key] = value
            except LookupError as e:
                raise Exception("The {!r} {} does not exist".format(self.key, self.kind)) # from e # PY3 only

    @renpy.pure
    class FieldValue(__GenericValue):
        """
        :doc: value
        :args: {args}

        A bar value that allows the user to adjust the value of a field
        on an object.

        `object`
            The object.
        `field`
            The field name, a string.
        """

        kind = "field"

        identity_fields = ('object',)
        equality_fields = __GenericValue.equality_fields + ("field",)

        def __init__(self, object, field, *args, **kwargs):
            self.object = object
            self.field = field
            super(FieldValue, self).__init__(*args, **kwargs)

        def get_value(self):
            value = _get_field(self.object, self.field, self.kind)

            return value

        def set_value(self, value):
            _set_field(self.object, self.field, value, self.kind)

    @renpy.pure
    class VariableValue(FieldValue):
        """
        :doc: value
        :args: {args}

        A bar value that allows the user to adjust the value of a variable in
        the default store.

        `variable`
            The `variable` parameter must be a string, and can be a simple
            name like "strength", or one with dots separating the variable
            from fields, like "hero.strength" or "persistent.show_cutscenes".
        """

        kind = "variable"

        def __init__(self, variable, *args, **kwargs):
            super(VariableValue, self).__init__(store, variable, *args, **kwargs)

    @renpy.pure
    class ScreenVariableValue(__GenericValue):
        """
        :doc: value
        :args: {args}

        A bar value that adjusts the value of a variable in a screen.

        In a ``use``\ d screen, this targets a variable in the context of
        the screen containing the ``use``\ d one(s). To target variables
        within a ``use``\ d screen, and only in that case, use
        :func:`LocalVariableValue` instead.

        `variable`
            A string giving the name of the variable to adjust.
        """

        kind = "screen variable" # not used in error messages, only in doc-gen

        identity_fields = ()
        equality_fields = __GenericValue.equality_fields + ('variable',)

        def __init__(self, variable, *args, **kwargs):
            self.variable = variable
            super(ScreenVariableValue, self).__init__(*args, **kwargs)

        def get_value(self):
            cs = renpy.current_screen()

            if cs is None:
                raise Exception("No current screen.")
            if self.variable not in cs.scope:
                raise Exception("The {!r} variable is not defined in the {} screen.".format(self.variable, cs.screen_name))

            value = cs.scope[self.variable]

            return value

        def set_value(self, value):
            cs = renpy.current_screen()
            cs.scope[self.variable] = value

    # unpure
    class LocalVariableValue(DictValue):
        """
        :doc: value
        :args: {args}

        A bar value that adjusts the value of a variable in a ``use``\ d
        screen.

        To target a variable in a top-level screen, prefer using
        :func:`ScreenVariableValue`.

        For more information, see :ref:`sl-use`.

        This must be created in the context that the variable is set in
        - it can't be passed in from somewhere else.

        `variable`
            A string giving the name of the variable to adjust.
        """

        kind = "local variable"

        def __init__(self, variable, *args, **kwargs):
            super(LocalVariableValue, self).__init__(sys._getframe(1).f_locals, variable, *args, **kwargs)

init -1500 python hide:
    if config.generating_documentation:
        import inspect
        import itertools

        generic_params = tuple(inspect.signature(__GenericValue.__init__).parameters.values())[1:]
        suffix = inspect.cleandoc("""
        `range`
            The range to adjust over. This must be specified if `max` and `min`
            are not given.
        `max_is_zero`
            If True, then when the {kind}'s value is zero, the value of the
            bar will be `range`, and all other values will be shifted down
            by 1. This works both ways - when the bar is set to the maximum,
            the value of the {kind} is set to 0.

            This is used internally, for some preferences.
        `style`
            The styles of the created bar.
        `offset`
            An offset to add to the value.
        `step`
            The amount to change the bar by. If None, defaults to 1/10th of
            the bar.
        `action`
            If not None, an action to call when the {kind}'s value is changed.
        `min`
            The minimum value of the bar. If both `min` and `max` are given,
            `range` and `offset` are calculated from them.
        `max`
            The maximum value of the bar. If both `min` and `max` are given,
            `range` and `offset` are calculated from them.
        """)

        for value in (DictValue, FieldValue, VariableValue, ScreenVariableValue, LocalVariableValue):
            docstr = inspect.cleandoc(value.__doc__)

            params = []
            for param in itertools.islice(inspect.signature(value.__init__).parameters.values(), 1, None):
                if param.kind not in (param.VAR_POSITIONAL, param.VAR_KEYWORD):
                    params.append(param)

            params.extend(generic_params)

            value.__doc__ = (docstr+"\n"+suffix).format(
                args=inspect.Signature(parameters=params),
                kind=value.kind)

init -1500 python:

    @renpy.pure
    class MixerValue(BarValue, DictEquality):
        """
        :doc: value

        The value of an audio mixer.

        `mixer`
            The name of the mixer to adjust. This is usually one of
            "main", "music", "sfx", or "voice". See :ref:`volume`
            for more information.
        """

        def __init__(self, mixer):
            self.mixer = mixer

        def get_volume(self):
            return _preferences.get_volume(self.mixer)

        def set_volume(self, volume):
            _preferences.set_volume(self.mixer, volume)

        def set_mixer(self, value):

            if value == 0:
                value = 0
            else:
                if config.quadratic_volumes:
                    value = value ** 2
                else:
                    value = 1.0 * value - config.volume_db_range
                    value = pow(10, value / 20)

            self.set_volume(value)

            renpy.restart_interaction()

        def get_mixer(self):
            import math

            value = self.get_volume()

            if value > 0:
                if config.quadratic_volumes:
                    value = math.sqrt(value)
                else:
                    value = math.log10(value) * 20 + config.volume_db_range
            else:
                value = 0

            return value

        def get_adjustment(self):
            import math

            value = self.get_mixer()

            if config.quadratic_volumes:
                range = 1.0
            else:
                range = config.volume_db_range * 1.0

            return ui.adjustment(
                range=range,
                value=value,
                changed=self.set_mixer)

        def get_style(self):
            return "slider", "vslider"

    @renpy.pure
    class _CharacterVolumeValue(MixerValue):

        def __init__(self, voice_tag):
            self.voice_tag = voice_tag

        def get_volume(self):
            return persistent._character_volume[self.voice_tag]

        def set_volume(self, volume):
            persistent._character_volume[self.voice_tag] = volume


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
