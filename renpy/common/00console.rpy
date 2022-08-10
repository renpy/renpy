# console.rpy
# Ren'Py console
# Copyright (C) 2012-2017 Shiz, C, delta, PyTom
#
# This program is free software. It comes without any warranty, to the extent permitted by applicable law.
# You can redistribute it and/or modify it under the terms of the Do What The Fuck You Want To Public License,
# Version 2, as published by Sam Hocevar. See http://sam.zoy.org/wtfpl/COPYING for more details.
#
# Usage:
#  With config.developer or config.console set to True, press the console key (`, the backtick, by default) to open the console.
#  Type 'help' for in-console help. Press escape or right-click to close the console.
#
# The following configuration variables are offered for customization:
#  - config.console_history_size: the number of commands to store in history. default: 100
#  - config.console_custom_commands: a simple name -> function dictionary for custom commands. Command functions should take a
# lexer, and return result text.
# The following styles are offered for customization:
#  - _console: the debug console frame.
#
#  - _console_input: the input frame.
#  - _console_prompt: the '>' or '...' text preceding a command input.
#  - _console_input_text: the actual text that is being input by the user.
#
#  - _console_history: the history frame.
#  - _console_history_item: an item frame in the history.
#  - _console_command: a command frame in the command history.
#  - _console_command_text: the actual command text.
#  - _console_result: the result frame from a command in the command history, if applicable.
#  - _console_result_text: the actual result text, if no error occurred.
#  - _console_result_text: the actual result text, if an error occurred.
#
#  - _console_trace: the trace box used to show expression and variable traces.
#  - _console_trace_var: the variable in a trace box.
#  - _console_trace_value: the value in a trace box.

# Console styles.
init -1500:

    style _console is _default:
        xpadding gui._scale(20)
        ypadding gui._scale(10)
        xfill True
        yfill True
        background "#d0d0d0d0"

    style _console_backdrop:
        background "#d0d0d0"

    style _console_vscrollbar is _vscrollbar

    style _console_text is _default:
        size gui._scale(16)

    style _console_input is _default:
        xfill True

    style _console_prompt is _console_text:
        minwidth gui._scale(22)
        text_align 1.0

    style _console_input_text is _console_text:
        color "#000000"
        adjust_spacing False

    style _console_history is _default:
        xfill True

    style _console_history_item is _default:
        xfill True
        bottom_margin gui._scale(8)

    style _console_command is _default:
        left_padding gui._scale(26)

    style _console_command_text is _console_text:
        color "#000000"

    style _console_result is _default:
        left_padding gui._scale(26)

    style _console_result_text is _console_text

    style _console_error_text is _console_text:
        color "#603030"
        # color "#ff8080"

    style _console_trace is _default:
        background "#00000040"
        xalign 1.0
        top_margin 20
        right_margin 20
        xpadding 2
        ypadding 2

    style _console_trace_text is _default:
        color "#fff"
        size gui._scale(16)

    style _console_trace_var is _console_trace_text:
        bold True

    style _console_trace_value is _console_trace_text

# Configuration and style initalization.
init -1500 python:

    # If true, the console is enabled despite config.developer being False.
    config.console = False

    config.console_history_size = 100
    config.console_history_lines = 1000

    config.console_commands = { }

    # If not None, this is called with the command that's about to be run
    # by the console. (The command is represented as a list of strings.) It
    # is expected to return a list of strings, which is the command that will
    # be actually run.
    config.console_callback = None

default persistent._console_short = True
default persistent._console_traced_short = True
default persistent._console_unicode_escaping = False

