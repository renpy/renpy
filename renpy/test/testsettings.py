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

from dataclasses import dataclass


@dataclass
class TestSettings:
    maximum_framerate: bool = True
    """Should we use maximum framerate mode?"""

    timeout: float = 5.0
    """How long should we wait before declaring the test stuck?"""

    force: bool = False
    """Should we force the test to proceed despite suppress_underlay?"""

    transition_timeout: float = 5.0
    """How long should we wait for a transition before we proceed?"""

    focus_trials: int = 100
    """How many times should we try to find a good spot to place the mouse?"""

    ignore_enabled_flag: bool = False
    """Should we ignore the enabled flag when executing test scripts?"""

    print_details: bool = False
    """Should we print details about the test cases?"""

    print_skipped: bool = False
    """Should we print skipped test cases?"""


_test = TestSettings()
