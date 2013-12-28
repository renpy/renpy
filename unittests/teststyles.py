#@PydevCodeAnalysisIgnore
import unittest

import renpy
renpy.import_all()
from renpy.styleaccel import Style, StyleManager, build_styles


class TestStyles(unittest.TestCase):

    def test_set_prefix(self):
        s = Style(None)

        s.bold = "insensitive"
        s.hover_bold = "hover"
        s.selected_bold = "selected"
        s.selected_hover_bold = "selected_hover"

        renpy.styleaccel.build_style(s)

        assert s.bold == "insensitive"

        s.set_prefix("hover_")
        assert s.bold == "hover"

        s.set_prefix("selected_idle_")
        assert s.bold == "selected"

        s.set_prefix("selected_hover_")
        assert s.bold == "selected_hover"

        s.set_prefix("insensitive_")
        assert s.bold == "insensitive"

    def test_inheritance(self):

        sm = StyleManager()

        sm.default = Style(None)

        assert sm.default is sm.default
        assert sm.default.name == ("default",)
        assert sm.default.parent is None

        assert sm.prefs_default is sm.prefs_default
        assert sm.prefs_default.name == ("prefs_default",)
        assert sm.prefs_default.parent == ("default",)

        assert sm.default["foo"] is sm.default["foo"]
        assert sm.default["foo"].name == ("default","foo")
        assert sm.default["foo"].parent is None

        assert sm.prefs_default["foo"] is sm.prefs_default["foo"]
        assert sm.prefs_default["foo"].name == ("prefs_default","foo")
        assert sm.prefs_default["foo"].parent == ("default","foo")

        sm.default.size = "default"
        sm.default.italic = "default"
        sm.default.bold = "default"

        sm.prefs_default.italic = "prefs_default"
        sm.prefs_default.bold = "prefs_default"

        sm.default["foo"].bold = "default_foo"

        build_styles()

        s = sm.prefs_default["foo"]

        assert s.bold == "default_foo"
        assert s.italic == "prefs_default"
        assert s.size == "default"






