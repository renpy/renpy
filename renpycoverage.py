from __future__ import print_function, unicode_literals, division, absolute_import

import Cython.Coverage
# import coverage
import os
import coverage
import cPickle

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

class CythonCoverage(Cython.Coverage.Plugin):

    def _find_source_files(self, filename):

        if not filename.endswith(".pyx"):
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
                return c_fn, filename

        print("Could not find C source for", filename)

        return None, None

    def file_tracer(self, filename):

        if not filename.endswith(".pyx"):
            return None

#         base = os.path.basename(filename)
#         if base.startswith("style_") and base.endswith("_functions.pyx"):
#             return None

        return super(CythonCoverage, self).file_tracer(filename)


class RenpyTracer(coverage.FileTracer):

    def __init__(self, filename):
        self.filename = filename

    def source_filename(self):
        return self.filename

import renpy
renpy_import_all = False


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
