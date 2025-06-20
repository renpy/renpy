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

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode  # *


import renpy
import renpy.pygame as pygame

from renpy.test.testast import Node, TestSuite, TestCase
from renpy.test.types import State, NodeLocation, RenpyTestTimeoutError
from renpy.test.testsettings import _test

initialized: bool = False

# A map from the name of a testcase to the testcase.
testcases: dict[str, TestCase] = {}

# An action to run before executing another command.
action: Node | None = None

# The set of labels that have been reached since the last time execute
# has been called.
labels: set[str] = set()

# A stack of text contexts, which tracks the execution of testcases.
context_stack: list["TestCaseContext"] = []
context_stack: list["TestSuiteContext"] = []

def take_name(name: str) -> None:
    """
    Takes the name of a statement that is about to run.
    """

    if len(context_stack) == 0:
        return

    if isinstance(name, str):
        labels.add(name)


def add_testcase(name: str, node: TestCase) -> None:
    """
    Adds a testcase to the `testcases` dictionary. The name is a tuple of strings,
    and the node is the root node of the testcase.
    """

    if name in testcases:
        raise KeyError("Testcase {} already exists.".format(name))

    if isinstance(node, TestSuite):
        for child in node.children:
            add_testcase(child.name, child)

    testcases[name] = node


def lookup(name: str, from_node: Node | None = None) -> TestCase:
    """
    Tries to look up the name with `target`. If found, returns it, otherwise
    raises an exception.
    """

    if name in testcases:
        return testcases[name]

    if from_node is None:
        raise KeyError("Testcase {} not found.".format(name))
    raise KeyError("Testcase {} not found at {}:{}.".format(name, from_node.filename, from_node.linenumber))


def initialize(name: str) -> None:
    """
    Initializes the test execution system. This is called when the game starts, and
    sets up the testcases and the context stack.
    """

    global initialized
    global testcases
    global context_stack

    if initialized:
        return


    root = lookup(name)

    ## Chain the nodes in the testcases
    for case in testcases.values():
        case.chain(None)


    # If the root is a TestCase, we create a TestSuite with it as the only child.
    if not isinstance(root, TestSuite):
        suite = TestSuite(name="", loc=(root.filename, root.linenumber), children=[root])
    else:
        suite = root

    push_context_stack(suite)

    initialized = True


def push_context_stack(node: str | TestSuite) -> None:
    global context_stack

    if isinstance(node, str):
        case = lookup(node)
        if not isinstance(case, TestSuite):
            loc: NodeLocation = (case.filename, case.linenumber)
            node = TestSuite(name="", loc=loc, children=[case])
        else:
            node = case

    tc = TestSuiteContext(node)
    context_stack.append(tc)



def pop_context_stack() -> "TestSuiteContext":
    """
    Pops the last call node from the stack and returns it.
    Pops the last context from the stack and returns it.
    """

    global context_stack

    if not context_stack:
        raise Exception("No context on context stack.")

    rv = context_stack.pop()

        ## Executing a subcase may artificially lengthen the time between state changes,
        ## so we update the value of last_state_change here
        ctx.last_state_change = renpy.display.core.get_time()

    renpy.test.testmouse.reset()

    return rv


def get_current_context() -> "TestSuiteContext":
    """
    Returns the current context, or raises an exception if there is no context.
    """

    global context_stack

    if len(context_stack) == 0:
        raise Exception("No context on context stack.")

    return context_stack[-1]


def set_next_node(next: Node | None) -> None:
    """
    Sets the next node to execute. This is used to change the flow of execution
    to a different node.
    """

    get_current_context().next_node = next


def is_in_test() -> bool:
    return len(context_stack) > 0


def execute() -> None:
    """
    Called periodically by the core interact loop when a new frame is drawn.
    This allows test code to generate events, if desired.
    """

    global context_stack
    global action
    global labels

    if len(context_stack) == 0:
        return

    if renpy.display.interface.suppress_underlay and (not _test.force):
        return

    if _test.maximum_framerate:
        renpy.exports.maximum_framerate(10.0)
    else:
        renpy.exports.maximum_framerate(None)

    # Make sure there are no test events in the event queue.
    for e in pygame.event.copy_event_queue():
        if getattr(e, "test", False):
            return

    if action:
        old_action = action
        action = None
        renpy.display.behavior.run(old_action)

    try:
        get_current_context().execute()
    except renpy.game.QuitException:
        while context_stack:
            pop_context_stack()
        raise

    labels.clear()


def exception_handler(exc: renpy.error.TracebackException) -> bool:
    """
    Handles exceptions that occur during the execution of testcases.
    This is called by Ren'Py when an exception is raised.
    """

    get_current_context().handle_exception(None)
    return True


