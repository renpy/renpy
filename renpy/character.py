# Copyright 2004-2010 PyTom <pytom@bishoujo.us>
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

import renpy

def predict_show_display_say(who, what, who_args, what_args, window_args, image=False, two_window=False, side_image=None, **kwargs):
    """
    This is the default function used by Character to predict images that
    will be used by show_display_say. It's called with more-or-less the
    same parameters as show_display_say, and it's expected to return a
    list of images used by show_display_say.
    """

    rv = [ ]

    if "background" in window_args:
        rv.append(window_args["background"])
    else:        
        rv.append(getattr(renpy.game.style, window_args["style"]).background)

    if two_window:
        rv.append(renpy.game.style.say_who_window.background)

    if image:
        if image != "<Dynamic>":
            rv.append(renpy.display.im.image(who, True))

    if side_image:
        rv.append(renpy.display.im.image(side_image, True))

    return rv

def show_display_say(who, what, who_args={}, what_args={}, window_args={},
                     image=False, side_image=None, two_window=False,
                     two_window_vbox_properties={},
                     who_window_properties={},
                     say_vbox_properties={},
                     transform=None,
                     variant=None,
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

    def handle_who():
        if who:
            if image:
                renpy.ui.add(renpy.display.im.image(who, loose=True, **who_args))
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

    # Apply the transform.
    if transform:
        renpy.ui.at(transform)
    
    if two_window:

        # Opens say_two_window_vbox.
        renpy.ui.vbox(**merge_style('say_two_window_vbox', two_window_vbox_properties))

        renpy.ui.window(**merge_style('say_who_window', who_window_properties))
        handle_who()

    renpy.ui.window(**window_args)
    # Opens the say_vbox.
    renpy.ui.vbox(**merge_style('say_vbox', say_vbox_properties))

    if not two_window:
        handle_who()

    rv = renpy.ui.text(what, **what_args)

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
    def __init__(self, ctc, ctc_position, callback, interact, type, cb_args):
        self.ctc = ctc
        self.ctc_position = ctc_position
        self.callback = callback
        self.interact = interact
        self.type = type
        self.cb_args = cb_args
        
    def __call__(self):
        
        if self.ctc and self.ctc_position == "fixed":
            renpy.ui.add(self.ctc)
            renpy.exports.restart_interaction()

        for c in self.callback:
            c("slow_done", interact=self.interact, type=self.type, **self.cb_args)

            
# This function takes care of repeatably showing the screen as part of
# an interaction.
def display_say(show_function,
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
                type,
                checkpoint=True,
                ctc_timedpause=None,
                ctc_force=False):

    
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

    if not interact:
        all_at_once = True

    if all_at_once:
        pause = None
    else:
        pause = 0

    # True if the {nw} tag was found in what_text.
    no_wait = False

    keep_interacting = True
    slow_start = 0
        
    while keep_interacting:

        # If we're going to do an interaction, then saybehavior needs
        # to be here.
        if interact:            
            behavior = renpy.ui.saybehavior(allow_dismiss=renpy.config.say_allow_dismiss)
        else:
            behavior = None

        for c in callback:
            c("show", interact=interact, type=type, **cb_args)
            
        what_text = show_function()

        # Update the properties of the what_text widget.

        if pause is not None and pause < what_text.pauses:
            if what_text.pause_lengths[pause] is not None:
                what_ctc = ctc_timedpause or ctc_pause
            else:
                what_ctc = ctc_pause
        else:
            what_ctc = ctc

        if not (interact or ctc_force):
            what_ctc = None
            
        what_ctc = renpy.easy.displayable_or_none(what_ctc)

        if what_ctc is not None:
            what_ctc = what_ctc.parameterize(('ctc',), ())

        # This object is called when the slow text is done.
        slow_done = SlowDone(what_ctc, ctc_position, callback, interact, type, cb_args)
        
        what_text.slow = slow
        what_text.slow_param = slow
        what_text.slow_done = slow_done
        what_text.slow_start = slow_start
        what_text.pause = pause

        if what_ctc and ctc_position == "nestled":
            what_text.tokens.append([ ("widget", what_ctc) ])

        # Now, re-run update on what_text.
        what_text.update(retokenize=False)
            
        keep_interacting = what_text.keep_pausing
        no_wait |= what_text.no_wait

        if no_wait:
            slow_done.ctc = None
        
        for c in callback:
            c("show_done", interact=interact, type=type, **cb_args)

        if behavior and afm:
            behavior.set_afm_length(what_text.get_simple_length() - slow_start) # E1103

        if interact:
            
            rv = renpy.ui.interact(mouse='say', type=type, roll_forward=roll_forward)

            # This is only the case if the user has rolled forward, {nw} happens, or
            # maybe in some other obscure cases.
            if rv is False:
                break 

        slow_start = what_text.get_laidout_length()

        if keep_interacting:
            pause += 1

            for i in renpy.config.say_sustain_callbacks:
                i()
    
    # Do the checkpoint and with None.
    if interact:

        if not no_wait:
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
NotSet = object()

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
            self.who_args = { }
            self.what_args = { }
            self.window_args = { }
            self.show_args = { }
            self.cb_args = { }

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

    # A curried version of this is called to cause the interaction to
    # occur.
    def do_show(self, who, what):
        return self.show_function(
            who,
            what, 
            who_args=self.who_args,
            what_args=self.what_args,
            window_args=self.window_args,
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
        display_say(lambda : self.do_show(who, what),
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
            **self.show_args)
    
    def __call__(self, what, **kwargs):

        # Check self.condition to see if we should show this line at all.

        if not (self.condition is None or renpy.python.py_eval(self.condition)):
            return True

        # Figure out the arguments to display.
        display_args = self.display_args.copy()
        display_args.update(kwargs)
                
        who = self.name

        # If dynamic is set, evaluate the name expression.
        if self.dynamic:
            who = renpy.python.py_eval(who)

        if who is not None:
            who = self.who_prefix + who + self.who_suffix

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
        
        
    def predict(self, what):

        if self.dynamic:
            who = "<Dynamic>"
        else:
            who = self.name

        return self.do_predict(who, what)
            
def Character(name=NotSet, kind=None, **properties):
    if kind is None:
        kind = renpy.store.adv

    return type(kind)(name, kind=kind, **properties)
    
            
def DynamicCharacter(name_expr, **properties):
    return Character(name_expr, dynamic=True, **properties)

