# This file tests the text tokenizer in renpy.text.textsupport.

init python:

    def textsupport__tokenize(s):
        import renpy.text.textsupport as textsupport
        return tuple(textsupport.tokenize(s))

    def textsupport__text(s):
        """The text runs of the tokenized string, with the tags dropped."""
        import renpy.text.textsupport as textsupport
        return tuple(
            value for kind, value in textsupport.tokenize(s)
            if kind == textsupport.TEXT
        )

# ==============
# === Tests ====
# ==============

testsuite textsupport:

    testcase dangling_lenticular_bracket_is_kept:
        description "A 【 that ends a text run is kept instead of being dropped"
        # GH-7393: The final flush in lenticular_bracket_ruby() only ran for a
        # non-empty buf, so a text run ending in 【 was silently dropped, while
        # a 【 followed by any text survived.
        # https://github.com/renpy/renpy/issues/7393

        assert eval textsupport__text("abc【") == ("abc", "【")
        assert eval textsupport__text("啊【") == ("啊", "【")
        assert eval textsupport__text("【") == ("【",)
        assert eval textsupport__text("abc【a｜b】") == ("abc", "a", "b")

    testcase unterminated_lenticular_bracket_behaviour_unchanged:
        description "Text runs that already worked keep their existing output"
        # The same change must not alter the cases the flush already handled.

        assert eval textsupport__text("【啊") == ("【啊",)
        assert eval textsupport__text("【【") == ("【",)
        assert eval textsupport__text("abc") == ("abc",)
        assert eval textsupport__text("") == ()
        assert eval textsupport__text("【a】") == ("【a】",)
        assert eval textsupport__text("【a｜b") == ("a", "b")

        # A bracketed run still turns into rb/rt tags.
        $ tokens = textsupport__tokenize("【a｜b】")
        assert eval [v for k, v in tokens if k == 1] == ["a", "b"]
        assert eval [v for k, v in tokens if k == 2] == ["rb", "/rb", "rt", "/rt"]
