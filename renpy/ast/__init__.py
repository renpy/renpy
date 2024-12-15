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

from __future__ import annotations

from renpy.ast.node import (
    DoesNotExtend as DoesNotExtend,
    Scry as Scry,
    Node as Node,
)

from renpy.ast.python import (
    PyExpr as PyExpr,
    PyCode as PyCode,
)

from renpy.ast.base_nodes import (
    Say as Say,
    Init as Init,
    Label as Label,
    Python as Python,
    EarlyPython as EarlyPython,
    Image as Image,
    Transform as Transform,
    Show as Show,
    ShowLayer as ShowLayer,
    Camera as Camera,
    Scene as Scene,
    Hide as Hide,
    With as With,
    Call as Call,
    Return as Return,
    Menu as Menu,
    Jump as Jump,
    Pass as Pass,
    While as While,
    If as If,
    UserStatement as UserStatement,
    PostUserStatement as PostUserStatement,
    Define as Define,
    Default as Default,
    Screen as Screen,
    Style as Style,
    Testcase as Testcase,
    RPY as RPY,
    Translate as Translate,
    TranslateSay as TranslateSay,
    EndTranslate as EndTranslate,
    TranslateString as TranslateString,
    TranslatePython as TranslatePython,
    TranslateBlock as TranslateBlock,
    TranslateEarlyBlock as TranslateEarlyBlock,
)

# For pickle compatibility.
if True:
    from renpy.parameter import (
        Parameter,
        Signature,
        ParameterInfo,
        ArgumentInfo,
        apply_arguments,
        EMPTY_PARAMETERS,
        EMPTY_ARGUMENTS,
    )

# Config variables that are set twice - once when the rpy is first loaded,
# and then again at init time.
EARLY_CONFIG = {
    "save_directory",
    "allow_duplicate_labels",
    "keyword_after_python",
    "steam_appid",
    "name",
    "version",
    "save_token_keys",
    "check_conflicting_properties",
    "check_translate_none",
    "defer_tl_scripts",
    "munge_in_strings",
    "interface_layer",
}

# All the define statements, in the order they were registered.
define_statements: list[Define] = []


def redefine(stores):
    """
    Re-runs the given define statements.
    """

    for i in define_statements:
        i.redefine(stores)


# All the default statements, in the order they were registered.
default_statements: list[Node] = []
