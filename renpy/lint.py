# Copyright 2004-2022 Tom Rothamel <pytom@bishoujo.us>
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

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode # *


import codecs
import time
import re
import sys
import collections
import textwrap
import builtins

import renpy

python_builtins = set(dir(builtins))
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

# Collect define/default statements to check for duplication
all_define_statments = {}
all_default_statements = {}

# True if at east one error was reported, false otherwise.
error_reported = False

# Reports a message to the user.


def report(msg, *args):
    if report_node:
        out = u"%s:%d " % (renpy.parser.unicode_filename(report_node.filename), report_node.linenumber)
    else:
        out = ""

    out += msg % args
    print("")
    print(out)

    global error_reported
    error_reported = True


added = { }

# Reports additional information about a message, the first time it
# occurs.


def add(msg, *args):
    if not msg in added:
        added[msg] = True
        msg = str(msg) % args
        print(msg)


# Tries to evaluate an expression, announcing an error if it fails.
def try_eval(where, expr, additional=None):
    """
    :doc: lint

    Tries to evaluate an expression, and writes an error to lint.txt if
    it fails.

    `where`
        A string giving the location the expression is found. Used to
        generate an error message of the form "Could not evaluate `expr`
        in `where`."

    `expr`
        The expression to try evaluating.

    `additional`
        If given, an additional line of information that is addded to the
        error message.
    """

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

    report("Could not evaluate '%s', in %s.", expr, where)
    if additional:
        add(additional)

# Returns True of the expression can be compiled as python, False
# otherwise.


def try_compile(where, expr, additional=None):
    """
    :doc: lint

    Tries to compile an expression, and writes an error to lint.txt if
    it fails.

    `where`
        A string giving the location the expression is found. Used to
        generate an error message of the form "Could not evaluate `expr`
        in `where`."

    `expr`
        The expression to try compiling.

    `additional`
        If given, an additional line of information that is addded to the
        error message.
    """

    try:
        renpy.python.py_compile_eval_bytecode(expr)
    except Exception:
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

    for im, d in renpy.display.image.images.items():

        if im[0] != nametag:
            continue

        attrs = set(im[1:])

        if [ i for i in banned if i in attrs ]:
            continue

        li = getattr(d, "_list_attributes", None)

        if li is not None:
            attrs = attrs | set(li(im[0], required))

        if [ i for i in required if i not in attrs ]:
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

    required = set()
    banned = set()

    for i in name[1:]:
        if i[0] == "-":
            banned.add(i[1:])
        else:
            required.add(i)

    for im, d in renpy.display.image.images.items():

        if im[0] != nametag:
            continue

        attrs = set(im[1:])

        if attrs - required:
            continue

        rest = required - attrs

        if rest:

            try:
                da = renpy.display.core.DisplayableArguments()
                da.name = (im[0],) + tuple(i for i in name[1:] if i in attrs)
                da.args = tuple(i for i in name[1:] if i in rest)
                da.lint = True
                d._duplicate(da)
            except Exception:
                continue

        precise_cache.add(name)

        return True

    return False


# This reports an error if we're sure that the image with the given name
# does not exist.
def image_exists(name, expression, tag, precise=True):
    """
    Checks a scene or show statement for image existence.
    """

    orig = name
    f = renpy.config.adjust_attributes.get(name[0], None) or renpy.config.adjust_attributes.get(None, None)
    if f is not None:
        name = f(name)

    # Add the tag to the set of known tags.
    tag = tag or name[0]
    image_prefixes[tag] = True

    if expression:
        return

    if not precise:
        if image_exists_imprecise(name):
            return

    # If we're not precise, then we have to start looking for images
    # that we can possibly match.
    if image_exists_precise(name):
        return

    report("'%s' is not an image.", " ".join(orig))


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
            d.visit_all(lambda a: a.predict_one())
    except Exception:
        pass

    for fn in files:
        check_file(what, fn)


# Lints ast.Image nodes.
def check_image(node):

    name = " ".join(node.imgname)

    check_displayable('image %s' % name, renpy.display.image.images[node.imgname])


def imspec(t):
    if len(t) == 3:
        return t[0], None, None, t[1], t[2], 0, None
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

    layer = renpy.exports.default_layer(layer, tag or name)

    if layer not in renpy.config.layers and layer not in renpy.config.top_layers:
        report("Uses layer '%s', which is not in config.layers.", layer)

    image_exists(name, expression, tag, precise=precise)

    for i in at_list:
        try_eval("the at list of a scene or show statment", i, "Perhaps you forgot to define or misspelled a transform.")


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

    layer = renpy.exports.default_layer(layer, tag)

    if layer not in renpy.config.layers and layer not in renpy.config.top_layers:
        report("Uses layer '%s', which is not in config.layers.", layer)

    if tag not in image_prefixes:
        report("The image tag '%s' is not the prefix of a declared image, nor was it used in a show statement before this hide statement.", tag)


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
    except Exception:
        report("Didn't properly report what the next statement should be.")


