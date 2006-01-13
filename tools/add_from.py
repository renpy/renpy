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

def main():

    pattern = "*/*.rpy"

    if len(sys.argv) >= 2:
        pattern = sys.argv[1]

    files = glob.glob(pattern)
    files = [ i for i in files if not i.startswith("common/") ]

    labels = { }
    
    for fn in files:
        print "Finding labels in", fn
        find_labels(fn, labels)

    for fn in files:
        print "Replacing labels in", fn
        replace_labels(fn, labels)
    


if __name__ == "__main__":
    main()
