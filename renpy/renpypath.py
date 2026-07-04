import renpy
import os
import functools
import contextlib
import io
import re
import unicodedata

from typing import Iterator, Literal, get_args, get_overloads, get_type_hints, overload
from bisect import bisect_left, bisect_right
from pathlib import Path, PurePosixPath
from glob import _GlobberBase


_FILE_SEPARATOR = '\x00'
_DIR_SEPARATOR = '\x01'

def normalize_renpy_path(path: str) -> str:
    """Convert unix path to alphabetically sortable path: 'a/b/c.txt' -> 'a\\x01b\\x00c.txt'"""
    parent, separator, name = path.rpartition('/')
    return parent.replace('/', _DIR_SEPARATOR) + _FILE_SEPARATOR + name

def denormalize_renpy_path(path: str) -> str:
    """Convert from alphabetically sortable path back to unix format: 'a\\x01b\\x00c.txt' -> 'a/b/c.txt'"""
    parent, separator, name = path.rpartition(_FILE_SEPARATOR)
    if not separator:
        return name.replace(_DIR_SEPARATOR, '/')
    if parent:
        return parent.replace(_DIR_SEPARATOR, '/') + '/' + name
    return name



class RenpyPathDirEntry(os.PathLike):
    """
    :doc: renpy_path class
    :name: RenpyPathDirEntry

    An entry returned by :meth:scandir and :meth:rscandir with the same purpose of
    `os.DirEntry <https://docs.python.org/3/library/os.html#os.DirEntry>`_

    You should avoid instantiating :class:`RenpyPathDirEntry` yourself.

    Do note that this class's attributes and methods have slightly different meanings than
    pathlib's DirEntry.

    Despite, ``stat()`` and ``inode()`` not being implemented,
    you can convert a DirEntry to ```RenpyPath``` with ``.renpypath()``

    .. attribute:: name
        The name of the file, the final component of the path, as a string.

    """
    __slots__ = ('name', '_raw_path', '_range_start', '_range_end', '_is_dir', '_path')

    def __init__(self, raw_path: str, range_start: int, range_end: int, is_dir: bool, child_prefix_len: int, parent_prefix_len: int) -> None:
        self._raw_path = raw_path
        self._range_start = range_start
        self._range_end = range_end
        self._is_dir = is_dir
        self.name = raw_path[parent_prefix_len:]

    @property
    def path(self) -> str:
        """
        :doc: renpy_path method

        The full path of the file, equivalent to str(path) at this Entry's location
        """
        try:
            return self._path
        except AttributeError:
            self._path = denormalize_renpy_path(self._raw_path)
            return self._path

    def renpypath(self) -> RenpyPath:
        """
        :doc: renpy_path method

        Convert this dir entry to a :class:`RenpyPath`
        """
        return RenpyPath()._create(self._raw_path, self._range_start, self._range_end, self._is_dir, len(self._raw_path))

    def is_dir(self, *, follow_symlinks: bool = True) -> bool:
        """
        :doc: renpy_path method

        Whether this entry represents a directory
        """
        return self._is_dir

    def is_file(self, *, follow_symlinks: bool = True) -> bool:
        """
        :doc: renpy_path method

        Whether this entry represents a file
        """
        return not self._is_dir

    def is_symlink(self) -> bool:
        """
        :doc: renpy_path method

        Always ``False``. Implemented for interoperability with other libraries
        """
        return False

    def is_junction(self) -> bool:
        """
        :doc: renpy_path method

        Always ``False``. Implemented for interoperability with other libraries
        """
        return False

    def __fspath__(self) -> str:
        return self.path

    def __repr__(self) -> str:
        return f"<RenpyPathDirEntry '{self.name}'>"




