"""
Tests for warp, the mechanism that fast-forwards through already-seen statements to reach a saved
position. Reconstruction replays only the nodes that opt in, and it restores the context, config, and
store state it changes even when a replayed statement fails.
"""

from types import SimpleNamespace

import pytest

import renpy
from renpy import ast, character, warp

################################################################################
# Fixtures and helpers
################################################################################


@pytest.fixture
def warp_context(mocker):
    """
    Provides the script context that warp reconstruction reads and writes, with ``rollback`` enabled.
    """

    return SimpleNamespace(
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


@pytest.fixture
def warp_store(mocker):
    """
    Provides the store fields that say and history code touch during warp, plus a ``bubble`` whose
    statement callback is a mock.
    """

    return SimpleNamespace(
        _last_say_who=None,
        _last_say_what="",
        _last_say_args=(),
        _last_say_kwargs={},
        _last_raw_what="",
        _side_image_attributes=None,
        _side_image_attributes_reset=False,
        _history=True,
        _history_list=[],
        bubble=SimpleNamespace(retain_layer="screens", statement_callback=mocker.Mock()),
    )


@pytest.fixture
def write_log(mocker):
    """
    Mocks ``renpy.exports.write_log``, which warp uses to report a skipped statement.
    """

    return mocker.patch.object(renpy.exports, "write_log")


@pytest.fixture
def log_exception(mocker):
    """
    Mocks ``renpy.display.log.exception``, which warp uses to log the traceback of a skipped statement.
    """

    return mocker.patch.object(renpy.display.log, "exception")


@pytest.fixture(autouse=True)
def warp_environment(mocker, warp_context, warp_store, write_log, log_exception):
    """
    Points the engine globals that warp reads at the fixtures above, and resets config and warp flags to
    their defaults, for every test in this module.
    """

    mocker.patch.object(renpy.game, "context", return_value=warp_context)
    mocker.patch.object(renpy, "store", warp_store)
    mocker.patch.object(renpy.exports, "get_showing_tags", return_value=[])
    mocker.patch.object(renpy.config, "skipping", None)
    mocker.patch.object(renpy.config, "say_menu_text_filter", None)
    mocker.patch.object(renpy.config, "say_menu_text_filters", [])
    mocker.patch.object(renpy.config, "statement_callbacks", [])
    mocker.patch.object(renpy.config, "say_arguments_callback", None)
    mocker.patch.object(renpy.config, "old_substitutions", False)
    mocker.patch.object(warp, "warping", False)
    mocker.patch.object(character, "multiple_count", 0)


def make_say(who, what="line", arguments=None):
    """
    Builds a Say node that speaks ``what``, returning it with ``who`` so that callers can pass both to
    run_says.
    """

    node = ast.Say(("game/warp.rpy", 1), "speaker", what, None, arguments=arguments)
    node.name = ("warp", what)
    node.next = None
    return node, who


def run_says(mocker, warp_context, pairs):
    """
    Reconstructs the Say nodes in ``pairs``. Each node's speaker is resolved by ``ast.eval_who`` from the
    node's text, so a node's ``who`` is the callable replayed for it. A ``who`` that is an exception instance
    is raised while the speaker is resolved, as an undefined speaker would be.
    """

    lookup = {node.what: who for node, who in pairs}

    def resolve(*args):
        who = lookup[warp_context.current[1]]

        if isinstance(who, Exception):
            raise who

        return who

    eval_who = mocker.patch.object(ast, "eval_who", side_effect=resolve)
    warp.reconstruct([node for node, _who in pairs])
    mocker.stop(eval_who)


def install_translation(mocker, default, translated):
    """
    Installs a script translator in which ``translated`` replaces ``default`` for the language "warp", and
    returns the persistent object so that a test can check the seen-translate bookkeeping.
    """

    translator = renpy.translation.ScriptTranslator()
    translator.default_translates["warp_test"] = default
    translator.language_translates[("warp_test", "warp")] = translated
    mocker.patch.object(renpy.game, "script", SimpleNamespace(translator=translator))
    mocker.patch.object(renpy.game, "preferences", SimpleNamespace(language="warp"))
    persistent = SimpleNamespace(_seen_translates=set())
    mocker.patch.object(renpy.game, "persistent", persistent)
    return persistent


################################################################################
# Replaying statements
################################################################################


def test_opt_in_and_unsupported_callables(mocker, warp_context, warp_store):
    """
    Only callables that opt in with ``warp=True`` are replayed. Warping ends with the context, ``config.skipping``,
    and ``warp.warping`` restored.
    """

    supported = mocker.Mock(warp=True, record_say=True, statement_name="say")
    unsupported = mocker.Mock(spec=["__call__"])
    run_says(mocker, warp_context, [make_say(unsupported, "skipped"), make_say(supported, "supported")])
    unsupported.assert_not_called()
    supported.assert_called_once_with("supported", interact=True)
    assert warp_store._last_say_what == "supported"
    assert not warp.warping
    assert warp_context.current == "original"
    assert renpy.config.skipping is None


def test_say_attributes_are_not_applied_during_warp(mocker, warp_context):
    """
    Permanent and temporary say attributes are cleared while a say is replayed, so the attributes recorded in
    the context at the time of the say are the node's permanent attributes only.
    """

    who = mocker.Mock(warp=True, record_say=True, statement_name="say")
    node, _who = make_say(who)
    node.attributes = ("permanent",)
    node.temporary_attributes = ("temporary",)
    seen_attributes = []
    say = mocker.Mock(
        side_effect=lambda *args, **kwargs: seen_attributes.append((
            warp_context.say_attributes,
            warp_context.temporary_attributes,
        ))
    )

    say_patch = mocker.patch.object(renpy.exports, "say", say)
    run_says(mocker, warp_context, [(node, who)])
    mocker.stop(say_patch)

    assert seen_attributes == [(("permanent",), None)]


def test_failed_callable_restores_bookkeeping_and_continues(mocker, warp_context, warp_store, write_log, log_exception):
    """
    When a replayed say raises, warp logs it, undoes the state the failed say changed (the multiple count, the
    say attributes, and the skipping flag), and goes on to replay the next node.
    """

    def fail(*args, **kwargs):
        assert renpy.exports.is_warping()
        character.multiple_count = 9
        warp_context.say_attributes = ("leaked",)
        renpy.config.skipping = None
        raise ValueError("missing runtime state")

    failing = mocker.Mock(warp=True, record_say=True, statement_name="say", side_effect=fail)
    valid = mocker.Mock(warp=True, record_say=True, statement_name="say")
    run_says(mocker, warp_context, [make_say(failing, "bad"), make_say(valid, "good")])
    valid.assert_called_once_with("good", interact=True)
    assert warp_store._last_say_what == "good"
    assert character.multiple_count == 0
    assert warp_context.say_attributes is None
    write_log.assert_called_once()
    log_exception.assert_called_once()


def test_control_exception_propagates_and_restores_flag(mocker, warp_context, log_exception):
    """
    A control-flow exception such as KeyboardInterrupt is not swallowed or logged. It propagates, while warp
    still clears its flag and the context and config are restored.
    """

    failing = mocker.Mock(warp=True, record_say=True, statement_name="say")
    failing.side_effect = KeyboardInterrupt
    with pytest.raises(KeyboardInterrupt):
        run_says(mocker, warp_context, [make_say(failing)])
    assert not warp.warping
    assert renpy.config.skipping is None
    assert warp_context.current == "original"
    log_exception.assert_not_called()


def test_failed_say_removes_new_retained_screen(mocker, warp_context):
    """
    When a say fails after it creates a retained screen, warp hides that new screen. Screens that were already
    showing are left alone.
    """

    who = mocker.Mock(warp=True, record_say=True, statement_name="say", side_effect=ValueError("completion"))
    tags = mocker.patch.object(
        renpy.exports, "get_showing_tags", side_effect=[["_retain_old"], ["_retain_old", "_retain_0"]]
    )
    hide = mocker.patch.object(renpy.exports, "hide_screen")
    run_says(mocker, warp_context, [make_say(who)])
    mocker.stop(tags)
    mocker.stop(hide)

    hide.assert_called_once_with("_retain_0", layer="screens", immediately=True)


class BrokenEligibility:
    """
    A speaker whose ``warp`` attribute raises when warp checks whether it can be replayed.
    """

    @property
    def warp(self) -> bool:
        raise ValueError("eligibility")


@pytest.mark.parametrize("failure", ["resolution", "eligibility", "arguments"])
def test_failed_say_preparation_is_skipped(mocker, warp_context, log_exception, failure):
    """
    A say that fails before it is replayed is skipped and logged, and the next say is still replayed. The
    failure can come from resolving the speaker, from checking whether it can warp, or from evaluating
    the say's arguments.
    """

    valid = mocker.Mock(warp=True, record_say=True, statement_name="say")
    arguments = None
    speaker = valid

    if failure == "resolution":
        speaker = ValueError("undefined")
    elif failure == "eligibility":
        speaker = BrokenEligibility()
    else:
        arguments = mocker.Mock()
        arguments.evaluate.side_effect = ValueError("arguments")

    run_says(mocker, warp_context, [make_say(speaker, "bad", arguments), make_say(valid, "good")])

    valid.assert_called_once_with("good", interact=True)
    log_exception.assert_called_once()


def test_narrator_and_string_adapter_eligibility(warp_store):
    """
    A missing speaker is warp-eligible only through the narrator, and a string speaker is eligible when the
    named ``say`` object has ``warp`` set.
    """

    warp_store.narrator = SimpleNamespace(warp=True)
    warp_store.say = SimpleNamespace(warp=False)
    assert renpy.exports.can_warp_say(None)
    assert not renpy.exports.can_warp_say("Name")
    warp_store.say.warp = True
    assert renpy.exports.can_warp_say("Name")


def test_skipped_menu_only_applies_bubble_clearing(mocker, warp_store):
    """
    A menu that is skipped during warp does not execute. It only runs the bubble statement callback, which
    clears the bubble.
    """

    menu = ast.Menu(("game/warp.rpy", 1), [], None, None, False, None, [])
    menu.name = "menu"
    menu.next = None
    execute_patch = mocker.patch.object(ast.Menu, "execute")
    callbacks_patch = mocker.patch.object(renpy.config, "statement_callbacks", [warp_store.bubble.statement_callback])
    warp.reconstruct([menu])
    mocker.stop(callbacks_patch)
    mocker.stop(execute_patch)

    execute_patch.assert_not_called()
    warp_store.bubble.statement_callback.assert_called_once_with("menu")


################################################################################
# Translation blocks
################################################################################


def test_optimized_translation_uses_selected_text_without_marking_seen(mocker, warp_context):
    """
    When a translation is selected, warp replays the translated text under the source's translate identifier
    and does not mark the translation as seen. The replayed callable records the identifier it observes,
    because an assertion inside a replayed callable would be swallowed by replay_node.
    """

    source = ast.TranslateSay(("game/warp.rpy", 1), "speaker", "source", None, identifier="warp_test")
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
    persistent = install_translation(mocker, source, translated)
    seen_identifiers = []
    who = mocker.Mock(warp=True, record_say=True, statement_name="say")
    who.side_effect = lambda *args, **kwargs: seen_identifiers.append(warp_context.translate_identifier)
    eval_who = mocker.patch.object(ast, "eval_who", return_value=who)
    warp.reconstruct([source])
    mocker.stop(eval_who)

    who.assert_called_once_with("translated", interact=True)
    assert seen_identifiers == ["warp_test"]
    assert persistent._seen_translates == set()
    assert warp_context.translate_identifier is None


def test_translation_block_skips_failed_say_and_replays_next(mocker, warp_store, log_exception):
    """
    In a translate block, a translated say that raises is logged and skipped, and the following say is
    still replayed. Neither say marks a translation as seen.
    """

    original, _ = make_say(None, "original")
    failed, _ = make_say(None, "bad")
    valid, _ = make_say(None, "good")
    end = ast.EndTranslate(("game/warp.rpy", 4))
    end.name = "end"
    source = ast.Translate(("game/warp.rpy", 1), "warp_test", None, [original])
    translated = ast.Translate(("game/tl/warp.rpy", 1), "warp_test", "warp", [failed, valid])
    source.name = "source"
    translated.name = "translated"
    source.chain(end)
    translated.chain(end)
    persistent = install_translation(mocker, source, translated)

    def speak(what, **kwargs):
        if what == "bad":
            raise ValueError("failed translated say")

    who = mocker.Mock(warp=True, record_say=True, statement_name="say", side_effect=speak)
    eval_who = mocker.patch.object(ast, "eval_who", return_value=who)
    warp.reconstruct([source, original, end])
    mocker.stop(eval_who)

    assert [call.args[0] for call in who.call_args_list] == ["bad", "good"]
    assert warp_store._last_say_what == "good"
    assert persistent._seen_translates == set()
    log_exception.assert_called_once()


def test_partial_translation_block_does_not_replay_target(mocker, warp_context):
    """
    When the selected translation block has fewer lines than the source block, warp replays only the lines
    before the target, and does not replay the target itself.
    """

    first, _ = make_say(None, "first")
    target, _ = make_say(None, "target")
    translated, _ = make_say(None, "translated")
    end = ast.EndTranslate(("game/warp.rpy", 4))
    end.name = "end"
    source = ast.Translate(("game/warp.rpy", 1), "warp_test", None, [first, target])
    selected = ast.Translate(("game/tl/warp.rpy", 1), "warp_test", "warp", [translated])
    source.name = "source"
    selected.name = "selected"
    source.chain(end)
    selected.chain(end)
    install_translation(mocker, source, selected)
    who = mocker.Mock(warp=True, record_say=True, statement_name="say")
    eval_who = mocker.patch.object(ast, "eval_who", return_value=who)
    warp.reconstruct([source, first])
    mocker.stop(eval_who)

    who.assert_called_once_with("first", interact=True)


################################################################################
# Finding the statement to warp to
################################################################################


def test_warp_lands_on_first_statement_of_line(mocker, warp_context):
    """
    Warping to a translatable user statement (like ``nvl clear``) lands on the Translate that starts its line. That
    Translate wraps the statement and the say on the next line, and is followed by an EndTranslate that has the
    Translate's line number but continues after the say, so landing on the EndTranslate would skip a line (#7487).

    The namemap is given in source order, so the old sort by line number, which was stable, always chose the
    EndTranslate here; in a real game the nodes were iterated in hash order, which made the failure intermittent.
    """

    def named(node, name):
        node.name = ("warp_target", name)
        return node

    clear = named(ast.Pass(("game/warp.rpy", 5)), "clear")
    after = named(ast.Say(("game/warp.rpy", 6), "n", "after", None), "after")
    translate = named(ast.Translate(("game/warp.rpy", 5), "warp_target", None, [clear, after]), "translate")
    end = named(ast.EndTranslate(("game/warp.rpy", 5)), "end_translate")
    too_far = named(ast.Say(("game/warp.rpy", 7), "n", "too far", None), "too_far")

    translate.chain(end)
    end.chain(too_far)
    too_far.next = None

    nodes = [translate, clear, after, end, too_far]
    mocker.patch.object(renpy.game, "script", SimpleNamespace(namemap={node: node for node in nodes}))
    mocker.patch.object(renpy.config, "developer", True)
    mocker.patch.object(renpy.game, "after_rollback", False)
    mocker.patch.object(renpy.exports, "block_rollback")
    mocker.patch.object(warp, "reconstruct")
    mocker.patch.object(warp, "warp_spec", "warp.rpy:5")
    warp_context.goto_label = mocker.Mock()
    warp_context.come_from = mocker.Mock()

    with pytest.raises(renpy.execution.RestartContext):
        warp.warp()

    warp_context.goto_label.assert_called_once_with(translate.name)
