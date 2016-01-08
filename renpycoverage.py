from __future__ import print_function, unicode_literals, division, absolute_import

import Cython.Coverage
# import coverage
import os
import coverage
import cPickle
import ast

ROOT = os.path.dirname(os.path.abspath(__file__))

def _find_c_source(base_path):

    base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "module", "gen.coverage", os.path.basename(base_path))

    if os.path.exists(base_path + '.c'):
        c_file = base_path + '.c'
    elif os.path.exists(base_path + '.cpp'):
        c_file = base_path + '.cpp'
    else:
        c_file = None

    return c_file

Cython.Coverage._find_c_source = _find_c_source


class FixedCythonReporter(coverage.FileReporter):

    def __init__(self, old, fn):
#         fn = old.filename
#
#         if not os.path.exists(fn):
#             new_fn = os.path.join(os.path.dirname(fn), "module", os.path.basename(fn))
#             if os.path.exists(new_fn):
#                 fn = new_fn

        super(FixedCythonReporter, self).__init__(fn)

        if old._code is None:
            self._lines = set()
        else:
            self._lines = set(old._code)

    def lines(self):
        return self._lines


class CythonCoverage(Cython.Coverage.Plugin):

    def _find_source_files(self, filename):

        if not filename.endswith(".pyx"):
            return None, None

        pyx_base = os.path.basename(filename)

        pyx_search = [
            "module",
            "module/gen.coverage",
            "module/pysdlsound",
            "renpy",
            "renpy/display",
            "renpy/gl",
            "renpy/styledata",
            "renpy/text",
            ]

        for i in pyx_search:
            pyx_fn = os.path.join(ROOT, i, pyx_base)

            if os.path.exists(pyx_fn):
                break
        else:
            print("Could not find pyx for", filename)
            return None, None


        c_base = os.path.basename(filename)[:-4] + ".c"

        modules = [
            "",
            "renpy.",
            "renpy.display.",
            "renpy.gl.",
            "renpy.styledata.",
            "renpy.text.",
            "pysdlsound."
            ]

        for i in modules:
            c_fn = os.path.join(ROOT, "module", "gen.coverage", i + c_base)
            if os.path.exists(c_fn):
                break
        else:
            print("Could not find C source for", filename)
            return None, None

        return c_fn, pyx_fn


    def file_tracer(self, filename):

        if not filename.endswith(".pyx"):
            return None

        _, pyx_fn = self._find_source_files(filename)

        rv =  super(CythonCoverage, self).file_tracer(pyx_fn)

        def source_filename():
            return pyx_fn

        rv.source_filename = source_filename

        return rv

    def file_reporter(self, filename):

        _, pyx_fn = self._find_source_files(filename)

        r = super(CythonCoverage, self).file_reporter(filename)
        return FixedCythonReporter(r, pyx_fn)


class RenpyTracer(coverage.FileTracer):

    def __init__(self, filename):
        self.filename = filename

    def source_filename(self):
        return self.filename

import renpy
renpy_import_all = False


class PycodeVisitor(ast.NodeVisitor):
    def __init__(self, lines):
        self.lines = lines

    def statement(self, n):
        self.lines.add(n.lineno)
        self.generic_visit(n)

    visit_FunctionDef = statement
    visit_ClassDef = statement
    visit_Return = statement
    visit_Delete = statement
    visit_AugAssign = statement

    visit_Print = statement

    visit_For = statement
    visit_While = statement
    visit_If = statement
    visit_With = statement

    visit_Raise = statement
    visit_TryExcept = statement
    visit_TryFinally = statement

    visit_Assert = statement

    visit_Import = statement
    visit_ImportFrom = statement

    # Global
    visit_Exec = statement

    # pass
    visit_Break = statement
    visit_Continue = statement

    def visit_Expr(self, n):
        if not isinstance(n.value, ast.Str):
            self.lines.add(n.lineno)

        self.generic_visit(n)


class RenpyReporter(coverage.FileReporter):

    def __init__(self, filename):
        super(RenpyReporter, self).__init__(filename)

        global renpy_import_all

        if not renpy_import_all:
            import pygame_sdl2
            pygame_sdl2.import_as_pygame()

            renpy.import_all()

            renpy_import_all = True

            renpy.config.basedir = '/'
            renpy.config.renpy_base = '/'

            # renpy.game.contexts = [ renpy.execution.Context(False) ]
            renpy.game.script = renpy.script.Script()

        # stmts = renpy.parser.parse(filename)

        with open(filename + "c", "rb") as f:
            data = renpy.game.script.read_rpyc_data(f, 1)

        try:
            stmts = cPickle.loads(data)[1]
        except:
            stmts = [ ]
            print(filename + "c", "failed")

        all_stmts = [ ]
        for i in stmts:
            i.get_children(all_stmts.append)

        self._lines = set()
        for i in all_stmts:
            self._lines.add(i.linenumber)

        for i in renpy.game.script.all_pycode:
            self.pycode_lines(i)

        renpy.game.script.all_pycode = [ ]

    def pycode_lines(self, pycode):
        if pycode.mode != 'exec':
            return

        nodes = renpy.python.py_compile(pycode.source, pycode.mode, pycode.location[0], pycode.location[1], ast_node=True)

        v = PycodeVisitor(self._lines)
        for i in nodes:
            v.visit(i)

    def lines(self):
        return self._lines

class RenpyCoverage(coverage.CoveragePlugin):

    def file_tracer(self, filename):

        for i in [ ".rpy", ".rpym" ]:
            if filename.endswith(i):
                break
        else:
            return None

        return RenpyTracer(filename)

    def file_reporter(self, filename):

        return RenpyReporter(filename)


def coverage_init(reg, options):
    reg.add_file_tracer(RenpyCoverage())
    reg.add_file_tracer(CythonCoverage())
