# This file tests transform interpolation and replacement behavior.

# ==============
# == Helpers ===
# ==============

init python in transforms_test:
    import math

    # ---- ATL-test helpers ----

    def state(layer="master", tag="eileen"):
        d = renpy.game.context().scene_lists.get_displayable_by_tag(layer, tag)
        return d.state

    def absolute(v):
        """The pixel part of a position, or the value itself when it is a plain number."""
        return getattr(v, "absolute", v)

    def relative(v):
        """The relative part of a position, or the value itself when it is a plain number."""
        return getattr(v, "relative", v)

    # Warpers that leave [0, 1]. Used with `warp transforms_test.overshoot ...`.
    def overshoot(t):
        return t + 0.6 * math.sin(math.pi * t)

    def undershoot(t):
        return t - 0.6 * math.sin(math.pi * t)

# ==============
# == Fixtures ==
# ==============

label transforms__matrixcolor__label:
    scene bg room
    show eileen happy:
        matrixcolor BrightnessMatrix(0.0)
    "Start"
    show eileen happy:
        linear 0.2 matrixcolor BrightnessMatrix(1.0)
    "Brightening"
    show eileen happy:
        linear 0.2 matrixcolor BrightnessMatrix(0.0)
    "Done"
    return

transform transforms__matrixcolor_shared__brighten:
    matrixcolor BrightnessMatrix(0.0) xoffset 0
    linear 0.5 matrixcolor BrightnessMatrix(1.0) xoffset 200

label transforms__matrixcolor_shared__label:
    scene bg room
    show eileen happy
    "Start"
    show eileen happy at transforms__matrixcolor_shared__brighten onlayer master
    "Master brightening"
    show eileen happy at transforms__matrixcolor_shared__brighten onlayer overlay
    "Both brightening"
    show eileen happy at transforms__matrixcolor_shared__brighten onlayer overlay
    "Overlay restarted"
    return

label transforms__matrixcolor_product__label:
    scene bg room
    show eileen happy:
        matrixcolor BrightnessMatrix(0.0) * TintMatrix("#fff")
    "Start"
    show eileen happy:
        linear 0.4 matrixcolor BrightnessMatrix(1.0) * TintMatrix("#fff")
    "Animating"
    return

label transforms__spline__open__label:
    scene bg room
    show eileen happy:
        xoffset 0
    "Open path begins"
    show eileen happy:
        linear 1.0 xoffset 100 knot 25 knot 50 knot 75
    "Open spline"
    return

label transforms__spline__loop__label:
    scene bg room
    show eileen happy:
        xoffset 0
        align (0.0, 0.0)
    "Loop path begins"
    show eileen happy:
        linear 1.0 xoffset 0 knot 20 knot 80 knot 120 loop \
            align (0.0, 0.0) knot (0.2, 0.2) knot (0.5, 0.5) knot (0.8, 0.8) loop
    "Loop spline"
    return

label transforms__spline__loop_repeat__label:
    scene bg room
    show eileen happy:
        xoffset 0
    "Repeated loop path begins"
    show eileen happy:
        linear 0.1 xoffset 0 knot 10 knot 20 knot 30 loop
        repeat 20
    "Repeated loop path ends"
    return

label transforms__spline__vector__label:
    scene bg room
    show eileen happy:
        align (0.0, 0.0)
    "Vector ready"
    show eileen happy:
        linear 1.0 align (1.0, 1.0) knot (0.25, 0.25) knot (0.5, 0.5) knot (0.75, 0.75)
    "Vector path"
    return

label transforms__spline__matrix__label:
    scene bg room
    show eileen happy:
        matrixcolor BrightnessMatrix(0.0)
    "Color path begins"
    show eileen happy:
        linear 1.0 matrixcolor SplineMatrix(BrightnessMatrix(1.0), [0.0, 0.25, 0.5, 0.75, 1.0])
    "Color path halfway"
    return

