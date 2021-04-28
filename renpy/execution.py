# Copyright 2004-2021 Tom Rothamel <pytom@bishoujo.us>
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

# This file contains code responsible for managing the execution of a
# renpy object, as well as the context object.

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals
from renpy.compat import *
from future.utils import reraise

import sys
import time

import renpy.display
import renpy.test

import ast as pyast

# The number of statements that have been run since the last infinite loop
# check.
il_statements = 0

# The deadline for reporting we're not in an infinite loop.
il_time = 0


def check_infinite_loop():
    global il_statements

    il_statements += 1

    if il_statements <= 1000:
        return

    il_statements = 0

    global il_time

    now = time.time()

    if now > il_time:
        il_time = now + 60
        raise Exception("Possible infinite loop.")

    if renpy.config.developer and (il_time > now + 60):
        il_time = now + 60

    return


def not_infinite_loop(delay):
    """
    :doc: other

    Resets the infinite loop detection timer to `delay` seconds.
    """

    # Give more time in non-developer mode, since computers can be crazy slow
    # and the player can't do much about it.
    if not renpy.config.developer:
        delay *= 5

    global il_time
    il_time = time.time() + delay


class Delete(object):
    pass


class PredictInfo(renpy.object.Object):
    """
    Not used anymore, but needed for backwards compatibility.
    """


class LineLogEntry(object):

    def __init__(self, filename, line, node, abnormal):
        self.filename = filename
        self.line = line
        self.node = node
        self.abnormal = abnormal

        for i in renpy.config.line_log_callbacks:
            i(self)

    def __eq__(self, other):
        if not isinstance(other, LineLogEntry):
            return False

        return (self.filename == other.filename) and (self.line == other.line) and (self.node is other.node)

    def __ne__(self, other):
        return not (self == other)


