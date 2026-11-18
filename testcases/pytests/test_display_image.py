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

"""Tests for renpy/display/image.py: the alt text of ImageReference."""

import renpy.display.image as image_module


def test_image_reference_explicit_alt(mocker):
    """ImageReference returns the explicit style.alt when one is set.

    The substitution is patched to echo its input, so the result comes only from the explicit alt text.
    """
    im_ref = image_module.ImageReference(("eileen", "happy"))
    im_ref.target = mocker.MagicMock(_tts=lambda raw: "")
    im_ref.style = mocker.MagicMock()
    im_ref.style.alt = "Eileen smiling warmly"
    mocker.patch("renpy.substitutions.substitute", return_value=("Eileen smiling warmly", False))
    assert im_ref._tts(raw=False) == "Eileen smiling warmly"


def test_image_reference_auto_image_alt(mocker):
    """ImageReference derives alt text from the image tags only when config.auto_image_alt is True.

    With the option off the reference produces no text. With it on, the substituted tag and attribute names are
    returned. The config value is restored by the mocker at teardown.
    """
    import renpy.config as config_module

    im_ref = image_module.ImageReference(("eileen", "happy"))
    im_ref.target = mocker.MagicMock(_tts=lambda raw: "")
    im_ref.style = mocker.MagicMock()
    im_ref.style.alt = None

    # When auto_image_alt is False
    mocker.patch.object(config_module, "auto_image_alt", False, create=True)
    assert im_ref._tts(raw=False) == ""

    # When auto_image_alt is True
    config_module.auto_image_alt = True
    mocker.patch("renpy.substitutions.substitute", return_value=("eileen happy", False))
    assert im_ref._tts(raw=False) == "eileen happy"
