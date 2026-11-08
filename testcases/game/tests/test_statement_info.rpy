# This file tests that renpy.get_statement_info describes the executing statement. What it returns while
# a statement is predicted is tested in testcases/pytests/test_execution_statement_info.py.

label statement_info_target:
    record statement info
    return


testcase statement_info:
    run Jump("statement_info_target")

    assert eval statement_info_execution is not None
    assert eval statement_info_execution.filename.endswith("tests/test_statement_info.rpy")
    assert eval statement_info_execution.linenumber > 0
    assert eval statement_info_execution.tlid is None
