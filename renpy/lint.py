# Copyright 2004-2015 Tom Rothamel <pytom@bishoujo.us>
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

import renpy.display
import renpy.text
import codecs
import time
import re
import sys
import collections
import textwrap

import __builtin__

python_builtins = set(dir(__builtin__))
renpy_builtins = set()

image_prefixes = None

# Things to check in lint.
#
# Image files exist, and are of the right case.
# Jump/Call targets defined.
# Say whos can evaluate.
# Call followed by say.
# Show/Scene valid.
# At valid.
# With valid.
# Hide maybe valid.
# Expressions can compile.

# The node the report will be about:
report_node = None

# Reports a message to the user.
def report(msg, *args):
    if report_node:
        out = u"%s:%d " % (renpy.parser.unicode_filename(report_node.filename), report_node.linenumber)
    else:
        out = ""

    out += msg % args
    print
    print out.encode('utf-8')

added = { }

# Reports additional information about a message, the first time it
# occurs.
def add(msg):
    if not msg in added:
        added[msg] = True
        print unicode(msg).encode('utf-8')


# Trys to evaluate an expression, announcing an error if it fails.
def try_eval(where, expr, additional=None):

    # Make sure the expression compiles.
    try_compile(where, expr)

    # Simply look up the first component of the python expression, and
    # see if it exists in the store.
    m = re.match(r'\s*([a-zA-Z_]\w*)', expr)

    if not m:
        return

    if hasattr(renpy.store, m.group(1)):
        return

    if m.group(1) in __builtins__:
        return

    report( "Could not evaluate '%s', in %s.", expr, where)
    if additional:
        add(additional)

# Returns True of the expression can be compiled as python, False
# otherwise.
def try_compile(where, expr, additional=None):

    try:
        renpy.python.py_compile_eval_bytecode(expr)
    except:
        report("'%s' could not be compiled as a python expression, %s.", expr, where)
        if additional:
            add(additional)


# The sets of names + attributes that we know are valid.
imprecise_cache = set()

def image_exists_imprecise(name):
    """
    Returns true if the image is a plausible image that can be used in a show
    statement. This returns true if at least one image exists with the same
    tag and containing all of the attributes (and none of the removed attributes).
    """


    if name in imprecise_cache:
        return True

    nametag = name[0]

    required = set()
    banned = set()

    for i in name[1:]:
        if i[0] == "-":
            banned.add(i[1:])
        else:
            required.add(i)

    for im in renpy.display.image.images:

        if im[0] != nametag:
            continue

        attrs = set(im[1:])

        if [ i for i in required if i not in attrs ]:
            continue

        if [ i for i in banned if i in attrs ]:
            continue

        imprecise_cache.add(name)
        return True

    return False


precise_cache = set()

def image_exists_precise(name):
    """
    Returns true if an image exists with the same tag and attributes as
    `name`. (The attributes are allowed to occur in any order.)
    """

    if name in precise_cache:
        return True

    nametag = name[0]

    required = set(name[1:])

    for im in renpy.display.image.images:

        if im[0] != nametag:
            continue

        attrs = set(im[1:])

        if attrs == required:
            precise_cache.add(name)
            return True

    return False


# This reports an error if we're sure that the image with the given name
# does not exist.
def image_exists(name, expression, tag, precise=True):
    """
    Checks a scene or show statement for image existence.
    """

    # Add the tag to the set of known tags.
    tag = tag or name[0]
    image_prefixes[tag] = True

    if expression:
        return

    namelist = list(name)
    names = " ".join(namelist)

    # Look for the precise name.
    while namelist:
        if tuple(namelist) in renpy.display.image.images:
            return

        namelist.pop()

    # If we're not precise, then we have to start looking for images
    # that we can possibly match.
    if precise:
        if image_exists_precise(name):
            return
    else:
        if image_exists_imprecise(name):
            return

    report("The image named '%s' was not declared.", names)

# Only check each file once.
check_file_cache = { }

