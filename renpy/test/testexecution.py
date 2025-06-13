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

from renpy.test.testast import Node, TestcaseException
from renpy.test.types import State, NodeLocation

# A map from the name of a testcase to the testcase.
testcases: dict[str, Node] = {}

# The root node.
node: Node | None = None
# The state of the root node.
state: State = None

# The next node to execute.
next_node: Node | None = None

# The previous state and location in the game script.
old_state: State | None = None
old_loc: NodeLocation | None = None

# The last time the state changed.
last_state_change: float = 0

# The time the root node started executing.
start_time: float = 0

# Whether the current node has started executing.
has_started: bool = False

# An action to run before executing another command.
action: Node | None = None

# The set of labels that have been reached since the last time execute
# has been called.
labels: set[str] = set()

# The stack of call nodes, used to implement the call statement.
# List of (Node, label)
call_node_stack: list[tuple[Node, str]] = []

def take_name(name: str) -> None:
    """
    Takes the name of a statement that is about to run.
    """

    if node is None:
        return

    if isinstance(name, str):
        labels.add(name)


class TestJump(Exception):
    """
    An exception that is raised in order to jump to `node`.
    """

    def __init__(self, node: Node):
        self.node = node


def lookup(name: str, from_node: Node) -> Node:
    """
    Tries to look up the name with `target`. If found, returns it, otherwise
    raises an exception.
    """

    if name in testcases:
        return testcases[name]

    raise KeyError("Testcase {} not found at {}:{}.".format(name, from_node.filename, from_node.linenumber))


def call_node(name: str) -> Node:
    """
    Calls the testcase with `name`. If found, returns it, otherwise
    raises an exception.
    """

    global node

    if name not in testcases:
        raise KeyError("Testcase {} not found")

    if node is not None:
        call_node_stack.append((node, name))

    return testcases[name]


def pop_call_node() -> Node | None:
    """
    Pops the last call node from the stack and returns it.
    """

    if not call_node_stack:
        if renpy.config.developer:
            raise Exception("No call on call stack.")
        return

    return call_node_stack.pop()[0]


def execute_node(
    now: float,
    current_node: Node,
    current_state: State | None,
    start: float,
    current_started: bool = False,
) -> tuple[Node | None, State | None, float, bool]:
    """
    Performs one execution cycle of a node.
    """

    try:
        if not current_started:
            if current_node.ready():
                # If the node is ready, we start it.
                current_state = current_node.start()
                start = now
                current_started = True
            else:
                return current_node, None, start, False

        current_state = current_node.execute(current_state, now - start)

    except TestJump as e:
        current_node = e.node
        current_state = None

    if current_state is None:
        return next_node, None, start, False
    else:
        return current_node, current_state, start, current_started


def execute() -> None:
    """
    Called periodically by the core interact loop when a new frame is drawn.
    This allows test code to generate events, if desired.
    """

    global node
    global state
    global start_time
    global has_started
    global action
    global old_state
    global old_loc
    global last_state_change

    _test = renpy.test.testast._test

    if node is None:
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

    now = renpy.display.core.get_time()

    try:
        node, state, start_time, has_started = execute_node(now, node, state, start_time, has_started)
    except Exception as e:
        report_exception(e)

        node = None
        state = None
        has_started = False

    labels.clear()

    if node is None and call_node_stack:
        # We've finished the current call, return
        popped_node = pop_call_node()
        if popped_node is not None:
            node = popped_node.next

    if node is None:
        end_testcase()
        return

    loc = renpy.exports.get_filename_line()

    if (old_state != state) or (old_loc != loc):
        last_state_change = now

    old_state = state
    old_loc = loc

    if (now - last_state_change) > _test.timeout:
        exc = TestcaseException("Testcase timed out after {} seconds.".format(_test.timeout))
        report_exception(exc)
        end_testcase()


def report_exception(e: Exception) -> None:
    """
    Called to report an exception that occurred during the execution of a testcase.
    This is used to print the traceback and other information about the exception.
    """

    global node
    global call_node_stack

    renpy.error.report_exception(e, editor=False)
    epc = renpy.error.MaybeColoredExceptionPrintContext(None)

    epc.indent_depth = 0
    epc.string("\nDuring testcase execution:")

    epc.indent_depth = 1

    nodes = [x[0] for x in call_node_stack[1:]] + [node]
    labels = [f"testcase {x[1]}" for x in call_node_stack]

    for n, label in zip(nodes, labels):
        filename = renpy.exports.unelide_filename(n.filename)
        epc.location(filename, n.linenumber, label)

        lines = renpy.lexer.list_logical_lines(filename)
        for fname, line_num, line in lines:
            if line_num == n.linenumber:
                epc.string("  " + line.strip())
                break


def end_testcase() -> None:
    """
    Ends the current testcase, resetting the state and node.
    """

    global node
    global state
    global start_time
    global has_started
    global action
    global old_state
    global old_loc
    global call_node_stack

    ## Pop off the call stack and end the testcase.
    if call_node_stack:
        # root = call_node_stack[0]
        # print(root)
        call_node_stack.clear()

    node = None
    state = None
    start_time = 0.0
    has_started = False
    action = None

    old_state = None
    old_loc = None

    renpy.test.testmouse.reset()
    for clbk in renpy.config.end_testcase_callbacks:
        clbk()


def test_command() -> bool:
    """
    The dialogue command. This updates dialogue.txt, a file giving all the dialogue
    in the game.
    """

    ap = renpy.arguments.ArgumentParser(description="Runs a testcase.")
    ap.add_argument("testcase", help="The name of a testcase to run.", nargs="?", default="default")

    args = ap.parse_args()

    if args.testcase not in testcases:
        raise Exception("Testcase {} was not found.".format(args.testcase))


    ## NOTE: This command gets called when the game starts for the first time, OR when the game
    ## goes back to the main menu after finishing the game. Special care is taken to avoid
    ## messing up the state of the test/call stack
    global node

    if not node and not call_node_stack:
        ## A bit janky, but we want the testcase to be the root node
        node = testcases[args.testcase]
        call_node(args.testcase)

        ## Chain the nodes in the testcases
        for name, root in testcases.items():
            root.chain(None)

    return True


renpy.arguments.register_command("test", test_command, uses_display=True)
