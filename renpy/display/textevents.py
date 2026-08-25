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

# This file contains the text events server. When enabled, Ren'Py listens on
# a TCP port on 127.0.0.1 and streams the text it shows on the screen, with
# the role each piece of text plays (who, what, choice, ...), as one JSON
# object per line. This lets text-to-speech engines, live translators, and
# similar tools react to what the game shows without scraping the screen.
#
# The text is gathered by a pass over the displayables that mirrors the one
# self-voicing makes, so the two agree about what's on screen and in what
# order.

import json
import os
import queue
import socket
import threading
import traceback

import renpy

# The TextEventServer, if one is running.
server = None

# The id of the next record.
next_id = 0

# The current interaction number. This goes up each time the set of text on
# the screen changes.
interaction = 0

# The (text, role, style) tuples sent for the current interaction, used to
# avoid sending the same text again when the interaction restarts.
last_texts = None

# The displayable the last focus record was sent for.
last_focused = None


class TextEventServer:
    """
    Listens for connections on a port, and sends records to every client
    that has connected. Records are sent from a thread, so a slow client
    never stalls the game.
    """

    def __init__(self, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("127.0.0.1", port))
        self.sock.listen(5)

        self.port = self.sock.getsockname()[1]

        self.clients = []
        self.lock = threading.Lock()
        self.queue = queue.Queue()

        threading.Thread(target=self.accept_loop, name="text events accept", daemon=True).start()
        threading.Thread(target=self.send_loop, name="text events send", daemon=True).start()

    def accept_loop(self):
        while True:
            try:
                conn, _addr = self.sock.accept()
            except OSError:
                return

            conn.settimeout(5.0)

            with self.lock:
                self.clients.append(conn)

    def send_loop(self):
        while True:
            data = self.queue.get()

            with self.lock:
                clients = list(self.clients)

            for c in clients:
                try:
                    c.sendall(data)
                except OSError:
                    self.drop(c)

    def drop(self, c):
        with self.lock:
            if c in self.clients:
                self.clients.remove(c)

        try:
            c.close()
        except OSError:
            pass

    def send(self, record):
        self.queue.put((json.dumps(record, ensure_ascii=False) + "\n").encode("utf-8"))


def init():
    """
    Starts the server, if config.text_events_port or the
    RENPY_TEXT_EVENTS_PORT environment variable is set.
    """

    global server

    if server is not None:
        return

    port = os.environ.get("RENPY_TEXT_EVENTS_PORT", None)

    if port is None:
        port = renpy.config.text_events_port

    if port is None:
        return

    try:
        server = TextEventServer(int(port))
    except Exception as e:
        renpy.display.log.write("Could not start the text events server on port %r: %r", port, e)
        return

    renpy.display.log.write("Text events server listening on 127.0.0.1:%d", server.port)


def send(record):
    global next_id

    record["id"] = next_id
    next_id += 1

    record["interaction"] = interaction

    server.send(record)


def style_info(d):
    """
    Returns the (role, style name) of the displayable `d`, or (None, None)
    if it can't be determined.

    The role comes from config.text_events_roles, looked up by the name of
    the displayable's style and then the names of its parents. If none of
    them is in the map, the name of the first named style is the role.
    """

    style = getattr(d, "style", None)

    first = None
    seen = 0

    while style is not None and seen < 32:
        seen += 1

        name = style.name

        if name:
            base = name[0]

            if base in renpy.config.text_events_roles:
                return renpy.config.text_events_roles[base], first or base

            if first is None:
                first = base

        parent = style.parent

        if not parent:
            break

        # Style names are tuples, and renpy.style.styles maps those to the
        # style objects.
        style = renpy.style.styles.get(parent, None)

    return first, first


def add(records, text, d):
    """
    Adds a record for `text`, shown by displayable `d`, to `records`.
    """

    text = text.strip()

    if not text:
        return

    role, style = style_info(d)
    records.append((text, role, style))


def gather(d, records):
    """
    Walks the displayable `d` and its children, adding the text they show to
    `records` in the order self-voicing would read it. Returns true if a
    displayable asked for the traversal to stop (a modal screen, for
    example), in which case the text before it is dropped, as self-voicing
    does.
    """

    if d is None:
        return False

    # Screens that are on their way out say nothing. Modal screens are read,
    # and then stop the traversal, so nothing behind them is read.
    if isinstance(d, renpy.display.screen.ScreenDisplayable):
        if d.phase in (renpy.display.screen.OLD, renpy.display.screen.HIDE):
            return False

        gather_children(d, records)
        return bool(d.modal)

    if isinstance(d, renpy.display.layout.NearRect) and d.parent_rect is None:
        return False

    if isinstance(d, renpy.display.behavior.DismissBehavior):
        return False

    # Buttons and bars are read as a whole, using their alt text or the text
    # of their children. Self-voicing skips them when reading the screen and
    # reads them when they're focused, but a tool wants to see choices and
    # the like as part of the screen.
    if isinstance(d, (renpy.display.behavior.Button, renpy.display.behavior.Bar)):
        try:
            text = d._tts_all(raw=False)
        except renpy.display.tts.TTSRoot:
            return False

        add(records, text, d)
        return isinstance(text, renpy.display.tts.TTSDone)

    # A displayable with alt text speaks that instead of its children.
    style = getattr(d, "style", None)

    if style is not None and style.alt is not None:
        text = d._tts_all(raw=False)
        add(records, text, d)
        return isinstance(text, renpy.display.tts.TTSDone)

    children = [i for i in d.visit() if i is not None]

    if not children:
        text = d._tts(raw=False)
        add(records, text, d)
        return isinstance(text, renpy.display.tts.TTSDone)

    return gather_children(d, records)


def gather_children(d, records):
    children = [i for i in d.visit() if i is not None]

    if isinstance(d, renpy.display.layout.MultiBox) and (d.layers or d.scene_list) and renpy.config.tts_front_to_back:
        children.reverse()

    for i in children:
        start = len(records)

        if gather(i, records):
            del records[:start]
            return True

    return False


def focus_changed(widget):
    """
    Called when an interaction starts or the focus changes. Sends the text
    on the screen, if it has changed, and then the text of the focused
    displayable.
    """

    global interaction
    global last_texts
    global last_focused

    if server is None:
        return

    root = renpy.display.tts.root

    if root is None:
        return

    records = []

    try:
        gather(root, records)
    except Exception as e:
        renpy.display.log.write("Text events: could not gather text: %r\n%s", e, traceback.format_exc())
        return

    if records != last_texts:
        last_texts = records
        last_focused = None
        interaction += 1

        send({"kind": "interaction", "image_tag": renpy.exports.get_say_image_tag()})

        for text, role, style in records:
            send({"kind": "text", "role": role, "style": style, "text": text})

    if widget is None or widget is last_focused:
        return

    last_focused = widget

    try:
        text = widget._tts_all(raw=False)
    except renpy.display.tts.TTSRoot:
        return
    except Exception:
        return

    text = text.strip()

    if not text:
        return

    role, style = style_info(widget)
    send({"kind": "focus", "role": role, "style": style, "text": text})
