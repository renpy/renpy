# Copyright 2004-2023 Tom Rothamel <pytom@bishoujo.us>
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

from __future__ import unicode_literals

import os
import codecs
import re
import math
import textwrap
import collections
import shutil

import renpy


class Define(object):

    def __init__(self, name, value, comment):
        self.name = name
        self.value = value
        self.comment = comment


# A map from language name to a list of defines.
language_defines = collections.defaultdict(list)


def translate_define(language, name, value, comment=None):
    """
    This function should be called to register the value of a define that is
    set when generating code in `language`.

    `name`
        A string giving the name of the define.

    `value`
        A string giving the value of the define. Be sure to quote it properly,
        or use repr().

    `comment`
        If not None, a comment that will be generated before the define. The
        comment will only be generated if the define does not exist in
        gui.rpy. There is no need to use "## ", as the comment will be
        added and wrapped automatically.
    """

    language_defines[language].append(Define(name, value, comment))


# A map from a language name to a list of (src, dst) pairs. Each represents a
# file that is copied into place.
language_copies = collections.defaultdict(list)


def translate_copy(language, src, dst):
    """
    This function should be called to copy a file from `src` to `dst`
    when generating code in `language`.

    `src`
        A path, relative to the launcher game directory.

    `dst`
        A path, relative to the game directory of the new game.
    """

    language_copies[language].append((src, dst))


# A map from language name and filename to code that should be added to the
# end of a newly-generated file.
language_code = collections.defaultdict(list)


def translate_code(language, filename, code):
    """
    This function can be called to include a block of code verbatim
    into `file` when a game is generated in `language`.
    """

    language_code[language, filename].extend([''] + code.split("\n"))


