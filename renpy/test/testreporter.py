import abc
from dataclasses import dataclass, field
from enum import Enum

import renpy
from renpy.error import ANSIColors
from renpy.test.testsettings import _test

class TestCaseStatus(Enum):
    NOT_RUN = "not_run"
    PENDING = "pending"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"

@dataclass
class TestCaseResults:
    name: str = ""
    num_asserts: int = 0
    num_asserts_passed: int = 0
    num_asserts_failed: int = 0
    start_time: float = field(default=0.0, repr=False)
    end_time: float = field(default=0.0, repr=False)
    seconds: float = 0.0
    status: TestCaseStatus = TestCaseStatus.NOT_RUN

    def begin(self) -> None:
        self.start_time = renpy.display.core.get_time()
        self.status = TestCaseStatus.PENDING

    def end(self, status: TestCaseStatus | None) -> None:
        """
        Finalize the test case results.

        If status is None, it will be set to PASSED if no asserts failed,
        otherwise it is set to FAILED.
        """
        if self.end_time > 0.0:
            return # Already ended

        now = renpy.display.core.get_time()
        if self.start_time == 0.0:
            self.start_time = now

        self.end_time = now
        self.seconds = self.end_time - self.start_time

        if status is not None:
            self.status = status

        elif self.status == TestCaseStatus.PENDING:
            if self.num_asserts_failed > 0:
                self.status = TestCaseStatus.FAILED
            else:
                self.status = TestCaseStatus.PASSED


@dataclass
class TestSuiteResults(TestCaseResults):
    num_testsuites: int = 0
    num_testsuites_passed: int = 0
    num_testsuites_failed: int = 0
    num_testsuites_skipped: int = 0
    num_testcases: int = 0
    num_testcases_passed: int = 0
    num_testcases_failed: int = 0
    num_testcases_skipped: int = 0
    children: list["TestSuiteResults | TestCaseResults"] = field(default_factory=list, repr=False)

    @property
    def num_testsuites_not_run(self) -> int:
        return (self.num_testsuites - self.num_testsuites_passed
            - self.num_testsuites_failed - self.num_testsuites_skipped)

    @ property
    def num_testcases_not_run(self) -> int:
        return (self.num_testcases - self.num_testcases_passed
            - self.num_testcases_failed - self.num_testcases_skipped)

    def populate_children(self, node: renpy.test.testast.TestSuite) -> None:
        for child in node.testcases:
            if isinstance(child, renpy.test.testast.TestSuite):
                r = TestSuiteResults(child.name)
                r.populate_children(child)
                self.children.append(r)
            elif isinstance(child, renpy.test.testast.TestCase):
                self.children.append(TestCaseResults(child.name))

    def end(self, status = None) -> None:
        """
        Finalize the test suite results.

        If status is None, it will be set to PASSED if all test cases passed,
        FAILED if any test case failed, or SKIPPED if all test cases were skipped.
        """

        if self.end_time > 0.0:
            return # Already ended

        now = renpy.display.core.get_time()
        if self.start_time == 0.0:
            self.start_time = now

        self.end_time = now
        self.seconds = self.end_time - self.start_time

        for child in self.children:
            self.num_asserts += child.num_asserts
            self.num_asserts_passed += child.num_asserts_passed
            self.num_asserts_failed += child.num_asserts_failed

            if isinstance(child, TestSuiteResults):
                self.num_testsuites += child.num_testsuites + 1
                self.num_testsuites_passed += child.num_testsuites_passed
                self.num_testsuites_failed += child.num_testsuites_failed
                self.num_testsuites_skipped += child.num_testsuites_skipped
                if child.status == TestCaseStatus.PASSED:
                    self.num_testsuites_passed += 1
                elif child.status == TestCaseStatus.FAILED:
                    self.num_testsuites_failed += 1
                elif child.status == TestCaseStatus.SKIPPED:
                    self.num_testsuites_skipped += 1
                self.num_testcases += child.num_testcases
                self.num_testcases_passed += child.num_testcases_passed
                self.num_testcases_failed += child.num_testcases_failed
                self.num_testcases_skipped += child.num_testcases_skipped
            else:
                self.num_testcases += 1
                if child.status == TestCaseStatus.PASSED:
                    self.num_testcases_passed += 1
                elif child.status == TestCaseStatus.FAILED:
                    self.num_testcases_failed += 1
                elif child.status == TestCaseStatus.SKIPPED:
                    self.num_testcases_skipped += 1

        if status is not None:
            self.status = status

        elif self.status == TestCaseStatus.PENDING:
            if self.num_testcases_failed > 0 or self.num_asserts_failed > 0:
                self.status = TestCaseStatus.FAILED
            elif self.num_testcases_skipped == self.num_testcases:
                self.status = TestCaseStatus.SKIPPED
            else:
                self.status = TestCaseStatus.PASSED

    def get_result_by_name(self, name: str) -> TestCaseResults:
        if name == self.name:
            return self

        def _recursive_search(results: TestSuiteResults) -> "TestCaseResults | None":
            for child in results.children:
                if isinstance(child, TestCaseResults) and child.name == name:
                    return child
                elif isinstance(child, TestSuiteResults):
                    result = _recursive_search(child)
                    if result is not None:
                        return result
            return None

        rv = _recursive_search(self)
        if rv is not None:
            return rv

        raise ValueError(f"Results for '{name}' not found in {self.name}. "
                         f"Available names: {[c.name for c in self.children]}")


