init python:
    def collect_statement_info_prediction(label="statement_info_target"):
        ctx = renpy.game.context()
        old_callback = config.predict_statements_callback
        old_count = config.predict_statements
        old_identifier = ctx.translate_identifier
        old_alternate = ctx.alternate_translate_identifier
        before = renpy.get_statement_info()

        statement_info_predictions[:] = []

        try:
            config.predict_statements_callback = lambda current: [label]
            config.predict_statements = 3
            ctx.translate_identifier = "statement_info_tlid"
            ctx.alternate_translate_identifier = None
            list(ctx.predict())
        finally:
            config.predict_statements_callback = old_callback
            config.predict_statements = old_count
            ctx.translate_identifier = old_identifier
            ctx.alternate_translate_identifier = old_alternate

        after = renpy.get_statement_info()
        return list(statement_info_predictions), before, after


label statement_info_target:
    record statement info
    return


label statement_info_failure_target:
    fail statement info prediction
    return


testcase statement_info:
    run Jump("statement_info_target")

    assert eval statement_info_execution is not None
    assert eval statement_info_execution.filename.endswith("tests/test_statement_info.rpy")
    assert eval statement_info_execution.linenumber > 0
    assert eval statement_info_execution.tlid is None

    $ predictions, before_prediction, after_prediction = collect_statement_info_prediction()

    assert eval len(predictions) == 1
    assert eval predictions[0].filename == statement_info_execution.filename
    assert eval predictions[0].linenumber == statement_info_execution.linenumber
    assert eval predictions[0].tlid == "statement_info_tlid"
    assert eval after_prediction.filename == before_prediction.filename
    assert eval after_prediction.linenumber == before_prediction.linenumber

    $ _, before_failure, after_failure = collect_statement_info_prediction("statement_info_failure_target")

    assert eval after_failure.filename == before_failure.filename
    assert eval after_failure.linenumber == before_failure.linenumber
