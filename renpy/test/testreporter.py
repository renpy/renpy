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

import abc
import contextlib
from dataclasses import dataclass, field
from enum import Enum
import io
import os
import platform

import renpy
from renpy.error import ANSIColors
from renpy.test.testsettings import _test
from renpy.test.types import RenpyTestAssertionError
from renpy.test.testast import TestCase, TestHook, TestSuite, BaseTestBlock, Assert


def format_seconds(seconds: float) -> str:
    if seconds >= 60:
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{seconds:0.3f} s [{minutes:02d}:{secs:02d}]"

    return f"{seconds:0.3f} s"


class OutcomeStatus(Enum):
    NOT_RUN = "not_run"
    PENDING = "pending"
    PASSED = "passed"
    XFAILED = "xfailed"  # Expected fail
    FAILED = "failed"
    XPASSED = "xpassed"  # Unexpected pass
    SKIPPED = "skipped"


@dataclass
class BaseOutcome:
    """
    Base class for test outcomes. Each (parameterized) run of a test case, test suite, or hook
    produces one of these.
    """

    test_block: BaseTestBlock = field(repr=False)
    name: str = "<unnamed>"
    full_path: str = "<unnamed_path>"

    parent: "BaseOutcome | None" = field(default=None, repr=False)
    num_asserts: int = 0
    num_asserts_passed: int = 0
    num_asserts_xfailed: int = 0
    num_asserts_failed: int = 0
    num_asserts_xpassed: int = 0

    start_time: float = field(default=0.0, repr=False)
    end_time: float = field(default=0.0, repr=False)
    duration: float = 0.0
    status: OutcomeStatus = OutcomeStatus.NOT_RUN
    exception: str = ""

    def begin(self) -> None:
        if self.name == "<unnamed>":
            self.name = self.test_block.current_parameterized_name
        if self.full_path == "<unnamed_path>":
            self.full_path = self.test_block.full_path

        self.start_time = renpy.display.core.get_time()
        self.end_time = 0.0
        self.status = OutcomeStatus.PENDING

    def finalize_time(self) -> None:
        if self.end_time == 0.0:
            now = renpy.display.core.get_time()
            if self.start_time == 0.0:
                self.start_time = now

            self.end_time = now
            self.duration = self.end_time - self.start_time

    def end(self, status: OutcomeStatus | None = None) -> None:
        """
        Finalize the test case outcomes.

        If status is None, it will be set to PASSED if no asserts failed,
        otherwise it is set to FAILED.
        """
        if self.end_time > 0.0:
            return  # Already ended

        self.finalize_time()

        if status is not None:
            self.status = status

        elif self.status == OutcomeStatus.PENDING:
            if self.num_asserts_failed > 0:
                self.status = OutcomeStatus.FAILED
            elif self.num_asserts_xfailed > 0 and self.num_asserts_passed == 0:
                self.status = OutcomeStatus.XFAILED
            else:
                self.status = OutcomeStatus.PASSED


@dataclass
class TestHookOutcome(BaseOutcome):
    test_block: TestHook = field(repr=False)


@dataclass
class TestCaseOutcome(BaseOutcome):
    test_block: TestCase = field(repr=False)


