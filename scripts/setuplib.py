# Copyright 2004-2025 Tom Rothamel <pytom@bishoujo.us>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# This file encapsulates much of the complexity of the Ren'Py build process,
# so setup.py can be clean by comparison.

from __future__ import print_function

import os
import sys
import re
import threading
import warnings
import pathlib
import platform
import subprocess
from concurrent.futures import ThreadPoolExecutor

import setuptools

warnings.simplefilter("ignore", category=setuptools.SetuptoolsDeprecationWarning)

# Platform selection.
windows = platform.win32_ver()[0]
macintosh = platform.mac_ver()[0]
linux = not windows and not macintosh

# Is coverage enabled?
coverage = "RENPY_COVERAGE" in os.environ

# Are we doing a static build?
static = "RENPY_STATIC" in os.environ

gen = "tmp/gen3"
PY2 = False

if coverage:
    gen += "-coverage"

if static:
    gen += "-static"

# The cython command.
cython_command = os.environ.get("RENPY_CYTHON", "cython")

# The include and library dirs that we compile against.
include_dirs = [ "src" ]
library_dirs = [ ]

# Extra arguments that will be given to the compiler.
extra_compile_args = [ ]
extra_link_args = [ ]


# The libraries that we link against.
libraries = [ ]

def library(name):
    """
    Links `name` into the build.
    """

    libraries.append(name)


# A list of extension objects that we use.
extensions = [ ]

# A list of macros that are defined for all modules.
global_macros = [ ]


def cmodule(name, source, define_macros=[], language="c", compile_args=[]):
    """
    Compiles `name`, as a Python module.

    `source`
        A list of source files that make up the module.

    `define_macros`
        A list of macros that are defined when compiling the module files.

    `language`
        The language that the module is written in. This is either "c" or "c++".

    `compile_args`
        A list of additional arguments that are passed to the compiler.
    """

    eca = list(extra_compile_args) + compile_args

    if language == "c":
        eca.insert(0, "-std=gnu99")

    extensions.append(setuptools.Extension(
        name,
        source,
        include_dirs=include_dirs,
        library_dirs=library_dirs,
        extra_compile_args=eca,
        extra_link_args=extra_link_args,
        libraries=libraries,
        define_macros=define_macros + global_macros,
        language=language,
        ))


# A list of cython files that were necessary to generate.
necessary_gen = [ ]

# A list of cython generation commands that will be run in parallel.
generate_cython_queue = [ ]

def cython(name, source=[], define_macros=[], pyx=None, language="c", compile_args=[]):
    """
    Compiles a cython module. This takes care of regenerating it as necessary
    when it, or any of the files it depends on, changes.
    """

    mod_coverage = coverage

    # Find the pyx file.
    split_name = name.split(".")

    if pyx is not None:
        fn = pyx
    else:
        fn = "/".join(split_name) + ".pyx"

    for d in [ ".", "src" ]:
        prepended = os.path.join(d, fn)
        if os.path.exists(prepended):
            fn = prepended
            break
    else:
        raise SystemExit("Could not find {0}.".format(fn))


    module_dir = os.path.dirname(fn)

    # Figure out what it depends on.
    deps = [ fn ]

    with open(fn) as f:
        for l in f:
            m = re.search(r'from\s*([\w.]+)\s*cimport', l)
            if m:
                deps.append(m.group(1).replace(".", "/") + ".pxd")
                continue

            m = re.search(r'cimport\s*([\w.]+)', l)
            if m:
                deps.append(m.group(1).replace(".", "/") + ".pxd")
                continue

            m = re.search(r'include\s*"(.*?)"', l)
            if m:
                deps.append(m.group(1))
                continue

    # Filter out cython stdlib dependencies.
    deps = [ i for i in deps if (not i.startswith("cpython/")) and (not i.startswith("libc/")) ]

    # Determine if any of the dependencies are newer than the c file.

    if language == "c++":
        c_fn = os.path.join(gen, name + ".cc")
        necessary_gen.append(name + ".cc")
    else:
        c_fn = os.path.join(gen, name + ".c")
        necessary_gen.append(name + ".c")

    if os.path.exists(c_fn):
        c_mtime = os.path.getmtime(c_fn)
    else:
        c_mtime = 0

    out_of_date = "RENPY_REGENERATE_CYTHON" in os.environ

    # print c_fn, "depends on", deps

    for dep_fn in deps:

        for d in [ module_dir, ".", "src", gen ]:
            prepended = os.path.join(d, dep_fn)
            if os.path.exists(prepended):
                dep_fn = prepended
                break
        else:
            print("{0} depends on {1}, which can't be found.".format(fn, dep_fn))
            sys.exit(-1)

        if os.path.getmtime(dep_fn) > c_mtime:
            out_of_date = True

    if out_of_date and not cython_command:
        print("WARNING:", name, "is out of date, but RENPY_CYTHON isn't set.")
        out_of_date = False

    # If the file is out of date, regenerate it.
    if out_of_date:
        print(name, "is out of date.")

        generate_cython_queue.append((name, language, mod_coverage, split_name, fn, c_fn))

    # Build the module normally once we have the c file.

    if mod_coverage:
        define_macros = define_macros + [ ("CYTHON_TRACE", "1") ]

    cmodule(name, [ c_fn ] + source,define_macros=define_macros, language=language, compile_args=compile_args)


lock = threading.Condition()
cython_failure = False

