# Copyright 2004-2015 Tom Rothamel <pytom@bishoujo.us>
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

# The Character object (and friends).

import renpy.display

import re

# This matches the dialogue-relevant text tags.
TAG_RE = re.compile(r'(\{\{)|(\{(p|w|nw|fast)(?:\=([^}]*))?\})', re.S)

class DialogueTextTags(object):
    """
    This object parses the text tags that only make sense in dialogue,
    like {fast}, {p}, {w}, and {nw}.
    """

    def __init__(self, s):

        # The text that we've accumulated, not including any tags.
        self.text = ""

        # The index in the produced string where each pause starts.
        self.pause_start = [ 0 ]

        # The index in the produced string where each pause ends.
        self.pause_end = [ ]

        # The time to delay for each pause. None to delay forever.
        self.pause_delay = [ ]

        # True if we've encountered the no-wait tag.
        self.no_wait = False

        i = iter(TAG_RE.split(s))

        while True:

            try:
                self.text += i.next()

                quoted = i.next()
                full_tag = i.next()
                tag = i.next()
                value = i.next()

                if value is not None:
                    value = float(value)

                if quoted is not None:
                    self.text += quoted
                    continue

                if tag == "p" or tag == "w":
                    self.pause_start.append(len(self.text))
                    self.pause_end.append(len(self.text))
                    self.pause_delay.append(value)

                elif tag == "nw":
                    self.no_wait = True

                elif tag == "fast":
                    self.pause_start = [ len(self.text) ]
                    self.pause_end = [ ]
                    self.pause_delay = [ ]
                    self.no_wait = False

                self.text += full_tag

            except StopIteration:
                break

        self.pause_end.append(len(self.text))

        if self.no_wait:
            self.pause_delay.append(0)
        else:
            self.pause_delay.append(None)


def predict_show_display_say(who, what, who_args, what_args, window_args, image=False, two_window=False, side_image=None, screen=None, **kwargs):
    """
    This is the default function used by Character to predict images that
    will be used by show_display_say. It's called with more-or-less the
    same parameters as show_display_say, and it's expected to return a
    list of images used by show_display_say.
    """

    if side_image:
        renpy.easy.predict(side_image)

    if renpy.store._side_image_attributes:
        renpy.easy.predict(renpy.display.image.ImageReference(("side",) + renpy.store._side_image_attributes))

    if image:
        if image != "<Dynamic>":
            renpy.easy.predict(who)

        kwargs["image"] = image

    if screen:
        props = compute_widget_properties(who_args, what_args, window_args)

        renpy.display.screen.predict_screen(
            screen,
            _widget_properties=props,
            who=who,
            what=what,
            two_window=two_window,
            side_image=side_image,
            **kwargs)

        return



def compute_widget_properties(who_args, what_args, window_args, variant=None):
    """
    Computes and returns the widget properties.
    """

    def style_args(d):

        if not "style" in d:
            return d

        in_rollback = renpy.exports.in_rollback()

        if (not in_rollback) and (not variant):
            return d

        d = d.copy()

        style = d["style"]

        if isinstance(style, basestring):
            style = getattr(renpy.store.style, style)

            if variant is not None:
                style = style[variant]

            if in_rollback:
                style = style["rollback"]

        d["style"] = style

        return d

    who_args = style_args(who_args)
    what_args = style_args(what_args)
    window_args = style_args(window_args)

    return {
        "window" : window_args,
        "what" : what_args,
        "who" : who_args,
        }


