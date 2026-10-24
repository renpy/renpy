# This file renders the Live2D Cubism sample models. Ren uses the Cubism 5.3
# blend modes and offscreens, while Mao uses neither.
#
# The models aren't distributed with Ren'Py, so these tests are skipped unless
# Live2D is installed and the models are present. To run them, copy the
# Samples/Resources/Ren and Samples/Resources/Mao directories from the Cubism
# SDK for Native (5-r.5 or later) into testcases/game/live2d/, which is ignored
# by git.

# ==============
# == Fixtures ==
# ==============

init python:

    def test_live2d__available():
        """
        Returns True if Live2D can be used and the sample models are present.
        """

        if not renpy.has_live2d():
            return False

        return all(renpy.loadable(f"live2d/{name}/{name}.model3.json") for name in ("Ren", "Mao"))

    # Live2D loads the model when it's created, so the images are only
    # defined when the models are present.
    if test_live2d__available():
        renpy.image("test_live2d_ren", Live2D("live2d/Ren", base=0.8, loop=False))
        renpy.image("test_live2d_mao", Live2D("live2d/Mao", base=0.8, loop=False))

transform test_live2d__closeup:
    xalign 0.5 yalign 0.12 zoom 3.0

label test_live2d__ren:
    scene black
    show test_live2d_ren at truecenter
    pause
    return

label test_live2d__mao:
    scene black
    show test_live2d_mao at truecenter
    pause
    return

label test_live2d__ren_closeup:
    scene black
    show test_live2d_ren at test_live2d__closeup
    pause
    return


# ==============
# === Tests ====
# ==============

testsuite live2d:
    description "Renders the Live2D sample models"
    enabled test_live2d__available()

    after testcase:
        if not screen "main_menu":
            run MainMenu(confirm=False, save=False)

    testcase ren:
        description "Renders a model that uses blend modes and offscreens"
        run Start("test_live2d__ren")
        pause 0.5
        screenshot "live2d/ren.png"

    testcase mao:
        description "Renders a model that doesn't use blend modes or offscreens"
        run Start("test_live2d__mao")
        pause 0.5
        screenshot "live2d/mao.png"

    testcase ren_closeup:
        description "Renders offscreens of a zoomed model at the drawable resolution"
        run Start("test_live2d__ren_closeup")
        pause 0.5
        screenshot "live2d/ren_closeup.png"
