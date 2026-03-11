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

from typing import Iterable, Literal, NamedTuple, overload
from importlib._bootstrap_external import _classify_pyc, _compile_bytecode

import renpy
import sys
import io
import time
import pathlib
import importlib.machinery
import importlib.abc
import importlib.util
import importlib.resources.abc

from renpy.loader import TreeEntry

PREFER_LOADER: bool = False
"This can be set to True to prefer the Ren'Py loader for Python imports, for testing purposes."

if PREFER_LOADER:
    print("Using Ren'Py loader for Python imports.")

# Package Resources

class RenpyPath(importlib.resources.abc.Traversable):
    """
    A class that represents a traversable resource in a Ren'Py package.
    """

    path: str
    "The path to the resource, relative to the game directory."

    tree: TreeEntry | None
    "The tree structure of the resource, or None if it is a file."

    def __init__(self, path: str, tree: TreeEntry|None):
        self.path = path
        self.tree = tree

    @property
    def name(self) -> str:
        return self.path.rpartition("/")[2]

    def iterdir(self):
        if not isinstance(self.tree, dict):
            return NotADirectoryError(f"Not a directory: {self.path}")

        for name, entry in self.tree.items():
            yield RenpyPath(self.path + "/" + name, entry)

    def is_dir(self) -> bool:
        return isinstance(self.tree, dict)

    def is_file(self) -> bool:
        return self.tree is True

    def __truediv__(self, other: str) -> "RenpyPath":
        path = f"{self.path}/{other}"

        if isinstance(self.tree, dict):
            return RenpyPath(path, self.tree.get(other, None))
        else:
            return RenpyPath(path, None)

    def joinpath(self, *args: str) -> "RenpyPath":
        rv = self

        for i in args:
            for j in i.strip("/").split("/"):
                rv = rv / j

        return rv

    def open(self, mode: str = "r", *args, **kwargs) -> io.BufferedReader | io.TextIOWrapper:  # type:ignore[reportIncompatibleMethodOverride]
        """
        Opens the resource for reading.
        """
        if not self.is_file():
            raise NotADirectoryError(f"Not a file: {self.path}")

        f = renpy.loader.load(self.path)

        if mode == "r":
            return io.TextIOWrapper(f, *args, **kwargs)
        else:
            return f

    def read_text(self, encoding=None) -> str:
        with self.open("r", encoding=encoding) as f:
            assert isinstance(f, io.TextIOWrapper)
            return f.read()

    def read_bytes(self) -> bytes:
        with self.open("rb") as f:
            assert isinstance(f, io.BufferedReader)
            return f.read()


class RenpyResourceReader(importlib.resources.abc.TraversableResources):

    def __init__(self, path: str):
        self.path = path

    def files(self) -> importlib.resources.abc.Traversable:
        """
        Returns a Traversable object representing the resource.
        """

        if not self.path.startswith("$game/"):
            return pathlib.Path(self.path)

        path = self.path[6:]

        rv = RenpyPath("", renpy.loader.tree)  # type:ignore[reportAbstractUsage]

        for i in path.strip("/").split("/"):
            rv = rv / i

        return rv