def show_display_say(who, what, who_args={}, what_args={}, window_args={},
                     image=False, side_image=None, two_window=False,
                     two_window_vbox_properties={},
                     who_window_properties={},
                     say_vbox_properties={},
                     transform=None,
                     variant=None,
                     screen=None,
                     layer=None,
                     **kwargs):
    """
    This is called (by default) by renpy.display_say to add the
    widgets corresponding to a screen of dialogue to the user. It is
    not expected to be called by the user, but instead to be called by
    display_say, or by a function passed as the show_function argument
    to Character or display_say.

    @param who: The name of the character that is speaking, or None to
    not show this name to the user.

    @param what: What that character is saying. Please not that this
    may not be a string, as it can also be a list containing both text
    and displayables, suitable for use as the first argument of ui.text().

    @param who_args: Additional keyword arguments intended to be
    supplied to the ui.text that creates the who widget of this dialogue.

    @param what_args: Additional keyword arguments intended to be
    supplied to the ui.text that creates the what widget of this dialogue.

    @param window_args: Additional keyword arguments intended to be
    supplied to the ui.window that creates the who widget of this
    dialogue.

    @param image: If True, then who should be interpreted as an image
    or displayable rather than a text string.

    @param kwargs: Additional keyword arguments should be ignored.

    This function is required to return the ui.text() widget
    displaying the what text.
    """

    props = compute_widget_properties(who_args, what_args, window_args, variant=variant)

    def handle_who():
        if who:
            if image:
                renpy.ui.add(renpy.display.im.image(who, loose=True, **props["who"]))
            else:
                renpy.ui.text(who, **who_args)

    def merge_style(style, properties):

        if isinstance(style, basestring):
            style = getattr(renpy.store.style, style)

        if variant is not None:
            style = style[variant]

        if renpy.exports.in_rollback():
            style = style["rollback"]

        rv = dict(style=style)
        rv.update(properties)
        return rv

    if screen and renpy.display.screen.has_screen(screen):

        if layer is None:
            layer = renpy.config.say_layer

        tag = screen
        index = 0

        while renpy.exports.showing(tag):
            index += 1
            tag = "%s%d" % (screen, index)

        if image:
            kwargs["image"] = image

        renpy.display.screen.show_screen(
            screen,
            _widget_properties=props,
            _transient = True,
            _tag = tag,
            side_image=side_image,
            two_window=two_window,
            who=who,
            what=what,
            _layer=layer,
            **kwargs)

        renpy.exports.shown_window()

        return renpy.display.screen.get_widget(screen, "what", layer)


    # Apply the transform.
    if transform:
        renpy.ui.at(transform)

    if two_window:

        # Opens say_two_window_vbox.
        renpy.ui.vbox(**merge_style('say_two_window_vbox', two_window_vbox_properties))

        renpy.ui.window(**merge_style('say_who_window', who_window_properties))
        handle_who()

    renpy.ui.window(**props["window"])
    # Opens the say_vbox.
    renpy.ui.vbox(**merge_style('say_vbox', say_vbox_properties))

    if not two_window:
        handle_who()

    rv = renpy.ui.text(what, **props["what"])

    # Closes the say_vbox.
    renpy.ui.close()

    if two_window:
        # Closes the say_two_window_vbox.
        renpy.ui.close()

    if side_image:
        renpy.ui.image(side_image)

    renpy.exports.shown_window()

    return rv



class SlowDone(object):
    delay = None

    def __init__(self, ctc, ctc_position, callback, interact, type, cb_args, delay): #@ReservedAssignment
        self.ctc = ctc
        self.ctc_position = ctc_position
        self.callback = callback
        self.interact = interact
        self.type = type
        self.cb_args = cb_args
        self.delay = delay

    def __call__(self):

        if self.ctc and self.ctc_position == "fixed":
            renpy.display.screen.show_screen("_ctc", _transient=True, ctc=self.ctc)
            renpy.exports.restart_interaction()

        if self.delay is not None:
            renpy.ui.pausebehavior(self.delay, True)
            renpy.exports.restart_interaction()

        for c in self.callback:
            c("slow_done", interact=self.interact, type=self.type, **self.cb_args)


