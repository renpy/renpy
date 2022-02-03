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
import zipfile
import tarfile
import shutil

from store import _, config, interface # type: ignore

temp_exists = False

def _ensure_temp():
    """
    Ensures that the directories needed by the extension API are present.
    """

    global temp_exists

    if temp_exists:
        return

    backups = os.path.join(config.renpy_base, "tmp", "installer", "backups")

    if not os.path.exists(backups):
        os.makedirs(os.path.dirname(backups))

    temp_exists = True

# The target directory that the extensions API operates on.
target = None


def set_target(directory):
    """
    This sets the directory that the extension API targets. This is where
    packages are unpacked to and the default working directory where the
    programs are run.
    """

    global target
    target = directory


def _path(filename):
    """
    Returns the full path to `filename`. If `filename` starts with the
    prefix temp:, it's placed in the temp directory. If the filename
    starts with backup, a backup filename is returned. Otherwise,
    the path is interpreted relative to the target directory.
    """

    _ensure_temp()

    tempdir = os.path.join(config.renpy_base, "tmp", "installer")
    backups = os.path.join(config.renpy_base, "tmp", "installer", "backups")

    prefix, _, rest = filename.partition(":")

    if prefix == "temp":
        return os.path.join(tempdir, rest)

    if prefix == "backup":
        base = os.path.basename(rest.rpartition(":")[2])
        return os.path.join(backups, base + "." + str(time.time()))

    if target is None:
        raise Exception("The target directory has not been set.")

    return os.path.join(target, filename)

def _friendly(filename):
    """
    Returns a version of the filename without any leading prefix.
    """

    return filename.rpartition(":")[2]


def _check_hash(filename, hashj):
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
    download_file = _friendly(filename)

    filename = _path(filename)

    if hash is not None:
        if _check_hash(filename, hash):
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
                        _("Downloading [installer.download_file]..."),
                        complete=downloaded, total=total_size)

    except requests.HTTPError as e:
        interface.error(_("Could not download [installer.download_file] from [installer.download_url]:\n{b}[installer.download_error]"))

    if hash is not None:
        if not _check_hash(filename, hash):
            interface.error(_("The downloaded file [installer.download_file] from [installer.download_url] is not correct."))

class _FixedZipFile(zipfile.ZipFile):
    """
    Patches zipfile.zipfile so it sets the executable bit when necessary.
    """

    def extract(self, member, path=None, pwd=None):

        if not isinstance(member, zipfile.ZipInfo):
            member = self.getinfo(member)

        if path is None:
            path = os.getcwd()

        ret_val = self._extract_member(member, path, pwd) # type: ignore
        attr = member.external_attr >> 16

        if attr:
            os.chmod(ret_val, attr)

        return ret_val

# The name of the archive being unpacked.
unpack_archive = ""

def unpack(archive, destination):
    """
    Unpacks `archive` to `destination`. `archive` should be the name of
    a zip or (perhaps compressed) tar file. `destination` should be a
    directory that the contents are unpacked into.
    """

    global unpack_archive
    unpack_archive = _friendly(archive)

    interface.processing(_("Unpacking [installer.unpack_archive]..."))

    archive = _path(archive)
    destination = _path(destination)

    if not os.path.exists(destination):
        os.makedirs(destination)

    old_cwd = os.getcwd()

    try:

        os.chdir(destination)

        if tarfile.is_tarfile(archive):
            tar = tarfile.open(archive)
            tar.extractall(".")
            tar.close()

        elif zipfile.is_zipfile(archive):
            zip = _FixedZipFile(archive)
            zip.extractall(".")
            zip.close()

        else:
            raise Exception("Unknown file type.")

    finally:
        os.chdir(old_cwd)


def remove(filename):
    """
    Removes a file or directory from the target directory, backing it up
    the temporary directory.
    """

    shutil.move(_path(filename), _path("backup:" + filename))


def main():
    set_target("/tmp")
    download("https://code.visualstudio.com/sha/download?build=stable&os=linux-x64", "temp:vscode.tar.gz")
    remove("VSCode-linux-x64")
    unpack("temp:vscode.tar.gz", ".")
