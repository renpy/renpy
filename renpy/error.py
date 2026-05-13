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

# This file contains code for formatting tracebacks.

from typing import TYPE_CHECKING, NotRequired, TextIO, Iterator, Callable, Any, Protocol, TypedDict, Unpack

# Those types can't be pickled!
if TYPE_CHECKING:
    from types import TracebackType, FrameType

import io
import os
import abc
import sys
import itertools
import textwrap
import dataclasses
import platform
import linecache
import time
import contextlib
import collections.abc

import renpy


class HasReportTraceback(Protocol):
    def report_traceback(self, name: str, last: bool, frame: "FrameType") -> list["FrameSummary"] | None:
        """
        Convert a frame corresponding to a call of a method `name` of this object to a
        list of FrameSummary objects.

        `last` is True if this is the last frame in the traceback.

        This method can return an empty list to hide this frame from the traceback
        or None to fall back to default conversion.

        The frame is guaranteed to have `self == frame.f_locals['self']`.

        For legacy purposes, this method can have only first 2 arguments, in
        which case it is assumed to return (filename, linenumber, name, line) tuples.
        """


class ExceptionPrintContextKwargs(TypedDict):
    filter_private: NotRequired[bool]
    max_group_width: NotRequired[int]
    max_group_depth: NotRequired[int]
    emit_context: NotRequired[bool]


class ExceptionPrintContext(abc.ABC):
    def __init__(self, **kwargs: Unpack[ExceptionPrintContextKwargs]):
        self.indent_depth = 0
        self.exception_group_depth = 0
        self.need_close = False

        self.filter_private = kwargs.get("filter_private", False)
        self.max_group_width = kwargs.get("max_group_width", 15)
        self.max_group_depth = kwargs.get("max_group_depth", 10)
        self.emit_context = kwargs.get("emit_context", True)

    def should_filter(self, filename: str) -> bool:
        """
        Returns true if the FrameSummary with the given filename should be
        skipped when printing the stack.

        By default filters Ren'Py common code, Ren'Py libraries, and all pure
        Python code.
        """

        if not self.filter_private:
            return False

        if filename and filename[0] == "<" and filename[-1] == ">":
            return True

        if filename.endswith((".rpy", ".rpym", "_ren.py")):
            # TODO: Make it more robust by is_relative_to check.
            return filename.startswith(("renpy/common/", "game/libs/"))
        elif filename.endswith(".py"):
            return True
        else:
            return False

    @contextlib.contextmanager
    def indent(self):
        self.indent_depth += 1
        try:
            yield
        finally:
            self.indent_depth -= 1

    @abc.abstractmethod
    def getvalue(self) -> Any:
        """
        Returns the object that becomes the result of formatting methods.
        """

    @abc.abstractmethod
    def location(self, filename: str, lineno: int, name: str | None):
        """
        Emits a line that shows the location of the frame in the source code.

        `filename`
            The filename of the source code.

        `lineno`
            The line number of the source code.

        `name`
            The name of the code that was running when the exception occurred
            or None if the name is not available.

        Subclasses should override this method to emit the location information
        in a way that makes sense for their particular application.
        """

    @abc.abstractmethod
    def source_carets(self, line: str, carets: str | None):
        """
        Emits a line(s) that shows the source code that was running in the
        frame when the exception occurred.

        `line`
            The source code that was running when the exception occurred.

        `carets`
            The carets that point to the location of the exception in the
            source code. If carets for that line are not available, this
            is None. Otherwise this is a string that contains spaces, ~, and ^
            characters.
        """

    @abc.abstractmethod
    def final_exception_line(self, exc_type: str, text: str | None):
        """
        Emits the final exception line from the string of the exception
        type and the optional exception text.
        """

    @abc.abstractmethod
    def string(self, text: str):
        """
        Emits a string.
        """

    @abc.abstractmethod
    def chain_cause(self):
        """
        Emits the message that above exception was the cause of the following exception.
        """

    @abc.abstractmethod
    def chain_context(self):
        """
        Emits the message that above exception is the context of the following exception.
        """

    @abc.abstractmethod
    def exceptions_separator(self, index: int, total: int):
        """
        Emits the separator between exceptions in the group.

        `index`
            The index of exception that is being printed.

        `total`
            The total number of exceptions in the group.
        """

    @abc.abstractmethod
    def exceptions_close(self):
        """
        Emits the closing separator for the exception group.
        """


CAUSE_MESSAGE = "The above exception was the direct cause of the following exception:"
CONTEXT_MESSAGE = "During handling of the above exception, another exception occurred:"


class TextIOExceptionPrintContext(ExceptionPrintContext):
    def __init__(self, file: TextIO, **kwargs: Unpack[ExceptionPrintContextKwargs]):
        super().__init__(**kwargs)

        self.file = file

    def getvalue(self):
        try:
            return self.file.getvalue()  # type: ignore
        except AttributeError:
            return None

    def _print(self, text: str = ""):
        if text:
            text = f"{'  ' * self.indent_depth}{text}"

        print(text, file=self.file)

    def string(self, text: str):
        self._print(text)

    def chain_cause(self):
        self._print()
        self._print(CAUSE_MESSAGE)
        self._print()

    def chain_context(self):
        self._print()
        self._print(CONTEXT_MESSAGE)
        self._print()

    def exceptions_separator(self, index: int, total: int):
        truncated = index >= self.max_group_width
        title = f"{index + 1}" if not truncated else "..."
        self._print(("+-" if index == 0 else "  ") + f"+---------------- {title} ----------------")

    def exceptions_close(self):
        self._print("+------------------------------------")


