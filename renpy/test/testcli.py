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

from renpy.arguments import ArgumentParser, register_command
from renpy.test import testexecution, testreporter
from renpy.test.testexecution import setup_global_test_suite
from renpy.test.testfilter import ExecutionFilter
from renpy.test.testsettings import _test, global_testsuite_name


def test_command() -> bool:
    """
    Command handler for the "test" command, which runs a specified test case or suite.
    """

    ## NOTE: This command gets called after the game finishes and returns to the main menu
    if testexecution.initialized:
        return True

    ap = ArgumentParser(description="Run a Ren'Py test case or suite.")

    ap.add_argument(
        "filters",
        help=f"Test filters to use (default: {global_testsuite_name}).",
        nargs="*",
        type=str,
        default=[],
    )

    group = ap.add_argument_group(title="Test Execution")
    group.add_argument(
        "--enable-all",
        dest="_test.enable_all",
        action="store_true",
        default=False,
        help="Run all test cases and test suites, even if they are disabled. "
        "Does not work if a specific test case or suite is specified.",
    )
    group.add_argument(
        "--overwrite-screenshots",
        dest="_test.overwrite_screenshots",
        action="store_true",
        default=False,
        help="Replace existing screenshots when a screenshot is taken during tests.",
    )

    group = ap.add_argument_group(title="Console Reporting")
    group.add_argument(
        "--hide-header",
        dest="_test.report.hide_header",
        action="store_true",
        default=False,
        help="Disable header at start of run",
    )
    group.add_argument(
        "--hide-execution",
        dest="_test.report.hide_execution",
        action="store",
        choices=["no", "hooks", "testcases", "all"],
        default="hooks",
        help="Hide test execution output. "
            "'hooks' hides hooks, 'testcases' hides test cases and hooks, "
            "and 'all' hides everything including test suites.",
    )
    group.add_argument(
        "--hide-summary",
        dest="_test.report.hide_summary",
        action="store_true",
        default=False,
        help="Disable summary",
    )
    group.add_argument(
        "--report-detailed",
        dest="_test.report.report_detailed",
        action="store_true",
        default=False,
        help="Show detailed information about each test during the run.",
    )
    group.add_argument(
        "--report-skipped",
        dest="_test.report.report_skipped",
        action="store_true",
        default=False,
        help="Show information about skipped tests (use with --report-detailed).",
    )

    args = ap.parse_args()

    for key, value in vars(args).items():
        key_parts = key.split(".")

        if key_parts[0] != "_test":
            continue
        obj = _test

        for part in key_parts[1:-1]:
            obj = getattr(obj, part)

        if hasattr(obj, key_parts[-1]):
            setattr(obj, key_parts[-1], value)
        else:
            raise AttributeError(f"Unknown test setting: {key}")

    testreporter.reporter.add_reporter(testreporter.ConsoleReporter())

    setup_global_test_suite()
    include_filters = args.filters
    run_plan = ExecutionFilter(include_filters)
    testexecution.initialize(run_plan)

    return True


register_command("test", test_command, uses_display=True)
