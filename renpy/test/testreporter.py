import abc
from dataclasses import dataclass, field
from enum import Enum
import io
import os
import contextlib

import renpy
from renpy.error import ANSIColors
from renpy.test.testsettings import _test
from renpy.test.types import RenpyTestAssertionError
from renpy.test.testast import TestCase, TestHook, TestSuite, Assert, Block

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
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class BaseOutcome:
    name: str = ""
    num_asserts: int = 0
    num_asserts_passed: int = 0
    num_asserts_failed: int = 0
    start_time: float = field(default=0.0, repr=False)
    end_time: float = field(default=0.0, repr=False)
    duration: float = 0.0
    status: OutcomeStatus = field(default=OutcomeStatus.NOT_RUN, repr=False)
    final_status: OutcomeStatus = OutcomeStatus.NOT_RUN
    exception: str = ""

    def begin(self) -> None:
        self.start_time = renpy.display.core.get_time()
        self.end_time = 0.0
        self.status = OutcomeStatus.PENDING

    def end(self, status: OutcomeStatus | None) -> None:
        """
        Finalize the test case outcomes.

        If status is None, it will be set to PASSED if no asserts failed,
        otherwise it is set to FAILED.
        """
        if self.end_time > 0.0:
            return # Already ended

        now = renpy.display.core.get_time()
        if self.start_time == 0.0:
            self.start_time = now

        self.end_time = now
        self.duration = self.end_time - self.start_time

        if status is not None:
            self.status = status

        elif self.status == OutcomeStatus.PENDING:
            if self.num_asserts_failed > 0:
                self.status = OutcomeStatus.FAILED
            else:
                self.status = OutcomeStatus.PASSED


@dataclass
class TestHookOutcome(BaseOutcome):
    num_runs_passed: int = 0
    num_runs_failed: int = 0
    num_runs_skipped: int = 0

    def end(self, status: OutcomeStatus | None) -> None:
        super().end(status)

        if self.status == OutcomeStatus.PASSED:
            self.num_runs_passed += 1
        elif self.status == OutcomeStatus.FAILED:
            self.num_runs_failed += 1
        elif self.status == OutcomeStatus.SKIPPED:
            self.num_runs_skipped += 1

        if self.num_runs_failed > 0:
            self.final_status = OutcomeStatus.FAILED
        elif self.num_runs_passed > 0 and self.num_runs_failed == 0:
            self.final_status = OutcomeStatus.PASSED
        elif self.num_runs_skipped > 0 and self.num_runs_passed == 0:
            self.final_status = OutcomeStatus.SKIPPED


@dataclass
class TestCaseOutcome(BaseOutcome):
    def end(self, status: OutcomeStatus | None) -> None:
        super().end(status)
        self.final_status = self.status


