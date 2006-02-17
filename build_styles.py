#!/usr/bin/python

import glob
import os

files = glob.glob("common/*.rpy")
files.sort()

styles = [ ]

for fn in files:
    f = file(fn)

    fi = iter(f)

    for l in iter(fi):

        l = l.strip()

        if l.startswith("### "):

            prefix, style, parent = l.split()

            desc = ""

            for l in fi:

                l = l.strip()
                if not l.startswith("# "):
                    break

                desc = desc + " " + l[2:]

            styles.append('        style.create("%s", "%s", "%s")' % (style, parent, desc[1:]))

    f.close()

f = file("common/style.rpy")
of = file("common/style.rpy.new", "w")

fi = iter(f)

for l in fi:

    of.write(l)

    if l.startswith("# AUTOMATICALLY GENERATED"):

        for l in styles:
            of.write(l + "\n")

        for l in fi:
            if l.startswith("# END AUTOMATICALLY GENERATED"):
                break

        of.write(l)

f.close()
of.close()

os.rename("common/style.rpy", "common/style.rpy.bak")
os.rename("common/style.rpy.new", "common/style.rpy")
