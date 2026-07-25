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

import os
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Literal, TypedDict

import setuptools

coverage = "RENPY_COVERAGE" in os.environ
"True if we are building with coverage enabled."

generate = False
"True if we are generating files without building."

gen: str = "tmp/gen"

if coverage:
    gen += "-coverage"

# The include and library dirs that we compile against.
include_dirs: list[str] = ["src", gen]

# Cache for pkgconfig results.
pkgconfig_cache: dict[str, dict[str, list]] = {}

# Extra arguments to supply to all extensions.
extra_compile_args: list[str] = []
extra_link_args: list[str] = []


def init():
    """
    Should be called before anything else to initialize this module.
    """

    os.makedirs(gen, exist_ok=True)


def check_imports(directory: Path, *module_files: str):
    """
    This checks that the only module files imported from `directory` are listed in `module_files`.
    """

    directory = directory.resolve()

    for m in sys.modules.values():
        fn = getattr(m, "__file__", None)
        if fn is None:
            continue

        try:
            p = Path(fn).relative_to(directory)
        except ValueError:
            continue

        if str(p) not in module_files:
            print(f"Module {p} is imported, but not listed in check_imports. (And probably not distributed.)")


class ExtensionData(TypedDict):
    sources: list[str]
    language: Literal["c", "c++"]
    extra_compile_args: list[str]
    define_macros: list[tuple[str, str | None]]
    packages: list[str]
    depends: list[str]
    setup_filename: str


# A mapping from module name to the data needed to create setuptools.Extension
# if we do actual build.
extensions: dict[str, ExtensionData] = {}

# A list of cython generation commands that will be run in parallel.
generate_cython_queue: list[tuple[str, str, str]] = []


def cython(
    name: str,
    source: list[str] | None = None,
    language: Literal["c", "c++"] = "c",
    compile_args: list[str] | None = None,
    define_macros: list[tuple[str, str | None]] | None = None,
    packages: str = "",
    setup_filename: str = "Setup",
):
    """
    Compiles a cython module. This takes care of regenerating it as necessary
    when it, or any of the files it depends on, changes.
    """

    split_name = name.split(".")
    fn = Path(*split_name).with_suffix(".pyx")

    for d in [".", "src"]:
        prepended = Path(d, fn)
        if prepended.exists():
            fn = prepended
            break
    else:
        raise SystemExit(f"Could not find {fn}.")

    c_fn = fn.relative_to(".")

    if language == "c++":
        c_fn = Path(gen, c_fn).with_suffix(".cpp").as_posix()
    else:
        c_fn = Path(gen, c_fn).with_suffix(".c").as_posix()

    define_macros = define_macros or []
    if coverage:
        define_macros += [("CYTHON_TRACE", "1")]

    extensions[name] = ExtensionData(
        sources=[c_fn] + (source or []),
        language=language,
        extra_compile_args=list(compile_args or []),
        define_macros=list(define_macros or []),
        packages=packages.split(),
        depends=[],
        setup_filename=setup_filename,
    )

    generate_cython_queue.append((name, fn.as_posix(), language))


def generate_all_cython():
    """
    Run all of the cython that needs to be generated.
    """

    if not generate_cython_queue:
        return

    from Cython.Build import cythonize

    force = "RENPY_REGENERATE_CYTHON" in os.environ
    show_all_warnings = "RENPY_CYTHON_SHOW_WARNINGS" in os.environ
    annotate = "RENPY_ANNOTATE_CYTHON" in os.environ

    # Empty string disables caching.
    cache_dir = os.environ.get("RENPY_CYTHON_CACHE_DIR", "tmp/cython_cache")

    if "RENPY_CYTHON_SINGLETHREAD" in os.environ:
        nthreads = 0
    else:
        nthreads = os.cpu_count() or 1

    cython_extensions = [
        setuptools.Extension(
            name=name,
            sources=[fn],
            language=language,
        )
        for name, fn, language in generate_cython_queue
    ]

    ext: setuptools.Extension
    for ext in cythonize(
        cython_extensions,
        build_dir=gen,
        include_path=["src"],
        language_level=3,
        show_all_warnings=show_all_warnings,
        cache=cache_dir,
        force=force,
        annotate=annotate,
        nthreads=nthreads,
        compiler_directives={
            "profile": False,
            "embedsignature": True,
            "embedsignature.format": "python",
            "linetrace": coverage,
        },
    ):
        extensions[ext.name]["depends"] += ext.depends


def generate_setup_files():
    """
    Generates the Setup files for all of the extensions that renpy-build
    consumes for static builds.
    """

    src_dir = Path("src")
    setup_files: dict[str, list[str]] = defaultdict(list)

    for name, data in sorted(extensions.items()):
        sources: list[str] = []
        for source in data["sources"]:
            target = Path(source).relative_to(src_dir, walk_up=True)
            sources.append(target.as_posix())

        setup_files[data["setup_filename"]].append(f"{name} {' '.join(sources)}")

    for setup_filename, lines in setup_files.items():
        (src_dir / setup_filename).write_text("\n".join(lines) + "\n", encoding="utf-8")

def env(name):
    """
    This sets an environment variable, if require. The logic is:

    * If NAME is set, then keep it.
    * Otherwise, if RENPY_NAME is set, then set NAME to RENPY_NAME.
    """

    if f"RENPY_{name}" in os.environ and name not in os.environ:
        os.environ[name] = os.environ[f"RENPY_{name}"]


def package_flags(*packages: str) -> defaultdict[str, Any]:
    """
    Given a list of pkgconfig packages, returns a dict keys that will be
    supplied to Extension to set up the 'libraries', the 'library_dirs', the
    'include_dirs', and the 'define_macros' arguments.
    """

    rv = defaultdict(list)

    import pkgconfig

    for package in packages:
        if package in pkgconfig_cache:
            pc = pkgconfig_cache[package]
        else:
            try:
                pc = pkgconfig.parse(package)
            except pkgconfig.PackageNotFoundError:
                raise SystemExit(f"Could not find pkg-config package '{package}'.")

            pkgconfig_cache[package] = pc

        for k, v in pc.items():
            for i in v:
                if i not in rv[k]:
                    rv[k].append(i)

    return rv


def setup(name, version):
    """
    Calls the distutils setup function. generate_all_cython() must be called
    before this, so that the Cython extensions have been turned into C/C++
    extensions with real source files.
    """

    ext_modules: list[setuptools.Extension] = []
    for name, data in extensions.items():
        package_kwargs = package_flags(*data["packages"])

        ext_include_dirs: list[str] = []
        ext_include_dirs += package_kwargs["include_dirs"]
        ext_include_dirs += include_dirs

        compile_args: list[str] = []

        if data["language"] == "c":
            compile_args.append("-std=gnu99")

        compile_args += data["extra_compile_args"]
        compile_args += extra_compile_args

        define_macros: list[tuple[str, str | None]] = []
        define_macros += package_kwargs["define_macros"]
        define_macros += data["define_macros"]

        link_args: list[str] = []
        link_args += package_kwargs["library_dirs"]
        link_args += extra_link_args

        ext_modules.append(
            setuptools.Extension(
                name=name,
                sources=data["sources"],
                language=data["language"],
                include_dirs=ext_include_dirs,
                extra_compile_args=compile_args,
                define_macros=define_macros,
                extra_link_args=link_args,
                libraries=package_kwargs["libraries"],
                depends=data["depends"],
            )
        )

    setuptools.setup(
        name=name,
        version=version,
        ext_modules=ext_modules,
        packages=[],
        py_modules=[],
        zip_safe=False,
    )
