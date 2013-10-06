#!/usr/bin/env python
#@PydevCodeAnalysisIgnore

# This file is part of Ren'Py. The license below applies to Ren'Py only.
# Games and other projects that use Ren'Py may use a different license.

# Copyright 2013 Koichi Akabe <vbkaisetsu@gmail.com>
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

import polib, os

po = polib.pofile("locale/credits/" + os.environ["LANGUAGE"] + ".po")

tc = ""

for podata in po:
    if podata.msgid == "translator-credits":
        tc = podata.msgstr
        break

if tc == "":
    tc = "???"

tc_lines = []
for line in tc.split("\n"):
    line_s = line.lstrip()
    tc_lines.append(" " * (len(line) - len(line_s)) + "* " + line_s)
    
tc = "\n\n".join(tc_lines)

creditsfile = open("source/credits.rst", "r")

reslines = []
for line in creditsfile:
    reslines.append(line.replace("@TRANSLATOR_CREDITS@", tc))

creditsfile.close()

creditsfile = open("source/credits.rst", "w")

for line in reslines:
    creditsfile.write(line)

creditsfile.close()
