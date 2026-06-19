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

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals  # type: ignore
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode  # *

import io
import os
import renpy


def get_clipboard_text() -> str:
    """
    :doc: clipboard

    Returns the text currently on the clipboard, or raises an exception
    if no text is available.

    Returns a string.
    """

    return renpy.pygame.scrap.get(renpy.pygame.scrap.SCRAP_TEXT).decode("utf-8")


def put_clipboard_text(text: str) -> None:
    """
    :doc: clipboard

    Places `text` onto the clipboard.

    `text`
        The string to place on the clipboard.
    """

    renpy.pygame.scrap.put(renpy.pygame.scrap.SCRAP_TEXT, text.encode("utf-8"))


def get_clipboard_data(mime_type: str) -> bytes:
    """
    :doc: clipboard

    Returns the clipboard data for `mime_type`, or raises an exception
    if no data is available for that MIME type.

    `mime_type`
        The MIME type to retrieve, for example "image/png".

    Returns bytes.
    """

    return renpy.pygame.scrap.get_data(mime_type)


def get_clipboard_mime_types() -> list[str]:
    """
    :doc: clipboard

    Returns a list of MIME type strings currently available on the clipboard.
    """

    return renpy.pygame.scrap.get_mime_types()


def put_clipboard_data(data_dict: dict[str | bytes, str | bytes]) -> None:
    """
    :doc: clipboard

    Sets up clipboard data for multiple MIME types.

    `data_dict`
        A dictionary mapping MIME type strings or bytes to data strings
        or bytes. String values are encoded as UTF-8.
    """

    renpy.pygame.scrap.put_data(data_dict)


def put_clipboard_image_file(filename: str, absolute_path: bool = False) -> None:
    """
    :doc: clipboard

    Copies an image file to the system clipboard. The image is placed
    on the clipboard in its original format, and also as a PNG if the
    original is not already a PNG. The filename is also placed on the
    clipboard as a text/plain string.

    Using this function tends to improve compatibility with other applications, as some applications are only
    able to handle image/png image data.

    `filename`
        The name of the image file to copy to the clipboard.

    `absolute_path`
        If True, `filename` is treated as an absolute filesystem path.
        If False (the default), the file is opened using Ren'Py's
        file loading mechanism.
    """

    # Read the image file.
    if absolute_path:
        with open(filename, "rb") as f:
            original_data = f.read()
    else:
        with renpy.loader.load(filename, "images") as f:
            original_data = f.read()

    # Determine the MIME type from the file extension.
    ext = os.path.splitext(filename)[1].lower()

    mime_map = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
        ".avif": "image/avif",
        ".svg": "image/svg+xml",
        ".bmp": "image/bmp",
        ".tga": "image/x-tga",
    }

    mime_type = mime_map.get(ext, None)
    if mime_type is None:
        raise ValueError("Unsupported image format: {}".format(ext))

    # Build the clipboard data dictionary.
    data_dict: dict[str | bytes, str | bytes] = {mime_type: original_data}

    # If the image is not already a PNG, convert to PNG and add it.
    if mime_type != "image/png":
        surf = renpy.pygame.image.load(io.BytesIO(original_data), namehint=filename)

        with io.BytesIO() as png_buffer:
            renpy.display.module.save_png(surf, png_buffer, 0)
            data_dict["image/png"] = png_buffer.getvalue()

    # Add the filename as text/plain.
    data_dict["text/plain"] = filename

    put_clipboard_data(data_dict)


def put_clipboard_text_file(filename: str, absolute_path: bool = False) -> None:
    """
    :doc: clipboard

    Copies a text file to the system clipboard as a text/plain attachment.

    `filename`
        The name of the text file to copy to the clipboard.

    `absolute_path`
        If True, `filename` is treated as an absolute filesystem path.
        If False (the default), the file is opened using Ren'Py's
        file loading mechanism.
    """

    # Read the text file.
    if absolute_path:
        with open(filename, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        with renpy.exports.open_file(filename, "utf-8") as f:
            text = f.read()

    put_clipboard_text(text)
