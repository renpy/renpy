# Declare an nvl-version of eileen.

#begin nvl1
define nvle = Character(_("Eileen"), color="#c8ffc8", kind=nvl)
#end nvl1

define config.adv_nvl_transition = dissolve
define config.nvl_adv_transition = dissolve

#begin nvl3a
define menu = nvl_menu

#end nvl3a

define menu = renpy.display_menu

label tutorial_nvlmode:

    window hide
    nvl clear
    nvl show dissolve

    nvle "NVL-style games are games that cover the full screen with text, rather then placing it in a window at the bottom of the screen. Like this."

    show screen example('nvl1', example_bottom)

    nvle "To use NVL-mode, you need to define Characters with a kind=nvl."

    show screen example('nvl2', example_bottom)

#begin nvl2
    nvle "Then just use that character in a say statement."

    nvl clear

    nvle "You use 'nvl clear' to clear the screen when that becomes necessary."

    nvl hide dissolve
    nvl show dissolve

    nvle "The 'nvl show' and 'nvl hide' statements use transitions to show and hide the NVL window."
#end nvl2


    # Doing this during the game isn't recommended, it's better to do
    # it in an init block. We have to do it here because we need to use
    # both kinds of menus.
    $ menu = nvl_menu

    show screen example([ 'nvl3a', 'nvl3' ], example_bottom)

#begin nvl3
menu:

    nvle "NVL-mode also supports showing menus to the player, providing it's the last thing on the screen. Understand?"

    "Yes.":

        nvl clear

        nvle "Good!"

    "No.":

        nvl clear

        nvle "Well, hopefully the code below makes it a little more clear."
#end nvl3

label after_nvl_menu:

    hide screen example

    nvle "Games can mix NVL-mode and the normal ADV-mode by having some characters that have kind=nvl, and some that do not."

    e "You can specify transitions that occur when going from NVL-mode to ADV-mode."

    nvle "As well as when going from ADV-mode to NVL-mode."

    nvle "Text tags like {{w}{w} work in NVL-mode."

    extend " As does the \"extend\" special character."

    nvle "And that's it for NVL-mode."

    $ menu = renpy.display_menu

    nvl hide dissolve
    $ _last_say_who = None
    window show dissolve

    return
