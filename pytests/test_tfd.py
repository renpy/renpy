import pytest

from renpy import tfd


@pytest.mark.parametrize("message", [None, "", "Notification", "Caf\u00e9\t\u65e5\u672c\u8a9e\nMessage"])
@pytest.mark.parametrize("icon", ["info", "warning", "error"])
def test_notify_popup_accepts_text_and_supported_icons(icon, message):
    """
    tinyfiledialogs' notifyPopup accepts every supported icon with missing, empty, plain, and non-ASCII
    multi-line messages.

    The "tinyfd_query" title asks the native backend whether it can show a notification, without
    displaying one, so the test runs on machines without a desktop. The result is 0 or 1 depending on
    whether a backend is available; anything else means the arguments were mishandled.
    """

    result = tfd.notifyPopup("tinyfd_query", message, icon)
    assert result in (0, 1)
