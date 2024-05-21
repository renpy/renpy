from __future__ import division, absolute_import, with_statement, print_function, unicode_literals

import os
import renpy
import textwrap


def shaders(incdir="source/inc"):

    def p(s):
        print(s, file=outf)

    def indented(s):
        s = textwrap.dedent(s)
        for i in s.split("\n"):
            print("    " + i, file=outf)

    with open(os.path.join(incdir, "shadersource"), "w") as outf:

        parts = list(renpy.gl2.gl2shadercache.shader_part.values())
        parts.sort(key=lambda x: x.name)

        for sp in parts:

            if sp.name == "renpy.ftl":
                continue

            header = "{}".format(sp.name)

            p(header)
            p("^" * len(header))

            if sp.raw_variables:
                p("Variables::")

                s = textwrap.dedent(sp.raw_variables)

                indented(sp.raw_variables)

            if sp.vertex_functions or sp.fragment_functions:
                raise Exception("Can't doc functions yet.")

            for prio, s in sorted(sp.vertex_parts):
                p("Vertex shader (priority %d)::" % prio)

                indented(s)

            for prio, s in sorted(sp.fragment_parts):
                p("Fragment shader (priority %d)::" % prio)

                indented(s)
