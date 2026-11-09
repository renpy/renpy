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

import renpy
import os
import shutil
import stat

# Added to the name of a directory being repaired, to get the name of the
# sibling directories that exist while repair_directory runs. They hold a copy
# being built, and the original once it has been replaced, respectively. These
# names are distinctive because repair_directory deletes them.
REPAIR_SUFFIX = ".renpy-repair"
REPLACED_SUFFIX = ".renpy-replaced"


def is_setgid(path):
    """
    Returns True if `path` has the set-group-ID bit.
    """

    return bool(os.stat(path).st_mode & stat.S_ISGID)


def is_shared_with_group(path):
    """
    Returns True if the directory `path` has the set-group-ID bit and its group
    has full access, so that what's created inside can be used by that group.
    """

    mode = os.stat(path).st_mode
    return bool(mode & stat.S_ISGID) and (mode & stat.S_IRWXG) == stat.S_IRWXG


def copy_into_setgid_directory(src, dst):
    """
    Copies the contents of the directory `src` into the existing setgid
    directory `dst`, so that what's created takes the group of `dst`. Files
    are flushed to disk and keep their modification times.

    Raises OSError on failure, including when `src` contains anything other
    than files and directories, which would otherwise be lost.
    """

    with os.scandir(src) as entries:
        for entry in entries:
            target = os.path.join(dst, entry.name)

            if entry.is_dir(follow_symlinks=False):
                # This has to stay a plain mkdir, as the directory inherits
                # setgid and a chmod (or shutil.copystat) would clear it.
                os.mkdir(target)
                copy_into_setgid_directory(entry.path, target)

            elif entry.is_file(follow_symlinks=False):
                shutil.copyfile(entry.path, target)
                expose_file(target)

                info = entry.stat(follow_symlinks=False)
                os.utime(target, ns=(info.st_atime_ns, info.st_mtime_ns))

                with open(target, "rb") as f:
                    os.fsync(f.fileno())

            else:
                raise OSError(f"{entry.path} is not a file or directory.")


def contains_copy_of(copy, original):
    """
    Returns True if every file in the directory `original` is also in `copy`,
    at the same relative path and with the same size. This is the check that
    has to pass before `original` can be deleted.
    """

    with os.scandir(original) as entries:
        for entry in entries:
            target = os.path.join(copy, entry.name)

            if entry.is_dir(follow_symlinks=False):
                if not os.path.isdir(target) or not contains_copy_of(target, entry.path):
                    return False

            elif not os.path.isfile(target) or os.path.getsize(target) != entry.stat(follow_symlinks=False).st_size:
                return False

    return True


def rebuild_directory(dn):
    """
    Implements repair_directory, raising an exception if the repair fails. See
    that function for the reasons this is needed.

    The original directory is only removed once a complete copy has replaced
    it, and an interrupted run is finished the next time this is called. The
    states, and what's done about them, are:

    * Only the repair directory exists beside `dn`: a copy was interrupted, so
      it's discarded and the repair starts over.
    * `dn` is missing, and the replaced directory exists: the swap was
      interrupted, so it's finished using the complete copy, or undone if
      there isn't one.
    * `dn` is setgid and holds everything in the replaced directory, which
      exists: only the deletion of the original was interrupted, so it's
      finished.

    In any other state with a replaced directory, something other than this
    function created `dn`, so nothing is deleted.
    """

    dn = os.path.abspath(dn)
    repair = dn + REPAIR_SUFFIX
    replaced = dn + REPLACED_SUFFIX

    if os.path.lexists(replaced) and not os.path.lexists(dn):
        os.rename(repair if os.path.lexists(repair) else replaced, dn)

    if os.path.lexists(replaced):
        if is_setgid(dn) and not os.path.lexists(repair) and contains_copy_of(dn, replaced):
            shutil.rmtree(replaced, ignore_errors=True)

        return

    if os.path.islink(dn) or not os.path.isdir(dn):
        return

    if is_shared_with_group(dn) or not is_setgid(os.path.dirname(dn)):
        return

    if os.path.lexists(repair):
        shutil.rmtree(repair)

    os.mkdir(repair)

    try:
        # The new directory is only useful if it inherited setgid and got group
        # access from the umask or a default ACL. Neither can be added after
        # the fact. Checking also ensures the repair can't repeat every launch.
        if not is_shared_with_group(repair):
            raise OSError(f"{repair} was created with mode {stat.S_IMODE(os.stat(repair).st_mode):o}.")

        copy_into_setgid_directory(dn, repair)

        os.rename(dn, replaced)

        try:
            os.rename(repair, dn)
        except Exception:
            os.rename(replaced, dn)
            raise

    except Exception:
        # If undoing the swap failed, the copy is complete, so it's kept. The
        # next call finishes the swap with it, unless something has recreated
        # dn by then. In that case, both directories are kept, undeleted.
        if os.path.lexists(dn) and not os.path.lexists(replaced):
            shutil.rmtree(repair, ignore_errors=True)

        raise

    shutil.rmtree(replaced, ignore_errors=True)

    renpy.display.log.write("Restored the group of %s.", dn)


def repair_directory(dn):
    """
    Repairs a directory in a setgid parent on Android that lost its setgid bit,
    as older versions of Ren'Py did, or that its group can't access. Files in
    a directory without the bit have the app's own group, rather than
    ext_data_rw, and can't be read by adb and storage tools.

    The app isn't in ext_data_rw, so it can't change the group of a file, and
    chmod would clear the bit rather than set it. What it can do is make a new
    directory in a setgid parent,
    which inherits the group and the bit, so `dn` is replaced by a copy made
    that way. Renaming isn't enough, as it keeps the group of each file.

    This has to be called before anything can create `dn`, so that it can finish
    a repair that was interrupted while `dn` was missing. It does nothing except
    on Android. Failures are logged, and leave `dn` as it was, unless both moving
    the copy into place and moving `dn` back failed.
    """

    if not renpy.android:
        return

    try:
        rebuild_directory(dn)
    except Exception:
        renpy.display.log.write("Could not restore the group of %s:", dn)
        renpy.display.log.exception()


def expose_file(fn):
    """
    Ensures that `fn` can be read and written by the user, on platforms where
    that may not be the default.
    """

    if renpy.android:
        try:
            os.chmod(fn, 0o660)
        except Exception:
            pass


def expose_directory(dn):
    """
    Ensures that `dn` can be read and written by the user, on platforms where
    that may not be the default.

    On Android, a setgid directory is left alone. Android creates app directories
    on external storage with the setgid bit and the ext_data_rw group, so that
    what's created inside them can be read by adb and storage tools. The app
    isn't in that group, so the kernel would clear the bit on any chmod, even
    one with a mode that includes it. Group access to a setgid directory comes
    from the umask when it's created, and repair_directory fixes those without.
    """

    if renpy.android:
        try:
            if not (os.stat(dn).st_mode & stat.S_ISGID):
                os.chmod(dn, 0o770)
        except Exception:
            pass
