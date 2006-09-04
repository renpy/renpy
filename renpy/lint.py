import renpy
import sys
import codecs
import os
import time

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

# Reports a message to the user.
def report(node, msg, *args):
    out = "%s:%d " % (node.filename, node.linenumber)     
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
def try_eval(node, where, expr, additional=None):

    try:
        renpy.python.py_eval(expr)
    except:
        report(node, "Could not evaluate '%s', in %s.", expr, where)
        if additional:
            add(additional)

# Returns True of the expression can be compiled as python, False
# otherwise.
def try_compile(node, where, expr):

    try:
        renpy.python.py_compile_eval_bytecode(expr)
    except:
        report(node, "'%s' could not be compiled as a python expression, %s.", expr, where)
        

# This reports an error if we're sure that the image with the given name
# does not exist.
def image_exists(node, name, expression, tag):

    # Add the tag to the set of known tags.
    tag = tag or name[0]
    image_prefixes[tag] = True

    if expression:
        return

    name = list(name)
    names = " ".join(name)

    while name:
        if tuple(name) in renpy.exports.images:
            return

        name.pop()

    report(node, "The image named '%s' was not declared.", names)
    
            

# Lints ast.Image nodes.
def check_image(node):

    name = " ".join(node.imgname)
    files = [ ]


    def files_callback(img):
        files.extend(img.predict_files())

    renpy.exports.images[node.imgname].predict(files_callback)

    for fn in files:

        if not renpy.loader.loadable(fn):
            report(node, "Image '%s' uses file '%s', which is not loadable.", name, fn)
            continue

        try:
           renpy.loader.transfn(fn)
        except:
            continue

        if renpy.loader.transfn(fn) and \
               fn.lower() in filenames and \
               fn != filenames[fn.lower()]:
            report(node, "Filename case mismatch for image '%s'. '%s' was used in the script, but '%s' was found on disk.", name, fn, filenames[fn.lower()])

            add("Case mismatches can lead to problems on Mac, Linux/Unix, and when archiving images. To fix them, either rename the file on disk, or the filename use in the script.")
            continue

def imspec(t):
    if len(t) == 3:
        return t[0], None, None, t[1], t[2], 0
    else:
        return t


# Lints ast.Show and ast.Scene nodets.
def check_show(node):

    # A Scene may have an empty imspec.
    if not node.imspec:
        return

    name, expression, tag, at_list, layer, zorder = imspec(node.imspec)

    if layer not in renpy.config.layers and layer not in renpy.config.top_layers:
        report(node, "Uses layer '%s', which is not in config.layers.", layer)

    image_exists(node, name, expression, tag)

    for i in at_list:
        try_eval(node, "the at list of a scene or show statment", i, "Perhaps you forgot to declare, or misspelled, a position?")
        

# Lints ast.Hide.

def check_hide(node):

    name, expression, tag, at_list, layer, zorder = imspec(node.imspec)

    tag = tag or name[0]

    if layer not in renpy.config.layers and layer not in renpy.config.top_layers:
        report(node, "Uses layer '%s', which is not in config.layers.", layer)

    if tag not in image_prefixes:
        report(node, "The image tag '%s' is not the prefix of a declared image, nor was it used in a show statement before this hide statement.", tag)

    # for i in at_list:
    #    try_eval(node, "at list of hide statment", i)
        
def check_with(node):
    try_eval(node, "a with statement or clause", node.expr, "Perhaps you forgot to declare, or misspelled, a transition?")


def check_say(node):

    if node.who:
        try_eval(node, "the who part of a say statement", node.who, "Perhaps you forgot to declare a character?")
        
    if node.with:
        try_eval(node, "the with clause of a say statement", node.with, "Perhaps you forgot to declare, or misspelled, a transition?")

def check_menu(node):

    if node.with:
        try_eval(node, "the with clause of a menu statement", node.with, "Perhaps you forgot to declare, or misspelled, a transition?")

    if not [ (l, c, b) for l, c, b in node.items if l ]:
        report(node, "The menu does not contain any selectable choices.")

    for l, c, b in node.items:
        if c:
            try_compile(node, "in the if clause of a menuitem", c)
        

def check_jump(node):

    if node.expression:
        return

    if not renpy.game.script.has_label(node.target):
        report(node, "The jump is to notexistent label '%s'.", node.target)

def check_call(node):

    if not isinstance(node.next.name, basestring):
        report(node, "The call does not have a from clause associated with it.")
        add("You can add from clauses to calls automatically by running the add_from program.")
        add("This is necessary to ensure saves can be loaded even when the script changes.")

    if node.expression:
        return

    if not renpy.game.script.has_label(node.label):
        report(node, "The call is to notexistent label '%s'.", node.label)

def check_while(node):
    try_compile(node, "in the condition of the while statement", node.condition)

def check_if(node):

    for condition, block in node.entries:
        try_compile(node, "in a condition of the if statement", condition)

def lint():
    """
    The master lint function, that's responsible for staging all of the
    other checks.
    """

    print codecs.BOM_UTF8
    print unicode(renpy.version + " lint report, generated at: " + time.ctime()).encode("utf-8")


    # This is used to support the check_image.
    global filenames
    filenames = { }

    for d in renpy.config.searchpath:
        for fn in os.listdir(d):
            filenames[fn.lower()] = fn

    # This supports check_hide.
    global image_prefixes
    image_prefixes = { }

    for k in renpy.exports.images:
        image_prefixes[k[0]] = True

    # Iterate through every statement in the program, processing
    # them. We sort them in filename, linenumber order.
    
    all_stmts = [ (i.filename, i.linenumber, i) for i in renpy.game.script.all_stmts ]
    all_stmts.sort()

    say_words = 0
    say_count = 0
    menu_count = 0
 
    for fn, ln, node in all_stmts:

        if isinstance(node, renpy.ast.Image):
            check_image(node)

        elif isinstance(node, renpy.ast.Show):
            check_show(node)
    
        elif isinstance(node, renpy.ast.Scene):
            check_show(node)

        elif isinstance(node, renpy.ast.Hide):
            check_hide(node)

        elif isinstance(node, renpy.ast.With):
            check_with(node)

        elif isinstance(node, renpy.ast.Say):
            check_say(node)
            say_count += 1
            say_words += len(node.what.split())

    
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

    for f in renpy.config.lint_hooks:
        f()
            
    print
    print
    print "Statistics:"
    print
    print "The game contains", say_count, "screens of dialogue."
    print "These screens contain a total of", say_words, "words."
    print "For an average of %.1f words per screen." % (1.0 * say_words / say_count) 
    print "The game contains", menu_count, "menus."

