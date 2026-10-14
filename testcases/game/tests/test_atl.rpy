# This file tests ATL transforms and replacement behavior.

# ==============
# == Fixtures ==
# ==============

image atl__inline_parameter_scope__solid = Solid("#fff")

label atl__inline_parameter_scope__start:
    call .show(_alpha=0.0)

    show atl__inline_parameter_scope__solid

    "The image was replaced without re-evaluating the previous ATL block."
    return

label .show(_alpha):
    show atl__inline_parameter_scope__solid:
        alpha _alpha
    return


# ==============
# === Tests ====
# ==============

testsuite atl:
    after testcase:
        if not screen "main_menu":
            run MainMenu(confirm=False, save=False)

    testcase inline_parameter_scope:
        description "Does not re-evaluate replaced inline ATL outside its parameter scope"
        # GH-7283: Replacing an image after returning from a parameterized label must not
        # evaluate the old inline ATL block after the label parameter has left scope.
        # https://github.com/renpy/renpy/issues/7283
        run Start("atl__inline_parameter_scope__start")
        pause 0.1

        python:
            entry = renpy.game.context().scene_lists.get_displayable_by_tag(
                "master", "atl__inline_parameter_scope__solid"
            )
            assert entry is not None
            assert entry.state.alpha == 0.0
