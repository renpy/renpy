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
    """Exercise expression interpolation with its configuration restored after each test."""

    mocker.patch.object(renpy.config, "interpolate_exprs", True)


@pytest.mark.parametrize("value", [0, False, None, "", 42, "text"])
def test_layered_scope_preserves_first_value(value):
    """A present false-valued local wins over the same name in an outer mapping."""

    scope = collections.ChainMap({"item": value}, {"item": "outer"})
    assert substitutions.interpolate("Item [item]", scope) == "Item " + format(value)


def test_layered_scope_avoids_generator_membership(mocker):
    """Ordinary layered scopes do not need the standard generator-based contains implementation."""

    contains = mocker.spy(collections.ChainMap, "__contains__")
    scope = collections.ChainMap({"item": 42}, {})
    assert substitutions.interpolate("Item [item]", scope) == "Item 42"
    contains.assert_not_called()


def test_layered_scope_keeps_mapping_callback_order():
    """Membership probes and subsequent value lookup keep their original order across mappings."""

    trace = []

    class TrackedMapping(dict):
        def __init__(self, name, values):
            super().__init__(values)
            self.name = name

        def __contains__(self, key):
            trace.append(("contains", self.name, key))
            return super().__contains__(key)

        def __getitem__(self, key):
            trace.append(("getitem", self.name, key))
            return super().__getitem__(key)

    scope = collections.ChainMap(TrackedMapping("local", {}), TrackedMapping("outer", {"item": 42}))
    assert substitutions.interpolate("Item [item]", scope) == "Item 42"
    assert trace == [
        ("contains", "local", "item"),
        ("contains", "outer", "item"),
        ("getitem", "local", "item"),
        ("getitem", "outer", "item"),
    ]


def test_layered_scope_short_circuits_on_first_hit():
    """A later custom mapping must not run its membership callback after an earlier match."""

    class UnusedMapping(dict):
        def __contains__(self, key):
            raise AssertionError("The local hit should stop the search")

    scope = collections.ChainMap({"item": 42}, UnusedMapping())
    assert substitutions.interpolate("Item [item]", scope) == "Item 42"


def test_chainmap_subclass_keeps_contains_override():
    """User subclasses retain their own membership behavior instead of using the built-in shortcut."""

    trace = []

    class CustomScope(collections.ChainMap):
        def __contains__(self, key):
            trace.append(key)
            return super().__contains__(key)

    assert substitutions.interpolate("[item]", CustomScope({"item": 42})) == "42"
    assert trace == ["item"]


def test_ordinary_mapping_keeps_contains_override():
    """The optimization does not bypass a non-ChainMap scope's membership callback."""

    trace = []

    class CustomScope(dict):
        def __contains__(self, key):
            trace.append(key)
            return super().__contains__(key)

    assert substitutions.interpolate("[item]", CustomScope(item=42)) == "42"
    assert trace == ["item"]


@pytest.mark.parametrize("error", [ValueError("membership failed"), StopIteration("membership stopped")])
def test_layered_scope_preserves_membership_exception(error):
    """Mapping errors propagate, including the RuntimeError conversion performed by the old generator."""

    class BrokenMapping(dict):
        def __contains__(self, key):
            raise error

    scope = collections.ChainMap(BrokenMapping())
    if isinstance(error, StopIteration):
        with pytest.raises(RuntimeError, match="generator raised StopIteration") as raised:
            substitutions.interpolate("[item]", scope)
        assert raised.value.__cause__ is error
    else:
        with pytest.raises(ValueError) as raised:
            substitutions.interpolate("[item]", scope)
        assert raised.value is error


def test_layered_scope_preserves_iterator_acquisition_error(mocker):
    """A StopIteration raised while obtaining the maps iterator is not a generator-body failure."""

    class BrokenMaps:
        def __iter__(self):
            raise StopIteration("cannot iterate maps")

    scope = collections.ChainMap()
    mocker.patch.object(scope, "maps", BrokenMaps())
    with pytest.raises(StopIteration, match="cannot iterate maps"):
        substitutions.interpolate("[item]", scope)


def test_layered_scope_keeps_dynamic_values_and_formatting():
    """Values and custom formatting are evaluated again instead of being cached across calls."""

    class Value:
        def __init__(self):
            self.calls = 0

        def __format__(self, spec):
            self.calls += 1
            return str(self.calls)

    value = Value()
    values: dict[str, object] = {"item": value}
    scope = collections.ChainMap(values)
    assert substitutions.interpolate("[item]", scope) == "1"
    assert substitutions.interpolate("[item]", scope) == "2"
    scope.maps[0]["item"] = 3
    assert substitutions.interpolate("[item]", scope) == "3"


def test_expression_observes_same_layered_scope_object():
    """Expression evaluation still receives the original ChainMap, rather than a replacement subclass."""

    scope = collections.ChainMap({"item": 41})
    assert substitutions.interpolate("[item + 1]", scope) == "42"
    assert substitutions.interpolate("[type(locals()).__name__]", scope) == "ChainMap"
