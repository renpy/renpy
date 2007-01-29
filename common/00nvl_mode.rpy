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

init -100:

    python:

        # Styles that are used by nvl mode.
        style.create('nvl_window', 'default')
        style.create('nvl_vbox', 'vbox')
        style.create('nvl_label', 'say_label')
        style.create('nvl_dialogue', 'say_dialogue')
        style.create('nvl_entry', 'default')

        style.create('nvl_menu_window', 'default')
        style.create('nvl_menu_choice', 'default')
        style.create('nvl_menu_choice_chosen', 'nvl_menu_choice')
        style.create('nvl_menu_choice_button', 'default')
        style.create('nvl_menu_choice_chosen_button', 'nvl_menu_choice_button')
        

        # A list of arguments that have been passed to nvl_record_show.
        nvl_list = None

        def nvl_show_core():
        
            ui.window(style='nvl_window')
            ui.vbox(style='nvl_vbox')

            rv = None
            
            for i in nvl_list:
                if not i:
                    continue

                a, kw = i                
                rv = renpy.show_display_say(*a, **kw)

            ui.close()

            return rv

            
        def nvl_show_function(*args, **kwargs):
 
            nvl_list[-1] = (args, kwargs)
            
            rv = nvl_show_core()
                
            nvl_list[-1][1]["what_args"]["slow"] = False
            nvl_list[-1][1]["what_args"]["slow_done"] = None
                
            return rv

        def nvl_show(with):
            nvl_show_core()
            renpy.with(with)

        def nvl_hide(with):
            nvl_show_core()
            renpy.with(None)
            renpy.with(with)
            
        class NVLCharacter(Character):

            def __init__(self, who,
                         show_say_vbox_properties={ 'box_layout' : 'horizontal' },
                         who_style='nvl_label',
                         what_style='nvl_dialogue',
                         window_style='nvl_entry',
                         **kwargs):

                Character.__init__(self, who,
                                   show_say_vbox_properties=show_say_vbox_properties,
                                   who_style=who_style,
                                   what_style=what_style,
                                   window_style=window_style,
                                   show_function=nvl_show_function,
                                   **kwargs)

            def __call__(self, *args, **kwargs):
                if nvl_list is None:
                    store.nvl_list = [ ]

                nvl_list.append(None)
                rv = Character.__call__(self, *args, **kwargs)


        def nvl_clear():
            global nvl_list
            nvl_list = [ ]

        # Run clear at the start of the game.
        config.start_callbacks.append(nvl_clear)
            
        def nvl_menu(items):

            # Clear out the previous scene list, as we will need to redraw
            # it.
            renpy.with(None)

            if nvl_list is None:
                store.nvl_list = [ ]

            ui.window(style='nvl_window')
            ui.vbox(style='nvl_vbox')

            for i in nvl_list:
                if not i:
                    continue

                a, kw = i            
                rv = renpy.show_display_say(*a, **kw)

            renpy.display_menu(items, interact=False,
                               window_style='nvl_menu_window',
                               choice_style='nvl_menu_choice',
                               choice_chosen_style='nvl_menu_choice_chosen',
                               choice_button_style='nvl_menu_choice_button',
                               choice_chosen_button_style='nvl_menu_choice_chosen_button',
                               )

            ui.close()

            roll_forward = renpy.roll_forward_info()
            
            rv = ui.interact(roll_forward=roll_forward)
            renpy.checkpoint(rv)

            return rv

python early hide:

    def parse_nvl_show_hide(l):
        rv = l.simple_expression()
        if rv is None:
            renpy.error('expected simple expression')

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

    renpy.statements.register('nvl clear',
                              parse=parse_nvl_clear,
                              execute=execute_nvl_clear)

    
