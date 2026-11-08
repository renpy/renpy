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

    def test_live2d__pose_state(tag="test_live2d_mao_pose"):
        """
        Returns the pose state of the rendered image with the given tag.
        """

        return next(
            state for name, state in renpy.gl2.live2d.states.items()
            if name[1] == tag
        )

    def test_live2d__clipping_frame(name, motion, st):
        """
        Renders one frame of a motion to a surface, using the current value of
        config.live2d_mask_clipping.

        This calls the render method directly, as the render cache could
        otherwise return the render made with the other setting. Physics and
        poses depend on the time between frames, so they're disabled to make
        the frame depend only on `st`. The common data is isolated by its key,
        so the other tests still use physics.
        """

        d = Live2D(
            f"live2d/{name}", base=0.8, loop=False, fade=False, pose=False, motions=[ motion ],
            deduplication_key=f"test_live2d_mask_clipping_{name}",
        )
        d.common.physics = None

        return renpy.render_to_surface(d.render(config.screen_width, config.screen_height, st, st))

    def test_live2d__max_difference(a, b=None):
        """
        Returns the largest difference in any channel of any pixel between
        surfaces `a` and `b`. If `b` is None, `a` is compared to a transparent
        surface.
        """

        if b is None:
            b = renpy.pygame.Surface(a.get_size(), 0, a)

        width, height = a.get_size()

        return max(
            abs(i - j)
            for y in range(height)
            for x in range(width)
            for i, j in zip(a.get_at((x, y)), b.get_at((x, y)))
        )

    # Live2D loads the model when it's created, so the images are only
    # defined when the models are present.
    if test_live2d__available():
        from uuid import uuid4 as test_live2d__uuid4

        # Never replace a player's existing save when exercising save/load.
        test_live2d__save_slot = "_test_live2d_pose_" + test_live2d__uuid4().hex

        renpy.image("test_live2d_ren", Live2D("live2d/Ren", base=0.8, loop=False))
        renpy.image("test_live2d_mao", Live2D("live2d/Mao", base=0.8, loop=False))
        renpy.image("test_live2d_mao_no_pose", Live2D("live2d/Mao", base=0.8, loop=False, pose=False))

        # Keep this model static between changes, so a cached render can be
        # older than the pose's fade time. Its common data is isolated from
        # the other Mao tests, which exercise the original sample files.
        test_live2d__pose_image = Live2D(
            "live2d/Mao", base=0.8, loop=False, pose=True, deduplication_key="test_live2d_pose"
        )
        test_live2d__pose_common = test_live2d__pose_image.common
        test_live2d__pose_common.physics = None
        test_live2d__pose_common.expressions["select_left_b"] = renpy.gl2.live2d.Live2DExpression(
            [
                {"Id": "PartArmLA", "Blend": "Overwrite", "Value": 0.0},
                {"Id": "PartArmLB", "Blend": "Overwrite", "Value": 1.0},
            ],
            0.0,
            0.0,
        )
        test_live2d__pose_common.all_expressions.update(test_live2d__pose_common.expressions)
        test_live2d__pose_common.attributes.add("select_left_b")
        renpy.image("test_live2d_mao_pose", test_live2d__pose_image)

        # Share the static model, but disable motion fading so the outgoing
        # motion cannot keep requesting its part after switching to still.
        renpy.image("test_live2d_mao_sustained", Live2D(
            "live2d/Mao", base=0.8, loop=False, pose=True, fade=False, deduplication_key="test_live2d_pose"
        ))

default test_live2d__saved = False

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

label test_live2d__mao_no_pose:
    scene black
    show test_live2d_mao_no_pose at truecenter
    pause
    return

label test_live2d__mao_sustained:
    scene black
    show test_live2d_mao_sustained still at truecenter
    pause
    show test_live2d_mao_sustained mtn_04
    pause
    show test_live2d_mao_sustained still
    pause
    return

