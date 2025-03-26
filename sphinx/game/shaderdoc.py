from __future__ import division, absolute_import, with_statement, print_function, unicode_literals

import os
import renpy
import textwrap

import re

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


def textshaders(incdir="source/inc"):

    with open(incdir + "/builtintextshaders", "w") as outf:

        for name, shader in sorted(renpy.config.textshaders.items()):

            if not shader.doc:
                continue

            doc = textwrap.dedent(shader.doc)

            uniforms = { }

            for u, v in shader.uniforms:
                uniforms[u] = v

            def replace_uniform(m):
                u = m.group(1)[1:-1]
                value = uniforms[u]

                u = u.replace("u_textshader_" + name + "_", "u__")

                if isinstance(value, renpy.display.displayable.Displayable):
                    value = "..."
                else:
                    value = repr(value)

                return "`{}` = {}".format(u, value)

            doc = re.sub(r"(`u_.*?`)", replace_uniform, doc)

            outf.write(".. textshader:: {}\n".format(name))
            outf.write("\n")

            for i in doc.split("\n"):
                outf.write("    {}\n".format(i))

            if not shader.include_default:
                outf.write("\n")
                outf.write("    Using this shader will prevent the default text shader from being used.\n")

            outf.write("\n")
