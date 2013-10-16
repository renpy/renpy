# Copyright 2004-2013 Tom Rothamel <pytom@bishoujo.us>
# See LICENSE.txt for license details.

init -1400 python:

    # basics: The width of a thumbnail.
    config.thumbnail_width = 66

    # basics: The height of a thumbnail.
    config.thumbnail_height = 50

    class Layout():
        def __call__(self, func):
            setattr(self, func.func_name, func)
            return func

    layout = _layout =  Layout()
    del Layout

    layout.compat_funcs = [ ]
    layout.provided = set()

    # This is used to jump to a label with a transition.
    def _intra_jumps_core(label, transition):
        renpy.transition(getattr(config, transition))
        renpy.jump(label)

    _intra_jumps = renpy.curry(_intra_jumps_core)

    # These are obsoleted by screens, but used by layout code.
    config.main_menu = [
        (u"Start Game", "start", "True"),
        (u"Load Game", _intra_jumps("load_screen", "main_game_transition"), "True"),
        (u"Preferences", _intra_jumps("preferences_screen", "main_game_transition"), "True"),
        (u"Help", _help, "True", "config.help"),
        (u"Quit", ui.jumps("_quit"), "True"),
        ]

    config.game_menu = [
        ( None, u"Return", ui.jumps("_return"), 'True'),
        ( "preferences", u"Preferences", _intra_jumps("preferences_screen", "intra_transition"), 'True' ),
        ( "save", u"Save Game", _intra_jumps("save_screen", "intra_transition"), 'not main_menu' ),
        ( "load", u"Load Game", _intra_jumps("load_screen", "intra_transition"), 'True'),
        ( None, u"Main Menu", ui.callsinnewcontext("_main_menu_prompt"), 'not main_menu' ),
        ( "help", u"Help", _help, "True", "config.help"),
        ( None, u"Quit", ui.callsinnewcontext("_quit_prompt"), 'True' ),
        ]

# These are used by layout-based code, and also by the screens code when a layout
# is used to invoke the screen.
label _quit_prompt:
    $ renpy.loadsave.force_autosave()

    if layout.invoke_yesno_prompt(None, layout.QUIT):
        jump _quit
    else:
        return

label _main_menu_prompt:
    $ renpy.loadsave.force_autosave()

    if layout.yesno_prompt(None, layout.MAIN_MENU):
        $ renpy.full_restart(transition=config.game_main_transition)
    else:
        return

