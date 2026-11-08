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


"""Tests for renpy.get_statement_info during Context.predict, in renpy/execution.py."""

from types import SimpleNamespace

import pytest

import renpy
from renpy.display import predict
from renpy.execution import Context


@pytest.fixture
def predicting_context(mocker):
    """
    Returns a function that predicts from a one-statement script and returns the StatementInfo objects its
    predict method collected.

    The script is replaced by one with a single label whose statement's predict method records
    renpy.get_statement_info(), as a creator-defined statement's predict function does, and then
    runs `behavior`. The Context is a real one, with the translate identifiers a running game would have.
    """

    seen = []

    class Node:
        """
        A statement that records its statement info when predicted, and then runs `behavior`.
        """

        filename = "game/script.rpy"
        linenumber = 42
        behavior = None

        def predict(self):
            seen.append(renpy.exports.get_statement_info())

            if self.behavior is not None:
                self.behavior()

            return []

    node = Node()

    script = SimpleNamespace(has_label=lambda label: label == "target", lookup=lambda label: node)
    mocker.patch.object(renpy.game, "script", script)
    mocker.patch.object(renpy.config, "predict_statements_callback", lambda current: ["target"])
    mocker.patch.object(renpy.config, "predict_statements", 3)
    mocker.patch.object(predict, "statement", None)
    mocker.patch.object(predict, "tlids", [])

    def run(behavior=None):
        node.behavior = behavior

        context = Context(False)
        context.current = "current"
        context.translate_identifier = "statement_info_tlid"
        context.alternate_translate_identifier = None

        list(context.predict())

        return seen

    return run


def test_predicted_statement_reports_its_location_and_translation_id(predicting_context) -> None:
    """
    While a statement is predicted, get_statement_info returns the statement's file and line, and the
    translation identifier of the statement being executed, so a creator-defined statement can tell where
    it is being predicted from. Afterwards the engine's own record of the predicted statement is cleared.
    """

    infos = predicting_context()

    assert len(infos) == 1
    assert infos[0].filename == "game/script.rpy"
    assert infos[0].linenumber == 42
    assert infos[0].tlid == "statement_info_tlid"
    assert predict.statement is None


def test_failing_prediction_restores_the_predicted_statement(predicting_context) -> None:
    """
    If a statement's predict method raises, prediction swallows the error and still clears the engine's
    record of the predicted statement, so that later calls to get_statement_info describe the statement
    that is executing rather than the one that failed.
    """

    def fail() -> None:
        raise Exception("statement info prediction failure")

    infos = predicting_context(fail)

    assert len(infos) == 1
    assert predict.statement is None