label transforms__interp__alpha_int__label:
    scene bg room
    show eileen happy:
        alpha 1.0
    "Alpha ready"
    show eileen happy:
        linear 1.0 alpha 0
    "Alpha fading"
    return

label transforms__interp__overshoot__label:
    scene bg room
    show eileen happy:
        xoffset 0
    "Overshoot ready"
    show eileen happy:
        warp transforms_test.overshoot 1.0 xoffset 100
    "Overshoot running"
    return

label transforms__interp__undershoot__label:
    scene bg room
    show eileen happy:
        xoffset 0
    "Undershoot ready"
    show eileen happy:
        warp transforms_test.undershoot 1.0 xoffset 100
    "Undershoot running"
    return

label transforms__interp__pos__label:
    scene bg room
    show eileen happy:
        pos (0, 0)
    "Pos ready"
    show eileen happy:
        linear 1.0 pos (200, 100)
    "Pos moving"
    return

label transforms__interp__step__label:
    scene bg room
    show eileen happy:
        transform_anchor False
    "Step ready"
    show eileen happy:
        linear 1.0 transform_anchor True
    "Step running"
    return

label transforms__interp__quadratic__label:
    scene bg room
    show eileen happy:
        xoffset 0
    "Quadratic ready"
    show eileen happy:
        linear 1.0 xoffset 100 knot 80
    "Quadratic running"
    return

label transforms__interp__cubic__label:
    scene bg room
    show eileen happy:
        xoffset 0
    "Cubic ready"
    show eileen happy:
        linear 1.0 xoffset 100 knot 20 knot 90
    "Cubic running"
    return

label transforms__interp__splinematrix_chain__label:
    scene bg room
    show eileen happy:
        matrixcolor BrightnessMatrix(0.0)
    "Chain ready"
    show eileen happy:
        linear 0.4 matrixcolor SplineMatrix(BrightnessMatrix(1.0), [0.0, 0.5, 1.0])
    "Chain first leg"
    show eileen happy:
        linear 0.4 matrixcolor SplineMatrix(BrightnessMatrix(0.0), [0.0, 0.5, 1.0])
    "Chain second leg"
    return

# ==============
# === Tests ====
# ==============