@dataclass
class TestSuiteOutcome(TestCaseOutcome):
    test_block: TestSuite = field(repr=False)
    name: str = ""

    children: list[BaseOutcome] = field(default_factory=list, repr=False)

    num_testsuites: int = 0
    num_testsuites_passed: int = 0
    num_testsuites_xfailed: int = 0
    num_testsuites_failed: int = 0
    num_testsuites_xpassed: int = 0
    num_testsuites_skipped: int = 0

    num_testcases: int = 0
    num_testcases_passed: int = 0
    num_testcases_xfailed: int = 0
    num_testcases_failed: int = 0
    num_testcases_xpassed: int = 0
    num_testcases_skipped: int = 0

    num_hooks: int = 0
    num_hooks_passed: int = 0
    num_hooks_xfailed: int = 0
    num_hooks_failed: int = 0
    num_hooks_xpassed: int = 0
    num_hooks_skipped: int = 0

    def get_child_by_test_block(self, test_block: BaseTestBlock) -> BaseOutcome:
        for child in self.children:
            if child.test_block == test_block and child.name == test_block.current_parameterized_name:
                return child

        if isinstance(test_block, TestHook):
            # Create TestHookOutcome dynamically
            outcome = TestHookOutcome(test_block)
            self.children.append(outcome)
            return outcome

        raise ValueError(
            f"Outcomes for '{test_block.current_full_parameterized_path}' not found in '{self.name}'.\n"
            f"Available names: {[c.name for c in self.children]}"
        )

    def end(self, status: OutcomeStatus | None = None) -> None:
        """
        Finalize the test suite outcome.

        If status is None, it will be set to PASSED if all test cases passed,
        FAILED if any test case failed, or SKIPPED if all test cases were skipped.
        """

        if self.end_time > 0.0:
            return  # Already ended

        self.finalize_time()

        for child in self.children:
            if status == OutcomeStatus.SKIPPED:
                child.end(OutcomeStatus.SKIPPED)

            self.num_asserts += child.num_asserts
            self.num_asserts_passed += child.num_asserts_passed
            self.num_asserts_failed += child.num_asserts_failed

            if isinstance(child, TestSuiteOutcome):
                self.num_testsuites += child.num_testsuites + 1
                self.num_testsuites_passed += child.num_testsuites_passed
                self.num_testsuites_xfailed += child.num_testsuites_xfailed
                self.num_testsuites_failed += child.num_testsuites_failed
                self.num_testsuites_xpassed += child.num_testsuites_xpassed
                self.num_testsuites_skipped += child.num_testsuites_skipped

                self.num_testcases += child.num_testcases
                self.num_testcases_passed += child.num_testcases_passed
                self.num_testcases_xfailed += child.num_testcases_xfailed
                self.num_testcases_failed += child.num_testcases_failed
                self.num_testcases_xpassed += child.num_testcases_xpassed
                self.num_testcases_skipped += child.num_testcases_skipped

                self.num_hooks += child.num_hooks
                self.num_hooks_passed += child.num_hooks_passed
                self.num_hooks_xfailed += child.num_hooks_xfailed
                self.num_hooks_failed += child.num_hooks_failed
                self.num_hooks_xpassed += child.num_hooks_xpassed
                self.num_hooks_skipped += child.num_hooks_skipped

                if child.status == OutcomeStatus.PASSED:
                    self.num_testsuites_passed += 1
                elif child.status == OutcomeStatus.XFAILED:
                    self.num_testsuites_xfailed += 1
                elif child.status == OutcomeStatus.FAILED:
                    self.num_testsuites_failed += 1
                elif child.status == OutcomeStatus.XPASSED:
                    self.num_testsuites_xpassed += 1
                elif child.status == OutcomeStatus.SKIPPED:
                    self.num_testsuites_skipped += 1

            elif isinstance(child, TestCaseOutcome):
                self.num_testcases += 1
                if child.status == OutcomeStatus.PASSED:
                    self.num_testcases_passed += 1
                elif child.status == OutcomeStatus.XFAILED:
                    self.num_testcases_xfailed += 1
                elif child.status == OutcomeStatus.FAILED:
                    self.num_testcases_failed += 1
                elif child.status == OutcomeStatus.XPASSED:
                    self.num_testcases_xpassed += 1
                elif child.status == OutcomeStatus.SKIPPED:
                    self.num_testcases_skipped += 1

            elif isinstance(child, TestHookOutcome):
                self.num_hooks += 1
                if child.status == OutcomeStatus.PASSED:
                    self.num_hooks_passed += 1
                elif child.status == OutcomeStatus.XFAILED:
                    self.num_hooks_xfailed += 1
                elif child.status == OutcomeStatus.FAILED:
                    self.num_hooks_failed += 1
                elif child.status == OutcomeStatus.XPASSED:
                    self.num_hooks_xpassed += 1
                elif child.status == OutcomeStatus.SKIPPED:
                    self.num_hooks_skipped += 1

        if status is not None:
            self.status = status

        elif self.status == OutcomeStatus.PENDING:
            if self.num_testcases_failed > 0 or self.num_hooks_failed > 0:
                self.status = OutcomeStatus.FAILED
            elif self.num_testcases_skipped == self.num_testcases:
                self.status = OutcomeStatus.SKIPPED
            elif self.num_testcases_xfailed > 0 and self.num_testcases_passed == 0:
                self.status = OutcomeStatus.XFAILED
            else:
                self.status = OutcomeStatus.PASSED