class ANSIColors:
    RESET = "\x1b[0m"

    BLACK = "\x1b[30m"
    BLUE = "\x1b[34m"
    CYAN = "\x1b[36m"
    GREEN = "\x1b[32m"
    MAGENTA = "\x1b[35m"
    RED = "\x1b[31m"
    WHITE = "\x1b[37m"  # more like LIGHT GRAY
    YELLOW = "\x1b[33m"

    BOLD_BLACK = "\x1b[1;30m"  # DARK GRAY
    BOLD_BLUE = "\x1b[1;34m"
    BOLD_CYAN = "\x1b[1;36m"
    BOLD_GREEN = "\x1b[1;32m"
    BOLD_MAGENTA = "\x1b[1;35m"
    BOLD_RED = "\x1b[1;31m"
    BOLD_WHITE = "\x1b[1;37m"  # actual WHITE
    BOLD_YELLOW = "\x1b[1;33m"

    # intense = like bold but without being bold
    INTENSE_BLACK = "\x1b[90m"
    INTENSE_BLUE = "\x1b[94m"
    INTENSE_CYAN = "\x1b[96m"
    INTENSE_GREEN = "\x1b[92m"
    INTENSE_MAGENTA = "\x1b[95m"
    INTENSE_RED = "\x1b[91m"
    INTENSE_WHITE = "\x1b[97m"
    INTENSE_YELLOW = "\x1b[93m"

    BACKGROUND_BLACK = "\x1b[40m"
    BACKGROUND_BLUE = "\x1b[44m"
    BACKGROUND_CYAN = "\x1b[46m"
    BACKGROUND_GREEN = "\x1b[42m"
    BACKGROUND_MAGENTA = "\x1b[45m"
    BACKGROUND_RED = "\x1b[41m"
    BACKGROUND_WHITE = "\x1b[47m"
    BACKGROUND_YELLOW = "\x1b[43m"

    INTENSE_BACKGROUND_BLACK = "\x1b[100m"
    INTENSE_BACKGROUND_BLUE = "\x1b[104m"
    INTENSE_BACKGROUND_CYAN = "\x1b[106m"
    INTENSE_BACKGROUND_GREEN = "\x1b[102m"
    INTENSE_BACKGROUND_MAGENTA = "\x1b[105m"
    INTENSE_BACKGROUND_RED = "\x1b[101m"
    INTENSE_BACKGROUND_WHITE = "\x1b[107m"
    INTENSE_BACKGROUND_YELLOW = "\x1b[103m"


class ANSIColoredPrintContext(TextIOExceptionPrintContext):
    LOCATION_COLOR = ANSIColors.INTENSE_BLUE
    PRIMARY_CARET_COLOR = ANSIColors.RED
    SECONDARY_CARET_COLOR = ANSIColors.INTENSE_RED
    EXCEPTION_TYPE_COLOR = ANSIColors.INTENSE_WHITE
    EXCEPTION_VALUE_COLOR = ANSIColors.RESET

    def location(self, filename, lineno, name):
        if name is None:
            name_str = ""
        else:
            name_str = f", in {name}"

        self._print(f'{self.LOCATION_COLOR}File "{filename}", line {lineno}{ANSIColors.RESET}{name_str}')

    def source_carets(self, line, carets):
        if carets is None:
            self._print(line)
            return

        zipped = zip(line, carets, strict=True)
        colorized_line_parts: list[str] = []
        for color, group in itertools.groupby(zipped, key=lambda x: x[1]):
            caret_group = list(group)
            line_part = "".join(char for char, _ in caret_group)
            if color == "^":
                line_part = f"{self.PRIMARY_CARET_COLOR}{line_part}{ANSIColors.RESET}"
            elif color == "~":
                line_part = f"{self.SECONDARY_CARET_COLOR}{line_part}{ANSIColors.RESET}"

            colorized_line_parts.append(line_part)

        self._print("".join(colorized_line_parts))

    def final_exception_line(self, exc_type: str, text: str | None):
        exc_type = f"{self.EXCEPTION_TYPE_COLOR}{exc_type}{ANSIColors.RESET}"
        if text is None:
            self._print(exc_type)
        else:
            text = f"{self.EXCEPTION_VALUE_COLOR}{text}{ANSIColors.RESET}"
            self._print(f"{exc_type}: {text}")


class NonColoredExceptionPrintContext(TextIOExceptionPrintContext):
    @staticmethod
    def _display_width(line: str) -> Iterator[int]:
        """
        Calculate the extra amount of width space the given source
        code segment might take if it were to be displayed on a fixed
        width output device. Supports wide unicode characters and emojis.
        """

        # Fast track for ASCII-only strings
        if line.isascii():
            return itertools.repeat(1, len(line))

        from unicodedata import east_asian_width

        return (2 if east_asian_width(char) in "WF" else 1 for char in line)

    def location(self, filename, lineno, name):
        if name is None:
            name_str = ""
        else:
            name_str = f", in {name}"

        self._print(f'File "{filename}", line {lineno}{name_str}')

    def source_carets(self, line, carets):
        self._print(line)
        if carets is not None:
            chars = list[str]()
            for width, char in zip(self._display_width(line), carets):
                chars.append(char * width)
            self._print("".join(chars))

    def final_exception_line(self, exc_type, text):
        if text is None:
            self._print(exc_type)
        else:
            self._print(f"{exc_type}: {text}")


def MaybeColoredExceptionPrintContext(
    file: TextIO | None = None, **kwargs: Unpack[ExceptionPrintContextKwargs]
) -> ExceptionPrintContext:
    """
    Returns exception print context that writes to a file or other text IO.
    If file is a tty, or other ANSI-capable terminal, it will use colored
    output. Otherwise, it will use carets and other non-colored output.
    """

    if file is None:
        file = sys.stdout
        if file is None:
            file = io.StringIO()

    if os.environ.get("NO_COLOR"):
        return NonColoredExceptionPrintContext(file, **kwargs)
    if os.environ.get("FORCE_COLOR"):
        return ANSIColoredPrintContext(file, **kwargs)
    if os.environ.get("TERM") == "dumb":
        return NonColoredExceptionPrintContext(file, **kwargs)

    try:
        fileno = file.fileno()
    except Exception:
        return NonColoredExceptionPrintContext(file, **kwargs)

    # TODO: nt._supports_virtual_terminal was added only in Python 3.13 to check for that.
    if sys.platform == "win32":
        import ctypes
        import ctypes.wintypes

        FILE_TYPE_CHAR = 0x0002
        FILE_TYPE_REMOTE = 0x8000
        ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004

        kernel32 = ctypes.windll.kernel32

        if fileno == 1:
            h = kernel32.GetStdHandle(-11)
        elif fileno == 2:
            h = kernel32.GetStdHandle(-12)
        else:
            return NonColoredExceptionPrintContext(file, **kwargs)

        if h is None or h == ctypes.wintypes.HANDLE(-1):
            return NonColoredExceptionPrintContext(file, **kwargs)

        if (kernel32.GetFileType(h) & ~FILE_TYPE_REMOTE) != FILE_TYPE_CHAR:
            return NonColoredExceptionPrintContext(file, **kwargs)

        mode = ctypes.wintypes.DWORD()
        if not kernel32.GetConsoleMode(h, ctypes.byref(mode)):
            return NonColoredExceptionPrintContext(file, **kwargs)

        if mode.value & ENABLE_VIRTUAL_TERMINAL_PROCESSING == 0:
            return NonColoredExceptionPrintContext(file, **kwargs)
        else:
            return ANSIColoredPrintContext(file, **kwargs)

    # POSIX system - just check isatty.
    else:
        try:
            try:
                isatty = file.isatty()
            except Exception:
                isatty = os.isatty(fileno)
        except Exception:
            isatty = False

        if isatty:
            return ANSIColoredPrintContext(file, **kwargs)
        else:
            return NonColoredExceptionPrintContext(file, **kwargs)


