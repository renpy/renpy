# Copyright 2004-2007 PyTom <pytom@bishoujo.us>
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
        rv.append(renpy.display.im.image(who, True))

    if side_image:
        rv.append(renpy.display.im.image(side_image, True))

    return rv

def show_display_say(who, what, who_args={}, what_args={}, window_args={},
                     image=False, side_image=None, two_window=False,
                     two_window_vbox_properties={},
                     who_window_properties={},
                     say_vbox_properties={},
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
        rv = dict(style=style)
        rv.update(properties)
        return rv

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

    return rv


def predict_display_say(who, what,
                what_style='say_dialogue',
                window_style='say_window',
                who_style='say_label',
                who_prefix='',
                who_suffix='',
                what_prefix='',
                what_suffix='',
                interact=True,
                slow=True,
                slow_abortable=True,
                image=False,
                afm=True,
                ctc=None,
                ctc_position="nestled",
                all_at_once=False,
                what_properties={},
                window_properties={},
                show_function = show_display_say,
                show_args = { },
                with_none = None,
                callback = None,
                **who_properties):
    """
    This is the default function used by Character to predict images that
    will be used by display_say. It's called with more-or-less the
    same parameters as display_say, and is expected to return a list
    of images used by display_say.
    """

    window_args = window_properties.copy()
    window_args["style"] = window_style

    who_args = who_properties.copy()
    who_args["style"] = who_style

    what_args = what_properties.copy()
    what_args["style"] = who_style

    func = show_args.get("predict_function", predict_show_display_say)
    rv = func(who, what, who_args=who_args, what_args=what_args, window_args=window_args, image=image,
              **show_args) 

    if ctc:
        rv.append(ctc)

    return rv

class SlowDone(object):
    def __init__(self, ctc, ctc_position, callback, interact):
        self.ctc = ctc
        self.ctc_position = ctc_position
        self.callback = callback
        self.interact = interact

    def __call__(self):
        
        if self.ctc and self.ctc_position == "fixed":
            renpy.ui.add(self.ctc)
            renpy.exports.restart_interaction()

        for c in self.callback:
            c("slow_done", interact=self.interact)

def display_say(who, what, who_style='say_label',
                what_style='say_dialogue',
                window_style='say_window',
                who_prefix='',
                who_suffix='',
                what_prefix='',
                what_suffix='',
                interact=True,
                slow=True,
                slow_abortable=True,
                image=False,
                afm=True,
                ctc=None,
                ctc_position="nestled",
                all_at_once=False,
                what_properties={},
                window_properties={},
                show_function = show_display_say,
                show_args = { },
                with_none = None,
                callback = None,
                **properties):
    """
    @param who: Who is saying the dialogue, or None if it's not being
    said by anyone.

    @param what: What is being said.

    @param afm: If True, the auto-forwarding mode is enabled. If False,
    it is disabled.

    @param all_at_once: If True, then the text is displayed all at once. (This is forced to true if interact=False.)

    For documentation of the other arguments, please read the
    documentation for Character.
    """

    # If we're in fast skipping mode, don't bother with say
    # statements at all.
    if renpy.config.skipping == "fast":

        # Clears out transients.
        renpy.exports.with(None)
        
        return

    if callback is None:
        if renpy.config.character_callback:
            callback = [ renpy.config.character_callback ]
        else:
            callback = [ ]
            
    if not isinstance(callback, list):
        callback = [ callback ]

    callback = renpy.config.all_character_callbacks + callback 
        
    for c in callback:
        c("begin", interact=interact)
    
    if renpy.exports.roll_forward_info():
        roll_forward = False
    else:
        roll_forward = None
    
    # If we're just after a rollback or roll_forward, disable slow.
    if renpy.game.after_rollback:
        slow = False
        
    # If we're committed to skipping this statement, disable slow.
    elif (renpy.config.skipping and
          (renpy.game.preferences.skip_unseen or
           renpy.game.context().seen_current(True))):    
        slow = False

    what = what_prefix + what + what_suffix

    if not interact:
        all_at_once = True

    if all_at_once:
        pause = None
    else:
        pause = 0

    keep_interacting = True
    slow_start = 0

    # Figure out window args.
    window_args = dict(style=window_style, **window_properties)

    # Figure out who and its arguments.
    if who is not None and not image:
        who = who_prefix + who + who_suffix
        who_args = dict(style=who_style, **properties)
    elif who is not None and image:
        who_args = dict(style=who_style, **properties)
    else:
        who_args = dict()

    while keep_interacting:

        # If we're going to do an interaction, then saybehavior needs
        # to be here.
        if interact:            
            behavior = renpy.ui.saybehavior(allow_dismiss=renpy.config.say_allow_dismiss)
        else:
            behavior = None

        # Code to support ctc.
        ctcwhat = [ what ]

        if ctc and ctc_position == "nestled":
            ctcwhat.extend([ " ", ctc ])

        slow_done = SlowDone(ctc, ctc_position, callback, interact)
                
        for c in callback:
            c("show", interact=interact)

            
        what_args = dict(style=what_style,
                         slow=slow,
                         slow_done=slow_done,
                         slow_abortable=slow_abortable,
                         slow_start=slow_start,
                         pause=pause)
            
        what_text = show_function(
            who,
            ctcwhat,
            who_args=who_args,
            what_args=what_args,
            window_args=window_args,
            image=image,
            no_ctc_what=what,
            **show_args)
        
        for c in callback:
            c("show_done", interact=interact)
        
        if behavior and afm:
            behavior.set_afm_length(what_text.get_simple_length() - slow_start)

        if interact:
            rv = renpy.ui.interact(mouse='say', roll_forward=roll_forward)

            # This is only the case if the user has rolled forward, or
            # maybe in some other obscure cases.
            if rv is False:
                break 

        keep_interacting = what_text.get_keep_pausing()
        slow_start = what_text.get_laidout_length()

        if keep_interacting:
            pause += 1

            for i in renpy.config.say_sustain_callbacks:
                i()

    if interact:

        # Store that we have shown the last thing we need to show.
        what_args = dict(style=what_style,
                         slow=False,
                         slow_done=None,
                         slow_abortable=slow_abortable,
                         slow_start=slow_start,
                         pause=pause)

        what_args.update(what_properties)

        renpy.game.context().info._reshow_say = renpy.curry.curry(show_function)(
            who,
            what,
            who_args=who_args,
            what_args=what_args,
            window_args=window_args,
            image=image,
            no_ctc_what=what,
            **show_args)

    # Log this line of dialogue.        
    if who and isinstance(who, (str, unicode)):
        renpy.exports.log(who)
    renpy.exports.log(what)
    renpy.exports.log("")

    # Do the checkpoint and with None.
    if interact:
        renpy.exports.checkpoint(True)

        if with_none is None:
            with_none = renpy.config.implicit_with_none

        if with_none:
            renpy.game.interface.with(None, None)

    for c in callback:
        callback("end", interact=interact)

# Used by copy.
NotSet = object()

class Character(object):
    """
    The character object contains information about a character. When
    passed as the first argument to a say statement, it can control
    the name that is displayed to the user, and the style of the label
    showing the name, the text of the dialogue, and the window
    containing both the label and the dialogue.
    """

    import renpy.config as config

    # Properties beginning with what or window that are treated
    # specially.
    special_properties = [
        'what_prefix',
        'what_suffix',
        'show_function',
        ]

    # When adding a new argument here, remember to add it to copy below.
    def __init__(self, name,
                 who_style='say_label',
                 what_style='say_dialogue',
                 window_style='say_window',
                 function=display_say,
                 predict_function=predict_display_say, 
                 condition=None,
                 dynamic=False,
                 **properties):
        
        self.name = name
        self.who_style = who_style
        self.what_style = what_style
        self.window_style = window_style
        self.properties = properties
        self.what_properties = { }
        self.window_properties = { }
        self.show_args = { }
        self.function = function
        self.predict_function = predict_function
        self.condition = condition
        self.dynamic = dynamic

        for k in list(self.properties):
            if k in self.special_properties:
                continue

            if k.startswith("show_"):
                self.show_args[k[len("show_"):]] = self.properties[k]
                del self.properties[k]
                continue

            if k.startswith("what_"):
                self.what_properties[k[len("what_"):]] = self.properties[k]
                del self.properties[k]
                continue

            if k.startswith("window_"):
                self.window_properties[k[len("window_"):]] = self.properties[k]
                del self.properties[k]
                continue

        for k in list(self.properties):
            if k in self.special_properties:
                continue

            if k.startswith("who_"):
                self.properties[k[len("who_"):]] = self.properties[k]
                del self.properties[k]
                continue
            

            
    def copy(self,
             name=NotSet,
             who_style=NotSet,
             what_style=NotSet,
             window_style=NotSet,
             function=NotSet,
             predict_function=NotSet,
             condition=NotSet,
             dynamic=NotSet,
             **properties):


        rv = Character(name=name,
                       who_style=who_style,
                       what_style=what_style,
                       window_style=window_style,
                       function=function,
                       predict_function=predict_function,
                       condition=condition,
                       dynamic=dynamic,
                       **properties)

        
        def merge(a, b):
            if a is not NotSet:
                return a
            else:
                return b

        def merge_dict(a, b):
            for k, v in b.iteritems():
                if k not in a:
                    a[k] = v
                    
        
        rv.name = merge(rv.name, self.name)
        rv.who_style = merge(rv.who_style, self.who_style)
        rv.what_style = merge(rv.what_style, self.what_style)
        rv.window_style = merge(rv.window_style, self.window_style)
    
        merge_dict(rv.properties, self.properties)
        merge_dict(rv.what_properties, self.what_properties)
        merge_dict(rv.window_properties, self.window_properties)
        merge_dict(rv.show_args, self.show_args)
        
        rv.function = merge(rv.function, self.function)
        rv.predict_function = merge(rv.predict_function, self.predict_function)
        rv.condition = merge(rv.condition, self.condition)
        rv.dynamic = merge(rv.dynamic, self.dynamic)

        return rv
        
    def check_condition(self):
        """
        Returns true if we should show this line of dialogue.
        """

        if self.condition is None:
            return True

        import renpy.python as python

        return python.py_eval(self.condition)
        

    def store_readback(self, who, what):
        """
        This is called when a say occurs, to store the information
        about what is said into the readback buffers.
        """

        return

    def __call__(self, what, **properties):

        props = self.properties.copy()
        props.update(properties)

        if not self.check_condition():
            return

        name = self.name

        if self.dynamic:
            import renpy.python as python            
            name = python.py_eval(name)

        self.function(name, what,
                      who_style=self.who_style,
                      what_style=self.what_style,
                      window_style=self.window_style,
                      what_properties=self.what_properties,
                      window_properties=self.window_properties,
                      show_args=self.show_args,
                      **props)

        self.store_readback(name, what)
        
    def predict(self, what):

        if self.dynamic and self.image:
            return [ ]

        if self.dynamic:
            name = "<Dynamic>"
        else:
            name = self.name

        return self.predict_function(
            name,
            what,
            who_style=self.who_style,
            what_style=self.what_style,
            window_style=self.window_style,
            what_properties=self.what_properties,
            window_properties=self.window_properties,
            show_args=self.show_args,
            **self.properties)
            
def DynamicCharacter(name_expr, **properties):
    """
    A DynamicCharacter is similar to a Character, except that instead
    of having a fixed name, it has an expression that is evaluated to
    produce a name before each line of dialogue is displayed. This allows
    one to have a character with a name that is read from the user, as
    may be the case for the POV character.

    This is now exactly the same as constructing a character with
    dynamic=True.
    """

    return Character(name_expr, dynamic=True, **properties)
