## This file tests warping (renpy.warp.warp), which reconstructs the dialogue state that leads up to a statement.
##
## Each scenario is a label that ends with a label for a target statement, `$ warp_test_snapshot()`. The testcase
## warps to that statement as `--warp` does, so renpy.warp.warp reconstructs the history, NVL page, and retained
## bubbles of the statements before it, and then the snapshot records them for the testcase to check. The result
## is kept in renpy.session, as returning to the main menu resets the store.

# ==============
# == Fixtures ==
# ==============

define warp_test_adv = Character("Warp")
define warp_test_nvl = Character("Warp", kind=nvl)
define warp_test_nvl_clear = Character("Warp", kind=nvl, clear=True)
define warp_test_bubble = Character(None, kind=bubble, image="warp", retain=True,
    screen="_warp_test_bubble", _open_db=False)
define warp_test_unretained = Character(None, kind=warp_test_bubble, retain=False, _open_db=False)
define warp_test_disabled = Character("Disabled", warp=False)

screen _warp_test_bubble(who, what, **kwargs):
    text what id "what"

default warp_test_target = None

init python:

    def warp_test_no_interaction(*args, **kwargs):
        raise AssertionError("Warp ran an interaction callback.")

    def warp_test_callable(what, **kwargs):
        assert renpy.is_warping()
        if what == "fail":
            raise ValueError("Intentional warp failure.")
        warp_test_adv(what, **kwargs)

    warp_test_callable.warp = True

    def warp_test_unsupported(what, **kwargs):
        raise AssertionError("Warp called an unsupported sayer.")

    CONFIG_NAMES = (
        "history_length", "nvl_list_length", "all_character_callbacks", "voice_tag_callback", "history_callbacks",
        "statement_callbacks")

    BUBBLE_NAMES = ("db", "properties", "properties_order", "tag_properties", "current_dialogue")

    def warp_test_begin():
        """
        Saves the state that the warp scenarios replace, and installs callbacks that fail if warping runs
        anything that waits for the player.
        """

        _test.warp_saved = (
            {name: getattr(config, name) for name in CONFIG_NAMES},
            {name: getattr(bubble, name) for name in BUBBLE_NAMES},
            store._history_list,
            store._history,
            store.nvl_list,
        )

        config.all_character_callbacks = [warp_test_no_interaction]
        config.voice_tag_callback = warp_test_no_interaction
        config.history_callbacks = []
        config.statement_callbacks = [bubble.statement_callback]

    def warp_test_end():
        """
        Restores what warp_test_begin saved.
        """

        saved_config, saved_bubble, history_list, history, nvl = _test.warp_saved
        del _test.warp_saved

        renpy.clear_retain(layer=bubble.retain_layer)
        store._history_list = history_list
        store._history = history
        store.nvl_list = nvl

        for name, value in saved_config.items():
            setattr(config, name, value)

        for name, value in saved_bubble.items():
            setattr(bubble, name, value)

    def warp_test_prepare(label, history_length=100, nvl_length=None, clear_text=None):
        """
        Starts a scenario with empty history, an empty NVL page, no retained bubbles, and a bubble database that
        has the "warp" image and no entries. `label` is the target statement's label. If `clear_text` is given,
        the bubble for the dialogue with that text is marked as clearing the retained bubbles.
        """

        import collections

        config.history_length = history_length
        config.nvl_list_length = nvl_length
        store._history_list = []
        store._history = True
        nvl_clear()
        bubble.db = collections.defaultdict(dict)
        bubble.properties = {"warp": {}}
        bubble.properties_order = ["warp"]
        bubble.tag_properties = {}
        bubble.current_dialogue = []
        renpy.clear_retain(layer=bubble.retain_layer)

        if clear_text is not None:
            for node in renpy.game.script.namemap.values():
                if isinstance(node, renpy.ast.TranslateSay) and node.what == clear_text:
                    bubble.db[node.identifier]["clear_retain"] = True

        store.warp_test_target = label
        renpy.session.pop("warp_test_result", None)
        _test.warp_seen = set(renpy.game.persistent._seen_translates)

    def warp_test_perform():
        """
        Warps to the statement after the label in warp_test_target, as the --warp argument does. This
        restarts the context there, so it doesn't return.
        """

        node = renpy.game.script.lookup(warp_test_target).next
        renpy.warp.warp_spec = "{}:{}".format(node.filename, node.linenumber)
        renpy.warp.warp()

    def warp_test_snapshot():
        """
        Records the history, the NVL page, the text of the retained bubbles, and the bubble editor's
        dialogue in renpy.session["warp_test_result"]. This also checks that the reconstructed state can be saved, which
        pickles the history, the page, and the retained screens, and that warping left nothing behind in
        the history that refers to a rollback, nor marked a translation as seen.
        """

        from renpy.compat import pickle as warp_pickle

        history = [h.what for h in _history_list]
        page = [entry[1] for entry in nvl_list]
        tags = [tag for tag in renpy.get_showing_tags(bubble.retain_layer, sort=True) if tag.startswith("_retain_")]
        retained = [renpy.get_screen(tag, layer=bubble.retain_layer) for tag in tags]
        texts = [screen.scope["_kwargs"]["what"] for screen in retained]

        roundtrip = warp_pickle.loads(warp_pickle.dumps((_history_list, nvl_list, retained)))
        assert [h.what for h in roundtrip[0]] == history
        assert [entry[1] for entry in roundtrip[1]] == page
        assert [screen.scope["_kwargs"]["what"] for screen in roundtrip[2]] == texts
        assert all(h.rollback_identifier is None for h in _history_list)
        assert not renpy.is_warping()
        assert set(renpy.game.persistent._seen_translates) == _test.warp_seen

        renpy.session["warp_test_result"] = {
            "history": history,
            "page": page,
            "bubbles": texts,
            "editor": list(bubble.current_dialogue),
        }

