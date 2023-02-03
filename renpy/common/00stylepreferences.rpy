# Copyright 2004-2023 Tom Rothamel <pytom@bishoujo.us>
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

# This file contains code for the style preferences system, which allows
# the user to define preferences that update styles.

init -1500 python:

    # A map from preference name to list of (alternative, style, property, value)
    # tuples.
    __preferences = { }

    # A map from preference name to the list of alternatives for that preference.
    __alternatives = { }

    # Are style preferences dirty? If so, we need to update them at the start of
    # the next operation.
    __spdirty = object()
    __spdirty.flag = True

    # A map from preference name to alternative.
    if persistent._style_preferences is None:
        persistent._style_preferences = { }


    def __register_style_preference(preference, alternative, style, property, value):
        """
        :doc: style_preferences
        :name: renpy.register_style_preference

        Registers information about an alternative for a style preference.

        `preference`
            A string, the name of the style preference.

        `alternative`
            A string, the name of the alternative.

        `style`
            The style that will be updated. This may be a style object or a string giving the style name.

        `property`
            A string giving the name of the style property that will be update.

        `value`
            The value that will be assigned to the style property.
        """

        if preference not in __preferences:
            __preferences[preference] = [ ]
            __alternatives[preference] = [ ]

        if alternative not in __alternatives:
            __alternatives[preference].append(alternative)

        __preferences[preference].append((alternative, style, property, value))

    def __init():
        """
        Called at the end of the init phase, to ensure that each preference
        has a valid value.
        """

        for preference, alternatives in __alternatives.items():
            alt = persistent._style_preferences.get(preference, None)

            if alt not in alternatives:
                persistent._style_preferences[preference] = alternatives[0]

    def __update():
        """
        Called at least once per interaction, to update the styles if necessary.
        """

        if not __spdirty.flag:
            return

        renpy.style.rebuild()

        __spdirty.flag = False

    def __apply_styles():
        """
        Called to apply the style preferences
        """

        for preference, alternatives in __preferences.items():

            alt = persistent._style_preferences.get(preference, None)

            for alternative, s, property, value in alternatives:
                if alternative == alt:
                    setattr(s, property, value)

    def __check(preference, alternative=None):

        if preference not in __alternatives:
            raise Exception("{0} is not a known style preference.".format(preference))

        if alternative is not None:
            if alternative not in __alternatives[preference]:
                raise Exception("{0} is not a known alternative for style preference {1}.".format(alternative, preference))

    def __change_language():
        __spdirty.flag = True
        __update()

    def __set_style_preference(preference, alternative):
        """
        :doc: style_preferences
        :name: renpy.set_style_preference

        Sets the selected alternative for the style preference.

        `preference`
            A string giving the name of the style preference.

        `alternative`
            A string giving the name of the alternative.
        """

        __check(preference, alternative)

        persistent._style_preferences[preference] = alternative
        __spdirty.flag = True

        renpy.restart_interaction()

    def __get_style_preference(preference):
        """
        :doc: style_preferences
        :name: renpy.get_style_preference

        Returns a string giving the name of the selected alternative for the named style preference.

        `preference`
            A string giving the name of the style preference.
        """

        __check(preference)

        return persistent._style_preferences[preference]

    @renpy.pure
    class StylePreference(Action):
        """
        :doc: style_preferences

        An action that causes `alternative` to become the selected alternative for the given style preference.

        `preference`
            A string giving the name of the style preference.

        `alternative`
            A string giving the name of the alternative.
        """

        def __init__(self, preference, alternative):

            __check(preference, alternative)

            self.preference = preference
            self.alternative = alternative

        def __call__(self):
            __set_style_preference(self.preference, self.alternative)

        def get_selected(self):
            return __get_style_preference(self.preference) == self.alternative

    renpy.register_style_preference = __register_style_preference
    renpy.set_style_preference = __set_style_preference
    renpy.get_style_preference = __get_style_preference

    config.interact_callbacks.append(__update)
    config.change_language_callbacks.append(__change_language)
    config.build_styles_callbacks.append(__apply_styles)

init 1500 python:
    __init()
