testsuite slparser:

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