# Reimplement parts of Python 3.14 traceback module, so we can add Ren'Py-specific behavior.
def normalize_renpy_line_offset(filename: str, linenumber: int, offset: int, line: str):
    """
    Given byte offset in `line`, convert it into character offset and
    discard extra offset from munged names.
    """

    # Correct extra offset from _ren.py transformation.
    if filename.endswith("_ren.py"):
        from renpy.lexer import ren_py_to_rpy_offsets, unelide_filename

        try:
            with open(unelide_filename(filename), "r", encoding="utf-8") as f:
                lines = f.readlines()  # TODO: optimize this block?
        except Exception:
            lines = []

        offsets = ren_py_to_rpy_offsets(lines, filename)
        for i, base_offset in enumerate(offsets, start=1):
            if base_offset is not None:
                if i == linenumber:
                    offset -= base_offset
                    break

    if not line.isascii():
        as_utf8 = line.encode("utf-8")
        offset = len(as_utf8[:offset].decode("utf-8", errors="replace"))

    from renpy.lexer import munge_filename, get_string_munger

    munge_prefix = munge_filename(filename)

    if munge_prefix in line:
        munged_line = get_string_munger(munge_prefix)(line)
        len_prefix = len(munge_prefix) - 2

        idx = 0
        while True:
            idx = munged_line.find(munge_prefix, idx, offset + len_prefix)

            if idx == -1:
                break

            offset -= len_prefix
            idx += len_prefix

    return offset


def _calculate_anchors(frame_summary: "FrameSummary"):
    """
    For given frame summary, return None if there is no column information or
    other error happens, or list of 4 (lineno, colno) tuples that represent:
        - position where secondary character starts
        - position where primary character starts
        - position where secondary character starts again
        - position where secondary character ends

    The invariant is that for split lines of frame code, carets can be rendered as
    nothing until first tuple, secondary char until second tuple, primary char
    until third tuple, secondary char until fourth tuple, and nothing after fourth
    tuple.
    """

    if frame_summary.colno is None or frame_summary.end_colno is None:
        return None

    all_lines = list(frame_summary.lines)
    end_lineno = frame_summary.end_lineno - frame_summary.lineno
    first_line = all_lines[0]
    # assume all_lines has enough lines (since we constructed it)
    last_line = all_lines[end_lineno]

    # character index of the start/end of the instruction
    start_offset = normalize_renpy_line_offset(
        frame_summary.filename, frame_summary.lineno, frame_summary.colno, first_line
    )

    end_offset = normalize_renpy_line_offset(
        frame_summary.filename, frame_summary.end_lineno, frame_summary.end_colno, last_line
    )

    default_anchors = [(0, start_offset), (0, start_offset), (end_lineno, end_offset), (end_lineno, end_offset)]

    # get exact code segment corresponding to the instruction
    segment = "\n".join(all_lines)
    segment = segment[start_offset : len(segment) - (len(last_line) - end_offset)]

    from ast import parse, expr, BinOp, Expr, Subscript, Call

    # Without parentheses, `segment` is parsed as a statement.
    # Binary ops, subscripts, and calls are expressions, so
    # we can wrap them with parentheses to parse them as
    # (possibly multi-line) expressions.
    # e.g. if we try to highlight the addition in
    # x = (
    #     a +
    #     b
    # )
    # then we would ast.parse
    #     a +
    #     b
    # which is not a valid statement because of the newline.
    # Adding brackets makes it a valid expression.
    # (
    #     a +
    #     b
    # )
    # Line locations will be different than the original,
    # which is taken into account later on.
    tree = parse(f"(\n{segment}\n)")

    if len(tree.body) != 1:
        return default_anchors

    lines = segment.splitlines()

    def normalize(lineno: int, offset: int):
        """Get character index given byte offset"""
        as_utf8 = lines[lineno].encode("utf-8")
        return len(as_utf8[:offset].decode("utf-8", errors="replace"))

    def next_valid_char(lineno: int, col: int):
        """Gets the next valid character index in `lines`, if
        the current location is not valid. Handles empty lines.
        """
        while lineno < len(lines) and col >= len(lines[lineno]):
            col = 0
            lineno += 1
        assert lineno < len(lines) and col < len(lines[lineno])
        return lineno, col

    def increment(lineno: int, col: int):
        """Get the next valid character index in `lines`."""
        col += 1
        lineno, col = next_valid_char(lineno, col)
        return lineno, col

    def next_line(lineno: int, col: int):
        """Get the next valid character at least on the next line"""
        col = 0
        lineno += 1
        lineno, col = next_valid_char(lineno, col)
        return lineno, col

    def increment_until(lineno: int, col: int, stop: Callable[[str], bool]):
        """Get the next valid non-"\\#" character that satisfies the `stop` predicate"""
        while True:
            ch = lines[lineno][col]
            if ch in "\\#":
                lineno, col = next_line(lineno, col)
            elif not stop(ch):
                lineno, col = increment(lineno, col)
            else:
                break
        return lineno, col

    def setup_positions(expr: expr, force_valid=True):
        """Get the lineno/col position of the end of `expr`. If `force_valid` is True,
        forces the position to be a valid character (e.g. if the position is beyond the
        end of the line, move to the next line)
        """
        # -2 since end_lineno is 1-indexed and because we added an extra
        # bracket + newline to `segment` when calling ast.parse
        if expr.end_lineno is None or expr.end_col_offset is None:
            raise Exception("Precise positions are not available.")

        lineno = expr.end_lineno - 2
        col = normalize(lineno, expr.end_col_offset)
        return next_valid_char(lineno, col) if force_valid else (lineno, col)

    match tree.body[0]:
        case Expr(value=expression):
            pass
        case _:
            return default_anchors

    match expression:
        case BinOp(left=left, right=right):
            # ast gives these locations for BinOp subexpressions
            # ( left_expr ) + ( right_expr )
            #   left^^^^^       right^^^^^
            left_lineno, left_col = setup_positions(left)

            # First operator character is the first non-space/')' character
            left_lineno, left_col = increment_until(left_lineno, left_col, lambda x: not x.isspace() and x != ")")

            # binary op is 1 or 2 characters long, on the same line,
            # before the right subexpression
            right_lineno = left_lineno
            right_col = left_col + 1
            if (
                right_col < len(lines[right_lineno])
                and (
                    # operator char should not be in the right subexpression
                    right.lineno - 2 > right_lineno or right_col < normalize(right.lineno - 2, right.col_offset)
                )
                and not (ch := lines[right_lineno][right_col]).isspace()
                and ch not in "\\#"
            ):
                right_col += 1

            if left_lineno == 0:
                left_col += start_offset
            if right_lineno == 0:
                right_col += start_offset

            return [
                (0, start_offset),  # start of left_expr
                (left_lineno, left_col),  # end of left_expr
                (right_lineno, right_col),  # start of right_expr
                (end_lineno, end_offset),  # end of right_expr
            ]

        case Subscript(value=value):
            # ast gives these locations for value and slice subexpressions
            # ( value_expr ) [ slice_expr ]
            #   value^^^^^     slice^^^^^
            # subscript^^^^^^^^^^^^^^^^^^^^

            # find left bracket
            left_lineno, left_col = setup_positions(value)
            left_lineno, left_col = increment_until(left_lineno, left_col, lambda x: x == "[")
            # find right bracket (final character of expression)
            right_lineno, right_col = setup_positions(expression, force_valid=False)

            if left_lineno == 0:
                left_col += start_offset
            if right_lineno == 0:
                right_col += start_offset

            return [
                (0, start_offset),
                (left_lineno, left_col),
                (right_lineno, right_col),
                (end_lineno, end_offset),
            ]

        case Call(func=func):
            # ast gives these locations for function call expressions
            # ( func_expr ) (args, kwargs)
            #   func^^^^^
            # call^^^^^^^^^^^^^^^^^^^^^^^^

            # find left bracket
            left_lineno, left_col = setup_positions(func)
            left_lineno, left_col = increment_until(left_lineno, left_col, lambda x: x == "(")
            # find right bracket (final character of expression)
            right_lineno, right_col = setup_positions(expression, force_valid=False)

            if left_lineno == 0:
                left_col += start_offset
            if right_lineno == 0:
                right_col += start_offset

            return [
                (0, start_offset),
                (left_lineno, left_col),
                (right_lineno, right_col),
                (end_lineno, end_offset),
            ]

        case _:
            return default_anchors


