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

# Child fixtures. Images are shown as atl__person so they can be replaced by tag.

# Tall enough to show above the say window.
image atl__red = Solid("#f00", xysize=(100, 300))
image atl__yellow = Solid("#ff0", xysize=(100, 300))
image atl__blue = Solid("#00f", xysize=(100, 300))
image atl__dynamic = "[atl__color]"

default atl__color = "atl__red"

transform atl__move:
    xpos 0.0
    linear 10.0 xpos 1.0

transform atl__wrap(child):
    child

transform atl__contains(child):
    contains:
        child

# Shows child, then atl__blue from 0.3 to 0.6 seconds, then child again.
transform atl__swap(child):
    animation
    child
    0.3
    "atl__blue"
    0.3
    child

# atl__swap, run inside a parallel block that is executing when the child is replaced.
transform atl__swap_parallel(child):
    animation
    parallel:
        child
        0.3
        "atl__blue"
        0.3
        child
    parallel:
        alpha 1.0

# atl__swap, run inside a choice block that is executing when the child is replaced.
transform atl__swap_choice(child):
    animation
    choice:
        child
        0.3
        "atl__blue"
        0.3
        child

init python:
    def atl__names(d):
        """
        Returns the names of the images d currently displays, following each transform's current
        child rather than every displayable its ATL block refers to.
        """

        if d is None:
            return []

        if isinstance(d, renpy.display.image.ImageReference):
            if isinstance(d.target, renpy.display.image.DynamicImage):
                return atl__names(d.target)

            return [" ".join(d.name)]

        if isinstance(d, renpy.display.image.DynamicImage):
            return atl__names(d.target)

        if isinstance(d, renpy.display.transform.Transform):
            return atl__names(d.child)

        rv = []

        for i in getattr(d, "children", ()):
            rv.extend(atl__names(i))

        return rv

    def atl__shown(tag="atl__person"):
        """
        Returns the names of the images displayed by the master layer entry with `tag`.
        """

        return atl__names(renpy.game.context().scene_lists.get_displayable_by_tag("master", tag))

    def atl__transition_from():
        """
        Returns the names of the images on the master layer that the current transition starts from.
        """

        return atl__names(renpy.game.interface.transition_from.get("master"))

    def atl__pixel():
        """
        Returns the (r, g, b, a) color of the last frame drawn, 200 virtual pixels above the
        bottom center of the screen. The default transform places the images there, above the
        say window.
        """

        surf = renpy.display.draw.screenshot(renpy.game.interface.surftree)
        w, h = surf.get_size()

        return tuple(surf.get_at((w // 2, h - 200 * h // config.screen_height)))

    def atl__transition_started():
        """
        Returns true once the transition on the master layer has drawn its first frame.
        """

        interface = renpy.game.interface
        return "master" in interface.ongoing_transition and interface.transition_time.get("master") is not None

label atl__child_replace(t):
    if t is None:
        show atl__red as atl__person:
            alpha 0.5
    else:
        show atl__red as atl__person at t

    "Red."

    show atl__yellow as atl__person

    "Yellow."
    return

label atl__child_replace__inline:
    call atl__child_replace(None)
    return

label atl__child_replace__move:
    call atl__child_replace(atl__move)
    return

label atl__child_replace__wrap:
    call atl__child_replace(atl__wrap)
    return

label atl__child_replace__contains:
    call atl__child_replace(atl__contains)
    return

label atl__child_replace__swap:
    call atl__child_replace(atl__swap)
    return

label atl__child_replace__swap_parallel:
    call atl__child_replace(atl__swap_parallel)
    return

label atl__child_replace__swap_choice:
    call atl__child_replace(atl__swap_choice)
    return

label atl__child_reshow__start:
    show atl__red as atl__person at atl__swap

    "Red."

    show atl__yellow as atl__person at atl__swap

    "Yellow."
    return

label atl__child_layer_dissolve(t):
    $ atl__color = "atl__red"

    scene
    show layer master at t
    show atl__dynamic as atl__person

    "Red."

    $ atl__color = "atl__yellow"
    with {"master": Dissolve(2.0)}

    "Dissolving."
    return

label atl__child_layer_dissolve__plain:
    call atl__child_layer_dissolve(Transform())
    return

label atl__child_layer_dissolve__wrap:
    call atl__child_layer_dissolve(atl__wrap)
    return

label atl__child_layer_dissolve__contains:
    call atl__child_layer_dissolve(atl__contains)
    return

label atl__child_layer_dissolve__swap:
    call atl__child_layer_dissolve(atl__swap)
    return

# Duplication fixtures.

# A displayable that isn't a transform, containing a running ATL transform.
define atl__moving_fixed = Fixed(At("atl__red", atl__move), fit_first=True)

# Dissolves from red to yellow, then interrupts that dissolve to dissolve to blue.
image atl__dissolving:
    "atl__red"
    0.3
    "atl__yellow" with Dissolve(1.0)
    0.3
    "atl__blue" with Dissolve(1.0)

init python:
    def atl__find(d, predicate):
        """
        Returns the first displayable in the tree under `d` that `predicate` is true for, following the
        targets of image references and the children of transforms and containers.
        """

        if d is None:
            return None

        if predicate(d):
            return d

        if isinstance(d, renpy.display.image.ImageReference):
            return atl__find(d.target, predicate)

        for i in getattr(d, "children", ()):
            rv = atl__find(i, predicate)

            if rv is not None:
                return rv

        return None

    def atl__find_shown(tag, predicate):
        """
        Returns the first displayable `predicate` is true for, under the master layer entry with `tag`.
        """

        return atl__find(renpy.game.context().scene_lists.get_displayable_by_tag("master", tag), predicate)

    def atl__moving(tag):
        """
        Returns the running atl__move transform shown with `tag`.
        """

        return atl__find_shown(tag, lambda d: isinstance(d, renpy.display.transform.ATLTransform))

    def atl__shown_red():
        """
        Returns the atl__red image shown by atl__dissolving, outside of any transition.
        """

        return atl__find_shown(
            "atl__person",
            lambda d: isinstance(d, renpy.display.image.ImageReference) and d.name == ("atl__red",),
        )

    def atl__dissolve():
        """
        Returns the outermost dissolve shown by atl__dissolving, or None if no dissolve is shown.
        """

        return atl__find_shown("atl__person", lambda d: isinstance(d, renpy.display.transition.Dissolve))

label atl__show_expression__start:
    show expression atl__moving_fixed as atl__first
    show expression atl__moving_fixed as atl__second

    "Shown."
    return

label atl__child_transition__start:
    show atl__dissolving as atl__person

    "Dissolving."
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

    # Showing a new image with an existing tag keeps the running transform and changes its child
    # (config.keep_running_transform). ATL that displays its `child` parameter compiles that
    # displayable into its block, so these check the transform shows the new child, not the one
    # it was created with.
    testsuite child:
        testcase replace:
            description "Replacing an image under a running transform displays the new image"
            parameter kind = ["inline", "move", "wrap", "contains", "swap"]
            run Start("atl__child_replace__" + kind)
            assert eval (atl__shown() == ["atl__red"]) timeout 1.0
            advance
            assert eval (atl__shown() == ["atl__yellow"]) timeout 1.0

            # Past atl__swap's final child statement, which must display the new child rather than
            # the one compiled into its block.
            pause 0.7
            assert eval (atl__shown() == ["atl__yellow"])

        testcase replace_keeps_properties:
            description "Replacing an image under inline ATL keeps the properties the ATL set"
            run Start("atl__child_replace__inline")
            assert eval (atl__shown() == ["atl__red"]) timeout 1.0
            advance
            assert eval (atl__shown() == ["atl__yellow"]) timeout 1.0
            assert eval (atl__state("atl__person").alpha == 0.5)

        testcase replace_during_other_child:
            description "An image replaced while ATL shows another child is displayed when ATL returns to child"
            run Start("atl__child_replace__swap")
            assert eval (atl__shown() == ["atl__blue"]) timeout 1.0
            advance

            # Past atl__swap's final child statement.
            pause 0.5
            assert eval (atl__shown() == ["atl__yellow"])

        testcase replace_in_parallel:
            description "An image replaced while a parallel block runs is displayed by that block's child statement"
            parameter kind = ["parallel", "choice"]
            run Start("atl__child_replace__swap_" + kind)
            assert eval (atl__shown() == ["atl__blue"]) timeout 1.0
            advance

            # Past the final child statement inside the running block.
            pause 0.5
            assert eval (atl__shown() == ["atl__yellow"])

        testcase reshow_same_transform:
            description "Showing a new image at the same ATL transform displays the new image"
            run Start("atl__child_reshow__start")
            assert eval (atl__shown() == ["atl__red"]) timeout 1.0
            advance
            assert eval (atl__shown() == ["atl__yellow"]) timeout 1.0

            # Past atl__swap's final child statement.
            pause 0.7
            assert eval (atl__shown() == ["atl__yellow"])

        testcase rollback_restores_child:
            description "Rolling back a replacement displays the original image again"
            parameter kind = ["move", "wrap", "contains", "swap"]
            run Start("atl__child_replace__" + kind)
            assert eval (atl__shown() == ["atl__red"]) timeout 1.0
            advance
            assert eval (atl__shown() == ["atl__yellow"]) timeout 1.0
            run Rollback()
            assert eval (atl__shown() == ["atl__red"]) timeout 1.0

        testcase layer_dissolve:
            description "A layer transition starts from the image displayed before it, inside a layer transform"
            # GH-6534, GH-6945: transition_from is an _in_current_store() copy of the layer, and must
            # not take the new value of the dynamic image from the copied ATL block.
            # https://github.com/renpy/renpy/issues/6534
            # https://github.com/renpy/renpy/issues/6945
            parameter kind = ["plain", "wrap", "contains", "swap"]
            run Start("atl__child_layer_dissolve__" + kind)
            assert eval (atl__shown() == ["atl__red"]) timeout 1.0

            # Wait for atl__swap to reach its final child statement.
            pause 0.7
            advance
            assert eval (atl__transition_from() == ["atl__red"]) timeout 1.0
            assert eval (atl__shown() == ["atl__yellow"]) timeout 1.0

            # 0.3 seconds into the 2 second dissolve from red to yellow, little green has blended
            # in. A dissolve that starts from the new image is already yellow (green 255).
            assert eval atl__transition_started() timeout 1.0
            pause 0.3
            assert eval (atl__pixel()[0] > 200 and atl__pixel()[1] < 160)

    # A duplicatable displayable has to be duplicated wherever it's shown, so that each place it's
    # shown runs its own ATL.
    testsuite duplicate:
        testcase show_expression:
            description "Each show expression of a displayable containing ATL runs its own copy of the ATL"
            run Start("atl__show_expression__start")
            assert eval (atl__moving("atl__first") is not None) timeout 1.0
            assert eval (atl__moving("atl__first") is not atl__moving("atl__second"))
            assert eval (atl__moving("atl__first") is not atl__moving_fixed.children[0])

        testcase child_transition:
            description "An ATL child statement's transition starts from the child being shown"
            run Start("atl__child_transition__start")
            assert eval (atl__shown_red() is not None) timeout 1.0
            $ atl__red_shown = atl__shown_red()

            assert eval (atl__dissolve() is not None) timeout 1.0
            assert eval (atl__dissolve().old_widget is atl__red_shown)
            $ atl__yellow_shown = atl__dissolve().new_widget

            # The second dissolve interrupts the first, and starts from yellow, not the first dissolve.
            assert eval (atl__dissolve().new_widget is not atl__yellow_shown) timeout 1.0
            assert eval (atl__dissolve().old_widget is atl__yellow_shown)
