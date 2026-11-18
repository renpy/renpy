# This file tests how safe-text mode displays malformed dialogue.

init python:

    def safe_text__what():
        """The text displayable of the current say statement."""
        return renpy.get_widget("say", "what")

    def safe_text__shown():
        """The text runs that the what displayable shows."""
        from renpy.text.textsupport import TEXT
        return [ value for kind, value in safe_text__what().tokens if kind == TEXT ]

    def safe_text__hides_tail():
        """
        True if layout got the marker that hides the text after it, False if it didn't, and None if the say statement
        hasn't been laid out yet.
        """
        what = safe_text__what()
        layout = what.get_layout() if what is not None else None

        if layout is None:
            return None

        return layout.end_segment is not None

    def safe_text__segments():
        """
        The (text, bold) pairs of the text segments in the laid-out say statement, or None if it hasn't been laid out.
        """
        what = safe_text__what()
        layout = what.get_layout() if what is not None else None

        if layout is None:
            return None

        return [
            (text, bool(segment.bold))
            for paragraph in layout.paragraphs
            for segment, text in paragraph
            if hasattr(segment, "bold")
        ]

define safe_text__speaker = Character(None, what_safe=True)

# These use Python calls rather than say statements, since lint correctly reports the malformed text in say statements.

label safe_text__dialogue:
    $ safe_text__speaker("one{w}two {")
    return

label safe_text__empty_tag:
    $ safe_text__speaker("a{w}b {}")
    return

label safe_text__bad_tag_value:
    $ safe_text__speaker("{size=30{w}more{w}end")
    return

label safe_text__failed_tag_closed:
    $ safe_text__speaker("{b}{size=abc}x{/size} y{/b}")
    return

# ==============
# === Tests ====
# ==============

testsuite safe_text:

    after testcase:
        if not screen "main_menu":
            run MainMenu(confirm=False, save=False)

    testcase pause_hides_tail_of_malformed_dialogue:
        description "An unclosed tag doesn't reveal the text after a pause, or the marker that hides it"
        # Text.update joins {_end} onto the text after the pause, so the unclosed tag used to make that whole string
        # fall back to literal text, which displayed the marker and the hidden text.

        run Start("safe_text__dialogue")

        assert eval (safe_text__hides_tail() is True) timeout 2.0
        assert eval (safe_text__shown() == ["one", "{w}two {"])

        # The first dismiss may only finish showing slow text, so this repeats until the pause ends.
        keysym "dismiss" until eval (safe_text__hides_tail() is False)

        assert eval (safe_text__shown() == ["one", "{w}two {"])

    testcase empty_tag_keeps_tail_hidden:
        description "An empty tag displays literally, without revealing the text after a pause or the marker hiding it"

        run Start("safe_text__empty_tag")

        assert eval (safe_text__hides_tail() is True) timeout 2.0
        assert eval (safe_text__shown() == ["a", "{w}b {}"])

        keysym "dismiss" until eval (safe_text__hides_tail() is False)

        assert eval (safe_text__shown() == ["a", "{w}b {}"])

    testcase bad_tag_value_doesnt_raise:
        description "A dialogue tag that ends up in the value of another tag doesn't raise on any page"
        # The tag is size=30{w, which can't be parsed as a size. Laying it out shows the tag as text instead of raising,
        # which it does on the last page, once the whole string is laid out.

        run Start("safe_text__bad_tag_value")

        assert eval (safe_text__hides_tail() is True) timeout 2.0
        assert eval (safe_text__shown() == ["{size=30", "more", "end"])

        keysym "dismiss" until eval (safe_text__hides_tail() is False)

        assert eval (safe_text__shown() == ["more", "end"])

    testcase failed_tag_keeps_close_tag_balanced:
        description "The close tag of a tag that fails in safe mode doesn't close the enclosing tag"
        # {size=abc} can't be parsed, so it's shown as text. {/size} must then close that tag and not the bold one.

        run Start("safe_text__failed_tag_closed")

        assert eval (safe_text__segments() == [("size=abc", True), ("x", True), (" y", True)]) timeout 2.0
