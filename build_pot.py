1#!/usr/bin/env python

import collections
import glob
import re
import sys
import time

# A map from string to filename, line number where the string is found.
strings = collections.defaultdict(list)

def process(fn):

    lineno = 0
    
    for data in file(fn, "r"):

        lineno += 1

        matches = [ ]
        
        matches += re.finditer(r'\bu\"(\\"|[^"])+\"', data)
        matches += re.finditer(r"\bu\'(\\'|[^'])+\'", data)

        for m in matches:
            s = m.group(0)[2:-1]

            if "\\u" in s:
                continue

            if len(s) == 1:
                continue
            
            strings[s].append("%s:%d" % (fn, lineno))

if __name__ == "__main__":

    files = [ ]

    files += glob.glob("launcher2/*.rpy")
    files += glob.glob("common/*.rpy")
    files += glob.glob("common/_layout/*.rpym")
    files += glob.glob("common/_compat/*.rpym")
        
    for fn in files:
        process(fn)


    converse = [ ]
        
    for k, v in strings.iteritems():
        v = " ".join(sorted(v))
        converse.append((v, k))

    converse.sort()

    print """\
# Ren'Py Visual Novel Engine
# Copyright (C) 2009 PyTom <pytom@bishoujo.us>
# This file is distributed under the same license as the Ren'Py package.
#
#, fuzzy
msgid ""
msgstr ""
"Project-Id-Version: mainline\\n"
"Report-Msgid-Bugs-To: PyTom <pytom@bishoujo.us>\\n"
"POT-Creation-Date: %s\\n"
"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\\n"
"Last-Translator: FULL NAME <EMAIL@ADDRESS>\\n"
"Language-Team: LANGUAGE <LL@li.org>\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: 8bit\\n"
""" % time.strftime("%Y-%m-%d %H:%M%z")
    
    for v, k in converse:
        print
        print "#:", v
        print "#, python-format"
        print "msgid \"%s\"" % k
        print "msgstr \"\""
        
        
        
