# Copyright 2004-2024 Tom Rothamel <pytom@bishoujo.us>
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

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode # *

import argparse
import os
import time
import zlib

import requests

from . import download
from . import common

# Constants from 00updater.py.
PREPARING = "PREPARING"
DOWNLOADING = "DOWNLOADING"
UNPACKING = "UNPACKING"
FINISHING = "FINISHING"


class UpdateError(Exception):
    """
    Raised when an error happens.
    """

    pass

class Plan(object):
    """
    This represents a plan for updating a single segment.
    """

    def __init__(self, block, old_filename, old_offset, old_size, compressed, new_filename, new_offset, new_size, hash):
        # Is old_filename a blockfile that might need to be downloaded?
        self.block = block

        # The source filename, size, and offset.
        self.old_filename = old_filename
        self.old_offset = old_offset
        self.old_size = old_size

        # If true, the source information is compressed.
        self.compressed = compressed

        # The target filename, size, and offset.
        self.new_filename = new_filename
        self.new_offset = new_offset
        self.new_size = new_size

        # The hash.
        self.hash = hash

class Update(object):

    def __init__(self, url, newlists, targetdir, oldlists, progress_callback=None, logfile=None, aggressive_removal=False):
        """
        `url`
            The url that's used as a base to download pack files from.

        `newlists`
            A list of one or more new file lists.

        `targetdir`
            The directory to update.

        `oldlists`
            A list of one or more old file lists.

        `progress_callback`
            A function that's called to report progress. It takes two arguments,
            a message and a float between 0.0 and 1.0.

        `logfile`
            A file to log to. If None, a file is created in the target directory.

        `aggressive_removal`
            If true, files that are not in the new file list are removed as soon
            as they are no longer needed.
        """

        self.url = url

        self.targetdir = targetdir
        self.oldlists = oldlists
        self.newlists = newlists

        self.old_directories = [ i for j in self.oldlists for i in j.directories ]
        self.new_directories = [ i for j in self.newlists for i in j.directories ]
        self.new_files = [ i for j in self.newlists for i in j.files ]
        self.old_files = [ i for j in self.oldlists for i in j.files ]
        self.block_files = [ i for j in self.newlists for i in j.blocks ]

        # The total number of bytes that will be used on disk before and after
        # the update.

        self.old_disk_total = 0
        self.new_disk_total = 0

        # The total number of bytes to download, and the number of bytes downloaded.
        self.download_total = 0
        self.download_done = 0

        # The total number of bytes to write, and the number of bytes written.
        self.write_total = 0
        self.write_done = 0

        # A list of plan objects.
        self.plan = [ ]

        # A cache for the destination filename and file pointer.
        self.destination_filename = None
        self.destination_fp = None

        # Should removal of old files be done ASAP, or at the end?
        self.aggressive_removal = aggressive_removal

        # The progress callback.
        self.progress_callback = progress_callback

        # The set of files to remove.
        self.removals = set() # type: set[str]

        # The various directories.
        self.updatedir = os.path.join(self.targetdir, "update")
        self.blockdir = os.path.join(self.updatedir, "block")
        self.deleteddir = os.path.join(self.updatedir, "deleted")

        self.logfile = logfile

    def init(self):
        """
        Called to initialize the update.
        """

        def makedirs(dir):
            if not os.path.isdir(dir):
                os.makedirs(dir)

        makedirs(self.updatedir)
        makedirs(self.blockdir)
        makedirs(self.deleteddir)

        print("-" * 80, file=self.logfile)
        print("Starting update at %s." % time.ctime(), file=self.logfile)

        self.progress(PREPARING, 0.0)

        self.write_padding()
        self.find_incomplete_files()
        self.scan_old_files()
        self.prepare_new_files()
        self.find_removals()
        self.remove_identical_files()
        self.create_plan()
        self.compute_totals()

    def update(self):
        """
        Called to actually perform the update.
        """

        self.make_directories()
        self.execute_plan()


        if self.destination_fp is not None:
            self.destination_fp.close()

        self.progress(FINISHING, 0.0)

        self.create_empty_new_files()
        self.rename_new_files()
        self.remove_old_files()
        self.set_xbit()

    def progress(self, message, done):
        """
        Called to report progress.

        `message`
            A human readable message.

        `done`
            The amount of progress that is done, between 0.0 and 1.0.
        """

        if self.progress_callback is not None:
            self.progress_callback(message, done)
        else:
            print("Progress: %s: %.4f" % (message, 100.0 * done))

    def log(self, message, *args):
        if self.logfile is not None:
            print(message % args, file=self.logfile)

    def delete(self, filename):
        """
        Try very hard to delete `filename`. If it can't be deleted, move it
        to the deleted directory, to be cleaned up the next time the game
        starts.
        """

        if not os.path.exists(filename):
            return

        try:
            os.unlink(filename)
            return
        except:
            pass

        basename = os.path.basename(filename)

        serial = 0

        while True:
            serial += 1
            new = os.path.join(self.deleteddir, "%s.delete.%d.rpu" % (basename, serial))

            if not os.path.exists(new):
                os.rename(filename, new)
                break

    def rename(self, old, new):
        try:
            os.rename(old, new)
        except:
            self.delete(new)
            os.rename(old, new)

    def make_directories(self):
        """
        Creates the directories in self.new_directories.
        """

        directories = list(self.new_directories)
        directories.sort(key=lambda i : i.name)

        for d in directories:
            if not os.path.exists(os.path.join(self.targetdir, d.name)):
                os.makedirs(os.path.join(self.targetdir, d.name))

    def find_incomplete_files(self):
        """
        Scan a directory, recursively, and add the files and directories
        found to this file test. This is intended for testing. This does
        not call .scan on the files.
        """

        root = self.targetdir

        for dn, dirs, files in os.walk(root):

            for fn in files:
                fn = os.path.join(dn, fn)

                if not fn.endswith(".new.rpu"):
                    continue

                oldfn = fn[:-len(".new.rpu")] + ".old.rpu"
                self.rename(fn, oldfn)

                relfn = os.path.relpath(oldfn, root)
                f = common.File(relfn, data_filename=oldfn)
                self.old_files.append(f)

    def write_padding(self):
        """
        Writes a file containing the padding for RPAs, so it's
        not necessary to download a block file just for that.
        """

        padding = b"Made with Ren'Py."

        fn = os.path.join(self.targetdir, "_padding.old.rpa")
        with open(fn, "wb") as f:
            f.write(padding)

        f = common.File("_padding.old.rpa", data_filename=fn)
        self.old_files.append(f)

    def scan_old_files(self):
        """
        Scans the old files, generating a list of segments.
        """

        total = 0
        done = 0

        existing = [ ]

        for i in self.old_files:
            i.add_data_filename(self.targetdir)

            if not os.path.exists(i.data_filename):
                continue

            existing.append(i)
            total += os.path.getsize(i.data_filename)

        self.old_files = existing

        total = max(1, total)

        for i in self.old_files:
            i.scan()
            done += os.path.getsize(i.data_filename)

            self.progress(PREPARING, done / total)

        self.old_disk_total = done


    def prepare_new_files(self):
        """
        Prepares the new files.
        """

        self.new_disk_total = 0

        for i in self.new_files:
            i.add_data_filename(self.targetdir)

            for s in i.segments:
                self.new_disk_total += s.size

    def remove_identical_files(self):
        """
        Removes from self.source_files any file that exists and is identical
        to the file in self.target_files.
        """

        old_by_name = { i.name : i for i in self.old_files }

        new_files = [ ]

        self.log("Removing identical files:")

        for f in self.new_files:
            if f.name not in old_by_name:
                new_files.append(f)
                self.log("  new     %s", f.name)
                continue

            if f.segments != old_by_name[f.name].segments:
                new_files.append(f)
                self.log("  changed %s", f.name)
                continue

            self.log("  same    %s", f.name)

        self.log("%d files are unchanged.", len(self.new_files) - len(new_files))
        self.log("%d files are new/changed.", len(new_files))

        self.new_files = new_files

    def create_plan(self):
        """
        Creates the plan for updating everything, by finding each missing
        segment and creating a plan object.
        """

        # A map from segment hash to (block, file, segment) tuples.
        segment_locations = { }

        for f in sorted(self.block_files, key=lambda i : i.mtime):
            for s in f.segments:
                segment_locations[s.hash] = (True, f, s)

        for f in sorted(self.old_files, key=lambda i : i.mtime):
            for s in f.segments:
                segment_locations[s.hash] = (False, f, s)

        plan = [ ]

        for target_file in self.new_files:

            for target_segment in target_file.segments:
                block, source_file, source_segment = segment_locations.get(target_segment.hash, (False, None, None))

                if source_file is None:
                    self.log("Segment %s was not found.", target_segment.hash)
                    raise Exception("Segment %s was not found in index.")

                plan.append(Plan(
                    block,
                    source_file.data_filename or source_file.name,
                    source_segment.offset,
                    source_segment.size,
                    source_segment.compressed,
                    target_file.data_filename,
                    target_segment.offset,
                    target_segment.size,
                    target_segment.hash,
                    ))

        plan.sort(key=lambda p : (p.block, p.old_filename, p.old_offset, p.old_size))

        self.log("Created a plan with %d entries.", len(plan))

        self.plan = plan

    def compute_totals(self):
        """
        Computes the total number of bytes to download and write.
        """

        self.download_total = 0
        self.write_total = 0

        download_set = set()

        for p in self.plan:
            self.write_total += p.new_size

            if p.block:

                key = (p.old_filename, p.old_offset, p.old_size)

                if key not in download_set:
                    download_set.add(key)
                    self.download_total += p.old_size


        # Make sure we can't divide by zero.
        self.download_total = max(self.download_total, 1)
        self.write_total = max(self.write_total, 1)

    def find_removals(self):
        """
        Find the set of files that exist in old but not in new.
        """

        old = { i.data_filename for i in self.old_files }
        new = { i.data_filename for i in self.new_files }

        self.removals = old - new

    def write_destination(self, filename, offset, data):
        """
        Writes data to the destination file at the given offset.
        """

        filename = filename + ".new.rpu"

        if self.destination_filename != filename:
            if self.destination_fp is not None:
                self.destination_fp.close()

            self.destination_filename = filename
            if os.path.exists(filename):
                self.destination_fp = open(os.path.join(self.targetdir, filename), "r+b")
            else:
                self.destination_fp = open(os.path.join(self.targetdir, filename), "wb")

        self.destination_fp.seek(offset)
        self.destination_fp.write(data)

        self.write_done += len(data)
        self.download_patch_progress()

    def download_patch_progress(self):

        done = 0.5 * self.download_done / self.download_total
        done += 0.5 * self.write_done / self.write_total

        done = min(done, 1.0)

        self.progress(DOWNLOADING, done)

    def download_block_file(self, filename, plan):
        """
        Downloads the portions of the block file that are needed.
        """

        ranges = { (i.old_offset, i.old_size) for i in plan }
        ranges = list(ranges)

        url = self.url + "/" + filename
        filename = os.path.join(self.targetdir, "update", filename)

        old_download_done = self.download_done

        def download_progress(done, total):
            self.download_done = old_download_done + done
            self.download_patch_progress()

        download.download(url, ranges, filename, download_progress)

        return filename

    def execute_file_plan(self, plan):
        """
        This executes the plan for one source file.
        """

        old_filename = plan[0].old_filename
        block = plan[0].block

        if block:
            old_filename = self.download_block_file(old_filename, plan)

        # From here on, source_filename must point to a complete file on disk.

        with open(old_filename, "rb") as f:

            hash = None
            data = b''

            for p in plan:

                self.log("%s (%d, %d)\n  -> %s (%d, %d) %s", p.old_filename, p.old_offset, p.old_size, p.new_filename, p.new_offset, p.new_size, "compressed" if p.compressed else "")

                if hash != p.hash:
                    f.seek(p.old_offset)
                    data = f.read(p.old_size)

                    if p.compressed == common.COMPRESS_ZLIB:
                        data = zlib.decompress(data)

                    hash = common.hash_data(data)

                    if hash != p.hash:
                        self.log("Hash mismatch on %s offset %d size %d.", p.old_filename, p.old_offset, p.old_size)
                        raise UpdateError("Hash mismatch on %s offset %d size %d." % (p.old_filename, p.old_offset, p.old_size))

                self.write_destination(p.new_filename, p.new_offset, data)

        if block:
            self.log("Blockfile delete %s.", old_filename)
            self.delete(old_filename)
        else:
            if self.aggressive_removal and old_filename in self.removals:
                self.log("Aggressively delete %s.", old_filename)
                self.delete(old_filename)

    def execute_plan(self):
        """
        This executes the full plan, one file at a time.
        """

        queue = [ ]
        old_key = (False, None)

        for p in self.plan:
            key = (p.block, p.old_filename)

            if key != old_key:
                if queue:
                    self.execute_file_plan(queue)

                queue = [ ]

                old_key = key

            queue.append(p)

        if queue:
            self.execute_file_plan(queue)

    def create_empty_new_files(self):
        """
        Creates new files that do not have any data.
        """

        for i in self.new_files:
            if not i.segments:
                self.log("Create empty file %s.", i.data_filename)
                with open(i.data_filename + ".new.rpu", "wb") as f:
                    pass

    def rename_new_files(self):
        """
        Renames the new files to final names.
        """

        for f in self.new_files:
            filename = os.path.join(self.targetdir, f.name)
            if os.path.exists(filename + ".new.rpu"):
                self.rename(filename + ".new.rpu", filename)

    def remove_old_files(self):
        """
        Removes the old files and directories.
        """

        for i in self.removals:
            self.log("Final delete %s.", i)
            self.delete(i)

        directories = set(i.name for i in self.old_directories) - set(i.name for i in self.new_directories)

        for i in reversed(sorted(directories)):
            self.log("Remove directory %s.", i)
            try:
                os.rmdir(os.path.join(self.targetdir, i))
            except:
                pass

    def set_xbit(self):
        """
        Sets the executable bit on files that require it.
        """

        for i in self.new_files:
            if i.xbit:
                try:
                    os.chmod(i.data_filename, 0o755)
                except:
                    raise UpdateError("Could not set the executable bit on %s." % i.data_filename)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("targetdir")

    args = ap.parse_args()

    targetlist = common.FileList()
    targetlist.scan(args.targetdir, data_filename=False)

    resp = requests.get(args.url + "/game.files.rpu")
    sourcelist = common.FileList.decode(resp.content)

    Update(args.url, [ sourcelist ], args.targetdir, [ targetlist ])

if __name__ == "__main__":
    main()