class OutcomeManager(TestSuiteOutcome):
    @property
    def num_testsuites_not_run(self) -> int:
        return (
            self.num_testsuites
            - self.num_testsuites_passed
            - self.num_testsuites_xfailed
            - self.num_testsuites_failed
            - self.num_testsuites_xpassed
            - self.num_testsuites_skipped
        )

    @property
    def num_testcases_not_run(self) -> int:
        return (
            self.num_testcases
            - self.num_testcases_passed
            - self.num_testcases_xfailed
            - self.num_testcases_failed
            - self.num_testcases_xpassed
            - self.num_testcases_skipped
        )

    @property
    def num_hooks_not_run(self) -> int:
        return (
            self.num_hooks
            - self.num_hooks_passed
            - self.num_hooks_xfailed
            - self.num_hooks_failed
            - self.num_hooks_xpassed
            - self.num_hooks_skipped
        )

    def __init__(self, root: TestSuite):
        super().__init__(root, root.current_parameterized_name)
        self.root = root
        self.children = self.build_outcome_hierarchy(root, self)

    def build_outcome_hierarchy(self, suite: TestSuite, parent_outcome: TestSuiteOutcome) -> list[BaseOutcome]:
        ## NOTE: TestHookOutcomes are created dynamically during execution, not here.
        rv: list[BaseOutcome] = []
        for parent_idx in range(len(suite.parameters) or 1):
            suite_param_outcome = TestSuiteOutcome(suite, suite.get_parameterized_name(parent_idx))
            suite_param_outcome.parent = parent_outcome
            rv.append(suite_param_outcome)

            for subtest in suite.subtests:
                if isinstance(subtest, TestSuite):
                    suite_param_outcome.children.extend(self.build_outcome_hierarchy(subtest, suite_param_outcome))

                elif isinstance(subtest, TestCase):
                    for idx in range(len(subtest.parameters) or 1):
                        outcome = TestCaseOutcome(subtest, subtest.get_parameterized_name(idx))
                        outcome.parent = suite_param_outcome
                        suite_param_outcome.children.append(outcome)

                else:
                    raise ValueError(f"Unsupported: {type(suite)}")

        return rv

    def get_outcome_by_test_block(self, test_block: BaseTestBlock) -> BaseOutcome:
        """Get the outcome object corresponding to the given test block (with parameterization)."""

        # Build the path from the target block back to the root
        path: list[BaseTestBlock] = []
        current = test_block
        while current:
            path.append(current)
            current = current.parent

        # Start at the root and traverse down to the target
        current_outcome: TestSuiteOutcome = self

        for i, n in enumerate(reversed(path)):
            n_outcome = current_outcome.get_child_by_test_block(n)

            if i == len(path) - 1:
                return n_outcome

            if not isinstance(n_outcome, TestSuiteOutcome):
                raise ValueError(f"Expected TestSuiteOutcome at '{n.full_path}', got {type(n_outcome).__name__}")

            current_outcome = n_outcome

        raise ValueError(f"Outcomes for '{test_block.current_full_parameterized_path}' not found.")


def get_exception_string(
    epc: renpy.error.ExceptionPrintContext, exception: Exception, run_stack: list[renpy.error.FrameSummary]
) -> str:
    force_color = not os.environ.get("FORCE_COLOR") and isinstance(epc, renpy.error.ANSIColoredPrintContext)
    if force_color:
        os.environ["FORCE_COLOR"] = "1"

    with contextlib.redirect_stdout(io.StringIO()) as string_stream:
        renpy.error.report_exception(exception, editor=False)

        ## Report where in the script this exception occurred
        if isinstance(epc, renpy.error.TextIOExceptionPrintContext):
            epc.file = string_stream

        ctx = renpy.game.context()
        frames = ctx.report_traceback("", last=False)
        for filename, line_number, name, text in frames:
            summary = renpy.error.FrameSummary(name, filename, line_number, text=text)
            filename = renpy.exports.unelide_filename(filename)

            epc.location(filename, line_number, name)
            epc.string("  " + summary.line.strip())

        epc.indent_depth = 0
        epc.string("\nDuring testcase execution:")

        epc.indent_depth = 1

        for frame in run_stack:
            filename = renpy.exports.unelide_filename(frame.filename)
            epc.location(filename, frame.lineno, frame.name)
            epc.string("  " + frame.line.strip())

    if force_color:
        del os.environ["FORCE_COLOR"]
    return string_stream.getvalue()


def get_assertion_error_string(epc: renpy.error.ExceptionPrintContext, assert_node: Assert, node_name: str) -> str:
    force_color = not os.environ.get("FORCE_COLOR") and isinstance(epc, renpy.error.ANSIColoredPrintContext)
    if force_color:
        os.environ["FORCE_COLOR"] = "1"

    with contextlib.redirect_stdout(io.StringIO()) as string_stream:
        expr = str(assert_node.condition)

        filename = renpy.exports.unelide_filename(assert_node.filename)
        lines = renpy.lexer.list_logical_lines(filename)
        for fname, line_num, line in lines:
            if line_num == assert_node.linenumber:
                expr = line.strip()
                break

        epc.location(filename, assert_node.linenumber, node_name)
        epc.final_exception_line("AssertionError", expr)

    if force_color:
        del os.environ["FORCE_COLOR"]

    return string_stream.getvalue()


