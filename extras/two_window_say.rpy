# This extra demonstrates the two window say mode. In this mode, the
# character's name is placed in a different window than the line said
# by that character.
#
# You can use this by including this file in your game directory. You
# then need to change the definitions of Character and
# DynamicCharacter object to set show_function=two_window_say. For example:
#
#     $ e = Character('Eileen', color=(200, 255, 200, 255),
#                     show_function=two_window_say)
#
# Once this is done, everything that is said by that character will be
# divided across two windows.
#
# You'll probably also want to customize the styles given below.

init -100:

    python:

        style.create('two_window_say_position', 'default',
                     '(position) Used to get the position of the two windows in two window say mode.')

        style.two_window_say_position.ypos = 1.0
        style.two_window_say_position.yanchor = 'bottom'

        style.create('who_window', 'window',
                     '(window) The style used for the window containing the who label when a Character uses the two_window_say function.')

        style.who_window.xminimum = 200
        style.who_window.yminimum = 50
        style.who_window.xfill = False
        style.who_window.xpos = 0
        style.who_window.xanchor = 0            

        def two_window_say(who, what,
                           who_args={},
                           what_args={},
                           window_args={},
                           image=False,
                           **kwargs):


            ui.vbox(style='two_window_say_position')
            
            if who is not None and image:
                ui.window(style='who_window')
                ui.image(who, **who_args)
            elif who is not None:
                ui.window(style='who_window')
                ui.text(who, **who_args)

            ui.window(**window_args)
            rv = ui.text(what, **what_args)

            ui.close()

            return rv
