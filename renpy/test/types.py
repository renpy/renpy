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

import enum
from typing import TypeAlias, Any

NodeState: TypeAlias = Any
NodeLocation: TypeAlias = tuple[str, int]
Position: TypeAlias = tuple[int | float, int | float]


class RenpyTestException(RuntimeError):
    pass


class RenpyTestAssertionError(AssertionError):
    pass


class RenpyTestScreenshotError(RenpyTestException):
    pass


class RenpyTestTimeoutError(TimeoutError):
    pass


class HookType(enum.Enum):
    SETUP = "setup"
    BEFORE_TESTSUITE = "before_testsuite"
    BEFORE_TESTCASE = "before_testcase"
    AFTER_TESTCASE = "after_testcase"
    AFTER_TESTSUITE = "after_testsuite"
    TEARDOWN = "teardown"
