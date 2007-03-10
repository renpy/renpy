# This is an implementation of Kana mode, a mode in which Ren'Py
# emulates the NVL-style games. Multiple lines of dialogue are shown
# on the screen at once, whenever a line of dialogue is said by a
# KanaCharacter. Calling the clear function clears the screen,
# ensuring that the the next line will appear at the top of the
# screen.


##############################################################################
# This is some sample code, demonstrating how to use Kana mode.

init:
    python:

        # First, we want to declare a character to be a
        # KanaCharacter. This character will always speak in
        # Kana mode.
        ke = KanaCharacter("Eileen", color="#cfc")

        # We re-declare the narrator as a Kana character, so narration
        # will be spoken in Kana mode.
        narrator = KanaCharacter(" ", who_suffix="")


        # style.kana_window:
        # The window containing the Kana mode.
        style.kana_window.background = "#0008"
        style.kana_window.yfill = True
        style.kana_window.xfill = True
        style.kana_window.xpadding = 20
        style.kana_window.ypadding = 20

        # style.kana_vbox:
        # The vbox containing all of the entries.
        style.kana_vbox.box_spacing = 10

        # style.kana_entry:
        # The windows containing each entry, individually.

        # style.kana_label
        # The label giving who is speaking.
        style.kana_label.minwidth = 150
        style.kana_label.text_align = 1.0

        # style.kana_dialogue
        # Dialogue being spoken by a KanaCharacter.
        
        

        # We can also display menus in Kana mode. When this is done,
        # the menu will be displayed at the bottom of the current
        # screen of text. 

        # Redefine the menu display function.
        menu = kana_menu

        # NOTE: These styles will not be used until 5.6.3 comes out.
        # Use style.menu_choice, style.menu_choice_button, etc. until then.

        # style.kana_menu_window:

        # style.kana_menu_choice:
        style.kana_menu_choice.idle_color = "#0ff"
        style.kana_menu_choice.hover_color = "#ff0"

        # style.kana_menu_choice_chosen:

        # style.kana_menu_choice_button:
        style.kana_menu_choice_button.left_margin = 160
        style.kana_menu_choice_button.right_margin = 20
        style.kana_menu_choice_button.xfill = True
        style.kana_menu_choice_button.hover_background = "#F0F2"

        # style.kana_menu_choice_button_chosen:
        

label kana_mode:

    show bg whitehouse

    $ kana_clear()

    ke "Kana mode is a mode in which we display more then one line
            of dialogue on the screen at once."

    "We can also display lines of narration."

    ke "This mode attempts to emulate the NVL style games."

    ke "It's named after the game {i}Kana: Little Sister{/i}, which was
       the first game that we played using the style."

    $ kana_clear()

    ke "To use this mode, you need to declare KanaCharacters rather then Characters."

    ke "You can also use the kana_clear function to clear the screen."

    menu:

        ke "Kana mode also supports menus. Do you understand?"

        "I understand.":
            return

        "Tell me again.":
            jump splashscreen

            
        
##############################################################################
# The implementation of Kana mode lives below this line.

init -100:

    python:

        # Styles that are used by kana mode.
        style.create('kana_window', 'default')
        style.create('kana_vbox', 'vbox')
        style.create('kana_label', 'say_label')
        style.create('kana_dialogue', 'say_dialogue')
        style.create('kana_entry', 'default')

        style.create('kana_menu_window', 'default')
        style.create('kana_menu_choice', 'default')
        style.create('kana_menu_choice_chosen', 'kana_menu_choice')
        style.create('kana_menu_choice_button', 'default')
        style.create('kana_menu_choice_chosen_button', 'kana_menu_choice_button')
        

        # A list of arguments that have been passed to kana_record_show.
        kana_list = None

        def kana_show(*args, **kwargs):

            kana_list[-1] = (args, kwargs)

            ui.window(style='kana_window')
            ui.vbox(style='kana_vbox')

            for i in kana_list:
                if not i:
                    continue

                a, kw = i                
                rv = renpy.show_display_say(*a, **kw)

            ui.close()

            return rv

        class KanaCharacter(Character):

            def __init__(self, who,
                         show_say_vbox_properties={ 'box_layout' : 'horizontal' },
                         who_style='kana_label',
                         what_style='kana_dialogue',
                         window_style='kana_entry',
                         **kwargs):

                Character.__init__(self, who,
                                   show_say_vbox_properties=show_say_vbox_properties,
                                   who_style=who_style,
                                   what_style=what_style,
                                   window_style=window_style,
                                   show_function=kana_show,
                                   **kwargs)

            def __call__(self, *args, **kwargs):
                if kana_list is None:
                    store.kana_list = [ ]

                kana_list.append(None)
                rv =  Character.__call__(self, *args, **kwargs)

                # Prevent this from being slow on later displays.
                if kana_list[-1]:
                    kana_list[-1][1]["what_args"]["slow"] = False
                

        def kana_clear():
            global kana_list
            kana_list = [ ]

        def kana_menu(items):

            # Clear out the previous scene list, as we will need to redraw
            # it.
            renpy.with(None)

            if kana_list is None:
                store.kana_list = [ ]

            ui.window(style='kana_window')
            ui.vbox(style='kana_vbox')

            for i in kana_list:
                if not i:
                    continue

                a, kw = i            
                rv = renpy.show_display_say(*a, **kw)

            renpy.display_menu(items, interact=False,
                               window_style='kana_menu_window',
                               choice_style='kana_menu_choice',
                               choice_chosen_style='kana_menu_choice_chosen',
                               choice_button_style='kana_menu_choice_button',
                               choice_chosen_button_style='kana_menu_choice_chosen_button',
                               )

            ui.close()

            rv = ui.interact()
            
            renpy.checkpoint()

            return rv
