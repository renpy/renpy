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

from __future__ import annotations

import ast
import functools
from typing import Any
import re

import renpy
from renpy.test.testast import TestCase
from renpy.test.testsettings import global_testsuite_name


class PathFilterSegment:
    raw_text: str
    name: str
    parameters: dict[str, Any]
    pattern: re.Pattern | None = None

    def __init__(self, raw_text: str) -> None:
        self.raw_text = raw_text
        self.name, self.parameters = self._parse_filter_segment()

    def _parse_filter_segment(self) -> tuple[str, dict[str, Any]]:
        text = self.raw_text.strip()
        if not text:
            raise KeyError("Empty filter segment.")

        if "(" not in text:
            return text, {}

        name, params_expr = text.split("(", 1)
        params_expr = params_expr.rstrip(")")

        try:
            expression = ast.parse(f"_({params_expr})", mode="eval")
        except SyntaxError as exc:
            raise KeyError(f"Invalid parameter filter in {text!r}: {exc.msg}.") from exc

        call = expression.body
        if isinstance(call, ast.Name):
            return call.id, {}
        if not isinstance(call, ast.Call):
            raise KeyError(f"Invalid parameter filter in {text!r}.")
        if call.args:
            raise KeyError(f"Parameter filter only supports keyword arguments: {text!r}.")

        parsed_parameters: dict[str, Any] = {}
        for keyword in call.keywords:
            if keyword.arg is None:
                raise KeyError(f"Parameter filter does not support **kwargs: {text!r}.")

            try:
                parsed_parameters[keyword.arg] = ast.literal_eval(keyword.value)
            except Exception as exc:
                raise KeyError(
                    f"Parameter filter value for {keyword.arg!r} must be a literal in {text!r}."
                ) from exc

        return name, parsed_parameters

    def matches(self, other: PathFilterSegment) -> bool:
        if self.pattern is None:
            self.pattern = re.compile("^" + re.escape(self.name).replace(r"\*", r"[^\.:]*") + "$")

        if not self.pattern.match(other.name):
            return False

        overlapping_keys = set(self.parameters) & set(other.parameters)
        for key in overlapping_keys:
            if self.parameters[key] != other.parameters[key]:
                return False

        return True

class PathFilter:
    raw_path: str

    segments: list[PathFilterSegment]
    "The testcase or testsuite nodes that this filter resolves to."

    def __init__(self, raw_path: str):
        self.raw_path = raw_path
        self.segments = self.parse_filter_text()

    def matches(self, other: PathFilter, exact: bool = False, is_parent: bool = False) -> bool:
        """
        Determines if this filter matches `other`.

        Specifically:
        - If `is_parent` is False, `other` is a more specific filter than or equal to `self`.
        - If `is_parent` is True, `self` is a more specific filter than or equal to `other`.
        - The more specific filter must have at least as many segments as the less specific filter.
        - If parameters are specified in both filters for a given segment, their values must match.

        Examples:
        - "global.screens" matches "global.screens(kind='load')"
            True: More specific parameters:

        - "global.screens(kind='load')" matches "global.screens(val=3)"
            True: Overlapping but non-conflicting parameters

        - "global.screens(kind='load')" matches "global.screens(kind='save')"
            False: Conflicting parameters

        - "global.screens" matches "global"
            True if is_parent, False otherwise: Less specific path

        - "global.screens" matches "global.screens(kind='load')"
            False if is_parent, True otherwise: More specific path
        """

        if exact and len(self.segments) != len(other.segments):
            return False

        if is_parent:
            if len(self.segments) < len(other.segments):
                return False
        else:
            if len(self.segments) > len(other.segments):
                return False

        for this_segment, other_segment in zip(self.segments, other.segments):
            if not this_segment.matches(other_segment):
                return False

        return True

    def __eq__(self, other):
        if not isinstance(other, PathFilter):
            return False

        return self.segments == other.segments

    def parse_filter_text(self) -> list[PathFilterSegment]:
        """
        Parses the raw filter text into a list of segments, each with an optional
        parameter filter.
        """
        text = self.raw_path.strip()
        if not text:
            raise KeyError("Filter is empty.")

        parts: list[str] = []
        depth = 0
        start = 0

        for i, ch in enumerate(text):
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth < 0:
                    raise KeyError(f"Unmatched parentheses in filter: {self.raw_path!r}.")
            elif ch == "." and depth == 0:
                part = text[start:i].strip()
                if not part:
                    raise KeyError(f"Empty segment in filter: {self.raw_path!r}.")
                parts.append(part)
                start = i + 1

        if depth != 0:
            raise KeyError(f"Unmatched parentheses in filter: {self.raw_path!r}.")

        tail = text[start:].strip()
        if not tail:
            raise KeyError(f"Empty segment in filter: {self.raw_path!r}.")
        parts.append(tail)

        segments: list[PathFilterSegment] = []
        for part in parts:
            segment = get_path_filter_segment(part)
            if not segments and segment.name != global_testsuite_name:
                segments.append(get_path_filter_segment(global_testsuite_name))
            segments.append(segment)

        return segments

class ExecutionFilter:
    """
    A filter that can be applied to test cases or test suites to determine
    if they should be included in a test run.
    """
    include_filters: list[PathFilter]
    matched_nodes: set[TestCase]
    exact_matched_nodes: set[TestCase]
    parent_nodes: set[TestCase]

    def __init__(self, include_filters: list[str]) -> None:
        self.include_filters = [get_path_filter(raw_filter) for raw_filter in include_filters]
        if not self.include_filters:
            return

        self.matched_nodes = set()
        self.exact_matched_nodes = set()
        self.parent_nodes = set()

        for node in renpy.test.testexecution.testcases.values():
            if self.matches(node):
                self.matched_nodes.add(node)

                # If we explicitly matched this node (not just a parent),
                # make sure it's enabled even if it would normally be disabled by its own filters
                if self.matches(node, exact=True):
                    self.exact_matched_nodes.add(node)
                    node.enabled = True

        if not self.matched_nodes:
            raise KeyError(f"No test cases match the provided filters: {include_filters!r}.")

        for node in self.matched_nodes:
            for parent in node.get_parent_chain():
                self.parent_nodes.add(parent)

                if node in self.exact_matched_nodes:
                    parent.enabled = True

    def matches(self, testcase: TestCase, exact: bool = False) -> bool:
        if not self.include_filters:
            return True

        is_parent = (testcase not in self.matched_nodes) and (testcase in self.parent_nodes)

        node_filter = get_path_filter(testcase.current_full_parameterized_path)
        for include_filter in self.include_filters:
            if include_filter.matches(node_filter, exact, is_parent):
                # Make sure that the specific parameter keywords actually exist in the node
                # Can be an issue for wildcard filters like "math.*(a=3)"
                nodes = testcase.get_parent_chain() + [testcase]
                for node, segment in zip(nodes, include_filter.segments):
                    if segment.parameters and not node.parameters:
                        return False

                    if not segment.parameters:
                        continue

                    node_keys = set(node.parameters[0].keys())
                    segment_keys = set(segment.parameters.keys())
                    if not segment_keys.issubset(node_keys):
                        return False
                return True

        return False

@functools.cache
def get_path_filter_segment(raw_text: str) -> PathFilterSegment:
    return PathFilterSegment(raw_text)

@functools.cache
def get_path_filter(raw_text: str) -> PathFilter:
    return PathFilter(raw_text)
