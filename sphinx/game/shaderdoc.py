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

    parts = list(renpy.gl2.gl2shadercache.shader_part.values())
    parts.sort(key=lambda x: x.name)

    vertex_priorities = [ ]
    fragment_priorities = [ ]

    for sp in parts:

        if sp.name == "renpy.ftl":
            continue

        for prio, source in sp.vertex_parts:
            vertex_priorities.append((prio, sp.name))

        for prio, source in sp.fragment_parts:
            fragment_priorities.append((prio, sp.name))

    fragment_priorities.sort()
    vertex_priorities.sort()

    with open(os.path.join(incdir, "shadervertexpriorities"), "w") as outf:

        for prio, name in vertex_priorities:
            p("| %d. :ref:`%s <shader-%s>`" % (prio, name, name))

    with open(os.path.join(incdir, "shaderfragmentpriorities"), "w") as outf:

        for prio, name in fragment_priorities:
            p("| %d. :ref:`%s <shader-%s>`" % (prio, name, name))

    with open(os.path.join(incdir, "shadersource"), "w") as outf:

        # Shaders.
        for sp in parts:

            if sp.name == "renpy.ftl":
                continue

            header = "{}".format(sp.name)

            p(".. _shader-{}:".format(sp.name))
            p("")

            p(header)
            p("-" * len(header))

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
