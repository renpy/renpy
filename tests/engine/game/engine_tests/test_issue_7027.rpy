image issue_7027_white = Solid("#ffffff", xysize=(300, 300))

transform issue_7027_movement_right:
    xoffset 100

transform issue_7027_tint_red:
    matrixcolor TintMatrix("#ff0000")

default issue_7027_some_bool = True

init python:
    def issue_7027_has_matrixcolor(d):
        worklist = [d]

        while worklist:
            d = worklist.pop()

            if isinstance(d, renpy.display.motion.Transform) and (d.state.matrixcolor is not None):
                return True

            worklist.extend(d.visit())

        return False


screen issue_7027_transform_chain():
    $ d = At("issue_7027_white", issue_7027_movement_right, issue_7027_tint_red) if issue_7027_some_bool else At("issue_7027_white", issue_7027_movement_right)

    add d:
        id "subject"
        align (0.5, 0.5)

    textbutton "Toggle tint":
        id "toggle_tint"
        action ToggleVariable("issue_7027_some_bool")


testsuite regressions:
    testcase issue_7027_transform_chain_state:
        $ issue_7027_some_bool = True

        run Show("issue_7027_transform_chain")
        pause until screen "issue_7027_transform_chain"

        python hide:
            d = renpy.get_displayable("issue_7027_transform_chain", "subject", base=True)
            assert d is not None
            assert issue_7027_has_matrixcolor(d)

        click id "toggle_tint"
        pause 0.1

        python hide:
            d = renpy.get_displayable("issue_7027_transform_chain", "subject", base=True)
            assert d is not None
            assert not issue_7027_has_matrixcolor(d)

        run Hide("issue_7027_transform_chain")
