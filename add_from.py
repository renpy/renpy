#!/usr/bin/env python

# This program adds froms to every unqualified call found in the game
# directory. It's not perfect, but it's better than nothing.

import sys
import os
import re

def find_labels(fn, labels):

    f = file(fn, "r")

    for l in f:

        m = re.match(r'^\s*call\s+\w+\s+from\s+(\w+)\s*$', l)
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
        of.write(l)

    f.close()
    of.close()
    
    os.rename(fn, fn + ".bak")
    os.rename(fn + ".new", fn)

def main():

    gamedir = "game"

    if len(sys.argv) >= 2:
        gamedir = sys.argv[1]

    print "Processing files in", gamedir

    files = [ gamedir + "/" + i for i in os.listdir(gamedir)
              if i.endswith(".rpy") ]

    labels = { }
    
    for fn in files:
        print "Finding labels in", fn
        find_labels(fn, labels)

    for fn in files:
        print "Replacing labels in", fn
        replace_labels(fn, labels)
    


if __name__ == "__main__":
    main()
