# Copyright 2004-2013 Tom Rothamel <pytom@bishoujo.us>
# See LICENSE.txt for license details.

init python:

    layout.provides('main_menu')
    renpy.load_module("_layout/imagemap_common")

    # The ground image.
    config.main_menu_ground = { }

    # The selected/hover image.
    config.main_menu_selected = { }

    # The idle image.
    config.main_menu_idle = { }

    # The hotspots. Each hotspot is defined by a tuple giving:
    # - The x-coordinate of the left side.
    # - The y-coordinate of the top side.
    # - The x-coordinate of the right side.
    # - The y-coordinate of the bottoms side.
    # - Either the (untranslated) name of the main menu button this hotspot
    #   is equivalent to, or, a label in the program to jump to when this
    #   hotspot is clicked.
    config.main_menu_hotspots = { }

    # This can be set from user code to define the main menu variant to use.
    _main_menu_variant = None

label main_menu_screen:

    python hide:

        # Ignore right-click while at the main menu.
        ui.keymap(game_menu=ui.returns(None))

        # Show the background.
        ui.window(style='mm_root')
        ui.null()

        ime = _ImageMapper(
            None,
            config.main_menu_ground,
            config.main_menu_idle,
            config.main_menu_selected,
            config.main_menu_idle,
            config.main_menu_selected,
            config.main_menu_hotspots,
            navigation=False,
            variant=_main_menu_variant)

        for e in config.main_menu:
            if len(e) == 4:
                name, act, enabled, shown = e
            else:
                name, act, enabled = e
                shown = "True"

            if not eval(shown):
                ime.nothing(name)

            if not eval(enabled):
                act = None

            if isinstance(act, basestring):
                act = ui.jumpsoutofcontext(act)

            ime.button(name, act, False)

        for i in list(ime.remaining_hotspots):
            ime.button(i, ui.jumpsoutofcontext(i), None)

        ime.close()
        ui.interact(mouse='mainmenu')

    jump main_menu_screen
