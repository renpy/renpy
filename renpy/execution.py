# This file contains code responsible for managing the execution of a
# renpy object, as well as the context object.

import renpy.game
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

    @ivar rollback: True if this context particpates in rollbacks.
    """

    def __init__(self, rollback, context=None):

        self.current = None
        self.return_stack = [ ]
        self.rollback = rollback

        oldsl = None
        if context:
            oldsl = context.oldsl

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

            node = node.execute()

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

    def lookup_return(self):
        """
        Returns the node to return to, or None if there is no
        such node.
        """

        if len(self.return_stack) == 0:
            return None

        label = self.return_stack.pop()
        return renpy.game.script.lookup(label)
            
    def rollback_copy(self):
        """
        Makes a copy of this object, suitable for rolling back to.
        """

        rv = Context(self.rollback)
        rv.return_stack = self.return_stack[:]
        rv.current = self.current
        rv.scene_lists = self.scene_lists.rollback_copy()

        return rv