def check_file(what, fn):

    present = check_file_cache.get(fn, None)
    if present is True:
        return
    if present is False:
        report("%s uses file '%s', which is not loadable.", what.capitalize(), fn)
        return

    if not renpy.loader.loadable(fn):
        report("%s uses file '%s', which is not loadable.", what.capitalize(), fn)
        check_file_cache[fn] = False
        return

    check_file_cache[fn] = True


def check_displayable(what, d):

    def predict_image(img):
        files.extend(img.predict_files())

    renpy.display.predict.image = predict_image

    files = [ ]

    try:
        if isinstance(d, renpy.display.core.Displayable):
            d.visit_all(lambda a : a.predict_one())
    except:
        pass

    for fn in files:
        check_file(what, fn)


# Lints ast.Image nodes.
def check_image(node):

    name = " ".join(node.imgname)

    check_displayable('image %s' % name, renpy.display.image.images[node.imgname])

def imspec(t):
    if len(t) == 3:
        return t[0], None, None, t[1], t[2], 0
    if len(t) == 6:
        return t[0], t[1], t[2], t[3], t[4], t[5], None
    else:
        return t


# Lints ast.Show and ast.Scene nodes.
def check_show(node, precise):

    # A Scene may have an empty imspec.
    if not node.imspec:
        return

    name, expression, tag, at_list, layer, _zorder, _behind = imspec(node.imspec)

    if layer not in renpy.config.layers and layer not in renpy.config.top_layers:
        report("Uses layer '%s', which is not in config.layers.", layer)

    image_exists(name, expression, tag, precise=precise)

    for i in at_list:
        try_eval("the at list of a scene or show statment", i, "Perhaps you forgot to declare, or misspelled, a position?")


def precheck_show(node):
    # A Scene may have an empty imspec.
    if not node.imspec:
        return

    tag = imspec(node.imspec)[2]
    image_prefixes[tag] = True


# Lints ast.Hide.

def check_hide(node):

    name, _expression, tag, _at_list, layer, _zorder, _behind = imspec(node.imspec)

    tag = tag or name[0]

    if layer not in renpy.config.layers and layer not in renpy.config.top_layers:
        report("Uses layer '%s', which is not in config.layers.", layer)

    if tag not in image_prefixes:
        report("The image tag '%s' is not the prefix of a declared image, nor was it used in a show statement before this hide statement.", tag)

    # for i in at_list:
    #    try_eval(node, "at list of hide statment", i)

def check_with(node):
    try_eval("a with statement or clause", node.expr, "Perhaps you forgot to declare, or misspelled, a transition?")

def check_user(node):

    def error(msg):
        report("%s", msg)

    renpy.exports.push_error_handler(error)
    try:
        node.call("lint")
    finally:
        renpy.exports.pop_error_handler()

    try:
        node.get_next()
    except:
        report("Didn't properly report what the next statement should be.")

def text_checks(s):
    msg = renpy.text.extras.check_text_tags(s)
    if msg:
        report("%s (in %s)", msg, repr(s)[1:])

    if "%" in s and renpy.config.old_substitutions:

        state = 0
        pos = 0
        fmt = ""
        while pos < len(s):
            c = s[pos]
            pos += 1

            # Not in a format.
            if state == 0:
                if c == "%":
                    state = 1
                    fmt = "%"

            # In a format.
            elif state == 1:
                fmt += c
                if c == "(":
                    state = 2
                elif c in "#0123456780- +hlL":
                    state = 1
                elif c in "diouxXeEfFgGcrs%":
                    state = 0
                else:
                    report("Unknown string format code '%s' (in %s)", fmt, repr(s)[1:])
                    state = 0

            # In a mapping key.
            elif state == 2:
                fmt += c
                if c == ")":
                    state = 1

        if state != 0:
            report("Unterminated string format code '%s' (in %s)", fmt, repr(s)[1:])

