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

label screen_layers_label:
    screen_layers_speaker "Dialogue on the screen's layer."
    $ renpy.display_menu([("ADV choice", True)], screen="screen_layers_choice")
    $ renpy.display_menu([("NVL choice", True)], screen="screen_layers_choice", type="nvl")
    screen_layers_default_speaker "Dialogue on the default layer."
    $ renpy.display_menu([("Default ADV choice", True)], screen="screen_layers_default_choice")
    $ renpy.display_menu([("Default NVL choice", True)], screen="screen_layers_default_choice", type="nvl")
    return

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

    testcase declared_and_default_layers:
        run Start("screen_layers_label")
        assert eval renpy.get_screen("screen_layers_say", "overlay") is not None
        assert eval renpy.get_screen("screen_layers_say", "screens") is None
        advance until screen "screen_layers_choice"
        assert eval renpy.get_screen("screen_layers_say", "overlay") is None
        assert eval renpy.get_screen("screen_layers_choice", "overlay") is not None
        click "ADV choice"
        assert eval renpy.get_screen("screen_layers_choice", "overlay") is not None
        click "NVL choice"
        assert eval renpy.get_screen("screen_layers_choice", "overlay") is None
        assert eval renpy.get_screen("screen_layers_default_say", "screens") is not None
        advance until screen "screen_layers_default_choice"
        assert eval renpy.get_screen("screen_layers_default_say", "screens") is None
        assert eval renpy.get_screen("screen_layers_default_choice", "screens") is not None
        click "Default ADV choice"
        assert eval renpy.get_screen("screen_layers_default_choice", "screens") is not None
        click "Default NVL choice"
        assert screen "main_menu"
        assert eval renpy.get_screen("screen_layers_default_choice", "screens") is None
