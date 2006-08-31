# The Character object (and friends).

import renpy


def predict_show_display_say(who, what, who_args, what_args, window_args, image=False, two_window=False, left_image=False, right_image=False, **kwargs):
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

    if left_image:
        rv.append(renpy.display.im.image(left_image, True))

    if right_image:
        rv.append(renpy.display.im.image(right_image, True))


    return rv

def show_display_say(who, what, who_args={}, what_args={}, window_args={}, image=False, left_image=None, right_image=None, two_window=False, **kwargs):
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

    if two_window:

        # Opens say_two_window_vbox.
        renpy.ui.vbox(style='say_two_window_vbox')

        renpy.ui.window(style='say_who_window')
        handle_who()

    renpy.ui.window(**window_args)
    # Opens the say_vbox.
    renpy.ui.vbox(style='say_vbox')

    if not two_window:
        handle_who()

    if left_image or right_image:        
        # Opens the say_hbox.
        renpy.ui.hbox(style='say_hbox')

    if left_image:
        renpy.ui.image(left_image)

    rv = renpy.ui.text(what, **what_args)

    if right_image:
        renpy.ui.image(right_image)

    if left_image or right_image:
        # Closes the say_hbox.
        renpy.ui.close()

    # Closes the say_vbox.
    renpy.ui.close()

    if two_window:
        # Closes the say_two_window_vbox.
        renpy.ui.close()

    return rv


def predict_display_say(who, what,
                        window_style='say_window',
                        window_properties={},
                        what_style='say_dialogue',
                        what_properties={},
                        who_style='say_label',
                        image=False,
                        ctc=None,
                        show_args={},
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


def display_say(who, what, who_style='say_label',
                what_style='say_dialogue',
                window_style='say_window',
                who_prefix='',
                who_suffix=': ',
                what_prefix='',
                what_suffix='',
                interact=True,
                slow=True,
                slow_speed=None,
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
        with(None)
        
        return

    # If we're just after a rollback, disable slow.
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
            behavior = renpy.ui.saybehavior()
        else:
            behavior = None

        # Code to support ctc.
        ctcwhat = [ what ]

        if ctc and ctc_position == "nestled":
            ctcwhat.extend([ " ", ctc ])

        slow_done = None

        if ctc and ctc_position == "fixed":
            def slow_done():
                renpy.ui.add(ctc)
                renpy.exports.restart_interaction()

                
        what_args = dict(style=what_style,
                         slow=slow,
                         slow_done=slow_done,
                         slow_abortable=slow_abortable,
                         slow_start=slow_start,
                         pause=pause,
                         slow_speed = None,
                         **what_properties)

        what_text = show_function(who, ctcwhat, who_args=who_args, what_args=what_args, window_args=window_args, image=image, **show_args)

        if behavior and afm:
            behavior.set_afm_length(what_text.get_simple_length() - slow_start)

        if interact:
            renpy.ui.interact(mouse='say')

        keep_interacting = what_text.get_keep_pausing()

        if keep_interacting:
            slow_start = what_text.get_laidout_length()
            pause += 1

            for i in renpy.config.say_sustain_callbacks:
                i()

    if who and isinstance(who, (str, unicode)):
        renpy.exports.log(who)
    renpy.exports.log(what)
    renpy.exports.log("")

    if interact:
        renpy.exports.checkpoint()

        if renpy.config.implicit_with_none:
            renpy.game.interface.with(None, None)



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
    
    def __init__(self, name,
                 who_style='say_label',
                 what_style='say_dialogue',
                 window_style='say_window',
                 function=display_say,
                 predict_function=predict_display_say, 
                 condition=None,
                 dynamic=False,
                 **properties):
        """
        @param name: The name of the character, as shown to the user.

        @param who_style: The name of the style that is applied to the
        characters name when it is shown to the user.

        @param what_style: The name of the style that is applied to
        the body of the character's dialogue, when it is shown to the
        user.

        @param window_style: The name of the style of the window
        containing all the dialogue.

        @param who_prefix: A prefix that is prepended to the name.
     
        @param who_suffix: A suffix that is appended to the name. (Defaults to ':')

        @param what_prefix: A prefix that is prepended to the text body.

        @param what_suffix: A suffix that is appended to the text body.

        @param show_function: A function that is called to show each
        step of this dialogue to the user. It should have the same
        signature as renpy.show_display_say.

        @param show_predict_function: A function that is called to predict
        images used by show_function. This should have the same signature
        as renpy.show_predict_function.

        @param function: deprecated, do not change.
        
        @param predict_function: deprecated, do not change.
        
        @param condition: A string containing a python expression, or
        None. If not None, the condition is evaluated when each line
        of dialogue is said. If it evaluates to False, the dialogue is
        not shown to the user.

        @param interact: If True (the default), then each line said
        through this character causes an interaction. If False, then
        the window is added to the screen, but control immediately
        proceeds. You'll need to call ui.interact yourself to show it.

        @param properties: Additional style properties, that are
        applied to the label containing the character's name.

        @param dynamic: If true, the name is interpreted as a python
        expression, which is evaluated to get the name that will be
        used by the rest of the code.

        @param image: If true, the name is considered to be the name
        of an image, which is rendered in place of the who label.

        @param ctc: If present, this is interpreted as a widget that
        is displayed when all text is shown to the user, prompting the
        user to click to continue. Animation or anim.Blink is a good
        choice for this sort of widget, as is Image.

        @param ctc_position: If "nestled", the ctc widget is
        displayed nestled in with the end of the text. If
        "fixed", the ctc widget is displayed directly on the screen,
        with its various position properties determining where it is
        actually shown.

        @param interact: If True, the default, an interaction will
        take place when the character speaks. Otherwise, no such
        interaction will take place.

        In addition, Character objects also take properties. If a
        property is prefixed with window_, it is applied to the
        window. If prefixed with what_, it is applied to the text
        being spoken. If prefixed with show_, properties are passed as keyword arguments
        to the show_ and predict_ functions. Unprefixed properties are applied to the who
        label, the name of the character speaking.
        """
        
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
