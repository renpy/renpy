## This file tests the control-flow, expression, and parameter statements of the test language itself.

# ==============
# == Fixtures ==
# ==============

# Also used by test_test_selectors.rpy.
label three_messages:
    "Message 1"
    "Message 2"
    "Message 3"
    return

# ==============
# === Tests ====
# ==============

testsuite flow:
    testcase skip:
        description "Guards that `enabled False` skips a testcase: if it ran, its `assert False` would fail the run."

        enabled False
        assert False

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

    testcase boolean_value_mixed:
        # A passing assert must not hide the failing one. The reporter's counts for this case are checked by
        # testcases/pytests/test_test_testreporter.py.
        xfail True
        assert True
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
        description "Checks that `assert eval` parses and evaluates whole expressions, in the game's store."

        assert eval False == False
        assert eval True != False
        assert eval (1 == 1) and (2 > 1)
        assert eval (0 or 1) == 1
        assert eval "hello" == "hello"
        assert eval not (7 not in [5, 6, 7, 8])
        assert eval renpy.is_in_test()

        $ testvar = 1
        assert eval (testvar - 1 == 0)
        $ testvar = 2
        assert eval (testvar - 1 == 0) xfail True

testsuite message_if:
    setup:
        run Start("three_messages")
        assert screen "say"

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

testsuite for_loops:
    description "Tests `for` loop statements with various patterns."

    testcase iterables:
        description "Loops over a range, a list, and a string run once per item and leave the last item bound."

        parameter (loop_items, loop_last, loop_count) = [(range(4), 3, 4), ([10, 20, 30, 40], 40, 4), ("hello", "o", 5)]

        $ counter = 0
        for item in loop_items:
            $ counter += 1

        assert eval (item == loop_last)
        assert eval (counter == loop_count)

    testcase unpacking:
        description "Tuple targets, nested tuple targets, and `enumerate` bind every name to the last item."

        $ counter = 0
        for (x, y) in [(1, 2), (3, 4), (5, 6)]:
            $ counter += 1

        assert eval (x == 5)
        assert eval (y == 6)
        assert eval (counter == 3)

        $ counter = 0
        for z, (x, y) in [("a", (1, 2)), ("b", (3, 4)), ("c", (5, 6))]:
            $ counter += 1

        assert eval (z == "c")
        assert eval (x == 5)
        assert eval (y == 6)
        assert eval (counter == 3)

        $ counter = 0
        for i, val in enumerate(["a", "b", "c"]):
            $ counter += 1

        assert eval (i == 2)
        assert eval (val == "c")
        assert eval (counter == 3)

    testcase empty_loop:
        description "Empty iterable"

        $ counter = 0
        for test_for_empty_loop_i in []:
            $ counter = 0

        # Loop should not execute, so i is undefined (or should not exist)
        assert eval (not "test_for_empty_loop_i" in locals() and not "test_for_empty_loop_i" in globals())
        assert eval (counter == 0)

    testcase break:
        description "`break` statement exits the loop early"

        parameter loop_stop = [0, 3]

        $ counter = 0
        for i in range(10):
            $ counter += 1
            if eval (i == loop_stop):
                break

        assert eval (i == loop_stop)
        assert eval (counter == loop_stop + 1)

    testcase enumerate_break:
        description "Enumerate with `break` in the middle leaves both targets at the breaking iteration"

        $ counter = 0
        for idx, val in enumerate(['x', 'y', 'z']):
            $ counter += 1
            if eval (idx == 1):
                break

        assert eval (idx == 1)
        assert eval (val == 'y')
        assert eval (counter == 2)

    testcase continue:
        description "`continue` statement skips the rest of the iteration, but not the following ones"

        parameter loop_skip = [0, 1, 3]

        $ counter = 0
        for i in range(4):
            if eval (i == loop_skip):
                continue
            $ counter += 1

        assert eval (i == 3)
        assert eval (counter == 3)

    testcase inner_loop:
        description "`break` and `continue` in an inner loop affect only that loop"

        parameter (inner_break, inner_skip, last_j, expected_counter) = [(99, 99, 2, 9), (1, 99, 1, 6), (99, 1, 2, 6)]

        $ counter = 0
        for i in range(3):
            for j in range(3):
                if eval (j == inner_skip):
                    continue
                $ counter += 1
                if eval (j == inner_break):
                    break

        assert eval (i == 2)
        assert eval (j == last_j)
        assert eval (counter == expected_counter)

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
        assert screen "choice"

        for option in ["Increment", "Increment", "Decrement", "Increment", "Increment"]:
            click text option

        assert "Value: 3" timeout 2.0
        click "Done"


testsuite while_loops:
    description "Tests `while` loop statements with various patterns."

    testcase counting:
        description "A loop runs until its condition becomes false, and not at all if it starts false"

        parameter loop_limit = [4, 0]

        $ i = 0
        $ counter = 0

        while eval (i < loop_limit):
            $ counter += 1
            $ i += 1

        assert eval (i == loop_limit)
        assert eval (counter == loop_limit)

    testcase break:
        description "`break` exits the loop early"

        parameter loop_stop = [0, 3]

        $ i = 0
        $ counter = 0

        while eval (i < 10):
            $ counter += 1
            if eval (i == loop_stop):
                break
            $ i += 1

        assert eval (i == loop_stop)
        assert eval (counter == loop_stop + 1)

    testcase continue:
        description "`continue` skips the rest of the body and keeps iterating"

        parameter (loop_skip, expected_hits) = [(1, [2, 3, 4, 5]), (3, [1, 2, 4, 5]), (5, [1, 2, 3, 4])]

        $ i = 0
        $ hits = []

        while eval (i < 5):
            $ i += 1
            if eval (i == loop_skip):
                continue
            $ hits.append(i)

        assert eval (i == 5)
        assert eval (hits == expected_hits)

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
        assert screen "choice"

        $ clicks = 0
        while eval (menu_var < 3):
            click "Increment"
            click "Increment"
            click "Decrement"
            $ clicks += 1

        assert eval (clicks == 3)
        assert "Value: 3" timeout 2.0
        click "Done"
