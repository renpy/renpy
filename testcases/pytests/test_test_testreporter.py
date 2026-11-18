# Copyright 2004-2026 Tom Rothamel <pytom@bishoujo.us>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


"""Tests for how the test reporter turns the asserts of a testcase into its status, in renpy/test/testreporter.py."""

from types import SimpleNamespace

import pytest

import renpy
from renpy.test.testreporter import OutcomeStatus, ReporterManager
from renpy.test.types import RenpyTestAssertionError

SCRIPT = """\
testsuite reporter_probe:
    testcase plain:
        pause 0

    testcase expected_to_fail:
        xfail True
        pause 0
"""


def assert_node(is_true: bool, xfail: bool = False) -> SimpleNamespace:
    """
    Returns a stand-in for an Assert node whose condition is `is_true`, and that is marked xfail if given.
    """

    return SimpleNamespace(is_assertion_true=is_true, xfail=xfail)


def run_testcase(name: str, *asserts: SimpleNamespace):
    """
    Runs the named testcase of SCRIPT through a new reporter, which logs `asserts` in order, and returns the
    testcase's outcome.

    The reporter has no console reporter attached, so nothing is printed. An assert that fails, or that was
    expected to fail and passes, raises RenpyTestAssertionError, as it does when the testcase is run; that
    is not an error here, as the outcome is what is checked.
    """

    suite = renpy.parser.parse("reporter_probe.rpy", SCRIPT)[0].test
    testcase = next(t for t in suite.subtests if t.name == name)

    reporter = ReporterManager()
    reporter.initialize_test_outcomes(suite)
    reporter.test_run_start()
    reporter.test_suite_start(suite)
    reporter.test_case_start(testcase)

    for node in asserts:
        try:
            reporter.log_assert(node)
        except RenpyTestAssertionError:
            pass

    reporter.test_case_end(testcase)

    return reporter.outcome_manager.get_outcome_by_test_block(testcase)


def test_expected_failure_is_not_hidden_by_a_passing_assert() -> None:
    """
    A testcase that is expected to fail, and has a passing assert before a failing one, is reported as
    xfailed, with both asserts counted.

    This is the case the boolean_conditions.boolean_value_mixed testcase relies on: it is xfail, with
    `assert True` and then `assert False`, and must not be reported as an unexpected pass because the first
    assert passed.
    """

    outcome = run_testcase("expected_to_fail", assert_node(True), assert_node(False))

    assert outcome.status == OutcomeStatus.XFAILED
    assert (outcome.num_asserts_passed, outcome.num_asserts_xfailed) == (1, 1)


@pytest.mark.parametrize(
    "name, asserts, status",
    [
        ("expected_to_fail", [assert_node(True)], OutcomeStatus.XPASSED),
        ("plain", [assert_node(True)], OutcomeStatus.PASSED),
        ("plain", [assert_node(False)], OutcomeStatus.FAILED),
        ("plain", [assert_node(False, xfail=True)], OutcomeStatus.XFAILED),
        ("plain", [assert_node(True), assert_node(False, xfail=True)], OutcomeStatus.PASSED),
        ("plain", [assert_node(True), assert_node(False)], OutcomeStatus.FAILED),
    ],
    ids=[
        "expected-failure-that-passes",
        "passing-assert",
        "failing-assert",
        "only-expected-failing-assert",
        "passing-and-expected-failing-asserts",
        "failure-after-pass",
    ],
)
def test_testcase_status_from_asserts(name: str, asserts: list[SimpleNamespace], status: OutcomeStatus) -> None:
    """
    The status of a testcase follows from its asserts and from whether the testcase or the assert is marked
    xfail: a failure is expected only where marked, and a testcase that is expected to fail but doesn't is
    reported as an unexpected pass.
    """

    assert run_testcase(name, *asserts).status == status
