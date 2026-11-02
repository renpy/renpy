label nested_context_rollback:
    "Before the nested context."
    $ renpy.call_in_new_context("nested_context_rollback_inner")
    "After the nested context."
    return

label nested_context_rollback_inner:
    $ renpy.session["nested_context_runs"] = renpy.session.get("nested_context_runs", 0) + 1

    if renpy.session["nested_context_runs"] == 1:
        $ renpy.rollback(force=True)

    return

label nested_context_restart_top:
    python:
        renpy.session["nested_context_outer_runs"] += 1
        renpy.call_in_new_context("nested_context_restart_top_inner")

    "After the nested context."
    return

label nested_context_restart_top_inner:
    python:
        renpy.session["nested_context_runs"] += 1

        if renpy.session["nested_context_runs"] == 1:
            raise renpy.execution.RestartTopContext()

    return

label nested_context_replay_start:
    "Before the replay."

    python:
        renpy.session["nested_context_outer_runs"] += 1
        renpy.call_replay("nested_context_replay")

    "After the replay."
    return

label nested_context_replay:
    "Replay before the rollback."

    python:
        renpy.session["nested_context_runs"] += 1
        renpy.session["nested_context_depths"].append(len(renpy.game.contexts))

        if renpy.session["nested_context_runs"] == 1:
            if renpy.session["nested_context_replay_nested"]:
                renpy.call_in_new_context("nested_context_replay_inner")
            else:
                renpy.rollback(force=True)

    "Replay after the rollback."
    return

label nested_context_replay_inner:
    $ renpy.rollback(force=True)
    return

label nested_context_reset:
    "Before the reset."
    $ renpy.session["nested_context_outer_runs"] += 1

    if renpy.session["nested_context_reset_from"] == "nested":
        $ renpy.call_in_new_context("nested_context_reset_inner")
    elif renpy.session["nested_context_reset_from"] == "replay":
        $ renpy.call_replay("nested_context_reset_inner")
    else:
        jump nested_context_reset_inner

    "Should not be reached."
    return

label nested_context_reset_inner:
    $ renpy.reset_all_contexts()
    "After the reset."
    return

testsuite nested_context:
    description "Tests control exceptions that are raised from a nested context."

    testcase reset_all_contexts:
        description "reset_all_contexts continues at the next statement, in a single new top context."

        parameter reset_from = ["top", "nested", "replay"]

        $ renpy.session["nested_context_outer_runs"] = 0
        $ renpy.session["nested_context_reset_from"] = reset_from
        run Start("nested_context_reset")
        advance until "After the reset."

        assert eval (len(renpy.game.contexts) == 1)
        assert eval (renpy.game.context().rollback)
        assert eval (renpy.session["nested_context_outer_runs"] == 1)

        # Leaving a replay also has to restore the game's store.
        assert eval (_in_replay is None)

        advance until screen "main_menu"

    testcase restart_top:
        description "RestartTopContext leaves the nested context and restarts the top one, rather than re-running the nested one."

        $ renpy.session["nested_context_runs"] = 0
        $ renpy.session["nested_context_outer_runs"] = 0
        run Start("nested_context_restart_top")
        advance until "After the nested context."

        assert eval (len(renpy.game.contexts) == 1)
        assert eval (renpy.session["nested_context_outer_runs"] == 2)
        assert eval (renpy.session["nested_context_runs"] == 2)

        advance until screen "main_menu"

    testcase rollback:
        description "Rolling back from a nested context resumes in the top context, without growing the context stack."

        $ renpy.session["nested_context_runs"] = 0
        run Start("nested_context_rollback")
        advance until "After the nested context."

        assert eval (len(renpy.game.contexts) == 1)
        assert eval (renpy.session["nested_context_runs"] == 2)

        advance until screen "main_menu"

    testcase replay_rollback:
        description "A replay has its own rollback log, so rolling back in it stays in the replay."

        parameter nested = [False, True]

        $ renpy.session["nested_context_runs"] = 0
        $ renpy.session["nested_context_outer_runs"] = 0
        $ renpy.session["nested_context_depths"] = []
        $ renpy.session["nested_context_replay_nested"] = nested
        run Start("nested_context_replay_start")
        advance until "Replay after the rollback."

        # Rolling back the game's log instead would enter the replay a second time.
        assert eval (renpy.session["nested_context_outer_runs"] == 1)
        assert eval (_in_replay == "nested_context_replay")
        assert eval (renpy.session["nested_context_runs"] == 2)
        assert eval (renpy.session["nested_context_depths"][0] == renpy.session["nested_context_depths"][1])

        advance until "After the replay."

        assert eval (_in_replay is None)
        assert eval (len(renpy.game.contexts) == 1)

        advance until screen "main_menu"