@dataclass
class TestSuiteOutcome(TestCaseOutcome):
    num_testsuites: int = 0
    num_testsuites_passed: int = 0
    num_testsuites_failed: int = 0
    num_testsuites_skipped: int = 0

    num_testcases: int = 0
    num_testcases_passed: int = 0
    num_testcases_failed: int = 0
    num_testcases_skipped: int = 0

    num_hooks: int = 0
    num_hooks_passed: int = 0
    num_hooks_failed: int = 0
    num_hooks_skipped: int = 0

    children: list["BaseOutcome"] = field(default_factory=list, repr=False)

    @property
    def num_testsuites_not_run(self) -> int:
        return (self.num_testsuites - self.num_testsuites_passed
            - self.num_testsuites_failed - self.num_testsuites_skipped)

    @property
    def num_testcases_not_run(self) -> int:
        return (self.num_testcases - self.num_testcases_passed
            - self.num_testcases_failed - self.num_testcases_skipped)

    @property
    def num_hooks_not_run(self) -> int:
        return (self.num_hooks - self.num_hooks_passed
            - self.num_hooks_failed - self.num_hooks_skipped)

    def populate_children(self, node: TestSuite) -> None:
        for hook in node.hooks:
            self.children.append(TestHookOutcome(hook.name))

        for child in node.subtests:
            if isinstance(child, TestSuite):
                r = TestSuiteOutcome(child.name)
                r.populate_children(child)
                self.children.append(r)

            elif isinstance(child, TestCase):
                self.children.append(TestCaseOutcome(child.name))

    def end(self, status = None) -> None:
        """
        Finalize the test suite outcomes.

        If status is None, it will be set to PASSED if all test cases passed,
        FAILED if any test case failed, or SKIPPED if all test cases were skipped.
        """

        if self.end_time > 0.0:
            return # Already ended

        now = renpy.display.core.get_time()
        if self.start_time == 0.0:
            self.start_time = now

        self.end_time = now
        self.duration = self.end_time - self.start_time

        for child in self.children:
            self.num_asserts += child.num_asserts
            self.num_asserts_passed += child.num_asserts_passed
            self.num_asserts_failed += child.num_asserts_failed

            if isinstance(child, TestSuiteOutcome):
                self.num_testsuites += child.num_testsuites + 1
                self.num_testsuites_passed += child.num_testsuites_passed
                self.num_testsuites_failed += child.num_testsuites_failed
                self.num_testsuites_skipped += child.num_testsuites_skipped

                self.num_testcases += child.num_testcases
                self.num_testcases_passed += child.num_testcases_passed
                self.num_testcases_failed += child.num_testcases_failed
                self.num_testcases_skipped += child.num_testcases_skipped

                if child.status == OutcomeStatus.PASSED:
                    self.num_testsuites_passed += 1
                elif child.status == OutcomeStatus.FAILED:
                    self.num_testsuites_failed += 1
                elif child.status == OutcomeStatus.SKIPPED:
                    self.num_testsuites_skipped += 1

            elif isinstance(child, TestCaseOutcome):
                self.num_testcases += 1
                if child.status == OutcomeStatus.PASSED:
                    self.num_testcases_passed += 1
                elif child.status == OutcomeStatus.FAILED:
                    self.num_testcases_failed += 1
                elif child.status == OutcomeStatus.SKIPPED:
                    self.num_testcases_skipped += 1

            elif isinstance(child, TestHookOutcome):
                self.num_hooks += 1
                if child.status == OutcomeStatus.PASSED:
                    self.num_hooks_passed += 1
                elif child.status == OutcomeStatus.FAILED:
                    self.num_hooks_failed += 1
                elif child.status == OutcomeStatus.SKIPPED:
                    self.num_hooks_skipped += 1


        if status is not None:
            self.status = status

        elif self.status == OutcomeStatus.PENDING:
            if self.num_testcases_failed > 0 or self.num_asserts_failed > 0:
                self.status = OutcomeStatus.FAILED
            elif self.num_testcases_skipped == self.num_testcases:
                self.status = OutcomeStatus.SKIPPED
            else:
                self.status = OutcomeStatus.PASSED

        self.final_status = self.status

    def get_outcome_by_name(self, name: str) -> BaseOutcome:
        if name == self.name:
            return self

        def _flatten_test_suite_outcomes(outcomes: TestSuiteOutcome) -> dict[str, "BaseOutcome"]:
            rv = {}
            for child in outcomes.children:
                rv[child.name] = child
                if isinstance(child, TestSuiteOutcome):
                    rv.update(_flatten_test_suite_outcomes(child))
            return rv

        # rv = _recursive_search(self)
        outcomes = _flatten_test_suite_outcomes(self)
        if rv := outcomes.get(name, None):
            return rv

        raise ValueError(f"outcomes for '{name}' not found in {self.name}. "
                         f"Available names: {list(outcomes.keys())}")