class CodeGenerator(object):
    """
    This is used to generate and update the GUI code.
    """

    def __init__(self, parameters):
        """
        Generates or updates gui.rpy.
        """

        self.p = parameters

    def load_template(self, filename):

        target = os.path.join(self.p.prefix, filename)

        if os.path.exists(target) and not self.p.replace_code:
            template = target
        else:
            template = os.path.join(self.p.template, filename)

        with codecs.open(template, "r", "utf-8") as f:
            self.lines = [ i.rstrip().replace(u"\ufeff", "") for i in f ]

    def remove_scale(self):

        def scale(m):
            original = int(m.group(1))
            scaled = int(math.ceil(original * self.p.scale))
            return str(scaled)

        lines = [ ]

        for l in self.lines:
            l = re.sub(r'gui.scale\((.*?)\)', scale, l)
            lines.append(l)

        self.lines = lines

    def update_size(self):

        gui_init = "gui.init({}, {})".format(self.p.width, self.p.height)

        lines = [ ]

        for l in self.lines:
            l = re.sub(r'gui.init\(.*?\)', gui_init, l)
            lines.append(l)

        self.lines = lines

    def update_defines(self, replacements, additions=[]):
        """
        Replaces define statements in gui.rpy.
        """

        replacements = dict(replacements)

        for d in additions:
            replacements[d.name] = d.value

        seen = set()

        lines = [ ]

        for l in self.lines:

            m = re.match('^(\s*)define (.*?) =', l)

            if m:
                indent = m.group(1)
                variable = m.group(2)

                if variable in replacements:
                    l = "{}define {} = {}".format(indent, variable, replacements[variable])

                seen.add(variable)

            lines.append(l)

        for d in additions:

            if d.name in seen:
                continue

            seen.add(d.name)

            lines.append("")

            if d.comment:
                for s in textwrap.wrap(d.comment):
                    lines.append("## " + s)

            lines.append("define {} = {}".format(d.name, d.value))

        self.lines = lines

    def update_gui_defines(self):
        """
        Replaces define statements in gui.rpy.
        """

        replacements = {
            'gui.accent_color' : repr(self.p.accent_color.hexcode),
            'gui.selected_color' : repr(self.p.selected_color.hexcode),
            'gui.hover_color' : repr(self.p.hover_color.hexcode),
            'gui.muted_color' : repr(self.p.muted_color.hexcode),
            'gui.hover_muted_color' : repr(self.p.hover_muted_color.hexcode),
            'gui.title_color' : repr(self.p.title_color.hexcode),
            'gui.idle_color' : repr(self.p.idle_color.hexcode),
            'gui.idle_small_color' : repr(self.p.idle_small_color.hexcode),
            'gui.insensitive_color' : repr(self.p.insensitive_color.hexcode),
            'gui.text_color' : repr(self.p.text_color.hexcode),
            'gui.interface_text_color' : repr(self.p.text_color.hexcode),
            'gui.choice_button_text_idle_color' : repr(self.p.idle_color.hexcode),
            'gui.choice_button_text_insensitive_color' : repr(self.p.insensitive_color.hexcode),
            }

        self.update_defines(replacements, language_defines[self.p.language])

    def update_options_defines(self):
        """
        Replaces define statements in options.rpy.
        """

        def quote(s):
            s = s.replace("\\", "\\\\")
            s = s.replace("\"", "\\\"")
            return '"' + s + '"'

        replacements = {
            'config.name' : "_({})".format(quote(self.p.name)),
            'build.name' : quote(self.p.simple_name),
            'config.save_directory' : quote(self.p.savedir),
            }

        self.update_defines(replacements)

    def write_target(self, filename):

        target = os.path.join(self.p.prefix, filename)

        if os.path.exists(target):

            backup = 1

            while True:

                bfn = "{}.{}.bak".format(target, backup)

                if not os.path.exists(bfn):
                    break

                backup += 1

            if not self.p.skip_backup:
                os.rename(target, bfn)

        with codecs.open(target, "w", "utf-8") as f:
            f.write(u"\ufeff")

            for l in self.lines:
                f.write(l + "\r\n")

    def translate_strings(self):

        def replace(m):
            s = eval(m.group(1))
            s = renpy.translation.translate_string(s, language=self.p.language)
            s = renpy.translation.quote_unicode(s)

            quote = m.group(1)[0]

            s = u"_({}{}{})".format(quote, s, quote)

            return s

        lines = [ ]

        for l in self.lines:

            l = re.sub(r'_\((\".*?\")\)', replace, l)
            l = re.sub(r'_\((\'.*?\')\)', replace, l)

            lines.append(l)

        self.lines = lines

    def translate_comments(self):

        lines = [ ]

        comment = [ ]
        indent = ""

        for l in self.lines:

            m = re.match(r'^(\s*## )(.*)', l.rstrip())

            if m:

                indent = m.group(1)
                c = m.group(2)

                if comment:
                    c = c.strip()

                comment.append(c)

            else:

                if comment:
                    s = "## " + ' '.join(comment)

                    if s.endswith("#"):
                        hashpad = True
                        s = s.rstrip('# ')
                    else:
                        hashpad = False

                    s = renpy.translation.translate_string(s, language=self.p.language)

                    m = re.match(r'## ?([ *]*)(.*)', s)

                    if m is None:
                        raise Exception("Comment translation doesn't start with '## ': {}".format(s))

                    prefix = m.group(1)
                    empty = ' ' * len(prefix)
                    rest = m.group(2)

                    len_prefix = len(indent) + len(prefix)
                    len_wrap = 80 - len_prefix

                    import store.gui

                    for i, s in enumerate(renpy.text.extras.textwrap(rest, len_wrap, store.gui.asian)):

                        if i == 0:
                            s = indent + prefix + s
                        else:
                            s = indent + empty + s

                        if hashpad and len(s) < 79:
                            s = s + ' ' + "#" * (79 - len(s))

                        lines.append(s)

                    comment = [ ]

                lines.append(l)

        self.lines = lines

    def copy_files(self):

        for src, dst in language_copies[self.p.language]:
            src = os.path.join(renpy.config.renpy_base, src)
            dst = os.path.join(self.p.prefix, dst)

            if os.path.exists(dst):
                continue

            dstdir = os.path.dirname(dst)

            if not os.path.exists(dstdir):
                os.makedirs(dstdir, 0o777)

            shutil.copy(src, dst)

    def copy_script(self, name):
        dst = os.path.join(self.p.prefix, name)

        if os.path.exists(dst):
            return

        language = renpy.store._preferences.language # @UndefinedVariable

        if language is None:
            language = "None"

        src = os.path.join(renpy.config.gamedir, "tl", language, name + "m")

        if not os.path.exists(src):
            src = os.path.join(self.p.template, name)

        self.load_template(src)
        self.remove_scale()
        self.write_target(dst)

    def add_code(self, fn):

        if not self.p.replace_code:
            return

        self.lines.extend(language_code[self.p.language, fn])

    def generate_gui(self, fn, defines=False):
        if not self.p.update_code:
            return

        self.load_template(fn)

        if defines:
            self.update_gui_defines()

        if self.p.replace_code:
            self.remove_scale()
            self.update_size()
            self.translate_strings()
            self.translate_comments()
            self.add_code(fn)

        self.write_target(fn)

    def generate_code(self, fn):

        target = os.path.join(self.p.prefix, fn)

        if os.path.exists(target):
            return

        self.load_template(fn)

        self.translate_strings()
        self.translate_comments()
        self.update_options_defines()

        self.add_code(fn)

        self.write_target(fn)
