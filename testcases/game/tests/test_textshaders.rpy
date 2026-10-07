# Tests for text shaders

# ==============
# == Fixtures ==
# ==============

label textshaders__cps__label:
    "{cps=40}This appears one letter at a time at a speed of 40 characters per second{/cps}"

init python:

    def textshaders__jitter_surface(shader, st, random_value=0.75):
        from unittest.mock import patch

        text = Text("H H H H H H H H", size=40, color="#fff", outlines=[],
                    slow=False, textshader=shader)
        displayable = Fixed(Solid("#000"), Transform(text, xpos=30, ypos=40),
                            xysize=(800, 160))
        with patch("random.random", return_value=random_value):
            return renpy.render_to_surface(displayable, st=st, resize=True)

    def textshaders__pixels(surface):
        return tuple(
            surface.get_at((x, y))[:3]
            for y in range(surface.get_height())
            for x in range(surface.get_width())
        )

    def textshaders__cps_surface(shader, st, tagged=True):
        text = "H " * 20
        if tagged:
            text = "{cps=40}" + text + "{/cps}"
        displayable = Fixed(
            Solid("#000"),
            Text(text, slow=True, slow_cps=True, textshader=shader,
                 size=22, color="#fff", outlines=[]),
            xysize=(740, 80),
        )
        return renpy.render_to_surface(displayable, st=st, resize=True)

    def textshaders__test_cps_tag():
        for shader in (None, "typewriter"):
            complete = textshaders__cps_surface(shader, 0.0, tagged=False)
            assert len(textshaders__glyph_columns(complete)) == 20, shader
            # Sample after each H's reveal interval; the shader starts revealing a glyph before legacy text does.
            for st, expected in ((0.0375, 1), (0.2875, 6), (0.5375, 11), (1.0125, 20)):
                surface = textshaders__cps_surface(shader, st)
                visible = len(textshaders__glyph_columns(surface))
                assert visible == expected, (shader, st, expected, visible)

    def textshaders__glyph_columns(surface):
        occupied = [
            x for x in range(surface.get_width())
            if any(surface.get_at((x, y))[0] > 128
                   for y in range(surface.get_height()))
        ]
        return [x for x in occupied if x - 1 not in occupied]

    def textshaders__glyph_tops(surface, columns):
        return [
            next(y for y in range(surface.get_height())
                 if surface.get_at((x, y))[0] > 128)
            for x in columns
        ]

    def textshaders__test_jitter_duration():
        plain = textshaders__pixels(textshaders__jitter_surface("typewriter", 0.0))
        for individual in (0, 1):
            for duration in (0.5, 1.0):
                shader = f"jitter:0, 40:u__duration={duration}:u__individual={individual}"
                for st in (duration, duration + 1.0):
                    surface = textshaders__jitter_surface(shader, st)
                    assert textshaders__pixels(surface) == plain, (shader, st)

                surface = textshaders__jitter_surface(shader, duration - 0.001)
                assert textshaders__pixels(surface) != plain, shader

            for duration in (0.0, -2.0):
                shader = f"jitter:0, 40:u__duration={duration}:u__individual={individual}"
                for st in (0.0, 1.0, 100.0):
                    surface = textshaders__jitter_surface(shader, st)
                    assert textshaders__pixels(surface) != plain, (shader, st)

            shader = f"jitter:0, 40:u__duration=10:u__individual={individual}"
            assert any(
                textshaders__pixels(textshaders__jitter_surface(shader, st)) != plain
                for st in (0.0, 0.25, 0.5)
            ), shader

    def textshaders__test_jitter_individual():
        reference = textshaders__jitter_surface("typewriter", 0.0)
        columns = textshaders__glyph_columns(reference)
        assert len(columns) == 8
        baseline = textshaders__glyph_tops(reference, columns)

        for shader in ("jitter:0, 40", "jitter:0, 40:u__duration=-2"):
            for st in (0.0, 1.0, 100.0):
                tops = textshaders__glyph_tops(textshaders__jitter_surface(shader, st), columns)
                offsets = [y - base for y, base in zip(tops, baseline)]
                assert max(offsets) - min(offsets) <= 1, offsets
                assert all(abs(offset) <= 21 for offset in offsets), offsets

        for st in (0.0, 1.0, 100.0):
            surface = textshaders__jitter_surface("jitter:0, 40:u__individual=1", st)
            tops = textshaders__glyph_tops(surface, columns)
            offsets = [y - base for y, base in zip(tops, baseline)]
            assert max(offsets) - min(offsets) > 1, offsets
            assert all(abs(offset) <= 21 for offset in offsets), offsets

        for individual in (0, 1):
            shader = f"jitter:0, 40:u__individual={individual}"
            first = textshaders__jitter_surface(shader, 1.0, random_value=0.25)
            second = textshaders__jitter_surface(shader, 1.0, random_value=0.75)
            assert textshaders__pixels(first) != textshaders__pixels(second)

# ==============
# === Tests ====
# ==============

testsuite textshaders:
    after testcase:
        if not screen "main_menu":
            run MainMenu(confirm=False, save=False)

    testcase jitter_duration:
        description "Positive durations stop jitter; zero and negative durations continue indefinitely"
        $ textshaders__test_jitter_duration()

    testcase jitter_individual:
        description "Jitter preserves block movement by default and optionally moves glyphs independently"
        $ textshaders__test_jitter_individual()

    testcase jitter_examples:
        description "Interactive jitter examples are reachable from the testcases menu"

        run Start()
        advance
        click "Text Shaders"
        assert "Default jitter:"
        advance
        assert "Larger jitter:"
        advance
        assert "Individual jitter:"
        advance
        assert "Zero duration:"
        advance
        assert "Negative duration:"
        advance
        assert "Timed block jitter:"
        pause 2.1
        advance
        assert "Timed individual jitter:"
        pause 2.1
        advance
        assert "these words"
        pause 2.1
        advance
        assert "Slow text:"
        pause 2.1
        advance until screen "choice"

    testcase respect_cps_tag:
        description "Typewriter shader follows {cps} when preferences.text_cps = 0"
        # GH-7242: Text shaders should follow the line's {cps} value even if
        # `preferences.text_cps` is set to instant text
        # https://github.com/renpy/renpy/issues/7242

        run Preference("text speed", 0)
        run Start("textshaders__cps__label")
        assert "This appears"
        $ textshaders__test_cps_tag()
        advance until screen "main_menu"
