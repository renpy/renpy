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

"""
The root `global` suite must make one pass over its tests for each of its parameter sets, or a single
pass when it has none. Each pass runs hooks and tests again in a game already changed by the last one.

These tests live here and not in the testcases project because its `global` suite ends with an `exit`
in teardown, which quits before the phase that decides whether to start another pass.
"""

import pytest

import renpy
from renpy.test import testexecution, testfilter, testreporter

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
