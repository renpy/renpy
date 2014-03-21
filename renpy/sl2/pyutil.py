# Copyright 2004-2014 Tom Rothamel <pytom@bishoujo.us>
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

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import

import renpy # @UnusedImport

# Import the Python AST module, instead of the Ren'Py ast module.
import ast

constants = { 'foo.bar' }

def is_constant(node):
    """
    Returns true if `node` is constant for the purpose of screen
    language. Node should be a python AST node.

    Screen language ignores object identity for the purposes of
    object equality.
    """

    def check_slice(slice): # @ReservedAssignment

        if isinstance(slice, ast.Index):
            return check_node(slice.value)

        elif isinstance(slice, ast.Slice):
            if slice.lower and not check_node(slice.lower):
                return False
            if slice.upper and not check_node(slice.upper):
                return False
            if slice.step and not check_node(slice.step):
                return False

            return True

        return False


    def check_name(node):
        """
        Check nodes that make up a name. This returns a pair:

        * The first element is True if the node is constant, and False
          otherwise.
        * The second element is None if the node is constant or the name is
          not known, and the name otherwise.
        """

        if isinstance(node, ast.Name):
            name = node.id

        elif isinstance(node, ast.Attribute):
            const, name = check_name(node.value)

            if const:
                return True, None
            if not name:
                return False, None

            name = name + "." + node.attr

        else:
            return check_node(node), None

        if name in constants:
            return True, None

        return False, name

    def check_nodes(nodes):
        """
        Checks a list of nodes. Returns true if all are constant, and
        False otherwise.
        """

        for i in nodes:
            if not check_node(i):
                return False
        return True

    def check_node(node):
        """
        Returns true if the ast node `node` is constant.
        """

        #PY3: see if there are new node types.

        if isinstance(node, (ast.Num, ast.Str)):
            return True

        elif isinstance(node, (ast.List, ast.Tuple)):
            return check_nodes(node.elts)

        elif isinstance(node, (ast.Attribute, ast.Name)):
            return check_name(node)[0]

        elif isinstance(node, ast.BoolOp):
            return check_nodes(node.values)

        elif isinstance(node, ast.BinOp):
            return (
                check_node(node.left) and
                check_node(node.right)
                )

        elif isinstance(node, ast.UnaryOp):
            return check_node(node.operand)

        elif isinstance(node, ast.IfExp):
            return (
                check_node(node.test) and
                check_node(node.body) and
                check_node(node.orelse)
                )

        elif isinstance(node, ast.Dict):
            return (
                check_nodes(node.keys) and
                check_nodes(node.values)
                )

        elif isinstance(node, ast.Set):
            return check_nodes(node.elts)

        elif isinstance(node, ast.Compare):
            return (
                check_node(node.left) and
                check_nodes(node.comparators)
                )

        elif isinstance(node, ast.Repr):
            return check_node(node.value)

        elif isinstance(node, ast.Subscript):
            return (
                check_node(node.value) and
                check_slice(node.slice)
                )

        return False

    return check_node(node)
