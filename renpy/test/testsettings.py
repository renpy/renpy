from renpy.object import Object

class TestSettings(Object):
    def __init__(self):

        # Should we use maximum framerate mode?
        self.maximum_framerate: bool = True

        # How long should we wait before declaring the test stuck?
        self.timeout: float = 5.0

        # Should we force the test to proceed despite suppress_underlay?
        self.force: bool = False

        # How long should we wait for a transition before we proceed?
        self.transition_timeout: float = 5.0

        # How many times should we try to find a good spot to place the mouse?
        self.focus_trials: int = 100

        # Should we ignore the skip flag when executing test scripts?
        self.ignore_skip_flag: bool = False

        # Should we print skipped test cases?
        self.print_skipped: bool = False

_test = TestSettings()
