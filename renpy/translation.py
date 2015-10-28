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

import renpy

import hashlib
import re
import collections
import os
import time
import io

################################################################################
# Script
################################################################################

class ScriptTranslator(object):

    def __init__(self):

        # All languages we know about.
        self.languages = set()

        # A map from the translate identifier to the translate object used when the
        # language is None.
        self.default_translates = { }

        # A map from (identifier, language) to the translate object used for that
        # language.
        self.language_translates = { }

        # A list of (identifier, language) tuples that we need to chain together.
        self.chain_worklist = [ ]

        # A map from filename to a list of (label, translate) pairs found in
        # that file.
        self.file_translates = collections.defaultdict(list)

        # A map from language to the StringTranslator for that language.
        self.strings = collections.defaultdict(StringTranslator)

        # A map from language to a list of TranslateBlock objects for
        # that language.
        self.block = collections.defaultdict(list)

        # A map from language to a list of TranslatePython objects for
        # that language.
        self.python = collections.defaultdict(list)

        # A map from filename to a list of additional strings we've found
        # in that file.
        self.additional_strings = collections.defaultdict(list)

    def count_translates(self):
        """
        Return the number of dialogue blocks in the game.
        """

        return len(self.default_translates)

    def take_translates(self, nodes):
        """
        Takes the translates out of the flattened list of statements, and stores
        them into the dicts above.
        """

        label = None

        if not nodes:
            return

        TranslatePython = renpy.ast.TranslatePython
        TranslateBlock = renpy.ast.TranslateBlock
        Menu = renpy.ast.Menu
        Translate = renpy.ast.Translate

        filename = renpy.exports.unelide_filename(nodes[0].filename)
        filename = os.path.normpath(os.path.abspath(filename))

        for n in nodes:

            if not n.translation_relevant:
                continue

            if n.name.__class__ is not tuple:
                if isinstance(n.name, basestring):
                    label = n.name

            type_n = n.__class__

            if type_n is TranslatePython:
                self.python[n.language].append(n)

            elif type_n is TranslateBlock:
                self.block[n.language].append(n)

            elif type_n is Menu:

                for i in n.items:
                    s = i[0]

                    if s is None:
                        continue

                    self.additional_strings[filename].append((n.linenumber, s))

            elif type_n is Translate:

                if n.language is None:
                    self.default_translates[n.identifier] = n
                    self.file_translates[filename].append((label, n))
                else:
                    self.languages.add(n.language)
                    self.language_translates[n.identifier, n.language] = n
                    self.chain_worklist.append((n.identifier, n.language))

    def chain_translates(self):
        """
        Chains nodes in non-default translates together.
        """

        unchained = [ ]

        for identifier, language in self.chain_worklist:

            if identifier not in self.default_translates:
                unchained.append((identifier, language))
                continue

            translate = self.language_translates[identifier, language]
            next_node = self.default_translates[identifier].after

            renpy.ast.chain_block(translate.block, next_node)

        self.chain_worklist = unchained

    def lookup_translate(self, identifier):

        language = renpy.game.preferences.language

        if language is not None:
            tl = self.language_translates.get((identifier, language), None)
        else:
            tl = None

        if tl is None:
            tl = self.default_translates[identifier]

        return tl.block[0]

def encode_say_string(s):
    """
    Encodes a string in the format used by Ren'Py say statements.
    """

    s = s.replace("\\", "\\\\")
    s = s.replace("\n", "\\n")
    s = s.replace("\"", "\\\"")
    s = re.sub(r'(?<= ) ', '\\ ', s)

    return "\"" + s + "\""

