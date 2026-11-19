## This file tests how text selectors match dialogue, which renpy/test/testfocus.py takes from the say statement.

##############################
## Fixtures
##############################

default testfocus_name = "Robin"

# The second and third lines are grouped with nvl clear, which is translatable, so each is a multi-statement
# translate block rather than a single translated say statement.
label testfocus_translate:
    "Apple for [testfocus_name]." id testfocus_one
    nvl clear
    "Banana for [testfocus_name]." id testfocus_two
    nvl clear
    "Cherry for [testfocus_name]." id testfocus_three
    "Damson for [testfocus_name]." id testfocus_four
    voice sustain
    "{i}Elder{/i} for [testfocus_name]." id testfocus_five
    return

# A say statement translated by a say statement.
translate testfocus testfocus_one:
    "Pomme pour [testfocus_name]."

# A block translated by a block.
translate testfocus testfocus_two:
    nvl clear
    "Banane pour [testfocus_name]."

# A block translated by a say statement, as when a translator drops the nvl clear.
translate testfocus testfocus_three:
    "Cerise pour [testfocus_name]."

# A say statement translated by a block.
translate testfocus testfocus_four:
    nvl clear
    "Prune pour [testfocus_name]."

# A block that is grouped by voice, the most common way, with text tags that are not displayed.
translate testfocus testfocus_five:
    voice sustain
    "{i}Sureau{/i} pour [testfocus_name]."


##############################
## Test cases
##############################

testsuite testfocus_translate:
    teardown:
        run Language(None)

    after testcase:
        if not screen "main_menu":
            run MainMenu(confirm=False, save=False)

    # Without raw, a text selector matches the dialogue as displayed: in the current language, and interpolated.
    # With raw, it matches the dialogue as written in the original-language script. Both hold whichever of a say
    # statement or a block the original and the translation are.
    testcase displayed_and_raw:
        parameter (language, one, two, three, four, five) = [(None, "Apple for Robin.", "Banana for Robin.", "Cherry for Robin.", "Damson for Robin.", "Elder for Robin."), ("testfocus", "Pomme pour Robin.", "Banane pour Robin.", "Cerise pour Robin.", "Prune pour Robin.", "Sureau pour Robin.")]

        $ _test.transition_timeout = 0.00
        run Language(language)
        run Start("testfocus_translate")

        assert text one timeout 2.0
        assert "Apple for [testfocus_name]." raw
        advance

        assert text two timeout 2.0
        assert "Banana for [testfocus_name]." raw
        advance

        assert text three timeout 2.0
        assert "Cherry for [testfocus_name]." raw
        advance

        assert text four timeout 2.0
        assert "Damson for [testfocus_name]." raw
        advance

        assert text five timeout 2.0
        assert "{i}Elder{/i} for [testfocus_name]." raw

    # On a translated line, the original-language dialogue is not displayed, and the translated dialogue is not
    # what the script says, so neither matches in the other mode.
    testcase translated_excludes_other_mode:
        $ _test.transition_timeout = 0.00
        run Language("testfocus")
        run Start("testfocus_translate")

        assert "Pomme pour" timeout 2.0
        assert not "Apple for"
        assert not "Pomme pour" raw
        advance

        assert "Banane pour" timeout 2.0
        assert not "Banana for"
        assert not "Banane pour" raw
        advance

        assert "Cerise pour" timeout 2.0
        assert not "Cherry for"
        assert not "Cerise pour" raw
        advance

        assert "Prune pour" timeout 2.0
        assert not "Damson for"
        assert not "Prune pour" raw
        advance

        assert "Sureau pour" timeout 2.0
        assert not "Elder for"
        assert not "Sureau" raw