def check_say(node):

    if node.who:
        try:
            char = renpy.ast.eval_who(node.who)
        except:
            report("Could not evaluate '%s' in the who part of a say statement.", node.who)
            add("Perhaps you forgot to define a character?")
            char = None

    if node.with_:
        try_eval("the with clause of a say statement", node.with_, "Perhaps you forgot to declare, or misspelled, a transition?")

    text_checks(node.what)

    if not node.who_fast:
        return

    # Code to check image attributes. (If we're lucky.)
    if node.who is None:
        return

    if not isinstance(char, renpy.character.ADVCharacter):
        return

    if node.attributes is None:
        return

    if char.image_tag is None:
        return

    name = (char.image_tag,) + node.attributes

    if image_exists_imprecise(name):
        return

    if image_exists_imprecise(('side', ) + name):
        return

    report("Could not find image (%s) corresponding to attributes on say statement.", " ".join(name))


def check_menu(node):

    if node.with_:
        try_eval("the with clause of a menu statement", node.with_, "Perhaps you forgot to declare, or misspelled, a transition?")

    if not [ (l, c, b) for l, c, b in node.items if b ]:
        report("The menu does not contain any selectable choices.")

    for l, c, b in node.items:
        if c:
            try_compile("in the if clause of a menuitem", c)

        text_checks(l)

def check_jump(node):

    if node.expression:
        return

    if not renpy.game.script.has_label(node.target):
        report("The jump is to nonexistent label '%s'.", node.target)

def check_call(node):

    if node.expression:
        return

    if not renpy.game.script.has_label(node.label):
        report("The call is to nonexistent label '%s'.", node.label)

def check_while(node):
    try_compile("in the condition of the while statement", node.condition)

def check_if(node):

    for condition, _block in node.entries:
        try_compile("in a condition of the if statement", condition)

def check_define(node, kind):
    if node.store != 'store':
        return

    if node.varname in renpy.config.lint_ignore_replaces:
        return

    if node.varname in python_builtins:
        report("'%s %s' replaces a python built-in name, which may cause problems.", kind, node.varname)

    if node.varname in renpy_builtins:
        report("'%s %s' replaces a Ren'Py built-in name, which may cause problems.", kind, node.varname)


def check_style(name, s):

    for p in s.properties:
        for k, v in p.iteritems():

            kname = name + ", property " + k

            # Treat font specially.
            if k.endswith("font"):
                check_file(name, v)

            if isinstance(v, renpy.display.core.Displayable):
                check_displayable(kname, v)

def check_label(node):

    def add_arg(n):
        if n is None:
            return

        if not hasattr(renpy.store, n):
            setattr(renpy.store, n, None)

    pi = node.parameters

    if pi is not None:

        for i in pi.positional:
            add_arg(i)
        add_arg(pi.extrapos)
        add_arg(pi.extrakw)


def check_styles():
    for full_name, s in renpy.style.styles.iteritems(): # @UndefinedVariable
        name = "style." + full_name[0]
        for i in full_name[1:]:
            name += "[{!r}]".format(i)

        check_style("Style " + name, s)

def humanize(n):
    s = str(n)

    rv = []

    for i, c in enumerate(reversed(s)):
        if i and not (i % 3):
            rv.insert(0, ',')

        rv.insert(0, c)

    return ''.join(rv)

def check_filename_encodings():
    """
    Checks files to ensure that they are displayable in unicode.
    """

    for _dirname, filename in renpy.loader.listdirfiles():
        try:
            filename.encode("ascii")
            continue
        except:
            pass

        report("%s contains non-ASCII characters in its filename.", filename)
        add("(ZIP file distributions can only reliably include ASCII filenames.)")

class Count(object):
    """
    Stores information about the word count.
    """

    def __init__(self):
        # The number of blocks of text.
        self.blocks = 0

        # The number of whitespace-separated words.
        self.words = 0

        # The number of characters.
        self.characters = 0

    def add(self, s):
        self.blocks += 1
        self.words += len(s.split())
        self.characters += len(s)

def common(n):
    """
    Returns true if the node is in the common directory.
    """

    filename = n.filename.replace("\\", "/")

    if filename.startswith("common/") or filename.startswith("renpy/common/"):
        return True
    else:
        return False

