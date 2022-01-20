from __future__ import print_function, unicode_literals

import inspect
import re
import collections
import keyword
import renpy.sl2
import shutil
import io
import os
import textwrap

try:
    import builtins
except ImportError:
    import __builtin__ as builtins

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

    for i in renpy.sl2.slparser.all_statements:
        rv.add(i.name)

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
            part1 = "(?:" + "|".join(prefixes) + ")"
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


def write_keywords():
    f = open("source/keywords.py", "w")

    kwlist = set(keyword.kwlist)
    kwlist |= script_keywords()
    kwlist |= sl2_keywords()
    kwlist |= set(ATL_KEYWORDS.split())
    kwlist |= set(SCRIPT_KEYWORDS.split())
    kwlist |= set(SL2_KEYWORDS.split())
    kwlist |= set(LI_KEYWORDS.split())

    kwlist = list(kwlist)

    kwlist.sort()

    f.write("keywords = %r\n" % kwlist)
    f.write("keyword_regex = %r\n" % ("|".join(re.escape(i) for i in kwlist)))

    properties = [ i for i in expanded_sl2_properties() if i not in kwlist ]

    f.write("properties = %r\n" % properties)

    f.write("property_regexes = %r\n" % sl2_regexps())

    f.close()

    shutil.copy("source/keywords.py", "../tutorial/game/keywords.py")


# A map from filename to a list of lines that are supposed to go into
# that file.
line_buffer = collections.defaultdict(list)

# A map from id(o) to the names it's documented under.
documented = collections.defaultdict(list)

# This keeps all objectsd we see alive, to prevent duplicates in documented.
documented_list = [ ]


def scan(name, o, prefix=""):

    doc_type = "function"

    # The section it's going into.
    section = None

    # The formatted arguments.
    args = None

    # Get the function's docstring.
    doc = inspect.getdoc(o)

    if not doc:
        return

    if doc[0] == ' ':
        print("Bad docstring for ", name, repr(doc))

    if re.match(r'[\w\.]+\(', doc):
        doc = doc.partition("\n\n")[2]
        doc = textwrap.dedent(doc)

    # Break up the doc string, scan it for specials.
    lines = [ ]

    for l in doc.split("\n"):

        m = re.match(r':doc: *(\w+) *(\w+)?', l)
        if m:
            section = m.group(1)

            if m.group(2):
                doc_type = m.group(2)

            continue

        m = re.match(r':args: *(.*)', l)
        if m:
            args = m.group(1)
            continue

        m = re.match(r':name: *(\S+)', l)
        if m:
            if name != m.group(1):
                return
            continue

        lines.append(l)

    if section is None:
        return

    if args is None:

        # Get the arguments.
        if inspect.isclass(o):
            init = getattr(o, "__init__", None)
            if not init:
                return

            init_doc = inspect.getdoc(init)

            if init_doc and not init_doc.startswith("x.__init__("):
                lines.append("")
                lines.extend(init_doc.split("\n"))

            try:
                args = inspect.getargspec(init)
            except Exception:
                args = None

        elif inspect.isfunction(o):
            args = inspect.getargspec(o)

        elif inspect.ismethod(o):
            args = inspect.getargspec(o)

        else:
            print("Warning: %s has section but not args." % name)

            return

        # Format the arguments.
        if args is not None:

            args = inspect.formatargspec(*args)
            args = args.replace("(self, ", "(")
        else:
            args = "()"

    # Put it into the line buffer.
    lb = line_buffer[section]

    lb.append(prefix + ".. %s:: %s%s" % (doc_type, name, args))

    for l in lines:
        lb.append(prefix + "    " + l)

    lb.append(prefix + "")

    if inspect.isclass(o):
        if (name not in [ "Matrix", "OffsetMatrix", "RotateMatrix", "ScaleMatrix" ]):
            for i in dir(o):
                scan(i, getattr(o, i), prefix + "    ")

    if name == "identity":
        raise Exception("identity")

    documented_list.append(o)
    documented[id(o)].append(name)


def scan_section(name, o):
    """
    Scans object o. Assumes it has the name name.
    """

    for n in dir(o):
        scan(name + n, getattr(o, n))


def write_line_buffer():

    for k, v in line_buffer.items():

        # f = file("source/inc/" + k, "w")

        f = io.StringIO()

        print(u".. Automatically generated file - do not modify.", file=f)
        print(u"", file=f)

        for l in v:
            print(l, file=f)

        s = f.getvalue()

        if os.path.exists("source/inc/" + k):
            with open("source/inc/" + k) as f:
                if f.read() == s:
                    print("Retaining", k)
                    continue

        print("Generating", k)

        with open("source/inc/" + k, "w") as f:
            f.write(s)


name_kind = collections.defaultdict(str)


def scan_docs():
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

    for i in os.listdir("source"):
        if i.endswith(".rst"):
            scan_file(os.path.join("source", i))

    for i in os.listdir("source/inc"):
        scan_file(os.path.join("source", "inc", i))


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


def write_pure_const():

    def write_set(f, s):
        l = list(s)
        l.sort()

        for i in l:
            f.write("* " + format_name(i) + "\n")

    pure = renpy.pyanalysis.pure_functions # @UndefinedVariable
    constants = renpy.pyanalysis.constants - pure # @UndefinedVariable

    with open("source/inc/pure_vars", "w") as f:
        write_set(f, pure)

    with open("source/inc/const_vars", "w") as f:
        write_set(f, constants)


def write_easings(ns):

    with open("source/inc/easings", "w") as f:
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


def tq_script(name):

    with open("../the_question/game/" + name, "r") as f:
        lines = f.readlines()
        lines = [ ("    " + i).rstrip() for i in lines ]
        return "\n".join(lines)


def write_tq():
    script = tq_script("script.rpy")
    options = tq_script("options.rpy")

    with open("source/thequestion.txt", "r") as f:
        template = f.read()

    with open("source/thequestion.rst", "w") as f:
        f.write(template.format(script=script, options=options))


def check_dups():

    duplicates = False

    for v in documented.values():
        if len(v) >= 2:
            duplicates = True

            print(" and ".join(v), "are duplicate.")

    if duplicates:
        raise SystemExit(1)
