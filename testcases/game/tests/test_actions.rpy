# Tests for action and bar value tooltips and mouse cursors.

# ==============
# == Fixtures ==
# ==============

init python in testcases.actions:
    import store

    class Action(store.Action):
        def __init__(self, tooltip=None, mouse=None):
            self.tooltip = tooltip
            self.mouse = mouse

        def __call__(self):
            return None

        def get_tooltip(self):
            return self.tooltip

        def get_mouse(self):
            return self.mouse


    class BarValue(store.BarValue):
        def __init__(self, tooltip=None, mouse=None, adjustable=True):
            self.tooltip = tooltip
            self.mouse = mouse
            self.adjustable = adjustable

        def get_adjustment(self):
            return ui.adjustment(range=1, value=0, adjustable=self.adjustable)

        def get_tooltip(self):
            return self.tooltip

        def get_mouse(self):
            return self.mouse


    class DefaultBarValue(store.BarValue):
        def get_adjustment(self):
            return ui.adjustment(range=1, value=0, adjustable=True)


    class Displayable(renpy.Displayable):
        focusable = True

        def render(self, width, height, st, at):
            """Provide a focus region without inheriting button cursor behavior."""
            rv = renpy.Render(200, 40)
            rv.add_focus(self, None, 0, 0, 200, 40)
            return rv


    class CustomMouseDisplayable(Displayable):
        def _get_mouse(self):
            return "custom_mouse"


    def plain_action():
        return None


    def make_action(kind, tooltip, mouse):
        """Build the public action and wrapper combinations used by hover tests."""
        action = Action(tooltip, mouse)
        if kind == "action":
            return action
        elif kind == "selected_if":
            return store.SelectedIf(action)
        elif kind == "sensitive_if":
            return store.SensitiveIf(action)
        elif kind == "list":
            return [None, plain_action, store.NullAction(), action, Action("later", "later")]
        elif kind == "tuple":
            return (None, plain_action, store.NullAction(), action, Action("later", "later"))
        elif kind == "nested":
            return [None, (store.NullAction(), [action]), Action("later", "later")]
        elif kind == "selected_if_list":
            return store.SelectedIf([store.NullAction(), action])
        elif kind == "selected_if_tuple":
            return store.SelectedIf((store.NullAction(), action))
        elif kind == "sensitive_if_list":
            return store.SensitiveIf([store.NullAction(), action])
        elif kind == "sensitive_if_tuple":
            return store.SensitiveIf((store.NullAction(), action))
        elif kind == "split":
            return [Action(tooltip=tooltip), Action(mouse=mouse)]
        elif kind == "nested_wrappers":
            return store.SelectedIf(store.SensitiveIf(store.Confirm("Confirm?", [action])))
        elif kind == "confirm":
            return store.Confirm("Confirm?", action)
        elif kind == "null":
            return store.NullAction()
        elif kind == "callable":
            return plain_action
        elif kind == "selected_if_bool":
            return store.SelectedIf(True)
        elif kind == "sensitive_if_bool":
            return store.SensitiveIf(True)
        elif kind == "empty_list":
            return []
        elif kind == "empty_tuple":
            return ()
        elif kind == "none":
            return None
        elif kind == "insensitive":
            return store.SensitiveIf(False)

        raise ValueError("Unknown test action kind: " + kind)


screen test_actions__screen(tooltip=None, mouse=None, kind="action", overrides=None, adjustable=True, vertical=False):
    vbox:
        pos (100, 100)
        spacing 30

        textbutton "Action":
            id "test_actions__action_button"
            action testcases.actions.make_action(kind, tooltip, mouse)
            properties (overrides or {})

        if vertical:
            vbar:
                id "test_actions__bar_value_bar"
                xysize (40, 200)
                value testcases.actions.BarValue(tooltip, mouse, adjustable)
                properties (overrides or {})
        else:
            bar:
                id "test_actions__bar_value_bar"
                xysize (400, 40)
                value testcases.actions.BarValue(tooltip, mouse, adjustable)
                properties (overrides or {})

        textbutton "Other":
            id "test_actions__other_button"
            action NullAction()
            tooltip "other tooltip"
            mouse "other_mouse"


screen test_actions__default_bar():
    bar:
        id "test_actions__default_bar"
        pos (100, 100)
        xysize (400, 40)
        value testcases.actions.DefaultBarValue()


screen test_actions__displayable(custom=False, tooltip=None, mouse=None):
    if custom:
        add testcases.actions.CustomMouseDisplayable(tooltip=tooltip, mouse=mouse):
            id "test_actions__displayable"
            pos (100, 100)
    else:
        add testcases.actions.Displayable(tooltip=tooltip, mouse=mouse):
            id "test_actions__displayable"
            pos (100, 100)


