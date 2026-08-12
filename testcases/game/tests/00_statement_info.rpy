python early:
    statement_info_execution = None
    statement_info_predictions = []

    def parse_record_statement_info(l):
        l.expect_eol()
        return True

    def execute_record_statement_info(parsed):
        global statement_info_execution
        statement_info_execution = renpy.get_statement_info()

    def predict_record_statement_info(parsed):
        statement_info_predictions.append(renpy.get_statement_info())

    def predict_fail_statement_info(parsed):
        raise Exception("statement info prediction failure")

    renpy.register_statement(
        "record statement info",
        parse=parse_record_statement_info,
        execute=execute_record_statement_info,
        predict=predict_record_statement_info,
        predict_all=False,
    )

    renpy.register_statement(
        "fail statement info prediction",
        parse=parse_record_statement_info,
        predict=predict_fail_statement_info,
        predict_all=False,
    )
