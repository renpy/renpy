# Copyright 2004-2021 Tom Rothamel <pytom@bishoujo.us>
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

# Trigger remote resource download, following a DownloadNeeded
# exception, and place it in the game/ in-memory filesystem when done.
# Placeholders (low-quality images, short silence sounds) are used by
# the engine meanwhile, and are replaced on completion.
# To save RAM, files are unlinked as soon as possible (e.g. once
# uploaded to GPU), and re-downloaded from browser cache if needed.
# Prediction is used to download resources in advance, but no guarantee.
# (e.g. won't work when loading a savegame, nor with 'show expression')

from __future__ import print_function
import renpy
import os
import renpy.display
import threading
import time

# A list of downloads, in-progress or waiting to be processed.
queue = [ ]

# A list of downloaded files to free later
to_unlink = { }

# A lock that must be held when updating the queue.
queue_lock = threading.RLock()

if renpy.emscripten:
    import emscripten, json

    # Space-efficient, copy-less download share
    # Note: could be reimplement with pyodide's jsproxy, but let's keep things small
    emscripten.run_script(r"""RenPyWeb = {
    xhr_id: 0,
    xhrs: {},

    dl_new: function(path) {
        var xhr = new XMLHttpRequest();
        xhr.responseType = 'arraybuffer';
        xhr.onerror = function() {
            console.log("Network error", xhr);
        };
        xhr.onload = function() {
            if (xhr.status == 200 || xhr.status == 304 || xhr.status == 206 || (xhr.status == 0 && xhr.response)) {
                // Create file reusing XHR's buffer (no-copy)
                try { FS.unlink(path); } catch(error) {}
                FS.writeFile(path, new Uint8Array(xhr.response), {canOwn:true});
            } else {
                console.log("Download error", xhr);
            }
        };
        xhr.open('GET', path);
        xhr.send();
        RenPyWeb.xhrs[RenPyWeb.xhr_id] = xhr;
        var ret = RenPyWeb.xhr_id;
        RenPyWeb.xhr_id++;
        return ret;
    },

    dl_get: function(xhr_id) {
        return RenPyWeb.xhrs[xhr_id];
    },

    dl_free: function(xhr_id) {
        delete RenPyWeb.xhrs[xhr_id];
        // Note: xhr.response kept alive until file is unlinked
    },
};
""")

    class XMLHttpRequest(object):
        def __init__(self, filename):
            url = 'game/' + filename
            self.id = emscripten.run_script_int(
                r'''RenPyWeb.dl_new({})'''.format(json.dumps(url)))

        def __del__(self):
            emscripten.run_script(r'''RenPyWeb.dl_free({});'''.format(self.id))

        @property
        def readyState(self):
            return emscripten.run_script_int(r'''RenPyWeb.dl_get({}).readyState'''.format(self.id))

        @property
        def status(self):
            return emscripten.run_script_int(r'''RenPyWeb.dl_get({}).status'''.format(self.id))

        @property
        def statusText(self):
            return emscripten.run_script_string(r'''RenPyWeb.dl_get({}).statusText'''.format(self.id))

elif os.environ.get('RENPY_SIMULATE_DOWNLOAD', False):
    # simulate
    # Ex: rm -rf odrdtest-simu && unzip -d odrdtest-simu/ odrdtest-1.0-dists/odrdtest-1.0-web/game.zip && RENPY_SIMULATE_DOWNLOAD=1 ./renpy.sh odrdtest-simu

    import urllib2, urllib, httplib, os, threading, time, random

    class XMLHttpRequest(object):
        def __init__(self, filename):
            self.done = False
            self.error = None
            url = 'http://127.0.0.1:8042/game/' + urllib.quote(filename)
            req = urllib2.Request(url)
            def thread_main():
                try:
                    time.sleep(random.random() * 0.5)
                    r = urllib2.urlopen(req)
                    fullpath = os.path.join(renpy.config.gamedir, filename)
                    with queue_lock:
                        with open(fullpath, 'wb') as f:
                            f.write(r.read())
                except urllib2.URLError as e:
                    self.error = str(e.reason)
                except httplib.HTTPException as e:
                    self.error = 'HTTPException'
                except Exception as e:
                    self.error = 'Error: ' + str(e)
                self.done = True
            threading.Thread(target=thread_main, name="XMLHttpRequest").start()

        @property
        def readyState(self):
            if self.done:
                return 4
            else:
                return 0

        @property
        def status(self):
            if self.error:
                return 0
            return 200

        @property
        def statusText(self):
            return self.error or 'OK'


