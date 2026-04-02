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


import re
import time
import os

try:
    import emscripten
except ImportError:
    pass

import renpy

from urllib.parse import urlencode as _urlencode

try:
    import urllib.request

    proxies = urllib.request.getproxies()
except Exception as e:
    proxies = {}


class FetchError(Exception):
    """
    :undocumented:

    The type of errors raised by :func:`renpy.fetch`.
    """

    def __init__(self, message, exception=None):
        super(FetchError, self).__init__(message)

        self.original_exception = exception

        m = re.search(r"\d\d\d", message)
        if m is not None:
            self.status_code = int(m.group(0))
        else:
            self.status_code = None


def fetch_pause():
    """
    Called by the fetch functions to pause for a short amount of time.
    """

    if renpy.game.context().init_phase:
        return

    if renpy.game.context().interacting:

        renpy.pygame.event.pump()
        renpy.audio.audio.periodic()

        if renpy.emscripten:
            emscripten.sleep(0)

        return

    renpy.exports.pause(0)


class FetchProgress(object):
    def __init__(self, data):
        if data is None:
            self.data = b""
        elif isinstance(data, basestring):
            self.data = data.encode("utf-8")
        else:
            self.data = data

        self.upload_expected = len(self.data)
        self.upload_current = 0
        self.offset = 0

        self.download_expected = 0
        self.download_current = 0
        self.monitoring_download = False

    def __len__(self):
        return self.upload_expected

    def read(self, size=-1):
        if size == -1:
            chunk = self.data[self.offset:]
            self.offset = self.upload_expected
        else:
            chunk = self.data[self.offset:self.offset+size]
            self.offset += len(chunk)

        self.upload_current += len(chunk)
        return chunk

    def get_progress(self):
        if self.monitoring_download:
            if self.download_expected == 0:
                # If we don't know the size, return 0.0 until done.
                return 0.0
            return min(self.download_current / self.download_expected, 1.0)
        else:
            if self.upload_expected == 0:
                return 1.0
            return min(self.upload_current / self.upload_expected, 1.0)


active_fetch_requests: set[FetchProgress] = set()
"""The set of active fetch requests."""

def get_fetch_requests_progress():
    """
    :undocumented:

    Returns the progress of the currently active fetch requests as a float
    between 0.0 and 1.0. If no fetches are in progress, returns 1.0.
    """
    if not active_fetch_requests:
        return 1.0

    total = sum(req.get_progress() for req in active_fetch_requests)
    return total / len(active_fetch_requests)


def fetch_requests(url, method, data, content_type, timeout, headers):
    """
    :undocumented:

    Used by fetch on non-emscripten systems.

    Returns either a bytes object, or a FetchError.
    """

    import threading
    import requests

    # Because we don't have nonlocal yet.
    resp = [None]

    progress = FetchProgress(data)
    active_fetch_requests.add(progress)

    if data is not None:
        headers = dict(headers)
        headers["Content-Type"] = content_type

    def make_request():
        try:
            r = requests.request(
                method, url,
                data=progress if data is not None else None,
                timeout=timeout,
                headers=headers,
                proxies=proxies,
                stream=True
            )
            r.raise_for_status()

            progress.monitoring_download = True
            progress.download_expected = int(r.headers.get("Content-Length", 0))

            chunks = []
            for chunk in r.iter_content(chunk_size=65536):
                if chunk:
                    chunks.append(chunk)
                    progress.download_current += len(chunk)

            resp[0] = b"".join(chunks)
        except Exception as e:
            resp[0] = FetchError(str(e), e)

    t = threading.Thread(target=make_request)
    t.start()

    try:
        while resp[0] is None:
            fetch_pause()
    finally:
        active_fetch_requests.discard(progress)

    t.join()

    return resp[0]


