import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

import renpy

if not hasattr(renpy, "warp"):
    renpy.import_all()

from renpy import ast, character, warp


class TestWarpReplay(unittest.TestCase):
    def setUp(self):
        self.ctx = SimpleNamespace(
            current="original",
            next_node=None,
            say_attributes=None,
            temporary_attributes=None,
            translate_identifier=None,
            alternate_translate_identifier=None,
            translated=False,
            deferred_translate_identifier=None,
            rollback=True,
        )
        self.store = SimpleNamespace(
            _last_say_who=None,
            _last_say_what="",
            _last_say_args=(),
            _last_say_kwargs={},
            _last_raw_what="",
            _side_image_attributes=None,
            _side_image_attributes_reset=False,
            _history=True,
            _history_list=[],
            bubble=SimpleNamespace(retain_layer="screens", statement_callback=Mock()),
        )
        self.start_patch(patch.object(renpy.game, "context", return_value=self.ctx))
        self.start_patch(patch.object(renpy, "store", self.store))
        self.start_patch(patch.object(renpy.exports, "get_showing_tags", return_value=[]))
        self.write_log = self.start_patch(patch.object(renpy.exports, "write_log"))
        self.log_exception = self.start_patch(patch.object(renpy.display.log, "exception"))
        self.start_patch(patch.object(renpy.config, "skipping", None))
        self.start_patch(patch.object(renpy.config, "say_menu_text_filter", None))
        self.start_patch(patch.object(renpy.config, "say_menu_text_filters", []))
        self.start_patch(patch.object(renpy.config, "statement_callbacks", []))
        self.start_patch(patch.object(renpy.config, "say_arguments_callback", None))
        self.start_patch(patch.object(renpy.config, "old_substitutions", False))
        self.start_patch(patch.object(warp, "warping", False))
        self.start_patch(patch.object(character, "multiple_count", 0))

    def start_patch(self, patcher):
        value = patcher.start()
        self.addCleanup(patcher.stop)
        return value

    def say(self, who, what="line", arguments=None):
        node = ast.Say(("game/warp.rpy", 1), "speaker", what, None, arguments=arguments)
        node.name = ("warp", what)
        node.next = None
        return node, who

    def run_says(self, pairs):
        lookup = {node.what: who for node, who in pairs}
        with patch.object(ast, "eval_who", side_effect=lambda *args: lookup[self.ctx.current[1]]):
            warp.reconstruct([node for node, _who in pairs])

    def test_opt_in_and_unsupported_callables(self):
        supported = Mock(warp=True, record_say=True, statement_name="say")
        unsupported = Mock(spec=["__call__"])
        self.run_says([self.say(unsupported, "skipped"), self.say(supported, "supported")])
        unsupported.assert_not_called()
        supported.assert_called_once_with("supported", interact=True)
        self.assertEqual(self.store._last_say_what, "supported")
        self.assertFalse(warp.warping)
        self.assertEqual(self.ctx.current, "original")
        self.assertIsNone(renpy.config.skipping)

    def test_say_attributes_are_not_applied_during_warp(self):
        who = Mock(warp=True, record_say=True, statement_name="say")
        node, _who = self.say(who)
        node.attributes = ("permanent",)
        node.temporary_attributes = ("temporary",)
        seen_attributes = []
        say = Mock(side_effect=lambda *args, **kwargs: seen_attributes.append(
            (self.ctx.say_attributes, self.ctx.temporary_attributes)
        ))

        with patch.object(renpy.exports, "say", say):
            self.run_says([(node, who)])

        self.assertEqual(seen_attributes, [(("permanent",), None)])

    def test_character_skips_temporary_and_speaking_attributes_during_warp(self):
        c = character.ADVCharacter.__new__(character.ADVCharacter)
        c.image_tag = "speaker"
        images = Mock()
        images.get_attributes.return_value = ("permanent",)
        self.ctx.images = images
        self.ctx.say_attributes = ("permanent",)
        self.ctx.temporary_attributes = ("temporary",)
        resolve = Mock(return_value=True)
        self.start_patch(patch.object(c, "resolve_say_attributes", resolve))
        self.start_patch(patch.object(c, "handle_say_transition"))

        with (
            patch.object(warp, "warping", True),
            patch.object(renpy.config, "speaking_attribute", "speaking"),
        ):
            state = c.handle_say_attributes(False, True)

        resolve.assert_called_once_with(False, ("permanent",))
        self.assertIsNone(state)
        self.assertIsNone(self.ctx.say_attributes)
        self.assertIsNone(self.ctx.temporary_attributes)

    def test_failed_callable_restores_bookkeeping_and_continues(self):
        def fail(*args, **kwargs):
            self.assertTrue(renpy.exports.is_warping())
            character.multiple_count = 9
            self.ctx.say_attributes = ("leaked",)
            renpy.config.skipping = None
            raise ValueError("missing runtime state")

        failing = Mock(warp=True, record_say=True, statement_name="say", side_effect=fail)
        valid = Mock(warp=True, record_say=True, statement_name="say")
        self.run_says([self.say(failing, "bad"), self.say(valid, "good")])
        valid.assert_called_once_with("good", interact=True)
        self.assertEqual(self.store._last_say_what, "good")
        self.assertEqual(character.multiple_count, 0)
        self.assertIsNone(self.ctx.say_attributes)
        self.write_log.assert_called_once()
        self.log_exception.assert_called_once()

    def test_failed_synthetic_node_uses_fallback_location(self):
        class SyntheticNode:
            name = "synthetic"
            next = None

            def can_warp(self):
                return True

            def execute(self):
                raise ValueError("synthetic failure")

        warp.replay_node(SyntheticNode())

        self.write_log.assert_called_once_with(
            "While warping, ignoring statement at %s:%s:",
            "<unknown>",
            0,
        )
        self.log_exception.assert_called_once()

    def test_failed_resolution_is_skipped(self):
        valid = Mock(warp=True, record_say=True, statement_name="say")
        pairs = [self.say(None, "bad"), self.say(valid, "good")]
        with patch.object(ast, "eval_who", side_effect=[ValueError("undefined"), valid]):
            warp.reconstruct([node for node, _who in pairs])
        valid.assert_called_once()
        self.log_exception.assert_called_once()

    def test_failed_eligibility_is_skipped(self):
        class Broken:
            @property
            def warp(self):
                raise ValueError("eligibility")

        valid = Mock(warp=True, record_say=True, statement_name="say")
        self.run_says([self.say(Broken(), "bad"), self.say(valid, "good")])
        valid.assert_called_once()
        self.log_exception.assert_called_once()

    def test_failed_arguments_are_skipped(self):
        valid = Mock(warp=True, record_say=True, statement_name="say")
        arguments = Mock()
        arguments.evaluate.side_effect = ValueError("arguments")
        self.run_says([self.say(valid, "bad", arguments), self.say(valid, "good")])
        valid.assert_called_once_with("good", interact=True)
        self.log_exception.assert_called_once()

    def test_control_exception_propagates_and_restores_flag(self):
        failing = Mock(warp=True, record_say=True, statement_name="say")
        failing.side_effect = KeyboardInterrupt
        with self.assertRaises(KeyboardInterrupt):
            self.run_says([self.say(failing)])
        self.assertFalse(warp.warping)
        self.assertIsNone(renpy.config.skipping)
        self.assertEqual(self.ctx.current, "original")
        self.log_exception.assert_not_called()

    def test_display_during_warp_only_creates_retained_screen(self):
        show = Mock()
        kwargs = {
            "interact": True,
            "slow": True,
            "afm": True,
            "ctc": None,
            "ctc_pause": None,
            "ctc_position": "nestled",
            "all_at_once": False,
            "cb_args": {},
            "with_none": True,
            "callback": Mock(),
            "type": "adv",
        }
        with patch.object(warp, "warping", True):
            character.display_say("Name", "text", show, **kwargs)
            show.assert_not_called()
            with patch.object(renpy.exports, "get_screen", side_effect=[object(), None]):
                character.display_say("Name", "text{w}more", show, retain=True, **kwargs)
        show.assert_called_once_with("Name", "text{w}more", multiple=None, retain="_retain_1")
        kwargs["callback"].assert_not_called()

    def test_reconstructed_history_has_no_rollback_identifier(self):
        c = character.ADVCharacter.__new__(character.ADVCharacter)
        c.who_args = c.what_args = c.window_args = c.show_args = {}
        c.image_tag = None
        with (
            patch.object(warp, "warping", True),
            patch.object(renpy.config, "history_length", 1),
            patch.object(renpy.config, "history_callbacks", []),
        ):
            c.do_done("Name", "one")
            c.do_done("Name", "two")
        self.assertEqual([h.what for h in self.store._history_list], ["two"])
        self.assertIsNone(self.store._history_list[0].rollback_identifier)

    def test_narrator_and_string_adapter_eligibility(self):
        self.store.narrator = SimpleNamespace(warp=True)
        self.store.say = SimpleNamespace(warp=False)
        self.assertTrue(renpy.exports.can_warp_say(None))
        self.assertFalse(renpy.exports.can_warp_say("Name"))
        self.store.say.warp = True
        self.assertTrue(renpy.exports.can_warp_say("Name"))

    def test_skipped_menu_only_applies_bubble_clearing(self):
        menu = ast.Menu(("game/warp.rpy", 1), [], None, None, False, None, [])
        menu.name = "menu"
        menu.next = None
        with (
            patch.object(ast.Menu, "execute") as execute,
            patch.object(renpy.config, "statement_callbacks", [self.store.bubble.statement_callback]),
        ):
            warp.reconstruct([menu])
        execute.assert_not_called()
        self.store.bubble.statement_callback.assert_called_once_with("menu")

    def translation_fixture(self, default, translated):
        translator = renpy.translation.ScriptTranslator()
        translator.default_translates["warp_test"] = default
        translator.language_translates[("warp_test", "warp")] = translated
        self.start_patch(patch.object(renpy.game, "script", SimpleNamespace(translator=translator)))
        self.start_patch(patch.object(renpy.game, "preferences", SimpleNamespace(language="warp")))
        persistent = SimpleNamespace(_seen_translates=set())
        self.start_patch(patch.object(renpy.game, "persistent", persistent))
        return persistent

    def test_optimized_translation_uses_selected_text_without_marking_seen(self):
        source = ast.TranslateSay(
            ("game/warp.rpy", 1),
            "speaker",
            "source",
            None,
            identifier="warp_test",
        )
        translated = ast.TranslateSay(
            ("game/tl/warp.rpy", 1),
            "speaker",
            "translated",
            None,
            identifier="warp_test",
            language="warp",
        )
        source.name = "source"
        translated.name = "translated"
        persistent = self.translation_fixture(source, translated)
        who = Mock(warp=True, record_say=True, statement_name="say")
        who.side_effect = lambda *args, **kwargs: self.assertEqual(self.ctx.translate_identifier, "warp_test")
        with patch.object(ast, "eval_who", return_value=who):
            warp.reconstruct([source])
        who.assert_called_once_with("translated", interact=True)
        self.assertEqual(persistent._seen_translates, set())
        self.assertIsNone(self.ctx.translate_identifier)

    def test_translation_block_skips_failed_say_and_replays_next(self):
        original, _ = self.say(None, "original")
        failed, _ = self.say(None, "bad")
        valid, _ = self.say(None, "good")
        end = ast.EndTranslate(("game/warp.rpy", 4))
        end.name = "end"
        source = ast.Translate(("game/warp.rpy", 1), "warp_test", None, [original])
        translated = ast.Translate(("game/tl/warp.rpy", 1), "warp_test", "warp", [failed, valid])
        source.name = "source"
        translated.name = "translated"
        source.chain(end)
        translated.chain(end)
        persistent = self.translation_fixture(source, translated)

        def speak(what, **kwargs):
            if what == "bad":
                raise ValueError("failed translated say")

        who = Mock(warp=True, record_say=True, statement_name="say", side_effect=speak)
        with patch.object(ast, "eval_who", return_value=who):
            warp.reconstruct([source, original, end])
        self.assertEqual([call.args[0] for call in who.call_args_list], ["bad", "good"])
        self.assertEqual(self.store._last_say_what, "good")
        self.assertEqual(persistent._seen_translates, set())
        self.log_exception.assert_called_once()

    def test_failed_say_removes_new_retained_screen(self):
        who = Mock(warp=True, record_say=True, statement_name="say", side_effect=ValueError("completion"))
        with (
            patch.object(
                renpy.exports, "get_showing_tags", side_effect=[["_retain_old"], ["_retain_old", "_retain_0"]]
            ),
            patch.object(renpy.exports, "hide_screen") as hide,
        ):
            self.run_says([self.say(who)])
        hide.assert_called_once_with("_retain_0", layer="screens", immediately=True)

    def test_partial_translation_block_does_not_replay_target(self):
        first, _ = self.say(None, "first")
        target, _ = self.say(None, "target")
        translated, _ = self.say(None, "translated")
        end = ast.EndTranslate(("game/warp.rpy", 4))
        end.name = "end"
        source = ast.Translate(("game/warp.rpy", 1), "warp_test", None, [first, target])
        selected = ast.Translate(("game/tl/warp.rpy", 1), "warp_test", "warp", [translated])
        source.name = "source"
        selected.name = "selected"
        source.chain(end)
        selected.chain(end)
        self.translation_fixture(source, selected)
        who = Mock(warp=True, record_say=True, statement_name="say")
        with patch.object(ast, "eval_who", return_value=who):
            warp.reconstruct([source, first])
        who.assert_called_once_with("first", interact=True)

    def test_disabled_history_stays_empty(self):
        c = character.ADVCharacter.__new__(character.ADVCharacter)
        with patch.object(renpy.config, "history_length", None):
            c.do_done("Name", "line")
        self.store._history = False
        with patch.object(renpy.config, "history_length", 10):
            c.do_done("Name", "line")
        self.assertEqual(self.store._history_list, [])

    def test_clearing_retained_screens_uses_the_requested_layer(self):
        with (
            patch.object(renpy.exports.displayexports, "get_showing_tags", return_value=["_retain_0", "other"]),
            patch.object(renpy.exports, "hide_screen") as hide,
        ):
            renpy.exports.clear_retain(layer="bubbles")
        hide.assert_called_once_with("_retain_0", layer="bubbles")