class Reporter(abc.ABC):
    """
    Base class for reporters that handle reporting of test outcomes.
    """

    def __init__(self):
        self.epc: renpy.error.ExceptionPrintContext = renpy.error.MaybeColoredExceptionPrintContext()

    def test_run_start(self, outcomes: OutcomeManager) -> None:
        """Called when the entire test run starts."""
        pass

    def test_run_end(self, outcomes: OutcomeManager) -> None:
        """Called when the entire test run ends."""
        pass

    def test_suite_start(self, outcome: TestSuiteOutcome, depth: int = 0) -> None:
        """Called when a test suite starts."""
        pass

    def test_suite_end(self, outcome: TestSuiteOutcome, depth: int = 0) -> None:
        """Called when a test suite ends."""
        pass

    def test_case_start(self, outcome: TestCaseOutcome, depth: int = 0) -> None:
        """Called when a test case starts."""
        pass

    def test_case_end(self, outcome: TestCaseOutcome, depth: int = 0) -> None:
        """Called when a test case ends."""
        pass

    def test_hook_start(self, outcome: TestHookOutcome, depth: int = 0) -> None:
        """Called when a test hook starts."""
        pass

    def test_hook_end(self, outcome: TestHookOutcome, depth: int = 0) -> None:
        """Called when a test hook ends."""
        pass

    def test_case_skipped(self, outcome: TestCaseOutcome, depth: int = 0) -> None:
        """Called when a test case is skipped."""
        pass

    def log_assert(self, assert_node: Assert, status: OutcomeStatus, node_name: str = "") -> None:
        """Called for each assert in the test case, even if it did not fail."""
        pass

    def log_exception(self, exception: Exception, run_stack: list[renpy.error.FrameSummary], xfailed: bool) -> None:
        """
        Called when an exception is raised from the test case or the game
        raises an error.
        """
        pass

    def log_message(self, message: str) -> None:
        """Called when a message should be logged."""
        pass

    def on_reload(self) -> None:
        """Called when the game is reloaded."""
        pass