def fetch_emscripten(url, method, data, content_type, timeout, headers):
    """
    :undocumented:

    Used by fetch on emscripten systems.

    Returns either a bytes object, or a FetchError.
    """

    import emscripten

    fn = "/req-" + str(time.time()) + ".data"

    with open(fn, "wb") as f:
        if data is not None:
            f.write(data)

    url = url.replace('"', '\\"')

    import json

    headers = json.dumps(headers)
    headers = headers.replace("\\", "\\\\").replace('"', '\\"')

    if method == "GET" or method == "HEAD":
        command = """fetchFile("{method}", "{url}", null, "{fn}", null, "{headers}")""".format(
            method=method, url=url, fn=fn, content_type=content_type, headers=headers
        )
    else:
        command = """fetchFile("{method}", "{url}", "{fn}", "{fn}", "{content_type}", "{headers}")""".format(
            method=method, url=url, fn=fn, content_type=content_type, headers=headers
        )

    fetch_id = emscripten.run_script_int(command)

    status = "PENDING"
    message = "Pending."

    start = time.time()
    while time.time() - start < timeout:
        fetch_pause()

        result = emscripten.run_script_string("""fetchFileResult({})""".format(fetch_id))
        status, _ignored, message = result.partition(" ")

        if status != "PENDING":
            break

    try:
        if status == "OK":
            with open(fn, "rb") as f:
                return f.read()

        else:
            return FetchError(message)

    finally:
        os.unlink(fn)


def fetch(
    url, method=None, data=None, json=None, content_type=None, timeout=5, result="bytes", params=None, headers={}
):
    """
    :doc: fetch

    This performs an HTTP (or HTTPS) request to the given URL, and returns
    the content of that request. If it fails, raises a FetchError exception,
    with text that describes the failure. (But may not be suitable for
    presentation to the user.)

    `url`
        The URL to fetch.

    `method`
        The method to use. Generally one of "GET", "POST", or "PUT", but other
        HTTP methods are possible. If `data` or `json` are not None, defaults to
        "POST", otherwise defaults to GET.

    `data`
        If not None, a byte string of data to send with the request.

    `json`
        If not None, a JSON object to send with the request. This takes precendence
        over `data`.

    `content_type`
        The content type of the data. If not given, defaults to "application/json"
        if `json` is not None, or "application/octet-stream" otherwise. Only
        used on a POST or PUT request.

    `timeout`
        The number of seconds to wait for the request to complete.

    `result`
        How to process the result. If "bytes", returns the raw bytes of the result.
        If "text", decodes the result using UTF-8 and returns a unicode string. If "json",
        decodes the result as JSON. (Other exceptions may be generated by the decoding
        process.)

    `params`
        A dictionary of parameters that are added to the URL as a query string.

    `headers`
        A dictionary of headers to send with the request.

    This may be called from inside or outside of an interaction.

    * Outside of an interation, while waiting for `timeout` to pass, this will
      repeatedly call :func:`renpy.pause`, so Ren'Py doesn't lock up. It
      may make sense to display a screen to the user to let them know what is going on.

    * Inside of an interaction (for example, inside an Action), this will block
      the display system until the fetch request finishes or times out. It will try
      to service the audio system, so audio will continue to play.

    This function should work on all platforms. However, on the web platform,
    requests going to a different origin than the game will fail unless allowed
    by CORS.
    """

    import json as _json

    if data is not None and json is not None:
        raise FetchError("data and json arguments are mutually exclusive.")

    if result not in ("bytes", "text", "json"):
        raise FetchError("result must be one of 'bytes', 'text', or 'json'.")

    if params is not None:
        url += "?" + _urlencode(params)

    if method is None:
        if data is not None or json is not None:
            method = "POST"
        else:
            method = "GET"

    if content_type is None:
        if json is not None:
            content_type = "application/json"
        else:
            content_type = "application/octet-stream"

    if json is not None:
        data = _json.dumps(json).encode("utf-8")

    if renpy.emscripten:
        content = fetch_emscripten(url, method, data, content_type, timeout, headers=headers)
    else:
        content = fetch_requests(url, method, data, content_type, timeout, headers=headers)

    if isinstance(content, Exception):
        raise content  # type: ignore

    try:
        if result == "bytes":
            return content
        elif result == "text":
            return content.decode("utf-8")  # type: ignore
        elif result == "json":
            return _json.loads(content)
    except Exception as e:
        raise FetchError("Failed to decode the result: " + str(e), e)


def get_fetch_progress():
    """
    :doc: fetch

    Returns the progress of the currently active fetch requests as a float
    between 0.0 and 1.0. If no fetches are in progress, returns 1.0.
    """

    if renpy.emscripten:
        return 0.0

    return get_fetch_requests_progress()