def quote_text(s):

    s = s.replace("\\", "\\\\")
    s = s.replace("\"", "\\\"")
    s = s.replace("\t", "\\t")
    s = s.replace("\n", "\\n")

    return "\"" + s + "\""


def text_checks(s):

    msg = renpy.text.extras.check_text_tags(s)
    if msg:
        report("%s (in %s)", msg, quote_text(s))

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
                    report("Unknown string format code '%s' (in %s)", fmt, quote_text(s))
                    state = 0

            # In a mapping key.
            elif state == 2:
                fmt += c
                if c == ")":
                    state = 1

        if state != 0:
            report("Unterminated string format code '%s' (in %s)", fmt, quote_text(s))


def check_say(node):

    if node.who:
        try:
            char = renpy.ast.eval_who(node.who)
        except Exception:
            report("Could not evaluate '%s' in the who part of a say statement.", node.who)
            add("Perhaps you forgot to define a character?")
            char = None
    else:
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

    if char.image_tag is None:
        return

    for attributes in (node.attributes, node.temporary_attributes):
        if attributes is None:
            continue

        name = (char.image_tag,) + attributes

        orig = name
        f = renpy.config.adjust_attributes.get(name[0], None) or renpy.config.adjust_attributes.get(None, None)
        if f is not None:
            name = f(name)

        if image_exists_imprecise(name):
            continue

        if image_exists_imprecise(('side',) + name):
            continue

        report("Could not find image (%s) corresponding to attributes on say statement.", " ".join(orig))


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

    if node.store == "store.persistent" and kind == "define":
        report("Define should not be used with a persistent variable. Use default persistent.%s = ... instead.", node.varname)
        return

    if node.store != 'store':
        return

    if node.varname in renpy.config.lint_ignore_replaces:
        return

    if node.varname in python_builtins:
        report("'%s %s' replaces a python built-in name, which may cause problems.", kind, node.varname)

    if node.varname in renpy_builtins:
        report("'%s %s' replaces a Ren'Py built-in name, which may cause problems.", kind, node.varname)


def check_redefined(node, kind):
    """
    Check if a define or default statement has already been created.
    """
    if kind == 'default':
        scanned = all_default_statements
    elif kind == 'define':
        scanned = all_define_statments

        if not (node.operator == "=" and node.index is None):
            return
    else:
        return

    # Combine store name and varname

    store_name = node.store
    if store_name.startswith("store."):
        store_name = store_name[6:]

    if store_name:
        full_name = "{}.{}".format(store_name, node.varname)
    else:
        full_name = node.varname

    if full_name in renpy.config.lint_ignore_redefine:
        return

    original_node = scanned.get(full_name)
    if original_node:
        report(
            "{} {} already defined at {}:{}".format(
                kind,
                full_name,
                original_node.filename,
                original_node.linenumber,
            )
        )
    scanned[full_name] = node


def check_style_property_displayable(name, property, d):

    if not d._duplicatable:
        check_displayable(
            "{}, property {}".format(name, property),
            d)
        return

    renpy.style.init_inspect()

    def sort_short(l):
        l = list(l)
        l.sort(key=len)
        return l

    alts = sort_short(renpy.style.prefix_alts)

    for p in sort_short(renpy.style.affects.get(property, [ ])):
        for prefix in alts:
            rest = p[len(prefix):]
            if rest in renpy.style.all_properties:
                args = d._args.copy(prefix=prefix)
                dd = d._duplicate(args)
                dd._unique()

                check_displayable(
                    "{}, property {}".format(name, prefix + property),
                    dd)

                break

        # print property, p


def check_style(name, s):

    for p in s.properties:
        for k, v in p.items():

            # Treat font specially.
            if k.endswith("font"):
                if isinstance(v, renpy.text.font.FontGroup):
                    for f in set(v.map.values()):
                        check_file(name, f)
                else:
                    check_file(name, v)

            if isinstance(v, renpy.display.core.Displayable):
                check_style_property_displayable(name, k, v)


def check_label(node):

    def add_arg(n):
        if n is None:
            return

        if not hasattr(renpy.store, n):
            setattr(renpy.store, n, None)

    pi = node.parameters

    if pi is not None:

        for i, _ in pi.parameters:
            add_arg(i)

        add_arg(pi.extrapos)
        add_arg(pi.extrakw)


