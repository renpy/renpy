#!/usr/bin/env python

from __future__ import print_function

import os.path
import re
import codecs

ENDINGS = [
    ".rpy",
    ".rpym",
    ".py",
    ".pyx",
    ".pxd",
    ]

WHITELIST = """\
renpy/vc_version.py
renpy/angle
renpy/gl/__init__.py
renpy/common/00splines.rpy
renpy/common/00console.rpy
renpy/text/__init__.py
module/maketegl.py
module/generate_linebreak.py
module/pysdlsound/linmixer.py
module/pysdlsound/__init__.py
module/build/
module/include/
module/gen/
launcher/game/EasyDialogsResources.py
launcher/game/EasyDialogsWin.py
launcher/game/pefile.py
launcher/game/script_version.rpy
launcher/game/tl
launcher/game/theme""".split()

LICENSE = "Permission is hereby granted"

def process_file(fn):

    for i in ENDINGS:
        if fn.endswith(i):
            break
    else:
        return

    for i in WHITELIST:
        if fn.startswith(i):
            return

    has_copyright = False
    has_license = False
    first = True

    with open(fn, "rb") as f:

        for l in f:
            if fn.endswith(".rpy") or fn.endswith(".rpym"):
                if first:
                    if codecs.BOM_UTF8 not in l:
                        print("Missing BOM", fn)
                    first = False
                else:
                    if codecs.BOM_UTF8 in l:
                        print("Extra BOM", fn)

                first = False


            m = re.search(
                r"Copyright (\d{4})-2015 Tom Rothamel",
                l)

            if m:
                has_copyright = True

            if LICENSE in l:
                has_license = True

            if has_copyright and has_license:
                return

    print("Missing copyright", fn)


def process(root):

    for dirname, _dirs, files in os.walk(root):
        for fn in files:
            fn = os.path.join(dirname, fn)
            process_file(fn)

process_file("renpy.py")
process("renpy")
process("module")
process("launcher/game")