class ConsoleReporter(Reporter):
    """
    Reporter that prints test outcomes to the console.
    """

    _is_last_line_written_by_reporter: bool = False

    def __init__(self):
        super().__init__()
        renpy.config.stdout_callbacks.append(self.stdout_callback)

    def stdout_callback(self, text: str) -> None:
        """
        Callback to handle stdout messages.
        This may be triggered by Ren'Py's internal logging or the user.
        """
        self._is_last_line_written_by_reporter = False

    def _erase_line(self) -> bool:
        """Erases the current line in the console if supported, and returns True if successful."""
        if can_erase := (
            isinstance(self.epc, renpy.error.ANSIColoredPrintContext) and self._is_last_line_written_by_reporter
        ):
            ## Move cursor up one line and erase it
            self._print("\x1b[1A\x1b[2K", end="\r")

        return can_erase

    def _print(self, text: str, end: str = "\n") -> None:
        if not isinstance(self.epc, renpy.error.ANSIColoredPrintContext):
            ## Remove ANSI color codes for non-colored output
            for value in ANSIColors.__dict__.values():
                if isinstance(value, str) and value.startswith("\x1b["):
                    text = text.replace(value, "")

        print(text, end=end)
        self._is_last_line_written_by_reporter = True

    def _format_with_status_color(self, msg: str, status: OutcomeStatus | None) -> str:
        """
        Formats the status of a test case with appropriate color.
        """
        if status == OutcomeStatus.PASSED:
            return f"{ANSIColors.GREEN}{msg}{ANSIColors.RESET}"
        elif status == OutcomeStatus.XFAILED:
            return f"{ANSIColors.MAGENTA}{msg}{ANSIColors.RESET}"
        elif status == OutcomeStatus.FAILED:
            return f"{ANSIColors.RED}{msg}{ANSIColors.RESET}"
        elif status == OutcomeStatus.XPASSED:
            return f"{ANSIColors.RED}{msg}{ANSIColors.RESET}"
        elif status == OutcomeStatus.PENDING:
            return f"{ANSIColors.CYAN}{msg}{ANSIColors.RESET}"
        elif status in [OutcomeStatus.SKIPPED, OutcomeStatus.NOT_RUN]:
            return f"{ANSIColors.YELLOW}{msg}{ANSIColors.RESET}"
        else:
            return msg

    def _get_status_text(self, status: OutcomeStatus) -> str:
        """
        Returns a colored status string based on the success of the test case.
        """
        text = status.name.upper().replace("_", " ").ljust(7)
        return self._format_with_status_color(text, status)

    def _print_detailed_outcome(self, outcome: BaseOutcome, depth=-1) -> None:
        """
        Prints all outcomes in a tree-like structure.
        """

        if depth == -1:
            self._print(f"{ANSIColors.CYAN}[rpytest]{ANSIColors.RESET} Test outcomes (Detailed)")

        if outcome.status == OutcomeStatus.SKIPPED and not _test.report.report_skipped:
            return

        test_name = outcome.name
        status_text = self._get_status_text(outcome.status)

        if isinstance(outcome, OutcomeManager):
            for child in outcome.children:
                self._print_detailed_outcome(child, depth + 1)

        elif isinstance(outcome, TestSuiteOutcome):
            self._print(
                f"{ANSIColors.CYAN}[rpytest]{ANSIColors.RESET} "
                + "  " * (depth)
                + f"{status_text} {test_name:20s}"
                + (f" - ({format_seconds(outcome.duration)})" if outcome.duration > 0 else "")
            )

            for child in outcome.children:
                self._print_detailed_outcome(child, depth + 1)

        elif isinstance(outcome, TestCaseOutcome):
            self._print(
                f"{ANSIColors.CYAN}[rpytest]{ANSIColors.RESET} "
                + "  " * (depth)
                + f"{status_text} {test_name:20s}"
                + (f" - ({format_seconds(outcome.duration)})" if outcome.duration > 0 else "")
            )

        if depth == -1:
            self._print("")
            self._print("=" * 20)
            self._print("")

    def _print_summarized_outcomes(self, outcome: OutcomeManager) -> None:
        self._print(f"{ANSIColors.CYAN}[rpytest]{ANSIColors.RESET} Test outcomes (Summary)")

        self._print(
            f"{ANSIColors.CYAN}[rpytest]{ANSIColors.RESET} "
            f"Test suites: {outcome.num_testsuites:5d} | "
            f"{ANSIColors.GREEN if outcome.num_testsuites_passed else ANSIColors.RESET}"
            f"{outcome.num_testsuites_passed:5d} passed{ANSIColors.RESET} | "
            f"{ANSIColors.MAGENTA if outcome.num_testsuites_xfailed else ANSIColors.RESET}"
            f"{outcome.num_testsuites_xfailed:5d} xfailed{ANSIColors.RESET} | "
            f"{ANSIColors.RED if outcome.num_testsuites_failed else ANSIColors.RESET}"
            f"{outcome.num_testsuites_failed:5d} failed{ANSIColors.RESET} | "
            f"{ANSIColors.RED if outcome.num_testsuites_xpassed else ANSIColors.RESET}"
            f"{outcome.num_testsuites_xpassed:5d} xpassed{ANSIColors.RESET} | "
            f"{ANSIColors.YELLOW if outcome.num_testsuites_skipped else ANSIColors.RESET}"
            f"{outcome.num_testsuites_skipped:5d} skipped{ANSIColors.RESET} | "
            f"{ANSIColors.YELLOW if outcome.num_testsuites_not_run else ANSIColors.RESET}"
            f"{outcome.num_testsuites_not_run:5d} not run{ANSIColors.RESET}"
        )

        self._print(
            f"{ANSIColors.CYAN}[rpytest]{ANSIColors.RESET} "
            f"Test cases : {outcome.num_testcases:5d} | "
            f"{ANSIColors.GREEN if outcome.num_testcases_passed else ANSIColors.RESET}"
            f"{outcome.num_testcases_passed:5d} passed{ANSIColors.RESET} | "
            f"{ANSIColors.MAGENTA if outcome.num_testcases_xfailed else ANSIColors.RESET}"
            f"{outcome.num_testcases_xfailed:5d} xfailed{ANSIColors.RESET} | "
            f"{ANSIColors.RED if outcome.num_testcases_failed else ANSIColors.RESET}"
            f"{outcome.num_testcases_failed:5d} failed{ANSIColors.RESET} | "
            f"{ANSIColors.RED if outcome.num_testcases_xpassed else ANSIColors.RESET}"
            f"{outcome.num_testcases_xpassed:5d} xpassed{ANSIColors.RESET} | "
            f"{ANSIColors.YELLOW if outcome.num_testcases_skipped else ANSIColors.RESET}"
            f"{outcome.num_testcases_skipped:5d} skipped{ANSIColors.RESET} | "
            f"{ANSIColors.YELLOW if outcome.num_testcases_not_run else ANSIColors.RESET}"
            f"{outcome.num_testcases_not_run:5d} not run{ANSIColors.RESET}"
        )

        self._print(
            f"{ANSIColors.CYAN}[rpytest]{ANSIColors.RESET} "
            f"Test hooks : {outcome.num_hooks:5d} | "
            f"{ANSIColors.GREEN if outcome.num_hooks_passed else ANSIColors.RESET}"
            f"{outcome.num_hooks_passed:5d} passed{ANSIColors.RESET} | "
            f"{ANSIColors.MAGENTA if outcome.num_hooks_xfailed else ANSIColors.RESET}"
            f"{outcome.num_hooks_xfailed:5d} xfailed{ANSIColors.RESET} | "
            f"{ANSIColors.RED if outcome.num_hooks_failed else ANSIColors.RESET}"
            f"{outcome.num_hooks_failed:5d} failed{ANSIColors.RESET} | "
            f"{ANSIColors.RED if outcome.num_hooks_xpassed else ANSIColors.RESET}"
            f"{outcome.num_hooks_xpassed:5d} xpassed{ANSIColors.RESET} | "
            f"{ANSIColors.YELLOW if outcome.num_hooks_skipped else ANSIColors.RESET}"
            f"{outcome.num_hooks_skipped:5d} skipped{ANSIColors.RESET} | "
            f"{ANSIColors.YELLOW if outcome.num_hooks_not_run else ANSIColors.RESET}"
            f"{outcome.num_hooks_not_run:5d} not run{ANSIColors.RESET}"
        )

        self._print(
            f"{ANSIColors.CYAN}[rpytest]{ANSIColors.RESET} "
            f"Assertions : {outcome.num_asserts:5d} | "
            f"{ANSIColors.GREEN if outcome.num_asserts_passed else ANSIColors.RESET}"
            f"{outcome.num_asserts_passed:5d} passed{ANSIColors.RESET} | "
            f"{ANSIColors.MAGENTA if outcome.num_asserts_xfailed else ANSIColors.RESET}"
            f"{outcome.num_asserts_xfailed:5d} xfailed{ANSIColors.RESET} | "
            f"{ANSIColors.RED if outcome.num_asserts_failed else ANSIColors.RESET}"
            f"{outcome.num_asserts_failed:5d} failed{ANSIColors.RESET} | "
            f"{ANSIColors.RED if outcome.num_asserts_xpassed else ANSIColors.RESET}"
            f"{outcome.num_asserts_xpassed:5d} xpassed{ANSIColors.RESET} | "
        )

        self._print("")
        self._print(f"{ANSIColors.CYAN}[rpytest]{ANSIColors.RESET} Time: {format_seconds(outcome.duration)}")
        self._print(f"{ANSIColors.CYAN}[rpytest]{ANSIColors.RESET} Status: {self._get_status_text(outcome.status)}")

    ##################################
    ## Reporter Interface Methods
    ##################################

    def test_run_start(self, outcomes) -> None:
        if _test.report.hide_header:
            return

        self._print("")
        self._print(f"{ANSIColors.CYAN}[rpytest]{ANSIColors.RESET} Starting test run")
        self._print(f"{ANSIColors.CYAN}[rpytest]{ANSIColors.RESET} Platform:      {platform.platform()}")
        self._print(f"{ANSIColors.CYAN}[rpytest]{ANSIColors.RESET} Python:        {platform.python_version()}")
        self._print(f"{ANSIColors.CYAN}[rpytest]{ANSIColors.RESET} Ren'Py:        {renpy.version}")
        self._print(f"{ANSIColors.CYAN}[rpytest]{ANSIColors.RESET} Game Version:  {renpy.store.config.version}")
        self._print("")

    def test_run_end(self, outcomes) -> None:
        self._print("")

        if _test.report.report_detailed:
            self._print_detailed_outcome(outcomes)

        if not _test.report.hide_summary:
            self._print_summarized_outcomes(outcomes)
            self._print("")

    def test_suite_start(self, outcome, depth=0) -> None:
        if _test.report.hide_execution == "all":
            return

        self._print(f"{ANSIColors.CYAN}[rpytest] [exc]{ANSIColors.RESET} {'  ' * depth}+ {outcome.name}")

    def test_suite_end(self, outcome, depth=0) -> None:
        pass

    def test_case_start(self, outcome, depth=0) -> None:
        if _test.report.hide_execution in ("all", "testcases"):
            return

        self._print(f"{ANSIColors.CYAN}[rpytest] [exc]{ANSIColors.RESET} {'  ' * depth}- {outcome.name}")

    def test_case_end(self, outcome, depth=0) -> None:
        if _test.report.hide_execution in ("all", "testcases"):
            return

        self._erase_line()
        self._print(
            f"{ANSIColors.CYAN}[rpytest] [exc]{ANSIColors.RESET} {'  ' * depth}- "
            f"{self._format_with_status_color(outcome.name, outcome.status)} ({format_seconds(outcome.duration)})"
        )

    def test_hook_start(self, outcome, depth=0) -> None:
        if _test.report.hide_execution in ("all", "testcases", "hooks"):
            return

        self._print(f"{ANSIColors.CYAN}[rpytest] [exc]{ANSIColors.RESET} {'  ' * depth}  {outcome.full_path}")

    def test_hook_end(self, outcome, depth=0) -> None:
        if _test.report.hide_execution in ("all", "testcases", "hooks"):
            return

        self._erase_line()
        self._print(
            f"{ANSIColors.CYAN}[rpytest] [exc]{ANSIColors.RESET} {'  ' * depth}  "
            f"{self._format_with_status_color(outcome.full_path, outcome.status)} ({format_seconds(outcome.duration)})"
        )

    def test_case_skipped(self, outcome, depth=0) -> None:
        pass

    def log_assert(self, assert_node, status, node_name="") -> None:
        if status in (OutcomeStatus.PASSED, OutcomeStatus.XFAILED):
            return

        if msg := get_assertion_error_string(self.epc, assert_node, node_name):
            self._print(msg)

    def log_exception(self, exception, run_stack, xfailed) -> None:
        if xfailed:
            return

        msg = get_exception_string(self.epc, exception, run_stack)

        self._print(msg)
        self._print("=" * 20)

    def log_message(self, message) -> None:
        self._print(f"{ANSIColors.CYAN}[rpytest] [log]{ANSIColors.RESET} {message}")

    def on_reload(self):
        self._is_last_line_written_by_reporter = False