class Restructurer(object):

    def __init__(self, children):
        self.label = None
        self.identifiers = set()
        self.callback(children)

    def id_exists(self, identifier):
        if identifier in self.identifiers:
            return True

        if identifier in renpy.game.script.translator.default_translates:
            return True

        return False

    def create_translate(self, block):
        """
        Creates an ast.Translate that wraps `block`. The block may only contain
        translatable statements.
        """

        md5 = hashlib.md5()

        for i in block:
            code = i.get_code()
            md5.update(code.encode("utf-8") + "\r\n")

        if self.label:
            base = self.label + "_" + md5.hexdigest()[:8]
        else:
            base = md5.hexdigest()[:8]

        i = 0
        suffix = ""

        while True:

            identifier = base + suffix

            if not self.id_exists(identifier):
                break

            i += 1
            suffix = "_{0}".format(i)

        self.identifiers.add(identifier)
        loc = (block[0].filename, block[0].linenumber)

        tl = renpy.ast.Translate(loc, identifier, None, block)
        tl.name = block[0].name + ("translate",)

        ed = renpy.ast.EndTranslate(loc)
        ed.name = block[0].name + ("end_translate",)

        return [ tl, ed ]

    def callback(self, children):
        """
        This should be called with a list of statements. It restructures the statements
        in the list so that translatable statements are contained within translation blocks.
        """

        new_children = [ ]
        group = [ ]

        for i in children:

            if isinstance(i, renpy.ast.Label):
                if not i.hide:
                    self.label = i.name

            if not isinstance(i, renpy.ast.Translate):
                i.restructure(self.callback)

            if isinstance(i, renpy.ast.Say):
                group.append(i)
                tl = self.create_translate(group)
                new_children.extend(tl)
                group = [ ]

            elif i.translatable:
                group.append(i)

            else:
                if group:
                    tl = self.create_translate(group)
                    new_children.extend(tl)
                    group = [ ]

                new_children.append(i)

        if group:
            nodes = self.create_translate(group)
            new_children.extend(nodes)
            group = [ ]

        children[:] = new_children

def restructure(children):
    Restructurer(children)


################################################################################
# String Translation
################################################################################

update_translations = ("RENPY_UPDATE_STRINGS" in os.environ)


def quote_unicode(s):
    s = s.replace("\\", "\\\\")
    s = s.replace("\"", "\\\"")
    s = s.replace("\a", "\\a")
    s = s.replace("\b", "\\b")
    s = s.replace("\f", "\\f")
    s = s.replace("\n", "\\n")
    s = s.replace("\r", "\\r")
    s = s.replace("\t", "\\t")
    s = s.replace("\v", "\\v")

    return s


class StringTranslator(object):
    """
    This object stores the translations for a single language. It can also
    buffer unknown translations, and write them to a file at game's end, if
    we want that to happen.
    """

    def __init__(self):

        # A map from translation to translated string.
        self.translations = { }

        # A list of unknown translations.
        self.unknown = [ ]

    def add(self, old, new):
        if old in self.translations:
            raise Exception("A translation for %r already exists." % old)

        self.translations[old] = new

    def translate(self, old):

        new = self.translations.get(old, None)

        if new is not None:
            return new

        if update_translations:
            self.translations[old] = old
            self.unknown.append(old)

        # Remove {#...} tags.
        if new is None:
            notags = re.sub(r"\{\#.*?\}", "", old)
            new = self.translations.get(notags, None)

        if new is not None:
            return new

        return old

    def write_updated_strings(self, language):

        if not self.unknown:
            return

        if language is None:
            fn = os.path.join(renpy.config.gamedir, "strings.rpy")
        else:
            fn = os.path.join(renpy.config.gamedir, renpy.config.tl_directory, language, "strings.rpy")

        f = open_tl_file(fn)

        f.write(u"translate {} strings:\n".format(language))
        f.write(u"\n")

        for i in self.unknown:

            i = quote_unicode(i)

            f.write(u"    old \"{}\"\n".format(i))
            f.write(u"    new \"{}\"\n".format(i))
            f.write(u"\n")

        f.close()

def add_string_translation(language, old, new):
    tl = renpy.game.script.translator
    stl = tl.strings[language]
    tl.languages.add(language)
    stl.add(old, new)

def translate_string(s):
    """
    Translates interface string `s`.
    """

    stl = renpy.game.script.translator.strings[renpy.game.preferences.language]
    return stl.translate(s)

def write_updated_strings():
    stl = renpy.game.script.translator.strings[renpy.game.preferences.language]
    stl.write_updated_strings(renpy.game.preferences.language)


################################################################################
# RPT Support
#
# RPT was the translation format used before 6.15.
################################################################################

