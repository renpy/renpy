## This file tests the statements of the test language in renpy/test/testast.py that the more specific
## test_test_testast_*.rpy files don't cover, such as how they wait for and skip transitions in the game.

# ==============
# == Fixtures ==
# ==============

# The delay of the screens layer transition in testast_layer_transition.
default testast_transition_delay = 0.1

# Set once the say statement in testast_layer_transition has been dismissed.
default testast_transition_said = False

# Set by testast_transition_button, which only receives events once the transition on the screens layer has
# finished or been skipped.
default testast_transition_clicked = False

screen testast_transition_button():
    textbutton "Transition Button":
        align (0.5, 0.5)
        action [ SetVariable("testast_transition_clicked", True), Return(True) ]

# A layer transition stays in the interface's ongoing transitions until the interaction ends, even after it has
# finished, so it is still recorded while the say statement waits for a click.
label testast_layer_transition:
    scene expression Solid("#000")
    with None
    show screen testast_transition_button
    $ renpy.transition({ "screens" : Dissolve(testast_transition_delay) })
    "Ready."
    $ testast_transition_said = True
    return


# ================
# == Test cases ==
# ================

testsuite testast_transitions:
    after testcase:
        $ _test.transition_timeout = 0.05

        if not screen "main_menu":
            run MainMenu(confirm=False, save=False)

    # The first parameter set has a transition that finishes well before the transition timeout, so move and click
    # must run as soon as it finishes; waiting for the timeout instead would exceed _test.timeout. The second has a
    # transition far longer than the timeout, so they skip it once and then run, rather than wrapping their state on
    # every frame until a RecursionError. In both, the button is on the transitioning layer, so a click sent before
    # the transition finished or was skipped would be ignored.
    testcase input_after_layer_transition:
        parameter (delay, transition_timeout) = [ (0.5, 10.0), (60.0, 0.05) ]

        $ store.testast_transition_delay = delay
        $ store.testast_transition_said = False
        $ store.testast_transition_clicked = False
        $ _test.transition_timeout = transition_timeout

        run Jump("testast_layer_transition")
        pause until eval renpy.get_mode() == "say"

        move pos (10, 10)
        assert eval renpy.get_mouse_pos() == (10, 10)

        click "Transition Button"
        assert eval testast_transition_clicked
        assert eval testast_transition_said
