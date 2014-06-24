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

# The set of names that should be treated as constants.
constants = { 'True', 'False', 'None', "config", "style" }

# The set of names that should be treated as pure functions.
pure_functions = {
    # Python builtins.
    "abs", "all", "any", "apply", "bin", "bool", "bytes", "callable", "chr",
    "cmp", "dict", "divmod",
    "filter", "float", "frozenset",
    "getattr", "globals", "hasattr", "hash", "hex", "int", "isinstance",
    "len", "list", "long", "map", "max", "min", "oct", "ord", "pow",
    "range", "reduce", "repr", "round", "set", "sorted",
    "str", "sum", "tuple", "unichr", "unicode", "vars", "zip",

    # enumerator and reversed return iterators at the moment.

    # minstore.py
    "_",

    # defaultstore.py
    "ImageReference", "Image", "Frame", "Solid", "LiveComposite", "LiveCrop",
    "LiveTile", "Flatten", "Null", "Window", "Viewport", "DynamicDisplayable",
    "ConditionSwitch", "ShowingSwitch", "Transform", "Animation", "Movie",
    "Particles", "SnowBlossom", "Text", "ParameterizedText", "FontGroup",
    "Drag", "Alpha", "Position", "Pan", "Move", "Motion", "Revolve", "Zoom",
    "RotoZoom", "FactorZoom", "SizeZoom", "Fade", "Dissolve", "ImageDissolve",
    "AlphaDissolve", "CropMove", "Pixellate", "OldMoveTransition",
    "MoveTransition", "MoveFactory", "MoveIn", "MoveOut", "ZoomInOut",
    "RevolveInOut", "MultipleTransition", "ComposeTransition", "Pause",
    "SubTransition", "ADVSpeaker", "ADVCharacter", "Speaker", "Character",
    "DynamicCharacter", "Fixed", "HBox", "VBox", "Grid", "AlphaBlend", "At",
    "color",

    }

def const(name):
    """
    :doc: const

    Declares a variable in the store to be constant.


    A variable is constant if nothing can change its value, or any value
    reached by indexing it or accessing its attributes. Variables must
    remain constant out of define, init, and translate python blocks.

    `name`
        A string giving the name of the variable to declare constant.
    """

    constants.add(name)


def pure(fn):
    """
    :doc: const

    Declares a function as pure. A pure function must always return the
    same value when it is called with the same arguments, outside of
    define, init, and translate python blocks.

    `fn`
        The name of the function to declare pure. This may either be a string
        containing the name of the function, or the function itself.

    Returns `fn`, allowing this function to be used as a decorator.
    """

    rv = fn

    if not isinstance(fn, basestring):
        fn = fn.__name__

    pure_functions.add(fn)

    return rv


class Analysis(object):
    """
    Represents the result of code analysis, and provides tools to perform
    code analysis.
    """

    def __init__(self):
        # The variables we consider to be not-constant.
        self.not_constant = set()

        # The variables we consider to be potentially constant.
        self.constant = set(constants)

    def mark_constant(self, name):
        """
        Marks `name` as potentially constant.
        """

        if not name in self.not_constant:
            self.constant.add(name)

    def mark_not_constant(self, name):
        """
        Marks `name` as definitely not-constant.
        """

        self.constant.discard(name)
        self.not_constant.add(name)

    def is_constant(self, node):
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

                if name is not None:
                    name = name + "." + node.attr

                if const:
                    return True, name

            else:
                return check_node(node), None

            if name in self.not_constant:
                return False, None

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

            elif isinstance(node, ast.Call):
                _const, name = check_name(node.func)

                # The function must have a name, and must be declared pure.
                if not name in pure_functions:
                    return False

                # Arguments and keyword arguments must be pure.
                if not check_nodes(node.args):
                    return False

                if not check_nodes(i.value for i in node.keywords):
                    return False

                if (node.starargs is not None) and not check_node(node.starargs):
                    return False

                if (node.kwargs is not None) and not check_node(node.kwargs):
                    return False

                return True

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


class ConstAnalysis(ast.NodeVisitor):
    """
    This analyzes python nodes and determines which variables should be
    marked const and not-const.
    """

    def __init__(self):

        # A set of variables that are const, and those that are not.
        self.constants = constants
        self.not_constants = set()

        # True if variables should be assigned const (if otherwise unknown),
        # false if they should be assigned non-const.
        self.const = False

    def visit_Name(self, node):
        if isinstance(node, ast.AugStore):
            self.constants.discard(node.id)
            self.not_constants.add(node.id)

        if isinstance(node.ctx, ast.Store):
            if self.const:
                if node.id not in self.not_constants:
                    self.constants.add(node.id)
            else:
                self.constants.discard(node.id)
                self.not_constants.add(node.id)