class Context(renpy.object.Object):
    """
    This is the context object which stores the current context
    of the game interpreter.

    @ivar current: The name of the node that is currently being
    executed.

    @ivar return_stack: A list of names of nodes that should be
    returned to when the return statement executes. (When a return
    occurs, the name is looked up, and name.text is then executed.)

    @ivar scene_lists: The scene lists associated with the current
    context.

    @ivar rollback: True if this context participates in rollbacks.

    @ivar runtime: The time spent in this context, in milliseconds.

    @ivar info: An object that is made available to user code. This object
    does participates in rollback.
    """

    __version__ = 16

    nosave = [ 'next_node' ]

    next_node = None

    force_checkpoint = False

    come_from_name = None
    come_from_label = None

    temporary_attributes = None

    deferred_translate_identifier = None

    def __repr__(self):

        if not self.current:
            return "<Context>"

        node = renpy.game.script.lookup(self.current)

        return "<Context: {}:{} {!r}>".format(
            node.filename,
            node.linenumber,
            node.diff_info(),
            )

    def after_upgrade(self, version):
        if version < 1:
            self.scene_lists.image_predict_info = self.predict_info.images

        if version < 2:
            self.abnormal = False
            self.last_abnormal = False

        if version < 3:
            self.music = { }

        if version < 4:
            self.interacting = False

        if version < 5:
            self.modes = renpy.python.RevertableList([ "start" ])
            self.use_modes = True

        if version < 6:
            self.images = self.predict_info.images

        if version < 7:
            self.init_phase = False
            self.next_node = None

        if version < 8:
            self.defer_rollback = None

        if version < 9:
            self.translate_language = None
            self.translate_identifier = None

        if version < 10:
            self.exception_handler = None

        if version < 11:
            self.say_attributes = None

        if version < 13:
            self.line_log = [ ]

        if version < 14:
            self.movie = { }

        if version < 15:
            self.abnormal_stack = [ False ] * len(self.return_stack)

        if version < 16:
            self.alternate_translate_identifier = None

    def __init__(self, rollback, context=None, clear=False):
        """
        `clear`
            True if we should clear out the context_clear_layers.
        """

        super(Context, self).__init__()

        self.current = None
        self.call_location_stack = [ ]
        self.return_stack = [ ]

        # The value of abnormal at the time of the call.
        self.abnormal_stack = [ ]

        # Two deeper then the return stack and call location stack.
        # 1 deeper is for the context top-level, 2 deeper is for
        # _args, _kwargs, and _return.
        self.dynamic_stack = [ { } ]

        self.rollback = rollback
        self.runtime = 0
        self.info = renpy.python.RevertableObject()
        self.seen = False

        # True if there has just been an abnormal transfer of control,
        # like the start of a context, a jump, or a call. (Returns are
        # considered to be normal.)
        #
        # Set directly by ast.Call and ast.Jump.
        self.abnormal = True

        # True if the last statement caused an abnormal transfer of
        # control.
        self.last_abnormal = False

        # A map from the name of a music channel to the MusicContext
        # object corresponding to that channel.
        self.music = renpy.python.RevertableDict()

        # True if we're in the middle of a call to ui.interact. This
        # will cause Ren'Py to generate an error if we call ui.interact
        # again.
        self.interacting = False

        # True if we're in the init phase. (Isn't inherited.)
        self.init_phase = False

        # When deferring a rollback, the arguments to pass to renpy.exports.rollback.
        self.defer_rollback = None

        # The exception handler that is called when an exception occurs while executing
        # code. If None, a default handler is used. This is reset when run is called.
        self.exception_handler = None

        # The attributes that are used by the current say statement.
        self.say_attributes = None
        self.temporary_attributes = None

        # A list of lines that were run since the last time this log was
        # cleared.
        self.line_log = [ ]

        # Do we want to force a checkpoint before the next statement
        # executed?
        self.force_checkpoint = False

        # A map from a channel to the Movie playing on that channel.
        self.movie = { }

        if context:
            oldsl = context.scene_lists
            self.runtime = context.runtime

            vars(self.info).update(vars(context.info))

            self.music = dict(context.music)
            self.movie = dict(context.movie)

            self.images = renpy.display.image.ShownImageInfo(context.images)

        else:
            oldsl = None
            self.images = renpy.display.image.ShownImageInfo(None)

        self.scene_lists = renpy.display.core.SceneLists(oldsl, self.images)

        for i in renpy.config.context_copy_remove_screens:
            self.scene_lists.remove("screens", i, None)

        self.make_dynamic([ "_return", "_args", "_kwargs", "mouse_visible", "suppress_overlay", "_side_image_attributes" ])
        self.dynamic_stack.append({ })

        if clear:
            for i in renpy.config.context_clear_layers:
                self.scene_lists.clear(layer=i)

        # A list of modes that the context has been in.
        self.modes = renpy.python.RevertableList([ "start" ])
        self.use_modes = True

        # The language we started with.
        self.translate_language = renpy.game.preferences.language

        # The identifier of the current translate block.
        self.translate_identifier = None

        # The alternate identifier of the current translate block.
        self.alternate_translate_identifier = None

        # The translate identifier of the last say statement with
        # interact = False.
        self.deferred_translate_identifier = None

    def replace_node(self, old, new):

        def replace_one(name):
            n = renpy.game.script.lookup(name)
            if n is old:
                return new.name

            return name

        self.current = replace_one(self.current)
        self.return_stack = [ replace_one(i) for i in self.return_stack ]

    def make_dynamic(self, names, context=False):
        """
        Makes the variable names listed in names dynamic, by backing up
        their current value (if not already dynamic in the current call).
        """

        store = renpy.store.__dict__

        if context:
            index = 0
        else:
            index = -1

        for i in names:

            if i in self.dynamic_stack[index]:
                continue

            if i in store:
                self.dynamic_stack[index][i] = store[i]
            else:
                self.dynamic_stack[index][i] = Delete()

    def pop_dynamic(self):
        """
        Pops one level of the dynamic stack. Called when the return
        statement is run.
        """

        if not self.dynamic_stack:
            return

        store = renpy.store.__dict__

        dynamic = self.dynamic_stack.pop()

        for k, v in dynamic.items():
            if isinstance(v, Delete):
                store.pop(k, None)
            else:
                store[k] = v

    def pop_all_dynamic(self):
        """
        Pops all levels of the dynamic stack. Called when we jump
        out of a context.
        """

        while self.dynamic_stack:
            self.pop_dynamic()

    def pop_dynamic_roots(self, roots):

        for dynamic in reversed(self.dynamic_stack):

            for k, v in dynamic.items():
                name = "store." + k

                if isinstance(v, Delete) and (name in roots):
                    del roots[name]
                else:
                    roots[name] = v

    def goto_label(self, node_name):
        """
        Sets the name of the node that will be run when this context
        next executes.
        """

        self.current = node_name

    def check_stacks(self):
        """
        Check and fix stack corruption.
        """

        if len(self.dynamic_stack) != len(self.return_stack) + 2:

            e = Exception("Potential return stack corruption: dynamic={} return={}".format(len(self.dynamic_stack), len(self.return_stack)))

            while len(self.dynamic_stack) < len(self.return_stack) + 2:
                self.dynamic_stack.append({})

            while len(self.dynamic_stack) > len(self.return_stack) + 2:
                self.pop_dynamic()

            raise e

    def report_traceback(self, name, last):

        if last:
            return

        rv = [ ]

        for i in self.call_location_stack:
            try:
                node = renpy.game.script.lookup(i)
                if not node.filename.replace("\\", "/").startswith("common/"):
                    rv.append((node.filename, node.linenumber, "script call", None))
            except:
                pass

        try:
            node = renpy.game.script.lookup(self.current)
            if not node.filename.replace("\\", "/").startswith("common/"):
                rv.append((node.filename, node.linenumber, "script", None))
        except:
            pass

        return rv

    def report_coverage(self, node):
        """
        Execs a python pass statement on the line of code corresponding to
        `node`. This indicates to python coverage tools that this line has
        been executed.
        """

        ps = pyast.Pass(lineno=node.linenumber, col_offset=0)
        module = pyast.Module(lineno=node.linenumber, col_offset=0, body=[ ps ])
        code = compile(module, node.filename, 'exec')
        exec(code)

    def come_from(self, name, label):
        """
        When control reaches name, call label. Only for internal use.
        """

        self.come_from_name = name
        self.come_from_label = label

    def run(self, node=None):
        """
        Executes as many nodes as possible in the current context. If the
        node argument is given, starts executing from that node. Otherwise,
        looks up the node given in self.current, and executes from there.
        """

        self.exception_handler = None

        self.abnormal = True

        if node is None:
            node = renpy.game.script.lookup(self.current)

        developer = renpy.config.developer
        tracing = sys.gettrace() is not None

        # Is this the first time through the loop?
        first = True

        while node:

            if node.name == self.come_from_name:
                self.come_from_name = None
                node = self.call(self.come_from_label, return_site=node.name)
                self.make_dynamic([ "_return", "_begin_rollback" ])
                renpy.store._begin_rollback = False

            this_node = node
            type_node_name = type(node).__name__

            renpy.plog(1, "--- start {} ({}:{})", type_node_name, node.filename, node.linenumber)

            self.current = node.name
            self.last_abnormal = self.abnormal
            self.abnormal = False
            self.defer_rollback = None

            if renpy.config.line_log:
                ll_entry = LineLogEntry(node.filename, node.linenumber, node, self.last_abnormal)

                if ll_entry not in self.line_log:
                    self.line_log.append(ll_entry)

            if not renpy.store._begin_rollback:
                update_rollback = False
                force_rollback = False
            elif first or self.force_checkpoint or (node.rollback == "force"):
                update_rollback = True
                force_rollback = True
            elif not renpy.config.all_nodes_rollback and (node.rollback == "never"):
                update_rollback = False
                force_rollback = False
            else:
                update_rollback = True
                force_rollback = False

            # Force a new rollback to start to match things in the forward log.
            if renpy.game.log.forward and renpy.game.log.forward[0][0] == node.name:
                update_rollback = True
                force_rollback = True

            first = False

            if update_rollback:

                if self.rollback and renpy.game.log:
                    renpy.game.log.begin(force=force_rollback)

                if self.rollback and self.force_checkpoint:
                    renpy.game.log.force_checkpoint = True
                    self.force_checkpoint = False

            self.seen = False

            renpy.test.testexecution.take_name(self.current)

            try:
                try:
                    check_infinite_loop()

                    if tracing:
                        self.report_coverage(node)

                    renpy.game.exception_info = "While running game code:"

                    self.next_node = None

                    renpy.plog(2, "    before execute {} ({}:{})", type_node_name, node.filename, node.linenumber)

                    node.execute()

                    renpy.plog(2, "    after execute {} ({}:{})", type_node_name, node.filename, node.linenumber)

                    if developer and self.next_node:
                        self.check_stacks()

                except renpy.game.CONTROL_EXCEPTIONS as e:

                    # An exception ends the current translation.
                    self.translate_interaction = None

                    raise

                except Exception as e:
                    self.translate_interaction = None

                    exc_info = sys.exc_info()
                    short, full, traceback_fn = renpy.error.report_exception(e, editor=False)

                    try:
                        handled = False

                        if self.exception_handler is not None:
                            self.exception_handler(short, full, traceback_fn)
                            handled = True
                        elif renpy.config.exception_handler is not None:
                            handled = renpy.config.exception_handler(short, full, traceback_fn)

                        if not handled:
                            if renpy.display.error.report_exception(short, full, traceback_fn):
                                raise
                    except renpy.game.CONTROL_EXCEPTIONS as ce:
                        raise ce
                    except Exception as ce:
                        reraise(exc_info[0], exc_info[1], exc_info[2])

                node = self.next_node

            except renpy.game.JumpException as e:
                node = renpy.game.script.lookup(e.args[0])
                self.abnormal = True

            except renpy.game.CallException as e:

                if e.from_current:
                    return_site = getattr(node, "statement_start", node).name
                else:
                    if self.next_node is None:
                        raise Exception("renpy.call can't be used when the next node is undefined.")
                    return_site = self.next_node.name

                node = self.call(e.label, return_site=return_site)
                self.abnormal = True
                renpy.store._args = e.args
                renpy.store._kwargs = e.kwargs

            if self.seen:
                renpy.game.persistent._seen_ever[self.current] = True # @UndefinedVariable
                renpy.game.seen_session[self.current] = True

            renpy.plog(2, "    end {} ({}:{})", type_node_name, this_node.filename, this_node.linenumber)

        if self.rollback and renpy.game.log:
            renpy.game.log.complete()

    def mark_seen(self):
        """
        Marks the current statement as one that has been seen by the user.
        """

        self.seen = True

    def call(self, label, return_site=None):
        """
        Calls the named label.
        """

        if not self.current:
            raise Exception("Context not capable of executing Ren'Py code.")

        if return_site is None:
            return_site = self.current

        self.call_location_stack.append(self.current)

        self.return_stack.append(return_site)
        self.dynamic_stack.append({ })
        self.abnormal_stack.append(self.last_abnormal)
        self.current = label

        self.make_dynamic([ "_args", "_kwargs" ])
        renpy.store._args = None
        renpy.store._kwargs = None

        return renpy.game.script.lookup(label)

    def pop_call(self):
        """
        Blindly pops the top call record from the stack.
        """

        if not self.return_stack:
            if renpy.config.developer:
                raise Exception("No call on call stack.")

            return

        self.return_stack.pop()
        self.call_location_stack.pop()
        self.pop_dynamic()
        self.abnormal_stack.pop()

    def lookup_return(self, pop=True):
        """
        Returns the node to return to, or None if there is no
        such node.
        """

        while self.return_stack:

            node = None

            if renpy.game.script.has_label(self.return_stack[-1]):
                node = renpy.game.script.lookup(self.return_stack[-1])
            elif renpy.game.script.has_label(self.call_location_stack[-1]):
                node = renpy.game.script.lookup(self.call_location_stack[-1]).next

            if node is None:

                if not pop:
                    return None

                # If we can't find anything, try to recover.

                if renpy.config.return_not_found_label:

                    while len(self.return_stack) > 1:
                        self.pop_call()

                    node = renpy.game.script.lookup(renpy.config.return_not_found_label)

                else:

                    if renpy.config.developer:
                        raise Exception("Could not find return label {!r}.".format(self.return_stack[-1]))

                    self.return_stack.pop()
                    self.call_location_stack.pop()
                    self.pop_dynamic()
                    self.abnormal = self.abnormal_stack.pop()

                    continue

            if pop:
                self.return_stack.pop()
                self.call_location_stack.pop()
                self.abnormal = self.abnormal_stack.pop()

            return node

        return None

    def rollback_copy(self):
        """
        Makes a copy of this object, suitable for rolling back to.
        """

        rv = Context(self.rollback, self)
        rv.call_location_stack = self.call_location_stack[:]
        rv.return_stack = self.return_stack[:]
        rv.dynamic_stack = [ i.copy() for i in self.dynamic_stack ]
        rv.current = self.current

        rv.runtime = self.runtime
        rv.info = self.info

        rv.translate_language = self.translate_language
        rv.translate_identifier = self.translate_identifier

        rv.abnormal = self.abnormal
        rv.last_abnormal = self.last_abnormal
        rv.abnormal_stack = list(self.abnormal_stack)

        return rv

    def predict_call(self, label, return_site):
        """
        This is called by the prediction code to indicate that a call to
        `label` will occur.

        `return_site`
            The name of the return site to push on the predicted return
            stack.

        Returns the node corresponding to `label`
        """

        self.predict_return_stack = list(self.predict_return_stack)
        self.predict_return_stack.append(return_site)

        return renpy.game.script.lookup(label)

    def predict_return(self):
        """
        This predicts that a return will occur.

        It returns the node we predict will be returned to.
        """

        if not self.predict_return_stack:
            return None

        self.predict_return_stack = list(self.predict_return_stack)
        label = self.predict_return_stack.pop()

        return renpy.game.script.lookup(label)

    def predict(self):
        """
        Performs image prediction, calling the given callback with each
        images that we predict to be loaded, in the rough order that
        they will be potentially loaded.
        """

        if not self.current:
            return

        if renpy.config.predict_statements_callback is None:
            return

        old_images = self.images

        # A worklist of (node, images, return_stack) tuples.
        nodes = [ ]

        # The set of nodes we've seen. (We only consider each node once.)
        seen = set()

        # Find the roots.
        for label in renpy.config.predict_statements_callback(self.current):

            if not renpy.game.script.has_label(label):
                continue

            node = renpy.game.script.lookup(label)

            if node in seen:
                continue

            nodes.append((node, self.images, self.return_stack))
            seen.add(node)

        # Predict statements.
        for i in range(0, renpy.config.predict_statements):

            if i >= len(nodes):
                break

            node, images, return_stack = nodes[i]

            self.images = renpy.display.image.ShownImageInfo(images)
            self.predict_return_stack = return_stack

            try:

                for n in node.predict():
                    if n is None:
                        continue

                    if n not in seen:
                        nodes.append((n, self.images, self.predict_return_stack))
                        seen.add(n)

            except:

                if renpy.config.debug_image_cache:
                    import traceback

                    print("While predicting images.")
                    traceback.print_exc()
                    print()

            self.images = old_images
            self.predict_return_stack = None

            yield True

        yield False

    def seen_current(self, ever):
        """
        Returns a true value if we have finshed the current statement
        at least once before.

        @param ever: If True, we're checking to see if we've ever
        finished this statement. If False, we're checking to see if
        we've finished this statement in the current session.
        """

        if not self.current:
            return False

        if ever:
            seen = renpy.game.persistent._seen_ever # @UndefinedVariable
        else:
            seen = renpy.game.seen_session

        return self.current in seen

    def do_deferred_rollback(self):
        """
        Called to cause deferred rollback to occur.
        """

        if not self.defer_rollback:
            return

        force, checkpoints = self.defer_rollback

        self.defer_rollback = None

        renpy.exports.rollback(force, checkpoints)

    def get_return_stack(self):
        return list(self.return_stack)

    def set_return_stack(self, return_stack):
        self.return_stack = list(return_stack)

        while len(self.call_location_stack) > len(self.return_stack):
            self.call_location_stack.pop()

            d = self.dynamic_stack.pop()
            d.update(self.dynamic_stack[-1])
            self.dynamic_stack[-1] = d

        while len(self.call_location_stack) < len(self.return_stack):
            self.call_location_stack.append("unknown location")
            self.dynamic_stack.append({})


def run_context(top):
    """
    Runs the current context until it can't be run anymore, while handling
    the RestartContext and RestartTopContext exceptions.
    """

    if renpy.config.context_callback is not None:
        renpy.config.context_callback()

    while True:

        try:

            context = renpy.game.context()

            context.run()

            rv = renpy.store._return

            context.pop_all_dynamic()

            return rv

        except renpy.game.RestartContext as e:

            # Apply defaults.
            renpy.exports.execute_default_statement(False)
            continue

        except renpy.game.RestartTopContext as e:
            if top:

                # Apply defaults.
                renpy.exports.execute_default_statement(False)
                continue

            else:
                raise

        except:
            context.pop_all_dynamic()
            raise