class Reporter(abc.ABC):
    """
    Base class for reporters that handle reporting of test results.
    """
    context: renpy.test.testast.TestSuite

    @abc.abstractmethod
    def test_run_start(self) -> None:
        """Called when the entire test run starts."""
        pass

    @abc.abstractmethod
    def test_run_end(self, results: TestSuiteResults) -> None:
        """Called when the entire test run ends."""
        pass

    @abc.abstractmethod
    def test_suite_start(self, node: renpy.test.testast.TestSuite) -> None:
        """Called when a test suite starts."""
        pass

    @abc.abstractmethod
    def test_suite_end(self, results: TestSuiteResults) -> None:
        """Called when a test suite ends."""
        pass

    @abc.abstractmethod
    def test_case_start(self, node: renpy.test.testast.TestCase) -> None:
        """Called when a test case starts."""
        pass

    @abc.abstractmethod
    def test_case_end(self, results: TestCaseResults) -> None:
        """Called when a test case ends."""
        pass

    @abc.abstractmethod
    def test_case_skipped(self, node: renpy.test.testast.TestCase) -> None:
        """Called when a test case is skipped."""
        pass

    @abc.abstractmethod
    def log_assert(self, node: renpy.test.testast.Assert) -> None:
        """Called for each assert in the test case, even if it did not fail."""
        pass

    @abc.abstractmethod
    def log_exception(self, exception: Exception, run_stack: list[renpy.error.FrameSummary]) -> None:
        """
        Called when an exception is raised from the test case or the game
        raises an error.
        """
        pass

    @abc.abstractmethod
    def log_message(self, message: str) -> None:
        """Called when a message should be logged."""
        pass

