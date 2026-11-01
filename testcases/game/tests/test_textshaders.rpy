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

    def textshaders__jitter_surface(shader, st):
        text = Text("H H H H H H H H", size=40, color="#fff", outlines=[],
                    slow=False, textshader=shader)
        displayable = Fixed(Solid("#000"), Transform(text, xpos=30, ypos=40),
                            xysize=(800, 160))
        return renpy.render_to_surface(displayable, st=st, resize=True)

    def textshaders__differs(a, b):
        """
        Returns True if any pixel differs between surfaces `a` and `b`. Comparing in C makes this
        much faster than reading each pixel with get_at.
        """

        dest = renpy.pygame.Surface(a.get_size(), 0, a)
        return renpy.pygame.transform._diff(dest, a, b, (0, 0, 0, 255), (255, 255, 255, 255)) > 0

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

    def textshaders__jitter_renders(shader, st):
        """
        Returns several renders of `shader` at `st`. Each render picks a new random offset, and with
        a jitter of 40 pixels, one in about 40 of them lands where the text started. Rendering
        several times means that can't make a test fail by chance.
        """

        return [ textshaders__jitter_surface(shader, st) for _ in range(8) ]

    def textshaders__jitter_moved(shader, st):
        """
        Returns True if the text was drawn away from its normal position by any of the renders.
        """

        plain = textshaders__jitter_surface("typewriter", 0.0)
        return any(textshaders__differs(plain, surface) for surface in textshaders__jitter_renders(shader, st))

    def textshaders__jitter_changes(shader, st):
        """
        Returns True if the renders of `shader` at `st` aren't all the same.
        """

        first, *rest = textshaders__jitter_renders(shader, st)
        return any(textshaders__differs(first, surface) for surface in rest)

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
        description "A positive duration stops jitter, returning the text to its normal position"

        $ shader = "jitter:0, 40:u__duration=1.0"
        assert eval textshaders__jitter_moved(shader, 0.999)
        assert eval not textshaders__jitter_moved(shader, 1.0)
        assert eval not textshaders__jitter_moved(shader, 2.0)

    testcase jitter_duration_unlimited:
        description "Zero and negative durations continue jitter indefinitely"
        parameter duration = [ 0.0, -2.0 ]

        assert eval textshaders__jitter_moved(f"jitter:0, 40:u__duration={duration}", 100.0)

    testcase jitter_changes:
        description "Jitter picks a new position each time the text is drawn"

        assert eval textshaders__jitter_changes("jitter:0, 40", 1.0)

    testcase jitter_block:
        description "Jitter moves all glyphs together by default"

        assert eval len(textshaders__glyph_columns(textshaders__jitter_surface("typewriter", 0.0))) == 8
        $ offsets = textshaders__jitter_offsets("jitter:0, 40", 1.0)
        assert eval max(offsets) - min(offsets) <= 1
        assert eval all(abs(offset) <= 21 for offset in offsets)

    testcase jitter_individual:
        description "Jitter can move glyphs independently"

        $ offsets = textshaders__jitter_offsets("jitter:0, 40:u__individual=1", 1.0)
        assert eval max(offsets) - min(offsets) > 1
        assert eval all(abs(offset) <= 21 for offset in offsets)

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
        advance
        assert "Timed individual jitter:"
        advance
        assert "these words"
        advance
        assert "Slow text:"
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
