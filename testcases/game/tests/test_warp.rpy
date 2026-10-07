define warp_test_adv = Character("Warp")
define warp_test_nvl = Character("Warp", kind=nvl)
define warp_test_nvl_clear = Character("Warp", kind=nvl, clear=True)
define warp_test_bubble = Character(None, kind=bubble, image="warp", retain=True,
    screen="_warp_test_bubble", _open_db=False)
define warp_test_unretained = Character(None, kind=warp_test_bubble, retain=False, _open_db=False)
define warp_test_disabled = Character("Disabled", warp=False)

screen _warp_test_bubble(who, what, **kwargs):
    text what id "what"

init python:
    if renpy.os.environ.get("RENPY_WARP_TEST"):
        config.history_length = 100

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

    def warp_test_replay(label, stop=None, history_length=100, nvl_length=None, clear_text=None):
        import collections
        from renpy.compat import pickle as warp_pickle

        ctx = renpy.game.context()
        node = renpy.game.script.lookup(label)
        stop_node = renpy.game.script.lookup(stop) if stop else None
        nodes = []
        while node is not None and not isinstance(node, renpy.ast.Return) and node is not stop_node:
            nodes.append(node)
            node = node.next

        saved_config = {
            name: getattr(config, name)
            for name in ("history_length", "nvl_list_length", "all_character_callbacks",
                "voice_tag_callback", "history_callbacks", "statement_callbacks")
        }
        saved_bubble = {
            name: getattr(bubble, name)
            for name in ("db", "properties", "properties_order", "tag_properties", "current_dialogue")
        }
        saved_history = store._history_list
        saved_history_enabled = store._history
        saved_nvl = store.nvl_list
        saved_current = ctx.current
        saved_seen = set(renpy.game.persistent._seen_translates)
        try:
            config.history_length = history_length
            config.nvl_list_length = nvl_length
            config.all_character_callbacks = [warp_test_no_interaction]
            config.voice_tag_callback = warp_test_no_interaction
            config.history_callbacks = []
            config.statement_callbacks = [bubble.statement_callback]
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
                for node in nodes:
                    if isinstance(node, renpy.ast.TranslateSay) and node.what == clear_text:
                        bubble.db[node.identifier]["clear_retain"] = True

            renpy.warp.reconstruct(nodes)

            history = [h.what for h in _history_list]
            page = [entry[1] for entry in nvl_list]
            tags = [tag for tag in renpy.get_showing_tags(bubble.retain_layer, sort=True) if tag.startswith("_retain_")]
            texts = [renpy.get_screen(tag, layer=bubble.retain_layer).scope["_kwargs"]["what"] for tag in tags]
            retained = [renpy.get_screen(tag, layer=bubble.retain_layer) for tag in tags]
            roundtrip = warp_pickle.loads(warp_pickle.dumps((_history_list, nvl_list, retained)))
            assert [h.what for h in roundtrip[0]] == history
            assert [entry[1] for entry in roundtrip[1]] == page
            assert [screen.scope["_kwargs"]["what"] for screen in roundtrip[2]] == texts
            assert all(h.rollback_identifier is None for h in _history_list)
            assert set(renpy.game.persistent._seen_translates) == saved_seen
            assert ctx.current == saved_current
            assert not renpy.is_warping()
            return history, page, texts, list(bubble.current_dialogue)
        finally:
            renpy.clear_retain(layer=bubble.retain_layer)
            store._history_list = saved_history
            store._history = saved_history_enabled
            store.nvl_list = saved_nvl
            for name, value in saved_config.items():
                setattr(config, name, value)
            for name, value in saved_bubble.items():
                setattr(bubble, name, value)


label warp_test_nvl_page:
    warp_test_nvl "one"
    warp_test_nvl "two"
    warp_test_nvl "three"
label warp_test_nvl_clear_boundary:
    nvl clear
    warp_test_nvl "four"
    warp_test_nvl "five"
    return

label warp_test_adv_lines:
    warp_test_adv "one"
    extend " two"
    warp_test_disabled "disabled"
    warp_test_unsupported "unsupported"
    warp_test_callable "fail"
    warp_test_adv "[warp_test_undefined_variable]"
    warp_test_callable "good"
    return

label warp_test_nvl_character_clear:
    warp_test_nvl "one"
    warp_test_nvl_clear "two"
    warp_test_nvl "three"
    return

