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

# This file contains code for formatting tracebacks.

from typing import IO, TYPE_CHECKING, Iterable, Iterator, Callable, Any

if TYPE_CHECKING:
    from types import TracebackType

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


# Reimplement parts of Python 3.14 traceback module, so we can add Ren'Py-specific behavior.
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


def _calculate_anchors(frame_summary: 'FrameSummary'):
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
    start_offset = frame_summary.colno
    end_offset = frame_summary.end_colno

    # Correct extra offset from _ren.py transformation.
    if frame_summary.filename.endswith("_ren.py"):
        from renpy.lexer import ren_py_to_rpy_offsets
        try:
            with open(frame_summary.filename, "r", encoding="utf-8") as f:
                lines = f.readlines()

            offsets = list(ren_py_to_rpy_offsets(lines, frame_summary.filename))
        except Exception:
            return None

        for i, offset in enumerate(offsets, start=1):
            if offset is not None:
                if i == frame_summary.lineno:
                    start_offset -= offset

                elif i == frame_summary.end_lineno:
                    end_offset -= offset

    # Correct extra offset from munged names.
    from renpy.lexer import munge_filename, get_string_munger
    munge_prefix = munge_filename(frame_summary.filename)
    munge_string = get_string_munger(munge_prefix)
    len_prefix = len(munge_prefix) - 2

    idx = 0
    munged_first_line = munge_string(first_line)
    while (idx := munged_first_line.find(munge_prefix, idx, start_offset + len_prefix)) != -1:
        start_offset -= len_prefix
        idx += len_prefix

    idx = 0
    munged_last_line = munge_string(last_line)
    while (idx := munged_last_line.find(munge_prefix, idx, end_offset + len_prefix)) != -1:
        end_offset -= len_prefix
        idx += len_prefix

    default_anchors = [
        (0, start_offset), (0, start_offset),
        (end_lineno, end_offset), (end_lineno, end_offset)]

    # get exact code segment corresponding to the instruction
    segment = "\n".join(all_lines)
    segment = segment[start_offset:len(segment) - (len(last_line) - end_offset)]

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
        return offset

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
            left_lineno, left_col = increment_until(
                left_lineno, left_col, lambda x: not x.isspace() and x != ')')

            # binary op is 1 or 2 characters long, on the same line,
            # before the right subexpression
            right_lineno = left_lineno
            right_col = left_col + 1
            if (
                right_col < len(lines[right_lineno])
                and (
                    # operator char should not be in the right subexpression
                    right.lineno - 2 > right_lineno or
                    right_col < normalize(right.lineno - 2, right.col_offset)
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
            left_lineno, left_col = increment_until(left_lineno, left_col, lambda x: x == '[')
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
            left_lineno, left_col = increment_until(left_lineno, left_col, lambda x: x == '(')
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


class ExceptionPrintContext(abc.ABC):
    def __init__(self, *, filter_private: bool):
        self.seen = set()
        self.indent_depth = 0
        self.exception_group_depth = 0
        self.need_close = False
        self.filter_private = filter_private

    def should_filter(self, filename: str) -> bool:
        """
        Returns true if the FrameSummary with the given filename should be
        skipped when printing the stack.

        By default filters Ren'Py common code, Ren'Py libraries, and all pure
        Python code.
        """

        if not self.filter_private:
            return False

        if filename.endswith((".rpy", ".rpym", "_ren.py")):
            return filename.startswith(("renpy/common/", "libs/"))
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
    def emit_location(self, filename: str, lineno: int, name: str):
        """
        Emits a line that shows the location of the frame in the source code.

        `filename`
            The filename of the source code.

        `lineno`
            The line number of the source code.

        `name`
            The name of the code that was running when the exception occurred.

        Subclasses should override this method to emit the location information
        in a way that makes sense for their particular application.
        """

    @abc.abstractmethod
    def emit_source_carets(self, line: str, carets: str | None):
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
    def emit_string(self, text: str):
        """
        Emits a string.
        """

    @abc.abstractmethod
    def emit_iterable(self, text_gen: Iterable[str]):
        """
        Emits an iterable of strings.
        """


class ANSIColoredPrintContext(ExceptionPrintContext):
    RESET = "\x1b[0m"
    MAGENTA = "\x1b[35m"
    BOLD_RED = "\x1b[1;31m"
    RED = "\x1b[31m"

    def __init__(self, file: IO[str], *, filter_private: bool):
        super().__init__(filter_private=filter_private)
        self.file = file

    def _print(self, text: str):
        print(f"{'  ' * self.indent_depth}{text}", file=self.file)

    def emit_location(self, filename, lineno, name):
        self._print(
            f'File {self.MAGENTA}"{filename}"{self.RESET}, '
            f'line {self.MAGENTA}{lineno}{self.RESET}, '
            f'in {self.MAGENTA}{name}{self.RESET}')

    def emit_source_carets(self, line, carets):
        if carets is None:
            self._print(line)
            return

        zipped = zip(line, carets, strict=True)
        colorized_line_parts: list[str] = []
        colorized_carets_parts: list[str] = []
        for color, group in itertools.groupby(zipped, key=lambda x: x[1]):
            caret_group = list(group)
            line_part = "".join(char for char, _ in caret_group)
            caret_part = "".join(caret for _, caret in caret_group)
            if color == "^":
                line_part = f"{self.BOLD_RED}{line_part}{self.RESET}"
                caret_part = f"{self.BOLD_RED}{caret_part}{self.RESET}"
            elif color == "~":
                line_part = f"{self.RED}{line_part}{self.RESET}"
                caret_part = f"{self.RED}{caret_part}{self.RESET}"

            colorized_line_parts.append(line_part)
            colorized_carets_parts.append(caret_part)

        self._print("".join(colorized_line_parts))
        self._print("".join(colorized_carets_parts))

    def emit_string(self, text: str):
        self._print(text)

    def emit_iterable(self, text_gen: Iterable[str]):
        for text in text_gen:
            self._print(text)


class NonColoredExceptionPrintContext(ExceptionPrintContext):
    def __init__(self, file: IO[str], *, filter_private: bool):
        super().__init__(filter_private=filter_private)
        self.file = file

    def _print(self, text: str):
        print(f"{'  ' * self.indent_depth}{text}", file=self.file)

    def emit_location(self, filename: str, lineno: int, name: str):
        self._print(f'    File "{filename}", line {lineno}, in {name}\n')

    def emit_source_carets(self, line: str, carets: str | None):
        self._print(line)
        if carets is not None:
            self._print(carets)

    def emit_string(self, text: str):
        self._print(text)

    def emit_iterable(self, text_gen: Iterable[str]):
        for text in text_gen:
            self._print(text)


@dataclasses.dataclass(repr=False, slots=True)
class FrameSummary:
    """Information about a single frame from a traceback."""

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

    name: str
    """The name of the function or method that was executing when the frame was captured."""

    _lines: list[str] | None = dataclasses.field(init=False, default=None, compare=False)
    _carets: list[str] | None = dataclasses.field(init=False, default=None, compare=False)
    _anchors_value: list[tuple[int, int]] | None = dataclasses.field(init=False, default=None, compare=False)

    locals: dict[str, Any] | None = dataclasses.field(default=None, compare=False)
    """Either None if locals were not supplied, or a dict mapping the name to the repr() of the variable."""

    def __post_init__(self):
        if self.lineno is None:
            raise ValueError("FrameSummary.lineno must not be None")

        if self.end_lineno is None:
            self.end_lineno = self.lineno

        from renpy.lexer import elide_filename
        self.filename = elide_filename(self.filename)

    def __repr__(self):
        return f"<FrameSummary file {self.filename}, line {self.lineno} in {self.name}>"

    @property
    def lines(self) -> Iterator[str]:
        """
        Yields the lines of the frame source code as-is.
        """

        if self._lines is None:
            lines = []
            for lineno in range(self.lineno, self.end_lineno + 1):
                # treat errors (empty string) and empty lines (newline) as the same
                lines.append(linecache.getline(self.filename, lineno).rstrip())

            self._lines = lines
        else:
            lines = self._lines

        yield from lines

    @property
    def _anchors(self) -> list[tuple[int, int]] | None:
        if self._anchors_value is None:
            try:
                anchors = _calculate_anchors(self)
            except Exception:
                anchors = None

            if anchors is None:
                anchors = []
            self._anchors_value = anchors

        return self._anchors_value or None

    @property
    def carets(self) -> Iterator[str]:
        """
        Yields the carets line for each line in the frame source code.
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
        Yields line numbers that are significant to render during format.
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

        ctx.emit_location(self.filename, self.lineno, self.name)

        original_lines = list(self.lines)
        dedent_lines = textwrap.dedent("\n".join(original_lines)).split("\n")
        dedent_amount = len(original_lines[0]) - len(dedent_lines[0])
        carets = [c[dedent_amount:] for c in self.carets]
        if not carets:
            carets = [None] * len(dedent_lines)

        sig_lines_list = list(self.significant_lines)
        with ctx.indent():
            for i, lineno in enumerate(self.significant_lines):
                if i:
                    line_diff = lineno - sig_lines_list[i - 1]
                    if line_diff == 2:
                        # 1 line in between - just output it
                        ctx.emit_source_carets(dedent_lines[lineno - 1], carets[lineno - 1])
                    elif line_diff > 2:
                        # > 1 line in between - abbreviate
                        ctx.emit_string(f"...<{line_diff - 1} lines>...")

                ctx.emit_source_carets(dedent_lines[lineno], carets[lineno])


class StackSummary(list[FrameSummary]):
    """
    A list of FrameSummary objects, representing a stack of frames.
    """

    def __init__(self, traceback: 'TracebackType', /):
        tb = traceback
        filenames = set()

        while tb:
            frame = tb.tb_frame
            code = frame.f_code
            filename = code.co_filename
            if tb.tb_lasti < 0:
                lineno = colno = end_lineno = end_colno = None
            else:
                lineno, end_lineno, colno, end_colno = \
                    next(itertools.islice(code.co_positions(), tb.tb_lasti // 2, None))

            if lineno is None:
                lineno = tb.tb_lineno

            tb = tb.tb_next

            filenames.add(filename)
            linecache.lazycache(filename, frame.f_globals)
            self.append(FrameSummary(
                filename,
                lineno,
                colno,
                end_lineno or lineno,
                end_colno,
                code.co_name,
                # frame.f_locals,
            ))

        for filename in filenames:
            linecache.checkcache(filename)

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
                last_file is None or last_file != frame_summary.filename or
                last_line is None or last_line != frame_summary.lineno or
                last_name is None or last_name != frame_summary.name
            ):
                if count > RECURSIVE_CUTOFF:
                    count -= RECURSIVE_CUTOFF
                    ctx.emit_string(
                        f'[Previous line repeated {count} more '
                        f'time{"s" if count > 1 else ""}]')

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
            ctx.emit_string(
                f'[Previous line repeated {count} more '
                f'time{"s" if count > 1 else ""}]')


def _safe_string(value, what, func: Callable[..., str] = str):
    try:
        return func(value)
    except:
        return f'<{what} {func.__name__}() failed>'


class TracebackException:
    """An exception ready for rendering.

    The traceback module captures enough attributes from the original exception
    to this intermediary form to ensure that no references are held, while
    still being able to fully print or format it.

    max_group_width and max_group_depth control the formatting of exception
    groups. The depth refers to the nesting level of the group, and the width
    refers to the size of a single exception group's exceptions array. The
    formatted output is truncated when either limit is exceeded.

    Use `from_exception` to create TracebackException instances from exception
    objects, or the constructor to create TracebackException instances from
    individual components.

    - :attr:`__cause__` A TracebackException of the original *__cause__*.
    - :attr:`__context__` A TracebackException of the original *__context__*.
    - :attr:`exceptions` For exception groups - a list of TracebackException
      instances for the nested *exceptions*.  ``None`` for other exceptions.
    - :attr:`__suppress_context__` The *__suppress_context__* value from the
      original exception.
    - :attr:`stack` A `StackSummary` representing the traceback.
    - :attr:`exc_type_str` String display of exc_type
    - :attr:`filename` For syntax errors - the filename where the error
      occurred.
    - :attr:`lineno` For syntax errors - the linenumber where the error
      occurred.
    - :attr:`end_lineno` For syntax errors - the end linenumber where the error
      occurred. Can be `None` if not present.
    - :attr:`text` For syntax errors - the text where the error
      occurred.
    - :attr:`offset` For syntax errors - the offset into the text where the
      error occurred.
    - :attr:`end_offset` For syntax errors - the end offset into the text where
      the error occurred. Can be `None` if not present.
    - :attr:`msg` For syntax errors - the compiler error message.
    """

    def __init__(
        self,
        exception: BaseException, *,
        max_group_width=15,
        max_group_depth=10,
        _seen=None,
    ):
        # Handle loops in __cause__ or __context__.
        is_recursive_call = _seen is not None
        if _seen is None:
            _seen = set()
        _seen.add(id(exception))

        self.max_group_width = max_group_width
        self.max_group_depth = max_group_depth

        assert exception.__traceback__ is not None
        self.stack = StackSummary(exception.__traceback__)

        # Capture now to permit freeing resources
        self._str = _safe_string(exception, 'exception')
        try:
            self.__notes__ = getattr(exception, '__notes__', None)
        except Exception as e:
            self.__notes__ = [
                f'Ignored error getting __notes__: {_safe_string(e, '__notes__', repr)}']

        self._is_syntax_error = False
        self._exc_type = type(exception)
        self.exc_type_qualname = type(exception).__qualname__
        self.exc_type_module = type(exception).__module__

        if isinstance(exception, SyntaxError):
            # Handle SyntaxError's specially
            self.filename = exception.filename
            lno = exception.lineno
            self.lineno = str(lno) if lno is not None else None
            end_lno = exception.end_lineno
            self.end_lineno = str(end_lno) if end_lno is not None else None
            self.text = exception.text
            self.offset = exception.offset
            self.end_offset = exception.end_offset
            self.msg = exception.msg
            self._is_syntax_error = True

        self.__suppress_context__ = exception.__suppress_context__

        self.__cause__: TracebackException | None = None
        self.__context__: TracebackException | None = None
        self.exceptions: list[TracebackException] | None = None

        # Convert __cause__ and __context__ to `TracebackExceptions`s, use a
        # queue to avoid recursion (only the top-level call gets _seen == None)
        if not is_recursive_call:
            queue: list[tuple[TracebackException, BaseException | None]] = [(self, exception)]
            while queue:
                te, e = queue.pop()
                if (e and e.__cause__ is not None and id(e.__cause__) not in _seen):
                    cause = TracebackException(
                        e.__cause__,
                        max_group_width=max_group_width,
                        max_group_depth=max_group_depth,
                        _seen=_seen)

                    te.__cause__ = cause
                    queue.append((te.__cause__, e.__cause__))

                if (e and e.__context__ is not None and id(e.__context__) not in _seen):
                    context = TracebackException(
                        e.__context__,
                        max_group_width=max_group_width,
                        max_group_depth=max_group_depth,
                        _seen=_seen)

                    te.__context__ = context
                    queue.append((te.__context__, e.__context__))

                if e and isinstance(e, BaseExceptionGroup):
                    exceptions = []
                    for exc in e.exceptions:
                        te = TracebackException(
                            exc,
                            max_group_width=max_group_width,
                            max_group_depth=max_group_depth,
                            _seen=_seen)
                        exceptions.append(te)
                        queue.append((te, exc))

                    te.exceptions = exceptions

        self.simple: str | None = None
        self.full: str | None = None
        self.traceback_fn: str | None = None

    @property
    def exc_type_str(self):
        s_type = self.exc_type_qualname
        s_mod = self.exc_type_module
        if s_mod not in ("__main__", "builtins"):
            if not isinstance(s_mod, str):
                s_mod = "<unknown>"
            s_type = s_mod + '.' + s_type
        return s_type

    def __eq__(self, other):
        if isinstance(other, TracebackException):
            return self.__dict__ == other.__dict__

        return NotImplemented

    def __str__(self):
        return self._str

    def _format_final_exc_line(self):
        if self._str:
            return f"{self.exc_type_str}: {self._str}"
        else:
            return f"{self.exc_type_str}"

    def format_exception_only(self, ctx: ExceptionPrintContext, /, *, show_group=False):
        """Format the exception part of the traceback.

        The return value is a generator of strings, each ending in a newline.

        Generator yields the exception message.
        For :exc:`SyntaxError` exceptions, it
        also yields (before the exception message)
        several lines that (when printed)
        display detailed information about where the syntax error occurred.
        Following the message, generator also yields
        all the exception's ``__notes__``.

        When *show_group* is ``True``, and the exception is an instance of
        :exc:`BaseExceptionGroup`, the nested exceptions are included as
        well, recursively, with indentation relative to their nesting depth.
        """

        if self._is_syntax_error:
            raise NotImplementedError

        ctx.emit_string(self._format_final_exc_line())

        if (
            isinstance(self.__notes__, collections.abc.Sequence)
            and not isinstance(self.__notes__, (str, bytes))
        ):
            for note in self.__notes__:
                ctx.emit_iterable(_safe_string(note, 'note').split('\n'))

        elif self.__notes__ is not None:
            ctx.emit_string(_safe_string(self.__notes__, '__notes__', func=repr))

        if show_group and self.exceptions:
            with ctx.indent():
                for ex in self.exceptions:
                    ex.format_exception_only(ctx, show_group=show_group)

    def format(self, ctx: ExceptionPrintContext, /, *, chain=True, show_group=False):
        """Format the exception.

        If chain is not *True*, *__cause__* and *__context__* will not be formatted.

        The return value is a generator of strings, each ending in a newline and
        some containing internal newlines. `print_exception` is a wrapper around
        this method which just prints the lines to a file.

        The message indicating which exception occurred is always the last
        string in the output.
        """

        output: list[tuple[str | None, TracebackException]] = []
        exc = self

        if chain:
            while exc:
                if exc.__cause__ is not None:
                    chained_msg = (
                        "\nThe above exception was the direct cause "
                        "of the following exception:\n\n")
                    chained_exc = exc.__cause__
                elif (exc.__context__ is not None and
                      not exc.__suppress_context__):
                    chained_msg = (
                        "\nDuring handling of the above exception, "
                        "another exception occurred:\n\n")
                    chained_exc = exc.__context__
                else:
                    chained_msg = None
                    chained_exc = None

                output.append((chained_msg, exc))
                exc = chained_exc
        else:
            output.append((None, exc))

        for msg, exc in reversed(output):
            if exc.stack.should_filter(ctx):
                ctx.emit_string("Traceback is suppressed.")
                continue

            if msg is not None:
                ctx.emit_string(msg)

            if exc.exceptions is None:
                ctx.emit_string('Traceback (most recent call last):')

                with ctx.indent():
                    exc.stack.format(ctx)

                exc.format_exception_only(ctx)

            elif ctx.exception_group_depth > self.max_group_depth:
                # exception group, but depth exceeds limit
                ctx.emit_string(f"... (max_group_depth is {self.max_group_depth})")
            else:
                # format exception group
                is_toplevel = (ctx.exception_group_depth == 0)
                if is_toplevel:
                    ctx.exception_group_depth += 1

                ctx.emit_string('Exception Group Traceback (most recent call last):')

                with ctx.indent():
                    exc.stack.format(ctx)

                exc.format_exception_only(ctx)

                num_exceptions = len(exc.exceptions)
                if num_exceptions <= self.max_group_width:
                    n = num_exceptions
                else:
                    n = self.max_group_width + 1
                ctx.need_close = False
                for i in range(n):
                    last_exc = (i == n-1)
                    if last_exc:
                        # The closing frame may be added by a recursive call
                        ctx.need_close = True

                    truncated = (i >= self.max_group_width)
                    title = f'{i+1}' if not truncated else '...'
                    with ctx.indent():
                        ctx.emit_string(
                            ('+-' if i == 0 else '  ') +
                            f'+---------------- {title} ----------------')

                        ctx.exception_group_depth += 1
                        if not truncated:
                            exc.exceptions[i].format(ctx, chain=chain)
                        else:
                            remaining = num_exceptions - self.max_group_width
                            plural = 's' if remaining > 1 else ''
                            ctx.emit_string(f"and {remaining} more exception{plural}")

                        if last_exc and ctx.need_close:
                            ctx.emit_string("+------------------------------------")
                            ctx.need_close = False

                    ctx.exception_group_depth -= 1

                if is_toplevel:
                    assert ctx.exception_group_depth == 1
                    ctx.exception_group_depth = 0

    # Mimic old report_exception return value.
    def __getitem__(self, pos):
        return (self.simple, self.full, self.traceback_fn)[pos]

    def __iter__(self):
        return iter([self.simple, self.full, self.traceback_fn])

    def __len__(self):
        return 3


def open_error_file(fn, mode):
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
    te.format(NonColoredExceptionPrintContext(simple, filter_private=True))

    print("Full traceback:", file=full)
    te.format(NonColoredExceptionPrintContext(full, filter_private=False))

    # Write to stdout/stderr.
    try:
        sys.stdout.write("\n")
        te.format(ANSIColoredPrintContext(sys.stdout, filter_private=False))
        sys.stdout.write("\n")
        te.format(ANSIColoredPrintContext(sys.stdout, filter_private=True))
    except Exception:
        pass

    print('', file=full)

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
            print('', file=f)

            f.write(te.simple)

            print('', file=f)
            print("-- Full Traceback ------------------------------------------------------------", file=f)
            print('', file=f)

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

    except Exception:
        te.traceback_fn = os.path.join(renpy.config.basedir, "traceback.txt")

    return te