@dataclasses.dataclass(init=False, repr=False, slots=True)
class FrameSummary:
    """Information about a single frame from a traceback."""

    name: str
    """The name of the code that was executing when the frame was captured."""

    filename: str
    """The filename of the source code."""

    lineno: int
    """The line number of the source code."""

    colno: int | None
    """The column number of the source code."""

    end_lineno: int
    """The line number of the end of the source code."""

    end_colno: int | None
    """The column number of the end of the source code."""

    locals: dict[str, Any] | None = dataclasses.field(default=None, compare=False)
    """Either None if locals were not supplied, or a dict mapping the name to the repr() of the variable."""

    _lines: list[str] | None = dataclasses.field(default=None, compare=False)
    _carets: list[str] | None = dataclasses.field(default=None, compare=False)
    _anchors_value: list[tuple[int, int]] | None = dataclasses.field(default=None, compare=False)

    def __init__(
        self,
        name: str,
        filename: str,
        lineno: int,
        colno: int | None = None,
        end_lineno: int | None = None,
        end_colno: int | None = None,
        text: str | None = None,
        locals: dict[str, Any] | None = None,
    ):
        self.name = name

        from renpy.lexer import elide_filename

        self.filename = elide_filename(filename)

        self.lineno = lineno
        self.colno = colno
        self.end_lineno = end_lineno or lineno
        self.end_colno = end_colno

        self.locals = locals

        if text is not None:
            self._lines = [text]
            self._anchors_value = []
            self._carets = []
        else:
            self._lines = None
            self._anchors_value = None
            self._carets = None

    def __repr__(self):
        return f"<FrameSummary file {self.filename}, line {self.lineno} in {self.name}>"

    @property
    def line(self):
        """
        Return a first line of the frame source code.
        """

        return next(self.lines)

    @property
    def lines(self) -> Iterator[str]:
        """
        Yields the lines of the frame source code as-is, including indentation.
        """

        lines = self._lines
        if lines is None:
            self._lines = lines = []
            for lineno in range(self.lineno, self.end_lineno + 1):
                # treat errors (empty string) and empty lines (newline) as the same
                lines.append(linecache.getline(self.filename, lineno).rstrip())

        yield from lines

    @property
    def _anchors(self) -> list[tuple[int, int]] | None:
        if self._anchors_value is None:
            try:
                anchors = _calculate_anchors(self)
            except Exception:
                anchors = None

            self._anchors_value = anchors or []

        return self._anchors_value or None

    @property
    def carets(self) -> Iterator[str]:
        """
        Yields the carets line for each line in the frame source code.

        If the frame has no carets information, this is an empty iterator.

        Otherwise, the length of the iterator is equal to the length of the
        `FrameSummary.lines`.
        """

        if self._carets is not None:
            yield from self._carets

        if (anchors := self._anchors) is None:
            self._carets = []
            return

        result = []
        for lineno, line in enumerate(self.lines):
            carets: list[str] = []
            whitespace = True
            for colno, char in enumerate(line):
                pos = (lineno, colno)
                if not char.isspace():
                    whitespace = False

                if whitespace:
                    carets.append(" ")
                elif pos >= anchors[3]:
                    carets.append(" ")
                elif pos >= anchors[2]:
                    carets.append("~")
                elif pos >= anchors[1]:
                    carets.append("^")
                elif pos >= anchors[0]:
                    carets.append("~")
                else:
                    carets.append(" ")

            result.append("".join(carets))
            yield result[-1]

        self._carets = result

    @property
    def significant_lines(self):
        """
        Yields indexes of lines that are significant to render during format.

        This includes the first and last lines, and if the frame has carets
        information, the lines around the carets.
        """

        yield 0

        len_lines = len(list(self.lines))
        seen = {-1, 0, len_lines}
        if (anchors := self._anchors) is not None:
            if anchors[0] != anchors[1] or anchors[2] != anchors[3]:
                for lineno, _ in anchors:
                    for i in range(lineno - 1, lineno + 2):
                        if i in seen:
                            continue

                        seen.add(i)
                        yield i

        if len_lines - 1 not in seen:
            yield len_lines - 1

    def format(self, ctx: ExceptionPrintContext, /):
        """
        Returns a string representing one frame involved in the stack. This
        gets called for every frame to be printed in the stack summary.
        """

        ctx.location(self.filename, self.lineno, self.name)

        original_lines = list(self.lines)

        # Do not print empty lines.
        if not any(l.strip() for l in original_lines):
            return

        dedent_lines = textwrap.dedent("\n".join(original_lines)).split("\n")
        dedent_amount = len(original_lines[0]) - len(dedent_lines[0])
        if carets := [*self.carets]:
            carets = [c[dedent_amount:] for c in self.carets]
        else:
            carets = [None] * len(dedent_lines)

        sig_lines_list = list(self.significant_lines)
        with ctx.indent():
            for i, lineno in enumerate(self.significant_lines):
                if i:
                    line_diff = lineno - sig_lines_list[i - 1]
                    if line_diff == 2:
                        # 1 line in between - just output it
                        ctx.source_carets(dedent_lines[lineno - 1], carets[lineno - 1])
                    elif line_diff > 2:
                        # > 1 line in between - abbreviate
                        ctx.string(f"...<{line_diff - 1} lines>...")

                ctx.source_carets(dedent_lines[lineno], carets[lineno])


