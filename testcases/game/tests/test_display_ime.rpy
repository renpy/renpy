# Tests for the in-game list of input method (IME) candidates.

# ==============
# == Fixtures ==
# ==============

screen ime__candidates__screen():
    default input_value = ""

    input:
        id "ime_input"
        value ScreenVariableInputValue('input_value')


init python:

    def ime__set_candidates(*candidates):
        """
        Makes Ren'Py behave as if the input method offered `candidates`, with the first one selected.
        """

        renpy.display.interface.set_text_editing_candidates(
            renpy.display.ime.IMECandidates(candidates, 0, True)
        )

    def ime__get_candidate_texts():
        """
        Returns the text of each candidate displayed by the _ime_candidates screen, in order, or
        None if the screen is not showing.
        """

        screen = renpy.get_screen("_ime_candidates")

        if screen is None:
            return None

        rv = [ ]

        def collect(d):
            if isinstance(d, Text):
                rv.append("".join(i for i in d.text if isinstance(i, str)))

        screen.visit_all(collect)

        return rv


# ==============
# === Tests ====
# ==============

testsuite display_ime:
    testcase candidates_shown_as_supplied:
        description "Candidates are displayed as the input method supplies them, without a second number."
        # GH-7535: SDL prefixes each candidate with the digit that selects it, and the screen
        # added a number of its own. The second candidate also checks that text tags are quoted.

        run Show("ime__candidates__screen")
        assert id "ime_input"

        $ ime__set_candidates("1 你", "2 {好}")
        pause 0.1

        assert screen "_ime_candidates"
        assert eval ime__get_candidate_texts() == ["1 你", "2 {{好}"]

        $ renpy.display.interface.set_text_editing_candidates(None)
        pause 0.1

        assert not screen "_ime_candidates"

        run Hide("ime__candidates__screen")