label warp_test_multiple:
    warp_test_nvl "multi one" (multiple=2)
    warp_test_nvl "multi two" (multiple=2)
    return

label warp_test_overrides:
    warp_test_adv "hidden" (condition="False")
    warp_test_adv "disabled" (warp=False)
    warp_test_adv "override" (what_prefix="(", what_suffix=")")
    warp_test_adv "no wait{nw}"
    warp_test_adv "paused{w} text"
    return

label warp_test_bubble_lines:
    warp_test_bubble "one"
    warp_test_bubble "two"
    return

label warp_test_bubble_cleared:
    warp_test_bubble "one"
    menu:
        "Skipped choice":
            pass
    warp_test_bubble "two"
    return

label warp_test_bubble_adv_clear:
    warp_test_bubble "one"
    warp_test_adv "clear"
    warp_test_bubble "two"
    return

label warp_test_bubble_unretained:
    warp_test_unretained "one"
    return

label warp_test_bubble_screen_clear:
    warp_test_bubble "one"
    call screen _warp_test_bubble(None, "must not be shown")
    warp_test_bubble "two"
    return

label warp_test_bubble_scene_clear:
    warp_test_bubble "one"
    scene
    warp_test_bubble "two"
    return

testcase warp_dialogue:
    assert eval not Character(kind=warp_test_disabled).warp
    assert eval Character(kind=warp_test_disabled, warp=True).warp

    $ history, page, bubbles, editor = warp_test_replay("warp_test_nvl_page", "warp_test_nvl_clear_boundary")
    assert eval history == ["one", "two", "three"]
    assert eval page == ["one", "two", "three"]

    $ history, page, bubbles, editor = warp_test_replay("warp_test_nvl_page")
    assert eval history == ["one", "two", "three", "four", "five"]
    assert eval page == ["four", "five"]

    $ history, page, bubbles, editor = warp_test_replay("warp_test_nvl_character_clear")
    assert eval history == ["one", "two", "three"]
    assert eval page == ["three"]

    $ history, page, bubbles, editor = warp_test_replay("warp_test_nvl_page", nvl_length=1, history_length=2)
    assert eval history == ["four", "five"]
    assert eval page == ["five"]

    $ history, page, bubbles, editor = warp_test_replay("warp_test_adv_lines")
    assert eval len(history) == 2
    assert eval history[0] == "one{fast} two"
    assert eval history[1] == "good"

    $ history, page, bubbles, editor = warp_test_replay("warp_test_multiple")
    assert eval history == ["multi one", "multi two"]
    assert eval page == ["multi one", "multi two"]

    $ history, page, bubbles, editor = warp_test_replay("warp_test_overrides")
    assert eval history == ["(override)", "no wait{nw}", "paused{w} text"]

testcase warp_bubbles:
    $ history, page, bubbles, editor = warp_test_replay("warp_test_bubble_lines")
    assert eval history == ["one", "two"]
    assert eval bubbles == ["one", "two"]
    assert eval editor == []

    $ history, page, bubbles, editor = warp_test_replay("warp_test_bubble_lines", clear_text="two")
    assert eval history == ["one", "two"]
    assert eval bubbles == ["two"]

    $ history, page, bubbles, editor = warp_test_replay("warp_test_bubble_cleared")
    assert eval history == ["one", "two"]
    assert eval bubbles == ["two"]

    $ history, page, bubbles, editor = warp_test_replay("warp_test_bubble_screen_clear")
    assert eval history == ["one", "two"]
    assert eval bubbles == ["two"]

    $ history, page, bubbles, editor = warp_test_replay("warp_test_bubble_scene_clear")
    assert eval history == ["one", "two"]
    assert eval bubbles == ["two"]

    $ history, page, bubbles, editor = warp_test_replay("warp_test_bubble_adv_clear")
    assert eval history == ["one", "clear", "two"]
    assert eval bubbles == ["two"]

    $ history, page, bubbles, editor = warp_test_replay("warp_test_bubble_unretained")
    assert eval history == ["one"]
    assert eval bubbles == []


label warp_test_real:
    scene
    nvl clear
    warp_test_nvl "real one"
    warp_test_callable "fail"
    warp_test_nvl "real two"

label warp_test_real_target:
    python:
        assert [h.what for h in _history_list][-2:] == ["real one", "real two"]
        assert [entry[1] for entry in nvl_list] == ["real one", "real two"]
        assert not renpy.is_warping()
        renpy.quit()
