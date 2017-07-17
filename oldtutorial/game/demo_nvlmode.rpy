# This demonstrates nvl_mode.rpy.

init:

    # Declare an nvl-version of eileen.
    $ nvle = Character(_("Eileen"), color="#c8ffc8", kind=nvl)

    $ config.adv_nvl_transition = dissolve
    $ config.nvl_adv_transition = dissolve

label demo_nvlmode:

    window hide
    nvl clear
    nvl show dissolve

    nvle "NVL-style games are games that cover the full screen with text, rather then placing it in a file at the bottom of the screen."

    nvle "Ren'Py ships with a file, nvl_mode.rpy, that implements NVL-style games. You're seeing an example of NVL-mode at work."

    nvl clear

    nvle "To use NVL-mode, you need to define Characters with a kind=nvl."

    nvle "You use 'nvl clear' to clear the screen when that becomes necessary."

    nvl hide dissolve
    nvl show dissolve

    nvle "The 'nvl show' and 'nvl hide' statements use transitions to show and hide the NVL window."

    nvle "The nvl_erase function removes a line from the screen."

    $ nvl_erase()

    nvle "Like that."

    # Doing this during the game isn't recommended, it's better to do
    # it in an init block. We have to do it here because we need to use
    # both kinds of menus.
    $ menu = nvl_menu

    menu:

        nvle "The nvl_mode also supports showing menus to the user, provided they are the last thing on the screen. Understand?"

        "Yes.":

            nvl clear

            nvle "Good!"

            nvl clear

        "No.":

            nvl clear

            nvle "Well, it might help if you take a look at the demo code."

            nvl clear

    eside "You can specify transitions that occur when going from NVL-mode to ADV-mode."

    nvle "As well as when going from ADV-mode to NVL-mode."

    nvle "Text tags like {{w}{w} work in NVL-mode."

    extend " As does the \"extend\" special character."

    nvle "And that's it for NVL-mode."

    $ menu = renpy.display_menu

    nvl hide dissolve
    $ _last_say_who = None
    window show dissolve

    return