class TestSuiteContext:
    """
    A context manager for testcases. This is used to set the current node and state
    when entering a testcase, and to reset them when exiting.
    """

    testsuite: TestSuite
    """The testcase being executed."""



    node: Node | None = None
    """Current node being executed."""

    state: State | None = None
    """The state of the current node being executed."""

    start_time: float = 0.0
    """The time the current node started executing."""

    has_started: bool = False
    """Whether the current node has run the start() method."""

    next_node: Node | None = None
    """The next node to execute after the current one."""

    old_state: State | None = None
    """The previous state of the current node."""

    old_loc: NodeLocation | None = None
    """The previous location in the game script of the current node."""

    last_state_change: float = 0.0
    """The last time the state changed."""


    def __init__(self, node: TestSuite):
        self.testsuite = node

        self.testcase_index = 0
        self.ran_before = self.testsuite.before is None
        self.ran_after = self.testsuite.after is None

        self.prepare_for_next_testcase()


    def prepare_for_next_testcase(self) -> None:
        self.ran_before_each = self.testsuite.before_each is None
        self.ran_testcase = len(self.testsuite.children) == 0
        self.ran_after_each = self.testsuite.after_each is None


    def execute(self) -> None:
        now = renpy.display.core.get_time()

        try:
            ## Before
            if not self.ran_before and self.testsuite.before:
                if self.node is None:
                    self.node = self.testsuite.before

                self.execute_node(now)
                self.ran_before = self.node is None

            ## Before Each
            elif not self.ran_before_each and self.testsuite.before_each:
                if self.node is None:
                    self.node = self.testsuite.before_each

                self.execute_node(now)
                self.ran_before_each = self.node is None

            ## Test Case
            elif not self.ran_testcase and self.testsuite.children:
                if self.node is None:
                    new_case = self.testsuite.children[self.testcase_index]

                    ctx = get_current_context()

                    if new_case.skip:
                        self.testcase_index += 1

                        return

                    self.node = new_case

                    if isinstance(self.node, TestSuite):
                        push_context_stack(self.node)

                if not isinstance(self.node, TestSuite):
                    self.execute_node(now)

                self.ran_testcase = self.node is None

            ## After Each
            elif not self.ran_after_each and self.testsuite.after_each:
                if self.node is None:
                    self.node = self.testsuite.after_each

                self.execute_node(now)
                self.ran_after_each = self.node is None

            elif self.testcase_index < len(self.testsuite.children) - 1:
                self.testcase_index += 1
                self.prepare_for_next_testcase()

            ## After
            elif not self.ran_after and self.testsuite.after:
                if self.node is None:
                    self.node = self.testsuite.after

                self.execute_node(now)
                self.ran_after = self.node is None

            ## Done with the testsuite
            else:
                pop_context_stack()
                return

        except renpy.game.QuitException:
            raise

        except Exception as exc:
            self.handle_exception(exc)
            return

        loc = renpy.exports.get_filename_line()

        if (self.old_state != self.state) or (self.old_loc != loc):
            self.last_state_change = now

        self.old_state = self.state
        self.old_loc = loc

        if (now - self.last_state_change) > _test.timeout:
            exc = RenpyTestTimeoutError("Testcase timed out after {} seconds.".format(_test.timeout))
            self.handle_exception(exc)
            return


    def execute_node(self, now: float) -> None:
        """
        Performs one execution cycle of a node.
        """

        if not self.has_started:
            if self.node.ready():
                # If the node is ready, we start it.
                self.state = self.node.start()
                self.start = now
                self.has_started = True
            else:
                self.state = None
                self.has_started = False
                return

        self.state = self.node.execute(self.state, now - self.start)

        ## If the current state is None, move to the next node
        if self.state is None:
            self.node = self.next_node
            self.has_started = False


    def handle_exception(self, exc: Exception | None) -> None:
        ctx = get_current_context()

        if self.ran_before and self.ran_before_each and not self.ran_testcase:
            ## If the exception happened in a testcase, move to the next one.
            self.ran_testcase = True

        else:
            pop_context_stack()


def test_command() -> bool:
    """
    The dialogue command. This updates dialogue.txt, a file giving all the dialogue
    in the game.
    """

    ap = renpy.arguments.ArgumentParser(description="Runs a testcase.")
    ap.add_argument("testcase", help="The name of a testcase to run.", nargs="?", default="default")

    args = ap.parse_args()

    ## NOTE: This command gets called when the game starts for the first time, OR when the game
    ## goes back to the main menu after finishing the game. Special care is taken to avoid
    ## messing up the state of the test/call stack
    initialize(args.testcase)

    return True


renpy.arguments.register_command("test", test_command, uses_display=True)
