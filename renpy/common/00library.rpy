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

# This is kind of a catch-all file for things that are defined in the library,
# but don't merit their own files.

init 9999:
    # Re-run the errorhandling setup, so we can adjust the styles to the new size
    # of the screen.
    call _errorhandling

init -1700 python:

    # Should we debug the equality operations?
    config.debug_equality = False

    class DictEquality(object):
        """
        Declares two objects equal if their types are the same, and
        their internal dictionaries are equal.
        """

        def __eq__(self, o):

            try:
                if self is o:
                    return True

                if _type(self) is _type(o):
                    return (self.__dict__ == o.__dict__)

                return False

            except Exception:
                if config.debug_equality:
                    raise

                return False

        def __ne__(self, o):
            return not (self == o)

        def __hash__(self):
            rv = hash(_type(self))

            for v in self.__dict__.values():
                rv ^= hash(v)

            return rv

    class FieldEquality(object):
        """
        Declares two objects equal if their types are the same, and
        the listed fields are equal.
        """

        # The lists of fields to use.
        equality_fields = [ ]
        identity_fields = [ ]

        def __eq__(self, o):

            try:

                if self is o:
                    return True

                if _type(self) is not _type(o):
                    return False

                for k in self.equality_fields:
                    if self.__dict__[k] != o.__dict__[k]:
                        return False

                for k in self.identity_fields:
                    if self.__dict__[k] is not o.__dict__[k]:
                        return False

                return True

            except Exception:

                if config.debug_equality:
                    raise

                return False

        def __ne__(self, o):
            return not (self == o)

        def __hash__(self):
            rv = hash(_type(self))

            for k in self.equality_fields:
                rv ^= hash(self.__dict__[k])

            for k in self.identity_fields:
                rv ^= hash(id(self.__dict__[k]))

            return rv


init -1700 python:

    # basics: True if the skip indicator should be shown.
    config.skip_indicator = True

    # This is updated to give the user an idea of where a save is
    # taking place.
    save_name = ''

    ##########################################################################
    # Alias the preferences object.

    # This is for compatibility with default preferences.foo = True.
    preferences = _preferences

    ##########################################################################
    # Empty window

    def _default_empty_window():

        try:
            scry = renpy.scry()

            # When running in a say statement or menu-with-caption, scry for
            # the next say statement, and get the window from that.
            if scry.say or scry.menu_with_caption:
                who = None

                for i in range(10):
                    if scry.say:
                        who = scry.who
                        break

                    scry = scry.next()

            else:
                who = _last_say_who
                who = renpy.eval_who(who)

        except Exception:
            who = None

        if who is None:
            who = narrator

        if isinstance(who, NVLCharacter):
            nvl_show_core()
        elif not isinstance(store.narrator, NVLCharacter):
            store.narrator.empty_window()
        else:
            store._narrator.empty_window()

    config.empty_window = _default_empty_window


    ##########################################################################
    # Extend

    config.extend_interjection = "{fast}"

    class _Extend(object):

        def get_who(self):

            who = _last_say_who
            who = renpy.eval_who(who)

            if who is None:
                who = narrator
            elif isinstance(who, basestring):
                who = Character(who, kind=name_only)

            return who

        def __call__(self, what, interact=True, *args, **kwargs):
            who = self.get_who()

            # This ensures extend works even with NVL mode.
            who.do_extend()

            what = _last_say_what + config.extend_interjection + _last_raw_what

            args = args + _last_say_args
            kw = dict(_last_say_kwargs)
            kw.update(kwargs)
            kw["interact"] = interact and kw.get("interact", True)

            renpy.exports.say(who, what, *args, **kw)
            store._last_say_what = what

        record_say = False

        def get_extend_text(self, what):
            return config.extend_interjection + what

        @property
        def statement_name(self):
            who = self.get_who()
            return getattr(who, "statement_name", "say")

    extend = _Extend()


    ##########################################################################
    # Skip indicator

    style.skip_indicator = Style(style.default, heavy=True, help='The skip indicator.')
    style.skip_indicator.xpos = 10
    style.skip_indicator.ypos = 10

    def _skip_indicator():

        if renpy.has_screen("skip_indicator"):

            if config.skipping and not renpy.get_screen("skip_indicator"):
                renpy.show_screen("skip_indicator")
            elif not config.skipping and renpy.get_screen("skip_indicator"):
                renpy.hide_screen("skip_indicator")

            return

        ### skip_indicator default
        # (text) The style and placement of the skip indicator.

        if config.skip_indicator is True:

            if config.skipping:
                ui.text(_(u"Skip Mode"), style='skip_indicator')

            return

        if not config.skip_indicator:
            return

        if not config.skipping:
            return

        ui.add(renpy.easy.displayable(config.skip_indicator))

    config.overlay_functions.append(_skip_indicator)


    ##########################################################################
    # Predictions

    # A list of labels we predict at start time.
    config.predict_start_labels = [ "start" ]

    # Prediction of statements.
    def _predict_statements(current):

        if main_menu:
            rv = list(config.predict_start_labels)
            rv.append(current)
            return rv

        return [ current ]

    config.predict_statements_callback = _predict_statements


    # Prediction of screens.
    def _predict_screens():

        for i in config.overlay_screens:
            renpy.predict_screen(i)

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

    config.expensive_predict_callbacks.append(_predict_screens)


    ##########################################################################
    # Constant stores.
    #
    # Set _constant on many default stores.

    _errorhandling._constant = True
    _gamepad._constant = True
    _renpysteam._constant = True
    _warper._constant = True
    audio._constant = True
    achievement._constant = True
    build._constant = True
    director._constant = True
    iap._constant = True
    layeredimage._constant = True
    updater._constant = True


    ##########################################################################
    # Misc.

    # Should we display tiles in places of transparency while in developer
    # mode?
    config.transparent_tile = True

    # Use DejaVuSans-Bold when appropriate.
    config.font_replacement_map["DejaVuSans.ttf", True, False] = ("DejaVuSans-Bold.ttf", False, False)

    # License text.
    renpy.license = _("This program contains free software under a number of licenses, including the MIT License and GNU Lesser General Public License. A complete list of software, including links to full source code, can be found {a=https://www.renpy.org/l/license}here{/a}.")


