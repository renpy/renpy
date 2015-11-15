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

# This file contains code responsible for managing the execution of a
# renpy object, as well as the context object.

import sys
import time

import renpy.display


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

    if time.time() > il_time:
        il_time = time.time() + 60
        raise Exception("Possible infinite loop.")

    return

def not_infinite_loop(delay):
    """
    :doc: other

    Resets the infinite loop detection timer to `delay` seconds.
    """

    global il_time
    il_time = time.time() + delay

class Delete(object):
    pass

class PredictInfo(renpy.object.Object):
    """
    Not used anymore, but needed for backwards compatibility.
    """

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

    __version__ = 13

    nosave = [ 'next_node' ]

    next_node = None

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

        if version < 12:
            self.translate_block_language = None

        if version < 13:
            self.line_log = [ ]


    def __init__(self, rollback, context=None, clear=False):
        """
        `clear`
            True if we should clear out the context_clear_layers.
        """

        super(Context, self).__init__()

        self.current = None
        self.call_location_stack = [ ]
        self.return_stack = [ ]

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

        # A list of lines that were run since the last time this log was
        # cleared.
        self.line_log = [ ]

        if context:
            oldsl = context.scene_lists
            self.runtime = context.runtime

            vars(self.info).update(vars(context.info))

            for k, v in context.music.iteritems():
                self.music[k] = v.copy()

            self.images = renpy.display.image.ShownImageInfo(context.images)

        else:
            oldsl = None
            self.images = renpy.display.image.ShownImageInfo(None)

        self.scene_lists = renpy.display.core.SceneLists(oldsl, self.images)

        self.make_dynamic([ "_return", "_args", "_kwargs", "mouse_visible", "suppress_overlay", "_side_image_attributes" ])
        self.dynamic_stack.append({ })

        if clear:
            for i in renpy.config.context_clear_layers:
                self.scene_lists.clear(layer=i)

        # A list of modes that the context has been in.
        self.modes = renpy.python.RevertableList([ "start" ])
        self.use_modes = True

        # The language we started with.
        self.translate_language = None

        # The identifier of the current translate block.
        self.translate_identifier = None

        # The language of the current translate block.
        self.translate_block_language = None


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

        for k, v in dynamic.iteritems():
            if isinstance(v, Delete):
                del store[k]
            else:
                store[k] = v

    def pop_all_dynamic(self):
        """
        Pops all levels of the dynamic stack. Called when we jump
        out of a context.
        """

        while self.dynamic_stack:
            self.pop_dynamic()


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

        while node:

            self.current = node.name
            self.last_abnormal = self.abnormal
            self.abnormal = False
            self.defer_rollback = None

            if renpy.config.line_log:
                ll_entry = (node.filename, node.linenumber)

                if ll_entry not in self.line_log:
                    self.line_log.append(ll_entry)

            if self.rollback and renpy.game.log:
                renpy.game.log.begin()

            self.seen = False

            try:
                try:
                    check_infinite_loop()

                    renpy.game.exception_info = "While running game code:"

                    self.next_node = None
                    node.execute()

                    if developer and self.next_node:
                        self.check_stacks()

                except renpy.game.CONTROL_EXCEPTIONS, e:

                    # An exception ends the current translation.
                    self.translate_interaction = None

                    raise

                except Exception, e:
                    self.translate_interaction = None

                    exc_info = sys.exc_info()
                    short, full, traceback_fn = renpy.error.report_exception(e, editor=False)

                    try:
                        if self.exception_handler is not None:
                            self.exception_handler(short, full, traceback_fn)
                        elif renpy.display.error.report_exception(short, full, traceback_fn):
                            raise
                    except renpy.game.CONTROL_EXCEPTIONS, ce:
                        raise ce
                    except Exception, ce:
                        raise exc_info[0], exc_info[1], exc_info[2]

                node = self.next_node

            except renpy.game.JumpException, e:
                node = renpy.game.script.lookup(e.args[0])
                self.abnormal = True

            except renpy.game.CallException, e:

                if self.next_node is None:
                    raise Exception("renpy.call can't be used when the next node is undefined.")

                node = self.call(e.label, return_site=self.next_node.name)
                self.abnormal = True
                renpy.store._args = e.args
                renpy.store._kwargs = e.kwargs

            if self.seen:
                renpy.game.persistent._seen_ever[self.current] = True  # @UndefinedVariable
                renpy.game.seen_session[self.current] = True

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

                if renpy.config.developer:
                    raise Exception("Could not find return label {!r}.".format(self.return_stack[-1]))

                self.return_stack.pop()
                self.call_location_stack.pop()
                self.pop_dynamic()

                continue

            if pop:
                self.return_stack.pop()
                self.call_location_stack.pop()

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
                return

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

                    print
                    traceback.print_exc()
                    print "While predicting images."

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
            seen = renpy.game.persistent._seen_ever  # @UndefinedVariable
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

    label = None

    while True:

        try:

            context = renpy.game.context()

            if label and renpy.game.script.has_label(label):
                context.call(label)
            label = None

            context.run()

            rv = renpy.store._return

            context.pop_all_dynamic()

            return rv

        except renpy.game.RestartContext as e:

            if e.label:
                label = e.label

            continue

        except renpy.game.RestartTopContext as e:
            if top:

                if e.label:
                    label = e.label

                continue

            else:
                raise

        except:
            context.pop_all_dynamic()
            raise
