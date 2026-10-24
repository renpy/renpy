import ast
import os
import unittest
from pathlib import Path
from textwrap import dedent
from types import SimpleNamespace
from unittest.mock import patch

import renpy
from unittests.renpy_test_support import initialize_renpy

initialize_renpy()

from renpy import character
from renpy.display import screen
from renpy.exports import menuexports


class TestScreenLayers(unittest.TestCase):
    def start_patch(self, patcher):
        value = patcher.start()
        self.addCleanup(patcher.stop)
        return value

    def setUp(self):
        self.start_patch(patch.object(renpy.exports, "shown_window"))
        self.start_patch(patch.object(screen, "has_screen", return_value=True))
        self.start_patch(patch.object(renpy.exports, "has_screen", return_value=True))
        self.start_patch(patch.object(renpy.exports, "roll_forward_info", return_value=None))
        self.start_patch(patch.object(renpy.exports, "in_fixed_rollback", return_value=False))
        self.start_patch(patch.object(renpy.exports, "in_rollback", return_value=False))
        self.start_patch(patch.object(renpy.exports, "log"))
        self.start_patch(patch.object(renpy.game, "context", return_value=SimpleNamespace(current="test")))
        self.start_patch(patch.object(renpy.config, "auto_choice_delay", None))
        self.start_patch(patch.object(renpy.config, "old_say_args", False))

    def test_say_layer_precedence_and_keyword_omission(self):
        for declared in ("dialogue", "screens"):
            for configured, explicit, expected in (
                (None, None, declared),
                ("configured", None, "configured"),
                (None, "explicit", "explicit"),
                ("configured", "explicit", "explicit"),
            ):
                with (
                    self.subTest(declared=declared, configured=configured, explicit=explicit),
                    patch.object(renpy.config, "say_layer", configured),
                    patch.object(screen, "get_screen_layer", return_value=declared),
                    patch.object(screen, "show_screen") as show,
                ):
                    result = character.show_display_say("Speaker", "Text", screen="say", layer=explicit)
                    self.assertEqual(result, ("say", "what", expected))
                    if configured is None and explicit is None:
                        self.assertNotIn("_layer", show.call_args.kwargs)
                    else:
                        self.assertEqual(show.call_args.kwargs["_layer"], expected)

    def test_retained_and_multiple_dialogue_resolve_screen_not_tag(self):
        for options, name, tag in (
            ({"retain": "retained"}, "say", "retained"),
            ({"multiple": (1, 2)}, "multiple_say", "block1_multiple2_say"),
        ):
            with (
                self.subTest(options=options),
                patch.object(renpy.config, "say_layer", None),
                patch.object(character, "compute_widget_properties", return_value={}),
                patch.object(screen, "get_screen_layer", return_value="dialogue") as get_layer,
                patch.object(screen, "show_screen") as show,
            ):
                result = character.show_display_say("Speaker", "Text", screen="say", **options)
                self.assertEqual(result, (tag, "what", "dialogue"))
                get_layer.assert_called_once_with(name)
                self.assertEqual(show.call_args.args, (name,))
                self.assertNotIn("_layer", show.call_args.kwargs)

    def test_menu_layer_precedence_and_keyword_omission(self):
        for menu_type, setting in (("menu", "choice_layer"), ("nvl", "nvl_choice_layer")):
            for configured, explicit, expected in (
                (None, None, None),
                ("configured", None, "configured"),
                (None, "explicit", "explicit"),
                ("configured", "explicit", "explicit"),
            ):
                with (
                    self.subTest(menu_type=menu_type, configured=configured, explicit=explicit),
                    patch.object(renpy.config, setting, configured),
                    patch.object(renpy.exports, "show_screen") as show,
                ):
                    menuexports.display_menu([], interact=False, type=menu_type, _layer=explicit, _args=(), _kwargs={})
                    if expected is None:
                        self.assertNotIn("_layer", show.call_args.kwargs)
                    else:
                        self.assertEqual(show.call_args.kwargs["_layer"], expected)

    def test_menu_argument_layer_override(self):
        with (
            patch.object(renpy.config, "choice_layer", "configured"),
            patch.object(renpy.exports, "show_screen") as show,
        ):
            menuexports.display_menu([], interact=False, _layer="explicit", _args=(), _kwargs={"_layer": "argument"})
            self.assertEqual(show.call_args.kwargs["_layer"], "argument")

    def test_screen_declared_layer_and_default(self):
        for definition, expected in (({}, "screens"), ({"layer": "dialogue"}, "dialogue")):
            with self.subTest(definition=definition), patch.dict(screen.screens), patch.dict(screen.screens_by_name):
                screen.Screen("_test_screen_layer", lambda **kwargs: None, **definition)
                self.assertEqual(screen.get_screen_layer("_test_screen_layer"), expected)

    def test_configuration_defaults_and_compatibility_boundary(self):
        settings = ("say_layer", "choice_layer", "nvl_choice_layer")
        for setting in settings:
            self.assertIsNone(getattr(renpy.config, setting))

        path = Path(renpy.config.renpy_base) / "renpy/common/00compat.rpy"
        source = path.read_text(encoding="utf-8-sig").split("init -1100 python:", 1)[1]
        source = source.split("\npython early ", 1)[0]
        module = ast.parse(dedent(source))
        functions = [node for node in module.body if isinstance(node, ast.FunctionDef)]
        namespace = {}
        exec(compile(ast.Module(body=functions, type_ignores=[]), str(path), "exec"), namespace)  # noqa: S102
        for version, expected in (((8, 5, 0), "screens"), ((8, 5, 99), "screens"), ((8, 6, 0), None), (None, None)):
            with self.subTest(version=version), patch.dict(os.environ):
                os.environ.pop("RENPY_EXPERIMENTAL", None)
                config = SimpleNamespace(**dict.fromkeys(settings))
                namespace["config"] = config
                namespace["_set_script_version"](version)
                for setting in settings:
                    self.assertEqual(getattr(config, setting), expected)