def get_exception_string(
        epc: renpy.error.ExceptionPrintContext,
        exception: Exception,
        run_stack: list[renpy.error.FrameSummary]
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


def get_assertion_error_string(
        epc: renpy.error.ExceptionPrintContext,
        assert_node: Assert,
        block_name: str
    ) -> str:

    if not assert_node.failed:
        return ""

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

        epc.location(filename, assert_node.linenumber, block_name)
        epc.final_exception_line("AssertionError", expr)
        # self._print(f"{ANSIColors.RED}FAILED:{ANSIColors.RESET} {expr}\n")

    if force_color:
        del os.environ["FORCE_COLOR"]

    return string_stream.getvalue()


class Reporter(abc.ABC):
    """
    Base class for reporters that handle reporting of test outcomes.
    """

    def __init__(self):
        self.epc: renpy.error.ExceptionPrintContext = renpy.error.MaybeColoredExceptionPrintContext()

    def test_run_start(self) -> None:
        """Called when the entire test run starts."""
        pass

    def test_run_end(self, outcomes: TestSuiteOutcome) -> None:
        """Called when the entire test run ends."""
        pass

    def test_suite_start(self, node: TestSuite, depth: int = 0) -> None:
        """Called when a test suite starts."""
        pass

    def test_suite_end(self, node: TestSuite, outcome: TestSuiteOutcome, depth: int = 0) -> None:
        """Called when a test suite ends."""
        pass

    def test_case_start(self, node: TestCase, depth: int = 0) -> None:
        """Called when a test case starts."""
        pass

    def test_case_end(self, node: TestCase, outcome: TestCaseOutcome, depth: int = 0) -> None:
        """Called when a test case ends."""
        pass

    def test_hook_start(self, node: TestHook, depth: int = 0) -> None:
        """Called when a test hook starts."""
        pass

    def test_hook_end(self, node: TestHook, outcome: TestHookOutcome, depth: int = 0) -> None:
        """Called when a test hook ends."""
        pass

    def test_case_skipped(self, node: TestCase, depth: int = 0) -> None:
        """Called when a test case is skipped."""
        pass

    def log_assert(self, assert_node: Assert, block_name: str = "") -> None:
        """Called for each assert in the test case, even if it did not fail."""
        pass

    def log_exception(self, exception: Exception, run_stack: list[renpy.error.FrameSummary]) -> None:
        """
        Called when an exception is raised from the test case or the game
        raises an error.
        """
        pass

    def log_message(self, message: str) -> None:
        """Called when a message should be logged."""
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
            isinstance(self.epc, renpy.error.ANSIColoredPrintContext)
            and self._is_last_line_written_by_reporter
        ):
            ## Move cursor up one line and erase it
            self._print(f"\x1b[1A\x1b[2K", end="\r")

        return can_erase

    def _print(self, text: str, end: str = "\n") -> None:
        if not isinstance(self.epc, renpy.error.ANSIColoredPrintContext):
            ## Remove ANSI color codes for non-colored output
            for value in ANSIColors.__dict__.values():
                if isinstance(value, str) and value.startswith("\x1b["):
                    text = text.replace(value, "")

        print(text, end=end)
        self._is_last_line_written_by_reporter = True


    def _format_with_status_color(self, msg: str, status: OutcomeStatus|None) -> str:
        """
        Formats the status of a test case with appropriate color.
        """
        if status == OutcomeStatus.PASSED:
            return f"{ANSIColors.GREEN}{msg}{ANSIColors.RESET}"
        elif status == OutcomeStatus.FAILED:
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

    def _print_detailed_outcomes(self, outcome: BaseOutcome, depth=0) -> None:
        """
        Prints all outcomes in a tree-like structure.
        """

        if depth == 0:
            self._print(f"{ANSIColors.CYAN}[rpytest]{ANSIColors.RESET} Test outcomes (Detailed)")

        if (outcome.status == OutcomeStatus.SKIPPED and not _test.print_skipped):
            return

        test_name = outcome.name.split(".")[-1]
        status_text = self._get_status_text(outcome.final_status)

        if isinstance(outcome, TestSuiteOutcome):
            self._print(
                f"{ANSIColors.CYAN}[rpytest]{ANSIColors.RESET} " +
                "  " * (depth) +
                f"{status_text} {test_name:20s}" +
                (f" - ({format_seconds(outcome.duration)})" if outcome.duration > 0 else "")
            )

            for child in outcome.children:
                self._print_detailed_outcomes(child, depth+1)

        elif isinstance(outcome, TestCaseOutcome):
            self._print(
                f"{ANSIColors.CYAN}[rpytest]{ANSIColors.RESET} " +
                "  " * (depth) +
                f"{status_text} {test_name:20s}" +
                (f" - ({format_seconds(outcome.duration)})" if outcome.duration > 0 else "")
            )

        if depth == 0:
            self._print("")
            self._print("=" * 20)
            self._print("")

    def _print_summarized_outcomes(self, outcome: TestSuiteOutcome) -> None:
        if outcome.name == renpy.test.testexecution.isolated_testsuite_name:
            top_name = outcome.children[0].name
        else:
            top_name = outcome.name

        self._print(
            f"{ANSIColors.CYAN}[rpytest]{ANSIColors.RESET} "
            f"Test outcomes (Summary): {top_name}"
        )

        self._print(
            f"{ANSIColors.CYAN}[rpytest]{ANSIColors.RESET} "
            f"Test suites: {outcome.num_testsuites:5d} | "

            f"{ANSIColors.GREEN if outcome.num_testsuites_passed else ANSIColors.RESET}"
            f"{outcome.num_testsuites_passed:5d} passed{ANSIColors.RESET} | "

            f"{ANSIColors.RED if outcome.num_testsuites_failed else ANSIColors.RESET}"
            f"{outcome.num_testsuites_failed:5d} failed{ANSIColors.RESET} | "

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

            f"{ANSIColors.RED if outcome.num_testcases_failed else ANSIColors.RESET}"
            f"{outcome.num_testcases_failed:5d} failed{ANSIColors.RESET} | "

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

            f"{ANSIColors.RED if outcome.num_hooks_failed else ANSIColors.RESET}"
            f"{outcome.num_hooks_failed:5d} failed{ANSIColors.RESET} | "

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

            f"{ANSIColors.RED if outcome.num_asserts_failed else ANSIColors.RESET}"
            f"{outcome.num_asserts_failed:5d} failed{ANSIColors.RESET} | "
        )

        self._print("")
        self._print(f"{ANSIColors.CYAN}[rpytest]{ANSIColors.RESET} Time: {format_seconds(outcome.duration)}")
        self._print(
            f"{ANSIColors.CYAN}[rpytest]{ANSIColors.RESET} "
            f"Status: {self._get_status_text(outcome.final_status)}"
        )

    ##################################
    ## Reporter Interface Methods
    ##################################

    def test_run_start(self) -> None:
        self._print("")
        self._print(f"{ANSIColors.CYAN}[rpytest]{ANSIColors.RESET} Starting test run")
        self._print(f"{ANSIColors.CYAN}[rpytest]{ANSIColors.RESET} Ren'Py Version:   {renpy.version}")
        self._print(f"{ANSIColors.CYAN}[rpytest]{ANSIColors.RESET} Game Version:     {renpy.store.config.version}")
        self._print("")

    def test_run_end(self, outcomes) -> None:
        self._print("")
        if _test.print_details:
            self._print_detailed_outcomes(outcomes)
        self._print_summarized_outcomes(outcomes)
        self._print("")

    def test_suite_start(self, node, depth=0) -> None:
        self._print(f"{ANSIColors.CYAN}[rpytest] [exc]{ANSIColors.RESET} {'  '*depth}+ {node.name}")

    def test_suite_end(self, node, outcome, depth=0) -> None:
        pass
        # self._print(f"{ANSIColors.CYAN}[rpytest] [exc]{ANSIColors.RESET} {node.name} done")

    def test_case_start(self, node, depth=0) -> None:
        self._print(f"{ANSIColors.CYAN}[rpytest] [exc]{ANSIColors.RESET} {'  '*depth}- {node.name}")

    def test_case_end(self, node, outcome, depth=0) -> None:
        self._erase_line()
        self._print(
            f"{ANSIColors.CYAN}[rpytest] [exc]{ANSIColors.RESET} {'  '*depth}- "
            f"{self._format_with_status_color(node.name, outcome.status)} ({format_seconds(outcome.duration)})"
        )

    def test_hook_start(self, node, depth=0) -> None:
        self._print(f"{ANSIColors.CYAN}[rpytest] [exc]{ANSIColors.RESET} {'  '*depth}  {node.name}")

    def test_hook_end(self, node, outcome, depth=0) -> None:
        self._erase_line()
        self._print(
            f"{ANSIColors.CYAN}[rpytest] [exc]{ANSIColors.RESET} {'  '*depth}  "
            f"{self._format_with_status_color(node.name, outcome.status)} ({format_seconds(outcome.duration)})"
        )

    def test_case_skipped(self, node, depth=0) -> None:
        pass

    def log_assert(self, assert_node, block_name = "") -> None:
        if msg := get_assertion_error_string(self.epc, assert_node, block_name):
            self._print(msg)

    def log_exception(self, exception, run_stack) -> None:
        msg = get_exception_string(self.epc, exception, run_stack)

        self._print(msg)
        self._print("=" * 20)

    def log_message(self, message) -> None:
        self._print(f"Message: {message}")