init -1400 python hide:

    # Called to indicate that the given kind of layout has been
    # provided.
    @layout
    def provides(kind):

        if kind in layout.provided:
            raise Exception("%s has already been provided by another layout function." % kind)

        layout.provided.add(kind)

    # Called by registered themes to have the default versions of
    # various kinds of layouts provided, if a more specific version
    # has not been requested by the user.
    @layout
    def defaults():

        # Do nothing, in compatibility mode.
        if 'compat' in layout.provided:
            return

        defaults = dict(
            main_menu=layout.classic_main_menu,
            load_save=layout.classic_load_save,
            navigation=layout.classic_navigation,
            yesno_prompt=layout.classic_yesno_prompt,
            preferences=layout.classic_preferences,
            joystick_preferences=layout.classic_joystick_preferences,
            )

        if renpy.has_screen("main_menu"):
            defaults["main_menu"] = layout.screen_main_menu

        if renpy.has_screen("load") and renpy.has_screen("save"):
            defaults["load_save"] = layout.screen_load_save

        if renpy.has_screen("yesno_prompt"):
            defaults["yesno_prompt"] = layout.screen_yesno_prompt

        if renpy.has_screen("preferences"):
            defaults["preferences"] = layout.screen_preferences

        if renpy.has_screen("joystick_preferences"):
            defaults["joystick_preferences"] = layout.screen_joystick_preferences

        for k, v in defaults.iteritems():
            if k not in layout.provided:
                v()

        if store._game_menu_screen is None:
            if renpy.has_label("save_screen"):
                store._game_menu_screen = "save_screen"
            elif renpy.has_label("preferences_screen"):
                store._game_menu_screen = "preferences_screen"


    ##########################################################################
    # These live on the layout object, and ease the construction of buttons,
    # labels, and prompts. A sufficently aggressive layout might change
    # these.

    @layout
    def button(label,
               type=None,
               selected=False,
               enabled=True,
               clicked=None,
               hovered=None,
               unhovered=None,
               index=None,
               **properties):

        """
         label - The label of this button. Will be translated if necessary.
         type - The type of this button. Used to generate the appropriate styles.
         selected - Determines if this button should be selected.
         enabled - Determines if this button should be enabled.
         clicked - A function that is run when the button is clicked.
         hovered - A function that is run when the button is hovered.
         unhovered - A function that is run when the button is unhovered.
         index - A style index. If None, label is used.
         size_group - The size_group used by this button.
         """

        if not enabled:
            clicked = None

        if selected and enabled:
            role = "selected_"
        else:
            role = ""

        if type:
            button_style = type + "_button"
            text_style = type + "_button_text"
        else:
            button_style = 'button'
            text_style = 'button_text'

        if index is None:
            index = label

        button_style = getattr(style, button_style)[index]
        text_style = getattr(style, text_style)[index]

        rv = ui.button(style=button_style, role=role, clicked=clicked, hovered=hovered, unhovered=unhovered, **properties)
        ui.text(_(label), style=text_style)

        return rv

    @layout
    def label(label, type, suffix="label", index=None, **properties):

        if index is None:
            index = label

        if type:
            label_style = getattr(style, type + "_" + suffix)[index]
            text_style = getattr(style, type + "_" + suffix + "_text")[index]
        else:
            label_style = style.label[index]
            text_style = style.label_text[index]

        ui.window(style=label_style, **properties)
        ui.text(_(label), style=text_style)

    @layout
    def prompt(label, type, index=None, **properties):
        return layout.label(label, type, "prompt", index, **properties)

    @layout
    def list(entries, clicked=None, hovered=None, unhovered=None, selected=None, **properties):

        ui.window(style=style.list, **properties)
        ui.vbox(style=style.list_box)

        size_group = str(id(entries))

        for i, (spacers, content) in enumerate(entries):
            if clicked is not None:
                new_clicked = renpy.curry(clicked)(i)
            else:
                new_clicked = None

            if hovered is not None:
                new_hovered = renpy.curry(hovered)(i)
            else:
                new_hovered = None

            if unhovered is not None:
                new_unhovered = renpy.curry(unhovered)(i)
            else:
                new_unhovered = None

            if selected == i:
                role = "selected_"
            else:
                role = ""

            ui.button(style=style.list_row[i%2],
                      clicked=new_clicked,
                      hovered=new_hovered,
                      unhovered=new_unhovered,
                      role=role,
                      size_group=size_group,
                      )

            ui.hbox(style=style.list_row_box)

            for j in range(0, spacers):
                ui.window(style=style.list_spacer)
                ui.null()

            ui.text(content, style=style.list_text)

            ui.close() # row

        ui.close() # vbox

    ##########################################################################
    # Misc.

    @layout
    def button_menu():

        config.narrator_menu = True

        style.menu.box_spacing = 2
        style.menu_window.set_parent(style.default)
        style.menu_window.xalign = 0.5
        style.menu_window.yalign = 0.5
        style.menu_choice.set_parent(style.button_text)
        style.menu_choice.clear()
        style.menu_choice_button.set_parent(style.button)
        style.menu_choice_button.xminimum = int(config.screen_width * 0.75)
        style.menu_choice_button.xmaximum = int(config.screen_width * 0.75)

    store._button_menu = button_menu

    ###########################################################################
    # Compat layout.

    @layout
    def compat():
        layout.provides('compat')
        renpy.load_module("_compat/styles")
        renpy.load_module("_compat/library")
        renpy.load_module("_compat/mainmenu")
        renpy.load_module("_compat/gamemenu")
        renpy.load_module("_compat/preferences")
        renpy.load_module("_compat/themes")

    ###########################################################################
    # Classic layout.

    @layout
    def classic_main_menu():
        renpy.load_module("_layout/classic_main_menu")

    @layout
    def classic_navigation():
        renpy.load_module('_layout/classic_navigation')

    @layout
    def classic_load_save():
        renpy.load_module('_layout/classic_load_save')

    @layout
    def classic_yesno_prompt():
        renpy.load_module('_layout/classic_yesno_prompt')

    @layout
    def classic_preferences(center=False):
        renpy.load_module('_layout/classic_preferences')

        if center:
            style.prefs_button.xalign = 0.5
            style.prefs_slider.xalign = 0.5
            style.prefs_jump_button.xalign = 0.5

    @layout
    def classic_joystick_preferences():
        renpy.load_module('_layout/classic_joystick_preferences')

    @layout
    def two_column_preferences():
        renpy.load_module("_layout/two_column_preferences")

    @layout
    def one_column_preferences():
        renpy.load_module("_layout/one_column_preferences")

    @layout
    def grouped_main_menu(per_group=2, equal_size=True):
        renpy.load_module("_layout/grouped_main_menu")
        config.main_menu_per_group = per_group

        if equal_size:
            style.mm_button.size_group = "main_menu"


    @layout
    def grouped_navigation(per_group=2, equal_size=True):
        renpy.load_module("_layout/grouped_navigation")
        config.navigation_per_group = per_group

        if equal_size:
            style.gm_nav_button.size_group = "navigation"

    @layout
    def scrolling_load_save():
        renpy.load_module("_layout/scrolling_load_save")


    @layout
    def imagemap_main_menu(ground, selected, hotspots, idle=None, variant=None):
        renpy.load_module("_layout/imagemap_main_menu")

        config.main_menu_ground[variant] = ground
        config.main_menu_selected[variant] = selected
        config.main_menu_hotspots[variant] = hotspots
        config.main_menu_idle[variant] = idle

    @layout
    def imagemap_navigation(ground, idle, hover, selected_idle, selected_hover,
                            hotspots):

        renpy.load_module("_layout/imagemap_navigation")

        config.navigation_ground = ground
        config.navigation_idle = idle
        config.navigation_hover = hover
        config.navigation_selected_idle = selected_idle
        config.navigation_selected_hover = selected_hover
        config.navigation_hotspots = hotspots

    @layout
    def imagemap_preferences(ground, idle, hover, selected_idle, selected_hover,
                            hotspots):

        renpy.load_module("_layout/imagemap_preferences")

        config.preferences_ground = ground
        config.preferences_idle = idle
        config.preferences_hover = hover
        config.preferences_selected_idle = selected_idle
        config.preferences_selected_hover = selected_hover
        config.preferences_hotspots = hotspots

    @layout
    def imagemap_yesno_prompt(ground, idle, hover, hotspots, prompt_images={ }):

        renpy.load_module("_layout/imagemap_yesno_prompt")

        config.yesno_prompt_ground = ground
        config.yesno_prompt_idle = idle
        config.yesno_prompt_hover = hover
        config.yesno_prompt_hotspots = hotspots
        config.yesno_prompt_message_images = prompt_images

    @layout
    def imagemap_load_save(ground, idle, hover, selected_idle, selected_hover,
                           hotspots, variant=None):

        renpy.load_module("_layout/imagemap_load_save")

        config.load_save_ground[variant] = ground
        config.load_save_idle[variant] = idle
        config.load_save_hover[variant] = hover
        config.load_save_selected_idle[variant] = selected_idle
        config.load_save_selected_hover[variant] = selected_hover
        config.load_save_hotspots[variant] = hotspots

    @layout
    def screen_main_menu():
        renpy.load_module("_layout/screen_main_menu")

    @layout
    def screen_load_save():
        renpy.load_module("_layout/screen_load_save")

    @layout
    def screen_preferences():
        renpy.load_module("_layout/screen_preferences")

    @layout
    def screen_joystick_preferences():
        renpy.load_module("_layout/screen_joystick_preferences")

    @layout
    def screen_yesno_prompt():
        renpy.load_module("_layout/screen_yesno_prompt")

    layout.ARE_YOU_SURE = _("Are you sure?")
    layout.DELETE_SAVE = _("Are you sure you want to delete this save?")
    layout.OVERWRITE_SAVE = _("Are you sure you want to overwrite your save?")
    layout.LOADING = _("Loading will lose unsaved progress.\nAre you sure you want to do this?")
    layout.QUIT = _("Are you sure you want to quit?")
    layout.MAIN_MENU = _("Are you sure you want to return to the main menu?\nThis will lose unsaved progress.")
    layout.SLOW_SKIP = _("Are you sure you want to begin skipping?")
    layout.FAST_SKIP_UNSEEN = _("Are you sure you want to skip to the next choice?")
    layout.FAST_SKIP_SEEN = _("Are you sure you want to skip to unseen dialogue or the next choice?")

    config.enter_yesno_transition = None
    config.exit_yesno_transition = None

    @layout
    def invoke_yesno_prompt(*args):

        _enter_menu()

        if config.enter_yesno_transition:
            renpy.transition(config.enter_yesno_transition)

        rv = layout.yesno_prompt(*args)

        if config.exit_yesno_transition:
            renpy.transition(config.exit_yesno_transition)

        return rv

    @layout
    def yesno_screen(message, yes=None, no=None):
        """
         :doc: other

         This causes the a yes/no prompt screen with the given message
         to be displayed. The screen will be hidden when the user hits
         yes or no.

         `message`
             The message that will be displayed.

         `yes`
             An action that is run when the user chooses yes.

         `no`
             An action that is run when the user chooses no.
         """

        if renpy.has_screen("yesno_prompt"):

            yes_action = [ Hide("yesno_prompt", config.exit_yesno_transition) ]
            no_action = [ Hide("yesno_prompt", config.exit_yesno_transition) ]

            if yes is not None:
                yes_action.append(yes)
            if no is not None:
                no_action.append(no)

            if config.enter_yesno_transition:
                renpy.transition(config.enter_yesno_transition)

            renpy.show_screen(
                "yesno_prompt",
                message=message,
                yes_action=yes_action,
                no_action=no_action)

            renpy.restart_interaction()

            return

        if renpy.invoke_in_new_context(layout.invoke_yesno_prompt, None, message):
            if yes is not None:
                yes()
        else:
            if no is not None:
                no()


    def __auto_save_extra_info():
        return save_name

    config.auto_save_extra_info = __auto_save_extra_info

