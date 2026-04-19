# test_savestring.rpy
#
# In-game testcase for save_to_string. Place in testcases/game/tests/
# alongside the existing test_*.rpy files.
#
# NOTE: this file intentionally does NOT exercise load_from_string
# end-to-end. Ren'Py's load path jumps via
# `log.unfreeze(..., label="_after_load")` which never returns to the
# caller -- you cannot write assertions after the call and have them
# execute. End-to-end verification of load_from_string is in
# MANUAL_QA.md (export on session A, quit, restart, import on
# session B, confirm restored values).
#
# This testcase verifies:
#   - save_to_string returns a well-formed string on an existing slot
#   - save_to_string returns None on a missing slot
#   - load_from_string raises InvalidSaveStringFormat on malformed input

label test_savestring:

    # Cleanup-first: remove any stale slot from a prior failed run
    # before we write a new one. Idempotent on a clean install.
    python:
        try:
            renpy.unlink_save("_test_savestring")
        except Exception:
            pass

    $ x = 1
    $ y = "hello"
    $ renpy.take_screenshot()
    $ renpy.save("_test_savestring")

    $ code = renpy.save_to_string("_test_savestring")

    if code is None:
        "FAIL: save_to_string returned None on existing slot"
        return

    if not code.startswith("RPYS1-"):
        "FAIL: code does not start with RPYS1-"
        return

    # Ren'Py text substitution accepts variable names but not
    # arbitrary function calls; compute the length into a local
    # variable first.
    $ code_len = len(code)
    "save_to_string produced [code_len]-char code"

    $ missing = renpy.save_to_string("_does_not_exist_ever_")
    if missing is not None:
        "FAIL: save_to_string on missing slot should return None"
        return

    python:
        bad_prefix_raised = False
        try:
            renpy.load_from_string("NOPE-xxxx")
        except renpy.InvalidSaveStringFormat:
            bad_prefix_raised = True

    if not bad_prefix_raised:
        "FAIL: bad-prefix did not raise InvalidSaveStringFormat"
        return

    python:
        bad_b64_raised = False
        try:
            renpy.load_from_string("RPYS1-!!!not-base64!!!")
        except renpy.InvalidSaveStringFormat:
            bad_b64_raised = True

    if not bad_b64_raised:
        "FAIL: bad-base64 did not raise InvalidSaveStringFormat"
        return

    python:
        none_input_raised = False
        try:
            renpy.load_from_string(None)
        except renpy.InvalidSaveStringFormat:
            none_input_raised = True

    if not none_input_raised:
        "FAIL: None input did not raise InvalidSaveStringFormat"
        return

    # Post-run cleanup (best-effort; covered by cleanup-first on
    # subsequent runs if this is skipped).
    python:
        try:
            renpy.unlink_save("_test_savestring")
        except Exception:
            pass

    "PASS: save_to_string and load_from_string error paths"
    return
