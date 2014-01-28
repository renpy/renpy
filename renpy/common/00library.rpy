# Copyright 2004-2014 Tom Rothamel <pytom@bishoujo.us>
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

# This is kind of a catch-all file for things that are defined in the library,
# but don't merit their own files.

init -1700 python:

    # basics: True if the skip indicator should be shown.
    config.skip_indicator = True

    # This is updated to give the user an idea of where a save is
    # taking place.
    save_name = ''

    def _default_empty_window():

        who = _last_say_who

        if who is not None:
            who = eval(who)

        if who is None:
            who = narrator

        if isinstance(who, NVLCharacter):
            nvl_show_core()
        else:
            store.narrator("", interact=False)

    config.empty_window = _default_empty_window

    style.skip_indicator = Style(style.default, heavy=True, help='The skip indicator.')
    style.skip_indicator.xpos = 10
    style.skip_indicator.ypos = 10


init -1700 python:

    config.extend_interjection = "{fast}"

    def extend(what, interact=True):
        who = _last_say_who

        if who is not None:
            who = eval(who)

        if who is None:
            who = narrator

        if isinstance(who, basestring):
            who = unknown.copy(who)

        # This ensures extend works even with NVL mode.
        who.do_extend()

        what = _last_say_what + config.extend_interjection + _last_raw_what

        renpy.exports.say(who, what, interact=interact)
        store._last_say_what = what

    extend.record_say = False


init -1700 python:

    _predict_screens = [ ]

    def skip_indicator():

        ### skip_indicator default
        # (text) The style and placement of the skip indicator.

        if config.skip_indicator is True:

            if config.skipping == "slow" and config.skip_indicator:
                ui.text(_(u"Skip Mode"), style='skip_indicator')

            if config.skipping == "fast" and config.skip_indicator:
                ui.text(_(u"Fast Skip Mode"), style='skip_indicator')

            return

        if not config.skip_indicator:
            return

        if not config.skipping:
            return

        ui.add(renpy.easy.displayable(config.skip_indicator))

    config.overlay_functions.append(skip_indicator)

    # Prediction of screens.
    def predict():

        for s in _predict_screens:
            if renpy.has_screen(s):
                renpy.predict_screen(s)

        s = _game_menu_screen

        if s is None:
            return

        if renpy.has_screen(s):
            renpy.predict_screen(s)
            return

        if s.endswith("_screen"):
            s = s[:-7]
            if renpy.has_screen(s):
                renpy.predict_screen(s)
                return


    config.predict_callbacks.append(predict)

init -1700 python:

    ##########################################################################
    # Side Images

    config.side_image_tag = None
    config.side_image_only_not_showing = False

    def SideImage(prefix_tag="side"):
        """
        :doc: side_image_function

        Returns the side image associated with the currently speaking character,
        or a Null displayable if no such side image exists.
        """

        name = renpy.get_side_image(prefix_tag, image_tag=config.side_image_tag, not_showing=config.side_image_only_not_showing)
        if name is None:
            return Null()
        else:
            return ImageReference(name)


init -1000:
    # Lock the library object.
    $ config.locked = True


# After init, make some changes based on if config.developer is True.
init 1700 python hide:

    if config.developer:

        if config.debug_sound is None:
            config.debug_sound = True

        renpy.load_module("_developer/developer")
        renpy.load_module("_developer/inspector")

# Entry point for the developer screen. The rest of it is loaded from
# _developer.rpym
label _developer:

    if not config.developer:
        return

    $ _enter_menu()

    jump expression "_developer_screen"


# This is used to ensure a fixed click-to-continue indicator is shown on
# its own layer.
screen _ctc:
    add ctc
