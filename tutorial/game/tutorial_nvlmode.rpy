# Declare an nvl-version of eileen.

example nvl1:
    define nvle = Character(_("Eileen"), color="#c8ffc8", kind=nvl)

define config.adv_nvl_transition = dissolve
define config.nvl_adv_transition = dissolve

example nvl3a:
    define menu = nvl_menu

define menu = renpy.display_menu

define config.lint_ignore_redefine += [ "store.menu" ]

label tutorial_nvlmode:

    window hide
    nvl clear
    nvl show dissolve

    nvle "NVL-style games are games that cover the full screen with text, rather then placing it in a window at the bottom of the screen. Like this."

    show example nvl1 bottom

    nvle "To use NVL-mode, you need to define Characters with a kind=nvl."

    example large bottom:

        nvle "Then just use that character in a say statement."

        nvl clear

        nvle "You use 'nvl clear' to clear the screen when that becomes necessary."

        nvl hide dissolve
        nvl show dissolve

        nvle "The 'nvl show' and 'nvl hide' statements use transitions to show and hide the NVL window."

    # Doing this during the game isn't recommended, it's better to do
    # it in an init block. We have to do it here because we need to use
    # both kinds of menus.
    $ menu = nvl_menu

    show example nvl3a nvl3 large bottom

example nvl3 hide:

    menu:

        nvle "NVL-mode also supports showing menus to the player, providing it's the last thing on the screen. Understand?"

        "Yes.":

            nvl clear

            nvle "Good!"

        "No.":

            nvl clear

            nvle "Well, hopefully the code below makes it a little more clear."


label after_nvl_menu:

    hide example

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
