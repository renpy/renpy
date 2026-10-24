# Tests for text shaders

# ==============
# == Fixtures ==
# ==============

# Horizontal bands of increasing brightness. As this is not an image file, it's rendered to a
# texture at the drawable resolution.
image textshaders_bands = Fixed(
    *[ Solid("#%02x%02xff" % (i * 20, i * 20), xysize=(400, 5), ypos=i * 5) for i in range(12) ],
    xysize=(400, 60))

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

    def textshaders__visible_glyphs(shader, st, tagged=True):
        return len(textshaders__glyph_columns(textshaders__cps_surface(shader, st, tagged)))

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

    def textshaders__jitter_pixels(shader, st, random_value=0.75):
        return textshaders__pixels(textshaders__jitter_surface(shader, st, random_value))

    def textshaders__jitter_offsets(shader, st):
        """
        Returns the vertical offset of each glyph rendered with `shader` at `st`, relative to
        the same glyph rendered without jitter.
        """

        reference = textshaders__jitter_surface("typewriter", 0.0)
        columns = textshaders__glyph_columns(reference)
        baseline = textshaders__glyph_tops(reference, columns)
        tops = textshaders__glyph_tops(textshaders__jitter_surface(shader, st), columns)
        return [ y - base for y, base in zip(tops, baseline) ]

    def textshaders__texture_profile(shader, draw_per_virt):
        """
        Renders three lines of text with `shader` while simulating a window scaled by
        `draw_per_virt`, and returns the brightest red value of each row of the result.
        """

        draw = renpy.display.draw
        old = (draw.draw_per_virt, draw.virt_to_draw, draw.draw_to_virt)

        try:
            draw.draw_per_virt = draw_per_virt
            draw.virt_to_draw = renpy.display.matrix.Matrix2D(draw_per_virt, 0, 0, draw_per_virt)
            draw.draw_to_virt = renpy.display.matrix.Matrix2D(1 / draw_per_virt, 0, 0, 1 / draw_per_virt)
            renpy.text.text.layout_cache_clear()

            text = Text("HHHH\nHHHH\nHHHH", size=30, color="#fff", outlines=[], slow=False, textshader=shader)
            surface = renpy.render_to_surface(Fixed(Solid("#000"), text, xysize=(200, 120)), resize=True)

        finally:
            draw.draw_per_virt, draw.virt_to_draw, draw.draw_to_virt = old
            renpy.text.text.layout_cache_clear()

        rv = [ ]

        for y in range(surface.get_height()):
            row = [ surface.get_at((x, y))[:3] for x in range(surface.get_width()) ]
            lit = [ p[0] for p in row if max(p) > 100 ]
            rv.append(max(lit) if lit else 0)

        return rv

    def textshaders__profile_difference(reference, scaled):
        """
        Returns the mean per-row brightness difference between two texture profiles.
        """

        return sum(abs(a - b) for a, b in zip(reference, scaled)) / sum(1 for i in reference if i)

# ==============
# === Tests ====
# ==============

testsuite textshaders:
    after testcase:
        if not screen "main_menu":
            run MainMenu(confirm=False, save=False)

    testcase jitter_duration_ends:
        description "Positive durations stop jitter"
        parameter individual = [ 0, 1 ]
        parameter duration = [ 0.5, 1.0 ]

        $ plain = textshaders__jitter_pixels("typewriter", 0.0)
        $ shader = f"jitter:0, 40:u__duration={duration}:u__individual={individual}"
        assert eval textshaders__jitter_pixels(shader, duration - 0.001) != plain
        assert eval textshaders__jitter_pixels(shader, duration) == plain
        assert eval textshaders__jitter_pixels(shader, duration + 1.0) == plain

    testcase jitter_duration_unlimited:
        description "Zero and negative durations continue jitter indefinitely"
        parameter individual = [ 0, 1 ]
        parameter duration = [ 0.0, -2.0 ]
        parameter st = [ 0.0, 1.0, 100.0 ]

        $ plain = textshaders__jitter_pixels("typewriter", 0.0)
        $ shader = f"jitter:0, 40:u__duration={duration}:u__individual={individual}"
        assert eval textshaders__jitter_pixels(shader, st) != plain

    testcase jitter_duration_active:
        description "Jitter is visible before a positive duration ends"
        parameter individual = [ 0, 1 ]

        $ plain = textshaders__jitter_pixels("typewriter", 0.0)
        $ shader = f"jitter:0, 40:u__duration=10:u__individual={individual}"
        assert eval any(textshaders__jitter_pixels(shader, st) != plain for st in (0.0, 0.25, 0.5))

    testcase jitter_block:
        description "Jitter moves all glyphs together by default"
        parameter shader = [ "jitter:0, 40", "jitter:0, 40:u__duration=-2" ]
        parameter st = [ 0.0, 1.0, 100.0 ]

        assert eval len(textshaders__glyph_columns(textshaders__jitter_surface("typewriter", 0.0))) == 8
        $ offsets = textshaders__jitter_offsets(shader, st)
        assert eval max(offsets) - min(offsets) <= 1
        assert eval all(abs(offset) <= 21 for offset in offsets)

    testcase jitter_individual:
        description "Jitter can move glyphs independently"
        parameter st = [ 0.0, 1.0, 100.0 ]

        $ offsets = textshaders__jitter_offsets("jitter:0, 40:u__individual=1", st)
        assert eval max(offsets) - min(offsets) > 1
        assert eval all(abs(offset) <= 21 for offset in offsets)

    testcase jitter_random:
        description "Jitter offsets follow the random source"
        parameter individual = [ 0, 1 ]

        $ shader = f"jitter:0, 40:u__individual={individual}"
        $ first = textshaders__jitter_pixels(shader, 1.0, random_value=0.25)
        $ second = textshaders__jitter_pixels(shader, 1.0, random_value=0.75)
        assert eval first != second

    testcase texture_scale:
        description "Texture and linetexture keep their virtual size when the window is scaled"
        # GH-7104: The texture was scaled by the drawable-to-virtual ratio when the
        # texture displayable was rendered to a texture.
        # https://github.com/renpy/renpy/issues/7104
        parameter shader = [ "linetexture:textshaders_bands", "texture:textshaders_bands" ]

        $ reference = textshaders__texture_profile(shader, 1.0)
        $ scaled = textshaders__texture_profile(shader, 2.0)
        assert eval textshaders__profile_difference(reference, scaled) < 5

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

        parameter shader = [ None, "typewriter" ]

        run Preference("text speed", 0)
        run Start("textshaders__cps__label")
        assert "This appears"
        assert eval textshaders__visible_glyphs(shader, 0.0, tagged=False) == 20

        # Sample after each H's reveal interval; the shader starts revealing a glyph before legacy text does.
        assert eval textshaders__visible_glyphs(shader, 0.0375) == 1
        assert eval textshaders__visible_glyphs(shader, 0.2875) == 6
        assert eval textshaders__visible_glyphs(shader, 0.5375) == 11
        assert eval textshaders__visible_glyphs(shader, 1.0125) == 20
        advance until screen "main_menu"
