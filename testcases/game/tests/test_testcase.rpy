## This file tests the testcase system itself

label three_messages:
    "Message 1"
    "Message 2"
    "Message 3"
    return

label hard_pause:
    "Before hard pause."
    $ renpy.pause(6, hard=True)
    "End"

screen teleporting_button(x=0, y=0, remaining=20):
    textbutton "Teleporting Button":
        id "teleporting_button"
        xpos x
        ypos y
        if remaining > 0:
            action Show("teleporting_button", x=(x + 23) % 400, y=(y + 47) % 400, remaining=remaining - 1)
        else:
            action Hide("teleporting_button")

testsuite flow:
    testcase skip:
        enabled False
        assert False

    testcase python:
        python hide:
            renpy.watch("renpy.is_in_test()")
            renpy.watch("waitch")
            renpy.watch("whether")
            waitch = 5

testsuite parameter_field:

    testsuite zipped:
        parameter z = [5, 10]

        testcase param_test:
            parameter (x, y) = [(1,4), (2,3)]

            assert eval (x + y == z) xfail z != 5

        testcase param_test2:
            parameter (x, y) = [(1,4), (2,3)]
            xfail z != 5

            assert eval (x + y == z)

    testsuite combinations:
        setup:
            $ num_tests = 0

        after testcase:
            $ num_tests += 1

        teardown:
            assert eval (num_tests == 8)

        testcase combinations:
            parameter a = [1, 2]
            parameter b = [3, 4]
            parameter c = [5, 6]
            parameter (x,y) = [(10, 11)]

            xfail (a, b, c) in [(1,3, 5), (2,4,6)]
            assert eval (a + b + c == x or a + b + c == y)



testsuite screenshot:
    testcase main_menu:
        screenshot "main_menu.png" #crop (0, 0, 400, 300)

    testcase menus:
        parameter screen_name = ["preferences", "save"]

        run Show(screen_name)
        screenshot f"screens/{screen_name}.png"

testsuite execution_order:
    before testcase:
        $ execution_order_test_var = False

    after testcase:
        assert eval execution_order_test_var

    testcase subcase:
        assert eval (not execution_order_test_var)
        $ execution_order_test_var = True

    testsuite subsuite:
        before testcase:
            assert eval (not execution_order_test_var)

        testcase subcase_2:
            $ execution_order_test_var = True


testsuite boolean_conditions:
    description "Tests for boolean conditions, operators, and eval."

    testcase boolean_value_true:
        assert True

    testcase boolean_value_false:
        assert False xfail True  # The assert should fail

    testcase boolean_value_false2:
        xfail True  # The test should fail
        assert False

    testcase boolean_operators:
        assert not False
        assert not not True
        assert True or False
        assert False or True
        assert not (True and False)
        assert not (False and True)
        assert True and True
        assert (True or False) and (not False)
        assert (not False) or (False and False)
        assert (True and not False) or False
        assert (not (False or False))

    testcase boolean_operators_eval:
        assert eval False == False
        assert eval True != False
        assert eval (1 == 1) and (2 > 1)
        assert eval (0 or 1) == 1
        assert eval "hello" == "hello"
        assert eval 42 == 42
        assert eval 3.14 > 3
        assert eval isinstance("abc", str)
        assert eval isinstance(123, int)
        assert eval isinstance(3.14, float)
        assert eval type("abc") == str
        assert eval type(123) == int
        assert eval len("abc") == 3
        assert eval "a" in "abc"
        assert eval 5 in [1, 2, 3, 4, 5]
        assert eval not (7 not in [5, 6, 7, 8])
        assert eval renpy.is_in_test()

        $ testvar = 1
        assert eval (testvar - 1 == 0)
        $ testvar = 2
        assert eval (testvar - 1 == 0) xfail True

testsuite message_if:
    setup:
        run Jump("three_messages")
        pause until screen "say"

    testcase test_if:
        if "Message 1":
            pass
        else:
            assert False

    testcase test_elif:
        if "Not here":
            assert False
        elif "Message 1":
            pass
        else:
            assert False

    testcase test_else:
        if "Not here":
            assert False
        elif "Message 1":
            pass
        else:
            assert False

testcase message_if.dotted_testcase:
    assert "Message 1"

testsuite selectors:
    testcase teleporting_button_test:
        run Show("teleporting_button")
        pause until screen "teleporting_button"
        click id "teleporting_button" until not screen "teleporting_button"

    testcase drag_and_drop:
        run Show("drag_and_drop")
        pause until screen "drag_and_drop"
        drag id "peg" pos (0, 0) to id "hole" pos (0, 0)
        assert id "success"
        drag id "peg" pos (0.5, 0.5) to id "hole" pos (0, 0)
        assert id "success"
        drag id "peg" pos (0.9, 0.9) to id "hole" pos (0, 0)
        assert id "success"
        drag id "peg" pos (0, 0) to id "hole" pos (0.5, 0.5)
        assert id "success"
        drag id "peg" pos (0.5, 0.5) to pos (0.2, 0.5)
        assert not id "success"
        run Hide("drag_and_drop")

    testcase scroll_test:
        run Show("scroll_screen")
        pause until screen "scroll_screen"
        scroll id "scroll_vp" amount 50
        click id "close_screen_button"
        assert not screen "scroll_screen"

testsuite timeout:
    testcase hard_pause_timeout:
        # Make sure _test.timeout can be changed
        run Jump("hard_pause")
        pause until screen "say"

        $ _test.timeout = 7
        advance until "End"
        $ _test.timeout = 5
