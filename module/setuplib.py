# Copyright 2004-2019 Tom Rothamel <pytom@bishoujo.us>
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

import distutils.core

# This flag determines if we are compiling for Android or not.
android = "RENPY_ANDROID" in os.environ

# True if we're building on ios.
ios = "RENPY_IOS" in os.environ

# True of we're building on raspberry pi.
raspi = "RENPY_RASPBERRY_PI" in os.environ

# True of we're building with emscripten.
emscripten = "RENPY_EMSCRIPTEN" in os.environ

# Is coverage enabled?
coverage = "RENPY_COVERAGE" in os.environ

# Are we doing a static build?
static = "RENPY_STATIC" in os.environ

if coverage:
    gen = "gen.coverage"
else:
    gen = "gen"


if static:
    gen += "-static"


# The cython command.
cython_command = os.environ.get("RENPY_CYTHON", "cython")

# Note that the android build sets up CFLAGS for us, and ensures
# that necessary libraries are present. So autoconfiguration is
# unnecessary on that platform.

# The install variable is a list of directories that have Ren'Py
# dependencies installed in them.
if not (android or ios):
    install = os.environ.get("RENPY_DEPS_INSTALL", "/usr")

    if "::" in install:
        install = install.split("::")
    else:
        install = install.split(os.pathsep)

    install = [ os.path.abspath(i) for i in install ]

    if "VIRTUAL_ENV" in os.environ:
        install.insert(0, os.environ["VIRTUAL_ENV"])

else:
    install = [ ]

# The include and library dirs that we compile against.
include_dirs = [ "." ]
library_dirs = [ ]

# Extra arguments that will be given to the compiler.
extra_compile_args = [ ]
extra_link_args = [ ]


def include(header, directory=None, optional=True):
    """
    Searches the install paths for `header`. If `directory` is given, we
    will append that to each of the install paths when trying to find
    the header. The directory the header is found in is added to include_dirs
    if it's not present already.

    `optional`
        If given, returns False rather than abandoning the process.
    """

    if android or ios or emscripten:
        return True

    for i in install:

        if directory is not None:
            idir = os.path.join(i, "include", directory)
        else:
            idir = os.path.join(i, "include")

        fn = os.path.join(idir, header)

        if os.path.exists(fn):

            if idir not in include_dirs:
                include_dirs.append(idir)

            return True

    if optional:
        return False

    if directory is None:
        print("Could not find required header {0}.".format(header))
    else:
        print("Could not find required header {0}/{1}.".format(directory, header))

    sys.exit(-1)


def library(name, optional=False):
    """
    Searches for `library`.

    `optional`
        If true, this function will return False if a library is not found,
        rather than reporting an error.
    """

    if android or ios or emscripten:
        return True

    for i in install:

        for ldir in [i, os.path.join(i, "lib"), os.path.join(i, "lib64"), os.path.join(i, "lib32") ]:

            for suffix in ( ".so", ".a", ".dll.a", ".dylib" ):

                fn = os.path.join(ldir, "lib" + name + suffix)

                if os.path.exists(fn):

                    if ldir not in library_dirs:
                        library_dirs.append(ldir)

                    return True

    if optional:
        return False

    print("Could not find required library {0}.".format(name))
    sys.exit(-1)


# A list of extension objects that we use.
extensions = [ ]

# A list of macros that are defined for all modules.
global_macros = [ ]


def cmodule(name, source, libs=[], define_macros=[], includes=[], language="c"):
    """
    Compiles the python module `name` from the files given in
    `source`, and the libraries in `libs`.
    """

    eca = list(extra_compile_args)

    if language == "c":
        eca.insert(0, "-std=gnu99")

    extensions.append(distutils.core.Extension(
        name,
        source,
        include_dirs=include_dirs + includes,
        library_dirs=library_dirs,
        extra_compile_args=eca,
        extra_link_args=extra_link_args,
        libraries=libs,
        define_macros=define_macros + global_macros,
        language=language,
        ))


necessary_gen = [ ]


def cython(name, source=[], libs=[], includes=[], compile_if=True, define_macros=[], pyx=None, language="c"):
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

    if os.path.exists(os.path.join("..", fn)):
        fn = os.path.join("..", fn)
    elif os.path.exists(fn):
        pass
    else:
        print("Could not find {0}.".format(fn))
        sys.exit(-1)

    module_dir = os.path.dirname(fn)

    # Figure out what it depends on.
    deps = [ fn ]

    f = file(fn)
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
    f.close()

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

    out_of_date = False

    # print c_fn, "depends on", deps

    for dep_fn in deps:

        if os.path.exists(os.path.join(module_dir, dep_fn)):
            dep_fn = os.path.join(module_dir, dep_fn)
        elif os.path.exists(os.path.join("..", dep_fn)):
            dep_fn = os.path.join("..", dep_fn)
        elif os.path.exists(os.path.join("include", dep_fn)):
            dep_fn = os.path.join("include", dep_fn)
        elif os.path.exists(os.path.join(gen, dep_fn)):
            dep_fn = os.path.join(gen, dep_fn)
        elif os.path.exists(dep_fn):
            pass
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

        try:
            import subprocess

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

            subprocess.check_call([
                cython_command,
                "-Iinclude",
                "-I" + gen,
                "-I..",
                ] + annotate + lang_args + coverage_args + [
                fn,
                "-o",
                c_fn])

            # Fix-up source for static loading
            if static and (len(split_name) > 1):
                parent_module = '.'.join(split_name[:-1])
                parent_module_identifier = parent_module.replace('.', '_')
                with open(c_fn, 'r') as f:
                    ccode = f.read()
                ccode = re.sub('Py_InitModule4\("([^"]+)"', 'Py_InitModule4("'+parent_module+'.\\1"', ccode)
                ccode = re.sub('^__Pyx_PyMODINIT_FUNC init', '__Pyx_PyMODINIT_FUNC init'+parent_module_identifier+'_', ccode, 0, re.MULTILINE)  # Cython 0.28.2
                ccode = re.sub('^PyMODINIT_FUNC init', 'PyMODINIT_FUNC init'+parent_module_identifier+'_', ccode, 0, re.MULTILINE)  # Cython 0.25.2
                with open(c_fn, 'w') as f:
                    f.write(ccode)

        except subprocess.CalledProcessError as e:
            print()
            print(str(e))
            print()
            sys.exit(-1)

    # Build the module normally once we have the c file.
    if compile_if:

        if mod_coverage:
            define_macros = define_macros + [ ("CYTHON_TRACE", "1") ]

        cmodule(name, [ c_fn ] + source, libs=libs, includes=includes, define_macros=define_macros, language=language)


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

    sf = file(sfn, "rb")
    data = sf.read()
    sf.close()

    if replace:
        data = data.replace(replace, replace_with)

    df = file(dfn, "wb")
    df.write("# This file was automatically generated from " + source + "\n")
    df.write("# Modifications will be automatically overwritten.\n\n")
    df.write(data)
    df.close()

    import shutil
    shutil.copystat(sfn, dfn)


def setup(name, version):
    """
    Calls the distutils setup function.
    """

    distutils.core.setup(
        name=name,
        version=version,
        ext_modules=extensions,
        py_modules=py_modules,
        )


# Ensure the gen directory exists.
if not os.path.exists(gen):
    os.mkdir(gen)
