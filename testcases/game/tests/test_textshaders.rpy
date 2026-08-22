# Tests for text shaders

# ==============
# == Fixtures ==
# ==============

label textshaders__cps__label:
    "{cps=40}This appears one letter at a time at a speed of 40 characters per second{/cps}"

# ==============
# === Tests ====
# ==============

testsuite textshaders:
    after testcase:
        if not screen "main_menu":
            run MainMenu(confirm=False, save=False)

    testcase respect_cps_tag:
        description "Typewriter shader follows {cps} when preferences.text_cps = 0"
        # GH-7242: Text shaders should follow the line's {cps} value even if
        # `preferences.text_cps` is set to instant text
        # https://github.com/renpy/renpy/issues/7242

        run Preference("text speed", 0)
        $ renpy.game.style.default.textshader = None
        $ renpy.game.style.rebuild()

        run Start("textshaders__cps__label")
        assert "This appears"
        pause 0.5
        screenshot "textshaders/cps.png" max_pixel_difference 200 crop (0, 440, 740, 80)
        advance until screen "main_menu"

        $ renpy.game.style.default.textshader = "typewriter"
        $ renpy.game.style.rebuild()

        run Start("textshaders__cps__label")
        assert "This appears"
        pause 0.5
        screenshot "textshaders/cps.png" max_pixel_difference 200 crop (0, 440, 740, 80)
        advance until screen "main_menu"