@functools.lru_cache(maxsize=4096, typed=True)
def _compile_pattern(*patterns, case_sensitive):
    """Compile multiple glob patterns for matching against normalized paths."""
    from glob import translate

    flags = re.DOTALL
    if not case_sensitive:
        flags |= re.IGNORECASE

    translator = functools.partial(translate, recursive=True, include_hidden=True, seps=(_DIR_SEPARATOR, _FILE_SEPARATOR))
    return re.compile(r'(?:' + r'\z)|(?:'.join(map(translator, patterns)) + r'\z)', flags=flags).match


type RenpyLoadableMode = Literal["r", "rb", "br"]

class RenpyPath(PurePosixPath):
    """
    :doc: renpy_path class
    :args: (path)
    :name: RenpyPath

    A `PathLike <https://docs.python.org/3/library/os.html#os.PathLike>`_
    for working with Ren'Py game files. It provides:

    + The complete\
    `pathlib.PurePath <https://docs.python.org/3/library/pathlib.html#pathlib.PurePath>`_ \
    (including the `/ <https://docs.python.org/3/library/pathlib.html#operators>`_ operator to join path components),

    + Some of `pathlib.Path <https://docs.python.org/3/library/pathlib.html#pathlib.Path>`_ behavior,

    + Some Ren'Py-specific or Ren'Py-specific file operations which, if already using :class:`RenpyPath` \
    can be performed more conveniently.

    Except, while builtin `Path <https://docs.python.org/3/library/pathlib.html#pathlib.Path>`_
    works on top of the file system, :class:`RenpyPath` works on top of the file list
    similar to the one returned by :func:`list_files`, but efficiently.

    The files are discovered using Ren'Py's standard search method, and may
    reside in the game directory, in an RPA archive, as an Android asset,
    in a remote server, or in any additional location a plugin may provide.

    :class:`RenpyPath` objects are not saved as part of the game state and must
    not be stored in variables that participate in rollback.

    Directories are inferred from the files Ren'Py knows about. A
    directory only exists when it has a descendant file (i.e. a file
    that would appear in :func:`list_files`). Therefore, methods like :meth:`is_dir`
    and :meth:`iterdir` will never find empty directories.

    `*path`
        Strings that, once combined, correspond to a path relative to
        one of the locations Ren'Py can find such as :var:`config.searchpath` directories or
        :var:`renpy.config.gamedir`.

        Like all paths in Ren'Py, uses forward slashes as directory separators.

    For attributes and methods not documented here, refer to
    `python's documentation of PurePosixPath <https://docs.python.org/3/library/pathlib.html#pure-paths>`_.

    """


    __slots__ = ('_range_start', '_range_end', '_is_dir', '_prefix_length', '_as_path')

    _paths: tuple[str, ...]
    _base = renpy.config.gamedir

    def _create(self, raw_path: str, range_start: int, range_end: int, is_dir: bool, child_prefix_len: int, parent_prefix_len: int | None = None) -> RenpyPath:

        if parent_prefix_len is not None:
            instance = self._from_parsed_parts('', '', self._tail_cached + [raw_path[parent_prefix_len:]])
        else:
            instance = self.with_segments(denormalize_renpy_path(raw_path))
        instance._range_start = range_start
        instance._range_end = range_end
        instance._is_dir = is_dir
        instance._prefix_length = child_prefix_len
        return instance

    @staticmethod
    def _detangle_tail(tail: list[str]) -> list[str]:
        skip_count = 0
        rv = []
        for e in tail[::-1]:
            if e == '..':
                skip_count += 1
            elif e == '.':
                continue
            elif skip_count > 0:
                skip_count -= 1
            else:
                rv.append(e)
        if skip_count > 0:
            return []

        rv.reverse()
        return rv

    def _find_ranges(self) -> None:
        tail = self._tail  # type:ignore

        if '.' in tail or '..' in tail:
            tail = self._detangle_tail(tail)

        if len(tail) < 2 and (len(tail) == 0 or tail[0] == ''):
            self._prefix_length = 0
            self._range_start = 0
            self._range_end = len(self._paths)
            self._is_dir = True
            return

        file_key = _DIR_SEPARATOR.join(tail[:-1]) + _FILE_SEPARATOR + tail[-1]

        self._prefix_length = len(file_key.lstrip(_FILE_SEPARATOR))
        self._is_dir = False

        self._range_start = bisect_left(self._paths, file_key)
        try:
            if self._paths[self._range_start] == file_key:
                self._range_end = self._range_start + 1
                return
        except IndexError:
            self._range_end = self._range_start
            return

        dir_key = _DIR_SEPARATOR.join(tail)
        self._range_start = bisect_left(self._paths, dir_key + _FILE_SEPARATOR, self._range_start)
        self._range_end = bisect_right(self._paths, dir_key + '\x02', self._range_start)
        self._is_dir = self._range_start < self._range_end


    def exists(self, *, follow_symlinks: bool = True) -> bool:
        """
        :doc: renpy_path method

        :return: ``True`` if this path corresponds to a known file or an inferred directory.
        """

        try:
            return self._range_start < self._range_end
        except AttributeError:
            self._find_ranges()
            return self._range_start < self._range_end

    def is_dir(self) -> bool:
        """
        :doc: renpy_path method

        :return: ``True`` if this path corresponds to an inferred directory.
        Ren'Py infers directories from existing files.
        A descendant file must exist for the directory to exist.
        """

        try:
            return self._is_dir
        except AttributeError:
            self._find_ranges()
            return self._is_dir

    def is_file(self) -> bool:
        """
        :doc: renpy_path method

        :return: ``True`` if this path points to a known file.
        """

        try:
            return not self._is_dir and self._range_start + 1 == self._range_end
        except AttributeError:
            self._find_ranges()
            return not self._is_dir and self._range_start + 1 == self._range_end

    def is_remote_file(self) -> bool:
        """
        :doc: renpy_path method

        :return: ``True`` if this file is a remote asset that may need to be downloaded before it can be used.
        """

        if not self.is_file():
            return False
        tail = self._tail
        if '.' in tail or '..' in tail:
            tail = self._detangle_tail(tail)
        return '/'.join(tail) in remote_files

    def samefile(self, other: 'RenpyPath | str') -> bool:
        """
        :doc: renpy_path method

        :return: ``True`` if, after resolving, self and other paths are equal. False otherwise.
        """

        try:
            # Ranges are fastest to compare but slowest to calculate
            return self is other or (
                self._range_start == other._range_start and
                self._range_end == other._range_end and
                self._prefix_length == other._prefix_length
            )
        except AttributeError:
            try:
                if self._raw_paths == other._raw_paths:
                    return True
                return self.resolve()._tail == other.resolve()._tail
            except AttributeError:
                if not isinstance(other, str):
                    return False

        return (type(self)(other)).samefile(self)


    def _iter_children(self, create):
        if not self.exists():
            raise FileNotFoundError(f"No such file or directory: '{self}'")
        if not self.is_dir():
            raise NotADirectoryError(f"Not a directory: '{self}'")

        prefix_length = self._prefix_length
        _paths = self._paths

        # Files
        file_i = self._range_start
        for file_i, fn in enumerate(_paths[self._range_start:self._range_end], start=self._range_start):
            if fn[prefix_length] != _FILE_SEPARATOR:
                break
            yield create(fn, file_i, file_i + 1, False, prefix_length, prefix_length + 1)
        else:
            return

        if prefix_length:
            prefix_length += 1

        # Directories
        while file_i < self._range_end:
            fn = _paths[file_i]
            slash_pos = fn.find(_DIR_SEPARATOR, prefix_length)
            if slash_pos == -1:
                slash_pos = fn.find(_FILE_SEPARATOR, prefix_length)
                if slash_pos == -1:
                    break
            child_path = fn[:slash_pos]
            child_range_end = bisect_left(_paths, child_path + '\x02', file_i, self._range_end)
            yield create(child_path, file_i, child_range_end, True, len(child_path), prefix_length)
            file_i = child_range_end

    def iterdir(self) -> Iterator[RenpyPath]:
        """
        :doc: renpy_path method

        Yields :class:`RenpyPath` objects for each entry in the directory this path
        points to. Analogous to
        `Path.iterdir <https://docs.python.org/3/library/pathlib.html#pathlib.Path.iterdir>`_
        """

        yield from self._iter_children(self._create)

    @contextlib.contextmanager
    def scandir(self) -> Iterator[Iterator[RenpyPathDirEntry]]:
        """
        :doc: renpy_path method

        :return: a list of :class:`RenpyPathDirEntry` objects for each entry in the\
        directory this path points to.

        Each :class:`RenpyPathDirEntry` has ``name``, ``path``, ``is_dir()``, and ``is_file()``, similar to
        `os.scandir <https://docs.python.org/3/library/os.html#os.scandir>`_.
        """

        yield self._iter_children(RenpyPathDirEntry)

    @contextlib.contextmanager
    def rscandir(self) -> Iterator[Iterator[RenpyPathDirEntry]]:
        """
        :doc: renpy_path method

        Behaves like a recursive scandir.

        Same as :meth:`scandir` with the following differences:

        #. Only yields files.
        #. Files yield can be at any descendant depth.
        #. If this Path is a file, the result is a single dir entry of that same file.
        #. If this path doesn't exist, the output is empty.

        """

        def flat_walker():

            try:
                start, end = self._range_start, self._range_end
            except AttributeError:
                self._find_ranges()
                start, end = self._range_start, self._range_end

            for pathnum, fn in enumerate(self._paths[start:end], start=start):
                file_sep_pos = fn.rfind(_FILE_SEPARATOR)
                yield RenpyPathDirEntry(fn, pathnum, pathnum + 1, False, len(fn), file_sep_pos)

        yield flat_walker()


    def walk(self, top_down: bool = True, on_error=None, follow_symlinks: bool = False):
        """
        :doc: renpy_path method

        Walks the directory tree rooted at this path, yielding
        ``(dirpath, dirnames, filenames)`` tuples, similar to
        `Path.walk <https://docs.python.org/3/library/pathlib.html#pathlib.Path.walk>`_.
        """

        if not self.is_dir():
            return

        dir_paths: list[RenpyPath] = []
        dir_names: list[str] = []
        file_names: list[str] = []

        for child in self.iterdir():
            if child.is_dir():
                dir_paths.append(child)
                dir_names.append(child.name)
            else:
                file_names.append(child.name)

        if top_down:
            yield self, dir_names, file_names
        for d in dir_paths:
            if top_down or d.name in dir_names:
                yield from d.walk(top_down=top_down, on_error=on_error)
        if not top_down:
            yield self, dir_names, file_names

    def _rglob_pattern(self, matcher):
        """Fast path for rglob with filename-only patterns: walk children, filter by name."""
        for child in self._iter_children(self._create):
            if matcher(child.name):
                yield child
            if child._is_dir:
                yield from child._rglob_pattern(matcher)

    def glob(self, pattern: str, *, case_sensitive: bool | None = None) -> Iterator[RenpyPath]:
        """
        :doc: renpy_path method

        Yields :class:`RenpyPath` objects matching the given glob `pattern` relative
        to this directory. Works the same way as
        `Path.glob <https://docs.python.org/3/library/pathlib.html#pathlib.Path.glob>`_.
        """

        if not self.exists():
            raise FileNotFoundError(f"[Errno 2] No such file or directory: '{self}'")
        if pattern == '*':
            yield from self.iterdir()
        elif '*' not in pattern and '?' not in pattern and '[' not in pattern:
            child = self / pattern
            if child.exists():
                yield child
        elif '**' not in pattern and '/' not in pattern:
            matcher = _compile_pattern(pattern, case_sensitive=case_sensitive)
            with self.scandir() as entries:
                for entry in entries:
                    if matcher(entry.name):
                        yield entry.renpypath()
        else:
            globber = _RenpyPathGlobber(sep='/', case_sensitive=case_sensitive or False, case_pedantic=False, recursive=True)
            pattern_list = pattern.split('/')
            pattern_list.reverse()
            selector_fn = globber.selector(pattern_list)
            for path_str in selector_fn(str(self) + '/', True):
                yield RenpyPath(path_str.rstrip('/'))

    def rglob(self, pattern: str, *, case_sensitive: bool | None = None) -> Iterator[RenpyPath]:
        """
        :doc: renpy_path method

        Like :meth:`glob`, but prefixes ``**/`` to the pattern, matching
        recursively in all subdirectories. Works the same way as
        `Path.rglob <https://docs.python.org/3/library/pathlib.html#pathlib.Path.rglob>`_.
        """

        if not self.exists():
            raise FileNotFoundError(f"[Errno 2] No such file or directory: '{self}'")

        if '/' not in pattern and '**' not in pattern:
            yield from self._rglob_pattern(_compile_pattern(pattern, case_sensitive=case_sensitive))
            return

        globber = _RenpyPathGlobber(sep='/', case_sensitive=case_sensitive or False, case_pedantic=False, recursive=True)
        pattern_list = ["**"]
        pattern_list.extend(pattern.split('/'))
        pattern_list.reverse()
        selector_fn = globber.selector(pattern_list)
        for path_str in selector_fn(str(self) + '/', True):
            yield RenpyPath(path_str.rstrip('/'))


    @overload
    def files_matching(self, *patterns: str, case_sensitive: bool | None = None, filepaths: Literal[True] = True) -> Iterator[str]: ...

    @overload
    def files_matching(self, *patterns: str, case_sensitive: bool | None = None, filepaths: Literal[False] = ...) -> Iterator[RenpyPath]: ...

    def files_matching(self, *patterns, case_sensitive=None, filepaths=True):
        """
        :doc: renpy_path method

        Takes glob patterns and yields all files that match any of the patterns.

        Same as :meth:`rglob` with the following differences:

        #. Can only glob files. (therefore, only yields files)
        #. Better performance than glob when directory depth is irrelevant.
        #. Returns full paths either as strings (filepaths=True) or :class:`RenpyPath` (filepaths=False).
        #. Can not supply a pattern at all, in which case, yields all directory and descendent files.

        `patterns`
            Glob patterns to match against, relative to this directory.
            Patterns may contain `..` but only descendent files of this directory will ever be yield.

        `case_sensitive`
            Whether search is case-sentitive. Defaults to ``False``.

        `filepaths`
            If ``True`` (the default), yields file paths as :class:`str`.
            If ``False``, yields :class:`RenpyPath` objects with pre-computed ranges
            (no additional binary search needed for :meth:`exists`, :meth:`is_file`, etc.).

        """
        try:
            start, end = self._range_start, self._range_end
        except AttributeError:
            self._find_ranges()
            start, end = self._range_start, self._range_end

        if not patterns:
            if filepaths:
                yield from map(denormalize_renpy_path, self._paths[self._range_start:self._range_end])
            else:
                rp = RenpyPath()
                for num, p in enumerate(self._paths[self._range_start:self._range_end], start=self._range_start):
                    yield rp._create(p, num, num + 1, False, len(p))
            return

        matcher = _compile_pattern(
            *[normalize_renpy_path(p) for p in patterns],
            case_sensitive=case_sensitive,
        )

        _prefix_length = self._prefix_length
        if filepaths:
            for fn in self._paths[start:end]:
                if matcher(fn[_prefix_length:]):
                    yield denormalize_renpy_path(fn)
        else:
            rp = RenpyPath()
            for num, fn in enumerate(self._paths[start:end], start=start):
                if matcher(fn[_prefix_length:]):
                    yield rp._create(fn, num, num + 1, False, len(fn))


    def is_absolute(self) -> bool:
        """
        :doc: renpy_path method

        Returns False.
        :class:`RenpyPath` paths are always relative to a base directory, so this always returns False.
        This method exists for completeness' sake.
        """

        return False

    def as_path(self) -> Path:
        """
        :doc: renpy_path method

        Returns a `builtin Path <https://docs.python.org/3/library/pathlib.html#pathlib.Path>`_
        pointing to this path on local filesystem.

        This path's location can be relative to any directory in the searchpath. This process is similar to how
        :func:`exists` searches, except it also supports directories.

        If the path this :class:`RenpyPath` represents doesn't exist in the filesystem, it assumes it to be present
        relative to :var:`config.gamedir` directory.

        You can manually confirm if the path was found by calling
        `.exists() <https://docs.python.org/3/library/pathlib.html#pathlib.Path.exists>`_ on the resulting
        `Path <https://docs.python.org/3/library/pathlib.html#pathlib.Path>`_
        """

        from loader import lower_map

        try:
            return self._as_path
        except AttributeError:
            pass

        # Similar to transpath() but not using transpath because requires support to directories
        path = str(self)
        path = Path(lower_map.get(unicodedata.normalize("NFC", path.lower()), path))
        base_path = Path(renpy.config.basedir)

        for d in renpy.config.searchpath:
            file_path = base_path / d / path

            if file_path.exists():
                self._as_path = file_path
                return self._as_path

        self._as_path = Path(self._base) / self
        return self._as_path


    @overload
    def open(self, mode: Literal["r"] = "r", *args, encoding=None, **kwargs) -> io.TextIOWrapper: ...

    @overload
    def open(self, mode: Literal["rb", "br"] = ..., *args, encoding=None, **kwargs) -> io.BufferedReader: ...

    def open(self, mode="r", *args, _tl=False, encoding=None, **kwargs):
        """
        :doc: renpy_path method

        Opens this file for reading.
        Similar to :func:`renpy.open_file` but with fundamental differences:

        - ``encoding`` does not dictate whether file is open in binary mode.
        - You cannot provide a directory to search relative to.

        `mode`
            Either ``"r"`` for text mode or ``"rb"`` for binary mode.

        `encoding`
            | Only has an effect when :attr:`mode` is ``r``.
            | Specifies the encoding to use when opening the file.
            | If ``None``, the default, the encoding is taken from :var:`config.open_file_encoding`.
            | In most cases, ``None`` means decode in UTF-8.

        Other arguments are passed-through to
        `io.TextIOWrapper <https://docs.python.org/3/library/io.html#io.TextIOWrapper>`_.

        :return: Either :class:`io.BufferedReader` in binary mode, or :class:`io.TextIOWrapper` in text mode.
        """

        if mode not in ("r", "rb", "br"):
            raise ValueError(f"Unsupported mode {mode!r}. Only {('r', 'rb', 'br')} are supported.")

        if not self.is_file():
            raise IsADirectoryError(f"Only files may be opened. This path does not point to a file: {str(self)}")

        f = renpy.loader.load(str(self), tl=_tl)

        if 'b' in mode:
            return f
        else:
            if encoding is None:
                encoding = renpy.config.open_file_encoding
            return io.TextIOWrapper(f, *args, encoding=encoding or None, **kwargs)


    def read_text(self, encoding=None) -> str:
        """
        :doc: renpy_path method

        Reads and returns the entire file contents as str.

        `encoding`
            Same as :meth:`open`
        """

        with self.open("r", encoding=encoding) as f:
            assert isinstance(f, io.TextIOWrapper)
            return f.read()

    def read_bytes(self) -> bytes:
        """
        :doc: renpy_path method

        Reads and returns the entire file contents as bytes.
        """

        with self.open("rb") as f:
            assert isinstance(f, io.BufferedReader)
            return f.read()

    def resolve(self, strict=False) -> RenpyPath:
        """
        :doc: renpy_path method

        Returns a new :class:`RenpyPath` with ``..`` and ``.`` segments resolved.

        `strict`
            If ``True``, Raises ``FileNotFoundError`` if file doesn't exist.
        """

        tail = self._tail
        if '.' not in tail and '..' not in tail:
            return self

        tail = self._detangle_tail(tail)
        resolved_path: RenpyPath = self._from_parsed_parts('', '', tail)
        if not strict or os.path.ALLOW_MISSING:
            return resolved_path

        if not resolved_path.exists():
            raise FileNotFoundError(f"[Errno 2] No such file or directory: '{resolved_path}'")

        return resolved_path

    @classmethod
    def current_path_line(cls) -> tuple[RenpyPath, int]:
        """
        :doc: renpy_path method
        :name: RenpyPath.current_path_line

        Returns a ``(path, line)`` tuple giving the :class:`RenpyPath` and line
        number of the Ren'Py script statement that is currently executing.

        Analogous to :func:`renpy.get_filename_line` except instead
        of filename, it is a :class:`RenpyPath`.
        """

        from renpy.exports.debugexports import get_filename_line
        fn, line = get_filename_line()
        path = cls._from_parsed_parts('', '', os.path.split(fn))
        return path, line


