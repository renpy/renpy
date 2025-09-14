# encoding: utf-8

# Based on: http://www.unicode.org/Public/UNIDATA/LineBreak.txt
# Based on: http://unicode.org/reports/tr14/#PairBasedImplementation

from __future__ import print_function

import re
import pathlib

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

breaking_lines = breaking.split("\n")

other_classes = " PITCH AI BK CB CJ CR LF NL SA SG SP HH AK AP AS VI VF EB EM XX"

def main():

    fn = pathlib.Path(__file__).parent.parent.parent / "renpy" / "text" / "linebreak.pxi"

    with open(fn, "w") as f:

        print("# This is generated code. Do not edit.", file=f)
        print(file=f)

        # A map from character class to the number that represents it.
        cl = {}


        for i, j in enumerate((breaking_lines[0] + other_classes).split()):
            print(("cdef char BC_{} = {}".format(j, i)), file=f)
            cl[j] = i

        print("CLASSES = {", file=f)

        for i, j in enumerate((breaking_lines[0] + other_classes).split()):
            print(('    "{}" : {},'.format(j, i)), file=f)
            cl[j] = i

        print("}", file=f)

        rules = []

        for l in breaking_lines[1:]:
            for c in l.split()[1:]:
                rules.append(c)

        print(file=f)
        print(('cdef char *break_rules = "' + "".join(rules) + '"'), file=f)


        # The number of characters that this matches.
        CHAR_COUNT = 65536 * 2
        cc = ["XX"] * CHAR_COUNT


        for l in open("LineBreak.txt"):
            m = re.match(r"(\w+)\.\.(\w+)\s*;\s*(\w\w)", l)
            if m:
                start = int(m.group(1), 16)
                end = int(m.group(2), 16)

                if start >= CHAR_COUNT:
                    continue

                if end >= CHAR_COUNT:
                    end = CHAR_COUNT - 1

                for i in range(start, end + 1):
                    cc[i] = m.group(3)

                continue

            m = re.match(r"(\w+)\s*;\s*(\w\w)", l)
            if m:
                start = int(m.group(1), 16)

                if start >= CHAR_COUNT:
                    continue

                cc[start] = m.group(2)
                continue


        def generate(name, func):
            ncc = []

            for i, ccl in enumerate(cc):
                ncc.append(func(i, ccl))

            assert "CJ" not in ncc
            assert "AI" not in ncc

            print(("cdef char *break_" + name + ' = "' + "".join("\\x%02x" % cl[i] for i in ncc) + '"'), file=f)


        def common_class(cl):
            if cl in { "AK", "AP", "AS", "VI", "VF", "EB", "EM" }:
                return "AL"
            else:
                return cl

        def western(i, cl):
            cl = common_class(cl)

            if cl == "CJ":
                return "ID"
            elif cl == "AI":
                return "AL"


            return cl


        hyphens = [0x2010, 0x2013, 0x301C, 0x30A0]

        iteration = [0x3005, 0x303B, 0x309D, 0x309E, 0x30FD, 0x30FE]
        inseperable = [0x2025, 0x2026]

        centered = [
            0x003A,
            0x003B,
            0x30FB,
            0xFF1A,
            0xFF1B,
            0xFF65,
            0x0021,
            0x003F,
            0x203C,
            0x2047,
            0x2048,
            0x2049,
            0xFF01,
            0xFF1F,
        ]
        postfixes = [0x0025, 0x00A2, 0x00B0, 0x2030, 0x2032, 0x2033, 0x2103, 0xFF05, 0xFFE0]
        prefixes = [0x0024, 0x00A3, 0x00A5, 0x20AC, 0x2116, 0xFF04, 0xFFE1, 0xFFE5]


        def cjk_strict(i, cl):
            cl = common_class(cl)

            if cl == "CJ":
                return "NS"
            if cl == "AI":
                return "ID"

            return cl


        def cjk_normal(i, cl):
            cl = common_class(cl)

            if i in hyphens:
                return "ID"

            if cl == "CJ":
                return "ID"
            if cl == "AI":
                return "ID"

            return cl


        def cjk_loose(i, cl):
            cl = common_class(cl)

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


        print("DEF BREAK_CHARACTER_COUNT = {}".format(CHAR_COUNT), file=f)

        generate("western", western)
        generate("cjk_strict", cjk_strict)
        generate("cjk_normal", cjk_normal)
        generate("cjk_loose", cjk_loose)


if __name__ == "__main__":
    main()
