import pytest

import renpy
from renpy.text.extras import filter_alt_text


@pytest.fixture(autouse=True)
def text_config(mocker):
    """
    Isolates filter_alt_text from game configuration.

    Custom text tags and text replacement are disabled, and the tags whose contents are hidden from
    alt text are fixed to noalt, rt, and art.
    """

    mocker.patch.object(renpy.config, "custom_text_tags", {})
    mocker.patch.object(renpy.config, "self_closing_custom_text_tags", {})
    mocker.patch.object(renpy.config, "replace_text", None)
    mocker.patch.object(renpy.config, "tts_filter_tags", ["noalt", "rt", "art"])


def test_nested_same_filter_tag_stays_hidden_until_outer_close():
    """
    Text inside nested tags of the same filtered kind stays hidden until the outermost tag closes.

    Closing the inner {noalt} must not make the " c" after it visible.
    """

    text = "{noalt}a {noalt}b{/noalt} c{/noalt}"

    assert filter_alt_text(text) == ""


def test_nested_different_filter_tags_stay_hidden_until_outer_close():
    """
    Closing a different filtered tag ({rt}) nested inside {noalt} does not end the hiding started by
    {noalt}.
    """

    text = "{noalt}hidden {rt}ruby{/rt} still hidden{/noalt}visible"

    assert filter_alt_text(text) == "visible"


def test_unmatched_close_does_not_cancel_later_open():
    """
    A stray closing tag doesn't drive the nesting depth negative.

    If the leading {/noalt} were counted, the later {noalt} would only bring the depth back to zero and
    the hidden text would leak into the alt text. The trailing extra {/noalt} likewise must not hide
    "after".
    """

    text = "{/noalt}before{noalt}hidden{noalt}inner{/noalt}hidden{/noalt}{/noalt}after"

    assert filter_alt_text(text) == "beforeafter"