def generate_cython(name, language, mod_coverage, split_name, fn, c_fn):
    import subprocess
    global cython_failure

    if language == "c++":
        lang_args = [ "--cplus" ]
    else:
        lang_args = [ ]

    if "RENPY_ANNOTATE_CYTHON" in os.environ:
        annotate = [ "-a" ]
    else:
        annotate = [ ]

    if mod_coverage:
        coverage_args = [ "-X", "linetrace=true" ]
    else:
        coverage_args = [ ]

    p = subprocess.Popen([
            cython_command,
            "-Isrc",
            "-I" + gen,
            "-I.",
            "-3",
            ] + annotate + lang_args + coverage_args + [
            "-X", "profile=False",
            "-X", "embedsignature=True",
            fn,
            "-o",
            c_fn], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    stdout, stderr = p.communicate()

    with lock:
        print("-", name, "-" * (76 - len(name)))
        if stdout:
            print(stdout.decode("utf-8", "surrogateescape"))
            print("")

    if p.returncode:
        cython_failure = True
        return

    # Fix-up source for static loading
    if static:
        parent_module = '.'.join(split_name[:-1])
        parent_module_identifier = parent_module.replace('.', '_')

        with open(c_fn, 'r') as f:
            ccode = f.read()

        with open(c_fn + ".dynamic", 'w') as f:
            f.write(ccode)

        if len(split_name) > 1:
            ccode = re.sub(r'Py_InitModule4\("([^"]+)"', 'Py_InitModule4("' + parent_module + '.\\1"', ccode) # Py2
            ccode = re.sub(r'(__pyx_moduledef.*?"){}"'.format(re.escape(split_name[-1])), '\\1' + '.'.join(split_name) + '"', ccode, count=1, flags=re.DOTALL) # Py3
            ccode = re.sub(r'^__Pyx_PyMODINIT_FUNC init', '__Pyx_PyMODINIT_FUNC init' + parent_module_identifier + '_', ccode, 0, re.MULTILINE) # Py2 Cython 0.28+
            ccode = re.sub(r'^__Pyx_PyMODINIT_FUNC PyInit_', '__Pyx_PyMODINIT_FUNC PyInit_' + parent_module_identifier + '_', ccode, 0, re.MULTILINE) # Py3 Cython 0.28+
            ccode = re.sub(r'^PyMODINIT_FUNC init', 'PyMODINIT_FUNC init' + parent_module_identifier + '_', ccode, 0, re.MULTILINE) # Py2 Cython 0.25.2

        with open(c_fn, 'w') as f:
            f.write(ccode)


def generate_all_cython():
    """
    Run all of the cython that needs to be generated.
    """

    if "RENPY_CYTHON_SINGLETHREAD" in os.environ:
        for args in generate_cython_queue:
            generate_cython(*args)
            if cython_failure:
                sys.exit(1)
    else:
        with ThreadPoolExecutor() as executor:
            for args in generate_cython_queue:
                executor.submit(generate_cython, *args)

        if cython_failure:
            sys.exit(1)


def find_unnecessary_gen():

    for i in os.listdir(gen):
        if not i.endswith(".c"):
            continue

        if i in necessary_gen:
            continue

        print("Unnecessary file", os.path.join(gen, i))


py_modules = [ ]


def pymodule(name):
    """
    Causes a python module to be included in the build.
    """

    py_modules.append(name)


def copyfile(source, dest, replace=None, replace_with=None):
    """
    Copy `source` to `dest`, preserving the modification time.

    If `replace` is given, instances of `replace` in the file contents are
    replaced with `replace_with`.
    """

    sfn = os.path.join("..", source)
    dfn = os.path.join("..", dest)

    if os.path.exists(dfn):
        if os.path.getmtime(sfn) <= os.path.getmtime(dfn):
            return

    with open(sfn, "r") as sf:
        data = sf.read()

    if replace and (replace_with is not None):
        data = data.replace(replace, replace_with)

    with open(dfn, "w") as df:
        df.write("# This file was automatically generated from " + source + "\n")
        df.write("# Modifications will be automatically overwritten.\n\n")
        df.write(data)

    import shutil
    shutil.copystat(sfn, dfn)


def env(name, pkgconfig_command=None):
    """
    This sets an environment variable, if require. The logic is:

    * If NAME is set, then keep it.
    * Otherwise, if RENPY_NAME is set, then set NAME to RENPY_NAME.
    * Otherwise, if pkgconfig_command is set, run it and set NAME to the output.
    """

    renpy_name = "RENPY_" + name
    if (renpy_name in os.environ) and (name not in os.environ):
        os.environ[name] = os.environ[renpy_name]

    if name in os.environ:
        return

    if pkgconfig_command is None:
        return

    try:
        os.environ[name] = subprocess.check_output(pkgconfig_command, shell=True, text=True).strip()
    except Exception:
        print(f"Could not run pkg-config to set {name}. Consider setting {name} or {renpy_name} manually.")


def init():
    """
    Should be  called before anything else to initialize this module.
    """

    os.makedirs(gen, exist_ok=True)


def check_imports(directory, *module_files):
    """
    This checks that the only module files imported from `directory` are listed in `module_files`.
    """

    directory = pathlib.Path(directory)

    for m in sys.modules.values():
        fn = getattr(m, "__file__", None)
        if fn is None:
            continue

        try:
            p = pathlib.Path(fn).relative_to(directory)
        except ValueError:
            continue

        if str(p) not in module_files:
            print("Module", p, "is imported, but not listed in check_imports. (And probably not distributed.)")


def setup(name, version):
    """
    Calls the distutils setup function.
    """

    if (len(sys.argv) >= 2) and (sys.argv[1] == "generate"):
        return

    setuptools.setup(
        name=name,
        version=version,
        ext_modules=extensions,
        py_modules=py_modules,
        zip_safe=False,
        )
