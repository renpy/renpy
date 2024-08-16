
# Copyright 2004-2024 Tom Rothamel <pytom@bishoujo.us>
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

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode # *

from itertools import chain as _chain
import collections

import renpy


class Parameter(object):
    """
    The default value (if any) of this class of parameters is a string,
    evaluable to the actual default value. This is how most Ren'Py callables
    work (labels, transforms directly defined using the transform statement,
    and screens), where the actual value is computed at the time of the call.
    """

    __slots__ = ("name", "kind", "default",)

    POSITIONAL_ONLY, POSITIONAL_OR_KEYWORD, VAR_POSITIONAL, KEYWORD_ONLY, VAR_KEYWORD = range(5)

    empty = None

    def __init__(self, name, kind, default=empty):
        # default should only be passed by keyword, todo when PY3-only
        self.name = name
        self.kind = kind
        self.default = default

    @property
    def has_default(self):
        return self.default is not self.empty

    def default_value(self, locals=None, globals=None):
        return renpy.python.py_eval(self.default, locals=locals, globals=globals)

    def replace(self, **kwargs):
        d = dict(name=self.name, kind=self.kind, default=self.default)
        d.update(kwargs)
        return type(self)(**d)

    def __str__(self):
        kind = self.kind
        formatted = self.name

        if kind == self.VAR_POSITIONAL:
            formatted = "*" + formatted
        elif kind == self.VAR_KEYWORD:
            formatted = "**" + formatted
        elif self.default is not self.empty:
            formatted += "=" + self.default # type: ignore

        return formatted

    def __repr__(self):
        return "<Parameter {}>".format(self)

    def __eq__(self, other):
        return (self is other) or (isinstance(other, Parameter) and (self.name == other.name) and (self.kind == other.kind) and (self.default == other.default))

class ValuedParameter(Parameter):
    """
    This is a more python-classic parameter, in which the default value is the
    final object itself, already evaluated.
    """

    __slots__ = ()

    class empty: pass # singleton, should be picklable

    def __init__(self, name, kind, default=empty):
        # default should only be passed by keyword, todo when PY3-only
        # this method is redefined in order to change default's default value
        super(ValuedParameter, self).__init__(name, kind, default)

    def default_value(self, *args, **kwargs):
        return self.default

    def __str__(self):
        kind = self.kind
        formatted = self.name

        if kind == self.VAR_POSITIONAL:
            formatted = "*" + formatted
        elif kind == self.VAR_KEYWORD:
            formatted = "**" + formatted
        elif self.default is not self.empty:
            formatted = "{}={!r}".format(formatted, self.default)

        return formatted