label warp_test_run:
    $ warp_test_perform()

# NVL.

label warp_test_nvl_three:
    warp_test_nvl "one"
    warp_test_nvl "two"
    warp_test_nvl "three"
label warp_test_nvl_three_target:
    $ warp_test_snapshot()
    return

label warp_test_nvl_page:
    warp_test_nvl "one"
    warp_test_nvl "two"
    warp_test_nvl "three"
    nvl clear
    warp_test_nvl "four"
    warp_test_nvl "five"
label warp_test_nvl_page_target:
    $ warp_test_snapshot()
    return

label warp_test_nvl_character_clear:
    warp_test_nvl "one"
    warp_test_nvl_clear "two"
    warp_test_nvl "three"
label warp_test_nvl_character_clear_target:
    $ warp_test_snapshot()
    return

label warp_test_multiple:
    warp_test_nvl "multi one" (multiple=2)
    warp_test_nvl "multi two" (multiple=2)
label warp_test_multiple_target:
    $ warp_test_snapshot()
    return

# ADV.

label warp_test_adv_lines:
    warp_test_adv "one"
    extend " two"
    warp_test_disabled "disabled"
    warp_test_unsupported "unsupported"
    warp_test_callable "fail"
    warp_test_adv "[warp_test_undefined_variable]"
    warp_test_callable "good"
label warp_test_adv_lines_target:
    $ warp_test_snapshot()
    return

label warp_test_overrides:
    warp_test_adv "hidden" (condition="False")
    warp_test_adv "disabled" (warp=False)
    warp_test_adv "override" (what_prefix="(", what_suffix=")")
    warp_test_adv "no wait{nw}"
    warp_test_adv "paused{w} text"
label warp_test_overrides_target:
    $ warp_test_snapshot()
    return

# Bubbles.

label warp_test_bubble_lines:
    warp_test_bubble "one"
    warp_test_bubble "two"
label warp_test_bubble_lines_target:
    $ warp_test_snapshot()
    return

label warp_test_bubble_cleared:
    warp_test_bubble "one"
    menu:
        "Skipped choice":
            pass
    warp_test_bubble "two"
