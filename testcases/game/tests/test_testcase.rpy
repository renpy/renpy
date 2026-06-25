## This file tests the testcase system itself

label three_messages:
    "Message 1"
    "Message 2"
    "Message 3"
    return

label hard_pause:
    "Before hard pause."
    $ renpy.pause(0.5, hard=True)
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

    # testcase python:
    #     python hide:
    #         renpy.watch("renpy.is_in_test()")
    #         renpy.watch("waitch")
    #         renpy.watch("whether")
    #         waitch = 5

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

    testsuite menus:
        parameter screen_name = ["preferences", "load"]

        setup:
            run ShowMenu(screen_name)

        teardown:
            run Return()

        testcase menu_screen:
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
    setup:
        run Jump("hard_pause")
        pause until screen "say"

    testcase hard_pause_fail_timeout:
        xfail True

        $ _test.timeout = 0.2
        advance until "End"

    testcase hard_pause_pass_timeout:
        $ _test.timeout = 1.0
        advance until "End"

testsuite context:
    testcase replay_action:
        description "Tests that the Replay action properly updates context variables."

        $ _test.timeout = 5.0

        $ replay_scope = {"context_test_inner_val": True}
        run Replay("start", scope=replay_scope)
        assert eval (not "replay_scope" in globals())
        assert eval ("context_test_inner_val" in globals())
        $ renpy.end_replay()
        assert eval ("replay_scope" in globals())

    testcase replay_python:
        description "Tests that `renpy.call_replay` properly updates context variables."

        $ replay_scope = {"context_test_inner_val": True}
        $ renpy.call_replay("start", scope=replay_scope)
        assert eval (not "replay_scope" in globals())
        assert eval ("context_test_inner_val" in globals())
        $ renpy.end_replay()
        assert eval ("replay_scope" in globals())

testsuite for_loops:
    description "Tests `for` loop statements with various patterns."

    testcase range:
        description "Basic `for` loop with `range`, variable accessible after loop"

        $ counter = 0
        for i in range(4):
            $ counter += 1

        assert eval (i == 3)
        assert eval (counter == 4)

    testcase tuple_unpacking:
        description "Tuple unpacking"

        $ counter = 0
        for (x, y) in [(1, 2), (3, 4), (5, 6)]:
            $ counter += 1

        # After loop, variables should have last iteration values
        assert eval (x == 5)
        assert eval (y == 6)
        assert eval (counter == 3)

    testcase tuple_unpacking2:
        description "Tuple unpacking with nested tuples"

        $ counter = 0
        for z, (x, y) in [("a", (1, 2)), ("b", (3, 4)), ("c", (5, 6))]:
            $ counter += 1

        # After loop, variables should have last iteration values
        assert eval (z == "c")
        assert eval (x == 5)
        assert eval (y == 6)
        assert eval (counter == 3)

    testcase break:
        description "`break` statement exits the loop early"

        $ counter = 0
        for i in range(10):
            $ counter += 1
            if eval (i == 3):
                break

        assert eval (i == 3)
        assert eval (counter == 4)

    testcase continue:
        description "`continue` statement skips to the next iteration"

        $ counter = 0
        for i in range(4):
            $ counter += 1
            if eval (i == 1):
                continue

        # After continue, loop should have continued normally
        assert eval (i == 3)
        assert eval (counter == 4)

    testcase string:
        description "Iterating over a string"

        $ counter = 0
        for char in "hello":
            $ counter += 1

        assert eval (char == 'o')
        assert eval (counter == 5)

    testcase empty_loop:
        description "Empty iterable"

        $ counter = 0
        for test_for_empty_loop_i in []:
            $ counter = 0

        # Loop should not execute, so i is undefined (or should not exist)
        assert eval (not "test_for_empty_loop_i" in locals() and not "test_for_empty_loop_i" in globals())
        assert eval (counter == 0)

    testcase list:
        description "Iterating over a list"

        $ counter = 0
        for item in [10, 20, 30, 40]:
            $ counter += 1

        assert eval (item == 40)
        assert eval (counter == 4)

    testcase enumerate:
        description "Enumerate with tuple unpacking"

        $ counter = 0
        for i, val in enumerate(['a', 'b', 'c']):
            $ counter += 1

        # After loop, i and val should have last iteration values
        assert eval (i == 2)
        assert eval (val == 'c')
        assert eval (counter == 3)

    testcase enumerate_break:
        description "Enumerate with `break` in middle"

        $ counter = 0
        for idx, val in enumerate(['x', 'y', 'z']):
            $ counter += 1
            if eval (idx == 1):
                break

        assert eval (idx == 1)
        assert eval (val == 'y')
        assert eval (counter == 2)

    testcase nested_loops:
        description "Nested for loops"

        $ counter = 0
        for i in range(3):
            for j in range(2):
                $ counter += 1

        # After nested loops, both should have last iteration values
        assert eval (i == 2)
        assert eval (j == 1)
        assert eval (counter == 6)

    testcase break_inner_loop:
        description "Break in inner loop should not affect outer loop"

        $ counter = 0
        for i in range(3):
            for j in range(3):
                $ counter += 1
                if eval (j == 1):
                    break

        assert eval (i == 2)
        assert eval (j == 1)
        assert eval (counter == 6)

    testcase continue_inner_loop:
        description "Continue in inner loop should skip to next iteration of inner loop"

        $ counter = 0
        for i in range(3):
            for j in range(3):
                if eval (j == 1):
                    continue
                $ counter += 1

        assert eval (i == 2)
        assert eval (j == 2)
        assert eval (counter == 6)

    testcase break_outer_loop:
        description "Break in outer loop should exit both loops"

        $ counter = 0
        for i in range(3):
            for j in range(3):
                $ counter += 1
            if eval (i == 1):
                break
        assert eval (i == 1)
        assert eval (j == 2)
        assert eval (counter == 6)

    testcase continue_outer_loop:
        description "Continue in outer loop should skip to next iteration of outer loop"
        $ counter = 0
        for i in range(3):
            if eval (i == 1):
                continue
            for j in range(3):
                $ counter += 1

        assert eval (i == 2)
        assert eval (j == 2)
        assert eval (counter == 6)

    testcase menu_choices:
        description "Clicks menu choices on loop"

        run Start("branching.variable_test")
        pause until screen "choice"

        for option in ["Increment", "Increment", "Decrement", "Increment", "Increment"]:
            click expression option

        assert "Value: 3" timeout 2.0
        click "Done"


