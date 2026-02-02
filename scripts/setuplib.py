# Copyright 2004-2026 Tom Rothamel <pytom@bishoujo.us>
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
import pkgconfig
import collections

from concurrent.futures import ThreadPoolExecutor

import setuptools

from typing import Any

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
include_dirs = ["src", gen]

# Cache for pkgconfig results.
pkgconfig_cache: dict[str, dict[str, list]] = { }

# Extra arguments to supply to all extensions.
extra_compile_args = []
extra_link_args = []

def package_flags(*packages: str) -> dict[str, Any]:
    """
    Given a list of pkgconfig packages, returns a dict keys that will be supplied to
    Extension to set up the include_dirs, library_dirs, libraries, extra_compile_args,
    """

    rv = collections.defaultdict(list)
    rv["include_dirs"] = include_dirs

    for package in packages:
        if package in pkgconfig_cache:
            pc = pkgconfig_cache[package]
        else:
            try:
                pc = pkgconfig.parse(package)
            except pkgconfig.PackageNotFoundError:
                raise SystemExit(f"Could not find pkg-config package '{package}'.")
                continue

            pkgconfig_cache[package] = pc

        for k, v in pc.items():
            for i in v:
                if i not in rv[k]:
                    rv[k].append(i)
    return rv



# The libraries that we link against.
libraries = []


# A list of extension objects that we use.
extensions = []


def cmodule(name, source, language="c", define_macros=[], compile_args=[], packages=""):
    """
    Compiles `name`, as a Python module.

    `source`
        A list of source files that make up the module.

    `language`
        The language that the module is written in. This is either "c" or "c++".

    `compile_args`
        A list of additional arguments that are passed to the compiler.
    """

    kwargs = package_flags(*packages.split())

    if language == "c":
        kwargs["extra_compile_args"].insert(0, "-std=gnu99")

    kwargs["include_dirs"] = include_dirs + kwargs["include_dirs"]
    kwargs["extra_compile_args"].extend(compile_args)
    kwargs["extra_compile_args"].extend(extra_compile_args)
    kwargs["define_macros"].extend(define_macros)
    kwargs["extra_link_args"].extend(extra_link_args)

    extensions.append(
        setuptools.Extension(
            name,
            source,
            language=language,
            **kwargs,
        )
    )


# A list of cython files that were necessary to generate.
necessary_gen = []

# A list of cython generation commands that will be run in parallel.
generate_cython_queue = []


def cython(name, source=[], pyx=None, language="c", compile_args=[], define_macros=[], packages=""):
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

    for d in [".", "src"]:
        prepended = os.path.join(d, fn)
        if os.path.exists(prepended):
            fn = prepended
            break
    else:
        raise SystemExit("Could not find {0}.".format(fn))

    module_dir = os.path.dirname(fn)

    # Figure out what it depends on.
    deps = [fn]

    def dep(m):
        """
        From a module name, return the corresponding .pxd file, resolving
        relative imports.
        """

        mod_name = m.group(1)
        if mod_name.startswith("."):
            level = len(mod_name) - len(mod_name.lstrip("."))
            base = split_name[:-level]
            rel_mod = mod_name.lstrip(".")
            if rel_mod:
                base.append(rel_mod)
            mod_name = ".".join(base)

        return mod_name.replace(".", "/") + ".pxd"


    with open(fn) as f:
        for line in f:
            m = re.search(r"from\s*([\w.]+)\s*cimport", line)
            if m:
                deps.append(dep(m))
                continue

            m = re.search(r"cimport\s*([\w.]+)", line)
            if m:
                deps.append(dep(m))
                continue

            m = re.search(r'include\s*"(.*?)"', line)
            if m:
                deps.append(m.group(1))
                continue

    # Filter out cython stdlib dependencies.
    deps = [i for i in deps if (not i.startswith("cpython/")) and (not i.startswith("libc/")) and (not i.startswith("libcpp"))]

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
        for d in [module_dir, ".", "src", "src/pygame/include", gen]:
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
        define_macros = define_macros + [("CYTHON_TRACE", "1")]

    cmodule(name, [c_fn] + source, compile_args=compile_args, define_macros=define_macros, language=language, packages=packages)


lock = threading.Condition()
cython_failure = False


def generate_cython(name, language, mod_coverage, split_name, fn, c_fn):
    import subprocess

    global cython_failure

    if language == "c++":
        lang_args = ["--cplus"]
    else:
        lang_args = []

    if "RENPY_ANNOTATE_CYTHON" in os.environ:
        annotate = ["-a"]
    else:
        annotate = []

    if mod_coverage:
        coverage_args = ["-X", "linetrace=true"]
    else:
        coverage_args = []

    includes = ["-Isrc", "-Isrc/pygame/include", f"-I{gen}", "-I."]

    xargs = ["-X", "profile=False", "-X", "embedsignature=True", "-X", "embedsignature.format=python"]

    cmd = [cython_command] + includes + annotate + lang_args + coverage_args + xargs + [fn, "-o", c_fn]

    print(" ".join(cmd))

    p = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

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
        parent_module = ".".join(split_name[:-1])
        parent_module_identifier = parent_module.replace(".", "_")

        with open(c_fn, "r") as f:
            ccode = f.read()

        with open(c_fn + ".dynamic", "w") as f:
            f.write(ccode)

        if len(split_name) > 1:
            ccode = re.sub(r'Py_InitModule4\("([^"]+)"', 'Py_InitModule4("' + parent_module + '.\\1"', ccode)  # Py2
            ccode = re.sub(
                r'(__pyx_moduledef.*?"){}"'.format(re.escape(split_name[-1])),
                "\\1" + ".".join(split_name) + '"',
                ccode,
                count=1,
                flags=re.DOTALL,
            )  # Py3

        with open(c_fn, "w") as f:
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


py_modules = []


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
