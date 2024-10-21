from __future__ import print_function, unicode_literals, annotations

import ast
import inspect
import re
import collections
import keyword
import renpy.sl2
import shutil
import io
import os
import textwrap
import pprint
import types

from typing import Any, Iterable, Literal

try:
    import builtins
except ImportError:
    import __builtin__ as builtins # type: ignore

# Additional keywords in the Ren'Py script language.
SCRIPT_KEYWORDS = """\
$
as
at
behind
expression
onlayer
zorder
strings
take
nointeract
elif
old
new
"""

# ATL Keywords.
ATL_KEYWORDS = """\
repeat
block
contains
parallel
choice
on
time
function
event
animation
clockwise
counterclockwise
circles
knot
"""

# SL2 Keywords (that aren't statements).
SL2_KEYWORDS = """\
tag
has
index
"""

# LayerImage keywords
LI_KEYWORDS = """\
layeredimage
attribute
group
always
"""


def script_keywords():

    tries = [ renpy.parser.statements ]

    rv = set()

    while tries:
        trie = tries.pop(0)
        for k, v in trie.words.items():
            rv.add(k)
            tries.append(v)

    rv.remove("layer")

    return rv


script_keywords()


def sl2_keywords():

    rv = set()

    for i in sorted(renpy.sl2.slparser.statements):
        rv.add(i)

    rv.remove("icon")
    rv.remove("iconbutton")

    return rv


def sl2_regexps():

    rv = [ ]

    groups = collections.defaultdict(set)
    has_style = { }

    for k, v in renpy.sl2.slparser.properties.items():
        prefix, style = k

        has_style[prefix] = style

        if prefix == "icon_":
            continue

        props = tuple(sorted(v))

        groups[props, style].add(prefix)

    style_part2 = "(?:" + "|".join(sorted(renpy.sl2.slparser.STYLE_PREFIXES)) + ")"

    items = list(groups.items())
    items.sort(key=lambda a : (tuple(sorted(a[1])), a[0][1]))

    for k, prefixes in items:
        names, style = k

        if len(prefixes) > 1:
            part1 = "(?:" + "|".join(sorted(prefixes)) + ")"
        else:
            part1 = tuple(prefixes)[0]

        if style:
            part2 = style_part2
        else:
            part2 = ""

        part3 = "(?:" + "|".join(sorted(names)) + ")"

        re = part1 + part2 + part3
        rv.append(re)

    return rv


def expanded_sl2_properties():

    rv = set()

    for k, v in renpy.sl2.slparser.properties.items():
        prefix, style = k

        if prefix == "icon_":
            continue

        if style:
            style_prefixes = renpy.sl2.slparser.STYLE_PREFIXES
        else:
            style_prefixes = [ '' ]

        for i in style_prefixes:
            for j in v:
                rv.add(prefix + i + j)

    rv = list(rv)
    rv.sort()

    return rv


def write_keywords(srcdir='source'):
    outf = os.path.join(srcdir, 'keywords.py')

    kwlist = set(keyword.kwlist)
    kwlist |= script_keywords()
    kwlist |= sl2_keywords()
    kwlist |= set(ATL_KEYWORDS.split())
    kwlist |= set(SCRIPT_KEYWORDS.split())
    kwlist |= set(SL2_KEYWORDS.split())
    kwlist |= set(LI_KEYWORDS.split())

    kwlist = list(kwlist)

    kwlist.sort()

    with open(outf, "w") as f:

        keyword_regex = [ re.escape(i) for i in kwlist ]

        f.write("keywords = %s\n" % pprint.pformat(kwlist))
        f.write("keyword_regex = %s\n" % pprint.pformat(keyword_regex))
        f.write("keyword_regex = '|'.join(keyword_regex)\n")

        properties = [ i for i in expanded_sl2_properties() if i not in kwlist ]

        f.write("properties = %s\n" % pprint.pformat(properties))
        f.write("property_regexes = %s\n" % pprint.pformat(sl2_regexps()))

    shutil.copy(outf, os.path.join(srcdir, "../../tutorial/game/keywords.py"))


# A map from filename to a list of lines that are supposed to go into
# that file.
line_buffer = collections.defaultdict[str, list[str]](list)

# A map from id(o) to the names it's documented under.
documented = collections.defaultdict[int, list[str]](list)