screen test_actions__imagebutton(tooltip=None, mouse=None):
    imagebutton:
        id "test_actions__imagebutton"
        pos (100, 100)
        idle Solid("#fff", xysize=(200, 40))
        action testcases.actions.Action(tooltip, mouse)


style test_actions__button is button:
    mouse "style_mouse"


# ==============
# === Tests ====
# ==============

testsuite actions:
    before testcase:
        move pos (0, 0)

    after testcase:
        run Hide("test_actions__screen")
        run Hide("test_actions__default_bar")
        run Hide("test_actions__displayable")
        run Hide("test_actions__imagebutton")

    testsuite tooltip:
        testcase button_action_tooltip:
            parameter kind = ["action", "selected_if", "sensitive_if", "selected_if_list", "selected_if_tuple", "sensitive_if_list", "sensitive_if_tuple", "confirm", "nested_wrappers", "split"]
            run Show("test_actions__screen", kind=kind)
            move id "test_actions__action_button"
            assert eval GetTooltip() is None
            run Show("test_actions__screen", kind=kind, tooltip="button_action_tooltip")
            assert eval GetTooltip() == "button_action_tooltip"
            run Show("test_actions__screen", kind=kind)
            assert eval GetTooltip() is None

        testcase first_tooltip_in_action_list:
            parameter kind = ["list", "tuple", "nested"]
            parameter tooltip = ["first", "", False, 0]
            run Show("test_actions__screen", kind=kind, tooltip=tooltip)
            move id "test_actions__action_button"
            assert eval GetTooltip() == tooltip

        testcase non_string_tooltip:
            run Show("test_actions__screen", tooltip=("tuple", "tooltip"))
            move id "test_actions__action_button"
            assert eval GetTooltip() == ("tuple", "tooltip")

        testcase action_list_skips_none:
            parameter kind = ["list", "tuple", "nested"]
            run Show("test_actions__screen", kind=kind)
            move id "test_actions__action_button"
            assert eval GetTooltip() == "later"

        testcase default_tooltip:
            parameter kind = ["null", "callable", "selected_if_bool", "sensitive_if_bool"]
            run Show("test_actions__screen", kind=kind)
            move id "test_actions__action_button"
            assert eval GetTooltip() is None

        testcase insensitive_button:
            parameter kind = ["none", "empty_list", "empty_tuple", "insensitive"]
            run Show("test_actions__screen", kind=kind, overrides={"tooltip": "not focusable"})
            move id "test_actions__action_button"
            assert eval GetTooltip() is None

        testcase explicit_tooltip_overrides_action_or_bar_value:
            parameter widget = ["test_actions__action_button", "test_actions__bar_value_bar"]
            parameter tooltip = ["explicit", "", False, 0]
            run Show("test_actions__screen", tooltip="inherited", overrides={"tooltip": tooltip})
            move id widget
            assert eval GetTooltip() == tooltip

        testcase explicit_none_tooltip:
            parameter (widget, expected) = [("test_actions__action_button", "inherited"), ("test_actions__bar_value_bar", None)]
            run Show("test_actions__screen", tooltip="inherited", overrides={"tooltip": None})
            move id widget
            assert eval GetTooltip() == expected

        testcase bar_value_tooltip:
            parameter vertical = [False, True]
            run Show("test_actions__screen", vertical=vertical)
            move id "test_actions__bar_value_bar"
            assert eval GetTooltip() is None
            run Show("test_actions__screen", vertical=vertical, tooltip="bar_value_tooltip")
            assert eval GetTooltip() == "bar_value_tooltip"
            run Show("test_actions__screen", vertical=vertical)
            assert eval GetTooltip() is None

        testcase default_bar_value_tooltip:
            run Show("test_actions__default_bar")
            move id "test_actions__default_bar"
            assert eval GetTooltip() is None

        testcase unadjustable_bar:
            run Show("test_actions__screen", tooltip="not focusable", adjustable=False)
            move id "test_actions__bar_value_bar"
            assert eval GetTooltip() is None

        testcase displayable_tooltip:
            run Show("test_actions__displayable", tooltip="displayable tooltip", mouse="displayable_mouse")
            move id "test_actions__displayable"
            assert eval GetTooltip() == "displayable tooltip"

        testcase imagebutton_action_tooltip:
            run Show("test_actions__imagebutton", tooltip="imagebutton tooltip")
            move id "test_actions__imagebutton"
            assert eval GetTooltip() == "imagebutton tooltip"

        testcase focus_changes:
            run Show("test_actions__screen", tooltip="action tooltip")
            move id "test_actions__action_button"
            assert eval GetTooltip("test_actions__screen") == "action tooltip"
            assert eval GetTooltip("main_menu") is None
            move id "test_actions__other_button"
            assert eval GetTooltip() == "other tooltip"
            move pos (0, 0)
            assert eval GetTooltip() is None
            assert eval GetTooltip(last=True) == "other tooltip"
            move id "test_actions__action_button"
            run Hide("test_actions__screen")
            assert eval GetTooltip() is None

    testsuite mouse:
        testcase button_action_mouse:
            parameter kind = ["action", "selected_if", "sensitive_if", "selected_if_list", "selected_if_tuple", "sensitive_if_list", "sensitive_if_tuple", "confirm", "nested_wrappers", "split"]
            run Show("test_actions__screen", kind=kind)
            move id "test_actions__action_button"
            assert eval renpy.get_mouse_name() == "button"
            run Show("test_actions__screen", kind=kind, mouse="action_mouse")
            assert eval renpy.get_mouse_name() == "action_mouse"
            assert eval renpy.get_mouse_names()[0] == "action_mouse"
            run Show("test_actions__screen", kind=kind)
            assert eval renpy.get_mouse_name() == "button"

        testcase first_mouse_in_action_list:
            parameter kind = ["list", "tuple", "nested"]
            run Show("test_actions__screen", kind=kind, mouse="first_mouse")
            move id "test_actions__action_button"
            assert eval renpy.get_mouse_name() == "first_mouse"

        testcase action_list_skips_none:
            parameter kind = ["list", "tuple", "nested"]
            run Show("test_actions__screen", kind=kind)
            move id "test_actions__action_button"
            assert eval renpy.get_mouse_name() == "later"

        testcase default_button_mouse:
            parameter kind = ["null", "callable", "selected_if_bool", "sensitive_if_bool"]
            run Show("test_actions__screen", kind=kind)
            move id "test_actions__action_button"
            assert eval renpy.get_mouse_name() == "button"

        testcase insensitive_button:
            parameter kind = ["none", "empty_list", "empty_tuple", "insensitive"]
            run Show("test_actions__screen", kind=kind, overrides={"mouse": "not_focusable"})
            move id "test_actions__action_button"
            assert eval renpy.get_mouse_name() == "default"

        testcase explicit_mouse_overrides_action_or_bar_value:
            parameter widget = ["test_actions__action_button", "test_actions__bar_value_bar"]
            run Show("test_actions__screen", mouse="inherited", overrides={"mouse": "explicit"})
            move id widget
            assert eval renpy.get_mouse_name() == "explicit"
            assert eval renpy.get_mouse_names()[0] == "explicit"

        testcase explicit_none_mouse:
            parameter (widget, expected) = [("test_actions__action_button", "inherited"), ("test_actions__bar_value_bar", "default")]
            run Show("test_actions__screen", mouse="inherited", overrides={"mouse": None})
            move id widget
            assert eval renpy.get_mouse_name() == expected

        testcase style_mouse_overrides_action:
            run Show("test_actions__screen", mouse="inherited", overrides={"style": "test_actions__button"})
            move id "test_actions__action_button"
            assert eval renpy.get_mouse_name() == "style_mouse"

        testcase bar_value_mouse:
            parameter vertical = [False, True]
            run Show("test_actions__screen", vertical=vertical)
            move id "test_actions__bar_value_bar"
            assert eval renpy.get_mouse_name() == "default"
            run Show("test_actions__screen", vertical=vertical, mouse="bar_mouse")
            assert eval renpy.get_mouse_name() == "bar_mouse"
            run Show("test_actions__screen", vertical=vertical)
            assert eval renpy.get_mouse_name() == "default"

        testcase default_bar_value_mouse:
            run Show("test_actions__default_bar")
            move id "test_actions__default_bar"
            assert eval renpy.get_mouse_name() == "default"

        testcase unadjustable_bar:
            run Show("test_actions__screen", mouse="not_focusable", adjustable=False)
            move id "test_actions__bar_value_bar"
            assert eval renpy.get_mouse_name() == "default"

        testcase displayable_mouse:
            parameter (custom, mouse, expected) = [(False, None, "default"), (False, "style_mouse", "style_mouse"), (True, "style_mouse", "custom_mouse")]
            run Show("test_actions__displayable", custom=custom, mouse=mouse, tooltip="not the cursor")
            move id "test_actions__displayable"
            assert eval renpy.get_mouse_name() == expected

        testcase imagebutton_action_mouse:
            parameter mouse = [None, "imagebutton_mouse"]
            run Show("test_actions__imagebutton", mouse=mouse)
            move id "test_actions__imagebutton"
            assert eval renpy.get_mouse_name() == (mouse or "button")

        testcase focus_changes:
            run Show("test_actions__screen", mouse="action_mouse")
            move id "test_actions__action_button"
            assert eval renpy.get_mouse_name() == "action_mouse"
            move id "test_actions__other_button"
            assert eval renpy.get_mouse_name() == "other_mouse"
            move pos (0, 0)
            assert eval renpy.get_mouse_name() == "default"
            move id "test_actions__action_button"
            run Hide("test_actions__screen")
            assert eval renpy.get_mouse_name() == "default"
