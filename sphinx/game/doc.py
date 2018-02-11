from __future__ import print_function

import inspect
import re
import collections
import keyword
import renpy.sl2
import shutil
import StringIO
import os

import __builtin__

# Keywords in the Ren'Py script language.
KEYWORD1 = """\
$
as
at
behind
call
expression
hide
if
in
image
init
jump
menu
onlayer
python
return
scene
set
show
with
while
zorder
transform
play
queue
stop
pause
define
screen
label
voice
translate
"""

# Words that are sometimes statement keywords, like for ATL
# or Screen language statements.
KEYWORD2 = """\
nvl
window
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
null
text
hbox
vbox
fixed
grid
side
frame
key
timer
input
button
imagebutton
textbutton
bar
vbar
viewport
imagemap
hotspot
hotbar
transform
add
use
has
style
"""


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
    items.sort(key=lambda a : ( tuple(sorted(a[1])), a[0][1] ) )

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
    f = file("source/keywords.py", "w")

    kwlist = list(keyword.kwlist)
    kwlist.extend(KEYWORD1.split())
    kwlist.extend(KEYWORD2.split())

    kwlist.sort()

    f.write("keywords = %r\n" % kwlist)

    properties = [ i for i in expanded_sl2_properties() if i not in kwlist ]

    f.write("properties = %r\n" % properties)

    f.write("property_regexes = %r\n" % sl2_regexps())

    f.close()

    shutil.copy("source/keywords.py", "../tutorial/game/keywords.py")


# A map from filename to a list of lines that are supposed to go into
# that file.
line_buffer = collections.defaultdict(list)


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
            except:
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
        for i in dir(o):
            scan(i, getattr(o, i), prefix + "    ")


def scan_section(name, o):
    """
    Scans object o. Assumes it has the name name.
    """

    for n in dir(o):
        scan(name + n, getattr(o, n))


def write_line_buffer():

    for k, v in line_buffer.iteritems():

        # f = file("source/inc/" + k, "w")

        f = StringIO.StringIO()

        print(".. Automatically generated file - do not modify.", file=f)
        print(file=f)

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

    print("Writing", dest)

    with open(dest, "w") as f:

        for i in sorted(dir(module)):

            if i == "doc":
                continue

            if i.startswith("_"):
                continue

            if ignore_builtins and hasattr(__builtin__, i):
                continue

            f.write("* " + format_name(i) + "\n")


def write_pure_const():

    def write_set(f, s):
        l = list(s)
        l.sort()

        for i in l:
            f.write("* " + format_name(i) + "\n")

    pure = renpy.pyanalysis.pure_functions  # @UndefinedVariable
    constants = renpy.pyanalysis.constants - pure  # @UndefinedVariable

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
