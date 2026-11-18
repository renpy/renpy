## This file tests the layers that the say and choice screens are shown on.

# ==============
# == Fixtures ==
# ==============

screen screen_layers_say(who, what):
    layer "overlay"
    text what id "what"

screen screen_layers_choice(items):
    layer "overlay"
    vbox:
        for item in items:
            textbutton item.caption action item.action

screen screen_layers_default_say(who, what):
    text what id "what"

screen screen_layers_default_choice(items):
    vbox:
        for item in items:
            textbutton item.caption action item.action

define screen_layers_speaker = Character(None, screen="screen_layers_say")
define screen_layers_default_speaker = Character(None, screen="screen_layers_default_say")

default screen_layers_menu_type = "menu"

label screen_layers_say_label:
    screen_layers_speaker "Dialogue on the screen's layer."
    return

label screen_layers_choice_label:
    $ renpy.display_menu([("Declared choice", True)], screen="screen_layers_choice", type=screen_layers_menu_type)
    return

label screen_layers_default_say_label:
    screen_layers_default_speaker "Dialogue on the default layer."
    return

label screen_layers_default_choice_label:
    $ renpy.display_menu(
        [("Default choice", True)], screen="screen_layers_default_choice", type=screen_layers_menu_type)
    return

init python:

    def screen_layers_restore_config(old_config):
        """
        Sets each config variable in the dict `old_config` back to its saved value.
        """

        for name, value in old_config.items():
            setattr(config, name, value)

# ==============
# === Tests ====
# ==============

testsuite screen_layers:
    setup:
        $ _test.screen_layers_old_config = (config.say_layer, config.choice_layer, config.nvl_choice_layer)
        $ config.say_layer = None
        $ config.choice_layer = None
        $ config.nvl_choice_layer = None

    teardown:
        $ config.say_layer, config.choice_layer, config.nvl_choice_layer = _test.screen_layers_old_config
        $ del _test.screen_layers_old_config

    after testcase:
        if not screen "main_menu":
            run MainMenu(confirm=False, save=False)

    testcase declared_say:
        description "With no configured layer, dialogue is shown on the layer its screen declares."

        run Start("screen_layers_say_label")
        pause until screen "screen_layers_say"
        assert eval renpy.get_screen("screen_layers_say", "overlay") is not None
        assert eval renpy.get_screen("screen_layers_say", "screens") is None

    testcase declared_choice:
        description "With no configured layer, ADV and NVL menus are shown on the layer their screen declares."

        parameter screen_layers_menu_type = ["menu", "nvl"]

        run Start("screen_layers_choice_label")
        pause until screen "screen_layers_choice"
        assert eval renpy.get_screen("screen_layers_choice", "overlay") is not None
        assert eval renpy.get_screen("screen_layers_choice", "screens") is None

        click "Declared choice"
        assert screen "main_menu"
        assert eval renpy.get_screen("screen_layers_choice", "overlay") is None

    testcase default_say:
        description "A dialogue screen that declares no layer is shown on the screens layer."

        run Start("screen_layers_default_say_label")
        pause until screen "screen_layers_default_say"
        assert eval renpy.get_screen("screen_layers_default_say", "screens") is not None
        assert eval renpy.get_screen("screen_layers_default_say", "overlay") is None

    testcase default_choice:
        description "An ADV or NVL menu screen that declares no layer is shown on the screens layer."

        parameter screen_layers_menu_type = ["menu", "nvl"]

        run Start("screen_layers_default_choice_label")
        pause until screen "screen_layers_default_choice"
        assert eval renpy.get_screen("screen_layers_default_choice", "screens") is not None
        assert eval renpy.get_screen("screen_layers_default_choice", "overlay") is None

        click "Default choice"
        assert screen "main_menu"
        assert eval renpy.get_screen("screen_layers_default_choice", "screens") is None

    testsuite script_version:
        description "Setting config.script_version to a release before 8.6 restores the old layer defaults."

        # Setting an old script_version changes more config variables than the layers. This saves and
        # restores all those that the 8.5 compatibility code sets, and the script version itself.
        setup:
            $ _test.compat_names = (
                "say_layer", "choice_layer", "nvl_choice_layer", "audio_directory", "audio_directories",
                "late_audio_scan", "add_to_special_directories", "scene_uses_tag_layer", "mesh_oversample",
                "glsl_version", "live2d_pose", "live2d_old_beziers")
            $ _test.compat_old = dict((_n, getattr(config, _n)) for _n in _test.compat_names)
            $ _test.compat_script_version = config.script_version

        teardown:
            $ screen_layers_restore_config(_test.compat_old)
            $ config.script_version = _test.compat_script_version
            $ del _test.compat_names, _test.compat_old, _test.compat_script_version

        before testcase:
            $ config.say_layer = None
            $ config.choice_layer = None
            $ config.nvl_choice_layer = None

        testcase layers:
            description "Releases up to 8.5.99 use the screens layer; later ones leave the layers unset."

            # _set_script_version does nothing when RENPY_EXPERIMENTAL is set.
            enabled ("RENPY_EXPERIMENTAL" not in os.environ)

            parameter (compat_version, compat_layer) = [
                ((8, 5, 0), "screens"), ((8, 5, 99), "screens"), ((8, 6, 0), None), ((9, 0, 0), None)]

            $ config.script_version = compat_version
            assert eval (config.say_layer == compat_layer)
            assert eval (config.choice_layer == compat_layer)
            assert eval (config.nvl_choice_layer == compat_layer)