def getdoc(o):
    """
    Returns the docstring for `o`, but unlike inspect.getdoc, does not get
    values from base classes if absent (and it's faster too).
    Will still get the inherited docstring for a non-overridden method in a
    subclass (because the method object is the same as the base classes).
    """

    doc = getattr(o, "__doc__", None)

    if not doc:
        return None

    return inspect.cleandoc(doc)

# The docstring for object.__init__ - which we don't want to pass for one of our classes's
objinidoc = getdoc(object.__init__)

_file_trees: dict[str, ast.Module] = {}

def scan_pep224(prefix: str, o_name: str | None, o: type | types.ModuleType, /):
    """
    Scan for PEP-224 docstrings for variables of `o` (either a module or class).
    For classes also scans its __init__ method.

    Documented variables are then scanned for Sphinx docstrings and added to the
    line buffer.
    """

    if isinstance(o, types.ModuleType):
        # No variables in namespace packages.
        if o.__spec__.origin is None:
            return

        module_name = o.__name__

    elif isinstance(o, type):
        module_name = o.__module__

    else:
        raise TypeError(f"Expected a class or module, got {o!r}")

    fn = inspect.getfile(o)

    # Can't read Cython files.
    if fn == "built-in":
        return

    # No source for Ren'Py store modules.
    if module_name in renpy.python.store_modules:
        return

    if fn in _file_trees:
        tree = _file_trees[fn]
    else:
        try:
            # Maybe raise exceptions with appropriate message
            # before using cleaned doc_obj.source
            source, _ = inspect.findsource(o)
            tree = ast.parse("".join(source), fn)

        except (OSError, TypeError, SyntaxError) as exc:
            print(f"Warning: couldn't read PEP-224 variable docstrings from {o!r}: {exc}")
            return

        _file_trees[fn] = tree

    def scan(tree: ast.AST, in_init_func: bool):
        from itertools import tee
        a, b = \
            tee(ast.iter_child_nodes(tree))

        next(b, None)

        for assign_node, str_node in zip(a, b):
            if not (isinstance(str_node, ast.Expr) and
                    isinstance(str_node.value, ast.Constant) and
                    isinstance(str_node.value.value, str)):
                continue

            if isinstance(assign_node, ast.Assign) and len(assign_node.targets) == 1:
                target = assign_node.targets[0]

            elif isinstance(assign_node, ast.AnnAssign):
                target = assign_node.target
            else:
                continue

            if (not in_init_func) and isinstance(target, ast.Name):
                name = target.id
            elif (in_init_func and
                isinstance(target, ast.Attribute) and
                isinstance(target.value, ast.Name) and
                target.value.id == 'self'):
                name = target.attr
            else:
                continue

            docstring = inspect.cleandoc(str_node.value.value)
            if not docstring:
                continue

            default = None
            if assign_node.value is not None:
                try:
                    default = ast.unparse(assign_node.value)
                except Exception:
                    pass

            if o_name is not None:
                name = f"{o_name}{name}"

            vars[name] = docstring, default

        return vars

    vars: dict[str, tuple[str, str | None]] = {}

    if isinstance(o, types.ModuleType):
        default_doc_type = "var"
        scan(tree, False)

    elif isinstance(o, type):
        default_doc_type = "attribute"

        class ClassFoundException(Exception):
            def __init__(self, class_def: ast.ClassDef):
                self.class_def = class_def

        class ClassFinder(ast.NodeVisitor):
            def __init__(self):
                self.stack = []

            def visit_FunctionDef(self, node):
                self.stack.append(node.name)
                self.stack.append('<locals>')
                self.generic_visit(node)
                self.stack.pop()
                self.stack.pop()

            visit_AsyncFunctionDef = visit_FunctionDef # type: ignore

            def visit_ClassDef(self, node):
                self.stack.append(node.name)
                if o.__qualname__ == '.'.join(self.stack):
                    raise ClassFoundException(node)
                self.generic_visit(node)
                self.stack.pop()

        try:
            ClassFinder().visit(tree)
        except ClassFoundException as e:
            scan(e.class_def, False)

            # For classes add instance variables defined in __init__
            # Get the *last* __init__ node in case it is preceded by @overloads.
            for node in reversed(e.class_def.body):
                if isinstance(node, ast.FunctionDef) and node.name == '__init__':
                    scan(node, True)
                    break
        else:
            print(f"Warning: couldn't find class {o.__qualname__} in {fn}")
            return

    for name, (docstring, default) in vars.items():
        (
            lines,
            doc_type,
            section,
            name,
            explicit_default,
        ) = inspect_doc(name, docstring, default)

        if section is None:
            continue

        if doc_type is None:
            doc_type = default_doc_type

        if explicit_default is not None:
            default = explicit_default

        if default is None:
            default = "..."

        # Put it into the line buffer.
        lb = line_buffer[section]

        lb.append(f"{prefix}.. {doc_type}:: {name} = {default}")

        for l in lines:
            lb.append(f"{prefix}    {l}")

        lb.append(prefix)


