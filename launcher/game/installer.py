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

import hashlib
import os
import time
import requests
import zipfile
import tarfile
import shutil
import subprocess
import renpy
import stat

VERSION = 1

# True if the installer should run in quiet mode.
quiet = False

from store import _, config, interface, project, Jump # type: ignore

temp_exists = False

def _ensure_temp():
    """
    Ensures that the directories needed by the extension API are present.
    """

    global temp_exists

    if temp_exists:
        return

    backups = os.path.join(config.renpy_base, "tmp", "installer", "backups")

    try:
        if not os.path.exists(backups):
            os.makedirs(os.path.dirname(backups))
    except Exception:
        pass

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

    _clean("temp:", 3)


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

    if prefix == "renpy":
        return os.path.join(config.renpy_base, rest)

    if target is None:
        raise Exception("The target directory has not been set.")

    return os.path.join(target, filename)


def _clean(directory, age=3):
    """
    Removes files from `directory` that are older than `age` days.
    """

    directory = _path(directory)

    for root, dirs, files in os.walk(directory, topdown=False):
        for f in files:
            filename = os.path.join(root, f)
            mtime = os.stat(filename).st_mtime
            if time.time() - mtime > age * 86400:
                try:
                    os.unlink(filename)
                except Exception:
                    pass


        if root != directory:

            try:
                os.rmdir(root)
            except Exception:
                pass


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
                    if not quiet:
                        interface.processing(
                            _("Downloading [installer.download_file]..."),
                            complete=downloaded, total=total_size)

    except requests.HTTPError as e:
        if not quiet:
            raise

        interface.error(_("Could not download [installer.download_file] from [installer.download_url]:\n{b}[installer.download_error]"))

    if hash is not None:
        if not quiet:
            raise Exception("Hash check failed.")
        if not _check_hash(filename, hash):
            interface.error(_("The downloaded file [installer.download_file] from [installer.download_url] is not correct."))

class _FixedZipFile(zipfile.ZipFile):
    """
    A patched version of zipfile.ZipFile that adds support for:

    * Unix permissions bits.
    * Unix symbolic links.
    """

    def _extract_member(self, member, targetpath, pwd):

        if not isinstance(member, zipfile.ZipInfo):
            member = self.getinfo(member)

        # build the destination pathname, replacing
        # forward slashes to platform specific separators.
        arcname = member.filename.replace('/', os.path.sep)

        if os.path.altsep:
            arcname = arcname.replace(os.path.altsep, os.path.sep)
        # interpret absolute pathname as relative, remove drive letter or
        # UNC path, redundant separators, "." and ".." components.
        arcname = os.path.splitdrive(arcname)[1]
        invalid_path_parts = ('', os.path.curdir, os.path.pardir)
        arcname = os.path.sep.join(x for x in arcname.split(os.path.sep) if x not in invalid_path_parts)

        targetpath = os.path.join(targetpath, arcname)
        targetpath = os.path.normpath(targetpath)

        # Create all upper directories if necessary.
        upperdirs = os.path.dirname(targetpath)
        if upperdirs and not os.path.exists(upperdirs):
            os.makedirs(upperdirs)

        if member.filename.endswith("/"):
            if not os.path.isdir(targetpath):
                os.mkdir(targetpath)
            return targetpath

        attr = member.external_attr >> 16

        if stat.S_ISLNK(attr):

            with self.open(member, pwd=pwd) as source:
                linkto = source.read()

            os.symlink(linkto, targetpath)

        else:

            with self.open(member, pwd=pwd) as source, open(targetpath, "wb") as target:
                shutil.copyfileobj(source, target)

            if attr:
                os.chmod(targetpath, attr)

        return targetpath


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

    if not quiet:
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


def exists(filename):
    """
    Returns true if `filename` exists.
    """

    return os.path.exists(_path(filename))


def remove(filename):
    """
    Removes a file or directory from the target directory, backing it up
    the temporary directory.
    """

    if not exists(filename):
        return

    backup = _path("backup:" + filename)
    shutil.move(_path(filename), backup)

    # Now, touch everything so _cleanup doesn't get it too quickly.

    if os.path.isdir(backup):
        for root, dirs, files in os.walk(backup):
            for f in files:
                try:
                    os.utime(os.path.join(root, f), None)
                except Exception:
                    pass
    else:
        try:
            os.utime(backup, None)
        except Exception:
            pass

def move(old_filename, new_filename):
    """
    Moves a filename from `old_filename` to `new_filename`.
    """

    remove(new_filename)
    shutil.move(_path(old_filename), _path(new_filename))


def mkdir(dirname):
    """
    Makes the named directory.
    """

    if not os.path.exists(_path(dirname)):
        os.makedirs(_path(dirname))


def info(message, **kwargs):
    """
    Displays `message` to the user, asking them to click through or
    cancel.
    """

    interface.info(message, cancel=Jump("front_page"), **kwargs)


def processing(message, **kwargs):
    """
    Displays `message` to the user, without waiting.
    """

    interface.processing(message, **kwargs)


def error(message, **kwargs):
    """
    Displays `message` to the user, as an error.
    """

    interface.error(message)


install_args = [ ]
install_error = ""

def run(*args, **kwargs):
    """
    Runs a program with the given arguments, in the target directory.
    """

    environ = { renpy.exports.fsencode(k) : renpy.exports.fsencode(v) for k, v in os.environ.items() }

    for k, v in kwargs.pop("environ", {}).items():
        environ[renpy.exports.fsencode(k)] = renpy.exports.fsencode(v)

    global install_args
    global install_error

    args = [ renpy.exports.fsencode(i) for i in args ]

    try:
        subprocess.check_call(args, cwd=target, env=environ) # type: ignore
    except Exception as e:
        install_args = args
        install_error = str(e)

        interface.error(_("Could not run [installer.install_args!r]:\n[installer.install_error]"))


_renpy = renpy

def manifest(url, renpy=False, insecure=False):
    """
    Executes the manifest at `url`.

    `renpy`
        If true, the manifest applies to Ren'Py. If False, the manifest applies
        to the current project.

    `insecure`
        If true, verificaiton is disabled.
    """

    import ecdsa

    download(url, "temp:manifest.py")

    with open(_path("temp:manifest.py"), "rb") as f:
        manifest = f.read()

    if not insecure:
        download(url + ".sig", "temp:manifest.py.sig")

        with open(_path("temp:manifest.py.sig"), "rb") as f:
            sig = f.read()

        key = ecdsa.VerifyingKey.from_pem(_renpy.exports.file("renpy_ecdsa_public.pem").read())

        if not key.verify(sig, manifest):
            error(_("The manifest signature is not valid."))
            return

    if renpy:
        set_target(config.renpy_base)
    else:
        if project.current is None:
            error(_("No project has been selected."))
            return

        set_target(project.current.path)

    exec(manifest.decode("utf-8"), {}, {})


def local_manifest(filename, renpy=False):
    """
    Executes the manifest in `filename`.

    `renpy`
        If true, the manifest applies to Ren'Py. If False, the manifest applies
        to the current project.
    """

    if renpy:
        set_target(config.renpy_base)
    else:
        if project.current is None:
            error(_("No project has been selected."))
            return

        set_target(project.current.path)

    with open(filename, "r") as f:
        exec(f.read(), {}, {})
