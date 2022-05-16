# Copyright 2004-2022 Tom Rothamel <pytom@bishoujo.us>
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

# This is an implementation of NVL-mode, which can be used to show
# dialogue in a fullscreen way, like NVL-style games. Multiple lines
# of dialogue are shown on the screen at once, whenever a line of
# dialogue is said by a NVLCharacter. Calling the nvl_clear function
# clears the screen, ensuring that the the next line will appear at
# the top of the screen.
#
# You can also have menus appear on the screen, by running:
#
# init:
#     $ menu = nvl_menu
#
# It's also possible to make the narrator a NVLCharacter, using code like:
#
# init:
#     $ narrator = NVLCharacter(None)

##############################################################################
# The implementation of NVL mode lives below this line.


# The language of the entries in nvl_list. If the language changes, this
# is updated and the list is reset.
default _nvl_language = None

init -1500 python:

    # Styles that are used by nvl mode.
    style.create('nvl_window', 'default', 'the window containing nvl-mode dialogue')
    style.create('nvl_vbox', 'vbox', 'the vbox containing each box of nvl-mode dialogue')
    style.create('nvl_label', 'say_label', 'an nvl-mode character\'s name')
    style.create('nvl_dialogue', 'say_dialogue', 'nvl-mode character dialogue')
    style.create('nvl_thought', 'nvl_dialogue', 'nvl-mode character thoughts')
    style.create('nvl_entry', 'default', 'a window containing each line of nvl-mode dialogue')

    style.create('nvl_menu_window', 'default', 'a window containing an nvl-mode menu')
    style.create('nvl_menu_choice', 'default', 'an nvl-mode menu choice')
    style.create('nvl_menu_choice_chosen', 'nvl_menu_choice', 'an nvl-mode menu choice that has been chosen')
    style.create('nvl_menu_choice_button', 'default', 'an nvl-mode choice button')
    style.create('nvl_menu_choice_chosen_button', 'nvl_menu_choice_button', 'an nvl-mode choice button that\'s been chosen.')

    # Set up nvl mode styles.
    style.nvl_label.minwidth = 150
    style.nvl_label.text_align = 1.0

    style.nvl_window.background = "#0008"
    style.nvl_window.yfill = True
    style.nvl_window.xfill = True
    style.nvl_window.xpadding = 20
    style.nvl_window.ypadding = 30

    style.nvl_vbox.box_spacing = 10

    style.nvl_menu_choice.idle_color = "#0ff"
    style.nvl_menu_choice.hover_color = "#ff0"
    style.nvl_menu_choice_button.left_margin = 160
    style.nvl_menu_choice_button.right_margin = 20
    style.nvl_menu_choice_button.xfill = True
    style.nvl_menu_choice_button.hover_background = "#F0F2"

    # nvlmode: The CTC indicator to use when at the end of an NVL page.
    config.nvl_page_ctc = None

    # nvlmode: The position of the CTC indicator used at the end of an NVL page.
    config.nvl_page_ctc_position = "nestled"

    # Should we used paged rollback?
    config.nvl_paged_rollback = False

    # A hook that delta wanted, that is called instead of renpy.show_display_say
    config.nvl_show_display_say = renpy.show_display_say

    # The layer the nvl screens are shown on.
    config.nvl_layer = "screens"

    # The maximum number of entries in nvl_list.
    config.nvl_list_length = None

    # A list of arguments that have been passed to nvl_record_show.
    nvl_list = None

    # If set, then all of the nvl-specific style get indexed with this.
    nvl_variant = None

    # Returns the appropriate variant style.
    def __s(s):
        if nvl_variant:
            return s[nvl_variant]
        else:
            return s

    class _NVLEntry(tuple):
        """
        NVLEntry objects are added to the list of dialogue that's
        shown on the screen.
        """

    def __nvl_screen_dialogue():
        """
         Returns widget_properties and dialogue for the current NVL
         mode screen.
         """

        dialogue = [ ]
        kwargs = { }
        widget_properties = { }

        for i, entry in enumerate(nvl_list):
            if not entry:
                continue

            who, what, kwargs = entry

            kwargs.setdefault("properties", { })
            kwargs.setdefault("multiple", None)

            if i == len(nvl_list) - 1:
                who_id = "who"
                what_id = "what"
                window_id = "window"

                for k, v in kwargs["properties"].items():
                    widget_properties[k + str(i)] =  v

            else:

                who_id = "who%d" % i
                what_id = "what%d" % i
                window_id = "window%d" % i

                for k, v in kwargs["properties"].items():
                    widget_properties[k] =  v

            widget_properties[who_id] = kwargs["who_args"]
            widget_properties[what_id] = kwargs["what_args"]
            widget_properties[window_id] = kwargs["window_args"]

            e = _NVLEntry((who, what, who_id, what_id, window_id))

            e.current = (i == (len(nvl_list) - 1))

            e.who = who
            e.what = what

            e.who_id = who_id
            e.what_id = what_id
            e.window_id = window_id

            e.who_args = kwargs["who_args"]
            e.what_args = kwargs["what_args"]
            e.window_args = kwargs["window_args"]
            e.properties = kwargs["properties"]

            e.multiple = kwargs["multiple"]

            dialogue.append(e)

        show_args = dict(kwargs)
        if show_args:
            del show_args["who_args"]
            del show_args["what_args"]
            del show_args["window_args"]

            show_args.pop("properties", None)
            show_args.pop("multiple", None)

        return widget_properties, dialogue, show_args

    def __nvl_show_screen(screen_name, **scope):
        """
         Shows an nvl-mode screen. Returns the "what" widget.
         """

        widget_properties, dialogue, show_args = __nvl_screen_dialogue()
        scope.update(show_args)

        renpy.show_screen(screen_name, _layer=config.nvl_layer, _transient=True, _widget_properties=widget_properties, dialogue=dialogue, **scope)
        renpy.shown_window()

        return renpy.get_widget(screen_name, "what", config.nvl_layer)

    def nvl_show_core(who=None, what=None, multiple=None):

         # Screen version.
        if renpy.has_screen("nvl"):
            return __nvl_show_screen("nvl", items=[ ])

        if renpy.in_rollback():
            nvl_window = __s(style.nvl_window)['rollback']
            nvl_vbox = __s(style.nvl_vbox)['rollback']
        else:
            nvl_window = __s(style.nvl_window)
            nvl_vbox = __s(style.nvl_vbox)

        ui.window(style=nvl_window)
        ui.vbox(style=nvl_vbox)

        rv = None

        for i in nvl_list:
            if not i:
                continue

            who, what, kw = i
            kw = dict(kw)
            kw.setdefault("show_say_vbox_properties",  { 'box_layout' : 'horizontal' }),
            rv = config.nvl_show_display_say(who, what, variant=nvl_variant, **kw)

        ui.close()

        renpy.shown_window()

        return rv

    def nvl_window():
        nvl_show_core()

    def nvl_show(with_):
        """
        :doc: nvl

        The Python equivalent of the ``nvl show`` statement.

        `with_`
            The transition to use to show the NVL-mode window.
        """

        nvl_show_core()
        renpy.with_statement(with_)
        store._last_say_who = "nvl"

    def nvl_hide(with_):
        """
        :doc: nvl

        The Python equivalent of the ``nvl hide`` statement.

        `with_`
            The transition to use to hide the NVL-mode window.
        """

        nvl_show_core()
        renpy.with_statement(None)
        renpy.with_statement(with_)
        store._last_say_who = None

    def nvl_erase():
        if nvl_list:
            nvl_list.pop()

    # Check to see if one of the next statements is nvl clear.
    def nvl_clear_next():

        # The number of statements forward to look.
        count = 10

        scry = renpy.scry()
        scry = scry.next()

        while count and scry:

            count -= 1
            if scry.nvl_clear:
                return True

            if scry.interacts:
                return False

            scry = scry.next()

    @renpy.pure
    class NVLCharacter(ADVCharacter):

        def __init__(self,
                     who=renpy.character.NotSet,
                     kind=None,
                     **properties):

            if kind is None:
                kind = store.nvl

            if "clear" in properties:
                self.clear = properties.pop("clear")
            else:
                self.clear = kind.clear

            ADVCharacter.__init__(
                self,
                who,
                kind=kind,
                **properties)

        def push_nvl_list(self, who, what, multiple=None):

            kwargs = self.show_args.copy()
            kwargs["properties"] = dict(self.properties)
            kwargs["what_args"] = dict(self.what_args)
            kwargs["who_args"] = dict(self.who_args)
            kwargs["window_args"] = dict(self.window_args)
            kwargs["multiple"] = multiple

            if multiple:

                def multiple_style(k):
                    style = kwargs[k]["style"]
                    style = "block{}_multiple{}_{}".format(multiple[0], multiple[1], style)
                    kwargs[k]["style"] = style

                multiple_style("what_args")
                multiple_style("who_args")
                multiple_style("window_args")

            store.nvl_list.append((who, what, kwargs))

        def pop_nvl_list(self):
            if store.nvl_list:
                store.nvl_list.pop()

        def do_add(self, who, what, multiple=None):

            if store.nvl_list is None:
                store.nvl_list = [ ]

            if store._nvl_language != _preferences.language:
                store.nvl_list = [ ]
                store._nvl_language = _preferences.language

            while config.nvl_list_length and (len(nvl_list) + 1 > config.nvl_list_length):
                nvl_list.pop(0)

        def do_display(self, who, what, multiple=None, **display_args):

            page = self.clear or nvl_clear_next()

            if config.nvl_page_ctc and page:
                display_args["ctc"] = renpy.easy.displayable_or_none(config.nvl_page_ctc)
                display_args["ctc_position"] = config.nvl_page_ctc_position

            if config.nvl_paged_rollback:
                if page:
                    checkpoint = True
                else:
                    if renpy.roll_forward_info() is not None:
                        renpy.checkpoint(renpy.roll_forward_info(), hard=False)
                        return

                    checkpoint = False
            else:
                checkpoint = True

            if multiple is not None:
                self.push_nvl_list(who, what, multiple=multiple)
            else:
                self.push_nvl_list(who, what)

            renpy.display_say(
                who,
                what,
                nvl_show_core,
                checkpoint=checkpoint,
                multiple=multiple,
                **display_args)

            self.pop_nvl_list()

        def do_done(self, who, what, multiple=None):

            if multiple is not None:
                self.push_nvl_list(who, what, multiple=multiple)
            else:
                self.push_nvl_list(who, what)

            if multiple is None:
                start = -1
            elif multiple[0] == multiple[1]:
                start = -multiple[0]
            else:
                start = 0

            for i in range(start, 0):
                nvl_list[i][2]["what_args"]["alt"] = ""
                nvl_list[i][2]["who_args"]["alt"] = ""

            if self.clear:
                nvl_clear()

            self.add_history("nvl", who, what)

        def do_extend(self):
            renpy.mode(self.mode)
            store.nvl_list = store.nvl_list[:-1]

            self.pop_history()


    # The default NVLCharacter.
    nvl = NVLCharacter(
        who_style='nvl_label',
        what_style='nvl_dialogue',
        window_style='nvl_entry',
        type='nvl',
        mode='nvl',
        clear=False,
        kind=adv)

    nvl_narrator = NVLCharacter(
        who_style='nvl_label',
        what_style='nvl_thought',
        window_style='nvl_entry',
        type='nvl',
        mode='nvl',
        clear=False,
        kind=adv)

    def nvl_clear():
        """
        :doc: nvl

        The Python equivalent of the ``nvl clear`` statement.
        """

        store.nvl_list = [ ]

    # Run clear at the start of the game.
    config.start_callbacks.append(nvl_clear)


    def nvl_menu(items):
        """
        :doc: nvl

        A Python function that displays a menu in NVL style. This is rarely
        used directly. Instead, it's assigned to the :var:`menu` variable,
        using something like::

            define menu = nvl_menu
        """


        renpy.mode('nvl_menu')
        renpy.shown_window()

        if nvl_list is None:
            store.nvl_list = [ ]

        screen = None

        if renpy.has_screen("nvl_choice"):
            screen = "nvl_choice"
        elif renpy.has_screen("nvl"):
            screen = "nvl"

        if screen is not None:

            widget_properties, dialogue, show_args = __nvl_screen_dialogue()
            scope = show_args.copy()
            scope["dialogue"] = dialogue

            return renpy.display_menu(
                items,
                widget_properties=widget_properties,
                screen=screen,
                scope=scope,
                window_style=__s(style.nvl_menu_window),
                choice_style=__s(style.nvl_menu_choice),
                choice_chosen_style=__s(style.nvl_menu_choice_chosen),
                choice_button_style=__s(style.nvl_menu_choice_button),
                choice_chosen_button_style=__s(style.nvl_menu_choice_chosen_button),
                type="nvl",
                )


        # Traditional version.
        ui.layer("transient")
        ui.clear()
        ui.close()

        ui.window(style=__s(style.nvl_window))
        ui.vbox(style=__s(style.nvl_vbox))

        for i in nvl_list:
            if not i:
                continue

            who, what, kw = i
            kw = dict(kw)
            kw.setdefault("show_say_vbox_properties",  { 'box_layout' : 'horizontal' }),
            rv = renpy.show_display_say(who, what, **kw)

        renpy.display_menu(items, interact=False,
                           window_style=__s(style.nvl_menu_window),
                           choice_style=__s(style.nvl_menu_choice),
                           choice_chosen_style=__s(style.nvl_menu_choice_chosen),
                           choice_button_style=__s(style.nvl_menu_choice_button),
                           choice_chosen_button_style=__s(style.nvl_menu_choice_chosen_button),
                           )

        ui.close()

        roll_forward = renpy.roll_forward_info()

        rv = ui.interact(roll_forward=roll_forward)
        renpy.checkpoint(rv)

        return rv

    NVLSpeaker = NVLCharacter

    config.nvl_adv_transition = None
    config.adv_nvl_transition = None


    # This is used to execute the nvl and adv mode transitions.
    def _nvl_adv_callback(mode, old_modes):

        old = old_modes[0]

        if config.adv_nvl_transition:
            if mode == "nvl" or mode == "nvl_menu":
                if old == "say" or old == "menu":
                    nvl_show(config.adv_nvl_transition)

        if config.nvl_adv_transition:
            if mode == "say" or mode == "menu":
                if old == "nvl" or old == "nvl_menu":
                    nvl_hide(config.nvl_adv_transition)

    config.mode_callbacks.append(_nvl_adv_callback)

python early hide:

    def parse_nvl_show_hide(l):
        rv = l.simple_expression()
        if rv is None:
            rv = "None"

        if not l.eol():
            renpy.error('expected end of line')

        return rv

    def lint_nvl_show_hide(trans):
        _try_eval(trans, 'transition')

    def execute_nvl_show(trans):
        nvl_show(eval(trans))

    def execute_nvl_hide(trans):
        nvl_hide(eval(trans))

    renpy.statements.register("nvl show",
                              parse=parse_nvl_show_hide,
                              execute=execute_nvl_show,
                              lint=lint_nvl_show_hide)

    renpy.statements.register("nvl hide",
                              parse=parse_nvl_show_hide,
                              execute=execute_nvl_hide,
                              lint=lint_nvl_show_hide)

    def parse_nvl_clear(l):
        if not l.eol():
            renpy.error('expected end of line')

        return None

    def execute_nvl_clear(parse):
        nvl_clear()

    def scry_nvl_clear(parse, scry):
        scry.nvl_clear = True

    renpy.statements.register('nvl clear',
                              parse=parse_nvl_clear,
                              execute=execute_nvl_clear,
                              scry=scry_nvl_clear,
                              translatable=True)
