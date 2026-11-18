# Tests for interacting with input fields in various scenarios

# ==============
# == Fixtures ==
# ==============

screen input__mesh_property__screen():
    default show = False
    default input_value = ""

    button:
        at transform:
            mesh True

        action ToggleScreenVariable('show')

        if show:
            input:
                id "transform_input"
                value ScreenVariableInputValue('input_value')

        else:
            text "Click to input":
                id "transform_input_click"


# ==============
# === Tests ====
# ==============

testsuite input:
    testcase input_accepts_text_inside_mesh:
        description "Input inside mesh True transform accepts typed text."
        # GH-7177: Input field does not work stably when a parent displayable has `mesh True`.
        # https://github.com/renpy/renpy/issues/7177

        run Show("input__mesh_property__screen")
        assert screen "input__mesh_property__screen"

        click id "transform_input_click"
        assert id "transform_input"

        type "Hello"

        $ value = renpy.exports.get_screen("input__mesh_property__screen").scope.get("input_value", "NOT DEFINED")
        $ assert value == "Hello", f"Expected 'Hello', got '{value}'"

        run Hide("input__mesh_property__screen")