class DownloadNeeded(Exception):
    def __init__(self, relpath, rtype, size):
        self.relpath = relpath
        self.rtype = rtype
        self.size = size


class ReloadRequest:
    def __init__(self, relpath, rtype, data):
        self.relpath = relpath
        self.rtype = rtype
        self.data = data
        self.gc_gen = 0
        self.xhr = XMLHttpRequest(self.relpath)

    def download_completed(self):
        return self.xhr.readyState == 4

    def __repr__(self):
        return u"<ReloadRequest {} '{}' {}>".format(self.rtype, self.relpath, self.download_completed())


def enqueue(relpath, rtype, data):
    global queue

    with queue_lock:
        for rr in queue:
            # de-dup same .data/image_filename
            # don't de-dup same .relpath (different .data == different cache entry)
            if rr.rtype == rtype == 'image':
                image_filename = data
                if rr.data == image_filename:
                    return
            elif rr.rtype == rtype == 'music' and rr.relpath == relpath:
                return
            elif rr.rtype == rtype == 'voice':
                if rr.relpath == relpath:
                    return
                if len([True for rr in queue if rr.type == 'voice']) > renpy.config.predict_statements:
                    # don't stack skipped dialogs
                    return
        queue.append(ReloadRequest(relpath, rtype, data))


def process_downloaded_resources():
    global queue, to_unlink

    reload_needed = False

    with queue_lock:

        todo = queue[:]
        postponed = []

        try:
            while todo:
                rr = todo.pop()

                if not rr.download_completed():
                    postponed.append(rr)
                    continue

                if rr.rtype == 'image':
                    fullpath = os.path.join(renpy.config.gamedir,rr.relpath)
                    if not os.path.exists(fullpath):
                        # trigger Ren'Py's error handler
                        raise IOError("Download error: {} ('{}' > '{}')".format(
                            (rr.xhr.statusText or "network error"), rr.relpath, fullpath))

                    image_filename = rr.data
                    renpy.exports.flush_cache_file(image_filename)

                    # mark for deletion
                    fullpath = os.path.join(renpy.config.gamedir,rr.relpath)
                    to_unlink[fullpath] = time.time()
                    reload_needed = True

                elif rr.rtype == 'music':
                    # - just wait for the 0.5s placeholder to finish,
                    #   will be reloaded on sound loop
                    # - no unlink
                    pass

                elif rr.rtype == 'voice':
                    # mark for deletion as it's a one-time usage (a bit delayed)
                    fullpath = os.path.join(renpy.config.gamedir,rr.relpath)
                    to_unlink[fullpath] = time.time() + 120

                # TODO: videos (when web support is implemented)

        # make sure the queue doesn't contain a corrupt file so we
        # don't rethrow an exception while in Ren'Py's error handler
        finally:
            queue = postponed + todo

    if reload_needed:
        # Refresh the screen and re-load images flushed from cache
        # Note: done at next Ren'Py interaction (prediction reset)
        renpy.display.render.free_memory()

    # Free files from memory once they are loaded
    # Due to search-path dups and derived images (including image-based animations)
    # files can't be removed right after actual load
    ttl = 60  # remove after 1mn - if your animation is longer than that, use a video
    for fullpath in to_unlink.keys():
        delta = time.time() - to_unlink[fullpath]
        if delta > ttl:
            os.unlink(fullpath)
            del to_unlink[fullpath]
