# Copyright 2004-2025 Tom Rothamel <pytom@bishoujo.us>
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


class RenpyTestTimeoutError(TimeoutError):
    pass


class HookType(enum.Enum):
    AFTER = "after"
    AFTER_EACH_CASE = "after_each_case"
    AFTER_EACH_SUITE = "after_each_suite"
    BEFORE = "before"
    BEFORE_EACH_CASE = "before_each_case"
    BEFORE_EACH_SUITE = "before_each_suite"
