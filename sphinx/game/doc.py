import inspect
import re
import collections
import keyword
import renpy
import shutil

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
"""


def write_keywords():
    f = file("source/keywords.py", "w")

    kwlist = list(keyword.kwlist)
    kwlist.extend(KEYWORD1.split())
    kwlist.extend(KEYWORD2.split())

    kwlist.sort()

    f.write("keywords = %r\n" % kwlist)

    properties = list(i for i in renpy.screenlang.all_keyword_names if i not in kwlist)
    properties.sort()

    f.write("properties = %r\n" % properties)

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
    lines = []

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
            print "Warning: %s has section but not args." % name

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

        print "Generating", k

        f = file("source/inc/" + k, "w")

        print >>f, ".. Automatically generated file - do not modify."
        print >>f

        for l in v:
            print >>f, l

        f.close()