def load_rpt(fn):
    """
    Loads the .rpt file `fn`.
    """

    def unquote(s):
        s = s.replace("\\n", "\n")
        s = s.replace("\\\\", "\\")
        return s

    language = os.path.basename(fn).replace(".rpt", "")

    f = renpy.loader.load(fn)

    old = None

    for l in f:
        l = l.decode("utf-8")
        l = l.rstrip()

        if not l:
            continue

        if l[0] == '#':
            continue

        s = unquote(l[2:])

        if l[0] == '<':
            if old:
                raise Exception("{0} string {1!r} does not have a translation.".format(language, old))

            old = s

        if l[0] == ">":
            if old is None:
                raise Exception("{0} translation {1!r} doesn't belong to a string.".format(language, s))

            add_string_translation(language, old, s)
            old = None

    f.close()

    if old is not None:
        raise Exception("{0} string {1!r} does not have a translation.".format(language, old))

def load_all_rpts():
    """
    Loads all .rpt files.
    """

    for fn in renpy.exports.list_files():
        if fn.endswith(".rpt"):
            load_rpt(fn)

################################################################################
# Changing language
################################################################################

style_backup = None

def init_translation():
    """
    Called before the game starts.
    """

    global style_backup
    style_backup = renpy.style.backup() # @UndefinedVariable

    load_all_rpts()

    renpy.store._init_language() # @UndefinedVariable

def change_language(language):
    """
    :doc: translation_functions

    Changes the current language to `language`, which can be a string or
    None to use the default language.
    """

    renpy.game.preferences.language = language

    tl = renpy.game.script.translator

    renpy.style.restore(style_backup) # @UndefinedVariable
    renpy.style.rebuild() # @UndefinedVariable

    def run_blocks():
        for i in tl.block[language]:
            renpy.game.context().run(i.block[0])

    renpy.game.invoke_in_new_context(run_blocks)

    for i in tl.python[language]:
        renpy.python.py_exec_bytecode(i.code.bytecode)

    for i in renpy.config.change_language_callbacks:
        i()

    # Reset various parts of the system. Most notably, this clears the image
    # cache, letting us load translated images.
    renpy.exports.free_memory()

    # Rebuild the styles.
    renpy.style.rebuild() # @UndefinedVariable

    # Restart the interaction.
    renpy.exports.restart_interaction()

def check_language():
    """
    Checks to see if the language has changed. If it has, jump to the start
    of the current translation block.
    """

    ctx = renpy.game.contexts[-1]
    preferences = renpy.game.preferences

    # Deal with a changed language.
    if ctx.translate_language != preferences.language:
        ctx.translate_language = preferences.language

        tid = ctx.translate_identifier

        if tid is not None:
            node = renpy.game.script.translator.lookup_translate(tid)

            if node is not None:
                raise renpy.game.JumpException(node.name)

def known_languages():
    """
    :doc: translation_functions

    Returns the set of known languages. This does not include the default
    language, None.
    """

    return renpy.game.script.translator.languages


################################################################################
# Translation Generation
################################################################################

STRING_RE = r"""(?x)
\b__?\s*\(\s*[uU]?(
\"\"\"(?:\\.|\"{1,2}|[^\\"])*?\"\"\"
|'''(?:\\.|\'{1,2}|[^\\'])*?'''
|"(?:\\.|[^\\"])*"
|'(?:\\.|[^\\'])*'
)\s*\)
"""

def scan_strings(filename):
    """
    Scans `filename`, a file containing Ren'Py script, for translatable
    strings.

    Generates a list of (line, string) tuples.
    """

    for line, s in renpy.game.script.translator.additional_strings[filename]:
        yield line, s

    line = 1

    for _filename, lineno, text in renpy.parser.list_logical_lines(filename):

        for m in re.finditer(STRING_RE, text):

            s = m.group(1)
            if s is not None:
                s = s.strip()
                s = "u" + s
                s = eval(s)
                yield lineno, s


def open_tl_file(fn):

    if not os.path.exists(fn):
        dn = os.path.dirname(fn)

        try:
            os.makedirs(dn)
        except:
            pass

        f = io.open(fn, "a", encoding="utf-8")
        f.write(u"\ufeff")

    else:
        f = io.open(fn, "a", encoding="utf-8")

    f.write(u"# TODO: Translation updated at {}\n".format(time.strftime("%Y-%m-%d %H:%M")))
    f.write(u"\n")

    return f