class Signature(object):
    """
    This class is used to store information about parameters (to a label, screen, ATL...)
    It has the same interface as inspect.Signature for the most part.
    """

    __slots__ = ("parameters",)

    def __init__(self, parameters=None):
        if parameters is None:
            self.parameters = {}
        else:
            # when in PY3-only, turn this into MappingProxyType o dict
            self.parameters = collections.OrderedDict((param.name, param) for param in parameters)

    @staticmethod
    def legacy_params(parameters, positional, extrapos, extrakw, last_posonly=None, first_kwonly=None):
        """
        Creates a list of Parameter from the legacy parameters format.

        `parameters` is a list of (name, default) pairs, where default is None
        for required parameters and a string for optional parameters.
        `positional` is a list of parameter names that are either
        positional-only or positional-or-keyword.
        `extrapos` is None or the name of the parameter that collects extra positional, like *args.
        `extrakw` is None or the name of the parameter that collects extra keyword arguments, like **kwargs.
        `last_posonly` is the name of the last positional-only parameter.
        `first_kwonly` is the name of the first keyword-only parameter.
        """

        pars = []
        posonly_found = (last_posonly is None)
        now_kw_only = False

        # long-time nonsense in atl.py
        if (not parameters) and positional:
            parameters = [(name, Parameter.empty) for name in positional]

        for name, default in parameters:
            if name == first_kwonly:
                now_kw_only = True
                if extrapos is not None:
                    pars.append(Parameter(extrapos, Parameter.VAR_POSITIONAL))

            if now_kw_only:
                kind = Parameter.KEYWORD_ONLY
            elif not posonly_found:
                kind = Parameter.POSITIONAL_ONLY
            else:
                kind = Parameter.POSITIONAL_OR_KEYWORD

            pars.append(Parameter(name, kind, default=default or Parameter.empty))

            if name == last_posonly:
                posonly_found = True

        if (not now_kw_only) and (extrapos is not None):
            pars.append(Parameter(extrapos, Parameter.VAR_POSITIONAL))

        if extrakw is not None:
            pars.append(Parameter(extrakw, Parameter.VAR_KEYWORD))

        return pars


    def __setstate__(self, state):
        if isinstance(state, dict):
            # legacy state
            positional_only = state.get("positional_only", [ ])
            last_posonly = positional_only[-1][0] if positional_only else None
            keyword_only = state.get("keyword_only", [ ])
            first_kwonly = keyword_only[0][0] if keyword_only else None
            self.__init__(self.legacy_params(state["parameters"], state["positional"], state["extrapos"], state["extrakw"], last_posonly, first_kwonly))
        else:
            # default behavior on py3, could be a super() call but this is faster and py2-compatible
            self.parameters = state[1]["parameters"]

    def apply_defaults(self, mapp, scope=None):
        """
        From a mapping representing the inner scope of the callable after binding,
        this mutates the mapping to apply the evaluated default values of the parameters.
        This is where the evaluation of the default values occurs.
        Evaluation occurs lazily : the default value of parameters already passed
        is not calculated.
        """
        # code inspired from stdlib's inspect.BoundArguments.apply_defaults
        # but optimized as to mutate the dict in-place
        # (because ordering doesn't matter to us)
        # resulting in 5x shorter execution time
        for name, param in self.parameters.items():
            if name not in mapp:
                if param.has_default:
                    val = param.default_value(locals=scope)
                elif param.kind == param.VAR_POSITIONAL:
                    val = ()
                elif param.kind == param.VAR_KEYWORD:
                    val = renpy.python.RevertableDict()
                else:
                    # result of a partial bind
                    continue
                mapp[name] = val

    def with_pos_only_as_pos_or_kw(self):
        """
        Returns a new Signature object where positional-only parameters are
        turned into positional-or-keyword parameters.
        """
        new_params = []
        itparams = iter(self.parameters.values())
        for param in itparams:
            if param.kind == Parameter.POSITIONAL_ONLY:
                new_params.append(param.replace(kind=Parameter.POSITIONAL_OR_KEYWORD))
            else:
                new_params.append(param)
                new_params.extend(itparams)
                break
        return Signature(new_params)

    def apply(self, args, kwargs, ignore_errors=False, partial=False, apply_defaults=True):
        """
        Takes args and kwargs, and returns a mapping corresponding to the
        inner scope of the callable as a result of that call.

        Improvements on the original inspect.Signature._bind :
        - manages _ignore_extra_kwargs (near the end of the method)
        - avoids creating a BoundArguments object, just returns the scope dict
        - ignore_errors
        - applies the defaults automatically (and lazily, as per the above)
        """

        # when in PY3-only, uncomment the "from None" in the raise statements

        if not renpy.config.developer:
            ignore_errors = True

        kwargs = dict(kwargs)

        def _raise(exct, msg, *argz, **kwargz):
            if not ignore_errors:
                raise exct(msg.format(*argz, **kwargz)) # from None

        # code mostly taken from stdlib's inspect.Signature._bind
        arguments = {}

        parameters = iter(self.parameters.values())
        parameters_ex = ()
        arg_vals = iter(args)

        while True:
            # Let's iterate through the positional arguments and corresponding
            # parameters
            try:
                arg_val = next(arg_vals)
            except StopIteration:
                # No more positional arguments
                try:
                    param = next(parameters)
                except StopIteration:
                    # No more parameters. That's it. Just need to check that
                    # we have no `kwargs` after this while loop
                    break
                else:
                    if param.kind == param.VAR_POSITIONAL:
                        # That's OK, just empty *args.  Let's start parsing
                        # kwargs
                        break
                    elif param.name in kwargs:
                        if param.kind == param.POSITIONAL_ONLY:
                            _raise(TypeError,
                                "{arg!r} parameter is positional only, but was passed as a keyword",
                                arg=param.name)
                        parameters_ex = (param,)
                        break
                    elif (param.kind == param.VAR_KEYWORD or
                                                param.default is not param.empty):
                        # That's fine too - we have a default value for this
                        # parameter.  So, lets start parsing `kwargs`, starting
                        # with the current parameter
                        parameters_ex = (param,)
                        break
                    else:
                        # No default, not VAR_KEYWORD, not VAR_POSITIONAL,
                        # not in `kwargs`
                        if partial or ignore_errors:
                            parameters_ex = (param,)
                            break
                        else:
                            if param.kind == param.KEYWORD_ONLY:
                                argtype = ' keyword-only'
                            else:
                                argtype = ''
                            msg = 'missing a required{argtype} argument: {arg!r}'
                            msg = msg.format(arg=param.name, argtype=argtype)
                            raise TypeError(msg) # from None
            else:
                # We have a positional argument to process
                try:
                    param = next(parameters)
                except StopIteration:
                    _raise(TypeError, 'too many positional arguments')
                    break
                else:
                    if param.kind in (param.VAR_KEYWORD, param.KEYWORD_ONLY):
                        # Looks like we have no parameter for this positional
                        # argument
                        _raise(TypeError, 'too many positional arguments')
                        break

                    if param.kind == param.VAR_POSITIONAL:
                        # We have an '*args'-like argument, let's fill it with
                        # all positional arguments we have left and move on to
                        # the next phase
                        values = [arg_val]
                        values.extend(arg_vals)
                        arguments[param.name] = tuple(values)
                        break

                    if param.name in kwargs and param.kind != param.POSITIONAL_ONLY:
                        _raise(TypeError,
                            'multiple values for argument {arg!r}',
                            arg=param.name)
                        break

                    arguments[param.name] = arg_val

        # Now, we iterate through the remaining parameters to process
        # keyword arguments
        kwargs_param = None
        for param in _chain(parameters_ex, parameters):
            if param.kind == param.VAR_KEYWORD:
                # Memorize that we have a '**kwargs'-like parameter
                kwargs_param = param
                continue

            if param.kind == param.VAR_POSITIONAL:
                # Named arguments don't refer to '*args'-like parameters.
                # We only arrive here if the positional arguments ended
                # before reaching the last parameter before *args.
                continue

            param_name = param.name
            try:
                arg_val = kwargs.pop(param_name)
            except KeyError:
                # We have no value for this parameter.  It's fine though,
                # if it has a default value, or it is an '*args'-like
                # parameter, left alone by the processing of positional
                # arguments.
                if (not (partial or ignore_errors) and param.kind != param.VAR_POSITIONAL and
                                                    param.default is param.empty):
                    raise TypeError('missing a required argument: {arg!r}'. \
                                    format(arg=param_name)) # from None

            else:
                if param.kind == param.POSITIONAL_ONLY:
                    # This should never happen in case of a properly built
                    # Signature object (but let's have this check here
                    # to ensure correct behaviour just in case)
                    _raise(TypeError,
                        "{arg!r} parameter is positional only, but was passed as a keyword",
                        arg=param.name)
                    continue

                arguments[param_name] = arg_val

        if kwargs:
            if kwargs_param is not None:
                # Process our '**kwargs'-like parameter
                arguments[kwargs_param.name] = kwargs
            elif not (ignore_errors or kwargs.pop('_ignore_extra_kwargs', False)):
                raise TypeError(
                    'got an unexpected keyword argument {arg!r}'.format(
                        arg=next(iter(kwargs))))

        if apply_defaults:
            self.apply_defaults(arguments)
        return arguments

    def __eq__(self, other):
        if self is other:
            return True
        if not isinstance(other, Signature):
            return False

        return tuple(self.parameters.values()) == tuple(other.parameters.values())

    def __str__(self):
        result = []
        render_pos_only_separator = False
        render_kw_only_separator = True
        for param in self.parameters.values():
            formatted = str(param)

            kind = param.kind

            if kind == Parameter.POSITIONAL_ONLY:
                render_pos_only_separator = True
            elif render_pos_only_separator:
                # It's not a positional-only parameter, and the flag
                # is set to 'True' (there were pos-only params before.)
                result.append('/')
                render_pos_only_separator = False

            if kind == Parameter.VAR_POSITIONAL:
                # OK, we have an '*args'-like parameter, so we won't need
                # a '*' to separate keyword-only arguments
                render_kw_only_separator = False
            elif kind == Parameter.KEYWORD_ONLY and render_kw_only_separator:
                # We have a keyword-only parameter to render and we haven't
                # rendered an '*args'-like parameter before, so add a '*'
                # separator to the parameters list ("foo(arg1, *, arg2)" case)
                result.append('*')
                # This condition should be only triggered once, so
                # reset the flag
                render_kw_only_separator = False

            result.append(formatted)

        if render_pos_only_separator:
            # There were only positional-only parameters, hence the
            # flag was not reset to 'False'
            result.append('/')

        return "({})".format(", ".join(result))

    def __repr__(self):
        return "<Signature {}>".format(self)

