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

    ignore_skip_flag: bool = False
    """Should we ignore the skip flag when executing test scripts?"""

    print_details: bool = False
    """Should we print details about the test cases?"""

    print_skipped: bool = False
    """Should we print skipped test cases?"""


_test = TestSettings()