class TranslateFile(object):

    def __init__(self, filename, language, filter): # @ReservedAssignment
        self.filename = filename
        self.filter = filter

        commondir = os.path.normpath(renpy.config.commondir)
        gamedir = os.path.normpath(renpy.config.gamedir)

        if filename.startswith(commondir):
            relfn = os.path.relpath(filename, commondir)

            if relfn == "_developer.rpym":
                return

            if relfn.startswith("compat"):
                return

            self.tl_filename = os.path.join(renpy.config.gamedir, renpy.config.tl_directory, language, "common.rpy")
        elif filename.startswith(gamedir):
            fn = os.path.relpath(filename, gamedir)
            self.tl_filename = os.path.join(renpy.config.gamedir, renpy.config.tl_directory, language, fn)

        if self.tl_filename.endswith(".rpym"):
            self.tl_filename = self.tl_filename[:-1]

        if language == "None":
            language = None

        self.language = language
        self.f = None

        if language is not None:
            self.write_translates()

        self.write_strings()

        self.close()

    def open(self):
        """
        Opens a translation file.
        """

        if self.f is not None:
            return

        self.f = open_tl_file(self.tl_filename)

    def close(self):
        """
        Closes the translation file, if it's open.
        """

        if self.f is not None:
            self.f.close()

    def write_translates(self):
        """
        Writes the translates to the file.
        """

        translator = renpy.game.script.translator

        for label, t in translator.file_translates[self.filename]:

            if (t.identifier, self.language) in translator.language_translates:
                continue

            self.open()

            if label is None:
                label = ""

            self.f.write(u"# {}:{}\n".format(t.filename, t.linenumber))
            self.f.write(u"translate {} {}:\n".format(self.language, t.identifier))
            self.f.write(u"\n")

            for n in t.block:
                self.f.write(u"    # " + n.get_code() + "\n")

            for n in t.block:
                self.f.write(u"    " + n.get_code(self.filter) + "\n")

            self.f.write(u"\n")

    def write_strings(self):
        """
        Writes strings to the file.
        """

        started = False
        filename = renpy.parser.elide_filename(self.filename)

        for line, s in scan_strings(self.filename):

            stl = renpy.game.script.translator.strings[self.language]

            if s in stl.translations:
                continue

            stl.translations[s] = s

            if not started:
                started = True

                self.open()
                self.f.write(u"translate {} strings:\n".format(self.language))
                self.f.write(u"\n")

            fs = self.filter(s)

            self.f.write(u"    # {}:{}\n".format(filename, line))
            self.f.write(u"    old \"{}\"\n".format(quote_unicode(s)))
            self.f.write(u"    new \"{}\"\n".format(quote_unicode(fs)))
            self.f.write(u"\n")

def null_filter(s):
    return s

def empty_filter(s):
    return ""

ROT13 = { }

for i, j in zip("ABCDEFGHIJKLM", "NMOPQRSTUVWYZ"):
    ROT13[i] = j
    ROT13[j] = i

    i = i.lower()
    j = j.lower()

    ROT13[i] = j
    ROT13[j] = i

def rot13_filter(s):

    def tag_pass(s):

        brace = False
        first = False
        rv = ""

        for i in s:

            if i == '{':

                if first:
                    brace = False
                else:
                    brace = True
                    first = True

                rv += "{"

            elif i == "}":
                first = False

                if brace:
                    brace = False

                rv += "}"

            else:
                first = False

                if brace:
                    rv += i
                else:
                    rv += ROT13.get(i, i)

        return rv

    def square_pass(s):
        squares = 0
        first = False

        rv = ""
        buf = ""

        for i in s:

            if i == "[":
                if first:
                    squares = 0
                else:
                    rv += tag_pass(buf)
                    buf = ""

                    if squares == 0:
                        first = True

                    squares += 1

                rv += "["

            elif i == "]":

                first = False

                squares -= 1
                if squares < 0:
                    squares += 1

                rv += "]"

            else:
                if squares:
                    rv += i
                else:
                    buf += i

        if buf:
            rv += tag_pass(buf)

        return rv


    return square_pass(s)

