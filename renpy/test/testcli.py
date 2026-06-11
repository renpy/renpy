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

import os

from renpy.arguments import ArgumentParser, register_command
from renpy.test import testexecution, testreporter
from renpy.test.testexecution import setup_global_test_suite
from renpy.test.testfilter import ExecutionFilter
from renpy.test.testsettings import _test, global_testsuite_name

def get_tmp_dir() -> str:
    """
    Makes the project's temporary directory, if it doesn't exist yet.

    Inspired by the launcher's make_tmp() function
    """

    project_dir_name = os.path.split(renpy.config.basedir)[-1]
    tmp = os.path.join(renpy.config.renpy_base, "tmp", project_dir_name)

    os.makedirs(tmp, exist_ok=True)

    return tmp


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

    group = ap.add_argument_group(title="Result Reporting")
    group.add_argument(
        "--reporter",
        dest="reporter_names",
        action="store",
        default="console",
        help="Comma-separated list of reporters to enable. Supported values: console, jsonl.",
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

    group = ap.add_argument_group(title="Console Reporting")
    group.add_argument(
        "--hide-header",
        dest="_test.report.hide_header",
        action="store_true",
        default=False,
        help="Disable header at start of run",
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
    group.add_argument(
        "--report-not-run",
        dest="_test.report.report_notrun",
        action="store_true",
        default=False,
        help="Show information about tests that were not run (use with --report-detailed).",
    )

    group = ap.add_argument_group(title="JSONL Reporting")
    group.add_argument(
        "--jsonl-output",
        dest="jsonl_test_report_output",
        action="store",
        default="",
        help="Output path for jsonl reporter (default: renpy-sdk/tmp/<project_name>/test_results.jsonl).",
    )
    group.add_argument(
        "--jsonl-initial-test-info",
        dest="jsonl_initial_test_info",
        action="store_true",
        default=False,
        help="Emit detailed information about each test at the start of the run.",
    )
    group.add_argument(
        "--jsonl-batch-size",
        dest="jsonl_batch_size",
        action="store",
        type=int,
        default=50,
        help="jsonl batch size before flush (default: 50).",
    )
    group.add_argument(
        "--jsonl-flush-interval-ms",
        dest="jsonl_flush_interval_ms",
        action="store",
        type=int,
        default=1000,
        help="jsonl max flush interval in milliseconds (default: 1000).",
    )
    group.add_argument(
        "--jsonl-heartbeat-interval-ms",
        dest="jsonl_heartbeat_interval_ms",
        action="store",
        type=int,
        default=1000,
        help="jsonl heartbeat interval in milliseconds (default: 1000).",
    )
    group.add_argument(
        "--jsonl-run-id",
        dest="jsonl_run_id",
        action="store",
        default="",
        help="Optional run id included in jsonl events.",
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

    reporter_names = [r.strip().lower() for r in args.reporter_names.split(",") if r.strip()]

    reporters = []
    for reporter_name in reporter_names:
        if reporter_name == "console":
            reporters.append(testreporter.ConsoleReporter())
        elif reporter_name == "jsonl":
            if args.jsonl_batch_size <= 0:
                ap.error("--jsonl-batch-size must be > 0.")
            if args.jsonl_flush_interval_ms <= 0:
                ap.error("--jsonl-flush-interval-ms must be > 0.")
            if args.jsonl_heartbeat_interval_ms <= 0:
                ap.error("--jsonl-heartbeat-interval-ms must be > 0.")

            jsonl_output_path = args.jsonl_test_report_output
            if not jsonl_output_path:
                jsonl_output_path = os.path.join(get_tmp_dir(), "test_results.jsonl")

            reporters.append(
                testreporter.JsonlStreamReporter(
                    jsonl_output_path,
                    run_id=args.jsonl_run_id or None,
                    batch_size=args.jsonl_batch_size,
                    flush_interval_ms=args.jsonl_flush_interval_ms,
                    heartbeat_interval_ms=args.jsonl_heartbeat_interval_ms,
                    emit_info_on_run_start=args.jsonl_initial_test_info,
                )
            )
        else:
            ap.error(
                f"Unknown reporter: {reporter_name}. Supported values are 'console', 'jsonl'."
            )

    if not reporters:
        ap.error("No reporters configured. Use --reporter with 'console', 'jsonl', or any combination.")

    testreporter.reporter.clear_reporters()
    for rep in reporters:
        testreporter.reporter.add_reporter(rep)


    setup_global_test_suite()
    include_filters = args.filters
    run_plan = ExecutionFilter(include_filters)
    testexecution.initialize(run_plan)

    return True


register_command("test", test_command, uses_display=True)
