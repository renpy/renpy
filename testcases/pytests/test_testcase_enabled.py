"""
The `enabled` property is compiled into the .rpyc, so it must be evaluated when tests are run rather
than when the script is parsed. Otherwise a result that depends on the platform or on game files would
be stale.
"""

import pytest

import renpy
from renpy.test import testexecution

SCRIPT = """\
testsuite enabled_probe:
    enabled enabled_probe_flag

    testcase inner:
        enabled not enabled_probe_flag
        pause 0

    testcase plain:
        pause 0
"""


def parse_suite(source: str = SCRIPT):
    """
    Parses `source` and returns the TestSuite defined by its first statement.
    """

    nodes = renpy.parser.parse("enabled_probe.rpy", source)
    return nodes[0].test


def evaluate(mocker, tests, **store):
    """
    Evaluates the enabled expressions of `tests` with `store` as the contents of the game store.

    The registered testcases are replaced by `tests` and the store values are added; both are restored
    when the test ends. A later call layers its values over an earlier one.
    """

    mocker.patch.dict(testexecution.testcases, {t.name: t for t in tests}, clear=True)
    mocker.patch.dict(renpy.python.store_dicts["store"], store)
    testexecution.evaluate_enabled_expressions()


def test_parse_does_not_evaluate_the_expression():
    """
    Parsing stores the enabled expression's source and leaves the test enabled.

    The name is undefined when parsing, so evaluating it then would fail.
    """

    suite = parse_suite()

    assert suite.enabled_expr == "enabled_probe_flag"
    assert suite.enabled


def test_evaluation_uses_the_store_when_run(mocker):
    """
    Evaluating the expressions uses the store values at run time, and the same parsed objects follow a
    later change, as a cached .rpyc would.

    The suite and its inner testcase have opposite expressions, and the plain testcase has none, so it
    stays enabled either way.
    """

    suite = parse_suite()
    inner, plain = suite.subtests

    evaluate(mocker, [suite, inner, plain], enabled_probe_flag=False)
    assert (suite.enabled, inner.enabled, plain.enabled) == (False, True, True)

    evaluate(mocker, [suite, inner, plain], enabled_probe_flag=True)
    assert (suite.enabled, inner.enabled, plain.enabled) == (True, False, True)


def test_tests_without_an_expression_keep_their_flag(mocker):
    """
    A test with no enabled_expr keeps its existing enabled flag.

    Objects unpickled from an older .rpyc have no enabled_expr slot, and must not be re-enabled or fail
    when the expressions are evaluated.
    """

    suite = parse_suite()
    suite.enabled = False
    del suite.enabled_expr

    evaluate(mocker, [suite], enabled_probe_flag=True)
    assert not suite.enabled


def test_only_requires_the_test_to_be_enabled(mocker):
    """
    Marking a test `only` while its enabled expression is false is an error, reported when the
    expressions are evaluated, because the run would otherwise silently do nothing.
    """

    suite = parse_suite(
        SCRIPT.replace("    enabled enabled_probe_flag\n", "    only True\n    enabled enabled_probe_flag\n")
    )

    with pytest.raises(ValueError):
        evaluate(mocker, [suite], enabled_probe_flag=False)
