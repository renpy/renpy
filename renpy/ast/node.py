# Copyright 2004-2024 Tom Rothamel <pytom@bishoujo.us>
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

# This file contains definition of base Node class of Ren'Py AST.

from __future__ import annotations

from typing import Any, Callable, ClassVar, Literal, Never, TypeAlias

import renpy

DoesNotExtend = renpy.object.Sentinel("DoesNotExtend")


class Scry(object):
    """
    This is used to store information about the future, if we know it. Unlike
    predict, this tries to only get things we _know_ will happen.
    """

    _next: Node | None = None
    interacts: bool = False

    say: bool = False
    menu_with_caption: bool = False
    who: str | None = None

    extend_text: str | None | renpy.object.Sentinel = None
    """
    Text that will be added to the current say statment by a call to
    extend.
    """

    # By default, all attributes are None.
    def __getattr__(self, name: str) -> Any:
        return None

    def __reduce__(self):
        raise Exception("Cannot pickle Scry.")

    def next(self) -> Scry | None:
        if self._next is None:
            return None
        else:
            try:
                return self._next.scry()
            except Exception:
                return None


NodeName: TypeAlias = "str | tuple[Any, ...] | None"


class Node(renpy.location.Location):
    """
    A node in the abstract syntax tree of the program.
    """

    __slots__ = [
        'name',
        'next',
    ]

    filename: str
    "Elided string file name of this node."
    linenumber: int
    "Integer line number of first line of this node in the source file."
    col_offset: int
    "Integer column offset of first line of this node in the source file."

    name: NodeName
    """
    Unique name of the node of all nodes in the abstract syntax tree.

    Can be one of:
    * A string, giving the name of the label this node defines.
    * An opaque tuple, giving the name of the non-label statement.
    * None, if not yet assigned.
    """

    next: Node | None
    """
    Node that unconditionally follows this one in the abstract syntax tree,
    or None if this node is the last one in the block.
    """

    translatable: bool = False
    """
    True if this node is translatable, False otherwise.
    (This can be set on the class or the instance.)
    """

    translation_relevant: bool = False
    """
    True if the node is releveant to translation, and has to be processed by
    take_translations.
    """

    rollback: Literal["normal", "never", "force"] = "normal"
    """
    How does the node participate in rollback?

    * "normal" in normal mode.
    * "never" generally never.
    * "force" force it to start.
    """

    # Statement_start used to be a property on all nodes.
    @property
    def statement_start(self) -> Node:
        return self

    @statement_start.setter
    def statement_start(self, value: Never):
        pass

    def __init__(self, loc: tuple[str, int]):
        """
        Initializes this Node object.

        `loc`
            A (filename, physical line number) tuple giving the
            logical line on which this Node node starts.
        """

        super().__init__(loc[0], loc[1])

        self.name = None
        self.next = None

    def diff_info(self) -> tuple[Any, ...]:
        """
        Returns a tuple of diff info about ourself. This is used to
        compare Nodes to see if they should be considered the same node. The
        tuple returned must be hashable.
        """

        return (id(self), )

    def get_children(self, f: Callable[[Node], Any]) -> None:
        """
        Calls `f` with this node and its children.
        """

        f(self)

    def get_init(self) -> tuple[int, Node | Callable[[], None]] | None:
        """
        Returns a node that should be run at init time (that is, before
        the normal start of the script.), or None if this node doesn't
        care to suggest one.
        """

        return None

    # get_init is only present on statements that define it.
    get_init = None  # type: ignore

    def chain(self, next: Node | None) -> None:
        """
        This is called with the Node node that should be followed after
        executing this node, and all nodes that this node
        executes. (For example, if this node is a block label, the
        next is the node that should be executed after all nodes in
        the block.)
        """

        self.next = next

    def replace_next(self, old: Node, new: Node) -> None:
        """
        Replaces instances of the `old` node with `new` when it is the next
        node.
        """

        if self.next is old:
            self.next = new

    def execute(self) -> None:
        """
        Causes this node to execute, and any action it entails to be
        performed. The node should call next_node with the node to
        be executed after this one.
        """

        raise Exception("Node subclass forgot to define execute.")

    def early_execute(self) -> None:
        """
        Called when the module is loaded.
        """

    # early_execute is only present on statements that define it.
    early_execute = None  # type: ignore

    def predict(self) -> list[Node | None]:
        """
        This is called to predictively load images from this node. It
        should cause renpy.display.predict.displayable and
        renpy.display.predict.screen to be called as necessary.

        Returns a list of nodes that may follow this one, where more
        likely to be executed first is earlier in the list.
        """

        if self.next is not None:
            return [self.next]
        else:
            return []

    def scry(self) -> Scry:
        """
        Called to return an object with some general, user-definable
        information about the future.
        """

        rv = Scry()
        rv._next = self.next
        return rv

    def restructure(self, callback: Callable[[list[Node]], Any]):
        """
        Called to restructure the AST.

        When this method is called, callback is called once for each child
        block of the node. The block, a list, can be updated by the callback
        using slice assignment to the list.
        """

        # Does nothing for nodes that do not contain child blocks.
        return

    def get_code(self, dialogue_filter: Callable[[str], str] | None = None) -> str:
        """
        Returns the canonical form of the code corresponding to this statement.
        This only needs to be defined if the statement is translatable.

        `dialogue_filter`
            If present, a filter that should be applied to human-readable
            text in the statement.
        """

        raise Exception("Not Implemented")

    def analyze(self) -> None:
        """
        Called on all code after the init phase, to analyze it.
        """

        # Does nothing by default.
        return

    warp: ClassVar[bool] = False

    def can_warp(self) -> bool:
        """
        Returns true if this should be run while warping, False otherwise.
        """

        return self.warp