ParameterInfo = Signature

def apply_arguments(parameters, args, kwargs, ignore_errors=False):

    if not renpy.config.developer:
        ignore_errors = True

    if parameters is None:
        if (args or kwargs) and not ignore_errors:
            raise Exception("Arguments supplied, but parameter list not present")
        else:
            return { }

    return parameters.apply(args or (), kwargs or {}, ignore_errors)


class ArgumentInfo(renpy.object.Object):

    __version__ = 1
    starred_indexes = set()
    doublestarred_indexes = set()

    def after_upgrade(self, version):
        if version < 1:
            arguments = self.arguments
            extrapos = self.extrapos # type: ignore
            extrakw = self.extrakw # type: ignore
            length = len(arguments) + bool(extrapos) + bool(extrakw)
            if extrapos:
                self.starred_indexes = { length - 1 }
                arguments.append((None, extrapos))

            if extrakw:
                self.doublestarred_indexes = { length - 1 }
                arguments.append((None, extrakw))

            if extrapos and extrakw:
                self.starred_indexes = { length - 2 }

    def __init__(self, arguments, starred_indexes=None, doublestarred_indexes=None):

        # A list of (keyword, expression) pairs.
        # If the keyword is None, the argument is thought of as positional.
        self.arguments = arguments

        # Indexes of arguments to be considered as * unpacking
        self.starred_indexes = starred_indexes or set()

        # Indexes of arguments to be considered as ** unpacking.
        self.doublestarred_indexes = doublestarred_indexes or set()

    def evaluate(self, scope=None):
        """
        Evaluates the arguments, returning a tuple of arguments and a
        dictionary of keyword arguments.
        """

        args = [ ]
        kwargs = renpy.revertable.RevertableDict()

        for i, (k, v) in enumerate(self.arguments):
            value = renpy.python.py_eval(v, locals=scope)

            if i in self.starred_indexes:
                args.extend(value)

            elif i in self.doublestarred_indexes:
                kwargs.update(value)

            elif k is not None:
                kwargs[k] = value
            else:
                args.append(value)

        return tuple(args), kwargs

    def get_code(self):

        l = [ ]

        for i, (keyword, expression) in enumerate(self.arguments):

            if i in self.starred_indexes:
                l.append("*" + expression)

            elif i in self.doublestarred_indexes:
                l.append("**" + expression)

            elif keyword is not None:
                l.append("{}={}".format(keyword, expression))
            else:
                l.append(expression)

        return "(" + ", ".join(l) + ")"

    __str__ = get_code

    def __repr__(self):
        return "<ArgumentInfo {}>".format(self)


EMPTY_PARAMETERS = Signature()
EMPTY_ARGUMENTS = ArgumentInfo([ ], None, None)