def lint():
    """
    The master lint function, that's responsible for staging all of the
    other checks.
    """

    ap = renpy.arguments.ArgumentParser(description="Checks the script for errors and prints script statistics.", require_command=False)
    ap.add_argument("filename", nargs='?', action="store", help="The file to write to.")

    args = ap.parse_args()

    if args.filename:
        f = open(args.filename, "w")
        sys.stdout = f

    renpy.game.lint = True

    print codecs.BOM_UTF8
    print unicode(renpy.version + " lint report, generated at: " + time.ctime()).encode("utf-8")

    # This supports check_hide.
    global image_prefixes
    image_prefixes = { }

    for k in renpy.display.image.images:
        image_prefixes[k[0]] = True

    # Iterate through every statement in the program, processing
    # them. We sort them in filename, linenumber order.

    all_stmts = [ (i.filename, i.linenumber, i) for i in renpy.game.script.all_stmts ]
    all_stmts.sort()

    # The current count.
    counts = collections.defaultdict(Count)

    # The current language.
    language = None

    menu_count = 0
    screen_count = 0
    image_count = 0

    global report_node

    for _fn, _ln, node in all_stmts:
        if isinstance(node, (renpy.ast.Show, renpy.ast.Scene)):
            precheck_show(node)

    for _fn, _ln, node in all_stmts:

        if common(node):
            continue

        report_node = node

        if isinstance(node, renpy.ast.Image):
            image_count += 1
            check_image(node)

        elif isinstance(node, renpy.ast.Show):
            check_show(node, False)

        elif isinstance(node, renpy.ast.Scene):
            check_show(node, True)

        elif isinstance(node, renpy.ast.Hide):
            check_hide(node)

        elif isinstance(node, renpy.ast.With):
            check_with(node)

        elif isinstance(node, renpy.ast.Say):
            check_say(node)

            counts[language].add(node.what)


        elif isinstance(node, renpy.ast.Menu):
            check_menu(node)
            menu_count += 1

        elif isinstance(node, renpy.ast.Jump):
            check_jump(node)

        elif isinstance(node, renpy.ast.Call):
            check_call(node)

        elif isinstance(node, renpy.ast.While):
            check_while(node)

        elif isinstance(node, renpy.ast.If):
            check_if(node)

        elif isinstance(node, renpy.ast.UserStatement):
            check_user(node)

        elif isinstance(node, renpy.ast.Label):
            check_label(node)

        elif isinstance(node, renpy.ast.Translate):
            language = node.language

        elif isinstance(node, renpy.ast.EndTranslate):
            language = None

        elif isinstance(node, renpy.ast.Screen):
            screen_count += 1

        elif isinstance(node, renpy.ast.Define):
            check_define(node, "define")

        elif isinstance(node, renpy.ast.Default):
            check_define(node, "default")



    report_node = None

    check_styles()
    check_filename_encodings()

    for f in renpy.config.lint_hooks:
        f()


    lines = [ ]

    def report_language(language):

        count = counts[language]

        if count.blocks <= 0:
            return

        if language is None:
            s = "The game"
        else:
            s = "The {0} translation".format(language)

        s += """ contains {0} dialogue blocks, containing {1} words
and {2} characters, for an average of {3:.1f} words and {4:.0f}
characters per block. """.format(
            humanize(count.blocks),
            humanize(count.words),
            humanize(count.characters),
            1.0 * count.words / count.blocks,
            1.0 * count.characters / count.blocks)

        lines.append(s)


    print
    print
    print "Statistics:"
    print

    languages = list(counts)
    languages.sort()
    for i in languages:
        report_language(i)

    lines.append("The game contains {0} menus, {1} images, and {2} screens.".format(
        humanize(menu_count), humanize(image_count), humanize(screen_count)))

    for l in lines:
        for ll in textwrap.wrap(l, 78):
            print ll.encode("utf-8")

        print

    print
    if renpy.config.developer:
        print "Remember to set config.developer to False before releasing."
        print

    print "Lint is not a substitute for thorough testing. Remember to update Ren'Py"
    print "before releasing. New releases fix bugs and improve compatibility."

    return False

