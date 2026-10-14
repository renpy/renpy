import unittest

from renpy import tfd


class TestNotificationPopup(unittest.TestCase):
    def test_notify_popup_accepts_text_and_supported_icons(self) -> None:
        """Query the native backend without displaying a notification."""
        for icon in ("info", "warning", "error"):
            for message in (None, "", "Notification", "Caf\u00e9\t\u65e5\u672c\u8a9e\nMessage"):
                with self.subTest(icon=icon, message=message):
                    result = tfd.notifyPopup("tinyfd_query", message, icon)
                    self.assertIn(result, (0, 1))
