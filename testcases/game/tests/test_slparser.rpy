init python:
    def slparser_legacy_screen(**kwargs):
        renpy.ui.text("Legacy content")

    renpy.display.screen.define_screen("slparser_legacy_screen", slparser_legacy_screen)

    def slparser_legacy_failure_stack():
        node = renpy.sl2.slast.SLUse(("test_slparser.rpy", 1), "slparser_missing_screen", None, None, None, None)
        context = renpy.sl2.slast.SLContext()
        old_stack = list(renpy.ui.stack)

        try:
            node.execute_use_screen(context)
        except renpy.display.screen.ScreenNotFound:
            pass
        else:
            raise AssertionError("Missing screen did not raise")

        assert len(renpy.ui.stack) == len(old_stack)
        assert all(a is b for a, b in zip(renpy.ui.stack, old_stack))


screen slparser_legacy_root():
    use slparser_legacy_screen
    text "SL2 content"


screen slparser_legacy_nested():
    vbox:
        use slparser_legacy_screen
        text "SL2 content"


testsuite slparser:

    testcase legacy_screen_use:
        run Show("slparser_legacy_root")
        assert eval len(renpy.get_screen("slparser_legacy_root").child.children) == 2
        run Hide("slparser_legacy_root")

        run Show("slparser_legacy_nested")
        assert eval len(renpy.get_screen("slparser_legacy_nested").child.children[0].children) == 2
        run Hide("slparser_legacy_nested")

    testcase legacy_screen_failure_restores_stack:
        $ slparser_legacy_failure_stack()

    testcase keyword_error_suggestions:
        $ text_parser = renpy.sl2.slparser.statements["text"]
        $ screen_parser = renpy.sl2.slparser.statements["screen"]
        $ textbutton_parser = renpy.sl2.slparser.statements["textbutton"]

        $ expected = "The text statement does not accept 'text_' prefixed properties. Did you mean: 'outlines'?"
        assert eval text_parser.get_keyword_error("text_outlines") == expected

        $ expected = "'selectedidle' is not a valid style property prefix. Did you mean: 'selected_idle'?"
        assert eval text_parser.get_keyword_error("selectedidle_color") == expected

        $ expected = "'outline' is not a keyword argument or valid child of the text statement."
        $ expected += " Did you mean: 'outlines'?"
        assert eval text_parser.get_keyword_error("outline") == expected

        $ expected = "'vboz' is not a keyword argument or valid child of the screen statement. Did you mean: 'vbox'?"
        assert eval screen_parser.get_keyword_error("vboz") == expected

        $ expected = "'text_outline' is not a keyword argument or valid child of the textbutton statement."
        $ expected += " Did you mean: 'text_outlines'?"
        assert eval textbutton_parser.get_keyword_error("text_outline") == expected

        $ expected = "'not_a_property' is not a keyword argument or valid child of the text statement."
        assert eval text_parser.get_keyword_error("not_a_property") == expected
