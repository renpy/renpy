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

import renpy
import sys
import io
import time
import pathlib
import importlib.machinery
import importlib.abc
import importlib.util
import importlib.resources.abc

from renpy.loader import RenpyPath

PREFER_LOADER: bool = False
"This can be set to True to prefer the Ren'Py loader for Python imports, for testing purposes."

if PREFER_LOADER:
    print("Using Ren'Py loader for Python imports.")

# Package Resources



class TraversableRenpyPath(importlib.resources.abc.Traversable, RenpyPath):

    def open(self, *args, **kwargs) -> "TraversableRenpyPath":
        return self.open(*args, _tl=True, **kwargs)


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

        rv = TraversableRenpyPath(path.lstrip("/"))

        return rv


# Module Loading
class RenpyImporter(importlib.abc.MetaPathFinder, importlib.abc.InspectLoader):
    """
    A meta-path importer, that tries to load pure Python modules from the places
    where Ren'Py searches for data files.
    """

    def __init__(self):
        self.prefixes: list[RenpyPath] = []
        "List of prefixes where modules can be found."

        self._finder_cache: dict[str, RenpyImporter._ModuleInfo] = {}
        """
        A dict from module name to module info of that module for all paths that
        can be loaded with this importer.
        """

    def add_prefix(self, prefix: str | RenpyPath):
        if isinstance(prefix, str):
            prefix = RenpyPath(prefix)

        if prefix in self.prefixes:
            return

        self.prefixes.append(prefix)
        self.invalidate_caches()

    class _ModuleInfo(NamedTuple):
        filename: str
        is_package: bool
        is_namespace: bool

    def _get_module_info(self, fullname: str) -> _ModuleInfo | None:

        if not self._finder_cache and not renpy.loader.game_files:
            renpy.loader.scandirfiles()

        try:
            return self._finder_cache[fullname]
        except KeyError:
            pass

        fullname_base = fullname.replace(".", "/")

        info = None
        for prefix in self.prefixes:
            dir: pathlib.Path = prefix / fullname_base

            if dir.is_dir():
                init = dir / '__init__.py'
                if init.exists():
                    info = RenpyImporter._ModuleInfo(str(init), True, False)
                else:
                    info = RenpyImporter._ModuleInfo(str(dir), True, True)
                break
            else:
                file = dir.with_name(f'{dir.name}.py')
                if file.exists() and file.is_file():
                    if not file.name.endswith('_ren.py'):
                        info = RenpyImporter._ModuleInfo(str(file), False, False)
                    break

        self._finder_cache[fullname] = info
        return info

    # MetaPathFinder interface
    def invalidate_caches(self):
        self._finder_cache.clear()

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

        with renpy.loader.load(module_info.filename, tl=False) as f:
            bindata = f.read()

        return importlib.util.decode_source(bindata)

    def get_code(self, fullname: str):
        module_info = self._get_module_info(fullname)
        if module_info is None:
            raise ImportError

        if module_info.is_namespace:
            return compile("", module_info.filename, "exec", dont_inherit=True)

        # TODO: add bytecode handling?

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


def add_python_directory(path: str | RenpyPath):
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