# This function takes care of repeatably showing the screen as part of
# an interaction.
def display_say(
    who,
    what,
    show_function,
    interact,
    slow,
    afm,
    ctc,
    ctc_pause,
    ctc_position,
    all_at_once,
    cb_args,
    with_none,
    callback,
    type, #@ReservedAssignment
    checkpoint=True,
    ctc_timedpause=None,
    ctc_force=False):

    if interact and (not renpy.game.preferences.skip_unseen) and (not renpy.game.context().seen_current(True)) and renpy.config.skipping == "fast":
        renpy.config.skipping = None

    # If we're in fast skipping mode, don't bother with say
    # statements at all.
    if interact and renpy.config.skipping == "fast":

        # Clears out transients.
        renpy.exports.with_statement(None)
        return

    # Figure out the callback(s) we want to use.
    if callback is None:
        if renpy.config.character_callback:
            callback = [ renpy.config.character_callback ]
        else:
            callback = [ ]

    if not isinstance(callback, list):
        callback = [ callback ]

    callback = renpy.config.all_character_callbacks + callback

    # Call the begin callback.
    for c in callback:
        c("begin", interact=interact, type=type, **cb_args)

    if renpy.exports.roll_forward_info():
        roll_forward = False
    else:
        roll_forward = None

    # If we're just after a rollback or roll_forward, disable slow.
    after_rollback = renpy.game.after_rollback
    if after_rollback:
        slow = False

    # If we're committed to skipping this statement, disable slow.
    elif (renpy.config.skipping and
          (renpy.game.preferences.skip_unseen or
           renpy.game.context().seen_current(True))):
        slow = False

    # Figure out which pause we're on. (Or set the pause to None in
    # order to put us in all-at-once mode.)
    if not interact or renpy.game.preferences.self_voicing:
        all_at_once = True

    dtt = DialogueTextTags(what)

    if all_at_once:
        pause_start = [ dtt.pause_start[0] ]
        pause_end = [ len(dtt.text) ]
        pause_delay = [ dtt.pause_delay[-1] ]
    else:
        pause_start = dtt.pause_start
        pause_end = dtt.pause_end
        pause_delay = dtt.pause_delay


    for i, (start, end, delay) in enumerate(zip(pause_start, pause_end, pause_delay)):

        last_pause = (i == len(pause_start) - 1)

        # If we're going to do an interaction, then saybehavior needs
        # to be here.
        if interact:
            behavior = renpy.ui.saybehavior(allow_dismiss=renpy.config.say_allow_dismiss)
        else:
            behavior = None


        # The string to show.
        what_string = dtt.text

        # Figure out the CTC to use, if any.
        if last_pause:
            what_ctc = ctc
        else:
            if delay is not None:
                what_ctc = ctc_timedpause or ctc_pause
            else:
                what_ctc = ctc_pause

        if not (interact or ctc_force):
            what_ctc = None

        what_ctc = renpy.easy.displayable_or_none(what_ctc)

        if what_ctc is not None:
            what_ctc = what_ctc.parameterize(('ctc',), ())

        if delay == 0:
            what_ctc = None

        # Create the callback that is called when the slow text is done.
        slow_done = SlowDone(what_ctc, ctc_position, callback, interact, type, cb_args, delay)

        # Run the show callback.
        for c in callback:
            c("show", interact=interact, type=type, **cb_args)

        # Show the text.
        what_text = show_function(who, what_string)

        if not isinstance(what_text, renpy.text.text.Text): #@UndefinedVariable
            raise Exception("The say screen (or show_function) must return a Text object.")

        if what_ctc and ctc_position == "nestled":
            what_text.set_ctc(what_ctc)

        # Update the properties of the what_text widget.
        what_text.start = start
        what_text.end = end
        what_text.slow = slow
        what_text.slow_done = slow_done

        what_text.update()

        for c in callback:
            c("show_done", interact=interact, type=type, **cb_args)

        if behavior and afm:
            behavior.set_afm_length(end - start)

        if not slow:
            slow_done()

        if interact:
            rv = renpy.ui.interact(mouse='say', type=type, roll_forward=roll_forward)

            # This is only the case if the user has rolled forward, {nw} happens, or
            # maybe in some other obscure cases.
            if rv is False:
                break

            if not last_pause:
                for i in renpy.config.say_sustain_callbacks:
                    i()

    # Do the checkpoint and with None.
    if interact:

        if not dtt.no_wait:
            if checkpoint:
                renpy.exports.checkpoint(True)
        else:
            renpy.game.after_rollback = after_rollback

        if with_none is None:
            with_none = renpy.config.implicit_with_none

        if with_none:
            renpy.game.interface.do_with(None, None)

    for c in callback:
        c("end", interact=interact, type=type, **cb_args)


# This is used to flag values that haven't been set by the user.
NotSet = renpy.object.Sentinel("NotSet")

