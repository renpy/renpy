# encoding: utf-8

# Based on: http://www.unicode.org/Public/UNIDATA/LineBreak.txt
# Based on: http://unicode.org/reports/tr14/#PairBasedImplementation

from __future__ import print_function

import re

breaking = """OP    CL    CP    QU    GL    NS    EX    SY    IS    PR    PO    NU    AL    HL    ID    IN    HY    BA    BB    B2    ZW    CM    WJ    H2    H3    JL    JV    JT    RI
OP    ^    ^    ^    ^    ^    ^    ^    ^    ^    ^    ^    ^    ^    ^    ^    ^    ^    ^    ^    ^    ^    @    ^    ^    ^    ^    ^    ^    ^
CL    _    ^    ^    %    %    ^    ^    ^    ^    %    %    _    _    _    _    _    %    %    _    _    ^    #    ^    _    _    _    _    _    _
CP    _    ^    ^    %    %    ^    ^    ^    ^    %    %    %    %    %    _    _    %    %    _    _    ^    #    ^    _    _    _    _    _    _
QU    ^    ^    ^    %    %    %    ^    ^    ^    %    %    %    %    %    %    %    %    %    %    %    ^    #    ^    %    %    %    %    %    %
GL    %    ^    ^    %    %    %    ^    ^    ^    %    %    %    %    %    %    %    %    %    %    %    ^    #    ^    %    %    %    %    %    %
NS    _    ^    ^    %    %    %    ^    ^    ^    _    _    _    _    _    _    _    %    %    _    _    ^    #    ^    _    _    _    _    _    _
EX    _    ^    ^    %    %    %    ^    ^    ^    _    _    _    _    _    _    _    %    %    _    _    ^    #    ^    _    _    _    _    _    _
SY    _    ^    ^    %    %    %    ^    ^    ^    _    _    %    _    _    _    _    %    %    _    _    ^    #    ^    _    _    _    _    _    _
IS    _    ^    ^    %    %    %    ^    ^    ^    _    _    %    %    %    _    _    %    %    _    _    ^    #    ^    _    _    _    _    _    _
PR    %    ^    ^    %    %    %    ^    ^    ^    _    _    %    %    %    %    _    %    %    _    _    ^    #    ^    %    %    %    %    %    _
PO    %    ^    ^    %    %    %    ^    ^    ^    _    _    %    %    %    _    _    %    %    _    _    ^    #    ^    _    _    _    _    _    _
NU    %    ^    ^    %    %    %    ^    ^    ^    %    %    %    %    %    _    %    %    %    _    _    ^    #    ^    _    _    _    _    _    _
AL    %    ^    ^    %    %    %    ^    ^    ^    _    _    %    %    %    _    %    %    %    _    _    ^    #    ^    _    _    _    _    _    _
HL    %    ^    ^    %    %    %    ^    ^    ^    _    _    %    %    %    _    %    %    %    _    _    ^    #    ^    _    _    _    _    _    _
ID    _    ^    ^    %    %    %    ^    ^    ^    _    %    _    _    _    _    %    %    %    _    _    ^    #    ^    _    _    _    _    _    _
IN    _    ^    ^    %    %    %    ^    ^    ^    _    _    _    _    _    _    %    %    %    _    _    ^    #    ^    _    _    _    _    _    _
HY    _    ^    ^    %    _    %    ^    ^    ^    _    _    %    _    _    _    _    %    %    _    _    ^    #    ^    _    _    _    _    _    _
BA    _    ^    ^    %    _    %    ^    ^    ^    _    _    _    _    _    _    _    %    %    _    _    ^    #    ^    _    _    _    _    _    _
BB    %    ^    ^    %    %    %    ^    ^    ^    %    %    %    %    %    %    %    %    %    %    %    ^    #    ^    %    %    %    %    %    %
B2    _    ^    ^    %    %    %    ^    ^    ^    _    _    _    _    _    _    _    %    %    _    ^    ^    #    ^    _    _    _    _    _    _
ZW    _    _    _    _    _    _    _    _    _    _    _    _    _    _    _    _    _    _    _    _    ^    _    _    _    _    _    _    _    _
CM    %    ^    ^    %    %    %    ^    ^    ^    _    _    %    %    %    _    %    %    %    _    _    ^    #    ^    _    _    _    _    _    _
WJ    %    ^    ^    %    %    %    ^    ^    ^    %    %    %    %    %    %    %    %    %    %    %    ^    #    ^    %    %    %    %    %    %
H2    _    ^    ^    %    %    %    ^    ^    ^    _    %    _    _    _    _    %    %    %    _    _    ^    #    ^    _    _    _    %    %    _
H3    _    ^    ^    %    %    %    ^    ^    ^    _    %    _    _    _    _    %    %    %    _    _    ^    #    ^    _    _    _    _    %    _
JL    _    ^    ^    %    %    %    ^    ^    ^    _    %    _    _    _    _    %    %    %    _    _    ^    #    ^    %    %    %    %    _    _
JV    _    ^    ^    %    %    %    ^    ^    ^    _    %    _    _    _    _    %    %    %    _    _    ^    #    ^    _    _    _    %    %    _
JT    _    ^    ^    %    %    %    ^    ^    ^    _    %    _    _    _    _    %    %    %    _    _    ^    #    ^    _    _    _    _    %    _
RI    _    ^    ^    %    %    %    ^    ^    ^    _    _    _    _    _    _    _    %    %    _    _    ^    #    ^    _    _    _    _    _    %
"""

