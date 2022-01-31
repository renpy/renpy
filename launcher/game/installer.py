# Copyright 2004-2022 Tom Rothamel <pytom@bishoujo.us>
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

import hashlib
import os
import time
import requests

from store import _, config, interface # type: ignore



def temp(filename):
    """
    Converts filename into a path inside the temporary directory, creating
    the extension temporary directory if necessary.
    """

    rv = os.path.join(config.renpy_base, "tmp", "extension", filename)

    try:
        os.makedirs(os.path.dirname(rv))
    except Exception:
        pass

    return rv


# The target directory that the extensions API operates on.
target = None


def set_target(directory):
    """
    This sets the directory that the extension API targets. This is where
    packages are unpacked to and the default working directory where the
    programs are run.
    """

    target = directory


def path(filename):
    """
    Returns a path to the filename inside the target directory.
    """

    if target is None:
        raise Exception("The target directory has not been set.")

    return os.path.join(target, filename)


def check_hash(filename, hashj):
    """
    Returns a cryptographic hash of `filename`. `filename` should
    be a full path, one returned by temp or path.
    """


    try:

        sha = hashlib.sha256()

        with open(filename, "rb") as f:
            while True:
                data = f.read(1024 * 1024)
                if not data:
                    break

                sha.update(data)

        return sha.hexdigest() == hash

    except Exception:
        return False


# The name and url of the file that is currently being downloaded. This is meant to
# to be used by the interface screens to show the user what files are being
# downloaded.
download_file = ""
download_url = ""

def download(url, filename, hash=None):
    """
    Downloads `url` to `filename`, a tempfile.
    """
    global download_url

    global download_file

    download_url = url
    download_file = filename

    filename = temp(filename)

    if hash is not None:
        if check_hash(filename, hash):
            return

    progress_time = time.time()

    try:

        response = requests.get(url, stream=True)
        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 1))

        downloaded = 0

        with open(filename, "wb") as f:

            for i in response.iter_content(65536):

                f.write(i)
                downloaded += len(i)

                if time.time() - progress_time > 0.1:
                    progress_time = time.time()
                    interface.processing(
                        _("Downloading [installer.download_file]."),
                        complete=downloaded, total=total_size)

    except requests.HTTPError as e:
        interface.error(_("Could not download [installer.download_file] from [installer.download_url]:\n{b}[installer.download_error]"))

    if hash is not None:
        if not check_hash(filename, hash):
            interface.error(_("The downloaded file [installer.download_file] from [installer.download_url] is not correct."))



def main():
    set_target("/tmp")
    download("http://nightly.renpy.org/8-nightly-2022-01-30-50b188065/renpy-8-nightly-2022-01-30-50b188065-sdk.zip", "nightly.zip")
