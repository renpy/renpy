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

import collections

import pytest

import renpy
from renpy import substitutions


@pytest.fixture(autouse=True)
def interpolate_expressions(mocker):
    """Enables expression interpolation for the duration of each test."""

    mocker.patch.object(renpy.config, "interpolate_exprs", True)


@pytest.mark.parametrize("value", [0, False, None, "", 42, "text"])
def test_first_mapping_wins(value):
    """A name in an earlier mapping shadows the same name later in the scope, even when its value is falsy."""

    scope = collections.ChainMap({"item": value}, {"item": "outer"})
    assert substitutions.interpolate("Item [item]", scope) == "Item " + format(value)


def test_name_from_later_mapping():
    """A name missing from earlier mappings is found in a later one."""

    scope = collections.ChainMap({}, {"item": 42})
    assert substitutions.interpolate("Item [item]", scope) == "Item 42"


def test_plain_dict_scope():
    """Scopes that are ordinary dicts work."""

    assert substitutions.interpolate("[item] [item + 1]", {"item": 41}) == "41 42"


def test_expressions_evaluate_in_scope():
    """Expressions that are not simple names are evaluated against the scope."""

    scope = collections.ChainMap({"item": 41}, {"offset": 1})
    assert substitutions.interpolate("[item + offset]", scope) == "42"
    assert substitutions.interpolate("[type(locals()).__name__]", scope) == "ChainMap"


def test_builtin_names_evaluate():
    """A simple name absent from the scope falls back to evaluation, which finds builtins."""

    assert substitutions.interpolate("[None] [True]", {}) == "None True"


def test_missing_name_raises():
    """A simple name that cannot be found anywhere raises NameError."""

    with pytest.raises(NameError):
        substitutions.interpolate("[missing]", collections.ChainMap({}, {}))


def test_missing_name_fallback(mocker):
    """In fallback mode, a field that fails to evaluate still raises the evaluation error."""

    mocker.patch.object(renpy.config, "interpolate_exprs", "fallback")

    with pytest.raises(NameError):
        substitutions.interpolate("[missing]", {})


def test_scope_subclass_lookup_is_honored():
    """A scope whose __getitem__ computes values is consulted for simple names."""

    class ComputedScope(dict):
        def __getitem__(self, key):
            if key == "item":
                return 42

            return super().__getitem__(key)

    assert substitutions.interpolate("[item]", ComputedScope()) == "42"


def test_scope_lookup_errors_propagate():
    """Errors other than KeyError raised by the scope are not swallowed."""

    class BrokenScope(dict):
        def __getitem__(self, key):
            raise ValueError("lookup failed")

    with pytest.raises(ValueError, match="lookup failed"):
        substitutions.interpolate("[item]", BrokenScope())


def test_values_are_not_cached():
    """Values are looked up and formatted on every call, so changes to the scope are seen."""

    class Counter:
        def __init__(self):
            self.calls = 0

        def __format__(self, spec):
            self.calls += 1
            return str(self.calls)

    values: dict[str, object] = {"item": Counter()}
    scope = collections.ChainMap(values)

    assert substitutions.interpolate("[item]", scope) == "1"
    assert substitutions.interpolate("[item]", scope) == "2"

    values["item"] = 3
    assert substitutions.interpolate("[item]", scope) == "3"


def test_conversion_and_format_spec():
    """Conversions and format specs apply to values found by simple-name lookup."""

    scope = collections.ChainMap({"item": "x", "number": 3.14159})
    assert substitutions.interpolate("[item!r] [number:.2f] [item=]", scope) == "'x' 3.14 item='x'"