class ConsoleReporter(Reporter):
    """
    Reporter that prints test results to the console.
    """

    def __init__(self):
        self.testcase_depth = 0
        self.epc: renpy.error.ExceptionPrintContext = renpy.error.MaybeColoredExceptionPrintContext()
        self.colored = isinstance(self.epc, renpy.error.ANSIColoredPrintContext)

    def _print(self, text: str):
        if not self.colored:
            ## Remove ANSI color codes for non-colored output
            for color, value in ANSIColors.__dict__.items():
                if isinstance(value, str) and value.startswith("\x1b["):
                    text = text.replace(value, "")

        print(text)

    def _format_with_status_color(self, test: str, status: TestCaseStatus) -> str:
        """
        Formats the status of a test case with appropriate color.
        """
        if status == TestCaseStatus.PASSED:
            return f"{ANSIColors.GREEN}{test}{ANSIColors.RESET}"
        elif status == TestCaseStatus.FAILED:
            return f"{ANSIColors.RED}{test}{ANSIColors.RESET}"
        elif status == TestCaseStatus.PENDING:
            return f"{ANSIColors.CYAN}{test}{ANSIColors.RESET}"
        elif status in [TestCaseStatus.SKIPPED, TestCaseStatus.NOT_RUN]:
            return f"{ANSIColors.YELLOW}{test}{ANSIColors.RESET}"
        else:
            return test

    def _get_status_text(self, status: TestCaseStatus) -> str:
        """
        Returns a colored status string based on the success of the test case.
        """
        text = status.name.upper().replace("_", " ").ljust(7)
        return self._format_with_status_color(text, status)

    def _print_detailed_results(self, results: TestCaseResults, depth=0) -> None:
        """
        Prints all results in a tree-like structure.
        """

        if depth == 0:
            self._print(f"{ANSIColors.CYAN}[rpytest]{ANSIColors.RESET} Test Results (Detailed)")

        if (results.status == TestCaseStatus.SKIPPED and not _test.print_skipped):
            return

        test_name = results.name.split(".")[-1]
        status_text = self._get_status_text(results.status)

        if isinstance(results, TestSuiteResults):
            self._print(
                f"{ANSIColors.CYAN}[rpytest]{ANSIColors.RESET} " +
                "  " * (depth) +
                f"{status_text} {test_name:20s}" +
                (f" - ({results.seconds:0.3f} s)" if results.seconds > 0 else "")
            )

            for child in results.children:
                self._print_detailed_results(child, depth+1)

        else:
            self._print(
                f"{ANSIColors.CYAN}[rpytest]{ANSIColors.RESET} " +
                "  " * (depth) +
                f"{status_text} {test_name:20s}" +
                (f" - ({results.seconds:0.3f} s)" if results.seconds > 0 else "")
            )

        if depth == 0:
            self._print("=" * 20)

    def _print_summarized_results(self, results: TestSuiteResults) -> None:
        if results.name == renpy.test.testexecution.isolated_testsuite_name:
            top_name = results.children[0].name
        else:
            top_name = results.name

        self._print(
            f"{ANSIColors.CYAN}[rpytest]{ANSIColors.RESET} "
            f"Test Results (Summary): {top_name}"
        )

        self._print(
            f"{ANSIColors.CYAN}[rpytest]{ANSIColors.RESET} "
            f"Test suites: {results.num_testsuites:5d} | "

            f"{ANSIColors.GREEN if results.num_testsuites_passed else ANSIColors.RESET}"
            f"{results.num_testsuites_passed:5d} passed{ANSIColors.RESET} | "

            f"{ANSIColors.RED if results.num_testsuites_failed else ANSIColors.RESET}"
            f"{results.num_testsuites_failed:5d} failed{ANSIColors.RESET} | "

            f"{ANSIColors.YELLOW if results.num_testsuites_skipped else ANSIColors.RESET}"
            f"{results.num_testsuites_skipped:5d} skipped{ANSIColors.RESET} | "

            f"{ANSIColors.YELLOW if results.num_testsuites_not_run else ANSIColors.RESET}"
            f"{results.num_testsuites_not_run:5d} not run{ANSIColors.RESET}"
        )

        self._print(
            f"{ANSIColors.CYAN}[rpytest]{ANSIColors.RESET} "
            f"Test cases : {results.num_testcases:5d} | "

            f"{ANSIColors.GREEN if results.num_testcases_passed else ANSIColors.RESET}"
            f"{results.num_testcases_passed:5d} passed{ANSIColors.RESET} | "

            f"{ANSIColors.RED if results.num_testcases_failed else ANSIColors.RESET}"
            f"{results.num_testcases_failed:5d} failed{ANSIColors.RESET} | "

            f"{ANSIColors.YELLOW if results.num_testcases_skipped else ANSIColors.RESET}"
            f"{results.num_testcases_skipped:5d} skipped{ANSIColors.RESET} | "

            f"{ANSIColors.YELLOW if results.num_testcases_not_run else ANSIColors.RESET}"
            f"{results.num_testcases_not_run:5d} not run{ANSIColors.RESET}"
        )

        self._print(
            f"{ANSIColors.CYAN}[rpytest]{ANSIColors.RESET} "
            f"Assertions : {results.num_asserts:5d} | "

            f"{ANSIColors.GREEN if results.num_asserts_passed else ANSIColors.RESET}"
            f"{results.num_asserts_passed:5d} passed{ANSIColors.RESET} | "

            f"{ANSIColors.RED if results.num_asserts_failed else ANSIColors.RESET}"
            f"{results.num_asserts_failed:5d} failed{ANSIColors.RESET} | "
        )

        self._print(f"{ANSIColors.CYAN}[rpytest]{ANSIColors.RESET} Time: {results.seconds:0.6f} s")
        self._print(
            f"{ANSIColors.CYAN}[rpytest]{ANSIColors.RESET} "
            f"Status: {self._get_status_text(results.status)}"
        )

    ##################################
    ## Reporter Interface Methods
    ##################################

    def test_run_start(self) -> None:
        self._print(f"{ANSIColors.CYAN}[rpytest]{ANSIColors.RESET} Starting test run")

    def test_run_end(self, results) -> None:
        if _test.print_details:
            self._print_detailed_results(results)
        self._print_summarized_results(results)

    def test_suite_start(self, node) -> None:
        self.context = node
        self.testcase_depth += 1

    def test_suite_end(self, results) -> None:
        self.testcase_depth -= 1

    def test_case_start(self, node) -> None:
        self.testcase_depth += 1

    def test_case_end(self, results) -> None:
        self.testcase_depth -= 1

    def test_case_skipped(self, node) -> None:
        pass

    def log_assert(self, node) -> None:
        if not node.failed:
            return

        expr = str(node.condition)

        filename = renpy.exports.unelide_filename(node.filename)
        lines = renpy.lexer.list_logical_lines(filename)
        for fname, line_num, line in lines:
            if line_num == node.linenumber:
                expr = line.strip()
                break

        self.epc.location(filename, node.linenumber, self.context.name)
        self._print(f"{ANSIColors.RED}FAILED:{ANSIColors.RESET} {expr}\n")

    def log_exception(self, exception, run_stack) -> None:
        renpy.error.report_exception(exception, editor=False)

        ## Report where in the script this exception occurred
        ctx = renpy.game.context()
        frames = ctx.report_traceback("", last=False)
        for filename, line_number, name, text in frames:
            summary = renpy.error.FrameSummary(name, filename, line_number, text=text)
            filename = renpy.exports.unelide_filename(filename)

            self.epc.location(filename, line_number, name)
            self.epc.string("  " + summary.line.strip())

        self.epc.indent_depth = 0
        self.epc.string("\nDuring testcase execution:")

        self.epc.indent_depth = 1

        for frame in run_stack:
            filename = renpy.exports.unelide_filename(frame.filename)
            self.epc.location(filename, frame.lineno, frame.name)
            self.epc.string("  " + frame.line.strip())

        self._print("=" * 20)

    def log_message(self, message) -> None:
        self._print(f"Message: {message}")


