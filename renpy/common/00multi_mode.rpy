# Copyright 2004-2013 Tom Rothamel <pytom@bishoujo.us>
# Copyright 2013 Koichi Akabe <vbkaisetsu@gmail.com>
# See LICENSE.txt for license details.

# This is an implementation of Multi-mode, which can be used to show
# dialogue in a separeted screen. Each dialogues are not removed
# while other characters are speaking.

##############################################################################
# The implementation of Multi mode lives below this line.

init -1500 python:

    # Styles that are used by multi mode.
    style.create('multi_window', 'say_window', 'the window containing multi-mode dialogue')
    style.create('multi_hbox', 'hbox', 'the hbox containing each box of multi-mode dialogue')
    style.create('multi_child_label_dual', 'say_label', 'the name of the character speaking dialogue in dual-mode')
    style.create('multi_child_dialogue_dual', 'say_dialogue', 'used for dialogue text in dual-mode')
    style.create('multi_child_window_dual', 'default', 'windows containing dialogue and thoughts in dual-mode')

    style.multi_hbox.box_spacing = 10

    # Set up dual mode styles.
    style.multi_child_window_dual.xminimum = int(config.screen_width / 2) - 5
    style.multi_child_window_dual.xmaximum = int(config.screen_width / 2) - 5

    # A hook that delta wanted, that is called instead of renpy.show_display_say
    config.multi_show_display_say = renpy.show_display_say

    # A list of arguments that have been passed to multi_record_show.
    multi_list = []
    multi_cols = {}

    multi_current_col = []

    multi_current_group = None

    # If set, then all of the multi-specific style get indexed with this.
    multi_variant = None

    # Returns the appropriate variant style.
    def __ms(s):
        if multi_variant:
            return s[multi_variant]
        else:
            return s

    def __multi_screen_dialogue():
        """
         Returns widget_properties and dialogue for the current Multi
         mode screen.
         """

        widget_properties = { }
        dialogue = [ ]

        for i, entry in enumerate(multi_list):
            if not entry:
                continue

            who, what, kwargs = entry

            who_id = "who%d" % i
            what_id = "what%d" % i
            window_id = "window%d" % i

            widget_properties[who_id] = kwargs["who_args"]
            widget_properties[what_id] = kwargs["what_args"]
            widget_properties[window_id] = kwargs["window_args"]

            dialogue.append((who, what, who_id, what_id, window_id))

        return widget_properties, dialogue

    def __multi_show_screen(screen_name, **scope):
        """
         Shows an multi-mode screen. Returns the "what" widget.
         """

        widget_properties, dialogue = __multi_screen_dialogue()

        renpy.show_screen(screen_name, _transient=True, _widget_properties=widget_properties, dialogue=dialogue, **scope) 
        renpy.shown_window()

        return [renpy.get_widget(screen_name, "what%d" % i) for i in multi_current_col]

    def multi_show_core(who=None, what=None):
         # Screen version.
        if renpy.has_screen("multi_%s" % multi_current_group):
            return __multi_show_screen("multi_%s" % multi_current_group, items=[ ])
        if renpy.has_screen("multi"):
            return __multi_show_screen("multi", items=[ ])

        if renpy.in_rollback():
            multi_window = __ms(style.multi_window)['rollback']
            multi_hbox = __ms(style.multi_hbox)['rollback']
        else:
            multi_window = __ms(style.multi_window)
            multi_hbox = __ms(style.multi_hbox)

        ui.window(style=multi_window)
        ui.hbox(style=multi_hbox)

        rv = []

        for col, i in enumerate(multi_list):
            if not i:
                continue

            who, what, kw = i
            rv_tmp = config.multi_show_display_say(who, what, variant=multi_variant, **kw)
            if col in multi_current_col:
                rv.append(rv_tmp)

        ui.close()

        renpy.shown_window()

        return rv

    def multi_window():
        multi_show_core()

    def multi_show(with_):
        multi_show_core()
        renpy.with_statement(with_)
        store._last_say_who = "multi"

    def multi_hide(with_):
        multi_show_core()
        renpy.with_statement(None)
        renpy.with_statement(with_)
        store._last_say_who = None

    class MultiCharacter(ADVCharacter):

        def __init__(self, 
                     who=renpy.character.NotSet,
                     kind=None,
                     col=0,
                     group=None,
                     **properties):

            if kind is None:
                kind = store.multi

            if group is None:
                group = "dual"
            self.group = group

            if not group in store.multi_cols:
                store.multi_cols[group] = 1

            if store.multi_cols[group] <= col:
                store.multi_cols[group] = col + 1
            self.col = col

            if not "who_style" in properties:
                properties["who_style"] = "multi_child_label_%s" % group
            if not "what_style" in properties:
                properties["what_style"] = "multi_child_dialogue_%s" % group
            if not "window_style" in properties:
                properties["window_style"] = "multi_child_window_%s" % group

            ADVCharacter.__init__(
                self, 
                who,
                kind=kind,
                **properties)

        def do_add(self, who, what):

            if store.multi_current_group != self.group or not store.multi_list:
                kwargs = self.show_args.copy()
                kwargs["what_args"] = self.what_args
                kwargs["who_args"] = self.who_args
                kwargs["window_args"] = self.window_args
                store.multi_list = [("", "", kwargs) for i in range(0, store.multi_cols[self.group])]
                store.multi_current_group = self.group

            kwargs = self.show_args.copy()
            kwargs["what_args"] = self.what_args
            kwargs["who_args"] = self.who_args
            kwargs["window_args"] = self.window_args

            store.multi_list[self.col] = (who, what, kwargs)
            store.multi_current_col.append(self.col)

        def do_display(self, who, what, **display_args):

            renpy.display_say(
                who,
                what,
                multi_show_core,
                **display_args)

        def do_done(self, who, what):
            store.multi_current_col = []

    # The default MultiCharacter.
    multi = MultiCharacter(
        type='multi',
        mode='multi',
        kind=adv)

    def multi_clear():
        store.multi_list = []

    # Run clear at the start of the game.
    config.start_callbacks.append(multi_clear)

    config.multi_adv_transition = None
    config.adv_multi_transition = None

    # This is used to execute the multi and adv mode transitions.
    def _multi_adv_callback(mode, old_modes):

        old = old_modes[0]

        if config.adv_multi_transition:
            if mode == "multi":
                if old == "say" or old == "menu":
                    multi_show(config.adv_multi_transition)

        if config.multi_adv_transition:
            if mode == "say" or mode == "menu":
                if old == "multi":
                    multi_hide(config.multi_adv_transition)

        # Clear dialogues automatically
        if old == "multi":
            multi_clear()

    config.mode_callbacks.append(_multi_adv_callback)

python early hide:

    def parse_multi_clear(l):
        if not l.eol():
            renpy.error('expected end of line')

        return None

    def execute_multi_clear(parse):
        multi_clear()

    def scry_multi_clear(parse, scry):
        scry.multi_clear = True

    renpy.statements.register('multi clear',
                              parse=parse_multi_clear,
                              execute=execute_multi_clear,
                              scry=scry_multi_clear)

    
