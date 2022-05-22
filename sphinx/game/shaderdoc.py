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

        def priority(sp):
            if sp.vertex_parts:
                return sp.vertex_parts[0][0], sp.name
            else:
                return sp.fragment_parts[0][0], sp.name

        parts.sort(key=priority)

        for sp in parts:

            if sp.name == "renpy.ftl":
                continue

            header = "{} (priority {})".format(sp.name, priority(sp)[0])

            p(header)
            p("^" * len(header))

            if sp.raw_variables:
                p("Variables::")

                s = textwrap.dedent(sp.raw_variables)

                indented(sp.raw_variables)

            if sp.vertex_functions or sp.fragment_functions:
                raise Exception("Can't doc functions yet.")

            for _, s in sp.vertex_parts:
                p("Vertex shader::")

                indented(s)

            for _, s in sp.fragment_parts:
                p("Fragment shader::")

                indented(s)