class ReporterManager:
    """
    A manager that forwards calls to all registered reporters.
    """

    reporters: list["Reporter"] = []

    outcome_manager: OutcomeManager | None = None
    "A TestSuiteOutcome object that contains the outcomes of all testcases to be executed."

    suites: list[TestSuite] = []
    testcase: TestCase | None = None
    hook: TestHook | None = None

    def initialize_test_outcomes(self, suite: TestSuite) -> None:
        self.outcome_manager = OutcomeManager(suite)

    @property
    def has_failed(self) -> bool:
        return self.outcome_manager is not None and (
            self.outcome_manager.status == OutcomeStatus.FAILED or self.outcome_manager.status == OutcomeStatus.XPASSED
        )

    def add_reporter(self, reporter: Reporter) -> None:
        self.reporters.append(reporter)

    def test_run_start(self) -> None:
        if self.outcome_manager is None:
            raise RuntimeError("Called before initializing test outcomes.")
        self.outcome_manager.begin()

        for reporter in self.reporters:
            reporter.test_run_start(self.outcome_manager)

    def test_run_end(self) -> None:
        if self.outcome_manager is None:
            raise RuntimeError("Called before initializing test outcomes.")
        self.outcome_manager.end()

        for reporter in self.reporters:
            reporter.test_run_end(self.outcome_manager)

    def test_suite_start(self, suite: TestSuite, depth: int = 0) -> None:
        self.suites.append(suite)
        self.testcase = None
        self.hook = None

        outcome = self.outcome_manager.get_outcome_by_test_block(suite)
        assert isinstance(outcome, TestSuiteOutcome)
        outcome.begin()

        for reporter in self.reporters:
            reporter.test_suite_start(outcome, depth=depth)

    def test_suite_end(self, suite: TestSuite, status: OutcomeStatus | None = None, depth: int = 0) -> None:
        removed = self.suites.pop()
        if removed != suite:
            raise RuntimeError("Mismatched test suite start/end calls.")
        self.testcase = None
        self.hook = None

        outcome = self.outcome_manager.get_outcome_by_test_block(suite)
        assert isinstance(outcome, TestSuiteOutcome)
        outcome.end(status)

        for reporter in self.reporters:
            reporter.test_suite_end(outcome, depth=depth)

    def test_case_start(self, test_case: TestCase, depth: int = 0) -> None:
        self.testcase = test_case
        self.hook = None

        outcome = self.outcome_manager.get_outcome_by_test_block(test_case)
        assert isinstance(outcome, TestCaseOutcome)
        outcome.begin()

        for reporter in self.reporters:
            reporter.test_case_start(outcome, depth)

    def test_case_end(self, test_case: TestCase, status: OutcomeStatus | None = None, depth: int = 0) -> None:
        self.testcase = None
        self.hook = None

        outcome = self.outcome_manager.get_outcome_by_test_block(test_case)
        assert isinstance(outcome, TestCaseOutcome)
        outcome.end(status)

        for reporter in self.reporters:
            reporter.test_case_end(outcome, depth)

    def test_hook_start(self, hook: TestHook, depth: int = 0) -> None:
        self.testcase = None
        self.hook = hook

        outcome = self.outcome_manager.get_outcome_by_test_block(hook)
        assert isinstance(outcome, TestHookOutcome)
        outcome.begin()

        for reporter in self.reporters:
            reporter.test_hook_start(outcome, depth=depth)

    def test_hook_end(self, hook: TestHook, status=None, depth: int = 0) -> None:
        self.testcase = None
        self.hook = None

        outcome = self.outcome_manager.get_outcome_by_test_block(hook)
        assert isinstance(outcome, TestHookOutcome)
        outcome.end(status)

        for reporter in self.reporters:
            reporter.test_hook_end(outcome, depth=depth)

    def test_case_skipped(self, test_case: TestCase, depth: int = 0) -> None:
        outcome = self.outcome_manager.get_outcome_by_test_block(test_case)
        assert isinstance(outcome, TestCaseOutcome)
        outcome.end(OutcomeStatus.SKIPPED)

        for reporter in self.reporters:
            reporter.test_case_skipped(outcome, depth=depth)

    def log_assert(self, assert_node: Assert) -> None:
        outcome = self._get_current_outcomes()
        outcome.num_asserts += 1

        status = self._determine_assert_status(assert_node, outcome)
        self._update_assert_counters(outcome, status)

        test_block = self._current_test_block()
        for reporter in self.reporters:
            reporter.log_assert(assert_node, status, test_block.current_full_parameterized_path)

        if status in (OutcomeStatus.FAILED, OutcomeStatus.XPASSED):
            raise RenpyTestAssertionError(f"{status.value}: {assert_node}")

    def _determine_assert_status(self, assert_node: Assert, outcome: BaseOutcome) -> OutcomeStatus:
        """Determine the outcome status for an assertion."""
        is_expected_failure = outcome.test_block.xfail if outcome.test_block else False
        is_true = assert_node.is_assertion_true

        if assert_node.xfail:
            return OutcomeStatus.XPASSED if is_true else OutcomeStatus.XFAILED
        elif is_expected_failure and not is_true:
            return OutcomeStatus.XFAILED
        else:
            return OutcomeStatus.PASSED if is_true else OutcomeStatus.FAILED

    def _update_assert_counters(self, outcome: BaseOutcome, status: OutcomeStatus) -> None:
        """Update assertion counters based on status."""
        if status == OutcomeStatus.PASSED:
            outcome.num_asserts_passed += 1
        elif status == OutcomeStatus.XFAILED:
            outcome.num_asserts_xfailed += 1
        elif status == OutcomeStatus.FAILED:
            outcome.num_asserts_failed += 1
        elif status == OutcomeStatus.XPASSED:
            outcome.num_asserts_xpassed += 1

    def log_exception(
        self, exception: Exception, run_stack: list[renpy.error.FrameSummary], xfailed: bool = False
    ) -> None:
        file = io.StringIO()
        epc = renpy.error.NonColoredExceptionPrintContext(file)
        outcome = self._get_current_outcomes()
        msg = get_exception_string(epc, exception, run_stack)
        outcome.exception = msg

        for reporter in self.reporters:
            reporter.log_exception(exception, run_stack, xfailed)

    def log_message(self, message: str) -> None:
        for reporter in self.reporters:
            reporter.log_message(message)

    def on_reload(self) -> None:
        for reporter in self.reporters:
            reporter.on_reload()

    def _current_test_block(self) -> BaseTestBlock:
        if self.hook is not None:
            return self.hook
        elif self.testcase is not None:
            return self.testcase
        elif self.suites:
            return self.suites[-1]
        else:
            raise RuntimeError("No current test case, hook, or suite to end outcomes for.")

    def _get_current_outcomes(self) -> BaseOutcome:
        if self.outcome_manager is None:
            raise RuntimeError("Called before initializing test outcomes.")

        return self.outcome_manager.get_outcome_by_test_block(self._current_test_block())


reporter = ReporterManager()
