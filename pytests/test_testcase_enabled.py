import unittest
from unittest.mock import patch

import renpy
from unittests.renpy_test_support import initialize_renpy

initialize_renpy()

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


class TestEnabledExpression(unittest.TestCase):
    """
    The `enabled` property is compiled into the .rpyc, so it must be evaluated
    when tests are run rather than when the script is parsed. Otherwise a
    result that depends on the platform or on game files would be stale.
    """

    def evaluate(self, tests, **store):
        """
        Evaluates the enabled expressions of `tests` with `store` as the
        contents of the game store.
        """

        with (
            patch.dict(testexecution.testcases, {t.name: t for t in tests}, clear=True),
            patch.dict(renpy.python.store_dicts["store"], store),
        ):
            testexecution.evaluate_enabled_expressions()

    def test_parse_does_not_evaluate_the_expression(self):
        # The name is undefined when parsing, so evaluating it would fail.
        suite = parse_suite()

        self.assertEqual(suite.enabled_expr, "enabled_probe_flag")
        self.assertTrue(suite.enabled)

    def test_evaluation_uses_the_store_when_run(self):
        suite = parse_suite()
        inner, plain = suite.subtests

        self.evaluate([suite, inner, plain], enabled_probe_flag=False)
        self.assertEqual((suite.enabled, inner.enabled, plain.enabled), (False, True, True))

        # The same parsed objects follow a later change, as a cached .rpyc would.
        self.evaluate([suite, inner, plain], enabled_probe_flag=True)
        self.assertEqual((suite.enabled, inner.enabled, plain.enabled), (True, False, True))

    def test_tests_without_an_expression_keep_their_flag(self):
        # Objects unpickled from an older .rpyc have no enabled_expr slot.
        suite = parse_suite()
        suite.enabled = False
        del suite.enabled_expr

        self.evaluate([suite], enabled_probe_flag=True)
        self.assertFalse(suite.enabled)

    def test_only_requires_the_test_to_be_enabled(self):
        suite = parse_suite(
            SCRIPT.replace("    enabled enabled_probe_flag\n", "    only True\n    enabled enabled_probe_flag\n")
        )

        with self.assertRaises(ValueError):
            self.evaluate([suite], enabled_probe_flag=False)


if __name__ == "__main__":
    unittest.main()
