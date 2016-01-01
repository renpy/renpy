# Copyright 2004-2015 Tom Rothamel <pytom@bishoujo.us>
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

import renpy.display
import pygame_sdl2

# A map from the name of a testcase to the testcase.
testcases = { }

# The root node.
node = None

# The state of the root node.
status = None

# The time the root node started executing.
start_time = None

# An action to run before executing another command.
action = None

def execute():
    """
    Called periodically by the test code to generate events, if desired.
    """

    global node
    global status
    global start_time
    global action

    if node is None:
        return

    if renpy.display.interface.suppress_underlay:
        return

    # Make sure there are no test events in the event queue.
    for e in pygame_sdl2.event.copy_event_queue():
        if getattr(e, "test", False):
            return

    if action:
        old_action = action
        action = None
        renpy.display.behavior.run(old_action)

    now = renpy.display.core.get_time()

    if status is None:
        status = node.start()
        start_time = now

    if status is None:
        node = None
        return

    status = node.execute(status, now - start_time)

    if status is None:
        node = None
        return


def test_command():
    """
    The dialogue command. This updates dialogue.txt, a file giving all the dialogue
    in the game.
    """

    ap = renpy.arguments.ArgumentParser(description="Runs a testcase.")
    ap.add_argument("testcase", help="The name of a testcase to run.", nargs='?', default="default")

    args = ap.parse_args()

    if args.testcase not in testcases:
        raise Exception("Testcase {} was not found.".format(args.testcase))

    global node
    node = testcases[args.testcase]

    return True

renpy.arguments.register_command("test", test_command)
