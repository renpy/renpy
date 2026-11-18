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

import http.server
import os
import threading
import time

import pytest

from renpy.exports import fetchexports


class Handler(http.server.BaseHTTPRequestHandler):
    """
    A request handler that records each request's declared Content-Length and the body it actually received in
    server.requests. /redirect-307 and /redirect-303 redirect to /final, and /bad-length sends an invalid
    Content-Length header on its response.
    """

    def log_message(self, *args):
        pass

    def handle_any(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        self.server.requests.append((self.command, self.path, length, body))

        if self.path.startswith("/redirect-"):
            self.send_response(int(self.path[len("/redirect-") :]))
            self.send_header("Location", "/final")
            self.send_header("Content-Length", "0")
            self.end_headers()
        elif self.path == "/bad-length":
            self.send_response(200)
            self.send_header("Content-Length", "abc")
            self.end_headers()
            self.wfile.write(b"ok")
            self.close_connection = True
        else:
            self.send_response(200)
            self.send_header("Content-Length", "2")
            self.end_headers()
            self.wfile.write(b"ok")

    do_GET = do_POST = do_PUT = handle_any


@pytest.fixture
def server(mocker):
    """
    A local HTTP server on an ephemeral port, shut down after the test. Its requests attribute lists what it
    received. fetch_pause is replaced with a short sleep, as it needs a running game context. Proxies are
    removed both from fetchexports and from the environment, which requests also consults, so that localhost
    requests are not diverted to a proxy.
    """

    mocker.patch.object(fetchexports, "fetch_pause", lambda: time.sleep(0.001))
    mocker.patch.object(fetchexports, "proxies", {})

    environ = {k: v for k, v in os.environ.items() if not k.lower().endswith("_proxy")}
    environ["NO_PROXY"] = environ["no_proxy"] = "127.0.0.1"
    mocker.patch.dict(os.environ, environ, clear=True)

    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    httpd.daemon_threads = True
    httpd.requests = []

    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()

    yield httpd

    httpd.shutdown()
    httpd.server_close()
    thread.join()


def fetch(server, path, method, data):
    """Runs fetch_requests against the test server and returns its result."""

    url = f"http://127.0.0.1:{server.server_address[1]}{path}"
    return fetchexports.fetch_requests(url, method, data, "application/octet-stream", 5, {})


@pytest.mark.parametrize("method", ["POST", "PUT"])
@pytest.mark.parametrize("status", [307, 308])
def test_redirect_resends_body(server, method, status):
    """
    A 307 or 308 redirect makes requests resend the body to the new location, which requires rewinding it. The
    server checks that the body arrives in full the second time, not empty with the old Content-Length.
    """

    assert fetch(server, f"/redirect-{status}", method, b"hello world") == b"ok"

    assert [(path, length, body) for _, path, length, body in server.requests] == [
        (f"/redirect-{status}", 11, b"hello world"),
        ("/final", 11, b"hello world"),
    ]


def test_redirect_303_becomes_get(server):
    """A 303 redirect turns the request into a GET without a body, which still has to work with the wrapper."""

    assert fetch(server, "/redirect-303", "POST", b"hello world") == b"ok"

    assert [(method, path, length) for method, path, length, _ in server.requests] == [
        ("POST", "/redirect-303", 11),
        ("GET", "/final", 0),
    ]


@pytest.mark.parametrize("data", [b"", None])
def test_empty_body(server, data):
    """An empty or missing body is sent as a plain zero-length body, not as a chunked upload."""

    assert fetch(server, "/final", "POST", data) == b"ok"

    assert server.requests == [("POST", "/final", 0, b"")]


def test_invalid_content_length_response(server):
    """
    A response with an unparseable Content-Length only affects the progress calculation, so the fetch still
    returns the body instead of failing with a FetchError.
    """

    assert fetch(server, "/bad-length", "GET", None) == b"ok"


def test_seek_resets_progress():
    """Seeking back to the start also resets the upload progress, so a resent body does not count twice."""

    progress = fetchexports.FetchProgress(b"hello world")

    assert progress.read(5) == b"hello"
    assert progress.tell() == 5
    assert 0 < progress.get_progress() < 1

    progress.seek(0)

    assert progress.tell() == 0
    assert progress.get_progress() == 0
    assert b"".join(progress) == b"hello world"