init -1500 python in _console:
    from store import config, persistent, NoRollback
    import sys
    import traceback
    import store

    from reprlib import Repr
    class PrettyRepr(Repr):
        _ellipsis = str("...")

        def _repr_bytes(self, x, level):
            s = repr(x)
            if len(s) > self.maxstring:
                i = max(0, (self.maxstring - 3) // 2)
                s = s[:i] + self._ellipsis + s[len(s) - i:]
            return s

        def _repr_string(self, x, level):
            s = repr(x)

            if persistent._console_unicode_escaping:
                s = s.encode("ascii", "backslashreplace").decode("utf-8")

            if len(s) > self.maxstring:
                i = max(0, (self.maxstring - 3) // 2)
                s = s[:i] + self._ellipsis + s[len(s) - i:]
            return s

        if PY2:
            repr_str = _repr_bytes
            repr_unicode = _repr_string
        else:
            repr_bytes = _repr_bytes
            repr_str = _repr_string

        def repr_tuple(self, x, level):
            if not x: return "()"

            if level <= 0: return "(...)"

            if len(x) == 1:
                item_r = self.repr1(x[0], level - 1)
                if item_r.endswith("\n"):
                    item_r = item_r[:-1] + ",\n"
                else:
                    item_r = item_r + ","
                return "(%s)" % item_r

            iter_x = self._to_shorted_list(x, self.maxtuple)
            return self._repr_iterable(iter_x, level, '(', ')')

        def repr_list(self, x, level):
            if not x: return "[]"

            if level <= 0: return "[...]"

            iter_x = self._to_shorted_list(x, self.maxlist)
            return self._repr_iterable(iter_x, level, '[', ']')

        repr_RevertableList = repr_list

        def repr_set(self, x, level):
            if not x: return "set()"

            if level <= 0: return "set({...})"

            iter_x = self._to_shorted_list(x, self.maxset, sort=True)
            return self._repr_iterable(iter_x, level, '{', '}')

        repr_RevertableSet = repr_set

        def repr_frozenset(self, x, level):
            if not x: return "frozenset()"

            if level <= 0: return "frozenset({...})"

            iter_x = self._to_shorted_list(x, self.maxfrozenset, sort=True)
            return self._repr_iterable(iter_x, level, 'frozenset({', '})')

        def repr_dict(self, x, level):
            if not x: return "{}"

            if level <= 0: return "{...}"

            iter_keys = self._to_shorted_list(x, self.maxdict, sort=PY2)
            iter_x = self._make_pretty_items(x, iter_keys, '{', '}')
            return self._repr_iterable(iter_x, level, '{', '}')

        repr_RevertableDict = repr_dict

        def repr_defaultdict(self, x, level):
            def_factory = x.default_factory
            def_factory = self.repr1(def_factory, level)
            left = "defaultdict(%s, {" % def_factory

            if not x: return left + "})"

            if level <= 0: return left + "...})"

            iter_keys = self._to_shorted_list(x, self.maxdict, sort=PY2)
            iter_x = self._make_pretty_items(x, iter_keys, left, '})')
            return self._repr_iterable(iter_x, level, left, '})')

        def repr_OrderedDict(self, x, level):
            if not x: return "OrderedDict()"

            if level <= 0: return "OrderedDict({...})"

            iter_keys = self._to_shorted_list(x, self.maxdict)
            iter_x = self._make_pretty_items(x, iter_keys, 'OrderedDict({', '})')
            return self._repr_iterable(iter_x, level, 'OrderedDict({', '})')

        def repr_dict_keys(self, x, level):
            if not x: return "dict_keys([])"

            if level <= 0: return "dict_keys([...])"

            iter_x = self._to_shorted_list(x, self.maxdict)
            return self._repr_iterable(iter_x, level, 'dict_keys([', '])')

        def repr_dict_values(self, x, level):
            if not x: return "dict_values([])"

            if level <= 0: return "dict_values([...])"

            iter_x = self._to_shorted_list(x, self.maxdict)
            return self._repr_iterable(iter_x, level, 'dict_values([', '])')

        def repr_dict_items(self, x, level):
            if not x: return "dict_items([])"

            if level <= 0: return "dict_items([...])"

            iter_x = self._to_shorted_list(x, self.maxdict)
            return self._repr_iterable(iter_x, level, 'dict_items([', '])')


        class _PrettyDictItem(object):
            """
            This class to store dictionary like key-value pairs
            to make pretty repr of this.
            """
            def __init__(self, key, value):
                self.key = key
                self.value = value

        def repr__PrettyDictItem(self, x, level):
            newlevel = level - 1
            key = self.repr1(x.key, newlevel)
            if x.value is self._ellipsis:
                value = x.value
            else:
                value = self.repr1(x.value, newlevel)
            return "%s: %s" % (key, value)

        def _make_pretty_items(self, x, iter_keys, left, right):
            ellipsis = self._ellipsis
            DictItem = self._PrettyDictItem
            iter_x = []
            for key in iter_keys:
                if key is ellipsis:
                    di = ellipsis
                elif x[key] is x:
                    di = DictItem(key, '%s%s%s' % (left, ellipsis, right))
                else:
                    di = DictItem(key, x[key])
                iter_x.append(di)
            return iter_x

        def _repr_iterable(self, iter_x, level, left, right):
            ellipsis = self._ellipsis
            newlevel = level - 1
            repr1 = self.repr1
            need_indent = False
            repr_len = 0
            rv = []
            for elem in iter_x:
                if elem is ellipsis:
                    rv.append(ellipsis)
                    continue

                e_repr = repr1(elem, newlevel)
                if "\n" in e_repr:
                    need_indent = True
                elif len(e_repr) > self.maxstring:
                    need_indent = True
                repr_len += len(e_repr)
                rv.append(e_repr)

            if repr_len > self.maxother:
                need_indent = True

            if not need_indent:
                return '%s%s%s' % (left, ", ".join(rv), right)

            indent = "    "
            sep = ",\n"
            result = ""
            for e_repr in rv:
                if '\n' in e_repr:
                    e_repr = e_repr.replace("\n", "\n    ")
                result += indent + e_repr + sep
            return '%s\n%s%s' % (left, result, right)

        def _to_shorted_list(self, x, maxlen, sort=False):
            """
            This function returns the list representation of `x`, where references
            to itself are replaced by an ellipsis, and also if the length of `x`
            is longer than `maxlen`, the values in the middle are replaced by
            an ellipsis. If `sort` is True, it also tries to sort the values.
            """
            # Since not all sequences of items can be sorted and comparison
            # functions may raise arbitrary exceptions, make an unsorted
            # sequence in that case.
            ellipsis = self._ellipsis
            iter_x = x
            if sort:
                try:
                    iter_x = sorted(iter_x)
                except Exception:
                    pass

            if not isinstance(x, (tuple, _list)):
                iter_x = list(iter_x)

            n = len(x)
            if n > maxlen:
                i = max(0, maxlen // 2)
                ellipsis_add = type(iter_x)([ellipsis])
                iter_x = iter_x[:i] + ellipsis_add + iter_x[n - i:]

            return [ellipsis if v is x else v for v in iter_x]

        def repr_Matrix(self, x, level):
            if level <= 0: return "Matrix([...])"

            rv = "Matrix(["

            for line in (
                [x.xdx, x.xdy, x.xdz, x.xdw],
                [x.ydx, x.ydy, x.ydz, x.ydw],
                [x.zdx, x.zdy, x.zdz, x.zdw],
                [x.wdx, x.wdy, x.wdz, x.wdw],
            ):
                rv += "\n    "

                for point in line:
                    rv += "{:10.7f}, ".format(point)

            return rv + "\n])"


    aRepr = PrettyRepr()
    aRepr.maxtuple = 20
    aRepr.maxlist = 20
    aRepr.maxarray = 20
    aRepr.maxdict = 10
    aRepr.maxset = 20
    aRepr.maxfrozenset = 20
    aRepr.maxstring = 60
    aRepr.maxother = 200

    traced_aRepr = PrettyRepr()
    traced_aRepr.maxtuple = 20
    traced_aRepr.maxlist = 20
    traced_aRepr.maxarray = 20
    traced_aRepr.maxdict = 10
    traced_aRepr.maxset = 20
    traced_aRepr.maxfrozenset = 20
    traced_aRepr.maxstring = 30
    traced_aRepr.maxother = 100

    # The list of traced expressions.
    class TracedExpressionsList(NoRollback, list):
        pass

    class BoundedList(list):
        """
        A list that's bounded at a certain size.
        """

        def __init__(self, size, lines=None):
            self.size = size
            self.lines = lines

        def append(self, value):
            super(BoundedList, self).append(value)

            while len(self) >= self.size:
                self.pop(0)

            if self.lines is not None:
                while (len(self) > 1) and (sum(i.lines for i in self) > self.lines):
                    self.pop(0)

        def clear(self):
            self[:] = [ ]

    class ConsoleHistoryEntry(object):
        """
        Represents an entry in the history list.
        """

        lines = 0

        def __init__(self, command, result=None, is_error=False):
            self.command = command
            self.result = result
            self.is_error = is_error

        def update_lines(self):

            if self.result is None:
                return

            lines = self.result.split("\n")
            lines = lines[-config.console_history_lines:]
            self.result = "\n".join(lines)
            self.lines = len(lines)

    HistoryEntry = ConsoleHistoryEntry


    stdio_lines = _list()

    def stdout_line(l):
        if not (config.console or config.developer):
            return

        stdio_lines.append((False, l))

        while len(stdio_lines) > config.console_history_lines:
            stdio_lines.pop(0)

    def stderr_line(l):
        if not (config.console or config.developer):
            return

        stdio_lines.append((True, l))

        while len(stdio_lines) > config.console_history_lines:
            stdio_lines.pop(0)


    config.stdout_callbacks.append(stdout_line)
    config.stderr_callbacks.append(stderr_line)


    class ScriptErrorHandler(object):
        """
        Handles error in Ren'Py script.
        """

        def __init__(self):
            self.target_depth = renpy.call_stack_depth()

        def __call__(self, short, full, traceback_fn):
            he = console.history[-1]
            he.result = short.split("\n")[-2]
            he.is_error = True

            while renpy.call_stack_depth() > self.target_depth:
                renpy.pop_call()

            renpy.jump("_console")


    class DebugConsole(object):

        def __init__(self):

            self.history = BoundedList(config.console_history_size, config.console_history_lines + config.console_history_size)
            self.line_history = BoundedList(config.console_history_size)
            self.line_index = 0

            if persistent._console_history is not None:
                for i in persistent._console_history:
                    he = ConsoleHistoryEntry(i[0], i[1], i[2])
                    he.update_lines()
                    self.history.append(he)

            if persistent._console_line_history is not None:
                self.line_history.extend(persistent._console_line_history)

            self.first_time = True

            self.reset()

        def backup(self):

            persistent._console_history = [ (i.command, i.result, i.is_error) for i in self.history ]
            persistent._console_line_history = list(self.line_history)

        def start(self):
            he = ConsoleHistoryEntry(None)

            message = ""

            if self.first_time:
                message += __("Press <esc> to exit console. Type help for help.\n")
                self.first_time = False

            if self.can_renpy():
                message += __("Ren'Py script enabled.")
            else:
                message += __("Ren'Py script disabled.")

            he.result = message
            he.update_lines()
            self.history.append(he)

        def reset(self):

            # The list of lines that have been entered by the user, but not yet
            # processed.
            self.lines = [ "" ]
            self.line_index = len(self.line_history)

        def recall_line(self, offset):

            self.line_index += offset

            if self.line_index < 0:
                self.line_index = 0

            if self.line_index > len(self.line_history):
                self.line_index = len(self.line_history)

            if self.line_index == len(self.line_history):
                self.lines = [ "" ]
            else:
                self.lines = list(self.line_history[self.line_index])

            renpy.jump("_console")

        def older(self):
            self.recall_line(-1)

        def newer(self):
            self.recall_line(1)

        def interact(self):

            self.show_stdio()

            def get_indent(s):
                """
                Computes the indentation for the line following line s.
                """

                rv = ""

                for i in s:
                    if i == " ":
                        rv += " "
                    else:
                        break

                if s.rstrip().endswith(":"):
                    rv += "    "

                if not s.rstrip():
                    rv = rv[:-4]

                return rv

            renpy.ui.reset()

            renpy.game.context().exception_handler = None

            renpy.show_screen("_console", lines=self.lines[:-1], default=self.lines[-1], history=self.history, _transient=True)
            line = ui.interact()

            self.lines.pop()
            self.lines.append(line)

            indent = get_indent(line)
            if indent:
                self.lines.append(indent)
                return

            lines = self.lines
            self.line_history.append(lines)

            self.reset()

            if config.console_callback is not None:
                lines = config.console_callback(lines)

                if not lines:
                    return

            try:
                self.run(lines)
            finally:
                self.backup()

        def show_stdio(self):

            old_entry = None

            if persistent._console_short:
                if len(stdio_lines) > 30:
                    stdio_lines[:] = stdio_lines[:10] + [ (False, " ... ") ] + stdio_lines[-20:]

            for error, l in stdio_lines:
                if persistent._console_short:
                    if len(l) > 200:
                        l = l[:100] + "..." + l[-100:]

                if (old_entry is not None) and (error == old_entry.is_error):
                    old_entry.result += "\n" + l
                else:
                    e = ConsoleHistoryEntry(None, l, error)
                    e.update_lines()
                    self.history.append(e)
                    old_entry = e

            if old_entry is not None:
                old_entry.update_lines()

            stdio_lines[:] = _list()

        def can_renpy(self):
            """
            Returns true if we can run Ren'Py code.
            """

            return renpy.game.context().rollback

        def format_exception(self):
            etype, evalue, etb = sys.exc_info()
            return traceback.format_exception_only(etype, evalue)[-1]

        def run(self, lines):

            line_count = len(lines)
            code = "\n".join(lines)

            he = ConsoleHistoryEntry(code)
            self.history.append(he)

            try:

                # If we have 1 line, try to parse it as a command.
                if line_count == 1:
                    block = [ ( "<console>", 1, code, [ ]) ]
                    l = renpy.parser.Lexer(block)
                    l.advance()

                    # Command can be None, but that's okay, since the lookup will fail.
                    command = l.word()

                    command_fn = config.console_commands.get(command, None)

                    if command_fn is not None:
                        he.result = command_fn(l)
                        he.update_lines()
                        return

                error = None

                # Try to run it as Ren'Py.
                if self.can_renpy():

                    # TODO: Can we run Ren'Py code?
                    name = renpy.load_string(code + "\nreturn")

                    if name is not None:
                        renpy.game.context().exception_handler = ScriptErrorHandler()
                        renpy.call(name)
                    else:
                        error = "\n\n".join(renpy.get_parse_errors())

                # Try to eval it.
                try:
                    renpy.python.py_compile(code, 'eval')
                except Exception:
                    pass
                else:
                    result = renpy.python.py_eval(code)
                    if persistent._console_short:
                        he.result = aRepr.repr(result)
                    else:
                        he.result = repr(result)

                    he.update_lines()
                    return

                # Try to exec it.
                try:
                    renpy.python.py_compile(code, "exec")
                except Exception:
                    if error is None:
                        error = self.format_exception()
                else:
                    renpy.python.py_exec(code)
                    return

                if error is not None:
                    he.result = error
                    he.update_lines()
                    he.is_error = True

            except renpy.game.CONTROL_EXCEPTIONS:
                raise

            except Exception:
                import traceback
                traceback.print_exc()

                he.result = self.format_exception().rstrip()
                he.update_lines()
                he.is_error = True


    console = None

    def enter():
        """
        Called to enter the debug console.
        """

        if console is None:
            return

        console.start()

        if renpy.game.context().rollback:
            try:
                renpy.rollback(checkpoints=0, force=True, greedy=False, current_label="_console")
            except renpy.game.CONTROL_EXCEPTIONS:
                raise
            except Exception:
                pass

        renpy.call_in_new_context("_console")

# Has to run after 00library.
init 1701 python in _console:

    if config.developer or config.console:
        console = DebugConsole()

init -1500 python in _console:

    def command(help=None):
        def wrap(f):
            f.help = help
            config.console_commands[f.__name__] = f
            return f

        return wrap

    @command(_("help: show this help"))
    def help(l, doc_generate=False):
        keys = list(config.console_commands.keys())
        keys.sort()

        rv = __("commands:\n")

        for k in keys:
            f = config.console_commands[k]
            if f.help is None:
                continue

            rv += " " + __(f.help) + "\n"

        if console.can_renpy() or doc_generate:
            rv += __(" <renpy script statement>: run the statement\n")

        rv += __(" <python expression or statement>: run the expression or statement")

        return rv

    @command()
    def halp(l):
        return help(l).replace("e", "a")

    @command(_("clear: clear the console history"))
    def clear(l):
        console.history[:] = [ ]

    @command(_("exit: exit the console"))
    def exit(l):
        renpy.jump("_console_return")

    @command()
    def quit(l):
        renpy.jump("_console_return")

    @command(_("stack: print the return stack"))
    def stack(l):
        def fmt(entry):
            if isinstance(entry, str):
                name = entry
            else:
                name = "(anonymous)"
            try:
                lkp = renpy.game.script.lookup(entry)
                filename, linenumber = lkp.filename, lkp.linenumber
            except Exception:
                filename = linenumber = "?"
            return "{} <{}:{}>".format(name, filename, linenumber)

        rs = renpy.exports.get_return_stack()
        if rs:
            print("Return stack (most recent call last):\n")
            for entry in rs:
                print(fmt(entry))
        else:
            print("The return stack is empty.")

    @command(_("load <slot>: loads the game from slot"))
    def load(l):
        name = l.rest().strip()

        if not name:
            raise Exception("Slot name must not be empty")

        try:
            renpy.load(name)
        finally:
            console.history[-1].result = "Loading slot {!r}.".format(name)


    @command(_("save <slot>: saves the game in slot"))
    def save(l):
        name = l.rest().strip()

        if not name:
            raise Exception("Slot name must not be empty")

        renpy.save(name)

        return "Saved slot {!r}.".format(name)

    @command(_("reload: reloads the game, refreshing the scripts"))
    def reload(l):
        store._reload_game()

    @command()
    def R(l):
        store._reload_game()

    @command(_("watch <expression>: watch a python expression\n watch short: makes the representation of traced expressions short (default)\n watch long: makes the representation of traced expressions as is"))
    def watch(l):
        expr = l.rest()
        expr = expr.strip()

        if expr == "short":
            persistent._console_traced_short = True
            return

        if expr == "long":
            persistent._console_traced_short = False
            return

        renpy.python.py_compile(expr, 'eval')

        traced_expressions.append(expr)

        if "_trace_screen" not in config.always_shown_screens:
            config.always_shown_screens.append("_trace_screen")

    def renpy_watch(expr):
        """
        :name: renpy.watch
        :doc: debug

        This watches the given Python expression, by displaying it in the
        upper-right corner of the screen.
        """

        block = [ ( "<console>", 1, expr, [ ]) ]

        l = renpy.parser.Lexer(block)
        l.advance()
        watch(l)

    renpy.watch = renpy_watch

    @command(_("unwatch <expression>: stop watching an expression"))
    def unwatch(l):
        expr = l.rest()
        expr = expr.strip()

        if expr == "all":
            renpy_unwatchall()
            return

        if expr in traced_expressions:
            traced_expressions.remove(expr)

        if not traced_expressions:

            if "_trace_screen" in renpy.config.always_shown_screens:
                config.always_shown_screens.remove("_trace_screen")

            renpy.hide_screen("_trace_screen")


    def watch_after_load():
        try:
            if config.developer and traced_expressions:
                renpy.show_screen("_trace_screen")
        except Exception:
            pass

    config.after_load_callbacks.append(watch_after_load)

    def renpy_unwatch(expr):
        """
        :name: renpy.unwatch
        :doc: debug

        Stops watching the given Python expression.
        """

        block = [ ( "<console>", 1, expr, [ ]) ]

        l = renpy.parser.Lexer(block)
        l.advance()
        unwatch(l)

    renpy.unwatch = renpy_unwatch


    @command(_("unwatchall: stop watching all expressions"))
    def unwatchall(l):
        traced_expressions[:] = [ ]

        if "_trace_screen" in renpy.config.always_shown_screens:
            config.always_shown_screens.remove("_trace_screen")

        renpy.hide_screen("_trace_screen")

    def renpy_unwatchall():
        """
        :name: renpy.unwatch
        :doc: debug

        Stops watching all Python expressions.
        """

        unwatchall(None)

    renpy.unwatchall = renpy_unwatchall

    @command(_("jump <label>: jumps to label"))
    def jump(l):
        label = l.label_name()

        if label is None:
            raise Exception("Could not parse label. (Unqualified local labels are not allowed.)")

        if not console.can_renpy():
            raise Exception("Ren'Py script not enabled. Not jumping.")

        if not renpy.has_label(label):
            raise Exception("Label %s not found." % label)

        renpy.pop_call()
        renpy.jump(label)

    @command(_("short: Shorten the representation of objects on the console (default)."))
    def short(l):
        persistent._console_short = True

    @command(_("long: Print the full representation of objects on the console."))
    def long(l):
        persistent._console_short = False

    @command(_("escape: Enables escaping of unicode symbols in unicode strings."))
    def escape(l):
        persistent._console_unicode_escaping = True

    @command(_("unescape: Disables escaping of unicode symbols in unicode strings and print it as is (default)."))
    def unescape(l):
        persistent._console_unicode_escaping = False


screen _console:
    # This screen takes as arguments:
    #
    # lines
    #    The current set of lines in the input buffer.
    # indent
    #    Indentation to apply to the new line.
    # history
    #    A list of command, result, is_error tuples.
    zorder 1500
    modal True

    if not _console.console.can_renpy():
        frame:
            style "_console_backdrop"

    frame:
        style "_console"

        has viewport:
            style_prefix "_console"
            mousewheel True
            scrollbars "vertical"
            yinitial 1.0

        has vbox

        # Draw historical console input.

        frame style "_console_history":

            has vbox:
                xfill True

            for he in history:

                frame style "_console_history_item":
                    has vbox

                    if he.command is not None:
                        frame style "_console_command":
                            xfill True
                            text "[he.command!q]" style "_console_command_text"

                    if he.result is not None:

                        frame style "_console_result":
                            if he.is_error:
                                text "[he.result!q]" style "_console_error_text"
                            else:
                                text "[he.result!q]" style "_console_result_text"

        # Draw the current input.
        frame style "_console_input":

            has vbox

            for line in lines:
                hbox:
                    spacing 4

                    if line[:1] != " ":
                        text "> " style "_console_prompt"
                    else:
                        text "... " style "_console_prompt"

                    text "[line!q]" style "_console_input_text"

            hbox:
                spacing 4

                if default[:1] != " ":
                    text "> " style "_console_prompt"
                else:
                    text "... " style "_console_prompt"

                input default default style "_console_input_text" exclude "" copypaste True


    key "game_menu" action Jump("_console_return")
    key "console_older" action _console.console.older
    key "console_newer" action _console.console.newer

default _console.traced_expressions = _console.TracedExpressionsList()

screen _trace_screen():

    zorder 1501

    if _console.traced_expressions:

        frame style "_console_trace":

            vbox:

                for expr in _console.traced_expressions:
                    python:
                        if persistent._console_traced_short:
                            repr_func = _console.traced_aRepr.repr
                        else:
                            repr_func = repr

                        try:
                            value = repr_func(eval(expr))
                        except Exception:
                            value = "eval failed"
                        del repr_func

                    hbox:
                        text "[expr!q]: " style "_console_trace_var"
                        text "[value!q]" style "_console_trace_value"

# The label that is called by _console.enter to actually run the console.
# This can be called in the current context (for normal Ren'Py code) or
# in a new context (in menus).
label _console:

    while True:
        python in _console:
            try:
                console.interact()
            finally:
                renpy.game.context().force_checkpoint = True
                renpy.exports.checkpoint(hard="not_greedy")

label _console_return:
    return

init -1010 python:
    config.per_frame_screens.append("_trace_screen")