def scan(name: str, o: Any, prefix="", inclass=False):
    """
    Given an object `o`, scans it for sphinx doc string and adds it to the
    line buffer and list of documented objects.
    """

    # The formatted arguments.
    args = None

    # Get the callable's docstring.
    doc = getdoc(o)

    if not doc:
        return

    # Cython-generated docstrings start with the function and arguments.
    if re.match(r'[\w\.]+\(', doc):
        sig, _, doc = doc.partition("\n\n")
        doc = textwrap.dedent(doc)

        if "(" in sig:
            args = "(" + sig.partition("(")[2]

    if not doc:
        return

    (
        lines,
        doc_type,
        section,
        new_name,
        explicit_args,
    ) = inspect_doc(name, doc, args)

    if section is None:
        return

    # Don't add documentation via this path.
    if new_name != name:
        return

    if inspect.isclass(o):
        if issubclass(o, (renpy.store.Action,
                        renpy.store.BarValue,
                        renpy.store.InputValue)):
            o_type = "function"
        else:
            o_type = "class"
    elif inclass:
        o_type = "method"
    else:
        o_type = "function"

    if doc_type is None:
        doc_type = o_type

    # Forbid to add functions/classes/method as variables.
    elif doc_type not in ("function", "class", "method"):
        print(f"Warning: {name} is a {o_type} but documented as {doc_type}.")
        return

    if explicit_args is not None:
        args = explicit_args

    if args is None:
        # Get the arguments.
        if inspect.isclass(o):
            init = getattr(o, "__init__", None)
            if not init:
                return

            init_doc = getdoc(init)

            if init_doc and (init_doc != objinidoc):
                lines.append("")
                lines.extend(init_doc.split("\n"))

            if init != object.__init__: # we don't want that signature either
                try:
                    args = inspect.signature(init)
                except Exception:
                    args = None

        elif inspect.isfunction(o) or inspect.ismethod(o):
            args = inspect.signature(o)

        else:
            print(f"Warning: {name} has section but not args.")
            return

        # Format the arguments.
        if args is not None:
            # Skip 'self' in methods.
            pars = iter(args.parameters.values())
            if "self" in args.parameters:
                next(pars)

            # Strip annotations, at least for now.
            pars = (p.replace(annotation=p.empty) for p in pars)
            args = args.replace(parameters=list(pars))

            args = str(args)
        else:
            args = "()"

    # Put it into the line buffer.
    lb = line_buffer[section]

    lb.append(f"{prefix}.. {doc_type}:: {name}{args}")

    for l in lines:
        lb.append(f"{prefix}    {l}")

    lb.append(prefix)

    if inspect.isclass(o):
        if (name not in [ "Matrix", "OffsetMatrix", "RotateMatrix", "ScaleMatrix" ]):
            # Scan for documented attributes in the class first.
            scan_pep224(prefix + "    ", None, o)

            # Then for other classes and methods.
            for i in dir(o):
                scan(i, getattr(o, i), prefix + "    ", inclass=True)

    if name == "identity":
        raise Exception("identity")

    documented[id(o)].append(name)


def inspect_doc(name: str, doc: str, args_or_default: str | None):
    """
    Given doc string after cleandoc, search for special lines
    :doc:, :name: and :args: or :default: in it.

    Return a (doc lines, doc_type, section, name, args or default) tuple.
    """

    if doc[0] == ' ':
        print("Bad docstring for ", name, repr(doc))

    # Break up the doc string, scan it for specials.
    lines: list[str] = [ ]

    # The section it's going into.
    section: str | None = None

    # The kind of doc for sphinx.
    doc_type: str | None = None

    for l in doc.split("\n"):

        m = re.match(r':doc: *(\w+) *(\w+)?', l)
        if m:
            section = m.group(1)

            if m.group(2):
                doc_type = m.group(2)

            continue

        m = re.match(r':args: *(.*)', l)
        if m:
            args_or_default = m.group(1)
            continue

        m = re.match(r':default: *(\S+)', l)
        if m:
            args_or_default = m.group(1)
            continue

        m = re.match(r':name: *(\S+)', l)
        if m:
            name = m.group(1)
            continue

        lines.append(l)

    return lines, doc_type, section, name, args_or_default