testsuite transforms:
    after testcase:
        if not screen "main_menu":
            run MainMenu(confirm=False, save=False)

    testsuite matrixcolor:
        testcase interrupt_preserves_brightness_state:
            description "Matrixcolor continues from interrupted value, not jumping to old target"
            # GH-2591: When a matrixcolor interpolation is interrupted and replaced, the new
            # interpolation must continue from the *current* value, not the target
            # value of the interrupted interpolation.
            # https://github.com/renpy/renpy/issues/2591

            run Start("transforms__matrixcolor__label")
            advance # Begin animation
            pause 0.2 * 0.25 # 25% brightness

            # Verify we're partway through the first animation.
            python:
                # BrightnessMatrix.get(value) puts value in xdw/ydw/zdw.
                first_brightness = transforms_test.state().matrixcolor.ydw
                assert abs (first_brightness - 0.25) < 0.1, \
                    f"First animation: expected brightness ~0.25, got {first_brightness}"

            # Interrupt by advancing to the next show statement, then let the new
            # reverse animation run partway.
            advance
            pause 0.2 * 0.3  # 30% reverse animation

            # The new animation should be reversing from ~0.25 toward 0.0, not
            # jumping toward the old target (1.0) first.
            python:
                second_brightness = transforms_test.state().matrixcolor.ydw
                # Continue from interrupted value (~0.25), decreasing by ~0.25*0.15.
                expected = first_brightness * (1.0 - 0.15)
                assert abs(second_brightness - expected) < 0.1, \
                    f"Expected brightness ~{expected:.2f} (continuing from {first_brightness:.2f}), got {second_brightness:.2f}"
                assert second_brightness < first_brightness, \
                    f"Expected brightness to decrease from {first_brightness}, got {second_brightness}"

            # Let the reverse animation complete; brightness should reach 0.0.
            pause 0.2
            python:
                final_brightness = transforms_test.state().matrixcolor.ydw
                assert abs(final_brightness - 0.0) < 0.05, \
                    f"Expected final brightness near 0.0, got {final_brightness}"


        testcase continuous_interpolation_reaches_target:
            description "A non-interrupted matrixcolor interpolation reaches its target"

            run Start("transforms__matrixcolor__label")
            advance  # start the 0→1 animation
            pause 0.2  # let it complete

            python:
                brightness = transforms_test.state().matrixcolor.ydw
                assert abs(brightness - 1.0) < 0.05, \
                    f"Expected brightness near 1.0, got {brightness}"


        testcase shared_callable_not_corrupted:
            description "Interrupting one image does not corrupt a shared matrixcolor callable used by another"

            run Start("transforms__matrixcolor_shared__label")

            # Begin animation on master layer
            advance until "Master brightening"
            pause 0.5 * 0.25  # 25% brightness on master

            # Begin animation on overlay layer (shares the callable).
            advance until "Both brightening"
            pause 0.5 * 0.25  # 25% brightness on overlay, 50% brightness on master

            python:
                m_b = transforms_test.state("master", "eileen").matrixcolor.ydw
                o_b = transforms_test.state("overlay", "eileen").matrixcolor.ydw
                assert abs(m_b - 0.5) < 0.05, f"Expected master brightness ~0.5, got {m_b}"
                assert abs(o_b - 0.25) < 0.05, f"Expected overlay brightness ~2.5, got {o_b}"

            # Restart the overlay transform (interrupts it).
            advance until "Overlay restarted"
            pause 0.5 * 0.1

            python:
                m_b = transforms_test.state("master", "eileen").matrixcolor.ydw
                o_b = transforms_test.state("overlay", "eileen").matrixcolor.ydw
                # Master has been brightening uninterrupted for 60% of the full run.
                assert abs(m_b - 0.6) < 0.05, f"Expected master brightness ~0.6, got {m_b}"
                # Overlay just restarted, should be near 20%, NOT corrupted by master's value.
                assert abs(o_b - 0.1) < 0.05, f"Shared callable corrupted: overlay brightness {o_b} (should be ~0.1 fresh restart)"


        testcase product_matrixcolor_interpolates:
            description "A multiplied matrixcolor animates over time instead of snapping to its target"
            # A product such as BrightnessMatrix * TintMatrix is a _MultiplyMatrix.
            # It must interpolate over the duration of the ATL statement, not jump
            # straight to the end value.

            run Start("transforms__matrixcolor_product__label")
            advance  # start the 0->1 product animation
            pause 0.4 * 0.25  # 25% through the animation

            python:
                brightness = transforms_test.state().matrixcolor.ydw
                # Before the fix this snapped to the target value (1.0) on every frame.
                assert brightness < 0.6, \
                    f"Product matrixcolor snapped to target: brightness {brightness:.2f}"
                assert brightness > 0.05, \
                    f"Product matrixcolor did not animate: brightness {brightness:.2f}"

            pause 0.4  # let the animation complete
            python:
                brightness = transforms_test.state().matrixcolor.ydw
                assert abs(brightness - 1.0) < 0.05, \
                    f"Expected brightness near 1.0, got {brightness:.2f}"

    testsuite numeric:
        testcase int_target_on_float_property:
            description "An int target on a float property still interpolates (type comes from the property, not the target)"

            run Start("transforms__interp__alpha_int__label")
            advance until "Alpha ready"
            advance until "Alpha fading"
            pause 0.5

            python:
                a = transforms_test.state().alpha
                assert abs(a - 0.5) < 0.15, f"Expected alpha ~0.5 halfway, got {a}"

            pause 0.6
            python:
                a = transforms_test.state().alpha
                assert abs(a - 0.0) < 0.02, f"Expected alpha 0.0 at the end, got {a}"

        testcase warper_overshoot_extrapolates:
            description "A warper returning t > 1 extrapolates past the target"

            run Start("transforms__interp__overshoot__label")
            advance until "Overshoot ready"
            advance until "Overshoot running"
            pause 0.7

            python:
                x = transforms_test.state().xoffset
                # The warper peaks at ~1.19 around t=0.68, so ~118 here.
                assert x > 105, f"Expected overshoot past 100, got {x}"

            pause 0.6
            python:
                x = transforms_test.state().xoffset
                assert abs(x - 100) < 1, f"Expected to settle at 100, got {x}"

        testcase warper_undershoot_extrapolates:
            description "A warper returning t < 0 extrapolates before the start"

            run Start("transforms__interp__undershoot__label")
            advance until "Undershoot ready"
            advance until "Undershoot running"
            pause 0.3

            python:
                x = transforms_test.state().xoffset
                # The warper bottoms out at ~-0.19 around t=0.3, so ~-18 here.
                assert x < -5, f"Expected undershoot below 0, got {x}"

            pause 1.0
            python:
                x = transforms_test.state().xoffset
                assert abs(x - 100) < 1, f"Expected to settle at 100, got {x}"

        testcase absolute_position_tuple_interpolates:
            description "pos with integer pixels interpolates both components"

            run Start("transforms__interp__pos__label")
            advance until "Pos ready"
            advance until "Pos moving"
            pause 0.5

            python:
                s = transforms_test.state()
                x = transforms_test.absolute(s.xpos)
                y = transforms_test.absolute(s.ypos)
                assert abs(x - 100) < 20, f"Expected xpos ~100, got {x}"
                assert abs(y - 50) < 20, f"Expected ypos ~50, got {y}"

            pause 0.6
            python:
                s = transforms_test.state()
                x = transforms_test.absolute(s.xpos)
                y = transforms_test.absolute(s.ypos)
                assert abs(x - 200) < 1, f"Expected xpos 200, got {x}"
                assert abs(y - 100) < 1, f"Expected ypos 100, got {y}"

        testcase boolean_steps_at_the_end:
            description "A non-interpolable value keeps its old value until the end of the statement"

            run Start("transforms__interp__step__label")
            advance until "Step ready"
            advance until "Step running"
            pause 0.5

            python:
                v = transforms_test.state().transform_anchor
                assert v is False, f"Expected transform_anchor to still be False halfway, got {v}"

            pause 0.6
            python:
                v = transforms_test.state().transform_anchor
                assert v is True, f"Expected transform_anchor True at the end, got {v}"

    testsuite spline:
        testcase renders_open_spline:
            description "An ATL Catmull-Rom spline moves a displayable through its knots"

            run Start("transforms__spline__open__label")
            advance until "Open path begins"
            advance until "Open spline"
            pause 0.5

            python:
                v = transforms_test.state().xoffset
                assert abs(v - 50) < 10, \
                    f"Expected the open spline to pass near xoffset 50, got {v}"

            pause 0.5
            python:
                v = transforms_test.state().xoffset
                assert abs(v - 100) < 5, \
                    f"Expected the open spline to reach xoffset 100, got {v}"

        testcase renders_loop_spline:
            description "An ATL spline can be closed with the loop keyword"

            run Start("transforms__spline__loop__label")
            advance until "Loop path begins"
            advance until "Loop spline"
            pause 0.5

            python:
                s = transforms_test.state()
                assert abs(s.xoffset - 80) < 12, \
                    f"Expected the loop spline to pass through xoffset 80, got {s.xoffset}"
                assert abs(s.xalign.relative - 0.5) < 0.1, \
                    f"Expected the loop spline to pass through xalign 0.5, got {s.xalign}"
                assert abs(s.yalign.relative - 0.5) < 0.1, \
                    f"Expected the loop spline to pass through yalign 0.5, got {s.yalign}"

            pause 0.5
            python:
                s = transforms_test.state()
                assert s.xoffset == 0, \
                    f"Expected the loop spline to reach xoffset 0, got {s.xoffset}"

        testcase loop_spline_does_not_drift:
            description "Repeating a loop spline does not accumulate endpoint error"

            run Start("transforms__spline__loop_repeat__label")
            advance until "Repeated loop path begins"
            advance until "Repeated loop path ends"

            python:
                s = transforms_test.state()
                assert s.xoffset == 0, \
                    f"Expected the repeated loop spline to end at xoffset 0, got {s.xoffset}"

        testcase renders_vector_spline:
            description "An ATL spline interpolates both components of an align property"

            run Start("transforms__spline__vector__label")
            advance until "Vector ready"
            advance until "Vector path"
            pause 0.5

            python:
                s = transforms_test.state()
                assert abs(s.xalign.relative - 0.5) < 0.1, \
                    f"Expected vector spline xalign near 0.5, got {s.xalign}"
                assert abs(s.yalign.relative - 0.5) < 0.1, \
                    f"Expected vector spline yalign near 0.5, got {s.yalign}"

        testcase renders_spline_matrix:
            description "SplineMatrix applies its spline while rendering a matrixcolor transform"

            run Start("transforms__spline__matrix__label")
            advance until "Color path begins"
            advance until "Color path halfway"
            pause 0.5

            python:
                brightness = transforms_test.state().matrixcolor.ydw
                assert abs(brightness - 0.5) < 0.1, \
                    f"Expected SplineMatrix brightness near 0.5, got {brightness}"

        testcase quadratic_spline:
            description "One knot gives a quadratic Bezier that does not pass through the knot"

            run Start("transforms__interp__quadratic__label")
            advance until "Quadratic ready"
            advance until "Quadratic running"
            pause 0.5

            python:
                x = transforms_test.state().xoffset
                # [0, 80, 100] at t=0.5 -> 65.
                assert abs(x - 65) < 12, f"Expected quadratic midpoint ~65, got {x}"

            pause 0.6
            python:
                x = transforms_test.state().xoffset
                assert x == 100, f"Expected the spline to end exactly on 100, got {x}"

        testcase cubic_spline:
            description "Two knots give a cubic Bezier"

            run Start("transforms__interp__cubic__label")
            advance until "Cubic ready"
            advance until "Cubic running"
            pause 0.5

            python:
                x = transforms_test.state().xoffset
                # [0, 20, 90, 100] at t=0.5 -> 53.75.
                assert abs(x - 53.75) < 12, f"Expected cubic midpoint ~54, got {x}"

            pause 0.6
            python:
                x = transforms_test.state().xoffset
                assert x == 100, f"Expected the spline to end exactly on 100, got {x}"

    testsuite matrix:
        testcase splinematrix_after_splinematrix:
            description "A SplineMatrix following a completed SplineMatrix continues from the previous matrix, not the new target"

            run Start("transforms__interp__splinematrix_chain__label")
            advance until "Chain ready"
            advance until "Chain first leg"
            pause 0.5

            python:
                b = transforms_test.state().matrixcolor.ydw
                assert abs(b - 1.0) < 0.05, f"Expected brightness 1.0 after the first leg, got {b}"

            advance until "Chain second leg"
            pause 0.2

            python:
                b = transforms_test.state().matrixcolor.ydw
                # 1.0 -> 0.0 with spline [0, 0.5, 1] at t=0.5 -> 0.5.
                assert abs(b - 0.5) < 0.15, f"Expected brightness ~0.5 halfway, got {b} (0.0 means it jumped to the target)"

            pause 0.3
            python:
                b = transforms_test.state().matrixcolor.ydw
                assert abs(b - 0.0) < 0.05, f"Expected brightness 0.0 at the end, got {b}"
