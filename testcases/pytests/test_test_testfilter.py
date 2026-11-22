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

import pytest

from renpy.test import testfilter


@pytest.mark.parametrize(
    ("text", "name", "parameters"),
    [
        ("coordinates", "coordinates", {}),
        ("screens(kind='load')", "screens", {"kind": "load"}),
        ("coordinates(point=(5, 5))", "coordinates", {"point": (5, 5)}),
        ("nested(value=((1, 2), (3,)))", "nested", {"value": ((1, 2), (3,))}),
        ("listed(value=[(1, 2)], other=3)", "listed", {"value": [(1, 2)], "other": 3}),
        ("case(s='a).b(')", "case", {"s": "a).b("}),
        ('case(s="it\'s (")', "case", {"s": "it's ("}),
        ("case(s='\\')(')", "case", {"s": "')("}),
    ],
)
def test_segment_parses_parameters(text, name, parameters):
    """
    A filter segment yields its name and literal keyword parameters, even when a value's repr contains
    parentheses, as tuples and some strings do (#7543). The segment's own closing parenthesis must not be
    confused with one belonging to a value.
    """

    segment = testfilter.TestFilterSegment(text)

    assert segment.name == name
    assert segment.parameters == parameters


@pytest.mark.parametrize(
    ("raw", "segments"),
    [
        ("repro.coordinates(point=(5, 5))", [("repro", {}), ("coordinates", {"point": (5, 5)})]),
        ("repro.case(s='(').other", [("repro", {}), ("case", {"s": "("}), ("other", {})]),
        ("repro.case(s='a.b)').other", [("repro", {}), ("case", {"s": "a.b)"}), ("other", {})]),
        ('repro.case(s="\\".)").other', [("repro", {}), ("case", {"s": '".)'}), ("other", {})]),
        ('repro.case(s="""a"b.(""").other', [("repro", {}), ("case", {"s": 'a"b.('}), ("other", {})]),
        ("repro.case(s='').other", [("repro", {}), ("case", {"s": ""}), ("other", {})]),
    ],
)
def test_filter_splits_outside_strings(raw, segments):
    """
    Filters split into segments only at dots outside parentheses and string literals, so string parameter
    values containing dots or unbalanced parentheses do not break the filter. The global suite is prepended
    because generated testcase paths always start with it.
    """

    test_filter = testfilter.TestFilter(raw)

    assert [(s.name, s.parameters) for s in test_filter.segments] == [("global", {})] + segments


@pytest.mark.parametrize(
    ("raw", "path", "expected"),
    [
        ("repro", "global.repro.coordinates(point=(5, 5))", True),
        ("repro.coordinates(point=(5, 5))", "global.repro.coordinates(point=(5, 5))", True),
        ("repro.coordinates(point=(5, 6))", "global.repro.coordinates(point=(5, 5))", False),
        ("repro", "global.repro.case(s='(')", True),
        ("repro.case(s='(')", "global.repro.case(s=')')", False),
    ],
)
def test_filter_matches_parameterized_path(raw, path, expected):
    """
    A user filter matches the generated path of a parameterized testcase, which is how `test <filter>`
    selects testcases. Filtering by suite name alone failed with a tuple parameter (#7543).
    """

    assert testfilter.TestFilter(raw).matches(testfilter.TestFilter(path)) is expected


@pytest.mark.parametrize(
    "raw",
    [
        "repro.case(x=1)y",
        "repro.case(x=1)(y=2)",
        "repro.case(s='abc)",
        "repro.case(x=(1, 2)",
        "repro.case(x=1))",
    ],
)
def test_invalid_filter_raises(raw):
    """
    Malformed filters, including trailing text after the parameter list, a second parameter list, an
    unterminated string, and unbalanced parentheses, are reported as KeyError rather than silently matching.
    """

    with pytest.raises(KeyError):
        testfilter.TestFilter(raw)