class ReporterManager(Reporter):
    """
    A manager that forwards calls to all registered reporters.
    """
    reporters: list["Reporter"] = []

    def register(self, reporter: Reporter) -> None:
        self.reporters.append(reporter)

    def test_run_start(self) -> None:
        for reporter in self.reporters:
            reporter.test_run_start()

    def test_run_end(self, results) -> None:
        for reporter in self.reporters:
            reporter.test_run_end(results)

    def test_suite_start(self, node) -> None:
        for reporter in self.reporters:
            reporter.test_suite_start(node)

    def test_suite_end(self, results) -> None:
        for reporter in self.reporters:
            reporter.test_suite_end(results)

    def test_case_start(self, node) -> None:
        for reporter in self.reporters:
            reporter.test_case_start(node)

    def test_case_end(self, results) -> None:
        for reporter in self.reporters:
            reporter.test_case_end(results)

    def test_case_skipped(self, node) -> None:
        for reporter in self.reporters:
            reporter.test_case_skipped(node)

    def log_assert(self, node) -> None:
        for reporter in self.reporters:
            reporter.log_assert(node)

    def log_exception(self, exception, run_stack) -> None:
        for reporter in self.reporters:
            reporter.log_exception(exception, run_stack)

    def log_message(self, message: str) -> None:
        for reporter in self.reporters:
            reporter.log_message(message)

reporter = ReporterManager()
