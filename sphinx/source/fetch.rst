HTTPS/HTTP Fetch
================

Ren'Py supports fetching information over HTTP and HTTPS using the
renpy.fetch function. This function:

* Supports GET, POST, and PUT requests.
* Support POSTing or PUTing data or json to the server.
* Can return the result as bytes, a string, or a json object.

The fetch function is meant to be used in the main thread of Ren'Py, after
the game has started. It can be used on desktop, mobile, or the web platform.
When used on the web platform, when not fetching from the same server that
originally served the game, the server must support `CORS <https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS>`_.

As a very simple example, this gets news from a server::

    $ news = renpy.fetch("https://example.com/news.txt", result="text")
    "Here's the news: [news]"

And this posts JSON to a server, and gets JSON back::

    $ result = renpy.fetch("https://example.com/api", json={"name": "Ren'Py"}, result="json")

As with any application that communicates over the network, security needs
to be considered when using renpy.fetch, especially when displaying media
returned this way. (Ren'Py is generally not hardened against malicious images,
movies, and audio files.)

.. include:: inc/fetch

Requests
--------

On desktop and mobile, Ren'Py includes the `Requests <https://requests.readthedocs.io/>`_
library. This is more powerful, but doesn't integrate as well as renpy.fetch.
(For example, Ren'Py will call :func:`renpy.pause` to wait for data, while
requests will block, which could lead to problems like audio stalling.)
