# This file tests ATL transforms and replacement behavior.

# ==============
# == Fixtures ==
# ==============

image atl__solid = Solid("#fff", xysize=(100, 100))

default atl__global_alpha = 0.25

init python:
    def atl__state(tag="atl__solid"):
        """
        Returns the transform state of the displayable shown with `tag` on the master layer.
        """

        return renpy.game.context().scene_lists.get_displayable_by_tag("master", tag).state

label atl__parameter_replace__start:
    call .show(_alpha=0.25)

    # Replacing the image copies the old ATL transform after _alpha has left scope.
    show atl__solid

    "Replaced."
    return

label .show(_alpha):
    show atl__solid:
        alpha _alpha
    return

label atl__parameter_hide__start:
    call .show(_alpha=0.25)

    # Hiding the image copies the old ATL transform to run its hide handler.
    hide atl__solid

    "Hidden."
    return

label .show(_alpha):
    show atl__solid:
        on show:
            alpha _alpha
        on hide:
            linear 0.2 alpha 0.0
    return

label atl__global_changed_replace__start:
    $ atl__global_alpha = 0.25

    show atl__solid:
        alpha atl__global_alpha

    "Shown."

    $ atl__global_alpha = 0.75
    show atl__solid

    "Replaced."
    return

label atl__running_replace__start:
    show atl__solid:
        xpos 0.0
        linear 10.0 xpos 1.0

    "Moving."

    show atl__solid

    "Replaced."
    return


# ==============
# === Tests ====
# ==============

testsuite atl:
    after testcase:
        if not screen "main_menu":
            run MainMenu(confirm=False, save=False)

    # GH-7283: Replacing or hiding an image copies its ATL transform. The copy must reuse the
    # compiled block, not re-evaluate the ATL, whose names may have left scope (label parameters
    # are dynamic variables) or changed since it was shown.
    # https://github.com/renpy/renpy/issues/7283

    testcase parameter_replace:
        description "Replacing an image does not re-evaluate inline ATL after its label parameter left scope"
        run Start("atl__parameter_replace__start")
        advance until "Replaced."
        assert eval (atl__state().alpha == 0.25)

    testcase parameter_hide:
        description "Hiding an image runs its on hide handler after its label parameter left scope"
        run Start("atl__parameter_hide__start")
        advance until "Hidden."
        pause 0.4
        assert eval (not renpy.showing("atl__solid"))

    testcase global_changed_replace:
        description "Replacing an image keeps the ATL values it was shown with"
        run Start("atl__global_changed_replace__start")
        advance until "Replaced."
        assert eval (atl__global_alpha == 0.75)
        assert eval (atl__state().alpha == 0.25)

    testcase running_replace:
        description "Replacing an image keeps its running ATL animation going"
        run Start("atl__running_replace__start")
        pause 0.2

        # A restarted animation would move back toward 0.0, so it would fall below this.
        $ atl__xpos_before = atl__state().xpos.relative
        advance
        pause 0.05

        assert eval (atl__xpos_before > 0.0)
        assert eval (atl__state().xpos.relative >= atl__xpos_before)
