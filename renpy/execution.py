# This file contains code responsible for managing the execution of a
# renpy object, as well as the context object.

import renpy
import copy

class Context(object):
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
    """

    def __init__(self, rollback, context=None):

        self.current = None
        self.return_stack = [ ]
        self.rollback = rollback
        self.runtime = 0

        oldsl = None
        if context:
            oldsl = context.scene_lists
            self.runtime = context.runtime

        import renpy.display.core as dcore
        self.scene_lists = dcore.SceneLists(oldsl)
        
    def goto_label(self, node_name):
        """
        Sets the name of the node that will be run when this context
        next executes.
        """
        
        self.current = node_name
        
    def run(self, node=None):
        """
        Executes as many nodes as possible in the current context. If the
        node argument is given, starts executing from that node. Otherwise,
        looks up the node given in self.current, and executes from there.
        """

        if node is None:
            node = renpy.game.script.lookup(self.current)

        while node:
            self.current = node.name

            renpy.game.exception_info = 'The last script statement executed was on line %d of %s.' % (node.linenumber, node.filename)

            if self.rollback and renpy.game.log:
                renpy.game.log.begin()

            try:
                node = node.execute()
            except renpy.game.JumpException, e:
                node = renpy.game.script.lookup(e.args[0])

            renpy.game.seen_ever[self.current] = True
            renpy.game.seen_session[self.current] = True

            if self.rollback and renpy.game.log:
                renpy.game.log.complete()
        

    def call(self, label, return_site=None):
        """
        Calls the named label.
        """

        if return_site is None:
            return_site is self.current

        self.return_stack.append(return_site)
        self.current = label

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
        else:
            label = self.return_stack[-1]

        return renpy.game.script.lookup(label)
            
    def rollback_copy(self):
        """
        Makes a copy of this object, suitable for rolling back to.
        """

        rv = Context(self.rollback)
        rv.return_stack = self.return_stack[:]
        rv.current = self.current
        rv.scene_lists = self.scene_lists.rollback_copy()
        rv.runtime = self.runtime

        return rv

    def predict(self, callback):
        """
        Performs image prediction, calling the given callback with each
        images that we predict to be loaded, in the rough order that
        they will be potentially loaded.
        """

        nodes = [ renpy.game.script.lookup(self.current) ]

        for i in range(0, renpy.config.predict_statements):
            if i >= len(nodes):
                break

            node = nodes[i]

            # Ignore exceptions in prediction, so long as
            # prediction is not needed.
            try:
                for n in node.predict(callback):
                    if n not in nodes:
                        nodes.append(n)
            except:
                if renpy.config.debug:
                    raise
                
                
    def seen_current(self, ever):
        """
        Returns a true value if we have finshed the current statement
        at least once before.

        @param ever: If True, we're checking to see if we've ever
        finished this statement. If False, we're checking to see if
        we've finished this statement in the current session.
        """

        if ever:
            seen = renpy.game.seen_ever
        else:
            seen = renpy.game.seen_session

        return self.current in seen