testsuite while_loops:
    description "Tests `while` loop statements with various patterns."

    testcase basic_while:
        description "Basic while loop increments until condition becomes false"

        $ i = 0
        $ counter = 0

        while eval (i < 4):
            $ counter += 1
            $ i += 1

        assert eval (i == 4)
        assert eval (counter == 4)

    testcase while_break:
        description "`break` exits the loop early"

        $ i = 0
        $ counter = 0

        while eval (i < 10):
            $ counter += 1
            if eval (i == 3):
                break
            $ i += 1

        assert eval (i == 3)
        assert eval (counter == 4)

    testcase while_continue:
        description "`continue` skips body segment and keeps iterating"

        $ i = 0
        $ counter = 0
        $ hits = []

        while eval (i < 5):
            $ i += 1
            if eval (i == 3):
                continue
            $ counter += 1
            $ hits.append(i)

        assert eval (i == 5)
        assert eval (counter == 4)
        assert eval (hits == [1, 2, 4, 5])

    testcase while_never_runs:
        description "Does not execute when condition starts false"

        $ i = 10
        $ counter = 0

        while eval (i < 5):
            $ counter += 1
            $ i += 1

        assert eval (i == 10)
        assert eval (counter == 0)

    testcase nested_while:
        description "Nested while loops"

        $ i = 0
        $ counter = 0

        while eval (i < 3):
            $ j = 0
            while eval (j < 2):
                $ counter += 1
                $ j += 1
            $ i += 1

        assert eval (i == 3)
        assert eval (j == 2)
        assert eval (counter == 6)

    testcase real_choices:
        description "Clicks menu choices on loop"

        run Start("branching.variable_test")
        pause until screen "choice"

        $ clicks = 0
        while eval (menu_var < 3):
            click "Increment"
            click "Increment"
            click "Decrement"
            $ clicks += 1

        assert eval (clicks == 3)
        assert "Value: 3" timeout 2.0
        click "Done"
