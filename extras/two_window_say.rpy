# This extra demonstrates the two window say mode. In this mode, the
# character's name is placed in a different window than the line said
# by that character.
#
# You can use this by including this file in your game directory. You
# then need to change the definitions of Character and
# DynamicCharacter object to set function=two_window_say. For example:
#
#     $ e = Character('Eileen', color=(200, 255, 200, 255),
#                     function=two_window_say)
#
# Once this is done, everything that is said by that character will be
# divided across two windows.
#
# You'll probably also want to customize the styles given below,
# especially by setting style.who_window.background to something
# a little more attractive.

init -100:

    python:

        style.create('two_window_say_position', 'default',
                     '(position) Used to get the position of the two windows in two window say mode.')

        style.two_window_say_position.ypos = 1.0
        style.two_window_say_position.yanchor = 'bottom'

        style.create('who_window', 'default',
                     '(window) The style used for the window containing the who label when a Character uses the two_window_say function.')
            
        style.who_window.background = Solid((0, 0, 255, 128))
        style.who_window.xminimum = 150
        style.who_window.xmargin = 10
        style.who_window.xpadding = 10
        style.who_window.ymargin = 5
        style.who_window.ypadding = 5
    

        def two_window_say(who, what,
                           who_style='say_label',
                           what_style='say_dialogue',
                           window_style='say_window',
                           who_window_style='who_window',
                           who_prefix='',
                           who_suffix=': ',
                           what_prefix='',
                           what_suffix='',
                           interact=True,
                           slow=True,
                           **properties):

            if interact:
                ui.saybehavior()

            if who is not None:
                who = who_prefix + who + who_suffix

            what = what_prefix + what + what_suffix

            ui.vbox(style='two_window_say_position')
            
            if who is not None:
                ui.window(style=who_window_style)
                ui.text(who, style=who_style, **properties)

            ui.window(style=window_style)
            ui.text(what, style=what_style, slow=slow)

            ui.close()

            if interact:
                ui.interact()
                renpy.checkpoint()