class ADVCharacter(object):
    """
    The character object contains information about a character. When
    passed as the first argument to a say statement, it can control
    the name that is displayed to the user, and the style of the label
    showing the name, the text of the dialogue, and the window
    containing both the label and the dialogue.
    """

    # Properties beginning with what or window that are treated
    # specially.
    special_properties = [
        'what_prefix',
        'what_suffix',
        'who_prefix',
        'who_suffix',
        'show_function',
        ]

    voice_tag = None

    # When adding a new argument here, remember to add it to copy below.
    def __init__(
        self,
        name=NotSet,
        kind=None,
        **properties):

        if kind is None:
            kind = renpy.store.adv

        if name is not NotSet:
            properties["name"] = name

        # This grabs a value out of properties, and then grabs it out of
        # kind if it's not set.
        def v(n):
            if n in properties:
                return properties.pop(n)
            else:
                return getattr(kind, n)


        # Similar, but it grabs the value out of kind.display_args instead.
        def d(n):
            if n in properties:
                return properties.pop(n)
            else:
                return kind.display_args[n]

        self.name = v('name')
        self.who_prefix = v('who_prefix')
        self.who_suffix = v('who_suffix')
        self.what_prefix = v('what_prefix')
        self.what_suffix = v('what_suffix')

        self.show_function = v('show_function')
        self.predict_function = v('predict_function')

        self.condition = v('condition')
        self.dynamic = v('dynamic')
        self.screen = v('screen')
        self.mode = v('mode')

        self.voice_tag = v('voice_tag')

        if renpy.config.new_character_image_argument:
            if "image" in properties:
                self.image_tag = properties.pop("image")
            else:
                self.image_tag = kind.image_tag
        else:
            self.image_tag = None

        self.display_args = dict(
            interact = d('interact'),
            slow = d('slow'),
            afm = d('afm'),
            ctc = renpy.easy.displayable_or_none(d('ctc')),
            ctc_pause = renpy.easy.displayable_or_none(d('ctc_pause')),
            ctc_timedpause = renpy.easy.displayable_or_none(d('ctc_timedpause')),
            ctc_position = d('ctc_position'),
            all_at_once = d('all_at_once'),
            with_none = d('with_none'),
            callback = d('callback'),
            type = d('type'),
            )

        if kind:
            self.who_args = kind.who_args.copy()
            self.what_args = kind.what_args.copy()
            self.window_args = kind.window_args.copy()
            self.show_args = kind.show_args.copy()
            self.cb_args = kind.cb_args.copy()

        else:
            self.who_args = { "substitute" : False }
            self.what_args = { "substitute" : False }
            self.window_args = { }
            self.show_args = { }
            self.cb_args = { }

        if not renpy.config.new_character_image_argument:
            if "image" in properties:
                self.show_args["image"] = properties.pop("image")

        if "slow_abortable" in properties:
            self.what_args["slow_abortable"] = properties.pop("slow_abortable")

        for k in list(properties):

            if "_" in k:
                prefix, suffix = k.split("_", 1)

                if prefix == "show":
                    self.show_args[suffix] = properties[k]
                    continue
                elif prefix == "cb":
                    self.cb_args[suffix] = properties[k]
                    continue
                elif prefix == "what":
                    self.what_args[suffix] = properties[k]
                    continue
                elif prefix == "window":
                    self.window_args[suffix] = properties[k]
                    continue
                elif prefix == "who":
                    self.who_args[suffix] = properties[k]
                    continue

            self.who_args[k] = properties[k]

    def copy(self, name=NotSet, **properties):
        return type(self)(name, kind=self, **properties)

    # This is called before the interaction.
    def do_add(self, who, what):
        return

    # This is what shows the screen for a given interaction.
    def do_show(self, who, what):
        return self.show_function(
            who,
            what,
            who_args=self.who_args,
            what_args=self.what_args,
            window_args=self.window_args,
            screen=self.screen,
            **self.show_args)

    # This is called after the last interaction is done.
    def do_done(self, who, what):
        return

    # This is called when an extend occurs, before the usual add/show
    # cycel.
    def do_extend(self):
        return

    # This is called to actually do the displaying.
    def do_display(self, who, what, **display_args):
        display_say(who,
                    what,
                    self.do_show,
                    **display_args)


    # This is called to predict images that will be used by this
    # statement.
    def do_predict(self, who, what):
        return self.predict_function(
            who,
            what,
            who_args=self.who_args,
            what_args=self.what_args,
            window_args=self.window_args,
            screen=self.screen,
            **self.show_args)

    def resolve_say_attributes(self, predict):
        """
        Deals with image attributes associated with the current say
        statement.
        """

        attrs = renpy.exports.get_say_attributes()

        if not attrs:
            return

        if not self.image_tag:
            if not predict:
                raise Exception("Say has image attributes %r, but there's no image tag associated with the speaking character." % (attrs,))
            else:
                return

        tagged_attrs = (self.image_tag,) + attrs
        images = renpy.game.context().images

        # If image is showing already, resolve it, then show or predict it.
        if images.showing("master", (self.image_tag,)):

            new_image = images.apply_attributes("master", self.image_tag, tagged_attrs)

            if new_image is None:
                new_image = tagged_attrs

            if predict:
                images.predict_show(new_image)
            else:
                trans = renpy.config.say_attribute_transition

                if trans is not None:
                    renpy.exports.with_statement(None)

                renpy.exports.show(new_image)

                if trans is not None:
                    renpy.exports.with_statement(trans)

        else:

            # Otherwise, just record the attributes of the image.
            images.predict_show("master", tagged_attrs, show=False)

    def __str__(self):
        who = self.name

        # If dynamic is set, evaluate the name expression.
        if self.dynamic:
            who = renpy.python.py_eval(who)

        return who


    def __call__(self, what, interact=True, **kwargs):

        # Check self.condition to see if we should show this line at all.
        if not (self.condition is None or renpy.python.py_eval(self.condition)):
            return True

        if not isinstance(what, basestring):
            raise Exception("Character expects its what argument to be a string, got %r." % (what,))

        self.resolve_say_attributes(False)

        old_side_image_attributes = renpy.store._side_image_attributes

        if self.image_tag:
            attrs = (self.image_tag,) + renpy.game.context().images.get_attributes("master", self.image_tag)
        else:
            attrs = None

        renpy.store._side_image_attributes = attrs

        if renpy.config.voice_tag_callback is not None:
            renpy.config.voice_tag_callback(self.voice_tag)

        try:

            if interact:
                renpy.exports.mode(self.mode)

            # Figure out the arguments to display.
            display_args = self.display_args.copy()
            display_args.update(kwargs)
            display_args["interact"] = display_args["interact"] and interact

            who = self.name

            # If dynamic is set, evaluate the name expression.
            if self.dynamic:
                who = renpy.python.py_eval(who)

            def sub(s, scope=None, force=False, translate=True):
                return renpy.substitutions.substitute(s, scope=scope, force=force, translate=translate)[0]

            if who is not None:
                if renpy.config.new_substitutions:
                    who_pattern = sub(self.who_prefix + "[[who]" + self.who_suffix)
                    who = who_pattern.replace("[who]", sub(who))
                else:
                    who = self.who_prefix + who + self.who_suffix

            ctx = renpy.game.context()

            if (ctx.translate_language is not None) and (ctx.translate_identifier is not None):
                translate = False
            else:
                translate = True

            if renpy.config.new_substitutions:
                what_pattern = sub(self.what_prefix + "[[what]" + self.what_suffix)
                what = what_pattern.replace("[what]", sub(what, translate=translate))
            else:
                what = self.what_prefix + what + self.what_suffix

            # Run the add_function, to add this character to the
            # things like NVL-mode.
            self.do_add(who, what)

            # Now, display the damned thing.
            self.do_display(who, what, cb_args=self.cb_args, **display_args)

            # Indicate that we're done.
            self.do_done(who, what)

            # Finally, log this line of dialogue.
            if who and isinstance(who, (str, unicode)):
                renpy.exports.log(who)
            renpy.exports.log(what)
            renpy.exports.log("")

        finally:

            if interact:
                renpy.store._side_image_attributes = old_side_image_attributes


    def predict(self, what):

        self.resolve_say_attributes(True)

        old_side_image_attributes = renpy.store._side_image_attributes

        if self.image_tag:
            attrs = ( self.image_tag, ) + renpy.game.context().images.get_attributes("master", self.image_tag)
        else:
            attrs = None

        renpy.store._side_image_attributes = attrs

        try:

            if self.dynamic:
                who = "<Dynamic>"
            else:
                who = self.name

            return self.do_predict(who, what)

        finally:
            renpy.store._side_image_attributes = old_side_image_attributes

    def will_interact(self):

        if not (self.condition is None or renpy.python.py_eval(self.condition)):
            return False

        return self.display_args['interact']