label warp_test_bubble_cleared_target:
    $ warp_test_snapshot()
    return

label warp_test_bubble_adv_clear:
    warp_test_bubble "one"
    warp_test_adv "clear"
    warp_test_bubble "two"
label warp_test_bubble_adv_clear_target:
    $ warp_test_snapshot()
    return

label warp_test_bubble_unretained:
    warp_test_unretained "one"
label warp_test_bubble_unretained_target:
    $ warp_test_snapshot()
    return

label warp_test_bubble_screen_clear:
    warp_test_bubble "one"
    call screen _warp_test_bubble(None, "must not be shown")
    warp_test_bubble "two"
label warp_test_bubble_screen_clear_target:
    $ warp_test_snapshot()
    return

label warp_test_bubble_scene_clear:
    warp_test_bubble "one"
    scene
    warp_test_bubble "two"
label warp_test_bubble_scene_clear_target:
    $ warp_test_snapshot()
    return


# ==============
# === Tests ====
# ==============

testcase warp_property:
    description "A character warps by default if it can, and the warp property overrides that."

    assert eval not Character(kind=warp_test_disabled).warp
    assert eval Character(kind=warp_test_disabled, warp=True).warp

testsuite warp_dialogue:
    description "Warping reconstructs the history and NVL page from say statements, skipping what can't be warped."

    setup:
        $ warp_test_begin()

    teardown:
        $ warp_test_end()

    after testcase:
        if not screen "main_menu":
            run MainMenu(confirm=False, save=False)

    testcase scenario:
        parameter (target, history_length, nvl_length, expected_history, expected_page) = [
            ("warp_test_nvl_three_target", 100, None, ["one", "two", "three"], ["one", "two", "three"]),
            ("warp_test_nvl_page_target", 100, None, ["one", "two", "three", "four", "five"], ["four", "five"]),
            ("warp_test_nvl_character_clear_target", 100, None, ["one", "two", "three"], ["three"]),
            ("warp_test_nvl_page_target", 2, 1, ["four", "five"], ["five"]),
            ("warp_test_adv_lines_target", 100, None, ["one{fast} two", "good"], []),
            ("warp_test_multiple_target", 100, None, ["multi one", "multi two"], ["multi one", "multi two"]),
            ("warp_test_overrides_target", 100, None, ["(override)", "no wait{nw}", "paused{w} text"], []),
        ]

        $ warp_test_prepare(target, history_length, nvl_length)
        run Start("warp_test_run")
        advance until screen "main_menu"

        assert eval (renpy.session["warp_test_result"]["history"] == expected_history)
        assert eval (renpy.session["warp_test_result"]["page"] == expected_page)

testsuite warp_bubbles:
    description "Warping reconstructs retained bubbles, which clear where they would have been cleared."

    setup:
        $ warp_test_begin()

    teardown:
        $ warp_test_end()

    after testcase:
        if not screen "main_menu":
            run MainMenu(confirm=False, save=False)

    testcase scenario:
        parameter (target, clear_text, expected_history, expected_bubbles) = [
            ("warp_test_bubble_lines_target", None, ["one", "two"], ["one", "two"]),
            ("warp_test_bubble_lines_target", "two", ["one", "two"], ["two"]),
            ("warp_test_bubble_cleared_target", None, ["one", "two"], ["two"]),
            ("warp_test_bubble_screen_clear_target", None, ["one", "two"], ["two"]),
            ("warp_test_bubble_scene_clear_target", None, ["one", "two"], ["two"]),
            ("warp_test_bubble_adv_clear_target", None, ["one", "clear", "two"], ["two"]),
            ("warp_test_bubble_unretained_target", None, ["one"], []),
        ]

        $ warp_test_prepare(target, clear_text=clear_text)
        run Start("warp_test_run")
        advance until screen "main_menu"

        assert eval (renpy.session["warp_test_result"]["history"] == expected_history)
        assert eval (renpy.session["warp_test_result"]["bubbles"] == expected_bubbles)
        assert eval (renpy.session["warp_test_result"]["editor"] == [])
