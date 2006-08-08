# This file contains code that displays an image to the left of a
# character's dialogue, when the character is talking. 
#
# To use it, use the SideCharacter function to declare the character,
# and include a show_side argument containing what the character will say.
#
# For example:
#
#    $ e = Character(u'Eileen', color=(200, 255, 200, 255),
#                    show_side="cyan.png")


init -1:

    python:

        def side_show_say(who, what,
                           who_args={},
                           what_args={},
                           window_args={},
                           image=False,
                           side=None,
                           **kwargs):

            ui.window(**window_args)

            ui.hbox()

            if side:
                ui.image(side)

            ui.vbox(style='say_vbox')

            if who:
                if image:
                    renpy.ui.add(renpy.display.im.image(who, loose=True, **who_args))
                else:
                    renpy.ui.text(who, **who_args)

            rv = renpy.ui.text(what, **what_args)
            ui.close()
            ui.close()

            return rv

        def side_show_predict_say(who, what, side=None, **kwargs):
            rv = renpy.predict_show_display_say(who, what, **kwargs)
            rv.append(Image(side, True))
            return rv

        def SideCharacter(*args, **kwargs):
            return Character(show_function=side_show_say,
                             show_predict_function=side_show_predict_say,
                             *args,
                             **kwargs)
