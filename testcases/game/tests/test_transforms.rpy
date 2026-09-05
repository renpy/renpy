# This file tests transform interpolation and replacement behavior.

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
                d = renpy.game.context().scene_lists.get_displayable_by_tag("master", "eileen")
                mc = d.state.matrixcolor
                # BrightnessMatrix.get(value) puts value in xdw/ydw/zdw.
                first_brightness = mc.ydw
                assert abs (first_brightness - 0.25) < 0.1, \
                    f"First animation: expected brightness ~0.25, got {first_brightness}"

            # Interrupt by advancing to the next show statement, then let the new
            # reverse animation run partway.
            advance
            pause 0.2 * 0.3  # 30% reverse animation

            # The new animation should be reversing from ~0.25 toward 0.0, not
            # jumping toward the old target (1.0) first.
            python:
                d = renpy.game.context().scene_lists.get_displayable_by_tag("master", "eileen")
                mc = d.state.matrixcolor
                second_brightness = mc.ydw
                # Continue from interrupted value (~0.25), decreasing by ~0.25*0.15.
                expected = first_brightness * (1.0 - 0.15)
                assert abs(second_brightness - expected) < 0.1, \
                    f"Expected brightness ~{expected:.2f} (continuing from {first_brightness:.2f}), got {second_brightness:.2f}"
                assert second_brightness < first_brightness, \
                    f"Expected brightness to decrease from {first_brightness}, got {second_brightness}"

            # Let the reverse animation complete; brightness should reach 0.0.
            pause 0.2
            python:
                d = renpy.game.context().scene_lists.get_displayable_by_tag("master", "eileen")
                mc = d.state.matrixcolor
                final_brightness = mc.ydw
                assert abs(final_brightness - 0.0) < 0.05, \
                    f"Expected final brightness near 0.0, got {final_brightness}"


        testcase continuous_interpolation_reaches_target:
            description "A non-interrupted matrixcolor interpolation reaches its target"

            run Start("transforms__matrixcolor__label")
            advance  # start the 0→1 animation
            pause 0.2  # let it complete

            python:
                d = renpy.game.context().scene_lists.get_displayable_by_tag("master", "eileen")
                mc = d.state.matrixcolor
                brightness = mc.ydw
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
                m = renpy.game.context().scene_lists.get_displayable_by_tag("master", "eileen")
                o = renpy.game.context().scene_lists.get_displayable_by_tag("overlay", "eileen")
                m_b = m.state.matrixcolor.ydw
                o_b = o.state.matrixcolor.ydw
                assert abs(m_b - 0.5) < 0.05, f"Expected master brightness ~0.5, got {m_b}"
                assert abs(o_b - 0.25) < 0.05, f"Expected overlay brightness ~2.5, got {o_b}"

            # Restart the overlay transform (interrupts it).
            advance until "Overlay restarted"
            pause 0.5 * 0.1

            python:
                m = renpy.game.context().scene_lists.get_displayable_by_tag("master", "eileen")
                o = renpy.game.context().scene_lists.get_displayable_by_tag("overlay", "eileen")
                m_b = m.state.matrixcolor.ydw
                o_b = o.state.matrixcolor.ydw
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
                d = renpy.game.context().scene_lists.get_displayable_by_tag("master", "eileen")
                mc = d.state.matrixcolor
                brightness = mc.ydw
                # Before the fix this snapped to the target value (1.0) on every frame.
                assert brightness < 0.6, \
                    f"Product matrixcolor snapped to target: brightness {brightness:.2f}"
                assert brightness > 0.05, \
                    f"Product matrixcolor did not animate: brightness {brightness:.2f}"

            pause 0.4  # let the animation complete
            python:
                d = renpy.game.context().scene_lists.get_displayable_by_tag("master", "eileen")
                mc = d.state.matrixcolor
                brightness = mc.ydw
                assert abs(brightness - 1.0) < 0.05, \
                    f"Expected brightness near 1.0, got {brightness:.2f}"