def translate_command():
    """
    The translate command. When called from the command line, this generates
    the translations.
    """

    ap = renpy.arguments.ArgumentParser(description="Generates or updates translations.")
    ap.add_argument("language", help="The language to generate translations for.")
    ap.add_argument("--rot13", help="Apply rot13 while generating translations.", dest="rot13", action="store_true")
    ap.add_argument("--empty", help="Produce empty strings while generating translations.", dest="empty", action="store_true")
    args = ap.parse_args()

    if args.rot13:
        filter = rot13_filter #@ReservedAssignment
    elif args.empty:
        filter = empty_filter # @ReservedAssignment
    else:
        filter = null_filter #@ReservedAssignment

    for dirname, filename in renpy.loader.listdirfiles():
        if dirname is None:
            continue

        filename = os.path.join(dirname, filename)

        if not (filename.endswith(".rpy") or filename.endswith(".rpym")):
            continue

        filename = os.path.normpath(filename)
        TranslateFile(filename, args.language, filter)

    return False

renpy.arguments.register_command("translate", translate_command)



def notags_filter(s):

    def tag_pass(s):

        brace = False
        first = False
        rv = ""

        for i in s:

            if i == '{':

                if first:
                    brace = False
                else:
                    brace = True
                    first = True

            elif i == "}":
                first = False

                if brace:
                    brace = False

            else:
                first = False

                if brace:
                    pass
                else:
                    rv += i

        return rv

    def square_pass(s):
        squares = 0
        first = False

        rv = ""
        buf = ""

        for i in s:

            if i == "[":
                if first:
                    squares = 0
                else:
                    rv += tag_pass(buf)
                    buf = ""

                    if squares == 0:
                        first = True

                    squares += 1

                rv += "["

            elif i == "]":

                first = False

                squares -= 1
                if squares < 0:
                    squares += 1

                rv += "]"

            else:
                if squares:
                    rv += i
                else:
                    buf += i

        if buf:
            rv += tag_pass(buf)

        return rv


    return square_pass(s)



class DialogueFile(object):

    def __init__(self, filename, output, tdf=True): # @ReservedAssignment
        """
        `filename`
            The file we're extracting dialogue from.

        `tdf`
            If true, dialogue is extracted in tab-delimited format. If false,
            dialogue is extracted by itself.
        """

        self.filename = filename

        commondir = os.path.normpath(renpy.config.commondir)

        if filename.startswith(commondir):
            return

        self.tdf = tdf

        self.f = open(output, "a")

        self.write_translates()

        self.f.close()

    def write_translates(self):
        """
        Writes the translates to the file.
        """

        translator = renpy.game.script.translator

        for label, t in translator.file_translates[self.filename]:

            if label is None:
                label = ""

            for n in t.block:

                if isinstance(n, renpy.ast.Say):

                    if not n.who:
                        who = ""
                    else:
                        who = n.who

                    what = notags_filter(n.what)

                    if self.tdf:

                        line = [
                            t.identifier,
                            who,
                            what,
                            n.filename,
                            str(n.linenumber),
                            ]

                    else:
                        line = [
                            what
                            ]

                    self.f.write("\t".join(line).encode("utf-8") + "\n")


def dialogue_command():
    """
    The dialogue command. This updates dialogue.txt, a file giving all the dialogue
    in the game.
    """

    ap = renpy.arguments.ArgumentParser(description="Generates or updates translations.")
    ap.add_argument("--text", help="Apply rot13 while generating translations.", dest="text", action="store_true")
    args = ap.parse_args()

    tdf = not args.text
    if tdf:
        output = os.path.join(renpy.config.basedir, "dialogue.tab")
    else:
        output = os.path.join(renpy.config.basedir, "dialogue.txt")

    with open(output, "w") as f:
        if tdf:
            line = [
                "Identifier",
                "Character",
                "Dialogue",
                "Filename",
                "Line Number",
                ]

            f.write("\t".join(line).encode("utf-8") + "\n")

    for dirname, filename in renpy.loader.listdirfiles():
        if dirname is None:
            continue

        filename = os.path.join(dirname, filename)

        if not (filename.endswith(".rpy") or filename.endswith(".rpym")):
            continue

        filename = os.path.normpath(filename)
        DialogueFile(filename, output, tdf=tdf)

    return False

renpy.arguments.register_command("dialogue", dialogue_command)