init -1000 python:
    # Set developer to the auto default.
    config.original_developer = "auto"

    if config.script_version:
        config.developer = False
        config.default_developer = False
    else:
        config.developer = True
        config.default_developer = True

    # Lock the library object.
    config.locked = True

    # Record the builtins.
    renpy.lint.renpy_builtins = set(globals())

    for i in """
adv
alt
anim
blinds
center
default
default_transition
dissolve
ease
easeinbottom
easeinleft
easeinright
easeintop
easeoutbottom
easeoutleft
easeoutright
easeouttop
fade
hpunch
irisin
irisout
left
menu
mouse_visible
move
moveinbottom
moveinleft
moveinright
moveintop
moveoutbottom
moveoutleft
moveoutright
moveouttop
name_only
nvl
nvl_variant
offscreenleft
offscreenright
pixellate
pushdown
pushleft
pushright
pushup
right
save_name
slideawaydown
slideawayleft
slideawayright
slideawayup
slidedown
slideleft
slideright
slideup
squares
suppress_overlay
sv
top
topleft
topright
truecenter
vpunch
wipedown
wipeleft
wiperight
wipeup
zoomin
zoominout
zoomout

_autosave
_confirm_quit
_dismiss_pause
_game_menu_screen
_ignore_action
_quit_slot
_rollback
_skipping
_window_subtitle
""".split():

        # _history, history_list, and _version are set later, so aren't included.
        renpy.lint.renpy_builtins.remove(i)

    del i

# After init, make some changes based on if config.developer is True.
init 1700 python hide:

    if config.developer:

        if config.debug_sound is None:
            config.debug_sound = True

        renpy.load_module("_developer/developer")
        renpy.load_module("_developer/inspector")

    if config.window_title is None:
        config.window_title = config.name or "A Ren'Py Game"


# Used by renpy.return_statement() to return.
label _renpy_return:
    return _return

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

# Creates the data structure that history is stored in.
default _history = True
default _history_list = [ ]
