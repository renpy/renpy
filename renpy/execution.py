# Copyright 2004-2011 Tom Rothamel <pytom@bishoujo.us>
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

import renpy.display

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

    __version__ = 7

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
        
        self.make_dynamic([ "_return", "_args", "_kwargs", "mouse_visible", "suppress_overlay" ])
        self.dynamic_stack.append({ })

        if clear:
            for i in renpy.config.context_clear_layers:
                self.scene_lists.clear(layer=i)

        # A list of modes that the context has been in.
        self.modes = renpy.python.RevertableList([ "start" ])
        self.use_modes = True
        
                
        
    def make_dynamic(self, names, context=False):
        """
        Makes the variable names listed in names dynamic, by backing up
        their current value (if not already dynamic in the current call).
        """

        store = vars(renpy.store)

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
        
        store = vars(renpy.store)

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

    def report_tb(self, out):

        for i in self.call_location_stack:
            try:
                node = renpy.game.script.lookup(i)
                if not node.filename.replace("\\", "/").startswith("common/"):
                    renpy.bootstrap.report_line(out, node.filename, node.linenumber, "script call")
            except:
                pass
                
        try:
            node = renpy.game.script.lookup(self.current)
            if not node.filename.replace("\\", "/").startswith("common/"):
                renpy.bootstrap.report_line(out, node.filename, node.linenumber, "script")
        except:
            pass
            
    def run(self, node=None):
        """
        Executes as many nodes as possible in the current context. If the
        node argument is given, starts executing from that node. Otherwise,
        looks up the node given in self.current, and executes from there.
        """

        self.abnormal = True
                
        if node is None:
            node = renpy.game.script.lookup(self.current)

        while node:
            
            self.current = node.name
            self.last_abnormal = self.abnormal
            self.abnormal = False
            
            if self.rollback and renpy.game.log:
                renpy.game.log.begin()

            self.seen = False

            try:
                try:
                    self.next_node = None                    
                    node.execute()
                
                except renpy.game.CONTROL_EXCEPTIONS, e:
                    raise

                except Exception, e:
                    short, full = renpy.bootstrap.report_exception(e, editor=False)

                    if renpy.display.error.report_exception(short, full):
                        raise
                              
                node = self.next_node
            
            except renpy.game.JumpException, e:
                node = renpy.game.script.lookup(e.args[0])
                self.abnormal = True
                                
            if self.seen:
                renpy.game.seen_ever[self.current] = True
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

    def lookup_return(self, pop=True):
        """
        Returns the node to return to, or None if there is no
        such node.
        """

        if len(self.return_stack) == 0:
            return None

        if pop:
            label = self.return_stack.pop()
            self.call_location_stack.pop()
        else:
            label = self.return_stack[-1]

        return renpy.game.script.lookup(label)
            
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
        
        return rv

    def predict(self):
        """
        Performs image prediction, calling the given callback with each
        images that we predict to be loaded, in the rough order that
        they will be potentially loaded.
        """

        if not self.current:
            return

        old_images = self.images
        
        nodes = [ (renpy.game.script.lookup(self.current), self.images) ]
        node_set = set()
        
        for i in range(0, renpy.config.predict_statements):

            if i >= len(nodes):
                break

            node, images = nodes[i]

            self.images = renpy.display.image.ShownImageInfo(images)
            
            # Ignore exceptions in prediction, so long as
            # prediction is not needed.

            try:
                for n in node.predict():
                    if n is None:
                        continue

                    if n not in node_set:
                        nodes.append((n, self.images))
                        node_set.add(n)
            except:

                if renpy.config.debug_image_cache:
                    import traceback

                    print
                    traceback.print_exc()
                    print "While predicting images."

                # We accept that sometimes prediction won't work.

        self.images = old_images

            
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
            seen = renpy.game.seen_ever
        else:
            seen = renpy.game.seen_session

        return self.current in seen
