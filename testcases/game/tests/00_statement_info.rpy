python early:
    statement_info_execution = None

    def parse_record_statement_info(l):
        l.expect_eol()
        return True

    def execute_record_statement_info(parsed):
        global statement_info_execution
        statement_info_execution = renpy.get_statement_info()

    renpy.register_statement(
        "record statement info",
        parse=parse_record_statement_info,
        execute=execute_record_statement_info,
    )