# Module Loading
class RenpyImporter(importlib.abc.MetaPathFinder, importlib.abc.InspectLoader):
    """
    A meta-path importer, that tries to load pure Python modules from the places
    where Ren'Py searches for data files.
    """

    def __init__(self):
        self.prefixes: list[str] = []
        "List of prefixes where modules can be found."

        self._finder_cache: dict[str, RenpyImporter._ModuleInfo] | None = None
        """
        A dict from module name to module info of that module for all paths that
        can be loaded with this importer.
        """

    def add_prefix(self, prefix: str):
        if prefix and not prefix.endswith("/"):
            prefix = prefix + "/"

        if prefix in self.prefixes:
            return

        self.prefixes.append(prefix)
        self.invalidate_caches()

    class _ModuleInfo(NamedTuple):
        filename: str
        is_package: bool
        is_namespace: bool

    def _visit_dir(self, *path: str, files: Iterable[str]):
        dir_to_fn: dict[str, list[str]] = {}
        seen_init = False
        prefix = ""
        if path:
            prefix += "/".join(path) + "/"
        mod_name_base = ".".join(path) if path else ""

        for fn in files:
            if "/" in fn:
                top_directory, _, sub_fn = fn.partition("/")
                if top_directory not in dir_to_fn:
                    dir_to_fn[top_directory] = []
                dir_to_fn[top_directory].append(sub_fn)
                continue

            if fn.endswith(".py"):
                stem = fn[:-3]
            elif fn.endswith(".pyc"):
                stem = fn[:-4]

            if stem is None:
                continue

            if stem == "__init__":
                seen_init = True
                mod_name = mod_name_base
                is_package = True
            else:
                is_package = False

                mod_name = mod_name_base + ("." + stem if mod_name_base else stem)

            py_file  = stem + ".py"
            pyc_file = stem + ".pyc"

            if py_file in files:
                chosen_filename = prefix+py_file
            elif pyc_file in files:
                chosen_filename = prefix+pyc_file
                # Optional: log when falling back
                # print(f"Falling back to {chosen_filename} (no {py_full})")
            else:
                # Should not happen because fn came from files, but safety
                continue
            
            #print('mod_name', mod_name, is_package, '->', chosen_filename)
            mod_info = RenpyImporter._ModuleInfo(chosen_filename, is_package, False)
            yield mod_name, mod_info

        if path and not seen_init:
            yield mod_name_base, RenpyImporter._ModuleInfo(prefix, True, True)

        for add_dir, subfiles in dir_to_fn.items():
            yield from self._visit_dir(*path, add_dir, files=subfiles)
            
    def _cache_entries(self) -> dict[str, _ModuleInfo]:
        if self._finder_cache is not None:
            return self._finder_cache

        if not renpy.loader.game_files:
            renpy.loader.scandirfiles()

        self._finder_cache = dict(
            self._visit_dir(files=(fn for _, fn in renpy.loader.game_files if (fn.endswith(".py") or fn.endswith(".pyc")) if not fn.endswith("_ren.py")))
        )
        return self._finder_cache

    def _get_module_info(self, fullname: str) -> _ModuleInfo | None:
        cache_entries = self._cache_entries()

        for prefix in self.prefixes:
            prefix = prefix.replace("/", ".")
            if rv := cache_entries.get(prefix + fullname):
                return rv

        return None

    # MetaPathFinder interface
    def invalidate_caches(self):
        self._finder_cache = None

    def find_spec(self, fullname, path, target=None):
        if module_info := self._get_module_info(fullname):
            spec = importlib.machinery.ModuleSpec(
                name=fullname,
                loader=self,
                is_package=module_info.is_package,
            )

            spec.has_location = True

            filename = renpy.loader.transpath(module_info.filename)

            if PREFER_LOADER:
                filename = None

            if filename is None:
                filename = "$game/" + module_info.filename

            if module_info.is_namespace:
                spec.submodule_search_locations = [filename]

            elif module_info.is_package:
                spec.submodule_search_locations = [filename.rpartition("/")[0]]

            if not module_info.is_namespace:
                if filename[-4:] == '.pyc':
                    spec.origin = filename
                    spec.cached = filename
                else:
                    spec.origin = filename
                    spec.cached = filename + "c"

            return spec

    def get_resource_reader(self, fullname: str) -> RenpyResourceReader | None:
        if module_info := self._get_module_info(fullname):
            filename = renpy.loader.transpath(module_info.filename)

            if PREFER_LOADER:
                filename = None

            if filename is None:
                filename = "$game/" + module_info.filename

            if module_info.is_namespace:
                return RenpyResourceReader(filename)
            else:
                # For non-namespace modules, we return a reader for the package directory.
                package_dir = filename.rpartition("/")[0]
                return RenpyResourceReader(package_dir)


    # InspectLoader interface
    def is_package(self, fullname: str) -> bool:
        if module_info := self._get_module_info(fullname):
            return module_info.is_package
        else:
            raise ImportError

    def get_source(self, fullname: str) -> str | None:
        module_info = self._get_module_info(fullname)
        if module_info is None:
            raise ImportError

        if module_info.is_namespace:
            return None

        if module_info.filename.endswith(".pyc"):
            # no source for .pyc-only modules
            return None
        
        with renpy.loader.load(module_info.filename, tl=False) as f:
            bindata = f.read()

        return importlib.util.decode_source(bindata)

    def get_code(self, fullname: str):
        module_info = self._get_module_info(fullname)
        if module_info is None:
            raise ImportError
        if module_info.is_namespace:
            return compile("", module_info.filename, "exec", dont_inherit=True)

        filename = module_info.filename
        if filename.endswith(".pyc"):
            # === BYTECODE ===
            with renpy.loader.load(filename, tl=False) as f:
                data = f.read()

            # Validate header (magic, hash/timestamp, etc.) exactly like CPython does
            exc_details = {"name": fullname, "path": filename}
            _classify_pyc(data, fullname, exc_details)

            # Skip the fixed 16-byte header (Python 3.7+) and compile
            return _compile_bytecode(
                memoryview(data)[16:],
                name=fullname,
                bytecode_path=filename,
            )


        # === SOURCE ===
        with renpy.loader.load(module_info.filename, tl=False) as f:
            source = f.read()

        return self.source_to_code(source, module_info.filename)

    def get_data(self, path: str):
        path = path.replace("\\", "/")

        if path.startswith("$game/"):
            path = path[6:]

            try:
                return renpy.loader.load(path, tl=False).read()
            except Exception as e:
                raise OSError(f"Could not open {path!r}.") from e

        else:
            with open(path, "rb") as f:
                return f.read()


meta_backup = []


def add_python_directory(path: str):
    """
    :doc: other

    Adds `path` to the list of paths searched for Python modules and packages.
    The path should be a string relative to the game directory. This must be
    called before an import statement.
    """

    for importer in sys.meta_path:
        if isinstance(importer, RenpyImporter):
            importer.add_prefix(path)


def init_importer():
    meta_backup[:] = sys.meta_path

    sys.meta_path.insert(0, RenpyImporter())

    add_python_directory("python-packages/")
    add_python_directory("")


def quit_importer():
    sys.meta_path[:] = meta_backup