class ReporterManager:
    """
    A manager that forwards calls to all registered reporters.
    """
    reporters: list["Reporter"] = []

    all_outcomes: TestSuiteOutcome | None = None
    "A TestSuiteoutcomes object that contains the outcomes of all testcases to be executed."

    suites: list[TestSuite] = []
    testcase: TestCase | None = None
    hook: TestHook | None = None

    def initialize_test_outcomes(self, suite: TestSuite) -> None:
        self.all_outcomes = TestSuiteOutcome(suite.name)
        self.all_outcomes.populate_children(suite)

    @property
    def has_failed(self) -> bool:
        return (self.all_outcomes is not None and
                self.all_outcomes.final_status == OutcomeStatus.FAILED)

    def add_reporter(self, reporter: Reporter) -> None:
        self.reporters.append(reporter)

    def test_run_start(self) -> None:
        for reporter in self.reporters:
            reporter.test_run_start()

    def test_run_end(self) -> None:
        if self.all_outcomes is None:
            raise RuntimeError("Called before initializing test outcomes.")

        for reporter in self.reporters:
            reporter.test_run_end(self.all_outcomes)

    def test_suite_start(self, node: TestSuite, depth: int = 0) -> None:
        self.suites.append(node)
        self.testcase = None
        self.hook = None

        outcome = self.all_outcomes.get_outcome_by_name(node.name)
        outcome.begin()

        for reporter in self.reporters:
            reporter.test_suite_start(node, depth=depth)

    def test_suite_end(self, node: TestSuite, status: OutcomeStatus|None = None, depth: int = 0) -> None:
        removed = self.suites.pop()
        if removed != node:
            raise RuntimeError("Mismatched test suite start/end calls.")
        self.testcase = None
        self.hook = None

        outcome = self.all_outcomes.get_outcome_by_name(node.name)
        assert isinstance(outcome, TestSuiteOutcome)
        outcome.end(status)

        for reporter in self.reporters:
            reporter.test_suite_end(node, outcome, depth=depth)

    def test_case_start(self, node: TestCase, depth: int = 0) -> None:
        self.testcase = node
        self.hook = None

        outcome = self.all_outcomes.get_outcome_by_name(node.name)
        outcome.begin()

        for reporter in self.reporters:
            reporter.test_case_start(node, depth)

    def test_case_end(self, node: TestCase, status: OutcomeStatus|None = None, depth: int = 0) -> None:
        self.testcase = None
        self.hook = None

        outcome = self.all_outcomes.get_outcome_by_name(node.name)
        assert isinstance(outcome, TestCaseOutcome)
        outcome.end(status)

        for reporter in self.reporters:
            reporter.test_case_end(node, outcome, depth)

    def test_hook_start(self, node: TestHook, depth: int = 0) -> None:
        self.testcase = None
        self.hook = node

        outcome = self.all_outcomes.get_outcome_by_name(node.name)
        outcome.begin()

        for reporter in self.reporters:
            reporter.test_hook_start(node, depth=depth)

    def test_hook_end(self, node: TestHook, status = None, depth: int = 0) -> None:
        self.testcase = None
        self.hook = None

        outcome = self.all_outcomes.get_outcome_by_name(node.name)
        assert isinstance(outcome, TestHookOutcome)
        outcome.end(status)

        for reporter in self.reporters:
            reporter.test_hook_end(node, outcome, depth=depth)

    def test_case_skipped(self, node: TestCase, depth: int = 0) -> None:
        outcome = self.all_outcomes.get_outcome_by_name(node.name)
        outcome.end(OutcomeStatus.SKIPPED)

        for reporter in self.reporters:
            reporter.test_case_skipped(node, depth=depth)

    def log_assert(self, assert_node) -> None:
        outcome = self._get_current_outcomes()
        outcome.num_asserts += 1

        if assert_node.failed:
            outcome.num_asserts_failed += 1
            raise RenpyTestAssertionError(f"Assertion failed: {assert_node}")
        else:
            outcome.num_asserts_passed += 1

        block_name = self._current_block_name()
        for reporter in self.reporters:
            reporter.log_assert(assert_node, block_name)

    def log_exception(self, exception, run_stack) -> None:
        file = io.StringIO()
        epc = renpy.error.NonColoredExceptionPrintContext(file)
        outcome = self._get_current_outcomes()
        msg = get_exception_string(epc, exception, run_stack)
        outcome.exception = msg

        for reporter in self.reporters:
            reporter.log_exception(exception, run_stack)

    def log_message(self, message: str) -> None:
        for reporter in self.reporters:
            reporter.log_message(message)

    def _current_block_name(self) -> str:
        if self.hook is not None:
            return self.hook.name
        elif self.testcase is not None:
            return self.testcase.name
        elif self.suites:
            return self.suites[-1].name
        else:
            raise RuntimeError("No current test case, hook, or suite to end outcomes for.")

    def _get_current_outcomes(self) -> BaseOutcome:
        if self.all_outcomes is None:
            raise RuntimeError("Called before initializing test outcomes.")

        return self.all_outcomes.get_outcome_by_name(self._current_block_name())


reporter = ReporterManager()
