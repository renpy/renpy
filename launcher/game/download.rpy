init python:

    import urllib2
    import os
    import threading
    import time

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
                self.urlfile = urllib2.urlopen(url)

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