def Character(name=NotSet, kind=None, **properties):
    """
    :doc: character
    :args: (name, kind=adv, **args)
    :name: Character

    Creates and returns a Character object, which controls the look
    and feel of dialogue and narration.

    `name`
        If a string, the name of the character for dialogue. When
        `name` is ``None``, display of the name is omitted, as for
        narration.

    `kind`
        The Character to base this Character off of. When used, the
        default value of any argument not supplied to this Character
        is the value of that argument supplied to `kind`. This can
        be used to define a template character, and then copy that
        character with changes.

    **Linked Image**
    An image tag may be associated with a Character. This allows a
    say statement involving this character to display an image with
    the tag, and also allows Ren'Py to automatically select a side
    image to show when this character speaks.

    `image`
         A string giving the image tag that is linked with this
         character.

    **Voice Tag**
    If a voice tag is assign to a Character, the voice files that are
    associated with it, can be muted or played in the preference
    screen.

    `voice_tag`
        A String that enables the voice file associated with the
        Character to be muted or played in the 'voice' channel.

    **Prefixes and Suffixes.**
    These allow a prefix and suffix to be applied to the name of the
    character, and to the text being shown. This can be used, for
    example, to add quotes before and after each line of dialogue.

    `what_prefix`
        A string that is prepended to the dialogue being spoken before
        it is shown.

    `what_suffix`
        A string that is appended to the dialogue being spoken before
        it is shown.

    `who_prefix`
        A string that is prepended to the name of the character before
        it is shown.

    `who_suffix`
        A string that is appended to the name of the character before
        it is shown.

    **Changing Name Display.**
    These options help to control the display of the name.

    `dynamic`
        If true, then `name` should be a string containing a python
        expression. That string will be evaluated before each line
        of dialogue, and the result used as the name of the character.

    **Controlling Interactions.**
    These options control if the dialogue is displayed, if an
    interaction occurs, and the mode that is entered upon display.

    `condition`
        If given, this should be a string containing a python
        expression. If the expression is false, the dialogue
        does not occur, as if the say statement did not happen.

    `interact`
        If true, the default, an interaction occurs whenever the
        dialogue is shown. If false, an interaction will not occur,
        and additional elements can be added to the screen.

    `mode`
        A string giving the mode to enter when this character
        speaks. See the section on :ref:`modes <modes>` for more details.

    `callback`
        A function that is called when events occur while the
        character is speaking. See the section on
        :ref:`character-callbacks` fore more information.

    **Click-to-continue.**
    A click-to-continue indicator is displayed once all the text has
    finished displaying, to prompt the user to advance.

    `ctc`
        A Displayable to use as the click-to-continue indicator, unless
        a more specific indicator is used.

    `ctc_pause`
        A Displayable to use a the click-to-continue indicator when the
        display of text is paused by the {p} or {w} text tags.

    `ctc_timedpause`
        A Displayable to use a the click-to-continue indicator when the
        display of text is paused by the {p=} or {w=} text tags. When
        None, this takes its default from ctc_pause, use ``Null()``
        when you want a ctc_pause but no ctc_timedpause.

    `ctc_position`
        Controls the location of the click-to-continue indicator. If
        ``"nestled"``, the indicator is displayed as part of the text
        being shown, immediately after the last character. If ``"fixed"``,
        the indicator is added to the screen, and its position is
        controlled by the position style properties.


    **Screens.**
    The display of dialogue uses a :ref:`screen <screens>`. These arguments
    allow you to select that screen, and to provide arguments to it.

    `screen`
        The name of the screen that is used to display the dialogue.

    Keyword arguments beginning with ``show_`` have the prefix
    stripped off, and are passed to the screen as arguments. For
    example, the value of ``show_side_image`` will become the
    value of the ``side_image`` variable in the screen.

    Some useful ``show_`` variables implemented by the default screens are:

    `show_side_image`
        When given a Displayable, shows that displayable when the
        dialogue is shown. The position of that displayable is
        controlled by its position properties. This is often used
        to show an image of the speaking character to the side
        of the dialogue.

    `show_two_window`
        If true, restructures the layout so that the name of the
        character is placed in one window, and the dialogue text in a
        second window.

    `show_layer`
        If given, this should be a string giving the name of the layer
        to show the "say" screen on.

    **Styling Text and Windows.**
    Keyword arguments beginning with ``who_``, ``what_``, and
    `window_`` have their prefix stripped, and are used to :ref:`style
    <styles>` the character name, the spoken text, and the window
    containing both, respectively.

    For example, if a character is given the keyword argument
    ``who_color="#c8ffc8"``, the color of the character's name is
    changed, in this case to green. ``window_background="frame.png"``
    sets the background of the window containing this character's
    dialogue.

    The style applied to the character name, spoken text, and window
    can also be set this way, using the `who_style`, `what_style`, and
    `window_style` arguments, respectively.
     """

    if kind is None:
        kind = renpy.store.adv

    return type(kind)(name, kind=kind, **properties)


def DynamicCharacter(name_expr, **properties):
    return Character(name_expr, dynamic=True, **properties)

