# Copyright 2004-2008 PyTom <pytom@bishoujo.us>
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

#!/usr/bin/env python

# This program adds froms to every unqualified call found in the game
# directory. It's not perfect, but it's better than nothing.

import sys
import os
import re
import glob

def find_labels(fn, labels):

    f = file(fn, "r")

    for l in f:

        m = re.match(r'^\s*call\s+\w+\s+from\s+(\w+)\s*$', l)
        if m:
            labels[m.group(1)] = True

        m = re.match(r'^\s*call\s+expression.*from\s+(\w+)\s*$', l)
        if m:
            labels[m.group(1)] = True

    f.close()

def replace_labels(fn, labels):

    f = file(fn, "r")
    of = file(fn + ".new", "w")


    def replaceit(m):
        target = m.group(2)

        num = 0

        while True:
            num += 1
            label = "_call_%s_%d" % (target, num)

            if label not in labels:
                break

        labels[label] = True

        return m.group(1) + "call " + target + " from " + label + m.group(3)

    for l in f:
        l = re.sub(r'^(\s*)call\s+(\w+)(\s*$)', replaceit, l)

        if re.search(r'call\s+expression', l) and not re.search('from', l):

            num = 0

            while True:
                num += 1
                label = "_call_expression_%d" % num

                if label not in labels:
                    break

            labels[label] = label

            l = l[:-1] + " from " + label + "\n"

        of.write(l)

    f.close()
    of.close()


    try:
        os.unlink(fn + ".bak")
    except:
        pass
    
    os.rename(fn, fn + ".bak")
    os.rename(fn + ".new", fn)

def add_from(gamedir, commondir):

    labels = { }

    game_files = [ gamedir + "/" + i for i in os.listdir(gamedir) if i.endswith(".rpy") ]
    
    if commondir:
        common_files = [ commondir + "/" + i for i in os.listdir(commondir) if i.endswith(".rpy") ]
    else:
        common_files = [ ]
    
    for fn in game_files + common_files:
        print "Finding labels in", fn
        find_labels(fn, labels)

    for fn in game_files:
        print "Replacing labels in", fn
        replace_labels(fn, labels)
    
