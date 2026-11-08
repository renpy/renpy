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

"""Tests for renpy.test.testexecution: the phases of a test run, the enabled expressions, and the window size."""

import pytest

import renpy
from renpy.test import testexecution, testfilter, testreporter

################################################################################
# Phases
#
# The root `global` suite must make one pass over its tests for each of its parameter sets, or a single pass
# when it has none. Each pass runs hooks and tests again in a game already changed by the last one.
#
# These tests live here and not in the testcases project because its `global` suite ends with an `exit` in
# teardown, which quits before the phase that decides whether to start another pass.
################################################################################

MAX_UPDATES = 1000
"Limits how long a test drives the phase controller, so that a run that never ends fails."


class FakeNodeExecutor:
    """
    Stands in for NodeExecutor, finishing each block immediately without running its nodes.

    The real executor needs a running game, while these tests are only about which blocks the phases
    choose and how the outcomes of those blocks are counted.
    """

    done = True

    def __init__(self):
        self.next_node = None
        self.end_callbacks = []

    def set_next_node(self, next):
        self.next_node = next

    def set_end_callback(self, callback):
        self.end_callbacks = callback if isinstance(callback, list) else [callback]

    def execute(self):
        self.next_node = None

        callbacks = self.end_callbacks
        self.end_callbacks = []

        for callback in callbacks:
            callback()


class RecordingReporter(testreporter.Reporter):
    """
    Records each hook and test case as it starts, along with the parameters in scope for a test case.
    """

    def __init__(self):
        super().__init__()
        self.events = []

    def test_hook_start(self, outcome, depth=0):
        self.events.append(outcome.test_block.name)

    def test_case_start(self, outcome, depth=0):
        self.events.append((outcome.test_block.name, dict(testexecution.get_current_scope())))


@pytest.fixture
def run(mocker):
    """
    Returns a function that runs a `testsuite global` script to completion, and returns its reporter
    manager and recording reporter.

    The module state the phases use is replaced, so that nothing is left behind for later tests.
    """

    def run(source):
        root = renpy.parser.parse("testsuite_passes.rpy", source)[0].test

        manager = testreporter.ReporterManager()
        recorder = RecordingReporter()
        manager.add_reporter(recorder)
        manager.initialize_test_outcomes(root)

        mocker.patch.object(testreporter, "reporter", manager)
        mocker.patch.object(testexecution, "suite_stack", [])
        mocker.patch.object(testexecution, "scope_stack", [{}])
        mocker.patch.object(testexecution, "node_executor", FakeNodeExecutor(), create=True)
        mocker.patch.object(testexecution, "execution_filter", testfilter.ExecutionFilter([]), create=True)
        mocker.patch.object(renpy.test.testmouse, "reset")

        controller = testexecution.TestPhaseController(root)

        for _ in range(MAX_UPDATES):
            if not controller.is_running:
                break

            controller.update()
        else:
            pytest.fail("The test run did not end.")

        return manager, recorder

    return run


def test_unparameterized_root_makes_one_pass(run):
    """
    Hooks and tests run once, in order, when the root suite has no parameters.

    The root's parameter index starts before the first set, so a run that never advances it before the
    first pass makes a second pass over the same tests.
    """

    _, recorder = run(
        """\
testsuite global:
    setup:
        pause 0
    before testcase:
        pause 0
    testcase one:
        pause 0
    testcase two:
        pause 0
"""
    )

    assert recorder.events == ["setup", "before_testcase", ("one", {}), "before_testcase", ("two", {})]


def test_totals_count_each_test_once(run):
    """
    The summary totals match the tests that exist, for tests directly in the root and in a nested suite.

    A second pass reuses the first pass's outcomes and adds their counts again, once more at each level
    of nesting, so the nested suite guards against more than the direct tests would.
    """

    manager, _ = run(
        """\
testsuite global:
    testcase direct:
        pause 0
    testsuite nested:
        testcase first:
            pause 0
        testcase second:
            pause 0
"""
    )

    outcomes = manager.outcome_manager

    assert outcomes.num_testcases == 3
    assert outcomes.num_testcases_passed == 3
    assert outcomes.num_testsuites == 2
    assert outcomes.num_testsuites_passed == 2


def test_parameterized_root_makes_one_pass_per_set(run):
    """
    A root suite with parameters runs its hooks and tests once for each set, in order.

    The outcomes of a parameterized suite are named after its parameters, so the first pass also has to
    begin on a real parameter set for its outcome to be found.
    """

    manager, recorder = run(
        """\
testsuite global:
    parameter x = [1, 2]
    setup:
        pause 0
    testcase one:
        pause 0
"""
    )

    assert recorder.events == ["setup", ("one", {"x": 1}), "setup", ("one", {"x": 2})]
    assert manager.outcome_manager.num_testcases == 2
    assert manager.outcome_manager.num_testcases_passed == 2


################################################################################
# Enabled expressions
#
# The `enabled` property is compiled into the .rpyc, so it must be evaluated when tests are run rather than
# when the script is parsed. Otherwise a result that depends on the platform or on game files would be stale.
################################################################################


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


################################################################################
# Window size
################################################################################


@pytest.mark.parametrize(
    ("initialized", "mobile", "expected"),
    [
        (False, False, None),
        (True, True, None),
        (True, False, (800, 600)),
    ],
    ids=["normal-execution", "mobile", "desktop-test-execution"],
)
def test_get_test_window_size(mocker, initialized, mobile, expected):
    """
    Outside test execution, and on mobile where the window is the whole screen, the window size is not
    overridden. During desktop test execution it is the game's virtual resolution, so tests see the same
    geometry on every machine.
    """

    mocker.patch.object(testexecution, "initialized", initialized)
    mocker.patch.object(renpy, "mobile", mobile)
    mocker.patch.object(renpy.config, "screen_width", 800)
    mocker.patch.object(renpy.config, "screen_height", 600)
    assert testexecution.get_test_window_size() == expected