class StackSummary(list[FrameSummary]):
    """
    A list of FrameSummary objects, representing a stack of frames.
    """

    def __init__(self, traceback: "TracebackType | None", /):
        tb = traceback
        filenames = set()

        while tb is not None:
            try:
                if (frames := self._report_traceback(tb)) is not None:
                    self.extend(frames)
                    tb = tb.tb_next
                    continue
            except Exception:
                renpy.display.log.write("While getting report_traceback:")
                renpy.display.log.exception()

            frame = tb.tb_frame
            code = frame.f_code
            filename = code.co_filename
            if tb.tb_lasti < 0:
                lineno = colno = end_lineno = end_colno = None
            else:
                lineno, end_lineno, colno, end_colno = next(
                    itertools.islice(code.co_positions(), tb.tb_lasti // 2, None)
                )

            if lineno is None:
                lineno = tb.tb_lineno

            tb = tb.tb_next

            filenames.add(filename)
            linecache.lazycache(filename, frame.f_globals)
            self.append(
                FrameSummary(
                    code.co_name,
                    filename,
                    lineno,
                    colno,
                    end_lineno,
                    end_colno,
                )
            )

        for filename in filenames:
            linecache.checkcache(filename)

    @staticmethod
    def _report_traceback(tb: "TracebackType"):
        if renpy.config.raw_tracebacks:
            return None

        try:
            obj = tb.tb_frame.f_locals["self"]
            report_traceback = obj.report_traceback
        except Exception:
            return None

        name = tb.tb_frame.f_code.co_name
        last = tb.tb_next is None

        import inspect

        try:
            inspect.signature(report_traceback).bind(obj, name, last, tb.tb_frame)
        except TypeError:
            # Legacy path
            frames = report_traceback(name, last)
            if frames is None:
                return None

            rv: list[FrameSummary] = []
            for filename, line_number, name, text in frames:
                rv.append(
                    FrameSummary(
                        name,
                        filename,
                        line_number,
                        text=text,
                    )
                )

            return rv
        else:
            return report_traceback(name, last, tb.tb_frame)

    def should_filter(self, ctx: ExceptionPrintContext, /) -> bool:
        """
        Returns true if the stack is empty or all frames should be skipped
        when printing the stack.
        """

        for frame_summary in self:
            if not ctx.should_filter(frame_summary.filename):
                return False

        return True

    def format(self, ctx: ExceptionPrintContext, /):
        """Format the stack ready for printing.

        Returns a list of strings ready for printing.  Each string in the
        resulting list corresponds to a single frame from the stack.
        Each string ends in a newline; the strings may contain internal
        newlines as well, for those items with source text lines.

        For long sequences of the same frame and line, the first few
        repetitions are shown, followed by a summary line stating the exact
        number of further repetitions.
        """

        RECURSIVE_CUTOFF = 3  # Hardcoded in traceback.c.

        last_file = None
        last_line = None
        last_name = None
        count = 0
        for frame_summary in self:
            if ctx.should_filter(frame_summary.filename):
                continue

            if (
                last_file is None
                or last_file != frame_summary.filename
                or last_line is None
                or last_line != frame_summary.lineno
                or last_name is None
                or last_name != frame_summary.name
            ):
                if count > RECURSIVE_CUTOFF:
                    count -= RECURSIVE_CUTOFF
                    ctx.string(f"[Previous line repeated {count} more time{'s' if count > 1 else ''}]")

                last_file = frame_summary.filename
                last_line = frame_summary.lineno
                last_name = frame_summary.name
                count = 0
            count += 1
            if count > RECURSIVE_CUTOFF:
                continue

            with ctx.indent():
                frame_summary.format(ctx)

        if count > RECURSIVE_CUTOFF:
            count -= RECURSIVE_CUTOFF
            ctx.string(f"[Previous line repeated {count} more time{'s' if count > 1 else ''}]")


def _safe_string(value, what, func: Callable[..., str] = str):
    try:
        return func(value)
    except:
        return f"<{what} {func.__name__}() failed>"


def compute_closest_value(value: str, values: list[str]) -> str | None:
    """
    Computes the closest (lexicographically) value in the list of values.

    Returns None if execution takes too long or all values are too distant.
    """

    MAX_CANDIDATE_ITEMS = 1200  # Python uses 750, but renpy.store can contain a lot more.
    MAX_STRING_SIZE = 40
    MOVE_COST = 2
    CASE_COST = 1

    def substitution_cost(ch_a: str, ch_b: str):
        if ch_a == ch_b:
            return 0

        if ch_a.lower() == ch_b.lower():
            return CASE_COST

        return MOVE_COST

    def levenshtein_distance(a, b, max_cost):
        # A Python implementation of Python/suggestions.c:levenshtein_distance.

        # Both strings are the same
        if a == b:
            return 0

        # Trim away common affixes
        pre = 0
        while a[pre:] and b[pre:] and a[pre] == b[pre]:
            pre += 1
        a = a[pre:]
        b = b[pre:]
        post = 0
        while a[: post or None] and b[: post or None] and a[post - 1] == b[post - 1]:
            post -= 1
        a = a[: post or None]
        b = b[: post or None]
        if not a or not b:
            return MOVE_COST * (len(a) + len(b))
        if len(a) > MAX_STRING_SIZE or len(b) > MAX_STRING_SIZE:
            return max_cost + 1

        # Prefer shorter buffer
        if len(b) < len(a):
            a, b = b, a

        # Quick fail when a match is impossible
        if (len(b) - len(a)) * MOVE_COST > max_cost:
            return max_cost + 1

        # Instead of producing the whole traditional len(a)-by-len(b)
        # matrix, we can update just one row in place.
        # Initialize the buffer row
        row = list(range(MOVE_COST, MOVE_COST * (len(a) + 1), MOVE_COST))

        result = 0
        for bindex in range(len(b)):
            bchar = b[bindex]
            distance = result = bindex * MOVE_COST
            minimum = sys.maxsize
            for index in range(len(a)):
                # 1) Previous distance in this row is cost(b[:b_index], a[:index])
                substitute = distance + substitution_cost(bchar, a[index])
                # 2) cost(b[:b_index], a[:index+1]) from previous row
                distance = row[index]
                # 3) existing result is cost(b[:b_index+1], a[index])

                insert_delete = min(result, distance) + MOVE_COST
                result = min(insert_delete, substitute)

                # cost(b[:b_index+1], a[:index+1])
                row[index] = result
                if result < minimum:
                    minimum = result
            if minimum > max_cost:
                # Everything in this row is too big, so bail early.
                return max_cost + 1

        return result

    if len(values) > MAX_CANDIDATE_ITEMS:
        return None

    value_len = len(value)
    if value_len > MAX_STRING_SIZE:
        return None

    # Compute closest match
    best_distance = value_len
    suggestion = None
    for possible_name in values:
        if possible_name == value:
            # A missing attribute is "found". Don't suggest it (see cpython issue #88821).
            continue

        # No more than 1/3 of the involved characters should need changed.
        max_distance = (len(possible_name) + value_len + 3) * MOVE_COST // 6
        # Don't take matches we've already beaten.
        max_distance = min(max_distance, best_distance - 1)
        current_distance = levenshtein_distance(value, possible_name, max_distance)
        if current_distance > max_distance:
            continue

        if not suggestion or current_distance < best_distance:
            suggestion = possible_name
            best_distance = current_distance

    return suggestion


def handle_attribute_error(exception: AttributeError):
    # Manually created, e.g. AttributeError(..., name=None)
    if exception.name is None:
        return None

    try:
        d = dir(exception.obj)
    except Exception:
        return None

    hide_underscored = exception.name[:1] != "_"
    if hide_underscored and exception.__traceback__ is not None:
        tb = exception.__traceback__
        while tb.tb_next is not None:
            tb = tb.tb_next

        frame = tb.tb_frame
        if "self" in frame.f_locals and frame.f_locals["self"] is exception.obj:
            hide_underscored = False

    if hide_underscored:
        d = [x for x in d if x[:1] != "_"]

    if suggestion := compute_closest_value(exception.name, d):
        return f" Did you mean: '{suggestion}'?"


def handle_name_error(exception: NameError):
    # Manually created NameError(..., name=None)
    if exception.name is None:
        return None

    # find most recent frame
    tb = exception.__traceback__
    if tb is None:
        return None

    while tb.tb_next is not None:
        tb = tb.tb_next

    frame = tb.tb_frame
    names = {}
    names |= frame.f_locals
    names |= frame.f_globals
    names |= frame.f_builtins
    d = list(names)

    # Check first if we are in a method and the instance
    # has the wrong name as attribute
    if "self" in frame.f_locals:
        self = frame.f_locals["self"]
        if hasattr(self, exception.name):
            return f" Did you mean: 'self.{exception.name}'?"

    is_stdlib_module_name = exception.name in sys.stdlib_module_names
    if suggestion := compute_closest_value(exception.name, d):
        if is_stdlib_module_name:
            return f" Did you mean: '{suggestion}' or did you forget to import '{exception.name}'?"
        else:
            return f" Did you mean: '{suggestion}'?"
    elif is_stdlib_module_name:
        return f" Did you forget to import '{exception.name}'?"


def handle_import_error(exception: ImportError):
    wrong_name = exception.name_from
    mod_name = exception.name
    if wrong_name is None or mod_name is None:
        return None

    try:
        mod = __import__(mod_name)
        d = dir(mod)
    except Exception:
        return None

    if wrong_name[:1] != "_":
        d = [x for x in d if x[:1] != "_"]

    if suggestion := compute_closest_value(wrong_name, d):
        return f" Did you mean: '{suggestion}'?"


class TracebackException:
    """
    An exception ready for rendering.

    This class captures enough attributes from the original exception
    to this intermediary form to ensure that no references are held, while
    still being able to fully print or format it.

    max_group_width and max_group_depth control the formatting of exception
    groups. The depth refers to the nesting level of the group, and the width
    refers to the size of a single exception group's exceptions array. The
    formatted output is truncated when either limit is exceeded.

    - :attr:`__cause__` A TracebackException of the original __cause__.
    - :attr:`__context__` A TracebackException of the original __context__.
    - :attr:`exceptions` For exception groups - a list of TracebackException
      instances for the nested *exceptions*. ``None`` for other exceptions.
    - :attr:`__suppress_context__` The __suppress_context__ value from the
      original exception.
    - :attr:`__notes__` List of string display of the __notes__ value from the
    original exception.
    - :attr:`stack` A `StackSummary` representing the traceback.
    - :attr:`exc_type_str` String display of exc_type.
    - :attr:`filename` For syntax errors - the filename where the error
      occurred.
    - :attr:`lineno` For syntax errors - the linenumber where the error
      occurred.
    - :attr:`end_lineno` For syntax errors - the end linenumber where the error
      occurred. Can be `None` if not present.
    - :attr:`text` For syntax errors - the text where the error occurred.
    - :attr:`offset` For syntax errors - the offset into the text where the
      error occurred.
    - :attr:`end_offset` For syntax errors - the end offset into the text where
      the error occurred. Can be `None` if not present.
    - :attr:`msg` For syntax errors - the compiler error message.
    """

    def __init__(self, exception: BaseException, /, _seen=None):
        self.stack = StackSummary(exception.__traceback__)

        # Capture now to permit freeing resources
        self._str = _safe_string(exception, "exception")

        self.__notes__: list[str]
        try:
            notes = getattr(exception, "__notes__", None)
        except Exception as e:
            err = _safe_string(e, "__notes__", repr)
            self.__notes__ = [f"Ignored error getting __notes__: {err}"]
        else:
            if isinstance(notes, collections.abc.Sequence) and not isinstance(notes, (str, bytes)):
                self.__notes__ = [_safe_string(note, "note") for note in notes]

            elif notes is not None:
                self.__notes__ = [_safe_string(notes, "__notes__")]
            else:
                self.__notes__ = []

        self._is_syntax_error = False
        self._exc_type = type(exception)
        self._exc_type_qualname = type(exception).__qualname__
        self._exc_type_module = type(exception).__module__

        if isinstance(exception, SyntaxError):
            # Handle SyntaxError's specially
            self.filename = exception.filename
            self.lineno = exception.lineno
            self.end_lineno = exception.end_lineno
            self.text = exception.text
            self.offset = exception.offset
            self.end_offset = exception.end_offset
            self.msg = exception.msg
            self._is_syntax_error = True

        elif handlers := renpy.config.error_suggestion_handlers:
            suggestion = None
            # Reversed so that the most specific handler is called first.
            for typ, handler in reversed(handlers.items()):
                if isinstance(exception, typ):
                    if suggestion := handler(exception):
                        break

            if suggestion:
                suggestion = suggestion.lstrip()
                if self._str.endswith("."):
                    self._str += f" {suggestion}"
                else:
                    self._str += f". {suggestion}"

        self.__suppress_context__ = exception.__suppress_context__

        self.__cause__: TracebackException | None = None
        self.__context__: TracebackException | None = None
        self.exceptions: list[TracebackException] | None = None

        self.simple: str | None = None
        self.full: str | None = None
        self.traceback_fn: str | None = None

        # Handle loops in __cause__ or __context__.
        is_recursive_call = _seen is not None
        if _seen is None:
            _seen = set()
        _seen.add(id(exception))

        # Convert __cause__ and __context__ to `TracebackExceptions`s, use a
        # queue to avoid recursion (only the top-level call gets _seen == None)
        if not is_recursive_call:
            queue: list[tuple[TracebackException, BaseException | None]] = [(self, exception)]
            while queue:
                te, e = queue.pop()
                if e and e.__cause__ is not None and id(e.__cause__) not in _seen:
                    cause = TracebackException(e.__cause__, _seen=_seen)
                    te.__cause__ = cause
                    queue.append((te.__cause__, e.__cause__))

                if e and e.__context__ is not None and id(e.__context__) not in _seen:
                    context = TracebackException(e.__context__, _seen=_seen)
                    te.__context__ = context
                    queue.append((te.__context__, e.__context__))

                if e and isinstance(e, BaseExceptionGroup):
                    exceptions = []
                    for exc in e.exceptions:
                        te = TracebackException(exc, _seen=_seen)
                        exceptions.append(te)
                        queue.append((te, exc))

                    te.exceptions = exceptions

    @property
    def exc_type_str(self):
        s_type = self._exc_type_qualname
        s_mod = self._exc_type_module
        if s_mod not in ("__main__", "builtins"):
            if not isinstance(s_mod, str):
                s_mod = "<unknown>"
            s_type = s_mod + "." + s_type
        return s_type

    def __eq__(self, other):
        if isinstance(other, TracebackException):
            return self.__dict__ == other.__dict__

        return NotImplemented

    def __str__(self):
        return self._str

    def format_exception_only(self, ctx: ExceptionPrintContext | None = None, /, *, show_group=False) -> Any:
        """
        Format the exception type, message and notes.

        If exception print context is not given, it defaults to the non-colorized
        string context.

        Returns the result of `getvalue` of the exception print context.

        When *show_group* is ``True``, and the exception is an instance of
        :exc:`BaseExceptionGroup`, the nested exceptions are included as
        well, recursively, with indentation relative to their nesting depth.
        """

        if ctx is None:
            ctx = NonColoredExceptionPrintContext(io.StringIO())

        if self._is_syntax_error:
            self._format_syntax_error(ctx)
        else:
            ctx.final_exception_line(self.exc_type_str, self._str or None)

        for note in self.__notes__:
            ctx.string(note)

        if show_group and self.exceptions:
            with ctx.indent():
                for ex in self.exceptions:
                    ex.format_exception_only(ctx, show_group=show_group)

        return ctx.getvalue()

    def _format_syntax_error(self, ctx: ExceptionPrintContext):
        """Format SyntaxError exceptions (internal helper)."""
        # Show exactly where the problem was found.

        with ctx.indent():
            filename = self.filename or "<string>"
            if self.lineno is not None:
                ctx.location(filename, self.lineno, None)

            with ctx.indent():
                text = self.text
                if isinstance(text, str):
                    # text  = "   foo\n"
                    # rtext = "   foo"
                    # ltext =    "foo"
                    rtext = text.rstrip("\n")
                    ltext = rtext.lstrip(" \n\f")
                    spaces = len(rtext) - len(ltext)
                    if self.offset is None:
                        ctx.source_carets(ltext, None)

                    elif isinstance(self.offset, int):
                        if self.lineno is not None:
                            offset = normalize_renpy_line_offset(filename, self.lineno, self.offset, rtext)
                        else:
                            offset = self.offset

                        if self.lineno == self.end_lineno:
                            end_offset = self.end_offset or offset
                        else:
                            end_offset = len(rtext) + 1

                        if self.end_lineno is not None:
                            end_offset = normalize_renpy_line_offset(filename, self.end_lineno, end_offset, rtext)

                        if self.text and offset > len(self.text):
                            offset = len(rtext) + 1
                        if self.text and end_offset > len(self.text):
                            end_offset = len(rtext) + 1
                        if offset >= end_offset or end_offset < 0:
                            end_offset = offset + 1

                        # Convert 1-based column offset to 0-based index into stripped text
                        colno = offset - 1 - spaces
                        end_colno = end_offset - 1 - spaces

                        if colno >= 0:
                            carets = "".join(
                                # non-space whitespace (likes tabs) must be kept for alignment
                                "^" if colno <= i < end_colno else (c if c.isspace() else " ")
                                for i, c in enumerate(ltext)
                            )
                            ctx.source_carets(ltext, carets)
                        else:
                            ctx.source_carets(ltext, None)

        msg = self.msg or "<no detail available>"
        ctx.final_exception_line(self.exc_type_str, msg)

    def format(self, ctx: ExceptionPrintContext | None = None, /, *, chain=True, show_group=False) -> Any:
        """
        Format the exception.

        If chain is True, adds *__cause__* and *__context__* exceptions to the output.

        If exception print context is not given, it defaults to the non-colorized
        string context.

        Returns the result of `getvalue` of the exception print context.

        The message indicating which exception occurred is always the last
        string in the output.
        """

        if ctx is None:
            ctx = NonColoredExceptionPrintContext(io.StringIO())

        output: list[tuple[Callable[[], None] | None, TracebackException]] = []
        exc = self

        if chain:
            while exc:
                if exc.__cause__ is not None:
                    chained_method = ctx.chain_cause
                    chained_exc = exc.__cause__
                elif exc.__context__ is not None and not exc.__suppress_context__:
                    chained_method = ctx.chain_context
                    chained_exc = exc.__context__
                else:
                    chained_method = chained_exc = None

                output.append((chained_method, exc))
                exc = chained_exc
        else:
            output.append((None, exc))

        for meth, exc in reversed(output):
            if meth is not None:
                meth()
                ctx.emit_context = True

            if exc.exceptions is None:
                if not exc.stack.should_filter(ctx):
                    if ctx.emit_context:
                        ctx.string("Traceback (most recent call last):")

                    exc.stack.format(ctx)

                exc.format_exception_only(ctx)

            elif ctx.exception_group_depth > ctx.max_group_depth:
                # exception group, but depth exceeds limit
                ctx.string(f"... (max group depth is {ctx.max_group_depth})")

            else:
                # format exception group
                is_toplevel = ctx.exception_group_depth == 0
                if is_toplevel:
                    ctx.exception_group_depth += 1

                if not exc.stack.should_filter(ctx):
                    if ctx.emit_context:
                        ctx.string("Exception Group Traceback (most recent call last):")

                    exc.stack.format(ctx)
                    exc.format_exception_only(ctx)

                num_exceptions = len(exc.exceptions)
                if num_exceptions <= ctx.max_group_width:
                    n = num_exceptions
                else:
                    n = ctx.max_group_width + 1

                ctx.need_close = False
                for i in range(n):
                    last_exc = i == n - 1
                    if last_exc:
                        # The closing frame may be added by a recursive call
                        ctx.need_close = True

                    truncated = i >= ctx.max_group_width
                    with ctx.indent():
                        ctx.exceptions_separator(i, n)

                        ctx.exception_group_depth += 1
                        if not truncated:
                            exc.exceptions[i].format(ctx, chain=chain)
                        else:
                            remaining = num_exceptions - ctx.max_group_width
                            plural = "s" if remaining > 1 else ""
                            ctx.string(f"and {remaining} more exception{plural}")

                        if last_exc and ctx.need_close:
                            ctx.exceptions_close()
                            ctx.need_close = False

                    ctx.exception_group_depth -= 1

                if is_toplevel:
                    assert ctx.exception_group_depth == 1
                    ctx.exception_group_depth = 0

        return ctx.getvalue()

    # Mimic old report_exception return value.
    def __getitem__(self, pos):
        return (self.simple, self.full, self.traceback_fn)[pos]

    def __iter__(self):
        return iter([self.simple, self.full, self.traceback_fn])

    def __len__(self):
        return 3


def open_error_file(fn, mode) -> tuple[TextIO, str]:
    """
    Opens an error/log/file. Returns the open file, and the filename that
    was opened.
    """

    try:
        new_fn = os.path.join(renpy.config.logdir, fn)  # type: ignore
        f = open(new_fn, mode)
        return f, new_fn
    except Exception:
        pass

    try:
        f = open(fn, mode)
        return f, fn
    except Exception:
        pass

    import tempfile

    new_fn = os.path.join(tempfile.gettempdir(), "renpy-" + fn)
    return open(new_fn, mode), new_fn


def report_exception(e: Exception, editor=True) -> TracebackException:
    # Note: Doki Doki Literature club calls this as ("Words...", False).
    # For what it's worth.
    if not isinstance(e, Exception):  # type: ignore
        e = Exception(e)

    # Still, if we were called directly with exception without traceback
    # we need to populate it.
    if e.__traceback__ is None:
        from types import TracebackType

        f = sys._getframe().f_back  # type: ignore
        assert f is not None
        e.__traceback__ = TracebackType(None, f, f.f_lasti, f.f_lineno)

    if not int(os.environ.get("RENPY_REPORT_EXCEPTIONS", "1")):
        raise

    # The sound system may not be ready during exception handling.
    renpy.config.debug_sound = False

    te = TracebackException(e)

    # Return values - which can be displayed to the user.
    simple = io.StringIO()
    full = io.StringIO()

    print(str(renpy.game.exception_info), file=simple)
    te.format(NonColoredExceptionPrintContext(simple, filter_private=True, emit_context=False))

    te.format(NonColoredExceptionPrintContext(full, filter_private=False))

    # Write to stdout/stderr.
    try:
        print(file=sys.stdout)
        print("Full traceback:", file=sys.stdout)
        te.format(MaybeColoredExceptionPrintContext(sys.stdout, filter_private=False, emit_context=False))

        print(file=sys.stdout)
        print(str(renpy.game.exception_info), file=sys.stdout)
        te.format(MaybeColoredExceptionPrintContext(sys.stdout, filter_private=True, emit_context=False))
    except Exception:
        pass

    print(file=full)

    try:
        print(str(platform.platform()), str(platform.machine()), file=full)
        print(renpy.version, file=full)
        print(renpy.config.name + " " + renpy.config.version, file=full)
        print(str(time.ctime()), file=full)
    except Exception:
        pass

    te.simple = simple.getvalue()
    te.full = full.getvalue()

    # Inside of the file, which may not be openable.
    try:
        f, te.traceback_fn = open_error_file("traceback.txt", "w")

        with f:
            f.write("\ufeff")  # BOM

            print("I'm sorry, but an uncaught exception occurred.", file=f)
            print("", file=f)

            f.write(te.simple)

            print("", file=f)
            print("-- Full Traceback ------------------------------------------------------------", file=f)
            print("", file=f)

            f.write(te.full)

        try:
            renpy.util.expose_file(te.traceback_fn)
        except Exception:
            pass

        try:
            if editor and ((renpy.game.args.command == "run") or (renpy.game.args.errors_in_editor)):
                renpy.editor.launch_editor([te.traceback_fn], 1, transient=True)
        except Exception:
            pass

        try:
            if not renpy.session.get("traceback_load", False):
                renpy.loadsave.cycle_saves("_tracesave-", 10)
                renpy.loadsave.save("_tracesave-1", extra_json={"_traceback": te.full}, include_screenshot=renpy.config.tracesave_screenshot)
        except Exception:
            pass

    except Exception:
        te.traceback_fn = os.path.join(renpy.config.basedir, "traceback.txt")

    return te