# _PathGlobber is buggy, not properly implemented in 3.14, so need to use the much slower _StringGlobber approach.
class _RenpyPathGlobber(_GlobberBase):

    @staticmethod
    def concat_path(path, text):
        return path + text

    @staticmethod
    def lexists(path):
        return RenpyPath(path.rstrip('/')).exists()

    @staticmethod
    def scandir(path):
        path = path.rstrip('/')
        rp = RenpyPath(path)
        with rp.scandir() as entries:
            path += '/'
            return ((e, e.name, path + e.name) for e in entries)


class RenpyCommonPath(RenpyPath):
    _base = renpy.config.commondir

class RenpyAllPath(RenpyPath):
    _base = renpy.config.basedir


def rpy_path(path: RenpyPath) -> RenpyPath:
    """
    :doc: renpy_path func

    :return: A :class:`RenpyPath` pointing to the ``.rpy``, ``.rpym``, or ``_ren.py`` source\
    file corresponding to this ``.rpyc`` or ``.rpymc`` path.
    """

    if path.is_dir():
        raise IsADirectoryError(f"Directories are not renpy files and can't be rpyc. '{str(path)}' is a directory")

    if path.suffix in ('.rpy', '.rpym') or path.name.endswith('_ren.py'):
        return path

    if path.suffix not in (".rpyc", ".rpymc"):
        raise Exception(f"Only rpyc/rpymc files can have rpy/rpym/_ren.py counter-parts. '{str(path)}' is none of those")

    as_ren_py = path.with_name(path.stem + '_ren.py')

    if as_ren_py.exists():
        return as_ren_py

    without_c = path.with_suffix(path.suffix[:-1])
    return without_c


def rpyc_path(path: RenpyPath) -> RenpyPath:
    """
    :doc: renpy_path func

    :return: A :class:`RenpyPath` pointing to the ``.rpyc`` compiled file\
    corresponding to this ``.rpy``, ``.rpym``, or ``_ren.py`` path.
    """

    if path.is_dir():
        raise IsADirectoryError(f"Directories are not renpy files and can't be rpy. '{str(path)}' is a directory")

    if path.suffix in ('.rpyc', '.rpymc'):
        return path

    name = path.name
    if path.suffix not in (".rpy", ".rpym") and not name.endswith('_ren.py'):
        raise Exception(f"Only rpy/rpym/_ren.py files can have rpyc counter-parts. '{str(path)}' is none of those")

    if name.endswith('_ren.py'):
        name = name[:-7] + '.rpy'

    return path.with_name(name + "c")
