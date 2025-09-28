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

testcase skip(enabled=False):
    assert False

testsuite test_subcase:
    before testcase:
        $ test_subcase_setup = False

    after testcase:
        assert eval test_subcase_setup

    testcase subcase1:
        assert eval (not test_subcase_setup)
        $ test_subcase_setup = True

    testsuite subcase2:
        before testcase:
            assert eval (not test_subcase_setup)

        testcase subcase2_2:
            $ test_subcase_setup = True


testsuite test_if:
    ## Check that if blocks work

    testcase boolean_value_true:
        assert True

    testcase boolean_value_false:
        assert False

    testcase boolean_operators:
        assert not False

        assert not not True

        assert True or False

        assert False or True

        assert not (True and False)

        assert not (False and True)

    # assert eval (False or True)

    # if eval (renpy.is_in_test() == False):
    #     assert False

testsuite message_if:
    setup:
        run Jump("three_messages")
        pause until screen say

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

testsuite timeout:
    testcase hard_pause_timeout:
        # Make sure _test.timeout can be changed
        run Jump("hard_pause")
        pause until screen say

        $ _test.timeout = 7
        advance until "End"
        $ _test.timeout = 5

testcase teleporting_button_test:
    run Show("teleporting_button")
    pause until screen teleporting_button
    click id "teleporting_button" until not screen teleporting_button
