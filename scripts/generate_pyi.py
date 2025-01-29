#!/usr/bin/env python3

from __future__ import annotations

TYPING_IMPORTS = "List, Dict, Tuple, Set, Optional, Union, Any, Callable, Type".split(", ")

from typing import List, Dict, Tuple, Set, Optional, Union, Any, Callable, Type, TextIO

import sys
import pathlib
import textwrap
import inspect
import types
import json

ROOT = pathlib.Path(__file__).parent.parent.absolute()
sys.path.insert(0, str(ROOT))

import _renpy
import renpy
renpy.import_all()

import pygame_sdl2
pygame_sdl2.import_as_pygame()

# Patch renpy.script so the Lexer can be used.
class FakeScript:
    all_pyexpr = None

renpy.game.script = FakeScript()

generated_files = [ ]

def python_signature(o):
    """
    Given a callabale object, try to return a python-style type signature.
    Returns the signature as a string if it can be determined, or None if
    no signature can be determined.

    This first uses inspect.signature to analyze the object. If that doesn't
    work, it looks for a signature on the first line of the docstring.
    If the signature containst Cython typing, it's converted to Python.
    """

    if not callable(o):
        return None

    # If this is pure-python, then just inspect the signature.
    try:
        sig = inspect.signature(o)
        return (str(sig))
    except Exception:
        pass

    # Otherwise, look at the docstring.
    s = getattr(o, "__doc__", "")

    renpy.game.script.all_pyexpr = [ ]


    s = s.split("\n\n")[0]

    if "(" not in s:
        return None

    if ")" not in s:
        return None

    s = s.replace("-> void", "")

    lines = renpy.parser.list_logical_lines('<test>', s, 1, add_lines=True)
    nested = renpy.parser.group_logical_lines(lines)

    l = renpy.parser.Lexer(nested)
    l.advance()

    l.word()
    while l.match(r"\."):
        l.word()

    rv = ""

    def consume(pattern):
        nonlocal rv
        m = l.match(pattern)
        if m:
            rv += m

        return m

    consume(r'\(')

    first = True

    while True:
        consume(",")

        if consume(r'\)'):
            break

        consume(r'\**')

        if not first:
            rv += " "
        else:
            first = False

        argname = l.word()

        while True:
            n = l.word()
            if n is not None:
                argname = n
            else:
                break

        rv += argname # type: ignore
        rv += l.delimited_python(",)")

    rv += " "
    rv += l.rest()

    return rv


def generate_namespace(out : TextIO, prefix : str, namespace : types.ModuleType|type):
    """
    This generates type information for a module or class namespace.
    """

    # Imports.
    for k, v in sorted(namespace.__dict__.items()):

        if not isinstance(v, types.ModuleType):
            continue

        name = v.__name__

        if name == k:
            out.write(prefix + f"import {name}\n")
        elif isinstance(namespace, types.ModuleType) and name == f"{namespace.__name__}.{k}":
            out.write(prefix + f"from . import {k}\n")
        else:
            out.write(prefix + f"import {name} as {k}\n")

    out.write("\n")

    generated = False

    # Classes, methods, and functions.
    for k, v in sorted(namespace.__dict__.items()):

        if k in TYPING_IMPORTS:
            continue

        if k in [ "__new__", "__init__" ]:
            continue

        if isinstance(v, type):

            if v.__module__ != namespace.__name__:
                if v.__module__.startswith("renpy") or v.__module__.startswith("pygame_sdl2"):
                    out.write(prefix + f"{k} = {v.__module__}.{v.__name__}\n")
                else:
                    out.write(prefix + f"from {v.__module__} import {v.__name__}\n")
                out.write("\n")
                generated = True
                continue

            # Bases and class name.
            bases = [ i.__module__ + "." + i.__name__ for i in v.__bases__  if i != object ]

            if bases:
                bases_clause = f"({', '.join(bases)})"
            else:
                bases_clause = ""

            out.write(prefix + f"class {v.__name__}{bases_clause}:\n")

            # Figure out the signature for init.
            init_sig = None

            try:
                init_sig = python_signature(v)
            except Exception:
                pass

            if not init_sig:
                try:
                    init_sig = python_signature(v.__init__)
                except Exception:
                    pass


            if init_sig:

                if "(self" not in init_sig:
                    init_sig = "(self, " + init_sig[1:]

                out.write(prefix + f"    def __init__{init_sig}: ...\n")

            # Methods and other contents.
            generate_namespace(out, prefix + "    ", v)

            generated = True

            continue

        try:
            sig = python_signature(v)
        except Exception:
            sig = None

        if sig is None:
            continue

        if prefix and ("(self" not in sig):
            out.write(prefix + "@staticmethod\n")

        out.write(prefix + f"def {k}{sig}: ...\n")
        out.write("\n")

        generated = True


    # Variables.

    for k, v in sorted(namespace.__dict__.items()):
        if isinstance(v, int):
            out.write(prefix + f"{k} : int\n")
            generated = True

    _types = getattr(namespace, "_types", "")

    for l in textwrap.dedent(_types.strip("\n")).split("\n"):
        if l:
            out.write(prefix + l + "\n")
            generated = True

    if not generated:

        out.write(prefix + "pass\n\n")