def scan_section(name, o):
    """
    Scans object o. Assumes it has the name name.
    """

    # For modules also scan for documented variables.
    if isinstance(o, types.ModuleType):
        scan_pep224("", name, o)

    for n in dir(o):
        scan(name + n, getattr(o, n))


def write_line_buffer(incdir='source/inc'):

    for k, v in line_buffer.items():

        f = io.StringIO()

        print(u".. Automatically generated file - do not modify.", file=f)
        print(u"", file=f)

        for l in v:
            print(l, file=f)

        s = f.getvalue()

        fname = os.path.join(incdir, k)
        if os.path.exists(fname):
            with open(fname) as f:
                if f.read() == s:
                    print("Retaining", k)
                    continue

        print("Generating", k)

        with open(fname, "w") as f:
            f.write(s)


name_kind = collections.defaultdict(str)


def scan_docs(srcdir='source', incdir='source/inc'):
    """
    Scans the documentation for functions, classes, and variables.
    """

    def scan_file(fn):
        f = open(fn)

        for l in f:
            m = re.search(r"\.\. (\w+):: ([.\w+]+)", l)

            if not m:
                continue

            name_kind[m.group(2)] = m.group(1)

    for i in os.listdir(srcdir):
        if i.endswith(".rst"):
            scan_file(os.path.join(srcdir, i))

    for i in os.listdir(incdir):
        scan_file(os.path.join(incdir, i))


def format_name(name):

    if name_kind[name] == 'function':
        name = ":func:`{}`".format(name)
    elif name_kind[name] == 'class':
        name = ":class:`{}`".format(name)
    elif name_kind[name] == 'var':
        name = ":var:`{}`".format(name)

    return name


def write_reserved(module, dest, ignore_builtins):

    with open(dest, "w") as f:

        for i in sorted(dir(module)):

            if i == "doc":
                continue

            if i.startswith("_"):
                continue

            if ignore_builtins and hasattr(builtins, i):
                continue

            f.write("* " + format_name(i) + "\n")


def write_pure_const(incdir='source/inc'):

    def write_set(f, s):
        l = list(s)
        l.sort()

        for i in l:
            f.write("* " + format_name(i) + "\n")

    pure = renpy.pyanalysis.pure_functions # @UndefinedVariable
    constants = renpy.pyanalysis.constants - pure # @UndefinedVariable

    with open(os.path.join(incdir, "pure_vars"), "w") as f:
        write_set(f, pure)

    with open(os.path.join(incdir, "const_vars"), "w") as f:
        write_set(f, constants)


def write_easings(ns, incdir='source/inc'):

    with open(os.path.join(incdir, "easings"), "w") as f:
        f.write(".. csv-table::\n")
        f.write('    :header: "Ren\'Py Name", "easings.net Name"\n')
        f.write('\n')

        for name in sorted(dir(ns)):
            if not name.startswith("ease"):
                continue
            if not "_" in name:
                continue

            stdname = name.replace("ease_", "easeInOut_").replace("easein_", "easeOut_").replace("easeout_", "easeIn_")
            f.write('    "{}", "{}"\n'.format(name, stdname))


def tq_script(name, srcdir='source'):

    with open(os.path.join(srcdir, "../../the_question/game", name), "r") as f:
        lines = f.readlines()
        lines = [ ("    " + i).rstrip() for i in lines ]
        return "\n".join(lines)


def write_tq(srcdir='source'):
    script = tq_script("script.rpy", srcdir=srcdir)
    options = tq_script("options.rpy", srcdir=srcdir)

    with open(os.path.join(srcdir, "thequestion.txt"), "r") as f:
        template = f.read()

    with open(os.path.join(srcdir, "thequestion.rst"), "w") as f:
        f.write(template.format(script=script, options=options))


def check_dups():

    duplicates = False

    for v in documented.values():
        if len(v) >= 2:
            duplicates = True

            print(" and ".join(v), "are duplicate.")

    if duplicates:
        raise SystemExit(1)