label test_live2d__mao_pose:
    scene black
    show test_live2d_mao_pose still at truecenter
    pause
    show test_live2d_mao_pose still select_left_b
    pause
    show test_live2d_mao_pose still -select_left_b
    $ test_live2d__saved = True
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
        # Surfaces can't be saved, and the setting must not reach other tests.
        $ test_live2d__cropped = None
        $ test_live2d__uncropped = None
        $ config.live2d_mask_clipping = True

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

    testcase mao_no_pose:
        description "Draws all of the alternative parts when the pose is disabled"
        run Start("test_live2d__mao_no_pose")
        pause 0.5
        screenshot "live2d/mao_no_pose.png"

    testcase mao_sustained:
        description "Keeps the part selected by a motion after that motion ends"
        run Start("test_live2d__mao_sustained")
        pause 0.1
        assert eval test_live2d__pose_state("test_live2d_mao_sustained").pose_opacities["PartArmLA"] == 1.0
        keysym "dismiss"
        pause 0.6
        assert eval test_live2d__pose_state("test_live2d_mao_sustained").pose_opacities["PartArmLB"] == 1.0
        keysym "dismiss"
        pause 0.6
        assert eval not test_live2d__pose_common.pose_requests
        assert eval test_live2d__pose_state("test_live2d_mao_sustained").pose_opacities["PartArmLB"] == 1.0
        assert eval test_live2d__pose_state("test_live2d_mao_sustained").pose_opacities["PartArmLA"] == 0.0
        # This fixture has no physics, so its screenshot is independent of frame timing.
        screenshot "live2d/mao_sustained_still.png"

    testcase mao_pose_idle_crossfade:
        description "Starts a pose crossfade after a static model's render has been cached"
        run Start("test_live2d__mao_pose")
        pause 2.0
        assert eval test_live2d__pose_state().pose_opacities["PartArmLA"] == 1.0
        keysym "dismiss"
        pause 0.1
        assert eval 0.0 < test_live2d__pose_state().pose_opacities["PartArmLB"] < 1.0
        pause 0.6
        assert eval test_live2d__pose_state().pose_opacities["PartArmLB"] == 1.0
        assert eval test_live2d__pose_state().pose_opacities["PartArmLA"] == 0.0

    testcase mao_pose_load:
        description "Resets a sustained pose when a saved game is loaded"
        run Start("test_live2d__mao_pose")
        pause 0.1
        keysym "dismiss"
        pause 0.6
        keysym "dismiss"
        pause 0.1
        assert eval test_live2d__pose_state().pose_sustained[0] == "PartArmLB"
        run Function(renpy.save, test_live2d__save_slot, include_screenshot=False)
        $ test_live2d__saved = False
        run Function(renpy.load, test_live2d__save_slot)
        pause 0.1
        assert eval test_live2d__saved
        assert eval test_live2d__pose_state().pose_sustained[0] == "PartArmLA"
        assert eval test_live2d__pose_state().pose_opacities["PartArmLA"] == 1.0
        assert eval test_live2d__pose_state().pose_opacities["PartArmLB"] == 0.0
        run Function(renpy.unlink_save, test_live2d__save_slot)

    testcase ren_closeup:
        description "Renders offscreens of a zoomed model at the drawable resolution"
        run Start("test_live2d__ren_closeup")
        pause 0.5
        screenshot "live2d/ren_closeup.png"

    testcase mask_clipping:
        description "Draws the same frame of a motion with cropped and uncropped clipping masks"
        parameter model = [ "Mao", "Ren" ]
        parameter motion = [ "mtn_02", "mtn_03" ]
        parameter st = [ 1.0, 2.5 ]
        $ config.live2d_mask_clipping = True
        $ test_live2d__cropped = test_live2d__clipping_frame(model, motion, st)
        $ config.live2d_mask_clipping = False
        $ test_live2d__uncropped = test_live2d__clipping_frame(model, motion, st)
        assert eval test_live2d__max_difference(test_live2d__uncropped) > 0
        # Cropping changes the edges of masks slightly, by at most 25/255 in the models tested.
        assert eval test_live2d__max_difference(test_live2d__cropped, test_live2d__uncropped) <= 25
        # Mao's masks differ in hundreds of pixels, so an identical frame means the setting was ignored.
        assert eval model != "Mao" or test_live2d__max_difference(test_live2d__cropped, test_live2d__uncropped) > 0