def generate_module(module : types.ModuleType, package : bool):
    """
    This generates type information for a module.
    """

    if module.__name__.startswith("renpy."):
        base = ROOT
    else:
        base = ROOT / "typings"

    modfn = module.__name__.replace(".", "/")

    if package:
        fn = base / modfn / "__init__.pyi"
    else:
        fn = base / f"{modfn}.pyi"

    if fn.exists() and not fn.read_text().startswith("from typing import"):
        return

    fn.parent.mkdir(parents=True, exist_ok=True)

    with open(fn, "w") as f:
        f.write(f"from typing import {', '.join(TYPING_IMPORTS)}\n\n")
        f.write("import builtins\n")
        f.write("import renpy\n")
        f.write("import pygame_sdl2\n\n")

        generate_namespace(f, "", module)

        generated_files.append(fn)


def is_extension(m : types.ModuleType):
    """
    Returns true if m is an extension module, and False otherwise.
    """

    if m.__file__ == "built-in":
        return True

    if m.__file__.endswith(".so"):
        return True

    if m.__file__.endswith(".pyd"):
        return True

    return False

def should_generate(name, m : Any):
    """
    Returns true if we should generate the type information for the module with
    `name`.
    """

    # E.g. pygame_sdl2.try_import adds MissingModule to sys.modules
    if not isinstance(m, types.ModuleType):
        return False

    prefix = name.partition(".")[0]

    if prefix == "renpy":
        return is_extension(m)

    if prefix in [ "pygame", "pygame_sdl2" ]:
        return True

    return False

def manage_gitignore():

    gitignore = ROOT / ".gitignore"

    old_lines = gitignore.read_text().split("\n")
    new_lines = [ ]

    for l in old_lines:

        if l.endswith(".pyi"):
            continue

        new_lines.append(l)

        if l == "# Pyi Files (generated by scripts/generate_pyi.py)":
            new_lines.extend(generated_files)

    gitignore.write_text("\n".join(new_lines))

def manage_vscode():

    settings = ROOT / ".vscode" / "settings.json"

    with open(settings) as f:
        j = json.load(f)

    files_exclude = j["files.exclude"]

    files_exclude = { k : v for k, v in files_exclude.items() if not k.endswith(".pyi") }

    for i in generated_files:
        files_exclude[str(i)] = True

    j["files.exclude"] = files_exclude

    with open(settings, "w") as f:
        json.dump(j, f, indent=4)


def main():

    global generated_files

    packages = set()

    for name in tuple(sys.modules):
        package = name.rpartition(".")[0]
        packages.add(package)

    for k, v in sorted(sys.modules.items()):

        if not should_generate(k, v):
            continue

        generate_module(v, k in packages)

    generated_files.sort()
    generated_files = [ str(i.relative_to(ROOT)) for i in generated_files ]
    generated_files = [ i for i in generated_files if i.startswith("renpy/") ]

    manage_gitignore()
    manage_vscode()

    for fn in (ROOT / "scripts" / "pyi").glob("**/*.pyi"):
        dfn =  ROOT / "typings" / fn.relative_to(ROOT / "scripts" / "pyi")
        text = fn.read_text()
        dfn.parent.mkdir(parents=True, exist_ok=True)
        dfn.write_text(text)

if __name__ == "__main__":
    main()
