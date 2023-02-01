# Copyright 2004-2023 Tom Rothamel <pytom@bishoujo.us>
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

init python:

    import urllib.request
    import os
    import threading
    import time

    ssl_context_cache = None

    def ssl_context():
        """
        Returns the SSL context.
        """

        global ssl_context_cache

        if ssl_context_cache is None:
            import ssl
            import certifi
            ssl_context_cache = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH, cafile=certifi.where())

        return ssl_context_cache

    class Downloader(object):

        def __init__(self, url, dest):
            """
            Downloads `url` to `dest`, providing progress reports
            as necessary.
            """

            self.url = url

            # The destination file, and the destination temp file.
            self.dest = dest
            self.tmp = dest + ".tmp"

            # Open the tmpfile.
            self.safe_unlink(self.tmp)
            self.tmpfile = open(self.tmp, "wb")

            # Set by the thread to indicate progress (ranges from 0.0 to 1.0).
            self.progress = 0.0

            # This is set to true by cancel() to indicate the download should be cancelled.
            self.cancelled = False

            # Set on succes or failure.
            self.success = False
            self.failure = None

            try:
                # Open the URL.

                self.urlfile = urllib.request.urlopen(url, context=ssl_context())

                t = threading.Thread(target=self.thread)
                t.daemon = True
                t.start()

            except Exception as e:
                self.failure = str(e)

        def thread(self):

            try:
                count = 0

                if "content-length" in self.urlfile.headers:
                    length = int(self.urlfile.headers["content-length"])
                else:
                    length = 0

                while not self.cancelled:

                    data = self.urlfile.read(65536)

                    if not data:
                        break

                    count += len(data)
                    self.tmpfile.write(data)

                    if length > 0:
                        self.progress = 1.0 * count / length

                self.tmpfile.close()

                if self.cancelled:
                    return

                if length and count != length:
                    self.failure = "Download length does not match content length."
                    return

                self.safe_unlink(self.dest)
                os.rename(self.tmp, self.dest)

                self.success = True

            except Exception as e:
                self.failure = str(e)


        def safe_unlink(self, fn):
            if os.path.exists(fn):
                os.unlink(fn)

        def cancel(self):
            """
            Cancels the download.
            """

            self.cancelled = True

        def check(self):
            """
            Returns True if the download is finished, False if it was cancelled,
            None if it's ongoing, and raises an Exception if the download has failed.
            """

            if self.success:
                return True
            if self.cancelled:
                return False
            if self.failure:
                raise Exception("Downloading {} to {} failed: {}".format(self.url, self.dest, self.failure))

            return None

    class DownloaderValue(BarValue):
        """
        A BarValue that reports the progress of a background download.
        """

        def __init__(self, d):
            self.downloader = d

        def get_adjustment(self):
            self.adjustment = ui.adjustment(value=0.0, range=1.0, adjustable=False)
            return self.adjustment

        def periodic(self, st):
            self.adjustment.change(self.downloader.progress)
            return .25

