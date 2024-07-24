# Copyright 2004-2024 Tom Rothamel <pytom@bishoujo.us>
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

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals # type: ignore
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode # *


import re
import time
import os

try:
    import emscripten
except ImportError:
    pass

import renpy

if PY2:
    from urllib import urlencode as _urlencode # type: ignore
else:
    from urllib.parse import urlencode as _urlencode

try:
    if PY2:
        import urllib
        proxies = urllib.getproxies() # type: ignore
    else:
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

        m = re.search(r'\d\d\d', message)
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
        import pygame_sdl2
        pygame_sdl2.event.pump()
        renpy.audio.audio.periodic()

        if renpy.emscripten:
            emscripten.sleep(0)

        return

    renpy.exports.pause(0)


def fetch_requests(url, method, data, content_type, timeout, headers):
    """
    :undocumented:

    Used by fetch on non-emscripten systems.

    Returns either a bytes object, or a FetchError.
    """

    import threading
    import requests

    # Because we don't have nonlocal yet.
    resp = [ None ]

    if data is not None:
        headers = dict(headers)
        headers["Content-Type"] = content_type

    def make_request():
        try:
            r = requests.request(method, url, data=data, timeout=timeout, headers=headers, proxies=proxies)
            r.raise_for_status()
            resp[0] = r.content # type: ignore
        except Exception as e:
            resp[0] = FetchError(str(e), e) # type: ignore

    t = threading.Thread(target=make_request)
    t.start()

    while resp[0] is None:
        fetch_pause()

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

    url = url.replace('"' , '\\"')

    import json
    headers = json.dumps(headers)
    headers = headers.replace("\\", "\\\\").replace('"', '\\"')

    if method == "GET" or method == "HEAD":
        command = """fetchFile("{method}", "{url}", null, "{fn}", null, "{headers}")""".format( method=method, url=url, fn=fn, content_type=content_type, headers=headers)
    else:
        command = """fetchFile("{method}", "{url}", "{fn}", "{fn}", "{content_type}", "{headers}")""".format( method=method, url=url, fn=fn, content_type=content_type, headers=headers)

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



def fetch(url, method=None, data=None, json=None, content_type=None, timeout=5, result="bytes", params=None, headers={}):
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

    if result not in ( "bytes", "text", "json" ):
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
        raise content # type: ignore

    try:
        if result == "bytes":
            return content
        elif result == "text":
            return content.decode("utf-8") # type: ignore
        elif result == "json":
            return _json.loads(content)
    except Exception as e:
        raise FetchError("Failed to decode the result: " + str(e), e)
