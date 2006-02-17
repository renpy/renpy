# This is an implementation of Kana mode, a mode in which multiple
# lines of dialogue are shown at once, in a fullscreen window. A
# single line of dialogue is placed onto the screen for each mouse
# click. Calling the clear function clears the screen, ensuring that
# the next line will appear at the top of the sceen.
#
# An example of using Kana mode follows the code that implements it.


# This init block contains all of the code needed to implement
# Kana mode. You probably don't want to change this... unless you
# do. But all of the customization is found below.
init -100:
    python:
        
        # This is a list of KanaCharacter, what tuples.
        kana_display_list = [ ]

        # Spacings used.
        kana_vspacing = 0
        kana_hspacing = 0

        def clear(arg=None):
            global kana_display_list
            kana_display_list = [ ]

        def kana_show():

            if not kana_display_list:
                return

            ui.window(style='say_window')
            ui.vbox(kana_vspacing)

            for i, (char, what) in enumerate(kana_display_list):
                text = char.show(what, i == len(kana_display_list) - 1)

            ui.close()

            # Magic to support auto-forward mode.
            b = ui.saybehavior()
            b.set_afm_length(text.get_simple_length())
            
            ui.interact()
            renpy.checkpoint()            

            
        # Characters and the narrator should be instances of this
        # object.
        class KanaCharacter(object):

            def __init__(self, who,
                         what_prefix='"',
                         what_suffix='"',
                         who_style='say_label',
                         what_style='say_dialogue',
                         **properties):

                self.who = who
                self.what_prefix = what_prefix
                self.what_suffix = what_suffix
                self.who_style = who_style
                self.what_style = what_style
                self.properties = properties

            def __call__(self, what):
                kana_display_list.append((self, what))
                kana_show()

            def show(self, what, slow):
                ui.hbox(kana_hspacing)
                ui.text(self.who, style=self.who_style,
                        **self.properties)

                rv = ui.text(self.what_prefix + what + self.what_suffix,
                             style=self.what_style, slow=slow)

                ui.close()

                return rv


# This section updates the styles that are used by the Kana mode stuff
# so that they work well with Kana mode. The user may want to change
# these so that they look more appropriate.
init:

    # The space between lines of dialogue.
    $ kana_vspacing = 10
    $ kana_hspacing = 10
    
    $ style.say_window.background = Solid((0, 0, 0, 96))
    $ style.say_window.xfill = True
    $ style.say_window.yfill = True
    $ style.say_window.xmargin = 0
    $ style.say_window.ymargin = 0
    $ style.say_window.xpadding = 20
    $ style.say_window.ypadding = 20

    $ style.say_label.minwidth = 100
    $ style.say_label.textalign = 1.0

    # This just makes it look nicer.
    $ style.say_dialogue.rest_indent = 9

    # Adjust the menu to match.
    $ style.menu_window.background = Solid((0, 0, 0, 96))
    $ style.menu_window.xfill = True
    $ style.menu_window.yfill = True
    $ style.menu_window.xmargin = 0
    $ style.menu_window.ymargin = 0
    $ style.menu_window.xpadding = 20
    $ style.menu_window.ypadding = 20

    $ style.menu.xpos = 110

# And now, the example. This example can't be simply run, but instead
# should serve as a guide to how to get Kana mode working in your own
# game.
    
# In the init block, declare the characters as KanaCharacters. We also
# want to declare the narrator as a special KanaCharacter.
init:
    $ p = KanaCharacter("")
    $ g = KanaCharacter("Girl:", color=(255, 128, 128, 255))
    $ narrator = KanaCharacter("",
                               what_prefix='',
                               what_suffix='',
                               what_style='say_thought')


# Now, the actual script of the example. (An excerpt from Moonlight
# Walks.) Notice how we place calls to clear in places where the
# we want the screen to be cleared.

# This text is here to serve as an example, and shouldn't be used
# in your game.
label example:

    show beach2
    show mary dark wistful

    $ clear()
    
    p "What can you tell me about your parents?"

    g "Papa and Mama both came across the ocean as settlers when they
       were just children."

    g "Papa fought in the war. When it was over, he married Mama, and
       they used his pension to move here from the mainland, and to
       build us a house."

    g "Together, they farmed the land, and eventually they had
       children."

    g "I had an older sister and a younger sister. I was the middle
       child."

    $ clear()

    show mary dark sad

    "She paused for a second to collect her thoughts before
     continuing. This part was taking a strain on her."

    g "When I was ten, an epidemic hit the island."

    g "We came down with it, and so did all of the other families."

    g "My family was too sick to move, but our neighbors, the Millers,
       sent some of their boys to get help from the mainland."

    "I remember thinking that Miller was the last name of my aunt and
     uncle, and wondering if they could be related to me."

    g "I don't know what happened to them, but I never heard from them
       again."

    show mary dark crying

    g "It lasted a week, and then it was over. My sisters... my
       parents... they all..."

    g "Now I'm the only one left."

    $ clear()

    p "I'm sorry."

    "I didn't know what else to say to a girl that had lost her
     family, and was obviously broken up about it."

    show mary dark sad

    "She nodded in response, wiped her tears, and we once again
     started walking in silence."

    menu menu_1:
        "Show me the example again.":
            jump example

        "I'm done. Let me go.":
            return