def check_screen(node):

    if (node.screen.parameters is None) and renpy.config.lint_screens_without_parameters:
        report("The screen %s has not been given a parameter list.", node.screen.name)
        add("This can be fixed by writing 'screen %s():' instead.", node.screen.name)


def check_styles():
    for full_name, s in renpy.style.styles.items(): # @UndefinedVariable
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
        except Exception:
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

def report_character_stats(charastats):
    """
    Returns a list of character stat lines.
    """

    # Keep all the statistics in a list, so that it gets wrapped ionto a
    rv = [ "Character statistics (for default language):" ]

    count_to_char = collections.defaultdict(list)

    for char, count in charastats.items():
        count_to_char[count].append(char)

    for count, chars in sorted(count_to_char.items(), reverse=True):
        chars.sort()

        if len(chars) == 1:
            start = chars[0] + " has "
        elif len(chars) == 2:
            start = chars[0] + " and " + chars[1] + " have "
        else:
            start = ", ".join(chars[:-1]) + ", and " + chars[-1] + " have "

        rv.append(
            " * " + start + humanize(count) +
            (" block " if count == 1 else " blocks ") + "of dialogue" +
            (" each." if len(chars) > 1 else ".")
            )

    return rv


def lint():
    """
    The master lint function, that's responsible for staging all of the
    other checks.
    """

    ap = renpy.arguments.ArgumentParser(description="Checks the script for errors and prints script statistics.", require_command=False)
    ap.add_argument("filename", nargs='?', action="store", help="The file to write to.")
    ap.add_argument("--error-code", action="store_true", help="If given, the error code is 0 if the game has no lint errros, 1 if lint errors are found.")

    args = ap.parse_args()

    if args.filename:
        f = open(args.filename, "w", encoding="utf-8")
        sys.stdout = f

    renpy.game.lint = True

    print("\ufeff" + renpy.version + " lint report, generated at: " + time.ctime())

    # Populate default statement values.
    renpy.exports.execute_default_statement(True)

    # Initialise store and values set by start callbacks.
    renpy.exports.call_in_new_context('_start_store')

    # This supports check_hide.
    global image_prefixes
    image_prefixes = { }

    for k in renpy.display.image.images:
        image_prefixes[k[0]] = True

    # Iterate through every statement in the program, processing
    # them. We sort them in filename, linenumber order.

    all_stmts = list(renpy.game.script.all_stmts)
    all_stmts.sort(key=lambda n : n.filename)

    # The current count.
    counts = collections.defaultdict(Count)

    charastats = collections.defaultdict(int)

    # The current language.
    language = None

    menu_count = 0
    screen_count = 0
    image_count = 0

    global report_node

    for node in all_stmts:
        if isinstance(node, (renpy.ast.Show, renpy.ast.Scene)):
            precheck_show(node)

    for node in all_stmts:

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
            if language is None:
                charastats[node.who if node.who else 'narrator' ] += 1

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
            check_screen(node)

        elif isinstance(node, renpy.ast.Define):
            check_define(node, "define")
            check_redefined(node, "define")

        elif isinstance(node, renpy.ast.Default):
            check_define(node, "default")
            check_redefined(node, "default")

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

    print("")
    print("")
    print("Statistics:")
    print("")

    languages = list(counts)
    languages.sort(key=lambda a : "" if not a else a)
    for i in languages:
        report_language(i)

    lines.append("The game contains {0} menus, {1} images, and {2} screens.".format(
        humanize(menu_count), humanize(image_count), humanize(screen_count)))

    if renpy.config.developer and renpy.config.lint_character_statistics:
        lines.append(report_character_stats(charastats))

    # Format the lines and lists of lines.
    for l in lines:
        if not isinstance(l, (tuple, list)):
            l = (l,)

        for ll in l:

            if ll.startswith(" * "):
                prefix = " * "
                altprefix = "   "
                ll = ll[3:]
            else:
                prefix  = ""
                altprefix = ""

            for lll in textwrap.wrap(ll, 78 - len(prefix)):
                print(prefix + lll)
                prefix = altprefix

        print("")

    for i in renpy.config.lint_stats_callbacks:
        i()

    print("")
    if renpy.config.developer and (renpy.config.original_developer != "auto"):
        print("Remember to set config.developer to False before releasing.")
        print("")

    print("Lint is not a substitute for thorough testing. Remember to update Ren'Py")
    print("before releasing. New releases fix bugs and improve compatibility.")

    if error_reported and args.error_code:
        renpy.exports.quit(status=1)

    return False