other_classes = " PITCH AI BK CB CJ CR LF NL SA SG SP XX"

lines = breaking.split("\n")

print("# This is generated code. Do not edit.")
print()

# A map from character class to the number that represents it.
cl = { }


for i, j in enumerate((lines[0] + other_classes).split()):
    print(("cdef char BC_{} = {}".format(j, i)))
    cl[j] = i

print("CLASSES = {")

for i, j in enumerate((lines[0] + other_classes).split()):
    print(("    \"{}\" : {},".format(j, i)))
    cl[j] = i

print("}")

rules = [ ]

for l in lines[1:]:
    for c in l.split()[1:]:
        rules.append(c)

print()
print(("cdef char *break_rules = \"" + "".join(rules) + "\""))

cc = [ 'XX' ] * 65536

for l in file("LineBreak.txt"):
    m = re.match("(\w+)\.\.(\w+);(\w\w)", l)
    if m:
        start = int(m.group(1), 16)
        end = int(m.group(2), 16)

        if start > 65535:
            continue

        if end > 65535:
            end = 65535

        for i in range(start, end + 1):
            cc[i] = m.group(3)

        continue

    m = re.match("(\w+);(\w\w)", l)
    if m:
        start = int(m.group(1), 16)

        if start > 65535:
            continue

        cc[start] = m.group(2)
        continue


def generate(name, func):

    ncc = [ ]

    for i, ccl in enumerate(cc):
        ncc.append(func(i, ccl))

    assert "CJ" not in ncc
    assert "AI" not in ncc

    print(("cdef char *break_" + name + " = \"" + "".join("\\x%02x" % cl[i] for i in ncc) + "\""))


def western(i, cl):
    if cl == "CJ":
        return "ID"
    elif cl == "AI":
        return "AL"

    return cl

hyphens = [ 0x2010, 0x2013, 0x301c, 0x30a0 ]

iteration = [ 0x3005, 0x303B, 0x309D, 0x309E, 0x30FD, 0x30FE ]
inseperable = [ 0x2025, 0x2026 ]

centered = [ 0x003A, 0x003B, 0x30FB, 0xff1a, 0xff1b, 0xff65, 0x0021, 0x003f, 0x203c, 0x2047, 0x2048, 0x2049, 0xff01, 0xff1f ]
postfixes = [ 0x0025, 0x00A2, 0x00B0, 0x2030, 0x2032, 0x2033, 0x2103, 0xff05, 0xffe0 ]
prefixes = [ 0x0024, 0x00a3, 0x00a5, 0x20ac, 0x2116, 0xff04, 0xffe1, 0xffe5 ]


def cjk_strict(i, cl):

    if cl == "CJ":
        return "NS"
    if cl == "AI":
        return "ID"

    return cl


def cjk_normal(i, cl):

    if i in hyphens:
        return "ID"

    if cl == "CJ":
        return "ID"
    if cl == "AI":
        return "ID"

    return cl


def cjk_loose(i, cl):

    if i in hyphens:
        return "ID"
    if i in iteration:
        return "ID"
    if i in inseperable:
        return "ID"
    if i in centered:
        return "ID"
    if i in postfixes:
        return "ID"
    if i in prefixes:
        return "ID"

    if cl == "CJ":
        return "ID"
    if cl == "AI":
        return "ID"

    return cl

generate("western", western)
generate("cjk_strict", cjk_strict)
generate("cjk_normal", cjk_normal)
generate("cjk_loose", cjk_loose)
